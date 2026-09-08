"""The committed computation record replays byte for byte, and a mutated
record is refused by name (the injection for this family's own gate)."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run  # noqa: E402


class ComputationRecord(unittest.TestCase):
    fresh: bytes

    @classmethod
    def setUpClass(cls) -> None:
        cls.fresh = run.receipt_bytes()

    def test_committed_record_replays_byte_for_byte(self) -> None:
        self.assertTrue(run.RECEIPT.is_file(), "run `python run.py --write` first")
        self.assertEqual(run.RECEIPT.read_bytes(), self.fresh)

    def test_a_changed_figure_is_detected(self) -> None:
        record = json.loads(self.fresh.decode("utf-8"))
        record["route_pair"]["span_total_late"] = 4
        mutated = (json.dumps(record, sort_keys=True, indent=1) + "\n").encode("utf-8")
        self.assertNotEqual(mutated, self.fresh)

    def test_record_carries_no_timestamp_or_path(self) -> None:
        text = self.fresh.decode("utf-8")
        for token in ("timestamp", "C:\\\\", "/Users/", "worktrees"):
            self.assertNotIn(token, text)

    def test_the_figures_the_readme_quotes(self) -> None:
        record = json.loads(self.fresh.decode("utf-8"))
        families = record["root_families"]
        self.assertEqual((families["L_mu1"]["classes"], families["L_mu1"]["raw_minima"]), (3, 6))
        self.assertEqual((families["F_mu1"]["classes"], families["F_mu1"]["raw_minima"]), (5, 10))
        self.assertEqual((families["L_mu2"]["classes"], families["L_mu2"]["raw_minima"]), (1, 2))
        self.assertEqual((families["F_mu2"]["classes"], families["F_mu2"]["raw_minima"]), (1, 2))
        self.assertEqual(record["route_pair"]["span_total_early"], 2)
        self.assertEqual(record["route_pair"]["span_total_late"], 3)
        for name in ("closed_L", "closed_F"):
            block = record["fixpoint_census"][name]
            self.assertTrue(block["all_good"] and block["all_characterizations_hold"]
                            and block["all_two_growths_demand"])


if __name__ == "__main__":
    unittest.main()
