"""Regression tests for the source-manifest and protected-boundary receipt."""

from __future__ import annotations

import json
from io import StringIO
import unittest
from unittest.mock import patch

import verify_manifest


class VerifyManifestTests(unittest.TestCase):
    def test_current_manifest_matches_lean_source_imports_and_symbols(self) -> None:
        lines = verify_manifest.verify_manifest()
        self.assertIn(
            "lean source imports: research\\primitive_difference_tower\\lean\\PrimitiveDifferenceTower.lean Derivation.PresentationNaturality",
            lines,
        )
        self.assertIn("lean source symbols: 10 declared uses match", lines)

    def test_missing_manifest_module_key_is_a_controlled_value_error(self) -> None:
        manifest = json.loads(verify_manifest.MANIFEST_PATH.read_text(encoding="utf-8"))
        manifest["modules"] = [{}]
        with patch.object(verify_manifest, "_read_manifest", return_value=manifest):
            with self.assertRaisesRegex(
                ValueError, "manifest module missing nonempty string 'module'"
            ):
                verify_manifest.verify_manifest()

    def test_malformed_manifest_main_returns_a_clean_failure(self) -> None:
        manifest = json.loads(verify_manifest.MANIFEST_PATH.read_text(encoding="utf-8"))
        manifest["modules"] = [{}]
        stderr = StringIO()
        with patch.object(verify_manifest, "_read_manifest", return_value=manifest), patch(
            "sys.stderr", stderr
        ):
            self.assertEqual(verify_manifest.main(), 1)
        self.assertIn("FAIL: manifest module missing nonempty string 'module'", stderr.getvalue())

    def test_untracked_protected_paths_are_reported_not_baselined(self) -> None:
        snapshot_commit = "f74ea9b7e40741429f74708c1f7671647b0962b6"

        def fake_git(*args: str) -> str:
            if args == ("rev-parse", f"{snapshot_commit}^{{tree}}"):
                return "4755d647c83db9926a2465e71c51aabb078cba9c"
            if args[0:2] == ("diff", "--name-only"):
                return ""
            if args[0:2] == ("ls-files", "--others"):
                return "prompt/local-only.md"
            self.fail(f"unexpected git call: {args}")

        with patch.object(verify_manifest, "_git", side_effect=fake_git), patch.object(
            verify_manifest, "_git_succeeds", return_value=True
        ):
            lines = verify_manifest.verify_protected_paths()
        self.assertEqual(lines[0], "protected history since source snapshot: unchanged")
        self.assertIn("prompt/local-only.md", lines[-1])

    def test_committed_protected_history_change_is_refused(self) -> None:
        snapshot_commit = "f74ea9b7e40741429f74708c1f7671647b0962b6"

        def fake_git(*args: str) -> str:
            if args == ("rev-parse", f"{snapshot_commit}^{{tree}}"):
                return "4755d647c83db9926a2465e71c51aabb078cba9c"
            if args[0:2] == ("diff", "--name-only"):
                return "prompt/prompt.md"
            self.fail(f"unexpected git call: {args}")

        with patch.object(verify_manifest, "_git", side_effect=fake_git), patch.object(
            verify_manifest, "_git_succeeds", return_value=True
        ):
            with self.assertRaisesRegex(
                ValueError, "protected-path history changed since source snapshot"
            ):
                verify_manifest.verify_protected_paths()


if __name__ == "__main__":
    unittest.main()
