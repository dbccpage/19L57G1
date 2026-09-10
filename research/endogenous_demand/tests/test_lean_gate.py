"""The report parser, forbidden tokens, and the committed Lean record."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_lean import ALLOWED_AXIOMS, FORBIDDEN, MATHLIB, RECORD, parse_reports  # noqa: E402

CENSUS = "ENDOGENOUS_DEMAND_THEOREM: EndogenousDemand.cut"


class ReportParser(unittest.TestCase):
    def test_accepts_primed_theorem_names(self) -> None:
        self.assertEqual(
            parse_reports(
                "'EndogenousDemand.cut'' depends on axioms: [propext]",
                "ENDOGENOUS_DEMAND_THEOREM: EndogenousDemand.cut'",
            ),
            {"EndogenousDemand.cut'": ["propext"]},
        )

    def test_axiom_free_report(self) -> None:
        self.assertEqual(
            parse_reports("'EndogenousDemand.cut' does not depend on any axioms", CENSUS),
            {"EndogenousDemand.cut": []},
        )

    def test_incomplete_or_disallowed_reports_fail_by_name(self) -> None:
        cases = [
            ("", "", "empty"),
            ("", CENSUS, "missing"),
            ("'EndogenousDemand.other' does not depend on any axioms", CENSUS, "mismatch"),
            ("'EndogenousDemand.cut' depends on axioms: [Classical.choice]", CENSUS, "disallowed"),
            (
                "'EndogenousDemand.cut' does not depend on any axioms\n"
                "'EndogenousDemand.cut' does not depend on any axioms",
                CENSUS,
                "duplicate report",
            ),
            (
                "'EndogenousDemand.cut' does not depend on any axioms",
                CENSUS + "\n" + CENSUS,
                "duplicate environment",
            ),
            (
                "'EndogenousDemand.cut' does not depend on any axioms\n"
                "'EndogenousDemand.extra' does not depend on any axioms",
                CENSUS,
                "extra",
            ),
        ]
        for log, census, reason in cases:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(ValueError, reason):
                    parse_reports(log, census)


class ForbiddenTokens(unittest.TestCase):
    def test_sorry_is_named(self) -> None:
        self.assertIsNotNone(FORBIDDEN.search("theorem t : True := sorry\n"))

    def test_mathlib_is_named(self) -> None:
        self.assertIsNotNone(MATHLIB.search("import mathlib\n"))

    def test_ordinary_admitted_is_not_the_token(self) -> None:
        self.assertIsNone(FORBIDDEN.search("the admitted instances of the regime\n"))


class CommittedRecord(unittest.TestCase):
    def test_record_is_within_the_whitelist_and_names_the_scope(self) -> None:
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        reports = record["reports"]
        self.assertEqual(record["theorem_count_including_generated"], len(reports))
        self.assertEqual(record["axiom_free_count"], sum(1 for v in reports.values() if not v))
        self.assertEqual(record["outcome"], "B")
        self.assertEqual(record["class"], "C_reqs")
        for name, axioms in reports.items():
            self.assertTrue(name.startswith("EndogenousDemand."), name)
            self.assertTrue(set(axioms) <= ALLOWED_AXIOMS, name)
        for theorem in (
            "EndogenousDemand.e2_on_C_reqs_unsat",
            "EndogenousDemand.replay_reqs_iff_impose",
            "EndogenousDemand.stepE_reqs_mem",
            "EndogenousDemand.applyDelta_reqs",
            "EndogenousDemand.event_constructors",
            "EndogenousDemand.historyL_reqs_from_impose",
            "EndogenousDemand.historyF_reqs_from_impose",
        ):
            self.assertIn(theorem, reports)


if __name__ == "__main__":
    unittest.main()
