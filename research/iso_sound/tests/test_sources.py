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
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True).stdout


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
        for relative in (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS, *guard.OPENED_PATHS,
                         "lean4/Derivation/Example.lean", *UNCONSUMED):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"# fixture source\n")
        git(root, "add", "--", *guard.CONSUMED_TREES, *guard.CONFIG_PATHS, *guard.OPENED_PATHS,
            *UNCONSUMED)
        git(root, "commit", "--quiet", "-m", "Fixture baseline")
        self.baseline = git(root, "rev-parse", "HEAD").decode().strip()
        self.original_baseline = guard.BASELINE_COMMIT
        guard.BASELINE_COMMIT = self.baseline
        manifest = {
            "schema": guard.SCHEMA,
            "baseline_commit": self.baseline,
            "text_normalization": "CRLF_TO_LF_ONLY",
            "runtime_modules": guard.RUNTIME_PATHS,
            "consumed_trees": {tree: git(root, "rev-parse", f"{self.baseline}:{tree}").decode().strip()
                               for tree in guard.CONSUMED_TREES},
            "tree_census": {tree: guard.tree_census(root, tree, suffix)[0]
                            for tree, suffix in guard.CONSUMED_TREES.items()},
            "source_sha256": {path: hashlib.sha256(git(root, "show", f"{self.baseline}:{path}")).hexdigest()
                              for path in (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS,
                                           *guard.OPENED_PATHS)},
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

    def test_changed_pinned_source_is_named(self) -> None:
        path = self.root / "code/derivation/model.py"
        original = path.read_bytes()
        path.write_bytes(b"# injected different payload\n")
        failures = self.fixture.check()
        path.write_bytes(original)
        self.assertIn("SOURCE_CHANGED: code/derivation/model.py", failures)

    def test_changed_opened_file_is_named(self) -> None:
        """2026-09-25: the sealed suite read by path is pinned, not only the trees."""
        path = self.root / "tests/test_iso.py"
        original = path.read_bytes()
        path.write_bytes(b"# injected different payload\n")
        failures = self.fixture.check()
        path.write_bytes(original)
        self.assertIn("SOURCE_CHANGED: tests/test_iso.py", failures)

    def test_assume_unchanged_lean_source_is_named(self) -> None:
        relative = "lean4/Derivation/Example.lean"
        path = self.root / relative
        original = path.read_bytes()
        git(self.root, "update-index", "--assume-unchanged", "--", relative)
        try:
            path.write_bytes(b"-- injected assume-unchanged payload\n")
            diff = git(self.root, "diff", "--name-only", self.fixture.baseline, "--", relative)
            self.assertEqual(diff.strip(), b"")
            failures = self.fixture.check()
            self.assertIn(f"SOURCE_CHANGED: {relative}", failures)
        finally:
            path.write_bytes(original)
            git(self.root, "update-index", "--no-assume-unchanged", "--", relative)
        self.assertEqual(self.fixture.check(), [])

    def test_untracked_source_in_a_consumed_tree_is_named(self) -> None:
        path = self.root / "code/derivation/new.py"
        path.write_bytes(b"# injected source\n")
        failures = self.fixture.check()
        path.unlink()
        self.assertTrue(any("SOURCE_CENSUS:" in f and "new.py" in f for f in failures), failures)

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
        self.assertTrue(any(f.startswith("RUNTIME_ORIGIN:") for f in guard.runtime_errors(self.root, modules)))
