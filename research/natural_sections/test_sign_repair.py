"""Tests for the sign-repair rung, mirroring the STATUS.md registration."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

import run_sign_repair
import sign_repair

HERE = Path(__file__).resolve().parent


class SurveyTests(unittest.TestCase):
    def test_family_and_odd_counts_with_zero_moved_total_misses(self) -> None:
        report = sign_repair.report()
        self.assertEqual(report["family_count"], 15625)
        self.assertEqual(report["fibrewise_odd_count"], 625)
        self.assertEqual(report["fibrewise_odd_moved_total_misses"], 0)

    def test_counting_and_search_decisions_agree_everywhere(self) -> None:
        report = sign_repair.report()
        self.assertEqual(report["certificate_agreement_misses"], 0)

    def test_positive_total_does_not_buy_a_certificate(self) -> None:
        report = sign_repair.report()
        count = report["positive_total_uncertified_count"]
        assert isinstance(count, int)
        self.assertGreater(count, 0)
        minimal = report["minimal_positive_total_uncertified"]
        assert isinstance(minimal, list)
        self.assertGreater(sum(minimal), 0)
        self.assertFalse(
            sign_repair.has_certificate_by_counting(tuple(minimal))
        )

    def test_the_open_question_is_answered_yes_at_the_bound(self) -> None:
        report = sign_repair.report()
        self.assertTrue(report["open_question_answer_at_bound"])
        self.assertTrue(report["pinned_witness_is_interacting"])
        self.assertTrue(report["pinned_witness_has_certificate"])

    def test_pinned_witness_certificate_is_the_lean_decomposition(self) -> None:
        """The Lean module exhibits pairs [1, 2] and residual [1, 1] for
        the pinned witness; the multisets must match."""

        w = sorted(sign_repair.PINNED_WITNESS)
        decomposition = sorted([1, -1, 2, -2] + [1, 1])
        self.assertEqual(w, decomposition)


class ReceiptTests(unittest.TestCase):
    def test_receipt_replays_byte_identically(self) -> None:
        committed = (HERE / "receipts" / "sign_repair.json").read_bytes()
        self.assertEqual(committed, run_sign_repair.render(sign_repair.report()))


if __name__ == "__main__":
    unittest.main()
