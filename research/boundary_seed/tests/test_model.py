"""Tests of the boundary kernel, Challenge 0 scope."""

from __future__ import annotations

import pathlib
import sys
import unittest

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE / "code"))

from boundary.model import (  # noqa: E402
    READING_O,
    READING_U,
    READINGS,
    SIDE_NAMES,
    AdmissionError,
    AdmitMark,
    Event,
    Regime,
    Supply,
    canonical,
    certify,
    contents,
    genesis,
    is_automorphism_reflection,
    observations,
    reflect,
    rename_marks,
    replay,
    serialize,
    side_profile,
    sides_collapsed,
    step,
)


class GenesisTests(unittest.TestCase):
    def test_two_readings_only(self) -> None:
        self.assertEqual(READINGS, ("U", "O"))
        for rd in READINGS:
            g = genesis(rd)
            self.assertEqual(g.n_marks(), 0)
            self.assertEqual(g.placement, ())

    def test_unknown_reading_refused(self) -> None:
        with self.assertRaises(AdmissionError):
            genesis("V")


class EventTests(unittest.TestCase):
    def test_supply_is_not_admission(self) -> None:
        for rd in READINGS:
            g = genesis(rd)
            self.assertEqual(step(g, Supply("a")), g)
            self.assertEqual(replay([Supply("a"), Supply("b"), Supply("a")], g), g)

    def test_admission_places_one_mark(self) -> None:
        r = step(genesis(READING_U), AdmitMark("a", 0))
        self.assertEqual(r.marks, ("a",))
        self.assertEqual(r.placement, (0,))
        r2 = step(r, AdmitMark("b", 1))
        self.assertEqual(r2.placement, (0, 1))

    def test_readmission_is_designation(self) -> None:
        r = step(genesis(READING_O), AdmitMark("a", 1))
        self.assertEqual(step(r, AdmitMark("a", 0)), r)

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


class ObservationTests(unittest.TestCase):
    def test_genesis_contents_empty_on_both_sides(self) -> None:
        for rd in READINGS:
            g = genesis(rd)
            self.assertEqual(contents(g, 0), frozenset())
            self.assertEqual(contents(g, 1), frozenset())
            self.assertEqual(observations(g), frozenset())

    def test_contents_refuses_a_third_side(self) -> None:
        with self.assertRaises(ValueError):
            contents(genesis(READING_U), 2)

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
            self.assertEqual(observations(r), frozenset({(0, 0)}))


class RenamingTests(unittest.TestCase):
    def test_reflect_is_an_involution_and_swaps_sides(self) -> None:
        r = Regime(READING_U, ("a", "b", "c"), (0, 1, 1))
        self.assertEqual(reflect(r).placement, (1, 0, 0))
        self.assertEqual(reflect(reflect(r)), r)

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
        self.assertTrue(is_automorphism_reflection(genesis(READING_O)))
        self.assertTrue(is_automorphism_reflection(Regime(READING_U, ("a",), (0,))))
        self.assertFalse(is_automorphism_reflection(Regime(READING_O, ("a",), (0,))))


if __name__ == "__main__":
    unittest.main()
