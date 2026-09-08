"""The committed census replays byte for byte; a mutated record is refused,
by the byte comparison and by the receipt's semantic refusals."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
from typing import Any
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

    def record(self) -> dict[str, Any]:
        loaded: dict[str, Any] = json.loads(self.fresh.decode("utf-8"))
        return loaded

    def test_committed_record_replays_byte_for_byte(self) -> None:
        self.assertTrue(run.RECEIPT.is_file(), "run `python run.py --write` first")
        self.assertEqual(run.RECEIPT.read_bytes(), self.fresh)

    def test_the_check_command_refuses_a_changed_figure(self) -> None:
        record = self.record()
        record["universe"]["distinct_endpoints_visible"] += 1
        mutated = (json.dumps(record, sort_keys=True, indent=1) + "\n").encode("utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            receipt = Path(tmp) / "census.json"
            with patch("run.receipt_bytes", return_value=self.fresh), patch("run.RECEIPT", receipt):
                receipt.write_bytes(mutated)
                self.assertEqual(run.main(["--check"]), 1)
                receipt.write_bytes(self.fresh)
                self.assertEqual(run.main(["--check"]), 0)

    def test_matching_bytes_cannot_adopt_a_semantic_failure(self) -> None:
        record = self.record()
        record["totals"]["failures"] = 1
        with patch("run.verify_sources", return_value=[]), patch("translation.census", return_value=record):
            with self.assertRaisesRegex(RuntimeError, "semantic failures"):
                run.receipt_bytes()

    def test_the_receipt_refuses_each_semantic_defect_by_name(self) -> None:
        cases: dict[str, tuple[str, Any]] = {
            "empty universe": ("enumerated nothing", lambda r: r["universe"].__setitem__("settings", 0)),
            "twelve settings": ("not thirteen", lambda r: r["sealed_settings"]["settings"].pop("triSym")),
            "unfaithful full-store setting": (
                "triProtected: the encoding is not faithful",
                lambda r: r["sealed_settings"]["settings"]["triProtected"].__setitem__("faithful", False)),
            "sealed verdict not reproduced": (
                "d2Bare: a sealed theorem verdict",
                lambda r: r["sealed_settings"]["settings"]["d2Bare"]["sealed_theorems"][0].__setitem__("agrees", False)),
            "visibility against collapse": (
                "d2Bare/mu1: visibility contradicts",
                lambda r: r["sealed_settings"]["settings"]["d2Bare"]["restart"]["mu1"].__setitem__(
                    "target_collapsed_at_root", True)),
            "visible pair with a response": (
                "tri/mu2: a visible pair whose root round",
                lambda r: r["sealed_settings"]["settings"]["tri"]["restart"]["mu2"]["root_round"][0].__setitem__(
                    "label", "inst2")),
            "collapsed pair missing a class": (
                "noPair/mu1_closed: a collapsed pair whose root round",
                lambda r: r["two_point"]["exhibits"]["noPair"]["restart"]["mu1_closed"]["root_round"].pop()),
            "collapsed pair at two items": (
                "boolEmpty/mu1: a collapsed pair whose root round",
                lambda r: r["sealed_settings"]["settings"]["boolEmpty"]["restart"]["mu1"]["root_round"][0].__setitem__(
                    "items", 2)),
        }
        for name, (message, mutate) in cases.items():
            with self.subTest(name=name):
                record = self.record()
                mutate(record)
                with patch("run.verify_sources", return_value=[]), patch("translation.census", return_value=record):
                    with self.assertRaisesRegex(RuntimeError, message):
                        run.receipt_bytes()

    def test_record_carries_no_timestamp_path_or_sentinel(self) -> None:
        text = self.fresh.decode("utf-8")
        for token in ("timestamp", "C:\\\\", "/Users/", "worktrees", "-1"):
            self.assertNotIn(token, text)

    def test_the_figures_the_readme_quotes(self) -> None:
        record = self.record()
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
        self.assertEqual(by_reading["A"]["holds_distinct"], 2352)
        self.assertEqual((by_reading["W"]["holds"], by_reading["W"]["holds_distinct"], by_reading["W"]["holds_collapsed"]),
                         (28044, 18624, 66))
        self.assertEqual((by_reading["C"]["holds"], by_reading["C"]["holds_distinct"]), (14022, 9312))
        self.assertEqual(by_reading["D"]["holds_collapsed"], 132)
        self.assertEqual(by_reading["E"]["holds_collapsed"], 100)
        for entry in by_reading.values():
            self.assertEqual(entry["holds_distinct"], entry["holds_visible"] + entry["holds_collapsed"])
            self.assertLessEqual(entry["holds_distinct"], entry["holds"])
        sources = record["verdict_sources"]
        self.assertEqual((sources["rows"], sources["sealed_rows"], sources["transcribed_rows"], sources["failures"]),
                         (42, 42, 42, []))
        thirteen = record["sealed_settings"]
        self.assertEqual(thirteen["failures"], [])
        self.assertEqual(thirteen["restart_bounds"], {"supply": False, "max_rounds": 4, "guard": 120})
        self.assertEqual(len(thirteen["settings"]), 13)
        self.assertEqual(sum(len(e["sealed_theorems"]) for e in thirteen["settings"].values()), 42)
        restarted = 0
        for name, entry in thirteen["settings"].items():
            self.assertTrue(entry["faithful"])
            if "restart" not in entry:
                self.assertEqual(entry["setting"]["a"], entry["setting"]["b"], name)
                continue
            restarted += 1
            for measure, restart in entry["restart"].items():
                labels = [c["label"] for c in restart["root_round"]]
                if entry["pair_visible"]:
                    self.assertEqual(labels, ["empty"], (name, measure))
                    self.assertEqual(restart["by_status"], {"expanded": 1, "terminal_all_separated": 1})
                else:
                    self.assertEqual(sorted(labels), ["inst2", "inst2diag"], (name, measure))
                    self.assertEqual([c["items"] for c in restart["root_round"]], [1, 1])
        self.assertEqual(restarted, 11)
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
                self.assertEqual({c["items"] for c in restart["root_round"]}, {1})
        self.assertEqual(record["totals"]["failures"], 0)


if __name__ == "__main__":
    unittest.main()
