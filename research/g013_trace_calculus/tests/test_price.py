"""Tests for additive price cocycles and 2-cell homotopy invariance."""

import pytest
from higher_cell import Cell2, Cell2Kind, h_compose, v_compose
from price import PriceCocycle, audit_2cell_homotopy_invariance
from trace import State, Trace, Transition


def test_price_cocycle_additivity() -> None:
    s0 = State.create("s0")
    s1 = State.create("s1")
    s2 = State.create("s2")

    t1 = Transition(s0, s1, "step1", cost=2.5)
    t2 = Transition(s1, s2, "step2", cost=3.5)

    p = Trace.from_step(t1)
    q = Trace.from_step(t2)

    cocycle = PriceCocycle(cost_map={"step1": 2.5, "step2": 3.5})

    assert cocycle.trace_price(Trace.id_trace(s0)) == 0.0
    assert cocycle.trace_price(p) == 2.5
    assert cocycle.trace_price(q) == 3.5

    is_additive, c_comp, c_sum, diff = cocycle.verify_additivity(p, q)
    assert is_additive
    assert c_comp == 6.0
    assert c_sum == 6.0
    assert diff == 0.0


def test_price_homotopy_invariance_commuting_diamond() -> None:
    s0 = State.create("s0")
    s1 = State.create("s1")
    s2 = State.create("s2")
    dst = State.create("dst")

    # Symmetric independent operations: a costs 1.0, b costs 2.0
    t_a1 = Transition(s0, s1, "a", cost=1.0)
    t_b1 = Transition(s1, dst, "b", cost=2.0)
    t_b2 = Transition(s0, s2, "b", cost=2.0)
    t_a2 = Transition(s2, dst, "a", cost=1.0)

    cell_comm = Cell2.commute(t_a1, t_b1, t_b2, t_a2, "independent a and b commute")

    cocycle = PriceCocycle(cost_map={"a": 1.0, "b": 2.0})

    inv, c_src, c_tgt = cocycle.verify_homotopy_invariance(cell_comm)
    assert inv
    assert c_src == 3.0
    assert c_tgt == 3.0

    audit = audit_2cell_homotopy_invariance(cocycle, [cell_comm])
    assert audit.all_invariant
    assert audit.max_divergence == 0.0
    assert len(audit.violations) == 0


def test_price_homotopy_invariance_composition() -> None:
    s0 = State.create("s0")
    s1 = State.create("s1")
    s2 = State.create("s2")

    # Construct two cells and compose them horizontally and vertically
    p1 = Trace.from_step(Transition(s0, s1, "a", cost=1.0))
    q1 = Trace.from_step(Transition(s0, s1, "b", cost=1.0))
    r1 = Trace.from_step(Transition(s0, s1, "c", cost=1.0))

    cell1 = Cell2(p1, q1, Cell2Kind.INDEPENDENT_COMMUTE, "a => b")
    cell2 = Cell2(q1, r1, Cell2Kind.INDEPENDENT_COMMUTE, "b => c")

    v_comp = v_compose(cell1, cell2)

    cocycle = PriceCocycle(cost_map={"a": 1.0, "b": 1.0, "c": 1.0})
    inv, c_src, c_tgt = cocycle.verify_homotopy_invariance(v_comp)
    assert inv
    assert c_src == 1.0
    assert c_tgt == 1.0


def test_price_homotopy_negative_control_violation() -> None:
    s0 = State.create("s0")
    s1 = State.create("s1")

    # One route uses an expensive action (10.0), other uses cheap action (1.0)
    p = Trace.from_step(Transition(s0, s1, "cheap", cost=1.0))
    q = Trace.from_step(Transition(s0, s1, "expensive", cost=10.0))

    cell = Cell2(p, q, Cell2Kind.INDEPENDENT_COMMUTE, "unequal cost route")
    cocycle = PriceCocycle(cost_map={"cheap": 1.0, "expensive": 10.0})

    inv, c_src, c_tgt = cocycle.verify_homotopy_invariance(cell)
    assert not inv
    assert c_src == 1.0
    assert c_tgt == 10.0

    audit = audit_2cell_homotopy_invariance(cocycle, [cell])
    assert not audit.all_invariant
    assert audit.max_divergence == 9.0
    assert len(audit.violations) == 1
