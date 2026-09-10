from __future__ import annotations

import unittest
from typing import Any

import verify


class VerificationControls(unittest.TestCase):
    def test_source_population_and_base(self) -> None:
        good = {"base": verify.BASE, "sources": {name: "0" * 64 for name in verify.SOURCE_PATHS}}
        self.assertEqual(len(verify.validate_manifest(good)), len(verify.SOURCE_PATHS))
        for bad, reason in (({"base": "wrong"}, "SOURCE_BASE"),
                            ({"base": verify.BASE, "sources": {}}, "SOURCE_POPULATION"),
                            ({"base": verify.BASE, "sources": dict.fromkeys(verify.SOURCE_PATHS, "bad")},
                             "SOURCE_DIGEST_SHAPE")):
            with self.assertRaisesRegex(ValueError, reason):
                verify.validate_manifest(bad)
        verify.validate_manifest(good)

    def test_axiom_population_and_dependencies(self) -> None:
        name = "InstanceDemand.example"
        census = "INSTANCE_DEMAND_THEOREM: " + name + "\n"
        good = "'" + name + "' depends on axioms: [propext]\n"
        self.assertEqual(verify.parse_reports(good, census), {name: ["propext"]})
        for text, inventory, reason in (
            (good, "", "THEOREM_CENSUS_EMPTY_OR_DUPLICATE"),
            (good, census + census, "THEOREM_CENSUS_EMPTY_OR_DUPLICATE"),
            (good + good, census, "DUPLICATE_REPORT"),
            ("", census, "THEOREM_REPORT_CENSUS_MISMATCH"),
            (good.replace("propext", "Classical.choice"), census, "AXIOM_RELIANCE"),
        ):
            with self.assertRaisesRegex(ValueError, reason):
                verify.parse_reports(text, inventory)
        self.assertEqual(verify.parse_reports(good, census), {name: ["propext"]})

    def test_coverage_requires_both_thresholds_and_exact_file(self) -> None:
        measured: dict[str, Any] = {str(verify.ROOT / name): {} for name in ("probe.py", "materialize.py")}
        payload: dict[str, Any] = {"files": measured,
                                  "totals": {"covered_lines": 100, "num_statements": 100,
                                             "covered_branches": 100, "num_branches": 100}}
        self.assertEqual(verify.check_coverage(payload), (100.0, 100.0))
        for key in ("covered_lines", "covered_branches"):
            payload["totals"][key] = 94
            with self.assertRaisesRegex(ValueError, "COVERAGE:"):
                verify.check_coverage(payload)
            payload["totals"][key] = 100
        payload["files"] = {"unrelated.py": {}}
        with self.assertRaisesRegex(ValueError, "COVERAGE_POPULATION"):
            verify.check_coverage(payload)
        payload["files"] = measured
        self.assertEqual(verify.check_coverage(payload), (100.0, 100.0))
