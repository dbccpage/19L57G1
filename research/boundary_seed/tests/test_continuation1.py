"""Tests of the continuation stage 1 receipt: determinism, the frozen pins, the
branch set recomputed from the closed rungs and held to their committed
receipts, the branch quotient and the part of its key that is load-bearing, the
declared generator space and its prices, what each generator emits at each
branch, the census that shows the weakest emitting generator reads nothing of
the branch, the declared and computed bounds, the correspondence between the
Lean numbers and the Python ones, the scores of this stage's frozen predictions
and of C5-X, and the negative direction of every scored clause."""

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

from boundary import challenge4, challenge5, continuation1  # noqa: E402
from boundary.continuation1 import (  # noqa: E402
    BASE_BRANCH,
    C0_PREDICTIONS_SHA256,
    C1_PREDICTIONS_SHA256,
    C2_PREDICTIONS_SHA256,
    C3_PREDICTIONS_SHA256,
    C4_PREDICTIONS_SHA256,
    C5_PREDICTIONS_SHA256,
    CAP_ADMIT,
    CAP_DEMAND,
    CAP_READ_STATE,
    CAP_SUPPLY,
    CEILING_SENSITIVITY,
    CLOSED_RUNGS,
    COORDINATES,
    DEFINITION_LEVEL_PREDICTIONS,
    IMPOSED_DEMANDS,
    INITIAL_INSCRIPTION,
    NODE_CEILING,
    PREDICTIONS_SHA256,
    PRESENTED_TEXTS,
    SCORED_PREDICTIONS,
    SEED_ROUND_BOUND,
    SEED_SHA256,
    SOURCE_ENUMERATION,
    SOURCE_NONE,
    SOURCE_STATE,
    Branch,
    Generator,
    augmentation_named,
    behaviour_digest,
    branch_candidates,
    branch_certified,
    branch_classes,
    branch_classes_without_the_policy,
    branch_configuration,
    branch_history,
    branch_key,
    branch_key_without_the_policy,
    branch_least_key,
    branch_pairs,
    branch_retention,
    branch_substitution_census,
    branching_bound,
    build,
    bundles,
    capabilities,
    changed_coordinates,
    combine,
    configuration_of_retention,
    declared_branches,
    demand_met,
    differing_branches,
    domain_member_with_marks,
    domain_texts,
    effective_structure,
    emitted,
    emitted_demand,
    emitted_inscription,
    emitted_key,
    event_returning_functions,
    events_named_facts,
    first_missing,
    generator_class_key,
    generator_name,
    generator_space,
    is_one_step,
    least_unpresented,
    live_requirement,
    marks_in,
    mu1,
    nodes,
    policy_named,
    presented_indices,
    reading_facts,
    record_facts,
    remaining_demands,
    retention_certified,
    round_bound,
    rung_classes,
    rung_minimum,
    score,
    score_c5x,
    tally,
    text_at,
    verdict,
)
from boundary.model import READING_O, READING_U, Configuration, genesis  # noqa: E402
from boundary.presentation import read_nested_whole  # noqa: E402
from run_continuation1 import render  # noqa: E402

Json = dict[str, Any]

ENVIRONMENT_SCAN = re.compile(
    r"(?<![a-z])(timestamp|time|date|python|platform|user)(?![a-z])"
)

RECEIPT = TREE / "receipts" / "continuation1.json"


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment_hits(payload: object) -> list[str]:
    return ENVIRONMENT_SCAN.findall(json.dumps(payload, sort_keys=True).lower())


def committed(name: str) -> Json:
    payload: Json = json.loads(
        (TREE / "receipts" / name).read_text(encoding="utf-8")
    )
    return payload


class PinTests(unittest.TestCase):
    def test_predictions_bytes_match_the_pin(self) -> None:
        self.assertEqual(
            sha(TREE / "continuation" / "stage1" / "PREDICTIONS.md"),
            PREDICTIONS_SHA256,
        )
        self.assertEqual(sha(TREE / "challenge5" / "PREDICTIONS.md"), C5_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge4" / "PREDICTIONS.md"), C4_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge3" / "PREDICTIONS.md"), C3_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge2" / "PREDICTIONS.md"), C2_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge1" / "PREDICTIONS.md"), C1_PREDICTIONS_SHA256)
        self.assertEqual(sha(TREE / "challenge0" / "PREDICTIONS.md"), C0_PREDICTIONS_SHA256)

    def test_seed_bytes_match_the_pin(self) -> None:
        self.assertEqual(sha(TREE / "SEED.md"), SEED_SHA256)

    def test_committed_receipt_matches_the_renderer(self) -> None:
        self.assertTrue(RECEIPT.exists(), "run run_continuation1.py first")
        self.assertEqual(RECEIPT.read_bytes(), render())
        self.assertNotIn(b"\r", RECEIPT.read_bytes())

    def test_receipt_is_inside_the_declared_split_threshold(self) -> None:
        # Over a megabyte the stage would owe a summary and a gzip with a
        # content hash.  Its spaces are eleven branches and twelve generators,
        # so every row is carried in full and the receipt stays far inside.
        self.assertLess(len(render()), 1_000_000)

    def test_receipt_carries_no_timestamp_or_environment(self) -> None:
        receipt = build()
        self.assertEqual(environment_hits(receipt), [])
        self.assertIn("branch", json.dumps(receipt, sort_keys=True).lower())

    def test_the_receipt_is_deterministic(self) -> None:
        self.assertEqual(render(), render())


