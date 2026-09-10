"""Coverage-gate regressions: statement vs combined percent, required files."""

from __future__ import annotations

import io
import json
from pathlib import Path
import sys
import tempfile
from unittest import mock
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_coverage  # noqa: E402


def _required() -> dict[str, object]:
    return {name: {} for name in check_coverage.REQUIRED_FILES}


def _totals(covered_lines: int = 95, statements: int = 100,
            covered_branches: int = 19, branches: int = 20) -> dict[str, object]:
    return {
        "percent_covered": 97.0,
        "covered_lines": covered_lines,
        "num_statements": statements,
        "covered_branches": covered_branches,
        "num_branches": branches,
    }


class CoverageGate(unittest.TestCase):
    def test_combined_percent_does_not_pass_low_statements(self) -> None:
        errors = check_coverage.report_errors({
            "totals": _totals(covered_lines=94, statements=100,
                              covered_branches=100, branches=100),
            "files": _required(),
        })
        self.assertTrue(any(e.startswith("COVERAGE_STATEMENT:") for e in errors), errors)

    def test_unrelated_only_population_fails(self) -> None:
        errors = check_coverage.report_errors({
            "totals": _totals(covered_lines=100, statements=100,
                              covered_branches=100, branches=100),
            "files": {"unrelated.py": {}},
        })
        self.assertTrue(any(e.startswith("COVERAGE_POPULATION:") for e in errors), errors)

    def test_pass_at_threshold(self) -> None:
        errors = check_coverage.report_errors({
            "totals": _totals(),
            "files": _required(),
        })
        self.assertEqual(errors, [])

    def test_payload_not_object(self) -> None:
        self.assertEqual(check_coverage.report_errors(["x"]), ["COVERAGE_SHAPE: not an object"])

    def test_missing_totals_and_files(self) -> None:
        self.assertTrue(any("COVERAGE_TOTALS" in e for e in check_coverage.report_errors({"files": _required()})))
        self.assertTrue(any("COVERAGE_FILES" in e for e in check_coverage.report_errors({"totals": _totals(), "files": {}})))

    def test_incomplete_totals(self) -> None:
        errors = check_coverage.report_errors({"totals": {"percent_covered": 100}, "files": _required()})
        self.assertTrue(any("covered_lines" in e for e in errors), errors)

    def test_zero_statements_and_branches(self) -> None:
        self.assertTrue(any("no statements" in e for e in check_coverage.report_errors({
            "totals": _totals(covered_lines=0, statements=0), "files": _required()})))
        self.assertTrue(any("no branches" in e for e in check_coverage.report_errors({
            "totals": _totals(covered_branches=0, branches=0), "files": _required()})))

    def test_low_branch_fails(self) -> None:
        errors = check_coverage.report_errors({
            "totals": _totals(covered_lines=100, statements=100, covered_branches=18, branches=20),
            "files": _required(),
        })
        self.assertTrue(any(e.startswith("COVERAGE_BRANCH:") for e in errors), errors)

    def test_leak(self) -> None:
        errors = check_coverage.report_errors({
            "totals": _totals(),
            "files": {"tests/test_x.py": {}},
        })
        self.assertTrue(any(e.startswith("COVERAGE_LEAK:") for e in errors), errors)

    def test_omit_dirs_are_components_not_substrings(self) -> None:
        # 'clean/' and 'subtests/' contain 'lean/'/'tests/' as substrings but are
        # not the omitted directories; a component match must not flag them.
        for good in ("clean/util.py", "subtests/util.py"):
            errors = check_coverage.report_errors({
                "totals": _totals(covered_lines=100, statements=100,
                                  covered_branches=100, branches=100),
                "files": {**_required(), good: {}},
            })
            self.assertFalse(any(e.startswith("COVERAGE_LEAK:") for e in errors),
                             (good, errors))
        errors = check_coverage.report_errors({
            "totals": _totals(),
            "files": {**_required(), "tests/test_x.py": {}},
        })
        self.assertTrue(any(e.startswith("COVERAGE_LEAK:") for e in errors), errors)

    def test_missing_report_and_unreadable(self) -> None:
        original = check_coverage.REPORT
        check_coverage.REPORT = Path(tempfile.gettempdir()) / "no-such-coverage.json"
        try:
            with mock.patch("sys.stdout", io.StringIO()):
                self.assertEqual(check_coverage.main(), 1)
        finally:
            check_coverage.REPORT = original
        tmp = Path(tempfile.mkdtemp()) / "coverage.json"
        tmp.write_text("{not json", encoding="utf-8")
        check_coverage.REPORT = tmp
        try:
            captured = io.StringIO()
            with mock.patch("sys.stdout", captured):
                self.assertEqual(check_coverage.main(), 1)
            self.assertIn("unreadable", captured.getvalue())
        finally:
            check_coverage.REPORT = original

    def test_main_pass_and_fail_print(self) -> None:
        original = check_coverage.REPORT
        tmp = Path(tempfile.mkdtemp()) / "coverage.json"
        tmp.write_text(json.dumps({"totals": _totals(), "files": _required()}), encoding="utf-8")
        check_coverage.REPORT = tmp
        try:
            captured = io.StringIO()
            with mock.patch("sys.stdout", captured):
                self.assertEqual(check_coverage.main(), 0)
            self.assertIn("statement 95.00%", captured.getvalue())
        finally:
            check_coverage.REPORT = original
        tmp.write_text(json.dumps({
            "totals": _totals(covered_lines=1),
            "files": _required(),
        }), encoding="utf-8")
        check_coverage.REPORT = tmp
        try:
            captured = io.StringIO()
            with mock.patch("sys.stdout", captured):
                self.assertEqual(check_coverage.main(), 1)
            self.assertIn("COVERAGE_STATEMENT:", captured.getvalue())
        finally:
            check_coverage.REPORT = original

    def test_percentages_and_bad_number(self) -> None:
        statement, branch = check_coverage.percentages(_totals(94, 100, 100, 100))
        self.assertAlmostEqual(statement, 94.0)
        self.assertAlmostEqual(branch, 100.0)
        with self.assertRaises(TypeError):
            check_coverage._number("x")
        with self.assertRaises(TypeError):
            check_coverage._number(True)
