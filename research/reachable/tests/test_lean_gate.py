"""The report parser fails on every incomplete or disallowed shape, by name."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import verify_lean  # noqa: E402

GOOD = "'Reachable.reach_rules' depends on axioms: [propext, Quot.sound]"


class ReportParser(unittest.TestCase):
    def test_accepts_the_census_exactly(self) -> None:
        reports = verify_lean.parse_reports(GOOD, "REACHABLE_THEOREM: Reachable.reach_rules")
        self.assertEqual(reports, {"Reachable.reach_rules": ["Quot.sound", "propext"]})

    def test_accepts_primed_names(self) -> None:
        log = "'Reachable.cut\\'' depends on axioms: [propext]"
        self.assertEqual(verify_lean.parse_reports(log, "REACHABLE_THEOREM: Reachable.cut\\'"),
                         {"Reachable.cut\\'": ["propext"]})

    def test_unreported_theorem_is_present_in_the_independent_census(self) -> None:
        inventory = "REACHABLE_THEOREM: Reachable.reach_rules\nREACHABLE_THEOREM: Reachable.unreported"
        with self.assertRaisesRegex(ValueError, "Reachable.unreported"):
            verify_lean.parse_reports(GOOD, inventory)
        with self.assertRaisesRegex(ValueError, "empty"):
            verify_lean.environment_census("#print axioms Reachable.reach_rules")

    def test_incomplete_or_disallowed_reports_fail(self) -> None:
        cases = [
            ("", ["Reachable.reach_rules"], "mismatch"),
            ("'Reachable.other' does not depend on any axioms", ["Reachable.reach_rules"], "mismatch"),
            ("'Reachable.reach_rules' depends on axioms: [Classical.choice]", ["Reachable.reach_rules"], "disallowed"),
            (GOOD + "\n" + GOOD, ["Reachable.reach_rules"], "duplicate report"),
        ]
        for log, census, reason in cases:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(ValueError, reason):
                    verify_lean.parse_reports(log, "\n".join("REACHABLE_THEOREM: " + name for name in census))

    def test_duplicate_census_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate"):
            verify_lean.environment_census("REACHABLE_THEOREM: A.x\nREACHABLE_THEOREM: A.x\n")


if __name__ == "__main__":
    unittest.main()