class ClosedRungTests(unittest.TestCase):
    def test_the_recomputed_minima_match_the_committed_receipts(self) -> None:
        # The branch set is derived from the closed rungs' own modules and not
        # restated; this holds the recomputation to what those rungs recorded.
        for rung in CLOSED_RUNGS:
            payload = committed(f"challenge{rung}.json")
            for reading in (READING_U, READING_O):
                want = payload["readings"][reading]["minima_by_mu1"]
                self.assertEqual(
                    rung_minimum(rung, reading), want["minimum"], (rung, reading)
                )
                self.assertEqual(
                    rung_classes(rung, reading),
                    [entry["members"] for entry in want["classes"]],
                    (rung, reading),
                )

    def test_only_the_one_step_and_null_points_are_needed(self) -> None:
        # The filter is what makes the recomputation cheap; if it dropped a
        # point the minima could move, so the answer is compared with the
        # receipts above and the filter's own reach is stated here.
        self.assertEqual(rung_classes(3, READING_O), [["base"]])
        self.assertEqual(rung_minimum(3, READING_O), 0)
        self.assertEqual(rung_minimum(4, READING_U), 1)


class BranchSetTests(unittest.TestCase):
    def test_the_branch_counts(self) -> None:
        self.assertEqual(len(declared_branches(READING_U)), 6)
        self.assertEqual(len(declared_branches(READING_O)), 5)

    def test_the_branch_names(self) -> None:
        self.assertEqual(
            [b.name for b in declared_branches(READING_U)],
            ["base", "withdraw_reflection", "withdraw_mark_permutations",
             "extra_mark_0", "opaque", "discard"],
        )
        self.assertEqual(
            [b.name for b in declared_branches(READING_O)],
            ["base", "withdraw_mark_permutations", "keep_labels", "opaque", "discard"],
        )

    def test_the_quotient_identifies_one_declaration_named_at_two_rungs(self) -> None:
        classes = branch_classes(READING_U)
        self.assertIn(
            ["withdraw_mark_permutations@3", "withdraw_mark_permutations@4"], classes
        )

    def test_the_quotient_identifies_the_null_minimum_with_the_base(self) -> None:
        self.assertIn(["base", "base@3"], branch_classes(READING_O))

    def test_the_two_further_mark_points_are_one_class_at_their_rung(self) -> None:
        self.assertEqual(rung_classes(3, READING_U)[2], ["extra_mark_0", "extra_mark_1"])

    def test_every_candidate_lies_in_exactly_one_class(self) -> None:
        for reading in (READING_U, READING_O):
            candidates = branch_candidates(reading)
            members = [name for members in branch_classes(reading) for name in members]
            self.assertEqual(sorted(members), sorted(b.label() for b in candidates))

    def test_the_base_branch_adopts_nothing(self) -> None:
        self.assertTrue(BASE_BRANCH.adopts_nothing())
        self.assertEqual(BASE_BRANCH.label(), "base")
        self.assertEqual(Branch("x", 3, challenge4.Augmentation(), None).label(), "x@3")

    def test_the_policy_part_of_the_key_is_load_bearing(self) -> None:
        # The two policy branches retain the same least key, so a key read at
        # the configuration alone reports one branch where the declarations
        # give two.  This is the Challenge 5 defect one level up.
        for reading, dropped in ((READING_U, 5), (READING_O, 4)):
            branches = {b.name: b for b in declared_branches(reading)}
            self.assertEqual(
                branch_least_key(reading, branches["opaque"]),
                branch_least_key(reading, branches["discard"]),
            )
            self.assertNotEqual(
                branch_key(reading, branches["opaque"]),
                branch_key(reading, branches["discard"]),
            )
            self.assertEqual(
                branch_key_without_the_policy(reading, branches["opaque"]),
                branch_key_without_the_policy(reading, branches["discard"]),
            )
            self.assertEqual(len(branch_classes_without_the_policy(reading)), dropped)

    def test_every_branch_replays_from_genesis(self) -> None:
        for reading in (READING_U, READING_O):
            for branch in declared_branches(reading):
                self.assertTrue(branch_certified(reading, branch), branch.name)

    def test_the_policy_branches_replay_in_the_deep_grammar(self) -> None:
        for reading in (READING_U, READING_O):
            for branch in declared_branches(reading):
                grammar = branch_history(reading, branch)["grammar"]
                self.assertEqual(
                    grammar, "deep" if branch.policy is not None else "inherited"
                )

    def test_a_branch_with_no_policy_has_no_retention(self) -> None:
        with self.assertRaises(ValueError):
            branch_retention(READING_U, BASE_BRANCH)

    def test_a_refusing_retention_gives_the_genesis_configuration(self) -> None:
        # The direction the declared branch set never takes: a policy that
        # admits nothing.  Separated so both directions are exercised.
        refusal = challenge5.retain(
            READING_U,
            read_nested_whole(challenge5.INSCRIPTION),
            challenge5.POLICY_REFUSE,
            challenge5.INSCRIPTION,
        )
        configuration = configuration_of_retention(READING_U, refusal)
        self.assertEqual(configuration, Configuration(genesis(READING_U), ()))
        self.assertFalse(retention_certified(READING_U, refusal))

    def test_an_unknown_point_name_is_refused_by_name(self) -> None:
        with self.assertRaises(KeyError):
            augmentation_named(3, "zzz_probe_absent")
        with self.assertRaises(KeyError):
            augmentation_named(4, "zzz_probe_absent")
        with self.assertRaises(KeyError):
            policy_named("zzz_probe_absent")

    def test_a_challenge_3_point_carries_across_by_its_shared_coordinates(self) -> None:
        self.assertEqual(
            augmentation_named(3, "withdraw_reflection"),
            challenge4.Augmentation(withdraw_reflection=True),
        )
        self.assertEqual(
            augmentation_named(3, "extra_mark_1"),
            challenge4.Augmentation(extra_mark=1),
        )
        self.assertEqual(
            augmentation_named(4, "keep_labels"),
            challenge4.Augmentation(keep_labels=True),
        )
        self.assertEqual(policy_named("opaque"), challenge5.POLICY_OPAQUE)


