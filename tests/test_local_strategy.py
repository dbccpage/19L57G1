"""Tests for the executable local finite-alphabet strategy mirror."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from derivation.local_strategy import (
    BARE,
    DEFAULT_MAX_CHAIN,
    DEPTH_TWO,
    PER_PAIR,
    PRESENCE,
    STRATEGIES,
    VALUED,
    ImportDiscipline,
    LocalStrategy,
    artifact_payload,
    ball,
    capacity_collision,
    capacity_threshold,
    classification,
    clears_within,
    encode,
    finite_declaration_within,
    finite_factor_table,
    fires_within,
    identity_grade_within,
    profile_code,
)

import run_local_strategy


def test_ball_and_encoding_match_lean_conventions() -> None:
    assert ball(4, 1) == (3, 4, 5)
    assert ball(0, 1) == (0, 1, 2)
    assert encode(8, (1, 2, 3)) == 1 + 8 * 2 + 64 * 3
    assert profile_code((True, True, True)) == 7


def test_invalid_natural_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        ball(-1, 0)
    with pytest.raises(ValueError):
        ball(0, -1)
    with pytest.raises(ValueError):
        encode(-1, ())
    with pytest.raises(ValueError):
        encode(2, (-1,))
    with pytest.raises(ValueError):
        LocalStrategy("bad", -1, ImportDiscipline.ONE_TIME, 1, lambda n, i: 0,
                      lambda values: values[0])
    with pytest.raises(ValueError):
        LocalStrategy("bad", 0, ImportDiscipline.ONE_TIME, 0, lambda n, i: 0,
                      lambda values: values[0])


def test_five_strategies_have_the_declared_classification() -> None:
    assert len(STRATEGIES) == 5
    table = {s.name: classification(s, DEFAULT_MAX_CHAIN) for s in STRATEGIES}
    assert table == {
        "none": "fires_unrepaired",
        "per_pair_fresh_mark": "repairs_by_recurring_imports",
        "automark_presence": "fires_unrepaired",
        "automark_valued": "generation_dead",
        "depth2": "fires_unrepaired",
    }
    assert BARE.view(4, 2) == PRESENCE.view(4, 2)


def test_finite_local_members_have_capacity_collisions() -> None:
    assert capacity_threshold(BARE) == 10
    assert capacity_threshold(PRESENCE) == 10
    assert capacity_threshold(DEPTH_TWO) == 516
    for strategy in (BARE, PRESENCE, DEPTH_TWO):
        pair = capacity_collision(strategy)
        assert pair is not None
        i, j = pair
        n = capacity_threshold(strategy)
        assert n is not None
        assert strategy.radius < i < j
        assert i + strategy.radius < n
        assert j + strategy.radius < n
        assert strategy.view(n, i) == strategy.view(n, j)
        assert finite_declaration_within(strategy, DEFAULT_MAX_CHAIN)
    assert capacity_threshold(PER_PAIR) is None
    assert capacity_collision(VALUED) is None


def test_identity_and_import_boundaries_are_nonvacuous() -> None:
    assert not identity_grade_within(BARE, DEFAULT_MAX_CHAIN)
    assert identity_grade_within(PER_PAIR, DEFAULT_MAX_CHAIN)
    assert identity_grade_within(VALUED, DEFAULT_MAX_CHAIN)
    assert PER_PAIR.import_discipline is ImportDiscipline.RECURRING
    assert VALUED.import_discipline is ImportDiscipline.ONE_TIME
    assert not finite_declaration_within(PER_PAIR, DEFAULT_MAX_CHAIN)
    assert not finite_declaration_within(VALUED, DEFAULT_MAX_CHAIN)
    assert fires_within(VALUED, DEFAULT_MAX_CHAIN)
    assert clears_within(VALUED, DEFAULT_MAX_CHAIN)


def test_unconstrained_view_fails_locality_fiber_check() -> None:
    constant_colour = lambda _n, _i: 0
    index_view = lambda _n, i: i
    assert finite_factor_table(0, constant_colour, index_view, 3) is None
    assert finite_factor_table(
        BARE.radius, BARE.colour, BARE.view, DEFAULT_MAX_CHAIN
    ) is not None
    with pytest.raises(ValueError):
        finite_factor_table(-1, constant_colour, index_view, 3)
    with pytest.raises(ValueError):
        finite_factor_table(0, constant_colour, index_view, -1)


def test_bounds_and_empty_prefix_paths() -> None:
    for function in (
        fires_within,
        clears_within,
        identity_grade_within,
        finite_declaration_within,
    ):
        with pytest.raises(ValueError):
            function(BARE, -1)
    assert not fires_within(BARE, 2)
    assert clears_within(BARE, 2)
    constant = LocalStrategy(
        "constant",
        0,
        ImportDiscipline.ONE_TIME,
        1,
        lambda _n, _i: 0,
        lambda values: values[0],
    )
    assert classification(constant, 2) == "bounded_other"
    with pytest.raises(ValueError):
        artifact_payload(4)


def test_runner_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    assert run_local_strategy.main(["--artifacts", str(first)]) == 0
    assert run_local_strategy.main(["--artifacts", str(second)]) == 0
    left = first / "local_strategy.json"
    right = second / "local_strategy.json"
    assert left.read_bytes() == right.read_bytes()
    payload = json.loads(left.read_text(encoding="utf-8"))
    assert payload["terminals"] == {
        "g1": "G1_CLASS_EXCLUSION_PROVED",
        "object_language": "OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE",
        "closure_policy": "OB1_UNCHANGED",
    }
    assert not payload["negative_locality_probe"][
        "constant_colour_identity_view_accepted"
    ]
