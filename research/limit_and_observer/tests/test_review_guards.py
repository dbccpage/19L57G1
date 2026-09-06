"""Regressions for the concrete counterexamples found during PR review."""
from dataclasses import replace
import contextlib
import io
import os
import unittest
from unittest.mock import mock_open, patch

import check_coverage

from code.demands import Situation, obs4_coexistence, reads_only_the_stage
from code.items import (
    AddContext, NewDatum, NewForm, NewInst, NewReader, NewRuleAll,
    StatedState, apply_delta, canonical_delta, capabilities,
)
from code.readers import ADMISSION_ONLY_READING, SEALED_READING, lawful
from code.regime import AdmissionRefused, genesis
from run_price import width_only_countermodel
from code.enumerate_space import DEFAULT_BOUNDS
from code.quotient import canonical_state
from verify_lean import CENSUS_ROOT, check_import_closure, parse_reports
from verify_prose import check_scores


class ReviewCounterexamples(unittest.TestCase):
    def test_obs4_transports_reading_and_aggregation_too(self):
        a = (False, True, True, True)
        base = genesis("F")
        delta = canonical_delta((
            NewForm(2), NewInst(0, (0, 0)), NewInst(0, (2, 2)),
            NewReader(ADMISSION_ONLY_READING, a), NewReader(SEALED_READING, a),
            AddContext(0, (0, (None, 0))), AddContext(1, (0, (None, 2))),
        ))
        state = apply_delta(StatedState(base, ()), delta, 3, 2)
        self.assertTrue(obs4_coexistence(Situation(base, delta, state, (0, 1), 3)))
        from code.demands import renaming_of_each_other
        rho = state.readers[0]
        self.assertFalse(renaming_of_each_other(
            state.regime, rho, replace(rho, aggregation=(False, True, False, True))))

    def test_replay_refuses_unlawful_or_malformed_readers(self):
        unlawful = (False, False, False, True)
        self.assertFalse(lawful(unlawful, 3))
        for reader in (
            NewReader(SEALED_READING, unlawful),
            NewReader(SEALED_READING, (False, True)),
            NewReader(SEALED_READING, (False, True, True, 1)),
            NewReader((False, True, True), (False, True, True, True)),
            NewReader((False, True, True, 1), (False, True, True, True)),
        ):
            with self.subTest(reader=reader), self.assertRaises(AdmissionRefused):
                apply_delta(StatedState(genesis("F"), ()), (reader,), 3, 2)

    def test_equal_behaviour_does_not_erase_the_frozen_reader_class(self):
        aggregation = (False, True, True, True)
        base = genesis("F")
        delta = canonical_delta((
            NewForm(2), NewInst(0, (0, 0)), NewInst(0, (2, 2)),
            NewReader(ADMISSION_ONLY_READING, aggregation),
            NewReader((False, True, True, False), aggregation),
            AddContext(0, (0, (None, 0))), AddContext(1, (0, (None, 2))),
        ))
        state = apply_delta(StatedState(base, ()), delta, 3, 2)
        self.assertTrue(obs4_coexistence(Situation(base, delta, state, (0, 1), 3)))
        same_class = replace(state, readers=(state.readers[0], replace(
            state.readers[1], reading=ADMISSION_ONLY_READING)))
        self.assertNotEqual(canonical_state(state), canonical_state(same_class))
        from code.enumerate_space import reader_suffixes
        from code.readers import all_reading_classes
        suffixes = tuple(reader_suffixes(base, 1, DEFAULT_BOUNDS))
        self.assertEqual({d[0].reading for d in suffixes}, set(all_reading_classes()))

    def test_all_six_item_kinds_reject_an_added_stage_field(self):
        items = (
            NewDatum(), NewForm(1), NewInst(0, (0,)), NewRuleAll(0),
            NewReader(SEALED_READING, (False, True, True, True)),
            AddContext(0, (0, (None,))),
        )
        for item in items:
            self.assertTrue(reads_only_the_stage((item,)))
            object.__setattr__(item, "stage", 1)
            with self.subTest(kind=type(item).__name__):
                self.assertFalse(reads_only_the_stage((item,)))
                with self.assertRaisesRegex(AdmissionRefused, "fields"):
                    apply_delta(StatedState(genesis("F"), ()), (item,), 3, 2)

    def test_capabilities_record_reader_properties_without_a_scalar_cost(self):
        delta = (NewReader(ADMISSION_ONLY_READING, (False, True, True, True)),)
        caps = capabilities(delta)
        self.assertEqual(caps["reading_class"], [[False, True, False, True]])
        self.assertEqual(caps["aggregation_lawful"], [True])
        self.assertEqual(len(caps), 9)

    def test_more_width_cannot_repair_equal_raw_signatures(self):
        countermodel = width_only_countermodel(DEFAULT_BOUNDS)
        self.assertGreater(countermodel["available_contexts"], 3)
        self.assertGreater(countermodel["reader_selections_checked"], 0)
        self.assertTrue(countermodel["all_readers_fail"])

    def test_primed_names_are_reported_and_population_must_match(self):
        name = "LimitObserver.probe'"
        marker = f"LIMIT_OBSERVER_DECL {name}\n"
        report = f"'{name}' does not depend on any axioms\n"
        self.assertEqual(parse_reports(marker + report), [f"{name}: []"])
        with self.assertRaisesRegex(ValueError, "missing=.*probe"):
            parse_reports(marker)
        with self.assertRaisesRegex(ValueError, "population"):
            parse_reports(report)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            parse_reports(marker + report + report)
        with self.assertRaisesRegex(ValueError, "Classical.choice"):
            parse_reports(marker + f"'{name}' depends on axioms: [Classical.choice]\n")

    def test_importing_a_new_module_does_not_extend_the_theorem_census(self):
        sources = {CENSUS_ROOT: "root.lean", "LimitObserver": "main.lean",
                   "LimitObserver.Probe": "probe.lean"}
        body = "import LimitObserver\nimport LimitObserver.Probe\n"
        output = io.StringIO()
        with patch("verify_lean.module_census", return_value=sources), \
                patch("builtins.open", mock_open(read_data=body)), \
                contextlib.redirect_stdout(output), self.assertRaises(SystemExit):
            check_import_closure([])
        self.assertIn("outside the declared theorem census", output.getvalue())
        self.assertIn("LimitObserver.Probe", output.getvalue())

    def test_line_and_branch_thresholds_are_independent(self):
        source = os.path.join("code", "probe.py")
        for lines, branches, failure in (
            (94, 100, "line coverage 94.00%"),
            (100, 94, "branch coverage 94.00%"),
            (100, 100, None),
        ):
            totals = {"covered_lines": lines, "num_statements": 100,
                      "covered_branches": branches, "num_branches": 100,
                      "percent_covered": (lines + branches) / 2}
            report = {"files": {source: {"summary": totals}}, "totals": totals,
                      "meta": {"timestamp": "2026-09-06T00:00:00"}}
            output = io.StringIO()
            with self.subTest(lines=lines, branches=branches), \
                    patch("check_coverage.os.path.isfile", return_value=True), \
                    patch("check_coverage.os.path.getmtime", return_value=0), \
                    patch("check_coverage.os.walk", return_value=[(
                        os.path.join(check_coverage.HERE, "code"), [], ["probe.py"])]), \
                    patch("builtins.open", mock_open()), \
                    patch("check_coverage.json.load", return_value=report), \
                    contextlib.redirect_stdout(output):
                if failure:
                    with self.assertRaises(SystemExit):
                        check_coverage.main()
                else:
                    check_coverage.main()
            self.assertIn(failure or "coverage clean", output.getvalue())

    def test_mixed_prediction_rows_are_not_silently_skipped(self):
        scores = {
            "P-10-no-finite-delta": True,
            "P-10-smallest-extension-UNTESTED": False,
            "P-18-no-observer-purchases-a-limit": True,
            "P-18-refinement-purchases-growth-UNTESTED": False,
        }
        receipt = {"predictions": {"scores": scores}}
        rows = ("| P-10 | finite delta and extension | first half **HIT**, second half **OPEN** |\n"
                "| P-18 | purchase | first half **HIT**, second half **UNTESTABLE** |\n")
        self.assertEqual(check_scores(receipt, rows), [])
        self.assertTrue(check_scores(receipt, rows.replace("HIT", "MISS", 1)))
        self.assertTrue(check_scores(receipt, rows.splitlines()[0]))
        self.assertTrue(check_scores(receipt, rows.replace("OPEN", "HIT")))
        scores["P-10-no-finite-delta"] = None
        open_rows = rows.replace("first half **HIT**", "first half **OPEN**", 1)
        self.assertEqual(check_scores(receipt, open_rows), [])
        self.assertTrue(check_scores(receipt, rows))
        scores["P-7"] = None
        self.assertEqual(check_scores(receipt, open_rows + "| P-7 | refusal | **OPEN** |\n"), [])
        self.assertTrue(check_scores(receipt, open_rows + "| P-7 | refusal | **MISS** |\n"))


if __name__ == "__main__":
    unittest.main()
