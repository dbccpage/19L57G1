"""Tests for 2-cells, horizontal/vertical composition, and the Interchange Law."""

import pytest
from higher_cell import (
    Cell2,
    Cell2Kind,
    ReplayEquivalence,
    h_compose,
    v_compose,
    verify_interchange_law,
)
from trace import State, Trace, Transition


def test_2cell_identity_and_commutation() -> None:
    s0 = State.create("s0", {"x": 0, "y": 0})
    s1 = State.create("s1", {"x": 1, "y": 0})
    s2 = State.create("s2", {"x": 0, "y": 1})
    dst = State.create("dst", {"x": 1, "y": 1})

    t_x1 = Transition(s0, s1, "inc_x")
    t_y1 = Transition(s1, dst, "inc_y")
    t_y2 = Transition(s0, s2, "inc_y")
    t_x2 = Transition(s2, dst, "inc_x")

    cell_comm = Cell2.commute(t_x1, t_y1, t_y2, t_x2, "x and y independent commutation")
    assert cell_comm.kind == Cell2Kind.INDEPENDENT_COMMUTE
    assert cell_comm.source_0cell == s0
    assert cell_comm.target_0cell == dst
    assert cell_comm.source_trace.labels() == ["inc_x", "inc_y"]
    assert cell_comm.target_trace.labels() == ["inc_y", "inc_x"]

    # Invert symmetry
    cell_symm = cell_comm.symm()
    assert cell_symm.source_trace == cell_comm.target_trace
    assert cell_symm.target_trace == cell_comm.source_trace


def test_2cell_vertical_and_horizontal_composition() -> None:
    s0 = State.create("s0")
    s1 = State.create("s1")
    s2 = State.create("s2")

    # 1-cells from s0 to s1
    t_a = Transition(s0, s1, "a")
    t_b = Transition(s0, s1, "b")
    t_c = Transition(s0, s1, "c")

    tr_a = Trace.from_step(t_a)
    tr_b = Trace.from_step(t_b)
    tr_c = Trace.from_step(t_c)

    cell_ab = Cell2(tr_a, tr_b, Cell2Kind.INDEPENDENT_COMMUTE, "a => b")
    cell_bc = Cell2(tr_b, tr_c, Cell2Kind.INDEPENDENT_COMMUTE, "b => c")

    # Vertical composition: (b => c) o_1 (a => b) => (a => c)
    v_comp = v_compose(cell_ab, cell_bc)
    assert v_comp.kind == Cell2Kind.VERTICAL_COMPOSITION
    assert v_comp.source_trace == tr_a
    assert v_comp.target_trace == tr_c

    # 1-cells from s1 to s2
    t_d = Transition(s1, s2, "d")
    t_e = Transition(s1, s2, "e")
    tr_d = Trace.from_step(t_d)
    tr_e = Trace.from_step(t_e)
    cell_de = Cell2(tr_d, tr_e, Cell2Kind.INDEPENDENT_COMMUTE, "d => e")

    # Horizontal composition: (a => b) o_0 (d => e) => (a * d => b * e)
    h_comp = h_compose(cell_ab, cell_de)
    assert h_comp.kind == Cell2Kind.HORIZONTAL_COMPOSITION
    assert h_comp.source_trace == tr_a.concat(tr_d)
    assert h_comp.target_trace == tr_b.concat(tr_e)


def test_middle_four_interchange_law() -> None:
    """Rigorous test of the 2-category interchange theorem:
    (alpha2 o_1 alpha1) o_0 (beta2 o_1 beta1) == (alpha2 o_0 beta2) o_1 (alpha1 o_0 beta1)
    """
    s0 = State.create("s0")
    s1 = State.create("s1")
    s2 = State.create("s2")

    # Left sector: s0 -> s1 with routes p1, q1, r1
    p1 = Trace.from_step(Transition(s0, s1, "p1"))
    q1 = Trace.from_step(Transition(s0, s1, "q1"))
    r1 = Trace.from_step(Transition(s0, s1, "r1"))

    alpha1 = Cell2(p1, q1, Cell2Kind.INDEPENDENT_COMMUTE, "alpha1: p1 => q1")
    alpha2 = Cell2(q1, r1, Cell2Kind.INDEPENDENT_COMMUTE, "alpha2: q1 => r1")

    # Right sector: s1 -> s2 with routes p2, q2, r2
    p2 = Trace.from_step(Transition(s1, s2, "p2"))
    q2 = Trace.from_step(Transition(s1, s2, "q2"))
    r2 = Trace.from_step(Transition(s1, s2, "r2"))

    beta1 = Cell2(p2, q2, Cell2Kind.INDEPENDENT_COMMUTE, "beta1: p2 => q2")
    beta2 = Cell2(q2, r2, Cell2Kind.INDEPENDENT_COMMUTE, "beta2: q2 => r2")

    coherent, left_comp, right_comp = verify_interchange_law(alpha1, alpha2, beta1, beta2)

    assert coherent
    assert left_comp.source_trace == p1.concat(p2)
    assert left_comp.target_trace == r1.concat(r2)
    assert right_comp.source_trace == p1.concat(p2)
    assert right_comp.target_trace == r1.concat(r2)
    assert left_comp.source_trace == right_comp.source_trace
    assert left_comp.target_trace == right_comp.target_trace


def test_confluence_and_endpoint_equivalence() -> None:
    s0 = State.create("s0")
    s_mid1 = State.create("s_mid1")
    s_mid2 = State.create("s_mid2")
    dst = State.create("dst")

    t1 = Transition(s0, s_mid1, "branch1")
    t2 = Transition(s_mid1, dst, "merge1")
    t3 = Transition(s0, s_mid2, "branch2")
    t4 = Transition(s_mid2, dst, "merge2")

    tr1 = Trace.from_steps([t1, t2])
    tr2 = Trace.from_steps([t3, t4])

    assert ReplayEquivalence.are_endpoints_equal(tr1, tr2)
    assert ReplayEquivalence.verify_confluence([tr1, tr2])

    divergent_different_target = Trace.from_step(Transition(s0, State.create("other"), "branch3"))
    assert not ReplayEquivalence.are_endpoints_equal(tr1, divergent_different_target)
    assert not ReplayEquivalence.verify_confluence([tr1, divergent_different_target])
