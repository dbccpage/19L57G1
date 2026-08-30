"""Tests for the counts comparison: identical closed-walk counts between the
square and its cover, different convention-read counts, and the receipt."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import tempfile
import unittest
from pathlib import Path

import dynamics_counts as dc
import holonomy_fixture as two
import run_dynamics_counts as runner

TREE = Path(__file__).resolve().parent


class PredictionTests(unittest.TestCase):
    def test_counts_identical_convention_read_not(self) -> None:
        sq_totals, sq_fixed = dc.counts_by_length(4, two.grid(2, 2), False, 6)
        cov_totals, cov_fixed = dc.counts_by_length(4, two.grid(2, 2), True, 6)
        self.assertEqual(sq_totals, cov_totals)
        self.assertEqual(sq_totals, [1, 0, 2, 0, 16, 0, 128])
        self.assertNotEqual(sq_fixed, cov_fixed)
        self.assertEqual(cov_fixed, cov_totals)  # the cover reads every walk
        self.assertEqual(sq_fixed, [1, 0, 2, 0, 12, 0, 80])
        for a, b in zip(sq_fixed, sq_totals):
            self.assertLessEqual(a, b)

    def test_report_flags(self) -> None:
        r = dc.report()
        self.assertTrue(r["counts_identical"])
        self.assertFalse(r["convention_read_identical"])

    def test_on_the_chain_both_agree(self) -> None:
        totals, fixed = dc.counts_by_length(4, two.chain(4), False, 6)
        self.assertEqual(totals, fixed)


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "dynamics_counts.json").read_bytes()
            self.assertEqual(one, (b / "dynamics_counts.json").read_bytes())
            self.assertEqual(one, (TREE / "receipts" / "dynamics_counts.json").read_bytes())

    def test_runner_refuses_an_output_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(runner.main(["--out", outside]), 1)


if __name__ == "__main__":
    unittest.main()
