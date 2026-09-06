"""The frozen predictions, the scorer, and the tree's own local gates.

The scorer is bound to the frozen text in two directions: every prediction
id must appear in ``PREDICTIONS.md``, and every expected value must be
carried by a quote that appears there verbatim.  Otherwise the expectations
in code could be edited to fit an answer while the frozen file stood.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import unittest
from unittest.mock import patch
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "code"))

from sidefree import control  # noqa: E402

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE))

import check_coverage  # noqa: E402
import verify_lean  # noqa: E402
import verify_pins  # noqa: E402

RECORD: Any = control.decide()
FROZEN = (TREE / "PREDICTIONS.md").read_text(encoding="utf-8")


class FrozenFiles(unittest.TestCase):
    def test_the_two_frozen_digests_are_what_the_verifier_pins(self) -> None:
        import hashlib

        for name, want in verify_pins.FROZEN.items():
            got = hashlib.sha256((TREE / name).read_bytes()).hexdigest()
            self.assertEqual(got, want, name)

    def test_the_receipt_reports_both_frozen_digests(self) -> None:
        block = RECORD["predictions"]
        assert isinstance(block, dict)
        self.assertEqual(
            block["frozen_file_sha256"], verify_pins.FROZEN["PREDICTIONS.md"]
        )
        self.assertEqual(block["design_file_sha256"], verify_pins.FROZEN["DESIGN.md"])

    def test_the_frozen_files_carry_no_cr_byte(self) -> None:
        for name in verify_pins.FROZEN:
            self.assertNotIn(b"\r", (TREE / name).read_bytes())


class Scoring(unittest.TestCase):
    def test_every_prediction_id_appears_in_the_frozen_file(self) -> None:
        for prediction in control.PREDICTIONS:
            self.assertIn(f"**{prediction.ident} ", FROZEN, prediction.ident)

    def test_every_quote_appears_in_the_frozen_file_verbatim(self) -> None:
        for prediction in control.PREDICTIONS:
            self.assertIn(prediction.quote, FROZEN, prediction.ident)

    def test_the_frozen_file_declares_no_prediction_the_scorer_skips(self) -> None:
        declared = set(re.findall(r"^\*\*(P\d+) ", FROZEN, re.M))
        scored = {p.ident for p in control.PREDICTIONS}
        self.assertEqual(declared, scored)

    def test_every_prediction_is_labelled_forced_or_not(self) -> None:
        forced = {p.ident for p in control.PREDICTIONS if p.forced}
        self.assertEqual(forced, {"P8", "P9", "P16", "P27"})
        for prediction in control.PREDICTIONS:
            label = "`FORCED`" if prediction.forced else "`NOT FORCED`"
            self.assertIn(label, FROZEN)

    def test_all_predictions_hit(self) -> None:
        block = RECORD["predictions"]
        assert isinstance(block, dict)
        scored = block["scored"]
        assert isinstance(scored, list)
        misses = [s for s in scored if isinstance(s, dict) and s["status"] == "MISS"]
        self.assertEqual(misses, [], json.dumps(misses, indent=1))
        self.assertEqual(block["misses"], 0)
        self.assertEqual(block["hits"], len(control.PREDICTIONS))
        self.assertTrue(block["quotes_all_found"])

    def test_the_scorer_reports_a_miss_rather_than_hiding_one(self) -> None:
        """Negative: a scorer that cannot report a MISS proves nothing."""
        broken: Any = dict(RECORD)
        decided = dict(RECORD["decided"])
        decided["side_free_minimum"] = 99
        broken["decided"] = decided
        block = control.score_predictions(broken)
        scored = block["scored"]
        assert isinstance(scored, list)
        first = scored[0]
        assert isinstance(first, dict)
        self.assertEqual(first["id"], "P1")
        self.assertEqual(first["status"], "MISS")
        self.assertEqual(block["misses"], 1)
        failures = first["failures"]
        assert isinstance(failures, list)
        self.assertEqual(failures[0]["computed"], 99)

    def test_the_scorer_reports_an_absent_path_rather_than_passing(self) -> None:
        block = control.score_predictions({})
        self.assertEqual(block["hits"], 0)
        self.assertEqual(block["misses"], len(control.PREDICTIONS))
        scored = block["scored"]
        assert isinstance(scored, list)
        for entry in scored:
            assert isinstance(entry, dict)
            cells = entry["ledger_cells"]
            assert isinstance(cells, dict)
            self.assertIsNone(cells["declared"])
            self.assertIsNone(cells["computed"])
            self.assertIn("NOT read as", str(cells["why_unclassified"]))

    def test_the_ledger_cells_a_prediction_reads_are_counted_as_cells(self) -> None:
        """A clause is not a cell, and the record now says which it counts.

        P22 carries twelve clauses over nine ledger cells: the three cells of
        the renaming row are objects and two clauses read each of them.  A
        scoring note called all twelve cells and then split them two ways
        that did not add up, so the population is computed here.  Exactly one
        of the nine is a declaration of this tree; the split is total.
        """
        block = RECORD["predictions"]
        assert isinstance(block, dict)
        scored = block["scored"]
        assert isinstance(scored, list)
        by_id = {str(entry["id"]): entry for entry in scored if isinstance(entry, dict)}
        reading = sorted(
            name for name, entry in by_id.items() if entry["ledger_cells"]["cells"]
        )
        self.assertEqual(reading, ["P22"])
        p22 = by_id["P22"]
        self.assertEqual(p22["clauses"], 12)
        cells = p22["ledger_cells"]
        self.assertEqual(len(cells["cells"]), 9)
        self.assertEqual(
            cells["declared"], ["coordinates_the_genesis_declaration_fixes:control"]
        )
        self.assertEqual(len(cells["computed"]), 8)
        ledger = RECORD["endowment_ledger"]
        assert isinstance(ledger, dict)
        for entry in scored:
            assert isinstance(entry, dict)
            block_cells = entry["ledger_cells"]
            assert isinstance(block_cells, dict)
            self.assertEqual(
                sorted(list(block_cells["declared"]) + list(block_cells["computed"])),
                block_cells["cells"],
            )
            for name in block_cells["declared"]:
                self.assertIn(name, ledger["declared_cells"])

    def test_the_forced_label_is_reported_and_not_counted_as_content(self) -> None:
        block = RECORD["predictions"]
        assert isinstance(block, dict)
        self.assertEqual(block["forced_hits"], 4)
        self.assertIn("not counted as content", str(block["tally_criterion"]))


class Terminal(unittest.TestCase):
    def test_the_terminal_sentence_carries_its_scope_clause(self) -> None:
        terminal = RECORD["terminal"]
        assert isinstance(terminal, dict)
        self.assertTrue(terminal["sentence_is_the_scoped_one"])
        self.assertIn("admission order", str(terminal["sentence"]))
        self.assertIn("Within the three declared coordinates", str(terminal["sentence"]))

    def test_the_open_obstructions_are_carried_rather_than_closed(self) -> None:
        obstructions = RECORD["open_obstructions"]
        assert isinstance(obstructions, list)
        self.assertEqual([o["id"] for o in obstructions], ["(a)", "(b)", "(c)", "(d)"])
        for entry in obstructions:
            self.assertTrue(entry["statement"])
            self.assertTrue(entry["why_open"])

    def test_the_scope_limits_name_the_lean_receipt_as_a_residual(self) -> None:
        limits = " ".join(str(s) for s in RECORD["scope_limits"])
        self.assertIn("MANUAL RECEIPT", limits)
        self.assertIn("no CI job builds it", limits)


class CoverageGate(unittest.TestCase):
    def test_the_percentages_are_computed_from_separate_counters(self) -> None:
        line, branch = check_coverage.percentages(
            {
                "num_statements": 200,
                "covered_lines": 190,
                "num_branches": 100,
                "covered_branches": 96,
            }
        )
        self.assertAlmostEqual(line, 95.0)
        self.assertAlmostEqual(branch, 96.0)

    def test_the_gate_refuses_impossible_or_absent_counters(self) -> None:
        for totals in (
            {"num_statements": 0, "covered_lines": 0, "num_branches": 1, "covered_branches": 0},
            {"num_statements": 1, "covered_lines": 0, "num_branches": 0, "covered_branches": 0},
            {"num_statements": 1, "covered_lines": 5, "num_branches": 1, "covered_branches": 0},
            {"num_statements": 1, "covered_lines": 1, "num_branches": 1, "covered_branches": 5},
        ):
            with self.assertRaises(ValueError):
                check_coverage.percentages(totals)
        with self.assertRaises(ValueError):
            check_coverage._count({"num_statements": True}, "num_statements")

    def test_the_measured_file_set_is_this_tree_s_code(self) -> None:
        expected = sorted(
            str(p.relative_to(TREE)).replace("\\", "/")
            for p in (TREE / "code" / "sidefree").rglob("*.py")
        )
        self.assertIn("code/sidefree/model.py", expected)
        self.assertIn("code/sidefree/control.py", expected)


class LeanGate(unittest.TestCase):
    def test_attribute_theorems_and_primed_reports_are_not_dropped(self) -> None:
        declaration = verify_lean.THEOREM.match("@[simp] theorem probe' : True := True.intro")
        self.assertIsNotNone(declaration)
        assert declaration is not None
        self.assertEqual(declaration.group(1), "probe'")
        line = "'SideFree.probe'' depends on axioms: [Classical.choice]"
        self.assertEqual(verify_lean.reports(line), [line])
        match = verify_lean.REPORT.search(line)
        assert match is not None
        self.assertEqual(match.group("name"), "SideFree.probe'")
        self.assertNotIn(match.group("axioms"), verify_lean.ALLOWED)

    def test_report_population_names_missing_duplicate_and_unparsed_reports(self) -> None:
        line = "'SideFree.probe'' does not depend on any axioms"
        with patch.object(verify_lean, "audited_theorems", return_value=["SideFree.probe'"]):
            self.assertEqual(verify_lean.report_problems(line), [])
            self.assertIn("SideFree.probe'", " ".join(verify_lean.report_problems("")))
            self.assertIn("found 2", " ".join(verify_lean.report_problems(line + "\n" + line)))
            self.assertIn("unparsed", " ".join(verify_lean.report_problems("broken depends on axioms: []")))
            self.assertEqual(verify_lean.report_problems(line), [])

    def test_the_forbidden_token_scan_finds_nothing_in_the_package(self) -> None:
        self.assertEqual(verify_lean.scan_sources(), [])

    def test_every_module_lies_in_the_root_import_closure(self) -> None:
        self.assertEqual(verify_lean.unreached_modules(), [])
        self.assertGreater(len(verify_lean.module_census()), 0)

    def test_every_declared_theorem_carries_an_axiom_report(self) -> None:
        self.assertEqual(verify_lean.unaudited_theorems(), [])
        self.assertGreater(len(verify_lean.declared_theorems()), 0)

    def test_the_committed_axiom_log_lies_within_the_whitelist(self) -> None:
        log = verify_lean.LOG.read_text(encoding="utf-8")
        self.assertNotIn("\r", log)
        found = verify_lean.reports(log)
        self.assertGreater(len(found), 0)
        for line in found:
            m = verify_lean.REPORT.search(line)
            assert m is not None
            axioms = {a.strip() for a in (m.group("axioms") or "").split(",") if a.strip()}
            self.assertTrue(axioms <= verify_lean.ALLOWED, line)

    def test_the_scanner_reads_prose_out_before_counting_theorems(self) -> None:
        stripped = verify_lean.strip_comments("/- theorem hidden -/\n-- theorem also\nx")
        self.assertNotIn("theorem", stripped)

    def test_the_forbidden_scan_would_name_an_injected_token(self) -> None:
        """Negative: the text scan must fire on each forbidden word."""
        for pattern, word in verify_lean.FORBIDDEN:
            probe = {
                "sorry": "  exact sorry",
                "admit": "  admit",
                "unsafe": "unsafe def f := 1",
                "partial": "partial def f := 1",
                "axiom": "axiom bad : True",
            }[word]
            self.assertIsNotNone(pattern.search(probe), word)


class PinVerifier(unittest.TestCase):
    def test_the_vendored_pin_matches_its_three_digests(self) -> None:
        self.assertEqual(verify_pins.check_vendored_pin(), [])

    def test_the_extracted_values_still_match_the_receipt(self) -> None:
        self.assertEqual(verify_pins.check_extracted_values(), [])

    def test_a_flipped_digest_is_named(self) -> None:
        """Negative: the pin check must fail on one changed hex digit."""
        raw = (TREE / verify_pins.PIN_REL).read_bytes()
        self.assertEqual(verify_pins.sha(raw), verify_pins.PIN_SHA256)
        self.assertNotEqual(verify_pins.sha(raw + b" "), verify_pins.PIN_SHA256)
        self.assertNotEqual(verify_pins.blob_id(raw + b" "), verify_pins.PIN_BLOB)

    def test_the_commit_check_is_reported_and_never_omitted(self) -> None:
        problems, notes = verify_pins.check_pinned_commit(True)
        self.assertEqual(problems, [])
        self.assertTrue(notes)
        self.assertTrue(any("PASS" in n or "SKIPPED" in n for n in notes))

    def test_the_verifier_runs_clean_from_the_repository_root(self) -> None:
        """The branch this clone is actually in, never the one this machine is in.

        The pinned commit sits on an unmerged branch, so a checkout that
        fetches only remote refs cannot reach it.  The verifier already
        reports that split -- hard by default, a reported SKIP under the flag
        -- and an earlier version of this test asserted exit 0 in default mode
        unconditionally, which fails in exactly that clone.  What is asserted
        now is the reported split itself, as ``comparison.load_pinned``
        already does for the vendored receipts.
        """
        root = TREE.parent.parent
        manifest = json.loads(
            (TREE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        commit = str(manifest["pinned_commit"])
        reachable = (
            subprocess.run(
                ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
                cwd=root,
                capture_output=True,
            ).returncode
            == 0
        )

        def run(*argv: str) -> "subprocess.CompletedProcess[str]":
            return subprocess.run(
                [sys.executable, str(TREE / "verify_pins.py"), *argv],
                cwd=root,
                capture_output=True,
                text=True,
            )

        proc = run()
        if reachable:
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("pins ok", proc.stdout)
            return
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(f"the pinned commit {commit} is unreachable", proc.stdout)
        downgraded = run("--allow-unreachable-pin")
        self.assertEqual(
            downgraded.returncode, 0, downgraded.stdout + downgraded.stderr
        )
        self.assertIn("pins ok", downgraded.stdout)


if __name__ == "__main__":
    unittest.main()
