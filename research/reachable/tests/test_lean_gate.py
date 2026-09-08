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
        reports = verify_lean.parse_reports(GOOD, ["Reachable.reach_rules"])
        self.assertEqual(reports, {"Reachable.reach_rules": ["Quot.sound", "propext"]})

    def test_accepts_primed_names(self) -> None:
        log = "'Reachable.cut\\'' depends on axioms: [propext]"
        self.assertEqual(verify_lean.parse_reports(log, ["Reachable.cut\\'"]),
                         {"Reachable.cut\\'": ["propext"]})

    def test_source_census_reads_the_print_lines(self) -> None:
        text = (ROOT / "lean" / "Reachable.lean").read_text(encoding="utf-8")
        names = verify_lean.source_census(text)
        self.assertIn("Reachable.formNoInst_unreachable", names)
        self.assertIn("Reachable.ruledMark_unreachable", names)
        self.assertEqual(len(names), len(set(names)))

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
                    verify_lean.parse_reports(log, census)

    def test_duplicate_census_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate"):
            verify_lean.source_census("#print axioms A.x\n#print axioms A.x\n")


if __name__ == "__main__":
    unittest.main()
