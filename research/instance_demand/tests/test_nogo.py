"""Python controls for the scoped two-edge no-go class.

These reconstruct InClass membership, channel E1 (host `AdmitInst` allowed),
the owed-separation clause, and E3 on the Stage-3 seed. They do not close
OB-1 outside that class.
AuthorityEffect: None.
"""

from __future__ import annotations

import unittest

from derivation.model import AdmitForm, AdmitInst, AdmitRuleAll, Impose, Regime, replay
from derivation.observe import derivable, separable
import emitter as e


def in_class(regime: Regime, c: tuple[int, tuple[int, ...]]) -> bool:
    form, args = c
    return form == 0 and len(args) == 3 and (form, args) in regime.insts


def reads_output(regime: Regime, c: tuple[int, tuple[int, ...]],
                 out: tuple[int, tuple[int, ...]]) -> bool:
    form, args = c
    return (
        (form, args) in regime.insts
        and form == 0
        and len(args) == 3
        and out in e.raw_outputs(regime.insts)
        and out[0] == 3 + args[2]
    )


def owed(regime: Regime, i: int, j: int) -> bool:
    return i < j < regime.n_data() and not separable(regime, i, j)


def e2_prime(r: Regime, s: Regime, impose: bool, out: tuple[int, tuple[int, ...]],
             i: int, j: int) -> bool:
    return (
        out[1] == (i, j)
        and owed(s, i, j)
        and (not impose)
        and out in e.raw_outputs(r.insts)
    )


def e3(r: Regime, s: Regime, out: tuple[int, tuple[int, ...]],
       i: int, j: int) -> bool:
    form, args = out
    return (
        args == (i, j)
        and owed(s, i, j)
        and not owed(r, i, j)
        and form in r.rules
    )


def unruled_seed() -> Regime:
    return replay(e.history(3, ((0, 2),), ((2, 1),), True, False))


def covered_seed() -> Regime:
    return replay(e.history(3, ((0, 2),), ((2, 1),), True, True))


class NoGoClass(unittest.TestCase):
    def test_class_nonempty_independent_of_output_coverage(self) -> None:
        instruction = (0, (0, 1, 2))
        self.assertTrue(in_class(unruled_seed(), instruction))
        self.assertTrue(in_class(covered_seed(), instruction))

    def test_every_stored_form0_ternary_is_in_class(self) -> None:
        r = unruled_seed()
        found = 0
        for inst in r.insts:
            if inst[0] == 0 and len(inst[1]) == 3:
                self.assertTrue(in_class(r, inst))
                found += 1
        self.assertEqual(found, 1)
        self.assertIn((5, (0, 1)), e.raw_outputs(r.insts))

    def test_cheating_class_that_drops_enabled_instruction_is_rejected(self) -> None:
        r = unruled_seed()
        instruction = (0, (0, 1, 2))

        def cheating(regime: Regime, c: tuple[int, tuple[int, ...]]) -> bool:
            return in_class(regime, c) and c[1][0] == 9

        self.assertTrue(in_class(r, instruction))
        self.assertFalse(cheating(r, instruction))
        self.assertIn((5, (0, 1)), e.raw_outputs(r.insts))

    def test_i1_singleton_is_not_in_class(self) -> None:
        r = unruled_seed()
        self.assertFalse(in_class(r, (0, (0, 1))))

    def test_unruled_enabled_output_is_not_natively_derivable(self) -> None:
        r = unruled_seed()
        out = (5, (0, 1))
        self.assertNotIn(out, r.insts)
        self.assertNotIn(5, r.rules)
        self.assertFalse(derivable(r, out))

    def test_non_admitInst_events_do_not_store_the_enabled_output(self) -> None:
        r = unruled_seed()
        out = (5, (0, 1))
        self.assertNotIn(out, r.insts)
        self.assertEqual(replay((Impose(0, 1),), base=r).insts, r.insts)
        self.assertEqual(replay((AdmitRuleAll(5),), base=r).insts, r.insts)
        self.assertEqual(replay((AdmitForm(2),), base=r).insts, r.insts)

    def test_host_emit_is_channel_e1_not_native_store(self) -> None:
        r = covered_seed()
        after, events = e.emit(r)
        c = (0, (0, 1, 2))
        out = (5, (0, 1))
        self.assertTrue(in_class(r, c))
        self.assertTrue(reads_output(r, c, out))
        self.assertIn(out, after.insts)
        self.assertNotIn(out, r.insts)
        self.assertTrue(events)
        self.assertTrue(all(isinstance(ev, AdmitInst) for ev in events))

    def test_impose_cannot_be_e2prime_origin(self) -> None:
        r = unruled_seed()
        after, _events = e.emit(r)
        out = (5, (0, 1))
        self.assertFalse(e2_prime(r, after, True, out, 0, 1))

    def test_unruled_emission_separates_so_owed_fails(self) -> None:
        r = unruled_seed()
        self.assertTrue(owed(r, 0, 1))
        after, _events = e.emit(r)
        self.assertTrue(separable(after, 0, 1))
        self.assertFalse(owed(after, 0, 1))
        self.assertFalse(e3(r, after, (5, (0, 1)), 0, 1))

    def test_covered_emission_is_already_owed_so_e3_fails(self) -> None:
        r = covered_seed()
        after, _events = e.emit(r)
        out = (5, (0, 1))
        self.assertTrue(owed(r, 0, 1))
        self.assertTrue(owed(after, 0, 1))
        self.assertIn(5, r.rules)
        self.assertFalse(e3(r, after, out, 0, 1))

    def test_weak_e3_without_freshness_would_pass_covered(self) -> None:
        r = covered_seed()
        after, _events = e.emit(r)
        self.assertFalse(separable(after, 0, 1))
        self.assertTrue(owed(after, 0, 1))
        self.assertTrue(owed(r, 0, 1))
        self.assertFalse(e3(r, after, (5, (0, 1)), 0, 1))

    def test_conjunction_fails_on_both_coverages(self) -> None:
        c = (0, (0, 1, 2))
        out = (5, (0, 1))
        for seed in (unruled_seed, covered_seed):
            r = seed()
            after, events = e.emit(r)
            self.assertTrue(in_class(r, c))
            self.assertTrue(reads_output(r, c, out))
            self.assertTrue(all(isinstance(ev, AdmitInst) for ev in events))
            self.assertFalse(e3(r, after, out, 0, 1))

    def test_functional_run_stays_in_class(self) -> None:
        r = covered_seed()
        c = (0, (0, 1, 2))
        self.assertTrue(in_class(r, c))
        self.assertEqual(e.eval_word(r.insts, (0, 1), 0), 1)
        self.assertIn((5, (0, 1)), e.raw_outputs(r.insts))
