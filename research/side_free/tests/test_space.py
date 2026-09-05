"""The presentation layer, the requirement, and the declared candidate space.

The negative direction is the point of most of these: a guard that cannot
fail is not a guard.
"""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "code"))

from sidefree import candidates as ctl  # noqa: E402
from sidefree.model import (  # noqa: E402
    AdmissionError,
    AdmitMark,
    AdmitOccurrence,
    Regime,
    Supply,
    genesis,
    replay,
)
from sidefree.presentation import (  # noqa: E402
    PRESENTED_POSITIONS,
    PresentationError,
    Whole,
    admission_event,
    read_whole,
    supply_event,
)
from sidefree.requirement import (  # noqa: E402
    DELETED_FROM_DECLARED,
    DELETED_FROM_SECOND_READING,
    DELETED_WORDS,
    REQUIREMENT,
    REQUIREMENT_SECOND_READING,
    RETAINED_MARKS,
    separates,
)

TREE = pathlib.Path(__file__).resolve().parent.parent
PIN = json.loads((TREE / "pinned" / "boundary_challenge3.json").read_text("utf-8"))


class Presentation(unittest.TestCase):
    def test_the_two_inscriptions_stay_two_facts(self) -> None:
        before, after = (read_whole(text) for text in ctl.INSCRIPTIONS)
        self.assertEqual(before.presented_position, "before")
        self.assertEqual(after.presented_position, "after")
        self.assertNotEqual(before, after)

    def test_a_whole_with_no_mark_reads_as_one(self) -> None:
        self.assertEqual(read_whole("<|>"), Whole(None, None))

    def test_the_reader_refuses_beyond_the_declared_bound_by_name(self) -> None:
        with self.assertRaises(PresentationError) as caught:
            read_whole("<ab|>")
        self.assertIn("more than one mark", str(caught.exception))
        with self.assertRaises(PresentationError) as caught:
            read_whole("<a|b>")
        self.assertIn("more than one mark", str(caught.exception))
        with self.assertRaises(PresentationError) as caught:
            read_whole("<<a|>|>")
        self.assertIn("not a whole", str(caught.exception))

    def test_a_mark_and_its_position_come_together(self) -> None:
        with self.assertRaises(PresentationError):
            Whole("a", None)
        with self.assertRaises(PresentationError):
            Whole("a", "sideways")

    def test_the_events_apply_nothing_and_carry_no_position(self) -> None:
        whole = read_whole("<a|>")
        self.assertEqual(supply_event(whole), Supply("a"))
        self.assertEqual(admission_event(whole), AdmitOccurrence("a"))
        with self.assertRaises(PresentationError):
            supply_event(Whole(None, None))
        with self.assertRaises(PresentationError):
            admission_event(Whole(None, None))

    def test_the_declared_positions_are_the_two(self) -> None:
        self.assertEqual(PRESENTED_POSITIONS, ("before", "after"))


class Requirement(unittest.TestCase):
    def test_the_control_text_is_the_pinned_text_with_the_phrase_deleted(self) -> None:
        pinned = PIN["requirement"]["declared"]
        self.assertEqual(pinned.count(DELETED_FROM_DECLARED), 1)
        self.assertEqual(pinned.replace(DELETED_FROM_DECLARED, "", 1), REQUIREMENT)

    def test_the_second_reading_likewise(self) -> None:
        pinned = PIN["requirement"]["second_reading"]
        self.assertEqual(pinned.count(DELETED_FROM_SECOND_READING), 1)
        self.assertEqual(
            pinned.replace(DELETED_FROM_SECOND_READING, "", 1),
            REQUIREMENT_SECOND_READING,
        )

    def test_neither_control_string_names_a_deleted_word(self) -> None:
        text = f" {REQUIREMENT} {REQUIREMENT_SECOND_READING} "
        for word in DELETED_WORDS:
            self.assertNotIn(f" {word} ", text)
            self.assertNotIn(f" {word},", text)

    def test_the_injection_of_the_phrase_back_is_caught(self) -> None:
        """Negative: reinserting the deleted phrase must not still match."""
        injected = REQUIREMENT.replace(
            "internally separable", "internally separable" + DELETED_FROM_DECLARED
        )
        self.assertNotEqual(injected, REQUIREMENT)
        self.assertEqual(injected, PIN["requirement"]["declared"])

    def test_the_retained_pair_is_the_pinned_pair(self) -> None:
        self.assertEqual(list(RETAINED_MARKS), PIN["requirement"]["retained_marks"])

    def test_the_verdict_function_is_what_it_says(self) -> None:
        self.assertTrue(separates([(0, 1)], 0, 1))
        self.assertFalse(separates([(0, 1), (1, 0)], 0, 1))
        self.assertTrue(separates([], 0, 1))


