"""Autonomous Reasoning Engine Agent with Adaptive Budget Re-allocation.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats in logical decisions.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple, Union

from .dual_relaxation import (
    DualPotential,
    DualRefusalReceipt,
    DualRelaxationSolver,
    DualityGapReceipt,
    _default_cost_fn,
)
from .hierarchical_search import (
    HierarchicalRefusalReceipt,
    HierarchicalSearchEngine,
    HierarchicalSearchResult,
)
from .interval_domain import (
    DyadicInterval,
    create_interval_coarsening_map,
    create_interval_movegraph,
)
from .projective_system import CoarseningMap, MoveEdge, MoveGraph, _to_fraction


class ReasoningActionType(str, Enum):
    """Discrete decision steps executed by the autonomous reasoning agent."""

    INITIAL_ALLOCATION = "initial_allocation"
    COARSE_PROBE = "coarse_probe"
    CERTIFIED_REFUSAL = "certified_refusal"
    BUDGET_REALLOCATION = "budget_reallocation"
    FINE_EXPANSION = "fine_expansion"
    OPTIMAL_SOLUTION = "optimal_solution"
    BUDGET_EXHAUSTION = "budget_exhaustion"


@dataclass(frozen=True)
class CandidateGoal:
    """An exploration target or hypothesis query evaluated by the agent."""

    goal_id: str
    target: Any
    priority: int = 1
    description: str = ""

    def __post_init__(self) -> None:
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
        if self.total_budget < 0:
            raise ValueError(f"Total budget cannot be negative: {self.total_budget}")
        if self.unallocated_budget < 0:
            raise ValueError(f"Unallocated budget cannot be negative: {self.unallocated_budget}")

    def allocate(self, goal_id: str, amount: Union[Fraction, int]) -> None:
        """Allocate a budget slice from unallocated funds to a goal."""
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
        reclaimed = self.allocated_budgets.pop(goal_id, Fraction(0, 1))
        self.unallocated_budget += reclaimed
        return reclaimed

    def consume(self, goal_id: str, amount: Union[Fraction, int]) -> None:
        """Consume budget during operational execution."""
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
        if not active_goal_ids or self.unallocated_budget <= 0:
            return

        avail = self.unallocated_budget
        if weights is None:
            # Uniform exact rational division
            n = len(active_goal_ids)
            slice_amt = avail / n
            for gid in active_goal_ids:
                self.allocated_budgets[gid] = self.allocated_budgets.get(gid, Fraction(0, 1)) + slice_amt
            self.unallocated_budget = Fraction(0, 1)
        else:
            total_weight = sum(weights.get(gid, Fraction(0, 1)) for gid in active_goal_ids)
            if total_weight <= 0:
                return
            allocated_so_far = Fraction(0, 1)
            for i, gid in enumerate(active_goal_ids):
                if i == len(active_goal_ids) - 1:
                    # Remainder absorption preserves conservation exactly
                    share = avail - allocated_so_far
                else:
                    w = weights.get(gid, Fraction(0, 1))
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
    """An immutable atomic event in the reasoning agent's execution log."""

    step: int
    action: ReasoningActionType
    goal_id: Optional[str]
    details: Dict[str, Any]
    ledger_snapshot: Dict[str, Any]


@dataclass(frozen=True)
class GoalOutcome:
    """The resolved outcome of a candidate goal."""

    goal_id: str
    status: str  # "SOLVED", "CERTIFIED_REFUSED", "BUDGET_EXHAUSTED"
    path: Optional[Tuple[MoveEdge, ...]]
    cost: Optional[Fraction]
    receipt: Optional[Union[DualityGapReceipt, DualRefusalReceipt, HierarchicalRefusalReceipt]]
    fine_nodes_explored: int
    coarse_pruned: bool
    budget_allocated: Fraction
    budget_consumed: Fraction


@dataclass(frozen=True)
class ReasoningAgentReceipt:
    """Cryptographically verifiable execution receipt of the autonomous reasoning engine."""

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


