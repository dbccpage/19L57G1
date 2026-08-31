"""Tests for the nine-slot inventory of existing objects."""

from __future__ import annotations

import json
from pathlib import Path

import run_observer_inventory
from derivation.observer_inventory import (
    NAMED_ELSEWHERE,
    SLOTS,
    as_json,
    d0_report,
    delta_report,
    edge_count,
    inventory_report,
    irrefl_census_on_two,
    is_sym_bit,
    local_states,
    residuals_report,
    witnesses_report,
)
from derivation.primdiff import D2, D2_REV, S2


def test_nine_slots_and_no_duplicates() -> None:
    assert len(SLOTS) == 9
    assert len(set(SLOTS)) == 9
    assert SLOTS == (
        "K", "F", "R", "delta", "d0", "d1", "J", "M", "tau"
    )


def test_irrefl_census_is_exactly_the_four() -> None:
    states = local_states()
    assert states["empty"] == frozenset()
    assert states["D2"] == D2.rel
    assert states["D2rev"] == D2_REV.rel
    assert states["S2"] == S2.rel
    census = irrefl_census_on_two()
    assert census["count"] == 4
    assert census["are_exactly_the_four"] is True
    assert census["names"] == ["D2", "D2rev", "S2", "empty"]


def test_witnesses_are_data_not_a_unique_inhabitant() -> None:
    rep = witnesses_report()
    assert rep["zero_ne_one"] is True
    assert rep["one_forward"] is True
    assert rep["one_reverse"] is True
    assert rep["zero_presence_empty"] is True
    assert rep["one_presence_is_D2"] is True


def test_d0_transpose_and_swap_agree_on_D2_and_differ() -> None:
    rep = d0_report()
    assert all(rep[k] is True for k in rep)


def test_delta_collision_is_not_source_irreflexivity() -> None:
    rep = delta_report()
    assert rep["D2_collides_under_merge"] is True
    assert rep["S2_collides_under_merge"] is True
    assert rep["empty_does_not_collide_under_merge"] is True
    assert rep["unit_self_loop_not_irreflexive"] is True
    assert rep["source_D2_still_irreflexive"] is True


def test_residuals_are_not_unique() -> None:
    assert edge_count(D2.rel) == 1
    assert edge_count(S2.rel) == 2
    assert is_sym_bit(D2.rel) == 0
    assert is_sym_bit(S2.rel) == 1
    assert is_sym_bit(D2_REV.rel) == 0
    assert is_sym_bit(frozenset()) == 0
    rep = residuals_report()
    assert rep["edge_count_D2"] == 1
    assert rep["edge_count_S2"] == 2
    assert rep["is_sym_bit_D2"] == 0
    assert rep["is_sym_bit_S2"] == 1
    assert rep["residuals_disagree_on_D2"] is True


def test_named_elsewhere_is_a_string_table() -> None:
    assert "K" in NAMED_ELSEWHERE
    assert "W" in NAMED_ELSEWHERE
    for vals in NAMED_ELSEWHERE.values():
        assert vals
        assert all(isinstance(v, str) and v for v in vals)


def test_inventory_report_flags() -> None:
    payload = inventory_report()
    assert payload["slot_count"] == 9
    assert payload["empty_ne_D2"] is True
    assert payload["witnesses_not_derived_as_necessary"] is True
    bindings = payload["bindings"]
    assert isinstance(bindings, dict)
    assert set(bindings) == set(SLOTS)
    copied = as_json(payload)
    assert copied["slot_count"] == 9


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_observer_inventory.main(["--artifacts", str(d1)]) == 0
    assert run_observer_inventory.main(["--artifacts", str(d2)]) == 0
    p1 = d1 / "observer_inventory.json"
    p2 = d2 / "observer_inventory.json"
    assert p1.read_bytes() == p2.read_bytes()
    payload = json.loads(p1.read_text(encoding="utf-8"))
    assert payload["irrefl_census"]["are_exactly_the_four"] is True
    assert payload["d0"]["operations_differ_on_self_loop"] is True
    assert payload["witnesses"]["one_presence_is_D2"] is True