class DeletionCriterion(unittest.TestCase):
    def test_the_mechanical_partition_equals_the_implemented_one(self) -> None:
        pinned = PIN["candidate_space"]["capability_of"]
        mechanical = sorted(name for name, text in pinned.items() if ctl.transfers(text))
        self.assertEqual(mechanical, sorted(ctl.COORDINATES))

    def test_the_partition_has_no_borderline_case(self) -> None:
        """Every pinned sentence is decided, and the two sides are non-empty."""
        pinned = PIN["candidate_space"]["capability_of"]
        decided = [ctl.transfers(text) for text in pinned.values()]
        self.assertEqual(len(decided), 5)
        self.assertEqual(sum(decided), 3)

    def test_moving_a_coordinate_across_the_criterion_is_caught(self) -> None:
        """Negative: a sentence that gains the word must stop transferring."""
        text = ctl.CAPABILITY_OF["keep_labels"]
        self.assertTrue(ctl.transfers(text))
        self.assertFalse(ctl.transfers(text + ", one per side"))
        self.assertFalse(ctl.transfers("the side-name form"))
        self.assertTrue(ctl.transfers("a sideways glance at nothing"))

    def test_the_capability_texts_are_byte_identical(self) -> None:
        pinned = PIN["candidate_space"]["capability_of"]
        for name in ctl.COORDINATES:
            self.assertEqual(ctl.CAPABILITY_OF[name], pinned[name])

    def test_the_names_are_string_identical_so_the_join_is_by_equality(self) -> None:
        for name in ctl.COORDINATES:
            self.assertIn(name, PIN["candidate_space"]["coordinates"])

    def test_the_value_set_change_is_read_from_the_pin(self) -> None:
        """extra_mark_0 and extra_mark_1 are ONE retained class under U."""
        classes = PIN["readings"]["U"]["minima_by_mu1"]["classes"]
        members = [c["members"] for c in classes]
        self.assertIn(["extra_mark_0", "extra_mark_1"], members)
        self.assertEqual(len(ctl.EXTRA_MARK_VALUES), 2)
        self.assertEqual(len(ctl.PINNED_EXTRA_MARK_VALUES), 3)


