"""Verified coarse-to-fine search over finite movegraphs.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero
floats in logical decisions.

A coarse potential is used for pruning or guidance only after two executable
checks: the projection is a movegraph morphism, and the lifted potential obeys
the fine cost inequality on every edge in its reachable domain. If the latter
check fails, the implementation falls back to an unguided exact fine search.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from .dual_relaxation import (
    DualPotential,
    DualRefusalReceipt,
    ExactPathSolver,
    DualityGapReceipt,
    _default_cost_fn,
    _validate_graph_costs,
    _validated_cost,
)
from .projective_system import CoarseningMap, MoveEdge, MoveGraph, _to_fraction


@dataclass(frozen=True)
class CoarseCertificateInspection:
    """Runtime evidence governing whether a coarse potential may be lifted."""

    coarse_source: Any
    coarse_target: Any
    coarse_bound: Optional[Fraction]
    morphism_verified: bool
    lifted_admissibility_verified: bool
    defects: Tuple[str, ...]


@dataclass(frozen=True)
class HierarchicalRefusalReceipt:
    """Refusal justified by a checked projection fact or lifted lower bound."""

    coarse_level: int
    fine_level: int
    source: Any
    target: Any
    coarse_source: Any
    coarse_target: Any
    budget: Optional[Fraction]
    coarse_dual_bound: Optional[Fraction]
    pruned_levels: Tuple[int, ...]
    refusal_basis: str
    morphism_verified: bool
    lifted_admissibility_verified: bool
    certified_refusal: bool = True
    reason: str = "Checked coarse certificate refuses fine search"


@dataclass(frozen=True)
class SearchExhaustionReceipt:
    """Receipt from complete finite search, optionally restricted by a budget."""

    source: Any
    target: Any
    budget: Optional[Fraction]
    nodes_explored: int
    certified_refusal: bool
    reason: str


SearchReceipt = Union[
    DualityGapReceipt,
    DualRefusalReceipt,
    HierarchicalRefusalReceipt,
    SearchExhaustionReceipt,
]


@dataclass(frozen=True)
class HierarchicalSearchResult:
    """Outcome of hierarchical multi-scale search with certificate and search telemetry."""

    path: Optional[Tuple[MoveEdge, ...]]
    receipt: SearchReceipt
    nodes_explored: int
    coarse_pruned: bool
    repeated_state_cycles_pruned: int
    coarse_certificate: CoarseCertificateInspection


class HierarchicalSearchEngine:
    """Use checked coarse information when sound, otherwise exact fine search."""

    @staticmethod
    def _inspect_with_dual(
        fine_graph: MoveGraph,
        coarse_graph: MoveGraph,
        coarsening_map: CoarseningMap,
        source: Any,
        target: Any,
        cost_fn: Callable[[MoveEdge], Fraction],
    ) -> Tuple[CoarseCertificateInspection, DualPotential]:
        """Verify the projection and every relevant lifted edge inequality."""
        morphism = coarsening_map.check_morphism(fine_graph, coarse_graph)
        if not morphism.is_valid:
            detail = "; ".join(morphism.defects)
            raise ValueError(f"Coarsening map failed morphism verification: {detail}")

        coarse_source = coarsening_map.apply_state(source)
        coarse_target = coarsening_map.apply_state(target)
        coarse_dual = ExactPathSolver.compute_dual_potential(
            coarse_graph, coarse_source, cost_fn=cost_fn
        )
        coarse_bound = coarse_dual.potential_difference(coarse_source, coarse_target)

        defects: List[str] = []
        for edge in fine_graph.edges:
            fine_cost = _validated_cost(edge, cost_fn)
            image_source = coarsening_map.apply_state(edge.source)
            image_target = coarsening_map.apply_state(edge.target)
            y_source = coarse_dual.get(image_source)
            y_target = coarse_dual.get(image_target)

            # The potential is partial outside the projected source's reachable
            # component. Such edges cannot occur on a projected source path.
            if y_source is None:
                continue
            if y_target is None:
                defects.append(
                    "Lifted reachable domain is not closed on fine edge "
                    f"{edge.source!r} -> {edge.target!r}"
                )
                continue

            lifted_difference = y_target - y_source
            if lifted_difference > fine_cost:
                defects.append(
                    f"Lifted potential violates fine edge {edge.source!r} -> "
                    f"{edge.target!r}: difference {lifted_difference} > cost {fine_cost}"
                )

        inspection = CoarseCertificateInspection(
            coarse_source=coarse_source,
            coarse_target=coarse_target,
            coarse_bound=coarse_bound,
            morphism_verified=True,
            lifted_admissibility_verified=not defects,
            defects=tuple(defects),
        )
        return inspection, coarse_dual

    @classmethod
    def inspect_coarse_certificate(
        cls,
        fine_graph: MoveGraph,
        coarse_graph: MoveGraph,
        coarsening_map: CoarseningMap,
        source: Any,
        target: Any,
        cost_fn: Callable[[MoveEdge], Fraction] = _default_cost_fn,
    ) -> CoarseCertificateInspection:
        """Return the checks that govern coarse pruning for one source-target pair."""
        if not fine_graph.has_state(source):
            raise KeyError(f"Source state {source!r} not in fine graph")
        if not fine_graph.has_state(target):
            raise KeyError(f"Target state {target!r} not in fine graph")
        _validate_graph_costs(fine_graph, cost_fn)
        _validate_graph_costs(coarse_graph, cost_fn)
        inspection, _ = cls._inspect_with_dual(
            fine_graph,
            coarse_graph,
            coarsening_map,
            source,
            target,
            cost_fn,
        )
        return inspection

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
        """Search a fine graph, using coarse data only after runtime checks."""
        if not fine_graph.has_state(source):
            raise KeyError(f"Source state {source!r} not in fine graph")
        if not fine_graph.has_state(target):
            raise KeyError(f"Target state {target!r} not in fine graph")

        q_budget = _to_fraction(budget, "budget") if budget is not None else None
        if q_budget is not None and q_budget < 0:
            raise ValueError(f"budget cannot be negative: {q_budget}")

        _validate_graph_costs(fine_graph, cost_fn)
        _validate_graph_costs(coarse_graph, cost_fn)
        inspection, coarse_dual = cls._inspect_with_dual(
            fine_graph,
            coarse_graph,
            coarsening_map,
            source,
            target,
            cost_fn,
        )
        coarse_source = inspection.coarse_source
        coarse_target = inspection.coarse_target
        coarse_bound = inspection.coarse_bound

        # A valid morphism maps every fine path to a coarse walk (with collapsed
        # steps allowed), so projected unreachability is enough on its own.
        if coarse_bound is None:
            refusal = HierarchicalRefusalReceipt(
                coarse_level=coarse_graph.level,
                fine_level=fine_graph.level,
                source=source,
                target=target,
                coarse_source=coarse_source,
                coarse_target=coarse_target,
                budget=q_budget,
                coarse_dual_bound=None,
                pruned_levels=(fine_graph.level,),
                refusal_basis="projected_unreachability",
                morphism_verified=True,
                lifted_admissibility_verified=inspection.lifted_admissibility_verified,
                reason="Coarse target is unreachable under the verified movegraph morphism",
            )
            return HierarchicalSearchResult(
                path=None,
                receipt=refusal,
                nodes_explored=0,
                coarse_pruned=True,
                repeated_state_cycles_pruned=0,
                coarse_certificate=inspection,
            )

        # A numerical coarse bound is safe only when its lifted potential
        # satisfies every relevant fine edge inequality.
        if (
            q_budget is not None
            and inspection.lifted_admissibility_verified
            and coarse_bound > q_budget
        ):
            refusal = HierarchicalRefusalReceipt(
                coarse_level=coarse_graph.level,
                fine_level=fine_graph.level,
                source=source,
                target=target,
                coarse_source=coarse_source,
                coarse_target=coarse_target,
                budget=q_budget,
                coarse_dual_bound=coarse_bound,
                pruned_levels=(fine_graph.level,),
                refusal_basis="verified_lifted_lower_bound",
                morphism_verified=True,
                lifted_admissibility_verified=True,
                reason=f"Verified lifted lower bound {coarse_bound} exceeds budget {q_budget}",
            )
            return HierarchicalSearchResult(
                path=None,
                receipt=refusal,
                nodes_explored=0,
                coarse_pruned=True,
                repeated_state_cycles_pruned=0,
                coarse_certificate=inspection,
            )

        def heuristic(state: Any) -> Fraction:
            if not inspection.lifted_admissibility_verified:
                return Fraction(0, 1)
            image = coarsening_map.apply_state(state)
            difference = coarse_dual.potential_difference(image, coarse_target)
            if difference is None or difference <= 0:
                return Fraction(0, 1)
            return difference

        counter = 0
        start_cost = Fraction(0, 1)
        queue: List[Tuple[Fraction, int, Fraction, Any, Tuple[MoveEdge, ...]]] = [
            (start_cost + heuristic(source), counter, start_cost, source, ())
        ]
        best_cost: Dict[Any, Fraction] = {source: start_cost}
        nodes_explored = 0
        repeated_cycles_pruned = 0

        while queue:
            _, _, current_cost, state, path_so_far = heapq.heappop(queue)
            if current_cost != best_cost.get(state):
                continue
            nodes_explored += 1

            if state == target:
                fine_dual = ExactPathSolver.compute_dual_potential(
                    fine_graph, source, cost_fn=cost_fn
                )
                fine_bound = fine_dual.potential_difference(source, target)
                if fine_bound is None:
                    raise RuntimeError("Reached target is missing from exact fine potential")
                gap = current_cost - fine_bound
                receipt = DualityGapReceipt(
                    source=source,
                    target=target,
                    primal_cost=current_cost,
                    dual_bound=fine_bound,
                    duality_gap=gap,
                    is_optimal=(gap == 0),
                    is_reachable=True,
                )
                return HierarchicalSearchResult(
                    path=path_so_far,
                    receipt=receipt,
                    nodes_explored=nodes_explored,
                    coarse_pruned=False,
                    repeated_state_cycles_pruned=repeated_cycles_pruned,
                    coarse_certificate=inspection,
                )

            path_states = {edge.source for edge in path_so_far}
            path_states.add(state)
            for edge in fine_graph.outgoing(state):
                next_state = edge.target
                edge_cost = _validated_cost(edge, cost_fn)
                next_cost = current_cost + edge_cost

                if q_budget is not None and next_cost > q_budget:
                    continue
                if next_state in path_states:
                    repeated_cycles_pruned += 1
                    continue
                if next_state not in best_cost or next_cost < best_cost[next_state]:
                    best_cost[next_state] = next_cost
                    counter += 1
                    heapq.heappush(
                        queue,
                        (
                            next_cost + heuristic(next_state),
                            counter,
                            next_cost,
                            next_state,
                            path_so_far + (edge,),
                        ),
                    )

        reason = (
            f"Complete finite search found no path with cost at most {q_budget}"
            if q_budget is not None
            else "Complete finite search found no source-target path"
        )
        search_refusal = SearchExhaustionReceipt(
            source=source,
            target=target,
            budget=q_budget,
            nodes_explored=nodes_explored,
            certified_refusal=True,
            reason=reason,
        )
        return HierarchicalSearchResult(
            path=None,
            receipt=search_refusal,
            nodes_explored=nodes_explored,
            coarse_pruned=False,
            repeated_state_cycles_pruned=repeated_cycles_pruned,
            coarse_certificate=inspection,
        )
