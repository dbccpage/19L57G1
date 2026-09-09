"""The committed hunt record replays byte for byte."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))
import hunt as hn  # noqa: E402
import run  # noqa: E402


class ComputationRecord(unittest.TestCase):
    fresh: bytes

    @classmethod
    def setUpClass(cls) -> None:
        cls.fresh = run.receipt_bytes()

    def test_committed_record_replays_byte_for_byte(self) -> None:
        self.assertTrue(run.HUNT.is_file(), "run `python run.py --write` first")
        self.assertEqual(run.HUNT.read_bytes(), self.fresh)

    def test_the_figures_the_readme_quotes(self) -> None:
        record = json.loads(self.fresh.decode("utf-8"))
        self.assertEqual(record["regime_count"], 56020)
        self.assertEqual(record["refined_class_count"], record["brute_class_count"])
        self.assertTrue(record["agreement"])
        self.assertEqual(record["falsifier_count"], 0)
        self.assertEqual(record["falsifiers"], [])
        self.assertEqual(record["general_soundness"], "OPEN")
        self.assertEqual(record["bounds"]["max_data"], 3)
        self.assertTrue(record["seed_corpus"]["agreement"])
        self.assertEqual(hn.claim_errors(record), ())

    def test_records_carry_no_timestamp_or_path(self) -> None:
        text = self.fresh.decode("utf-8")
        for token in ("timestamp", "C:\\\\", "/Users/", "worktrees"):
            self.assertNotIn(token, text)
