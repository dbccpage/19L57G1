"""Tests for the instrumented decider and summation meter, against the
pre-registered BC3 claims and the receipt."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import tempfile
import unittest
from pathlib import Path

import budget_meter as bm
import run_budget_meter as runner

TREE = Path(__file__).resolve().parent


class DeciderTests(unittest.TestCase):
    def test_decider_within_declared_budget_everywhere_with_matching_verdicts(self) -> None:
        r = bm.report()
        self.assertTrue(r["decider_all_within_budget"])
        self.assertTrue(r["decider_all_verdicts_match"])
        rows = r["decider"]
        assert isinstance(rows, list)
        self.assertEqual(len(rows), 54)  # nine fixtures x three rounds x two presentations

    def test_instances_cover_rounds_and_re_presentations(self) -> None:
        names = [name for name, _, _, _ in bm.instances()]
        self.assertIn("square_2x2_r0", names)
        self.assertIn("square_2x2_r2", names)
        self.assertIn("square_2x2_r1_repres", names)
        self.assertIn("chain_P4_r2_repres", names)


class MeterTests(unittest.TestCase):
    def test_sum_meter_breaches_the_linear_budget_at_length_8_not_6(self) -> None:
        """Pre-registration said the breach came at length 6; computed, length 6
        fits the declared budget by 731 <= 840 and the breach arrives at 8.
        The miss is recorded in STATUS.md; the growth-factor prediction held."""
        r = bm.report()
        rows = r["sum_meter_square"]
        assert isinstance(rows, list)
        by_len = {row["max_len"]: row for row in rows}
        self.assertTrue(by_len[6]["within_budget"])
        self.assertFalse(by_len[8]["within_budget"])
        self.assertEqual(by_len[6]["steps"], 731)
        self.assertEqual(by_len[8]["steps"], 5851)

    def test_growth_factor_exceeds_two_per_added_length(self) -> None:
        r = bm.report()
        growth = r["sum_meter_growth_factors"]
        assert isinstance(growth, list)
        for g in growth:
            self.assertGreater(g, 2.0)

    def test_walk_counts_match_the_dynamics_receipt(self) -> None:
        rows = bm.report()["sum_meter_square"]
        assert isinstance(rows, list)
        by_len = {row["max_len"]: row["closed_walks"] for row in rows}
        self.assertEqual(by_len[6], 147)  # agrees with receipts/dynamics_counts.json


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "budget_meter.json").read_bytes()
            self.assertEqual(one, (b / "budget_meter.json").read_bytes())
            self.assertEqual(one, (TREE / "receipts" / "budget_meter.json").read_bytes())

    def test_runner_refuses_an_output_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(runner.main(["--out", outside]), 1)


if __name__ == "__main__":
    unittest.main()
