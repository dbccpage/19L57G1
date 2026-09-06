"""Tests of the boundary kernel, Challenges 0 and 1."""

from __future__ import annotations

import pathlib
import sys
import unittest

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE / "code"))

from boundary.model import (  # noqa: E402
    INITIAL_DATUM,
    automorphisms_under,
    canonical_under,
    is_isomorphic_under,
    mark_automorphism_to_under,
    mark_orbit_under,
    marks_separable_under,
    permitted_images_under,
    serialize_keeping_labels,
    side_exchanging_automorphism_under,
    OBSERVATION_TYPES,
    READING_O,
    READING_U,
    READINGS,
    SIDE_NAMES,
    AdmissionError,
    AdmitMark,
    AdmitOccurrence,
    Event,
    OnSide,
    OpaqueDatum,
    Regime,
    SideNamed,
    Supply,
    automorphisms,
    canonical,
    certify,
    contents,
    event_follows,
    genesis,
    is_automorphism_reflection,
    is_isomorphic,
    isomorphism_witness,
    mark_automorphism_to,
    mark_observations,
    mark_profile,
    mark_side,
    marks_internally_separable,
    marks_on_different_sides,
    mentioned,
    name_observations,
    new_observations,
    observation_holds,
    observations,
    permitted_images,
    reflect,
    rename_marks,
    replay,
    serialize,
    side_exchanging_automorphism,
    side_profile,
    sides_collapsed,
    step,
    supplied,
)
from itertools import product  # noqa: E402


class GenesisTests(unittest.TestCase):
    def test_two_readings_only(self) -> None:
        self.assertEqual(READINGS, ("U", "O"))
        for rd in READINGS:
            g = genesis(rd)
            self.assertEqual(g.n_marks(), 0)
            self.assertEqual(g.placement, ())
            self.assertEqual(g.initial_datum, INITIAL_DATUM)

    def test_unknown_reading_refused(self) -> None:
        with self.assertRaises(AdmissionError):
            genesis("V")

    def test_invalid_regimes_are_refused(self) -> None:
        bad = (
            ("V", (), (), INITIAL_DATUM),
            (READING_U, ("a",), (), INITIAL_DATUM),
            (READING_U, ("a",), (2,), INITIAL_DATUM),
            (READING_U, (), (), OpaqueDatum(1)),
        )
        for args in bad:
            with self.subTest(args=args), self.assertRaises(AdmissionError):
                Regime(*args)

    def test_a_repeated_label_is_a_valid_regime_from_challenge_2(self) -> None:
        # Challenges 0 and 1 refused this construction, which identified the
        # presentation token with the internal identity.  Challenge 2 supplies
        # two wholes carrying the same visible mark, so the requirement is
        # withdrawn: the label repeats and the two internal identities, the
        # admission indices, do not.
        r = Regime(READING_U, ("a", "a"), (0, 1))
        self.assertEqual(r.n_marks(), 2)
        self.assertEqual(mark_side(r, 0), 0)
        self.assertEqual(mark_side(r, 1), 1)
        self.assertNotEqual(mark_profile(r, 0), mark_profile(r, 1))


