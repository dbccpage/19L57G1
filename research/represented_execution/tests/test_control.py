"""Control by data: the brief's items 3–5 on small controlled settings, the
kept-apart terminals, the family without a selector, the bookkeeping laws,
and the reference-step correspondence.  The expected operation values come
from the merged ``translation.run``, which the tests may consult."""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "setting_translation"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import control as ct  # noqa: E402
import execution as ex  # noqa: E402
import translation as tr  # noqa: E402

CYCLE = (1, 2, 0)      # op 0: 0 -> 1 -> 2 -> 0
ZERO = (0, 0, 0)       # op 1: everything -> 0
SUCC = (1, 2, 2)       # op 2: 0 -> 1 -> 2 -> 2
BASE = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 1, (CYCLE, ZERO, SUCC))

# Branching by data: at 0 the cycle fires, at 1 the zero map fires, at 2 nothing.
PING = ct.Controlled(BASE, frozenset({(0, 0), (1, 1)}))
# A program that halts by data: climb with SUCC until 2, where nothing is enabled.
CLIMB = ct.Controlled(BASE, frozenset({(0, 2), (1, 2)}))
# The cycle enabled everywhere: runs until the fuel is spent.
FOREVER = ct.Controlled(BASE, frozenset({(0, 0), (1, 0), (2, 0)}))
# Two operations enabled at 0: a genuine branch.
FORK = ct.Controlled(BASE, frozenset({(0, 0), (0, 1)}))


class Representation(unittest.TestCase):
    def test_the_controlled_regime_is_well_formed_and_binary(self) -> None:
        for C in (PING, CLIMB, FOREVER, FORK):
            r = ct.encode_c(C)
            self.assertEqual(r.forms, (2,) * (3 + 2 * ct.nops(C)))
            self.assertFalse(r.rules)
            self.assertFalse(r.reqs)
            self.assertTrue(ct.program(C) <= frozenset(r.insts))

    def test_the_program_carries_no_store(self) -> None:
        F = tr.FiniteSetting(3, tr.BOTH, tr.EDGE, tr.EDGE, 0, 1, (CYCLE,))
        C = ct.Controlled(F, frozenset({(0, 0)}))
        self.assertTrue(all(form >= 3 for form, _ in ct.program(C)))
        self.assertTrue(any(form < 3 for form, _ in ct.encode_c(C).insts))

    def test_enablement_is_read_faithfully(self) -> None:
        for C in (PING, CLIMB, FOREVER, FORK):
            g = ct.program(C)
            for x in range(C.F.n):
                for k in range(ct.nops(C)):
                    self.assertEqual(ct.enabled(g, ct.nops(C), x, k), (x, k) in C.ctrl, (x, k))

    def test_init_does_not_read_the_designated_pair(self) -> None:
        other = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 2, 0, (CYCLE, ZERO, SUCC))
        self.assertEqual(ct.init(ct.Controlled(other, PING.ctrl), 0, 5), ct.init(PING, 0, 5))

    def test_out_of_range_enablement_is_refused(self) -> None:
        with self.assertRaises(ex.ExecutionError):
            ct.Controlled(BASE, frozenset({(0, 3)}))
        with self.assertRaises(ex.ExecutionError):
            ct.Controlled(BASE, frozenset({(3, 0)}))


