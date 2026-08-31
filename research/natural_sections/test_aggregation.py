"""Tests for the aggregation survey, against the pre-registered AG3 and
AG4 claims and the receipt."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import tempfile
import unittest
from pathlib import Path

import aggregation as ag
import run_aggregation as runner

TREE = Path(__file__).resolve().parent


class SurveyTests(unittest.TestCase):
    def test_edge_sum_is_additive_and_calibrated_everywhere(self) -> None:
        row = ag.survey()
        av = row["additivity_violations"]
        cf = row["calibration_failures"]
        assert isinstance(av, dict) and isinstance(cf, dict)
        self.assertEqual(av["edge_sum"], 0)
        self.assertEqual(cf["edge_sum"], 0)

    def test_max_aggregator_calibrated_but_not_additive(self) -> None:
        row = ag.survey()
        av = row["additivity_violations"]
        cf = row["calibration_failures"]
        assert isinstance(av, dict) and isinstance(cf, dict)
        self.assertGreater(av["max_agg"], 0)
        self.assertEqual(cf["max_agg"], 0)
        self.assertIsNotNone(row["first_max_violation_witness"])

    def test_doubled_additive_but_fails_calibration_on_exactly_810(self) -> None:
        """AG4: five edges times the 162 assignments with a nonzero
        phase at that edge."""
        row = ag.survey()
        av = row["additivity_violations"]
        cf = row["calibration_failures"]
        assert isinstance(av, dict) and isinstance(cf, dict)
        self.assertEqual(av["doubled"], 0)
        self.assertEqual(cf["doubled"], 810)

    def test_named_witness_replays(self) -> None:
        w = (1, 1, 0, 0, 0)
        self.assertEqual(ag.max_agg((0, 1), w), 1)
        self.assertEqual(ag.max_agg((0,), w) + ag.max_agg((1,), w), 2)


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically_and_matches_the_committed_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=TREE) as scratch:
            a = Path(scratch) / "a"
            b = Path(scratch) / "b"
            self.assertEqual(runner.main(["--out", str(a)]), 0)
            self.assertEqual(runner.main(["--out", str(b)]), 0)
            one = (a / "aggregation.json").read_bytes()
            self.assertEqual(one, (b / "aggregation.json").read_bytes())
            self.assertEqual(one, (TREE / "receipts" / "aggregation.json").read_bytes())

    def test_runner_refuses_an_output_directory_outside_the_tree(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(runner.main(["--out", outside]), 1)


if __name__ == "__main__":
    unittest.main()
