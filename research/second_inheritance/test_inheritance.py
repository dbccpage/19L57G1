"""Tests for rung zero.  Run from this directory:
``python -m unittest discover -s . -p "test_*.py"``."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from inheritance import (  # noqa: E402
    MAX_DATA,
    REPO,
    absent_trees,
    all_free_growth,
    grammar_census,
    replay_challenges,
    replay_closed,
    replay_standing_summary,
    replay_two_sided_receipts,
    snapshot_commit,
    supplies_are_inert,
)
from derivation.engine import READINGS  # noqa: E402

FROZEN_SEED = "52439e5f75d1c599ce52dc716beb88f1dd7bfc83856ee73ce85f3a7eeec5e70e"
FROZEN_PROMPT = "aa804ee3eaab8b358ff347036fce8810f41f431fd68390c18d709775fd5a1447"
FROZEN_PREDICTIONS = "86767fe4d8b2ed73ec516855d6d78d3310c22ca6815c835ea4b46060c026ab3a"


def _sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FreezeTests(unittest.TestCase):
    def test_seed_is_frozen(self) -> None:
        self.assertEqual(_sha(REPO / "research" / "second" / "SEED.md"), FROZEN_SEED)

    def test_prompt_is_frozen(self) -> None:
        self.assertEqual(_sha(HERE / "PROMPT.md"), FROZEN_PROMPT)

    def test_predictions_are_frozen(self) -> None:
        self.assertEqual(_sha(HERE / "PREDICTIONS.md"), FROZEN_PREDICTIONS)

    def test_prompt_states_no_number(self) -> None:
        text = (HERE / "PROMPT.md").read_text(encoding="utf-8")
        body = text.replace("mu1", "").replace("mu2", "")
        self.assertIsNone(re.search(r"[0-9]", body))

    def test_frozen_texts_are_lf(self) -> None:
        for p in (HERE / "PROMPT.md", HERE / "PREDICTIONS.md", REPO / "research" / "second" / "SEED.md"):
            self.assertNotIn(b"\r", p.read_bytes(), p.name)


class ReplayTests(unittest.TestCase):
    def test_sealed_challenges_regenerate_byte_identically(self) -> None:
        self.assertTrue(replay_challenges()["byte_identical"])

    def test_sealed_closed_baselines_match_every_field(self) -> None:
        for rd in READINGS:
            out = replay_closed(rd)
            self.assertEqual(out["differing_fields"], [], rd.name)
            self.assertTrue(out["match"], rd.name)

    def test_absent_trees_are_checked_at_the_snapshot_not_head(self) -> None:
        snapshot = snapshot_commit()
        for a in absent_trees(snapshot):
            self.assertIn("present_at_snapshot", a)
            self.assertIn(a["pull_request"], (127, 128))

    def test_landed_commitment_receipts_regenerate(self) -> None:
        standing = replay_standing_summary()
        two_sided = replay_two_sided_receipts()
        self.assertTrue(standing["byte_identical"])
        self.assertTrue(two_sided["summary_byte_identical"])
        self.assertTrue(two_sided["full_content_identical"])


class CensusTests(unittest.TestCase):
    def test_sealed_grammar_has_six_kinds_one_state_preserving(self) -> None:
        c = grammar_census()
        self.assertEqual(c["sealed_event_count"], 6)
        self.assertEqual(c["sealed_state_preserving_count"], 1)
        rows = c["sealed_event_kinds"]
        assert isinstance(rows, list)
        preserving = [r["event"] for r in rows if not r["changes_state"]]
        self.assertEqual(preserving, ["Supply"])

    def test_sealed_engine_declares_two_policies_and_dual_three_events(self) -> None:
        c = grammar_census()
        self.assertEqual(c["sealed_policy_count"], 2)
        pols = c["sealed_policies"]
        assert isinstance(pols, list)
        self.assertTrue(all(p["present"] for p in pols))
        self.assertEqual(c["dual_declared_count"], 3)
        rows = c["dual_declared_events"]
        assert isinstance(rows, list)
        self.assertEqual(sorted(r["event"] for r in rows), ["RequireSame", "Retract", "Switch"])


class InertiaTests(unittest.TestCase):
    def test_supplies_leave_both_geneses_unchanged(self) -> None:
        for rd in READINGS:
            self.assertTrue(supplies_are_inert(rd)["regime_unchanged"], rd.name)

    def test_all_free_growth_is_a_collapsed_chain(self) -> None:
        for rd in READINGS:
            g = all_free_growth(rd)
            self.assertTrue(g["every_state_totally_collapsed"], rd.name)
            self.assertEqual(g["forms_ever_admitted"], 0)
            self.assertEqual(g["responses"], 0)
            self.assertTrue(g["all_pair_labels_evaluated"])
            chain = g["chain"]
            assert isinstance(chain, list)
            self.assertTrue(all(row["demands_all_free"] == 0 for row in chain))
            self.assertTrue(all(row["demands_undeclared"] == 0 for row in chain))
            self.assertTrue(all(row["labels_checked"] == row["all_pairs"] for row in chain))
            self.assertTrue(all(row["honours_checked"] == row["all_pairs"] for row in chain))
            self.assertEqual(chain[-1]["data"], MAX_DATA)
            self.assertEqual(g["growth_edges"], len(chain) - 1)


class ReceiptTests(unittest.TestCase):
    def test_receipt_regenerates_byte_identically(self) -> None:
        from run_inheritance import build_all

        from derivation.export import dumps_deterministic

        committed = (HERE / "receipts" / "inheritance.json").read_bytes()
        self.assertNotIn(b"\r", committed)
        self.assertEqual(dumps_deterministic(build_all()), committed)

    def test_receipt_records_the_frozen_hashes(self) -> None:
        payload = json.loads((HERE / "receipts" / "inheritance.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["seed_sha256"], FROZEN_SEED)
        self.assertEqual(payload["prompt_sha256"], FROZEN_PROMPT)
        self.assertEqual(payload["predictions_sha256"], FROZEN_PREDICTIONS)
        self.assertEqual(sorted(payload["predictions_scored"]), ["R0-1", "R0-2", "R0-3"])


if __name__ == "__main__":
    unittest.main()