class AutonomousReasoningAgent:
    """Autonomous multi-scale reasoning agent with adaptive budget re-allocation."""

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
    ) -> Tuple[Dict[str, GoalOutcome], ReasoningAgentReceipt]:
        """Execute the autonomous reasoning workflow across candidate goals."""
        if not goals:
            return {}, ReasoningAgentReceipt(
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

        # 1. Phase 1: Initial Priority-Weighted Budget Allocation
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
        coarse_bounds: Dict[str, Fraction] = {}

        coarse_s = self.coarsening_map.apply_state(source)

        # 2. Phase 2: Coarse Continuous Dual Screening & Certified Pruning
        for g in goals:
            alloc = self.ledger.allocated_budgets[g.goal_id]
            coarse_t = self.coarsening_map.apply_state(g.target)

            # Compute coarse dual relaxation
            coarse_dual = DualRelaxationSolver.compute_dual_potential(
                self.coarse_graph, coarse_s, cost_fn=self.cost_fn
            )
            coarse_bound = coarse_dual.potential_difference(coarse_s, coarse_t)

            self._record_event(
                ReasoningActionType.COARSE_PROBE,
                g.goal_id,
                {"coarse_bound": str(coarse_bound) if coarse_bound is not None else "disconnected"},
            )

            # Check if provably unreachable under allocated budget
            if coarse_bound is None or coarse_bound > alloc:
                # Certified hierarchical refusal: 0 fine nodes explored
                refusal_rcpt = HierarchicalRefusalReceipt(
                    coarse_level=self.coarse_scale,
                    fine_level=self.fine_scale,
                    source=source,
                    target=g.target,
                    coarse_source=coarse_s,
                    coarse_target=coarse_t,
                    budget=alloc,
                    coarse_dual_bound=coarse_bound if coarse_bound is not None else Fraction(-1, 1),
                    pruned_levels=(self.fine_scale,),
                    reason="Coarse dual lower bound exceeds allocated budget; fine search pruned",
                )
                reclaimed = self.ledger.reclaim(g.goal_id)
                self._total_reclaimed += reclaimed

                self._record_event(
                    ReasoningActionType.CERTIFIED_REFUSAL,
                    g.goal_id,
                    {"reclaimed": str(reclaimed), "reason": refusal_rcpt.reason},
                )

                outcomes[g.goal_id] = GoalOutcome(
                    goal_id=g.goal_id,
                    status="CERTIFIED_REFUSED",
                    path=None,
                    cost=None,
                    receipt=refusal_rcpt,
                    fine_nodes_explored=0,
                    coarse_pruned=True,
                    budget_allocated=alloc,
                    budget_consumed=Fraction(0, 1),
                )
            else:
                viable_goals.append(g)
                coarse_bounds[g.goal_id] = coarse_bound

        # 3. Phase 3: Adaptive Budget Re-allocation
        if viable_goals and self.ledger.unallocated_budget > 0:
            reclaimed_pool = self.ledger.unallocated_budget
            # Re-allocate reclaimed funds inversely proportional to coarse bound, weighted by priority
            # Lower bound means closer target -> higher priority for execution
            weights: Dict[str, Fraction] = {}
            for g in viable_goals:
                dist = coarse_bounds[g.goal_id]
                # Avoid division by zero: weight = priority / (dist + 1/2)
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

        # 4. Phase 4: Coarse-Guided Fine-Scale Execution
        # Sort viable goals by coarse bound ascending (closest first)
        viable_goals.sort(key=lambda g: coarse_bounds[g.goal_id])

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
                # Path found within budget
                actual_cost = sum((self.cost_fn(e) for e in result.path), Fraction(0, 1))
                self.ledger.consume(g.goal_id, actual_cost)

                # Reclaim remaining unused budget and re-allocate to subsequent viable goals
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

                # Dynamically redistribute remainder to remaining viable goals that haven't been run yet
                remaining_unrun = [
                    rem.goal_id
                    for rem in viable_goals
                    if rem.goal_id not in outcomes and rem.goal_id != g.goal_id
                ]
                if remaining_unrun and self.ledger.unallocated_budget > 0:
                    self.ledger.redistribute_unallocated(remaining_unrun)
            else:
                # Search failed or budget exhausted
                self.ledger.consume(g.goal_id, current_budget)
                self._record_event(
                    ReasoningActionType.BUDGET_EXHAUSTION,
                    g.goal_id,
                    {"nodes_explored": result.nodes_explored},
                )

                outcomes[g.goal_id] = GoalOutcome(
                    goal_id=g.goal_id,
                    status="BUDGET_EXHAUSTED",
                    path=None,
                    cost=None,
                    receipt=result.receipt,
                    fine_nodes_explored=result.nodes_explored,
                    coarse_pruned=result.coarse_pruned,
                    budget_allocated=current_budget,
                    budget_consumed=current_budget,
                )

        # 5. Final Audit and Verification Receipt
        conservation_ok = self.ledger.audit_conservation()
        if not conservation_ok:
            raise RuntimeError(
                f"Budget conservation violated: total={self.ledger.total_budget}, "
                f"unallocated={self.ledger.unallocated_budget}, "
                f"allocated={self.ledger.allocated_budgets}, "
                f"consumed={self.ledger.consumed_budget}"
            )

        # Compute trace digest
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

        receipt = ReasoningAgentReceipt(
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
