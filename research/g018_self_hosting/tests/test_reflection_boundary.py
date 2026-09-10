"""Tests for reflection boundary, fuel exhaustion thresholds, and capacity limits."""

from __future__ import annotations

import pytest

from carrier_repr import MachineSpec, MachineState, Transition
from reflection_boundary import (
    compute_fuel_required,
    find_pigeonhole_collision,
    max_reflection_depth,
    run_reflection_tower,
)


@pytest.fixture
def finite_work_spec() -> MachineSpec:
    """A machine that performs 3 discrete steps and halts."""
    transitions = (
        Transition(0, 0, 1, 1, 1, False),
        Transition(1, 0, 2, 2, 1, False),
        Transition(2, 0, 3, 3, 0, True),
    )
    return MachineSpec(transitions=transitions, default_sym=0)


def test_fuel_required_calculation() -> None:
    # Base 3 steps
    # Depth 0: 3
    assert compute_fuel_required(0, 3, overhead_per_step=1, layer_overhead=1) == 3
    # Depth 1: 3 * 1 + 1 = 4
    assert compute_fuel_required(1, 3, overhead_per_step=1, layer_overhead=1) == 4
    # Depth 2: 4 * 1 + 1 = 5
    assert compute_fuel_required(2, 3, overhead_per_step=1, layer_overhead=1) == 5
    # With overhead multiplier 2:
    # Depth 1: 3 * 2 + 1 = 7
    # Depth 2: 7 * 2 + 1 = 15
    assert compute_fuel_required(2, 3, overhead_per_step=2, layer_overhead=1) == 15


def test_max_reflection_depth() -> None:
    # Available fuel 14 with base 3 steps and 2x overhead:
    # depth 1 needs 7 <= 14
    # depth 2 needs 15 > 14 -> max depth is 1
    assert max_reflection_depth(14, base_steps=3, overhead_per_step=2, layer_overhead=1) == 1
    assert max_reflection_depth(15, base_steps=3, overhead_per_step=2, layer_overhead=1) == 2


def test_reflection_tower_sufficient_fuel(finite_work_spec: MachineSpec) -> None:
    spec = finite_work_spec
    state = MachineState(state=0, cursor=0, tape=(0, 0), fuel=3, halted=False)

    # Required host fuel is 3, allocate 10
    result = run_reflection_tower(depth=1, spec=spec, state=state, host_fuel=10)

    assert not result.fuel_exhausted
    assert result.completed_base_steps == 3
    assert result.final_guest_state.halted
    assert result.final_guest_state.tape == (1, 2, 3)
    assert result.host_fuel_remaining == 7


def test_reflection_tower_fuel_exhaustion(finite_work_spec: MachineSpec) -> None:
    spec = finite_work_spec
    state = MachineState(state=0, cursor=0, tape=(0, 0), fuel=3, halted=False)

    # Allocate only 2 host fuel (requires 3 steps)
    result = run_reflection_tower(depth=1, spec=spec, state=state, host_fuel=2)

    assert result.fuel_exhausted
    assert result.completed_base_steps == 2
    assert not result.final_guest_state.halted
    assert result.host_fuel_remaining == 0


def test_state_capacity_pigeonhole_collision() -> None:
    # Domain size 5 (states 0..4) into codomain size 4 (carrier slots 0..3)
    # Mapping: s -> s % 4
    witness = find_pigeonhole_collision(
        domain_size=5,
        codomain_size=4,
        encoding_fn=lambda s: s % 4,
    )
    assert witness is not None
    assert witness.state_1 != witness.state_2
    assert (witness.state_1 % 4) == (witness.state_2 % 4)
    assert witness.mapped_carrier_index == 0
    assert witness.state_1 == 0
    assert witness.state_2 == 4


def test_state_capacity_no_collision_when_sufficient() -> None:
    # Domain size 4 into codomain size 4
    witness = find_pigeonhole_collision(
        domain_size=4,
        codomain_size=4,
        encoding_fn=lambda s: s,
    )
    assert witness is None