class EventTests(unittest.TestCase):
    def test_supply_is_not_admission(self) -> None:
        for rd in READINGS:
            g = genesis(rd)
            self.assertEqual(step(g, Supply("a")), g)
            self.assertEqual(replay([Supply("a"), Supply("b"), Supply("a")], g), g)

    def test_low_level_step_places_one_mark(self) -> None:
        r = step(genesis(READING_U), AdmitMark("a", 0))
        self.assertEqual(r.marks, ("a",))
        self.assertEqual(r.placement, (0,))
        r2 = step(r, AdmitMark("b", 1))
        self.assertEqual(r2.placement, (0, 1))

    def test_readmission_on_its_side_is_a_no_op(self) -> None:
        r = step(genesis(READING_O), AdmitMark("a", 1))
        self.assertEqual(step(r, AdmitMark("a", 1)), r)
        self.assertEqual(replay([Supply("a"), AdmitMark("a", 1), AdmitMark("a", 1)], genesis(READING_O)), r)

    def test_moving_admission_is_refused_by_name(self) -> None:
        for rd in READINGS:
            r = step(genesis(rd), AdmitMark("a", 0))
            with self.assertRaisesRegex(AdmissionError, "admitted on side 0.*side 1 would move it"):
                step(r, AdmitMark("a", 1))
            history: list[Event] = [Supply("a"), AdmitMark("a", 0), AdmitMark("a", 1)]
            with self.assertRaisesRegex(AdmissionError, "would move it and is refused"):
                replay(history, genesis(rd))
            self.assertFalse(certify(history, genesis(rd), r))
            self.assertFalse(certify(history, genesis(rd), Regime(rd, ("a",), (1,))))

    def test_bad_side_refused(self) -> None:
        with self.assertRaises(AdmissionError):
            step(genesis(READING_U), AdmitMark("a", 2))

    def test_replay_certifies_and_refuses(self) -> None:
        g = genesis(READING_U)
        history: list[Event] = [Supply("a"), AdmitMark("a", 0), Supply("b")]
        claimed = Regime(READING_U, ("a",), (0,))
        self.assertTrue(certify(history, g, claimed))
        self.assertFalse(certify(history, g, Regime(READING_U, ("a",), (1,))))
        self.assertFalse(certify(history[:1], g, claimed))

    def test_certifying_replay_refuses_unsupplied_admission(self) -> None:
        g = genesis(READING_U)
        event = AdmitMark("never-supplied", 0)
        with self.assertRaises(AdmissionError):
            replay([event], g)
        self.assertFalse(certify([event], g, Regime(READING_U, ("never-supplied",), (0,))))

    def test_no_event_follows_from_challenge0_state(self) -> None:
        for rd in READINGS:
            g = genesis(rd)
            self.assertFalse(event_follows(g, Supply("a")))
            self.assertFalse(event_follows(g, AdmitMark("a", 0)))


class ObservationTests(unittest.TestCase):
    def test_genesis_contents_empty_on_both_sides(self) -> None:
        for rd in READINGS:
            g = genesis(rd)
            self.assertEqual(contents(g, 0), frozenset())
            self.assertEqual(contents(g, 1), frozenset())
            self.assertEqual(mark_observations(g), frozenset())
        self.assertEqual(observations(genesis(READING_U)), frozenset())
        self.assertEqual(
            observations(genesis(READING_O)),
            frozenset((SideNamed(0, "near"), SideNamed(1, "far"))),
        )

    def test_closed_observation_grammar_and_holds(self) -> None:
        self.assertEqual(OBSERVATION_TYPES, (OnSide, SideNamed))
        u = Regime(READING_U, ("a",), (0,))
        o = Regime(READING_O, ("a",), (0,))
        self.assertTrue(observation_holds(u, OnSide(0, 0)))
        self.assertFalse(observation_holds(u, OnSide(0, 1)))
        self.assertFalse(observation_holds(u, OnSide(1, 0)))
        self.assertFalse(observation_holds(u, SideNamed(0, "near")))
        self.assertTrue(observation_holds(o, SideNamed(0, "near")))
        self.assertFalse(observation_holds(o, SideNamed(0, "far")))
        self.assertEqual(name_observations(u), frozenset())
        with self.assertRaises(ValueError):
            OnSide(-1, 0)
        with self.assertRaises(ValueError):
            OnSide(0, 2)
        with self.assertRaises(ValueError):
            SideNamed(2, "elsewhere")

    def test_contents_refuses_a_third_side(self) -> None:
        with self.assertRaises(ValueError):
            contents(genesis(READING_U), 2)
        with self.assertRaises(ValueError):
            side_profile(genesis(READING_U), 2)

    def test_sides_collapsed_under_U_and_named_under_O(self) -> None:
        self.assertTrue(sides_collapsed(genesis(READING_U)))
        self.assertFalse(sides_collapsed(genesis(READING_O)))
        o = genesis(READING_O)
        self.assertEqual(side_profile(o, 0), (SIDE_NAMES[0], frozenset()))
        self.assertEqual(side_profile(o, 1), (SIDE_NAMES[1], frozenset()))
        self.assertEqual(side_profile(genesis(READING_U), 0), (frozenset(),))

    def test_one_mark_separates_the_sides_under_both_readings(self) -> None:
        for rd in READINGS:
            r = step(genesis(rd), AdmitMark("a", 0))
            self.assertFalse(sides_collapsed(r))
            self.assertEqual(contents(r, 0), frozenset({0}))
            self.assertEqual(mark_observations(r), frozenset({OnSide(0, 0)}))


