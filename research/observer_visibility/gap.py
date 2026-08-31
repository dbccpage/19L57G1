"""OV7: I - max J = edge_loss + fragment, both nonnegative."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from typing import Sequence

from diagram import Edge, Section, cob, coord, mass, nu


def observed(s: Section, edges: Sequence[Edge]) -> int:
    return sum(abs(coord(cob(s, e))) for e in edges)


def edge_loss(s: Section, edges: Sequence[Edge]) -> int:
    return mass(s, edges) - observed(s, edges)


def fragment(s: Section, edges: Sequence[Edge], max_j: int) -> int:
    obs = observed(s, edges)
    if max_j > obs:
        raise ValueError("max J exceeds observed mass")
    return obs - max_j


def gap(s: Section, edges: Sequence[Edge], max_j: int) -> dict[str, int]:
    i = mass(s, edges)
    el = edge_loss(s, edges)
    fr = fragment(s, edges, max_j)
    return {"I": i, "maxJ": max_j, "edge_loss": el, "fragment": fr, "sum": el + fr}


def observer_j(s: Section, edges: Sequence[Edge], mask: Sequence[bool]) -> int:
    total = 0
    for edge, watched in zip(edges, mask, strict=True):
        if watched:
            total += abs(coord(cob(s, edge)))
    return total


def max_observer_j(
    s: Section, edges: Sequence[Edge], observers: Sequence[Sequence[bool]]
) -> int:
    if not observers:
        raise ValueError("no observers")
    return max(observer_j(s, edges, mask) for mask in observers)


def gap_from_observers(
    s: Section, edges: Sequence[Edge], observers: Sequence[Sequence[bool]]
) -> dict[str, int]:
    return gap(s, edges, max_observer_j(s, edges, observers))
