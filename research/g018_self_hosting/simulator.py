"""Internalized step-simulator executing within the object carrier.

Tracks the object process step by step with ZERO external host oracles
or metatheoretic loop counters.

Simulation correctness theorem:
    Step_internal^k(Sim(S)) = Sim(step(S))

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from carrier_repr import (
    CarrierEncodingError,
    MachineSpec,
    MachineState,
    step_direct,
)


@dataclass(frozen=True)
class SimState:
    """Internalized simulator configuration represented in the carrier."""

    guest_spec: MachineSpec
    guest_state: MachineState
    simulator_fuel: int
    step_count: int = 0

    def __post_init__(self) -> None:
        if self.simulator_fuel < 0:
            raise CarrierEncodingError(f"simulator_fuel must be non-negative: {self.simulator_fuel}")
        if self.step_count < 0:
            raise CarrierEncodingError(f"step_count must be non-negative: {self.step_count}")


def sim_embed(spec: MachineSpec, state: MachineState, simulator_fuel: int) -> SimState:
    """Embed guest specification and state into internalized simulator carrier state."""
    return SimState(
        guest_spec=spec,
        guest_state=state,
        simulator_fuel=simulator_fuel,
        step_count=0,
    )


def sim_extract(sim: SimState) -> tuple[MachineSpec, MachineState]:
    """Extract guest machine specification and state from simulator carrier state."""
    return sim.guest_spec, sim.guest_state


def step_internal(sim: SimState) -> SimState:
    """Single internalized simulation cycle within the carrier.

    Consults ONLY carrier-represented data:
      - Reads symbol from guest tape at guest cursor
      - Looks up rule in guest transition table within carrier
      - Updates guest state, tape, cursor, and fuel
      - Decrements host simulator fuel
    Zero external host oracles or metatheoretic loop counters.
    """
    if sim.simulator_fuel == 0 or sim.guest_state.halted or sim.guest_state.fuel == 0:
        return sim

    next_guest_state = step_direct(sim.guest_spec, sim.guest_state)
    return SimState(
        guest_spec=sim.guest_spec,
        guest_state=next_guest_state,
        simulator_fuel=sim.simulator_fuel - 1,
        step_count=sim.step_count + 1,
    )


def run_internal(sim: SimState, max_steps: int | None = None) -> SimState:
    """Iterate internalized simulation until halted, out of fuel, or limit reached."""
    curr = sim
    count = 0
    while curr.simulator_fuel > 0 and not curr.guest_state.halted and curr.guest_state.fuel > 0:
        if max_steps is not None and count >= max_steps:
            break
        curr = step_internal(curr)
        count += 1
    return curr


# --- Micro-step Internal Simulation Engine (k = 4 cycles per guest step) ---

STAGE_FETCH = 0
STAGE_LOOKUP = 1
STAGE_WRITE_MOVE = 2
STAGE_COMMIT = 3
MICRO_STEPS_PER_MACRO_STEP = 4


@dataclass(frozen=True)
class MicroSimState:
    """Fine-grained internalized carrier state with internal registers."""

    guest_spec: MachineSpec
    guest_state: MachineState
    simulator_fuel: int
    stage: int  # 0..3
    reg_symbol: int = 0
    reg_next_state: int = 0
    reg_write_sym: int = 0
    reg_move_cursor: int = 0
    reg_halt: bool = False
    macro_steps_completed: int = 0

    def __post_init__(self) -> None:
        if self.stage not in (0, 1, 2, 3):
            raise CarrierEncodingError(f"Invalid stage: {self.stage}")


def micro_sim_embed(spec: MachineSpec, state: MachineState, simulator_fuel: int) -> MicroSimState:
    """Embed machine into micro-step simulator carrier."""
    return MicroSimState(
        guest_spec=spec,
        guest_state=state,
        simulator_fuel=simulator_fuel,
        stage=STAGE_FETCH,
    )


def micro_step_internal(sim: MicroSimState) -> MicroSimState:
    """Single micro-step transition inside the carrier engine."""
    if sim.simulator_fuel == 0 or (sim.stage == STAGE_FETCH and (sim.guest_state.halted or sim.guest_state.fuel == 0)):
        return sim

    next_fuel = sim.simulator_fuel - 1

    if sim.stage == STAGE_FETCH:
        # Stage 0: Fetch current symbol under cursor
        sym = sim.guest_state.read_symbol(sim.guest_spec.default_sym)
        return MicroSimState(
            guest_spec=sim.guest_spec,
            guest_state=sim.guest_state,
            simulator_fuel=next_fuel,
            stage=STAGE_LOOKUP,
            reg_symbol=sym,
            macro_steps_completed=sim.macro_steps_completed,
        )

    elif sim.stage == STAGE_LOOKUP:
        # Stage 1: Lookup transition in spec
        trans = sim.guest_spec.lookup(sim.guest_state.state, sim.reg_symbol)
        if trans is None:
            # Missing transition -> halt
            return MicroSimState(
                guest_spec=sim.guest_spec,
                guest_state=sim.guest_state,
                simulator_fuel=next_fuel,
                stage=STAGE_COMMIT,
                reg_symbol=sim.reg_symbol,
                reg_next_state=sim.guest_state.state,
                reg_write_sym=sim.reg_symbol,
                reg_move_cursor=0,
                reg_halt=True,
                macro_steps_completed=sim.macro_steps_completed,
            )
        return MicroSimState(
            guest_spec=sim.guest_spec,
            guest_state=sim.guest_state,
            simulator_fuel=next_fuel,
            stage=STAGE_WRITE_MOVE,
            reg_symbol=sim.reg_symbol,
            reg_next_state=trans.next_state,
            reg_write_sym=trans.write_sym,
            reg_move_cursor=trans.move_cursor,
            reg_halt=trans.halt,
            macro_steps_completed=sim.macro_steps_completed,
        )

    elif sim.stage == STAGE_WRITE_MOVE:
        # Stage 2: Write tape and compute new cursor position
        new_tape = sim.guest_state.write_symbol(sim.reg_write_sym, sim.guest_spec.default_sym)
        new_cursor = max(0, sim.guest_state.cursor + sim.reg_move_cursor)
        intermediate_state = MachineState(
            state=sim.reg_next_state,
            cursor=new_cursor,
            tape=new_tape,
            fuel=sim.guest_state.fuel,
            halted=sim.guest_state.halted,
        )
        return MicroSimState(
            guest_spec=sim.guest_spec,
            guest_state=intermediate_state,
            simulator_fuel=next_fuel,
            stage=STAGE_COMMIT,
            reg_symbol=sim.reg_symbol,
            reg_next_state=sim.reg_next_state,
            reg_write_sym=sim.reg_write_sym,
            reg_move_cursor=sim.reg_move_cursor,
            reg_halt=sim.reg_halt,
            macro_steps_completed=sim.macro_steps_completed,
        )

    else:
        # Stage 3: Commit state, consume guest fuel, record halt
        final_guest_state = MachineState(
            state=sim.guest_state.state,
            cursor=sim.guest_state.cursor,
            tape=sim.guest_state.tape,
            fuel=sim.guest_state.fuel - 1,
            halted=sim.reg_halt,
        )
        return MicroSimState(
            guest_spec=sim.guest_spec,
            guest_state=final_guest_state,
            simulator_fuel=next_fuel,
            stage=STAGE_FETCH,
            macro_steps_completed=sim.macro_steps_completed + 1,
        )


def micro_step_k(sim: MicroSimState, k: int) -> MicroSimState:
    """Iterate k micro-steps."""
    curr = sim
    for _ in range(k):
        curr = micro_step_internal(curr)
    return curr
