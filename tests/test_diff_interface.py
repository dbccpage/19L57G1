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
    swap_top,
    tower_next,
    tower_orbit,
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
    the parent/fresh pair as zero, and the pre-closure measure is
    positive."""
    for n in range(ROUNDS):
        assert cview(n, n) == cview(n, n + 1)
        assert (n, n + 1) in active_pairs(n + 2, n)
        assert measure(n + 2, n) > 0


def test_orbit_is_complete_and_uniformly_bounded() -> None:
    for n in range(ROUNDS):
        orbit = tower_orbit(n)
        assert orbit == sorted([(n, n + 1), (n + 1, n)])
        assert len(orbit) == 2  # the fixed uniform bound B = 2
        # complete under the declared symmetries: swap maps the orbit
        # onto itself
        assert {
            (swap_top(n, x), swap_top(n, y)) for (x, y) in orbit
        } == set(orbit)


def test_closure_discharges_preserves_and_decreases() -> None:
    rep = tower_report()
    assert rep["all_strictly_decrease"] is True
    assert rep["all_preserve_old"] is True
    assert rep["all_closed_before"] is True
    assert rep["all_obstruct_after_reflection"] is True
    assert rep["uniform_orbit_bound"] == 2


def test_tower_round_shape() -> None:
    row = tower_round(3)
    assert row["reflected_pair"] == [3, 4]
    assert row["parent_fresh_zero_pre_closure"] is True
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
    outcome, _ = drive(tower_next, 0, (5, 3))
    assert outcome == "out_of_fuel"


def test_bool_grammar_forces_proposal() -> None:
    assert len(bool_views()) == 8
    rep = bool_grammar_report()
    assert rep["views_checked"] == 8
    assert rep["every_view_obstructed"] is True
    assert rep["proposal_required"] is True
    assert rep["proposal_kind"] == "observerStructure"


def test_countermodels_all_zero_none_active() -> None:
    rep = countermodel_report()
    assert rep["all_zero_despite_feature"] is True
    assert rep["none_active"] is True
    rows = rep["rows"]
    assert isinstance(rows, list)
    assert [r["feature"] for r in rows] == [
        "freshness", "tagging", "edge", "new_hash", "repetition",
    ]
    for row in rows:
        assert row["feature_present"] is True
        assert row["zero"] is True
        assert row["active_without_protection"] is False


def test_run_main(tmp_path: Path) -> None:
    out = tmp_path / "artifacts"
    assert run_diff_interface.main(["--artifacts", str(out)]) == 0
    payload = json.loads(
        (out / "diff_interface.json").read_text(encoding="utf-8")
    )
    assert payload["tower"]["all_strictly_decrease"] is True
    assert payload["bool_grammar"]["proposal_required"] is True
    assert payload["countermodels"]["all_zero_despite_feature"] is True
    out2 = tmp_path / "artifacts2"
    run_diff_interface.main(["--artifacts", str(out2)])
    assert (out / "diff_interface.json").read_bytes() == (
        out2 / "diff_interface.json"
    ).read_bytes()
