"""The report parser and the committed Lean record."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_lean import ALLOWED_AXIOMS, MODULES, RECORD, parse_reports  # noqa: E402

CENSUS = "LIMITS_THEOREM: Limits.ofSeq_toSeq"
BRIDGE = ("Limits.toSeq_ofSeq", "Limits.stable", "Limits.ofSeq_toSeq", "Limits.eventual_agrees",
          "Limits.eventual_not_compatible", "Limits.etoSeq_eofSeq", "Limits.estable",
          "Limits.eofSeq_etoSeq", "Limits.thread_even", "Limits.even_thread", "Limits.shift_not_local",
          "Observe.stepDet_inr", "Observe.next_tape", "Observe.obs_prefix", "Observe.obs_prefix_add",
          "Observe.next_active_det", "Observe.lost_fuel")


class ReportParser(unittest.TestCase):
    def test_accepts_primed_theorem_names(self) -> None:
        self.assertEqual(
            parse_reports("'Limits.ofSeq_toSeq'' depends on axioms: [propext]",
                          "LIMITS_THEOREM: Limits.ofSeq_toSeq'"),
            {"Limits.ofSeq_toSeq'": ["propext"]})

    def test_incomplete_or_disallowed_reports_fail_by_name(self) -> None:
        cases = [
            ("", "", "empty"),
            ("", CENSUS, "missing"),
            ("'Limits.other' does not depend on any axioms", CENSUS, "mismatch"),
            ("'Limits.ofSeq_toSeq' depends on axioms: [Classical.choice]", CENSUS, "disallowed"),
            ("'Limits.ofSeq_toSeq' does not depend on any axioms\n"
             "'Limits.ofSeq_toSeq' does not depend on any axioms", CENSUS, "duplicate report"),
            ("'Limits.ofSeq_toSeq' does not depend on any axioms", CENSUS + "\n" + CENSUS,
             "duplicate environment"),
            ("'Limits.ofSeq_toSeq' does not depend on any axioms\n"
             "'Limits.extra' does not depend on any axioms", CENSUS, "extra"),
        ]
        for log, census, reason in cases:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(ValueError, reason):
                    parse_reports(log, census)


class CommittedRecord(unittest.TestCase):
    def test_record_is_within_the_whitelist_and_carries_the_bridge(self) -> None:
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        reports = record["reports"]
        self.assertEqual(record["theorem_count_including_generated"], len(reports))
        self.assertEqual(record["axiom_free_count"], sum(1 for v in reports.values() if not v))
        for name, axioms in reports.items():
            self.assertTrue(any(name.startswith(m + ".") for m in MODULES), name)
            self.assertTrue(set(axioms) <= ALLOWED_AXIOMS, name)
        self.assertEqual(sum(record["reports_per_namespace"].values()), len(reports))
        for theorem in BRIDGE:
            self.assertIn(theorem, reports)
        self.assertEqual(record["python_mirror_refinement"], "NOT_PROVED")

    def test_the_figures_the_readme_quotes(self) -> None:
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        authored = sum(
            1 for module in MODULES
            for line in (RECORD.parents[1] / "lean" / f"{module}.lean").read_text(encoding="utf-8").splitlines()
            if line.startswith("#print axioms ")
        )
        self.assertEqual(authored, 21)
        self.assertEqual(record["theorem_count_including_generated"], 43)
        self.assertEqual(record["axiom_free_count"], 10)
        self.assertEqual(record["reports_per_namespace"], {"Limits": 24, "Observe": 19})
        self.assertEqual(record["reports"]["Observe.zeros_bound"], ["Quot.sound", "propext"])


if __name__ == "__main__":
    unittest.main()
