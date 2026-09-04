"""Tests of the Challenge 1 receipt: determinism, the frozen pins, the
scores of the frozen predictions and of C0-X, the negative direction of
the scorer, and the unpruned cross-checks of the bounded enumerations."""

from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import sys
import unittest
from typing import Any

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE / "code"))
sys.path.insert(0, str(TREE))

from boundary import challenge0  # noqa: E402
from boundary.challenge1 import (  # noqa: E402
    BOUNDARY_DEPENDENCE,
    C0_PREDICTIONS_SHA256,
    INSCRIPTION,
    JUDGMENT_DOMAIN_MAX_MARKS,
    PREDICTIONS_SHA256,
    REGIME_DOMAIN_MAX_MARKS,
    SEED_SHA256,
    build,
    event_json,
    event_returning_functions_by_module,
    history_json,
    invariant_under_permitted_renamings,
    judgment_domain,
    one_step_admissions,
    reading_facts,
    regime_domain,
    score,
    separating_judgments,
)
from boundary.model import (  # noqa: E402
    AdmitMark,
    OnSide,
    Regime,
    SideNamed,
    Supply,
    genesis,
    replay,
    step,
    supplied,
)
from run_challenge1 import render  # noqa: E402

Json = dict[str, Any]


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PinTests(unittest.TestCase):
    def test_seed_bytes_match_the_pin(self) -> None:
        self.assertEqual(sha(TREE / "SEED.md"), SEED_SHA256)
        self.assertEqual(SEED_SHA256, challenge0.SEED_SHA256)

    def test_predictions_bytes_match_the_pin(self) -> None:
        self.assertEqual(sha(TREE / "challenge1" / "PREDICTIONS.md"), PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge0" / "PREDICTIONS.md"), C0_PREDICTIONS_SHA256)

    def test_predictions_file_has_lf_endings(self) -> None:
        self.assertNotIn(b"\r", (TREE / "challenge1" / "PREDICTIONS.md").read_bytes())


class ReceiptTests(unittest.TestCase):
    def test_build_is_deterministic(self) -> None:
        self.assertEqual(build(), build())

    def test_committed_receipt_matches_the_renderer(self) -> None:
        path = TREE / "receipts" / "challenge1.json"
        self.assertTrue(path.exists(), "run run_challenge1.py first")
        self.assertEqual(path.read_bytes(), render())
        self.assertNotIn(b"\r", path.read_bytes())

    def test_receipt_carries_no_timestamp_or_environment(self) -> None:
        text = json.dumps(build(), sort_keys=True).lower()
        hit = re.search(r"\b(timestamp|time|date|python|platform|user)\b", text)
        self.assertIsNone(hit, hit.group(0) if hit else None)
        self.assertIn("candidates", text)

    def test_receipt_shape(self) -> None:
        receipt = build()
        self.assertEqual(receipt["challenge"], 1)
        self.assertEqual(receipt["inscription"], INSCRIPTION)
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertEqual(receipt["event_kinds"], ["Supply", "AdmitMark"])
        self.assertEqual(receipt["observation_vocabulary"], ["OnSide", "SideNamed"])
        self.assertEqual(receipt["state_event_generators"], [])
        self.assertEqual(
            receipt["event_returning_functions_by_module"],
            {
                "model": [],
                "presentation": ["admission_event", "supply_event"],
                # the census reads module members as they are, so the two
                # constructors imported from presentation are listed here too
                "challenge1": [
                    "admission_event",
                    "one_step_admissions",
                    "probes",
                    "supply_event",
                ],
            },
        )
        self.assertEqual(
            event_returning_functions_by_module(),
            receipt["event_returning_functions_by_module"],
        )
        self.assertEqual(receipt["boundary_dependence"], BOUNDARY_DEPENDENCE)
        self.assertEqual(
            sorted(receipt["what_the_challenge_exercises"]),
            sorted(
                [
                    "supply",
                    "mention",
                    "admission",
                    "current-state designation",
                    "retention",
                    "observation",
                    "side",
                    "equality",
                ]
            ),
        )


class FactTests(unittest.TestCase):
    def setUp(self) -> None:
        self.receipt = build()
        self.u = self.receipt["readings"]["U"]
        self.o = self.receipt["readings"]["O"]

    def test_scores(self) -> None:
        scores = self.receipt["scores"]
        for cid in ("C1-1", "C1-2", "C1-3", "C1-4", "C1-5", "C1-6", "C1-7"):
            self.assertEqual(scores[cid]["status"], "HIT", cid)
        for cid in ("C1-1", "C1-2", "C1-3", "C1-4", "C1-6"):
            self.assertEqual(scores[cid]["label"], "FORCED", cid)
        for cid in ("C1-5", "C1-7", "C1-X", "C0-X"):
            self.assertEqual(scores[cid]["label"], "NOT FORCED", cid)
        self.assertEqual(scores["C1-X"]["status"], "PENDING")
        self.assertEqual(scores["C0-X"]["status"], "HIT")
        self.assertEqual(scores["C0-X"]["U_half_status"], "HIT")
        self.assertEqual(scores["C0-X"]["O_half_status"], "HIT")

    def test_supply_is_presentation_only_under_both_readings(self) -> None:
        for rd in (self.u, self.o):
            sup = rd["supply"]
            self.assertEqual(sup["history"], [{"kind": "Supply", "token": "a"}])
            self.assertTrue(sup["regime_equals_genesis"])
            self.assertTrue(sup["certifies_genesis"])
            self.assertTrue(sup["observations_unchanged"])
            self.assertEqual(sup["mentioned"], ["a"])
            self.assertEqual(sup["supplied"], ["a"])
            self.assertEqual(sup["admitted"], [])
        self.assertEqual(self.u["supply"]["holding_judgments_after"], 0)
        self.assertEqual(self.o["supply"]["holding_judgments_after"], 2)

    def test_candidate_space_and_classes(self) -> None:
        self.assertEqual(self.u["candidate_space"]["count"], 2)
        self.assertEqual(self.o["candidate_space"]["count"], 2)
        self.assertEqual(self.u["candidate_space"]["classes_under_isomorphism"], 1)
        self.assertEqual(self.o["candidate_space"]["classes_under_isomorphism"], 2)
        self.assertEqual(self.u["retained_non_isomorphic_candidates"], [])
        self.assertEqual(
            self.o["retained_non_isomorphic_candidates"],
            [{"kind": "AdmitMark", "token": "a", "side": 1}],
        )

    def test_designated_current_is_by_the_declared_convention(self) -> None:
        for rd in (self.u, self.o):
            des = rd["designated_current"]
            self.assertEqual(des["convention"], "left is side 0")
            self.assertEqual(des["placement"], [0])
            self.assertTrue(des["certified"])
            self.assertEqual(
                [e["kind"] for e in des["history"]], ["Supply", "AdmitMark"]
            )
            conv = rd["convention"]
            self.assertEqual(conv["presented_side"], "left")
            self.assertFalse(conv["candidates_equal"])
            self.assertTrue(conv["other_is_reflection_of_designated"])
            self.assertEqual(conv["designation_is_by"], "declared convention, not proof")
        self.assertTrue(self.u["convention"]["isomorphic_under_reading"])
        self.assertEqual(
            self.u["convention"]["isomorphism_witness"],
            {"reflected": True, "permutation": [0]},
        )
        self.assertFalse(self.o["convention"]["isomorphic_under_reading"])
        self.assertIsNone(self.o["convention"]["isomorphism_witness"])

    def test_separating_judgments_under_each_reading(self) -> None:
        both = [
            {"kind": "OnSide", "mark": 0, "side": 0},
            {"kind": "OnSide", "mark": 0, "side": 1},
        ]
        self.assertEqual(self.u["convention"]["separating_judgments"], both)
        self.assertEqual(self.o["convention"]["separating_judgments"], both)
        self.assertEqual(
            self.u["convention"]["permitted_renaming_invariant_separating_judgments"], []
        )
        self.assertEqual(
            self.o["convention"]["permitted_renaming_invariant_separating_judgments"], both
        )

    def test_each_candidate_adds_exactly_its_own_judgment(self) -> None:
        for rd in (self.u, self.o):
            for cand in rd["candidates"]:
                side = cand["event"]["side"]
                expected = [{"kind": "OnSide", "mark": 0, "side": side}]
                self.assertEqual(cand["new_observations"], expected)
                self.assertEqual(cand["mark_profile"], expected)
                self.assertFalse(cand["other_side_judgment_holds"])
                self.assertTrue(cand["name_observations_unchanged"])
                self.assertFalse(cand["sides_collapsed"])
                self.assertTrue(cand["certified"])
                self.assertTrue(cand["unsupplied_admission_refused"])
                self.assertTrue(cand["initial_datum_unchanged"])
                self.assertTrue(cand["reading_unchanged"])
                self.assertTrue(cand["event_follows_relation_empty"])
                self.assertEqual(cand["marks"], 1)
                ret = cand["retention"]
                self.assertTrue(ret["regime_unchanged_by_supply_and_redesignation"])
                self.assertTrue(ret["mark_judgment_retained_after_same_token_probe"])
                self.assertTrue(ret["mark_judgment_retained_after_growth"])
                self.assertTrue(ret["growth_regime_has_two_marks"])
                self.assertEqual(cand["mentioned"], ["a"])
                self.assertEqual(cand["admitted"], ["a"])

    def test_event_and_history_json(self) -> None:
        self.assertEqual(event_json(Supply("a")), {"kind": "Supply", "token": "a"})
        self.assertEqual(
            history_json([Supply("a"), AdmitMark("a", 1)]),
            [{"kind": "Supply", "token": "a"}, {"kind": "AdmitMark", "token": "a", "side": 1}],
        )


class EnumerationCrossChecks(unittest.TestCase):
    def test_one_step_admissions_is_the_declared_bounded_space(self) -> None:
        g = genesis("U")
        self.assertEqual(
            one_step_admissions(g, frozenset({"a"})), [AdmitMark("a", 0), AdmitMark("a", 1)]
        )
        self.assertEqual(one_step_admissions(g, frozenset()), [])
        admitted = step(g, AdmitMark("a", 0))
        self.assertEqual(one_step_admissions(admitted, frozenset({"a"})), [])
        self.assertEqual(
            one_step_admissions(admitted, frozenset({"b", "a"})),
            [AdmitMark("b", 0), AdmitMark("b", 1)],
        )
        self.assertEqual(
            [e.token for e in one_step_admissions(g, frozenset({"z", "b"}))],
            ["b", "b", "z", "z"],
        )

    def test_declared_candidate_space_matches_an_unpruned_enumeration(self) -> None:
        for rd in ("U", "O"):
            g = genesis(rd)
            history = [Supply("a")]
            after = replay(history, g)
            declared = one_step_admissions(after, supplied(history))
            unpruned = [
                AdmitMark(token, side)
                for token in sorted(supplied(history))
                for side in (0, 1)
                if replay(history + [AdmitMark(token, side)], g) != after
            ]
            self.assertEqual(declared, unpruned)
            self.assertEqual(len(declared), 2)

    def test_domains_have_the_declared_sizes(self) -> None:
        self.assertEqual(len(judgment_domain(JUDGMENT_DOMAIN_MAX_MARKS)), 8)
        for rd in ("U", "O"):
            self.assertEqual(len(regime_domain(rd, REGIME_DOMAIN_MAX_MARKS)), 3)
            self.assertEqual(len(regime_domain(rd, 2)), 7)

    def test_invariance_under_permitted_renamings(self) -> None:
        u_domain = regime_domain("U", 2)
        o_domain = regime_domain("O", 1)
        self.assertFalse(invariant_under_permitted_renamings(OnSide(0, 0), u_domain))
        self.assertTrue(invariant_under_permitted_renamings(SideNamed(0, "near"), u_domain))
        self.assertTrue(invariant_under_permitted_renamings(OnSide(5, 0), u_domain))
        self.assertTrue(invariant_under_permitted_renamings(OnSide(0, 0), o_domain))
        self.assertFalse(invariant_under_permitted_renamings(OnSide(0, 0), regime_domain("O", 2)))

    def test_separating_judgments_are_the_holding_differences(self) -> None:
        a = Regime("O", ("a",), (0,))
        b = Regime("O", ("a",), (1,))
        self.assertEqual(
            separating_judgments(a, b, judgment_domain(1)),
            [OnSide(0, 0), OnSide(0, 1)],
        )
        self.assertEqual(separating_judgments(a, a, judgment_domain(1)), [])


class ScorerNegativeDirection(unittest.TestCase):
    def setUp(self) -> None:
        self.u = reading_facts("U")
        self.o = reading_facts("O")
        self.kinds = ["OnSide", "SideNamed"]
        self.events = ["Supply", "AdmitMark"]

    def run_score(self, u: Json | None = None, o: Json | None = None,
                  kinds: list[str] | None = None, events: list[str] | None = None) -> Json:
        return score(
            self.u if u is None else u,
            self.o if o is None else o,
            self.kinds if kinds is None else kinds,
            self.events if events is None else events,
        )

    def mutated(self, base: Json, path: list[Any], value: Any) -> Json:
        out = copy.deepcopy(base)
        node = out
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = value
        return out

    def test_baseline_hits(self) -> None:
        scores = self.run_score()
        for cid in ("C1-1", "C1-2", "C1-3", "C1-4", "C1-5", "C1-6", "C1-7", "C0-X"):
            self.assertEqual(scores[cid]["status"], "HIT", cid)

    def test_c1_1_misses_when_supply_changes_state(self) -> None:
        u = self.mutated(self.u, ["supply", "regime_equals_genesis"], False)
        self.assertEqual(self.run_score(u=u)["C1-1"]["status"], "MISSED")
        o = self.mutated(self.o, ["supply", "observations_unchanged"], False)
        self.assertEqual(self.run_score(o=o)["C1-1"]["status"], "MISSED")

    def test_c1_2_misses_on_unsupplied_admission_or_lost_retention(self) -> None:
        u = self.mutated(self.u, ["candidates", 0, "unsupplied_admission_refused"], False)
        self.assertEqual(self.run_score(u=u)["C1-2"]["status"], "MISSED")
        o = self.mutated(
            self.o, ["candidates", 1, "retention", "mark_judgment_retained_after_growth"], False
        )
        self.assertEqual(self.run_score(o=o)["C1-2"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["supply", "admitted"], ["a"])
        self.assertEqual(self.run_score(u=u2)["C1-2"]["status"], "MISSED")

    def test_c1_3_misses_on_a_second_judgment_or_a_changed_name(self) -> None:
        extra = [
            {"kind": "OnSide", "mark": 0, "side": 0},
            {"kind": "OnSide", "mark": 1, "side": 0},
        ]
        u = self.mutated(self.u, ["candidates", 0, "new_observations"], extra)
        self.assertEqual(self.run_score(u=u)["C1-3"]["status"], "MISSED")
        o = self.mutated(self.o, ["candidates", 0, "name_observations_unchanged"], False)
        self.assertEqual(self.run_score(o=o)["C1-3"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["supply", "holding_judgments_after"], 1)
        self.assertEqual(self.run_score(u=u2)["C1-3"]["status"], "MISSED")
        o2 = self.mutated(self.o, ["candidates", 1, "other_side_judgment_holds"], True)
        self.assertEqual(self.run_score(o=o2)["C1-3"]["status"], "MISSED")

    def test_c1_4_misses_when_u_separates_or_splits(self) -> None:
        u = self.mutated(
            self.u,
            ["convention", "permitted_renaming_invariant_separating_judgments"],
            [{"kind": "OnSide", "mark": 0, "side": 0}],
        )
        self.assertEqual(self.run_score(u=u)["C1-4"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["candidate_space", "classes_under_isomorphism"], 2)
        self.assertEqual(self.run_score(u=u2)["C1-4"]["status"], "MISSED")
        u3 = self.mutated(self.u, ["candidates", 1, "sides_collapsed"], True)
        self.assertEqual(self.run_score(u=u3)["C1-4"]["status"], "MISSED")

    def test_c1_5_misses_when_o_collapses_or_loses_the_branch(self) -> None:
        o = self.mutated(self.o, ["candidate_space", "classes_under_isomorphism"], 1)
        self.assertEqual(self.run_score(o=o)["C1-5"]["status"], "MISSED")
        o2 = self.mutated(self.o, ["convention", "isomorphic_under_reading"], True)
        self.assertEqual(self.run_score(o=o2)["C1-5"]["status"], "MISSED")
        o3 = self.mutated(self.o, ["retained_non_isomorphic_candidates"], [])
        self.assertEqual(self.run_score(o=o3)["C1-5"]["status"], "MISSED")
        o4 = self.mutated(self.o, ["convention", "other_is_reflection_of_designated"], False)
        self.assertEqual(self.run_score(o=o4)["C1-5"]["status"], "MISSED")

    def test_c1_6_misses_on_a_following_event_or_a_new_form(self) -> None:
        u = self.mutated(self.u, ["candidates", 0, "event_follows_relation_empty"], False)
        self.assertEqual(self.run_score(u=u)["C1-6"]["status"], "MISSED")
        self.assertEqual(self.run_score(kinds=self.kinds + ["Empty"])["C1-6"]["status"], "MISSED")
        self.assertEqual(self.run_score(events=self.events + ["Remove"])["C1-6"]["status"], "MISSED")
        o = self.mutated(self.o, ["candidates", 1, "reading_unchanged"], False)
        self.assertEqual(self.run_score(o=o)["C1-6"]["status"], "MISSED")

    def test_c1_7_misses_on_a_second_datum_or_mark(self) -> None:
        u = self.mutated(self.u, ["candidates", 0, "marks"], 2)
        self.assertEqual(self.run_score(u=u)["C1-7"]["status"], "MISSED")
        o = self.mutated(self.o, ["candidates", 0, "initial_datum_unchanged"], False)
        self.assertEqual(self.run_score(o=o)["C1-7"]["status"], "MISSED")

    def test_c0_x_halves_miss_independently(self) -> None:
        u = self.mutated(self.u, ["genesis_sides_collapsed"], False)
        c0x = self.run_score(u=u)["C0-X"]
        self.assertEqual(c0x["U_half_status"], "MISSED")
        self.assertEqual(c0x["O_half_status"], "HIT")
        self.assertEqual(c0x["status"], "MISSED")
        o = self.mutated(
            self.o,
            ["candidates", 0, "new_observations"],
            [
                {"kind": "OnSide", "mark": 0, "side": 0},
                {"kind": "SideNamed", "side": 0, "name": "left"},
            ],
        )
        c0x = self.run_score(o=o)["C0-X"]
        self.assertEqual(c0x["U_half_status"], "HIT")
        self.assertEqual(c0x["O_half_status"], "MISSED")
        self.assertEqual(c0x["status"], "MISSED")
        c0x = self.run_score(events=self.events + ["Remove"])["C0-X"]
        self.assertEqual(c0x["U_half_status"], "MISSED")


if __name__ == "__main__":
    unittest.main()