class RenamingTests(unittest.TestCase):
    def test_reflect_is_an_involution_and_swaps_sides(self) -> None:
        r = Regime(READING_U, ("a", "b", "c"), (0, 1, 1))
        self.assertEqual(reflect(r).placement, (1, 0, 0))
        self.assertEqual(reflect(reflect(r)), r)

    def test_reflect_commutes_with_replay(self) -> None:
        # The falsifier of the commutation claim: a history whose reflected
        # replay is not the replay of the side-exchanged history.  Every
        # history of up to three events over two tokens is tried from genesis
        # under both readings; a refused history must be refused exchanged.
        def exchange(e: Event) -> Event:
            return e if isinstance(e, Supply) else AdmitMark(e.token, 1 - e.side)

        alphabet: list[Event] = [
            Supply("a"), Supply("b"),
            AdmitMark("a", 0), AdmitMark("a", 1), AdmitMark("b", 0), AdmitMark("b", 1),
        ]
        checked = 0
        for rd in READINGS:
            g = genesis(rd)
            for n in range(4):
                for history in product(alphabet, repeat=n):
                    exchanged = [exchange(e) for e in history]
                    try:
                        after = replay(list(history), g)
                    except AdmissionError:
                        with self.assertRaises(AdmissionError):
                            replay(exchanged, g)
                        continue
                    self.assertEqual(reflect(after), replay(exchanged, reflect(g)), history)
                    checked += 1
        # 43 accepted histories per reading: 1 + 2 + 8 + 32 by length.
        self.assertEqual(checked, 86)

    def test_rename_marks_permutes_and_refuses(self) -> None:
        r = Regime(READING_O, ("a", "b"), (0, 1))
        self.assertEqual(rename_marks(r, (1, 0)), Regime(READING_O, ("b", "a"), (1, 0)))
        with self.assertRaises(ValueError):
            rename_marks(r, (0, 0))

    def test_serialize_forgets_tokens(self) -> None:
        a = Regime(READING_U, ("a",), (0,))
        b = Regime(READING_U, ("z",), (0,))
        self.assertEqual(serialize(a), serialize(b))

    def test_canonical_identifies_the_reflection_under_U_only(self) -> None:
        left_u = Regime(READING_U, ("a",), (0,))
        right_u = Regime(READING_U, ("a",), (1,))
        self.assertEqual(canonical(left_u), canonical(right_u))
        left_o = Regime(READING_O, ("a",), (0,))
        right_o = Regime(READING_O, ("a",), (1,))
        self.assertNotEqual(canonical(left_o), canonical(right_o))

    def test_canonical_is_invariant_under_mark_renaming(self) -> None:
        r = Regime(READING_O, ("a", "b", "c"), (0, 1, 0))
        self.assertEqual(canonical(r), canonical(rename_marks(r, (2, 0, 1))))

    def test_reflection_automorphism_at_genesis(self) -> None:
        self.assertTrue(is_automorphism_reflection(genesis(READING_U)))
        self.assertFalse(is_automorphism_reflection(genesis(READING_O)))
        self.assertFalse(is_automorphism_reflection(Regime(READING_U, ("a",), (0,))))
        self.assertTrue(
            is_automorphism_reflection(Regime(READING_U, ("a", "b"), (0, 1)))
        )
        self.assertFalse(is_automorphism_reflection(Regime(READING_O, ("a",), (0,))))

