from __future__ import annotations

import json
from pathlib import Path
from typing import cast
import unittest

import verify_frozen_compatibility as subject


class FrozenCompatibilityAuditTests(unittest.TestCase):
    def test_axiom_parser_handles_wrapped_reports(self) -> None:
        output = (
            "'Alpha' depends on axioms: [propext,\n Quot.sound]\n"
            "'Beta' does not depend on any axioms\n"
        )
        self.assertEqual(
            subject.parse_axiom_reports(output),
            [
                {
                    "declaration": "Alpha",
                    "axioms": ["Quot.sound", "propext"],
                    "allowed": True,
                },
                {"declaration": "Beta", "axioms": [], "allowed": True},
            ],
        )

    def test_axiom_parser_marks_forbidden_dependency(self) -> None:
        reports = subject.parse_axiom_reports(
            "'Alpha' depends on axioms: [Classical.choice]"
        )
        self.assertFalse(reports[0]["allowed"])

    def test_exact_report_population_rejects_missing_extra_and_duplicate(self) -> None:
        module = "ActualSectionAdapter.lean"
        expected = sorted(subject.EXPECTED_REPORTS[module])
        reports = [
            {"declaration": name, "axioms": [], "allowed": True}
            for name in expected
        ]
        self.assertEqual(subject.audit_axiom_reports(module, reports), (True, True))
        self.assertEqual(subject.audit_axiom_reports(module, reports[:-1]), (False, False))
        extra = [*reports, {"declaration": "Extra", "axioms": [], "allowed": True}]
        self.assertEqual(subject.audit_axiom_reports(module, extra), (False, False))
        duplicate = [*reports, reports[0]]
        self.assertEqual(subject.audit_axiom_reports(module, duplicate), (False, False))

    def test_tournament_packet_graph_and_sparse_cost_replay(self) -> None:
        path = Path(__file__).with_name("tournament") / "packets.jsonl"
        packets = [
            cast(dict[str, object], json.loads(line))
            for line in path.read_text(encoding="utf-8").splitlines()
            if line
        ]
        by_id = {str(packet["id"]): packet for packet in packets}
        self.assertEqual(len(by_id), len(packets))
        roots = [packet for packet in packets if packet["level"] == 0]
        self.assertEqual([root["id"] for root in roots], ["M0"])
        for packet in packets:
            imports = cast(list[str], packet["imports"])
            primitives = cast(list[str], packet["new_primitives"])
            obligations = cast(list[str], packet["obligations"])
            self.assertEqual(packet["l1"], len(imports) + len(primitives) + len(obligations))
            level = cast(int, packet["level"])
            for parent_id in cast(list[str], packet["parents"]):
                self.assertIn(parent_id, by_id)
                self.assertLess(cast(int, by_id[parent_id]["level"]), level)
        terminal = by_id["T0"]
        self.assertEqual(terminal["status"], "open")
        self.assertEqual(
            terminal["residual"],
            "Exchange authorization, nontriviality, unit calibration, actual adapter fields, and retained-trace integration remain unresolved or refuted as forced.",
        )


if __name__ == "__main__":
    unittest.main()
