"""The committed computation records replay byte for byte."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run  # noqa: E402


class ComputationRecord(unittest.TestCase):
    fresh: dict[str, bytes]

    @classmethod
    def setUpClass(cls) -> None:
        cls.fresh = run.receipt_bytes()

    def test_committed_records_replay_byte_for_byte(self) -> None:
        self.assertTrue(run.GRAMMAR.is_file(), "run `python run.py --write` first")
        self.assertTrue(run.CANDIDATES.is_file(), "run `python run.py --write` first")
        self.assertEqual(run.GRAMMAR.read_bytes(), self.fresh["grammar"])
        self.assertEqual(run.CANDIDATES.read_bytes(), self.fresh["candidates"])

    def test_a_changed_figure_is_detected(self) -> None:
        record = json.loads(self.fresh["grammar"].decode("utf-8"))
        record["reqs_writers"] = ["AdmitRuleAll"]
        mutated = (json.dumps(record, sort_keys=True, indent=1) + "\n").encode("utf-8")
        self.assertNotEqual(mutated, self.fresh["grammar"])

    def test_records_carry_no_timestamp_or_path(self) -> None:
        for blob in self.fresh.values():
            text = blob.decode("utf-8")
            for token in ("timestamp", "C:\\\\", "/Users/", "worktrees"):
                self.assertNotIn(token, text)

    def test_the_figures_the_readme_quotes(self) -> None:
        grammar = json.loads(self.fresh["grammar"].decode("utf-8"))
        candidates = json.loads(self.fresh["candidates"].decode("utf-8"))
        self.assertEqual(grammar["outcome"], "B")
        self.assertEqual(grammar["reqs_writers"], ["Impose"])
        self.assertEqual(grammar["reading_replays"]["L"]["reqs"], [[0, 1]])
        self.assertEqual(grammar["reading_replays"]["F"]["reqs"], [[1, 2]])
        self.assertEqual(candidates["outcome"], "B")
        self.assertEqual(len(candidates["census"]), 11)
        self.assertEqual(candidates["guard_errors"], [])
        i1 = next(row for row in candidates["census"] if row["id"] == "I1")
        self.assertEqual(i1["status"], "OPEN")


if __name__ == "__main__":
    unittest.main()
