"""The custody check passes on the pinned commit and names what it refuses."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import verify_sources  # noqa: E402


class SourceCustody(unittest.TestCase):
    def test_manifest_shape(self) -> None:
        manifest = json.loads((ROOT / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema"], verify_sources.SCHEMA)
        self.assertEqual(manifest["baseline_commit"], verify_sources.BASELINE_COMMIT)
        # 2026-09-25: the directory pins are retired; the Lean import closure is
        # pinned file by file in source_sha256 instead of consumed_trees.
        self.assertNotIn("consumed_trees", manifest)
        self.assertNotIn("tree_census", manifest)
        self.assertEqual(
            set(manifest["source_sha256"]),
            set(verify_sources.RUNTIME_PATHS.values()) | set(verify_sources.CONFIG_PATHS)
            | set(verify_sources.LEAN_PATHS),
        )
        self.assertEqual(set(manifest["artifact_sha256"]), set(verify_sources.ARTIFACT_PATHS))
        self.assertEqual(manifest["runtime_modules"], verify_sources.RUNTIME_PATHS)

    def test_consumed_sources_are_unchanged(self) -> None:
        self.assertEqual(verify_sources.verify_sources(check_runtime=False), [])

    def test_a_foreign_root_is_refused_by_name(self) -> None:
        failures = verify_sources.verify_sources(ROOT, check_runtime=False)
        self.assertTrue(failures)
        self.assertTrue(all(f.split(":")[0].isupper() for f in failures), failures)


if __name__ == "__main__":
    unittest.main()
