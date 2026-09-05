"""Tests of the Challenge 3 receipt: determinism, the frozen pins, replay from
genesis for every candidate history, the declared candidate space and its
exhaustiveness over its own coordinates, the two cost measures, the minima and
their quotient, the scores of the frozen predictions and of C2-X, the negative
direction of the scorer, and the unpruned cross-checks of every bounded
enumeration."""

from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import sys
import unittest
from itertools import permutations, product
from typing import Any
from unittest.mock import patch

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE / "code"))
sys.path.insert(0, str(TREE))

from boundary import challenge3  # noqa: E402
from boundary.challenge3 import (  # noqa: E402
    C0_PREDICTIONS_SHA256,
    C1_PREDICTIONS_SHA256,
    C2_PREDICTIONS_SHA256,
    COLLATERAL_FACTS,
    COORDINATES,
    DECLARED_MARK_PROPERTIES,
    DEFINITION_LEVEL_PREDICTIONS,
    EXTRA_MARK_VALUES,
    NULL_AUGMENTATION,
    PREDICTIONS_SHA256,
    PROPERTY_DOMAIN_MAX_MARKS,
    READING_O_BUNDLE,
    SCORED_PREDICTIONS,
    SEED_SHA256,
    Augmentation,
    build,
    candidate_history,
    candidate_space,
    capabilities,
    changed_coordinates,
    class_key,
    collateral_facts,
    comparison_regimes,
    counterfactual_square,
    domain_images,
    expected_placement,
    effective_structure,
    flags,
    is_one_step,
    key_of,
    minima,
    mu1,
    mu2,
    on_side_0,
    one_step_detail,
    orbit_property_separates,
    point_name,
    price_facts,
    probes,
    process_admission,
    property_domain,
    property_invariant,
    property_separates,
    reading_facts,
    requirement_met,
    score,
    sides_fact_agrees_with_the_requirement,
    tally,
)
from boundary.model import (  # noqa: E402
    READING_O,
    READING_U,
    AdmitMark,
    AdmitOccurrence,
    automorphisms_under,
    Event,
    Regime,
    Supply,
    genesis,
    permitted_images_under,
    replay,
    serialize,
)
from boundary.presentation import DECLARED_CONVENTION, read_whole  # noqa: E402
from run_challenge3 import render  # noqa: E402

Json = dict[str, Any]

# The same whole-word scan the earlier receipt tests use: a watched word glued
# to letters is not a hit, but one joined by an underscore or a digit is.
ENVIRONMENT_SCAN = re.compile(r"(?<![a-z])(timestamp|time|date|python|platform|user)(?![a-z])")


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment_hits(payload: object) -> list[str]:
    return ENVIRONMENT_SCAN.findall(json.dumps(payload, sort_keys=True).lower())


def rebuild(history: list[dict[str, object]]) -> list[Event]:
    """Rebuild the events of a rendered history, so the receipt's own histories
    are replayed rather than trusted."""
    out: list[Event] = []
    for row in history:
        token = str(row["token"])
        if row["kind"] == "Supply":
            out.append(Supply(token))
        else:
            out.append(AdmitOccurrence(token, int(str(row["side"]))))
    return out


class PinTests(unittest.TestCase):
    def test_predictions_bytes_match_the_pin(self) -> None:
        self.assertEqual(sha(TREE / "challenge3" / "PREDICTIONS.md"), PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge2" / "PREDICTIONS.md"), C2_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge1" / "PREDICTIONS.md"), C1_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge0" / "PREDICTIONS.md"), C0_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "SEED.md"), SEED_SHA256)

    def test_predictions_file_has_lf_endings(self) -> None:
        self.assertNotIn(b"\r", (TREE / "challenge3" / "PREDICTIONS.md").read_bytes())


class ReceiptTests(unittest.TestCase):
    def test_build_is_deterministic(self) -> None:
        self.assertEqual(build(), build())

    def test_committed_receipt_matches_the_renderer(self) -> None:
        path = TREE / "receipts" / "challenge3.json"
        self.assertTrue(path.exists(), "run run_challenge3.py first")
        self.assertEqual(path.read_bytes(), render())
        self.assertNotIn(b"\r", path.read_bytes())

    def test_receipt_is_inside_the_declared_split_threshold(self) -> None:
        # Over a megabyte the rung would owe a summary and a gzip with a
        # content hash; it is well inside, so it is committed whole.
        self.assertLess(len(render()), 1_000_000)

    def test_receipt_carries_no_timestamp_or_environment(self) -> None:
        receipt = build()
        self.assertEqual(environment_hits(receipt), [])
        self.assertIn("orbit", json.dumps(receipt, sort_keys=True).lower())

    def test_receipt_shape(self) -> None:
        receipt = build()
        self.assertEqual(receipt["challenge"], 3)
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertEqual(receipt["new_event_kinds_at_challenge_3"], [])
        self.assertEqual(receipt["event_kinds"], ["Supply", "AdmitMark", "AdmitOccurrence"])
        self.assertEqual(receipt["observation_vocabulary"], ["OnSide", "SideNamed"])
        self.assertEqual(receipt["state_event_generators"], [])
        self.assertEqual(receipt["candidate_space"]["coordinates"], list(COORDINATES))
        self.assertEqual(receipt["candidate_space"]["size"], 48)
        self.assertEqual(receipt["collateral_facts"], list(COLLATERAL_FACTS))
        self.assertEqual(receipt["property_domain_size"], 85)
        self.assertEqual(receipt["tally"], tally(receipt["scores"]))
        self.assertEqual(
            receipt["event_returning_functions_by_module"],
            {
                "model": [],
                "presentation": ["admission_event", "supply_event"],
                "challenge2": ["caller_history", "policy_event", "probes", "supply_event"],
                # the census reads module members as they are, so what the
                # Challenge 3 module imports from elsewhere is listed here too
                "challenge3": [
                    "caller_history",
                    "candidate_history",
                    "probes",
                    "process_admission",
                ],
            },
        )