class RequirementTests(unittest.TestCase):
    def test_the_live_requirement_is_unresolved_at_the_base(self) -> None:
        for reading in (READING_U, READING_O):
            row = live_requirement(reading, BASE_BRANCH)
            self.assertTrue(row["carried"])
            self.assertFalse(row["met"])

    def test_the_challenge_4_minimum_meets_the_live_requirement(self) -> None:
        for reading in (READING_U, READING_O):
            branch = next(
                b
                for b in declared_branches(reading)
                if b.name == "withdraw_mark_permutations"
            )
            self.assertTrue(live_requirement(reading, branch)["met"])

    def test_the_requirement_disappears_on_a_policy_branch(self) -> None:
        for reading in (READING_U, READING_O):
            branch = next(b for b in declared_branches(reading) if b.name == "opaque")
            row = live_requirement(reading, branch)
            self.assertFalse(row["carried"])
            self.assertIsNone(row["met"])
            self.assertEqual(branch_pairs(reading, branch), [])

    def test_the_further_mark_branch_carries_a_third_whole(self) -> None:
        branch = next(
            b for b in declared_branches(READING_U) if b.name == "extra_mark_0"
        )
        self.assertEqual(branch_pairs(READING_U, branch), [(0, 1), (0, 2), (1, 2)])
        self.assertEqual(remaining_demands(READING_U, branch), [(0, 2), (1, 2)])
        self.assertTrue(demand_met(READING_U, branch, (0, 2)))

    def test_no_other_branch_leaves_a_demand(self) -> None:
        for reading in (READING_U, READING_O):
            for branch in declared_branches(reading):
                if branch.name == "extra_mark_0":
                    continue
                self.assertEqual(remaining_demands(reading, branch), [], branch.name)

    def test_the_imposed_record_is_the_pair_the_caller_demanded(self) -> None:
        self.assertEqual(IMPOSED_DEMANDS, ((0, 1),))


class RecordTests(unittest.TestCase):
    def test_the_presented_record_is_the_rungs_own_inscriptions(self) -> None:
        self.assertEqual(
            PRESENTED_TEXTS,
            (INITIAL_INSCRIPTION, "<a|>", "<|a>", "<a|b>", "<b|a>", "<<a|>|>"),
        )
        self.assertEqual(presented_indices(), [0, 12, 1, 14, 25, 72])

    def test_every_presented_text_is_a_member_of_the_declared_domain(self) -> None:
        for text in PRESENTED_TEXTS:
            self.assertIn(text, domain_texts())

    def test_the_first_challenge(self) -> None:
        self.assertEqual(least_unpresented(), "<|b>")
        record = record_facts()
        self.assertEqual(record["least_unpresented_index"], 2)
        self.assertEqual(record["least_unpresented_marks"], 1)
        self.assertEqual(record["least_unpresented_depth"], 1)
        self.assertTrue(record["least_unpresented_is_a_further_mark"])
        self.assertNotIn("<|b>", PRESENTED_TEXTS)

    def test_first_missing_reads_both_ways(self) -> None:
        self.assertEqual(first_missing([0, 1, 3], 5), 2)
        self.assertEqual(first_missing([0, 1, 2, 3, 4], 5), None)
        self.assertEqual(first_missing([], 1), 0)

    def test_text_at_no_index_is_no_text(self) -> None:
        self.assertIsNone(text_at(None))
        self.assertEqual(text_at(0), "<|>")

    def test_marks_are_counted_at_every_level(self) -> None:
        self.assertEqual(marks_in(read_nested_whole("<|>")), 0)
        self.assertEqual(marks_in(read_nested_whole("<a|b>")), 2)
        self.assertEqual(marks_in(read_nested_whole("<<a|>|>")), 1)
        self.assertEqual(marks_in(read_nested_whole("<<a|b>|<a|b>>")), 4)

    def test_the_domain_holds_no_member_of_five_marks(self) -> None:
        self.assertEqual(domain_member_with_marks(4), "<<a|a>|<a|a>>")
        self.assertIsNone(domain_member_with_marks(5))


