"""The side-free carrier: events, replay, certification, keys, renaming.

Every certified state in this file is the replay of an explicit history from
genesis.  Nothing here mutates admitted state by any other route, and the
negative tests below fail if that stops being true.
"""

from __future__ import annotations

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "code"))

from sidefree.model import (  # noqa: E402
    DECLARED_KEY_CHOICE,
    INITIAL_DATUM,
    KEY_CHOICES,
    Admitted,
    AdmitMark,
    AdmitOccurrence,
    AdmissionError,
    Event,
    OpaqueDatum,
    Regime,
    Supply,
    automorphisms_under,
    canonical_under,
    certify,
    event_follows,
    genesis,
    is_isomorphic_under,
    key_of,
    mark_automorphism_to_under,
    mark_observations,
    mark_orbit_under,
    mark_profile,
    marks_separable_under,
    mentioned,
    new_observations,
    no_permitted_renaming_moves_an_index,
    observation_holds,
    observations,
    permitted_images_under,
    rename_marks,
    replay,
    serialize,
    serialize_keeping_labels,
    step,
    supplied,
)
from sidefree.requirement import separates  # noqa: E402


class SuppliedDatum(unittest.TestCase):
    def test_genesis_admits_nothing(self) -> None:
        self.assertEqual(genesis().n_marks(), 0)
        self.assertEqual(genesis().marks, ())

    def test_the_initial_datum_is_fixed(self) -> None:
        with self.assertRaises(AdmissionError):
            Regime((), OpaqueDatum(1))

    def test_the_datum_numeral_is_not_a_mark_index(self) -> None:
        r = replay([Supply("a"), AdmitOccurrence("a")], genesis())
        self.assertEqual(r.initial_datum, INITIAL_DATUM)
        self.assertEqual(r.initial_datum.internal_id, 0)
        self.assertEqual(r.n_marks(), 1)


class Events(unittest.TestCase):
    def test_supply_changes_no_state(self) -> None:
        r = genesis()
        self.assertEqual(step(r, Supply("a")), r)
        after = replay([Supply("a"), Supply("z")], genesis())
        self.assertEqual(after, genesis())

    def test_only_an_admission_changes_state(self) -> None:
        before = genesis()
        after = step(before, AdmitOccurrence("a"))
        self.assertNotEqual(before, after)
        self.assertEqual(after.marks, ("a",))

    def test_occurrence_admission_is_fresh_whatever_the_label(self) -> None:
        r = replay(
            [Supply("a"), AdmitOccurrence("a"), Supply("a"), AdmitOccurrence("a")],
            genesis(),
        )
        self.assertEqual(r.marks, ("a", "a"))

    def test_label_keyed_admission_of_a_held_label_is_a_no_op(self) -> None:
        r = Regime(("a",))
        self.assertEqual(step(r, AdmitMark("a")), r)

    def test_label_keyed_admission_is_refused_by_name_on_a_repeated_label(self) -> None:
        r = Regime(("a", "a"))
        with self.assertRaises(AdmissionError) as caught:
            step(r, AdmitMark("a"))
        self.assertIn("names more than one admitted mark", str(caught.exception))

    def test_replay_refuses_an_admission_never_supplied(self) -> None:
        with self.assertRaises(AdmissionError) as caught:
            replay([AdmitOccurrence("q")], genesis())
        self.assertIn("was not supplied before admission", str(caught.exception))
        with self.assertRaises(AdmissionError) as caught:
            replay([AdmitMark("q")], genesis())
        self.assertIn("was not supplied before admission", str(caught.exception))

    def test_label_keyed_admission_of_an_already_admitted_mark_needs_no_supply(
        self,
    ) -> None:
        history: list[Event] = [Supply("a"), AdmitOccurrence("a"), AdmitMark("a")]
        self.assertEqual(replay(history, genesis()).marks, ("a",))

    def test_certify_is_replay_equality_and_refuses_rather_than_raising(self) -> None:
        history: list[Event] = [Supply("a"), AdmitOccurrence("a")]
        self.assertTrue(certify(history, genesis(), Regime(("a",))))
        self.assertFalse(certify(history, genesis(), Regime(("z",))))
        self.assertFalse(certify([AdmitOccurrence("q")], genesis(), genesis()))

    def test_no_event_is_entailed_by_state(self) -> None:
        r = Regime(("a",))
        for e in (Supply("a"), AdmitMark("a"), AdmitOccurrence("a")):
            self.assertFalse(event_follows(r, e))

    def test_mentioned_and_supplied_read_a_history(self) -> None:
        history: list[Event] = [Supply("a"), AdmitOccurrence("a"), AdmitMark("z")]
        self.assertEqual(mentioned(history), frozenset({"a", "z"}))
        self.assertEqual(supplied(history), frozenset({"a"}))


