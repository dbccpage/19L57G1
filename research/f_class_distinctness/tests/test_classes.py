"""Python F representatives match Lean field snapshots and are pairwise non-iso."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

from derivation.engine import READING_F, READING_L  # noqa: E402
from derivation.iso import isomorphic  # noqa: E402
import classes as cl  # noqa: E402


class Fields(unittest.TestCase):
    def test_f_fields_match_lean(self) -> None:
        for name, reg in cl.F_REPS:
            self.assertEqual(cl.regime_fields(reg), cl.LEAN_F_FIELDS[name], name)

    def test_l_fields_match_lean(self) -> None:
        for name, reg in cl.L_REPS:
            self.assertEqual(cl.regime_fields(reg), cl.LEAN_L_FIELDS[name], name)

    def test_inline_f_defs_match_the_lean_source(self) -> None:
        # DiagF/LinkF/OutF/InF are defined inline in the Lean file as field
        # literals; assert those literals match LEAN_F_FIELDS so a Lean-def edit
        # cannot silently diverge from the Python snapshot the mirror checks.
        # (MarkF is the sealed U0F and the L reps are sealed defs, referenced by
        # name rather than literal, so they are out of this source-bridge scope.)
        lean = (Path(__file__).resolve().parents[1] / "lean"
                / "FClassDistinctness.lean").read_text(encoding="utf-8")
        for name in ("DiagF", "LinkF", "OutF", "InF"):
            n, forms, insts, rules, reqs = cl.LEAN_F_FIELDS[name]
            forms_s = "[" + ", ".join(str(a) for a in forms) + "]"
            insts_s = "[" + ", ".join(
                "(" + str(f) + ", [" + ", ".join(str(x) for x in args) + "])"
                for f, args in insts
            ) + "]"
            rules_s = "[" + ", ".join(str(r) for r in rules) + "]"
            reqs_s = "[" + ", ".join("(" + str(i) + ", " + str(j) + ")" for i, j in reqs) + "]"
            literal = f"⟨{n}, {forms_s}, {insts_s}, {rules_s}, {reqs_s}⟩"
            # bind the literal to its exact def, not merely its presence anywhere
            # (e.g. DiagF' carries the [2,2] literal), so an edit to `def DiagF`
            # cannot pass by matching another definition's body.
            self.assertIn(f"def {name} : Regime := {literal}", lean, (name, literal))


class Distinctness(unittest.TestCase):
    def test_f_pairwise_noniso(self) -> None:
        self.assertEqual(cl.pairwise_noniso(cl.F_REPS), [])

    def test_l_pairwise_noniso(self) -> None:
        self.assertEqual(cl.pairwise_noniso(cl.L_REPS), [])

    def test_identical_pair_is_reported(self) -> None:
        twin = (("A", cl.mark_f()), ("B", cl.mark_f()))
        self.assertEqual(cl.pairwise_noniso(twin), [("A", "B")])

    def test_within_class_swaps_are_iso(self) -> None:
        for name, a, b in cl.F_SWAPS:
            self.assertTrue(isomorphic(a, b), name)


class Engine(unittest.TestCase):
    def test_engine_counts_and_rep_hits(self) -> None:
        f_engine = cl.mu1_class_regimes(READING_F)
        l_engine = cl.mu1_class_regimes(READING_L)
        self.assertEqual(len(f_engine), 5)
        self.assertEqual(len(l_engine), 3)
        hits = cl.rep_engine_hits(cl.F_REPS, f_engine)
        for row in hits:
            labels = row["engine_labels"]
            self.assertIsInstance(labels, list)
            assert isinstance(labels, list)
            self.assertEqual(len(labels), 1, row)

    def test_progress_lemma_failure_is_named(self) -> None:
        with mock.patch("classes.min_responses", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "progress lemma"):
                cl.mu1_class_regimes(READING_F)

    def test_class_record_records_within_and_iso_failures(self) -> None:
        with mock.patch("classes.isomorphic", return_value=False):
            record = cl.class_record()
        failures = record["within_class_iso_failures"]
        self.assertEqual(failures, ["MarkF", "DiagF", "LinkF", "OutF", "InF"])
        hits = record["pairwise_iso_hits"]
        self.assertIsInstance(hits, list)
        self.assertEqual(hits, [])