class Challenge1KernelTests(unittest.TestCase):
    def test_mention_is_not_supply_and_not_admission(self) -> None:
        history: list[Event] = [Supply("a"), AdmitMark("a", 0), AdmitMark("c", 1)]
        self.assertEqual(mentioned(history), frozenset({"a", "c"}))
        self.assertEqual(supplied(history), frozenset({"a"}))
        self.assertEqual(mentioned([]), frozenset())
        with self.assertRaises(AdmissionError):
            replay(history, genesis(READING_U))

    def test_mark_profile_is_the_side_and_nothing_else(self) -> None:
        for rd in READINGS:
            r = Regime(rd, ("a", "b"), (0, 1))
            self.assertEqual(mark_profile(r, 0), frozenset({OnSide(0, 0)}))
            self.assertEqual(mark_profile(r, 1), frozenset({OnSide(1, 1)}))
            with self.assertRaises(ValueError):
                mark_profile(r, 2)
            with self.assertRaises(ValueError):
                mark_profile(r, -1)

    def test_new_observations_is_the_extension_difference(self) -> None:
        for rd in READINGS:
            g = genesis(rd)
            self.assertEqual(new_observations(g, step(g, Supply("a"))), frozenset())
            admitted = step(g, AdmitMark("a", 1))
            self.assertEqual(new_observations(g, admitted), frozenset({OnSide(0, 1)}))
            self.assertEqual(new_observations(admitted, g), frozenset())

    def test_permitted_images_count_the_permitted_renamings(self) -> None:
        for n in range(4):
            marks = tuple(f"m{i}" for i in range(n))
            placement = tuple(i % 2 for i in range(n))
            fact = 1
            for k in range(2, n + 1):
                fact *= k
            self.assertEqual(len(permitted_images(Regime(READING_U, marks, placement))), 2 * fact)
            self.assertEqual(len(permitted_images(Regime(READING_O, marks, placement))), fact)
        images = permitted_images(Regime(READING_U, ("a",), (0,)))
        self.assertIn((True, (0,), Regime(READING_U, ("a",), (1,))), images)

    def test_isomorphism_witness_and_relation(self) -> None:
        left_u = Regime(READING_U, ("a",), (0,))
        right_u = Regime(READING_U, ("z",), (1,))
        self.assertEqual(isomorphism_witness(left_u, right_u), (True, (0,)))
        self.assertTrue(is_isomorphic(left_u, right_u))
        self.assertNotEqual(left_u, right_u)
        left_o = Regime(READING_O, ("a",), (0,))
        right_o = Regime(READING_O, ("a",), (1,))
        self.assertIsNone(isomorphism_witness(left_o, right_o))
        self.assertFalse(is_isomorphic(left_o, right_o))
        self.assertFalse(is_isomorphic(left_u, left_o))
        self.assertEqual(
            isomorphism_witness(
                Regime(READING_O, ("a", "b"), (0, 1)), Regime(READING_O, ("a", "b"), (1, 0))
            ),
            (False, (1, 0)),
        )

    def test_isomorphism_agrees_with_canonical_keys_to_three_marks(self) -> None:
        for rd in READINGS:
            regimes: list[Regime] = []
            for n in range(4):
                marks = tuple(f"m{i}" for i in range(n))
                regimes.extend(Regime(rd, marks, p) for p in product((0, 1), repeat=n))
            for a in regimes:
                for b in regimes:
                    self.assertEqual(
                        is_isomorphic(a, b), canonical(a) == canonical(b), (a, b)
                    )


