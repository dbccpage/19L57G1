"""test_estate_honesty.py — Test suite for Target 10 Estate Honesty Pass.

Verifies:
1. Full 48-tree audit coverage and existence.
2. Exact Gate 11 CI integration counts (13 trees wired, 35 local receipts).
3. Exact Lean CI axiom checking (2 trees in CI: second_nofirst, typed_translation).
4. Reconciliation of root test count drift (481 in README vs. 523 collected by pytest).
5. Kernel axiom report integrity (1,530 reports, all within {propext, Quot.sound}).
6. Generation and claim hygiene of ESTATE_AUDIT_REPORT.md and RECONCILED_CLAIMS_LEDGER.md.
"""

from pathlib import Path
import sys
from typing import Any
import unittest

ROOT = Path(__file__).resolve().parents[2]
ESTATE_HONESTY_DIR = ROOT / "research" / "estate_honesty"

for p in (str(ROOT), str(ESTATE_HONESTY_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import audit_estate as ae  # type: ignore[import-not-found]  # noqa: E402
import axiom_inventory as ai  # type: ignore[import-not-found]  # noqa: E402


class TestEstateHonesty(unittest.TestCase):
    """Integrity and reconciliation tests for the research estate."""

    trees: list[ae.TreeAuditRecord]
    test_audit: dict[str, Any]
    axiom_audit: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.trees = ae.audit_trees(ROOT)
        cls.test_audit = ae.audit_test_counts(ROOT)
        cls.axiom_audit = ae.audit_axioms(ROOT)

    def test_all_48_trees_audited(self) -> None:
        """Exactly 48 trees are declared in research/README.md and audited."""
        self.assertEqual(len(self.trees), 48)
        missing_on_disk = [t.name for t in self.trees if not t.exists_on_disk]
        self.assertEqual(missing_on_disk, [], "All 48 declared trees must exist on disk")

    def test_gate_11_ci_integration_counts(self) -> None:
        """Gate 11 in .github/workflows/verify.yml wires exactly 13 trees; 35 are local receipts."""
        g11_trees = [t.name for t in self.trees if t.in_verify_yml_gate11]
        local_trees = [t.name for t in self.trees if not t.in_verify_yml_gate11]
        self.assertEqual(len(g11_trees), 13)
        self.assertEqual(len(local_trees), 35)

        expected_g11 = {
            "blind_restart", "boundary_seed", "limit_and_observer", "partial_decide",
            "portable_interface", "primitive_difference_tower", "second",
            "second_inheritance", "second_nofirst", "second_stake", "second_stream",
            "side_free", "typed_translation",
        }
        self.assertEqual(set(g11_trees), expected_g11)

    def test_lean_ci_axiom_gate_counts(self) -> None:
        """Only second_nofirst and typed_translation have Lean axiom audits run in CI."""
        ci_lean_trees = [t.name for t in self.trees if t.in_verify_yml_lean]
        self.assertEqual(set(ci_lean_trees), {"second_nofirst", "typed_translation"})

    def test_root_test_suite_drift_reconciled(self) -> None:
        """Root test suite collects 523 tests across 41 files; drift is exactly +42."""
        root = self.test_audit["root_suite"]
        self.assertEqual(root["readme_collected"], 481)
        self.assertEqual(root["current_collected"], 523)
        self.assertEqual(root["drift_collected"], 42)
        self.assertEqual(root["current_files"], 41)
        self.assertEqual(root["readme_files"], 41)

    def test_gate11_literal_pins_exist(self) -> None:
        """Gate 11 pinned literal test counts are present in verify.yml."""
        pins = self.test_audit["gate11_pinned_counts"]
        self.assertEqual(pins["second_stream"], 150)
        self.assertEqual(pins["boundary_seed"], 566)
        self.assertEqual(pins["second_nofirst"], 180)
        self.assertEqual(pins["side_free"], 364)
        self.assertEqual(pins["typed_translation"], 119)
        self.assertIsNotNone(pins["limit_and_observer"])

    def test_kernel_axioms_strictly_constructive(self) -> None:
        """All 1,530 kernel axiom reports are strictly contained in {propext, Quot.sound}."""
        k = self.axiom_audit["kernel_axioms"]
        self.assertEqual(k["current_report_count"], 1530)
        self.assertEqual(k["historical_count_20260817"], 1314)
        self.assertEqual(k["drift"], 216)
        self.assertEqual(k["elaborated_modules"], 75)
        self.assertTrue(k["all_within_allowed"])
        self.assertEqual(k["disallowed_count"], 0)

    def test_research_tree_axioms_forbid_classical_choice(self) -> None:
        """No research tree with verify_lean.py permits Classical.choice."""
        inventory = ai.inspect_tree_axiom_scripts(ROOT)
        self.assertGreaterEqual(len(inventory), 28)
        for tree_name, data in inventory.items():
            self.assertFalse(
                data["permits_choice"],
                f"Tree {tree_name} permits Classical.choice!",
            )

    def test_generated_reports_exist_and_follow_claim_hygiene(self) -> None:
        """ESTATE_AUDIT_REPORT.md and RECONCILED_CLAIMS_LEDGER.md exist and observe claim hygiene."""
        audit_rep = ESTATE_HONESTY_DIR / "ESTATE_AUDIT_REPORT.md"
        claims_led = ESTATE_HONESTY_DIR / "RECONCILED_CLAIMS_LEDGER.md"

        self.assertTrue(audit_rep.is_file())
        self.assertTrue(claims_led.is_file())

        audit_text = audit_rep.read_text(encoding="utf-8")
        claims_text = claims_led.read_text(encoding="utf-8")

        # AuthorityEffect: None must be stated
        self.assertTrue("AuthorityEffect" in audit_text and "None" in audit_text)
        self.assertTrue("AuthorityEffect" in claims_text and "None" in claims_text)

        # Forbidden hype words check
        forbidden_words = [
            "weaponized",
            "flawless",
            "perfectly",
            "true intelligence",
            "mathematically verifies",
            "fundamentally",
        ]
        for word in forbidden_words:
            self.assertNotIn(f" {word} ", audit_text.lower(), f"Forbidden word '{word}' found in audit report")
            self.assertNotIn(f" {word} ", claims_text.lower(), f"Forbidden word '{word}' found in claims ledger")


if __name__ == "__main__":
    unittest.main()
