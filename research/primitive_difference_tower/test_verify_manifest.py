"""Regression tests for the source-manifest, boundary, and receipt checker."""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path, PurePosixPath
import subprocess
import tempfile
from typing import Any
import unittest
from unittest.mock import patch

import verify_manifest


SNAPSHOT = "f74ea9b7e40741429f74708c1f7671647b0962b6"
SNAPSHOT_TREE = "4755d647c83db9926a2465e71c51aabb078cba9c"
SOURCE_TREE = "lean4/Derivation/"


def _manifest() -> dict[str, Any]:
    payload: dict[str, Any] = json.loads(
        verify_manifest.MANIFEST_PATH.read_text(encoding="utf-8")
    )
    return payload


class VerifyManifestTests(unittest.TestCase):
    def test_current_manifest_matches_lean_source_imports_and_symbols(self) -> None:
        lines = verify_manifest.verify_manifest()
        self.assertIn(
            "lean source imports: research/primitive_difference_tower/lean/"
            "PrimitiveDifferenceTower.lean Derivation.PresentationNaturality",
            lines,
        )
        self.assertIn("lean source symbols: 10 declared uses match", lines)
        # Output is rendered with POSIX separators on every platform.
        self.assertTrue(all("\\" not in line for line in lines), lines)

    def test_missing_manifest_module_key_is_a_controlled_value_error(self) -> None:
        manifest = _manifest()
        manifest["modules"] = [{}]
        with patch.object(verify_manifest, "_read_manifest", return_value=manifest):
            with self.assertRaisesRegex(
                ValueError, "manifest module missing nonempty string 'module'"
            ):
                verify_manifest.verify_manifest()

    def test_malformed_manifest_main_returns_a_clean_failure(self) -> None:
        manifest = _manifest()
        manifest["modules"] = [{}]
        stderr = StringIO()
        with patch.object(verify_manifest, "_read_manifest", return_value=manifest), patch(
            "sys.stderr", stderr
        ):
            self.assertEqual(verify_manifest.main([]), 1)
        self.assertIn("FAIL: manifest module missing nonempty string 'module'", stderr.getvalue())

    def test_transitive_use_without_explicit_citation_is_refused(self) -> None:
        manifest = _manifest()
        manifest["explicit_transitive_citations"] = [
            citation
            for citation in manifest["explicit_transitive_citations"]
            if citation["module"] != "Derivation.ContactBridge"
        ]
        with patch.object(verify_manifest, "_read_manifest", return_value=manifest):
            with self.assertRaisesRegex(
                ValueError,
                "uses transitive module Derivation.ContactBridge without an explicit "
                "transitive citation",
            ):
                verify_manifest.verify_manifest()

    def test_explicit_citation_must_name_exactly_the_symbols_used(self) -> None:
        manifest = _manifest()
        for citation in manifest["explicit_transitive_citations"]:
            if citation["module"] == "Derivation.ContactBridge":
                citation["symbols"] = ["obsApart", "unusedSymbol"]
        with patch.object(verify_manifest, "_read_manifest", return_value=manifest):
            with self.assertRaisesRegex(ValueError, "does not match lean_source uses"):
                verify_manifest.verify_manifest()

    def test_declared_symbol_absent_from_the_source_is_refused(self) -> None:
        manifest = _manifest()
        manifest["lean_source"]["symbol_uses"][0]["symbols"].append("notInSource")
        with patch.object(verify_manifest, "_read_manifest", return_value=manifest):
            with self.assertRaisesRegex(
                ValueError, r"missing \[\('PresentationNaturality', 'notInSource'\)\]"
            ):
                verify_manifest.verify_manifest()

    def test_safe_relative_rejects_traversal_on_every_platform(self) -> None:
        for bad in (
            "lean4/Derivation/..\\..\\secret",
            "lean4/Derivation/../x.lean",
            "lean4/Derivation/./x.lean",
            "lean4/Derivation//x.lean",
            "/lean4/Derivation/x.lean",
            "C:lean4/Derivation/x.lean",
        ):
            with self.assertRaisesRegex(ValueError, "unsafe manifest path", msg=bad):
                verify_manifest._safe_relative(bad, SOURCE_TREE, "source")
        with self.assertRaisesRegex(ValueError, "lies outside"):
            verify_manifest._safe_relative("code/model.py", SOURCE_TREE, "source")
        self.assertEqual(
            verify_manifest._safe_relative("lean4\\Derivation\\X.lean", SOURCE_TREE, "source"),
            PurePosixPath("lean4/Derivation/X.lean"),
        )

    def test_lean_scrubber_refuses_unterminated_strings_and_skips_char_literals(self) -> None:
        with self.assertRaisesRegex(ValueError, "unterminated string literal"):
            verify_manifest._strip_lean_comments_and_strings('def s := "open')
        with self.assertRaisesRegex(ValueError, "unterminated block comment"):
            verify_manifest._strip_lean_comments_and_strings("/- open")
        source = (
            "def c := '\"'\n"
            "def h' := Foo.bar -- Baz.qux\n"
            "/- Block.hidden /- Nested.hidden -/ -/ Keep.me \"Str.ing\" Also.kept\n"
        )
        scrubbed = verify_manifest._strip_lean_comments_and_strings(source)
        for kept in ("Foo.bar", "h'", "Keep.me", "Also.kept"):
            self.assertIn(kept, scrubbed)
        for hidden in ("Baz.qux", "Block.hidden", "Nested.hidden", "Str.ing"):
            self.assertNotIn(hidden, scrubbed)

    def test_is_ancestor_distinguishes_no_from_undecided(self) -> None:
        def completed(code: int) -> subprocess.CompletedProcess[bytes]:
            return subprocess.CompletedProcess(
                args=["git"], returncode=code, stdout=b"", stderr=b"fatal: bad object"
            )

        with patch.object(subprocess, "run", return_value=completed(0)):
            self.assertTrue(verify_manifest._is_ancestor("a", "b"))
        with patch.object(subprocess, "run", return_value=completed(1)):
            self.assertFalse(verify_manifest._is_ancestor("a", "b"))
        with patch.object(subprocess, "run", return_value=completed(128)):
            with self.assertRaisesRegex(ValueError, "was not decided.*bad object"):
                verify_manifest._is_ancestor("a", "b")

    def test_untracked_protected_paths_are_reported_not_baselined(self) -> None:
        def fake_git(*args: str) -> str:
            if args == ("rev-parse", f"{SNAPSHOT}^{{tree}}"):
                return SNAPSHOT_TREE
            if args[0] == "log":
                return ""
            if args[0:2] == ("diff", "--name-only"):
                return ""
            if args[0:2] == ("ls-files", "--others"):
                return "prompt/local-only.md"
            self.fail(f"unexpected git call: {args}")

        with patch.object(verify_manifest, "_git", side_effect=fake_git), patch.object(
            verify_manifest, "_is_ancestor", return_value=True
        ):
            lines = verify_manifest.verify_protected_paths()
        self.assertEqual(
            lines[0],
            "protected history since source snapshot: no commit touched a protected path",
        )
        self.assertIn("prompt/local-only.md", lines[-1])

    def test_commit_touching_a_protected_path_is_refused_even_if_later_reverted(self) -> None:
        calls: list[tuple[str, ...]] = []

        def fake_git(*args: str) -> str:
            calls.append(args)
            if args == ("rev-parse", f"{SNAPSHOT}^{{tree}}"):
                return SNAPSHOT_TREE
            if args[0] == "log":
                # The endpoint trees agree, so only a per-commit walk sees these.
                return "deadbeef\ncafebabe"
            self.fail(f"unexpected git call: {args}")

        with patch.object(verify_manifest, "_git", side_effect=fake_git), patch.object(
            verify_manifest, "_is_ancestor", return_value=True
        ):
            with self.assertRaisesRegex(
                ValueError, "commits since the source snapshot touched a protected path"
            ):
                verify_manifest.verify_protected_paths()
        log_call = next(call for call in calls if call[0] == "log")
        self.assertIn("--full-history", log_call)
        self.assertIn(f"{SNAPSHOT}..HEAD", log_call)
        self.assertEqual(log_call[log_call.index("--") + 1 :], verify_manifest.PROTECTED_PREFIXES)

    def test_snapshot_that_is_not_an_ancestor_is_refused(self) -> None:
        def fake_git(*args: str) -> str:
            if args == ("rev-parse", f"{SNAPSHOT}^{{tree}}"):
                return SNAPSHOT_TREE
            self.fail(f"unexpected git call: {args}")

        with patch.object(verify_manifest, "_git", side_effect=fake_git), patch.object(
            verify_manifest, "_is_ancestor", return_value=False
        ):
            with self.assertRaisesRegex(ValueError, "not an ancestor of HEAD"):
                verify_manifest.verify_protected_paths()

    def test_receipt_matches_code_and_prose_cites_it(self) -> None:
        lines = verify_manifest.verify_receipt_and_prose()
        self.assertTrue(lines[0].startswith("receipt: receipts/finite_tower_0_15.json "), lines)
        self.assertTrue(
            lines[1].startswith("receipt: receipts/symmetry_obstruction_bridge.json "),
            lines,
        )
        self.assertEqual(
            lines[2:],
            [
                "prose cites receipts and snapshot: CLAIM_LEDGER.md",
                "prose cites receipts and snapshot: FINDINGS.md",
            ],
        )

    def test_stale_receipt_is_refused(self) -> None:
        with patch.object(verify_manifest, "render_report", return_value=b"{}\n"):
            with self.assertRaisesRegex(ValueError, "differs from render_report"):
                verify_manifest.verify_receipt_and_prose()

    def test_stale_bridge_receipt_is_refused(self) -> None:
        with patch.object(verify_manifest, "render_bridge_report", return_value=b"{}\n"):
            with self.assertRaisesRegex(ValueError, "symmetry_obstruction_bridge.json"):
                verify_manifest.verify_receipt_and_prose()

    def test_prose_that_drops_the_receipt_hash_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            stale = Path(temporary) / "STALE.md"
            stale.write_text(f"snapshot {SNAPSHOT} but no receipt hash", encoding="utf-8")
            with patch.object(verify_manifest, "PROSE_PATHS", (stale,)):
                with self.assertRaisesRegex(
                    ValueError, "STALE.md does not cite the current receipt SHA-256"
                ):
                    verify_manifest.verify_receipt_and_prose()

    def test_repin_rewrites_hashes_and_moves_the_snapshot_to_head(self) -> None:
        manifest = _manifest()
        manifest["modules"][0]["sha256"] = "0" * 64
        manifest["source_snapshot"] = {"commit": "0" * 40, "tree": "0" * 40}
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "SOURCE_MANIFEST.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            with patch.object(verify_manifest, "MANIFEST_PATH", path):
                lines = verify_manifest.repin_manifest()
                rewritten = json.loads(path.read_text(encoding="utf-8"))
                raw = path.read_bytes()
        head = verify_manifest._git("rev-parse", "HEAD")
        self.assertEqual(rewritten["source_snapshot"]["commit"], head)
        self.assertEqual(rewritten["modules"], _manifest()["modules"])
        rehashed = [line for line in lines if line.startswith("rehashed: ")]
        self.assertEqual(len(rehashed), 1)
        self.assertTrue(rehashed[0].startswith("rehashed: lean4/Derivation/DiffInterface.lean "))
        self.assertIn(f"source snapshot: {'0' * 40} -> {head}", lines)
        self.assertNotIn(b"\r\n", raw)


if __name__ == "__main__":
    unittest.main()
