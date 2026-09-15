"""Continuous Relaxation & Dual Potential Solver over discrete movegraphs.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from fractions import Fraction
from types import MappingProxyType
from typing import Any, Callable, Dict, Iterator, List, Mapping, Optional, Sequence, Set, Tuple, Union

from .projective_system import MoveEdge, MoveGraph, _to_fraction


def _default_cost_fn(e: MoveEdge) -> Fraction:
    """Default operational cost function extracting mu1 as exact Fraction."""
    return _to_fraction(e.mu1, "mu1")


@dataclass(frozen=True)
class DualPotential:
    """Exact rational dual potential vector y: V -> Q on a movegraph.

    Satisfies the continuous relaxation admissibility condition:
      y(v) - y(u) <= cost(u, v) for all directed edges e = (u, v).
    """

    source: Any
    potentials: Mapping[Any, Fraction]

    def __post_init__(self) -> None:
        if self.source not in self.potentials:
            raise ValueError(f"source {self.source!r} must be in potentials mapping")
        # Ensure mapping is immutable and values are exact non-negative fractions
        clean_pot: Dict[Any, Fraction] = {}
        for k, v in self.potentials.items():
            clean_pot[k] = _to_fraction(v, f"potential[{k!r}]")
        object.__setattr__(self, "potentials", MappingProxyType(clean_pot))

    def get(self, state: Any) -> Optional[Fraction]:
        """Return potential of state, or None if state is unreachable/unassigned."""
        return self.potentials.get(state)

    def potential_difference(self, from_state: Any, to_state: Any) -> Optional[Fraction]:
        """Return y(to_state) - y(from_state), or None if either state is unassigned."""
        y_from = self.get(from_state)
        y_to = self.get(to_state)
        if y_from is None or y_to is None:
            return None
        return y_to - y_from

    def verify_admissibility(
        self,
        graph: MoveGraph,
        cost_fn: Callable[[MoveEdge], Fraction] = _default_cost_fn,
    ) -> Tuple[bool, Tuple[str, ...]]:
        """Verify the dual admissibility condition y(v) - y(u) <= cost(u, v) for all edges."""
        defects: List[str] = []
        for e in graph.edges:
            y_u = self.get(e.source)
            y_v = self.get(e.target)
            if y_u is not None and y_v is not None:
                diff = y_v - y_u
                c = cost_fn(e)
                if diff > c:
                    defects.append(
                        f"Admissibility violated on edge {e.source!r} -> {e.target!r}: "
                        f"y(v) - y(u) = {diff} > cost = {c}"
                    )
        return len(defects) == 0, tuple(defects)


@dataclass(frozen=True)
class DualityGapReceipt:
    """Exact rational duality gap receipt certifying path optimality or bound tightness."""

    source: Any
    target: Any
    primal_cost: Optional[Fraction]
    dual_bound: Optional[Fraction]
    duality_gap: Optional[Fraction]
    is_optimal: bool
    is_reachable: bool


@dataclass(frozen=True)
class DualRefusalReceipt:
    """Certified Farkas unreachability/budget-exhaustion receipt.

    Certifies that for any path p from source to target, cost(p) >= dual_bound > budget.
    """

    source: Any
    target: Any
    budget: Fraction
    dual_bound: Optional[Fraction]
    certified_refusal: bool
    reason: str


class DualRelaxationSolver:
    """Continuous relaxation solver computing exact rational dual potentials and certificates."""

    @classmethod
    def compute_dual_potential(
        cls,
        graph: MoveGraph,
        source: Any,
        cost_fn: Callable[[MoveEdge], Fraction] = _default_cost_fn,
    ) -> DualPotential:
        """Compute the maximal admissible dual potential rooted at source via exact rational Dijkstra."""
        if not graph.has_state(source):
            raise KeyError(f"Source state {source!r} not in graph")

        dist: Dict[Any, Fraction] = {source: Fraction(0, 1)}
        counter = 0
        pq: List[Tuple[Fraction, int, Any]] = [(Fraction(0, 1), counter, source)]
        visited: Set[Any] = set()

        while pq:
            d_u, _, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)

            for edge in graph.outgoing(u):
                v = edge.target
                w = cost_fn(edge)
                if w < 0:
                    raise ValueError(f"Negative edge cost {w} encountered on edge {edge!r}")
                d_v = d_u + w
                if v not in dist or d_v < dist[v]:
                    dist[v] = d_v
                    counter += 1
                    heapq.heappush(pq, (d_v, counter, v))

        return DualPotential(source=source, potentials=dist)

    @classmethod
    def solve_shortest_path(
        cls,
        graph: MoveGraph,
        source: Any,
        target: Any,
        cost_fn: Callable[[MoveEdge], Fraction] = _default_cost_fn,
    ) -> Tuple[Optional[Tuple[MoveEdge, ...]], Optional[Fraction]]:
        """Find the exact rational shortest path and its total cost from source to target."""
        if not graph.has_state(source):
            raise KeyError(f"Source state {source!r} not in graph")
        if not graph.has_state(target):
            raise KeyError(f"Target state {target!r} not in graph")

        if source == target:
            return (), Fraction(0, 1)

        dist: Dict[Any, Fraction] = {source: Fraction(0, 1)}
        parent_edge: Dict[Any, MoveEdge] = {}
        counter = 0
        pq: List[Tuple[Fraction, int, Any]] = [(Fraction(0, 1), counter, source)]
        visited: Set[Any] = set()

        while pq:
            d_u, _, u = heapq.heappop(pq)
            if u == target:
                break
            if u in visited:
                continue
            visited.add(u)

            for edge in graph.outgoing(u):
                v = edge.target
                w = cost_fn(edge)
                d_v = d_u + w
                if v not in dist or d_v < dist[v]:
                    dist[v] = d_v
                    parent_edge[v] = edge
                    counter += 1
                    heapq.heappush(pq, (d_v, counter, v))

        if target not in dist:
            return None, None

        # Reconstruct path
        path_edges: List[MoveEdge] = []
        curr = target
        while curr != source:
            e = parent_edge[curr]
            path_edges.append(e)
            curr = e.source
        path_edges.reverse()
        return tuple(path_edges), dist[target]

    @classmethod
    def solve_primal_dual(
        cls,
        graph: MoveGraph,
        source: Any,
        target: Any,
        budget: Optional[Union[Fraction, int]] = None,
        cost_fn: Callable[[MoveEdge], Fraction] = _default_cost_fn,
    ) -> Tuple[Optional[Tuple[MoveEdge, ...]], Union[DualityGapReceipt, DualRefusalReceipt]]:
        """Compute the primal solution alongside its certified dual receipt or refusal."""
        q_budget = _to_fraction(budget, "budget") if budget is not None else None

        # 1. Compute dual potential from source
        dual = cls.compute_dual_potential(graph, source, cost_fn=cost_fn)
        dual_bound = dual.potential_difference(source, target)

        # 2. Check if target is unreachable or exceeds declared budget
        if dual_bound is None:
            # Target completely unreachable
            if q_budget is not None:
                refusal = DualRefusalReceipt(
                    source=source,
                    target=target,
                    budget=q_budget,
                    dual_bound=None,
                    certified_refusal=True,
                    reason="Target unreachable in movegraph topology",
                )
                return None, refusal
            else:
                receipt = DualityGapReceipt(
                    source=source,
                    target=target,
                    primal_cost=None,
                    dual_bound=None,
                    duality_gap=None,
                    is_optimal=False,
                    is_reachable=False,
                )
                return None, receipt

        if q_budget is not None and dual_bound > q_budget:
            # Certified Farkas separation: dual lower bound strictly exceeds budget
            refusal = DualRefusalReceipt(
                source=source,
                target=target,
                budget=q_budget,
                dual_bound=dual_bound,
                certified_refusal=True,
                reason=f"Dual lower bound {dual_bound} strictly exceeds allocated budget {q_budget}",
            )
            return None, refusal

        # 3. Target is reachable within budget; compute primal path
        path, primal_cost = cls.solve_shortest_path(graph, source, target, cost_fn=cost_fn)
        if path is None or primal_cost is None:
            raise RuntimeError("Consistency defect: dual bound exists but primal path missing")

        duality_gap = primal_cost - dual_bound
        receipt = DualityGapReceipt(
            source=source,
            target=target,
            primal_cost=primal_cost,
            dual_bound=dual_bound,
            duality_gap=duality_gap,
            is_optimal=(duality_gap == 0),
            is_reachable=True,
        )
        return path, receipt

    @classmethod
    def verify_path_against_dual(
        cls,
        path: Sequence[MoveEdge],
        dual: DualPotential,
        source: Any,
        target: Any,
        cost_fn: Callable[[MoveEdge], Fraction] = _default_cost_fn,
    ) -> Tuple[bool, Fraction, Optional[Fraction], Optional[Fraction]]:
        """Independently verify path validity and compute exact duality gap in O(len(path)).

        Returns:
            (is_valid, primal_cost, dual_bound, duality_gap)
        """
        if not path:
            if source == target:
                return True, Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)
            return False, Fraction(0, 1), None, None

        if path[0].source != source or path[-1].target != target:
            return False, Fraction(0, 1), None, None

        total_cost = Fraction(0, 1)
        for i in range(len(path)):
            e = path[i]
            total_cost += cost_fn(e)
            if i + 1 < len(path):
                if e.target != path[i + 1].source:
                    return False, Fraction(0, 1), None, None

        dual_bound = dual.potential_difference(source, target)
        if dual_bound is None:
            return True, total_cost, None, None

        gap = total_cost - dual_bound
        if gap < 0:
            raise ValueError(f"Duality violation: primal cost {total_cost} < dual bound {dual_bound}")

        return True, total_cost, dual_bound, gap
