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
# A sealed Lean module beside the pinned ones that the tree does not import.
UNCONSUMED_LEAN = "lean4/Derivation/Unconsumed.lean"


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
        pinned = (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS, *guard.LEAN_PATHS,
                  *guard.OPENED_PATHS)
        for relative in (*pinned, UNCONSUMED_LEAN, *UNCONSUMED):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"# fixture source\n")
        git(root, "add", "--", *pinned, UNCONSUMED_LEAN, *UNCONSUMED)
        git(root, "commit", "--quiet", "-m", "Fixture baseline")
        self.baseline = git(root, "rev-parse", "HEAD").decode().strip()
        self.original_baseline = guard.BASELINE_COMMIT
        guard.BASELINE_COMMIT = self.baseline
        manifest = {
            "schema": guard.SCHEMA,
            "baseline_commit": self.baseline,
            "text_normalization": "CRLF_TO_LF_ONLY",
            "runtime_modules": guard.RUNTIME_PATHS,
            "source_sha256": {path: hashlib.sha256(git(root, "show", f"{self.baseline}:{path}")).hexdigest()
                              for path in pinned},
            "artifact_sha256": {},
        }
        packet = root / guard.PACKET
        packet.mkdir(parents=True)
        self.manifest_path = packet / "SOURCE_MANIFEST.json"
        self.manifest = manifest
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

    def test_assume_unchanged_lean_source_is_named(self) -> None:
        relative = guard.LEAN_PATHS[0]
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

    def test_changed_pinned_lean_source_is_named(self) -> None:
        relative = guard.LEAN_PATHS[-1]
        path = self.root / relative
        original = path.read_bytes()
        path.write_bytes(b"-- injected different payload\n")
        failures = self.fixture.check()
        path.write_bytes(original)
        self.assertIn(f"SOURCE_CHANGED: {relative}", failures)

    def test_unconsumed_neighbours_are_not_failures(self) -> None:
        """2026-09-25: the directory pins are retired, so a file the tree does not
        consume may change or appear beside the pinned ones.  Until then both
        failed, as SOURCE_CHANGED and SOURCE_CENSUS."""
        neighbour = self.root / UNCONSUMED_LEAN
        neighbour.write_bytes(b"-- an edit this tree does not read\n")
        new = self.root / "code/derivation/new.py"
        new.write_bytes(b"# a module nothing here imports\n")
        try:
            self.assertEqual(self.fixture.check(), [])
        finally:
            new.unlink()
            git(self.root, "checkout", "--", UNCONSUMED_LEAN)

    def test_a_manifest_with_directory_pins_is_refused(self) -> None:
        manifest = dict(self.fixture.manifest, consumed_trees={"lean4/Derivation": "0" * 40})
        self.fixture.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertEqual(
            self.fixture.check(),
            ["MANIFEST_TREE_PINS: whole-directory pins were retired on 2026-09-25"],
        )

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