class SpaceTests(unittest.TestCase):
    def test_the_space_is_the_product_of_its_declared_coordinates(self) -> None:
        space = candidate_space()
        self.assertEqual(len(space), 48)
        self.assertEqual(len(set(space)), 48)
        self.assertEqual(
            len(space), 2 * 2 * 2 * 2 * len(EXTRA_MARK_VALUES)
        )
        self.assertEqual(space[0], NULL_AUGMENTATION)
        self.assertEqual([point_name(a) for a in space].count("base"), 1)

    def test_side_zero_is_a_moved_coordinate(self) -> None:
        # The defect this test holds: `extra_mark = 0` is a move off the
        # inherited `None`, and a truth test would silently drop it, `0` and
        # falsehood being equal in this language.  It was live and the point
        # `extra_mark_0` disappeared from the enumeration.
        aug = Augmentation(extra_mark=0)
        self.assertEqual(changed_coordinates(aug), ["extra_mark"])
        self.assertEqual(mu1(aug), 1)
        self.assertTrue(is_one_step(aug))
        self.assertEqual(point_name(aug), "extra_mark_0")
        self.assertIn(aug, candidate_space())

    def test_one_step_is_exactly_capability_count_one(self) -> None:
        for aug in candidate_space():
            self.assertEqual(is_one_step(aug), mu1(aug) == 1, aug)
            self.assertEqual(len(capabilities(aug)), len(changed_coordinates(aug)), aug)

    def test_the_reading_O_bundle_is_refused_as_two_capabilities(self) -> None:
        self.assertEqual(mu1(READING_O_BUNDLE), 2)
        self.assertFalse(is_one_step(READING_O_BUNDLE))
        self.assertEqual(point_name(READING_O_BUNDLE), "withdraw_reflection+admit_names")

    def test_the_effective_structure_collapses_the_no_ops_under_O(self) -> None:
        # Under O, withdrawing an already absent side exchange and admitting
        # already admitted names change nothing, so the quotient must not
        # count them as different structures; under U they are different.
        for aug in (Augmentation(withdraw_reflection=True), Augmentation(admit_names=True)):
            self.assertEqual(
                effective_structure(READING_O, aug),
                effective_structure(READING_O, NULL_AUGMENTATION),
                aug,
            )
            self.assertNotEqual(
                effective_structure(READING_U, aug),
                effective_structure(READING_U, NULL_AUGMENTATION),
                aug,
            )

    def test_the_process_admission_needs_no_new_supply(self) -> None:
        wholes = [read_whole(text) for text in ("<a|>", "<|a>")]
        g = genesis(READING_U)
        aug = Augmentation(extra_mark=1)
        self.assertEqual(process_admission(NULL_AUGMENTATION), [])
        self.assertEqual(process_admission(aug), [AdmitOccurrence("a", 1)])
        history = candidate_history(wholes, aug, DECLARED_CONVENTION, False)
        self.assertEqual(len(history), 5)
        self.assertEqual(list(replay(history, g).placement), [0, 1, 1])


