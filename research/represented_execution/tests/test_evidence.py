"""The committed process record replays byte for byte; a mutated record is
refused, by the byte comparison and by the receipt's semantic refusals."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
from typing import Any
import unittest
from unittest.mock import patch

# Dependencies first, this tree last, so this tree wins name collisions with
# the merged sibling (``run``, ``verify_sources``).
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "setting_translation"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import control as ct  # noqa: E402
import execution as ex  # noqa: E402
import run  # noqa: E402


class ProcessRecord(unittest.TestCase):
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
        record["runs"][0]["active"] += 1
        mutated = (json.dumps(record, sort_keys=True, indent=1) + "\n").encode("utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            receipt = Path(tmp) / "process.json"
            with patch("run.receipt_bytes", return_value=self.fresh), patch("run.RECEIPT", receipt):
                receipt.write_bytes(mutated)
                self.assertEqual(run.main(["--check"]), 1)
                receipt.write_bytes(self.fresh)
                self.assertEqual(run.main(["--check"]), 0)

    def test_the_receipt_refuses_a_machine_that_disagrees_with_the_operations(self) -> None:
        name, F, word, start = run.RUNS[0]
        good = ex.run(ex.init(F, word, start))
        assert good is not None
        wrong = ex.Config(good.graph, (), (good.active + 1) % F.n, good.output)
        with patch("run.verify_sources", return_value=[]), patch("execution.run", return_value=wrong):
            with self.assertRaisesRegex(RuntimeError, "is not the operations'"):
                run.receipt_bytes()

    def test_the_receipt_refuses_an_unconsumed_word(self) -> None:
        name, F, word, start = run.RUNS[0]
        good = ex.run(ex.init(F, word, start))
        assert good is not None
        stuck = ex.Config(good.graph, (0,), good.active, good.output)
        with patch("run.verify_sources", return_value=[]), patch("execution.run", return_value=stuck):
            with self.assertRaisesRegex(RuntimeError, "not consumed"):
                run.receipt_bytes()

    def test_the_receipt_refuses_a_refusal(self) -> None:
        with patch("run.verify_sources", return_value=[]), patch("execution.run", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "refused a well-formed word"):
                run.receipt_bytes()

    def test_the_receipt_refuses_a_transition_that_is_not_a_reference_step(self) -> None:
        terminal, good = ct.trace(run.PING, 0, 4)
        # 0 -> 2 is no step of PING: the cycle enabled at 0 moves to 1.
        bad = ct.State(good.graph, good.nops, good.active, (0, 2, 0, 1, 0), good.clock, good.fuel)
        with patch("run.verify_sources", return_value=[]), patch("control.trace", return_value=(terminal, bad)):
            with self.assertRaisesRegex(RuntimeError, "not a reference step"):
                run.receipt_bytes()

    def test_the_receipt_refuses_a_clock_that_does_not_count_the_firings(self) -> None:
        terminal, good = ct.trace(run.PING, 0, 4)
        miscounted = ct.State(good.graph, good.nops, good.active, good.tape, good.clock + 1, good.fuel)
        with patch("run.verify_sources", return_value=[]), patch("control.trace", return_value=(terminal, miscounted)):
            with self.assertRaisesRegex(RuntimeError, "clock does not count"):
                run.receipt_bytes()

    def test_the_receipt_refuses_a_two_locus_step_that_moves_both_loci(self) -> None:
        """The exchange `(3, 2, 1, 0)` sends `(0, 0)` to `(1, 1)`: one step,
        both loci.  It is not an operation of any product setting, which is
        exactly what the refusal is for."""
        import product as pr  # noqa: PLC0415
        import translation as tr  # noqa: PLC0415
        coupled = tr.FiniteSetting(4, tr.NONE, tr.NONE, tr.NONE, 0, 3, ((3, 2, 1, 0),))
        with patch("run.verify_sources", return_value=[]),                 patch("run.PAIR", pr.scheduled(coupled, lambda _: 0)):
            with self.assertRaisesRegex(RuntimeError, "moved both loci"):
                run.receipt_bytes()

    def test_the_receipt_refuses_a_schedule_the_runner_had_to_choose_in(self) -> None:
        """Two operations enabled at one datum is a host choice by another
        name; the runner refuses it and so does the receipt."""
        import translation as tr  # noqa: PLC0415
        both = tr.FiniteSetting(4, tr.NONE, tr.NONE, tr.NONE, 0, 3,
                                ((1, 0, 3, 2), (2, 3, 0, 1)))
        with patch("run.verify_sources", return_value=[]),                 patch("run.PAIR", ct.Controlled(both, frozenset({(0, 0), (0, 1)}))):
            with self.assertRaisesRegex(RuntimeError, "left a choice"):
                run.receipt_bytes()

    def test_every_recorded_run_replays_from_its_own_record(self) -> None:
        """CL-RE-06's falsifier, mechanically: rebuild each run from the
        record alone — the index-ordered tables with the recorded word or
        enablements, start and fuel — and compare the recorded outcome.  The
        sealed ``setting_json`` is set-valued and does not determine it."""
        import translation as tr  # noqa: PLC0415
        record = self.record()

        def setting(entry: dict[str, Any]) -> tr.FiniteSetting:
            sealed_json = entry["setting_json"]
            pairs = {key: frozenset((int(p[0]), int(p[1])) for p in sealed_json[key])
                     for key in ("r", "ret", "prot")}
            tables = tuple(tuple(int(v) for v in table) for table in entry["ops_in_index_order"])
            self.assertEqual(sorted(list(t) for t in set(tables)), sealed_json["ops"])
            return tr.FiniteSetting(int(sealed_json["n"]), pairs["r"], pairs["ret"], pairs["prot"],
                                    int(sealed_json["a"]), int(sealed_json["b"]), tables)

        for entry in record["runs"]:
            c = ex.run(ex.init(setting(entry), tuple(entry["word"]), int(entry["start"])))
            assert c is not None
            self.assertEqual(c.active, entry["active"], entry["setting"])
            self.assertEqual(list(c.output), entry["output"], entry["setting"])
        for entry in record["control_runs"]:
            C = ct.Controlled(setting(entry),
                              frozenset((int(p[0]), int(p[1])) for p in entry["enablements"]))
            terminal, s = ct.trace(C, int(entry["start"]), int(entry["fuel"]))
            self.assertEqual(list(s.tape), entry["tape"], entry["program"])
            self.assertEqual(terminal.value, entry["terminal"], entry["program"])

    def test_record_carries_no_timestamp_path_or_sentinel(self) -> None:
        text = self.fresh.decode("utf-8")
        for token in ("timestamp", "C:\\\\", "/Users/", "worktrees", "-1"):
            self.assertNotIn(token, text)

    def test_the_record_names_the_fragment_and_the_machines(self) -> None:
        record = self.record()
        self.assertEqual(record["fragment"], "control")
        self.assertEqual(record["config_status"], "DECLARED_HOST_CONFIG")
        self.assertEqual(record["words"]["step"], "Execution.step")
        self.assertEqual(record["words"]["run"], "Execution.run")
        self.assertEqual(record["words"]["correspondence"], "Execution.run_encode")
        self.assertEqual(record["control"]["step"], "Control.stepDet")
        self.assertEqual(record["control"]["soundness"], "Control.successors_sound")
        self.assertEqual(record["control"]["completeness"], "Control.successors_complete")
        self.assertEqual(record["control"]["terminals"], ["halt", "exhausted", "refuse", "branch"])
        self.assertEqual(len(record["runs"]), len(run.RUNS))
        for entry in record["runs"]:
            self.assertEqual(entry["active"], entry["reference_active"])
            self.assertEqual(len(entry["output"]), len(entry["word"]))
        self.assertEqual(len(record["control_runs"]), len(run.CONTROL_RUNS))
        for entry in record["control_runs"]:
            self.assertEqual(entry["clock"], len(entry["tape"]) - 1)
            self.assertEqual(entry["clock"] + entry["fuel_left"], entry["fuel"])
        self.assertEqual(record["branching_example"]["tapes_by_start"],
                         {"0": [0, 1, 0, 1, 0], "1": [1, 0, 1, 0, 1], "2": [2]})
        self.assertEqual(record["iteration_example"]["firings_by_start"], {"0": 2, "1": 1, "2": 0})
        self.assertEqual(record["iteration_example"]["terminals_by_start"],
                         {"0": "halt", "1": "halt", "2": "halt"})
        by_program = {(e["program"], e["start"]): e for e in record["control_runs"]}
        self.assertEqual(by_program[("forever", 0)]["terminal"], "exhausted")
        self.assertEqual(by_program[("forever", 0)]["clock"], 5)
        self.assertEqual(by_program[("fork", 0)]["terminal"], "branch")
        self.assertEqual(by_program[("fork", 0)]["successors_at_end"], [0, 1])
        self.assertTrue(any("retained record" in item for item in record["not_delivered"]))
        two = record["two_loci"]
        self.assertEqual(two["alternating_run"]["tape"], [0, 2, 3, 1, 0])
        self.assertEqual(two["mirror_run"]["tape"], [0, 1, 3, 2, 0])
        self.assertTrue(two["one_locus_at_a_time"]["holds"])
        self.assertTrue(two["square"]["on_the_outcome"]["agree"])
        self.assertFalse(two["square"]["on_the_observation"]["agree"])
        self.assertEqual(two["projections"]["destuttered"]["first_locus"],
                         two["projections"]["one_locus_run"])
        self.assertEqual(two["projections"]["destuttered"]["second_locus"],
                         two["projections"]["one_locus_run"])
        self.assertNotEqual(two["projections"]["first_locus"],
                            two["projections"]["second_locus"])


if __name__ == "__main__":
    unittest.main()
