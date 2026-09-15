"""Hierarchical Multi-Scale Search Engine with Coarsening Pruning & Cycle Filtering.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple, Union

from .dual_relaxation import (
    DualPotential,
    DualRefusalReceipt,
    DualRelaxationSolver,
    DualityGapReceipt,
    _default_cost_fn,
)
from .projective_system import CoarseningMap, MoveEdge, MoveGraph, _to_fraction


@dataclass(frozen=True)
class HierarchicalRefusalReceipt:
    """Certified hierarchical refusal pruning fine-scale search via coarse dual potential."""

    coarse_level: int
    fine_level: int
    source: Any
    target: Any
    coarse_source: Any
    coarse_target: Any
    budget: Fraction
    coarse_dual_bound: Fraction
    pruned_levels: Tuple[int, ...]
    certified_refusal: bool = True
    reason: str = "Coarse dual lower bound strictly exceeds budget"


@dataclass(frozen=True)
class HierarchicalSearchResult:
    """Outcome of hierarchical multi-scale search with certificate and search telemetry."""

    path: Optional[Tuple[MoveEdge, ...]]
    receipt: Union[DualityGapReceipt, DualRefusalReceipt, HierarchicalRefusalReceipt]
    nodes_explored: int
    coarse_pruned: bool
    dissipative_cycles_pruned: int


class HierarchicalSearchEngine:
    """Solver engine combining continuous dual relaxation, coarsening morphisms, and cycle filtering."""

    @classmethod
    def search_with_coarse_pruning(
        cls,
        fine_graph: MoveGraph,
        coarse_graph: MoveGraph,
        coarsening_map: CoarseningMap,
        source: Any,
        target: Any,
        budget: Optional[Union[Fraction, int]] = None,
        cost_fn: Callable[[MoveEdge], Fraction] = _default_cost_fn,
    ) -> HierarchicalSearchResult:
        """Search fine movegraph with hierarchical coarse-level pruning and cycle filtering."""
        q_budget = _to_fraction(budget, "budget") if budget is not None else None

        if not fine_graph.has_state(source):
            raise KeyError(f"Source state {source!r} not in fine graph")
        if not fine_graph.has_state(target):
            raise KeyError(f"Target state {target!r} not in fine graph")

        coarse_s = coarsening_map.apply_state(source)
        coarse_t = coarsening_map.apply_state(target)

        # 1. Stage 1: Coarse Continuous Dual Relaxation
        coarse_dual = DualRelaxationSolver.compute_dual_potential(
            coarse_graph, coarse_s, cost_fn=cost_fn
        )
        coarse_bound = coarse_dual.potential_difference(coarse_s, coarse_t)

        # 2. Stage 2: Coarse Pruning Check
        if coarse_bound is None:
            # Coarse target completely disconnected; fine target must be disconnected
            refusal = HierarchicalRefusalReceipt(
                coarse_level=coarse_graph.level,
                fine_level=fine_graph.level,
                source=source,
                target=target,
                coarse_source=coarse_s,
                coarse_target=coarse_t,
                budget=q_budget if q_budget is not None else Fraction(0, 1),
                coarse_dual_bound=Fraction(-1, 1),
                pruned_levels=(fine_graph.level,),
                reason="Coarse target unreachable; fine search pruned",
            )
            return HierarchicalSearchResult(
                path=None,
                receipt=refusal,
                nodes_explored=0,
                coarse_pruned=True,
                dissipative_cycles_pruned=0,
            )

        if q_budget is not None and coarse_bound > q_budget:
            # Certified coarse Farkas separation: coarse lower bound > budget
            refusal = HierarchicalRefusalReceipt(
                coarse_level=coarse_graph.level,
                fine_level=fine_graph.level,
                source=source,
                target=target,
                coarse_source=coarse_s,
                coarse_target=coarse_t,
                budget=q_budget,
                coarse_dual_bound=coarse_bound,
                pruned_levels=(fine_graph.level,),
                reason=f"Coarse dual bound {coarse_bound} exceeds budget {q_budget}; fine search pruned",
            )
            return HierarchicalSearchResult(
                path=None,
                receipt=refusal,
                nodes_explored=0,
                coarse_pruned=True,
                dissipative_cycles_pruned=0,
            )

        # 3. Stage 3: Fine-scale Guided Search with Dissipative Cycle Filtering
        # Heuristic h(u) = coarse_dual.potential_difference(pi(u), pi(target))
        def heuristic(u: Any) -> Fraction:
            c_u = coarsening_map.apply_state(u)
            diff = coarse_dual.potential_difference(c_u, coarse_t)
            return diff if diff is not None and diff > 0 else Fraction(0, 1)

        # Priority queue: (f_score, counter, g_score, state, path_tuple, visited_path_states)
        counter = 0
        g_start = Fraction(0, 1)
        f_start = g_start + heuristic(source)
        # Store (f_score, counter, g_score, state, path_edges)
        pq: List[Tuple[Fraction, int, Fraction, Any, Tuple[MoveEdge, ...]]] = [
            (f_start, counter, g_start, source, ())
        ]

        best_g: Dict[Any, Fraction] = {source: g_start}
        nodes_explored = 0
        cycles_pruned = 0

        while pq:
            f_u, _, g_u, u, path_so_far = heapq.heappop(pq)
            nodes_explored += 1

            if u == target:
                # Target reached! Compute duality gap against fine dual
                fine_dual = DualRelaxationSolver.compute_dual_potential(
                    fine_graph, source, cost_fn=cost_fn
                )
                fine_bound = fine_dual.potential_difference(source, target)
                duality_gap = g_u - fine_bound if fine_bound is not None else Fraction(0, 1)
                receipt = DualityGapReceipt(
                    source=source,
                    target=target,
                    primal_cost=g_u,
                    dual_bound=fine_bound,
                    duality_gap=duality_gap,
                    is_optimal=(duality_gap == 0),
                    is_reachable=True,
                )
                return HierarchicalSearchResult(
                    path=path_so_far,
                    receipt=receipt,
                    nodes_explored=nodes_explored,
                    coarse_pruned=False,
                    dissipative_cycles_pruned=cycles_pruned,
                )

            if g_u > best_g.get(u, g_u):
                continue

            for edge in fine_graph.outgoing(u):
                v = edge.target
                w = cost_fn(edge)
                g_v = g_u + w

                # Check budget exhaustion
                if q_budget is not None and g_v > q_budget:
                    continue

                # Dissipative cycle filter: check if v is already in current path
                path_states = {e.source for e in path_so_far}
                path_states.add(u)
                if v in path_states:
                    # Dissipative loop detected (potential mu1 or action mu2 burned without progression)
                    cycles_pruned += 1
                    continue

                if v not in best_g or g_v < best_g[v]:
                    best_g[v] = g_v
                    f_v = g_v + heuristic(v)
                    counter += 1
                    new_path = path_so_far + (edge,)
                    heapq.heappush(pq, (f_v, counter, g_v, v, new_path))

        # Target not reached
        refusal_receipt = DualRefusalReceipt(
            source=source,
            target=target,
            budget=q_budget if q_budget is not None else Fraction(0, 1),
            dual_bound=None,
            certified_refusal=True,
            reason="Search exhausted without reaching target",
        )
        return HierarchicalSearchResult(
            path=None,
            receipt=refusal_receipt,
            nodes_explored=nodes_explored,
            coarse_pruned=False,
            dissipative_cycles_pruned=cycles_pruned,
        )
