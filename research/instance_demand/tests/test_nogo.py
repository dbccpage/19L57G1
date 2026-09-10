"""Python controls for the scoped two-edge no-go class.

These reconstruct InClass membership and the in-class failure shapes on
the Stage-3 seed. They do not close OB-1 outside that class.
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


def e2_prime(regime: Regime, impose: bool, i: int, j: int) -> bool:
    return (not separable(regime, i, j)) and (not impose)


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

    def test_host_emit_writes_via_admitInst_events(self) -> None:
        r = unruled_seed()
        after, events = e.emit(r)
        self.assertIn((5, (0, 1)), after.insts)
        self.assertNotIn((5, (0, 1)), r.insts)
        self.assertTrue(events)
        self.assertTrue(all(isinstance(ev, AdmitInst) for ev in events))

    def test_impose_cannot_be_e2prime_origin(self) -> None:
        r = unruled_seed()
        self.assertFalse(separable(r, 0, 1))
        self.assertFalse(e2_prime(r, True, 0, 1))
        self.assertTrue(e2_prime(r, False, 0, 1))

    def test_unruled_emission_separates_so_e3_fails(self) -> None:
        r = unruled_seed()
        self.assertFalse(separable(r, 0, 1))
        after, _events = e.emit(r)
        self.assertTrue(separable(after, 0, 1))
