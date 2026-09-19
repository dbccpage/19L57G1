"""Temporary-repository refusal/recovery checks for the author amendment."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType
import unittest

# The checker is loaded by path inside setUpClass, not at collection.  A
# missing or broken research file then fails these tests by naming that file,
# instead of interrupting collection of the whole root suite, and sys.path is
# left untouched, so the tree's other top-level modules shadow nothing for the
# rest of the session.
FREEZE_REL = "research/boundary_seed/verify_freeze.py"
FREEZE_PATH = Path(__file__).resolve().parents[1] / FREEZE_REL
# Private module name: the checker's frozen dataclasses resolve their string
# annotations through sys.modules, so it must be registered while it runs.
FREEZE_MODULE = "_boundary_seed_verify_freeze"


def load_freeze() -> ModuleType:
    if not FREEZE_PATH.is_file():
        raise ImportError(f"custody tests cannot load {FREEZE_REL}: no such file at {FREEZE_PATH}")
    spec = importlib.util.spec_from_file_location(FREEZE_MODULE, FREEZE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"custody tests cannot load {FREEZE_REL}: no module spec for {FREEZE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[FREEZE_MODULE] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        sys.modules.pop(FREEZE_MODULE, None)
        raise ImportError(
            f"custody tests cannot load {FREEZE_REL}: {type(exc).__name__}: {exc}"
        ) from exc
    return module


class CustodyPolicyTests(unittest.TestCase):
    freeze: ModuleType

    @classmethod
    def setUpClass(cls) -> None:
        cls.freeze = load_freeze()
        cls.addClassCleanup(sys.modules.pop, FREEZE_MODULE, None)

    def setUp(self) -> None:
        freeze = self.freeze
        self.temp = tempfile.TemporaryDirectory(prefix="custody-policy-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        freeze.git(self.root, "init", "-q")
        self.write(f"{freeze.REL}/.gitattributes", b"FREEZE.md -text\n")
        self.write(f"{freeze.REL}/source.txt", b"original source\n")
        self.write(freeze.CHECKER, b"original checker\n")
        self.commit("source")
        freeze.write_marker(self.root)
        self.commit("dedicated freeze")
        self.marker = self.head()
        self.assertTrue(freeze.audit(self.root).frozen)
        for path in freeze.APPARATUS:
            self.write(path, b"post-freeze apparatus\n")
        self.commit("historical breach")
        self.base = self.head()
        self.assertFalse(freeze.audit(self.root).frozen)
        historical = {p: self.oid(p) for p in sorted(freeze.APPARATUS)}
        self.write(freeze.CHECKER, b"amended checker\n")
        freeze.git(self.root, "add", "--", freeze.CHECKER)
        current = historical | {freeze.CHECKER: self.oid(freeze.CHECKER, ":")}
        self.policy = {
            "schema": "boundary-custody-amendment-v1",
            "freeze": self.marker,
            "baseline": self.base,
            "historical_exceptions": {self.base: historical},
            "current_blobs": current,
        }
        self.save_policy()
        self.commit("authorized amendment")
        self.assertTrue(freeze.audit(self.root).frozen, freeze.audit(self.root).problems)

    def write(self, path: str, data: bytes) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def commit(self, message: str) -> None:
        # Only a new, isolated test repository is staged in full.
        self.freeze.git(self.root, "add", "--all")
        self.freeze.git(self.root, "-c", "user.name=Custody test", "-c",
                        "user.email=test@example.invalid", "-c", "commit.gpgsign=false",
                        "commit", "-qm", message)

    def head(self) -> str:
        return self.freeze.git(self.root, "rev-parse", "HEAD").decode().strip()

    def oid(self, path: str, revision: str = "HEAD:") -> str:
        return self.freeze.git(self.root, "rev-parse", revision + path).decode().strip()

    def save_policy(self) -> None:
        self.write(self.freeze.POLICY, (json.dumps(self.policy, indent=2) + "\n").encode())

    def refused(self, needle: str) -> None:
        result = self.freeze.audit(self.root)
        self.assertFalse(result.frozen)
        self.assertIn(needle, "\n".join(result.problems))

    def test_valid_amendment_keeps_acknowledged_history_visible(self) -> None:
        result = self.freeze.audit(self.root)
        self.assertEqual(len(result.acknowledged), 1)
        self.assertIn(self.base, result.acknowledged[0])
        self.assertTrue(result.frozen)

    def test_untracked_extra_source_is_refused_then_recovers(self) -> None:
        path = f"{self.freeze.REL}/unapproved.py"
        self.write(path, b"unapproved\n")
        self.refused(path)
        (self.root / path).unlink()
        self.assertTrue(self.freeze.audit(self.root).frozen)

    def test_each_approved_path_still_has_exact_working_bytes(self) -> None:
        for path in sorted(self.freeze.APPARATUS | {self.freeze.CHECKER}):
            original = (self.root / path).read_bytes()
            self.write(path, original + b"changed\n")
            self.refused(f"working:{path}")
            self.write(path, original)
            self.assertTrue(self.freeze.audit(self.root).frozen)

    def test_staged_change_hidden_by_clean_working_copy_is_refused(self) -> None:
        path = self.freeze.CHECKER
        original = (self.root / path).read_bytes()
        self.write(path, b"staged replacement\n")
        self.freeze.git(self.root, "add", "--", path)
        self.write(path, original)
        self.refused(f"INDEX:{path}")

    def test_source_edit_and_reversion_remain_historical_failures(self) -> None:
        path = f"{self.freeze.REL}/source.txt"
        self.write(path, b"changed source\n")
        self.commit("forbidden source revision")
        self.write(path, b"original source\n")
        self.commit("revert does not erase history")
        self.refused(path)

    def test_removing_policy_cannot_make_original_freeze_pass(self) -> None:
        (self.root / self.freeze.POLICY).unlink()
        self.commit("remove amendment")
        self.refused("source changed after freeze")

    def test_uncommitted_policy_edit_is_not_authority(self) -> None:
        self.write(self.freeze.POLICY, b"{}\n")
        self.refused("differs between HEAD, index and working")

    def test_duplicate_keys_are_rejected(self) -> None:
        data = (self.root / self.freeze.POLICY).read_bytes()
        self.write(self.freeze.POLICY, data.replace(b'{', b'{"schema":"duplicate",', 1))
        self.commit("duplicate policy key")
        self.refused("duplicate custody policy key")

    def test_wrong_historical_blob_does_not_waive_change(self) -> None:
        history = self.policy["historical_exceptions"]
        history[self.base][sorted(self.freeze.APPARATUS)[0]] = self.oid(self.freeze.CHECKER)
        self.save_policy()
        self.commit("wrong historical blob")
        self.refused("source changed after freeze")

    def test_path_wildcard_is_not_an_exception(self) -> None:
        self.policy["current_blobs"][f"{self.freeze.REL}/*"] = self.oid(self.freeze.CHECKER)
        self.save_policy()
        self.commit("unsupported broad permission")
        self.refused("path census differs")

    def test_nonexact_baseline_is_refused(self) -> None:
        self.policy["baseline"] = "HEAD"
        self.save_policy()
        self.commit("moving policy anchor")
        self.refused("exact commit")

    def test_mode_change_is_not_covered_by_byte_permission(self) -> None:
        self.freeze.git(self.root, "update-index", "--chmod=+x", "--", self.freeze.CHECKER)
        self.refused("INDEX:")


if __name__ == "__main__":
    unittest.main()
