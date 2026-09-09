"""The report parser and the committed Lean record."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_lean import ALLOWED_AXIOMS, MODULES, RECORD, parse_reports  # noqa: E402

CENSUS = "EXECUTION_THEOREM: Execution.run_encode"
BRIDGE = ("Execution.lookup_mem", "Execution.lookup_isSome", "Execution.lookup_encode",
          "Execution.run_evalWord", "Execution.run_word", "Execution.evalWord_append",
          "Execution.run_append", "Execution.iterate_add", "Execution.evalWord_encode",
          "Execution.run_encode", "Execution.run_total", "Execution.run_lt", "Execution.run_nil",
          "Control.encodeC_wf", "Control.lookup_program_op", "Control.enabled_program",
          "Control.fire_ok", "Control.fire_exhausted", "Control.mem_successors",
          "Control.successors_sound", "Control.successors_complete", "Control.init_pair",
          "Control.live_successor", "Control.stepDet_branch", "Control.runDet_branch",
          "Control.run_branch", "Product.left_right_comm", "Product.prod_comm",
          "Product.coupling_breaks_the_square", "Product.uncoupled_square_holds",
          "Schedule.enabledAt_scheduled", "Schedule.scheduled_no_branch",
          "Schedule.step_moves_one_locus", "Schedule.pair_run", "Schedule.pair_terminal",
          "Schedule.square_on_the_outcome", "Schedule.square_fails_on_the_observation",
          "Schedule.locus1_is_its_own_run", "Schedule.locus2_is_its_own_run",
          "Schedule.swap_moves_both",
          "Rename.rename_op", "Rename.rename_enabledAt", "Rename.rename_lookup",
          "Rename.rename_stepDet", "Rename.rename_runDet", "Rename.rename_run",
          "Rename.rename_tape", "Rename.not_a_renaming",
          "Runner.stepDetOf_of_two", "Runner.stepDetOf_branch_iff", "Runner.ctrl_branch_iff",
          "Runner.stepDetOf_inr", "Runner.stepDetOf_spec", "Runner.stepDetOf_branch",
          "Runner.runDetOf_branch", "Runner.obsOf_prefix_add", "Runner.ctrl_stepDet",
          "Runner.ctrl_runDet", "Runner.blind_halts", "Runner.greedy_branches")


class ReportParser(unittest.TestCase):
    def test_accepts_primed_theorem_names(self) -> None:
        self.assertEqual(
            parse_reports("'Execution.run_encode'' depends on axioms: [propext]",
                          "EXECUTION_THEOREM: Execution.run_encode'"),
            {"Execution.run_encode'": ["propext"]})

    def test_incomplete_or_disallowed_reports_fail_by_name(self) -> None:
        cases = [
            ("", "", "empty"),
            ("", CENSUS, "missing"),
            ("'Execution.other' does not depend on any axioms", CENSUS, "mismatch"),
            ("'Execution.run_encode' depends on axioms: [Classical.choice]", CENSUS, "disallowed"),
            ("'Execution.run_encode' does not depend on any axioms\n"
             "'Execution.run_encode' does not depend on any axioms", CENSUS, "duplicate report"),
            ("'Execution.run_encode' does not depend on any axioms", CENSUS + "\n" + CENSUS,
             "duplicate environment"),
            ("'Execution.run_encode' does not depend on any axioms\n"
             "'Execution.extra' does not depend on any axioms", CENSUS, "extra"),
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
        """The generated population is the **complement** of the authored one,
        not a second count by a name heuristic.  Two independently pinned
        numbers can drift apart and did: the README once put the `Renaming`
        field projections inside a heuristic count that excluded them, so
        authored + generated did not reach the total and nothing noticed."""
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        authored = {line.split("#print axioms ")[1].strip()
                    for module in MODULES
                    for line in (RECORD.parents[1] / "lean" / f"{module}.lean")
                    .read_text(encoding="utf-8").splitlines()
                    if line.startswith("#print axioms ")}
        reports = set(record["reports"])
        generated = reports - authored
        self.assertEqual(authored - reports, set(), "an authored report is not in the record")
        self.assertEqual(len(authored) + len(generated), len(reports))
        self.assertEqual(len(authored), 114)
        self.assertEqual(len(generated), 59)
        self.assertEqual(record["theorem_count_including_generated"], 173)
        self.assertEqual(record["axiom_free_count"], 42)
        self.assertEqual(record["reports_per_namespace"],
                         {"Execution": 24, "Control": 49, "Product": 19,
                          "Schedule": 30, "Rename": 30, "Runner": 21})

    def test_the_generated_population_breaks_down_exhaustively(self) -> None:
        """Every generated name is one of six kinds, and the six partition it:
        the README's breakdown is checked to be a partition, not a list that
        happens to be near the total."""
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        authored = {line.split("#print axioms ")[1].strip()
                    for module in MODULES
                    for line in (RECORD.parents[1] / "lean" / f"{module}.lean")
                    .read_text(encoding="utf-8").splitlines()
                    if line.startswith("#print axioms ")}
        generated = set(record["reports"]) - authored

        def kind(name: str) -> str:
            if "instDecidable" in name:
                return "decidable equality"
            if "._proof_" in name:
                return "proof term"
            if name.endswith((".inj", ".injEq")):
                return "constructor injectivity"
            if "sizeOf_spec" in name:
                return "size specification"
            if "ofNat_ctorIdx" in name:
                return "constructor index"
            return "field projection"

        counts: dict[str, int] = {}
        for name in generated:
            counts[kind(name)] = counts.get(kind(name), 0) + 1
        self.assertEqual(counts, {"constructor injectivity": 10, "proof term": 31,
                                  "size specification": 11, "field projection": 4,
                                  "constructor index": 1, "decidable equality": 2})
        self.assertEqual(sum(counts.values()), len(generated))
        # The four field projections are `Renaming`'s Prop-valued fields, which
        # Lean classifies as theorems.  They are a kind of their own and not
        # inside the proof terms, which is where the README once put them.
        self.assertEqual({name for name in generated if kind(name) == "field projection"},
                         {"Rename.Renaming.fwd_lt", "Rename.Renaming.bwd_lt",
                          "Rename.Renaming.left", "Rename.Renaming.right"})


if __name__ == "__main__":
    unittest.main()
