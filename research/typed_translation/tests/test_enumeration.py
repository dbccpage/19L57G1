from __future__ import annotations

import unittest

from typed_translation.enumerate import (
    COORDINATE_VALUES,
    Candidate,
    canonical_history_order,
    enumerate_candidates,
    enumerate_candidates_product,
    enumerate_histories,
    enumerate_histories_unpruned,
    iter_permutations,
    unique_states,
)
from typed_translation.model import SourceEvent, replay_source


class EnumerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.histories = enumerate_histories()
        cls.unpruned = enumerate_histories_unpruned()

    def test_history_count_is_nonvacuous_and_exact(self) -> None:
        self.assertEqual(len(self.histories), 1459)

    def test_unpruned_history_census_agrees_in_order(self) -> None:
        self.assertEqual(self.unpruned, self.histories)

    def test_every_prefix_replays(self) -> None:
        for history in self.histories:
            replay_source(history)

    def test_every_history_uses_each_event_at_most_once(self) -> None:
        self.assertTrue(all(len(set(history)) == len(history) for history in self.histories))

    def test_history_order_is_length_then_frozen_lexicographic(self) -> None:
        self.assertEqual(canonical_history_order(reversed(self.histories)), self.histories)

    def test_empty_and_full_histories_are_retained(self) -> None:
        self.assertEqual(self.histories[0], ())
        self.assertEqual(sum(len(history) == 8 for history in self.histories), 468)

    def test_unique_source_state_census(self) -> None:
        states = unique_states(self.histories)
        self.assertEqual(len(states), 22)
        self.assertEqual(len(set(states)), len(states))

    def test_candidate_product_has_seven_axes(self) -> None:
        self.assertEqual(len(COORDINATE_VALUES), 7)
        self.assertTrue(all(len(axis) == 2 for axis in COORDINATE_VALUES))

    def test_candidate_count_is_exact_and_unpruned(self) -> None:
        self.assertEqual(len(enumerate_candidates()), 128)

    def test_independent_candidate_product_agrees_in_order(self) -> None:
        self.assertEqual(enumerate_candidates_product(), enumerate_candidates())

    def test_candidate_record_carries_every_coordinate(self) -> None:
        candidate = enumerate_candidates()[-1]
        self.assertEqual(len(candidate.coordinates()), 7)
        self.assertEqual(set(candidate.as_record()), {
            "address_family",
            "event_context",
            "keep_labels",
            "mark_permutations",
            "outer_exchange",
            "synthetic_supply",
            "tag_levels_named",
        })

    def test_permutation_wrapper_is_total(self) -> None:
        self.assertEqual(tuple(iter_permutations((0, 1))), ((0, 1), (1, 0)))

    def test_candidate_constructor_retains_boolean_coordinates(self) -> None:
        candidate = Candidate("memoryless", False, False, False, False, False, "direct")
        self.assertEqual(candidate.coordinates()[1:6], (False, False, False, False, False))

    def test_dependency_order_is_present_in_every_full_history(self) -> None:
        for history in (row for row in self.histories if len(row) == 8):
            self.assertLess(history.index(SourceEvent.SUPPLY_D0), history.index(SourceEvent.ADMIT_D0))
            self.assertLess(history.index(SourceEvent.ADMIT_FORM), history.index(SourceEvent.ADMIT_RULE))


if __name__ == "__main__":
    unittest.main()
