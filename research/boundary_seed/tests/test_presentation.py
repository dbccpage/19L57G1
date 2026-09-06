"""Tests of the presentation layer: the bounded reader of a supplied whole
and the declared presentation-to-side conventions."""

from __future__ import annotations

import pathlib
import sys
import unittest

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE / "code"))

from boundary.model import AdmitMark, Supply  # noqa: E402
from boundary.presentation import (  # noqa: E402
    CONVENTIONS,
    DECLARED_CONVENTION,
    OTHER_CONVENTION,
    PRESENTED_SIDES,
    PresentationError,
    Whole,
    admission_event,
    admitted_side,
    read_whole,
    supply_event,
)


class ReaderTests(unittest.TestCase):
    def test_reads_the_initial_and_the_one_mark_wholes(self) -> None:
        self.assertEqual(read_whole("<|>"), Whole(None, None))
        self.assertEqual(read_whole("<a|>"), Whole("a", "left"))
        self.assertEqual(read_whole("<|a>"), Whole("a", "right"))

    def test_refuses_anything_beyond_the_declared_bound(self) -> None:
        for text in ("<ab|>", "<a|b>", "<<a|>|>", "a|", "<a>", "", "<A|>", "<a||>", "<a|> "):
            with self.subTest(text=text), self.assertRaises(PresentationError):
                read_whole(text)

    def test_more_than_one_mark_is_refused_by_name(self) -> None:
        with self.assertRaisesRegex(PresentationError, "more than one mark"):
            read_whole("<a|b>")
        with self.assertRaisesRegex(PresentationError, "one bar"):
            read_whole("<<a|>|>")

    def test_whole_invariants(self) -> None:
        with self.assertRaises(PresentationError):
            Whole("a", None)
        with self.assertRaises(PresentationError):
            Whole(None, "left")
        with self.assertRaises(PresentationError):
            Whole("a", "above")


class EventTests(unittest.TestCase):
    def test_supply_event_presents_the_token_only(self) -> None:
        self.assertEqual(supply_event(read_whole("<a|>")), Supply("a"))
        self.assertEqual(supply_event(read_whole("<|a>")), Supply("a"))
        with self.assertRaises(PresentationError):
            supply_event(read_whole("<|>"))

    def test_conventions_are_the_two_bijections(self) -> None:
        self.assertEqual(PRESENTED_SIDES, ("left", "right"))
        self.assertEqual(set(CONVENTIONS), {DECLARED_CONVENTION, OTHER_CONVENTION})
        for side in PRESENTED_SIDES:
            self.assertEqual(
                admitted_side(side, DECLARED_CONVENTION),
                1 - admitted_side(side, OTHER_CONVENTION),
            )
        self.assertEqual(admitted_side("left", DECLARED_CONVENTION), 0)
        self.assertEqual(admitted_side("right", DECLARED_CONVENTION), 1)

    def test_admitted_side_refuses_unknowns(self) -> None:
        with self.assertRaisesRegex(PresentationError, "unknown convention"):
            admitted_side("left", "left is near")
        with self.assertRaisesRegex(PresentationError, "unknown presented side"):
            admitted_side("above", DECLARED_CONVENTION)

    def test_admission_event_under_each_convention(self) -> None:
        whole = read_whole("<a|>")
        self.assertEqual(admission_event(whole, DECLARED_CONVENTION), AdmitMark("a", 0))
        self.assertEqual(admission_event(whole, OTHER_CONVENTION), AdmitMark("a", 1))
        mirror = read_whole("<|a>")
        self.assertEqual(admission_event(mirror, DECLARED_CONVENTION), AdmitMark("a", 1))
        with self.assertRaises(PresentationError):
            admission_event(read_whole("<|>"), DECLARED_CONVENTION)


if __name__ == "__main__":
    unittest.main()
