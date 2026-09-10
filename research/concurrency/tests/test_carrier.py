"""Unit tests for carrier.py: State3, packing, unpacking, projections, and updates."""

from __future__ import annotations

import pytest
from carrier import (
    State3,
    generate_state_grid,
    pack3,
    proj1,
    proj2,
    proj_m,
    swap,
    unpack3,
    update_l1,
    update_l2,
    update_m,
)


def test_state_creation_and_validity() -> None:
    s = State3(l1=1, l2=2, m=3)
    assert s.l1 == 1
    assert s.l2 == 2
    assert s.m == 3
    assert s.is_valid(2, 3, 4)
    assert not s.is_valid(1, 3, 4)
    assert not s.is_valid(2, 2, 4)
    assert not s.is_valid(2, 3, 3)


def test_packing_roundtrip_small() -> None:
    n1, n2, nm = 3, 4, 5
    for a in range(n1):
        for b in range(n2):
            for c in range(nm):
                s = State3(l1=a, l2=b, m=c)
                packed = pack3(n2, nm, s)
                assert 0 <= packed < n1 * n2 * nm
                recovered = unpack3(n2, nm, packed)
                assert recovered == s


def test_packing_roundtrip_larger() -> None:
    n1, n2, nm = 10, 10, 10
    grid = generate_state_grid(n1, n2, nm)
    assert len(grid) == 1000
    for s in grid:
        packed = pack3(n2, nm, s)
        assert 0 <= packed < 1000
        recovered = unpack3(n2, nm, packed)
        assert recovered == s


def test_packing_invalid_capacities() -> None:
    s = State3(l1=0, l2=0, m=0)
    with pytest.raises(ValueError, match="strictly positive"):
        pack3(0, 5, s)
    with pytest.raises(ValueError, match="strictly positive"):
        pack3(5, 0, s)
    with pytest.raises(ValueError, match="strictly positive"):
        unpack3(-1, 5, 10)
    with pytest.raises(ValueError, match="non-negative"):
        unpack3(5, 5, -1)


def test_projections() -> None:
    s = State3(l1=7, l2=42, m=99)
    assert proj1(s) == (7, 99)
    assert proj2(s) == (42, 99)
    assert proj_m(s) == 99


def test_coordinate_updates_preservation() -> None:
    s = State3(l1=10, l2=20, m=30)

    s_l1 = update_l1(lambda x: x + 5, s)
    assert s_l1.l1 == 15
    assert s_l1.l2 == 20
    assert s_l1.m == 30

    s_l2 = update_l2(lambda x: x * 2, s)
    assert s_l2.l1 == 10
    assert s_l2.l2 == 40
    assert s_l2.m == 30

    s_m = update_m(lambda x: x - 10, s)
    assert s_m.l1 == 10
    assert s_m.l2 == 20
    assert s_m.m == 20


def test_disjoint_update_commutation() -> None:
    s = State3(l1=5, l2=10, m=15)
    f = lambda x: x + 3
    g = lambda x: x * 2
    h = lambda x: x + 100

    # L1 and L2
    assert update_l1(f, update_l2(g, s)) == update_l2(g, update_l1(f, s))
    # L1 and M
    assert update_l1(f, update_m(h, s)) == update_m(h, update_l1(f, s))
    # L2 and M
    assert update_l2(g, update_m(h, s)) == update_m(h, update_l2(g, s))


def test_swap_involution_and_projections() -> None:
    s = State3(l1=12, l2=34, m=56)
    s_swapped = swap(s)
    assert s_swapped.l1 == 34
    assert s_swapped.l2 == 12
    assert s_swapped.m == 56

    # Involution: swap(swap(s)) == s
    assert swap(s_swapped) == s

    # Projection duality
    assert proj1(s_swapped) == proj2(s)
    assert proj2(s_swapped) == proj1(s)
    assert proj_m(s_swapped) == proj_m(s)
