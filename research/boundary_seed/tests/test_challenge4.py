"""Tests of the Challenge 4 receipt: determinism, the frozen pins, replay from
genesis for every candidate history, the widened reader and what the narrower
one refuses, the declared candidate space, the whole sense of separability
against the pointwise one, the whole-property census and the key-determination
clause that repairs it, the two cost measures, the minima and their quotient,
the scores of the frozen predictions and of C3-X, the negative direction of the
scorer, and the unpruned cross-checks of every bounded enumeration."""

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

from boundary import challenge4  # noqa: E402
from boundary.challenge4 import (  # noqa: E402
    C0_PREDICTIONS_SHA256,
    C1_PREDICTIONS_SHA256,
    C2_PREDICTIONS_SHA256,
    C3_PREDICTIONS_SHA256,
    CALLER_TOKENS,
    COLLATERAL_FACTS,
    COORDINATES,
    DECLARED_WHOLE_PROPERTIES,
    DEFINITION_LEVEL_PREDICTIONS,
    DOMAIN_GROUPINGS,
    EXTRA_MARK_VALUES,
    FRESH_TOKEN,
    GROUPING_BUNDLE,
    NULL_AUGMENTATION,
    PREDICTIONS_SHA256,
    PRICE_FIELDS_DECLARED,
    READING_O_BUNDLE,
    RETAINED_WHOLES,
    SCORED_PREDICTIONS,
    SEED_SHA256,
    SIDE_PROPERTIES,
    Augmentation,
    analyse,
    build,
    caller_wholes,
    candidate_history,
    candidate_space,
    capabilities,
    changed_coordinates,
    class_key,
    collateral_facts,
    comparison_configurations,
    configuration_of,
    domain_images,
    effective_structure,
    expected_placement,
    fact_agrees_with_the_requirement,
    grouping_square,
    holding,
    is_one_step,
    mark_pairs,
    marks_pairwise_separable,
    matching_broken,
    mu1,
    mu2,
    named,
    one_step_detail,
    orbit_witness_separates,
    point_name,
    point_row,
    price_facts,
    process_admission,
    property_domain,
    property_invariant,
    property_key_determined,
    property_separates,
    reader_facts,
    reading_facts,
    reduction_to_challenge_3,
    renamings,
    requirement_met,
    retention_groups,
    retention_history,
    score,
    separable_mark_pairs,
    set_is_the_first_whole,
    tally,
    two_element_sets,
    witness_json,
)
from boundary.model import (  # noqa: E402
    READING_O,
    READING_U,
    AdmissionError,
    AdmitOccurrence,
    Configuration,
    Event,
    Regime,
    Renamings,
    Supply,
    configuration_automorphisms,
    configuration_key,
    configurations_isomorphic,
    genesis,
    group_carrying_automorphism,
    mark_carrying_automorphism,
    permitted_configuration_images,
    relabel_groups,
    rename_groups,
    replay,
    tag_maps,
    whole_orbit,
    wholes_separable_in,
)
from boundary.presentation import (  # noqa: E402
    DECLARED_CONVENTION,
    DECLARED_WITHIN_WHOLE_ORDER,
    OTHER_WITHIN_WHOLE_ORDER,
    PairWhole,
    PresentationError,
    pair_marks,
    read_pair_whole,
)
from run_challenge4 import render  # noqa: E402

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
        self.assertEqual(sha(TREE / "challenge4" / "PREDICTIONS.md"), PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge3" / "PREDICTIONS.md"), C3_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge2" / "PREDICTIONS.md"), C2_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge1" / "PREDICTIONS.md"), C1_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge0" / "PREDICTIONS.md"), C0_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "SEED.md"), SEED_SHA256)

    def test_predictions_file_has_lf_endings(self) -> None:
        self.assertNotIn(b"\r", (TREE / "challenge4" / "PREDICTIONS.md").read_bytes())


class ReceiptTests(unittest.TestCase):
    def test_build_is_deterministic(self) -> None:
        self.assertEqual(build(), build())

    def test_committed_receipt_matches_the_renderer(self) -> None:
        path = TREE / "receipts" / "challenge4.json"
        self.assertTrue(path.exists(), "run run_challenge4.py first")
        self.assertEqual(path.read_bytes(), render())
        self.assertNotIn(b"\r", path.read_bytes())

    def test_receipt_is_inside_the_declared_split_threshold(self) -> None:
        # Over a megabyte the rung would owe a summary and a gzip with a
        # content hash.  The 192 points twice over are the evidence, so the
        # point rows carry the facts that HOLD and the full map is on the
        # one-step rows; that is what keeps it inside.
        self.assertLess(len(render()), 1_000_000)

    def test_receipt_carries_no_timestamp_or_environment(self) -> None:
        receipt = build()
        self.assertEqual(environment_hits(receipt), [])
        self.assertIn("orbit", json.dumps(receipt, sort_keys=True).lower())


class ReaderTests(unittest.TestCase):
    def test_the_challenge_1_reader_refuses_both_inscriptions(self) -> None:
        facts = reader_facts()
        self.assertTrue(facts["challenge_1_reader_refuses_both"])
        for row in facts["challenge_1_reader"]:
            self.assertIn("beyond the Challenge 1 bound", str(row["refusal"]))

    def test_the_widened_reader_reads_a_mark_on_each_side(self) -> None:
        self.assertEqual(read_pair_whole("<a|b>"), PairWhole("a", "b"))
        self.assertEqual(read_pair_whole("<a|>"), PairWhole("a", None))
        self.assertEqual(read_pair_whole("<|b>"), PairWhole(None, "b"))
        self.assertEqual(read_pair_whole("<|>"), PairWhole(None, None))

    def test_the_widened_reader_refuses_what_is_beyond_its_bound(self) -> None:
        with self.assertRaisesRegex(PresentationError, "one mark on each side"):
            read_pair_whole("<<a|>|>")
        with self.assertRaisesRegex(PresentationError, "beyond the Challenge 4 bound"):
            read_pair_whole("<ab|c>")
        self.assertIn("one mark on each side", str(reader_facts()["nested_whole_refusal"]))

    def test_the_within_whole_order_is_a_declaration_with_another_value(self) -> None:
        whole = read_pair_whole("<a|b>")
        self.assertEqual(
            pair_marks(whole, DECLARED_CONVENTION, DECLARED_WITHIN_WHOLE_ORDER),
            [("a", 0), ("b", 1)],
        )
        self.assertEqual(
            pair_marks(whole, DECLARED_CONVENTION, OTHER_WITHIN_WHOLE_ORDER),
            [("b", 1), ("a", 0)],
        )
        with self.assertRaisesRegex(PresentationError, "unknown within-whole order"):
            pair_marks(whole, DECLARED_CONVENTION, "middle first")

    def test_a_one_sided_whole_contributes_one_mark(self) -> None:
        # The Challenge 1 and Challenge 2 shapes still read: a whole with one
        # side empty admits one mark, and the grouping counts one tag for it.
        wholes = [read_pair_whole("<a|>"), read_pair_whole("<|b>")]
        history = retention_history(wholes)
        self.assertEqual([type(e).__name__ for e in history], ["Supply", "AdmitOccurrence"] * 2)
        self.assertEqual(retention_groups(wholes), (0, 1))
        self.assertEqual(pair_marks(wholes[0], DECLARED_CONVENTION, DECLARED_WITHIN_WHOLE_ORDER), [("a", 0)])


