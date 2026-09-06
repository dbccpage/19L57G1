from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import unittest

from typed_translation.report import FROZEN_SHA256, build_receipt, canonical_json, rendered_prose


HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "verify.yml"
EXPECTED_TESTS = 119


class GateRegistrationTests(unittest.TestCase):
    def test_freeze_hashes_match_the_committed_contract(self) -> None:
        for name, wanted in FROZEN_SHA256.items():
            self.assertEqual(hashlib.sha256((HERE / name).read_bytes()).hexdigest(), wanted)

    def test_source_manifest_is_exact_and_nonempty(self) -> None:
        manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertRegex(manifest["pinned_commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(len(manifest["sources"]), 31)
        self.assertEqual(len({row["path"] for row in manifest["sources"]}), 31)
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) for row in manifest["sources"]))

    def test_vendored_population_names_the_manifest_snapshot(self) -> None:
        manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        vendored = json.loads((HERE / "pinned" / "boundary_dependence.json").read_text(encoding="utf-8"))
        self.assertEqual(vendored["snapshot"], manifest["pinned_commit"])
        self.assertEqual(len(vendored["rows"]), 37)

    def test_kernel_has_no_cross_tree_absolute_import(self) -> None:
        forbidden = {"derivation", "boundary", "sidefree", "limit_and_observer"}
        for path in (HERE / "code" / "typed_translation").rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            roots: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    roots.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    roots.add(node.module.split(".", 1)[0])
            self.assertFalse(roots & forbidden, path)

    def test_workflow_literal_equals_discovered_test_count(self) -> None:
        suite = unittest.defaultTestLoader.discover(str(HERE / "tests"), pattern="test_*.py")
        self.assertEqual(suite.countTestCases(), EXPECTED_TESTS)
        text = WORKFLOW.read_text(encoding="utf-8")
        match = re.search(r"Typed translation, tests, coverage, receipt, isolation.*?Ran (\d+) tests in ", text, re.S)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(int(match.group(1)), EXPECTED_TESTS)

    def test_workflow_registers_every_tree_gate(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        for command in (
            "research/typed_translation/verify_pins.py",
            "research/typed_translation/verify_lean.py",
            "python check_coverage.py",
            "python run_translation.py",
            "python verify_prose.py",
            "python -m mypy",
        ):
            self.assertIn(command, text)

    def test_committed_receipt_is_lf_and_current(self) -> None:
        data = (HERE / "receipts" / "typed_translation.json").read_bytes()
        self.assertNotIn(b"\r", data)
        self.assertEqual(data, canonical_json(build_receipt()))

    def test_generated_prose_is_lf_and_current(self) -> None:
        for name, expected in rendered_prose(build_receipt()).items():
            data = (HERE / name).read_bytes()
            self.assertNotIn(b"\r", data)
            self.assertEqual(data, expected.encode("utf-8"))

    def test_lean_inventory_names_every_theorem_target(self) -> None:
        inventory = (HERE / "lean" / "axioms.txt").read_text(encoding="utf-8")
        self.assertEqual(len(inventory.splitlines()), 3)
        self.assertIn("memoryless_fixed_block_obstruction", inventory)
        self.assertIn("symmetric_form_cost_obstruction", inventory)
        self.assertIn("retained_provenance_not_equal", inventory)


if __name__ == "__main__":
    unittest.main()
