"""Deterministic budgeted search coordinator with exact re-allocation.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats in logical decisions.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple, Union

from .dual_relaxation import (
    DualRefusalReceipt,
    ExactPathSolver,
    _default_cost_fn,
    _validated_cost,
)
from .hierarchical_search import (
    HierarchicalSearchEngine,
    SearchReceipt,
)
from .interval_domain import (
    create_interval_coarsening_map,
    create_interval_movegraph,
)
from .projective_system import CoarseningMap, MoveEdge, MoveGraph, _to_fraction


class ReasoningActionType(str, Enum):
    """Discrete decisions recorded by the budgeted coordinator."""

    INITIAL_ALLOCATION = "initial_allocation"
    BOUND_PROBE = "bound_probe"
    CERTIFIED_REFUSAL = "certified_refusal"
    BUDGET_REALLOCATION = "budget_reallocation"
    FINE_EXPANSION = "fine_expansion"
    OPTIMAL_SOLUTION = "optimal_solution"


@dataclass(frozen=True)
class CandidateGoal:
    """An exploration target or hypothesis query evaluated by the agent."""

    goal_id: str
    target: Any
    priority: int = 1
    description: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.goal_id, str) or not self.goal_id:
            raise ValueError("goal_id must be a non-empty string")
        if self.priority < 1:
            raise ValueError(f"Priority must be strictly positive, got {self.priority}")


@dataclass
class BudgetLedger:
    """Exact rational budget manager enforcing strict conservation invariants."""

    total_budget: Fraction
    unallocated_budget: Fraction
    allocated_budgets: Dict[str, Fraction] = field(default_factory=dict)
    consumed_budget: Fraction = field(default_factory=lambda: Fraction(0, 1))

    def __post_init__(self) -> None:
        self.total_budget = _to_fraction(self.total_budget, "total_budget")
        self.unallocated_budget = _to_fraction(
            self.unallocated_budget, "unallocated_budget"
        )
        self.consumed_budget = _to_fraction(self.consumed_budget, "consumed_budget")
        clean_allocations: Dict[str, Fraction] = {}
        for goal_id, amount in self.allocated_budgets.items():
            if not isinstance(goal_id, str) or not goal_id:
                raise ValueError("allocated budget keys must be non-empty strings")
            clean_allocations[goal_id] = _to_fraction(
                amount, f"allocated_budgets[{goal_id!r}]"
            )
        self.allocated_budgets = clean_allocations

        values = {
            "total budget": self.total_budget,
            "unallocated budget": self.unallocated_budget,
            "consumed budget": self.consumed_budget,
            **{
                f"allocation for {goal_id!r}": amount
                for goal_id, amount in self.allocated_budgets.items()
            },
        }
        for label, amount in values.items():
            if amount < 0:
                raise ValueError(f"{label} cannot be negative: {amount}")
        if not self.audit_conservation():
            raise ValueError(
                "Initial ledger violates conservation: total must equal "
                "unallocated + allocated + consumed"
            )

    def allocate(self, goal_id: str, amount: Union[Fraction, int]) -> None:
        """Allocate a budget slice from unallocated funds to a goal."""
        if not isinstance(goal_id, str) or not goal_id:
            raise ValueError("goal_id must be a non-empty string")
        q_amt = _to_fraction(amount, "allocation_amount")
        if q_amt < 0:
            raise ValueError(f"Cannot allocate negative budget: {q_amt}")
        if q_amt > self.unallocated_budget:
            raise ValueError(
                f"Insufficient unallocated budget: requested {q_amt}, available {self.unallocated_budget}"
            )
        self.unallocated_budget -= q_amt
        self.allocated_budgets[goal_id] = self.allocated_budgets.get(goal_id, Fraction(0, 1)) + q_amt

    def reclaim(self, goal_id: str) -> Fraction:
        """Reclaim all remaining allocated budget for a goal back into unallocated pool."""
        if not isinstance(goal_id, str) or not goal_id:
            raise ValueError("goal_id must be a non-empty string")
        reclaimed = self.allocated_budgets.pop(goal_id, Fraction(0, 1))
        self.unallocated_budget += reclaimed
        return reclaimed

    def consume(self, goal_id: str, amount: Union[Fraction, int]) -> None:
        """Consume budget during operational execution."""
        if not isinstance(goal_id, str) or not goal_id:
            raise ValueError("goal_id must be a non-empty string")
        q_amt = _to_fraction(amount, "consumed_amount")
        if q_amt < 0:
            raise ValueError(f"Cannot consume negative budget: {q_amt}")
        current = self.allocated_budgets.get(goal_id, Fraction(0, 1))
        if q_amt > current:
            raise ValueError(
                f"Goal {goal_id!r} exceeded allocated budget: allocated {current}, requested consumption {q_amt}"
            )
        self.allocated_budgets[goal_id] = current - q_amt
        self.consumed_budget += q_amt

    def redistribute_unallocated(
        self,
        active_goal_ids: Sequence[str],
        weights: Optional[Mapping[str, Fraction]] = None,
    ) -> None:
        """Redistribute all unallocated funds across active candidate goals."""
        if any(not isinstance(goal_id, str) or not goal_id for goal_id in active_goal_ids):
            raise ValueError("active_goal_ids must contain non-empty strings")
        if len(set(active_goal_ids)) != len(active_goal_ids):
            raise ValueError("active_goal_ids must be unique")
        clean_weights: Optional[Dict[str, Fraction]] = None
        if weights is not None:
            extras = set(weights) - set(active_goal_ids)
            if extras:
                raise ValueError(
                    f"weights contain inactive goal ids: {sorted(extras)!r}"
                )
            clean_weights = {}
            for goal_id in active_goal_ids:
                weight = _to_fraction(
                    weights.get(goal_id, Fraction(0, 1)),
                    f"weight[{goal_id!r}]",
                )
                if weight < 0:
                    raise ValueError(f"weight for {goal_id!r} cannot be negative")
                clean_weights[goal_id] = weight

        if not active_goal_ids or self.unallocated_budget <= 0:
            return

        avail = self.unallocated_budget
        if clean_weights is None:
            # Uniform exact rational division
            n = len(active_goal_ids)
            slice_amt = avail / n
            for gid in active_goal_ids:
                self.allocated_budgets[gid] = self.allocated_budgets.get(gid, Fraction(0, 1)) + slice_amt
            self.unallocated_budget = Fraction(0, 1)
        else:
            total_weight = sum(
                (clean_weights[gid] for gid in active_goal_ids),
                Fraction(0, 1),
            )
            if total_weight <= 0:
                return
            allocated_so_far = Fraction(0, 1)
            for i, gid in enumerate(active_goal_ids):
                if i == len(active_goal_ids) - 1:
                    # Remainder absorption preserves conservation exactly
                    share = avail - allocated_so_far
                else:
                    w = clean_weights[gid]
                    share = (avail * w) / total_weight
                    allocated_so_far += share
                self.allocated_budgets[gid] = self.allocated_budgets.get(gid, Fraction(0, 1)) + share
            self.unallocated_budget = Fraction(0, 1)

    def audit_conservation(self) -> bool:
        """Verify the exact budget conservation invariant."""
        sum_allocated = sum(self.allocated_budgets.values(), Fraction(0, 1))
        return self.total_budget == (self.unallocated_budget + sum_allocated + self.consumed_budget)


@dataclass(frozen=True)
class ReasoningTraceEvent:
    """One deterministic event in the coordinator execution log."""

    step: int
    action: ReasoningActionType
    goal_id: Optional[str]
    details: Dict[str, Any]
    ledger_snapshot: Dict[str, Any]


@dataclass(frozen=True)
class GoalOutcome:
    """The resolved outcome of a candidate goal."""

    goal_id: str
    status: str  # "SOLVED" or "CERTIFIED_REFUSED"
    path: Optional[Tuple[MoveEdge, ...]]
    cost: Optional[Fraction]
    receipt: Optional[SearchReceipt]
    fine_nodes_explored: int
    coarse_pruned: bool
    budget_allocated: Fraction
    budget_consumed: Fraction


@dataclass(frozen=True)
class ReasoningCoordinatorReceipt:
    """Deterministic summary with SHA-256 content checksums, not an authenticity proof."""

    total_initial_budget: Fraction
    consumed_budget: Fraction
    unallocated_budget: Fraction
    reclaimed_budget: Fraction
    goals_total: int
    goals_solved: int
    goals_refused: int
    goals_exhausted: int
    total_fine_nodes_explored: int
    trace_length: int
    trace_digest: str
    budget_conservation_verified: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_initial_budget": str(self.total_initial_budget),
            "consumed_budget": str(self.consumed_budget),
            "unallocated_budget": str(self.unallocated_budget),
            "reclaimed_budget": str(self.reclaimed_budget),
            "goals_total": self.goals_total,
            "goals_solved": self.goals_solved,
            "goals_refused": self.goals_refused,
            "goals_exhausted": self.goals_exhausted,
            "total_fine_nodes_explored": self.total_fine_nodes_explored,
            "trace_length": self.trace_length,
            "trace_digest": self.trace_digest,
            "budget_conservation_verified": self.budget_conservation_verified,
        }

    def digest(self) -> str:
        canonical_json = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


class BudgetedReasoningCoordinator:
    """One-shot deterministic coordinator for budgeted finite-graph searches."""

    def __init__(
        self,
        fine_scale: int = 4,
        coarse_scale: int = 2,
        total_budget: Union[Fraction, int] = Fraction(1, 1),
        fine_graph: Optional[MoveGraph] = None,
        coarse_graph: Optional[MoveGraph] = None,
        coarsening_map: Optional[CoarseningMap] = None,
        cost_fn: Callable[[MoveEdge], Fraction] = _default_cost_fn,
    ) -> None:
        self.fine_scale = fine_scale
        self.coarse_scale = coarse_scale
        self.total_budget = _to_fraction(total_budget, "total_budget")
        self.cost_fn = cost_fn

        # Build default interval graphs if not provided
        self.fine_graph = (
            fine_graph
            if fine_graph is not None
            else create_interval_movegraph(scale=fine_scale)
        )
        self.coarse_graph = (
            coarse_graph
            if coarse_graph is not None
            else create_interval_movegraph(scale=coarse_scale)
        )
        self.coarsening_map = (
            coarsening_map
            if coarsening_map is not None
            else create_interval_coarsening_map(coarse_scale, fine_scale)
        )

        self.ledger = BudgetLedger(
            total_budget=self.total_budget,
            unallocated_budget=self.total_budget,
        )
        self.trace: List[ReasoningTraceEvent] = []
        self._step_counter = 0
        self._total_reclaimed = Fraction(0, 1)
        self._has_run = False

    def _record_event(
        self,
        action: ReasoningActionType,
        goal_id: Optional[str],
        details: Dict[str, Any],
    ) -> None:
        self._step_counter += 1
        snapshot = {
            "total": str(self.ledger.total_budget),
            "unallocated": str(self.ledger.unallocated_budget),
            "consumed": str(self.ledger.consumed_budget),
            "allocated": {k: str(v) for k, v in self.ledger.allocated_budgets.items()},
        }
        self.trace.append(
            ReasoningTraceEvent(
                step=self._step_counter,
                action=action,
                goal_id=goal_id,
                details=details,
                ledger_snapshot=snapshot,
            )
        )

    def run(
        self,
        source: Any,
        goals: Sequence[CandidateGoal],
    ) -> Tuple[Dict[str, GoalOutcome], ReasoningCoordinatorReceipt]:
        """Allocate once, screen by exact bounds, reallocate, and search."""
        if self._has_run:
            raise RuntimeError("BudgetedReasoningCoordinator instances are one-shot")
        if not self.fine_graph.has_state(source):
            raise KeyError(f"Source state {source!r} not in fine graph")
        goal_ids = [goal.goal_id for goal in goals]
        if len(set(goal_ids)) != len(goal_ids):
            raise ValueError("Candidate goal_id values must be unique")
        for goal in goals:
            if not self.fine_graph.has_state(goal.target):
                raise KeyError(
                    f"Target state {goal.target!r} for goal {goal.goal_id!r} "
                    "not in fine graph"
                )
        morphism = self.coarsening_map.check_morphism(
            self.fine_graph, self.coarse_graph
        )
        if not morphism.is_valid:
            detail = "; ".join(morphism.defects)
            raise ValueError(f"Coarsening map failed morphism verification: {detail}")

        self._has_run = True
        if not goals:
            return {}, ReasoningCoordinatorReceipt(
                total_initial_budget=self.total_budget,
                consumed_budget=Fraction(0, 1),
                unallocated_budget=self.total_budget,
                reclaimed_budget=Fraction(0, 1),
                goals_total=0,
                goals_solved=0,
                goals_refused=0,
                goals_exhausted=0,
                total_fine_nodes_explored=0,
                trace_length=0,
                trace_digest=hashlib.sha256(b"[]").hexdigest(),
                budget_conservation_verified=self.ledger.audit_conservation(),
            )

        # Stage 1: initial priority-weighted allocation.
        total_priority = sum(g.priority for g in goals)
        for g in goals:
            slice_amt = (self.total_budget * g.priority) / total_priority
            self.ledger.allocate(g.goal_id, slice_amt)
            self._record_event(
                ReasoningActionType.INITIAL_ALLOCATION,
                g.goal_id,
                {"allocated": str(slice_amt), "priority": g.priority},
            )

        outcomes: Dict[str, GoalOutcome] = {}
        viable_goals: List[CandidateGoal] = []
        exact_bounds: Dict[str, Fraction] = {}

        # Stage 2: exact fine-graph distance screening. This computation does
        # traverse the finite graph; zero below means zero subsequent path-search
        # expansions, not zero certificate work.
        fine_potential = ExactPathSolver.compute_dual_potential(
            self.fine_graph, source, cost_fn=self.cost_fn
        )
        for g in goals:
            alloc = self.ledger.allocated_budgets[g.goal_id]
            exact_bound = fine_potential.potential_difference(source, g.target)

            self._record_event(
                ReasoningActionType.BOUND_PROBE,
                g.goal_id,
                {
                    "exact_bound": (
                        str(exact_bound) if exact_bound is not None else "unreachable"
                    )
                },
            )

            if exact_bound is None or exact_bound > alloc:
                reason = (
                    "Target is unreachable in the exact finite fine graph"
                    if exact_bound is None
                    else (
                        f"Exact shortest-path lower bound {exact_bound} strictly "
                        f"exceeds allocated budget {alloc}"
                    )
                )
                refusal_receipt = DualRefusalReceipt(
                    source=source,
                    target=g.target,
                    budget=alloc,
                    dual_bound=exact_bound,
                    certified_refusal=True,
                    reason=reason,
                )
                reclaimed = self.ledger.reclaim(g.goal_id)
                self._total_reclaimed += reclaimed

                self._record_event(
                    ReasoningActionType.CERTIFIED_REFUSAL,
                    g.goal_id,
                    {"reclaimed": str(reclaimed), "reason": refusal_receipt.reason},
                )

                outcomes[g.goal_id] = GoalOutcome(
                    goal_id=g.goal_id,
                    status="CERTIFIED_REFUSED",
                    path=None,
                    cost=None,
                    receipt=refusal_receipt,
                    fine_nodes_explored=0,
                    coarse_pruned=False,
                    budget_allocated=alloc,
                    budget_consumed=Fraction(0, 1),
                )
            else:
                viable_goals.append(g)
                exact_bounds[g.goal_id] = exact_bound

        # Stage 3: exact re-allocation of reclaimed funds.
        if viable_goals and self.ledger.unallocated_budget > 0:
            reclaimed_pool = self.ledger.unallocated_budget
            weights: Dict[str, Fraction] = {}
            for g in viable_goals:
                dist = exact_bounds[g.goal_id]
                weights[g.goal_id] = Fraction(g.priority, 1) / (dist + Fraction(1, 2))

            viable_ids = [g.goal_id for g in viable_goals]
            self.ledger.redistribute_unallocated(viable_ids, weights=weights)

            self._record_event(
                ReasoningActionType.BUDGET_REALLOCATION,
                None,
                {
                    "reallocated_total": str(reclaimed_pool),
                    "beneficiaries": {gid: str(self.ledger.allocated_budgets[gid]) for gid in viable_ids},
                },
            )

        # Stage 4: checked coarse-to-fine execution, ordered by exact bound.
        viable_goals.sort(key=lambda g: exact_bounds[g.goal_id])

        for g in viable_goals:
            current_budget = self.ledger.allocated_budgets[g.goal_id]

            self._record_event(
                ReasoningActionType.FINE_EXPANSION,
                g.goal_id,
                {"budget_available": str(current_budget)},
            )

            result = HierarchicalSearchEngine.search_with_coarse_pruning(
                fine_graph=self.fine_graph,
                coarse_graph=self.coarse_graph,
                coarsening_map=self.coarsening_map,
                source=source,
                target=g.target,
                budget=current_budget,
                cost_fn=self.cost_fn,
            )

            if result.path is not None:
                actual_cost = sum(
                    (_validated_cost(edge, self.cost_fn) for edge in result.path),
                    Fraction(0, 1),
                )
                self.ledger.consume(g.goal_id, actual_cost)

                reclaimed_remainder = self.ledger.reclaim(g.goal_id)
                self._total_reclaimed += reclaimed_remainder

                self._record_event(
                    ReasoningActionType.OPTIMAL_SOLUTION,
                    g.goal_id,
                    {
                        "actual_cost": str(actual_cost),
                        "nodes_explored": result.nodes_explored,
                        "reclaimed_remainder": str(reclaimed_remainder),
                    },
                )

                outcomes[g.goal_id] = GoalOutcome(
                    goal_id=g.goal_id,
                    status="SOLVED",
                    path=result.path,
                    cost=actual_cost,
                    receipt=result.receipt,
                    fine_nodes_explored=result.nodes_explored,
                    coarse_pruned=result.coarse_pruned,
                    budget_allocated=current_budget,
                    budget_consumed=actual_cost,
                )

                remaining_unrun = [
                    rem.goal_id
                    for rem in viable_goals
                    if rem.goal_id not in outcomes and rem.goal_id != g.goal_id
                ]
                if remaining_unrun and self.ledger.unallocated_budget > 0:
                    self.ledger.redistribute_unallocated(remaining_unrun)
            else:
                raise RuntimeError(
                    "Consistency defect: exact screening admitted goal "
                    f"{g.goal_id!r} at bound {exact_bounds[g.goal_id]}, but "
                    "checked search returned no path"
                )

        # Stage 5: exact conservation audit and deterministic content checksum.
        conservation_ok = self.ledger.audit_conservation()
        if not conservation_ok:
            raise RuntimeError(
                f"Budget conservation violated: total={self.ledger.total_budget}, "
                f"unallocated={self.ledger.unallocated_budget}, "
                f"allocated={self.ledger.allocated_budgets}, "
                f"consumed={self.ledger.consumed_budget}"
            )

        raw_trace_json = json.dumps(
            [
                {
                    "step": ev.step,
                    "action": ev.action.value,
                    "goal_id": ev.goal_id,
                    "details": {k: str(v) for k, v in ev.details.items()},
                    "ledger": ev.ledger_snapshot,
                }
                for ev in self.trace
            ],
            sort_keys=True,
        )
        trace_digest = hashlib.sha256(raw_trace_json.encode("utf-8")).hexdigest()

        receipt = ReasoningCoordinatorReceipt(
            total_initial_budget=self.total_budget,
            consumed_budget=self.ledger.consumed_budget,
            unallocated_budget=self.ledger.unallocated_budget,
            reclaimed_budget=self._total_reclaimed,
            goals_total=len(goals),
            goals_solved=sum(1 for o in outcomes.values() if o.status == "SOLVED"),
            goals_refused=sum(1 for o in outcomes.values() if o.status == "CERTIFIED_REFUSED"),
            goals_exhausted=sum(1 for o in outcomes.values() if o.status == "BUDGET_EXHAUSTED"),
            total_fine_nodes_explored=sum(o.fine_nodes_explored for o in outcomes.values()),
            trace_length=len(self.trace),
            trace_digest=trace_digest,
            budget_conservation_verified=conservation_ok,
        )

        return outcomes, receipt