class SpaceTests(unittest.TestCase):
    def test_the_space_is_the_product_of_its_declared_coordinates(self) -> None:
        space = candidate_space()
        self.assertEqual(len(space), 192)
        self.assertEqual(len(set(space)), 192)
        self.assertEqual(len(space), 2 * 2 * 2 * 2 * 2 * 2 * len(EXTRA_MARK_VALUES))
        self.assertEqual(space[0], NULL_AUGMENTATION)
        self.assertEqual([point_name(a) for a in space].count("base"), 1)
        self.assertEqual(len(COORDINATES), 7)

    def test_side_zero_is_a_moved_coordinate(self) -> None:
        # Inherited from Challenge 3, where it was a live defect: `extra_mark
        # = 0` is a move off the inherited `None`, and a truth test would drop
        # it, `0` and falsehood being equal in this language.
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

    def test_the_grouping_bundle_costs_two_and_neither_half_is_one(self) -> None:
        self.assertEqual(mu1(GROUPING_BUNDLE), 2)
        self.assertFalse(is_one_step(GROUPING_BUNDLE))
        self.assertEqual(point_name(GROUPING_BUNDLE), "admit_grouping+name_wholes")
        self.assertEqual(mu1(Augmentation(admit_grouping=True)), 1)
        self.assertEqual(mu1(Augmentation(name_wholes=True)), 1)
        self.assertEqual(mu1(READING_O_BUNDLE), 2)

    def test_the_effective_structure_collapses_the_no_ops(self) -> None:
        # Naming wholes that no mark carries changes nothing under BOTH
        # readings; under O, withdrawing an absent side exchange and admitting
        # admitted names change nothing either.
        self.assertEqual(
            effective_structure(READING_U, Augmentation(name_wholes=True)),
            effective_structure(READING_U, NULL_AUGMENTATION),
        )
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
        self.assertNotEqual(
            effective_structure(READING_U, Augmentation(admit_grouping=True)),
            effective_structure(READING_U, NULL_AUGMENTATION),
        )

    def test_the_retention_history_and_its_grouping(self) -> None:
        wholes = caller_wholes()
        history = retention_history(wholes)
        self.assertEqual(
            [type(e).__name__ for e in history],
            ["Supply", "Supply", "AdmitOccurrence", "AdmitOccurrence"] * 2,
        )
        self.assertEqual(len(history), 8)
        self.assertEqual(retention_groups(wholes), (0, 0, 1, 1))
        self.assertEqual(retention_groups(wholes, Augmentation(extra_mark=1)), (0, 0, 1, 1, 2))
        r = replay(history, genesis(READING_U))
        self.assertEqual(list(r.placement), [0, 1, 0, 1])
        self.assertEqual(list(r.marks), ["a", "b", "b", "a"])

    def test_the_process_admission_needs_no_new_supply(self) -> None:
        wholes = caller_wholes()
        aug = Augmentation(extra_mark=1)
        self.assertEqual(process_admission(NULL_AUGMENTATION), [])
        self.assertEqual(process_admission(aug), [AdmitOccurrence("a", 1)])
        history = candidate_history(wholes, aug)
        self.assertEqual(len(history), 9)
        self.assertEqual(list(replay(history, genesis(READING_U)).placement), [0, 1, 0, 1, 1])


