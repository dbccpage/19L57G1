"""Prose carries both readings, states the pairwise theorem, and keeps the catalog open."""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
L_THEOREMS = (
    "U0_not_iso_BL",
    "U0_not_iso_BD",
    "BL_not_iso_BD",
    "isoU1U0",
)


class Prose(unittest.TestCase):
    def test_readme_and_claims_keep_catalog_open_and_carry_both_readings(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        claims = (ROOT / "CLAIMS.md").read_text(encoding="utf-8")
        for text, name in ((readme, "README"), (claims, "CLAIMS")):
            self.assertIn("OPEN", text, name)
            self.assertIn("AuthorityEffect: None", text, name)
            self.assertIn("reading f", text.lower(), name)
            self.assertIn("reading l", text.lower(), name)
            self.assertIn("five_classes_pairwise_noniso", text, name)
            self.assertNotIn("import mathlib", text.lower(), name)
            self.assertNotIn("catalog is complete", text.lower(), name)

    def test_lean_does_not_cite_l_distinctness_theorems(self) -> None:
        lean = (ROOT / "lean" / "FClassDistinctness.lean").read_text(encoding="utf-8")
        for name in L_THEOREMS:
            self.assertNotIn(name, lean, name)

    def test_status_records_injections(self) -> None:
        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
        for gate in ("G1", "G2", "G3", "G4", "G5", "G6", "G7"):
            self.assertIn(gate, status)
