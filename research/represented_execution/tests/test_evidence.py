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

    def test_record_carries_no_timestamp_path_or_sentinel(self) -> None:
        text = self.fresh.decode("utf-8")
        for token in ("timestamp", "C:\\\\", "/Users/", "worktrees", "-1"):
            self.assertNotIn(token, text)

    def test_the_record_names_the_fragment_and_the_machine(self) -> None:
        record = self.record()
        self.assertEqual(record["fragment"], "words")
        self.assertEqual(record["config_status"], "DECLARED_HOST_CONFIG")
        self.assertEqual(record["step"], "Execution.step")
        self.assertEqual(record["run"], "Execution.run")
        self.assertEqual(record["correspondence"], "Execution.run_encode")
        self.assertEqual(len(record["runs"]), len(run.RUNS))
        for entry in record["runs"]:
            self.assertEqual(entry["active"], entry["reference_active"])
            self.assertEqual(len(entry["output"]), len(entry["word"]))
        self.assertIn("control", record["not_delivered"])


if __name__ == "__main__":
    unittest.main()
