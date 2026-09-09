"""The depth-two machine, the mixed-arity regime, and the ladder.

The sweeps are exhaustive over every deterministic program of each built
depth on the declared two-point setting, so a failure names a program.  The
tapes asserted are hand-copied from the statements of ``lean/Depth.lean``:
the Lean machine is written on functions and this one on value tables and
frozen sets, so agreement is a cross-check between two implementations and
not a second reading of one.
"""

from __future__ import annotations

from itertools import product as tuples
from pathlib import Path
import sys
from typing import cast
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "setting_translation"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "represented_execution"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "coherent_process_limits"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import control as ct  # noqa: E402
import runner as rn  # noqa: E402
import depth as dp  # noqa: E402
import record as rc  # noqa: E402
import translation as tr  # noqa: E402
from execution import ExecutionError  # noqa: E402

BASE = tr.FiniteSetting(3, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((1, 2, 0), (0, 0, 0), (1, 2, 2)))
TWO = tr.FiniteSetting(2, tr.NONE, tr.NONE, tr.NONE, 0, 1, ((1, 0), (0, 1)))
TWIST2 = dp.Recorded2(BASE, frozenset({(0, 0, 0, 0), (0, 0, 1, 0), (0, 1, 2, 0),
                                       (1, 2, 0, 0), (2, 0, 1, 1)}))
TWIST = rc.Recorded(BASE, frozenset({(0, 0, 0), (0, 1, 1), (1, 0, 1)}))


class TheMixedArityRegime(unittest.TestCase):
    def test_the_enablement_form_is_ternary_and_the_rest_binary(self) -> None:
        self.assertEqual(list(dp.encode_r2(TWIST2).forms), [2, 2, 2, 2, 2, 2, 3, 3, 3])
        self.assertEqual(list(dp.forms_of(3)), [2, 2, 2, 2, 2, 2, 3, 3, 3])

    def test_the_program_is_the_sealed_replay_of_its_own_history(self) -> None:
        self.assertEqual(dp.r2program(TWIST2), dp.r2program_by_replay(TWIST2))

    def test_an_enablement_outside_the_setting_is_refused_by_name(self) -> None:
        for bad in ((3, 0, 0, 0), (0, 3, 0, 0), (0, 0, 3, 0), (0, 0, 0, 3)):
            with self.assertRaises(ExecutionError):
                dp.Recorded2(BASE, frozenset({bad}))

    def test_a_start_or_a_scale_outside_its_range_is_refused(self) -> None:
        with self.assertRaises(ExecutionError):
            dp.r2init(TWIST2, 3, 5)
        with self.assertRaises(ExecutionError):
            dp.r2init(TWIST2, 0, -1)
        with self.assertRaises(ExecutionError):
            dp.r2iter(-1, dp.r2init(TWIST2, 0, 5))


class TheExhibit(unittest.TestCase):
    def test_the_depth_two_run_is_the_tape_the_theorem_names(self) -> None:
        self.assertEqual(list(dp.r2obs(5, dp.r2init(TWIST2, 0, 5))), [0, 1, 2, 0, 1, 0])

    def test_that_tape_is_functional_in_triples_and_not_in_pairs(self) -> None:
        tape = dp.r2obs(5, dp.r2init(TWIST2, 0, 5))
        self.assertTrue(dp.functional(3, tape))
        self.assertFalse(dp.functional(2, tape))

    def test_no_depth_one_program_realises_it(self) -> None:
        """`Depth.no_record_run_realises`, checked over every deterministic
        depth-one program on the same carrier rather than proved."""
        target = (0, 1, 2, 0, 1, 0)
        for choice in dp.deterministic_choices(2, BASE.n, len(BASE.ops)):
            C = rc.Recorded(BASE, frozenset((key[0], key[1], k) for key, k in choice.items()))
            for start in range(BASE.n):
                self.assertNotEqual(rc.robs(5, rc.rinit(C, start, 5)), target)

    def test_the_depth_one_exhibit_breaks_the_rung_below_it(self) -> None:
        tape = rc.robs(3, rc.rinit(TWIST, 0, 3))
        self.assertEqual(list(tape), [0, 1, 0, 0])
        self.assertTrue(dp.functional(2, tape))
        self.assertFalse(dp.functional(1, tape))

    def test_a_depth_one_setting_lifted_reads_the_entry_it_is_given_and_ignores_it(self) -> None:
        lifted = dp.lift2(TWIST)
        for start in range(BASE.n):
            self.assertEqual(dp.r2obs(5, dp.r2init(lifted, start, 5)),
                             rc.robs(5, rc.rinit(TWIST, start, 5)), start)


class Windows(unittest.TestCase):
    def test_the_windows_of_a_tape_are_its_contiguous_runs(self) -> None:
        self.assertEqual(dp.windows(2, (0, 1, 2)), ((0, 1), (1, 2)))
        self.assertEqual(dp.windows(3, (0, 1, 2)), ((0, 1, 2),))
        self.assertEqual(dp.windows(4, (0, 1, 2)), ())

    def test_a_window_without_a_length_is_refused(self) -> None:
        with self.assertRaises(ExecutionError):
            dp.windows(0, (0, 1))

    def test_a_tape_functional_in_fewer_entries_is_functional_in_more(self) -> None:
        """`Depth.triples_of_pairs` and `quads_of_triples`, over every tape of
        length at most five on three data."""
        for length in range(1, 6):
            for tape in tuples(range(3), repeat=length):
                for k in (1, 2, 3):
                    if dp.functional(k, tape):
                        self.assertTrue(dp.functional(k + 1, tape), (tape, k))


