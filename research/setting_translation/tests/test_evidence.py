"""The committed census replays byte for byte; a mutated record is refused."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))
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
        record["universe"]["distinct_endpoints_visible"] += 1
        mutated = (json.dumps(record, sort_keys=True, indent=1) + "\n").encode("utf-8")
        self.assertNotEqual(mutated, self.fresh)

    def test_matching_bytes_cannot_adopt_a_semantic_failure(self) -> None:
        record = json.loads(self.fresh.decode("utf-8"))
        record["totals"]["failures"] = 1
        with patch("run.verify_sources", return_value=[]), patch("translation.census", return_value=record):
            with self.assertRaisesRegex(RuntimeError, "semantic failures"):
                run.receipt_bytes()

    def test_an_empty_universe_or_a_short_setting_list_cannot_be_recorded(self) -> None:
        for name in ("empty universe", "twelve settings"):
            with self.subTest(name=name):
                record = json.loads(self.fresh.decode("utf-8"))
                if name == "empty universe":
                    record["universe"]["settings"] = 0
                else:
                    record["sealed_settings"]["settings"].pop("triSym")
                with patch("run.verify_sources", return_value=[]), patch("translation.census", return_value=record):
                    with self.assertRaises(RuntimeError):
                        run.receipt_bytes()

    def test_record_carries_no_timestamp_or_path(self) -> None:
        text = self.fresh.decode("utf-8")
        for token in ("timestamp", "C:\\\\", "/Users/", "worktrees"):
            self.assertNotIn(token, text)

    def test_the_figures_the_readme_quotes(self) -> None:
        record = json.loads(self.fresh.decode("utf-8"))
        universe = record["universe"]
        self.assertEqual(universe["settings"], 56088)
        self.assertEqual(universe["by_carrier_size"], {"1": 24, "2": 768, "3": 55296})
        self.assertEqual(universe["failures"], [])
        self.assertEqual(universe["settings_with_distinct_endpoints"], 37248)
        self.assertEqual(universe["distinct_endpoints_visible"], 37116)
        self.assertEqual(universe["distinct_endpoints_collapsed"], 132)
        by_reading = universe["by_reading"]
        for reading in ("A", "Bs", "Bc", "Bl", "C", "F"):
            self.assertEqual(by_reading[reading]["holds_collapsed"], 0, reading)
        self.assertEqual(by_reading["A"]["holds"], 2352)
        self.assertEqual(by_reading["W"]["holds_collapsed"], 66)
        self.assertEqual(by_reading["D"]["holds_collapsed"], 132)
        self.assertEqual(by_reading["E"]["holds_collapsed"], 100)
        thirteen = record["sealed_settings"]
        self.assertEqual(thirteen["failures"], [])
        self.assertEqual(len(thirteen["settings"]), 13)
        self.assertEqual(sum(len(e["sealed_theorems"]) for e in thirteen["settings"].values()), 42)
        for entry in thirteen["settings"].values():
            self.assertTrue(entry["faithful"])
            for check in entry["sealed_theorems"]:
                self.assertTrue(check["agrees"], check)
        # At every visible pair the root round's minimum is the empty response.
        for name, entry in thirteen["settings"].items():
            if "restart" not in entry:
                self.assertEqual(entry["setting"]["a"], entry["setting"]["b"], name)
                continue
            for measure, restart in entry["restart"].items():
                labels = [c["label"] for c in restart["root_round"]]
                if entry["pair_visible"]:
                    self.assertEqual(labels, ["empty"], (name, measure))
                    self.assertFalse(restart["target_collapsed_at_root"])
                else:
                    self.assertEqual(sorted(labels), ["inst2", "inst2diag"], (name, measure))
                    self.assertTrue(restart["target_collapsed_at_root"])
        self.assertFalse(thirteen["settings"]["boolEmpty"]["pair_visible"])
        self.assertTrue(thirteen["settings"]["boolEmptyMerged"]["pair_visible"])
        two_point = record["two_point"]
        self.assertEqual(two_point["failures"], [])
        visible = {name: e["visible"] for name, e in two_point["exhibits"].items()}
        self.assertEqual(visible, {"selfOnly": True, "linkOnly": True, "selfAndLink": True,
                                   "bothLinks": True, "everyPair": False, "noPair": False})
        for name in ("everyPair", "noPair"):
            for restart in two_point["exhibits"][name]["restart"].values():
                self.assertEqual(sorted(c["label"] for c in restart["root_round"]), ["inst2", "inst2diag"])
                self.assertEqual({c["cost"][0] for c in restart["root_round"]}, {1})
        self.assertEqual(record["totals"]["failures"], 0)


if __name__ == "__main__":
    unittest.main()
