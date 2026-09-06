from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from typed_translation.removal import (
    BOUNDARY_PROBES,
    NOT_FORMULATED,
    ROW_PROBES,
    DependenceClass,
    DependenceRow,
    actual_class,
    carrier_record,
    claimed_class,
    evaluate_probe,
    load_rows,
    removal_report,
    remove_boundary,
    score_row,
)


EXPECTED_WRONG = [
    "R09", "R13", "R15", "R16", "R17", "R18", "R20", "R21",
    "R23", "R25", "R29", "R30", "R32", "R33", "R34",
]


class RemovalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = load_rows()
        cls.report = removal_report(cls.rows)

    def test_vendored_population_is_exact_and_ordered(self) -> None:
        self.assertEqual(len(self.rows), 37)
        self.assertEqual([row.row_id for row in self.rows], [f"R{i:02d}" for i in range(37)])

    def test_every_row_has_a_nonempty_frozen_probe_tuple(self) -> None:
        self.assertEqual(set(ROW_PROBES), {row.row_id for row in self.rows})
        self.assertTrue(all(row.probes for row in self.rows))

    def test_projection_drops_exactly_boundary(self) -> None:
        for row in self.rows:
            before = carrier_record(row)
            after = remove_boundary(before)
            self.assertEqual(set(before) ^ set(after), {"boundary"})

    def test_projection_retains_unknown_future_fields(self) -> None:
        record = carrier_record(self.rows[0])
        record["future_field"] = {"value": 7}
        projected = remove_boundary(record)
        self.assertEqual(projected["future_field"], {"value": 7})

    def test_boundary_probe_becomes_not_formulated(self) -> None:
        row = next(row for row in self.rows if "side_profiles" in row.probes)
        before = carrier_record(row)
        self.assertNotEqual(evaluate_probe(before, "side_profiles"), NOT_FORMULATED)
        self.assertEqual(evaluate_probe(remove_boundary(before), "side_profiles"), NOT_FORMULATED)

    def test_generic_probe_survives_with_equal_json_value(self) -> None:
        row = self.rows[0]
        before = carrier_record(row)
        after = remove_boundary(before)
        self.assertEqual(
            evaluate_probe(before, "event_follows_empty"),
            evaluate_probe(after, "event_follows_empty"),
        )

    def test_unknown_probe_is_not_formulated(self) -> None:
        self.assertEqual(evaluate_probe({}, "missing"), NOT_FORMULATED)

    def test_actual_class_uses_only_survival_bools(self) -> None:
        self.assertIs(actual_class([True, True]), DependenceClass.INDEPENDENT)
        self.assertIs(actual_class([False, False]), DependenceClass.DEPENDENT)
        self.assertIs(actual_class([True, False]), DependenceClass.MIXED)

    def test_claim_parser_has_three_independent_branches(self) -> None:
        self.assertIs(claimed_class("does not depend on the admitted boundary"), DependenceClass.INDEPENDENT)
        self.assertIs(claimed_class("requires the admitted boundary"), DependenceClass.DEPENDENT)
        mixed = "does not depend on the boundary as a rule, but every configuration does"
        self.assertIs(claimed_class(mixed), DependenceClass.MIXED)
        c2 = "The values use the paid boundary. Attempt accounting and checks are metatheory."
        self.assertIs(claimed_class(c2), DependenceClass.MIXED)

    def test_claim_parser_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "unclassified"):
            claimed_class("perhaps")

    def test_total_score_matches_frozen_prediction(self) -> None:
        self.assertEqual(self.report["population"], 37)
        self.assertEqual(self.report["hit_count"], 22)
        self.assertEqual(self.report["wrong_count"], 15)
        self.assertEqual(self.report["wrong_ids"], EXPECTED_WRONG)

    def test_every_wrong_row_is_mechanically_mixed(self) -> None:
        rows = self.report["rows"]
        self.assertTrue(all(row["actual"] == "MIXED" for row in rows if not row["hit"]))

    def test_every_probe_records_before_after_and_survival(self) -> None:
        for row in self.report["rows"]:
            for probe in row["probes"]:
                self.assertEqual(set(probe), {"after", "before", "probe", "survives"})

    def test_boundary_probe_census_is_used(self) -> None:
        used = {probe for row in self.rows for probe in row.probes}
        self.assertTrue(BOUNDARY_PROBES <= used)

    def test_score_row_does_not_read_claim_for_actual_class(self) -> None:
        source = self.rows[0]
        changed = DependenceRow(source.row_id, source.stage, source.subject, "requires the admitted boundary", source.probes)
        original = score_row(source)
        mutated = score_row(changed)
        self.assertEqual(original["actual"], mutated["actual"])
        self.assertNotEqual(original["claimed"], mutated["claimed"])

    def test_loader_fails_on_nonobject(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "rows list"):
                load_rows(path)

    def test_loader_fails_on_nonobject_row(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.json"
            path.write_text(json.dumps({"rows": [1]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not an object"):
                load_rows(path)

    def test_loader_fails_on_probe_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.json"
            path.write_text(
                json.dumps({"rows": [{"id": "R00", "stage": "x", "subject": "x", "claim": "x", "probes": ["wrong"]}]}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "probes differ"):
                load_rows(path)


if __name__ == "__main__":
    unittest.main()
