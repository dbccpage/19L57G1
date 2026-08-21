"""Tests for the axiom-report parser and audit; no Lean toolchain is needed."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import verify_lean


SAMPLE = (
    "'PrimitiveDifferenceTower.towerDown_after_towerUp' depends on axioms: [propext, Quot.sound]\n"
    "'PrimitiveDifferenceTower.primed'' does not depend on any axioms\n"
    "info: an unrelated line\n"
    "'PrimitiveDifferenceTower.replay_rounds_closed' depends on axioms: [propext]\n"
)


class VerifyLeanTests(unittest.TestCase):
    def test_parser_reads_exact_axiom_sets_including_primed_names(self) -> None:
        self.assertEqual(
            verify_lean.parse_axiom_report(SAMPLE),
            {
                "PrimitiveDifferenceTower.towerDown_after_towerUp": frozenset(
                    {"propext", "Quot.sound"}
                ),
                "PrimitiveDifferenceTower.primed'": frozenset(),
                "PrimitiveDifferenceTower.replay_rounds_closed": frozenset({"propext"}),
            },
        )

    def test_duplicate_report_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate axiom report"):
            verify_lean.parse_axiom_report(SAMPLE + SAMPLE)

    def test_disallowed_axiom_fails_even_though_the_name_is_present(self) -> None:
        output = "'A.b' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
        self.assertIn("A.b", output)  # the only condition the former check applied
        with self.assertRaisesRegex(
            ValueError, r"A\.b depends on disallowed axioms: \['Classical\.choice'\]"
        ):
            verify_lean.check_axiom_reports(verify_lean.parse_axiom_report(output), ("A.b",))

    def test_inventory_must_match_exactly(self) -> None:
        reports = {"A.b": frozenset({"propext"}), "A.extra": frozenset[str]()}
        with self.assertRaisesRegex(
            ValueError, r"missing \['A\.c'\], unexpected \['A\.extra'\]"
        ):
            verify_lean.check_axiom_reports(reports, ("A.b", "A.c"))
        self.assertEqual(
            verify_lean.check_axiom_reports(
                {"A.b": frozenset({"propext"}), "A.c": frozenset[str]()}, ("A.b", "A.c")
            ),
            ["A.b: ['propext']", "A.c: no axioms"],
        )

    def test_python_inventory_matches_axiom_report_lean(self) -> None:
        source = (verify_lean.LEAN_ROOT / verify_lean.AXIOM_REPORT_SOURCE).read_text(
            encoding="utf-8"
        )
        self.assertEqual(
            verify_lean.declared_report_inventory(source), verify_lean.AXIOM_REPORT_DECLARATIONS
        )

    def test_forbidden_token_scan_names_the_token_and_passes_the_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            bad = Path(temporary) / "Bad.lean"
            bad.write_text("theorem t : True := by\n  " + "sor" + "ry\n", encoding="utf-8")
            self.assertEqual(
                verify_lean.scan_forbidden_tokens([bad]),
                ["Bad.lean: forbidden token '" + "sor" + "ry'"],
            )
        sources = verify_lean.research_lean_sources()
        self.assertEqual(
            sorted(path.name for path in sources),
            ["AxiomReport.lean", "PrimitiveDifferenceTower.lean", "lakefile.lean"],
        )
        self.assertEqual(verify_lean.scan_forbidden_tokens(sources), [])


if __name__ == "__main__":
    unittest.main()
