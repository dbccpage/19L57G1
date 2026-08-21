"""Tests for Goal 5's integrated deterministic bridge receipt."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from symmetry_obstruction_bridge import (
    REPORT_SCHEMA,
    REPORT_SCOPE,
    bridge_report,
    bridge_report_sha256,
    displayed_anchor_imports,
    render_bridge_report,
    verify_bridge_report,
    write_bridge_report,
)
from verify_lean import AXIOM_REPORT_SOURCE, BRIDGE_AXIOM_REPORT_DECLARATIONS, LEAN_ROOT


class SymmetryObstructionBridgeReportTests(unittest.TestCase):
    def test_report_checks_the_five_goal_outputs_at_one_declared_scope(self) -> None:
        report = bridge_report()
        self.assertEqual(report["schema"], REPORT_SCHEMA)
        self.assertEqual(report["scope"], REPORT_SCOPE)
        self.assertEqual(report["contract"]["residual"], [1, 0])
        self.assertTrue(all(report["checks"].values()))
        self.assertEqual(
            report["selection"]["residual_singleton_choices"], [[0, 1], [1, 0]]
        )
        self.assertEqual(len(report["continuations"]), 4)
        self.assertEqual(
            [entry["selected_singleton"] for entry in report["continuations"]],
            [[1, 0], [0, 1], None, None],
        )

    def test_anchor_imports_are_visible_and_not_inferred_from_the_swap(self) -> None:
        anchors = displayed_anchor_imports()
        self.assertEqual([anchor.anchor.origin.value for anchor in anchors], ["admitted", "admitted"])
        report = bridge_report()
        self.assertTrue(report["checks"]["anchored_branches_are_explicit_imports"])
        self.assertEqual(
            report["selection"]["singleton_equivariance"],
            {"[0, 1]": False, "[1, 0]": False},
        )

    def test_rendering_is_byte_stable_and_the_checker_rejects_tampering(self) -> None:
        first = render_bridge_report()
        second = render_bridge_report()
        self.assertEqual(first, second)
        self.assertEqual(bridge_report_sha256(), bridge_report_sha256())
        payload = json.loads(first)
        self.assertTrue(verify_bridge_report(payload))
        tampered = copy.deepcopy(payload)
        tampered["checks"]["declared_repair_obstruction"] = False
        self.assertFalse(verify_bridge_report(tampered))

    def test_writer_has_identical_bytes_at_two_destinations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "one" / "bridge.json"
            second = root / "two" / "bridge.json"
            write_bridge_report(first)
            write_bridge_report(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(first.read_bytes(), render_bridge_report())

    def test_report_inventory_is_written_in_the_axiom_report_source(self) -> None:
        source = (LEAN_ROOT / AXIOM_REPORT_SOURCE).read_text(encoding="utf-8")
        report = bridge_report()
        self.assertEqual(report["lean_axiom_inventory"], list(BRIDGE_AXIOM_REPORT_DECLARATIONS))
        for declaration in BRIDGE_AXIOM_REPORT_DECLARATIONS:
            self.assertIn(f"#print axioms {declaration}", source)


if __name__ == "__main__":
    unittest.main()
