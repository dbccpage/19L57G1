"""Direct, dependency-free checks for the grammar-fit packet."""

from __future__ import annotations

import hashlib
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import grammar_fit


def _receipt() -> dict:
    return grammar_fit.build_receipt()


def test_prompt_and_read_only_input_are_pinned() -> None:
    assert hashlib.sha256(grammar_fit.PROMPT_PATH.read_bytes()).hexdigest() == grammar_fit.PROMPT_SHA256
    assert hashlib.sha256(grammar_fit.PRICED_RECEIPT_PATH.read_bytes()).hexdigest() == grammar_fit.PRICED_RECEIPT_SHA256
    assert b"\r" not in grammar_fit.PROMPT_PATH.read_bytes()
    assert b"\r" not in grammar_fit.PRICED_RECEIPT_PATH.read_bytes()


def test_three_objects_are_seated_without_smuggling_fields() -> None:
    receipt = _receipt()
    objects = receipt["objects"]
    assert set(objects) == {"collision", "equal_profiles", "directional_residual"}
    assert all(item["seated"] for item in objects.values())
    assert objects["collision"]["fields_outside_grammar_state"] == [
        "asserted_pair",
        "identifying_map",
        "pushed_edges",
    ]
    assert objects["equal_profiles"]["fields_outside_grammar_state"] == [
        "contexts",
        "equal_pair",
        "profiles",
    ]
    assert objects["directional_residual"]["fields_outside_grammar_state"] == [
        "left_presentation",
        "residual_pair",
        "right_presentation",
    ]


def test_event_columns_keep_external_and_noop_separate() -> None:
    event_fit = _receipt()["event_fit"]
    search = event_fit["search"]
    assert event_fit["not_used_as_passage"] == {
        "names": ["refineCol", "addCol"],
        "status": "REFUSED",
        "reason": "Those names are not reconstructed or upgraded here; no-op labels are not passage constructors.",
    }
    assert all(not report["object_derived_state_change"] for report in search.values())
    assert all(not report["guarded_response"] for report in search.values())
    assert all(not report["next_event_found"] for report in search.values())
    assert all(report["external_challenge_found"] for report in search.values())
    assert search["collision"]["object_derived_noop_label"] == []
    assert search["equal_profiles"]["object_derived_noop_label"][0]["source_field"] == "contexts"
    assert [item["source_field"] for item in search["directional_residual"]["object_derived_noop_label"]] == [
        "left_presentation",
        "right_presentation",
    ]
    assert all(
        item["event"]["kind"] == "Impose"
        for report in search.values()
        for item in report["external_challenge"]
    )
    assert _receipt()["event_fit"]["external_challenges_do_not_set_next_event_found"]
    assert _receipt()["event_fit"]["no_op_labels_do_not_set_next_event_found"]


def test_observe_replays_as_a_state_noop() -> None:
    search = _receipt()["event_fit"]["search"]
    for report in search.values():
        assert all(check["state_unchanged"] for check in report["no_op_replay_checks"])


def test_nontrivial_profile_case_is_built() -> None:
    case = _receipt()["profile_case"]
    assert case["terminal"] == "PROFILE_CASE_BUILT"
    assert case["equal_profiles"] is False
    assert case["internally_separable"] is True
    assert case["instance_holds"] == [True, False]
    assert case["profile_rows_computed_from_state"] is True
    assert case["grammar_state"]["instances"] == [[0, [0]]]
    assert case["empty_profile_falsifier"]["empty_profiles_are_not_the_built_case"]


def test_comparison_policy_is_explicitly_excluded() -> None:
    comparison = _receipt()["comparison"]
    assert comparison["terminal"] == "COMPARISON_EXCLUDED"
    assert comparison["status"] == "DECLARED_POLICY"
    assert comparison["policy"] is None
    assert comparison["constructor_spends_atom"] is None
    assert "OPEN" in comparison["residual_leftover"]


def test_one_measure_orientation_and_ties_are_retained() -> None:
    receipt = _receipt()
    measure = receipt["measure"]
    orientation = receipt["orientation"]
    assert measure["name"] == "mu_fit_oriented_s9"
    assert measure["only_measure"] is True
    assert measure["old_measure_reused"] is False
    assert measure["candidate_cost"] == 8
    assert orientation["terminal"] == "ORIENTATION_PRICED"
    assert orientation["forward_reverse_keys_differ"] is True
    assert orientation["iso_key_preserves_ordered_pair"] is True
    assert orientation["ties_retained"] is True
    assert orientation["tie_class_count"] >= 2


def test_s9_supply_bridge_leaves_all_six_lines_unpaid() -> None:
    s9 = _receipt()["s9_bridge"]
    assert s9["terminal"] == "S9_BRIDGE_PRICED"
    assert s9["supply_is_not_admission"] is True
    assert s9["replayed_state"]["data"] == []
    assert len(s9["lines"]) == 6
    assert s9["all_unpaid"] is True
    assert all(not line["paid"] for line in s9["lines"])


def test_opens_and_refusals_remain_open() -> None:
    receipt = _receipt()
    opens = receipt["open_boundaries"]
    assert opens["OB-1"] == "OPEN"
    assert opens["S6_item_6"] == "OPEN"
    assert opens["S9_last_bullet"] == "OPEN"
    assert opens["comparison_policy"].startswith("OPEN")
    assert all(item["status"] == "REFUSED" for item in receipt["refusals"])
    assert "REFUSED" in receipt["terminals"]
    histories = [
        event
        for item in receipt["objects"].values()
        for event in item["history"]
    ]
    assert all(event["kind"] != "two_rule" for event in histories)


def test_table_and_clock_closures_are_not_reported() -> None:
    payload = str(_receipt())
    assert "tick_analysis" not in payload
    assert "machine_check" not in payload
    assert "TICK_" not in payload
    assert "OBJECT_LANGUAGE_GENERATOR" not in payload
    assert "NEXT_EVENT_FOUND" not in _receipt()["terminals"]


def test_receipt_replay_is_byte_identical() -> None:
    committed = (grammar_fit.ROOT / "receipts" / "grammar_fit.json").read_bytes()
    with tempfile.TemporaryDirectory() as directory:
        first = grammar_fit.write_receipt(Path(directory) / "first.json").read_bytes()
        second = grammar_fit.write_receipt(Path(directory) / "second.json").read_bytes()
    assert first == second == committed
