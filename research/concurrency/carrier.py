"""Multi-locus product carrier: L1 x L2 x M.

Constructive three-locus product carrier for concurrent operational semantics:
- Locus 1: Observer 1's local coordinate (capacity n1)
- Locus 2: Observer 2's local coordinate (capacity n2)
- Locus M: Shared message/coupling cell (capacity nm)

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Tuple


@dataclass(frozen=True)
class State3:
    """Three-locus state."""

    l1: int
    l2: int
    m: int

    def is_valid(self, n1: int, n2: int, nm: int) -> bool:
        """Check if all coordinates are within declared capacities."""
        return 0 <= self.l1 < n1 and 0 <= self.l2 < n2 and 0 <= self.m < nm

    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.l1, self.l2, self.m)


def pack3(n2: int, nm: int, s: State3) -> int:
    """Pack a 3-locus state into a single natural number.

    Formula matching Lean formalization: nm * (n2 * s.l1 + s.l2) + s.m.
    """
    if n2 <= 0 or nm <= 0:
        raise ValueError("Capacities n2 and nm must be strictly positive.")
    return nm * (n2 * s.l1 + s.l2) + s.m


def unpack3(n2: int, nm: int, x: int) -> State3:
    """Unpack a natural number back into a 3-locus state."""
    if n2 <= 0 or nm <= 0:
        raise ValueError("Capacities n2 and nm must be strictly positive.")
    if x < 0:
        raise ValueError("Packed state index x must be non-negative.")
    m = x % nm
    div_m = x // nm
    l2 = div_m % n2
    l1 = div_m // n2
    return State3(l1=l1, l2=l2, m=m)


def proj1(s: State3) -> Tuple[int, int]:
    """Projected observation for Observer 1: (local state L1, message buffer M)."""
    return (s.l1, s.m)


def proj2(s: State3) -> Tuple[int, int]:
    """Projected observation for Observer 2: (local state L2, message buffer M)."""
    return (s.l2, s.m)


def proj_m(s: State3) -> int:
    """Projected observation of shared message buffer M."""
    return s.m


def update_l1(f: Callable[[int], int], s: State3) -> State3:
    """Local update at Locus 1."""
    return State3(l1=f(s.l1), l2=s.l2, m=s.m)


def update_l2(g: Callable[[int], int], s: State3) -> State3:
    """Local update at Locus 2."""
    return State3(l1=s.l1, l2=g(s.l2), m=s.m)


def update_m(h: Callable[[int], int], s: State3) -> State3:
    """Local update at Message Locus M."""
    return State3(l1=s.l1, l2=s.l2, m=h(s.m))


def swap(s: State3) -> State3:
    """Symmetry swap involution exchanging observers L1 and L2 while preserving M."""
    return State3(l1=s.l2, l2=s.l1, m=s.m)


def generate_state_grid(n1: int, n2: int, nm: int) -> list[State3]:
    """Generate all states in the Cartesian product [0, n1) x [0, n2) x [0, nm)."""
    return [
        State3(l1=a, l2=b, m=c)
        for a in range(n1)
        for b in range(n2)
        for c in range(nm)
    ]
