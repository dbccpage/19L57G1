"""Tests for diagonal obstruction theorem and simulation sweeps."""

from __future__ import annotations

import pytest

from carrier_repr import MachineState, run_direct
from diagonal_obstruction import (
    build_diagonal_machine_for_prediction,
    evaluate_diagonal_obstruction,
    make_halting_machine,
    make_looping_machine,
    predictor_always_halt,
    predictor_never_halt,
    sweep_candidate_predictors,
)


def test_diagonal_machine_semantics() -> None:
    # Machine built for True prediction must NOT halt
    loop_spec = build_diagonal_machine_for_prediction(True)
    st_loop = MachineState(state=0, cursor=0, tape=(0,), fuel=10, halted=False)
    end_loop = run_direct(loop_spec, st_loop)
    assert not end_loop.halted
    assert end_loop.fuel == 0

    # Machine built for False prediction MUST halt
    halt_spec = build_diagonal_machine_for_prediction(False)
    st_halt = MachineState(state=0, cursor=0, tape=(0,), fuel=10, halted=False)
    end_halt = run_direct(halt_spec, st_halt)
    assert end_halt.halted
    assert end_halt.fuel == 9


def test_refute_always_halt_oracle() -> None:
    ref = evaluate_diagonal_obstruction("AlwaysHaltOracle", predictor_always_halt, fuel_budget=20)
    assert ref.refutation_success
    assert ref.predicted_halt is True
    assert ref.actual_halt is False


def test_refute_never_halt_oracle() -> None:
    ref = evaluate_diagonal_obstruction("NeverHaltOracle", predictor_never_halt, fuel_budget=20)
    assert ref.refutation_success
    assert ref.predicted_halt is False
    assert ref.actual_halt is True


def test_comprehensive_predictor_sweep() -> None:
    results = sweep_candidate_predictors(fuel_budget=30)
    assert len(results) >= 7
    for ref in results:
        assert ref.refutation_success, f"Failed to refute predictor {ref.predictor_name}"
        assert ref.predicted_halt != ref.actual_halt