class FactTests(unittest.TestCase):
    def setUp(self) -> None:
        self.receipt = build()
        self.u = self.receipt["readings"]["U"]
        self.o = self.receipt["readings"]["O"]

    def test_scores(self) -> None:
        scores = self.receipt["scores"]
        for cid in SCORED_PREDICTIONS:
            self.assertEqual(scores[cid]["status"], "HIT", cid)
        self.assertEqual(scores["C3-X"]["status"], "PENDING")
        self.assertEqual(scores["C2-X"]["status"], "PARTIAL")
        for cid in DEFINITION_LEVEL_PREDICTIONS:
            self.assertTrue(scores[cid]["result_basis"].startswith("DEFINITION-level"), cid)
            self.assertIn("not counted as content", scores[cid]["result_basis"], cid)
        for cid in ("C3-2", "C3-3", "C3-5", "C3-6", "C3-7", "C3-8"):
            self.assertTrue(scores[cid]["result_basis"].startswith("content"), cid)
        for cid in ("C3-2", "C3-3", "C3-5", "C3-6", "C3-7"):
            self.assertEqual(scores[cid]["label"], "FORCED", cid)
        for cid in ("C3-1", "C3-4", "C3-8", "C3-X", "C2-X"):
            self.assertEqual(scores[cid]["label"], "NOT FORCED", cid)

    def test_the_previous_extrapolation_is_scored_clause_by_clause(self) -> None:
        c2x = self.receipt["scores"]["C2-X"]
        self.assertEqual(c2x["sense_clause_status"], "HIT")
        self.assertEqual(c2x["O_already_satisfied_clause_status"], "HIT")
        self.assertEqual(c2x["U_unsatisfied_clause_status"], "HIT")
        self.assertEqual(c2x["no_judgment_only_augmentation_clause_status"], "HIT")
        self.assertEqual(c2x["tied_minima_clause_status"], "HIT")
        # the recorded miss, and its own falsifier: two retained minima pay
        # neither a side name nor a further datum
        self.assertEqual(
            c2x["every_minimum_names_a_side_or_admits_a_datum_clause_status"], "MISSED"
        )
        self.assertEqual(c2x["same_clause_on_the_weaker_reading_status"], "MISSED")
        self.assertEqual(c2x["status"], "PARTIAL")

    def test_tally_counts(self) -> None:
        counted = self.receipt["tally"]
        self.assertEqual(
            counted["hit_as_content"], ["C3-2", "C3-3", "C3-5", "C3-6", "C3-7", "C3-8"]
        )
        self.assertEqual(counted["hit_definition_level"], ["C3-1", "C3-4"])
        self.assertEqual(counted["partial"], [])
        self.assertEqual(counted["missed"], [])

    def test_every_candidate_history_replays_from_genesis(self) -> None:
        checked = 0
        for name, rd in self.receipt["readings"].items():
            g = genesis(name)
            for row in [rd["base"], *rd["one_step_detail"]]:
                events = rebuild(list(row["history"]))
                after = replay(events, g)
                self.assertEqual(list(after.placement), row["placement"], row["name"])
                self.assertTrue(row["certified"], row["name"])
                self.assertTrue(row["replays_from_genesis"], row["name"])
                self.assertTrue(row["initial_datum_unchanged"], row["name"])
                self.assertTrue(row["reading_unchanged"], row["name"])
                checked += 1
        self.assertEqual(checked, 14)

    def test_the_requirement_at_the_current_regime_under_each_reading(self) -> None:
        self.assertFalse(self.u["base"]["satisfies"])
        self.assertTrue(self.o["base"]["satisfies"])
        self.assertEqual(self.u["base"]["automorphism_count"], 2)
        self.assertEqual(self.o["base"]["automorphism_count"], 1)
        self.assertEqual(
            self.u["base"]["mark_exchange_witness"], {"reflected": True, "permutation": [1, 0]}
        )
        self.assertIsNone(self.o["base"]["mark_exchange_witness"])
        for rd in (self.u, self.o):
            self.assertTrue(rd["requirement_matches_the_challenge_2_notion"])
            self.assertTrue(rd["requirement_readings_agree_at_every_point"])

    def test_the_counterfactual_square_turns_on_the_exchange_alone(self) -> None:
        for rd in (self.u, self.o):
            square = rd["counterfactual_square"]
            self.assertEqual(len(square), 4)
            for cell in square:
                self.assertEqual(
                    cell["requirement_met"], not cell["side_exchange_permitted"], cell
                )
            self.assertEqual(sum(1 for c in square if c["is_the_real_cell_for_this_reading"]), 1)
        real_u = next(c for c in self.u["counterfactual_square"] if c["is_the_real_cell_for_this_reading"])
        real_o = next(c for c in self.o["counterfactual_square"] if c["is_the_real_cell_for_this_reading"])
        self.assertEqual((real_u["names_admitted"], real_u["side_exchange_permitted"]), (False, True))
        self.assertEqual((real_o["names_admitted"], real_o["side_exchange_permitted"]), (True, False))

    def test_the_minima_under_U_are_three_tied_classes(self) -> None:
        by_mu1 = self.u["minima_by_mu1"]
        self.assertEqual(by_mu1["minimum"], 1)
        self.assertEqual(by_mu1["class_count"], 3)
        self.assertFalse(by_mu1["unique"])
        self.assertEqual(
            sorted(by_mu1["points"]),
            ["extra_mark_0", "extra_mark_1", "withdraw_mark_permutations", "withdraw_reflection"],
        )
        members = sorted(sorted(entry["members"]) for entry in by_mu1["classes"])
        self.assertEqual(
            members,
            [
                ["extra_mark_0", "extra_mark_1"],
                ["withdraw_mark_permutations"],
                ["withdraw_reflection"],
            ],
        )
        self.assertTrue(self.u["measures_agree_on_minima"])
        self.assertEqual(self.u["minima_by_mu2"]["minimum"], 1)
        self.assertEqual(self.u["minima_by_mu2"]["class_count"], 3)

    def test_the_minimum_under_O_is_the_null_augmentation_alone(self) -> None:
        by_mu1 = self.o["minima_by_mu1"]
        self.assertEqual(by_mu1["minimum"], 0)
        self.assertEqual(by_mu1["class_count"], 1)
        self.assertTrue(by_mu1["unique"])
        self.assertEqual(by_mu1["points"], ["base"])
        self.assertTrue(self.o["price"]["requirement_met_without_augmentation"])
        self.assertTrue(self.o["price"]["nothing_new_paid_at_challenge_3"])
        self.assertIn("side names under O", self.o["price"]["capabilities_not_used"])
        self.assertFalse(self.u["price"]["requirement_met_without_augmentation"])
        self.assertEqual(self.u["price"]["paid_by"], "the run")

    def test_the_three_mechanisms(self) -> None:
        rows = {str(row["name"]): row for row in self.u["one_step_detail"]}
        self.assertEqual(
            rows["withdraw_reflection"]["invariant_separating_mark_properties"],
            ["on_side_0", "on_side_1"],
        )
        self.assertEqual(
            rows["withdraw_mark_permutations"]["invariant_separating_mark_properties"],
            ["has_index_0", "has_index_1"],
        )
        self.assertEqual(rows["extra_mark_0"]["invariant_separating_mark_properties"], [])
        self.assertEqual(rows["extra_mark_1"]["invariant_separating_mark_properties"], [])
        # the second minimum meets the requirement by unfolding: with the mark
        # permutations withdrawn no permitted renaming moves an index at all
        self.assertTrue(rows["withdraw_mark_permutations"]["no_permitted_renaming_moves_an_index"])
        self.assertFalse(rows["withdraw_reflection"]["no_permitted_renaming_moves_an_index"])
        self.assertFalse(rows["extra_mark_0"]["no_permitted_renaming_moves_an_index"])
        # the label property is invariant everywhere and separates nothing:
        # both retained marks carry the same label, which is Challenge 2's
        # result restated at this rung
        for row in self.u["one_step_detail"]:
            self.assertIn("carries_label_a", row["invariant_mark_properties"], row["name"])
            self.assertNotIn("carries_label_a", row["separating_mark_properties"], row["name"])

    def test_the_two_failing_one_step_candidates(self) -> None:
        rows = {str(row["name"]): row for row in self.u["one_step_detail"]}
        for name in ("admit_names", "keep_labels"):
            self.assertFalse(rows[name]["satisfies"], name)
            self.assertEqual(rows[name]["automorphism_count"], 2, name)
            self.assertEqual(rows[name]["mu1"], 1, name)
        self.assertEqual(self.u["points_satisfying_with_grammar_change_only"], [])
        self.assertEqual(rows["admit_names"]["holding_judgments_with_names"], 4)
        self.assertEqual(rows["admit_names"]["mark_side_names"], ["near", "far"])
        self.assertEqual(self.u["base"]["holding_judgments_with_names"], 2)

    def test_the_two_measures_are_not_the_same_measure(self) -> None:
        self.assertTrue(self.u["measures_differ_somewhere"])
        self.assertTrue(self.o["measures_differ_somewhere"])
        differing = [row["name"] for row in self.u["points"] if row["mu1"] != row["mu2"]]
        self.assertGreater(len(differing), 0)
        self.assertIn("withdraw_reflection+extra_mark_0", differing)

    def test_the_measures_select_the_same_minima_under_U_and_not_under_O(self) -> None:
        # Review found the paper claiming the agreement under BOTH readings.
        # It holds under U alone: under O the capability count's minimum is
        # the null augmentation and nothing else, while the collateral count's
        # minimum of zero is attained by five points in three classes.
        self.assertTrue(self.u["measures_agree_on_minima"])
        self.assertFalse(self.o["measures_agree_on_minima"])
        self.assertEqual(self.o["minima_by_mu1"]["points"], ["base"])
        self.assertEqual(self.o["minima_by_mu1"]["class_count"], 1)
        self.assertTrue(self.o["minima_by_mu1"]["unique"])
        self.assertEqual(len(self.o["minima_by_mu2"]["points"]), 5)
        self.assertEqual(self.o["minima_by_mu2"]["class_count"], 3)
        self.assertFalse(self.o["minima_by_mu2"]["unique"])

    def test_the_sides_fact_agrees_with_the_requirement_at_every_point(self) -> None:
        # The second measure was declared to read what a candidate costs
        # BESIDE what it was asked for.  Review found that it does not: the
        # first declared fact is the requirement said of the two SIDES, and it
        # takes the requirement's value at all 48 points under each reading,
        # so where the base fails the requirement a satisfying candidate
        # carries that one fact in its count.
        for rd in (self.u, self.o):
            self.assertTrue(rd["sides_fact_agrees_with_the_requirement_at_every_point"])
            for row in rd["points"]:
                self.assertEqual(
                    row["collateral_facts"]["sides_internally_separable"],
                    row["satisfies"],
                    row["name"],
                )
        for name in ("withdraw_reflection", "withdraw_mark_permutations", "extra_mark_0"):
            row = next(r for r in self.u["points"] if r["name"] == name)
            self.assertEqual(row["mu2"], 1, name)
            self.assertEqual(
                sorted(k for k, v in row["collateral_facts"].items() if v),
                ["sides_internally_separable"],
                name,
            )

    def test_the_sides_fact_agreement_reads_false_when_one_point_parts(self) -> None:
        # The negative direction, so the key above is not a tautology of its
        # own construction: one row whose fact and requirement part.
        parted = copy.deepcopy(self.u["points"])
        row = parted[0]
        row["collateral_facts"]["sides_internally_separable"] = not row["satisfies"]
        self.assertFalse(sides_fact_agrees_with_the_requirement(parted))
        self.assertTrue(sides_fact_agrees_with_the_requirement(self.u["points"]))

    def test_the_bundles_are_refused_and_counted(self) -> None:
        # 48 points: the base at count zero, six one-step points, and the
        # rest bundles.
        self.assertEqual(self.u["bundles_refused_count"], 41)
        self.assertEqual(len(self.u["one_step_points"]), 6)
        for row in self.u["points"]:
            self.assertEqual(row["bundles"], row["mu1"] >= 2, row["name"])
            self.assertEqual(row["one_step"], row["mu1"] == 1, row["name"])
        self.assertTrue(self.u["one_step_iff_capability_count_one"])
        self.assertEqual(self.u["reading_O_bundle"]["mu1"], 2)
        self.assertTrue(self.u["reading_O_bundle"]["bundles"])
        self.assertTrue(self.u["reading_O_bundle"]["satisfies"])

    def test_the_probe_set_offers_every_event_kind(self) -> None:
        # Review found that the Challenge 1 probe set offered no occurrence
        # admission, so the event kind Challenge 2 declared was never offered
        # to the empty relation at all.  This set offers all three.
        kinds = {type(e).__name__ for e in probes("a")}
        self.assertEqual(kinds, {"Supply", "AdmitMark", "AdmitOccurrence"})
        self.assertIn(AdmitOccurrence("a", 1), probes("a"))
        self.assertIn(AdmitMark("a", 0), probes("a"))
        self.assertEqual(sorted(kinds), sorted(self.receipt["event_kinds"]))
        # three kinds, five probes: the relation is offered every event of
        # every declared kind, not one probe per kind
        self.assertEqual(len(probes("a")), 5)
        for row in self.u["one_step_detail"]:
            self.assertTrue(row["event_follows_relation_empty"], row["name"])

    def test_the_probe_set_check_sees_a_dropped_event_kind(self) -> None:
        # The negative direction of the check above.  The Challenge 1 shape it
        # replaced offered no occurrence admission at all, and that is exactly
        # what a totality over the declared kinds must reject.
        kinds = set(self.receipt["event_kinds"])
        dropped = [e for e in probes("a") if not isinstance(e, AdmitOccurrence)]
        self.assertEqual({type(e).__name__ for e in dropped}, {"Supply", "AdmitMark"})
        self.assertNotEqual({type(e).__name__ for e in dropped}, kinds)

    def test_the_placement_is_checked_against_the_declared_convention(self) -> None:
        # The one statement about a candidate regime that is not a comparison
        # of a replay with itself.
        wholes = [read_whole(text) for text in ("<a|>", "<|a>")]
        self.assertEqual(expected_placement(wholes, NULL_AUGMENTATION), [0, 1])
        self.assertEqual(expected_placement(wholes, Augmentation(extra_mark=1)), [0, 1, 1])
        for rd in (self.u, self.o):
            for row in [rd["base"], *rd["one_step_detail"]]:
                self.assertTrue(row["placement_matches_the_declared_convention"], row["name"])

    def test_the_placement_key_reads_false_when_the_prediction_parts(self) -> None:
        # The negative direction: every committed row reads True, so the key
        # is worth nothing until it is shown able to read False.  With the
        # predicted placement moved off the convention's, the same row does,
        # and the row's own placement is unmoved.
        wholes = [read_whole(text) for text in ("<a|>", "<|a>")]
        domain = property_domain(READING_U, PROPERTY_DOMAIN_MAX_MARKS)
        cache = {(True, True): domain_images(domain, True, True)}
        base = collateral_facts(READING_U, NULL_AUGMENTATION, wholes)
        row = one_step_detail(READING_U, NULL_AUGMENTATION, wholes, cache, base)
        self.assertTrue(row["placement_matches_the_declared_convention"])
        with patch("boundary.challenge3.expected_placement", return_value=[1, 0]):
            moved = one_step_detail(READING_U, NULL_AUGMENTATION, wholes, cache, base)
        self.assertFalse(moved["placement_matches_the_declared_convention"])
        self.assertEqual(moved["placement"], [0, 1])

    def test_the_price_is_read_off_the_enumeration(self) -> None:
        # The Challenge 2 field of this shape was a literal that no run could
        # move; this one is the minimum and the retained minima's capability
        # coordinates, so a rung that genuinely paid nothing would flip it.
        self.assertEqual(
            self.u["price"]["new_at_challenge_3"],
            ["extra_mark", "withdraw_mark_permutations", "withdraw_reflection"],
        )
        self.assertFalse(self.u["price"]["nothing_new_paid_at_challenge_3"])
        self.assertEqual(self.o["price"]["new_at_challenge_3"], [])
        self.assertTrue(self.o["price"]["nothing_new_paid_at_challenge_3"])
        free = price_facts(
            READING_U,
            False,
            {"minimum": 0, "classes": [{"class_key": [], "members": ["base"]}]},
            [{"name": "base", "capability_coordinates": []}],
        )
        self.assertTrue(free["nothing_new_paid_at_challenge_3"])
        self.assertEqual(free["new_at_challenge_3"], [])

    def test_the_process_admission_facts(self) -> None:
        proc = self.u["process_admission"]
        self.assertTrue(proc["token_already_supplied"])
        self.assertTrue(proc["accepted_without_a_new_supply"])
        self.assertTrue(proc["fresh_token_refused"])
        self.assertIn("was not supplied before admission", str(proc["fresh_token_refusal"]))


