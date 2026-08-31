"""Pins for the phase-receiver rung, exactly as pre-registered in STATUS.md."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import unittest
from pathlib import Path

import q_one
import run_q_one

HERE = Path(__file__).resolve().parent


class GroupLawTests(unittest.TestCase):
    def test_no_law_misses_up_to_index_six(self) -> None:
        laws = q_one.group_law_survey(6)
        self.assertEqual(laws["pairs"], 28)
        self.assertEqual(laws["assoc_misses"], 0)
        self.assertEqual(laws["comm_misses"], 0)
        self.assertEqual(laws["inv_misses"], 0)


class LayerTests(unittest.TestCase):
    def test_layer_compatibility_has_no_misses(self) -> None:
        compat = q_one.layer_compat_survey(6)
        self.assertEqual(compat["misses"], 0)

    def test_order_of_layer_one_is_the_part_count(self) -> None:
        self.assertEqual(
            [q_one.order_of_layer_one(k) for k in range(8)],
            [1, 2, 3, 4, 5, 6, 7, 8],
        )

    def test_reduced_counts_are_the_coprime_counts(self) -> None:
        self.assertEqual(
            [q_one.reduced_count_at(d) for d in range(1, 9)],
            [1, 1, 2, 2, 4, 2, 6, 4],
        )

    def test_joint_layers_are_least_common_multiples(self) -> None:
        report = q_one.report()
        joints = report["joint_layers"]
        assert isinstance(joints, list)
        self.assertEqual([case["joint"] for case in joints], [6, 12, 2, 1, 6])


class ReceiptReplayTests(unittest.TestCase):
    def test_receipt_replays_byte_identical(self) -> None:
        committed = (HERE / "receipts" / "q_one.json").read_bytes()
        regenerated = run_q_one.render(q_one.report())
        self.assertEqual(committed, regenerated)


if __name__ == "__main__":
    unittest.main()
