"""The committed census replays byte for byte; a mutated record is refused."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run  # noqa: E402


class CensusRecord(unittest.TestCase):
    fresh: bytes

    @classmethod
    def setUpClass(cls) -> None:
        cls.fresh = run.receipt_bytes()

    def test_committed_record_replays_byte_for_byte(self) -> None:
        self.assertTrue(run.RECEIPT.is_file(), "run `python run.py --write` first")
        self.assertEqual(run.RECEIPT.read_bytes(), self.fresh)

    def test_a_changed_figure_is_detected(self) -> None:
        record = json.loads(self.fresh.decode("utf-8"))
        record["totals"]["rounds"] += 1
        mutated = (json.dumps(record, sort_keys=True, indent=1) + "\n").encode("utf-8")
        self.assertNotEqual(mutated, self.fresh)

    def test_matching_bytes_cannot_adopt_a_semantic_failure(self) -> None:
        record = json.loads(self.fresh.decode("utf-8"))
        record["totals"]["failures"] = 1
        with patch("run.verify_sources", return_value=[]), patch("magnification.census", return_value=record):
            with self.assertRaisesRegex(RuntimeError, "semantic failures"):
                run.receipt_bytes()

    def test_bad_magnification_or_restart_cannot_be_recorded(self) -> None:
        for name in ("invalid response", "unequal restart", "incomplete restart"):
            with self.subTest(name=name):
                record = json.loads(self.fresh.decode("utf-8"))
                if name == "invalid response":
                    record["exports"]["closed_L"]["magnification"]["seed_responses_valid"] = 0
                else:
                    layer = record["restart_samples"]["runs"][0]["layers"][0]
                    layer.pop("equal")
                    if name == "unequal restart":
                        layer["equal"] = False
                with patch("run.verify_sources", return_value=[]), patch("magnification.census", return_value=record):
                    with self.assertRaises(RuntimeError):
                        run.receipt_bytes()

    def test_record_carries_no_timestamp_or_path(self) -> None:
        text = self.fresh.decode("utf-8")
        for token in ("timestamp", "C:\\\\", "/Users/", "worktrees"):
            self.assertNotIn(token, text)

    def test_the_figures_the_readme_quotes(self) -> None:
        record = json.loads(self.fresh.decode("utf-8"))
        totals = record["totals"]
        self.assertEqual((totals["nodes"], totals["edges"], totals["rounds"], totals["supplies"]),
                         (5240, 5498, 4546, 952))
        self.assertEqual(totals["minima"], totals["rounds"])
        self.assertEqual(totals["failures"], 0)
        depths = {name: ex["engine_class"]["completeness_depth"] for name, ex in record["exports"].items()}
        self.assertEqual(depths, {"closed_L": 1, "closed_F": 3, "tree_L_mu1": 6, "tree_L_mu2": 15,
                                  "tree_F_mu1": 5, "tree_F_mu2": 15})
        for ex in record["exports"].values():
            self.assertEqual(ex["orbit_brute_force"]["disagreements"], [])
            self.assertEqual(ex["restart_two_step"]["failures"], [])
            mag = ex["magnification"]
            self.assertEqual(mag["seed_responses_valid"], mag["creation_rounds"])
        self.assertFalse(record["root_orbit_demands"]["F_seed_is_orbit_representative"])
        for run_record in record["restart_samples"]["runs"]:
            for layer in run_record["layers"]:
                self.assertTrue(layer.get("equal", False), run_record)


if __name__ == "__main__":
    unittest.main()
