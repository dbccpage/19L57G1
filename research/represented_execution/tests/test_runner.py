"""One interpreter at several readers, and the merged machine as one of them.

The Lean states the identification as `rfl`; Python checks it, exhaustively
over every deterministic and every non-deterministic program on the declared
three-point setting, from every datum, at every scale up to the fuel.  A
failure names the program, the start and the scale.
"""

from __future__ import annotations

from itertools import product as tuples
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "setting_translation"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import control as ct  # noqa: E402
import runner as rn  # noqa: E402
import translation as tr  # noqa: E402

BASE = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((1, 2, 0), (0, 0, 0), (1, 2, 2)))
FUEL = 6


def every_program() -> list[ct.Controlled]:
    """Every enablement relation on the setting, deterministic or not: each
    datum may enable any subset of the three operations."""
    out: list[ct.Controlled] = []
    for choice in tuples(range(8), repeat=BASE.n):
        pairs = {(x, k) for x, mask in enumerate(choice) for k in range(3) if mask >> k & 1}
        out.append(ct.Controlled(BASE, frozenset(pairs)))
    return out


class TheMergedMachineIsTheGenericOne(unittest.TestCase):
    programs: list[ct.Controlled]

    @classmethod
    def setUpClass(cls) -> None:
        cls.programs = every_program()

    def test_the_population_is_every_enablement_relation(self) -> None:
        self.assertEqual(len(self.programs), 8 ** 3)

    def test_one_step_agrees_at_every_state_a_run_reaches(self) -> None:
        for C in self.programs:
            for start in range(BASE.n):
                s = ct.init(C, start, FUEL)
                for _ in range(FUEL + 1):
                    mine, theirs = ct.step_det(s), rn.step_det_of(rn.ctrl_reader, s)
                    self.assertEqual(mine, theirs, (sorted(C.ctrl), start))
                    if isinstance(mine, ct.Terminal):
                        break
                    s = mine

    def test_the_whole_run_agrees(self) -> None:
        for C in self.programs:
            for start in range(BASE.n):
                s = ct.init(C, start, FUEL)
                self.assertEqual(ct.run(s), rn.run_det_of(rn.ctrl_reader, s.fuel, s),
                                 (sorted(C.ctrl), start))

    def test_the_observation_agrees_at_every_scale(self) -> None:
        for C in self.programs:
            for start in range(BASE.n):
                s = ct.init(C, start, FUEL)
                for scale in range(FUEL + 1):
                    self.assertEqual(rn.obs_of(rn.ctrl_reader, scale, s),
                                     rn.iter_of(rn.ctrl_reader, scale, s).tape, scale)

    def test_the_observation_only_appends(self) -> None:
        for C in self.programs:
            for start in range(BASE.n):
                s = ct.init(C, start, FUEL)
                for scale in range(FUEL):
                    coarse = rn.obs_of(rn.ctrl_reader, scale, s)
                    fine = rn.obs_of(rn.ctrl_reader, scale + 1, s)
                    self.assertEqual(fine[: len(coarse)], coarse, (sorted(C.ctrl), start, scale))

    def test_it_never_selects_on_any_program(self) -> None:
        for C in self.programs:
            for start in range(BASE.n):
                s = ct.init(C, start, FUEL)
                terminal, final = rn.run_det_of(rn.ctrl_reader, s.fuel, s)
                if terminal is ct.Terminal.BRANCH:
                    self.assertGreaterEqual(len(rn.ctrl_reader(final)), 2, sorted(C.ctrl))


class TheTwoExtremeReaders(unittest.TestCase):
    def test_a_reader_that_ignores_the_state_halts_at_once(self) -> None:
        s = ct.init(ct.Controlled(BASE, frozenset({(0, 0)})), 0, FUEL)
        self.assertIs(rn.step_det_of(rn.blind_reader, s), ct.Terminal.HALT)
        self.assertEqual(rn.obs_of(rn.blind_reader, 5, s), s.tape)

    def test_a_reader_that_names_two_everywhere_always_branches(self) -> None:
        s = ct.init(ct.Controlled(BASE, frozenset({(0, 0)})), 0, FUEL)
        self.assertIs(rn.step_det_of(rn.greedy_reader, s), ct.Terminal.BRANCH)
        self.assertIs(rn.run_det_of(rn.greedy_reader, s.fuel, s)[0], ct.Terminal.BRANCH)

    def test_the_next_value_is_none_where_the_reader_does_not_name_one(self) -> None:
        s = ct.init(ct.Controlled(BASE, frozenset({(0, 0)})), 0, FUEL)
        self.assertIsNone(rn.next_value_of(rn.blind_reader, s))
        self.assertIsNone(rn.next_value_of(rn.greedy_reader, s))
        self.assertEqual(rn.next_value_of(rn.ctrl_reader, s), 1)


if __name__ == "__main__":
    unittest.main()