class ReferenceStep(unittest.TestCase):
    def test_successors_are_sound_and_complete(self) -> None:
        for C in (PING, CLIMB, FOREVER, FORK):
            for x in range(C.F.n):
                s = ct.init(C, x, 1)
                seen = {t.active for t in ct.successors(s)}
                expected = {tr.run(C.F, (k,), x) for k in range(ct.nops(C)) if (x, k) in C.ctrl}
                self.assertEqual(seen, expected, (C.ctrl, x))
                for t in ct.successors(s):
                    self.assertTrue(any(ct.cstep(C, x, k, t.active) for k in range(ct.nops(C))))

    def test_soundness_and_completeness_hold_at_every_state_a_run_reaches(self) -> None:
        """The Lean statements carry the program as a hypothesis rather than
        naming the initial state, so they speak at every step of a run."""
        for C in (PING, CLIMB, FOREVER):
            for x in range(C.F.n):
                s = ct.init(C, x, 6)
                for _ in range(6):
                    seen = {t.active for t in ct.successors(s)}
                    expected = {tr.run(C.F, (k,), s.active)
                                for k in range(ct.nops(C)) if (s.active, k) in C.ctrl}
                    self.assertEqual(seen, expected, (C.ctrl, s.active))
                    for t in ct.successors(s):
                        self.assertTrue(any(ct.cstep(C, s.active, k, t.active)
                                            for k in range(ct.nops(C))))
                    nxt = ct.step_det(s)
                    if not isinstance(nxt, ct.State):
                        break
                    s = nxt

    def test_an_edit_away_from_the_active_datum_leaves_the_step_unchanged(self) -> None:
        """The other half of the causal footprint: a firing reads the
        enablement and the edge at the active datum, so an instance elsewhere
        is not read.  The 'an edit at it does' half is the word machine's
        mutation tests."""
        s = ct.init(PING, 0, 3)
        elsewhere = ct.State(ex.replace_edge(s.graph, 3, 2, 2), s.nops, s.active, s.tape,
                             s.clock, s.fuel)
        self.assertNotEqual(elsewhere.graph, s.graph)
        here, there = ct.fire(s, 0), ct.fire(elsewhere, 0)
        assert isinstance(here, ct.State) and isinstance(there, ct.State)
        self.assertEqual((there.active, there.tape, there.clock, there.fuel),
                         (here.active, here.tape, here.clock, here.fuel))
        self.assertEqual({t.active for t in ct.successors(elsewhere)},
                         {t.active for t in ct.successors(s)})
        self.assertEqual(ct.run(elsewhere)[1].tape, ct.run(s)[1].tape)
        at_it = ct.State(ex.replace_edge(s.graph, 3, 0, 2), s.nops, s.active, s.tape, s.clock, s.fuel)
        self.assertNotEqual(ct.run(at_it)[1].tape, ct.run(s)[1].tape)

    def test_no_fuel_no_successor(self) -> None:
        self.assertEqual(ct.successors(ct.init(FOREVER, 0, 0)), ())


class Control(unittest.TestCase):
    def test_a_branch_driven_by_data(self) -> None:
        _, s = ct.trace(PING, 0, 4)
        self.assertEqual(s.tape, (0, 1, 0, 1, 0))
        _, s = ct.trace(PING, 1, 4)
        self.assertEqual(s.tape, (1, 0, 1, 0, 1))
        term, s = ct.trace(PING, 2, 4)
        self.assertEqual((term, s.tape), (ct.Terminal.HALT, (2,)))

    def test_iteration_length_is_set_by_the_data_not_the_interpreter(self) -> None:
        lengths = {x: ct.trace(CLIMB, x, 10)[1].clock for x in range(3)}
        self.assertEqual(lengths, {0: 2, 1: 1, 2: 0})
        for x in range(3):
            self.assertEqual(ct.trace(CLIMB, x, 10)[0], ct.Terminal.HALT)

    def test_different_programs_same_data_different_outputs(self) -> None:
        a = ct.trace(PING, 0, 3)[1].tape
        b = ct.trace(CLIMB, 0, 3)[1].tape
        c = ct.trace(FOREVER, 0, 3)[1].tape
        self.assertEqual(len({a, b, c}), 3)

    def test_arbitrarily_long_runs_until_the_fuel_is_spent(self) -> None:
        for fuel in range(8):
            term, s = ct.trace(FOREVER, 0, fuel)
            self.assertEqual(term, ct.Terminal.EXHAUSTED)
            self.assertEqual(s.clock, fuel)
            self.assertEqual(s.fuel, 0)
            self.assertEqual(len(s.tape), fuel + 1)
            self.assertEqual(s.tape, tuple(i % 3 for i in range(fuel + 1)))

    def test_the_runner_never_selects(self) -> None:
        term, s = ct.trace(FORK, 0, 5)
        self.assertEqual(term, ct.Terminal.BRANCH)
        self.assertEqual(s.clock, 0)
        family = {t.active for t in ct.successors(s)}
        self.assertEqual(family, {1, 0})

    def test_the_family_is_invariant_under_permuting_the_operations(self) -> None:
        swapped = ct.with_ops(FORK, (ZERO, CYCLE, SUCC), frozenset({(0, 1), (0, 0)}))
        before = {t.active for t in ct.successors(ct.init(FORK, 0, 5))}
        after = {t.active for t in ct.successors(ct.init(swapped, 0, 5))}
        self.assertEqual(before, after)


