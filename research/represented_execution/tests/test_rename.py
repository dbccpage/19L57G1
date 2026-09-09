"""Renaming the carrier: the permutation, the conjugation, the transport,
and the maps that are refused.

The sweeps are exhaustive over every permutation of the declared carriers and
every deterministic program on them, so a failure names a program, a
permutation and a start.
"""

from __future__ import annotations

from itertools import permutations, product as tuples
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "setting_translation"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import control as ct  # noqa: E402
import rename as rn  # noqa: E402
import translation as tr  # noqa: E402
from execution import ExecutionError  # noqa: E402

BASE = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((1, 2, 0), (0, 0, 0), (1, 2, 2)))
STORED = tr.FiniteSetting(3, frozenset({(0, 1), (1, 2)}), frozenset({(2, 2)}),
                          frozenset({(0, 0)}), 0, 2, ((1, 2, 0),))


class ThePermutation(unittest.TestCase):
    def test_the_inverse_is_computed_and_undoes_the_map(self) -> None:
        for n in (1, 2, 3, 4):
            for order in permutations(range(n)):
                sigma = rn.Renaming(n, order)
                for x in range(n):
                    self.assertEqual(sigma.bwd[sigma.fwd[x]], x, (order, x))
                    self.assertEqual(sigma.fwd[sigma.bwd[x]], x, (order, x))

    def test_a_map_that_is_not_a_permutation_is_refused_by_name(self) -> None:
        for bad in ((0, 0, 1), (0, 1), (0, 1, 3), (1, 1, 1)):
            with self.assertRaises(ExecutionError):
                rn.Renaming(3, bad)

    def test_an_empty_carrier_is_refused(self) -> None:
        with self.assertRaises(ExecutionError):
            rn.Renaming(0, ())

    def test_a_renaming_of_another_carrier_is_refused(self) -> None:
        with self.assertRaises(ExecutionError):
            rn.rename_setting(BASE, rn.identity(2))


class TheConjugation(unittest.TestCase):
    def test_the_identity_renaming_changes_nothing(self) -> None:
        self.assertEqual(rn.rename_setting(BASE, rn.identity(3)), BASE)

    def test_renaming_twice_is_renaming_by_the_composite(self) -> None:
        for first, second in tuples(permutations(range(3)), repeat=2):
            one, two = rn.Renaming(3, first), rn.Renaming(3, second)
            composite = rn.Renaming(3, tuple(two.fwd[one.fwd[x]] for x in range(3)))
            self.assertEqual(rn.rename_setting(rn.rename_setting(BASE, one), two),
                             rn.rename_setting(BASE, composite), (first, second))

    def test_renaming_by_a_permutation_and_back_is_the_setting(self) -> None:
        for order in permutations(range(3)):
            sigma = rn.Renaming(3, order)
            back = rn.Renaming(3, sigma.bwd)
            self.assertEqual(rn.rename_setting(rn.rename_setting(STORED, sigma), back), STORED)

    def test_the_stores_and_endpoints_move_with_the_data(self) -> None:
        sigma = rn.Renaming(3, (1, 2, 0))
        renamed = rn.rename_setting(STORED, sigma)
        self.assertEqual(renamed.rel, frozenset({(1, 2), (2, 0)}))
        self.assertEqual(renamed.ret, frozenset({(0, 0)}))
        self.assertEqual(renamed.prot, frozenset({(1, 1)}))
        self.assertEqual((renamed.a, renamed.b), (1, 0))

    def test_a_conjugated_operation_is_the_operation_read_at_renamed_data(self) -> None:
        for order in permutations(range(3)):
            sigma = rn.Renaming(3, order)
            for table in BASE.ops:
                conjugate = rn.rename_table(sigma, table)
                for x in range(3):
                    self.assertEqual(conjugate[sigma.fwd[x]], sigma.fwd[table[x]], (order, x))


class TheTransport(unittest.TestCase):
    def test_every_run_of_every_program_transports_under_every_permutation(self) -> None:
        result = rn.sweep(BASE, 6)
        self.assertEqual(result["renamings"], 6)
        self.assertEqual(result["programs"], 64)
        self.assertEqual(result["runs_checked"], 1152)
        self.assertTrue(result["every_run_transports"])

    def test_it_transports_on_a_two_point_carrier_too(self) -> None:
        flip = tr.FiniteSetting(2, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((1, 0), (0, 1)))
        result = rn.sweep(flip, 5)
        self.assertEqual(result["runs_checked"], 2 * 9 * 2)
        self.assertTrue(result["every_run_transports"])

    def test_the_branching_program_branches_under_every_renaming(self) -> None:
        """The terminal is carried, not only the tape: a fork stays a fork."""
        fork = ct.Controlled(BASE, frozenset({(0, 0), (0, 1)}))
        for order in permutations(range(3)):
            sigma = rn.Renaming(3, order)
            renamed = rn.rename_controlled(fork, sigma)
            self.assertIs(ct.trace(renamed, sigma.fwd[0], 5)[0], ct.Terminal.BRANCH, order)

    def test_the_sweep_names_the_run_that_fails(self) -> None:
        """The refusal is diagnostic, not a bare False: a setting whose
        operations are renamed but whose enablement is not would break the
        transport, and the message says which run."""
        original = rn.rename_controlled

        def broken(C: ct.Controlled, sigma: rn.Renaming) -> ct.Controlled:
            return ct.Controlled(rn.rename_setting(C.F, sigma), C.ctrl)

        rn.rename_controlled = broken
        try:
            with self.assertRaisesRegex(ExecutionError, "does not transport under"):
                rn.sweep(BASE, 6)
        finally:
            rn.rename_controlled = original


if __name__ == "__main__":
    unittest.main()
