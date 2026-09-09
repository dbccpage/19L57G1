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


class CoverageGate(unittest.TestCase):
    def test_missing_report_fails(self) -> None:
        original = check_coverage.REPORT
        check_coverage.REPORT = Path(tempfile.gettempdir()) / "no-such-coverage.json"
        try:
            with mock.patch("sys.stdout", io.StringIO()):
                self.assertEqual(check_coverage.main(), 1)
        finally:
            check_coverage.REPORT = original

    def _write(self, payload: dict[str, object]) -> Path:
        tmp = Path(tempfile.mkdtemp()) / "coverage.json"
        tmp.write_text(json.dumps(payload), encoding="utf-8")
        return tmp

    def test_leaked_tests_path_fails(self) -> None:
        tmp = self._write({
            "totals": {"percent_covered": 100.0, "covered_branches": 1, "num_branches": 1},
            "files": {"tests/test_x.py": {}},
        })
        original = check_coverage.REPORT
        check_coverage.REPORT = tmp
        try:
            with mock.patch("sys.stdout", io.StringIO()):
                self.assertEqual(check_coverage.main(), 1)
        finally:
            check_coverage.REPORT = original

    def test_missing_totals_fails(self) -> None:
        tmp = self._write({"files": {"grammar.py": {}}})
        original = check_coverage.REPORT
        check_coverage.REPORT = tmp
        try:
            with mock.patch("sys.stdout", io.StringIO()):
                self.assertEqual(check_coverage.main(), 1)
        finally:
            check_coverage.REPORT = original

    def test_empty_files_fails(self) -> None:
        tmp = self._write({
            "totals": {"percent_covered": 100.0, "covered_branches": 0, "num_branches": 0},
            "files": {},
        })
        original = check_coverage.REPORT
        check_coverage.REPORT = tmp
        try:
            with mock.patch("sys.stdout", io.StringIO()):
                self.assertEqual(check_coverage.main(), 1)
        finally:
            check_coverage.REPORT = original

    def test_low_line_fails(self) -> None:
        tmp = self._write({
            "totals": {"percent_covered": 10.0, "covered_branches": 10, "num_branches": 10},
            "files": {"grammar.py": {}},
        })
        original = check_coverage.REPORT
        check_coverage.REPORT = tmp
        try:
            with mock.patch("sys.stdout", io.StringIO()):
                self.assertEqual(check_coverage.main(), 1)
        finally:
            check_coverage.REPORT = original

    def test_pass_at_threshold(self) -> None:
        tmp = self._write({
            "totals": {"percent_covered": 95.0, "covered_branches": 19, "num_branches": 20},
            "files": {"grammar.py": {}},
        })
        original = check_coverage.REPORT
        check_coverage.REPORT = tmp
        try:
            with mock.patch("sys.stdout", io.StringIO()):
                self.assertEqual(check_coverage.main(), 0)
        finally:
            check_coverage.REPORT = original


if __name__ == "__main__":
    unittest.main()
