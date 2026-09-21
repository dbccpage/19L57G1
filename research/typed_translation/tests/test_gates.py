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
MINIMUM_TESTS = 119


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

    def test_workflow_minimum_is_met_by_discovered_test_count(self) -> None:
        suite = unittest.defaultTestLoader.discover(str(HERE / "tests"), pattern="test_*.py")
        self.assertGreaterEqual(suite.countTestCases(), MINIMUM_TESTS)
        text = WORKFLOW.read_text(encoding="utf-8")
        match = re.search(r'Typed translation, tests, coverage, receipt, isolation.*?test-count "\$log" --minimum (\d+)', text, re.S)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(int(match.group(1)), MINIMUM_TESTS)

    def test_workflow_registers_every_tree_gate(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        for command in (
            "research/typed_translation/verify_pins.py",
            "research/typed_translation/verify_lean.py",
            "python check_coverage.py",
            "python run_translation.py --check",
            "python verify_prose.py",
            "python -m mypy",
        ):
            self.assertIn(command, text)

    def test_receipt_check_is_unconditional_and_cannot_be_bypassed(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        def problems(value: str) -> list[str]:
            match = re.search(
                r"      - name: Typed translation, tests, coverage, receipt, isolation\n(.*?)(?=      - name:|\Z)",
                value, re.S,
            )
            if match is None:
                return ["missing receipt step"]
            block = match.group(1)
            lines = block.splitlines()
            check = "          python run_translation.py --check"
            compare = "          git diff --exit-code -- receipts/typed_translation.json STATUS.md FINDINGS.md CLAIM_LEDGER.md"
            if (lines.count(check) != 1 or lines.count(compare) != 1
                    or lines.index(check) >= lines.index(compare)
                    or re.search(r"^\s*(?:if|elif|else|fi)(?:\s|;|$)", block, re.M)
                    or "continue-on-error:" in block or "||" in block or "set +e" in block):
                return ["unconditional fresh receipt comparison required"]
            return []
        self.assertEqual(problems(text), [])
        for replacement in ("python run_translation.py", "python run_translation.py --check || true"):
            injected = text.replace("python run_translation.py --check", replacement, 1)
            self.assertEqual(problems(injected), ["unconditional fresh receipt comparison required"])
            self.assertEqual(problems(text), [])

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