class Challenge2KernelTests(unittest.TestCase):
    def test_occurrence_admission_admits_a_fresh_mark_whatever_the_label(self) -> None:
        for rd in READINGS:
            g = genesis(rd)
            history: list[Event] = [
                Supply("a"),
                AdmitOccurrence("a", 0),
                Supply("a"),
                AdmitOccurrence("a", 1),
            ]
            r = replay(history, g)
            self.assertEqual(r.marks, ("a", "a"))
            self.assertEqual(r.placement, (0, 1))
            self.assertTrue(certify(history, g, r))

    def test_occurrence_admission_refuses_an_unsupplied_token_by_name(self) -> None:
        g = genesis(READING_U)
        with self.assertRaisesRegex(AdmissionError, "was not supplied before admission"):
            replay([AdmitOccurrence("a", 0)], g)
        self.assertFalse(certify([AdmitOccurrence("a", 0)], g, Regime(READING_U, ("a",), (0,))))

    def test_occurrence_admission_refuses_a_bad_side(self) -> None:
        with self.assertRaisesRegex(AdmissionError, "side must be 0 or 1"):
            step(genesis(READING_U), AdmitOccurrence("a", 2))

    def test_token_keyed_admission_refuses_a_repeated_label_by_name(self) -> None:
        # The Challenge 1 event is keyed by the label; on a regime that carries
        # the label twice it cannot say which mark it names, and refuses rather
        # than taking the earliest.
        r = Regime(READING_O, ("a", "a"), (0, 1))
        with self.assertRaisesRegex(AdmissionError, "names more than one admitted mark"):
            step(r, AdmitMark("a", 0))
        self.assertEqual(step(r, AdmitMark("b", 0)).marks, ("a", "a", "b"))

    def test_the_two_identity_policies_disagree_on_the_callers_history(self) -> None:
        # The same caller history under the two admission events: the
        # token-keyed one is refused because the second whole names the first
        # mark; the occurrence-keyed one admits two marks.
        for rd in READINGS:
            g = genesis(rd)
            shared: list[Event] = [
                Supply("a"), AdmitMark("a", 0), Supply("a"), AdmitMark("a", 1)
            ]
            with self.assertRaisesRegex(AdmissionError, "would move it and is refused"):
                replay(shared, g)
            distinct: list[Event] = [
                Supply("a"), AdmitOccurrence("a", 0), Supply("a"), AdmitOccurrence("a", 1)
            ]
            self.assertEqual(replay(distinct, g).n_marks(), 2)

    def test_automorphisms_are_the_self_carrying_permitted_renamings(self) -> None:
        u = Regime(READING_U, ("a", "a"), (0, 1))
        o = Regime(READING_O, ("a", "a"), (0, 1))
        self.assertEqual(sorted(automorphisms(u)), [(False, (0, 1)), (True, (1, 0))])
        self.assertEqual(automorphisms(o), [(False, (0, 1))])
        # every automorphism is a permitted renaming that serializes back
        for r in (u, o):
            for reflected, pi in automorphisms(r):
                self.assertIn(
                    (reflected, pi),
                    [(refl, perm) for refl, perm, _img in permitted_images(r)],
                )
        self.assertEqual(automorphisms(genesis(READING_U)), [(False, ()), (True, ())])
        self.assertEqual(automorphisms(genesis(READING_O)), [(False, ())])

    def test_marks_are_separable_under_O_and_exchanged_under_U(self) -> None:
        u = Regime(READING_U, ("a", "a"), (0, 1))
        o = Regime(READING_O, ("a", "a"), (0, 1))
        self.assertEqual(mark_automorphism_to(u, 0, 1), (True, (1, 0)))
        self.assertFalse(marks_internally_separable(u, 0, 1))
        self.assertIsNone(mark_automorphism_to(o, 0, 1))
        self.assertTrue(marks_internally_separable(o, 0, 1))
        # the identity carries every mark to itself under both readings
        for r in (u, o):
            self.assertEqual(mark_automorphism_to(r, 0, 0), (False, (0, 1)))
            self.assertFalse(marks_internally_separable(r, 0, 0))
        # two marks on the SAME side are exchanged under both readings
        same = Regime(READING_O, ("a", "a"), (1, 1))
        self.assertEqual(mark_automorphism_to(same, 0, 1), (False, (1, 0)))
        self.assertFalse(marks_internally_separable(same, 0, 1))
        for bad in (-1, 2):
            with self.assertRaises(ValueError):
                mark_automorphism_to(u, bad, 0)
            with self.assertRaises(ValueError):
                mark_automorphism_to(u, 0, bad)

    def test_side_exchanging_automorphism_only_under_U(self) -> None:
        u = Regime(READING_U, ("a", "a"), (0, 1))
        o = Regime(READING_O, ("a", "a"), (0, 1))
        self.assertEqual(side_exchanging_automorphism(u), (True, (1, 0)))
        self.assertIsNone(side_exchanging_automorphism(o))
        # one mark: the reflection moves it, so no automorphism exchanges sides
        self.assertIsNone(side_exchanging_automorphism(Regime(READING_U, ("a",), (0,))))
        self.assertEqual(side_exchanging_automorphism(genesis(READING_U)), (True, ()))
        self.assertIsNone(side_exchanging_automorphism(genesis(READING_O)))

    def test_mark_side_and_different_sides(self) -> None:
        r = Regime(READING_U, ("a", "a"), (0, 1))
        self.assertEqual((mark_side(r, 0), mark_side(r, 1)), (0, 1))
        with self.assertRaises(ValueError):
            mark_side(r, 2)
        self.assertTrue(marks_on_different_sides(r))
        self.assertTrue(marks_on_different_sides(genesis(READING_U)))
        self.assertTrue(marks_on_different_sides(Regime(READING_O, ("a",), (0,))))
        self.assertFalse(marks_on_different_sides(Regime(READING_O, ("a", "b"), (1, 1))))
        self.assertFalse(
            marks_on_different_sides(Regime(READING_O, ("a", "b", "c"), (0, 1, 0)))
        )

    def test_different_sides_is_invariant_under_every_permitted_renaming(self) -> None:
        # The falsifier of C2-7: a permitted renaming after which two marks
        # share a side.  Checked over every regime of at most three marks
        # under both readings, and over every permitted image of each.
        checked = 0
        for rd in READINGS:
            for n in range(4):
                marks = tuple(f"m{i}" for i in range(n))
                for placement in product((0, 1), repeat=n):
                    r = Regime(rd, marks, placement)
                    want = marks_on_different_sides(r)
                    for _reflected, _pi, image in permitted_images(r):
                        self.assertEqual(marks_on_different_sides(image), want, r)
                        checked += 1
        # 177 images: for each of the 2^n placements, 2*n! under U and n!
        # under O, summed over n = 0 to 3.
        self.assertEqual(checked, 177)


