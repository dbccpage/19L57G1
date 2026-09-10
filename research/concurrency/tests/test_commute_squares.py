"""Unit tests for commute.py: commuting squares and failing squares."""

from __future__ import annotations

import pytest
from carrier import State3, generate_state_grid, update_l1, update_l2, update_m
from commute import (
    commutes,
    find_commute_counterexample,
    make_coord_update,
    op_inc_m,
    op_read_l1_write_m,
    op_read_m_write_l1,
    op_read_m_write_l2,
    op_write1,
    op_write2,
)


@pytest.fixture
def state_grid_small() -> list[State3]:
    """Exhaustive grid of 4 x 4 x 4 = 64 states."""
    return generate_state_grid(4, 4, 4)


@pytest.fixture
def state_grid_medium() -> list[State3]:
    """Exhaustive grid of 6 x 6 x 6 = 216 states."""
    return generate_state_grid(6, 6, 6)


def test_independent_coordinate_updates_commute_exhaustively(
    state_grid_medium: list[State3],
) -> None:
    """Disjoint coordinate updates commute on 100% of states in the grid."""
    f = lambda x: (x + 3) % 6
    g = lambda x: (x * 2) % 6
    h = lambda x: (x + 5) % 6

    op1 = make_coord_update("L1", f)
    op2 = make_coord_update("L2", g)
    op_m = make_coord_update("M", h)

    # L1 and L2
    assert commutes(op1, op2, state_grid_medium) is True
    assert find_commute_counterexample(op1, op2, state_grid_medium) is None

    # L1 and M
    assert commutes(op1, op_m, state_grid_medium) is True
    assert find_commute_counterexample(op1, op_m, state_grid_medium) is None

    # L2 and M
    assert commutes(op2, op_m, state_grid_medium) is True
    assert find_commute_counterexample(op2, op_m, state_grid_medium) is None


def test_write_write_conflict_fails_commute(
    state_grid_small: list[State3],
) -> None:
    """Two writes to L1 fail to commute."""
    assert commutes(op_write1, op_write2, state_grid_small) is False

    witness = find_commute_counterexample(op_write1, op_write2, state_grid_small)
    assert witness is not None
    s, s12, s21 = witness
    assert s12.l1 == 1
    assert s21.l1 == 2
    assert s12 != s21


def test_read_write_conflict_fails_commute(
    state_grid_small: list[State3],
) -> None:
    """Operation reading M into L1 conflicts with operation mutating M."""
    assert commutes(op_read_m_write_l1, op_inc_m, state_grid_small) is False

    witness = find_commute_counterexample(op_read_m_write_l1, op_inc_m, state_grid_small)
    assert witness is not None
    s, s12, s21 = witness
    # op_read_m_write_l1(op_inc_m(s)) sees the updated m in l1
    # op_inc_m(op_read_m_write_l1(s)) sees the old m in l1
    assert s12.l1 == s.m + 1
    assert s21.l1 == s.m
    assert s12 != s21


def test_cross_observer_message_coupling_breaks_the_square(
    state_grid_small: list[State3],
) -> None:
    """Observer 1 writing to M and Observer 2 reading from M break commutation with each other."""
    # O1 writes L1 to M; O2 reads M into L2.
    assert commutes(op_read_l1_write_m, op_read_m_write_l2, state_grid_small) is False

    witness = find_commute_counterexample(
        op_read_l1_write_m, op_read_m_write_l2, state_grid_small
    )
    assert witness is not None
    s, s12, s21 = witness
    # Order 1 (O1 then O2): s12 = O1(O2(s)): O2 reads old M into L2, O1 writes L1 into M
    # Order 2 (O2 then O1): s21 = O2(O1(s)): O1 writes L1 into M, O2 reads new M (L1) into L2
    assert s12 != s21


@pytest.mark.parametrize(
    "shift_a, shift_b",
    [
        (1, 1),
        (2, 3),
        (5, 7),
        (11, 13),
    ],
)
def test_parameterized_modular_shifts_commute_on_disjoint_loci(
    shift_a: int, shift_b: int, state_grid_small: list[State3]
) -> None:
    """Test commutation across a variety of mathematical functions on disjoint loci."""
    op_a = make_coord_update("L1", lambda x: (x + shift_a) % 4)
    op_b = make_coord_update("L2", lambda x: (x + shift_b) % 4)
    assert commutes(op_a, op_b, state_grid_small) is True
