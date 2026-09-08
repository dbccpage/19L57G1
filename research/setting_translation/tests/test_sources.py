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
LEAN_SOURCES = ("lean4/Derivation/Example.lean", "research/local_reuse/lean/LocalReuse.lean",
                "research/magnification/lean/EngineClass.lean")


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
        for relative in (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS, *LEAN_SOURCES, *UNCONSUMED):
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
            "consumed_trees": {tree: git(root, "rev-parse", f"{self.baseline}:{tree}").decode().strip()
                               for tree in guard.CONSUMED_TREES},
            "tree_census": {tree: guard.tree_census(root, tree, suffix)[0]
                            for tree, suffix in guard.CONSUMED_TREES.items()},
            "source_sha256": {path: hashlib.sha256(git(root, "show", f"{self.baseline}:{path}")).hexdigest()
                              for path in (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS)},
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
    fixture: Fixture

    def setUp(self) -> None:
        self.fixture = Fixture()
        self.root = self.fixture.root

    def tearDown(self) -> None:
        self.fixture.close()

    def test_exact_fixture_passes_and_crlf_checkout_is_accepted(self) -> None:
        self.assertEqual(self.fixture.check(), [])
        for relative in (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS):
            source = self.root / relative
            source.write_bytes(source.read_bytes().replace(b"\n", b"\r\n"))
        git(self.root, "config", "core.autocrlf", "true")
        self.assertEqual(self.fixture.check(), [])

    def test_changed_pinned_source_is_named(self) -> None:
        for relative in ("code/derivation/primitive_core.py", "lean4/lakefile.toml",
                         "research/magnification/lean/lakefile.toml"):
            with self.subTest(relative=relative):
                path = self.root / relative
                original = path.read_bytes()
                path.write_bytes(b"# injected different payload\n")
                failures = self.fixture.check()
                path.write_bytes(original)
                self.assertIn(f"SOURCE_CHANGED: {relative}", failures)
                self.assertIn(f"CONSUMED_TRACKED_DIFF: {relative}", failures)
        self.assertEqual(self.fixture.check(), [])

    def test_untracked_source_in_a_consumed_tree_is_named(self) -> None:
        for relative in ("code/derivation/new.py", "lean4/Derivation/New.lean",
                         "research/local_reuse/lean/Extra.lean", "research/magnification/lean/Extra.lean"):
            with self.subTest(relative=relative):
                path = self.root / relative
                path.write_bytes(b"# injected source\n")
                failures = self.fixture.check()
                path.unlink()
                self.assertTrue(any("SOURCE_CENSUS:" in f and relative in f for f in failures), failures)
        self.assertEqual(self.fixture.check(), [])

    def test_changed_consumed_lean_source_is_a_tracked_diff(self) -> None:
        path = self.root / "research/magnification/lean/EngineClass.lean"
        path.write_bytes(b"-- injected change to a consumed proof\n")
        failures = self.fixture.check()
        self.assertIn("CONSUMED_TRACKED_DIFF: research/magnification/lean/EngineClass.lean", failures)

    def test_build_outputs_under_lake_are_not_sources(self) -> None:
        path = self.root / "research/magnification/lean/.lake/build/Copy.lean"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"-- not a source\n")
        self.assertEqual(self.fixture.check(), [])

    def test_changes_outside_the_consumed_scope_are_not_reported(self) -> None:
        for relative in UNCONSUMED:
            (self.root / relative).write_bytes(b"injected unrelated change\n")
        self.assertEqual(self.fixture.check(), [])

    def test_staged_change_survives_working_file_recovery(self) -> None:
        source = self.root / "code/derivation/iso.py"
        original = source.read_bytes()
        source.write_bytes(b"injected staged payload\n")
        git(self.root, "add", "--", "code/derivation/iso.py")
        source.write_bytes(original)
        self.assertIn("CONSUMED_TRACKED_DIFF: code/derivation/iso.py", self.fixture.check())

    def test_missing_baseline_fails_closed(self) -> None:
        missing = "0" * 40
        guard.BASELINE_COMMIT = missing
        manifest = json.loads(self.fixture.manifest_path.read_text(encoding="utf-8"))
        manifest["baseline_commit"] = missing
        self.fixture.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertTrue(any(f.startswith("BASELINE_UNAVAILABLE:") for f in self.fixture.check()))

    def test_duplicate_manifest_key_is_refused(self) -> None:
        text = self.fixture.manifest_path.read_text(encoding="utf-8")
        doubled = text.replace('{"schema"', '{"baseline_commit": "0", "schema"', 1)
        self.fixture.manifest_path.write_text(doubled, encoding="utf-8")
        self.assertTrue(any("duplicate manifest key" in f for f in self.fixture.check()))

    def test_manifest_cannot_adopt_drift(self) -> None:
        for field in ("source_sha256", "consumed_trees", "tree_census"):
            with self.subTest(field=field):
                fixture = Fixture()
                try:
                    manifest = json.loads(fixture.manifest_path.read_text(encoding="utf-8"))
                    if field == "source_sha256":
                        source = fixture.root / "code/derivation/model.py"
                        source.write_bytes(b"# changed and adopted\n")
                        manifest[field]["code/derivation/model.py"] = hashlib.sha256(source.read_bytes()).hexdigest()
                    elif field == "consumed_trees":
                        manifest[field]["code/derivation"] = "0" * 40
                    else:
                        manifest[field]["code/derivation"].append("code/derivation/invented.py")
                    fixture.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                    failures = fixture.check()
                    self.assertTrue(any("PIN:" in f or "MANIFEST_TREE_CENSUS:" in f for f in failures), failures)
                finally:
                    fixture.close()
                    guard.BASELINE_COMMIT = self.fixture.baseline

    def test_unrelated_later_commit_is_allowed(self) -> None:
        path = self.root / "research/unrelated.txt"
        path.write_text("Later unrelated research\n", encoding="utf-8")
        git(self.root, "add", "--", "research/unrelated.txt")
        git(self.root, "commit", "--quiet", "-m", "Unrelated research")
        self.assertEqual(self.fixture.check(), [])

    def test_runtime_origin_and_census_are_independently_checked(self) -> None:
        modules: dict[str, ModuleType] = {}
        for name, relative in guard.RUNTIME_PATHS.items():
            module = ModuleType(name)
            module.__file__ = str(self.root / relative)
            module.__spec__ = ModuleSpec(name, loader=None, origin=module.__file__)
            modules[name] = module
        self.assertEqual(guard.runtime_errors(self.root, modules), [])
        foreign = Path(self.fixture.tmp.name) / "foreign_core.py"
        foreign.write_bytes((self.root / "code/derivation/primitive_core.py").read_bytes())
        modules["derivation.primitive_core"].__file__ = str(foreign)
        self.assertTrue(any(f.startswith("RUNTIME_ORIGIN: derivation.primitive_core __file__")
                            for f in guard.runtime_errors(self.root, modules)))
        modules["derivation.unpinned"] = ModuleType("derivation.unpinned")
        self.assertTrue(any(f.startswith("RUNTIME_CENSUS:") for f in guard.runtime_errors(self.root, modules)))


if __name__ == "__main__":
    unittest.main()
