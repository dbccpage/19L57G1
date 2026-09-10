"""Python controls for the scoped two-edge no-go class.

These reconstruct InClass membership and the three failure shapes on
the existing Stage-3 seed. They do not close OB-1 outside that class.
AuthorityEffect: None.
"""

from __future__ import annotations

import unittest

from derivation.model import AdmitDatum, AdmitForm, AdmitInst, Impose, Regime, Supply, replay
from derivation.observe import separable
import emitter as e


def in_class(regime: Regime, c: tuple[int, tuple[int, ...]]) -> bool:
    form, args = c
    return form == 0 and len(args) == 3 and (form, args) in regime.insts


def unruled_seed() -> Regime:
    return replay(e.history(3, ((0, 2),), ((2, 1),), True, False))


def covered_seed() -> Regime:
    return replay(e.history(3, ((0, 2),), ((2, 1),), True, True))


class NoGoClass(unittest.TestCase):
    def test_class_nonempty_and_covers_seed_instruction(self) -> None:
        self.assertTrue(in_class(unruled_seed(), (0, (0, 1, 2))))
        self.assertTrue(in_class(covered_seed(), (0, (0, 1, 2))))

    def test_unruled_enabled_output_is_not_stored(self) -> None:
        r = unruled_seed()
        self.assertNotIn((5, (0, 1)), r.insts)
        self.assertNotIn(5, r.rules)

    def test_host_emit_writes_via_admitInst_events(self) -> None:
        r = unruled_seed()
        after, events = e.emit(r)
        self.assertIn((5, (0, 1)), after.insts)
        self.assertNotIn((5, (0, 1)), r.insts)
        self.assertTrue(events)
        self.assertTrue(all(isinstance(ev, AdmitInst) for ev in events))

    def test_impose_is_not_owed_separation_origin(self) -> None:
        r = unruled_seed()
        child = replay((Impose(0, 1),), base=r)
        self.assertIn((0, 1), child.reqs)
        self.assertNotIn((0, 1), r.reqs)

    def test_i1_shape_is_already_separable(self) -> None:
        r = replay((
            Supply("a"), AdmitDatum("a"), Supply("b"), AdmitDatum("b"),
            AdmitForm(2), AdmitInst(0, (0, 1)),
        ))
        self.assertTrue(separable(r, 0, 1))

    def test_cheating_class_that_drops_enabled_instruction_is_rejected(self) -> None:
        r = unruled_seed()
        def cheating(regime: Regime, c: tuple[int, tuple[int, ...]]) -> bool:
            return in_class(regime, c) and c[1][0] == 9
        self.assertFalse(cheating(r, (0, (0, 1, 2))))
        self.assertTrue(in_class(r, (0, (0, 1, 2))))
