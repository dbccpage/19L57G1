"""The report parser and the committed Lean record."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_lean import ALLOWED_AXIOMS, MODULES, RECORD, parse_reports  # noqa: E402

CENSUS = "MAGNIFICATION_THEOREM: Restart.cut"


class ReportParser(unittest.TestCase):
    def test_accepts_primed_theorem_names(self) -> None:
        self.assertEqual(
            parse_reports("'Restart.cut'' depends on axioms: [propext]", "MAGNIFICATION_THEOREM: Restart.cut'"),
            {"Restart.cut'": ["propext"]})

    def test_incomplete_or_disallowed_reports_fail_by_name(self) -> None:
        cases = [
            ("", "", "empty"),
            ("", CENSUS, "missing"),
            ("'Restart.other' does not depend on any axioms", CENSUS, "mismatch"),
            ("'Restart.cut' depends on axioms: [Classical.choice]", CENSUS, "disallowed"),
            ("'Restart.cut' does not depend on any axioms\n'Restart.cut' does not depend on any axioms",
             CENSUS, "duplicate report"),
            ("'Restart.cut' does not depend on any axioms", CENSUS + "\n" + CENSUS, "duplicate environment"),
            ("'Restart.cut' does not depend on any axioms\n'Restart.extra' does not depend on any axioms",
             CENSUS, "extra"),
        ]
        for log, census, reason in cases:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(ValueError, reason):
                    parse_reports(log, census)


class CommittedRecord(unittest.TestCase):
    def test_record_is_within_the_whitelist_and_covers_the_three_namespaces(self) -> None:
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        reports = record["reports"]
        self.assertEqual(record["theorem_count_including_generated"], len(reports))
        self.assertEqual(record["axiom_free_count"], sum(1 for v in reports.values() if not v))
        for name, axioms in reports.items():
            self.assertTrue(any(name.startswith(m + ".") for m in MODULES), name)
            self.assertTrue(set(axioms) <= ALLOWED_AXIOMS, name)
        per = record["reports_per_namespace"]
        self.assertEqual(sum(per.values()), len(reports))
        for theorem in ("EngineClass.isMin_no_rule", "EngineClass.good_rooted", "EngineClass.rooted_replays",
                        "Restart.path_append_iff", "Restart.path_cut_unique", "Restart.rooted_restart",
                        "Restart.fire_rename", "Restart.fire_auto", "Restart.not_orbitRep_rootF_12",
                        "Restart.orbitRep_rootF_01", "Magnification.fresh_form_valid",
                        "Magnification.bare_round_embeds", "Magnification.context_changes_minimum",
                        "Magnification.induced_constant"):
            self.assertIn(theorem, reports)
        self.assertEqual(record["python_driver_refinement"], "NOT_PROVED")


if __name__ == "__main__":
    unittest.main()
