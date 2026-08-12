"""Tests for the primitive-difference-interface mirror."""

from __future__ import annotations

import json
from pathlib import Path

from derivation.diff_interface import (
    ROUNDS,
    active_pairs,
    bool_grammar_report,
    bool_views,
    countermodel_report,
    cview,
    drive,
    fuel_report,
    measure,
    obstruction_active,
    swap_top,
    tower_next,
    tower_demand_support,
    tower_report,
    tower_round,
)

import run_diff_interface


def test_closed_stage_measure_zero() -> None:
    for n in range(ROUNDS):
        assert measure(n + 1, n) == 0
        assert active_pairs(n + 1, n) == []


def test_reflection_produces_active_obstruction() -> None:
    """The Lean pipeline theorem, in bounds: the stale observer sees
    the parent/new pair as zero, and the pre-closure measure is
    positive."""
    for n in range(ROUNDS):
        assert cview(n, n) == cview(n, n + 1)
        assert (n, n + 1) in active_pairs(n + 2, n)
        assert measure(n + 2, n) > 0


def test_demand_is_map_saturated_and_uniformly_bounded() -> None:
    for n in range(ROUNDS):
        support = tower_demand_support(n)
        assert support == sorted([(n, n + 1), (n + 1, n)])
        assert len(support) == 2  # the fixed uniform demand bound B = 2
        # The declared top-swap maps the demand support onto itself.
        assert {
            (swap_top(n, x), swap_top(n, y)) for (x, y) in support
        } == set(support)


def test_closure_discharges_preserves_and_decreases() -> None:
    rep = tower_report()
    assert rep["all_strictly_decrease"] is True
    assert rep["all_preserve_old"] is True
    assert rep["all_closed_before"] is True
    assert rep["all_obstruct_after_reflection"] is True
    assert rep["uniform_demand_bound"] == 2


def test_tower_round_shape() -> None:
    row = tower_round(3)
    assert row["reflected_pair"] == [3, 4]
    assert row["parent_new_zero_pre_closure"] is True
    assert row["preclose_measure"] == 2
    assert row["closed_measure_after"] == 0


def test_fuel_driver_terminates_closed() -> None:
    rep = fuel_report()
    assert rep["all_terminate_closed"] is True
    rows = rep["rows"]
    assert isinstance(rows, list)
    for row in rows:
        assert row["outcome"] == "closed"
        assert row["fuel"] == row["measure"] + 1


def test_fuel_driver_out_of_fuel_without_budget() -> None:
    outcome, _, proposal = drive(tower_next, 0, (5, 3))
    assert outcome == "out_of_fuel"
    assert proposal is None


def test_fuel_driver_preserves_proposal_payload() -> None:
    proposal = {"kind": "observerStructure", "demanded": [[0, 1]]}
    initial = (3, 0)
    outcome, state, returned = drive(
        lambda _: ("proposal", proposal), 1, initial
    )
    assert outcome == "proposal"
    assert state == initial
    assert returned is proposal


def test_no_bool_grammar_view_is_closed() -> None:
    assert len(bool_views()) == 8
    rep = bool_grammar_report()
    assert rep["views_checked"] == 8
    assert rep["every_view_obstructed"] is True
    assert rep["no_view_closed"] is True
    assert rep["available_proposal_kind"] == "observerStructure"


def test_countermodels_all_zero_all_unprotected_and_inactive() -> None:
    rep = countermodel_report()
    assert rep["all_zero_despite_feature"] is True
    assert rep["all_unprotected_and_inactive"] is True
    rows = rep["rows"]
    assert isinstance(rows, list)
    assert [r["feature"] for r in rows] == [
        "freshness", "tagging", "edge", "new_hash", "repetition",
    ]
    for row in rows:
        assert row["feature_present"] is True
        assert row["zero"] is True
        assert row["retained"] is True
        assert row["guarded"] is False
        assert row["active"] is False


def test_activity_is_exactly_the_three_way_conjunction() -> None:
    assert obstruction_active(retained=True, zero=True, guarded=True)
    assert not obstruction_active(retained=False, zero=True, guarded=True)
    assert not obstruction_active(retained=True, zero=False, guarded=True)
    assert not obstruction_active(retained=True, zero=True, guarded=False)


def test_run_main(tmp_path: Path) -> None:
    out = tmp_path / "artifacts"
    assert run_diff_interface.main(["--artifacts", str(out)]) == 0
    payload = json.loads(
        (out / "diff_interface.json").read_text(encoding="utf-8")
    )
    assert payload["tower"]["all_strictly_decrease"] is True
    assert payload["bool_grammar"]["no_view_closed"] is True
    assert payload["countermodels"]["all_zero_despite_feature"] is True
    out2 = tmp_path / "artifacts2"
    run_diff_interface.main(["--artifacts", str(out2)])
    assert (out / "diff_interface.json").read_bytes() == (
        out2 / "diff_interface.json"
    ).read_bytes()
