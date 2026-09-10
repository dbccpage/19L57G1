"""Unit tests for Target M104 / M107 Equality Layers & Order Family."""

from __future__ import annotations

from fractions import Fraction
import pytest

try:
    from research.m104_equality_order.equality_order import (
        AdmittedObserver,
        ExecutionTrace,
        ProofStep,
        PropositionalPath,
        StateWithHiddenSector,
        SyntaxTerm,
        cost_leq,
        evaluate_term,
        is_definitially_equal,
        is_observationally_equivalent,
        observer_refinement_leq,
        reachability_leq,
        verify_m104_m107_invariants,
    )
except ModuleNotFoundError:
    from equality_order import (
        AdmittedObserver,
        ExecutionTrace,
        ProofStep,
        PropositionalPath,
        StateWithHiddenSector,
        SyntaxTerm,
        cost_leq,
        evaluate_term,
        is_definitially_equal,
        is_observationally_equivalent,
        observer_refinement_leq,
        reachability_leq,
        verify_m104_m107_invariants,
    )


def test_m104_equality_layers_strict_separation() -> None:
    # 1. DefEq without Presentation Identity
    t_add = SyntaxTerm("Add", (SyntaxTerm("Const", (), "4"), SyntaxTerm("Const", (), "6")), "A")
    t_mul = SyntaxTerm("Mul", (SyntaxTerm("Const", (), "2"), SyntaxTerm("Const", (), "5")), "B")
    assert evaluate_term(t_add) == 10
    assert evaluate_term(t_mul) == 10
    assert is_definitially_equal(t_add, t_mul)
    assert not t_add.is_presentation_identical(t_mul)

    # 2. Propositional path
    path = PropositionalPath(t_add, t_mul, (ProofStep("arith", "4+6=2*5"),))
    assert path.is_valid()

    # 3. Observational equivalence without state identity
    s1 = StateWithHiddenSector(5, 7, hidden_c=100)
    s2 = StateWithHiddenSector(5, 7, hidden_c=200)
    obs_all = [AdmittedObserver("ObsAB", ("a", "b")), AdmittedObserver("ObsA", ("a",))]
    assert is_observationally_equivalent(s1, s2, obs_all)
    assert s1 != s2


def test_m104_quotient_representative_independence() -> None:
    # Price and operation evaluated on quotient representatives (e.g. fractions or normal forms)
    # Representative 1: (2, 4), Representative 2: (1, 2)
    def price_function(t: SyntaxTerm) -> Fraction:
        # Price is strictly determined by normal form value in Q
        val = evaluate_term(t)
        return Fraction(val, 1)

    t1 = SyntaxTerm("Add", (SyntaxTerm("Const", (), "2"), SyntaxTerm("Const", (), "2")))
    t2 = SyntaxTerm("Const", (), "4")
    assert is_definitially_equal(t1, t2)
    assert price_function(t1) == price_function(t2) == Fraction(4, 1)


def test_m107_reachability_preorder() -> None:
    # Graph with a cycle and a dead end:
    # 0 -> 1 -> 2 -> 0, 2 -> 3
    adj = {
        "0": ["1"],
        "1": ["2"],
        "2": ["0", "3"],
        "3": [],
    }
    # Preorder reflexivity
    for node in ["0", "1", "2", "3"]:
        assert reachability_leq(node, node, adj)

    # Preorder transitivity
    assert reachability_leq("0", "3", adj)
    # Mutual reachability in cycle (not antisymmetric -> preorder, not poset)
    assert reachability_leq("0", "2", adj)
    assert reachability_leq("2", "0", adj)
    # 3 cannot reach 0
    assert not reachability_leq("3", "0", adj)


def test_m107_refinement_order_poset() -> None:
    # Observers: O_none < O_a < O_ab
    o_a = AdmittedObserver("ObsA", ("a",))
    o_b = AdmittedObserver("ObsB", ("b",))
    o_ab = AdmittedObserver("ObsAB", ("a", "b"))

    sample_states = (
        StateWithHiddenSector(0, 0, 0),
        StateWithHiddenSector(0, 1, 0),
        StateWithHiddenSector(1, 0, 0),
        StateWithHiddenSector(1, 1, 0),
    )

    # o_a <= o_ab
    assert observer_refinement_leq(o_a, o_ab, sample_states)
    # o_b <= o_ab
    assert observer_refinement_leq(o_b, o_ab, sample_states)
    # o_ab is not <= o_a
    assert not observer_refinement_leq(o_ab, o_a, sample_states)
    # Incomparable observers o_a and o_b
    assert not observer_refinement_leq(o_a, o_b, sample_states)
    assert not observer_refinement_leq(o_b, o_a, sample_states)


def test_m107_cost_order_in_Q() -> None:
    tr_cheap = ExecutionTrace("start", "end1", steps=10, cost=Fraction(1, 2))
    tr_expensive = ExecutionTrace("start", "end2", steps=2, cost=Fraction(5, 1))

    assert cost_leq(tr_cheap, tr_expensive)
    assert not cost_leq(tr_expensive, tr_cheap)


def test_verify_invariants_comprehensive() -> None:
    res = verify_m104_m107_invariants()
    assert res["status"] == "PASS"
    assert res["m104_equality_layers_separated"] is True
    assert res["m107_orders_non_conflated"] is True
