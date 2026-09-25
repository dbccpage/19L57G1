"""The report parser, forbidden tokens, and the committed Lean record."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verify_lean import (  # noqa: E402
    ALLOWED_AXIOMS,
    EXPECTED_FILES,
    FORBIDDEN,
    LEAN,
    MATHLIB,
    RECORD,
    REPORTING_MODULES,
    check_written,
    parse_reports,
    strip_comments,
    written_census,
    written_theorems,
)

CENSUS = "ENDOGENOUS_DEMAND_THEOREM: EndogenousDemand.cut"


class ReportParser(unittest.TestCase):
    def test_accepts_primed_theorem_names(self) -> None:
        self.assertEqual(
            parse_reports(
                "'EndogenousDemand.cut'' depends on axioms: [propext]",
                "ENDOGENOUS_DEMAND_THEOREM: EndogenousDemand.cut'",
            ),
            {"EndogenousDemand.cut'": ["propext"]},
        )

    def test_axiom_free_report(self) -> None:
        self.assertEqual(
            parse_reports("'EndogenousDemand.cut' does not depend on any axioms", CENSUS),
            {"EndogenousDemand.cut": []},
        )

    def test_incomplete_or_disallowed_reports_fail_by_name(self) -> None:
        cases = [
            ("", "", "empty"),
            ("", CENSUS, "missing"),
            ("'EndogenousDemand.other' does not depend on any axioms", CENSUS, "mismatch"),
            ("'EndogenousDemand.cut' depends on axioms: [Classical.choice]", CENSUS, "disallowed"),
            (
                "'EndogenousDemand.cut' does not depend on any axioms\n"
                "'EndogenousDemand.cut' does not depend on any axioms",
                CENSUS,
                "duplicate report",
            ),
            (
                "'EndogenousDemand.cut' does not depend on any axioms",
                CENSUS + "\n" + CENSUS,
                "duplicate environment",
            ),
            (
                "'EndogenousDemand.cut' does not depend on any axioms\n"
                "'EndogenousDemand.extra' does not depend on any axioms",
                CENSUS,
                "extra",
            ),
        ]
        for log, census, reason in cases:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(ValueError, reason):
                    parse_reports(log, census)


class ObstructionPackaging(unittest.TestCase):
    def test_obstruction_lean_is_in_the_lake_package(self) -> None:
        actual = {
            p.relative_to(LEAN).as_posix()
            for p in LEAN.rglob("*.lean")
            if ".lake" not in p.relative_to(LEAN).parts
        }
        self.assertEqual(actual, EXPECTED_FILES)
        self.assertIn("EndogenousDemandObstruction.lean", EXPECTED_FILES)
        lakefile = (LEAN / "lakefile.toml").read_text(encoding="utf-8")
        self.assertIn('name = "EndogenousDemandObstruction"', lakefile)


class ForbiddenTokens(unittest.TestCase):
    def test_sorry_is_named(self) -> None:
        self.assertIsNotNone(FORBIDDEN.search("theorem t : True := sorry\n"))

    def test_mathlib_is_named(self) -> None:
        self.assertIsNotNone(MATHLIB.search("import mathlib\n"))

    def test_ordinary_admitted_is_not_the_token(self) -> None:
        self.assertIsNone(FORBIDDEN.search("the admitted instances of the regime\n"))


class CommittedRecord(unittest.TestCase):
    def test_record_is_within_the_whitelist_and_names_the_scope(self) -> None:
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        reports = record["reports"]
        self.assertEqual(record["theorem_count_including_generated"], len(reports))
        self.assertEqual(record["axiom_free_count"], sum(1 for v in reports.values() if not v))
        self.assertEqual(record["outcome"], "B")
        self.assertEqual(record["class"], "C_reqs")
        for name, axioms in reports.items():
            # The census covers both proof modules (2026-09-24); before, only
            # the EndogenousDemand namespace was recorded.
            self.assertTrue(name.startswith(("EndogenousDemand.", "EndogenousDemandObstruction.")), name)
            self.assertTrue(set(axioms) <= ALLOWED_AXIOMS, name)
        for theorem in (
            "EndogenousDemand.e2_on_C_reqs_unsat",
            "EndogenousDemand.replay_reqs_iff_impose",
            "EndogenousDemand.stepE_reqs_mem",
            "EndogenousDemand.applyDelta_reqs",
            "EndogenousDemand.event_constructors",
            "EndogenousDemand.historyL_reqs_from_impose",
            "EndogenousDemand.historyF_reqs_from_impose",
            "EndogenousDemandObstruction.endogenous_termination_bound",
            "EndogenousDemandObstruction.endogenous_termination_from_empty",
            "EndogenousDemandObstruction.endogenous_trace_le_binom2",
            "EndogenousDemandObstruction.endogenous_obstruction_no_excess",
        ):
            self.assertIn(theorem, reports)

    def test_every_written_theorem_has_a_recorded_report(self) -> None:
        """The check that was missing: read without a Lean build, so a theorem
        written outside the recorded audit fails here by name."""
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        written = written_census()
        self.assertEqual(sorted(set(written) - set(record["reports"])), [])
        self.assertEqual(record["written_theorem_count"], len(written))
        self.assertEqual(len([w for w in written if w.startswith("EndogenousDemandObstruction.")]), 17)
        self.assertEqual(len([w for w in written if w.startswith("EndogenousDemand.")]), 22)

    def test_both_proof_modules_are_read_for_reports(self) -> None:
        self.assertEqual(set(REPORTING_MODULES) | {"Inventory.lean"}, EXPECTED_FILES)
        inventory = (LEAN / "Inventory.lean").read_text(encoding="utf-8")
        self.assertIn("import EndogenousDemandObstruction", inventory)


class WrittenTheoremCensus(unittest.TestCase):
    def test_namespaces_sections_and_root(self) -> None:
        text = (
            "namespace A.B\n"
            "theorem one : True := trivial\n"
            "section S\n"
            "@[simp] protected theorem two : True := trivial\n"
            "end S\n"
            "theorem _root_.three : True := trivial\n"
            "end A.B\n"
            "private theorem four : True := trivial\n"
            "section\n"
            "theorem five' : True := trivial\n"
            "end\n"
        )
        self.assertEqual(written_theorems(text), ["A.B.one", "A.B.two", "three", "four", "five'"])

    def test_comments_are_not_declarations(self) -> None:
        text = (
            "/-! theorem hidden : True := trivial\n"
            "  /- nested theorem deeper -/ still inside -/\n"
            "-- theorem line : True := trivial\n"
            "/-- A docstring naming theorem nothing. -/\n"
            "theorem shown : True := trivial\n"
            "#print axioms shown\n"
        )
        self.assertEqual(written_theorems(text), ["shown"])
        self.assertEqual(strip_comments("a/-x\ny-/b").splitlines(), ["a ", " b"])

    def test_malformed_sources_fail_by_name(self) -> None:
        cases = [
            ("/- open", "unterminated block comment"),
            ("end Stray\n", "unmatched end"),
            ("theorem t : True := trivial\ntheorem t : True := trivial\n", "duplicate written theorem"),
        ]
        for text, reason in cases:
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(ValueError, reason):
                    written_theorems(text)

    def test_unreported_written_theorem_is_named(self) -> None:
        check_written(["N.t"], {"N.t": []})
        with self.assertRaisesRegex(ValueError, r"written theorem without axiom report: \['N.u'\]"):
            check_written(["N.t", "N.u"], {"N.t": []})


if __name__ == "__main__":
    unittest.main()