class FactTests(unittest.TestCase):
    receipt: Json
    u: Json
    o: Json

    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt = build()
        cls.u = cls.receipt["readings"]["U"]
        cls.o = cls.receipt["readings"]["O"]

    def test_receipt_shape(self) -> None:
        receipt = self.receipt
        self.assertEqual(receipt["challenge"], 4)
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertEqual(receipt["new_event_kinds_at_challenge_4"], [])
        self.assertEqual(receipt["event_kinds"], ["Supply", "AdmitMark", "AdmitOccurrence"])
        self.assertEqual(receipt["observation_vocabulary"], ["OnSide", "SideNamed"])
        self.assertEqual(receipt["state_event_generators"], [])
        self.assertEqual(receipt["candidate_space"]["coordinates"], list(COORDINATES))
        self.assertEqual(receipt["candidate_space"]["size"], 192)
        self.assertEqual(receipt["collateral_facts"], list(COLLATERAL_FACTS))
        self.assertEqual(receipt["property_domain_size"], 768)
        self.assertEqual(receipt["property_domain_groupings"], [list(g) for g in DOMAIN_GROUPINGS])
        self.assertEqual(receipt["tally"], tally(receipt["scores"]))
        self.assertEqual(
            receipt["event_returning_functions_by_module"],
            {
                "model": [],
                "presentation": ["admission_event", "supply_event"],
                "challenge3": [
                    "caller_history",
                    "candidate_history",
                    "probes",
                    "process_admission",
                ],
                # the census reads module members as they are, so what the
                # Challenge 4 module imports from elsewhere is listed here too
                "challenge4": [
                    "candidate_history",
                    "probes",
                    "process_admission",
                    "retention_history",
                ],
            },
        )

    def test_scores(self) -> None:
        scores = self.receipt["scores"]
        for cid in ("C4-1", "C4-2", "C4-4", "C4-5", "C4-6", "C4-7", "C4-8"):
            self.assertEqual(scores[cid]["status"], "HIT", cid)
        self.assertEqual(scores["C4-3"]["status"], "PARTIAL")
        self.assertEqual(scores["C4-X"]["status"], "PENDING")
        self.assertEqual(scores["C3-X"]["status"], "PARTIAL")
        for cid in DEFINITION_LEVEL_PREDICTIONS:
            self.assertTrue(scores[cid]["result_basis"].startswith("DEFINITION-level"), cid)
            self.assertIn("not counted as content", scores[cid]["result_basis"], cid)
        for cid in ("C4-2", "C4-3", "C4-5", "C4-6", "C4-7", "C4-8"):
            self.assertTrue(scores[cid]["result_basis"].startswith("content"), cid)
        for cid in ("C4-1", "C4-2", "C4-5", "C4-6", "C4-7", "C4-8"):
            self.assertEqual(scores[cid]["label"], "FORCED", cid)
        for cid in ("C4-3", "C4-4", "C4-X", "C3-X"):
            self.assertEqual(scores[cid]["label"], "NOT FORCED", cid)

    def test_the_recorded_miss_of_this_rung(self) -> None:
        # C4-3's invariance clause is false under U and true under O: the
        # side-reading properties are not invariant where the side exchange is
        # a permitted renaming.  Recorded next to its value, not repaired.
        c43 = self.receipt["scores"]["C4-3"]
        self.assertEqual(c43["status"], "PARTIAL")
        self.assertEqual(c43["side_properties_separate_neither_whole_status"], "HIT")
        self.assertEqual(c43["side_properties_invariant_under_both_readings_status"], "MISSED")
        self.assertEqual(c43["side_properties_invariant_by_reading"], {"U": False, "O": True})
        self.assertEqual(c43["cross_boundary_matching_unavailable_status"], "HIT")
        self.assertEqual(c43["label_keeping_parts_the_readings_status"], "HIT")

    def test_the_previous_extrapolation_is_scored_clause_by_clause(self) -> None:
        c3x = self.receipt["scores"]["C3-X"]
        self.assertEqual(c3x["reader_widening_clause_status"], "HIT")
        self.assertEqual(c3x["placement_clause_status"], "HIT")
        self.assertEqual(c3x["equal_counts_and_side_exchange_clause_status"], "HIT")
        self.assertEqual(c3x["U_fails_at_minimum_one_clause_status"], "HIT")
        self.assertEqual(c3x["matching_stays_unavailable_clause_status"], "HIT")
        self.assertEqual(c3x["boundary_contributes_the_side_clause_status"], "HIT")
        # the recorded miss, and its own falsifier: the O requirement needs a
        # new declaration, so the boundary's contribution is not what it was
        self.assertEqual(c3x["O_holds_with_no_new_declaration_clause_status"], "MISSED")
        self.assertEqual(
            c3x["boundary_contributes_exactly_what_it_did_clause_status"], "MISSED"
        )
        self.assertEqual(c3x["status"], "PARTIAL")

    def test_tally_counts(self) -> None:
        counted = self.receipt["tally"]
        self.assertEqual(
            counted["hit_as_content"], ["C4-2", "C4-5", "C4-6", "C4-7", "C4-8"]
        )
        self.assertEqual(counted["hit_definition_level"], ["C4-1", "C4-4"])
        self.assertEqual(counted["partial"], ["C4-3"])
        self.assertEqual(counted["missed"], [])

    def test_every_candidate_history_replays_from_genesis(self) -> None:
        checked = 0
        for name, rd in self.receipt["readings"].items():
            g = genesis(name)
            for row in [rd["base"], *rd["one_step_detail"]]:
                events = rebuild(list(row["history"]))
                after = replay(events, g)
                self.assertEqual(list(after.placement), row["placement"], row["name"])
                self.assertEqual(list(after.marks), row["labels"], row["name"])
                self.assertTrue(row["certified"], row["name"])
                self.assertTrue(row["replays_from_genesis"], row["name"])
                self.assertTrue(row["initial_datum_unchanged"], row["name"])
                self.assertTrue(row["reading_unchanged"], row["name"])
                self.assertTrue(row["event_follows_relation_empty"], row["name"])
                checked += 1
        self.assertEqual(checked, 18)

    def test_the_requirement_fails_under_both_readings(self) -> None:
        for rd in (self.u, self.o):
            base = rd["base"]
            self.assertFalse(base["satisfies"], rd["reading"])
            self.assertIsNotNone(base["whole_exchange_witness"])
            self.assertEqual(base["whole_members"], [[0, 1], [2, 3]])
            self.assertEqual(base["marks_on_each_side"], [2, 2])
            self.assertTrue(rd["requirement_readings_agree_at_every_point"])
        # the witness under O uses no side exchange, so the withdrawal reading
        # O carries does not touch it
        self.assertFalse(self.o["base"]["whole_exchange_witness"]["reflected"])
        self.assertEqual(self.o["base"]["whole_exchange_witness"]["permutation"], [2, 3, 0, 1])
        self.assertIsNone(self.o["base"]["side_exchange_witness"])
        self.assertIsNotNone(self.u["base"]["side_exchange_witness"])

    def test_the_pairs_of_marks_the_boundary_separates(self) -> None:
        self.assertEqual(self.u["base"]["separable_mark_pairs"], [])
        self.assertEqual(
            self.o["base"]["separable_mark_pairs"], [[0, 1], [0, 3], [1, 2], [2, 3]]
        )
        for i, j in self.o["base"]["separable_mark_pairs"]:
            self.assertNotEqual(
                self.o["base"]["placement"][i], self.o["base"]["placement"][j]
            )
        self.assertEqual(self.o["base"]["mark_pair_count"], 6)

    def test_the_minimum_under_U_is_one_class_and_uniqueness_is_not_refuted(self) -> None:
        by_mu1 = self.u["minima_by_mu1"]
        self.assertEqual(self.u["satisfying_one_step_points"], ["withdraw_mark_permutations"])
        self.assertEqual(by_mu1["minimum"], 1)
        self.assertEqual(by_mu1["class_count"], 1)
        self.assertTrue(by_mu1["unique"])
        self.assertEqual(by_mu1["points"], ["withdraw_mark_permutations"])
        self.assertTrue(self.u["measures_agree_on_minima"])

    def test_the_minima_under_O_are_two_tied_classes(self) -> None:
        by_mu1 = self.o["minima_by_mu1"]
        self.assertEqual(
            sorted(self.o["satisfying_one_step_points"]),
            ["keep_labels", "withdraw_mark_permutations"],
        )
        self.assertEqual(by_mu1["minimum"], 1)
        self.assertEqual(by_mu1["class_count"], 2)
        self.assertFalse(by_mu1["unique"])
        self.assertTrue(self.o["measures_agree_on_minima"])
        self.assertEqual(self.o["minima_by_mu2"]["minimum"], 3)

    def test_the_coordinates_that_were_minima_at_the_previous_rung_are_not(self) -> None:
        rows = {str(row["name"]): row for row in self.u["one_step_detail"]}
        for name in ("withdraw_reflection", "extra_mark_0", "extra_mark_1", "admit_names"):
            self.assertFalse(rows[name]["satisfies"], name)
        self.assertFalse(rows["keep_labels"]["satisfies"])
        self.assertTrue(rows["withdraw_mark_permutations"]["satisfies"])
        self.assertTrue(rows["withdraw_mark_permutations"]["no_permitted_renaming_moves_an_index"])
        self.assertFalse(rows["withdraw_reflection"]["no_permitted_renaming_moves_an_index"])

    def test_the_grouping_square_turns_on_both_coordinates(self) -> None:
        for rd in (self.u, self.o):
            square = rd["grouping_square"]
            self.assertEqual(len(square), 4)
            self.assertEqual(
                [cell["requirement_met"] for cell in square], [False, False, False, True]
            )
            self.assertEqual(
                [cell["capability_count"] for cell in square], [0, 1, 1, 2]
            )
            self.assertEqual(sum(1 for c in square if c["is_the_inherited_cell"]), 1)
            self.assertTrue(rd["name_wholes_collapses_into_the_base"])
            self.assertEqual(rd["grouping_bundle"]["mu1"], 2)
            self.assertTrue(rd["grouping_bundle"]["bundles"])
            self.assertTrue(rd["grouping_bundle"]["satisfies"])

    def test_the_witness_of_each_satisfying_one_step_point(self) -> None:
        u_rows = {str(row["name"]): row for row in self.u["one_step_detail"]}
        o_rows = {str(row["name"]): row for row in self.o["one_step_detail"]}
        self.assertEqual(
            u_rows["withdraw_mark_permutations"]["witness_whole_properties"],
            ["set_contains_mark_0"],
        )
        self.assertEqual(
            o_rows["keep_labels"]["witness_whole_properties"],
            ["set_carries_label_a_on_side_0"],
        )
        # and no witness anywhere the requirement fails
        for rows in (u_rows, o_rows):
            for name, row in rows.items():
                if not row["satisfies"]:
                    self.assertEqual(row["witness_whole_properties"], [], name)

    def test_the_tag_property_is_invariant_and_not_determined_by_the_key(self) -> None:
        # The defect this key exists to catch, found live: at the base the tag
        # property is invariant under every permitted renaming and separates
        # the two wholes, so a census of invariance alone reported it as a
        # witness at the very point where the requirement fails.  The key
        # cannot see the grouping there, and the second conjunct says so.
        for rd in (self.u, self.o):
            base = rd["base"]
            self.assertIn("set_is_the_first_whole", base["invariant_whole_properties"])
            self.assertIn("set_is_the_first_whole", base["separating_whole_properties"])
            self.assertNotIn(
                "set_is_the_first_whole", base["key_determined_whole_properties"]
            )
            self.assertEqual(base["witness_whole_properties"], [])

    def test_the_two_senses_of_separability_part(self) -> None:
        for rd in (self.u, self.o):
            self.assertTrue(rd["pointwise_implies_whole_at_every_point"])
            self.assertTrue(
                rd["at_every_parting_point_the_wholes_separate_and_the_marks_do_not"]
            )
            self.assertTrue(rd["reduction_to_challenge_3"]["senses_agree"])
            self.assertNotEqual(rd["points_where_the_two_senses_part"], [])
        self.assertIn("admit_grouping+name_wholes", self.u["points_where_the_two_senses_part"])
        self.assertEqual(self.u["reduction_to_challenge_3"]["whole_sense"], False)
        self.assertEqual(self.o["reduction_to_challenge_3"]["whole_sense"], True)

    def test_neither_near_fact_re_counts_the_requirement(self) -> None:
        # Challenge 3 found its first collateral fact taking the requirement's
        # value at every point, so its second measure re-counted what it was
        # asked for.  Here neither of the two facts near the requirement does.
        for rd in (self.u, self.o):
            self.assertFalse(rd["sides_fact_agrees_with_the_requirement_at_every_point"])
            self.assertFalse(rd["pairwise_fact_agrees_with_the_requirement_at_every_point"])
        self.assertTrue(self.u["measures_differ_somewhere"])
        self.assertTrue(self.o["measures_differ_somewhere"])

    def test_the_fact_agreement_check_reads_both_ways(self) -> None:
        # The negative direction of the key above: a row set in which the fact
        # does track the requirement reads true.
        rows = copy.deepcopy(self.u["points"])
        for row in rows:
            row["collateral_facts_holding"] = (
                ["sides_internally_separable"] if row["satisfies"] else []
            )
        self.assertTrue(
            fact_agrees_with_the_requirement(rows, "sides_internally_separable")
        )
        self.assertFalse(
            fact_agrees_with_the_requirement(
                self.u["points"], "sides_internally_separable"
            )
        )

    def test_the_bundles_are_refused_and_counted(self) -> None:
        # 192 points: the base at count zero, eight one-step points, and the
        # rest bundles.
        for rd in (self.u, self.o):
            self.assertEqual(rd["bundles_refused_count"], 183)
            self.assertEqual(len(rd["one_step_points"]), 8)
            self.assertTrue(rd["one_step_iff_capability_count_one"])
            for row in rd["points"]:
                self.assertEqual(row["bundles"], row["mu1"] >= 2, row["name"])
                self.assertEqual(row["one_step"], row["mu1"] == 1, row["name"])

    def test_the_price_is_read_off_the_enumeration(self) -> None:
        self.assertEqual(
            self.u["price"]["new_at_challenge_4"], ["withdraw_mark_permutations"]
        )
        self.assertEqual(
            sorted(self.o["price"]["new_at_challenge_4"]),
            ["keep_labels", "withdraw_mark_permutations"],
        )
        for rd in (self.u, self.o):
            self.assertFalse(rd["price"]["requirement_met_without_augmentation"])
            self.assertFalse(rd["price"]["nothing_new_paid_at_challenge_4"])
            self.assertEqual(rd["price"]["minimum_capability_count"], 1)
            self.assertEqual(rd["price"]["paid_by"], "the run")
        free = price_facts(
            READING_U,
            False,
            {"minimum": 0, "classes": [{"class_key": [], "members": ["base"]}]},
            [{"name": "base", "capability_coordinates": []}],
        )
        self.assertTrue(free["nothing_new_paid_at_challenge_4"])
        self.assertEqual(free["new_at_challenge_4"], [])

    def test_the_declared_price_fields_do_not_move_with_the_enumeration(self) -> None:
        declared = self.o["price"]["fields_declared_not_computed"]
        self.assertEqual(list(PRICE_FIELDS_DECLARED), declared)
        other = price_facts(
            READING_O,
            True,
            {"minimum": 2, "classes": [{"class_key": [], "members": ["p"]}]},
            [{"name": "p", "capability_coordinates": ["admit_grouping"]}],
        )
        for field in declared:
            self.assertEqual(other[str(field)], self.o["price"][str(field)], field)
        for field in ("new_at_challenge_4", "minimum_capability_count"):
            self.assertNotEqual(other[field], self.o["price"][field], field)

    def test_the_placement_is_checked_against_the_declarations(self) -> None:
        wholes = caller_wholes()
        self.assertEqual(expected_placement(wholes, NULL_AUGMENTATION), [0, 1, 0, 1])
        self.assertEqual(expected_placement(wholes, Augmentation(extra_mark=1)), [0, 1, 0, 1, 1])
        for rd in (self.u, self.o):
            for row in [rd["base"], *rd["one_step_detail"]]:
                self.assertTrue(row["placement_matches_the_declarations"], row["name"])

    def test_the_placement_key_reads_false_when_the_prediction_parts(self) -> None:
        # The negative direction: every committed row reads True, so the key is
        # worth nothing until it is shown able to read False.
        wholes = caller_wholes()
        domain = property_domain(READING_U)[:8]
        rn = renamings(READING_U, NULL_AUGMENTATION)
        cache = {
            (rn.reflection, rn.mark_permutations, rn.group_permutations): domain_images(
                domain, rn
            )
        }
        analysis = analyse(READING_U, NULL_AUGMENTATION, wholes)
        row = one_step_detail(analysis, wholes, domain, cache, analysis.facts)
        self.assertTrue(row["placement_matches_the_declarations"])
        with patch("boundary.challenge4.expected_placement", return_value=[1, 0, 1, 0]):
            moved = one_step_detail(analysis, wholes, domain, cache, analysis.facts)
        self.assertFalse(moved["placement_matches_the_declarations"])
        self.assertEqual(moved["placement"], [0, 1, 0, 1])

    def test_the_process_admission_facts(self) -> None:
        proc = self.u["process_admission"]
        self.assertTrue(proc["token_already_supplied"])
        self.assertTrue(proc["accepted_without_a_new_supply"])
        self.assertTrue(proc["fresh_token_refused"])
        self.assertEqual(proc["carries_a_tag_of_its_own"], 2)
        self.assertIn("was not supplied before admission", str(proc["fresh_token_refusal"]))


