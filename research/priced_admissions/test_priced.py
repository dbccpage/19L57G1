"""Deterministic and adversarial tests for the priced-admissions run."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from priced import (  # noqa: E402
    LEGAL_TERMINALS,
    PROMPT_SHA256,
    build_collision,
    build_directional_residual,
    build_equal_profiles,
    build_receipt,
    canonical_key,
    orientation_report,
    prompt_hash,
    receipt_bytes,
    s9_bill_report,
    write_receipt,
)


def test_prompt_is_pinned_and_lf_only() -> None:
    prompt_path = HERE / "PROMPT.md"
    raw = prompt_path.read_bytes()
    assert prompt_hash() == PROMPT_SHA256
    assert b"\r\n" not in raw
    assert len(raw) == 8852


def test_three_objects_are_concrete_data() -> None:
    collision = build_collision()
    profiles = build_equal_profiles()
    residual = build_directional_residual()
    assert collision.carrier == (0, 1)
    assert collision.edges == ((0, 1),)
    assert collision.identifying_map == (0, 0)
    assert collision.pushed_edges == ((0, 0),)
    assert collision.law_before is True
    assert collision.law_after is False
    assert profiles.contexts
    assert profiles.profiles == ((), ())
    assert profiles.profiles[0] == profiles.profiles[1]
    assert residual.left_presentation == (0, 0)
    assert residual.right_presentation == (0, 1)
    assert residual.left_presentation[0] == residual.left_presentation[1]
    assert residual.right_presentation[0] != residual.right_presentation[1]
    assert residual.left_image != residual.right_image


def test_event_search_uses_constructed_objects_not_a_requirements_table() -> None:
    receipt = build_receipt()
    encoded = json.dumps(receipt, sort_keys=True)
    assert "TICK_REQUIREMENTS" not in encoded
    assert "machine_check" not in encoded
    searches = receipt["event_grammar"]["search"]
    assert set(searches) == {"collision", "equal_profiles", "directional_residual"}
    for report in searches.values():
        assert report["next_event_found"] is True
        assert report["external_challenge_found"] is True
        assert report["guarded_response_found"] is False
        assert report["endogenous_successor_found"] is False
        assert report["missing_admissions_for_guarded_response"]
    assert searches["equal_profiles"]["constructed_observation_events"]
    assert searches["directional_residual"]["constructed_observation_events"]


def test_orientation_is_an_atom_and_order_is_not_forgotten() -> None:
    report = orientation_report()
    assert report["policy"] == "ORIENTATION_INCLUDED_AND_PRICED"
    assert report["atom_cost"] == 1
    assert report["iso_key_preserves_ordered_pair"] is True
    assert report["forward_reverse_keys_differ"] is True
    assert report["orientation_price"] == 1
    priced = report["minimum_with_orientation"]
    assert priced["minimum_cost"] == 8
    assert priced["minimum_isomorphism_class_count"] == 2
    assert priced["non_unique_first_answer"] is True
    assert report["ties_retained"] is True
    assert all(
        row["candidate"]["orientation_admitted"]
        for row in priced["representatives"]
    )


def test_s9_bill_replays_supply_without_admission() -> None:
    report = s9_bill_report()
    assert report["history"] == [{"kind": "Supply", "token": "<>"}]
    assert report["replayed_state"]["data"] == []
    assert report["supply_is_not_admission"] is True
    assert len(report["lines"]) == 6
    assert report["lines"][1]["required"] == ["left occurrence", "right occurrence"]
    assert report["all_unpaid"] is True
    assert report["paid_lines"] == []


def test_forbidden_closures_and_genesis_two_rule_are_negative() -> None:
    receipt = build_receipt()
    assert set(receipt["terminals"]).issubset(set(LEGAL_TERMINALS))
    assert "NO_FORCED_DYNAMICAL_LAW" not in receipt["terminals"]
    assert receipt["open_boundaries"]["OB-1"] == "OPEN"
    assert receipt["open_boundaries"]["S6_item_6"] == "OPEN"
    assert receipt["open_boundaries"]["S9_last_bullet"] == "OPEN"
    assert all(
        item["rule"] in {"FW-DYNAMICS", "FW-OB1", "FW-TABLE"}
        for item in receipt["refusals"]
    )
    assert receipt["s9_bill"]["history"] == [{"kind": "Supply", "token": "<>"}]
    assert all(event["kind"] != "two_rule" for event in receipt["s9_bill"]["history"])


def test_table_claimed_as_computation_is_rejected() -> None:
    receipt = build_receipt()
    assert receipt["objects_are_concrete_data"] is True
    for object_payload in receipt["objects"].values():
        assert isinstance(object_payload["carrier"], list)
        assert object_payload["carrier"]
        assert "absent" in object_payload
    assert "requirements_table" not in receipt
    assert "TICK_BASELINE" not in json.dumps(receipt, sort_keys=True)


def test_law_violation_rows_are_computed_in_named_finite_space() -> None:
    rows = build_receipt()["law_lattice"]["rows"]
    assert rows["irreflexive"]["identifying_witnessed_pair_can_violate"] is True
    assert rows["asymmetric"]["identifying_witnessed_pair_can_violate"] is True
    assert rows["symmetric"]["identifying_witnessed_pair_can_violate"] is False
    assert rows["transitive"]["identifying_witnessed_pair_can_violate"] is True
    assert build_receipt()["law_lattice"]["uncompared_laws_remain_open"] is True


def test_receipt_replay_is_byte_identical() -> None:
    committed = HERE / "receipts" / "priced_admissions.json"
    assert committed.exists()
    expected = receipt_bytes(build_receipt())
    with tempfile.TemporaryDirectory() as scratch:
        fresh = Path(scratch) / "priced_admissions.json"
        write_receipt(fresh)
        assert fresh.read_bytes() == expected
    assert committed.read_bytes() == expected
    assert b"\r\n" not in expected


@pytest.mark.parametrize("bad_terminal", ["OB1_CLOSED", "S66_CLOSED", "S9_LAST_CLOSED"])
def test_unknown_closure_terminal_is_not_legal(bad_terminal: str) -> None:
    assert bad_terminal not in LEGAL_TERMINALS
