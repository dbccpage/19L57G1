"""Tests for internalized step simulator and simulation correctness."""

from __future__ import annotations

import pytest

from carrier_repr import (
    MachineSpec,
    MachineState,
    Transition,
    run_direct,
    step_direct,
)
from simulator import (
    MICRO_STEPS_PER_MACRO_STEP,
    micro_sim_embed,
    micro_step_k,
    run_internal,
    sim_embed,
    sim_extract,
    step_internal,
)


@pytest.fixture
def binary_inverter_spec() -> MachineSpec:
    """Inverts 0 to 1 and 1 to 0 across a 3-element tape then halts."""
    transitions = (
        # State 0: invert at cursor 0, move right to 1
        Transition(curr_state=0, read_sym=0, next_state=1, write_sym=1, move_cursor=1, halt=False),
        Transition(curr_state=0, read_sym=1, next_state=1, write_sym=0, move_cursor=1, halt=False),
        # State 1: invert at cursor 1, move right to 2
        Transition(curr_state=1, read_sym=0, next_state=2, write_sym=1, move_cursor=1, halt=False),
        Transition(curr_state=1, read_sym=1, next_state=2, write_sym=0, move_cursor=1, halt=False),
        # State 2: invert at cursor 2, stay, halt
        Transition(curr_state=2, read_sym=0, next_state=3, write_sym=1, move_cursor=0, halt=True),
        Transition(curr_state=2, read_sym=1, next_state=3, write_sym=0, move_cursor=0, halt=True),
    )
    return MachineSpec(transitions=transitions, default_sym=0)


def test_step_simulation_correctness_single_cycle(binary_inverter_spec: MachineSpec) -> None:
    """Verify Step_internal(Sim(S)) == Sim(step(S)) at every single step."""
    spec = binary_inverter_spec
    state = MachineState(state=0, cursor=0, tape=(1, 0, 1), fuel=10, halted=False)
    host_fuel = 50

    curr_direct = state
    curr_sim = sim_embed(spec, state, host_fuel)

    while not curr_direct.halted and curr_direct.fuel > 0:
        # Expected next state by direct operational transition
        next_direct = step_direct(spec, curr_direct)

        # Actual next state by internal simulator transition
        next_sim = step_internal(curr_sim)

        # Commutation: extracted state from next_sim must exactly match next_direct
        extracted_spec, extracted_state = sim_extract(next_sim)
        assert extracted_spec == spec
        assert extracted_state == next_direct

        # Direct step_embed matches next_sim
        expected_sim_state = sim_embed(spec, next_direct, curr_sim.simulator_fuel - 1)
        assert next_sim.guest_state == expected_sim_state.guest_state
        assert next_sim.simulator_fuel == expected_sim_state.simulator_fuel

        curr_direct = next_direct
        curr_sim = next_sim

    assert curr_direct.halted
    assert curr_direct.tape == (0, 1, 0)


def test_multi_step_simulation_equivalence(binary_inverter_spec: MachineSpec) -> None:
    """Verify run_internal(Sim(S)) yields exact final state of run_direct(S)."""
    spec = binary_inverter_spec
    state = MachineState(state=0, cursor=0, tape=(0, 0, 0), fuel=10, halted=False)

    final_direct = run_direct(spec, state)
    sim = sim_embed(spec, state, simulator_fuel=100)
    final_sim = run_internal(sim)

    ext_spec, ext_state = sim_extract(final_sim)
    assert ext_spec == spec
    assert ext_state == final_direct
    assert ext_state.tape == (1, 1, 1)
    assert ext_state.halted


def test_micro_step_simulation_k_steps(binary_inverter_spec: MachineSpec) -> None:
    """Verify Step_micro^k(Sim(S)) == Sim(step(S)) with k = 4 micro-steps."""
    spec = binary_inverter_spec
    state = MachineState(state=0, cursor=0, tape=(1, 1, 0), fuel=5, halted=False)

    # 1 macro-step directly
    direct_next = step_direct(spec, state)

    # 4 micro-steps internally
    micro_sim = micro_sim_embed(spec, state, simulator_fuel=20)
    micro_sim_4 = micro_step_k(micro_sim, MICRO_STEPS_PER_MACRO_STEP)

    assert micro_sim_4.guest_state == direct_next
    assert micro_sim_4.stage == 0
    assert micro_sim_4.macro_steps_completed == 1
    assert micro_sim_4.simulator_fuel == 20 - 4


def test_bidirectional_cursor_movement() -> None:
    """Verify simulation handles leftward and rightward tape cursor traversals."""
    # Write 5 at 0, move right; write 7 at 1, move left; halt at 0
    spec = MachineSpec(
        transitions=(
            Transition(curr_state=0, read_sym=0, next_state=1, write_sym=5, move_cursor=1, halt=False),
            Transition(curr_state=1, read_sym=0, next_state=2, write_sym=7, move_cursor=-1, halt=False),
            Transition(curr_state=2, read_sym=5, next_state=3, write_sym=9, move_cursor=0, halt=True),
        )
    )
    init_state = MachineState(state=0, cursor=0, tape=(0, 0), fuel=10, halted=False)
    sim = sim_embed(spec, init_state, simulator_fuel=20)

    final_sim = run_internal(sim)
    assert final_sim.guest_state.tape == (9, 7)
    assert final_sim.guest_state.cursor == 0
    assert final_sim.guest_state.halted
