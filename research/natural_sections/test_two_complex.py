"""Tests for the chord-square face survey, against the pre-registered
TC4 claims and the receipt."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import tempfile
import unittest
from pathlib import Path

import two_complex as tc
import run_two_complex as runner

TREE = Path(__file__).resolve().parent


class SurveyTests(unittest.TestCase):
    def test_boundary_identity_and_potential_flux_agreement_everywhere(self) -> None:
        for row in (tc.survey(n) for n in tc.MODULI):
            self.assertTrue(row["boundary_identity_everywhere"])
            self.assertTrue(row["potential_matches_flux_criterion"])

    def test_pre_registered_counts(self) -> None:
        """TC4: sections N^3, outer-zero N^4, outer-zero-obstructed
        N^4 - N^3, T1-filled N^4 with N^3 sectioned."""
        for n in tc.MODULI:
            row = tc.survey(n)
            self.assertEqual(row["total"], n**5)
            self.assertEqual(row["sections"], n**3)
            self.assertEqual(row["outer_zero"], n**4)
            self.assertEqual(row["outer_zero_obstructed"], n**4 - n**3)
            self.assertEqual(row["t1_filled"], n**4)
            self.assertEqual(row["t1_filled_with_section"], n**3)

    def test_separating_assignment_is_outer_blind(self) -> None:
        """The Lean countermodel at Z_3: Phi on e13, -Phi on e32, zero
        elsewhere -- outer flux zero, no section."""
        n = 3
        w = (0, 1, n - 1, 0, 0)  # e01, e13, e32, e20, e03
        self.assertEqual(tc.flux_outer(w, n), 0)
        self.assertEqual(tc.flux_t1(w, n), 1)
        self.assertFalse(tc.potential_exists(w, n))

    def test_filling_both_faces_gives_a_section(self) -> None:
        n = 3
        w = (1, 1, 1, 1, 2)  # f1 = 1+1-2 = 0, f2 = 2+1+1 = 4 = 1 -- not both
        self.assertEqual(tc.flux_t1(w, n), 0)
        self.assertFalse(tc.potential_exists(w, n))
        w2 = (1, 1, 0, 1, 2)  # f1 = 0, f2 = 2+0+1 = 0
        self.assertEqual(tc.flux_t1(w2, n), 0)
        self.assertEqual(tc.flux_t2(w2, n), 0)
        self.assertTrue(tc.potential_exists(w2, n))


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "two_complex.json").read_bytes()
            self.assertEqual(one, (b / "two_complex.json").read_bytes())
            self.assertEqual(one, (TREE / "receipts" / "two_complex.json").read_bytes())

    def test_runner_refuses_an_output_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(runner.main(["--out", outside]), 1)


if __name__ == "__main__":
    unittest.main()
