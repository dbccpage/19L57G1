"""Fresh replay, complete ties, challenge validity and finite frontier checks."""

from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import sys
import unittest
from dataclasses import replace
from typing import Any
from unittest.mock import patch

TREE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TREE / "code"))
from boundary import challenge4, challenge5, continuation1 as prior, continuation2 as run, model  # noqa: E402


class ContinuationTests(unittest.TestCase):
    receipt: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt = run.build()

    def test_stage2_prediction_bytes_are_pinned(self) -> None:
        self.assertEqual(hashlib.sha256((TREE / "continuation/stage2/PREDICTIONS.md").read_bytes()).hexdigest(), run.PREDICTIONS_SHA256)

    def test_committed_receipt_matches_the_renderer(self) -> None:
        self.assertEqual((TREE / "receipts/continuation2.json").read_bytes(), run.render(self.receipt))

    def test_every_inherited_generator_class_is_a_root(self) -> None:
        for reading in model.READINGS:
            expected = []
            for branch in prior.declared_branches(reading):
                detail = prior.branch_detail(reading, branch)
                # Use the inherited eligibility rows independently of stage 2.
                rows = detail["generators"]
                self.assertTrue(rows)
                eligible = [row for row in rows if row["one_step"] and row["emits"]]
                least = min(row["mu1"] for row in eligible)
                keys: set[str] = set()
                for row in eligible:
                    key = repr(row["class_key"])
                    if row["mu1"] == least and key not in keys:
                        expected.append((branch.label(), row["name"]))
                        keys.add(key)
            roots = [node for node in self.receipt["readings"][reading]["nodes"] if node["parent"] is None]
            self.assertCountEqual([(node["origin"], node["generator"]) for node in roots], expected)

    def test_exact_node_and_frontier_counts(self) -> None:
        u, o = (self.receipt["readings"][reading] for reading in model.READINGS)
        self.assertEqual((u["root_count"], u["node_count"], len(u["frontier"]), len(u["terminals"])), (7, 33, 6, 1))
        self.assertEqual((o["root_count"], o["node_count"], len(o["frontier"]), len(o["terminals"])), (5, 25, 5, 0))

    def test_frontier_has_exact_next_challenge_and_zero_accepted(self) -> None:
        for forest in self.receipt["readings"].values():
            for node in forest["nodes"]:
                self.assertEqual(node["accepted"], 0)
                if node["id"] in forest["frontier"]:
                    self.assertEqual(node["attempted"], 4)
                    self.assertEqual(node["status"], "attempt_bound")
                    self.assertEqual(node["challenge"], {"inscription": "<|<a|>>", "demand": None})

    def test_supply_prefix_is_indices_two_through_five(self) -> None:
        forest = self.receipt["readings"]["U"]
        line = [node for node in forest["nodes"] if node["origin"] == "base"]
        self.assertEqual([node["presented"][-1] for node in line[1:]], [2, 3, 4, 5])
        self.assertEqual([node["state"]["placement"] for node in line], [line[0]["state"]["placement"]] * 5)
        self.assertEqual([len(node["state"]["continuation_events"]) for node in line], [0, 1, 2, 3, 4])

    def test_demand_line_tracks_new_requirements_and_exhaustion(self) -> None:
        nodes = [node for node in self.receipt["readings"]["U"]["nodes"] if node["generator"] == "none+demands"]
        self.assertEqual([node["challenge"] for node in nodes], [{"inscription": None, "demand": [0, 2]}, {"inscription": None, "demand": [1, 2]}, None])
        self.assertEqual(nodes[-1]["requirements"], {"0,1": "unresolved", "0,2": "met", "1,2": "met"})
        self.assertEqual(nodes[-1]["status"], "no_next_challenge")
        self.assertEqual(nodes[-1]["attempted"], 2)

    def test_every_recorded_endpoint_is_replayed_and_certified(self) -> None:
        for reading, forest in self.receipt["readings"].items():
            branches = {branch.label(): branch for branch in prior.declared_branches(reading)}
            for node in forest["nodes"]:
                events: list[model.Event] = []
                for event in node["state"]["full_flat_replay_history"]:
                    if event["kind"] == "Supply":
                        events.append(model.Supply(event["token"]))
                    else:
                        self.assertEqual(event["kind"], "AdmitOccurrence")
                        events.append(model.AdmitOccurrence(event["token"], event["side"]))
                self.assertTrue(prior.branch_certified(reading, branches[node["origin"]]))
                replayed = model.replay(events, model.genesis(reading))
                self.assertEqual(list(replayed.placement), node["state"]["placement"])
                self.assertEqual(list(replayed.marks), node["state"]["marks"])
                self.assertTrue(node["state"]["certified"])

    def test_successful_null_is_never_no_valid_response(self) -> None:
        for forest in self.receipt["readings"].values():
            for node in forest["nodes"]:
                if node["minimum_classes"] == [["null"]]:
                    self.assertEqual(node["status"], "expanded")
                    self.assertTrue(any(row["name"] == "null" and row["valid"] for row in node["candidate_rows"]))
                    self.assertTrue(any(row["cost"] > 0 for row in node["candidate_rows"]))

    def test_nontrivial_demand_rejects_null_and_finds_positive_responses(self) -> None:
        state = run.initial(prior.BASE_BRANCH)
        for reading in model.READINGS:
            rows, groups = run.response_rows(reading, state, run.Challenge(demand=(0, 1)), prior.IMPOSED_DEMANDS)
            self.assertFalse(rows[0]["valid"])
            self.assertTrue(groups)
            self.assertTrue(all(response.cost == 1 for group in groups for response in group))

    def test_supply_predicate_is_recomputed_not_inferred_from_inertia(self) -> None:
        state = run.initial(prior.BASE_BRANCH)
        with patch.object(run, "valid", return_value=False):
            rows, groups = run.response_rows("U", state, run.Challenge("<|b>"), prior.IMPOSED_DEMANDS)
        self.assertFalse(groups)
        self.assertTrue(all(not row["valid"] for row in rows))

    def test_candidate_space_contains_all_available_positive_capabilities(self) -> None:
        state = run.initial(prior.BASE_BRANCH)
        responses = run.candidates("U", state, run.Challenge("<|b>"))
        self.assertEqual({response.value for response in responses if response.kind == "declare"}, set(challenge4.COORDINATES[:-1]))
        self.assertEqual({response.value for response in responses if response.kind == "occurrence"}, {"0", "1"})
        self.assertEqual({response.value for response in responses if response.kind == "policy"}, set(challenge5.POLICY_SPACE[1:]))
        self.assertIn("retain", [response.name() for response in responses])

    def test_recording_policy_is_a_priced_refused_bundle(self) -> None:
        rows, _groups = run.response_rows("U", run.initial(prior.BASE_BRANCH), run.Challenge("<|b>"), prior.IMPOSED_DEMANDS)
        record = next(row for row in rows if row["name"] == "policy:" + challenge5.POLICY_ADDRESS)
        self.assertEqual(record["cost"], 2)
        self.assertFalse(record["valid"])
        self.assertIn("bundles", record["refusal"])

    def test_positive_occurrence_has_explicit_admission_replay(self) -> None:
        state = run.initial(prior.BASE_BRANCH)
        after = run.apply_response("U", state, run.Challenge(demand=(0, 1)), run.Response("occurrence", "1", 1))
        self.assertEqual(after.events, (model.AdmitOccurrence("a", 1),))
        self.assertEqual(run.configuration("U", after).regime.n_marks(), 5)
        self.assertEqual(run.configuration("U", after).groups[-1], 2)
        self.assertTrue(run.state_json("U", after)["certified"])

    def test_genesis_prefix_preserves_supply_witnesses_for_positive_candidates(self) -> None:
        for reading in model.READINGS:
            for branch in prior.declared_branches(reading):
                rows, _groups = run.response_rows(reading, run.initial(branch), run.Challenge("<|b>"), prior.IMPOSED_DEMANDS)
                occurrences = [row for row in rows if row["name"].startswith("occurrence:")]
                self.assertEqual(len(occurrences), 2)
                self.assertTrue(all(row["valid"] for row in occurrences), branch.label())

    def test_lean_prefix_and_root_bounds_agree_with_executed_census(self) -> None:
        self.assertEqual(prior.nodes(7, 3, 4), 847)
        self.assertEqual(prior.nodes(5, 3, 4), 605)
        text = (TREE / "lean/BoundarySeed/Continuation2.lean").read_text(encoding="utf-8")
        self.assertIn("supplyPrefix 4 presentedIndices = [2, 3, 4, 5]", text)
        self.assertIn("domainSize = some 6", text)

    def test_retention_uses_declared_policy_and_is_not_supply(self) -> None:
        state = run.initial(prior.BASE_BRANCH)
        retained = run.apply_response("U", state, run.Challenge("<|b>"), run.Response("retain", cost=1))
        self.assertEqual(retained.events, (model.Supply("b"), model.AdmitOccurrence("b", 1)))
        with self.assertRaisesRegex(ValueError, "retention refused"):
            run.apply_response("U", state, run.Challenge("<<a|>|>"), run.Response("retain", cost=1))
        opaque = replace(state, policy=challenge5.POLICY_OPAQUE)
        nested = run.apply_response("U", opaque, run.Challenge("<<a|>|>"), run.Response("retain", cost=1))
        self.assertEqual(len(nested.groups), 1)
        with self.assertRaisesRegex(ValueError, "depth exceeds"):
            run.apply_response("U", replace(state, policy=challenge5.POLICY_ADDRESS), run.Challenge("<<a|>|>"), run.Response("retain", cost=1))

    def test_inapplicable_responses_are_refused_by_name(self) -> None:
        for response in [run.Response("unknown"), run.Response("retain")]:
            with self.assertRaisesRegex(ValueError, "inapplicable response"):
                run.apply_response("U", run.initial(prior.BASE_BRANCH), run.Challenge(demand=(0, 1)), response)

    def test_generator_exhaustion_and_unknown_generator(self) -> None:
        state = run.initial(prior.BASE_BRANCH)
        self.assertIsNone(run.next_challenge("U", state, prior.ENUMERATION_GENERATOR, tuple(range(144)), prior.IMPOSED_DEMANDS))
        self.assertIsNone(run.next_challenge("U", state, prior.DEMAND_GENERATOR, (), prior.IMPOSED_DEMANDS))
        with self.assertRaisesRegex(ValueError, "outside the inherited"):
            run.next_challenge("U", state, prior.NULL_GENERATOR, (), ())

    def test_invalid_bounds_fail_without_dropping_roots(self) -> None:
        for attempts, ceiling in [(-1, 1000), (4, 0), (4, 1)]:
            with self.assertRaisesRegex(ValueError, "bound|every inherited"):
                run.execute("U", attempts, ceiling)

    def test_zero_attempt_and_node_ceiling_frontiers_are_exact(self) -> None:
        zero = run.execute("O", 0)
        self.assertEqual(len(zero["frontier"]), 5)
        limited = run.execute("U", node_ceiling=7)
        self.assertEqual(limited["node_count"], 7)
        self.assertEqual(len(limited["frontier"]), 7)
        self.assertTrue(all(node["status"] == "node_ceiling" for node in limited["nodes"]))

    def test_accepted_bound_is_not_attempt_bound(self) -> None:
        with patch.object(run, "ACCEPTED_BOUND", 0):
            forest = run.execute("O")
        self.assertTrue(all(node["status"] == "accepted_bound" for node in forest["nodes"]))

    def test_no_valid_response_is_a_real_failed_predicate_terminal(self) -> None:
        with patch.object(run, "valid", return_value=False):
            forest = run.execute("O")
        self.assertEqual(len(forest["terminals"]), 5)
        self.assertTrue(all(node["status"] == "no_valid_response" for node in forest["nodes"]))

    def test_branching_bound_preserves_the_entire_pending_tie(self) -> None:
        alternatives = [[run.Response("declare", coordinate, 1)] for coordinate in challenge4.COORDINATES[:4]]
        with patch.object(run, "response_rows", return_value=([], alternatives)):
            forest = run.execute("O")
        self.assertEqual(len(forest["frontier"]), 5)
        for node in forest["nodes"]:
            self.assertEqual(node["status"], "branching_bound")
            self.assertEqual(len(node["minimum_classes"]), 4)

    def test_positive_accepted_response_is_counted_and_preserved(self) -> None:
        with patch.object(run, "response_rows", return_value=([], [[run.Response("declare", "withdraw_reflection", 1)]])):
            forest = run.execute("U", 1)
        self.assertTrue(all(node["accepted"] == 1 for node in forest["nodes"] if node["parent"] is not None))

    def test_every_tied_minimum_class_is_retained(self) -> None:
        state = run.initial(prior.BASE_BRANCH)
        points = [run.Response("declare", name, 1) for name in ("withdraw_reflection", "withdraw_mark_permutations")]
        with patch.object(run, "candidates", return_value=points), patch.object(run, "valid", return_value=True):
            _rows, groups = run.response_rows("U", state, run.Challenge("<|b>"), ())
        self.assertEqual({response.name() for group in groups for response in group}, {point.name() for point in points})
        self.assertEqual(len(groups), 2)

    def test_u_reflection_quotient_and_policy_domain_are_load_bearing(self) -> None:
        state = run.initial(prior.BASE_BRANCH)
        left = run.apply_response("U", state, run.Challenge("<|b>"), run.Response("occurrence", "0", 1))
        right = run.apply_response("U", state, run.Challenge("<|b>"), run.Response("occurrence", "1", 1))
        self.assertEqual(run.state_key("U", left, ()), run.state_key("U", right, ()))
        self.assertNotEqual(run.state_key("O", left, ()), run.state_key("O", right, ()))
        self.assertNotEqual(run.state_key("U", replace(state, policy=challenge5.POLICY_OPAQUE), ()), run.state_key("U", replace(state, policy=challenge5.POLICY_FLATTEN), ()))

    def test_requirements_do_not_conflate_disappearance_with_satisfaction(self) -> None:
        state = run.initial(prior.BASE_BRANCH)
        self.assertEqual(run.requirement("U", state, (0, 99)), "disappeared")
        self.assertFalse(run.valid("U", state, state, run.Challenge(demand=(0, 99))))
        self.assertFalse(run.valid("U", state, state, run.Challenge()))
        with patch.object(run, "MARK_BOUND", 0):
            self.assertFalse(run.valid("U", state, state, run.Challenge("<|b>")))

    def test_met_carried_requirement_cannot_be_lost(self) -> None:
        state = run.initial(prior.BASE_BRANCH)
        def status(reading: str, current: run.State, pair: tuple[int, int]) -> str:
            return "met" if not current.events else "unresolved"
        with patch.object(run, "requirement", side_effect=status), patch.object(run, "candidates", return_value=[run.Response("occurrence", "0", 1)]):
            rows, groups = run.response_rows("U", state, run.Challenge("<|b>"), prior.IMPOSED_DEMANDS)
        self.assertFalse(rows[0]["valid"])
        self.assertFalse(groups)

    def test_uncertified_origin_cannot_be_used(self) -> None:
        branch = replace(prior.BASE_BRANCH, name="uncertified-probe")
        with patch.object(prior, "branch_certified", return_value=False):
            with self.assertRaisesRegex(ValueError, "uncertified origin"):
                run.origin_configuration("U", branch)

    def test_clean_export_replays(self) -> None:
        self.assertEqual(run.verify_export(self.receipt), [])

    def test_corrupted_replay_and_tie_omission_are_named(self) -> None:
        for field in ("state", "minimum_classes", "nodes", "frontier"):
            broken = copy.deepcopy(self.receipt)
            forest = broken["readings"]["U"]
            if field == "state":
                forest["nodes"][7]["state"]["continuation_events"][0]["token"] = "changed"
            elif field == "minimum_classes":
                forest["nodes"][0][field] = []
            else:
                forest[field].pop()
            problems = run.verify_export(broken)
            self.assertTrue(problems)
            self.assertTrue(any(field in problem for problem in problems))

    def test_export_type_and_field_censuses_fail_closed(self) -> None:
        broken = copy.deepcopy(self.receipt)
        broken["stage"] = "2"
        self.assertIn("value type differs", run.verify_export(broken)[0])
        broken = copy.deepcopy(self.receipt)
        del broken["scores"]
        self.assertIn("field census differs", run.verify_export(broken)[0])

    def test_scores_preserve_literal_misses_and_pending_extrapolation(self) -> None:
        scores = self.receipt["scores"]
        self.assertTrue(all(scores[f"S2-{number}"]["status"] == "HIT" for number in range(1, 7)))
        self.assertEqual(scores["S2-X"]["status"], "PENDING")
        self.assertEqual(scores["S1-X"]["status"], "PARTIAL")
        self.assertFalse(scores["S1-X"]["clauses"]["every_first_challenge_supplies_the_predicted_text"])
        self.assertFalse(scores["S1-X"]["clauses"]["every_branch_stops_for_want_of_a_response_before_the_bound"])
        self.assertEqual(scores["C5-X"]["status"], "HIT")

    def test_each_stage2_score_has_a_negative_direction(self) -> None:
        for number in range(1, 7):
            readings = copy.deepcopy(self.receipt["readings"])
            u = readings["U"]
            if number == 1:
                u["root_count"] = 6
            elif number == 2:
                u["nodes"][0]["candidate_rows"] = []
            elif number == 3:
                next(node for node in u["nodes"] if node["generator"] == "none+demands")["minimum_classes"] = []
            elif number == 4:
                u["nodes"][0]["accepted"] = 1
            elif number == 5:
                for forest in readings.values():
                    forest["frontier"] = []
            else:
                for node in u["nodes"]:
                    node["requirements"] = {}
            self.assertEqual(run.score(readings)[f"S2-{number}"]["status"], "MISSED")

    def test_receipt_is_deterministic_and_environment_free(self) -> None:
        self.assertEqual(run.render(self.receipt), run.render(run.build()))
        self.assertNotIn(b"\r", run.render(self.receipt))
        self.assertNotIn("timestamp", json.dumps(self.receipt).lower())
        self.assertEqual(self.receipt["authority_effect"], "None")

    def test_s2_2_misses_when_positive_candidates_are_all_inapplicable(self) -> None:
        readings = copy.deepcopy(self.receipt["readings"])
        for forest in readings.values():
            for node in forest["nodes"]:
                for row in node["candidate_rows"]:
                    if row["cost"] > 0:
                        row["valid"] = False
        self.assertEqual(run.score(readings)["S2-2"]["status"], "MISSED")
        self.assertEqual(self.receipt["scores"]["S2-2"]["status"], "HIT")


if __name__ == "__main__":
    unittest.main()
