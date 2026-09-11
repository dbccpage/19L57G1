"""Custody failures injected into temporary fixtures, never sealed originals."""

from __future__ import annotations

import hashlib
from importlib.machinery import ModuleSpec
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import ModuleType
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verify_sources as guard  # noqa: E402

UNCONSUMED = ("prompt/input.md", "paper/claim.md", "artifacts/other.json")


def git(root: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
    ).stdout


class Fixture:
    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "fixture"
        self.root.mkdir()
        root = self.root
        git(root, "init", "--quiet")
        git(root, "config", "core.autocrlf", "false")
        git(root, "config", "user.name", "Custody fixture")
        git(root, "config", "user.email", "fixture@example.invalid")
        for relative in (
            *guard.RUNTIME_PATHS.values(),
            *guard.CONFIG_PATHS,
            "lean4/Derivation/Example.lean",
            *UNCONSUMED,
        ):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"# fixture source\n")
        git(root, "add", "--", *guard.CONSUMED_TREES, *guard.CONFIG_PATHS, *UNCONSUMED)
        git(root, "commit", "--quiet", "-m", "Fixture baseline")
        self.baseline = git(root, "rev-parse", "HEAD").decode().strip()
        self.original_baseline = guard.BASELINE_COMMIT
        guard.BASELINE_COMMIT = self.baseline
        manifest = {
            "schema": guard.SCHEMA,
            "baseline_commit": self.baseline,
            "text_normalization": "CRLF_TO_LF_ONLY",
            "runtime_modules": guard.RUNTIME_PATHS,
            "consumed_trees": {
                tree: git(root, "rev-parse", f"{self.baseline}:{tree}").decode().strip()
                for tree in guard.CONSUMED_TREES
            },
            "tree_census": {
                tree: guard.tree_census(root, tree, suffix)[0]
                for tree, suffix in guard.CONSUMED_TREES.items()
            },
            "source_sha256": {
                path: hashlib.sha256(
                    git(root, "show", f"{self.baseline}:{path}")
                ).hexdigest()
                for path in (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS)
            },
            "artifact_sha256": {},
        }
        packet = root / guard.PACKET
        packet.mkdir(parents=True)
        self.manifest_path = packet / "SOURCE_MANIFEST.json"
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    def close(self) -> None:
        guard.BASELINE_COMMIT = self.original_baseline
        self.tmp.cleanup()

    def check(self) -> list[str]:
        return guard.verify_sources(self.root, check_runtime=False)


class CustodyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = Fixture()
        self.root = self.fixture.root

    def tearDown(self) -> None:
        self.fixture.close()

    def test_exact_fixture_passes(self) -> None:
        self.assertEqual(self.fixture.check(), [])

    def test_first_byte_change_of_model_is_source_changed(self) -> None:
        path = self.root / "code/derivation/model.py"
        original = path.read_bytes()
        path.write_bytes(bytes([original[0] ^ 0xFF]) + original[1:])
        failures = self.fixture.check()
        path.write_bytes(original)
        self.assertIn("SOURCE_CHANGED: code/derivation/model.py", failures)

    def test_unconsumed_paths_are_not_reported(self) -> None:
        for relative in UNCONSUMED:
            (self.root / relative).write_bytes(b"injected unrelated change\n")
        self.assertEqual(self.fixture.check(), [])

    def test_duplicate_manifest_key_is_refused(self) -> None:
        text = self.fixture.manifest_path.read_text(encoding="utf-8")
        doubled = text.replace('{"schema"', '{"baseline_commit": "0", "schema"', 1)
        self.fixture.manifest_path.write_text(doubled, encoding="utf-8")
        self.assertTrue(
            any("duplicate manifest key" in item for item in self.fixture.check())
        )

    def test_schema_guard(self) -> None:
        manifest = json.loads(self.fixture.manifest_path.read_text(encoding="utf-8"))
        manifest["schema"] = "wrong"
        self.fixture.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertTrue(
            any(item.startswith("MANIFEST_SCHEMA:") for item in self.fixture.check())
        )

    def test_lone_cr_is_not_checkout_conversion(self) -> None:
        self.assertNotEqual(
            guard.canonical_text(b"a\rb\n"),
            guard.canonical_text(b"a\nb\n"),
        )

    def test_no_repin_flag(self) -> None:
        source = Path(__file__).resolve().parents[1] / "verify_sources.py"
        text = source.read_text(encoding="utf-8")
        self.assertNotIn('add_argument("--repin"', text)
        self.assertNotIn("add_argument('--repin'", text)

    def test_runtime_origin_is_independently_checked(self) -> None:
        modules: dict[str, ModuleType] = {}
        for name, relative in guard.RUNTIME_PATHS.items():
            module = ModuleType(name)
            module.__file__ = str(self.root / relative)
            module.__spec__ = ModuleSpec(name, loader=None, origin=module.__file__)
            modules[name] = module
        self.assertEqual(guard.runtime_errors(self.root, modules), [])
        foreign = Path(self.fixture.tmp.name) / "foreign_model.py"
        foreign.write_bytes((self.root / "code/derivation/model.py").read_bytes())
        modules["derivation.model"].__file__ = str(foreign)
        self.assertTrue(
            any(
                item.startswith("RUNTIME_ORIGIN:")
                for item in guard.runtime_errors(self.root, modules)
            )
        )


if __name__ == "__main__":
    unittest.main()
