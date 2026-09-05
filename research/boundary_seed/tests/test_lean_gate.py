"""Tests of the tree-local Lean gate's two source censuses: every module
under lean/BoundarySeed/ must be reached by the root, or it is text-scanned
but never elaborated; and every theorem those modules declare must carry a
``#print axioms`` line in the root, or the log comparison would compare a
population that silently omits it."""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE))

import verify_lean  # noqa: E402


MODULES = [
    "BoundarySeed.Basic",
    "BoundarySeed.Challenge1",
    "BoundarySeed.Challenge2",
    "BoundarySeed.Challenge3",
    "BoundarySeed.Challenge4",
    "BoundarySeed.Challenge5",
    "BoundarySeed.Continuation1",
]


class ImportClosureTests(unittest.TestCase):
    def test_every_tree_module_is_reached_by_the_root(self) -> None:
        self.assertEqual(verify_lean.module_census(), MODULES)
        self.assertEqual(verify_lean.import_closure(), set(MODULES))
        self.assertEqual(verify_lean.unreached_modules(), [])

    def test_planted_unreached_module_is_named(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lean = pathlib.Path(tmp)
            (lean / "BoundarySeed" / "Sub").mkdir(parents=True)
            (lean / "BoundarySeed.lean").write_text("import BoundarySeed.Basic\n", encoding="utf-8")
            (lean / "BoundarySeed" / "Basic.lean").write_text(
                "import BoundarySeed.Sub.Deep\n", encoding="utf-8"
            )
            (lean / "BoundarySeed" / "Sub" / "Deep.lean").write_text("", encoding="utf-8")
            (lean / "BoundarySeed" / "Zzz.lean").write_text("", encoding="utf-8")
            with (
                patch.object(verify_lean, "LEAN", lean),
                patch.object(verify_lean, "ROOT_MODULE", lean / "BoundarySeed.lean"),
            ):
                self.assertEqual(
                    verify_lean.import_closure(),
                    {"BoundarySeed.Basic", "BoundarySeed.Sub.Deep"},
                )
                self.assertEqual(verify_lean.unreached_modules(), ["BoundarySeed.Zzz"])


class AuditTotalityTests(unittest.TestCase):
    def test_every_declared_theorem_carries_a_report_line(self) -> None:
        declared = verify_lean.declared_theorems()
        audited = verify_lean.audited_theorems()
        self.assertGreater(len(declared), 0)
        self.assertEqual(verify_lean.unaudited_theorems(), [])
        self.assertEqual(declared, audited)
        self.assertIn("BoundarySeed.retained_onSide_true_iff", declared)
        self.assertIn(
            "BoundarySeed.no_invariant_mark_property_separates_retained", declared
        )
        self.assertIn(
            "BoundarySeed.no_invariant_pair_property_separates_the_wholes", declared
        )

    def test_comments_are_stripped_before_the_population_is_read(self) -> None:
        # A doc comment whose line begins with the declaration word, and a
        # line comment carrying one, must not enter the population; a real
        # declaration inside a namespace must, with its namespace.
        text = (
            "/-! module doc\n"
            "theorem not_a_declaration is only prose here\n"
            "-/\n"
            "namespace Probe\n"
            "/-- theorem also_not_one -/\n"
            "theorem kept (n : Nat) : n = n := rfl\n"
            "-- theorem commented_out\n"
            "private theorem kept_private : True := trivial\n"
            "end Probe\n"
            "theorem outside_the_namespace : True := trivial\n"
        )
        self.assertEqual(
            verify_lean.strip_comments("/- a -/ b -- c\nd"), " b \nd"
        )
        with tempfile.TemporaryDirectory() as tmp:
            lean = pathlib.Path(tmp)
            (lean / "BoundarySeed").mkdir()
            (lean / "BoundarySeed" / "Probe.lean").write_text(text, encoding="utf-8")
            (lean / "BoundarySeed.lean").write_text(
                "#print axioms Probe.kept\n", encoding="utf-8"
            )
            with (
                patch.object(verify_lean, "LEAN", lean),
                patch.object(verify_lean, "ROOT_MODULE", lean / "BoundarySeed.lean"),
            ):
                self.assertEqual(
                    verify_lean.declared_theorems(),
                    ["Probe.kept", "Probe.kept_private", "outside_the_namespace"],
                )
                self.assertEqual(verify_lean.audited_theorems(), ["Probe.kept"])
                self.assertEqual(
                    verify_lean.unaudited_theorems(),
                    ["Probe.kept_private", "outside_the_namespace"],
                )


if __name__ == "__main__":
    unittest.main()
