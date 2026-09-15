"""Empirical Benchmarking Suite: Hierarchical Dual-Certified Solver vs. Un-relaxed Search.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats in logical decisions.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .dual_relaxation import DualRelaxationSolver, DualityGapReceipt
from .hierarchical_search import HierarchicalRefusalReceipt, HierarchicalSearchEngine
from .interval_domain import (
    DyadicInterval,
    create_interval_coarsening_map,
    create_interval_movegraph,
)
from .projective_system import MoveEdge, MoveGraph


@dataclass(frozen=True)
class ScaleBenchmarkResult:
    """Benchmark outcome for a single scale depth k."""

    scale: int
    num_intervals: int
    num_edges: int
    unrelaxed_nodes_explored: int
    hierarchical_nodes_explored: int
    node_reduction_ratio: float
    unrelaxed_time_ms: float
    hierarchical_time_ms: float
    speedup_ratio: float
    certified_outcome: str


@dataclass(frozen=True)
class BenchmarkReport:
    """Consolidated empirical benchmark report across multiple scale depths."""

    scales: Tuple[int, ...]
    refusal_benchmarks: Tuple[ScaleBenchmarkResult, ...]
    guided_benchmarks: Tuple[ScaleBenchmarkResult, ...]


def run_unrelaxed_search(
    graph: MoveGraph,
    source: Any,
    target: Any,
    budget: Optional[Fraction] = None,
) -> Tuple[Optional[Tuple[MoveEdge, ...]], int]:
    """Un-relaxed discrete Dijkstra/BFS search expanding nodes blindly without dual or coarse guidance."""
    import heapq

    if not graph.has_state(source) or not graph.has_state(target):
        return None, 0

    dist: Dict[Any, Fraction] = {source: Fraction(0, 1)}
    parent: Dict[Any, MoveEdge] = {}
    counter = 0
    pq: List[Tuple[Fraction, int, Any]] = [(Fraction(0, 1), counter, source)]
    visited = set()
    nodes_explored = 0

    while pq:
        d_u, _, u = heapq.heappop(pq)
        nodes_explored += 1
        if u == target:
            break
        if u in visited:
            continue
        visited.add(u)

        for edge in graph.outgoing(u):
            v = edge.target
            w = edge.mu1
            d_v = d_u + w
            if budget is not None and d_v > budget:
                continue
            if v not in dist or d_v < dist[v]:
                dist[v] = d_v
                parent[v] = edge
                counter += 1
                heapq.heappush(pq, (d_v, counter, v))

    if target not in dist:
        return None, nodes_explored

    path = []
    curr = target
    while curr != source:
        e = parent[curr]
        path.append(e)
        curr = e.source
    path.reverse()
    return tuple(path), nodes_explored


def run_hierarchical_benchmark(
    scales: Sequence[int] = (4, 6, 8),
    coarse_scale: int = 2,
) -> BenchmarkReport:
    """Run empirical benchmark comparing hierarchical dual-certified search vs un-relaxed search.

    Tests both:
    1. Early Refusal Benchmark: Bounded insufficient budget where coarse dual potential prunes.
    2. Guided Search Benchmark: Reachable target where coarse heuristic guides fine-scale A*.
    """
    refusal_results: List[ScaleBenchmarkResult] = []
    guided_results: List[ScaleBenchmarkResult] = []

    for k in scales:
        coarse_mg = create_interval_movegraph(scale=coarse_scale)
        fine_mg = create_interval_movegraph(scale=k)
        cmap = create_interval_coarsening_map(coarse_scale=coarse_scale, fine_scale=k)

        num_int = (1 << k) - 1
        num_edg = len(fine_mg.edges)
        s = DyadicInterval(scale=k, index=0)
        t = DyadicInterval(scale=k, index=num_int - 1)

        # Scenario 1: Early Refusal Benchmark
        # Required cost is (2^k - 2)/2^k ~ 1. Allocate insufficient budget 1/4.
        refusal_budget = Fraction(1, 4)

        t0 = time.perf_counter()
        _, unrelaxed_nodes_refusal = run_unrelaxed_search(fine_mg, s, t, budget=refusal_budget)
        t1 = time.perf_counter()
        unrelaxed_time_refusal = (t1 - t0) * 1000.0

        t2 = time.perf_counter()
        hier_res_refusal = HierarchicalSearchEngine.search_with_coarse_pruning(
            fine_graph=fine_mg,
            coarse_graph=coarse_mg,
            coarsening_map=cmap,
            source=s,
            target=t,
            budget=refusal_budget,
        )
        t3 = time.perf_counter()
        hier_time_refusal = (t3 - t2) * 1000.0

        hier_nodes_refusal = hier_res_refusal.nodes_explored
        red_refusal = (
            float(unrelaxed_nodes_refusal - hier_nodes_refusal) / float(unrelaxed_nodes_refusal)
            if unrelaxed_nodes_refusal > 0
            else 0.0
        )
        speedup_refusal = (
            unrelaxed_time_refusal / hier_time_refusal if hier_time_refusal > 0 else 1.0
        )

        refusal_results.append(
            ScaleBenchmarkResult(
                scale=k,
                num_intervals=num_int,
                num_edges=num_edg,
                unrelaxed_nodes_explored=unrelaxed_nodes_refusal,
                hierarchical_nodes_explored=hier_nodes_refusal,
                node_reduction_ratio=red_refusal,
                unrelaxed_time_ms=unrelaxed_time_refusal,
                hierarchical_time_ms=hier_time_refusal,
                speedup_ratio=speedup_refusal,
                certified_outcome=type(hier_res_refusal.receipt).__name__,
            )
        )

        # Scenario 2: Guided Reachable Search Benchmark
        sufficient_budget = Fraction(1, 1)

        t4 = time.perf_counter()
        _, unrelaxed_nodes_guided = run_unrelaxed_search(fine_mg, s, t, budget=sufficient_budget)
        t5 = time.perf_counter()
        unrelaxed_time_guided = (t5 - t4) * 1000.0

        t6 = time.perf_counter()
        hier_res_guided = HierarchicalSearchEngine.search_with_coarse_pruning(
            fine_graph=fine_mg,
            coarse_graph=coarse_mg,
            coarsening_map=cmap,
            source=s,
            target=t,
            budget=sufficient_budget,
        )
        t7 = time.perf_counter()
        hier_time_guided = (t7 - t6) * 1000.0

        hier_nodes_guided = hier_res_guided.nodes_explored
        red_guided = (
            float(unrelaxed_nodes_guided - hier_nodes_guided) / float(unrelaxed_nodes_guided)
            if unrelaxed_nodes_guided > 0
            else 0.0
        )
        speedup_guided = (
            unrelaxed_time_guided / hier_time_guided if hier_time_guided > 0 else 1.0
        )

        guided_results.append(
            ScaleBenchmarkResult(
                scale=k,
                num_intervals=num_int,
                num_edges=num_edg,
                unrelaxed_nodes_explored=unrelaxed_nodes_guided,
                hierarchical_nodes_explored=hier_nodes_guided,
                node_reduction_ratio=red_guided,
                unrelaxed_time_ms=unrelaxed_time_guided,
                hierarchical_time_ms=hier_time_guided,
                speedup_ratio=speedup_guided,
                certified_outcome=type(hier_res_guided.receipt).__name__,
            )
        )

    return BenchmarkReport(
        scales=tuple(scales),
        refusal_benchmarks=tuple(refusal_results),
        guided_benchmarks=tuple(guided_results),
    )


if __name__ == "__main__":
    report = run_hierarchical_benchmark(scales=(4, 6, 8), coarse_scale=2)
    print("=== Early Refusal Benchmark (Insufficient Budget = 1/4) ===")
    for r in report.refusal_benchmarks:
        print(
            f"Scale {r.scale} ({r.num_intervals} intervals, {r.num_edges} edges): "
            f"Unrelaxed Nodes = {r.unrelaxed_nodes_explored} vs Hierarchical Nodes = {r.hierarchical_nodes_explored} "
            f"(Reduction = {r.node_reduction_ratio * 100:.1f}%), "
            f"Outcome = {r.certified_outcome}"
        )

    print("\n=== Guided Search Benchmark (Sufficient Budget = 1) ===")
    for r in report.guided_benchmarks:
        print(
            f"Scale {r.scale} ({r.num_intervals} intervals, {r.num_edges} edges): "
            f"Unrelaxed Nodes = {r.unrelaxed_nodes_explored} vs Hierarchical Nodes = {r.hierarchical_nodes_explored} "
            f"(Reduction = {r.node_reduction_ratio * 100:.1f}%), "
            f"Outcome = {r.certified_outcome}"
        )
