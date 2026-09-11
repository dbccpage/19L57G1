"""Receipt decoder refuses duplicate JSON keys and CR bytes."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import run  # noqa: E402


class Receipt(unittest.TestCase):
    def test_duplicate_json_keys_are_rejected(self) -> None:
        raw = b'{"policy": 1, "policy": 2}\n'
        with self.assertRaises(ValueError) as ctx:
            run.load_receipt(raw)
        self.assertIn("duplicate JSON key", str(ctx.exception))

    def test_cr_bytes_are_rejected(self) -> None:
        raw = b'{"authority_effect": "None"}\r\n'
        with self.assertRaises(ValueError) as ctx:
            run.load_receipt(raw)
        self.assertIn("CR bytes", str(ctx.exception))

    def test_lone_cr_is_rejected(self) -> None:
        raw = b'{"authority_effect": "None"}\r'
        with self.assertRaises(ValueError):
            run.load_receipt(raw)

    def test_object_required(self) -> None:
        with self.assertRaises(ValueError):
            run.load_receipt(b"[1]\n")

    def test_nested_duplicate_keys_are_rejected(self) -> None:
        raw = b'{"outer": {"policy": 1, "policy": 2}}\n'
        with self.assertRaises(ValueError) as ctx:
            run.load_receipt(raw)
        self.assertIn("duplicate JSON key", str(ctx.exception))

    def test_committed_record_has_no_cr(self) -> None:
        repo = Path(__file__).resolve().parents[3]
        rel = "research/alpha_engine/evidence/three_phase.json"
        raw = subprocess.check_output(["git", "show", f"HEAD:{rel}"], cwd=repo)
        self.assertNotIn(b"\r", raw)
        payload = run.load_receipt(raw)
        self.assertEqual(payload.get("authority_effect"), "None")
        self.assertEqual(payload.get("receipt_is_not_proof"), True)
        self.assertEqual(payload.get("driver_b"), "OPEN")
        self.assertEqual(payload.get("ob_1"), "OPEN")
        self.assertEqual(payload.get("demand_generation"), "OPEN")
        self.assertEqual(payload.get("field_layout_is_not_temporal_proof"), True)
        self.assertIs(payload.get("auto_apply_unique_delta"), False)


if __name__ == "__main__":
    unittest.main()
