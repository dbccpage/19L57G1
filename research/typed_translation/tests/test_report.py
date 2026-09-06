from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

from typed_translation.report import (
    EXPECTED_WRONG,
    FROZEN_SHA256,
    build_receipt,
    canonical_json,
    rendered_prose,
    sha256,
)


HERE = Path(__file__).resolve().parents[1]


class ReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt = build_receipt()
        cls.data = canonical_json(cls.receipt)

    def test_schema_and_terminals_are_explicit(self) -> None:
        self.assertEqual(self.receipt["schema"], "typed_translation.receipt.v1")
        self.assertEqual(
            self.receipt["terminal"],
            {
                "bounded_map": "MAP_WITH_PRICE",
                "exact_cost": "PROVED_EXACT_COST_OBSTRUCTION",
                "global": "OPEN_AT_BOUND",
                "removal": "TOTAL_REMOVAL_SCORED",
            },
        )

    def test_all_frozen_predictions_are_scored_hits(self) -> None:
        predictions = self.receipt["predictions"]
        self.assertEqual([row["id"] for row in predictions], [f"P{i}" for i in range(1, 12)])
        self.assertEqual({row["status"] for row in predictions}, {"HIT"})

    def test_candidate_and_history_crosschecks_are_true(self) -> None:
        self.assertTrue(self.receipt["map"]["candidate_order_crosscheck"])
        self.assertTrue(self.receipt["histories"]["ordered_unpruned_crosscheck"])

    def test_exact_two_orientation_tied_maps(self) -> None:
        map_data = self.receipt["map"]
        self.assertEqual(map_data["valid_count"], 2)
        self.assertEqual(
            {row["address_family"] for row in map_data["valid_candidates"]},
            {"direct", "complemented"},
        )
        self.assertTrue(map_data["orientation_quotient_equal"])

    def test_common_measures_have_one_named_implementation(self) -> None:
        costs = self.receipt["costs"]
        self.assertEqual(costs["shared_implementation"], "typed_translation.model.measure")
        self.assertNotIn("source_mu1", costs)
        self.assertNotIn("target_mu1", costs)

    def test_complete_distortion_table_is_present(self) -> None:
        table = self.receipt["costs"]["distortion"]["table"]
        self.assertEqual(len(table), self.receipt["histories"]["count"])

    def test_removal_misses_are_exact(self) -> None:
        self.assertEqual(self.receipt["removal"]["wrong_ids"], EXPECTED_WRONG)

    def test_frozen_hashes_are_recorded(self) -> None:
        self.assertEqual(self.receipt["freeze"]["sha256"], FROZEN_SHA256)

    def test_canonical_json_is_sorted_lf_and_round_trips(self) -> None:
        self.assertNotIn(b"\r", self.data)
        self.assertEqual(json.loads(self.data), self.receipt)
        self.assertEqual(self.data, canonical_json(self.receipt))

    def test_sha_helper_matches_standard_library(self) -> None:
        self.assertEqual(sha256(self.data), hashlib.sha256(self.data).hexdigest())

    def test_committed_receipt_matches_fresh_bytes(self) -> None:
        self.assertEqual((HERE / "receipts" / "typed_translation.json").read_bytes(), self.data)

    def test_rendered_prose_matches_all_three_documents(self) -> None:
        rendered = rendered_prose(self.receipt)
        self.assertEqual(set(rendered), {"STATUS.md", "FINDINGS.md", "CLAIM_LEDGER.md"})
        for name, text in rendered.items():
            self.assertEqual((HERE / name).read_text(encoding="utf-8"), text)

    def test_receipt_has_no_environment_or_timestamp_fields(self) -> None:
        text = self.data.decode("utf-8").casefold()
        self.assertNotIn("timestamp", text)
        self.assertNotIn("computername", text)


if __name__ == "__main__":
    unittest.main()