class CandidateSpace(unittest.TestCase):
    def test_the_space_is_eight_points_with_three_one_step(self) -> None:
        space = ctl.candidate_space()
        self.assertEqual(len(space), 8)
        self.assertEqual(sum(1 for a in space if len(ctl.changed_coordinates(a)) == 1), 3)
        self.assertEqual(sum(1 for a in space if len(ctl.changed_coordinates(a)) >= 2), 4)

    def test_each_coordinate_is_tested_against_its_own_inherited_value(self) -> None:
        """Negative: a coordinate inherited at True must count False as moved."""
        self.assertEqual(ctl.changed_coordinates(ctl.NULL_AUGMENTATION), [])
        for name in ctl.COORDINATES:
            self.assertIn(name, ctl.INHERITED)
            flipped = {n: (n == name) for n in ctl.COORDINATES}
            aug = ctl.Augmentation(**flipped)
            self.assertEqual(ctl.changed_coordinates(aug), [name])

    def test_the_guard_would_bite_if_an_inherited_value_moved(self) -> None:
        original = dict(ctl.INHERITED)
        try:
            ctl.INHERITED["keep_labels"] = True
            self.assertEqual(
                ctl.changed_coordinates(ctl.NULL_AUGMENTATION), ["keep_labels"]
            )
        finally:
            ctl.INHERITED.clear()
            ctl.INHERITED.update(original)
        self.assertEqual(ctl.changed_coordinates(ctl.NULL_AUGMENTATION), [])

    def test_an_unknown_coordinate_is_refused_by_name(self) -> None:
        with self.assertRaises(ValueError):
            ctl.NULL_AUGMENTATION.value_of("withdraw_reflection")

    def test_point_names_are_deterministic(self) -> None:
        self.assertEqual(ctl.point_name(ctl.NULL_AUGMENTATION), "base")
        self.assertEqual(
            ctl.point_name(ctl.Augmentation(keep_labels=True, extra_mark=True)),
            "keep_labels+extra_mark",
        )
        self.assertEqual(
            ctl.Augmentation(keep_labels=True).values(), (False, True, False)
        )

    def test_capabilities_are_one_per_moved_coordinate(self) -> None:
        aug = ctl.Augmentation(keep_labels=True, extra_mark=True)
        self.assertEqual(len(ctl.capabilities(aug)), 2)
        self.assertEqual(ctl.capabilities(ctl.NULL_AUGMENTATION), [])


class Histories(unittest.TestCase):
    def test_every_regime_is_the_replay_of_an_explicit_history(self) -> None:
        wholes = ctl.caller_wholes()
        for aug in ctl.candidate_space():
            history = ctl.candidate_history(wholes, aug)
            main, _order, _label = ctl.comparison_regimes(wholes, aug)
            self.assertEqual(replay(history, genesis()), main)

    def test_the_further_mark_uses_the_token_already_supplied(self) -> None:
        aug = ctl.Augmentation(extra_mark=True)
        added = ctl.process_admission(aug)
        self.assertEqual(added, [AdmitOccurrence(ctl.SUPPLIED_TOKEN)])
        self.assertEqual(ctl.process_admission(ctl.NULL_AUGMENTATION), [])

    def test_a_never_supplied_token_is_refused_by_name(self) -> None:
        with self.assertRaises(AdmissionError) as caught:
            replay([AdmitOccurrence("q")], genesis())
        self.assertIn("q", str(caught.exception))

    def test_the_shared_policy_yields_one_mark_and_no_subject(self) -> None:
        wholes = ctl.caller_wholes()
        shared = replay(ctl.shared_policy_history(wholes), genesis())
        self.assertEqual(shared.n_marks(), 1)
        declared = replay(ctl.caller_history(wholes), genesis())
        self.assertEqual(declared.n_marks(), 2)

    def test_a_whole_with_no_mark_cannot_be_retained(self) -> None:
        with self.assertRaises(AdmissionError):
            ctl.caller_history([Whole(None, None)])
        with self.assertRaises(AdmissionError):
            ctl.shared_policy_history([Whole(None, None)])

    def test_the_two_orders_give_the_same_regime_and_the_reason_is_stated(self) -> None:
        wholes = ctl.caller_wholes()
        forward = replay(ctl.caller_history(wholes), genesis())
        backward = replay(ctl.caller_history(list(reversed(wholes))), genesis())
        self.assertEqual(forward, backward)
        self.assertIn("same token", ctl.ORDER_FACT_REASON)
        self.assertIn("NOT", ctl.ORDER_FACT_REASON)

    def test_relabelling_keeps_the_arity_and_changes_the_labels(self) -> None:
        r = Regime(("a", "a"))
        self.assertEqual(ctl.relabelled(r).marks, ("z", "z"))

    def test_the_probe_set_offers_every_event_kind(self) -> None:
        kinds = {type(e).__name__ for e in ctl.probes("a")}
        self.assertEqual(kinds, {"Supply", "AdmitMark", "AdmitOccurrence"})


