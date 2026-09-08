"""The report parser and the committed Lean record."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_lean import ALLOWED_AXIOMS, RECORD, parse_reports  # noqa: E402

CENSUS = "IGNITION_THEOREM: Ignition.cut"


class ReportParser(unittest.TestCase):
    def test_accepts_primed_theorem_names(self) -> None:
        self.assertEqual(
            parse_reports("'Ignition.cut'' depends on axioms: [propext]", "IGNITION_THEOREM: Ignition.cut'"),
            {"Ignition.cut'": ["propext"]})

    def test_axiom_free_report(self) -> None:
        self.assertEqual(parse_reports("'Ignition.cut' does not depend on any axioms", CENSUS),
                         {"Ignition.cut": []})

    def test_incomplete_or_disallowed_reports_fail_by_name(self) -> None:
        cases = [
            ("", "", "empty"),
            ("", CENSUS, "missing"),
            ("'Ignition.other' does not depend on any axioms", CENSUS, "mismatch"),
            ("'Ignition.cut' depends on axioms: [Classical.choice]", CENSUS, "disallowed"),
            ("'Ignition.cut' does not depend on any axioms\n'Ignition.cut' does not depend on any axioms",
             CENSUS, "duplicate report"),
            ("'Ignition.cut' does not depend on any axioms", CENSUS + "\n" + CENSUS, "duplicate environment"),
            ("'Ignition.cut' does not depend on any axioms\n'Ignition.extra' does not depend on any axioms",
             CENSUS, "extra"),
        ]
        for log, census, reason in cases:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(ValueError, reason):
                    parse_reports(log, census)


class CommittedRecord(unittest.TestCase):
    def test_record_is_within_the_whitelist_and_names_the_scope(self) -> None:
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        reports = record["reports"]
        self.assertEqual(record["theorem_count_including_generated"], len(reports))
        self.assertEqual(record["axiom_free_count"], sum(1 for v in reports.values() if not v))
        for name, axioms in reports.items():
            self.assertTrue(name.startswith("Ignition."), name)
            self.assertTrue(set(axioms) <= ALLOWED_AXIOMS, name)
        self.assertEqual(record["python_driver_refinement"], "NOT_PROVED")
        for theorem in ("Ignition.grow_demand_iff", "Ignition.grow_at_most_one_demand",
                        "Ignition.two_grows_collapsed", "Ignition.runHist_replays",
                        "Ignition.demand_iff_residual", "Ignition.identity_not_signature_determined",
                        "Ignition.future_factors_through_endpoint", "Ignition.idle_lawful",
                        "Ignition.idle_and_active_both_lawful", "Ignition.good_fire"):
            self.assertIn(theorem, reports)


if __name__ == "__main__":
    unittest.main()
