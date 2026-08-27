"""Dependency-free checks for the admit-leftover packet."""

from __future__ import annotations

import hashlib
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import admit_leftover


def _receipt() -> dict:
    return admit_leftover.build_receipt()


def test_prompt_and_grammar_fit_input_are_pinned() -> None:
    assert hashlib.sha256(admit_leftover.PROMPT_PATH.read_bytes()).hexdigest() == admit_leftover.PROMPT_SHA256
    assert hashlib.sha256(admit_leftover.GRAMMAR_FIT_RECEIPT_PATH.read_bytes()).hexdigest() == admit_leftover.GRAMMAR_FIT_RECEIPT_SHA256
    assert b"\r" not in admit_leftover.PROMPT_PATH.read_bytes()
    assert b"\r" not in admit_leftover.GRAMMAR_FIT_RECEIPT_PATH.read_bytes()


def test_collision_leftover_is_admitted_without_map_smuggling() -> None:
    choice = _receipt()["admission_choice"]
    assert choice["admitted"] is True
    assert choice["constructor"] == {"kind": "assertWit", "pair": [0, 1]}
    assert choice["state_after"]["asserted"] == [[0, 1]]
    assert choice["identifying_map_in_state"] is False
    assert choice["identifying_map_leftover"]
    line = next(row for row in _receipt()["admission_bill"]["lines"] if row["field"] == "asserted_pair")
    assert line["paid"] is True and line["atom_cost"] == 1


def test_profile_rows_are_computed_from_admitted_state() -> None:
    receipt = _receipt()
    case = receipt["profile_case"]
    rebuilt = admit_leftover.profile_case_from_input(admit_leftover.load_grammar_fit())
    assert case["profiles_computed_from_state"] == rebuilt["profiles_computed_from_state"]
    assert case["input_rows_match_computation"] is True
    assert case["profiles_computed_from_state"] == [[[0, [None]]], []]
    assert case["instance_holds"] == [True, False]


def test_search_columns_keep_noop_external_and_conditional_separate() -> None:
    searches = _receipt()["search_after_each_choice"]
    assert all(not report["object_derived_state_change"] for report in searches.values())
    assert all(not report["state_change_found"] for report in searches.values())
    assert all(report["external_challenge"][0]["applied_to_state"] is False for report in searches.values())
    assert all(report["external_challenge"][0]["event"]["kind"] == "Impose" for report in searches.values())
    assert searches["collision"]["guarded_response"][0]["status"] == "CONDITIONAL"
    assert searches["collision"]["guarded_response"][0]["fires_in_current_state"] is False
    assert searches["equal_profiles"]["label_only"] is True
    assert searches["directional_residual"]["label_only"] is True
    assert all(
        check["state_unchanged"]
        for report in searches.values()
        for label in report["object_derived_noop_label"]
        for check in [label]
    )


def test_each_extra_field_is_paid_conditional_or_explicitly_outside() -> None:
    bill = _receipt()["admission_bill"]
    assert bill["measure_name"] == "mu_leftover_admission"
    assert bill["chosen_total"] == 1
    assert bill["no_free_store_admissions"] is True
    assert bill["minimum_claim"] is False
    allowed = {"ADMITTED", "CONDITIONAL", "DECLARED_POLICY", "LEFT_OUTSIDE"}
    assert all(row["status"] in allowed for row in bill["lines"])
    comparison = _receipt()["comparison"]
    assert comparison["terminal"] == "COMPARISON_EXCLUDED"
    assert comparison["constructor"] is None


def test_orientation_and_ties_are_inherited_without_forgetting_order() -> None:
    orientation = _receipt()["orientation"]
    assert orientation["terminal"] == "ORIENTATION_PRICED"
    assert orientation["inherited_read_only"] is True
    assert orientation["forward_reverse_keys_differ"] is True
    assert orientation["iso_key_preserves_ordered_pair"] is True
    assert orientation["ties_retained"] is True
    assert orientation["tie_class_count"] >= 2


def test_supply_bridge_stays_separate_from_extra_admission() -> None:
    bridge = _receipt()["s9_bridge"]
    assert bridge["terminal"] == "S9_BRIDGE_PRICED"
    assert bridge["history"] == [{"kind": "Supply", "token": "<>"}]
    assert bridge["replayed_state"]["data"] == []
    assert bridge["extra_admission_not_in_supply_history"] is True
    assert len(bridge["lines"]) == 6
    assert bridge["all_unpaid"] is True


def test_opens_refusals_and_distinctions_remain_explicit() -> None:
    receipt = _receipt()
    opens = receipt["open_boundaries"]
    assert opens["OB-1"] == "OPEN"
    assert opens["S6_item_6"] == "OPEN"
    assert opens["S9_last_bullet"] == "OPEN"
    assert opens["identifying_map"].startswith("OPEN")
    assert opens["guarded_family"].endswith("unfired")
    assert all(item["status"] == "REFUSED" for item in receipt["refusals"])
    assert "two_rule" not in str(receipt["admission_choice"]["history_after"])
    assert receipt["distinctions"]["difference"].startswith("Primitive Difference")


def test_forbidden_table_reference_and_pytest_import_are_absent() -> None:
    receipt_text = str(_receipt())
    assert "tick_analysis" not in receipt_text
    assert "machine_check" not in receipt_text
    assert "TICK_" not in receipt_text
    assert "OBJECT_LANGUAGE_GENERATOR" not in receipt_text
    assert "import pytest" not in (HERE / "admit_leftover.py").read_text(encoding="utf-8")
    assert "STATE_CHANGE_FOUND" not in _receipt()["terminals"]


def test_receipt_replays_byte_identically() -> None:
    committed = (HERE / "receipts" / "admit_leftover.json").read_bytes()
    with tempfile.TemporaryDirectory() as directory:
        first = admit_leftover.write_receipt(Path(directory) / "first.json").read_bytes()
        second = admit_leftover.write_receipt(Path(directory) / "second.json").read_bytes()
    assert first == second == committed
    assert b"\r" not in committed


if __name__ == "__main__":
    import traceback

    failed = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_") or not callable(fn):
            continue
        try:
            fn()
            print(f"PASS {name}")
        except Exception as exc:
            failed += 1
            print(f"FAIL {name}: {exc}")
            traceback.print_exc()
    raise SystemExit(failed)
