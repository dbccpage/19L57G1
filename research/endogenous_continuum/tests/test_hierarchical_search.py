"""Tests for Hierarchical Multi-Scale Search with Coarsening Pruning & Cycle Filtering.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from research.endogenous_continuum.dual_relaxation import (
    DualityGapReceipt,
)
from research.endogenous_continuum.hierarchical_search import (
    HierarchicalRefusalReceipt,
    HierarchicalSearchEngine,
)
from research.endogenous_continuum.interval_domain import (
    DyadicInterval,
    create_interval_coarsening_map,
    create_interval_movegraph,
)
from research.endogenous_continuum.projective_system import MoveEdge, MoveGraph


def test_coarse_pruning_zero_nodes_expanded() -> None:
    """Coarse dual potential prunes fine search immediately (0 fine nodes explored) when budget is exceeded."""
    coarse_k = 2
    fine_k = 4
    coarse_mg = create_interval_movegraph(scale=coarse_k)
    fine_mg = create_interval_movegraph(scale=fine_k)
    cmap = create_interval_coarsening_map(coarse_scale=coarse_k, fine_scale=fine_k)

    fine_s = DyadicInterval(scale=fine_k, index=0)
    # Fine target index 14 is at the other end: coarse projection is index 2
    fine_t = DyadicInterval(scale=fine_k, index=14)

    # Coarse distance from 0 to 2 is 2 * (1/4) = 1/2.
    # If we declare budget 1/4 < 1/2:
    tight_budget = Fraction(1, 4)
    result = HierarchicalSearchEngine.search_with_coarse_pruning(
        fine_graph=fine_mg,
        coarse_graph=coarse_mg,
        coarsening_map=cmap,
        source=fine_s,
        target=fine_t,
        budget=tight_budget,
    )

    assert result.path is None
    assert result.coarse_pruned
    assert result.nodes_explored == 0  # Zero fine nodes expanded!
    assert isinstance(result.receipt, HierarchicalRefusalReceipt)
    assert result.receipt.certified_refusal
    assert result.receipt.coarse_level == coarse_k
    assert result.receipt.fine_level == fine_k
    assert result.receipt.budget == tight_budget
    assert result.receipt.coarse_dual_bound == Fraction(1, 2)


def test_hierarchical_guided_search_finds_optimal_path() -> None:
    """Coarse dual heuristic guides fine search to optimal path with exact zero duality gap."""
    coarse_k = 2
    fine_k = 3
    coarse_mg = create_interval_movegraph(scale=coarse_k)
    fine_mg = create_interval_movegraph(scale=fine_k)
    cmap = create_interval_coarsening_map(coarse_scale=coarse_k, fine_scale=fine_k)

    fine_s = DyadicInterval(scale=fine_k, index=0)
    fine_t = DyadicInterval(scale=fine_k, index=6)

    # Budget 1 is ample (cost is 6/8 = 3/4)
    result = HierarchicalSearchEngine.search_with_coarse_pruning(
        fine_graph=fine_mg,
        coarse_graph=coarse_mg,
        coarsening_map=cmap,
        source=fine_s,
        target=fine_t,
        budget=Fraction(1, 1),
    )

    assert result.path is not None
    assert len(result.path) == 6
    assert not result.coarse_pruned
    assert isinstance(result.receipt, DualityGapReceipt)
    assert result.receipt.is_optimal
    assert result.receipt.primal_cost == Fraction(3, 4)
    assert result.receipt.duality_gap == Fraction(0, 1)


def test_dissipative_cycle_detection_prunes_loops() -> None:
    """Cycle filter detects and prunes loops where potential mu1 is invariant but dissipation mu2 accumulates."""
    # Build a graph with a 2-cycle loop
    s0 = "start"
    s1 = "cycle_a"
    s2 = "cycle_b"
    target = "goal"

    edges = [
        MoveEdge(source=s0, target=s1, mu1=Fraction(1, 1), mu2=Fraction(1, 1)),
        # 2-cycle between s1 and s2
        MoveEdge(source=s1, target=s2, mu1=Fraction(1, 1), mu2=Fraction(1, 1)),
        MoveEdge(source=s2, target=s1, mu1=Fraction(1, 1), mu2=Fraction(1, 1)),
        # Path to target from s2
        MoveEdge(source=s2, target=target, mu1=Fraction(1, 1), mu2=Fraction(1, 1)),
    ]
    graph = MoveGraph.build(level=1, states=[s0, s1, s2, target], edges=edges)
    cmap = create_interval_coarsening_map(coarse_scale=1, fine_scale=1)
    coarse_graph = create_interval_movegraph(scale=1)

    # Use identity coarsening mapping for this custom graph
    custom_cmap = create_interval_coarsening_map(1, 1)
    # Search fine graph directly using identity
    result = HierarchicalSearchEngine.search_with_coarse_pruning(
        fine_graph=graph,
        coarse_graph=graph,
        coarsening_map=custom_cmap.identity(graph),
        source=s0,
        target=target,
        budget=Fraction(10, 1),
    )

    assert result.path is not None
    assert len(result.path) == 3  # s0 -> s1 -> s2 -> target
    assert result.dissipative_cycles_pruned >= 1


def test_hierarchical_search_negative_controls() -> None:
    """Negative controls reject non-existent states and float budgets."""
    coarse_mg = create_interval_movegraph(scale=2)
    fine_mg = create_interval_movegraph(scale=3)
    cmap = create_interval_coarsening_map(coarse_scale=2, fine_scale=3)

    s = DyadicInterval(scale=3, index=0)
    t = DyadicInterval(scale=3, index=2)

    with pytest.raises(TypeError, match="must be exact rational"):
        HierarchicalSearchEngine.search_with_coarse_pruning(
            fine_mg, coarse_mg, cmap, s, t, budget=2.0  # type: ignore[arg-type]
        )

    with pytest.raises(KeyError, match="not in fine graph"):
        HierarchicalSearchEngine.search_with_coarse_pruning(
            fine_mg, coarse_mg, cmap, "unknown", t
        )
