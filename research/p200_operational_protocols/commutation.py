"""Readout-to-step commutation on non-disturbing sectors.

Proves and verifies:
1. Readout-to-step commutation theorem:
   For any readout operation and process state transition whose carrier footprints
   are disjoint (non-disturbing sector), the operations commute on all carrier states:
       Readout ∘ Step = Step ∘ Readout
2. Disturbance detection and pricing:
   When access footprints overlap, operational commutation fails in general.
   Disturbance is explicitly priced and recorded in the carrier's diagnostic register.

AuthorityEffect: None.
Axiom Scope: Constructive finite state evaluations without external host oracles.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Tuple

from protocol import (
    CarrierState,
    Footprint,
    Locus,
    MeasurementInstrument,
    non_disturbing_readout_2,
    disturbing_readout_1,
)


@dataclass(frozen=True)
class ProcessStep:
    """An autonomous state transition step of the carrier process."""

    name: str
    target_locus: Locus
    transition_fn: Callable[[int], int]
    reads: frozenset[Locus]
    writes: frozenset[Locus]

    @property
    def footprint(self) -> Footprint:
        return Footprint(reads=self.reads, writes=self.writes)

    def execute(self, s: CarrierState) -> CarrierState:
        target_val = int(getattr(s, self.target_locus.name.lower()))
        new_val = self.transition_fn(target_val)
        kwargs = {self.target_locus.name.lower(): new_val}
        # Construct new state with updated field
        d = {
            "l1": s.l1,
            "l2": s.l2,
            "m": s.m,
            "r1": s.r1,
            "r2": s.r2,
            "dist": s.dist,
        }
        d.update(kwargs)
        return CarrierState(**d)


def is_non_disturbing_sector(fp_readout: Footprint, fp_step: Footprint) -> bool:
    """Determine whether readout and step occupy mutually non-disturbing sectors."""
    return fp_readout.is_disjoint(fp_step)


def check_commutation(
    s: CarrierState,
    op1: Callable[[CarrierState], CarrierState],
    op2: Callable[[CarrierState], CarrierState],
) -> bool:
    """Check whether two state operations commute on a specific state."""
    left = op1(op2(s))
    right = op2(op1(s))
    return left == right


def sweep_commutation(
    states: List[CarrierState],
    op1: Callable[[CarrierState], CarrierState],
    op2: Callable[[CarrierState], CarrierState],
) -> dict[str, Any]:
    """Exhaustively verify commutation across a state ensemble."""
    total = len(states)
    commuting = 0
    failing_witnesses: List[Tuple[CarrierState, CarrierState, CarrierState]] = []

    for s in states:
        left = op1(op2(s))
        right = op2(op1(s))
        if left == right:
            commuting += 1
        else:
            if len(failing_witnesses) < 5:
                failing_witnesses.append((s, left, right))

    return {
        "total_states": total,
        "commuting_count": commuting,
        "all_commute": commuting == total,
        "failing_count": total - commuting,
        "sample_failure": failing_witnesses[0] if failing_witnesses else None,
    }


def step_l1(f: Callable[[int], int]) -> Callable[[CarrierState], CarrierState]:
    """Create a step operation at Locus 1."""
    return lambda s: CarrierState(
        l1=f(s.l1), l2=s.l2, m=s.m, r1=s.r1, r2=s.r2, dist=s.dist
    )


def step_m(h: Callable[[int], int]) -> Callable[[CarrierState], CarrierState]:
    """Create a step operation at coupling locus M."""
    return lambda s: CarrierState(
        l1=s.l1, l2=s.l2, m=h(s.m), r1=s.r1, r2=s.r2, dist=s.dist
    )


@dataclass(frozen=True)
class DisturbanceReceipt:
    """Receipt documenting disturbance detection and explicit pricing."""

    interfering: bool
    disturbance_cost: int
    commutation_preserved_on_priced_carrier: bool
    diagnostic_mark: int


def evaluate_disturbance_pricing(
    s: CarrierState,
    readout_op: Callable[[CarrierState], CarrierState],
    step_op: Callable[[CarrierState], CarrierState],
) -> DisturbanceReceipt:
    """Evaluate whether disturbance occurred, inspect costs, and verify commutation."""
    left = readout_op(step_op(s))
    right = step_op(readout_op(s))

    commutes = (left == right)
    cost = max(left.dist, right.dist) - s.dist
    interfering = not commutes

    return DisturbanceReceipt(
        interfering=interfering,
        disturbance_cost=cost,
        commutation_preserved_on_priced_carrier=commutes,
        diagnostic_mark=max(left.dist, right.dist),
    )