class EnumerationCrossChecks(unittest.TestCase):
    def test_the_flagged_automorphisms_match_an_unpruned_re_derivation(self) -> None:
        # The declared automorphism list against a re-derivation that builds
        # the images itself, with no shared helper.
        for rd in (READING_U, READING_O):
            for placement in ((0, 1), (0, 0), (0, 1, 0)):
                for reflection, perms, keep in product((False, True), repeat=3):
                    r = Regime(rd, tuple("a" for _ in placement), placement)
                    n = len(placement)
                    pis = list(permutations(range(n))) if perms else [tuple(range(n))]
                    bases = [(False, placement)] + (
                        [(True, tuple(1 - s for s in placement))] if reflection else []
                    )
                    unpruned = []
                    for reflected, base in bases:
                        for pi in pis:
                            image = [0] * n
                            for k in range(n):
                                image[pi[k]] = base[k]
                            if tuple(image) == placement:
                                unpruned.append((reflected, pi))
                    self.assertEqual(
                        automorphisms_under(r, reflection, perms, keep),
                        unpruned,
                        (r, reflection, perms, keep),
                    )

    def test_the_property_domain_and_its_images(self) -> None:
        domain = property_domain(READING_U, PROPERTY_DOMAIN_MAX_MARKS)
        self.assertEqual(len(domain), 85)
        self.assertEqual(len(property_domain(READING_O, 0)), 1)
        images = domain_images(domain, True, True)
        self.assertEqual(len(images), 85)
        self.assertEqual(
            sum(len(entries) for _r, entries in images),
            sum(len(permitted_images_under(r, True, True)) for r in domain),
        )

    def test_property_invariance_is_a_census_and_reports_a_false(self) -> None:
        u_images = domain_images(property_domain(READING_U, 2), True, True)
        o_images = domain_images(property_domain(READING_O, 2), False, True)
        self.assertFalse(property_invariant(on_side_0, u_images))
        self.assertTrue(property_invariant(on_side_0, o_images))
        # a vacuous domain reports invariance for anything, which is why the
        # declared domain carries marks
        self.assertTrue(
            property_invariant(on_side_0, domain_images(property_domain(READING_U, 0), True, True))
        )

    def test_property_separation_reads_the_two_retained_marks(self) -> None:
        self.assertTrue(property_separates(on_side_0, Regime(READING_U, ("a", "a"), (0, 1))))
        self.assertFalse(property_separates(on_side_0, Regime(READING_U, ("a", "a"), (0, 0))))
        self.assertEqual(len(DECLARED_MARK_PROPERTIES), 5)

    def test_the_orbit_witness_agrees_with_the_requirement_at_every_point(self) -> None:
        wholes = [read_whole(text) for text in ("<a|>", "<|a>")]
        checked = 0
        for reading in (READING_U, READING_O):
            for aug in candidate_space():
                main, _o, _l, _c = comparison_regimes(reading, wholes, aug)
                self.assertEqual(
                    requirement_met(main, reading, aug),
                    orbit_property_separates(main, reading, aug),
                    (reading, point_name(aug)),
                )
                checked += 1
        self.assertEqual(checked, 96)

    def test_the_class_key_is_the_structure_with_the_canonical_regime(self) -> None:
        wholes = [read_whole(text) for text in ("<a|>", "<|a>")]
        first, *_ = comparison_regimes(READING_U, wholes, Augmentation(extra_mark=0))
        second, *_ = comparison_regimes(READING_U, wholes, Augmentation(extra_mark=1))
        self.assertNotEqual(list(first.placement), list(second.placement))
        self.assertEqual(
            class_key(READING_U, Augmentation(extra_mark=0), first),
            class_key(READING_U, Augmentation(extra_mark=1), second),
        )
        third, *_ = comparison_regimes(READING_U, wholes, Augmentation(withdraw_reflection=True))
        self.assertNotEqual(
            class_key(READING_U, Augmentation(withdraw_reflection=True), third),
            class_key(READING_U, NULL_AUGMENTATION, third),
        )

    def test_minima_over_no_satisfying_candidate(self) -> None:
        empty = minima([{"satisfies": False, "mu1": 0, "name": "x", "class_key": []}], "mu1")
        self.assertIsNone(empty["minimum"])
        self.assertEqual(empty["classes"], [])
        self.assertFalse(empty["unique"])

    def test_the_collateral_measure_counts_only_what_the_base_lacked(self) -> None:
        wholes = [read_whole(text) for text in ("<a|>", "<|a>")]
        base = collateral_facts(READING_U, NULL_AUGMENTATION, wholes)
        self.assertEqual([k for k, v in base.items() if v], [])
        o_base = collateral_facts(READING_O, NULL_AUGMENTATION, wholes)
        self.assertEqual(
            sorted(k for k, v in o_base.items() if v),
            ["side_names_hold", "sides_internally_separable"],
        )
        # under O those two are already available, so they are not collateral
        self.assertEqual(mu2(o_base, o_base), 0)
        self.assertEqual(mu2(base, base), 0)
        labelled = collateral_facts(READING_U, Augmentation(keep_labels=True), wholes)
        self.assertTrue(labelled["label_internally_available"])
        self.assertEqual(mu2(labelled, base), 1)

    def test_the_flags_and_the_key_follow_the_reading(self) -> None:
        self.assertEqual(flags(READING_U, NULL_AUGMENTATION), (True, True, False))
        self.assertEqual(flags(READING_O, NULL_AUGMENTATION), (False, True, False))
        self.assertEqual(
            flags(READING_U, Augmentation(withdraw_reflection=True, keep_labels=True)),
            (False, True, True),
        )
        r = Regime(READING_U, ("a", "b"), (0, 1))
        self.assertEqual(key_of(r, False), serialize(r))
        self.assertEqual(key_of(r, True), (READING_U, ("a", "b"), (0, 1)))


