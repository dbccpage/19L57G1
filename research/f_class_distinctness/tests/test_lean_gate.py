"""The report parser, forbidden tokens, and the committed Lean record."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_lean import ALLOWED_AXIOMS, FORBIDDEN, MATHLIB, RECORD, parse_reports  # noqa: E402

CENSUS = "F_CLASS_THEOREM: FClassDistinctness.cut"


class ReportParser(unittest.TestCase):
    def test_axiom_free_report(self) -> None:
        self.assertEqual(
            parse_reports("'FClassDistinctness.cut' does not depend on any axioms", CENSUS),
            {"FClassDistinctness.cut": []},
        )

    def test_foreign_namespace_reports_are_ignored(self) -> None:
        log = (
            "'Derivation.U0_not_iso_BL' does not depend on any axioms\n"
            "'FClassDistinctness.cut' does not depend on any axioms"
        )
        self.assertEqual(parse_reports(log, CENSUS), {"FClassDistinctness.cut": []})

    def test_prefixed_and_primed_reports(self) -> None:
        census = "info: Inventory.lean:11:0: F_CLASS_THEOREM: FClassDistinctness.isoDiagF'_exists"
        log = (
            "info: FClassDistinctness.lean:303:0: "
            "'FClassDistinctness.isoDiagF'_exists' depends on axioms: [propext, Quot.sound]"
        )
        self.assertEqual(
            parse_reports(log, census),
            {"FClassDistinctness.isoDiagF'_exists": ["Quot.sound", "propext"]},
        )

    def test_incomplete_or_disallowed_reports_fail_by_name(self) -> None:
        cases = [
            ("", "", "empty"),
            ("", CENSUS, "missing"),
            ("'FClassDistinctness.other' does not depend on any axioms", CENSUS, "mismatch"),
            ("'FClassDistinctness.cut' depends on axioms: [Classical.choice]", CENSUS, "disallowed"),
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
    def test_record_is_within_the_whitelist_and_keeps_catalog_open(self) -> None:
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        reports = record["reports"]
        self.assertEqual(record["outcome"], "five_f_classes_pairwise_noniso")
        self.assertIn("OPEN", record["catalog_completeness"])
        for name, axioms in reports.items():
            self.assertTrue(name.startswith("FClassDistinctness."), name)
            self.assertTrue(set(axioms) <= ALLOWED_AXIOMS, name)
        for theorem in (
            "FClassDistinctness.five_classes_pairwise_noniso",
            "FClassDistinctness.five_valid_pairwise_noniso",
            "FClassDistinctness.OutF_not_iso_InF",
        ):
            self.assertIn(theorem, reports)
