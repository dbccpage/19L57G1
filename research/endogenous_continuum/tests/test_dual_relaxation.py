"""Tests for exact rational shortest-distance potentials and receipts.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from research.endogenous_continuum.dual_relaxation import (
    DualPotential,
    DualRefusalReceipt,
    ExactPathSolver,
    DualityGapReceipt,
)
from research.endogenous_continuum.interval_domain import (
    DyadicInterval,
    create_interval_movegraph,
)
from research.endogenous_continuum.projective_system import MoveEdge, MoveGraph


def test_dual_potential_admissibility_and_differences() -> None:
    """Dual potential satisfies admissibility y(v) - y(u) <= cost(u, v) on interval movegraph."""
    mg = create_interval_movegraph(scale=3)
    s = DyadicInterval(scale=3, index=0)
    dual = ExactPathSolver.compute_dual_potential(mg, s)

    is_adm, defects = dual.verify_admissibility(mg)
    assert is_adm
    assert len(defects) == 0

    # Potential of source is 0
    assert dual.get(s) == Fraction(0, 1)

    # Adjacent node has potential exactly 1 / 2^3 = 1/8
    s1 = DyadicInterval(scale=3, index=1)
    assert dual.get(s1) == Fraction(1, 8)
    assert dual.potential_difference(s, s1) == Fraction(1, 8)

    # Terminal node index 6 has potential 6 / 8 = 3/4
    s6 = DyadicInterval(scale=3, index=6)
    assert dual.get(s6) == Fraction(6, 8)
    assert dual.potential_difference(s, s6) == Fraction(3, 4)


def test_exact_path_solver_optimal_path_zero_gap() -> None:
    """Primal-dual solver finds shortest path with exact zero duality gap."""
    mg = create_interval_movegraph(scale=3)
    s = DyadicInterval(scale=3, index=0)
    t = DyadicInterval(scale=3, index=4)

    path, receipt = ExactPathSolver.solve_primal_dual(mg, s, t)
    assert path is not None
    assert len(path) == 4
    assert isinstance(receipt, DualityGapReceipt)
    assert receipt.is_optimal
    assert receipt.is_reachable
    assert receipt.primal_cost == Fraction(4, 8)
    assert receipt.dual_bound == Fraction(4, 8)
    assert receipt.duality_gap == Fraction(0, 1)


def test_dual_refusal_on_insufficient_budget() -> None:
    """Solver refuses when an exact lower bound exceeds the budget."""
    mg = create_interval_movegraph(scale=3)
    s = DyadicInterval(scale=3, index=0)
    t = DyadicInterval(scale=3, index=6)
    # Required cost is 6/8 = 3/4. Allocate budget 1/2 < 3/4.
    insufficient_budget = Fraction(1, 2)

    path, receipt = ExactPathSolver.solve_primal_dual(
        mg, s, t, budget=insufficient_budget
    )
    assert path is None
    assert isinstance(receipt, DualRefusalReceipt)
    assert receipt.certified_refusal
    assert receipt.budget == insufficient_budget
    assert receipt.dual_bound == Fraction(3, 4)
    assert "strictly exceeds allocated budget" in receipt.reason


def test_dual_refusal_on_unreachable_target() -> None:
    """Solver emits certified refusal on disconnected components."""
    s1 = "state_1"
    s2 = "state_2"
    isolated = "isolated_target"
    e1 = MoveEdge(source=s1, target=s2, mu1=Fraction(1, 1), mu2=Fraction(0, 1))
    mg = MoveGraph.build(level=1, states=[s1, s2, isolated], edges=[e1])

    path, receipt = ExactPathSolver.solve_primal_dual(
        mg, s1, isolated, budget=Fraction(10, 1)
    )
    assert path is None
    assert isinstance(receipt, DualRefusalReceipt)
    assert receipt.certified_refusal
    assert receipt.dual_bound is None
    assert "Target unreachable" in receipt.reason


def test_independent_path_verification() -> None:
    """Independent path verifier checks path continuity and duality gap in O(len(path))."""
    mg = create_interval_movegraph(scale=3)
    s = DyadicInterval(scale=3, index=0)
    t = DyadicInterval(scale=3, index=3)

    path, _ = ExactPathSolver.solve_primal_dual(mg, s, t)
    assert path is not None
    dual = ExactPathSolver.compute_dual_potential(mg, s)

    is_valid, cost, bound, gap = ExactPathSolver.verify_path_against_dual(
        path, dual, s, t
    )
    assert is_valid
    assert cost == Fraction(3, 8)
    assert bound == Fraction(3, 8)
    assert gap == Fraction(0, 1)


def test_negative_controls_and_type_discipline() -> None:
    """Negative controls verify rejection of floats and malformed dual potentials."""
    mg = create_interval_movegraph(scale=2)
    s = DyadicInterval(scale=2, index=0)
    t = DyadicInterval(scale=2, index=2)

    # Rejection of float budget
    with pytest.raises(TypeError, match="must be exact rational"):
        ExactPathSolver.solve_primal_dual(mg, s, t, budget=1.5)  # type: ignore[arg-type]

    # Rejection of unknown state
    with pytest.raises(KeyError, match="not in graph"):
        ExactPathSolver.compute_dual_potential(mg, "unknown_state")

    with pytest.raises(KeyError, match="not in graph"):
        ExactPathSolver.solve_primal_dual(mg, s, "unknown_target")

    with pytest.raises(ValueError, match="budget cannot be negative"):
        ExactPathSolver.solve_primal_dual(
            mg, s, t, budget=Fraction(-1, 1)
        )

    with pytest.raises(ValueError, match="Negative edge cost"):
        ExactPathSolver.solve_shortest_path(
            mg,
            s,
            t,
            cost_fn=lambda _edge: Fraction(-1, 1),
        )

    # Detection of violated admissibility
    invalid_pot = {
        DyadicInterval(scale=2, index=0): Fraction(0, 1),
        DyadicInterval(scale=2, index=1): Fraction(10, 1),  # Exceeds edge cost 1/4
        DyadicInterval(scale=2, index=2): Fraction(10, 1),
    }
    bad_dual = DualPotential(source=s, potentials=invalid_pot)
    is_adm, defects = bad_dual.verify_admissibility(mg)
    assert not is_adm
    assert len(defects) > 0

    # A partial potential may omit an unreachable component, but not a target
    # reached by an edge leaving its assigned domain.
    partial = DualPotential(source=s, potentials={s: Fraction(0, 1)})
    is_adm, defects = partial.verify_admissibility(mg)
    assert not is_adm
    assert any("not closed" in defect for defect in defects)
