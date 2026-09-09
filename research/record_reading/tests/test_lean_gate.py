"""The report parser and the committed Lean record."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_lean import ALLOWED_AXIOMS, MODULES, RECORD, parse_reports  # noqa: E402

CENSUS = "RECORD_THEOREM: Record.twist_tape"
BRIDGE = ("Record.encodeR_wf", "Record.renabled_rprogram", "Record.previous_fire", "Record.rsuccessors_sound",
          "Record.rsuccessors_complete", "Record.lift_RStep", "Record.lift_renabled", "Record.twist_tape",
          "Record.record_is_read", "Record.memoryless_functional", "Record.forget_twist", "Record.rrun_branch",
          "Record.robs_prefix", "Select.stepDet_spec", "Select.obs_bisim", "Select.obs_take",
          "Select.forever_differ", "Select.forever_indistinguishable", "Select.turncoat_agrees",
          "Select.turncoat_differs_scale", "Select.turncoat_differs_start",
          "Record.rstepDet_spec", "Select.robs_bisim", "Select.robs_take",
          "Record.robs_functional", "Record.rchain_functional",
          "Depth.encodeR2_wf", "Depth.twist2_tape", "Depth.no_record_run_realises",
          "Depth.depth_two_is_deeper", "Depth.r2enabled_r2program")


class ReportParser(unittest.TestCase):
    def test_accepts_primed_theorem_names(self) -> None:
        self.assertEqual(
            parse_reports("'Record.twist_tape'' depends on axioms: [propext]",
                          "RECORD_THEOREM: Record.twist_tape'"),
            {"Record.twist_tape'": ["propext"]})

    def test_incomplete_or_disallowed_reports_fail_by_name(self) -> None:
        cases = [
            ("", "", "empty"),
            ("", CENSUS, "missing"),
            ("'Record.other' does not depend on any axioms", CENSUS, "mismatch"),
            ("'Record.twist_tape' depends on axioms: [Classical.choice]", CENSUS, "disallowed"),
            ("'Record.twist_tape' does not depend on any axioms\n"
             "'Record.twist_tape' does not depend on any axioms", CENSUS, "duplicate report"),
            ("'Record.twist_tape' does not depend on any axioms", CENSUS + "\n" + CENSUS,
             "duplicate environment"),
            ("'Record.twist_tape' does not depend on any axioms\n"
             "'Record.extra' does not depend on any axioms", CENSUS, "extra"),
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
        self.assertEqual(authored, 86)
        self.assertEqual(record["theorem_count_including_generated"], 120)
        self.assertEqual(record["axiom_free_count"], 6)
        self.assertEqual(record["reports_per_namespace"], {"Record": 58, "Select": 28, "Depth": 34})
        self.assertEqual(record["reports"]["Select.obs_bisim"], ["Quot.sound", "propext"])
        self.assertEqual(record["reports"]["Record.memoryless_functional"], ["propext"])
        self.assertEqual(record["reports"]["Record.previous_fire"], ["propext"])


if __name__ == "__main__":
    unittest.main()