class GeneratorSpaceTests(unittest.TestCase):
    def test_the_space_is_the_product_of_its_declared_coordinates(self) -> None:
        space = generator_space()
        self.assertEqual(len(space), 12)
        self.assertEqual(len(set(generator_name(g) for g in space)), 12)
        self.assertEqual(len(COORDINATES), 3)

    def test_the_declared_capability_counts(self) -> None:
        self.assertEqual(mu1(Generator()), 0)
        self.assertEqual(capabilities(Generator(SOURCE_ENUMERATION)), [CAP_SUPPLY])
        self.assertEqual(
            capabilities(Generator(SOURCE_STATE)), [CAP_SUPPLY, CAP_READ_STATE]
        )
        self.assertEqual(capabilities(Generator(demands=True)), [CAP_DEMAND])
        self.assertEqual(capabilities(Generator(retains=True)), [CAP_ADMIT])
        self.assertEqual(
            capabilities(Generator(SOURCE_ENUMERATION, retains=True)),
            [CAP_SUPPLY, CAP_ADMIT],
        )

    def test_one_step_is_capability_count_one_and_not_coordinate_count(self) -> None:
        for g in generator_space():
            self.assertEqual(is_one_step(g), mu1(g) == 1)
            self.assertEqual(bundles(g), mu1(g) >= 2)
        state = Generator(SOURCE_STATE)
        self.assertEqual(len(changed_coordinates(state)), 1)
        self.assertEqual(mu1(state), 2)
        self.assertFalse(is_one_step(state))

    def test_a_generator_that_supplies_and_retains_is_refused(self) -> None:
        g = Generator(SOURCE_ENUMERATION, retains=True)
        self.assertTrue(bundles(g))
        self.assertFalse(is_one_step(g))

    def test_retaining_what_no_source_named_collapses_but_still_costs(self) -> None:
        self.assertEqual(
            effective_structure(Generator(retains=True)), effective_structure(Generator())
        )
        self.assertEqual(mu1(Generator(retains=True)), 1)
        self.assertNotEqual(
            effective_structure(Generator(SOURCE_ENUMERATION, retains=True)),
            effective_structure(Generator(SOURCE_ENUMERATION)),
        )

    def test_the_generator_names_are_deterministic(self) -> None:
        self.assertEqual(generator_name(Generator()), "none")
        self.assertEqual(
            generator_name(Generator(SOURCE_ENUMERATION, True, True)),
            "enumeration+retains+demands",
        )


