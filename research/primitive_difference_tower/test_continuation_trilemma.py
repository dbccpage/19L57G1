"""Tests for Goal 4's declared continuation grammar."""

from __future__ import annotations

import unittest

from bridge_contract import Origin, Provenance, two_coordinate_contract
from continuation_trilemma import (
    AnchoredContinuation,
    ContinuationMode,
    RefusedContinuation,
    RetainedOrbitContinuation,
    declared_continuations,
    is_swap_stable,
    selected_singleton,
)
from equivariant_selection import AnchoredSingletonChoice, anchored_singleton_choice


class ContinuationTrilemmaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = two_coordinate_contract()
        self.left_anchor = anchored_singleton_choice(
            self.contract,
            (1, 0),
            Provenance("left-anchor", Origin.ADMITTED),
        )
        self.right_anchor = anchored_singleton_choice(
            self.contract,
            (0, 1),
            Provenance("right-anchor", Origin.ADMITTED),
        )

    def test_trilemma_preserves_both_supplied_tied_anchor_branches(self) -> None:
        branches = declared_continuations(
            self.contract,
            (self.left_anchor, self.right_anchor),
            "no-free-singleton",
        )
        self.assertEqual(
            [branch.mode for branch in branches],
            [
                ContinuationMode.ANCHORED_SINGLETON,
                ContinuationMode.ANCHORED_SINGLETON,
                ContinuationMode.RETAIN_ORBIT,
                ContinuationMode.REFUSE,
            ],
        )
        self.assertEqual(
            [selected_singleton(branch) for branch in branches],
            [(1, 0), (0, 1), None, None],
        )

    def test_only_aggregate_and_refusal_branches_are_swap_stable(self) -> None:
        branches = declared_continuations(
            self.contract,
            (self.left_anchor, self.right_anchor),
            "no-free-singleton",
        )
        self.assertEqual(
            [is_swap_stable(self.contract, branch) for branch in branches],
            [False, False, True, True],
        )
        aggregate = branches[2]
        assert isinstance(aggregate, RetainedOrbitContinuation)
        self.assertEqual(aggregate.members, self.contract.residual_orbit)
        refusal = branches[3]
        assert isinstance(refusal, RefusedContinuation)

    def test_aggregate_and_refusal_do_not_hide_a_singleton_choice(self) -> None:
        branches = declared_continuations(self.contract, (), "withhold-selection")
        self.assertEqual(len(branches), 2)
        self.assertTrue(all(selected_singleton(branch) is None for branch in branches))

    def test_no_anchor_is_manufactured_and_nonmembers_are_rejected(self) -> None:
        unsupported = AnchoredSingletonChoice(
            choice=(0, 0),
            anchor=Provenance("outside-orbit", Origin.ADMITTED),
        )
        with self.assertRaises(ValueError):
            declared_continuations(self.contract, (unsupported,), "refuse")
        branches = declared_continuations(self.contract, (self.left_anchor,), "refuse")
        anchored = branches[0]
        assert isinstance(anchored, AnchoredContinuation)
        self.assertEqual(anchored.selection.anchor.origin, Origin.ADMITTED)


if __name__ == "__main__":
    unittest.main()
