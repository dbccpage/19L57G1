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
from unittest.mock import patch

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE / "code"))
sys.path.insert(0, str(TREE))

from boundary import challenge0, model  # noqa: E402
from boundary.challenge1 import (  # noqa: E402
    BOUNDARY_DEPENDENCE,
    C0_PREDICTIONS_SHA256,
    DEFINITION_LEVEL_PREDICTIONS,
    INSCRIPTION,
    JUDGMENT_DOMAIN_MAX_MARKS,
    PREDICTIONS_SHA256,
    REGIME_DOMAIN_MAX_MARKS,
    SCORED_PREDICTIONS,
    SEED_SHA256,
    STATE_CHANGING_EVENT_KINDS,
    TALLY_CRITERION,
    build,
    candidate_classes,
    current_state_facts,
    event_json,
    event_returning_functions_by_module,
    history_json,
    invariant_under_permitted_renamings,
    judgment_domain,
    one_step_admissions,
    reading_facts,
    refusal,
    regime_domain,
    retention_facts,
    score,
    separating_judgments,
    tally,
)
from boundary.model import (  # noqa: E402
    AdmitMark,
    Event,
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

# A watched word is a hit when it is not glued to letters on either side,
# so ``build_date`` and ``run_timestamp`` are caught while ``candidates``
# is not.  ``\b`` would treat ``_`` as a word character and miss both.
ENVIRONMENT_SCAN = re.compile(r"(?<![a-z])(timestamp|time|date|python|platform|user)(?![a-z])")


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment_hits(payload: object) -> list[str]:
    return ENVIRONMENT_SCAN.findall(json.dumps(payload, sort_keys=True).lower())


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
        receipt = build()
        self.assertEqual(environment_hits(receipt), [])
        self.assertIn("candidates", json.dumps(receipt, sort_keys=True).lower())

    def test_environment_scan_catches_planted_snake_case_keys(self) -> None:
        planted = dict(build())
        planted["build_date"] = "probe"
        planted["run_timestamp"] = "probe"
        planted["python_version"] = "probe"
        self.assertEqual(environment_hits(planted), ["date", "python", "timestamp"])
        self.assertIsNone(re.search(r"\b(timestamp|date|python)\b", "build_date run_timestamp python_version"))
        self.assertEqual(environment_hits({"candidates": [], "updated_marks": 0}), [])

    def test_receipt_shape(self) -> None:
        receipt = build()
        self.assertEqual(receipt["challenge"], 1)
        self.assertEqual(receipt["inscription"], INSCRIPTION)
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertEqual(receipt["event_kinds"], ["Supply", "AdmitMark"])
        self.assertEqual(receipt["state_changing_event_kinds"], ["AdmitMark"])
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
        self.assertEqual(receipt["tally"], tally(receipt["scores"]))
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
        for cid in ("C1-1", "C1-3", "C1-6", "C1-7"):
            self.assertEqual(scores[cid]["status"], "HIT", cid)
        self.assertEqual(scores["C1-2"]["status"], "PARTIAL")
        self.assertEqual(scores["C1-2"]["facts_status"], "HIT")
        self.assertEqual(scores["C1-2"]["either_side_readmission_clause_status"], "MISSED")
        self.assertNotIn("readmission_clause_status", scores["C1-2"])
        self.assertEqual(scores["C1-4"]["status"], "PARTIAL")
        self.assertEqual(scores["C1-4"]["facts_status"], "HIT")
        self.assertEqual(scores["C1-4"]["only_event_clause_status"], "MISSED")
        self.assertEqual(scores["C1-4"]["only_state_changing_event_status"], "HIT")
        self.assertEqual(scores["C1-5"]["status"], "PARTIAL")
        self.assertEqual(scores["C1-5"]["facts_status"], "HIT")
        self.assertEqual(scores["C1-5"]["current_state_designation_status"], "MISSED")
        self.assertTrue(scores["C1-7"]["result_basis"].startswith("DEFINITION-level"))
        self.assertIn("proxy", scores["C1-7"]["mechanical_part"])
        # The DEFINITION-level bases are receipt facts, one per listed
        # prediction, and the one content hit says why it is not by unfolding.
        for cid in DEFINITION_LEVEL_PREDICTIONS:
            self.assertTrue(scores[cid]["result_basis"].startswith("DEFINITION-level"), cid)
            self.assertIn("not counted as content", scores[cid]["result_basis"], cid)
        self.assertTrue(scores["C1-3"]["result_basis"].startswith("content"))
        self.assertIn("none of them by unfolding", scores["C1-3"]["result_basis"])
        for cid in ("C1-2", "C1-4", "C1-5"):
            self.assertNotIn("result_basis", scores[cid], cid)
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

    def test_current_state_is_the_replay_of_the_supplied_only_history(self) -> None:
        for rd in (self.u, self.o):
            cur = rd["current_state"]
            self.assertEqual(cur["history"], [{"kind": "Supply", "token": "a"}])
            self.assertEqual(cur["placement"], [])
            self.assertEqual(cur["marks"], 0)
            self.assertTrue(cur["regime_equals_genesis"])
            self.assertTrue(cur["certified"])
            self.assertFalse(cur["admitted_candidate_is_current"])
            self.assertIn("did not retain", cur["rule"])

    def test_current_state_designation_is_candidate_membership(self) -> None:
        # The fact is membership in the candidate regimes, not "has a mark":
        # a caller history admitting another token has a mark and no
        # Challenge 1 candidate current.  The withdrawn proxy read True there.
        g = genesis("O")
        supplied_only: list[Event] = [Supply("a")]
        candidates = [replay(supplied_only + [AdmitMark("a", s)], g) for s in (0, 1)]
        facts = current_state_facts(g, supplied_only, candidates)
        self.assertFalse(facts["admitted_candidate_is_current"])
        self.assertEqual(facts["marks"], 0)
        # a hypothetical caller history that admits: no such history is the
        # caller's at Challenge 1, and what Challenge 2's "retains" admits is
        # that rung's decision, so this is not called a retention here
        admitted_by_caller: list[Event] = [Supply("a"), AdmitMark("a", 1)]
        facts = current_state_facts(g, admitted_by_caller, candidates)
        self.assertTrue(facts["admitted_candidate_is_current"])
        self.assertEqual(facts["marks"], 1)
        other: list[Event] = [Supply("z"), AdmitMark("z", 0)]
        facts = current_state_facts(g, other, candidates)
        self.assertFalse(facts["admitted_candidate_is_current"])
        self.assertEqual(facts["marks"], 1)
        self.assertFalse(
            current_state_facts(g, admitted_by_caller, [])["admitted_candidate_is_current"]
        )

    def test_moving_admission_fact_reads_accepted_and_inert_only_when_the_kernel_absorbs(self) -> None:
        # The other-side half of the frozen C1-2 parenthetical is a fact
        # about the kernel: the repaired kernel refuses the moving admission
        # and the fact is false; a kernel that absorbs it as the pre-repair
        # one did makes the fact true and the refusal false.
        g = genesis("U")
        history: list[Event] = [Supply("a"), AdmitMark("a", 0)]
        r = replay(history, g)
        facts = retention_facts(g, history, r, AdmitMark("a", 0))
        self.assertTrue(facts["moving_admission_refused"])
        self.assertFalse(facts["moving_admission_accepted_and_inert"])
        real_step = model.step

        def absorbing_step(regime: Regime, e: Event) -> Regime:
            if isinstance(e, AdmitMark) and e.token in regime.marks:
                return regime
            return real_step(regime, e)

        with patch.object(model, "step", absorbing_step):
            absorbed = retention_facts(g, history, r, AdmitMark("a", 0))
        self.assertFalse(absorbed["moving_admission_refused"])
        self.assertIsNone(absorbed["moving_admission_refusal"])
        self.assertTrue(absorbed["moving_admission_accepted_and_inert"])

    def test_candidate_space_and_classes(self) -> None:
        self.assertEqual(self.u["candidate_space"]["count"], 2)
        self.assertEqual(self.o["candidate_space"]["count"], 2)
        self.assertEqual(self.u["candidate_space"]["classes_under_isomorphism"], 1)
        self.assertEqual(self.o["candidate_space"]["classes_under_isomorphism"], 2)
        side0 = {"kind": "AdmitMark", "token": "a", "side": 0}
        side1 = {"kind": "AdmitMark", "token": "a", "side": 1}
        self.assertEqual(
            self.u["candidate_classes"],
            [{"canonical_key": ["U", [0]], "members": [side0, side1]}],
        )
        self.assertEqual(
            self.o["candidate_classes"],
            [
                {"canonical_key": ["O", [0]], "members": [side0]},
                {"canonical_key": ["O", [1]], "members": [side1]},
            ],
        )
        for rd in (self.u, self.o):
            self.assertEqual(
                sorted(m["side"] for cls in rd["candidate_classes"] for m in cls["members"]),
                [0, 1],
            )

    def test_convention_selects_a_candidate_and_admits_nothing(self) -> None:
        for rd in (self.u, self.o):
            conv = rd["convention"]
            self.assertEqual(conv["declared"], "left is side 0")
            self.assertEqual(conv["presented_side"], "left")
            self.assertEqual(conv["candidate_event"], {"kind": "AdmitMark", "token": "a", "side": 0})
            self.assertEqual(conv["other_event"], {"kind": "AdmitMark", "token": "a", "side": 1})
            self.assertEqual(conv["candidate_placement"], [0])
            self.assertEqual(conv["other_placement"], [1])
            self.assertFalse(conv["candidates_equal"])
            self.assertTrue(conv["other_is_reflection_of_candidate"])
            self.assertIn("admits nothing", conv["selection_is_by"])
            self.assertIn(conv["candidate_event"], [c["event"] for c in rd["candidates"]])
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
                self.assertEqual([e["kind"] for e in cand["history"]], ["Supply", "AdmitMark"])
                ret = cand["retention"]
                self.assertTrue(ret["regime_unchanged_by_supply_and_readmission"])
                self.assertTrue(ret["mark_judgment_retained_after_readmission"])
                self.assertTrue(ret["moving_admission_refused"])
                self.assertFalse(ret["moving_admission_accepted_and_inert"])
                self.assertEqual(
                    ret["moving_admission_refusal"],
                    f"mark 'a' is admitted on side {side}; an admission naming side "
                    f"{1 - side} would move it and is refused",
                )
                self.assertEqual(
                    ret["moving_admission_probe"],
                    [{"kind": "AdmitMark", "token": "a", "side": 1 - side}],
                )
                self.assertEqual([e["kind"] for e in ret["readmission_probe"]], ["Supply", "Supply", "AdmitMark"])
                self.assertEqual(ret["readmission_probe"][-1]["side"], side)
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

    def test_refusal_names_the_refused_history_and_is_silent_otherwise(self) -> None:
        g = genesis("U")
        self.assertIsNone(refusal([Supply("a"), AdmitMark("a", 0)], g))
        self.assertEqual(
            refusal([Supply("a"), AdmitMark("a", 0), AdmitMark("a", 1)], g),
            "mark 'a' is admitted on side 0; an admission naming side 1 would move it and is refused",
        )
        self.assertEqual(refusal([AdmitMark("a", 0)], g), "mark 'a' was not supplied before admission")


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
            history: list[Event] = [Supply("a")]
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

    def test_candidate_classes_group_by_canonical_key(self) -> None:
        history: list[Event] = [Supply("a")]
        u = candidate_classes(genesis("U"), history, [AdmitMark("a", 0), AdmitMark("a", 1)])
        self.assertEqual(len(u), 1)
        self.assertEqual(len(u[0]["members"]), 2)
        o = candidate_classes(genesis("O"), history, [AdmitMark("a", 0), AdmitMark("a", 1)])
        self.assertEqual([cls["canonical_key"] for cls in o], [["O", [0]], ["O", [1]]])
        self.assertEqual(candidate_classes(genesis("O"), history, []), [])

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

    def run_score(
        self,
        u: Json | None = None,
        o: Json | None = None,
        kinds: list[str] | None = None,
        events: list[str] | None = None,
        state_changing: list[str] | None = None,
    ) -> Json:
        return score(
            self.u if u is None else u,
            self.o if o is None else o,
            self.kinds if kinds is None else kinds,
            self.events if events is None else events,
            STATE_CHANGING_EVENT_KINDS if state_changing is None else state_changing,
        )

    def mutated(self, base: Json, path: list[Any], value: Any) -> Json:
        out = copy.deepcopy(base)
        node = out
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = value
        return out

    def test_baseline(self) -> None:
        scores = self.run_score()
        for cid in ("C1-1", "C1-3", "C1-6", "C1-7", "C0-X"):
            self.assertEqual(scores[cid]["status"], "HIT", cid)
        for cid in ("C1-2", "C1-4", "C1-5"):
            self.assertEqual(scores[cid]["status"], "PARTIAL", cid)
            self.assertEqual(scores[cid]["facts_status"], "HIT", cid)

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

    def test_c1_2_misses_when_a_moving_admission_is_accepted_and_moves_the_mark(self) -> None:
        # Accepted, not refused, and not inert: the falsifier "an event that
        # moves the admitted mark" fires, so the facts miss.
        o = self.mutated(self.o, ["candidates", 0, "retention", "moving_admission_refused"], False)
        scores = self.run_score(o=o)
        self.assertEqual(scores["C1-2"]["status"], "MISSED")
        self.assertEqual(scores["C1-2"]["facts_status"], "MISSED")
        self.assertEqual(scores["C1-2"]["either_side_readmission_clause_status"], "MISSED")
        u = self.mutated(
            self.u, ["candidates", 1, "retention", "regime_unchanged_by_supply_and_readmission"], False
        )
        self.assertEqual(self.run_score(u=u)["C1-2"]["status"], "MISSED")

    def test_c1_2_either_side_clause_hits_only_when_every_moving_admission_is_accepted_and_inert(
        self,
    ) -> None:
        # The frozen parenthetical, read literally, hits only under a kernel
        # that accepts the other-side re-admission and leaves the regime
        # unchanged, on every candidate.  The real receipt refuses it:
        # facts HIT, clause MISSED, PARTIAL.
        scores = self.run_score()
        self.assertEqual(scores["C1-2"]["status"], "PARTIAL")
        self.assertEqual(scores["C1-2"]["facts_status"], "HIT")
        self.assertEqual(scores["C1-2"]["either_side_readmission_clause_status"], "MISSED")
        o = self.mutated(self.o, ["candidates", 0, "retention", "moving_admission_refused"], False)
        o = self.mutated(o, ["candidates", 0, "retention", "moving_admission_accepted_and_inert"], True)
        scores = self.run_score(o=o)
        self.assertEqual(scores["C1-2"]["status"], "PARTIAL")
        self.assertEqual(scores["C1-2"]["facts_status"], "HIT")
        self.assertEqual(scores["C1-2"]["either_side_readmission_clause_status"], "MISSED")
        u = self.u
        for i in (0, 1):
            u = self.mutated(u, ["candidates", i, "retention", "moving_admission_refused"], False)
            u = self.mutated(u, ["candidates", i, "retention", "moving_admission_accepted_and_inert"], True)
            o = self.mutated(o, ["candidates", i, "retention", "moving_admission_refused"], False)
            o = self.mutated(o, ["candidates", i, "retention", "moving_admission_accepted_and_inert"], True)
        scores = self.run_score(u=u, o=o)
        self.assertEqual(scores["C1-2"]["status"], "HIT")
        self.assertEqual(scores["C1-2"]["facts_status"], "HIT")
        self.assertEqual(scores["C1-2"]["either_side_readmission_clause_status"], "HIT")

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

    def test_c1_4_only_event_clause_is_scored_literally(self) -> None:
        # The literal clause would hit only if the history were the admission
        # alone; a supply is an event, so the actual two-event history is a
        # literal miss and a state-changing hit, hence PARTIAL.
        admission_only = [{"kind": "AdmitMark", "token": "a", "side": 0}]
        u = self.mutated(self.u, ["candidates", 0, "history"], admission_only)
        u = self.mutated(u, ["candidates", 1, "history"], [{"kind": "AdmitMark", "token": "a", "side": 1}])
        scores = self.run_score(u=u)
        self.assertEqual(scores["C1-4"]["status"], "HIT")
        self.assertEqual(scores["C1-4"]["only_event_clause_status"], "HIT")
        two_admissions = [
            {"kind": "AdmitMark", "token": "a", "side": 0},
            {"kind": "AdmitMark", "token": "b", "side": 0},
        ]
        u2 = self.mutated(self.u, ["candidates", 0, "history"], two_admissions)
        scores = self.run_score(u=u2)
        self.assertEqual(scores["C1-4"]["status"], "MISSED")
        self.assertEqual(scores["C1-4"]["facts_status"], "HIT")
        self.assertEqual(scores["C1-4"]["only_state_changing_event_status"], "MISSED")
        # a supply counted as state-changing would fail the weaker reading too
        self.assertEqual(
            self.run_score(state_changing=["Supply", "AdmitMark"])["C1-4"]["status"], "MISSED"
        )

    def test_c1_5_misses_when_o_collapses_or_loses_the_branch(self) -> None:
        o = self.mutated(self.o, ["candidate_space", "classes_under_isomorphism"], 1)
        self.assertEqual(self.run_score(o=o)["C1-5"]["status"], "MISSED")
        o2 = self.mutated(self.o, ["convention", "isomorphic_under_reading"], True)
        self.assertEqual(self.run_score(o=o2)["C1-5"]["status"], "MISSED")
        o3 = self.mutated(self.o, ["candidate_classes"], self.o["candidate_classes"][:1])
        self.assertEqual(self.run_score(o=o3)["C1-5"]["status"], "MISSED")
        o4 = self.mutated(self.o, ["convention", "other_is_reflection_of_candidate"], False)
        self.assertEqual(self.run_score(o=o4)["C1-5"]["status"], "MISSED")
        o5 = self.mutated(
            self.o, ["convention", "candidate_event"], {"kind": "AdmitMark", "token": "z", "side": 0}
        )
        self.assertEqual(self.run_score(o=o5)["C1-5"]["status"], "MISSED")

    def test_c1_5_designation_clause_hits_only_if_an_admitted_candidate_were_current(self) -> None:
        scores = self.run_score()
        self.assertEqual(scores["C1-5"]["status"], "PARTIAL")
        self.assertEqual(scores["C1-5"]["current_state_designation_status"], "MISSED")
        o = self.mutated(self.o, ["current_state", "admitted_candidate_is_current"], True)
        scores = self.run_score(o=o)
        self.assertEqual(scores["C1-5"]["status"], "HIT")
        self.assertEqual(scores["C1-5"]["current_state_designation_status"], "HIT")

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

    def test_tally_counts_definition_level_hits_apart_from_content(self) -> None:
        # The tally the paper reports is computed from the statuses and the
        # declared DEFINITION-level list: C1-3 is the one content hit, C1-1,
        # C1-6, and C1-7 hit by construction, and the three PARTIALs are
        # neither.  The list is declared, not inferred from the receipt.
        counted = tally(self.run_score())
        self.assertEqual(counted["scored"], list(SCORED_PREDICTIONS))
        self.assertEqual(counted["definition_level_declared"], ["C1-1", "C1-6", "C1-7"])
        self.assertEqual(counted["criterion"], TALLY_CRITERION)
        self.assertEqual(counted["hit_as_content"], ["C1-3"])
        self.assertEqual(counted["hit_definition_level"], ["C1-1", "C1-6", "C1-7"])
        self.assertEqual(counted["partial"], ["C1-2", "C1-4", "C1-5"])
        self.assertEqual(counted["missed"], [])
        self.assertEqual(
            sorted(counted["hit_as_content"] + counted["hit_definition_level"]
                   + counted["partial"] + counted["missed"]),
            sorted(SCORED_PREDICTIONS),
        )
        self.assertNotIn("C0-X", counted["scored"])
        self.assertNotIn("C1-X", counted["scored"])

    def test_tally_moves_a_miss_out_of_every_hit_list_and_refuses_an_unknown_status(
        self,
    ) -> None:
        # A DEFINITION-level prediction that misses is a miss, not a hit by
        # construction; a content prediction that misses leaves the content
        # list empty; a status outside HIT, PARTIAL, MISSED is refused by
        # name rather than silently dropped from the count.
        scores = self.run_score()
        missed_definition = self.mutated(scores, ["C1-1", "status"], "MISSED")
        counted = tally(missed_definition)
        self.assertEqual(counted["hit_definition_level"], ["C1-6", "C1-7"])
        self.assertEqual(counted["missed"], ["C1-1"])
        self.assertEqual(counted["hit_as_content"], ["C1-3"])
        missed_content = self.mutated(scores, ["C1-3", "status"], "MISSED")
        counted = tally(missed_content)
        self.assertEqual(counted["hit_as_content"], [])
        self.assertEqual(counted["missed"], ["C1-3"])
        self.assertEqual(counted["hit_definition_level"], ["C1-1", "C1-6", "C1-7"])
        partial_definition = self.mutated(scores, ["C1-6", "status"], "PARTIAL")
        counted = tally(partial_definition)
        self.assertEqual(counted["partial"], ["C1-2", "C1-4", "C1-5", "C1-6"])
        self.assertEqual(counted["hit_definition_level"], ["C1-1", "C1-7"])
        with self.assertRaisesRegex(ValueError, "unexpected status 'PENDING' for C1-2"):
            tally(self.mutated(scores, ["C1-2", "status"], "PENDING"))

    def test_c0_x_halves_miss_independently(self) -> None:
        u = self.mutated(self.u, ["genesis_sides_collapsed"], False)
        c0x = self.run_score(u=u)["C0-X"]
        self.assertEqual(c0x["U_half_status"], "MISSED")
        self.assertEqual(c0x["O_half_status"], "HIT")
        self.assertEqual(c0x["status"], "MISSED")
        o = self.mutated(
            self.o,
            ["candidates", 1, "new_observations"],
            [
                {"kind": "OnSide", "mark": 0, "side": 1},
                {"kind": "SideNamed", "side": 0, "name": "left"},
            ],
        )
        c0x = self.run_score(o=o)["C0-X"]
        self.assertEqual(c0x["U_half_status"], "HIT")
        self.assertEqual(c0x["O_half_status"], "MISSED")
        self.assertEqual(c0x["status"], "MISSED")
        c0x = self.run_score(events=self.events + ["Remove"])["C0-X"]
        self.assertEqual(c0x["U_half_status"], "MISSED")
        u2 = self.mutated(self.u, ["candidates", 1, "sides_collapsed"], True)
        self.assertEqual(self.run_score(u=u2)["C0-X"]["U_half_status"], "MISSED")


if __name__ == "__main__":
    unittest.main()
