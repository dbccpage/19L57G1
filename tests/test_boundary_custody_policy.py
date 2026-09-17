"""Temporary-repository refusal/recovery checks for the author amendment."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research/boundary_seed"))
import verify_freeze as freeze


class CustodyPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
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
        freeze.git(self.root, "add", "--all")
        freeze.git(self.root, "-c", "user.name=Custody test", "-c",
                   "user.email=test@example.invalid", "-c", "commit.gpgsign=false",
                   "commit", "-qm", message)

    def head(self) -> str:
        return freeze.git(self.root, "rev-parse", "HEAD").decode().strip()

    def oid(self, path: str, revision: str = "HEAD:") -> str:
        return freeze.git(self.root, "rev-parse", revision + path).decode().strip()

    def save_policy(self) -> None:
        self.write(freeze.POLICY, (json.dumps(self.policy, indent=2) + "\n").encode())

    def refused(self, needle: str) -> None:
        result = freeze.audit(self.root)
        self.assertFalse(result.frozen)
        self.assertIn(needle, "\n".join(result.problems))

    def test_valid_amendment_keeps_acknowledged_history_visible(self) -> None:
        result = freeze.audit(self.root)
        self.assertEqual(len(result.acknowledged), 1)
        self.assertIn(self.base, result.acknowledged[0])
        self.assertTrue(result.frozen)

    def test_untracked_extra_source_is_refused_then_recovers(self) -> None:
        path = f"{freeze.REL}/unapproved.py"
        self.write(path, b"unapproved\n")
        self.refused(path)
        (self.root / path).unlink()
        self.assertTrue(freeze.audit(self.root).frozen)

    def test_each_approved_path_still_has_exact_working_bytes(self) -> None:
        for path in sorted(freeze.APPARATUS | {freeze.CHECKER}):
            original = (self.root / path).read_bytes()
            self.write(path, original + b"changed\n")
            self.refused(f"working:{path}")
            self.write(path, original)
            self.assertTrue(freeze.audit(self.root).frozen)

    def test_staged_change_hidden_by_clean_working_copy_is_refused(self) -> None:
        path = freeze.CHECKER
        original = (self.root / path).read_bytes()
        self.write(path, b"staged replacement\n")
        freeze.git(self.root, "add", "--", path)
        self.write(path, original)
        self.refused(f"INDEX:{path}")

    def test_source_edit_and_reversion_remain_historical_failures(self) -> None:
        path = f"{freeze.REL}/source.txt"
        self.write(path, b"changed source\n")
        self.commit("forbidden source revision")
        self.write(path, b"original source\n")
        self.commit("revert does not erase history")
        self.refused(path)

    def test_removing_policy_cannot_make_original_freeze_pass(self) -> None:
        (self.root / freeze.POLICY).unlink()
        self.commit("remove amendment")
        self.refused("source changed after freeze")

    def test_uncommitted_policy_edit_is_not_authority(self) -> None:
        self.write(freeze.POLICY, b"{}\n")
        self.refused("differs between HEAD, index and working")

    def test_duplicate_keys_are_rejected(self) -> None:
        data = (self.root / freeze.POLICY).read_bytes()
        self.write(freeze.POLICY, data.replace(b'{', b'{"schema":"duplicate",', 1))
        self.commit("duplicate policy key")
        self.refused("duplicate custody policy key")

    def test_wrong_historical_blob_does_not_waive_change(self) -> None:
        history = self.policy["historical_exceptions"]
        history[self.base][sorted(freeze.APPARATUS)[0]] = self.oid(freeze.CHECKER)
        self.save_policy()
        self.commit("wrong historical blob")
        self.refused("source changed after freeze")

    def test_path_wildcard_is_not_an_exception(self) -> None:
        self.policy["current_blobs"][f"{freeze.REL}/*"] = self.oid(freeze.CHECKER)
        self.save_policy()
        self.commit("unsupported broad permission")
        self.refused("path census differs")

    def test_nonexact_baseline_is_refused(self) -> None:
        self.policy["baseline"] = "HEAD"
        self.save_policy()
        self.commit("moving policy anchor")
        self.refused("exact commit")

    def test_mode_change_is_not_covered_by_byte_permission(self) -> None:
        freeze.git(self.root, "update-index", "--chmod=+x", "--", freeze.CHECKER)
        self.refused("INDEX:")


if __name__ == "__main__":
    unittest.main()
