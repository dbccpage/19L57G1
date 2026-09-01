"""Tests for the layer-balance rung, mirroring the STATUS.md registration."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

import layer_balance
import run_layer_balance

HERE = Path(__file__).resolve().parent


class BalanceValueTests(unittest.TestCase):
    def test_balance_at_small_part_counts_matches_the_lean_pin(self) -> None:
        report = layer_balance.report()
        self.assertEqual(
            report["balance_1_12"], [1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0]
        )

    def test_fresh_counts_match_the_receiver_rungs_reduced_counts(self) -> None:
        report = layer_balance.report()
        fresh = report["fresh_counts_1_12"]
        assert isinstance(fresh, list)
        self.assertEqual(fresh, [1, 1, 2, 2, 4, 2, 6, 4, 6, 4, 10, 4])
        receiver = json.loads((HERE / "receipts" / "q_one.json").read_text("ascii"))
        self.assertEqual(fresh[:8], receiver["reduced_counts"])

    def test_the_two_balance_computations_agree_with_zero_misses(self) -> None:
        report = layer_balance.report()
        self.assertEqual(report["agreement_misses"], 0)

    def test_partition_and_inversion_have_zero_misses(self) -> None:
        report = layer_balance.report()
        self.assertEqual(report["partition_misses"], [])
        self.assertEqual(report["inversion_misses"], [])


class RunningBalanceTests(unittest.TestCase):
    def test_checkpoints_match_the_registration(self) -> None:
        report = layer_balance.report()
        self.assertEqual(
            report["running_balance_checkpoints"],
            {
                "10": -1,
                "30": -3,
                "100": 1,
                "1000": 2,
                "10000": -23,
                "100000": -48,
                "1000000": 212,
            },
        )

    def test_growth_maximum_is_four_fifths_at_part_count_five(self) -> None:
        report = layer_balance.report()
        growth = report["growth"]
        assert isinstance(growth, dict)
        self.assertEqual(growth["max_squared_ratio_num"], 4)
        self.assertEqual(growth["max_squared_ratio_den"], 5)
        self.assertEqual(growth["at_part_count"], 5)
        self.assertTrue(growth["stays_below_the_square_root"])


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically(self) -> None:
        committed = (HERE / "receipts" / "layer_balance.json").read_bytes()
        self.assertEqual(committed, run_layer_balance.render(layer_balance.report()))


if __name__ == "__main__":
    unittest.main()
