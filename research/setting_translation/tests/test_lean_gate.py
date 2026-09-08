"""The report parser and the committed Lean record."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_lean import ALLOWED_AXIOMS, MODULES, RECORD, parse_reports  # noqa: E402

CENSUS = "TRANSLATION_THEOREM: Chains.cut"


class ReportParser(unittest.TestCase):
    def test_accepts_primed_theorem_names(self) -> None:
        self.assertEqual(
            parse_reports("'Chains.cut'' depends on axioms: [propext]", "TRANSLATION_THEOREM: Chains.cut'"),
            {"Chains.cut'": ["propext"]})

    def test_incomplete_or_disallowed_reports_fail_by_name(self) -> None:
        cases = [
            ("", "", "empty"),
            ("", CENSUS, "missing"),
            ("'Chains.other' does not depend on any axioms", CENSUS, "mismatch"),
            ("'Chains.cut' depends on axioms: [Classical.choice]", CENSUS, "disallowed"),
            ("'Chains.cut' does not depend on any axioms\n'Chains.cut' does not depend on any axioms",
             CENSUS, "duplicate report"),
            ("'Chains.cut' does not depend on any axioms", CENSUS + "\n" + CENSUS, "duplicate environment"),
            ("'Chains.cut' does not depend on any axioms\n'Chains.extra' does not depend on any axioms",
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
        for theorem in ("Translation.encode_wf", "Translation.derivable_rel", "Translation.derivable_op",
                        "Translation.A_iff", "Translation.Bs_iff", "Translation.Bc_iff", "Translation.Bl_iff",
                        "Translation.C_iff", "Translation.D_iff", "Translation.F_iff", "Translation.W_iff",
                        "Chains.E_iff", "Chains.E_iff_noChain", "Chains.shorten", "Chains.clos_word",
                        "Chains.word_in_clos", "Visible.separable_iff_visible",
                        "Visible.collapsed_iff_not_visible", "Visible.A_separable",
                        "Visible.witness_alone_invisible", "Visible.A_no_fire", "Visible.one_inst_min",
                        "Visible.link_valid", "Visible.self_valid", "Visible.link_min", "Visible.self_min",
                        "Visible.encode_link_min", "Visible.encode_self_min", "Visible.A_separable_rev",
                        "Visible.noPair_fires_self", "Visible.noPair_fires_link", "Visible.everyPair_fires",
                        "Visible.seed_embeds", "Transcription.d2Bare_not_bs", "Transcription.boolEmpty_e",
                        "Transcription.triProtected_f"):
            self.assertIn(theorem, reports)
        self.assertEqual(record["python_mirror_refinement"], "NOT_PROVED")

    def test_the_figures_the_readme_quotes(self) -> None:
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        authored = sum(
            1 for module in MODULES
            for line in (RECORD.parents[1] / "lean" / f"{module}.lean").read_text(encoding="utf-8").splitlines()
            if line.startswith("#print axioms ")
        )
        self.assertEqual(authored, 144)
        self.assertEqual(record["theorem_count_including_generated"], 176)
        self.assertEqual(record["axiom_free_count"], 22)
        self.assertEqual(record["reports_per_namespace"],
                         {"Translation": 51, "Chains": 24, "Visible": 51, "Transcription": 50})


if __name__ == "__main__":
    unittest.main()
