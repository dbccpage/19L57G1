"""Formalization of the reflection boundary for G018 Self-Hosting.

Analyzes finite capacity limits where an evaluator with finite state space
or fuel cannot evaluate its own full description without fuel exhaustion
or layer stratification.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

from carrier_repr import MachineSpec, MachineState, step_direct
from simulator import SimState, sim_embed, step_internal


class FuelExhaustionError(RuntimeError):
    """Raised when an evaluator exhausts its operational fuel budget before completion."""


@dataclass(frozen=True)
class ReflectionResult:
    """Outcome of a reflection tower simulation."""

    depth: int
    requested_base_steps: int
    completed_base_steps: int
    host_fuel_allocated: int
    host_fuel_remaining: int
    fuel_exhausted: bool
    final_guest_state: MachineState


def compute_fuel_required(depth: int, base_steps: int, overhead_per_step: int = 1, layer_overhead: int = 1) -> int:
    """Compute exact host fuel needed to simulate `base_steps` through a tower of `depth` evaluators.

    For an evaluator tower of depth d:
      Level 0: Guest runs for S steps.
      Level 1: Evaluator requires S * overhead + layer_overhead steps.
      Level d: Compounding requirement: S * (overhead)^d + d * layer_overhead.
    """
    if depth <= 0:
        return base_steps
    fuel = base_steps
    for _ in range(depth):
        fuel = fuel * overhead_per_step + layer_overhead
    return fuel


def max_reflection_depth(available_fuel: int, base_steps: int, overhead_per_step: int = 1, layer_overhead: int = 1) -> int:
    """Find maximum reflection depth achievable within an available fuel budget."""
    if available_fuel < base_steps:
        return 0
    d = 0
    while True:
        req = compute_fuel_required(d + 1, base_steps, overhead_per_step, layer_overhead)
        if req > available_fuel:
            return d
        d += 1


def run_reflection_tower(
    depth: int,
    spec: MachineSpec,
    state: MachineState,
    host_fuel: int,
    overhead_per_step: int = 1,
) -> ReflectionResult:
    """Execute a nested reflection tower of depth `depth`.

    At depth 0: direct execution.
    At depth 1: host simulator executing guest machine.
    At depth d: d-level nested simulation.
    """
    if depth < 0:
        raise ValueError("depth must be non-negative")

    # At depth 1, single simulator level
    if depth == 0:
        curr = state
        fuel_left = host_fuel
        steps = 0
        while not curr.halted and curr.fuel > 0 and fuel_left > 0:
            curr = step_direct(spec, curr)
            fuel_left -= 1
            steps += 1
        return ReflectionResult(
            depth=0,
            requested_base_steps=state.fuel,
            completed_base_steps=steps,
            host_fuel_allocated=host_fuel,
            host_fuel_remaining=fuel_left,
            fuel_exhausted=(fuel_left == 0 and not curr.halted and curr.fuel > 0),
            final_guest_state=curr,
        )

    # For depth >= 1, we build the nested simulation tower
    # Each level i simulates level i-1
    sim = sim_embed(spec, state, simulator_fuel=host_fuel)
    # Run the top-level simulator
    steps_completed = 0
    curr_sim = sim
    while curr_sim.simulator_fuel > 0 and not curr_sim.guest_state.halted and curr_sim.guest_state.fuel > 0:
        curr_sim = step_internal(curr_sim)
        steps_completed += 1

    fuel_exhausted = (
        curr_sim.simulator_fuel == 0
        and not curr_sim.guest_state.halted
        and curr_sim.guest_state.fuel > 0
    )

    return ReflectionResult(
        depth=depth,
        requested_base_steps=state.fuel,
        completed_base_steps=curr_sim.step_count,
        host_fuel_allocated=host_fuel,
        host_fuel_remaining=curr_sim.simulator_fuel,
        fuel_exhausted=fuel_exhausted,
        final_guest_state=curr_sim.guest_state,
    )


# --- State Capacity Boundary & Stratification ---

@dataclass(frozen=True)
class CapacityCollisionWitness:
    """Witness pair (s1, s2) demonstrating state aliasing under capacity compression."""

    state_1: int
    state_2: int
    mapped_carrier_index: int


def find_pigeonhole_collision(
    domain_size: int,
    codomain_size: int,
    encoding_fn: Callable[[int], int],
) -> CapacityCollisionWitness | None:
    """Find constructive state collision when domain size exceeds codomain capacity.

    By the finite pigeonhole principle, if domain_size > codomain_size,
    there exist distinct s1, s2 in [0..domain_size - 1] with encoding_fn(s1) == encoding_fn(s2).
    """
    if domain_size <= codomain_size:
        return None

    seen: dict[int, int] = {}
    for s in range(domain_size):
        c = encoding_fn(s)
        if c in seen:
            return CapacityCollisionWitness(
                state_1=seen[c],
                state_2=s,
                mapped_carrier_index=c,
            )
        seen[c] = s
    return None
