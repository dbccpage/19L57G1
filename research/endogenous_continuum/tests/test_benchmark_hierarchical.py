"""Tests for Empirical Hierarchical Benchmark Suite.

AuthorityEffect: None.
"""

from __future__ import annotations

from research.endogenous_continuum.benchmark_hierarchical import (
    run_hierarchical_benchmark,
    run_unrelaxed_search,
)
from research.endogenous_continuum.interval_domain import (
    DyadicInterval,
    create_interval_movegraph,
)


def test_hierarchical_benchmark_runs_across_scale_depths() -> None:
    """Benchmark reports bounded and reachable cases at scales 4, 6, and 8."""
    report = run_hierarchical_benchmark(scales=(4, 6, 8), coarse_scale=2)
    assert report.scales == (4, 6, 8)
    assert len(report.refusal_benchmarks) == 3
    assert len(report.guided_benchmarks) == 3

    # The default cross-scale cost lift is not admissible, so the implementation
    # must fall back rather than advertise a zero-node coarse refusal.
    for r in report.refusal_benchmarks:
        assert r.hierarchical_nodes_explored > 0
        assert r.unrelaxed_nodes_explored > 0
        assert r.certified_outcome == "SearchExhaustionReceipt"
        assert r.node_reduction_ratio <= 1.0

    # On reachable search, an exact optimality receipt is returned.
    for r in report.guided_benchmarks:
        assert r.certified_outcome == "DualityGapReceipt"
        assert r.hierarchical_nodes_explored > 0


def test_unrelaxed_search_direct() -> None:
    """Un-relaxed search directly finds paths on interval movegraphs."""
    mg = create_interval_movegraph(scale=3)
    s = DyadicInterval(scale=3, index=0)
    t = DyadicInterval(scale=3, index=4)

    path, nodes = run_unrelaxed_search(mg, s, t)
    assert path is not None
    assert len(path) == 4
    assert nodes > 0