class Terminals(unittest.TestCase):
    def test_halt_exhausted_refuse_branch_are_distinct(self) -> None:
        self.assertEqual(ct.trace(CLIMB, 0, 10)[0], ct.Terminal.HALT)
        self.assertEqual(ct.trace(FOREVER, 0, 3)[0], ct.Terminal.EXHAUSTED)
        self.assertEqual(ct.trace(FORK, 0, 3)[0], ct.Terminal.BRANCH)
        s = ct.init(CLIMB, 0, 10)
        torn = ct.State(ex.remove_edge(s.graph, 3 + 2, 1), s.nops, s.active, s.tape, s.clock, s.fuel)
        term, stuck = ct.run(torn)
        self.assertEqual(term, ct.Terminal.REFUSE)
        self.assertEqual((stuck.active, stuck.tape, stuck.clock), (1, (0, 1), 1))

    def test_a_refusal_writes_nothing(self) -> None:
        s = ct.init(CLIMB, 1, 10)
        torn = ct.State(ex.remove_edge(s.graph, 3 + 2, 1), s.nops, s.active, s.tape, s.clock, s.fuel)
        term, stuck = ct.run(torn)
        self.assertEqual(term, ct.Terminal.REFUSE)
        self.assertEqual(stuck, torn)


class Bookkeeping(unittest.TestCase):
    def test_the_clock_counts_exactly_the_firings(self) -> None:
        for C, x in product((PING, CLIMB, FOREVER), range(3)):
            for fuel in range(6):
                _, s = ct.trace(C, x, fuel)
                self.assertEqual(s.clock, len(s.tape) - 1)
                self.assertEqual(s.clock + s.fuel, fuel)

    def test_fuel_is_spent_by_one_per_firing_and_renewed_by_nothing(self) -> None:
        s = ct.init(FOREVER, 0, 3)
        fuels = [s.fuel]
        while True:
            fired = ct.fire(s, 0)
            if not isinstance(fired, ct.State):
                self.assertEqual(fired, ct.Refusal.EXHAUSTED)
                break
            s = fired
            fuels.append(s.fuel)
        self.assertEqual(fuels, [3, 2, 1, 0])

    def test_a_state_with_no_fuel_fires_nothing_however_the_state_was_built(self) -> None:
        """The Lean `fire` matches the fuel as a `Nat`; a hand-built state
        with negative fuel has no counterpart there and must not fire."""
        s = ct.init(FOREVER, 0, 0)
        self.assertEqual(ct.fire(s, 0), ct.Refusal.EXHAUSTED)
        negative = ct.State(s.graph, s.nops, s.active, s.tape, s.clock, -1)
        self.assertEqual(ct.fire(negative, 0), ct.Refusal.EXHAUSTED)
        self.assertEqual(ct.run(negative), (ct.Terminal.EXHAUSTED, negative))
        self.assertEqual(ct.run_det(-3, negative), (ct.Terminal.EXHAUSTED, negative))

    def test_a_negative_operation_index_is_refused_by_name(self) -> None:
        """`3 + k` for a negative `k` would address a store form."""
        with self.assertRaisesRegex(ex.ExecutionError, "not an operation index"):
            ct.fire(ct.init(FOREVER, 0, 3), -3)

    def test_firing_keeps_the_program(self) -> None:
        s = ct.init(PING, 0, 2)
        fired = ct.fire(s, 0)
        assert isinstance(fired, ct.State)
        self.assertEqual(fired.graph, s.graph)
        self.assertEqual(fired.nops, s.nops)


if __name__ == "__main__":
    unittest.main()
