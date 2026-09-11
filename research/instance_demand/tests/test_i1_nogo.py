"""Python controls for the I1 pair-instance sibling no-go class.

I1Class is a stored binary form-0 instance with distinct endpoints.
It is disjoint from the instruction class. These tests do not close
OB-1 outside the two named classes.
AuthorityEffect: None.
"""

from __future__ import annotations

import unittest

from derivation.model import AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Impose, Regime, replay
from derivation.observe import separable
import emitter as e


def in_class(regime: Regime, c: tuple[int, tuple[int, ...]]) -> bool:
    form, args = c
    return form == 0 and len(args) == 3 and (form, args) in regime.insts


def owed(regime: Regime, i: int, j: int) -> bool:
    return i < j < regime.n_data() and not separable(regime, i, j)


def i1_class(regime: Regime, c: tuple[int, tuple[int, ...]]) -> bool:
    form, args = c
    return (
        form == 0
        and len(args) == 2
        and args[0] != args[1]
        and (form, args) in regime.insts
    )


def i1_lone() -> Regime:
    return replay((AdmitDatum("0"), AdmitDatum("1"), AdmitForm(2), AdmitInst(0, (0, 1))))


def i1_covered() -> Regime:
    return replay((
        AdmitDatum("0"), AdmitDatum("1"), AdmitForm(2), AdmitInst(0, (0, 1)), AdmitRuleAll(0),
    ))


class I1NoGoClass(unittest.TestCase):
    def test_i1_class_nonempty_on_both_coverages(self) -> None:
        pair = (0, (0, 1))
        self.assertTrue(i1_class(i1_lone(), pair))
        self.assertTrue(i1_class(i1_covered(), pair))

    def test_i1_is_disjoint_from_instruction_class(self) -> None:
        lone = i1_lone()
        pair = (0, (0, 1))
        self.assertTrue(i1_class(lone, pair))
        self.assertFalse(in_class(lone, pair))
        seed = replay(e.history(3, ((0, 2),), ((2, 1),), True, False))
        instruction = (0, (0, 1, 2))
        self.assertTrue(in_class(seed, instruction))
        self.assertFalse(i1_class(seed, instruction))

    def test_cheating_i1_class_that_requires_equal_endpoints_is_rejected(self) -> None:
        lone = i1_lone()
        pair = (0, (0, 1))

        def cheating(regime: Regime, c: tuple[int, tuple[int, ...]]) -> bool:
            return i1_class(regime, c) and c[1][0] == c[1][1]

        self.assertTrue(i1_class(lone, pair))
        self.assertFalse(cheating(lone, pair))

    def test_unruled_i1_separates_so_owed_fails(self) -> None:
        r = i1_lone()
        self.assertTrue(separable(r, 0, 1))
        self.assertFalse(owed(r, 0, 1))

    def test_covered_i1_stays_collapsed(self) -> None:
        r = i1_covered()
        self.assertFalse(separable(r, 0, 1))
        self.assertTrue(owed(r, 0, 1))

    def test_i1_store_is_admitInst_not_native_store(self) -> None:
        base = replay((AdmitDatum("0"), AdmitDatum("1"), AdmitForm(2)))
        pair = (0, (0, 1))
        self.assertFalse(i1_class(base, pair))
        after = replay((AdmitInst(0, (0, 1)),), base=base)
        self.assertTrue(i1_class(after, pair))
        self.assertNotIn(pair, base.insts)
        self.assertEqual(replay((Impose(0, 1),), base=base).insts, base.insts)
        self.assertEqual(replay((AdmitRuleAll(0),), base=base).insts, base.insts)

    def test_i1_is_not_an_enabled_output(self) -> None:
        r = i1_lone()
        pair = (0, (0, 1))
        self.assertNotIn(pair, e.raw_outputs(r.insts))

    def test_conjunction_fails_unruled_and_covered(self) -> None:
        pair = (0, (0, 1))
        for regime in (i1_lone(), i1_covered()):
            self.assertTrue(i1_class(regime, pair))
            self.assertNotIn(pair, e.raw_outputs(regime.insts))


if __name__ == "__main__":
    unittest.main()
