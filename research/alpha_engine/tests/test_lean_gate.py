"""The report parser, forbidden tokens, and the committed Lean record."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_lean import (  # noqa: E402
    ALLOWED_AXIOMS,
    FORBIDDEN,
    MATHLIB,
    RECORD,
    parse_reports,
)

CENSUS = "HARNESS_THEOREM: Harness.license_is_not_event"


class ReportParser(unittest.TestCase):
    def test_axiom_free_report(self) -> None:
        self.assertEqual(
            parse_reports(
                "'Harness.license_is_not_event' does not depend on any axioms",
                CENSUS,
            ),
            {"Harness.license_is_not_event": []},
        )

    def test_foreign_namespace_reports_are_ignored(self) -> None:
        log = (
            "'Derivation.supply_no_op' does not depend on any axioms\n"
            "'Harness.license_is_not_event' does not depend on any axioms"
        )
        self.assertEqual(
            parse_reports(log, CENSUS),
            {"Harness.license_is_not_event": []},
        )

    def test_prefixed_and_primed_reports(self) -> None:
        census = (
            "info: Inventory.lean:11:0: "
            "HARNESS_THEOREM: Harness.EvalResult.mk.injEq"
        )
        log = (
            "info: Inventory.lean:40:0: "
            "'Harness.EvalResult.mk.injEq' depends on axioms: [propext, Quot.sound]"
        )
        self.assertEqual(
            parse_reports(log, census),
            {"Harness.EvalResult.mk.injEq": ["Quot.sound", "propext"]},
        )

    def test_incomplete_or_disallowed_reports_fail_by_name(self) -> None:
        cases = [
            ("", "", "empty"),
            ("", CENSUS, "missing"),
            (
                "'Harness.other' does not depend on any axioms",
                CENSUS,
                "mismatch",
            ),
            (
                "'Harness.license_is_not_event' depends on axioms: [Classical.choice]",
                CENSUS,
                "disallowed",
            ),
        ]
        for log, census, reason in cases:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(ValueError, reason):
                    parse_reports(log, census)


class ForbiddenTokens(unittest.TestCase):
    def test_sorry_and_mathlib_are_named(self) -> None:
        self.assertIsNotNone(FORBIDDEN.search("  sorry\n"))
        self.assertIsNotNone(MATHLIB.search("import mathlib\n"))


class CommittedRecord(unittest.TestCase):
    def test_record_is_within_the_whitelist_and_not_a_proof(self) -> None:
        if not RECORD.is_file():
            self.skipTest("run python verify_lean.py --write first")
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        reports = record["reports"]
        self.assertEqual(record["authority_effect"], "None")
        self.assertEqual(record["python_driver_refinement"], "NOT_PROVED")
        self.assertEqual(record["receipt_is_not_proof"], True)
        self.assertIn("sealed object-language theorem", record["scope"])
        for name, axioms in reports.items():
            self.assertTrue(name.startswith("Harness."), name)
            self.assertTrue(set(axioms) <= ALLOWED_AXIOMS, name)
        for theorem in (
            "Harness.license_is_not_event",
            "Harness.policy_explored_subset",
            "Harness.uniqueness_does_not_apply",
            "Harness.evaluation_does_not_admit",
        ):
            self.assertIn(theorem, reports)
            self.assertEqual(reports[theorem], [])


if __name__ == "__main__":
    unittest.main()
