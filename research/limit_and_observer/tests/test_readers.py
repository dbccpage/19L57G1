"""The reader axis, and the lemma that lets the quotient key by behaviour.

The sharpest structural fact this tree derives: the sixteen readings collapse
to exactly **four** induced-separation behaviours, and the sealed observation
relation is one of them.
"""

from __future__ import annotations

import itertools
import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

from code.census import population, reading_axis_census  # noqa: E402
from code.enumerate_space import DEFAULT_BOUNDS  # noqa: E402
from code.grammar import (  # noqa: E402
    contexts,
    coverage_bit,
    sealed_relation,
)
from code.readers import (  # noqa: E402
    ADMISSION_ONLY_READING,
    ALL_READINGS,
    BEHAVIOUR_NAMES,
    BLIND,
    COVERED,
    EITHER,
    Reader,
    SEALED_READING,
    UNCOVERED,
    all_reading_classes,
    behaviour,
    complement,
    induced_blocks,
    induced_relation,
    non_constant_reading_classes,
    reading_class,
    reads_at,
    sealed_as_reader,
    state_lawful,
    lawful_aggregations,
)
from code.regime import genesis  # noqa: E402

POP = population(3, DEFAULT_BOUNDS)


def _reps() -> tuple[object, ...]:
    seen: dict[tuple[bool, bool], object] = {}
    for b in all_reading_classes():
        seen.setdefault(behaviour(b), b)
    return tuple(seen[k] for k in sorted(seen))


class TheReadingAxisIsCompleteAndSmall(unittest.TestCase):
    def test_sixteen_readings(self) -> None:
        self.assertEqual(len(ALL_READINGS), 16)

    def test_eight_complement_classes_seven_non_constant(self) -> None:
        self.assertEqual(len(all_reading_classes()), 8)
        self.assertEqual(len(non_constant_reading_classes()), 7)

    def test_a_reading_and_its_complement_are_one_class(self) -> None:
        for b in ALL_READINGS:
            self.assertEqual(reading_class(b), reading_class(complement(b)))

    def test_exactly_four_induced_separation_behaviours(self) -> None:
        self.assertEqual(
            len({behaviour(b) for b in ALL_READINGS}), 4
        )
        self.assertEqual(
            sorted(BEHAVIOUR_NAMES.values()),
            ["blind", "covered", "either", "uncovered"],
        )

    def test_the_coverage_bit_does_not_depend_on_the_datum(self) -> None:
        """Why the axis collapses: at a fixed context the coverage bit is
        constant across data, so a reading either varies with the admission
        bit there or is constant there."""
        for r in POP:
            for c in contexts(r):
                self.assertIsInstance(coverage_bit(r, c), bool)


class TheBehaviourLemma(unittest.TestCase):
    """Two readings sharing a behaviour induce the same relation everywhere.

    This is what makes keying the quotient by behaviour elimination *by
    proof* rather than a convenience."""

    def test_same_behaviour_gives_the_same_relation_at_every_state(
        self,
    ) -> None:
        checked = 0
        for r in POP:
            ctx = contexts(r)
            if not ctx:
                continue
            for a in lawful_aggregations(3):
                for w in range(0, min(2, len(ctx)) + 1):
                    for sel in itertools.combinations(ctx, w):
                        by_beh: dict[tuple[bool, bool], set[object]] = {}
                        for b in ALL_READINGS:
                            rel = induced_relation(r, Reader(sel, b, a))
                            by_beh.setdefault(behaviour(b), set()).add(rel)
                        for beh, rels in by_beh.items():
                            self.assertEqual(
                                len(rels), 1,
                                f"behaviour {BEHAVIOUR_NAMES[beh]} induced "
                                f"{len(rels)} different relations",
                            )
                            checked += 1
        self.assertGreater(checked, 0)


class TheSealedObserverIsAPointOfTheReaderSpace(unittest.TestCase):
    def test_the_sealed_reading_has_the_uncovered_behaviour(self) -> None:
        self.assertEqual(behaviour(SEALED_READING), UNCOVERED)
        self.assertEqual(behaviour(ADMISSION_ONLY_READING), EITHER)

    def test_sealed_relation_equals_the_full_uncovered_reader(self) -> None:
        """Checked at every state of the population, not merely at the
        bases."""
        for r in POP:
            self.assertEqual(
                induced_relation(r, sealed_as_reader(r)),
                sealed_relation(r),
            )

    def test_reads_at_agrees_with_the_behaviour_pair(self) -> None:
        for b in ALL_READINGS:
            self.assertEqual(reads_at(b, False), behaviour(b)[0])
            self.assertEqual(reads_at(b, True), behaviour(b)[1])

    def test_the_sealed_observer_is_blind_at_a_covered_context(self) -> None:
        """The conflation, stated as a computation: where the uniform rule
        covers the form, the sealed relation reads true for every datum and
        so separates nothing there."""
        self.assertFalse(reads_at(SEALED_READING, True))
        self.assertTrue(reads_at(SEALED_READING, False))
        self.assertTrue(reads_at(ADMISSION_ONLY_READING, True))


class LawfulnessClasses(unittest.TestCase):
    def test_a_lawful_reader_is_state_lawful_everywhere(self) -> None:
        for r in POP:
            ctx = contexts(r)
            for a in lawful_aggregations(3):
                for w in range(0, min(2, len(ctx)) + 1):
                    for sel in itertools.combinations(ctx, w):
                        for b in _reps():
                            self.assertTrue(
                                state_lawful(r, Reader(sel, b, a))  # type: ignore[arg-type]
                            )

    def test_blocks_are_between_one_and_the_carrier(self) -> None:
        for r in POP:
            if r.n_data() == 0:
                continue
            ctx = contexts(r)
            for a in lawful_aggregations(3):
                for w in range(0, min(2, len(ctx)) + 1):
                    for sel in itertools.combinations(ctx, w):
                        for b in _reps():
                            k = induced_blocks(r, Reader(sel, b, a))  # type: ignore[arg-type]
                            self.assertGreaterEqual(k, 1)
                            self.assertLessEqual(k, r.n_data())


class TheAxisCensusIsWhatIsReported(unittest.TestCase):
    def test_the_monotone_split_is_measured(self) -> None:
        """2 of the 4 lawful aggregations at width 3 are block-count
        monotone.  The refinement proof reaches those two; the other two are
        covered by computation only."""
        from code.readers import monotone_aggregations

        self.assertEqual(len(monotone_aggregations(3)), 2)
        self.assertTrue(
            set(monotone_aggregations(3)) <= set(lawful_aggregations(3))
        )
        self.assertEqual(
            {w: len(monotone_aggregations(w)) for w in (1, 2, 3, 4)},
            {1: 2, 2: 2, 3: 2, 4: 2},
        )

    def test_census_matches_the_direct_computation(self) -> None:
        c = reading_axis_census(3)
        self.assertEqual(c["monotone"], 2)
        self.assertEqual(c["complement_classes"], 8)
        self.assertEqual(c["non_constant_complement_classes"], 7)
        self.assertEqual(c["induced_separation_behaviours"], 4)
        self.assertEqual(c["sealed_behaviour"], "uncovered")
        self.assertEqual(c["admission_only_behaviour"], "either")
        self.assertEqual(c["lawful"], 4)
        self.assertEqual(c["unlawful_refused"], 4)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