class EmissionTests(unittest.TestCase):
    def test_the_enumeration_generator_emits_the_same_challenge_everywhere(self) -> None:
        for reading in (READING_U, READING_O):
            keys = {
                repr(emitted_key(reading, branch, Generator(SOURCE_ENUMERATION)))
                for branch in declared_branches(reading)
            }
            self.assertEqual(len(keys), 1)
            row = emitted(
                reading, declared_branches(reading)[0], Generator(SOURCE_ENUMERATION)
            )
            self.assertEqual(row["inscription"], "<|b>")
            self.assertFalse(row["retained"])
            self.assertIsNone(row["demand"])
            self.assertTrue(row["emits"])

    def test_the_null_generator_emits_nothing_anywhere(self) -> None:
        for reading in (READING_U, READING_O):
            for branch in declared_branches(reading):
                self.assertFalse(emitted(reading, branch, Generator())["emits"])
                self.assertFalse(
                    emitted(reading, branch, Generator(retains=True))["emits"]
                )

    def test_the_demand_generator_emits_on_one_branch_of_reading_u_alone(self) -> None:
        u = [
            branch.name
            for branch in declared_branches(READING_U)
            if emitted(READING_U, branch, Generator(demands=True))["emits"]
        ]
        o = [
            branch.name
            for branch in declared_branches(READING_O)
            if emitted(READING_O, branch, Generator(demands=True))["emits"]
        ]
        self.assertEqual(u, ["extra_mark_0"])
        self.assertEqual(o, [])

    def test_the_demand_it_emits_is_already_met(self) -> None:
        branch = next(
            b for b in declared_branches(READING_U) if b.name == "extra_mark_0"
        )
        row = emitted(READING_U, branch, Generator(demands=True))
        self.assertEqual(row["demand"], [0, 2])
        self.assertTrue(row["demand_already_met"])

    def test_a_generator_that_does_not_demand_emits_no_demand(self) -> None:
        self.assertIsNone(
            emitted_demand(READING_U, BASE_BRANCH, Generator(SOURCE_ENUMERATION))
        )
        self.assertIsNone(emitted_demand(READING_U, BASE_BRANCH, Generator(demands=True)))

    def test_the_state_source_reads_the_mark_count(self) -> None:
        branches = {b.name: b for b in declared_branches(READING_U)}
        self.assertEqual(
            emitted_inscription(READING_U, branches["base"], Generator(SOURCE_STATE)),
            "<<a|a>|<a|a>>",
        )
        self.assertEqual(
            emitted_inscription(READING_U, branches["opaque"], Generator(SOURCE_STATE)),
            "<|a>",
        )
        self.assertIsNone(
            emitted_inscription(
                READING_U, branches["extra_mark_0"], Generator(SOURCE_STATE)
            )
        )
        self.assertIsNone(
            emitted_inscription(READING_U, branches["base"], Generator(SOURCE_NONE))
        )

    def test_two_generators_are_two_when_they_part_at_a_branch(self) -> None:
        parted = differing_branches(
            READING_U, Generator(SOURCE_ENUMERATION), Generator(demands=True)
        )
        self.assertEqual(len(parted), 6)
        self.assertEqual(
            differing_branches(
                READING_U, Generator(SOURCE_ENUMERATION), Generator(SOURCE_ENUMERATION)
            ),
            [],
        )

    def test_the_class_key_is_the_structure_with_the_behaviour_digest(self) -> None:
        key = generator_class_key(READING_U, Generator(SOURCE_ENUMERATION), "abc")
        self.assertEqual(key[-1], "abc")
        self.assertEqual(key[:-1], ["enumeration", "False", "False"])
        self.assertNotEqual(behaviour_digest([1]), behaviour_digest([2]))


class SubstitutionCensusTests(unittest.TestCase):
    def test_the_enumeration_generator_reads_nothing_of_the_branch(self) -> None:
        for reading in (READING_U, READING_O):
            row = branch_substitution_census(reading, Generator(SOURCE_ENUMERATION))
            self.assertTrue(row["reads_nothing_of_the_branch"])
            self.assertEqual(row["substitutions_that_move_the_challenge"], 0)
            self.assertGreater(row["distinct_configuration_keys"], 1)

    def test_the_state_source_moves_under_the_same_census(self) -> None:
        # The direction that makes the census a test and not a tautology.
        for reading in (READING_U, READING_O):
            row = branch_substitution_census(reading, Generator(SOURCE_STATE))
            self.assertFalse(row["reads_nothing_of_the_branch"])
            self.assertGreater(row["substitutions_that_move_the_challenge"], 0)

    def test_the_demand_generator_moves_under_u_and_not_under_o(self) -> None:
        self.assertFalse(
            branch_substitution_census(READING_U, Generator(demands=True))[
                "reads_nothing_of_the_branch"
            ]
        )
        self.assertTrue(
            branch_substitution_census(READING_O, Generator(demands=True))[
                "reads_nothing_of_the_branch"
            ]
        )


class MinimaTests(unittest.TestCase):
    def test_the_minimum_among_emitting_generators_is_one(self) -> None:
        for reading in (READING_U, READING_O):
            facts = reading_facts(reading)
            self.assertEqual(facts["minimum_capability_count_among_emitting"], [1])

    def test_the_tie_is_on_the_further_mark_branch_of_reading_u_alone(self) -> None:
        u = reading_facts(READING_U)
        o = reading_facts(READING_O)
        self.assertEqual(u["branches_with_a_tie"], ["extra_mark_0"])
        self.assertEqual(o["branches_with_a_tie"], [])
        self.assertFalse(u["the_minimum_is_unique_on_every_branch"])
        self.assertTrue(o["the_minimum_is_unique_on_every_branch"])

    def test_both_tied_classes_are_retained(self) -> None:
        u = reading_facts(READING_U)
        row = next(r for r in u["branch_detail"] if r["name"] == "extra_mark_0")
        self.assertEqual(len(row["minima_by_mu1"]["classes"]), 2)
        self.assertEqual(
            sorted(row["weakest_emitting_generators"]), ["enumeration", "none+demands"]
        )
        self.assertFalse(row["minima_by_mu1"]["unique"])

    def test_every_other_branch_has_one_weakest_generator(self) -> None:
        for reading in (READING_U, READING_O):
            for row in reading_facts(reading)["branch_detail"]:
                if row["name"] == "extra_mark_0":
                    continue
                self.assertEqual(row["weakest_emitting_generators"], ["enumeration"])

    def test_the_null_generator_is_not_eligible(self) -> None:
        for reading in (READING_U, READING_O):
            for row in reading_facts(reading)["branch_detail"]:
                self.assertNotIn("none", row["weakest_emitting_generators"])
                self.assertNotIn("none", row["emitting_generators"])