class ObservationGrammar(unittest.TestCase):
    def test_the_extension_is_empty_at_genesis(self) -> None:
        self.assertEqual(observations(genesis()), frozenset())
        self.assertEqual(mark_observations(genesis()), frozenset())

    def test_the_one_form_holds_exactly_of_the_admitted(self) -> None:
        r = Regime(("a", "a"))
        self.assertTrue(observation_holds(r, Admitted(0)))
        self.assertTrue(observation_holds(r, Admitted(1)))
        self.assertFalse(observation_holds(r, Admitted(2)))

    def test_a_negative_mark_identity_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            Admitted(-1)

    def test_the_profile_of_a_mark_names_only_that_mark(self) -> None:
        r = Regime(("a", "a"))
        self.assertEqual(mark_profile(r, 1), frozenset({Admitted(1)}))
        with self.assertRaises(ValueError):
            mark_profile(r, 2)

    def test_new_observations_is_the_difference_of_two_extensions(self) -> None:
        before = Regime(("a",))
        after = Regime(("a", "a"))
        self.assertEqual(new_observations(before, after), frozenset({Admitted(1)}))


class RenamingAndKeys(unittest.TestCase):
    def test_renaming_carries_labels_with_their_marks(self) -> None:
        r = Regime(("a", "z"))
        self.assertEqual(rename_marks(r, (1, 0)).marks, ("z", "a"))

    def test_a_non_permutation_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            rename_marks(Regime(("a", "z")), (0, 0))

    def test_the_declared_key_forgets_the_labels_and_keeps_the_arity(self) -> None:
        self.assertEqual(serialize(Regime(("a", "z"))), (2,))
        self.assertEqual(serialize(Regime(("a", "z")), "empty"), ())
        self.assertEqual(serialize_keeping_labels(Regime(("a", "z"))), (("a", "z"),))
        with self.assertRaises(ValueError):
            serialize(Regime(()), "some other choice")

    def test_key_of_switches_on_the_declared_flag(self) -> None:
        r = Regime(("a", "z"))
        self.assertEqual(key_of(r, False), (2,))
        self.assertEqual(key_of(r, True), (("a", "z"),))

    def test_the_permitted_images_are_unpruned(self) -> None:
        r = Regime(("a", "z", "a"))
        self.assertEqual(len(permitted_images_under(r, True)), 6)
        self.assertEqual(len(permitted_images_under(r, False)), 1)

    def test_withdrawing_the_permutations_leaves_only_the_identity(self) -> None:
        r = Regime(("a", "a"))
        self.assertTrue(no_permitted_renaming_moves_an_index(r, False))
        self.assertFalse(no_permitted_renaming_moves_an_index(r, True))

    def test_automorphisms_at_the_retained_regime(self) -> None:
        r = Regime(("a", "a"))
        self.assertEqual(len(automorphisms_under(r, True, False)), 2)
        self.assertEqual(len(automorphisms_under(r, False, False)), 1)
        self.assertEqual(len(automorphisms_under(r, True, True)), 2)
        self.assertEqual(len(automorphisms_under(Regime(("a", "z")), True, True)), 1)

    def test_separability_is_the_one_shared_verdict_and_not_a_second_one(self) -> None:
        """The kernel's separability must BE ``separates`` over its own set."""
        for marks in (("a", "a"), ("a", "z")):
            for mp in (False, True):
                for kl in (False, True):
                    r = Regime(marks)
                    self.assertEqual(
                        marks_separable_under(r, 0, 1, mp, kl),
                        separates(automorphisms_under(r, mp, kl), 0, 1),
                    )

    def test_separability_refuses_a_mark_that_is_not_admitted(self) -> None:
        with self.assertRaises(ValueError):
            marks_separable_under(Regime(("a",)), 0, 1, True, False)

    def test_the_witness_search_finds_the_exchange_and_refuses_a_bad_mark(self) -> None:
        r = Regime(("a", "a"))
        self.assertEqual(mark_automorphism_to_under(r, 0, 1, True, False), (1, 0))
        self.assertIsNone(mark_automorphism_to_under(r, 0, 1, False, False))
        with self.assertRaises(ValueError):
            mark_automorphism_to_under(r, 0, 5, True, False)

    def test_isomorphism_is_the_implemented_relation_not_equality(self) -> None:
        a = Regime(("a", "z"))
        b = Regime(("z", "a"))
        self.assertNotEqual(a, b)
        self.assertTrue(is_isomorphic_under(a, b, True, True))
        self.assertFalse(is_isomorphic_under(a, b, False, True))
        self.assertTrue(is_isomorphic_under(a, b, False, False))

    def test_the_canonical_key_is_the_minimum_over_the_permitted_images(self) -> None:
        self.assertEqual(canonical_under(Regime(("z", "a")), True, True), (("a", "z"),))
        self.assertEqual(canonical_under(Regime(("z", "a")), False, True), (("z", "a"),))
        self.assertEqual(canonical_under(Regime(("z", "a")), True, False), (2,))

    def test_the_orbit_is_the_witness_the_second_reading_asks_for(self) -> None:
        r = Regime(("a", "a"))
        orbit = mark_orbit_under(r, 0, True, False)
        self.assertIn((repr((2,)), 1), orbit)
        self.assertNotIn((repr((2,)), 1), mark_orbit_under(r, 0, False, False))
        with self.assertRaises(ValueError):
            mark_orbit_under(r, 9, True, False)

    def test_both_declared_key_choices_are_offered(self) -> None:
        self.assertEqual(KEY_CHOICES, ("arity", "empty"))
        self.assertEqual(DECLARED_KEY_CHOICE, "arity")


if __name__ == "__main__":
    unittest.main()