class TheLadder(unittest.TestCase):
    rows: list[dict[str, object]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = dp.ladder(TWO, 6)

    def test_every_realised_tape_meets_its_own_depth_ceiling(self) -> None:
        for row in self.rows:
            self.assertTrue(row["every_tape_meets_this_ceiling"], row["entries_read"])

    def test_each_rung_realises_a_tape_the_one_below_cannot(self) -> None:
        for row in self.rows[1:]:
            self.assertTrue(row["strictly_more_than_the_depth_below"], row["entries_read"])
            self.assertTrue(row["tapes_breaking_the_ceiling_below"], row["entries_read"])

    def test_the_counts_the_receipt_records(self) -> None:
        self.assertEqual([row["tapes_realised"] for row in self.rows], [10, 22, 70])
        self.assertEqual([row["window"] for row in self.rows], [2, 3, 4])

    def test_breaking_the_ceiling_below_is_a_proper_subset_of_being_unrealisable(self) -> None:
        """The ceiling gives one direction: a tape breaking it is realised by
        no program of the depth below.  The converse is **false**, and the test
        asserts that it is false so the stronger claim cannot be re-asserted
        quietly.  The extra tapes are all short — runs that stopped before the
        fuel ran out — and are functional at the shallower window; the ceiling
        says nothing about when a machine may halt."""
        for row in self.rows[1:]:
            beyond = {tuple(t) for t in cast(list[list[int]],
                                             row["tapes_the_depth_below_cannot_realise"])}
            breaking = {tuple(t) for t in cast(list[list[int]],
                                               row["tapes_breaking_the_ceiling_below"])}
            self.assertTrue(breaking < beyond, row["entries_read"])
            for tape in beyond - breaking:
                self.assertTrue(dp.functional(cast(int, row["entries_read"]) - 1, tape), tape)
                self.assertLess(len(tape), 7, tape)

    def test_the_two_cardinalities_the_ledger_quotes(self) -> None:
        self.assertEqual([len(cast(list[list[int]], row["tapes_breaking_the_ceiling_below"]))
                          for row in self.rows], [0, 8, 38])
        self.assertEqual([len(cast(list[list[int]], row["tapes_the_depth_below_cannot_realise"]))
                          for row in self.rows], [0, 12, 48])

    def test_a_depth_no_machine_is_built_for_is_refused_rather_than_guessed(self) -> None:
        with self.assertRaises(ExecutionError):
            dp.realized_tapes(4, TWO, 3)


class AgainstTheMemorylessMachine(unittest.TestCase):
    def test_a_memoryless_run_is_functional_in_its_entries(self) -> None:
        """`Observe.obs_functional`, over every deterministic memoryless
        program on the three-point carrier."""
        for choice in dp.deterministic_choices(1, BASE.n, len(BASE.ops)):
            C = ct.Controlled(BASE, frozenset((key[0], k) for key, k in choice.items()))
            for start in range(BASE.n):
                self.assertTrue(dp.functional(1, ct.trace(C, start, 6)[1].tape), choice)


class ThreeReadersOneRunner(unittest.TestCase):
    """W44 in Python: the three machines are the one interpreter at three
    readers, checked over the declared populations rather than by `rfl`."""

    def record_reader(self, s: ct.State) -> tuple[int, ...]:
        return rc.renabled_at(s.graph, s.nops, rc.previous(s), s.active)

    def depth_reader(self, s: ct.State) -> tuple[int, ...]:
        return dp.r2enabled_at(s.graph, s.nops, dp.before(s), rc.previous(s), s.active)

    def test_the_record_machine_is_the_generic_one_at_its_reader(self) -> None:
        """Over every deterministic depth-one program on the two-point
        setting: 81 programs, both starts, seven steps each."""
        for choice in dp.deterministic_choices(2, TWO.n, len(TWO.ops)):
            C = rc.Recorded(TWO, frozenset((key[0], key[1], k) for key, k in choice.items()))
            for start in range(TWO.n):
                s = rc.rinit(C, start, 6)
                for _ in range(7):
                    mine = rc.rstep_det(s)
                    self.assertEqual(mine, rn.step_det_of(self.record_reader, s), (choice, start))
                    if isinstance(mine, ct.Terminal):
                        break
                    s = mine

    def test_the_depth_two_machine_is_the_generic_one_at_its_reader(self) -> None:
        for choice in dp.deterministic_choices(3, 2, 2):
            F = TWO
            C = dp.Recorded2(F, frozenset((key[0], key[1], key[2], k) for key, k in choice.items()))
            for start in range(F.n):
                s = dp.r2init(C, start, 6)
                for _ in range(7):
                    mine = dp.r2step_det(s)
                    self.assertEqual(mine, rn.step_det_of(self.depth_reader, s), (choice, start))
                    if isinstance(mine, ct.Terminal):
                        break
                    s = mine

    def test_both_observations_are_the_generic_one(self) -> None:
        for choice in dp.deterministic_choices(2, TWO.n, len(TWO.ops)):
            C = rc.Recorded(TWO, frozenset((key[0], key[1], k) for key, k in choice.items()))
            for start in range(TWO.n):
                s = rc.rinit(C, start, 6)
                for scale in range(7):
                    self.assertEqual(rc.robs(scale, s),
                                     rn.obs_of(self.record_reader, scale, s), (choice, start, scale))


if __name__ == "__main__":
    unittest.main()
