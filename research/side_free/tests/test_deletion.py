"""The deletion register: population, classification, and totality.

The population is enumerated INDEPENDENTLY of the classifier -- from the
pinned source at the pinned commit -- so a name the classifier cannot place
fails the population check instead of cancelling out on both sides of it.
That check needs every declared pinned source and fails by name when one is
unavailable; the totality checks below need no git at all and always run.

The classification is declared in ``control.DELETION_REGISTER`` and is held
in BOTH directions: a DELETED name must be absent from the side-free
modules' identifier census, and a NARROWED name must be present in it.
"""

from __future__ import annotations

import ast
import json
import pathlib
import re
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "code"))

from sidefree import control  # noqa: E402

TREE = pathlib.Path(__file__).resolve().parent.parent
ROOT = TREE.parent.parent
BLOCK = control.deletion_register_block()


def pinned_source() -> dict[str, str]:
    """The pinned .py sources; missing or empty source populations fail."""
    manifest = json.loads((TREE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    commit = manifest["pinned_commit"]
    out: dict[str, str] = {}
    for source in manifest["sources"]:
        path = source["path"]
        if not path.endswith(".py"):
            continue
        proc = subprocess.run(
            ["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True
        )
        if proc.returncode != 0:
            raise RuntimeError(f"pinned population source {commit}:{path} is unavailable")
        out[path] = proc.stdout.decode("utf-8")
    if not out:
        raise RuntimeError(f"pinned population at {commit} has no Python sources")
    return out


def defined_names(source: str) -> set[str]:
    found: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            found.add(node.name)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found.update(
                    a.arg
                    for a in [
                        *node.args.args,
                        *node.args.kwonlyargs,
                        *node.args.posonlyargs,
                    ]
                )
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            found.add(node.target.id)
        elif isinstance(node, ast.Assign):
            found.update(t.id for t in node.targets if isinstance(t, ast.Name))
    return found


def top_level(source: str) -> dict[str, list[ast.AST]]:
    out: dict[str, list[ast.AST]] = {}
    for node in ast.parse(source).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.setdefault(node.name, []).append(node)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            out.setdefault(node.target.id, []).append(node)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out.setdefault(t.id, []).append(node)
    return out


class Population(unittest.TestCase):
    def test_the_population_is_the_mechanical_closure_over_the_pinned_source(
        self,
    ) -> None:
        sources = pinned_source()
        seed: set[str] = set()
        for text in sources.values():
            seed |= {n for n in defined_names(text) if control.carries_a_deleted_stem(n)}
        closure: set[str] = set()
        for text in sources.values():
            for name, nodes in top_level(text).items():
                if control.carries_a_deleted_stem(name):
                    continue
                for node in nodes:
                    for sub in ast.walk(node):
                        reached = None
                        if isinstance(sub, ast.Name):
                            reached = sub.id
                        elif isinstance(sub, ast.Attribute):
                            reached = sub.attr
                        elif isinstance(sub, ast.arg):
                            reached = sub.arg
                        elif isinstance(sub, ast.keyword) and sub.arg:
                            reached = sub.arg
                        if reached is not None and control.carries_a_deleted_stem(reached):
                            closure.add(name)
        registered = {name for name, _kind, _why in control.DELETION_REGISTER}
        self.assertEqual(registered, seed | closure)
        self.assertEqual(len(registered), 119)

    def test_missing_population_source_fails_by_name_then_recovers(self) -> None:
        baseline = pinned_source()
        self.assertTrue(baseline)
        first = next(iter(baseline))
        failed: subprocess.CompletedProcess[bytes] = subprocess.CompletedProcess(
            ["git", "show", "PinProbeMissing"], 1, b"", b"missing probe"
        )
        with patch.object(subprocess, "run", return_value=failed):
            with self.assertRaisesRegex(RuntimeError, re.escape(first)) as caught:
                pinned_source()
        self.assertEqual(pinned_source(), baseline)
        print(f"INJECTION population: {caught.exception}; RECOVERY clean")

    def test_every_entry_carries_a_kind_and_a_reason(self) -> None:
        for name, kind, why in control.DELETION_REGISTER:
            self.assertIn(kind, ("DELETED", "NARROWED"))
            self.assertTrue(why.startswith(("direct:", "via:")), name)
            self.assertTrue(name)

    def test_the_register_has_no_duplicate_name(self) -> None:
        names = [name for name, _kind, _why in control.DELETION_REGISTER]
        self.assertEqual(len(names), len(set(names)))


class Totality(unittest.TestCase):
    def test_no_deleted_name_survives_in_the_side_free_modules(self) -> None:
        self.assertEqual(BLOCK["deleted_names_surviving"], [])
        self.assertGreater(int(str(BLOCK["deleted_count"])), 0)
        self.assertGreater(int(str(BLOCK["identifier_census_size"])), 0)

    def test_every_narrowed_name_is_present(self) -> None:
        """The other direction: a narrowing that quietly vanished is a defect."""
        self.assertEqual(BLOCK["narrowed_names_absent"], [])
        self.assertGreater(int(str(BLOCK["narrowed_count"])), 0)

    def test_no_identifier_carries_a_deleted_stem_outside_the_allowlist(self) -> None:
        self.assertEqual(BLOCK["deleted_stem_leaks"], [])
        for name, reason in control.DELETION_WORD_ALLOWLIST_REASONS.items():
            self.assertIn(name, control.DELETION_WORD_ALLOWLIST)
            self.assertTrue(reason)

    def test_the_totality_check_fails_when_a_deleted_name_comes_back(self) -> None:
        """Negative: reintroduce a deleted identifier and the scan must name it."""
        census = control.side_free_identifiers()
        deleted = [n for n, kind, _w in control.DELETION_REGISTER if kind == "DELETED"]
        probe = "placement"
        self.assertIn(probe, deleted)
        self.assertNotIn(probe, census)
        injected = census | {probe}
        survivors = sorted(name for name in deleted if name in injected)
        self.assertEqual(survivors, [probe])

    def test_the_stem_scan_reads_the_syntax_and_not_the_text(self) -> None:
        """A deleted word inside prose is how a deletion gets explained."""
        text = (TREE / "code" / "sidefree" / "model.py").read_text("utf-8")
        self.assertIn("side", text)
        self.assertNotIn("side", control.side_free_identifiers())

    def test_the_component_split_handles_both_naming_styles(self) -> None:
        self.assertTrue(control.carries_a_deleted_stem("on_side_0"))
        self.assertTrue(control.carries_a_deleted_stem("SideNamed"))
        self.assertTrue(control.carries_a_deleted_stem("READING_O"))
        self.assertFalse(control.carries_a_deleted_stem("read_whole"))
        self.assertFalse(control.carries_a_deleted_stem("marks_separable_under"))

    def test_the_excluded_modules_are_named_and_not_implicit(self) -> None:
        excluded = BLOCK["modules_excluded_by_declaration"]
        self.assertIsInstance(excluded, dict)
        assert isinstance(excluded, dict)
        self.assertIn("mirror.py", excluded)
        self.assertIn("control.py", excluded)
        self.assertEqual(len(control.SIDE_FREE_MODULES), 5)
        for name in control.SIDE_FREE_MODULES:
            self.assertTrue((TREE / "code" / "sidefree" / name).is_file())

    def test_the_removed_refusal_is_recorded_as_removed(self) -> None:
        refusal = BLOCK["removed_refusal"]
        assert isinstance(refusal, dict)
        self.assertEqual(refusal["status"], "REMOVED, not absorbed")

    def test_the_register_is_rendered_in_the_prose_file(self) -> None:
        prose = (TREE / "DELETED.md").read_text("utf-8")
        for name, _kind, _why in control.DELETION_REGISTER:
            self.assertIn(f"`{name}`", prose, name)
        listed = set(re.findall(r"^\| `([A-Za-z_][A-Za-z0-9_]*)` \|", prose, re.M))
        self.assertEqual(
            listed,
            {name for name, _kind, _why in control.DELETION_REGISTER}
            | set(control.DELETION_WORD_ALLOWLIST),
        )


if __name__ == "__main__":
    unittest.main()
