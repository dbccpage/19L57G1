"""Native vocabulary: no companion ledger IDs, no seventh Event, no heuristics."""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

COMPANION_IDS = (
    "S-BRANCH",
    "S-LIFT",
    "S-NOGEN",
    "S-ALPHA",
    "AE-PROBLEM",
    "AE-GRADES",
    "AE-AXIOM-BOUND",
    "AE-NO-FIAT",
    "AdmitCell",
)

HEURISTICS = ("UCB", "visit-count", "visit_count", "rollout")


def _iter_text_files() -> list[Path]:
    out: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".mypy_cache", "__pycache__", ".lake"} for part in path.parts):
            continue
        if path.suffix in {".py", ".md", ".json", ".toml"}:
            out.append(path)
    return out


class Vocabulary(unittest.TestCase):
    def test_companion_ids_are_absent_from_production_and_prose(self) -> None:
        for path in _iter_text_files():
            if path.name.startswith("test_"):
                continue
            text = path.read_text(encoding="utf-8")
            for token in COMPANION_IDS:
                self.assertNotIn(token, text, f"{path.name} carries {token}")

    def test_heuristics_are_absent_from_production(self) -> None:
        for name in (
            "harness.py",
            "evaluate.py",
            "proposer.py",
            "search_policy.py",
            "driver_a.py",
        ):
            text = (ROOT / name).read_text(encoding="utf-8")
            for token in HEURISTICS:
                self.assertNotIn(token, text, f"{name} carries {token}")

    def test_no_seventh_event_constructor(self) -> None:
        text = (ROOT / "harness.py").read_text(encoding="utf-8")
        self.assertIn("AdmitRuleAll", text)
        self.assertNotIn("AdmitCell", text)
        self.assertNotIn("DualEvent", text)
        self.assertNotIn("TSEvent", text)


if __name__ == "__main__":
    unittest.main()
