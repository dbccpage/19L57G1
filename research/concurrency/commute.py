"""Commuting squares and operational interference.

Verifies operational independence squares (S1 ∘ S2 = S2 ∘ S1) on disjoint footprints
and exhibits non-commuting failing squares for interfering operations.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Callable, Iterable, Optional, Tuple

from carrier import State3, update_l1, update_l2, update_m


def commutes(
    op1: Callable[[State3], State3],
    op2: Callable[[State3], State3],
    states: Iterable[State3],
) -> bool:
    """Check if op1 and op2 commute across all provided states."""
    for s in states:
        if op1(op2(s)) != op2(op1(s)):
            return False
    return True


def find_commute_counterexample(
    op1: Callable[[State3], State3],
    op2: Callable[[State3], State3],
    states: Iterable[State3],
) -> Optional[Tuple[State3, State3, State3]]:
    """Find a witness state where op1 and op2 fail to commute.

    Returns (initial_state, op1(op2(s)), op2(op1(s))) or None.
    """
    for s in states:
        s12 = op1(op2(s))
        s21 = op2(op1(s))
        if s12 != s21:
            return (s, s12, s21)
    return None


# Canonical operations matching Lean formalization
def op_write1(s: State3) -> State3:
    """Write constant 1 to Locus 1."""
    return State3(l1=1, l2=s.l2, m=s.m)


def op_write2(s: State3) -> State3:
    """Write constant 2 to Locus 1."""
    return State3(l1=2, l2=s.l2, m=s.m)


def op_read_m_write_l1(s: State3) -> State3:
    """Read M and write to Locus 1."""
    return State3(l1=s.m, l2=s.l2, m=s.m)


def op_inc_m(s: State3) -> State3:
    """Increment Message Locus M."""
    return State3(l1=s.l1, l2=s.l2, m=s.m + 1)


def op_read_l1_write_m(s: State3) -> State3:
    """Transmit L1 to M."""
    return State3(l1=s.l1, l2=s.l2, m=s.l1)


def op_read_m_write_l2(s: State3) -> State3:
    """Receive M into L2."""
    return State3(l1=s.l1, l2=s.m, m=s.m)


def make_coord_update(coord: str, func: Callable[[int], int]) -> Callable[[State3], State3]:
    """Helper to construct pure coordinate updates."""
    if coord == "L1":
        return lambda s: update_l1(func, s)
    elif coord == "L2":
        return lambda s: update_l2(func, s)
    elif coord == "M":
        return lambda s: update_m(func, s)
    else:
        raise ValueError(f"Unknown coordinate: {coord}")
