"""The pricing routine and the tie-retention harness.

The invariant that matters: the response classes must **partition** the raw
minima.  Each invariant below is checked by constructing a value that
violates it and requiring the refusal.
"""

from __future__ import annotations

import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

from code.calibration import CALIBRATION_BOUNDS, separation_demand  # noqa: E402
from code.demands import DEMANDS, DEMANDS_BY_NAME  # noqa: E402
from code.enumerate_space import DEFAULT_BOUNDS, Bounds  # noqa: E402
from code.items import NewForm, NewInst, NewRuleAll  # noqa: E402
from code.price import (  # noqa: E402
    GradeRefused,
    Minimum,
    ResponseClass,
    price,
    price_many,
    satisfies_at,
)
from code.regime import genesis  # noqa: E402

TIGHT = Bounds(
    max_items=5, max_sealed_items=3, max_reader_items=2,
    max_arity=1, w_max=3, max_readers=2,
)


def _class(members):  # type: ignore[no-untyped-def]
    return ResponseClass(
        key=("k",),
        representative=min(members, key=str),
        members=tuple(sorted(members, key=str)),
        capability_vector={},
    )


def _minimum(raw, classes, **kw):  # type: ignore[no-untyped-def]
    base = dict(
        demand="D", evidence_arity="single state", base_reading="L",
        measure="mu1", cost=(1, -1), raw_minima=raw, classes=classes,
        cost_below_minimum_all_fail=True, complete_within=DEFAULT_BOUNDS,
        designated=None,
    )
    base.update(kw)
    return Minimum(**base)  # type: ignore[arg-type]


class HarnessInvariants(unittest.TestCase):
    def test_a_class_is_never_empty(self) -> None:
        with self.assertRaises(GradeRefused):
            ResponseClass(("k",), (NewForm(1),), (), {})

    def test_a_class_holds_no_duplicate(self) -> None:
        with self.assertRaises(GradeRefused):
            ResponseClass(
                ("k",), (NewForm(1),), (NewForm(1), NewForm(1)), {}
            )

    def test_the_representative_is_a_member(self) -> None:
        with self.assertRaises(GradeRefused):
            ResponseClass(("k",), (NewForm(2),), (NewForm(1),), {})

    def test_members_are_sorted(self) -> None:
        with self.assertRaises(GradeRefused):
            ResponseClass(
                ("k",), (NewForm(1),),
                ((NewRuleAll(0),), (NewForm(1),)), {},  # type: ignore[arg-type]
            )

    def test_raw_minima_hold_no_duplicate(self) -> None:
        d = (NewForm(1),)
        with self.assertRaises(GradeRefused):
            _minimum((d, d), (_class([d]),))

    def test_classes_must_partition_the_raw_minima(self) -> None:
        """The load-bearing invariant."""
        a, b = (NewForm(1),), (NewForm(2),)
        with self.assertRaises(GradeRefused):
            _minimum(tuple(sorted((a, b), key=str)), (_class([a]),))

    def test_classes_have_distinct_keys(self) -> None:
        a = (NewForm(1),)
        c = _class([a])
        with self.assertRaises(GradeRefused):
            _minimum((a,), (c, c))

    def test_grades_are_assigned_from_the_shape(self) -> None:
        a, b = (NewForm(1),), (NewForm(2),)
        self.assertEqual(_minimum((), ()).grade, "Empty")
        self.assertEqual(_minimum((a,), (_class([a]),)).grade, "UniqueDelta")
        raw = tuple(sorted((a, b), key=str))
        self.assertEqual(
            _minimum(raw, (_class([a, b]),)).grade, "UniqueClass"
        )
        two = (
            ResponseClass(("k1",), a, (a,), {}),
            ResponseClass(("k2",), b, (b,), {}),
        )
        self.assertEqual(_minimum(raw, two).grade, "Tie")


class OneRoutineForEveryDemand(unittest.TestCase):
    def test_the_wrapper_agrees_with_the_shared_enumeration(self) -> None:
        """Enumerating once for many demands must give exactly what
        enumerating once per demand gives."""
        for reading in ("L", "F"):
            many = price_many(
                genesis(reading), reading,
                (DEMANDS_BY_NAME["OBS-1"], DEMANDS_BY_NAME["OBS-2"]),
                ("mu1", "mu2"), TIGHT,
            )
            for name in ("OBS-1", "OBS-2"):
                for measure in ("mu1", "mu2"):
                    one = price(
                        genesis(reading), reading,
                        DEMANDS_BY_NAME[name], measure, TIGHT,
                    )
                    got = many[(name, measure)]
                    self.assertEqual(one.cost, got.cost)
                    self.assertEqual(one.raw_minima, got.raw_minima)
                    self.assertEqual(
                        [c.key for c in one.classes],
                        [c.key for c in got.classes],
                    )

    def test_an_unknown_measure_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            price(
                genesis("L"), "L", DEMANDS_BY_NAME["OBS-1"], "mu9", TIGHT
            )

    def test_every_demand_is_total_and_decidable(self) -> None:
        """Every demand answers on every candidate without raising."""
        from code.demands import Situation
        from code.enumerate_space import iter_candidates
        import itertools

        for reading in ("L", "F"):
            base = genesis(reading)
            for total in (0, 1, 2, 3):
                for delta, state in itertools.islice(
                    iter_candidates(base, total, DEFAULT_BOUNDS), 150
                ):
                    sit = Situation(base, delta, state, (0, 1), 3)
                    for d in DEMANDS:
                        self.assertIsInstance(d.predicate(sit), bool)


class PurchaseIsRunNotInferred(unittest.TestCase):
    def test_satisfies_at_runs_the_predicate(self) -> None:
        base = genesis("L")
        delta = (NewForm(1), NewRuleAll(0), NewInst(0, (0,)))
        self.assertFalse(
            satisfies_at(base, delta, DEMANDS_BY_NAME["OBS-3"], DEFAULT_BOUNDS)
        )

    def test_an_ill_formed_delta_is_refused_not_counted(self) -> None:
        base = genesis("L")
        self.assertFalse(
            satisfies_at(
                base, (NewInst(0, (0,)),), DEMANDS_BY_NAME["OBS-1"],
                DEFAULT_BOUNDS,
            )
        )


class CalibrationIsPricedByTheSameRoutine(unittest.TestCase):
    def test_the_separation_demand_goes_through_price(self) -> None:
        d = separation_demand((0, 1))
        m = price(genesis("L"), "L", d, "mu1", CALIBRATION_BOUNDS,
                  prune=False)
        self.assertEqual(m.cost, (2, -1))
        self.assertEqual(len(m.raw_minima), 6)
        self.assertEqual(len(m.classes), 3)
        self.assertTrue(m.cost_below_minimum_all_fail)

    def test_the_imposed_pair_is_carried_by_the_demand(self) -> None:
        self.assertEqual(separation_demand((1, 2)).impose, (1, 2))
        self.assertIsNone(DEMANDS_BY_NAME["OBS-1"].impose)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
