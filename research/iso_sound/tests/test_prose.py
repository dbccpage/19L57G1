"""Prose states the bound, the hunt result, and that general soundness is OPEN."""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Prose(unittest.TestCase):
    def test_readme_and_claims_keep_soundness_open(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        claims = (ROOT / "CLAIMS.md").read_text(encoding="utf-8")
        for text, name in ((readme, "README"), (claims, "CLAIMS")):
            self.assertIn("OPEN", text, name)
            self.assertIn("56020", text, name)
            self.assertIn("AuthorityEffect: None", text, name)
            self.assertNotIn("import mathlib", text.lower(), name)
            self.assertNotIn("CL-ISO-SOUND is proved", text)

    def test_status_records_injections(self) -> None:
        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
        for gate in ("G1", "G2", "G3", "G4", "G5", "G6", "G7"):
            self.assertIn(gate, status)
