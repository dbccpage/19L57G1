"""The committed class record replays, and claim guards fire by name."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))
import classes as cl  # noqa: E402
import run  # noqa: E402


class ComputationRecord(unittest.TestCase):
    fresh: bytes
    record: dict[str, object]

    @classmethod
    def setUpClass(cls) -> None:
        cls.fresh = run.receipt_bytes()
        loaded: object = json.loads(cls.fresh.decode("utf-8"))
        assert isinstance(loaded, dict)
        cls.record = loaded

    def test_committed_record_replays_byte_for_byte(self) -> None:
        self.assertTrue(run.RECORD.is_file(), "run `python run.py --write` first")
        self.assertEqual(run.RECORD.read_bytes(), self.fresh)

    def test_claim_errors_on_the_fresh_record(self) -> None:
        self.assertEqual(cl.claim_errors(self.record), ())

    def test_records_carry_no_timestamp_or_path(self) -> None:
        text = self.fresh.decode("utf-8")
        for token in ("timestamp", "C:\\\\", "/Users/", "worktrees"):
            self.assertNotIn(token, text)

    def test_guards_fire_by_name(self) -> None:
        cases: list[tuple[str, str, object]] = [
            ("SCHEMA_GUARD", "schema", "other"),
            ("AUTHORITY_GUARD", "authority_effect", "Some"),
            ("READINGS_GUARD", "readings_carried", ["F"]),
            ("F_COUNT_GUARD", "f_engine_class_count", 4),
            ("L_COUNT_GUARD", "l_engine_class_count", 2),
            ("PAIRWISE_GUARD", "pairwise_noniso", False),
            ("ISO_HITS_GUARD", "pairwise_iso_hits", [["MarkF", "LinkF"]]),
            ("THEOREM_GUARD", "lean_theorem", "Derivation.U0_not_iso_BL"),
            ("CATALOG_GUARD", "catalog_completeness", "proved"),
            ("L_ISO_HITS_GUARD", "l_pairwise_iso_hits", [["U0", "BL"]]),
            ("WITHIN_GUARD", "within_class_iso_failures", ["MarkF"]),
        ]
        for guard, key, value in cases:
            mutated = dict(self.record)
            mutated[key] = value
            self.assertIn(guard, cl.claim_errors(mutated), guard)

    def test_rep_engine_guard_on_empty_and_double_hit(self) -> None:
        mutated = dict(self.record)
        mutated["f_rep_to_engine"] = []
        self.assertIn("REP_ENGINE_GUARD", cl.claim_errors(mutated))
        mutated["f_rep_to_engine"] = [{"rep": "MarkF", "engine_labels": []}] * 5
        self.assertIn("REP_ENGINE_GUARD", cl.claim_errors(mutated))
        mutated["f_rep_to_engine"] = ["x"] * 5
        self.assertIn("REP_ENGINE_GUARD", cl.claim_errors(mutated))
        mutated["f_rep_to_engine"] = [{"rep": "MarkF", "engine_labels": "x"}] * 5
        self.assertIn("REP_ENGINE_GUARD", cl.claim_errors(mutated))
