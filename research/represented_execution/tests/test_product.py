"""Two loci: the packing, the independence square, the coupling that breaks
it, and a scheduled two-locus run whose record the theorems name.

The sweeps are exhaustive over the declared small tables rather than
sampled, so a failure names a table and a datum.  The tapes asserted at the
end are hand-copied from the statements of ``lean/Schedule.lean``: they are a
cross-check between two independent implementations — Lean operations are
functions, these are value tables — and not a second reading of one.
"""

from __future__ import annotations

from itertools import product as tuples
from pathlib import Path
import sys
from typing import Callable
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "setting_translation"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import control as ct  # noqa: E402
import product as pr  # noqa: E402
import translation as tr  # noqa: E402
from execution import ExecutionError  # noqa: E402

# Every value table on two and on three points.
TABLES2 = tuple(tuples(range(2), repeat=2))
TABLES3 = tuple(tuples(range(3), repeat=3))


def setting(n: int, ops: tuple[tuple[int, ...], ...]) -> tr.FiniteSetting:
    return tr.FiniteSetting(n, tr.NONE, tr.NONE, tr.NONE, 0, n - 1, ops)


class Packing(unittest.TestCase):
    def test_the_pair_is_recovered_from_the_datum_that_packs_it(self) -> None:
        for m in (1, 2, 3, 4):
            for a, b in tuples(range(4), range(m)):
                x = pr.pack(m, a, b)
                self.assertEqual((pr.fst_of(m, x), pr.snd_of(m, x)), (a, b), (m, a, b))

    def test_a_packed_datum_of_the_product_lies_in_its_carrier(self) -> None:
        for n, m in tuples((1, 2, 3), (1, 2, 3)):
            for a, b in tuples(range(n), range(m)):
                self.assertLess(pr.pack(m, a, b), n * m)

    def test_an_empty_second_locus_is_refused_by_name(self) -> None:
        calls: tuple[Callable[[], int], ...] = (
            lambda: pr.pack(0, 1, 0), lambda: pr.fst_of(0, 1), lambda: pr.snd_of(0, 1))
        for call in calls:
            with self.assertRaises(ExecutionError):
                call()

    def test_a_negative_datum_is_refused_rather_than_wrapped(self) -> None:
        # Python's floor division would answer -1 // 2 == -1 rather than refuse.
        calls: tuple[Callable[[], int], ...] = (lambda: pr.fst_of(2, -1), lambda: pr.snd_of(2, -1))
        for call in calls:
            with self.assertRaises(ExecutionError):
                call()


class Locality(unittest.TestCase):
    def test_a_move_at_one_locus_leaves_the_other_where_it_was(self) -> None:
        for f, g in tuples(TABLES2, TABLES3):
            left, right = pr.left_op(3, 2, f), pr.right_op(3, 2, g)
            for x in range(6):
                self.assertEqual(pr.snd_of(3, left[x]), pr.snd_of(3, x), (f, x))
                self.assertEqual(pr.fst_of(3, right[x]), pr.fst_of(3, x), (g, x))

    def test_two_moves_at_different_loci_commute(self) -> None:
        for f, g in tuples(TABLES2, TABLES3):
            left, right = pr.left_op(3, 2, f), pr.right_op(3, 2, g)
            for x in range(6):
                self.assertEqual(left[right[x]], right[left[x]], (f, g, x))

    def test_a_move_that_reads_the_other_locus_does_not_commute(self) -> None:
        # The exchange reads both coordinates; it is at neither locus.
        swap = pr.swap_op(2, 2)
        right = pr.right_op(2, 2, (1, 0))
        self.assertTrue(any(swap[right[x]] != right[swap[x]] for x in range(4)))

    def test_the_exchange_moves_both_loci_in_one_step(self) -> None:
        swap = pr.swap_op(2, 2)
        self.assertNotEqual(pr.fst_of(2, swap[1]), pr.fst_of(2, 1))
        self.assertNotEqual(pr.snd_of(2, swap[1]), pr.snd_of(2, 1))

    def test_every_operation_of_a_product_setting_moves_at_most_one_locus(self) -> None:
        for f, g in tuples(TABLES2, TABLES2):
            P = pr.prod_setting(setting(2, (f,)), setting(2, (g,)))
            for table in P.ops:
                for x in range(P.n):
                    self.assertTrue(
                        pr.fst_of(2, table[x]) == pr.fst_of(2, x)
                        or pr.snd_of(2, table[x]) == pr.snd_of(2, x), (f, g, x))