class EnumerationCrossChecks(unittest.TestCase):
    def test_the_analysis_agrees_with_the_kernel_functions(self) -> None:
        # The receipt derives every fact from ONE enumeration of a candidate's
        # images; the kernel functions are the declared definitions.  This
        # checks the two agree at every one-step point, at the grouping bundle,
        # and at a sample of wider bundles, under both readings.
        wholes = caller_wholes()
        sample = [aug for aug in candidate_space() if is_one_step(aug)] + [
            NULL_AUGMENTATION,
            GROUPING_BUNDLE,
            READING_O_BUNDLE,
            Augmentation(admit_grouping=True, name_wholes=True, extra_mark=0),
            Augmentation(keep_labels=True, withdraw_reflection=True, extra_mark=1),
        ]
        checked = 0
        for reading in (READING_U, READING_O):
            for aug in sample:
                analysis = analyse(reading, aug, wholes)
                parts = comparison_configurations(reading, wholes, aug)
                rn = renamings(reading, aug)
                self.assertEqual(
                    analysis.satisfies, requirement_met(parts["main"], rn), (reading, aug)
                )
                self.assertEqual(
                    analysis.second_reading,
                    orbit_witness_separates(parts["main"], rn),
                    (reading, aug),
                )
                self.assertEqual(
                    analysis.facts, collateral_facts(reading, aug, parts), (reading, aug)
                )
                self.assertEqual(
                    analysis.automorphisms,
                    configuration_automorphisms(parts["main"], rn),
                    (reading, aug),
                )
                self.assertEqual(
                    analysis.separable_pairs,
                    separable_mark_pairs(parts["main"], rn),
                    (reading, aug),
                )
                self.assertEqual(
                    analysis.facts["marks_pairwise_separable"],
                    marks_pairwise_separable(parts["main"], rn),
                )
                checked += 1
        self.assertEqual(checked, 26)

    def test_the_configuration_images_match_an_unpruned_re_derivation(self) -> None:
        # The declared enumeration against a re-derivation that builds the
        # images itself, with no shared helper.
        for reading in (READING_U, READING_O):
            for placement in ((0, 1, 0, 1), (0, 0, 1, 1)):
                for groups in ((0, 0, 1, 1), (0, 1, 0, 1)):
                    c = Configuration(
                        Regime(reading, ("a", "b", "b", "a"), placement), groups
                    )
                    for reflection, perms, tags in product((False, True), repeat=3):
                        rn = Renamings(reflection, perms, tags, False, True)
                        n = len(placement)
                        pis = list(permutations(range(n))) if perms else [tuple(range(n))]
                        sigmas = [(0, 1), (1, 0)] if tags else [(0, 1)]
                        bases = [(False, placement)] + (
                            [(True, tuple(1 - s for s in placement))] if reflection else []
                        )
                        unpruned = []
                        for reflected, base in bases:
                            for pi in pis:
                                image = [0] * n
                                tagged = [0] * n
                                for k in range(n):
                                    image[pi[k]] = base[k]
                                for sigma in sigmas:
                                    for k in range(n):
                                        tagged[pi[k]] = sigma[groups[k]]
                                    unpruned.append(
                                        (reflected, pi, sigma, tuple(image), tuple(tagged))
                                    )
                        got = [
                            (r, p, s, im.regime.placement, im.groups)
                            for r, p, s, im in permitted_configuration_images(c, rn)
                        ]
                        self.assertEqual(got, unpruned, (reading, placement, groups, rn))

    def test_the_key_determination_census_reads_both_ways(self) -> None:
        # The repair, in both directions: the tag property is not determined by
        # a key that does not carry the grouping, and is once the grouping is
        # admitted.  A census run over a configuration's own two wholes alone
        # would report it determined either way, which is the defect.
        domain = property_domain(READING_U)
        without = renamings(READING_U, NULL_AUGMENTATION)
        with_groups = renamings(READING_U, Augmentation(admit_grouping=True))
        self.assertFalse(property_key_determined(set_is_the_first_whole, domain, without))
        self.assertTrue(
            property_key_determined(set_is_the_first_whole, domain, with_groups)
        )
        own_wholes_only = {
            configuration_key(c, without): tuple(
                set_is_the_first_whole(c, c.members(w)) for w in RETAINED_WHOLES
            )
            for c in domain
        }
        self.assertEqual(set(own_wholes_only.values()), {(True, False)})

    def test_the_property_domain_and_its_images(self) -> None:
        domain = property_domain(READING_U)
        self.assertEqual(len(domain), 768)
        self.assertEqual(len(set(domain)), 768)
        self.assertEqual(len(two_element_sets(4)), 6)
        rn = renamings(READING_U, NULL_AUGMENTATION)
        images = domain_images(domain[:5], rn)
        self.assertEqual(len(images), 5)
        for c, sets, carried in images:
            self.assertEqual(sets, (c.members(0), c.members(1)))
            self.assertEqual(len(carried), len(permitted_configuration_images(c, rn)))

    def test_property_invariance_is_a_census_and_reports_both_values(self) -> None:
        domain = property_domain(READING_O)[:64]
        o_images = domain_images(domain, renamings(READING_O, NULL_AUGMENTATION))
        u_images = domain_images(domain, renamings(READING_U, NULL_AUGMENTATION))
        side = dict(DECLARED_WHOLE_PROPERTIES)[SIDE_PROPERTIES[0]]
        index = dict(DECLARED_WHOLE_PROPERTIES)["set_contains_mark_0"]
        self.assertTrue(property_invariant(side, o_images))
        self.assertFalse(property_invariant(side, u_images))
        self.assertFalse(property_invariant(index, o_images))
        self.assertEqual(len(DECLARED_WHOLE_PROPERTIES), 5)

    def test_property_separation_reads_the_two_retained_wholes(self) -> None:
        wholes = caller_wholes()
        c = configuration_of(READING_U, wholes, NULL_AUGMENTATION)
        index = dict(DECLARED_WHOLE_PROPERTIES)["set_contains_mark_0"]
        side = dict(DECLARED_WHOLE_PROPERTIES)[SIDE_PROPERTIES[0]]
        self.assertTrue(property_separates(index, c))
        self.assertFalse(property_separates(side, c))

    def test_the_orbit_witness_agrees_with_the_requirement_at_every_point(self) -> None:
        wholes = caller_wholes()
        checked = 0
        for reading in (READING_U, READING_O):
            for aug in candidate_space():
                main = configuration_of(reading, wholes, aug)
                rn = renamings(reading, aug)
                self.assertEqual(
                    requirement_met(main, rn),
                    orbit_witness_separates(main, rn),
                    (reading, point_name(aug)),
                )
                checked += 1
        self.assertEqual(checked, 384)

    def test_the_class_key_is_the_structure_with_the_least_configuration(self) -> None:
        wholes = caller_wholes()
        first = analyse(READING_U, Augmentation(extra_mark=0), wholes)
        second = analyse(READING_U, Augmentation(extra_mark=1), wholes)
        self.assertNotEqual(
            list(first.main.regime.placement), list(second.main.regime.placement)
        )
        self.assertEqual(
            class_key(READING_U, first.aug, first.least_key),
            class_key(READING_U, second.aug, second.least_key),
        )
        third = analyse(READING_U, Augmentation(admit_grouping=True), wholes)
        self.assertNotEqual(
            class_key(READING_U, third.aug, third.least_key),
            class_key(READING_U, NULL_AUGMENTATION, third.least_key),
        )

    def test_the_collateral_measure_counts_only_what_the_base_lacked(self) -> None:
        wholes = caller_wholes()
        base = analyse(READING_U, NULL_AUGMENTATION, wholes).facts
        self.assertEqual(holding(base), [])
        o_base = analyse(READING_O, NULL_AUGMENTATION, wholes).facts
        self.assertEqual(
            holding(o_base), ["sides_internally_separable", "side_names_hold"]
        )
        self.assertEqual(mu2(o_base, o_base), 0)
        self.assertEqual(mu2(base, base), 0)
        labelled = analyse(READING_U, Augmentation(keep_labels=True), wholes).facts
        self.assertTrue(labelled["labels_internally_available"])
        self.assertTrue(labelled["cross_boundary_matching_internally_available"])
        self.assertEqual(mu2(labelled, base), 2)

    def test_the_matching_variant_replaces_one_token_and_refuses_none(self) -> None:
        wholes = caller_wholes()
        c = configuration_of(READING_U, wholes, NULL_AUGMENTATION)
        broken = matching_broken(c)
        self.assertEqual(list(broken.regime.marks), ["a", "b", "b", FRESH_TOKEN])
        # a second whole carrying no copy of the first token leaves it alone,
        # which is the branch the caller's own configuration never takes
        other = Configuration(Regime(READING_U, ("a", "b", "b", "b"), (0, 1, 0, 1)), (0, 0, 1, 1))
        self.assertEqual(list(matching_broken(other).regime.marks), ["a", "b", "b", "b"])

    def test_the_flags_a_candidate_declares(self) -> None:
        self.assertEqual(
            renamings(READING_U, NULL_AUGMENTATION),
            Renamings(True, True, False, False, False),
        )
        self.assertEqual(
            renamings(READING_O, NULL_AUGMENTATION),
            Renamings(False, True, False, False, False),
        )
        self.assertEqual(
            renamings(READING_U, GROUPING_BUNDLE),
            Renamings(True, True, False, False, True),
        )
        self.assertEqual(
            renamings(READING_U, Augmentation(admit_grouping=True)),
            Renamings(True, True, True, False, True),
        )

    def test_the_reduction_at_the_challenge_3_configuration(self) -> None:
        for reading, expected in ((READING_U, False), (READING_O, True)):
            row = reduction_to_challenge_3(reading)
            self.assertEqual(row["placement"], [0, 1])
            self.assertEqual(row["groups"], [0, 1])
            self.assertEqual(row["whole_sense"], expected)
            self.assertEqual(row["pointwise_sense"], expected)
            self.assertTrue(row["senses_agree"])

    def test_the_witness_renderer_and_the_pair_helpers(self) -> None:
        self.assertIsNone(witness_json(None))
        self.assertEqual(
            witness_json((True, (1, 0), (0, 1))),
            {"reflected": True, "permutation": [1, 0], "tag_map": [0, 1]},
        )
        wholes = caller_wholes()
        c = configuration_of(READING_O, wholes, NULL_AUGMENTATION)
        self.assertEqual(len(mark_pairs(c)), 6)
        self.assertEqual(
            [list(p) for p in separable_mark_pairs(c, renamings(READING_O, NULL_AUGMENTATION))],
            [[0, 1], [0, 3], [1, 2], [2, 3]],
        )

    def test_the_grouping_square_is_computed_and_not_declared(self) -> None:
        wholes = caller_wholes()
        square = grouping_square(READING_U, wholes)
        self.assertEqual([cell["requirement_met"] for cell in square], [False, False, False, True])
        self.assertEqual(sum(1 for cell in square if cell["is_the_inherited_cell"]), 1)

    def test_a_point_row_carries_the_facts_that_hold(self) -> None:
        wholes = caller_wholes()
        analysis = analyse(READING_O, Augmentation(keep_labels=True), wholes)
        base = analyse(READING_O, NULL_AUGMENTATION, wholes).facts
        row = point_row(analysis, base)
        self.assertEqual(row["name"], "keep_labels")
        self.assertEqual(row["collateral_facts_holding"], holding(analysis.facts))
        self.assertEqual(row["mu2"], mu2(analysis.facts, base))
        self.assertTrue(row["satisfies"])
        self.assertEqual(len(row["coordinates"]), 7)


