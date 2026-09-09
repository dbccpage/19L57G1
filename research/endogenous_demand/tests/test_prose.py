"""Prose of this tree states Outcome B and keeps the instance channel OPEN."""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Prose(unittest.TestCase):
    def test_readme_and_claims_state_the_outcome(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        claims = (ROOT / "CLAIMS.md").read_text(encoding="utf-8")
        for text, name in ((readme, "README"), (claims, "CLAIMS")):
            self.assertIn("Outcome B", text, name)
            self.assertIn("C_reqs", text, name)
            self.assertIn("OPEN", text, name)
            self.assertIn("AuthorityEffect: None", text, name)
            self.assertNotIn("import mathlib", text.lower(), name)

    def test_claims_do_not_call_c5_or_c6_endogenous(self) -> None:
        claims = (ROOT / "CLAIMS.md").read_text(encoding="utf-8")
        for cid in ("C5", "C6"):
            self.assertNotIn(f"{cid} is endogenous", claims)
            self.assertNotIn(f"{cid} satisfies E1", claims)

    def test_status_records_injections(self) -> None:
        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
        for gate in ("G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9",
                     "G10", "G11", "G12"):
            self.assertIn(gate, status)


if __name__ == "__main__":
    unittest.main()
