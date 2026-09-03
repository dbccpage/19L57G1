"""Tests for the reach_measure tree.  AuthorityEffect: None."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import dual_side  # noqa: E402
import reach as rch  # noqa: E402
import run_reach  # noqa: E402
import sealed_side  # noqa: E402
from derivation.candidates import NewInst, NewRuleAll  # noqa: E402


class MeasureLaws(unittest.TestCase):
    def test_the_sealed_measures_cannot_tell_the_two_apart(self) -> None:
        # the Lean blindness theorem, recomputed
        inst = (NewInst(0, (0,)),)
        rule = (NewRuleAll(0),)
        self.assertEqual(rch.mu1(inst), rch.mu1(rule))
        self.assertEqual(rch.mu2(inst), rch.mu2(rule))

    def test_reach_is_base_relative(self) -> None:
        w = sealed_side.base_relative_witness()
        self.assertTrue(w["reach_differs_across_bases"], w)
        self.assertNotEqual(w["low_reach"], w["high_reach"])
        self.assertEqual(w["mu1_on_both"], 1)

    def test_reach_is_not_a_refinement_of_the_item_count(self) -> None:
        w = sealed_side.order_inversion_witness()
        self.assertTrue(w["orders_inverted"], w)
        self.assertTrue(w["A_reach_is_positive"], w)

    def test_reach_of_a_single_instance_is_at_most_one(self) -> None:
        for _name, base in sealed_side._pinned_bases():
            for d in range(len(base.data)):
                for f in range(len(base.forms)):
                    if base.forms[f] != 1:
                        continue
                    delta = (NewInst(f, (d,)),)
                    self.assertLessEqual(rch.reach(base, delta), 1, (f, d))


class SealedSide(unittest.TestCase):
    def test_no_rule_appears_among_the_sealed_minima(self) -> None:
        r = sealed_side.report()
        rows = r["readings"]
        assert isinstance(rows, list)
        for row in rows:
            self.assertFalse(row["any_rule_item"], row["reading"])
            self.assertEqual(row["kinds"], ["form+inst"], row["reading"])

    def test_reach_narrows_the_sealed_tie_as_far_as_the_refined_measure(self) -> None:
        r = sealed_side.report()
        rows = r["readings"]
        assert isinstance(rows, list)
        for row in rows:
            self.assertLess(row["mu3_minima"], row["mu1_minima"], row["reading"])
            self.assertEqual(row["mu3_minima"], row["mu2_minima"], row["reading"])
            self.assertTrue(row["mu2_and_mu3_agree"], row["reading"])


class DualSide(unittest.TestCase):
    rows: list[dict[str, object]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = [r for r in dual_side.demand_rows() if not r["no_response"]]

    def test_every_demand_is_answered_under_the_retraction(self) -> None:
        self.assertEqual(len(self.rows), 51)

    def test_reach_never_widens_the_valid_set(self) -> None:
        for r in self.rows:
            self.assertLessEqual(
                int(str(r["mu3_minima"])), int(str(r["valid_at_min_items"])), r["target"]
            )

    def test_some_demands_admit_only_a_global_response(self) -> None:
        only_rules = [r for r in self.rows
                      if r["rule_available"] and not r["inst_available"]]
        self.assertGreater(len(only_rules), 0)

    def test_no_demand_admits_only_a_local_response(self) -> None:
        only_inst = [r for r in self.rows
                     if r["inst_available"] and not r["rule_available"]]
        self.assertEqual(len(only_inst), 0)

    def test_reach_halves_the_cross_kind_ties(self) -> None:
        mu1 = len([r for r in self.rows if len(r["mu1_kinds"]) > 1])  # type: ignore[arg-type]
        mu3 = len([r for r in self.rows if len(r["mu3_kinds"]) > 1])  # type: ignore[arg-type]
        self.assertLess(mu3, mu1)

    def test_a_rule_is_not_global_by_syntax(self) -> None:
        # the recorded refutation: a rule whose form has one plugging left
        # has the same reach as an instance, and reach says so
        equal = [r for r in self.rows
                 if r["inst_available"] and r["rule_available"]
                 and not r["mu3_selected_inst_over_rule"]]
        self.assertGreater(len(equal), 0)
        for r in equal:
            self.assertEqual(r["reach_values"], [1], r["target"])


class ReceiptTests(unittest.TestCase):
    def test_committed_receipt_replays_byte_for_byte(self) -> None:
        report = run_reach.build()
        want = (HERE / "receipts" / "reach_measure.json").read_bytes()
        got = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
        self.assertEqual(got, want)


if __name__ == "__main__":
    unittest.main()
