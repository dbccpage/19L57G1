"""The report parser, forbidden tokens, and the committed Lean record."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_lean import ALLOWED_AXIOMS, FORBIDDEN, MATHLIB, RECORD, parse_reports  # noqa: E402

CENSUS = "ISO_SOUND_THEOREM: IsoSound.cut"


class ReportParser(unittest.TestCase):
    def test_axiom_free_report(self) -> None:
        self.assertEqual(
            parse_reports("'IsoSound.cut' does not depend on any axioms", CENSUS),
            {"IsoSound.cut": []},
        )

    def test_incomplete_or_disallowed_reports_fail_by_name(self) -> None:
        cases = [
            ("", "", "empty"),
            ("", CENSUS, "missing"),
            ("'IsoSound.other' does not depend on any axioms", CENSUS, "mismatch"),
            ("'IsoSound.cut' depends on axioms: [Classical.choice]", CENSUS, "disallowed"),
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
    def test_record_is_within_the_whitelist_and_keeps_the_bridge_open(self) -> None:
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        reports = record["reports"]
        self.assertEqual(record["general_soundness"], "OPEN")
        self.assertEqual(record["outcome"], "no_falsifier_in_bound")
        for name, axioms in reports.items():
            self.assertTrue(name.startswith("IsoSound."), name)
            self.assertTrue(set(axioms) <= ALLOWED_AXIOMS, name)
        for theorem in (
            "IsoSound.genesis_unique",
            "IsoSound.equal_of_fields",
            "IsoSound.general_bridge_recorded_open",
        ):
            self.assertIn(theorem, reports)