class MarkProperties(unittest.TestCase):
    def test_the_residue_judgment_is_a_declared_property(self) -> None:
        names = [name for name, _prop in ctl.DECLARED_MARK_PROPERTIES]
        self.assertEqual(
            names, ["admitted", "has_index_0", "has_index_1", "carries_label_a"]
        )

    def test_the_domain_is_every_hypothetical_regime_to_the_bound(self) -> None:
        self.assertEqual(len(ctl.property_domain(3)), 15)
        self.assertEqual(len(ctl.property_domain(0)), 1)

    def test_the_index_properties_are_invariant_only_with_the_permutations_gone(
        self,
    ) -> None:
        domain = ctl.property_domain(2)
        kept = ctl.domain_images(domain, True)
        gone = ctl.domain_images(domain, False)
        index = dict(ctl.DECLARED_MARK_PROPERTIES)["has_index_0"]
        self.assertFalse(ctl.property_invariant(index, kept))
        self.assertTrue(ctl.property_invariant(index, gone))

    def test_the_residue_judgment_separates_nothing(self) -> None:
        admitted = dict(ctl.DECLARED_MARK_PROPERTIES)["admitted"]
        for aug in ctl.candidate_space():
            for r in ctl.route_census_regimes(aug):
                self.assertFalse(ctl.property_separates(admitted, r))

    def test_the_label_property_is_invariant_and_reads_the_state(self) -> None:
        label = dict(ctl.DECLARED_MARK_PROPERTIES)["carries_label_a"]
        self.assertTrue(label(Regime(("a", "z")), 0))
        self.assertFalse(label(Regime(("a", "z")), 1))
        self.assertFalse(label(Regime(()), 0))


class Census(unittest.TestCase):
    def test_the_withdrawal_census_is_eight_cells(self) -> None:
        self.assertEqual(len(ctl.withdrawal_census(True)), 8)
        self.assertEqual(sum(ctl.withdrawal_census(True)), 2)
        self.assertEqual(sum(ctl.withdrawal_census(False)), 8)

    def test_the_route_census_domain_grows_with_the_further_mark(self) -> None:
        base = ctl.route_census_regimes(ctl.NULL_AUGMENTATION)
        extra = ctl.route_census_regimes(ctl.Augmentation(extra_mark=True))
        self.assertEqual(len(base), 4)
        self.assertEqual(len(extra), 4)
        self.assertEqual({r.n_marks() for r in base}, {2})
        self.assertEqual({r.n_marks() for r in extra}, {3})


class CollateralFacts(unittest.TestCase):
    def test_only_two_pinned_facts_have_a_side_free_subject(self) -> None:
        self.assertEqual(len(ctl.COLLATERAL_FACTS), 2)
        self.assertEqual(len(ctl.PINNED_COLLATERAL_FACTS_WITHOUT_A_SIDE_FREE_SUBJECT), 3)
        self.assertEqual(
            sorted(
                [*ctl.COLLATERAL_FACTS, *ctl.PINNED_COLLATERAL_FACTS_WITHOUT_A_SIDE_FREE_SUBJECT]
            ),
            sorted(PIN["collateral_facts"]),
        )

    def test_the_label_fact_turns_on_exactly_at_keep_labels(self) -> None:
        wholes = ctl.caller_wholes()
        for aug in ctl.candidate_space():
            facts = ctl.collateral_facts(wholes, aug)
            self.assertEqual(facts["label_internally_available"], aug.keep_labels)
            self.assertFalse(facts["order_internally_available"])


if __name__ == "__main__":
    unittest.main()
