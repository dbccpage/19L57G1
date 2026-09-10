"""Unit tests for Target G015 / G017 Autonomous Stepping & Demand Dynamics."""

from __future__ import annotations

from fractions import Fraction
import pytest

try:
    from research.g015_autonomous_stepping.stepping import (
        CarrierState,
        Demand,
        DemandStatus,
        StepOutcome,
        run_to_saturation,
        select_first_demand,
        step_autonomous,
    )
except ModuleNotFoundError:
    from stepping import (
        CarrierState,
        Demand,
        DemandStatus,
        StepOutcome,
        run_to_saturation,
        select_first_demand,
        step_autonomous,
    )


def test_first_demand_selection_priority_and_tie_breaking() -> None:
    d1 = Demand(1, "WRITE", priority=10, target_locus="l1", payload=100, remaining_budget=0, status=DemandStatus.PENDING)
    d2 = Demand(2, "WRITE", priority=5, target_locus="l2", payload=200, remaining_budget=0, status=DemandStatus.PENDING)
    d3 = Demand(3, "WRITE", priority=5, target_locus="l3", payload=300, remaining_budget=0, status=DemandStatus.PENDING)

    # d2 and d3 have highest priority (5 < 10); d2 has smaller demand_id (2 < 3)
    state = CarrierState.create_initial({"l1": 0, "l2": 0, "l3": 0}, [d1, d2, d3])
    assert select_first_demand(state) == 2

    # After discharging d2, d3 is chosen next
    discharged_d2 = Demand(2, "WRITE", priority=5, target_locus="l2", payload=200, remaining_budget=0, status=DemandStatus.DISCHARGED)
    state2 = CarrierState.create_initial({"l1": 0, "l2": 0, "l3": 0}, [d1, discharged_d2, d3])
    assert select_first_demand(state2) == 3


def test_autonomous_step_write_and_quiescence() -> None:
    d1 = Demand(10, "WRITE", priority=1, target_locus="reg_a", payload=42, remaining_budget=0, status=DemandStatus.PENDING)
    state = CarrierState.create_initial({"reg_a": 0}, [d1])

    assert state.get_memory("reg_a") == 0
    assert state.step_count == 0
    assert state.resources_spent == Fraction(0, 1)

    outcome = step_autonomous(state)
    assert outcome.status == "TRANSITION"
    assert outcome.cost == Fraction(1, 1)
    new_s = outcome.state
    assert new_s.get_memory("reg_a") == 42
    assert new_s.step_count == 1
    assert new_s.resources_spent == Fraction(1, 1)

    # Second step should become quiescent
    outcome2 = step_autonomous(new_s)
    assert outcome2.status == "QUIESCENT"
    assert outcome2.cost == Fraction(0, 1)
    assert outcome2.state.step_count == 1


def test_inert_history_remains_quiescent() -> None:
    # An empty demand set is inert
    inert_state = CarrierState.create_initial({"reg_a": 10}, [])
    assert inert_state.is_inert is True

    outcome = step_autonomous(inert_state)
    assert outcome.status == "QUIESCENT"
    assert outcome.state == inert_state
    assert outcome.state.step_count == 0


def test_reopen_chain_and_finite_saturation() -> None:
    # A demand that reopens 3 times before discharging
    chain_d = Demand(1, "REOPEN_CHAIN", priority=1, target_locus="counter", payload=1, remaining_budget=3, status=DemandStatus.PENDING)
    state = CarrierState.create_initial({"counter": 0}, [chain_d])

    final_state, outcomes = run_to_saturation(state, max_steps=10)
    # Expected: 3 transitions, then 1 quiescent step
    assert len(outcomes) == 4
    assert [o.status for o in outcomes] == ["TRANSITION", "TRANSITION", "TRANSITION", "QUIESCENT"]
    assert final_state.step_count == 3
    assert final_state.resources_spent == Fraction(3, 1)
    assert final_state.get_memory("counter") == 3


def test_refusal_on_unknown_demand_kind() -> None:
    bad_d = Demand(99, "ILLEGAL_OP", priority=1, target_locus="l", payload=0, remaining_budget=0, status=DemandStatus.PENDING)
    state = CarrierState.create_initial({"l": 0}, [bad_d])

    outcome = step_autonomous(state)
    assert outcome.status == "REFUSAL"
    assert "Refusal" in outcome.message
    # State is not mutated on refusal
    assert outcome.state == state
    assert outcome.cost == Fraction(0, 1)
