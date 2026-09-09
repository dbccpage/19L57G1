"""The abstract inverse system, the represented process at step scales, the
artifact consumed, the connected experiment, the three verdicts and the
failures."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import cast
import unittest

# Dependencies first, this tree last, so this tree wins name collisions with
# the sibling families (``run``, ``verify_sources``).
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1] / "code"))
sys.path.insert(0, str(ROOT.parent / "setting_translation"))
sys.path.insert(0, str(ROOT.parent / "represented_execution"))
sys.path.insert(0, str(ROOT))

import control as ct  # noqa: E402
import limits as lm  # noqa: E402


class AbstractSystem(unittest.TestCase):
    def test_prefixes_of_a_sequence_are_compatible_and_read_back(self) -> None:
        for seq in (lambda i: i % 3, lambda i: i * i % 2, lambda i: 0):
            family = lm.of_seq(seq, 12)
            self.assertTrue(lm.compatible(family))
            for i in range(11):
                self.assertEqual(lm.to_seq(family, i), seq(i))

    def test_eventual_agreement_is_not_compatibility(self) -> None:
        family = lm.eventual(8)
        self.assertFalse(lm.compatible(family))
        self.assertTrue(lm.eventually_compatible(family, 2))
        self.assertNotEqual(lm.bond(family[2]), family[1])

    def test_the_even_subsystem_reads_back_the_same_sequence(self) -> None:
        family = lm.of_seq(lambda i: (i * 7) % 3, 20)
        even = lm.even_family(family)
        for n in range(len(even) - 1):
            self.assertEqual(even[n + 1][: 2 * n], even[n])
        for i in range(9):
            self.assertEqual(even[i + 1][i], lm.to_seq(family, i))

    def test_shifting_is_not_a_function_of_the_prefix(self) -> None:
        a, b = (0, 1, 2), (0, 1, 0)
        self.assertEqual(a[:2], b[:2])
        self.assertNotEqual(lm.shift_obs(a, 2), lm.shift_obs(b, 2))


class Artifact(unittest.TestCase):
    record: lm.JsonObj
    programs: dict[str, ct.Controlled]

    @classmethod
    def setUpClass(cls) -> None:
        cls.record = lm.load_artifact()
        cls.programs, _ = lm.identify_programs(cls.record)

    def test_the_artifact_is_authored_by_the_represented_execution_family(self) -> None:
        self.assertEqual(lm.ARTIFACT.parent.parent.name, "represented_execution")
        self.assertFalse((ROOT / "evidence" / "process.json").exists())

    def test_the_fragment_is_control(self) -> None:
        self.assertEqual(self.record["fragment"], "control")

    def test_the_programs_are_identified_uniquely_from_the_recorded_runs(self) -> None:
        self.assertEqual(set(self.programs), {"ping", "climb", "forever", "fork"})
        forever = self.programs["forever"]
        self.assertEqual(forever.F.ops[0], (1, 2, 0))
        self.assertEqual(forever.ctrl, frozenset({(0, 0), (1, 0), (2, 0)}))

    def test_the_sorted_schema_alone_would_misidentify(self) -> None:
        runs = self.record["control_runs"]
        assert isinstance(runs, list)
        setting_json = runs[0]["setting_json"]
        sorted_order = lm.setting_from_json(setting_json, range(3))
        self.assertNotEqual(sorted_order.ops[0], (1, 2, 0))

    def test_every_recorded_run_replays(self) -> None:
        runs = self.record["control_runs"]
        assert isinstance(runs, list)
        for r in runs:
            C = self.programs[str(r["program"])]
            terminal, s = ct.trace(C, int(r["start"]), int(r["fuel"]))
            self.assertEqual(list(s.tape), r["tape"], r["program"])
            self.assertEqual(terminal.value, r["terminal"], r["program"])

    def test_an_inconsistent_artifact_is_refused(self) -> None:
        import copy
        record = copy.deepcopy(self.record)
        runs = record["control_runs"]
        assert isinstance(runs, list)
        runs[0]["tape"] = [9, 9]
        with self.assertRaisesRegex(lm.LimitsError, "does not replay"):
            lm.identify_programs(record)

    def test_an_artifact_without_the_order_still_identifies_by_replay(self) -> None:
        """The path for a record written before the producer carried the
        index order: the unique permutation of the sealed tables."""
        import copy
        record = copy.deepcopy(self.record)
        runs = record["control_runs"]
        assert isinstance(runs, list)
        for r in runs:
            del r["ops_in_index_order"]
        programs, finding = lm.identify_programs(record)
        self.assertEqual(programs["forever"].F.ops[0], (1, 2, 0))
        self.assertEqual(finding["recovered_order_of_sorted_tables"], [1, 0, 2])
        self.assertIn("recovered by replay", str(finding["order_read_from"]))

    def test_tables_that_disagree_with_the_sealed_set_are_refused(self) -> None:
        import copy
        record = copy.deepcopy(self.record)
        runs = record["control_runs"]
        assert isinstance(runs, list)
        runs[0]["ops_in_index_order"] = [[0, 0, 0], [0, 0, 0], [1, 2, 2]]
        with self.assertRaisesRegex(lm.LimitsError, "not the sealed schema's set of tables"):
            lm.identify_programs(record)

    def test_runs_that_disagree_on_the_order_are_refused(self) -> None:
        import copy
        record = copy.deepcopy(self.record)
        runs = record["control_runs"]
        assert isinstance(runs, list)
        runs[1]["ops_in_index_order"] = [[0, 0, 0], [1, 2, 0], [1, 2, 2]]
        with self.assertRaisesRegex(lm.LimitsError, "do not share one operation order"):
            lm.identify_programs(record)

    def test_an_enablement_naming_a_collapsed_table_is_refused_by_name(self) -> None:
        """The sealed schema is set-valued: a setting with a repeated table
        is recorded with fewer tables than it has operations.  Without the
        index order, a run naming the missing index must be refused rather
        than replayed on a smaller setting."""
        import copy
        record = copy.deepcopy(self.record)
        runs = record["control_runs"]
        assert isinstance(runs, list)
        entry: dict[str, object] = copy.deepcopy(runs[0])
        record["control_runs"] = [entry]
        del entry["ops_in_index_order"]
        setting = dict(cast(dict[str, object], entry["setting_json"]))
        setting["ops"] = [[0, 0, 0], [1, 2, 0]]
        entry["setting_json"] = setting
        entry["enablements"] = [[0, 2]]
        with self.assertRaisesRegex(lm.LimitsError, "collapses repeated tables"):
            lm.identify_programs(record)

    def test_one_name_with_two_enablement_sets_is_refused(self) -> None:
        import copy
        record = copy.deepcopy(self.record)
        runs = record["control_runs"]
        assert isinstance(runs, list)
        extra = copy.deepcopy(next(r for r in runs if r["program"] == "ping"))
        extra["enablements"] = [[0, 0]]
        extra["start"], extra["fuel"] = 2, 4
        extra["tape"], extra["terminal"], extra["clock"], extra["fuel_left"] = [2], "halt", 0, 4
        extra["successors_at_end"] = []
        record["control_runs"] = [*runs, extra]
        with self.assertRaisesRegex(lm.LimitsError, "two enablement sets"):
            lm.identify_programs(record)

    def test_a_wrong_fragment_is_refused(self) -> None:
        import copy
        import tempfile
        import json
        record = copy.deepcopy(self.record)
        record["fragment"] = "words"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "process.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaisesRegex(lm.LimitsError, "fragment"):
                lm.load_artifact(path)


class Observations(unittest.TestCase):
    programs: dict[str, ct.Controlled]

    @classmethod
    def setUpClass(cls) -> None:
        cls.programs, _ = lm.identify_programs(lm.load_artifact())

    def test_observations_are_compatible_at_every_scale(self) -> None:
        for C in self.programs.values():
            for x in range(C.F.n):
                s = ct.init(C, x, 12)
                for n in range(12):
                    self.assertTrue(lm.is_prefix(lm.obs(n, s), lm.obs(n + 1, s)), (C.ctrl, x, n))

    def test_the_tape_does_not_determine_the_future_the_fuel_is_lost(self) -> None:
        report = lm.lost_fuel(self.programs["forever"])
        self.assertTrue(report["same_tape"])
        self.assertEqual(report["after_one_step_fuel_0"], [0])
        self.assertEqual(report["after_one_step_fuel_1"], [0, 1])

    def test_the_next_datum_is_determined_by_program_and_active(self) -> None:
        C = self.programs["forever"]
        for x in range(3):
            a = ct.step_det(ct.init(C, x, 5))
            b = ct.step_det(ct.State(ct.program(C), ct.nops(C), x, (7, 7, x), 40, 2))
            assert isinstance(a, ct.State) and isinstance(b, ct.State)
            self.assertEqual(a.active, b.active)

    def test_realized_tapes_are_functional_and_the_witness_is_not_realized(self) -> None:
        F = self.programs["forever"].F
        report = lm.verdicts(F, 4)
        self.assertEqual(report["programs"], 64)
        self.assertTrue(report["all_realized_tapes_functional"])
        self.assertTrue(report["witness_has_no_realized_extension"])
        self.assertFalse(lm.functional(lm.NOT_REALIZED))


class ConnectedExperiment(unittest.TestCase):
    def test_the_bound_derived_at_the_coarse_scale_survives_the_fine_scales(self) -> None:
        record = lm.load_artifact()
        programs, _ = lm.identify_programs(record)
        runs = record["control_runs"]
        assert isinstance(runs, list)
        recorded = tuple(int(v) for v in next(r for r in runs if r["program"] == "forever")["tape"])
        report = lm.connected_experiment(programs["forever"], recorded)
        scales = report["scales"]
        assert isinstance(scales, list)
        self.assertEqual([e["scale"] for e in scales], [3, 6, 12, 24])
        for e in scales:
            self.assertTrue(e["bound_holds"])
            self.assertTrue(e["prefix_of_next"])
            self.assertTrue(e["recorded_tape_prefix_related"])
            self.assertIn(e["three_count_minus_length"], (0, 1, 2))
        self.assertEqual(report["derived_from"], [0, 1, 2, 0])

    def test_the_scales_are_observations_of_one_state(self) -> None:
        """The chain of prefixes is an instance of `Observe.obs_prefix_add`
        for one state, not a comparison of runs with different fuel."""
        programs, _ = lm.identify_programs(lm.load_artifact())
        s = ct.init(programs["forever"], 0, lm.SCALES[-1])
        for n in lm.SCALES:
            self.assertTrue(lm.is_prefix(lm.obs(n, s), lm.obs(lm.SCALES[-1], s)))
        self.assertEqual([len(lm.obs(n, s)) for n in lm.SCALES], [4, 7, 13, 25])

    def test_the_bound_is_not_vacuous(self) -> None:
        self.assertTrue(lm.bound_holds((0, 1, 2, 0, 1, 2)))
        self.assertFalse(lm.bound_holds((0, 0, 0, 0)))
        self.assertFalse(lm.bound_holds((1, 2, 1, 2, 1, 2)))


if __name__ == "__main__":
    unittest.main()
