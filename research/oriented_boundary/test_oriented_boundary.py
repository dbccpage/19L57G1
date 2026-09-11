"""Tests for the (B)-empty mechanization. Exhaustive over the four judgments."""

from __future__ import annotations

import unittest

from oriented_boundary import (
    ALL_JUDGMENTS,
    S2_O,
    S2_U,
    _all_admitted_sets,
    b_is_empty,
    breaking_witnesses,
    distinguishes,
    has_A_witness,
    receipt,
    swap_in_aut,
    swap_preserves,
)


class TestBEmpty(unittest.TestCase):
    def test_symmetric_and_asymmetric_classification(self) -> None:
        self.assertEqual([d for d in ALL_JUDGMENTS if distinguishes(d)], [(False, True), (True, False)])
        self.assertEqual([d for d in ALL_JUDGMENTS if swap_preserves(d)], [(False, False), (True, True)])

    def test_b_is_empty_over_every_admitted_set(self) -> None:
        # The load-bearing lemma, exhaustively: no admitted set is a counterexample.
        for s in _all_admitted_sets():
            self.assertTrue(b_is_empty(s), f"(B)-empty failed on {s}")

    def test_swap_in_aut_iff_no_A_witness(self) -> None:
        # sigma in Aut EXACTLY when no admitted judgment distinguishes the pair.
        for s in _all_admitted_sets():
            self.assertEqual(swap_in_aut(s), not has_A_witness(s), f"iff failed on {s}")

    def test_from_nowhere_withdrawal_is_unrepresentable(self) -> None:
        # Route (B): sigma not in Aut with NO witness. It occurs for no admitted set.
        for s in _all_admitted_sets():
            if not swap_in_aut(s):
                self.assertTrue(has_A_witness(s), f"witnessless sigma-out-of-Aut on {s}")

    def test_unoriented_swap_is_an_automorphism(self) -> None:
        self.assertTrue(swap_in_aut(S2_U))  # AP1

    def test_oriented_breaks_it_at_exactly_one_capability(self) -> None:
        self.assertFalse(swap_in_aut(S2_O))  # AP2
        self.assertEqual(len(breaking_witnesses(S2_O)), 1)  # one capability

    def test_receipt_values(self) -> None:
        r = receipt()
        self.assertTrue(r["b_is_empty_over_all_admitted_sets"])
        self.assertTrue(r["swap_in_aut_iff_no_A_witness"])
        self.assertFalse(r["from_nowhere_withdrawal_representable"])
        self.assertTrue(r["S2_U_swap_is_automorphism"])
        self.assertFalse(r["S2_O_swap_is_automorphism"])
        self.assertEqual(r["S2_O_breaking_witness_count"], 1)
        self.assertEqual(r["n_admitted_sets_checked"], 16)


if __name__ == "__main__":
    unittest.main()
