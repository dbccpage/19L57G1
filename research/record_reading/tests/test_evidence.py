"""The committed record replays byte for byte; a mutated record is refused,
by the byte comparison and by the receipt's semantic refusals."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
from typing import Any
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1] / "code"))
sys.path.insert(0, str(ROOT.parent / "setting_translation"))
sys.path.insert(0, str(ROOT.parent / "represented_execution"))
sys.path.insert(0, str(ROOT.parent / "coherent_process_limits"))
sys.path.insert(0, str(ROOT))
from execution import ExecutionError  # noqa: E402
import run  # noqa: E402
import selection as sel  # noqa: E402


class RecordFile(unittest.TestCase):
    fresh: bytes

    @classmethod
    def setUpClass(cls) -> None:
        cls.fresh = run.receipt_bytes()

    def record(self) -> dict[str, Any]:
        loaded: dict[str, Any] = json.loads(self.fresh.decode("utf-8"))
        return loaded

    def test_committed_record_replays_byte_for_byte(self) -> None:
        self.assertTrue(run.RECEIPT.is_file(), "run `python run.py --write` first")
        self.assertEqual(run.RECEIPT.read_bytes(), self.fresh)

    def test_the_check_command_refuses_a_changed_figure(self) -> None:
        record = self.record()
        record["selection"]["classes"]["record"]["survivors"] += 1
        mutated = (json.dumps(record, sort_keys=True, indent=1) + "\n").encode("utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            receipt = Path(tmp) / "record.json"
            with patch("run.receipt_bytes", return_value=self.fresh), patch("run.RECEIPT", receipt):
                receipt.write_bytes(mutated)
                self.assertEqual(run.main(["--check"]), 1)
                receipt.write_bytes(self.fresh)
                self.assertEqual(run.main(["--check"]), 0)

    def test_the_receipt_refuses_a_setting_that_is_not_the_transcribed_base(self) -> None:
        with patch("run.verify_sources", return_value=[]), \
                patch("record.check_base", side_effect=ExecutionError("not the transcribed base")):
            with self.assertRaisesRegex(ExecutionError, "transcribed base"):
                run.receipt_bytes()

    def test_the_receipt_refuses_a_transition_that_is_not_a_reference_step(self) -> None:
        with patch("run.verify_sources", return_value=[]), patch("record.rstep", return_value=False):
            with self.assertRaisesRegex(RuntimeError, "not a reference step"):
                run.receipt_bytes()

    def test_the_receipt_refuses_a_class_with_no_survivor(self) -> None:
        with patch("run.verify_sources", return_value=[]), patch("selection.survivors", return_value=[]):
            with self.assertRaisesRegex(sel.SelectError, "replays"):
                run.receipt_bytes()

    def test_every_recorded_run_replays_from_its_own_record(self) -> None:
        """The house check the producer family carries: rebuild each recorded
        run from the record's own fields — the index-ordered tables with the
        recorded enablements, start and fuel — and compare the recorded
        outcome.  The sealed `setting_json` is set-valued and does not
        determine the program on its own."""
        import record as rc  # noqa: PLC0415
        import translation as tr  # noqa: PLC0415
        record = self.record()
        for entry in record["record_runs"]:
            sealed = entry["setting_json"]
            pairs = {key: frozenset((int(q[0]), int(q[1])) for q in sealed[key])
                     for key in ("r", "ret", "prot")}
            tables = tuple(tuple(int(v) for v in t) for t in entry["ops_in_index_order"])
            self.assertEqual(sorted(list(t) for t in set(tables)), sealed["ops"])
            F = tr.FiniteSetting(int(sealed["n"]), pairs["r"], pairs["ret"], pairs["prot"],
                                 int(sealed["a"]), int(sealed["b"]), tables)
            C = rc.Recorded(F, frozenset((int(t[0]), int(t[1]), int(t[2]))
                                         for t in entry["enablements"]))
            terminal, state = rc.rtrace(C, int(entry["start"]), int(entry["fuel"]))
            self.assertEqual(list(state.tape), entry["tape"], entry["program"])
            self.assertEqual(terminal.value, entry["terminal"], entry["program"])
            self.assertEqual(state.clock, entry["clock"], entry["program"])
            self.assertEqual(state.fuel, entry["fuel_left"], entry["program"])
            self.assertEqual(rc.previous(state), entry["previous_at_end"], entry["program"])

    def test_the_minimum_burden_and_the_second_readout_the_record_reports(self) -> None:
        classes = self.record()["selection"]["classes"]
        for name in ("memoryless", "record"):
            minimum = classes[name]["minimum_burden"]
            self.assertLessEqual(minimum["least"], classes[name]["burden"])
            self.assertEqual(len(minimum["a_least_set"]), minimum["least"])
            second = classes[name]["second_readout"]
            self.assertTrue(second["refines_the_first"])
            self.assertTrue(second["within_a_class_the_enablement_agrees_on_every_reached_pair"])
            self.assertIn("HOST READOUT", second["status"])
        record_class = classes["record"]
        self.assertEqual(record_class["minimum_burden"]["least"], 3)
        self.assertEqual(record_class["second_readout"]["residual_classes_under_the_first_readout"], 45)
        self.assertEqual(record_class["second_readout"]["residual_classes_under_both"], 896)
        self.assertEqual(record_class["second_readout"]["largest_class_under_both"], 64)
        for start in ("0", "1", "2"):
            self.assertFalse(record_class["minimum_burden"]["a_single_start"][start]["suffices"])

    def test_record_carries_no_timestamp_path_or_sentinel(self) -> None:
        text = self.fresh.decode("utf-8")
        for token in ("timestamp", "C:\\\\", "/Users/", "worktrees"):
            self.assertNotIn(token, text)

    def test_the_figures_the_readme_quotes(self) -> None:
        record = self.record()
        self.assertFalse(record["artifact"]["written_here"])
        runs = record["record_runs"]
        self.assertEqual([r["program"] for r in runs][:2], ["twist", "twist"])
        self.assertEqual(runs[0]["tape"], [0, 1, 0, 0])
        self.assertEqual(runs[1]["tape"], [0, 1, 0, 0, 1, 0, 0])
        self.assertEqual(runs[0]["ops_in_index_order"], [[1, 2, 0], [0, 0, 0], [1, 2, 2]])
        self.assertEqual(record["record_is_read"]["actives_by_step"], [0, 1, 0, 0])
        self.assertFalse(record["record_is_read"]["memoryless_class_checked"]["tape_0_1_0_0_realized"])
        self.assertEqual(record["forget"]["tape"], [0, 1])
        self.assertTrue(record["forget"]["distinction_disappears"])
        self.assertTrue(record["lift"]["agrees_with_forever_at_every_declared_input"])
        selection = record["selection"]
        self.assertEqual(selection["observation"], [0, 1, 2, 0])
        memoryless = selection["classes"]["memoryless"]
        self.assertEqual((memoryless["class_size"], memoryless["survivors"], memoryless["burden"]), (64, 8, 0))
        self.assertEqual(memoryless["residual"]["residual_classes"], 1)
        rec = selection["classes"]["record"]
        self.assertEqual((rec["class_size"], rec["survivors"], rec["burden"]), (262144, 32768, 3))
        self.assertEqual([(e["start"], e["scale"], e["classes_after"]) for e in rec["experiments"]],
                         [(1, 6, 11), (2, 2, 37), (0, 4, 45)])
        self.assertEqual(rec["residual"]["residual_classes"], 45)
        self.assertEqual(rec["residual"]["largest_class"], 4096)
        for name in ("memoryless", "record"):
            residual = selection["classes"][name]["residual"]
            self.assertTrue(residual["within_a_class_the_next_value_function_agrees_on_reached_pairs"])
            self.assertFalse(selection["classes"][name]["separated_into_singletons"])
            self.assertFalse(selection["classes"][name]["one_survivor"])
        # One residual class in the memoryless population: no pair of classes
        # to differ on, so the between-class claim is not made there.
        self.assertEqual(memoryless["residual"]["class_pairs_compared"], 0)
        self.assertIsNone(memoryless["residual"]["between_classes_it_differs_on_a_reached_pair"])
        self.assertEqual(memoryless["residual"]["class_of_the_law_that_produced_the_observation"], 8)
        self.assertEqual(rec["residual"]["class_pairs_compared"], 990)
        self.assertTrue(rec["residual"]["between_classes_it_differs_on_a_reached_pair"])
        # The law that produced the seen observation is in the largest class:
        # the record class identifies it least of all.
        self.assertEqual(rec["residual"]["class_of_the_law_that_produced_the_observation"], 4096)
        self.assertTrue(selection["ambiguity_exhibited"]["programs_differ"])
        self.assertFalse(selection["ambiguity_exhibited"]["separated_by_a_declared_input"])
        self.assertTrue(selection["discrimination_exhibited"]["agree_at_the_seen_observation"])
        self.assertEqual(selection["discrimination_exhibited"]["separated_by_scale"]["readouts"],
                         [[0, 1, 2, 0, 0], [0, 1, 2, 0, 1]])
        self.assertEqual(selection["discrimination_exhibited"]["separated_by_start"]["readouts"],
                         [[2, 0, 0], [2, 0, 1]])


if __name__ == "__main__":
    unittest.main()