class ScheduleIsData(unittest.TestCase):
    def test_a_schedule_leaves_the_runner_a_singleton_at_every_datum(self) -> None:
        for f, g in tuples(TABLES2, TABLES2):
            P = pr.prod_setting(setting(2, (f,)), setting(2, (g,)))
            for choices in tuples(range(len(P.ops)), repeat=P.n):
                C = pr.scheduled(P, lambda x, c=choices: c[x])  # type: ignore[misc]
                graph, count = ct.program(C), ct.nops(C)
                for x in range(P.n):
                    self.assertEqual(ct.enabled_at(graph, count, x), (choices[x],), (choices, x))

    def test_a_scheduled_run_never_branches(self) -> None:
        for f, g in tuples(TABLES2, TABLES2):
            P = pr.prod_setting(setting(2, (f,)), setting(2, (g,)))
            for choices in tuples(range(len(P.ops)), repeat=P.n):
                C = pr.scheduled(P, lambda x, c=choices: c[x])  # type: ignore[misc]
                for start in range(P.n):
                    terminal, state = ct.trace(C, start, 6)
                    self.assertIsNot(terminal, ct.Terminal.BRANCH, (choices, start))
                    self.assertTrue(pr.moves_one_locus(2, state.tape), (choices, start))

    def test_a_schedule_naming_an_operation_outside_the_setting_is_refused(self) -> None:
        P = pr.prod_setting(setting(2, ((1, 0),)), setting(2, ((1, 0),)))
        with self.assertRaises(ExecutionError):
            pr.scheduled(P, lambda _: len(P.ops))

    def test_the_destuttered_projection_is_that_locus_own_run(self) -> None:
        # Every schedule over the two-point loci, each start, read at each locus.
        flip = setting(2, ((1, 0),))
        P = pr.prod_setting(flip, flip)
        for choices in tuples(range(2), repeat=4):
            C = pr.scheduled(P, lambda x, c=choices: c[x])  # type: ignore[misc]
            for start in range(4):
                tape = ct.trace(C, start, 6)[1].tape
                for which in (0, 1):
                    reading = pr.destutter(pr.locus(2, which, tape))
                    # The locus's own run is the flip iterated from where it began.
                    here = pr.locus(2, which, (start,))[0]
                    own = tuple((here + i) % 2 for i in range(len(reading)))
                    self.assertEqual(reading, own, (choices, start, which))


class TheRecordedRun(unittest.TestCase):
    """The tapes hand-copied from `lean/Schedule.lean`."""

    def setUp(self) -> None:
        flip = setting(2, ((1, 0),))
        self.pair = pr.two_locus(flip, flip, lambda x: 0 if pr.fst_of(2, x) == pr.snd_of(2, x) else 1)
        self.mirror = pr.two_locus(flip, flip, lambda x: 1 if pr.fst_of(2, x) == pr.snd_of(2, x) else 0)
        self.solo = pr.scheduled(flip, lambda _: 0)

    def test_the_two_locus_run_is_the_tape_the_theorem_names(self) -> None:
        terminal, state = ct.trace(self.pair, 0, 4)
        self.assertEqual(list(state.tape), [0, 2, 3, 1, 0])          # Schedule.pair_run
        self.assertIs(terminal, ct.Terminal.EXHAUSTED)               # Schedule.pair_terminal

    def test_the_mirror_run_is_the_tape_the_theorem_names(self) -> None:
        self.assertEqual(list(ct.trace(self.mirror, 0, 4)[1].tape), [0, 1, 3, 2, 0])

    def test_the_two_orders_reach_the_same_datum_by_different_tapes(self) -> None:
        forward, mirror = ct.trace(self.pair, 0, 2)[1], ct.trace(self.mirror, 0, 2)[1]
        self.assertEqual(forward.active, mirror.active)              # square_on_the_outcome
        self.assertNotEqual(forward.tape, mirror.tape)               # square_fails_on_the_observation
        self.assertEqual(list(forward.tape), [0, 2, 3])
        self.assertEqual(list(mirror.tape), [0, 1, 3])

    def test_each_locus_reads_its_own_run_off_the_two_locus_tape(self) -> None:
        tape = ct.trace(self.pair, 0, 4)[1].tape
        own = list(ct.trace(self.solo, 0, 2)[1].tape)
        self.assertEqual(own, [0, 1, 0])                             # Schedule.solo_run
        self.assertEqual(list(pr.locus(2, 0, tape)), [0, 1, 1, 0, 0])
        self.assertEqual(list(pr.locus(2, 1, tape)), [0, 0, 1, 1, 0])
        for which in (0, 1):
            self.assertEqual(list(pr.destutter(pr.locus(2, which, tape))), own)

    def test_a_locus_index_outside_the_two_is_refused_by_name(self) -> None:
        with self.assertRaises(ExecutionError):
            pr.locus(2, 2, (0, 1))


if __name__ == "__main__":
    unittest.main()
