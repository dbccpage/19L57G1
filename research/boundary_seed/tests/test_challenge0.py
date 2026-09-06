"""Tests of the Challenge 0 receipt: determinism, the frozen pins, the
scores, and the negative direction of the scorer."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys
import types
import unittest
from unittest.mock import patch

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE / "code"))
sys.path.insert(0, str(TREE))

from boundary.challenge0 import (  # noqa: E402
    BOUNDARY_DEPENDENCE,
    CENSUS_MAX_MARKS,
    PREDICTIONS_SHA256,
    SEED_SHA256,
    build,
    genesis_facts,
    judgment_json,
    observation_vocabulary,
    reflection_census,
    score,
    state_event_generators,
)
from boundary.model import AdmitMark, OnSide  # noqa: E402
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
        # The same token scan as the Challenge 1 receipt: a watched word is a
        # hit when it is not glued to letters, so snake_case keys are split.
        text = json.dumps(build(), sort_keys=True).lower()
        hits = re.findall(
            r"(?<![a-z])(timestamp|time|date|python|platform|user)(?![a-z])", text
        )
        self.assertEqual(hits, [])
        self.assertIn("readings", text)


class FactTests(unittest.TestCase):
    def test_scores(self) -> None:
        scores = build()["scores"]
        for cid in ("C0-1", "C0-2", "C0-3", "C0-5"):
            self.assertEqual(scores[cid]["status"], "HIT", cid)
        self.assertEqual(scores["C0-4"]["status"], "PARTIAL")
        self.assertEqual(scores["C0-4"]["target_status"], "HIT")
        self.assertEqual(scores["C0-4"]["no_observation_fires_status"], "MISSED")
        self.assertEqual(scores["C0-X"]["status"], "PENDING")
        self.assertEqual(scores["C0-5"]["general_clause"]["status"], "SHARPENED")
        self.assertEqual(scores["C0-5"]["general_clause"]["max_marks"], 4)
        self.assertEqual(scores["C0-4"]["label"], "NOT FORCED")

    def test_initial_datum_and_boundary_dependence_are_explicit(self) -> None:
        receipt = build()
        for rd in ("U", "O"):
            self.assertEqual(
                receipt["readings"][rd]["initial_datum"],
                {"internal_id": 0, "present": True},
            )
        self.assertEqual(receipt["boundary_dependence"], BOUNDARY_DEPENDENCE)

    def test_no_state_event_generator_in_the_kernel(self) -> None:
        self.assertEqual(state_event_generators(), [])

    def test_generator_census_sees_a_planted_generator(self) -> None:
        planted = types.ModuleType("planted")

        def emit(r: object) -> AdmitMark:
            return AdmitMark("a", 0)

        planted.emit = emit  # type: ignore[attr-defined]
        self.assertEqual(state_event_generators(planted), ["emit"])

    def test_generator_census_sees_an_optional_event(self) -> None:
        planted = types.ModuleType("planted_optional")

        def maybe_emit(r: object) -> AdmitMark | None:
            return AdmitMark("a", 0) if r is not None else None

        planted.maybe_emit = maybe_emit  # type: ignore[attr-defined]
        self.assertEqual(state_event_generators(planted), ["maybe_emit"])

    def test_generator_census_skips_private_and_falls_back_on_bad_hints(self) -> None:
        planted = types.ModuleType("planted_defensive_paths")

        def _private() -> AdmitMark:
            return AdmitMark("a", 0)

        def unresolved() -> "MissingAnnotation":  # type: ignore[name-defined]  # noqa: F821
            raise AssertionError("the census must not call inspected functions")

        planted._private = _private  # type: ignore[attr-defined]
        planted.unresolved = unresolved  # type: ignore[attr-defined]
        self.assertEqual(state_event_generators(planted), [])

    def test_observation_vocabulary_is_derived_from_closed_sum(self) -> None:
        self.assertEqual(observation_vocabulary(), ["OnSide", "SideNamed"])

    def test_observation_vocabulary_rejects_alias_drift(self) -> None:
        with patch("boundary.challenge0.OBSERVATION_TYPES", (OnSide,)):
            with self.assertRaisesRegex(AssertionError, "disagree"):
                observation_vocabulary()

    def test_judgment_json_refuses_unknown_values(self) -> None:
        self.assertEqual(
            judgment_json(OnSide(0, 1)),
            {"kind": "OnSide", "mark": 0, "side": 1},
        )
        with self.assertRaisesRegex(TypeError, "unknown observation judgment"):
            judgment_json(object())

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
        kinds = observation_vocabulary()
        u_bad = dict(u, sides_collapsed=False)
        self.assertEqual(score(u_bad, o, census, kinds)["C0-1"]["status"], "MISSED")
        o_bad = dict(o, side_profiles=[["near", []], ["far", [0]]])
        self.assertEqual(score(u, o_bad, census, kinds)["C0-2"]["status"], "MISSED")
        u_follows = dict(u, event_follows_relation_empty=False)
        self.assertEqual(score(u_follows, o, census, kinds)["C0-3"]["status"], "MISSED")
        u_obs = dict(u, mark_observations=[{"kind": "OnSide", "mark": 0, "side": 0}])
        self.assertEqual(score(u_obs, o, census, kinds)["C0-4"]["status"], "MISSED")
        self.assertEqual(score(u, o, census, kinds + ["Empty"])["C0-4"]["status"], "MISSED")
        o_no_obs = dict(o, all_observations=[])
        self.assertEqual(score(u, o_no_obs, census, kinds)["C0-4"]["status"], "HIT")
        o_ren = dict(o, reflection_is_permitted_renaming=True)
        self.assertEqual(score(u, o_ren, census, kinds)["C0-5"]["status"], "MISSED")
        o_auto = dict(o, reflection_is_permitted_automorphism=True)
        self.assertEqual(score(u, o_auto, census, kinds)["C0-5"]["status"], "MISSED")

    def test_general_clause_fails_closed_when_census_fails(self) -> None:
        u = genesis_facts("U")
        o = genesis_facts("O")
        census = dict(reflection_census(1), fixed_iff_equal_counts=False)
        clause = score(u, o, census, observation_vocabulary())["C0-5"][
            "general_clause"
        ]
        self.assertEqual(clause["status"], "MISSED")
        self.assertIn("failed within", clause["fact"])

    def test_census_records_a_planted_equal_count_mismatch(self) -> None:
        with patch("boundary.challenge0.fixed_up_to_mark_renaming", return_value=False):
            self.assertFalse(reflection_census(0)["fixed_iff_equal_counts"])


if __name__ == "__main__":
    unittest.main()