class KernelTests(unittest.TestCase):
    def test_a_configuration_needs_one_tag_per_mark(self) -> None:
        r = Regime(READING_U, ("a", "b"), (0, 1))
        self.assertEqual(Configuration(r, (0, 1)).members(0), frozenset({0}))
        with self.assertRaisesRegex(AdmissionError, "one group tag per admitted mark"):
            Configuration(r, (0,))
        with self.assertRaisesRegex(AdmissionError, "nonnegative index"):
            Configuration(r, (0, -1))

    def test_the_tag_maps_are_declared(self) -> None:
        self.assertEqual(tag_maps(False), [(0, 1)])
        self.assertEqual(tag_maps(True), [(0, 1), (1, 0)])
        self.assertEqual(relabel_groups((0, 0, 1, 1, 2), (1, 0)), (1, 1, 0, 0, 2))
        self.assertEqual(rename_groups((0, 0, 1, 1), (3, 2, 1, 0)), (1, 1, 0, 0))
        with self.assertRaisesRegex(ValueError, "not a permutation"):
            rename_groups((0, 1), (0, 0))

    def test_the_key_carries_the_grouping_only_when_it_is_admitted(self) -> None:
        c = Configuration(Regime(READING_U, ("a", "b"), (0, 1)), (0, 1))
        plain = Renamings(True, True, False, False, False)
        grouped = Renamings(True, True, False, False, True)
        self.assertEqual(configuration_key(c, plain), (READING_U, (0, 1)))
        self.assertEqual(configuration_key(c, grouped), (READING_U, (0, 1), (0, 1)))
        labelled = Renamings(True, True, False, True, True)
        self.assertEqual(
            configuration_key(c, labelled), (READING_U, ("a", "b"), (0, 1), (0, 1))
        )

    def test_a_whole_that_groups_no_mark_is_refused(self) -> None:
        c = Configuration(Regime(READING_U, ("a", "b"), (0, 1)), (0, 0))
        rn = Renamings(True, True, False, False, False)
        with self.assertRaisesRegex(ValueError, "groups no admitted mark"):
            group_carrying_automorphism(c, 0, 1, rn)
        with self.assertRaisesRegex(ValueError, "groups no admitted mark"):
            wholes_separable_in(c, 1, 0, rn)

    def test_a_mark_outside_the_configuration_is_refused(self) -> None:
        c = Configuration(Regime(READING_U, ("a", "b"), (0, 1)), (0, 1))
        rn = Renamings(True, True, False, False, False)
        with self.assertRaisesRegex(ValueError, "is not admitted"):
            mark_carrying_automorphism(c, 0, 5, rn)

    def test_configurations_of_different_readings_are_never_isomorphic(self) -> None:
        rn = Renamings(True, True, False, False, False)
        u = Configuration(Regime(READING_U, ("a",), (0,)), (0,))
        o = Configuration(Regime(READING_O, ("a",), (0,)), (0,))
        self.assertFalse(configurations_isomorphic(u, o, rn))
        self.assertTrue(configurations_isomorphic(u, u, rn))

    def test_the_whole_orbit_carries_the_key_and_the_mark_set(self) -> None:
        c = Configuration(Regime(READING_O, ("a", "b"), (0, 1)), (0, 1))
        rn = Renamings(False, True, False, False, False)
        orbit = whole_orbit(c, 0, rn)
        self.assertEqual(len(orbit), 2)
        self.assertIn((configuration_key(c, rn), frozenset({0})), orbit)


