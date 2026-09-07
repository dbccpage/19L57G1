from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest

import audit
from audit import AuditFailure, descendant_keys, evidence, replay_cuts, sample
from derivation.candidates import Bounds, NewInst, min_responses, response_valid_naive
from derivation.engine import READING_L
from derivation.export import tree_full_json, verify_full_export
from derivation.model import AdmissionError, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Impose, Supply, replay
from derivation.observe import separable


@pytest.fixture(scope="module")
def record() -> dict[str, Any]:
    return evidence()


def test_original_seven_round_run_and_full_export(record: dict[str, Any]) -> None:
    assert record["open_run"]["stats"]["max_depth"] == 7
    assert record["open_run"]["stats"]["expansions_with_ties"] == 1
    assert record["open_run"]["stats"]["by_status"]["completed"] == 3
    assert record["open_run"]["replay_cut_checks"] == 180
    assert all(verify_full_export(tree) for tree in record["trees"].values())


def test_closed_run_answers_request_then_stops(record: dict[str, Any]) -> None:
    assert record["closed_run"]["stats"]["max_depth"] == 1
    assert record["closed_run"]["stats"]["by_status"]["terminal_all_separated"] == 1
    assert separable(sample(supply=False).nodes[-1].regime, 0, 1)


def test_restart_matches_endpoints_edges_costs_and_classes(record: dict[str, Any]) -> None:
    assert record["restart"]["remaining_rounds"] == 5
    assert record["restart"]["descendant_classes"] == 10
    assert record["restart"]["same_transition_records"] is True


@pytest.mark.parametrize("field,value", [("orbits", 99), ("response_label", "changed"),
                                       ("round_no", 99), ("class_size", 99), ("cost", (88, 88))])
def test_restart_comparison_rejects_changed_edge_metadata(monkeypatch: Any, field: str, value: Any) -> None:
    original = sample(supply=True)
    real_build = audit.build_tree
    def changed(*args: Any, **kwargs: Any) -> Any:
        result = real_build(*args, **kwargs)
        setattr(result.edges[0], field, value)
        return result
    monkeypatch.setattr(audit, "build_tree", changed)
    with pytest.raises(AuditFailure, match="exported-record correspondence"):
        audit.restart_witness(original)


def test_restart_comparison_preserves_edge_multiplicity(monkeypatch: Any) -> None:
    original = sample(supply=True)
    real_build = audit.build_tree
    def duplicated(*args: Any, **kwargs: Any) -> Any:
        result = real_build(*args, **kwargs)
        result.edges.append(result.edges[0])
        return result
    monkeypatch.setattr(audit, "build_tree", duplicated)
    with pytest.raises(AuditFailure, match="exported-record correspondence"):
        audit.restart_witness(original)


def test_replay_composition_including_repeated_admissions() -> None:
    events = (Supply("a"), AdmitDatum("a"), AdmitDatum("a"), AdmitDatum("b"),
              AdmitForm(1), AdmitInst(0, (0,)), Impose(0, 1), AdmitRuleAll(0))
    endpoint = replay(events)
    for cut in range(len(events) + 1):
        assert replay(events[cut:], replay(events[:cut])) == endpoint


@pytest.mark.parametrize("bad", [AdmitForm(0), AdmitInst(2, (0,)), Impose(0, 5)])
def test_restarted_refusal_matches_whole_history(bad: Any) -> None:
    prefix = (AdmitDatum("a"), AdmitDatum("b"))
    for cut in range(len(prefix) + 1):
        with pytest.raises(AdmissionError) as whole:
            replay(prefix + (bad,))
        with pytest.raises(AdmissionError) as restarted:
            replay(prefix[cut:] + (bad,), replay(prefix[:cut]))
        assert str(whole.value) == str(restarted.value)


