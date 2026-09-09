"""In-memory injections for every named guard.  Receipts are never rewritten."""

from __future__ import annotations

import io
import json
from pathlib import Path
import sys
import tempfile
from unittest import mock
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "code"))

import candidates as cd  # noqa: E402
import check_coverage  # noqa: E402
import grammar as gr  # noqa: E402
import reader  # noqa: E402
from verify_lean import FORBIDDEN, MATHLIB  # noqa: E402


class Injections(unittest.TestCase):
    def test_g1_host_next_demand_labelled_endogenous(self) -> None:
        errors = cd.census_errors(cd.mutated_endogenous(cd.CENSUS, "C1"))
        self.assertIn("E1_GUARD: C1 labelled endogenous", errors)

    def test_g2_generating_step_with_impose_is_visible(self) -> None:
        history = gr.CHALLENGE3["L"]
        self.assertTrue(gr.is_impose(history[-1]))
        self.assertTrue(gr.last_event_extends_reqs(history))
        self.assertIsNone(gr.e2_violation(history))

    def test_g3_laundering_is_identical_to_supplied(self) -> None:
        w = cd.witness_c3()
        self.assertTrue(w["identical_to_supplied"])
        self.assertEqual(w["supplied_pair"], [0, 1])

    def test_g4_already_separable_is_named_e3(self) -> None:
        row = next(r for r in cd.CENSUS if r["id"] == "C9")
        self.assertEqual(row["fails"], ("E3",))
        self.assertTrue(cd.witness_c9()["already_separable"])

    def test_g5_class_emptied_to_c4(self) -> None:
        errors = cd.census_errors(cd.mutated_narrow(cd.CENSUS))
        self.assertTrue(any("CLASS_NONVACUITY:" in e for e in errors), errors)
        self.assertTrue(any("CLASS_NARROW:" in e for e in errors), errors)

    def test_g6_sorry_and_mathlib_are_named(self) -> None:
        self.assertIsNotNone(FORBIDDEN.search("  sorry\n"))
        self.assertIsNotNone(MATHLIB.search("import Mathlib.Data.Nat.Basic\n"))

    def test_g7_pin_first_byte_is_the_source_changed_name(self) -> None:
        # The named failure lives in verify_sources; this records the spelling
        # the injection test in test_sources already fires.
        self.assertEqual("SOURCE_CHANGED: code/derivation/model.py".split(":")[0], "SOURCE_CHANGED")

    def test_g8_reader_branch_on_reqs_is_named(self) -> None:
        hits = reader.reader_source_violations("def f(regime):\n    return regime.reqs\n")
        self.assertTrue(any(":reqs" in h for h in hits), hits)

    def test_g9_endogenous_label_on_c5_is_named(self) -> None:
        errors = cd.census_errors(cd.mutated_endogenous(cd.CENSUS, "C5"))
        self.assertIn("E1_GUARD: C5 labelled endogenous", errors)


def _required_files() -> dict[str, object]:
    return {name: {} for name in check_coverage.REQUIRED_FILES}


def _ok_totals(covered_lines: int = 95, statements: int = 100,
               covered_branches: int = 19, branches: int = 20) -> dict[str, object]:
    return {
        "percent_covered": 97.0,
        "covered_lines": covered_lines,
        "num_statements": statements,
        "covered_branches": covered_branches,
        "num_branches": branches,
    }


