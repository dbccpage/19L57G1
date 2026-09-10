"""Target G015 / G017: First-Demand, Invocation Bridge & Autonomous Endogenous Stepping.

This module formalizes:
1. Event-wise demand lifecycle (creation, activation, discharge, reopening).
2. Deterministic first-demand index selection with canonical tie-breaking.
3. Endogenous stepping without host intervention, schedulers, or unrecorded selectors.
4. Prohibition of spontaneous demand creation from inert histories.
5. Exact rational resource charging and finite saturation.

AuthorityEffect: None.
Claim Hygiene: Discrete finite carrier models; all properties exact and constructive.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Any, Generic, Mapping, Sequence, TypeVar

T = TypeVar("T")
E = TypeVar("E")


@dataclass(frozen=True)
class Result(Generic[T, E]):
    """Monadic Result type for explicit failure and refusal tracking."""

    _value: T | None
    _error: E | None
    _is_ok: bool

    @classmethod
    def ok(cls, value: T) -> Result[T, E]:
        return cls(_value=value, _error=None, _is_ok=True)

    @classmethod
    def err(cls, error: E) -> Result[T, E]:
        return cls(_value=None, _error=error, _is_ok=False)

    def is_ok(self) -> bool:
        return self._is_ok

    def is_err(self) -> bool:
        return not self._is_ok

    def unwrap(self) -> T:
        if not self._is_ok:
            raise ValueError(f"Called unwrap on Err: {self._error}")
        assert self._value is not None
        return self._value

    def unwrap_err(self) -> E:
        if self._is_ok:
            raise ValueError("Called unwrap_err on Ok")
        assert self._error is not None
        return self._error


class DemandStatus(Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    DISCHARGED = "DISCHARGED"
    REOPENED = "REOPENED"


@dataclass(frozen=True)
class Demand:
    """A represented operational demand in the process carrier."""

    demand_id: int
    kind: str
    priority: int  # Lower number = higher priority
    target_locus: str
    payload: int
    remaining_budget: int
    status: DemandStatus


@dataclass(frozen=True)
class CarrierState:
    """Discrete process carrier with represented memory and internal demands."""

    memory: tuple[tuple[str, int], ...]
    demands: tuple[Demand, ...]
    step_count: int
    resources_spent: Fraction
    is_booted: bool
    is_inert: bool

    @classmethod
    def create_initial(
        cls,
        memory: Mapping[str, int],
        initial_demands: Sequence[Demand],
    ) -> CarrierState:
        mem_pairs = tuple(sorted(memory.items(), key=lambda p: p[0]))
        sorted_demands = tuple(initial_demands)
        return cls(
            memory=mem_pairs,
            demands=sorted_demands,
            step_count=0,
            resources_spent=Fraction(0, 1),
            is_booted=True,
            is_inert=len(initial_demands) == 0,
        )

    def get_memory(self, locus: str) -> int | None:
        for k, v in self.memory:
            if k == locus:
                return v
        return None

    def with_memory(self, locus: str, val: int) -> CarrierState:
        mem_dict = dict(self.memory)
        mem_dict[locus] = val
        sorted_pairs = tuple(sorted(mem_dict.items(), key=lambda p: p[0]))
        return CarrierState(
            memory=sorted_pairs,
            demands=self.demands,
            step_count=self.step_count,
            resources_spent=self.resources_spent,
            is_booted=self.is_booted,
            is_inert=False,
        )

    def pending_demands(self) -> tuple[Demand, ...]:
        return tuple(
            d for d in self.demands
            if d.status in (DemandStatus.PENDING, DemandStatus.REOPENED)
        )


@dataclass(frozen=True)
class StepOutcome:
    """Represented outcome of an endogenous step."""

    status: str  # "TRANSITION", "QUIESCENT", "REFUSAL"
    state: CarrierState
    discharged_demand_id: int | None
    cost: Fraction
    message: str


def select_first_demand(state: CarrierState) -> int | None:
    """Deterministic first-demand selection index.

    Picks the pending/reopened demand with lowest priority value (highest priority).
    Ties broken strictly by minimum demand_id.
    Zero external choice or randomness.
    """
    pending = state.pending_demands()
    if not pending:
        return None

    # Deterministic minimum by (priority, demand_id)
    best = min(pending, key=lambda d: (d.priority, d.demand_id))
    return best.demand_id


def step_autonomous(state: CarrierState) -> StepOutcome:
    """Execute one autonomous endogenous transition step without external driving.

    Rules:
    - If no pending demand exists: transitions to QUIESCENT with zero mutation.
    - If inert without boot demands: stays QUIESCENT (no spontaneous demand from inert history).
    - Otherwise selects first demand canonically.
    - Performs the demand action:
        - "WRITE": updates memory at target_locus with payload, discharges demand.
        - "REOPEN_CHAIN": decrements budget, if budget > 0 reopens with payload increment, else discharges.
    - Charges exact rational resource cost Fraction(1, 1).
    """
    if not state.is_booted:
        return StepOutcome(
            status="REFUSAL",
            state=state,
            discharged_demand_id=None,
            cost=Fraction(0, 1),
            message="Refusal: system not booted",
        )

    target_id = select_first_demand(state)
    if target_id is None:
        # Quiescent state: no pending demand
        return StepOutcome(
            status="QUIESCENT",
            state=state,
            discharged_demand_id=None,
            cost=Fraction(0, 1),
            message="Quiescent: zero pending demands",
        )

    # Locate demand
    demand_idx = -1
    for i, d in enumerate(state.demands):
        if d.demand_id == target_id:
            demand_idx = i
            break
    assert demand_idx >= 0
    curr_d = state.demands[demand_idx]

    # Execute action
    step_cost = Fraction(1, 1)
    new_memory_dict = dict(state.memory)
    new_demands_list = list(state.demands)

    if curr_d.kind == "WRITE":
        new_memory_dict[curr_d.target_locus] = curr_d.payload
        # Discharge demand
        new_demands_list[demand_idx] = Demand(
            demand_id=curr_d.demand_id,
            kind=curr_d.kind,
            priority=curr_d.priority,
            target_locus=curr_d.target_locus,
            payload=curr_d.payload,
            remaining_budget=0,
            status=DemandStatus.DISCHARGED,
        )

    elif curr_d.kind == "REOPEN_CHAIN":
        new_memory_dict[curr_d.target_locus] = curr_d.payload
        if curr_d.remaining_budget > 1:
            # Reopen demand with decremented budget
            new_demands_list[demand_idx] = Demand(
                demand_id=curr_d.demand_id,
                kind=curr_d.kind,
                priority=curr_d.priority,
                target_locus=curr_d.target_locus,
                payload=curr_d.payload + 1,
                remaining_budget=curr_d.remaining_budget - 1,
                status=DemandStatus.REOPENED,
            )
        else:
            # Fully discharged
            new_demands_list[demand_idx] = Demand(
                demand_id=curr_d.demand_id,
                kind=curr_d.kind,
                priority=curr_d.priority,
                target_locus=curr_d.target_locus,
                payload=curr_d.payload + 1,
                remaining_budget=0,
                status=DemandStatus.DISCHARGED,
            )
    else:
        # Unknown kind results in explicit refusal
        return StepOutcome(
            status="REFUSAL",
            state=state,
            discharged_demand_id=curr_d.demand_id,
            cost=Fraction(0, 1),
            message=f"Refusal: unrecognized demand kind '{curr_d.kind}'",
        )

    new_state = CarrierState(
        memory=tuple(sorted(new_memory_dict.items(), key=lambda p: p[0])),
        demands=tuple(new_demands_list),
        step_count=state.step_count + 1,
        resources_spent=state.resources_spent + step_cost,
        is_booted=True,
        is_inert=False,
    )

    return StepOutcome(
        status="TRANSITION",
        state=new_state,
        discharged_demand_id=curr_d.demand_id,
        cost=step_cost,
        message=f"Executed demand {curr_d.demand_id} ({curr_d.kind})",
    )


def run_to_saturation(
    initial_state: CarrierState, max_steps: int = 1000
) -> tuple[CarrierState, list[StepOutcome]]:
    """Run autonomous stepping loop until quiescence or step budget exhausted."""
    outcomes: list[StepOutcome] = []
    current = initial_state
    for _ in range(max_steps):
        outcome = step_autonomous(current)
        outcomes.append(outcome)
        current = outcome.state
        if outcome.status in ("QUIESCENT", "REFUSAL"):
            break
    return current, outcomes