def test_standing_requirements_are_not_discardable() -> None:
    history = (AdmitDatum("a"), AdmitDatum("b"), AdmitDatum("c"),
               AdmitForm(1), AdmitInst(0, (0,)), Impose(0, 1))
    base = replay(history)
    delta = (NewInst(0, (1,)),)
    # The proposed mark separates the new target but destroys the old one.
    after = replay((AdmitInst(0, (1,)),), base)
    assert separable(after, 1, 2)
    assert not separable(after, 0, 1)
    assert not response_valid_naive(base, (1, 2), delta)
    forgotten = replay(history[:-1])
    assert response_valid_naive(forgotten, (1, 2), delta)


@pytest.mark.parametrize("index,raw,classes", [(0, 6, 3), (1, 2, 1), (2, 10, 5), (3, 2, 1)])
def test_all_tied_classes_are_retained(record: dict[str, Any], index: int, raw: int, classes: int) -> None:
    row = record["branch_widths"][index]
    assert row["raw_minima"] == raw
    assert row["result_classes"] == classes


def test_bounded_absence_is_not_global_impossibility() -> None:
    base = replay(READING_L.genesis)
    assert min_responses(base, (0, 1), "mu2", Bounds(1, 2)) is None
    assert min_responses(base, (0, 1), "mu2", Bounds(2, 2)) is not None


def test_phase_reset_does_not_resume_queue(record: dict[str, Any]) -> None:
    assert record["phase_reset"]["original_moves"] == ["supply"]
    assert record["phase_reset"]["restarted_moves"] == ["separate(0, 1)"]
    assert record["phase_reset"]["restart_stats"]["nodes"] == 1


def test_root_request_does_not_supply_all_closure_orbits(record: dict[str, Any]) -> None:
    assert len(record["multiple_challenges"]["closure_targets"]) == 2
    assert len(record["multiple_challenges"]["fresh_root_moves"]) == 1


def test_generated_names_need_freshness_beyond_structural_identity(record: dict[str, Any]) -> None:
    collision = record["name_collisions"]
    assert collision["same_initial_key"] is True
    assert collision["after_new_datum_counts"] == [2, 3]
    assert collision["same_final_key"] is False
    assert collision["supply_self_merge"] == [1, 1]


def test_valid_state_can_be_outside_engine_domain(record: dict[str, Any]) -> None:
    assert "rule-free base" in record["domain_limits"]["rule_base_refusal"]
    assert "362880" in record["domain_limits"]["permutation_budget_refusal_at_zero_rounds"]
    assert record["domain_limits"]["guard_one_stats"]["nodes"] == 4


def test_full_state_transport_includes_requirements(record: dict[str, Any]) -> None:
    transport = record["full_state_transport"]
    assert transport["source_requirements"] == [(0, 1)]
    assert transport["image_requirements"] == [(0, 2)]
    assert transport["same_result_classes"] == 1


def test_tampered_export_and_missing_creation_edge_fail(record: dict[str, Any]) -> None:
    tree = deepcopy(record["trees"]["open"])
    tree["nodes"][1]["regime_sha256"] = "0" * 64
    assert not verify_full_export(tree)
    tree = deepcopy(record["trees"]["open"])
    tree["edges"] = tree["edges"][1:]
    assert not verify_full_export(tree)


def test_cut_checker_rejects_corrupt_node_history() -> None:
    tree = sample(supply=True)
    tree.nodes[1].history = ()
    with pytest.raises((AuditFailure, AdmissionError)):
        replay_cuts(tree)


def test_unknown_descendant_root_is_refused() -> None:
    with pytest.raises(ValueError, match="unknown start node"):
        descendant_keys(sample(supply=False), -1)


def test_open_claims_are_not_promoted_by_finite_examples(record: dict[str, Any]) -> None:
    assert record["universal_python_refinement"] == "NOT_PROVED"
    assert record["arbitrary_problem_encoding"] == "OPEN"
    assert record["automatic_representation_or_carrier_repair"] == "NOT_ESTABLISHED"
    assert record["undecidability"] == "NOT_PROVED"