class ScorerNegativeDirection(unittest.TestCase):
    def setUp(self) -> None:
        self.u = reading_facts(READING_U)
        self.o = reading_facts(READING_O)
        self.kinds = ["OnSide", "SideNamed"]

    def run_score(
        self, u: Json | None = None, o: Json | None = None, kinds: list[str] | None = None
    ) -> Json:
        return score(
            self.u if u is None else u,
            self.o if o is None else o,
            self.kinds if kinds is None else kinds,
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
        for cid in SCORED_PREDICTIONS:
            self.assertEqual(scores[cid]["status"], "HIT", cid)
        self.assertEqual(scores["C2-X"]["status"], "PARTIAL")

    def test_c3_1_misses_when_the_two_readings_part(self) -> None:
        u = self.mutated(self.u, ["requirement_readings_agree_at_every_point"], False)
        self.assertEqual(self.run_score(u=u)["C3-1"]["status"], "MISSED")
        o = self.mutated(self.o, ["requirement_matches_the_challenge_2_notion"], False)
        self.assertEqual(self.run_score(o=o)["C3-1"]["status"], "MISSED")
        # and when every satisfying candidate has a declared witness, so the
        # orbit property is never needed
        u2 = copy.deepcopy(self.u)
        for row in u2["one_step_detail"]:
            row["invariant_separating_mark_properties"] = ["on_side_0"]
        self.assertEqual(self.run_score(u=u2)["C3-1"]["status"], "MISSED")

    def test_c3_2_misses_when_a_cell_of_the_square_turns(self) -> None:
        u = copy.deepcopy(self.u)
        u["counterfactual_square"][0]["requirement_met"] = False
        self.assertEqual(self.run_score(u=u)["C3-2"]["status"], "MISSED")
        o = self.mutated(self.o, ["base", "satisfies"], False)
        self.assertEqual(self.run_score(o=o)["C3-2"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["base", "satisfies"], True)
        self.assertEqual(self.run_score(u=u2)["C3-2"]["status"], "MISSED")
        o2 = self.mutated(self.o, ["price", "nothing_new_paid_at_challenge_3"], False)
        self.assertEqual(self.run_score(o=o2)["C3-2"]["status"], "MISSED")
        o3 = self.mutated(
            self.o,
            ["price", "capabilities_the_satisfaction_uses"],
            ["admitted boundary", "side names under O", "occurrence identity"],
        )
        self.assertEqual(self.run_score(o=o3)["C3-2"]["status"], "MISSED")

    def test_c3_3_misses_when_a_grammar_change_alone_would_satisfy(self) -> None:
        u = copy.deepcopy(self.u)
        for row in u["one_step_detail"]:
            if row["name"] == "admit_names":
                row["satisfies"] = True
        self.assertEqual(self.run_score(u=u)["C3-3"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["points_satisfying_with_grammar_change_only"], ["admit_names"])
        self.assertEqual(self.run_score(u=u2)["C3-3"]["status"], "MISSED")
        u3 = self.mutated(
            self.u, ["base", "invariant_mark_properties"], ["on_side_0", "carries_label_a"]
        )
        self.assertEqual(self.run_score(u=u3)["C3-3"]["status"], "MISSED")
        self.assertEqual(self.run_score(kinds=self.kinds + ["Empty"])["C3-3"]["status"], "MISSED")

    def test_c3_4_misses_on_a_different_space_or_a_free_bundle(self) -> None:
        u = self.mutated(self.u, ["space_size"], 47)
        self.assertEqual(self.run_score(u=u)["C3-4"]["status"], "MISSED")
        o = self.mutated(self.o, ["reading_O_bundle", "mu1"], 1)
        self.assertEqual(self.run_score(o=o)["C3-4"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["one_step_iff_capability_count_one"], False)
        self.assertEqual(self.run_score(u=u2)["C3-4"]["status"], "MISSED")
        u3 = copy.deepcopy(self.u)
        u3["points"][0]["bundles"] = True
        self.assertEqual(self.run_score(u=u3)["C3-4"]["status"], "MISSED")

    def test_c3_5_misses_when_a_minimum_is_lost_or_uniqueness_appears(self) -> None:
        u = self.mutated(
            self.u,
            ["satisfying_one_step_points"],
            ["withdraw_reflection", "extra_mark_0", "extra_mark_1"],
        )
        self.assertEqual(self.run_score(u=u)["C3-5"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["minima_by_mu1", "class_count"], 1)
        self.assertEqual(self.run_score(u=u2)["C3-5"]["status"], "MISSED")
        u3 = self.mutated(self.u, ["minima_by_mu1", "unique"], True)
        self.assertEqual(self.run_score(u=u3)["C3-5"]["status"], "MISSED")
        u4 = self.mutated(self.u, ["minima_by_mu1", "minimum"], 2)
        self.assertEqual(self.run_score(u=u4)["C3-5"]["status"], "MISSED")

    def test_c3_6_misses_when_the_measures_part_or_coincide(self) -> None:
        u = self.mutated(self.u, ["measures_agree_on_minima"], False)
        self.assertEqual(self.run_score(u=u)["C3-6"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["measures_differ_somewhere"], False)
        self.assertEqual(self.run_score(u=u2)["C3-6"]["status"], "MISSED")
        u3 = copy.deepcopy(self.u)
        for row in u3["points"]:
            if row["name"] == "withdraw_reflection":
                row["mu2"] = 2
        self.assertEqual(self.run_score(u=u3)["C3-6"]["status"], "MISSED")

    def test_c3_7_misses_when_a_mechanism_row_moves(self) -> None:
        u = copy.deepcopy(self.u)
        for row in u["one_step_detail"]:
            if row["name"] == "withdraw_mark_permutations":
                row["invariant_separating_mark_properties"] = ["on_side_0", "on_side_1"]
        self.assertEqual(self.run_score(u=u)["C3-7"]["status"], "MISSED")
        u2 = copy.deepcopy(self.u)
        for row in u2["one_step_detail"]:
            if row["name"] == "extra_mark_0":
                row["invariant_separating_mark_properties"] = ["on_side_0"]
        self.assertEqual(self.run_score(u=u2)["C3-7"]["status"], "MISSED")
        u3 = copy.deepcopy(self.u)
        for row in u3["one_step_detail"]:
            if row["name"] == "withdraw_reflection":
                row["no_permitted_renaming_moves_an_index"] = True
        self.assertEqual(self.run_score(u=u3)["C3-7"]["status"], "MISSED")

    def test_c3_8_misses_when_a_reading_stops_changing_the_price(self) -> None:
        o = self.mutated(self.o, ["minima_by_mu1", "minimum"], 1)
        self.assertEqual(self.run_score(o=o)["C3-8"]["status"], "MISSED")
        o2 = self.mutated(self.o, ["minima_by_mu1", "class_count"], 3)
        self.assertEqual(self.run_score(o=o2)["C3-8"]["status"], "MISSED")
        u = self.mutated(self.u, ["price", "paid_by"], "the boundary")
        self.assertEqual(self.run_score(u=u)["C3-8"]["status"], "MISSED")

    def test_c2x_clauses_move_on_their_own_facts(self) -> None:
        # had the enumeration produced only the two minima the frozen clause
        # names, that clause would have hit and C2-X with it
        u = copy.deepcopy(self.u)
        u["minima_by_mu1"]["classes"] = [
            entry
            for entry in u["minima_by_mu1"]["classes"]
            if "withdraw_mark_permutations" not in entry["members"]
            and "withdraw_reflection" not in entry["members"]
        ]
        c2x = self.run_score(u=u)["C2-X"]
        self.assertEqual(c2x["every_minimum_names_a_side_or_admits_a_datum_clause_status"], "HIT")
        self.assertEqual(c2x["status"], "HIT")
        # dropping only the index candidate leaves the literal clause missed
        # and the weaker reading hitting
        u2 = copy.deepcopy(self.u)
        u2["minima_by_mu1"]["classes"] = [
            entry
            for entry in u2["minima_by_mu1"]["classes"]
            if "withdraw_mark_permutations" not in entry["members"]
        ]
        c2x = self.run_score(u=u2)["C2-X"]
        self.assertEqual(c2x["every_minimum_names_a_side_or_admits_a_datum_clause_status"], "MISSED")
        self.assertEqual(c2x["same_clause_on_the_weaker_reading_status"], "HIT")
        self.assertEqual(c2x["status"], "PARTIAL")
        # and a core clause failing takes the whole extrapolation to MISSED
        o = self.mutated(self.o, ["base", "satisfies"], False)
        self.assertEqual(self.run_score(o=o)["C2-X"]["status"], "MISSED")

    def test_tally_refuses_an_unknown_status_and_moves_a_miss(self) -> None:
        scores = self.run_score()
        missed_definition = self.mutated(scores, ["C3-1", "status"], "MISSED")
        counted = tally(missed_definition)
        self.assertEqual(counted["hit_definition_level"], ["C3-4"])
        self.assertEqual(counted["missed"], ["C3-1"])
        partial_content = self.mutated(scores, ["C3-5", "status"], "PARTIAL")
        counted = tally(partial_content)
        self.assertEqual(counted["partial"], ["C3-5"])
        self.assertNotIn("C3-5", counted["hit_as_content"])
        with self.assertRaisesRegex(ValueError, "unexpected status 'PENDING' for C3-2"):
            tally(self.mutated(scores, ["C3-2", "status"], "PENDING"))
        self.assertNotIn("C2-X", counted["scored"])
        self.assertNotIn("C3-X", counted["scored"])

    def test_the_module_declares_no_authority(self) -> None:
        self.assertEqual(build()["authority_effect"], "None")


if __name__ == "__main__":
    unittest.main()
