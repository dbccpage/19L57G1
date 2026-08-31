"""Finite diagrams, coboundary mass, observers, joint kernels.

Carriers are integer pairs with l1 mass.  Identity restrictions.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from typing import Sequence

Vec = tuple[int, int]
Section = dict[int, Vec]
Edge = tuple[int, int]


def vadd(p: Vec, q: Vec) -> Vec:
    return (p[0] + q[0], p[1] + q[1])


def vneg(p: Vec) -> Vec:
    return (-p[0], -p[1])


def nu(p: Vec) -> int:
    return abs(p[0]) + abs(p[1])


def cob(s: Section, edge: Edge) -> Vec:
    src, tgt = edge
    return vadd(s[tgt], vneg(s[src]))


def mass(s: Section, edges: Sequence[Edge]) -> int:
    return sum(nu(cob(s, e)) for e in edges)


def coord(p: Vec) -> int:
    return p[0]


def joint_ker_member(p: Vec, watched: bool) -> bool:
    """Rank-1 first-coordinate watcher: kernel is first component zero."""

    if not watched:
        return True
    return p[0] == 0


PATCH3_EDGES: tuple[Edge, ...] = (
    (3, 0),
    (3, 1),
    (4, 1),
    (4, 2),
    (5, 2),
    (5, 0),
)


def patch3_section() -> Section:
    s: Section = {i: (0, 0) for i in range(6)}
    for i in (3, 4, 5):
        s[i] = (0, 1)
    return s


def patch3_scale_section(lam: int) -> Section:
    """OV3 scaling family: overlaps get (0, lam), patches (0, 0)."""

    s: Section = {i: (0, 0) for i in range(6)}
    for i in (3, 4, 5):
        s[i] = (0, lam)
    return s


def j_coord(s: Section, edges: Sequence[Edge]) -> int:
    return sum(abs(coord(cob(s, e))) for e in edges)


def kills(p: Vec, first: bool, second: bool) -> bool:
    if first and p[0] != 0:
        return False
    if second and p[1] != 0:
        return False
    return True


def all_green(
    s: Section,
    edges: Sequence[Edge],
    watch_flags: Sequence[tuple[bool, bool]] | None = None,
) -> bool:
    if watch_flags is None:
        return j_coord(s, edges) == 0
    return all(
        kills(cob(s, edge), first, second)
        for edge, (first, second) in zip(edges, watch_flags, strict=True)
    )
