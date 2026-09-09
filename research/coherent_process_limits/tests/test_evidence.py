"""The committed limits record replays byte for byte; a mutated record is
refused, by the byte comparison and by the receipt's semantic refusals."""

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
sys.path.insert(0, str(ROOT))
import limits as lm  # noqa: E402
import run  # noqa: E402


class LimitsRecord(unittest.TestCase):
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
        record["connected_experiment"]["scales"][0]["count_zero"] += 1
        mutated = (json.dumps(record, sort_keys=True, indent=1) + "\n").encode("utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            receipt = Path(tmp) / "limits.json"
            with patch("run.receipt_bytes", return_value=self.fresh), patch("run.RECEIPT", receipt):
                receipt.write_bytes(mutated)
                self.assertEqual(run.main(["--check"]), 1)
                receipt.write_bytes(self.fresh)
                self.assertEqual(run.main(["--check"]), 0)

    def test_the_receipt_refuses_a_failing_bound(self) -> None:
        with patch("run.verify_sources", return_value=[]), patch("limits.bound_holds", return_value=False):
            with self.assertRaisesRegex(lm.LimitsError, "bound"):
                run.receipt_bytes()

    def test_the_receipt_refuses_incompatible_observations(self) -> None:
        with patch("run.verify_sources", return_value=[]), patch("limits.is_prefix", return_value=False):
            with self.assertRaisesRegex(lm.LimitsError, "prefix"):
                run.receipt_bytes()

    def test_the_receipt_refuses_a_foreign_fragment(self) -> None:
        artifact = lm.load_artifact()
        artifact["fragment"] = "words"
        with patch("run.verify_sources", return_value=[]), \
                patch("limits.load_artifact", side_effect=lm.LimitsError("the artifact's fragment is 'words'")):
            with self.assertRaisesRegex(lm.LimitsError, "fragment"):
                run.receipt_bytes()

    def test_record_carries_no_timestamp_path_or_sentinel(self) -> None:
        text = self.fresh.decode("utf-8")
        for token in ("timestamp", "C:\\\\", "/Users/", "worktrees"):
            self.assertNotIn(token, text)

    def test_the_figures_the_readme_quotes(self) -> None:
        record = self.record()
        self.assertEqual(record["artifact"]["fragment"], "control")
        self.assertFalse(record["artifact"]["written_here"])
        finding = record["artifact"]["finding_for_the_represented_execution_family"]
        self.assertIn("collapses repetitions", finding["sealed_schema_is_set_valued"])
        self.assertIn("ops_in_index_order", finding["order_read_from"])
        self.assertIsNone(finding["recovered_order_of_sorted_tables"])
        self.assertEqual(finding["identified_from_recorded_runs"], 8)
        scales = record["connected_experiment"]["scales"]
        self.assertEqual([e["scale"] for e in scales], [3, 6, 12, 24])
        self.assertEqual([e["tape_length"] for e in scales], [4, 7, 13, 25])
        self.assertEqual([e["count_zero"] for e in scales], [2, 3, 5, 9])
        self.assertTrue(all(e["bound_holds"] and e["prefix_of_next"] and e["recorded_tape_prefix_related"]
                            for e in scales))
        # The recorded tape (fuel 5, six entries) is a prefix of every scale
        # at least as fine, and an extension of the coarsest one.
        self.assertEqual([e["recorded_tape_is_a_prefix_of_this_one"] for e in scales],
                         [False, True, True, True])
        self.assertEqual(record["connected_experiment"]["fuel"], 24)
        self.assertIn("one state", record["connected_experiment"]["observed_from"])
        self.assertEqual(record["connected_experiment"]["derived_from"], [0, 1, 2, 0])
        verdicts = record["verdicts"]
        self.assertEqual(verdicts["programs"], 64)
        self.assertTrue(verdicts["all_realized_tapes_functional"])
        self.assertTrue(verdicts["witness_has_no_realized_extension"])
        self.assertFalse(verdicts["surjective"])
        self.assertEqual(record["lost_fuel"]["after_one_step_fuel_0"], [0])
        self.assertEqual(record["lost_fuel"]["after_one_step_fuel_1"], [0, 1])
        self.assertEqual(record["shift"]["shifted"], [[1, 2], [1, 0]])


if __name__ == "__main__":
    unittest.main()
