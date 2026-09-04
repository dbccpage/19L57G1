"""Tests of the Challenge 0 receipt: determinism, the frozen pins, the
scores, and the negative direction of the scorer."""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import types
import unittest

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE / "code"))
sys.path.insert(0, str(TREE))

from boundary.challenge0 import (  # noqa: E402
    CENSUS_MAX_MARKS,
    PREDICTIONS_SHA256,
    SEED_SHA256,
    build,
    genesis_facts,
    reflection_census,
    score,
    state_event_generators,
)
from boundary.model import AdmitMark  # noqa: E402
from run_challenge0 import render  # noqa: E402


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PinTests(unittest.TestCase):
    def test_seed_bytes_match_the_pin(self) -> None:
        self.assertEqual(sha(TREE / "SEED.md"), SEED_SHA256)

    def test_predictions_bytes_match_the_pin(self) -> None:
        self.assertEqual(sha(TREE / "challenge0" / "PREDICTIONS.md"), PREDICTIONS_SHA256)


class ReceiptTests(unittest.TestCase):
    def test_build_is_deterministic(self) -> None:
        self.assertEqual(build(), build())

    def test_committed_receipt_matches_the_renderer(self) -> None:
        path = TREE / "receipts" / "challenge0.json"
        self.assertTrue(path.exists(), "run run_challenge0.py first")
        self.assertEqual(path.read_bytes(), render())
        self.assertNotIn(b"\r", path.read_bytes())

    def test_receipt_carries_no_timestamp_or_environment(self) -> None:
        text = json.dumps(build(), sort_keys=True)
        for word in ("time", "date", "python", "platform", "user"):
            self.assertNotIn(word, text.lower().replace("timestamp", "time"))


class FactTests(unittest.TestCase):
    def test_scores(self) -> None:
        scores = build()["scores"]
        for cid in ("C0-1", "C0-2", "C0-3", "C0-4", "C0-5"):
            self.assertEqual(scores[cid]["status"], "HIT", cid)
        self.assertEqual(scores["C0-X"]["status"], "PENDING")
        self.assertEqual(scores["C0-5"]["general_clause"]["status"], "SHARPENED")

    def test_no_state_event_generator_in_the_kernel(self) -> None:
        self.assertEqual(state_event_generators(), [])

    def test_generator_census_sees_a_planted_generator(self) -> None:
        planted = types.ModuleType("planted")

        def emit(r: object) -> AdmitMark:
            return AdmitMark("a", 0)

        planted.emit = emit  # type: ignore[attr-defined]
        self.assertEqual(state_event_generators(planted), ["emit"])

    def test_census_rows(self) -> None:
        census = reflection_census(CENSUS_MAX_MARKS)
        self.assertTrue(census["fixed_iff_equal_counts"])
        rows = {row["marks"]: row for row in census["rows"]}
        self.assertEqual(rows[0]["fixed_by_reflection_up_to_mark_renaming"], 1)
        self.assertEqual(rows[1]["fixed_by_reflection_up_to_mark_renaming"], 0)
        self.assertEqual(rows[2]["fixed_by_reflection_up_to_mark_renaming"], 2)
        self.assertEqual(rows[1]["classes_under_U"], 1)
        self.assertEqual(rows[1]["classes_under_O"], 2)
        self.assertEqual(rows[4]["classes_under_U"], 3)
        self.assertEqual(rows[4]["classes_under_O"], 5)

    def test_scorer_misses_when_a_fact_moves(self) -> None:
        u = genesis_facts("U")
        o = genesis_facts("O")
        census = reflection_census(1)
        u_bad = dict(u, sides_collapsed=False)
        self.assertEqual(score(u_bad, o, census, [])["C0-1"]["status"], "MISSED")
        o_bad = dict(o, side_profiles=[["near", []], ["far", [0]]])
        self.assertEqual(score(u, o_bad, census, [])["C0-2"]["status"], "MISSED")
        self.assertEqual(score(u, o, census, ["emit"])["C0-3"]["status"], "MISSED")
        u_obs = dict(u, observations=[[0, 0]])
        self.assertEqual(score(u_obs, o, census, [])["C0-4"]["status"], "MISSED")
        o_ren = dict(o, reflection_is_permitted_renaming=True)
        self.assertEqual(score(u, o_ren, census, [])["C0-5"]["status"], "MISSED")


if __name__ == "__main__":
    unittest.main()
