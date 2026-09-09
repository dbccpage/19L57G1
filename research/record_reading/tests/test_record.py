"""The record-reading machine: the program, the read, the reference step,
the distinction and its disappearance."""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys
import unittest

# Dependencies first, this tree last, so this tree wins name collisions with
# the sibling families (``run``, ``verify_sources``).
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1] / "code"))
sys.path.insert(0, str(ROOT.parent / "setting_translation"))
sys.path.insert(0, str(ROOT.parent / "represented_execution"))
sys.path.insert(0, str(ROOT.parent / "coherent_process_limits"))
sys.path.insert(0, str(ROOT))

import control as ct  # noqa: E402
from execution import ExecutionError  # noqa: E402
import limits as lm  # noqa: E402
import record as rc  # noqa: E402
import translation as tr  # noqa: E402


class Setting(unittest.TestCase):
    F: tr.FiniteSetting
    forever: ct.Controlled

    @classmethod
    def setUpClass(cls) -> None:
        programs, _ = lm.identify_programs(lm.load_artifact())
        cls.forever = programs["forever"]
        cls.F = cls.forever.F
        rc.check_base(cls.F)


class Program(Setting):
    def test_the_direct_program_is_the_sealed_replay_beyond_the_stores(self) -> None:
        laws: list[rc.Recorded] = [rc.twist(self.F), rc.turncoat(self.F), rc.lift(self.forever)]
        laws.extend(rc.lift(C) for C in lm.deterministic_programs(self.F))
        pairs = [(p, x) for p in range(3) for x in range(3)]
        for index, choice in enumerate(product(range(-1, 3), repeat=9)):
            if index % 997 == 0:
                laws.append(rc.Recorded(self.F, frozenset((p, x, k) for (p, x), k in zip(pairs, choice) if k >= 0)))
        self.assertGreater(len(laws), 300)
        for C in laws:
            self.assertEqual(rc.rprogram(C), rc.rprogram_by_replay(C))

    def test_the_regime_has_one_more_form_per_operation(self) -> None:
        r = rc.encode_r(rc.twist(self.F))
        self.assertEqual(len(r.forms), 3 + 2 * 3)
        self.assertTrue(all(a == 2 for a in r.forms))
        self.assertIn((3 + 3 + 1, (1, 0)), rc.rprogram(rc.twist(self.F)))

    def test_the_record_read_is_faithful_and_relational(self) -> None:
        C = rc.turncoat(self.F)
        g = rc.rprogram(C)
        for p in range(3):
            for x in range(3):
                for k in range(3):
                    self.assertEqual(rc.renabled(g, 3, p, x, k), (p, x, k) in C.hctrl)
        # several instances of one control form leave datum 0: a relation, not a function.
        self.assertGreater(sum(1 for f, args in g if f == 3 + 3 + 0 and args[0] == 0), 1)

    def test_the_memoryless_reader_refuses_a_record_program(self) -> None:
        """A record program is not an operation graph on its control forms:
        several instances of one form leave one record entry.  The merged
        reader goes through ``lookup``, which refuses such a form by name, so
        it must not be applied here — the dispatch in ``selection.py`` is what
        keeps it away."""
        for C in (rc.turncoat(self.F), rc.lift(self.forever)):
            g = rc.rprogram(C)
            with self.assertRaisesRegex(ExecutionError, "not an operation graph"):
                ct.enabled_at(g, 3, 0)
            with self.assertRaisesRegex(ExecutionError, "not an operation graph"):
                ct.step_det(ct.State(g, 3, 0, (0,), 0, 3))

    def test_an_enablement_outside_the_setting_is_refused(self) -> None:
        with self.assertRaisesRegex(ExecutionError, "outside the setting"):
            rc.Recorded(self.F, frozenset({(0, 3, 0)}))
        with self.assertRaisesRegex(ExecutionError, "outside the setting"):
            rc.Recorded(self.F, frozenset({(0, 0, 3)}))
        with self.assertRaisesRegex(ExecutionError, "outside the carrier"):
            rc.rinit(rc.twist(self.F), 3, 1)

    def test_a_setting_whose_tables_are_not_the_transcribed_ones_is_refused(self) -> None:
        other = tr.FiniteSetting(3, self.F.rel, self.F.ret, self.F.prot, 0, 1, (self.F.ops[1], self.F.ops[0], self.F.ops[2]))
        with self.assertRaisesRegex(ExecutionError, "not the transcribed base"):
            rc.check_base(other)