class BoundTests(unittest.TestCase):
    def test_the_node_counts(self) -> None:
        self.assertEqual(nodes(6, 3, 0), 6)
        self.assertEqual(nodes(6, 3, 4), 726)
        self.assertEqual(nodes(6, 3, 5), 2184)
        self.assertEqual(nodes(5, 3, 4), 605)
        self.assertEqual(nodes(5, 3, 5), 1820)

    def test_a_negative_round_count_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            nodes(6, 3, -1)

    def test_the_round_bound_is_computed_from_the_ceiling(self) -> None:
        self.assertEqual(round_bound(6, 3, NODE_CEILING), 4)
        self.assertEqual(round_bound(5, 3, NODE_CEILING), 4)
        self.assertEqual(round_bound(6, 3, 10), 0)
        self.assertEqual(round_bound(1, 1, 10 ** 9), SEED_ROUND_BOUND)

    def test_the_branching_bound_is_read_off_the_closed_rungs(self) -> None:
        self.assertEqual(branching_bound(), 3)
        self.assertEqual(len(rung_classes(3, READING_U)), 3)

    def test_the_bounds_row(self) -> None:
        for reading, branches in ((READING_U, 6), (READING_O, 5)):
            bounds = reading_facts(reading)["bounds"]
            self.assertEqual(bounds["branches"], branches)
            self.assertEqual(bounds["round_bound"], 4)
            self.assertTrue(bounds["short_of_the_seed_bound"])
            self.assertTrue(bounds["frontier_export_is_owed"])
            self.assertEqual(bounds["rounds_accepted_at_this_stage"], 0)
            self.assertLessEqual(bounds["nodes_at_the_round_bound"], NODE_CEILING)
            self.assertGreater(bounds["nodes_one_round_further"], NODE_CEILING)
            self.assertEqual(len(bounds["ceiling_sensitivity"]), len(CEILING_SENSITIVITY))

    def test_the_ceiling_is_declared_and_the_bound_moves_with_it(self) -> None:
        rows = reading_facts(READING_U)["bounds"]["ceiling_sensitivity"]
        self.assertEqual([row[1] for row in rows], [0, 2, 4, 6, 8])


class LeanAgreementTests(unittest.TestCase):
    """The Lean file states the same numbers; a rename or a drift is caught."""

    def source(self) -> str:
        return (TREE / "lean" / "BoundarySeed" / "Continuation1.lean").read_text(
            encoding="utf-8"
        )

    def test_the_lean_record_is_the_python_record(self) -> None:
        text = self.source()
        self.assertIn(
            "def presentedIndices : List Nat := "
            + str(presented_indices()).replace(" ", " "),
            text,
        )
        self.assertIn(f"def domainSize : Nat := {len(domain_texts())}", text)

    def test_the_lean_first_challenge_is_the_python_one(self) -> None:
        index = presented_indices()
        self.assertNotIn(2, index)
        self.assertIn(
            "firstMissing presentedIndices domainSize = some 2", self.source()
        )

    def test_the_lean_node_counts_are_the_python_ones(self) -> None:
        text = self.source()
        for b, r, value in ((6, 4, 726), (6, 5, 2184), (5, 4, 605), (5, 5, 1820)):
            self.assertEqual(nodes(b, 3, r), value)
            self.assertIn(f"nodes {b} 3 {r} = {value}", text)
        self.assertIn(f"nodes 6 3 4 ≤ {NODE_CEILING}", text)
        self.assertIn(f"nodes 5 3 4 ≤ {NODE_CEILING}", text)

    def test_the_lean_theorems_are_audited(self) -> None:
        root = (TREE / "lean" / "BoundarySeed.lean").read_text(encoding="utf-8")
        for name in ("firstMissing_never_repeats", "roundBound_U", "roundBound_O",
                     "firstMissingFrom_none_means_every_index_present"):
            self.assertIn(f"#print axioms BoundarySeed.{name}", root)