class Challenge3KernelTests(unittest.TestCase):
    """The flagged enumerations, and that each reduces to the Challenge 2
    function at the flags the reading declares."""

    def test_flagged_images_reduce_to_the_readings_own_enumeration(self) -> None:
        # The instance claim: at the flags definitions 13 and 16 declare, the
        # flagged enumeration IS the one Challenges 0 to 2 used.  Checked over
        # every regime of at most three marks under both readings.
        checked = 0
        for rd in READINGS:
            reflection = rd == READING_U
            for n in range(4):
                marks = tuple(f"m{i}" for i in range(n))
                for placement in product((0, 1), repeat=n):
                    r = Regime(rd, marks, placement)
                    self.assertEqual(
                        permitted_images_under(r, reflection, True), permitted_images(r), r
                    )
                    self.assertEqual(
                        automorphisms_under(r, reflection, True, False), automorphisms(r), r
                    )
                    self.assertEqual(
                        canonical_under(r, reflection, True, False), canonical(r), r
                    )
                    checked += 1
        self.assertEqual(checked, 30)

    def test_flagged_separation_reduces_to_the_challenge_2_notion(self) -> None:
        for rd in READINGS:
            reflection = rd == READING_U
            for placement in ((0, 1), (1, 0), (0, 0), (1, 1)):
                r = Regime(rd, ("a", "a"), placement)
                self.assertEqual(
                    marks_separable_under(r, 0, 1, reflection, True, False),
                    marks_internally_separable(r, 0, 1),
                    r,
                )
                self.assertEqual(
                    mark_automorphism_to_under(r, 0, 1, reflection, True, False),
                    mark_automorphism_to(r, 0, 1),
                    r,
                )
                self.assertEqual(
                    side_exchanging_automorphism_under(r, reflection, True, False),
                    side_exchanging_automorphism(r),
                    r,
                )
                self.assertEqual(
                    is_isomorphic_under(r, reflect(r), reflection, True, False),
                    is_isomorphic(r, reflect(r)),
                    r,
                )

    def test_withdrawing_a_generator_shrinks_the_enumeration(self) -> None:
        r = Regime(READING_U, ("a", "a"), (0, 1))
        self.assertEqual(len(permitted_images_under(r, True, True)), 4)
        self.assertEqual(len(permitted_images_under(r, False, True)), 2)
        self.assertEqual(len(permitted_images_under(r, True, False)), 2)
        self.assertEqual(len(permitted_images_under(r, False, False)), 1)
        # withdrawing either generator separates the two marks; withdrawing
        # neither does not
        self.assertFalse(marks_separable_under(r, 0, 1, True, True, False))
        self.assertTrue(marks_separable_under(r, 0, 1, False, True, False))
        self.assertTrue(marks_separable_under(r, 0, 1, True, False, False))

    def test_keeping_the_labels_does_not_separate_a_repeated_label(self) -> None:
        # The negative direction of the label coordinate: with the tokens
        # kept, two marks carrying the SAME label are still exchanged, so
        # withdrawing the forgetting of definition 14 separates nothing here.
        same = Regime(READING_U, ("a", "a"), (0, 1))
        self.assertFalse(marks_separable_under(same, 0, 1, True, True, True))
        # with different labels it does separate, which is what makes the
        # coordinate a real one rather than a dead flag
        differing = Regime(READING_U, ("a", "b"), (0, 1))
        self.assertTrue(marks_separable_under(differing, 0, 1, True, True, True))
        self.assertFalse(marks_separable_under(differing, 0, 1, True, True, False))

    def test_serialize_keeping_labels_keeps_them(self) -> None:
        r = Regime(READING_U, ("a", "b"), (0, 1))
        self.assertEqual(serialize(r), (READING_U, (0, 1)))
        self.assertEqual(serialize_keeping_labels(r), (READING_U, ("a", "b"), (0, 1)))
        self.assertEqual(
            canonical_under(r, False, False, True), (READING_U, ("a", "b"), (0, 1))
        )

    def test_isomorphic_under_refuses_across_readings(self) -> None:
        u = Regime(READING_U, ("a",), (0,))
        o = Regime(READING_O, ("a",), (0,))
        self.assertFalse(is_isomorphic_under(u, o, True, True, False))

    def test_the_orbit_is_the_separation_test(self) -> None:
        # The second reading of the Challenge 3 requirement: the pair of the
        # second mark lies outside the first mark's orbit exactly when no
        # permitted automorphism carries one to the other.
        for flags in ((True, True), (False, True), (True, False), (False, False)):
            for placement in ((0, 1), (0, 0)):
                r = Regime(READING_U, ("a", "a"), placement)
                orbit = mark_orbit_under(r, 0, *flags, False)
                outside = (serialize(r), 1) not in orbit
                self.assertEqual(outside, marks_separable_under(r, 0, 1, *flags, False), r)
        with self.assertRaisesRegex(ValueError, "mark 2 is not admitted"):
            mark_orbit_under(Regime(READING_U, ("a", "a"), (0, 1)), 2, True, True, False)


if __name__ == "__main__":
    unittest.main()
