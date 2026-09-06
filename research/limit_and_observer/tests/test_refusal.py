"""A real small-budget refusal must not certify an interrupted minimum."""
from dataclasses import replace
import copy
import json
import os
import unittest
from unittest.mock import patch

from code.demands import Demand, SINGLE_STATE
from code.enumerate_space import DEFAULT_BOUNDS, CandidateBudgetRefused
from code.items import StatedState, apply_delta
from code.price import PricingTrace, price_many
from code.regime import genesis
from run_price import minimum_json, trace_json
import run_price


class RefusalCertificate(unittest.TestCase):
    def setUp(self):
        self.bounds = replace(DEFAULT_BOUNDS, max_items=2, candidate_budget=3)
        self.demands = (
            Demand("ALWAYS", lambda s: True, SINGLE_STATE, "control"),
            Demand("NEVER", lambda s: False, SINGLE_STATE, "control"),
            Demand("AT-ONE", lambda s: len(s.delta) == 1, SINGLE_STATE, "control"),
        )

    def test_actual_refusal_retains_only_completed_levels(self):
        for reading in ("L", "F"):
            trace = PricingTrace()
            got = price_many(genesis(reading), reading, self.demands,
                             ("mu1", "mu2"), self.bounds, trace=trace,
                             retain_completed_on_refusal=True)
            self.assertEqual(trace.completed_levels, {0: 1})
            self.assertEqual(trace.refused_level, 1)
            self.assertEqual(trace.yielded_at_refusal, 3)
            self.assertEqual(trace.observed_hits_at_refusal, {"NEVER": 0, "AT-ONE": 3})
            self.assertIn("AT-ONE", trace.first_witnesses_at_refusal)
            self.assertIsNotNone(trace.first_refused)
            self.assertIsNotNone(trace.last_yielded)
            for delta in (trace.last_yielded, trace.first_refused):
                self.assertIsNotNone(delta)
                apply_delta(StatedState(genesis(reading), ()), delta, 3, 2)
            for measure in ("mu1", "mu2"):
                done = got[("ALWAYS", measure)]
                self.assertEqual(done.cost[0], 0)
                self.assertTrue(done.cost_below_minimum_all_fail)
                self.assertFalse(done.search_refused)
                for name in ("NEVER", "AT-ONE"):
                    pending = got[(name, measure)]
                    self.assertEqual(pending.raw_minima, ())
                    self.assertEqual(pending.grade, "Refused")
                    self.assertFalse(pending.cost_below_minimum_all_fail)
                    self.assertTrue(pending.search_refused)
                    encoded = minimum_json(pending)
                    self.assertEqual(encoded["outcome"], "OPEN")
                    self.assertIsNone(encoded["cost"])
                    self.assertIsNone(encoded["raw_minimum_count"])
            receipt = trace_json(reading, trace)
            self.assertEqual(receipt["terminal"], "CandidateBudgetRefused")
            self.assertEqual(receipt["first_refused_ordinal"], 4)

    def test_default_still_raises_and_reversal_recovers(self):
        with self.assertRaisesRegex(CandidateBudgetRefused, "item count 1"):
            price_many(genesis("F"), "F", self.demands, ("mu1",), self.bounds)
        trace = PricingTrace()
        got = price_many(genesis("F"), "F", self.demands, ("mu1",),
                         replace(self.bounds, candidate_budget=10000), trace=trace)
        self.assertIsNone(trace.refused_level)
        self.assertEqual(got[("AT-ONE", "mu1")].cost[0], 1)
        self.assertTrue(got[("AT-ONE", "mu1")].cost_below_minimum_all_fail)
        self.assertFalse(got[("NEVER", "mu1")].search_refused)
        self.assertTrue(got[("NEVER", "mu1")].cost_below_minimum_all_fail)
        self.assertEqual(trace_json("F", trace)["terminal"], "COMPLETE")

    def test_metadata_refresh_preserves_the_computed_packet(self):
        path = os.path.join(os.path.dirname(run_price.__file__), "receipts", "price.json")
        with open(path, encoding="utf-8") as fh:
            report = json.load(fh)
        protected = {key: copy.deepcopy(report[key]) for key in (
            "prices", "searches", "censuses", "predictions", "bounds", "scope", "calibration")}
        report["obstructions"]["LIM-G"]["reach_of_the_declared_space"][
            "what_the_empty_price_row_therefore_carries"] = "injected stale description"
        for row in report["comparison"]["table"]:
            row["distinct_induced_relations"] = -99
        run_price.refresh_search_descriptions(report)
        for key, value in protected.items():
            self.assertEqual(report[key], value)
        for row in report["comparison"]["table"]:
            key = f"{row['demand']}|{row['base_reading']}|mu1"
            self.assertEqual(row["distinct_induced_relations"],
                             report["prices"][key]["distinct_induced_relations"])
        self.assertIsNone(report["obstructions"]["LIM-F"]["escape"]["smallest_lifting_admission"])
        self.assertIn("OPEN", report["obstructions"]["LIM-F"]["escape"]["extension_status"])
        once = copy.deepcopy(report)
        run_price.refresh_search_descriptions(report)
        self.assertEqual(report, once)

    def test_comparison_never_reports_zero_relations_for_a_refusal(self):
        store = {}
        for reading in run_price.READINGS:
            priced = price_many(genesis(reading), reading, run_price.DEMANDS,
                                run_price.MEASURES, self.bounds,
                                retain_completed_on_refusal=True)
            store.update({(name, reading, measure): minimum
                          for (name, measure), minimum in priced.items()})
        with patch.object(run_price, "_STORE", store, create=True):
            report = run_price.comparison(self.bounds)
        refused = [row for row in report["table"] if row["incomplete"]]
        self.assertTrue(refused)
        for row in refused:
            self.assertIsNone(row["distinct_induced_relations"])
            self.assertIsNone(row["iso_classes_mu1"])
        self.assertTrue(report["containment_omitted"])


if __name__ == "__main__":
    unittest.main()