class ScoreTests(unittest.TestCase):
    def facts(self) -> tuple[Json, Json, Json]:
        receipt = build()
        return (
            receipt["readings"][READING_U],
            receipt["readings"][READING_O],
            receipt["record"],
        )

    def test_the_scores_on_the_real_receipt(self) -> None:
        u, o, record = self.facts()
        scores = score(u, o, record)
        self.assertEqual(
            {cid: scores[cid]["status"] for cid in SCORED_PREDICTIONS},
            {
                "S1-1": "HIT",
                "S1-2": "HIT",
                "S1-3": "HIT",
                "S1-4": "HIT",
                "S1-5": "HIT",
                "S1-6": "PARTIAL",
                "S1-7": "HIT",
                "S1-8": "HIT",
                "S1-9": "HIT",
            },
        )
        self.assertEqual(scores["S1-X"]["status"], "PENDING")

    def test_s1_6_misses_its_event_census_clause(self) -> None:
        # The frozen clause asserted this stage's module would have no function
        # returning an event, and it has one: the reader of the recorded caller
        # history each branch replays.  The miss is recorded, not repaired.
        self.assertEqual(event_returning_functions(), ["inherited_history"])
        u, o, record = self.facts()
        scores = score(u, o, record)
        self.assertEqual(
            scores["S1-6"]["no_event_returning_function_clause_status"], "MISSED"
        )
        self.assertEqual(scores["S1-6"]["substitution_clause_status"], "HIT")
        facts = events_named_facts()
        self.assertEqual(facts["functions"], ["inherited_history"])
        self.assertTrue(facts["every_branch_configuration_is_certified"])
        self.assertEqual(facts["event_kinds_declared_at_this_stage"], [])

    def test_s1_1_misses_when_a_branch_count_moves(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(u)
        moved["branch_count"] = 7
        self.assertEqual(score(moved, o, record)["S1-1"]["counts_clause_status"], "MISSED")
        self.assertEqual(score(moved, o, record)["S1-1"]["status"], "PARTIAL")

    def test_s1_1_misses_when_the_quotient_identifies_nothing(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(u)
        moved["branch_classes"] = [[name] for group in u["branch_classes"] for name in group]
        scores = score(moved, o, record)
        self.assertEqual(
            scores["S1-1"]["quotient_identifies_a_class_clause_status"], "MISSED"
        )

    def test_s1_2_misses_when_the_policy_part_carries_nothing(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(u)
        moved["branch_count_without_the_policy_key"] = 6
        self.assertEqual(score(moved, o, record)["S1-2"]["status"], "MISSED")

    def test_s1_3_misses_when_the_space_size_moves(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(u)
        moved["generator_space_size"] = 8
        scores = score(moved, o, record)
        self.assertEqual(scores["S1-3"]["space_size_clause_status"], "MISSED")

    def test_s1_3_misses_when_the_two_counts_agree(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(u)
        moved["one_step_iff_one_coordinate_moved"] = True
        scores = score(moved, o, record)
        self.assertEqual(scores["S1-3"]["counts_part_clause_status"], "MISSED")

    def test_s1_4_misses_when_the_minimum_moves(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(u)
        moved["minimum_capability_count_among_emitting"] = [2]
        self.assertEqual(
            score(moved, o, record)["S1-4"]["minimum_clause_status"], "MISSED"
        )

    def test_s1_4_misses_when_the_tie_moves(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(u)
        moved["branches_with_a_tie"] = []
        self.assertEqual(score(moved, o, record)["S1-4"]["tie_clause_status"], "MISSED")

    def test_s1_4_misses_when_the_demand_generator_emits_elsewhere(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(o)
        moved["demand_generator_emits_at"] = ["base"]
        self.assertEqual(
            score(u, moved, record)["S1-4"]["demand_generator_clause_status"], "MISSED"
        )

    def test_s1_5_misses_when_the_challenge_differs_between_branches(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(u)
        moved["the_same_challenge_on_every_branch"] = False
        self.assertEqual(
            score(moved, o, record)["S1-5"]["same_challenge_clause_status"], "MISSED"
        )

    def test_s1_5_misses_when_the_first_challenge_is_not_a_further_mark(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(record)
        moved["least_unpresented_is_a_further_mark"] = False
        self.assertEqual(
            score(u, o, moved)["S1-5"]["first_challenge_clause_status"], "MISSED"
        )

    def test_s1_6_misses_when_the_generator_reads_the_branch(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(u)
        for row in moved["substitution_census"]:
            if row["generator"] == "enumeration":
                row["reads_nothing_of_the_branch"] = False
        scores = score(moved, o, record)
        self.assertEqual(scores["S1-6"]["substitution_clause_status"], "MISSED")
        self.assertEqual(scores["S1-6"]["status"], "MISSED")

    def test_s1_7_misses_when_the_challenge_is_already_presented(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(record)
        moved["presented"] = [*record["presented"], record["least_unpresented"]]
        self.assertEqual(score(u, o, moved)["S1-7"]["status"], "MISSED")

    def test_s1_8_misses_when_the_round_bound_moves(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(u)
        moved["bounds"]["round_bound"] = 15
        self.assertEqual(score(moved, o, record)["S1-8"]["status"], "MISSED")

    def test_s1_9_misses_when_a_branch_does_not_replay(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(u)
        moved["branch_detail"][0]["certified"] = False
        scores = score(moved, o, record)
        self.assertEqual(scores["S1-9"]["inertia_clause_status"], "MISSED")

    def test_s1_9_misses_when_a_round_is_accepted(self) -> None:
        u, o, record = self.facts()
        moved = copy.deepcopy(u)
        moved["bounds"]["rounds_accepted_at_this_stage"] = 1
        scores = score(moved, o, record)
        self.assertEqual(scores["S1-9"]["no_round_accepted_clause_status"], "MISSED")

    def test_c5x_is_pending_with_four_clauses_hit(self) -> None:
        u, o, record = self.facts()
        row = score_c5x(u, o, record)
        self.assertEqual(row["status"], "PENDING")
        self.assertEqual(row["frontier_exported_clause_status"], "PENDING")
        for key in (
            "first_challenge_is_a_further_mark_clause_status",
            "imports_no_undeclared_structure_clause_status",
            "fifteen_rounds_not_reached_clause_status",
            "smaller_bound_declared_clause_status",
        ):
            self.assertEqual(row[key], "HIT", key)

    def test_c5x_clauses_read_both_ways(self) -> None:
        u, o, record = self.facts()
        no_mark = copy.deepcopy(record)
        no_mark["least_unpresented_is_a_further_mark"] = False
        self.assertEqual(
            score_c5x(u, o, no_mark)["first_challenge_is_a_further_mark_clause_status"],
            "MISSED",
        )
        reads = copy.deepcopy(u)
        for row in reads["substitution_census"]:
            if row["generator"] == "enumeration":
                row["reads_nothing_of_the_branch"] = False
        self.assertEqual(
            score_c5x(reads, o, record)["imports_no_undeclared_structure_clause_status"],
            "MISSED",
        )
        ran = copy.deepcopy(u)
        ran["bounds"]["rounds_accepted_at_this_stage"] = 15
        self.assertEqual(
            score_c5x(ran, o, record)["fifteen_rounds_not_reached_clause_status"],
            "MISSED",
        )
        wide = copy.deepcopy(u)
        wide["bounds"]["short_of_the_seed_bound"] = False
        self.assertEqual(
            score_c5x(wide, o, record)["smaller_bound_declared_clause_status"], "MISSED"
        )

    def test_the_scoring_helpers_read_every_way(self) -> None:
        self.assertEqual(verdict(True), "HIT")
        self.assertEqual(verdict(False), "MISSED")
        self.assertEqual(combine("HIT", "HIT"), "HIT")
        self.assertEqual(combine("MISSED", "MISSED"), "MISSED")
        self.assertEqual(combine("HIT", "MISSED"), "PARTIAL")

    def test_the_tally_counts_definition_level_apart_from_content(self) -> None:
        receipt = build()
        counts = receipt["tally"]
        self.assertEqual(counts["hit_definition_level"], list(DEFINITION_LEVEL_PREDICTIONS))
        self.assertEqual(counts["partial"], ["S1-6"])
        self.assertEqual(counts["missed"], [])
        self.assertEqual(len(counts["hit_as_content"]), 7)

    def test_the_tally_refuses_an_unknown_status(self) -> None:
        scores = {cid: {"status": "HIT"} for cid in SCORED_PREDICTIONS}
        scores["S1-1"]["status"] = "SHARPENED"
        with self.assertRaises(ValueError):
            tally(scores)

    def test_the_tally_moves_a_miss_out_of_the_hit_lists(self) -> None:
        scores = {cid: {"status": "HIT"} for cid in SCORED_PREDICTIONS}
        scores["S1-2"]["status"] = "MISSED"
        counts = tally(scores)
        self.assertEqual(counts["missed"], ["S1-2"])
        self.assertNotIn("S1-2", counts["hit_as_content"])


class ReceiptShapeTests(unittest.TestCase):
    def test_the_receipt_states_that_no_round_is_run(self) -> None:
        receipt = build()
        self.assertEqual(receipt["stage"], 1)
        self.assertIn("no round is run", receipt["closes"])
        self.assertEqual(receipt["new_event_kinds_at_stage_1"], [])
        self.assertEqual(receipt["withdrawn_rules_at_stage_1"], [])
        self.assertEqual(receipt["authority_effect"], "None")

    def test_the_kernel_declares_no_event_generator(self) -> None:
        receipt = build()
        census = receipt["event_returning_functions_by_module"]
        self.assertEqual(census["model"], [])
        self.assertEqual(census["continuation1"], ["inherited_history"])

    def test_every_branch_row_reports_its_declarations_and_its_replay(self) -> None:
        receipt = build()
        for reading in (READING_U, READING_O):
            rows = receipt["readings"][reading]["branch_detail"]
            self.assertEqual(len(rows), len(declared_branches(reading)))
            for row in rows:
                self.assertTrue(row["certified"])
                self.assertTrue(row["replays_from_genesis"])
                self.assertTrue(row["initial_datum_unchanged"])
                self.assertTrue(row["reading_unchanged"])
                self.assertTrue(row["event_follows_relation_empty"])
                self.assertTrue(row["deep_event_follows_relation_empty"])
                self.assertEqual(len(row["generators"]), 12)
                self.assertGreaterEqual(row["automorphism_count"], 1)

    def test_the_branch_configurations_are_the_recorded_replays(self) -> None:
        for reading in (READING_U, READING_O):
            for branch in declared_branches(reading):
                configuration = branch_configuration(reading, branch)
                self.assertEqual(
                    configuration.regime.n_marks(), len(configuration.groups)
                )


if __name__ == "__main__":
    unittest.main()