class ScorerNegativeDirection(unittest.TestCase):
    u: Json
    o: Json
    reader: Json

    @classmethod
    def setUpClass(cls) -> None:
        cls.u = reading_facts(READING_U)
        cls.o = reading_facts(READING_O)
        cls.reader = reader_facts()

    def run_score(
        self, u: Json | None = None, o: Json | None = None, reader: Json | None = None
    ) -> Json:
        return score(
            self.u if u is None else u,
            self.o if o is None else o,
            self.reader if reader is None else reader,
            ["OnSide", "SideNamed"],
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
            self.assertIn(scores[cid]["status"], ("HIT", "PARTIAL"), cid)
        self.assertEqual(scores["C4-3"]["status"], "PARTIAL")
        self.assertEqual(scores["C3-X"]["status"], "PARTIAL")

    def test_c4_1_misses_when_the_reader_or_the_retention_moves(self) -> None:
        reader = self.mutated(self.reader, ["challenge_1_reader_refuses_both"], False)
        self.assertEqual(self.run_score(reader=reader)["C4-1"]["status"], "MISSED")
        reader2 = self.mutated(self.reader, ["paid_by"], "the boundary")
        self.assertEqual(self.run_score(reader=reader2)["C4-1"]["status"], "MISSED")
        u = self.mutated(self.u, ["base", "placement"], [0, 1, 1, 0])
        self.assertEqual(self.run_score(u=u)["C4-1"]["status"], "MISSED")
        o = self.mutated(self.o, ["base", "labels"], ["a", "b", "a", "b"])
        self.assertEqual(self.run_score(o=o)["C4-1"]["status"], "MISSED")
        u2 = copy.deepcopy(self.u)
        u2["base"]["collateral_facts"]["within_whole_order_internally_available"] = True
        self.assertEqual(self.run_score(u=u2)["C4-1"]["status"], "MISSED")

    def test_c4_2_misses_when_a_reading_meets_the_requirement(self) -> None:
        o = self.mutated(self.o, ["base", "satisfies"], True)
        self.assertEqual(self.run_score(o=o)["C4-2"]["status"], "MISSED")
        o2 = copy.deepcopy(self.o)
        o2["base"]["whole_exchange_witness"]["reflected"] = True
        self.assertEqual(self.run_score(o=o2)["C4-2"]["status"], "MISSED")
        u = self.mutated(self.u, ["base", "separable_mark_pairs"], [[0, 1]])
        self.assertEqual(self.run_score(u=u)["C4-2"]["status"], "MISSED")
        o3 = self.mutated(self.o, ["base", "separable_mark_pairs"], [[0, 2]])
        self.assertEqual(self.run_score(o=o3)["C4-2"]["status"], "MISSED")

    def test_c4_3_moves_between_partial_and_hit_on_its_own_clauses(self) -> None:
        # the invariance clause is the recorded miss; were the side properties
        # invariant under U as well, the prediction would hit outright
        u = copy.deepcopy(self.u)
        u["base"]["invariant_whole_properties"] = list(SIDE_PROPERTIES)
        self.assertEqual(self.run_score(u=u)["C4-3"]["status"], "HIT")
        u2 = copy.deepcopy(self.u)
        u2["base"]["separating_whole_properties"] = [SIDE_PROPERTIES[0]]
        self.assertEqual(self.run_score(u=u2)["C4-3"]["status"], "MISSED")
        o = copy.deepcopy(self.o)
        for row in o["one_step_detail"]:
            if row["name"] == "keep_labels":
                row["satisfies"] = False
        self.assertEqual(self.run_score(o=o)["C4-3"]["status"], "MISSED")
        u3 = copy.deepcopy(self.u)
        u3["base"]["collateral_facts"]["cross_boundary_matching_internally_available"] = True
        self.assertEqual(self.run_score(u=u3)["C4-3"]["status"], "MISSED")

    def test_c4_4_misses_on_a_different_space_or_a_live_no_op(self) -> None:
        u = self.mutated(self.u, ["space_size"], 191)
        self.assertEqual(self.run_score(u=u)["C4-4"]["status"], "MISSED")
        o = self.mutated(self.o, ["one_step_iff_capability_count_one"], False)
        self.assertEqual(self.run_score(o=o)["C4-4"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["name_wholes_collapses_into_the_base"], False)
        self.assertEqual(self.run_score(u=u2)["C4-4"]["status"], "MISSED")
        u3 = copy.deepcopy(self.u)
        u3["points"][0]["bundles"] = True
        self.assertEqual(self.run_score(u=u3)["C4-4"]["status"], "MISSED")

    def test_c4_5_misses_when_a_second_minimum_appears_under_U(self) -> None:
        u = self.mutated(
            self.u,
            ["satisfying_one_step_points"],
            ["withdraw_mark_permutations", "withdraw_reflection"],
        )
        self.assertEqual(self.run_score(u=u)["C4-5"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["minima_by_mu1", "unique"], False)
        self.assertEqual(self.run_score(u=u2)["C4-5"]["status"], "MISSED")
        u3 = self.mutated(self.u, ["minima_by_mu1", "minimum"], 2)
        self.assertEqual(self.run_score(u=u3)["C4-5"]["status"], "MISSED")
        u4 = copy.deepcopy(self.u)
        for row in u4["one_step_detail"]:
            if row["name"] == "extra_mark_0":
                row["satisfies"] = True
        self.assertEqual(self.run_score(u=u4)["C4-5"]["status"], "MISSED")

    def test_c4_6_misses_when_the_O_minima_move(self) -> None:
        o = self.mutated(self.o, ["satisfying_one_step_points"], ["withdraw_mark_permutations"])
        self.assertEqual(self.run_score(o=o)["C4-6"]["status"], "MISSED")
        o2 = self.mutated(self.o, ["minima_by_mu1", "class_count"], 1)
        self.assertEqual(self.run_score(o=o2)["C4-6"]["status"], "MISSED")
        o3 = self.mutated(self.o, ["minima_by_mu1", "unique"], True)
        self.assertEqual(self.run_score(o=o3)["C4-6"]["status"], "MISSED")

    def test_c4_7_misses_when_a_half_of_the_bundle_would_do(self) -> None:
        u = copy.deepcopy(self.u)
        for row in u["one_step_detail"]:
            if row["name"] == "admit_grouping":
                row["satisfies"] = True
        self.assertEqual(self.run_score(u=u)["C4-7"]["status"], "MISSED")
        o = self.mutated(self.o, ["grouping_bundle", "mu1"], 1)
        self.assertEqual(self.run_score(o=o)["C4-7"]["status"], "MISSED")
        u2 = copy.deepcopy(self.u)
        u2["grouping_square"][2]["requirement_met"] = True
        self.assertEqual(self.run_score(u=u2)["C4-7"]["status"], "MISSED")
        o2 = self.mutated(self.o, ["grouping_bundle", "satisfies"], False)
        self.assertEqual(self.run_score(o=o2)["C4-7"]["status"], "MISSED")

    def test_c4_8_misses_when_the_two_senses_coincide_or_invert(self) -> None:
        u = self.mutated(self.u, ["points_where_the_two_senses_part"], [])
        self.assertEqual(self.run_score(u=u)["C4-8"]["status"], "MISSED")
        o = self.mutated(self.o, ["pointwise_implies_whole_at_every_point"], False)
        self.assertEqual(self.run_score(o=o)["C4-8"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["reduction_to_challenge_3", "senses_agree"], False)
        self.assertEqual(self.run_score(u=u2)["C4-8"]["status"], "MISSED")
        u3 = self.mutated(
            self.u,
            ["at_every_parting_point_the_wholes_separate_and_the_marks_do_not"],
            False,
        )
        self.assertEqual(self.run_score(u=u3)["C4-8"]["status"], "MISSED")
        u4 = self.mutated(
            self.u, ["points_where_the_two_senses_part"], ["keep_labels+extra_mark_0"]
        )
        self.assertEqual(self.run_score(u=u4)["C4-8"]["status"], "MISSED")

    def test_c3x_clauses_move_on_their_own_facts(self) -> None:
        # had the enumeration met the requirement under O with no augmentation,
        # the frozen clause would have hit and C3-X with it
        o = copy.deepcopy(self.o)
        o["base"]["satisfies"] = True
        c3x = self.run_score(o=o)["C3-X"]
        self.assertEqual(c3x["O_holds_with_no_new_declaration_clause_status"], "HIT")
        self.assertEqual(c3x["boundary_contributes_exactly_what_it_did_clause_status"], "HIT")
        self.assertEqual(c3x["status"], "HIT")
        # a core clause failing takes the whole extrapolation to MISSED
        u = self.mutated(self.u, ["base", "placement"], [0, 0, 1, 1])
        self.assertEqual(self.run_score(u=u)["C3-X"]["status"], "MISSED")
        u2 = self.mutated(self.u, ["minima_by_mu1", "minimum"], 2)
        self.assertEqual(self.run_score(u=u2)["C3-X"]["status"], "MISSED")
        u3 = self.mutated(self.u, ["base", "marks_on_each_side"], [3, 1])
        self.assertEqual(self.run_score(u=u3)["C3-X"]["status"], "MISSED")
        u4 = self.mutated(self.u, ["base", "side_exchange_witness"], None)
        self.assertEqual(self.run_score(u=u4)["C3-X"]["status"], "MISSED")
        u5 = self.mutated(self.u, ["base", "mark_profiles"], [[], [], [], []])
        self.assertEqual(
            self.run_score(u=u5)["C3-X"]["boundary_contributes_the_side_clause_status"],
            "MISSED",
        )

    def test_tally_refuses_an_unknown_status_and_moves_a_miss(self) -> None:
        scores = self.run_score()
        missed_definition = self.mutated(scores, ["C4-1", "status"], "MISSED")
        counted = tally(missed_definition)
        self.assertEqual(counted["hit_definition_level"], ["C4-4"])
        self.assertEqual(counted["missed"], ["C4-1"])
        partial_content = self.mutated(scores, ["C4-5", "status"], "PARTIAL")
        counted = tally(partial_content)
        self.assertEqual(sorted(counted["partial"]), ["C4-3", "C4-5"])
        self.assertNotIn("C4-5", counted["hit_as_content"])
        with self.assertRaisesRegex(ValueError, "unexpected status 'PENDING' for C4-2"):
            tally(self.mutated(scores, ["C4-2", "status"], "PENDING"))
        self.assertNotIn("C3-X", counted["scored"])
        self.assertNotIn("C4-X", counted["scored"])

    def test_the_module_declares_no_authority(self) -> None:
        self.assertEqual(challenge4.CAPABILITY_OF["admit_grouping"].startswith("each"), True)
        self.assertEqual(build()["authority_effect"], "None")


if __name__ == "__main__":
    unittest.main()
