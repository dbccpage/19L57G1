"""Tests for the repair-mass survey, against the pre-registered QM2 and
QM4 claims and the receipt."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import tempfile
import unittest
from pathlib import Path

import quotient_mass as qm
import run_quotient_mass as runner

TREE = Path(__file__).resolve().parent


class SurveyTests(unittest.TestCase):
    def test_gauge_classes_are_flux_pairs_with_orbits_n_cubed(self) -> None:
        """QM2 computationally: N^2 classes, each of size N^3, and the
        image of d0 is exactly the zero class."""
        for n in qm.MODULI:
            row = qm.survey(n)
            self.assertEqual(row["class_count"], n**2)
            self.assertTrue(row["orbit_sizes_all_n_cubed"])
            self.assertTrue(row["d0_image_is_the_zero_class"])

    def test_support_price_trichotomy_and_counts(self) -> None:
        """QM3/QM4: price 0 iff (0,0); 1 iff on an axis or the
        anti-diagonal; 2 otherwise; counts 1 / 3(N-1) / (N-1)(N-2)."""
        for n in qm.MODULI:
            row = qm.survey(n)
            self.assertTrue(row["supp_price_matches_qm3"])
            counts = row["supp_price_counts"]
            assert isinstance(counts, dict)
            self.assertEqual(counts[0], 1)
            self.assertEqual(counts[1], 3 * (n - 1))
            self.assertEqual(counts[2], (n - 1) * (n - 2))

    def test_circular_price_properties(self) -> None:
        for n in qm.MODULI:
            row = qm.survey(n)
            self.assertTrue(row["circ_zero_only_at_origin"])
            self.assertTrue(row["circ_le_pair_bound"])
            self.assertTrue(row["circ_antidiagonal_exact"])

    def test_chord_prices_the_antidiagonal_alone(self) -> None:
        """The class (1, N-1) is carried by the single chord edge."""
        n = 3
        w = (0, 0, 0, 0, 2)  # e03 = 2: class (-2, 2) = (1, 2)
        self.assertEqual(qm.flux_t1(w, n), 1)
        self.assertEqual(qm.flux_t2(w, n), 2)
        self.assertEqual(qm.supp_mass(w), 1)


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "quotient_mass.json").read_bytes()
            self.assertEqual(one, (b / "quotient_mass.json").read_bytes())
            self.assertEqual(one, (TREE / "receipts" / "quotient_mass.json").read_bytes())

    def test_runner_refuses_an_output_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(runner.main(["--out", outside]), 1)


if __name__ == "__main__":
    unittest.main()
