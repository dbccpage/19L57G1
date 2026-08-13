"""Tests for the declared cell calculus and its invariants."""

from __future__ import annotations

import pytest

from derivation.higher_structure import (
    EMPTY_COMPLEX,
    Complex,
    alt_num,
    bd2,
    bd2_neg,
    bd3,
    boundary_not_forced,
    coeff_e,
    coeff_v,
    creplay,
    cstep,
    cut_census,
    d2_zero_tet,
    d2_zero_triangles,
    shell1,
    shell2,
    shell3,
    k4,
    k4_boundary,
    k4_events,
    push1,
    push2,
    subsets_of,
)


def test_k4_builds_in_creation_order() -> None:
    cx = k4()
    assert cx.c0 == (0, 1, 2, 3)
    assert cx.c1 == ((0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (0, 3))
    assert cx.c2 == ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
    assert cx.c3 == ((0, 1, 2, 3),)


def test_horn_guards_load_bearing() -> None:
    guard = Complex(c0=(0, 1, 2), c1=((0, 1),))
    # incomplete boundary: triangle refused
    assert cstep(guard, ("addT", 0, 1, 2)) == guard
    assert not shell2(guard, 0, 1, 2)
    # vertex dedup
    assert cstep(guard, ("addV", 0)) == guard
    # edge needs both endpoints and freshness
    assert cstep(guard, ("addE", 0, 1)) == guard
    assert cstep(guard, ("addE", 0, 7)) == guard
    assert not shell1(guard, 0, 0)
    # tetrahedron needs all four faces
    shell = k4_boundary()
    assert shell3(shell, 0, 1, 2, 3)
    assert shell.c3 == ()
    partial_shell = creplay(k4_events()[:13], EMPTY_COMPLEX)
    assert not shell3(partial_shell, 0, 1, 2, 3)
    assert cstep(partial_shell,
                 ("addQ", 0, 1, 2, 3)) == partial_shell
    # duplicate solid cell refused
    full = k4()
    assert cstep(full, ("addQ", 0, 1, 2, 3)) == full
    # malformed kind raises
    with pytest.raises(ValueError):
        cstep(full, ("bogus",))


def test_alt_num_stages() -> None:
    assert alt_num(creplay(k4_events()[:4], EMPTY_COMPLEX)) == 4
    assert alt_num(creplay(k4_events()[:10], EMPTY_COMPLEX)) == -2
    assert alt_num(k4_boundary()) == 2
    assert alt_num(k4()) == 1


def test_cut_census() -> None:
    assert cut_census(2, 0, 1) == 1
    assert cut_census(3, 0, 1) == 2
    assert cut_census(4, 0, 1) == 4
    assert cut_census(5, 0, 1) == 8
    assert len(subsets_of([0, 1, 2])) == 8


def test_boundary_calculus() -> None:
    full = k4()
    assert d2_zero_triangles(full)
    assert d2_zero_tet(full, (0, 1, 2, 3))
    # composite vanishes cell by cell
    for t in full.c2:
        for v in full.c0:
            assert coeff_v(v, push1(bd2(t))) == 0
    for e in full.c1:
        assert coeff_e(e, push2(bd3((0, 1, 2, 3)))) == 0
    # and a non-face coefficient is genuinely nonzero pre-composite
    assert coeff_e((1, 2), [(c, e) for (c, e) in bd2((0, 1, 2))]) == 1
    # the convention is declared, not derived
    assert bd2((0, 1, 2)) != bd2_neg((0, 1, 2))
    assert boundary_not_forced((0, 1, 2))


def test_d2_zero_fails_for_broken_convention() -> None:
    # a deliberately wrong boundary (dropping the middle face) does
    # NOT compose to zero: the vanishing is a fact about the declared
    # convention, not a triviality.
    t = (0, 1, 2)
    broken = [(1, (t[1], t[2])), (1, (t[0], t[1]))]
    assert any(coeff_v(v, push1(broken)) != 0 for v in (0, 1, 2))
