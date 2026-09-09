"""The selection experiment: the protocol declared before the readout, the
survivors by replay, the burden, the residual and its reason, the exhibited
ambiguity and the exhibited discrimination."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys
from typing import cast
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1] / "code"))
sys.path.insert(0, str(ROOT.parent / "setting_translation"))
sys.path.insert(0, str(ROOT.parent / "represented_execution"))
sys.path.insert(0, str(ROOT.parent / "coherent_process_limits"))
sys.path.insert(0, str(ROOT))

import control as ct  # noqa: E402
import limits as lm  # noqa: E402
import record as rc  # noqa: E402
import selection as sel  # noqa: E402
import translation as tr  # noqa: E402


class Setting(unittest.TestCase):
    F: tr.FiniteSetting
    forever: ct.Controlled
    observation: sel.Word

    @classmethod
    def setUpClass(cls) -> None:
        artifact = lm.load_artifact()
        programs, _ = lm.identify_programs(artifact)
        cls.forever = programs["forever"]
        cls.F = cls.forever.F
        runs = artifact["control_runs"]
        assert isinstance(runs, list)
        recorded = tuple(int(v) for v in next(r for r in runs if r["program"] == "forever")["tape"])
        cls.observation = recorded[: sel.OBSERVED_SCALE + 1]


class Protocol(Setting):
    def test_the_protocol_is_declared_as_constants(self) -> None:
        self.assertEqual(sel.STARTS, (0, 1, 2))
        self.assertEqual(sel.SCALES, tuple(range(1, 9)))
        self.assertEqual(len(sel.INPUTS), 24)
        self.assertEqual((sel.OBSERVED_START, sel.OBSERVED_SCALE), (0, 3))
        self.assertEqual(self.observation, (0, 1, 2, 0))

    def test_the_seen_observation_is_the_declared_readout_of_the_recorded_program(self) -> None:
        self.assertEqual(sel.observe(self.forever, sel.OBSERVED_START, sel.OBSERVED_SCALE), self.observation)

    def test_the_survivor_rule_reads_the_protocol_at_call_time(self) -> None:
        """The start and scale are not frozen as default arguments: a
        protocol change moves both halves together."""
        from unittest.mock import patch  # noqa: PLC0415
        laws: list[sel.Law] = [self.forever]
        with patch("selection.OBSERVED_SCALE", 4):
            self.assertEqual(sel.survivors(laws, (0, 1, 2, 0)), [])
            self.assertEqual(sel.survivors(laws, (0, 1, 2, 0, 1)), [self.forever])
        self.assertEqual(sel.survivors(laws, (0, 1, 2, 0)), [self.forever])

    def test_survivors_are_retained_by_replay_only(self) -> None:
        laws: list[sel.Law] = [self.forever, ct.Controlled(self.F, frozenset({(0, 1)})), rc.turncoat(self.F),
                               rc.twist(self.F)]
        kept = sel.survivors(laws, self.observation)
        self.assertEqual(len(kept), 2)
        self.assertTrue(all(sel.observe(law, 0, 3) == self.observation for law in kept))
        self.assertEqual(sel.survivors(laws, (0, 1, 0, 0)), [rc.twist(self.F)])

    def test_the_finest_scale_carries_every_coarser_one(self) -> None:
        for law in (self.forever, rc.turncoat(self.F), rc.twist(self.F)):
            for x in sel.STARTS:
                fine = sel.observe(law, x, sel.MAX_SCALE)
                for n in sel.SCALES:
                    coarse = sel.observe(law, x, n)
                    self.assertEqual(coarse, fine[: len(coarse)])

    def test_next_value_is_what_a_step_moves_to(self) -> None:
        for law in (self.forever, rc.turncoat(self.F), rc.twist(self.F)):
            for x in sel.STARTS:
                s = ct.init(law, x, 4) if isinstance(law, ct.Controlled) else rc.rinit(law, x, 4)
                for _ in range(4):
                    p = rc.previous(s)
                    value = sel.next_value(law, p, s.active)
                    nxt = lm.next_state(s) if isinstance(law, ct.Controlled) else rc.rnext(s)
                    if value is None:
                        self.assertEqual(nxt.tape, s.tape)
                    else:
                        self.assertEqual(nxt.active, value)
                    s = nxt


class Memoryless(Setting):
    def test_eight_survive_one_residual_class_no_further_input_helps(self) -> None:
        kept = sel.survivors(sel.memoryless_class(self.F), self.observation)
        self.assertEqual(len(kept), 8)
        sequence, residual = sel.burden(kept)
        self.assertEqual(sequence, [])
        self.assertEqual(residual, 1)
        reason = sel.residual_reason(kept, witness=self.forever)
        self.assertTrue(reason["within_a_class_the_next_value_function_agrees_on_reached_pairs"])
        # One class: there is no pair of classes to differ on, so the claim is
        # not made rather than reported vacuously true.
        self.assertEqual(reason["class_pairs_compared"], 0)
        self.assertIsNone(reason["between_classes_it_differs_on_a_reached_pair"])
        self.assertEqual(reason["class_of_the_law_that_produced_the_observation"], 8)

    def test_the_between_class_check_is_made_where_there_are_two_classes(self) -> None:
        """The same check on a population with two residual classes: it is a
        claim there, and it holds."""
        kept: list[sel.Law] = [self.forever, ct.Controlled(self.F, frozenset({(0, 0), (1, 1)}))]
        reason = sel.residual_reason(kept)
        self.assertEqual(reason["class_pairs_compared"], 1)
        self.assertTrue(reason["between_classes_it_differs_on_a_reached_pair"])

    def test_forever_and_climb_first_differ_and_are_not_separated(self) -> None:
        climb_first = ct.Controlled(self.F, frozenset({(0, 2), (1, 0), (2, 0)}))
        self.assertNotEqual(ct.program(self.forever), ct.program(climb_first))
        self.assertEqual(sel.signature(self.forever), sel.signature(climb_first))
        for x in range(3):
            self.assertEqual(sel.next_value(self.forever, x, x), sel.next_value(climb_first, x, x))


class Record(Setting):
    def test_turncoat_agrees_at_the_seen_observation_and_is_separated(self) -> None:
        turncoat, lifted = rc.turncoat(self.F), rc.lift(self.forever)
        self.assertEqual(sel.observe(turncoat, 0, 3), sel.observe(lifted, 0, 3))
        self.assertNotEqual(sel.observe(turncoat, 0, 4), sel.observe(lifted, 0, 4))
        self.assertNotEqual(sel.observe(turncoat, 2, 2), sel.observe(lifted, 2, 2))
        self.assertEqual(sel.observe(turncoat, 0, 4), (0, 1, 2, 0, 0))
        self.assertEqual(sel.observe(lifted, 0, 4), (0, 1, 2, 0, 1))

    def test_the_greedy_burden_refines_and_stops(self) -> None:
        laws: list[sel.Law] = [rc.turncoat(self.F), rc.lift(self.forever), rc.twist(self.F)]
        sequence, residual = sel.burden(laws)
        self.assertEqual(residual, 3)
        self.assertEqual(len(sequence), 1)
        self.assertEqual(sequence[0]["classes_after"], 3)

    def test_the_record_class_has_the_declared_size(self) -> None:
        laws = sel.record_class(self.F)
        self.assertEqual(len(laws), 4 ** 9)
        self.assertIn(rc.turncoat(self.F), laws)
        self.assertIn(rc.twist(self.F), laws)
        self.assertIn(rc.lift(self.forever), laws)


class Refusals(Setting):
    def test_a_seen_observation_of_the_wrong_scale_is_refused(self) -> None:
        with self.assertRaisesRegex(sel.SelectError, "scale"):
            sel.experiment(self.F, (0, 1, 2), self.forever)
class TheMinimumBurdenAndTheSecondReadout(unittest.TestCase):
    """W42 and W39: the minimum against the greedy sequence, and the readout
    that reports which operation fired."""

    F: tr.FiniteSetting
    forever: ct.Controlled
    observation: sel.Word
    kept: list[sel.Law]
    sigs: list[sel.Signature]
    memo: list[sel.Law]
    memo_sigs: list[sel.Signature]

    @classmethod
    def setUpClass(cls) -> None:
        programs, _ = lm.identify_programs(lm.load_artifact())
        cls.forever = programs["forever"]
        cls.F = cls.forever.F
        cls.observation = sel.observe(cls.forever, sel.OBSERVED_START, sel.OBSERVED_SCALE)
        cls.kept = sel.survivors(sel.record_class(cls.F), cls.observation)
        cls.sigs = sel.signatures(cls.kept)
        cls.memo = sel.survivors(sel.memoryless_class(cls.F), cls.observation)
        cls.memo_sigs = sel.signatures(cls.memo)

    def test_the_minimum_is_reached_and_is_a_minimum(self) -> None:
        result = sel.minimum_burden(self.sigs)
        least = [(int(entry["start"]), int(entry["scale"]))
                 for entry in cast(list[dict[str, int]], result["a_least_set"])]
        target = len(sel.partition(self.sigs, list(sel.INPUTS)))
        self.assertEqual(len(sel.partition(self.sigs, least)), target)
        for size in range(len(least)):
            for subset in combinations(sel.INPUTS, size):
                self.assertNotEqual(len(sel.partition(self.sigs, list(subset))), target, subset)

    def test_the_greedy_sequence_is_no_shorter_than_the_minimum(self) -> None:
        greedy, _ = sel.burden(self.kept, self.sigs)
        self.assertGreaterEqual(len(greedy), cast(int, sel.minimum_burden(self.sigs)["least"]))

    def test_no_single_start_separates_the_record_class(self) -> None:
        single = cast(dict[str, dict[str, object]], sel.minimum_burden(self.sigs)["a_single_start"])
        for start in sel.STARTS:
            self.assertFalse(single[str(start)]["suffices"], start)

    def test_the_refined_partition_is_the_partition_by_annotated_runs(self) -> None:
        """The refinement is computed from the fired index at reached pairs;
        this checks it against partitioning by the annotated runs themselves,
        on the class small enough to do both."""
        direct: dict[object, list[int]] = {}
        for index, law in enumerate(self.memo):
            key = tuple(sel.annotated_run(law, start, scale) for start, scale in sel.INPUTS)
            direct.setdefault(key, []).append(index)
        refined = sel.annotated_partition(self.memo, self.memo_sigs)
        self.assertEqual(sorted(sorted(m) for m in direct.values()),
                         sorted(sorted(m) for m in refined.values()))

    def test_the_second_readout_refines_the_first_and_leaves_only_unreached_pairs(self) -> None:
        result = sel.second_readout(self.kept, self.sigs)
        self.assertGreater(cast(int, result["residual_classes_under_both"]),
                           cast(int, result["residual_classes_under_the_first_readout"]))
        self.assertLess(cast(int, result["largest_class_under_both"]),
                        cast(int, result["largest_class_under_the_first_readout"]))
        self.assertTrue(result["within_a_class_the_enablement_agrees_on_every_reached_pair"])

    def test_the_annotated_run_reports_an_index_for_every_entry_but_the_first(self) -> None:
        for law in (self.forever, rc.turncoat(self.F)):
            for start in sel.STARTS:
                plain = sel.observe(law, start, 4)
                annotated = sel.annotated_run(law, start, 4)
                self.assertEqual([datum for datum, _ in annotated], list(plain), start)
                self.assertEqual(annotated[0][1], len(self.F.ops), start)
                for _, index in annotated[1:]:
                    self.assertLess(index, len(self.F.ops), start)

    def test_a_refinement_that_is_not_one_is_refused(self) -> None:
        """The refusal is the receipt's, not a comment.  Reporting the plain
        partition as if the second readout had refined it would claim a
        collapse that did not happen; the check fires because a plain class
        holds laws whose fired index differs at a pair the runs reach --
        which is the ambiguity CL-RR-09 exhibits."""
        from unittest.mock import patch  # noqa: PLC0415
        with patch("selection.annotated_partition",
                   side_effect=lambda laws, sigs: sel.partition(sigs, list(sel.INPUTS))):
            with self.assertRaisesRegex(sel.SelectError, "disagrees on a reached pair"):
                sel.second_readout(self.kept, self.sigs)


if __name__ == "__main__":
    unittest.main()