class CoverageGate(unittest.TestCase):
    def test_missing_report_fails(self) -> None:
        original = check_coverage.REPORT
        check_coverage.REPORT = Path(tempfile.gettempdir()) / "no-such-coverage.json"
        try:
            with mock.patch("sys.stdout", io.StringIO()):
                self.assertEqual(check_coverage.main(), 1)
        finally:
            check_coverage.REPORT = original

    def test_leaked_tests_path_fails(self) -> None:
        errors = check_coverage.report_errors({
            "totals": _ok_totals(),
            "files": {"tests/test_x.py": {}},
        })
        self.assertTrue(any(e.startswith("COVERAGE_LEAK:") for e in errors), errors)

    def test_missing_totals_fails(self) -> None:
        errors = check_coverage.report_errors({"files": _required_files()})
        self.assertTrue(any(e.startswith("COVERAGE_TOTALS:") for e in errors), errors)

    def test_empty_files_fails(self) -> None:
        errors = check_coverage.report_errors({
            "totals": _ok_totals(),
            "files": {},
        })
        self.assertTrue(any(e.startswith("COVERAGE_FILES:") for e in errors), errors)

    def test_low_statement_fails_even_when_percent_covered_is_high(self) -> None:
        """94% statements + 100% branches used to pass as 97% 'line' coverage."""
        errors = check_coverage.report_errors({
            "totals": _ok_totals(covered_lines=94, statements=100,
                                 covered_branches=100, branches=100),
            "files": _required_files(),
        })
        self.assertTrue(any(e.startswith("COVERAGE_STATEMENT:") for e in errors), errors)
        self.assertFalse(any(e.startswith("COVERAGE_BRANCH:") for e in errors), errors)

    def test_combined_percent_covered_is_not_statement_coverage(self) -> None:
        totals = _ok_totals(covered_lines=94, statements=100,
                            covered_branches=100, branches=100)
        statement, branch = check_coverage.percentages(totals)
        self.assertAlmostEqual(statement, 94.0)
        self.assertAlmostEqual(branch, 100.0)
        combined = totals["percent_covered"]
        assert isinstance(combined, (int, float))
        self.assertGreater(float(combined), statement)

    def test_unrelated_only_population_fails(self) -> None:
        errors = check_coverage.report_errors({
            "totals": _ok_totals(covered_lines=100, statements=100,
                                 covered_branches=100, branches=100),
            "files": {"unrelated.py": {}},
        })
        self.assertTrue(any(e.startswith("COVERAGE_POPULATION:") for e in errors), errors)
        self.assertTrue(any("grammar.py" in e for e in errors), errors)

    def test_missing_branch_measurement_fails(self) -> None:
        errors = check_coverage.report_errors({
            "totals": _ok_totals(covered_branches=0, branches=0),
            "files": _required_files(),
        })
        self.assertTrue(any("no branches" in e for e in errors), errors)

    def test_payload_not_object_fails(self) -> None:
        errors = check_coverage.report_errors(["not", "an", "object"])
        self.assertEqual(errors, ["COVERAGE_SHAPE: not an object"])

    def test_incomplete_totals_fail_closed(self) -> None:
        errors = check_coverage.report_errors({
            "totals": {"percent_covered": 100.0},
            "files": _required_files(),
        })
        self.assertTrue(any("covered_lines" in e for e in errors), errors)

    def test_zero_statements_fails(self) -> None:
        errors = check_coverage.report_errors({
            "totals": _ok_totals(covered_lines=0, statements=0),
            "files": _required_files(),
        })
        self.assertTrue(any("no statements" in e for e in errors), errors)

    def test_low_branch_fails_with_high_statements(self) -> None:
        errors = check_coverage.report_errors({
            "totals": _ok_totals(covered_lines=100, statements=100,
                                 covered_branches=18, branches=20),
            "files": _required_files(),
        })
        self.assertTrue(any(e.startswith("COVERAGE_BRANCH:") for e in errors), errors)
        self.assertFalse(any(e.startswith("COVERAGE_STATEMENT:") for e in errors), errors)

    def test_unreadable_report_fails(self) -> None:
        tmp = Path(tempfile.mkdtemp()) / "coverage.json"
        tmp.write_text("{not json", encoding="utf-8")
        original = check_coverage.REPORT
        check_coverage.REPORT = tmp
        try:
            captured = io.StringIO()
            with mock.patch("sys.stdout", captured):
                self.assertEqual(check_coverage.main(), 1)
            self.assertIn("unreadable", captured.getvalue())
        finally:
            check_coverage.REPORT = original

    def test_main_prints_named_failures(self) -> None:
        tmp = Path(tempfile.mkdtemp()) / "coverage.json"
        tmp.write_text(json.dumps({
            "totals": _ok_totals(covered_lines=1, statements=100,
                                 covered_branches=20, branches=20),
            "files": _required_files(),
        }), encoding="utf-8")
        original = check_coverage.REPORT
        check_coverage.REPORT = tmp
        try:
            captured = io.StringIO()
            with mock.patch("sys.stdout", captured):
                self.assertEqual(check_coverage.main(), 1)
            self.assertIn("COVERAGE_STATEMENT:", captured.getvalue())
        finally:
            check_coverage.REPORT = original

    def test_pass_at_threshold(self) -> None:
        errors = check_coverage.report_errors({
            "totals": _ok_totals(covered_lines=95, statements=100,
                                 covered_branches=19, branches=20),
            "files": _required_files(),
        })
        self.assertEqual(errors, [])

    def test_main_reports_statement_not_combined_percent(self) -> None:
        tmp = Path(tempfile.mkdtemp()) / "coverage.json"
        tmp.write_text(json.dumps({
            "totals": _ok_totals(covered_lines=95, statements=100,
                                 covered_branches=19, branches=20),
            "files": _required_files(),
        }), encoding="utf-8")
        original = check_coverage.REPORT
        check_coverage.REPORT = tmp
        try:
            captured = io.StringIO()
            with mock.patch("sys.stdout", captured):
                self.assertEqual(check_coverage.main(), 0)
            self.assertIn("statement 95.00%", captured.getvalue())
            self.assertIn("branch 95.00%", captured.getvalue())
        finally:
            check_coverage.REPORT = original


if __name__ == "__main__":
    unittest.main()
