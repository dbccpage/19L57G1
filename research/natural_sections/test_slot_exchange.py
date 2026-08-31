"""Pins for the slot-exchange rung, exactly as pre-registered in STATUS.md."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import unittest
from pathlib import Path

import run_slot_exchange
import slot_exchange

HERE = Path(__file__).resolve().parent


class CharacterCountTests(unittest.TestCase):
    def test_rotation_admits_every_value(self) -> None:
        chars = slot_exchange.character_counts(8)
        self.assertEqual(chars["rotation_counts"], [1, 2, 3, 4, 5, 6, 7, 8])

    def test_swap_counts_alternate_with_parity(self) -> None:
        chars = slot_exchange.character_counts(8)
        self.assertEqual(chars["swap_counts"], [1, 2, 1, 2, 1, 2, 1, 2])

    def test_swap_admissible_values_are_the_two_torsion(self) -> None:
        self.assertEqual(slot_exchange.swap_admissible(4), [0, 2])
        self.assertEqual(slot_exchange.swap_admissible(5), [0])
        self.assertEqual(slot_exchange.swap_admissible(2), [0, 1])


class OddFamilyTests(unittest.TestCase):
    def test_exactly_seven_families_at_bound_three(self) -> None:
        checks = slot_exchange.odd_family_checks(3)
        self.assertEqual(checks["count"], 7)

    def test_every_total_is_zero(self) -> None:
        checks = slot_exchange.odd_family_checks(3)
        self.assertTrue(checks["all_totals_zero"])
        self.assertEqual(checks["totals"], [0] * 7)

    def test_pairing_cancels_with_zero_misses(self) -> None:
        checks = slot_exchange.odd_family_checks(3)
        self.assertEqual(checks["pairing_misses"], 0)


class DiscardCountermodelTests(unittest.TestCase):
    def test_full_total_zero_discarded_total_four(self) -> None:
        disc = slot_exchange.discard_countermodel()
        self.assertEqual(disc["full_total"], 0)
        self.assertEqual(disc["discarded_total"], 4)
        self.assertFalse(disc["conflatable"])


class DecompositionSurveyTests(unittest.TestCase):
    def test_moved_pair_always_cancels_and_totals_match_complement(self) -> None:
        dec = slot_exchange.decomposition_survey(2)
        self.assertEqual(dec["families"], 125)
        self.assertEqual(dec["moved_pair_nonzero"], 0)
        self.assertEqual(dec["total_mismatch"], 0)

    def test_fifty_negative_totals_price_the_residual_hypothesis(self) -> None:
        dec = slot_exchange.decomposition_survey(2)
        self.assertEqual(dec["negative_totals"], 50)


class ReceiptReplayTests(unittest.TestCase):
    def test_receipt_replays_byte_identical(self) -> None:
        committed = (HERE / "receipts" / "slot_exchange.json").read_bytes()
        regenerated = run_slot_exchange.render(slot_exchange.report())
        self.assertEqual(committed, regenerated)


if __name__ == "__main__":
    unittest.main()