class TheRecordIsRead(Setting):
    def test_twist_visits_0_1_0_0(self) -> None:
        s = rc.rinit(rc.twist(self.F), 0, 3)
        self.assertEqual(rc.robs(3, s), (0, 1, 0, 0))
        self.assertEqual(rc.robs(6, rc.rinit(rc.twist(self.F), 0, 6)), (0, 1, 0, 0, 1, 0, 0))
        actives = [rc.riter(n, s).active for n in range(4)]
        self.assertEqual(actives[2], actives[0])
        self.assertNotEqual(actives[3], actives[1])

    def test_no_memoryless_program_visits_0_1_0_0(self) -> None:
        for C in lm.deterministic_programs(self.F):
            for x in range(3):
                self.assertNotEqual(ct.trace(C, x, 3)[1].tape, (0, 1, 0, 0))
        self.assertFalse(lm.functional((0, 1, 0, 0)))

    def test_previous_is_what_the_last_firing_wrote(self) -> None:
        for C in (rc.twist(self.F), rc.turncoat(self.F), rc.lift(self.forever)):
            for x in range(3):
                s = rc.rinit(C, x, 6)
                self.assertTrue(rc.synced(s))
                self.assertEqual(rc.previous(s), x)
                for _ in range(6):
                    nxt = rc.rstep_det(s)
                    if not isinstance(nxt, ct.State):
                        break
                    self.assertEqual(rc.previous(nxt), s.active)
                    self.assertTrue(rc.synced(nxt))
                    s = nxt

    def test_the_read_is_from_the_state_and_nowhere_else(self) -> None:
        C = rc.twist(self.F)
        s = rc.rinit(C, 0, 3)
        # the instance the third step reads: the constant map at 0 after 1
        read = (3 + 3 + 1, (1, 0))
        edited = ct.State(frozenset(s.graph - {read}) | {(3 + 3 + 0, (1, 0))}, s.nops, s.active, s.tape, s.clock, s.fuel)
        self.assertEqual(rc.robs(3, edited), (0, 1, 0, 1))
        # an instance no step reads: the climb at 2 after 2
        untouched = ct.State(frozenset(s.graph | {(3 + 3 + 2, (2, 2))}), s.nops, s.active, s.tape, s.clock, s.fuel)
        self.assertEqual(rc.robs(3, untouched), (0, 1, 0, 0))

    def test_forgetting_the_record_removes_the_distinction(self) -> None:
        forgotten = rc.forget(rc.twist(self.F))
        self.assertEqual(forgotten.ctrl, frozenset({(0, 0)}))
        terminal, s = ct.trace(forgotten, 0, 3)
        self.assertEqual(s.tape, (0, 1))
        self.assertEqual(terminal, ct.Terminal.HALT)

    def test_the_lifted_memoryless_program_runs_as_the_memoryless_one(self) -> None:
        lifted = rc.lift(self.forever)
        self.assertEqual(len(lifted.hctrl), 9)
        for x in range(3):
            for n in range(9):
                self.assertEqual(rc.robs(n, rc.rinit(lifted, x, 8)), lm.obs(n, ct.init(self.forever, x, 8)))
        self.assertEqual(rc.forget(lifted), self.forever)


class ReferenceAndRunner(Setting):
    def test_successors_are_exactly_the_reference_steps(self) -> None:
        for C in (rc.twist(self.F), rc.turncoat(self.F), rc.lift(self.forever)):
            for p in range(3):
                for x in range(3):
                    s = ct.State(rc.rprogram(C), 3, x, (p, x), 1, 2)
                    self.assertEqual(rc.previous(s), p)
                    got = sorted(t.active for t in rc.rsuccessors(s))
                    expected = sorted(tr.run(C.F, (k,), x) for k in range(3) if (p, x, k) in C.hctrl)
                    self.assertEqual(got, expected, (C.hctrl, p, x))
                    for t in rc.rsuccessors(s):
                        self.assertTrue(any(rc.rstep(C, p, x, k, t.active) for k in range(3)))

    def test_the_runner_never_selects(self) -> None:
        fork = rc.Recorded(self.F, frozenset({(0, 0, 0), (0, 0, 1)}))
        terminal, s = rc.rtrace(fork, 0, 5)
        self.assertEqual(terminal, ct.Terminal.BRANCH)
        self.assertEqual(s.tape, (0,))
        self.assertEqual(len(rc.rsuccessors(s)), 2)

    def test_the_terminals_are_kept_apart(self) -> None:
        halt = rc.Recorded(self.F, frozenset())
        self.assertEqual(rc.rtrace(halt, 0, 3)[0], ct.Terminal.HALT)
        self.assertEqual(rc.rtrace(rc.twist(self.F), 0, 0)[0], ct.Terminal.EXHAUSTED)
        s = rc.rinit(rc.twist(self.F), 0, 3)
        broken = ct.State(frozenset(i for i in s.graph if i != (3, (0, 1))), s.nops, s.active, s.tape, s.clock, s.fuel)
        self.assertEqual(rc.rrun(broken)[0], ct.Terminal.REFUSE)
        self.assertEqual(rc.rrun(broken)[1].tape, (0,))

    def test_observations_are_compatible_at_every_scale(self) -> None:
        for C in (rc.twist(self.F), rc.turncoat(self.F), rc.lift(self.forever)):
            for x in range(3):
                s = rc.rinit(C, x, 10)
                for n in range(10):
                    self.assertTrue(lm.is_prefix(rc.robs(n, s), rc.robs(n + 1, s)))

    def test_the_clock_counts_the_firings_and_fuel_is_spent(self) -> None:
        terminal, s = rc.rtrace(rc.twist(self.F), 0, 6)
        self.assertEqual(terminal, ct.Terminal.EXHAUSTED)
        self.assertEqual(s.clock, 6)
        self.assertEqual(s.fuel, 0)


if __name__ == "__main__":
    unittest.main()
