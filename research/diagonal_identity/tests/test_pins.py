"""Manifest, formula, and pure-function tests.

AuthorityEffect: None.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

import check_coverage
import diagonal_identity as di
import verify_lean
import verify_pins
import verify_sources

TREE = Path(__file__).resolve().parents[1]


def tampered() -> dict[str, Any]:
    return copy.deepcopy(verify_pins.read_manifest())


class PinTests(unittest.TestCase):
    def test_manifest_resolves_at_snapshot_and_head(self) -> None:
        lines = verify_pins.verify()
        self.assertTrue(lines[0].startswith("verification commit: "))
        manifest = verify_pins.read_manifest()
        pins = [line for line in lines if line.startswith("pin: ")]
        self.assertEqual(len(pins), len(manifest["sources"]))
        self.assertEqual(len(pins), 3)
        drift = [line for line in lines if line.startswith("DRIFT: ")]
        self.assertEqual(
            lines[-1],
            f"drift since the snapshot: {len(drift)} pinned source(s) or sealed path(s)"
            " moved at HEAD",
        )

    def test_verify_sources_wrapper_is_empty_on_pass(self) -> None:
        self.assertEqual(verify_sources.verify_sources(), [])

    def test_tampered_hash_is_refused(self) -> None:
        manifest = tampered()
        manifest["sources"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, r"hash mismatch for lean4/Derivation/PrimDiff"):
            verify_pins.verify(manifest)

    def test_unknown_role_is_refused(self) -> None:
        manifest = tampered()
        manifest["sources"][0]["role"] = "import"
        with self.assertRaisesRegex(ValueError, "unknown source role"):
            verify_pins.verify(manifest)

    def test_sealed_input_outside_seal_is_refused(self) -> None:
        manifest = tampered()
        manifest["sources"][0]["path"] = "research/unboundedness/lean/Continuum.lean"
        manifest["sources"][0]["role"] = "sealed input"
        with self.assertRaisesRegex(ValueError, "sealed input is not under a sealed prefix"):
            verify_pins.verify(manifest)

    def test_research_input_outside_allowed_prefix_is_refused(self) -> None:
        manifest = tampered()
        manifest["sources"][1]["path"] = "paper/paper.md"
        manifest["sources"][1]["role"] = "research input"
        with self.assertRaisesRegex(ValueError, "research input is not under an allowed prefix"):
            verify_pins.verify(manifest)

    def test_schema_mismatch_is_refused(self) -> None:
        manifest = tampered()
        manifest["schema"] = "nope"
        with self.assertRaisesRegex(ValueError, "manifest schema"):
            verify_pins.verify(manifest)

    def test_unsafe_path_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsafe path"):
            verify_pins._safe_relative("../secret")
        with self.assertRaisesRegex(ValueError, "unsafe path separator"):
            verify_pins._safe_relative("lean4\\Derivation\\PrimDiff.lean")

    def test_hex_and_missing_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "uppercase"):
            verify_pins._require_hex("ab", 2, "x", uppercase=True)
        with self.assertRaisesRegex(ValueError, "missing string"):
            verify_pins._required_string({}, "path", "src")
        with self.assertRaisesRegex(ValueError, "source_snapshot"):
            verify_pins.verify({"schema": verify_pins.SCHEMA, "source_snapshot": "nope", "sources": []})

    def test_porcelain_sealed_violation_is_pure(self) -> None:
        lines = verify_pins.sealed_prefix_violations(
            "?? code/derivation/__pycache__/model.cpython-314.pyc\n"
        )
        self.assertEqual(len(lines), 1)
        self.assertEqual(verify_pins.sealed_prefix_violations(""), [])
        with self.assertRaisesRegex(ValueError, "malformed"):
            verify_pins.sealed_prefix_violations("XX")


class FormulaTests(unittest.TestCase):
    def test_dual_module_states_not_instance(self) -> None:
        text = (TREE / "lean" / "DiagonalIdentity" / "Dual.lean").read_text(
            encoding="utf-8"
        )
        self.assertIn("theorem dual_on_declared_carriers", text)
        self.assertIn("theorem d2Const_not_as_covering_family", text)
        self.assertIn("theorem family_not_as_d2_const", text)
        self.assertIn("theorem covering_miss_witness_is_diagFlip", text)
        self.assertNotIn("identity of obstruction_under_irrefl", text.lower())

    def test_covering_formulas_match_continuum(self) -> None:
        covering = di.COVERING.read_text(encoding="utf-8")
        continuum = di.CONTINUUM.read_text(encoding="utf-8")
        self.assertEqual(di.formulas_match(covering, continuum), [])
        self.assertEqual(di.standing(), di.TERMINAL)

    def test_formula_drift_is_named(self) -> None:
        covering = di.COVERING.read_text(encoding="utf-8").replace(
            "fun n => ! (f n n)", "fun n => f n n"
        )
        continuum = di.CONTINUUM.read_text(encoding="utf-8")
        self.assertIn("diagBool", di.formulas_match(covering, continuum))

    def test_missing_definition_is_named(self) -> None:
        with self.assertRaisesRegex(ValueError, "definition diagBool not found"):
            di._def_body("theorem other : True := trivial", "diagBool")

    def test_standing_refuses_identity_and_wrong_terminal(self) -> None:
        payload = di.record()
        payload["identity_proved"] = True
        with self.assertRaisesRegex(ValueError, "identity_proved must stay False"):
            di.standing(payload)
        payload = di.record()
        payload["terminal"] = "PROVED"
        with self.assertRaisesRegex(ValueError, "unexpected terminal"):
            di.standing(payload)
        payload = di.record()
        payload["formula_mismatches"] = ["diagBool"]
        with self.assertRaisesRegex(ValueError, "covering formulas drifted"):
            di.standing(payload)


class LeanAuditTests(unittest.TestCase):
    def test_parse_and_check_reports(self) -> None:
        text = (
            "'Foo.bar' does not depend on any axioms\n"
            "'Foo.baz' depends on axioms: [propext, Quot.sound]\n"
        )
        reports = verify_lean.parse_axiom_report(text)
        self.assertEqual(reports["Foo.bar"], frozenset())
        self.assertEqual(reports["Foo.baz"], frozenset({"propext", "Quot.sound"}))
        lines = verify_lean.check_axiom_reports(
            reports, expected=("Foo.bar", "Foo.baz")
        )
        self.assertEqual(len(lines), 2)
        with self.assertRaisesRegex(ValueError, "duplicate axiom report"):
            verify_lean.parse_axiom_report(text + text)
        with self.assertRaisesRegex(ValueError, "inventory differs"):
            verify_lean.check_axiom_reports(reports, expected=("Foo.bar",))
        bad = dict(reports)
        bad["Foo.bar"] = frozenset({"Classical.choice"})
        with self.assertRaisesRegex(ValueError, "disallowed axioms"):
            verify_lean.check_axiom_reports(bad, expected=("Foo.bar", "Foo.baz"))

    def test_print_axioms_inventory(self) -> None:
        source = (TREE / "lean" / "DiagonalIdentity" / "AxiomReport.lean").read_text(
            encoding="utf-8"
        )
        self.assertEqual(
            verify_lean.declared_report_inventory(source),
            verify_lean.AXIOM_REPORT_DECLARATIONS,
        )

    def test_writes_outside_root_and_malformed(self) -> None:
        before = {" M research/diagonal_identity/README.md"}
        after = before | {
            "!! lean4/.lake/build",
            " M research/diagonal_identity/STATUS.md",
        }
        hits = verify_lean.writes_outside_root(before, after)
        self.assertTrue(any("lean4/.lake" in line for line in hits))
        self.assertFalse(any("STATUS.md" in line for line in hits))
        with self.assertRaisesRegex(ValueError, "malformed"):
            verify_lean.writes_outside_root(set(), {"XX"})

    def test_forbidden_token_scan_and_lakefile(self) -> None:
        lakefile = (TREE / "lean" / "lakefile.lean").read_text(encoding="utf-8")
        self.assertTrue(verify_lean.lakefile_has_no_require(lakefile))
        self.assertFalse(verify_lean.lakefile_has_no_require("require foo from git\n"))
        self.assertTrue(verify_lean.lakefile_has_no_require("-- must not require a path\n"))
        hits = verify_lean.scan_forbidden_tokens([TREE / "lean" / "DiagonalIdentity.lean"])
        self.assertEqual(hits, [])

    def test_coverage_evaluate_shape(self) -> None:
        errors, _, _ = check_coverage.evaluate("nope")
        self.assertTrue(errors[0].startswith("COVERAGE_SHAPE"))
        errors, _, _ = check_coverage.evaluate({"totals": {}})
        self.assertTrue(any("COVERAGE_FILES" in e for e in errors))


class CoverageReportTests(unittest.TestCase):
    def test_report_errors_empty_on_good_payload(self) -> None:
        payload = {
            "totals": {
                "covered_lines": 100,
                "num_statements": 100,
                "covered_branches": 100,
                "num_branches": 100,
            },
            "files": {
                "research/diagonal_identity/diagonal_identity.py": {},
                "research/diagonal_identity/verify_pins.py": {},
                "research/diagonal_identity/verify_lean.py": {},
                "research/diagonal_identity/verify_sources.py": {},
                "research/diagonal_identity/run.py": {},
                "research/diagonal_identity/check_coverage.py": {},
            },
        }
        self.assertEqual(check_coverage.report_errors(payload), [])
        totals = payload["totals"]
        assert isinstance(totals, dict)
        statement, branch = check_coverage.percentages(totals)
        self.assertEqual(statement, 100.0)
        self.assertEqual(branch, 100.0)
        with self.assertRaises(TypeError):
            check_coverage._number(True)
        leaked = {
            "totals": payload["totals"],
            "files": {"research/diagonal_identity/tests/test_pins.py": {}},
        }
        errors = check_coverage.report_errors(leaked)
        self.assertTrue(any("COVERAGE_LEAK" in e or "COVERAGE_POPULATION" in e for e in errors))


class ExtraCoverageTests(unittest.TestCase):
    def test_stage_sources_and_inventory(self) -> None:
        lines = verify_lean.stage_sources()
        self.assertTrue(any(line.startswith("staged: lean4/Derivation/PrimDiff.lean") for line in lines))
        self.assertTrue(verify_lean.research_lean_sources())
        with self.assertRaisesRegex(ValueError, "source_snapshot"):
            verify_lean.stage_sources({"sources": []})
        with self.assertRaisesRegex(ValueError, "not pinned"):
            verify_lean.stage_sources({
                "source_snapshot": {"commit": "0ab0e67037900606159ec2babb2e7cf5b7854f20"},
                "sources": [],
            })

    def test_scan_sorry_and_lake_failure(self) -> None:
        from unittest import mock
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Bad.lean"
            path.write_text("theorem t : True := sorry\n", encoding="utf-8")
            hits = verify_lean.scan_forbidden_tokens([path])
            self.assertTrue(any("sorry" in h for h in hits))
        with mock.patch.object(verify_lean, "_run_lake", return_value=""):
            with mock.patch.object(verify_lean, "repository_records", return_value=frozenset()):
                with mock.patch.object(verify_lean, "stage_sources", return_value=["staged"]):
                    with mock.patch.object(
                        verify_lean,
                        "parse_axiom_report",
                        return_value={name: frozenset() for name in verify_lean.AXIOM_REPORT_DECLARATIONS},
                    ):
                        lines = verify_lean.verify_axiom_report()
                        self.assertTrue(any("lake build" in line for line in lines))
        with mock.patch(
            "subprocess.run",
            return_value=mock.Mock(returncode=1, stdout="boom"),
        ):
            with self.assertRaisesRegex(RuntimeError, "lake .* failed"):
                verify_lean._run_lake(("build",))
        with mock.patch(
            "subprocess.run",
            return_value=mock.Mock(returncode=0, stdout="ok"),
        ):
            self.assertEqual(verify_lean._run_lake(("env",)), "ok")

    def test_mains_and_check_coverage_missing(self) -> None:
        from unittest import mock
        import io

        with mock.patch("sys.argv", ["verify_pins.py"]):
            self.assertEqual(verify_pins.main(), 0)
        with mock.patch.object(verify_lean, "verify_axiom_report", return_value=["ok"]):
            with mock.patch("sys.argv", ["verify_lean.py"]):
                self.assertEqual(verify_lean.main(), 0)
        with mock.patch.object(
            verify_lean, "verify_axiom_report", side_effect=ValueError("nope")
        ):
            self.assertEqual(verify_lean.main(), 1)
        with mock.patch.object(check_coverage, "REPORT", Path("no-such-coverage.json")):
            self.assertEqual(check_coverage.main(), 1)
        buf = io.StringIO()
        with mock.patch("sys.stdout", buf):
            with mock.patch.object(check_coverage, "REPORT") as report:
                report.is_file.return_value = True
                report.read_text.side_effect = OSError("bad")
                self.assertEqual(check_coverage.main(), 1)

    def test_run_check_mismatch_and_verify_failure(self) -> None:
        import run as runner
        from unittest import mock

        with mock.patch.object(runner, "verify_sources", return_value=["bad pin"]):
            with self.assertRaisesRegex(RuntimeError, "source verification failed"):
                runner.receipt_bytes()
        with mock.patch.object(runner, "receipt_bytes", return_value=b"fresh\n"):
            with mock.patch.object(runner, "RECORD") as record_path:
                record_path.is_file.return_value = True
                record_path.read_bytes.return_value = b"stale\n"
                with mock.patch("sys.argv", ["run.py", "--check"]):
                    self.assertEqual(runner.main(), 1)
        with mock.patch.object(runner, "receipt_bytes", return_value=b"{}\n"):
            with mock.patch.object(runner, "RECORD") as record_path:
                record_path.parent.mkdir = mock.Mock()
                record_path.write_bytes = mock.Mock()
                with mock.patch("sys.argv", ["run.py", "--write"]):
                    self.assertEqual(runner.main(), 0)

    def test_verify_pins_main_fail_and_git_error(self) -> None:
        from unittest import mock

        with mock.patch.object(verify_pins, "verify", side_effect=ValueError("x")):
            with mock.patch("sys.argv", ["verify_pins.py"]):
                self.assertEqual(verify_pins.main(), 1)
        with mock.patch(
            "subprocess.run",
            return_value=mock.Mock(returncode=1, stdout=b"", stderr=b"nope"),
        ):
            with self.assertRaisesRegex(ValueError, "git .* failed"):
                verify_pins._git_bytes("status")

    def test_source_missing_sha_and_non_dict_manifest(self) -> None:
        from unittest import mock

        with self.assertRaisesRegex(ValueError, "SOURCE_MANIFEST.json must be an object"):
            from unittest import mock
            with mock.patch.object(verify_pins, "MANIFEST_PATH") as path:
                path.read_text.return_value = "[]"
                verify_pins.read_manifest()
        manifest = tampered()
        del manifest["sources"][0]["sha256"]
        with self.assertRaisesRegex(ValueError, "sha256"):
            verify_pins.verify(manifest)
        self.assertEqual(verify_sources.verify_manifest(), verify_pins.verify())
        with mock.patch.object(verify_pins, "verify", side_effect=ValueError("pin fail")):
            self.assertEqual(verify_sources.verify_sources(), ["pin fail"])

    def test_check_coverage_thresholds_and_main_pass(self) -> None:
        from unittest import mock
        import tempfile

        files: dict[str, dict[str, object]] = {
            "research/diagonal_identity/diagonal_identity.py": {},
            "research/diagonal_identity/verify_pins.py": {},
            "research/diagonal_identity/verify_lean.py": {},
            "research/diagonal_identity/verify_sources.py": {},
            "research/diagonal_identity/run.py": {},
            "research/diagonal_identity/check_coverage.py": {},
        }
        self.assertTrue(any("COVERAGE_TOTALS" in e for e in check_coverage.report_errors({"totals": [], "files": files})))
        low_stmt = {
            "totals": {
                "covered_lines": 1,
                "num_statements": 100,
                "covered_branches": 100,
                "num_branches": 100,
            },
            "files": files,
        }
        self.assertTrue(any("COVERAGE_STATEMENT" in e for e in check_coverage.report_errors(low_stmt)))
        low_br = {
            "totals": {
                "covered_lines": 100,
                "num_statements": 100,
                "covered_branches": 1,
                "num_branches": 100,
            },
            "files": files,
        }
        self.assertTrue(any("COVERAGE_BRANCH" in e for e in check_coverage.report_errors(low_br)))
        empty_stmt = {
            "totals": {
                "covered_lines": 0,
                "num_statements": 0,
                "covered_branches": 1,
                "num_branches": 1,
            },
            "files": files,
        }
        self.assertTrue(any("no statements" in e for e in check_coverage.report_errors(empty_stmt)))
        empty_br = {
            "totals": {
                "covered_lines": 1,
                "num_statements": 1,
                "covered_branches": 0,
                "num_branches": 0,
            },
            "files": files,
        }
        self.assertTrue(any("no branches" in e for e in check_coverage.report_errors(empty_br)))
        bad_types = {
            "totals": {
                "covered_lines": True,
                "num_statements": 1,
                "covered_branches": 1,
                "num_branches": 1,
            },
            "files": files,
        }
        self.assertTrue(any("COVERAGE_TOTALS" in e for e in check_coverage.report_errors(bad_types)))
        good = {
            "totals": {
                "covered_lines": 100,
                "num_statements": 100,
                "covered_branches": 100,
                "num_branches": 100,
            },
            "files": files,
        }
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "coverage.json"
            report.write_text(json.dumps(good), encoding="utf-8")
            with mock.patch.object(check_coverage, "REPORT", report):
                self.assertEqual(check_coverage.main(), 0)
            report.write_text("{", encoding="utf-8")
            with mock.patch.object(check_coverage, "REPORT", report):
                self.assertEqual(check_coverage.main(), 1)
            report.write_text(json.dumps(low_stmt), encoding="utf-8")
            with mock.patch.object(check_coverage, "REPORT", report):
                self.assertEqual(check_coverage.main(), 1)

    def test_verify_axiom_report_refusals(self) -> None:
        from unittest import mock

        with mock.patch.object(verify_lean, "declared_report_inventory", return_value=("Nope",)):
            with self.assertRaisesRegex(ValueError, "names"):
                verify_lean.verify_axiom_report()
        with mock.patch.object(verify_lean, "lakefile_has_no_require", return_value=False):
            with self.assertRaisesRegex(ValueError, "must not declare a Lake require"):
                verify_lean.verify_axiom_report()
        with mock.patch.object(verify_lean, "research_lean_sources", return_value=[]):
            with self.assertRaisesRegex(ValueError, "no Lean sources"):
                verify_lean.verify_axiom_report()
        with mock.patch.object(verify_lean, "scan_forbidden_tokens", return_value=["sorry"]):
            with self.assertRaisesRegex(ValueError, "forbidden tokens"):
                verify_lean.verify_axiom_report()
        with mock.patch.object(verify_lean, "stage_sources", return_value=["s"]):
            with mock.patch.object(verify_lean, "_run_lake", return_value=""):
                with mock.patch.object(
                    verify_lean,
                    "repository_records",
                    side_effect=[
                        frozenset(),
                        frozenset({"!! lean4/.lake/build"}),
                    ],
                ):
                    with self.assertRaisesRegex(ValueError, "wrote outside"):
                        verify_lean.verify_axiom_report()

    def test_stage_sources_bad_snapshot_and_repin(self) -> None:
        from unittest import mock

        with self.assertRaisesRegex(ValueError, "40-digit"):
            verify_lean.stage_sources({
                "source_snapshot": {"commit": "HEAD"},
                "sources": [{"path": "lean4/Derivation/PrimDiff.lean", "sha256": "0" * 64}],
            })
        with self.assertRaisesRegex(ValueError, "must list sources"):
            verify_lean.stage_sources({
                "source_snapshot": {"commit": "0ab0e67037900606159ec2babb2e7cf5b7854f20"},
                "sources": "nope",
            })
        with self.assertRaisesRegex(ValueError, "hashes to"):
            verify_lean.stage_sources({
                "source_snapshot": {"commit": "0ab0e67037900606159ec2babb2e7cf5b7854f20"},
                "sources": [{
                    "path": "lean4/Derivation/PrimDiff.lean",
                    "sha256": "0" * 64,
                }],
            })
        with mock.patch.object(
            verify_lean,
            "STAGED_SOURCES",
            (("lean4/Derivation/PrimDiff.lean", "../../../../escape.lean"),),
        ):
            with self.assertRaisesRegex(ValueError, "escapes"):
                verify_lean.stage_sources()
        import shutil
        import tempfile

        tmp = Path(tempfile.mkdtemp()) / "SOURCE_MANIFEST.json"
        shutil.copy(verify_pins.MANIFEST_PATH, tmp)
        payload = json.loads(tmp.read_text(encoding="utf-8"))
        payload["sources"][0]["sha256"] = "0" * 64
        tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        with mock.patch.object(verify_pins, "MANIFEST_PATH", tmp):
            lines = verify_pins.repin()
            self.assertTrue(any("rehashed" in line or "repinned" in line for line in lines))
        dirty = verify_lean.STAGED_ROOT / "Derivation" / "PrimDiff.lean"
        if dirty.is_file():
            dirty.write_bytes(b"not the blob")
            verify_lean.stage_sources()

    def test_live_porcelain_violation_path(self) -> None:
        from unittest import mock

        with mock.patch.object(
            verify_pins,
            "_live_porcelain",
            return_value="!! code/derivation/__pycache__/x.pyc\n",
        ):
            with self.assertRaisesRegex(ValueError, "worktree carries files"):
                verify_pins.verify()
        original = verify_pins._sha256_git_blob
        calls = {"n": 0}

        def _head_differs(revision: str, relative: Any) -> str:
            calls["n"] += 1
            if calls["n"] == 2:
                return "0" * 64
            return original(revision, relative)

        # 2026-09-23: a source that moved at HEAD is drift, reported and not
        # failed; --require-current restores the failure, naming the path.
        with mock.patch.object(verify_pins, "_sha256_git_blob", side_effect=_head_differs):
            lines = verify_pins.verify()
        moved = [line for line in lines if line.startswith("DRIFT: ") and "at HEAD is 0000" in line]
        self.assertEqual(len(moved), 1)
        calls["n"] = 0
        with mock.patch.object(verify_pins, "_sha256_git_blob", side_effect=_head_differs):
            with self.assertRaisesRegex(ValueError, "--require-current"):
                verify_pins.verify(require_current=True)

        def _head_missing(revision: str, relative: Any) -> str:
            if revision != verify_pins._git("rev-parse", "HEAD") or calls["n"]:
                return original(revision, relative)
            calls["n"] += 1
            raise ValueError("git show failed: missing")

        calls["n"] = 0
        with mock.patch.object(verify_pins, "_sha256_git_blob", side_effect=_head_missing):
            with self.assertRaisesRegex(ValueError, "could not read"):
                verify_pins.verify()
        with mock.patch.object(verify_pins, "_sha256_git_blob", side_effect=_head_missing),                 mock.patch.object(verify_pins, "_git", side_effect=lambda *a: (
                    "" if a[0] == "ls-tree" else verify_pins._git_bytes(*a).decode().strip())):
            calls["n"] = 0
            lines = verify_pins.verify()
        self.assertTrue(any(line.endswith("is absent at HEAD") for line in lines))
        self.assertEqual(verify_pins.sealed_prefix_violations("\n\n"), [])
        from unittest import mock as mock_mod

        def _merge_fail(*args: str) -> Any:
            if args[:2] == ("merge-base", "--is-ancestor"):
                return mock_mod.Mock(returncode=1, stdout=b"", stderr=b"")
            return verify_pins._run_git(*args)

        with mock_mod.patch.object(verify_pins, "_run_git", side_effect=_merge_fail):
            self.assertFalse(verify_pins._is_ancestor("aaa", "bbb"))

        def _merge_err(*args: str) -> Any:
            if args[:2] == ("merge-base", "--is-ancestor"):
                return mock_mod.Mock(returncode=2, stdout=b"", stderr=b"boom")
            return verify_pins._run_git(*args)

        with mock_mod.patch.object(verify_pins, "_run_git", side_effect=_merge_err):
            with self.assertRaisesRegex(ValueError, "merge-base"):
                verify_pins._is_ancestor("aaa", "bbb")
        records = verify_lean.repository_records()
        self.assertIsInstance(records, frozenset)


class RunTests(unittest.TestCase):
    def test_receipt_roundtrip(self) -> None:
        import run as runner
        from unittest import mock

        fresh = runner.receipt_bytes()
        self.assertIn(b"DUAL_NOT_IDENTITY_ON_DECLARED_CARRIERS", fresh)
        with mock.patch.object(runner, "RECORD") as record_path:
            record_path.is_file.return_value = True
            record_path.read_bytes.return_value = fresh
            with mock.patch("sys.argv", ["run.py", "--check"]):
                self.assertEqual(runner.main(), 0)
        with mock.patch("sys.argv", ["run.py"]):
            with self.assertRaises(SystemExit):
                runner.main()


class MorePinRefusals(unittest.TestCase):
    def test_empty_sources_and_non_object_manifest(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least one source"):
            verify_pins.verify({
                "schema": verify_pins.SCHEMA,
                "source_snapshot": tampered()["source_snapshot"],
                "sources": [],
            })
        with self.assertRaisesRegex(ValueError, "must be an object"):
            verify_pins._sources({"sources": ["nope"]})

    def test_snapshot_commit_must_be_lowercase_hex(self) -> None:
        manifest = tampered()
        manifest["source_snapshot"]["commit"] = "HEAD"
        with self.assertRaisesRegex(ValueError, "snapshot commit"):
            verify_pins.verify(manifest)

    def test_tree_mismatch(self) -> None:
        manifest = tampered()
        manifest["source_snapshot"]["tree"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "snapshot tree mismatch"):
            verify_pins.verify(manifest)

    def test_unresolved_snapshot(self) -> None:
        manifest = tampered()
        manifest["source_snapshot"]["commit"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "does not resolve"):
            verify_pins.verify(manifest)


if __name__ == "__main__":
    unittest.main()
