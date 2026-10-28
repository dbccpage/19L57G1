"""Markerless-tree and stale-row regressions; AuthorityEffect: None."""
from pathlib import Path
import subprocess
import tempfile
import unittest

from research_population import inventory_errors, research_trees


class ResearchPopulationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)
        for rel in ("research/without_marker/FINDINGS.md", "research/closed/CLOSURE.md",
                    "research/with_lean/lean/Example.lean", "research/with_lean/TREE_CONTRACT.json",
                    "research/notes/README.md", "research/e2e_tests/README.md",
                    "research/_scaffold/README.md"):
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("fixture\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "--", "research"], check=True, capture_output=True)
        untracked = self.root / "research/not_tracked/README.md"
        untracked.parent.mkdir()
        untracked.write_text("Not indexed\n", encoding="utf-8")

    def test_markerless_trees_follow_tracked_population_with_exact_exclusions(self):
        self.assertEqual(research_trees(self.root), [
            ("closed", False, False), ("with_lean", True, True), ("without_marker", False, False)])

    def test_missing_and_stale_rows_are_both_named(self):
        text = "| [`research/with_lean/`](URL) | contract |\n| [`research/notes/`](URL) | notes |\n"
        self.assertEqual(inventory_errors(self.root, text), [
            "missing research tree: closed", "missing research tree: without_marker", "unexpected research tree: notes"])

    def test_mentions_outside_the_table_cannot_replace_missing_rows(self):
        text = "research/without_marker/ is described in prose.\n| [`research/closed/`](URL) |\n| [`research/with_lean/`](URL) |\n"
        self.assertEqual(inventory_errors(self.root, text), ["missing research tree: without_marker"])


if __name__ == "__main__":
    unittest.main()
