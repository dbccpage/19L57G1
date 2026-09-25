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
import re
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verify_sources as guard  # noqa: E402

UNCONSUMED = ("prompt/input.md", "paper/claim.md", "artifacts/other.json")
# Files beside the pinned ones that this family does not read (2026-09-25).
NEIGHBOURS = ("lean4/Derivation/Example.lean", "research/local_reuse/lean/LocalReuse.lean",
              "research/coherent_process_limits/lean/Limits.lean",
              "research/coherent_process_limits/README.md",
              "research/represented_execution/SOURCE_MANIFEST.json",
              "research/setting_translation/verify_sources.py")


def git(root: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True).stdout


class Fixture:
    def __init__(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = (Path(self.tmp.name) / "fixture").resolve()
        self.root.mkdir()
        root = self.root
        git(root, "init", "--quiet")
        git(root, "config", "core.autocrlf", "false")
        git(root, "config", "user.name", "Custody fixture")
        git(root, "config", "user.email", "fixture@example.invalid")
        for relative in (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS, *guard.LEAN_PATHS,
                         *NEIGHBOURS, *UNCONSUMED):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"# fixture source\n")
        git(root, "add", "--", *guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS, *guard.LEAN_PATHS,
            *NEIGHBOURS, *UNCONSUMED)
        git(root, "commit", "--quiet", "-m", "Fixture baseline")
        self.baseline = git(root, "rev-parse", "HEAD").decode().strip()
        self.original_baseline = guard.BASELINE_COMMIT
        guard.BASELINE_COMMIT = self.baseline
        try:
            self._write_manifest(root)
        except BaseException:
            guard.BASELINE_COMMIT = self.original_baseline
            self.tmp.cleanup()
            raise

    def _write_manifest(self, root: Path) -> None:
        manifest = {
            "schema": guard.SCHEMA,
            "baseline_commit": self.baseline,
            "text_normalization": "CRLF_TO_LF_ONLY",
            "runtime_modules": guard.RUNTIME_PATHS,
            "source_sha256": {path: hashlib.sha256(git(root, "show", f"{self.baseline}:{path}")).hexdigest()
                              for path in (*guard.RUNTIME_PATHS.values(), *guard.CONFIG_PATHS,
                                           *guard.LEAN_PATHS)},
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
        for relative in ("code/derivation/primitive_core.py", "research/coherent_process_limits/lean/lakefile.toml",
                         "research/represented_execution/evidence/process.json",
                         "research/coherent_process_limits/lean/Observe.lean",
                         "lean4/Derivation/PrimitiveCore.lean"):
            with self.subTest(relative=relative):
                path = self.root / relative
                original = path.read_bytes()
                path.write_bytes(b"# injected different payload\n")
                failures = self.fixture.check()
                path.write_bytes(original)
                self.assertIn(f"SOURCE_CHANGED: {relative}", failures)
                self.assertIn(f"CONSUMED_TRACKED_DIFF: {relative}", failures)
        self.assertEqual(self.fixture.check(), [])

    def test_unconsumed_neighbours_are_not_failures(self) -> None:
        """2026-09-25: the directory pins are retired.  A file beside the pinned
        ones that this family does not read may change, tracked or not; until
        then each of these failed as CONSUMED_TRACKED_DIFF or SOURCE_CENSUS."""
        for relative in NEIGHBOURS:
            (self.root / relative).write_bytes(b"# an edit this family does not read\n")
        git(self.root, "add", "--", *NEIGHBOURS)
        for relative in ("code/derivation/new.py", "research/coherent_process_limits/lean/Extra.lean",
                         "research/represented_execution/extra.py"):
            (self.root / relative).write_bytes(b"# nothing here imports this\n")
        self.assertEqual(self.fixture.check(), [])

    def test_a_manifest_with_directory_pins_is_refused(self) -> None:
        manifest = json.loads(self.fixture.manifest_path.read_text(encoding="utf-8"))
        manifest["consumed_trees"] = {"lean4/Derivation": "0" * 40}
        self.fixture.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertEqual(
            self.fixture.check(),
            ["MANIFEST_TREE_PINS: whole-directory pins were retired on 2026-09-25"],
        )

    def test_changed_consumed_observer_is_a_tracked_diff(self) -> None:
        path = self.root / "research/coherent_process_limits/limits.py"
        path.write_bytes(b"# injected change to the consumed observer\n")
        failures = self.fixture.check()
        self.assertIn("CONSUMED_TRACKED_DIFF: research/coherent_process_limits/limits.py", failures)

    def test_build_outputs_under_lake_are_not_sources(self) -> None:
        path = self.root / "research/coherent_process_limits/lean/.lake/build/Copy.lean"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"-- not a source\n")
        self.assertEqual(self.fixture.check(), [])

    def test_changes_outside_the_consumed_scope_are_not_reported(self) -> None:
        for relative in UNCONSUMED:
            (self.root / relative).write_bytes(b"injected unrelated change\n")
        self.assertEqual(self.fixture.check(), [])

    def test_missing_baseline_fails_closed(self) -> None:
        missing = "0" * 40
        guard.BASELINE_COMMIT = missing
        manifest = json.loads(self.fixture.manifest_path.read_text(encoding="utf-8"))
        manifest["baseline_commit"] = missing
        self.fixture.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertTrue(any(f.startswith("BASELINE_UNAVAILABLE:") for f in self.fixture.check()))

    def test_manifest_cannot_adopt_drift(self) -> None:
        for field in ("process.json", "lean"):
            with self.subTest(field=field):
                fixture = Fixture()
                try:
                    manifest = json.loads(fixture.manifest_path.read_text(encoding="utf-8"))
                    relative = ("research/represented_execution/evidence/process.json"
                                if field == "process.json" else guard.LEAN_PATHS[0])
                    source = fixture.root / relative
                    source.write_bytes(b"# changed and adopted\n")
                    manifest["source_sha256"][relative] = hashlib.sha256(source.read_bytes()).hexdigest()
                    fixture.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                    failures = fixture.check()
                    self.assertTrue(any("PIN:" in f for f in failures), failures)
                finally:
                    fixture.close()
                    guard.BASELINE_COMMIT = self.fixture.baseline

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
class TheReadmeNamesTheBaselineItPins(unittest.TestCase):
    """A commit id written in prose drifts at every repin, silently.  This
    review found two stale ones in a sibling README; the repair is not to
    substitute more carefully but to make the prose checkable."""

    def test_every_commit_id_in_the_readme_is_the_pinned_baseline(self) -> None:
        tree = Path(__file__).resolve().parents[1]
        text = (tree / "README.md").read_text(encoding="utf-8")
        named = set(re.findall(r"[0-9a-f]{40}", text))
        self.assertTrue(named, "the README names no baseline at all")
        self.assertEqual(named, {guard.BASELINE_COMMIT})

    def test_the_manifest_names_the_same_one(self) -> None:
        tree = Path(__file__).resolve().parents[1]
        manifest = json.loads((tree / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["baseline_commit"], guard.BASELINE_COMMIT)


if __name__ == "__main__":
    unittest.main()
