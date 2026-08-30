"""Refinement fixtures: subdividing every hop leaves every verdict alone.

A subdivision round replaces each undirected hop of a two-label
configuration graph by two hops through a fresh midpoint node, the flip
bit carried by the first half and the second half flip-free -- the
parity of every cycle is unchanged by construction, and the class is
decided by cycle parity (``representation.components_even``).  Rounds are
iterated; objects and hops grow, verdicts must not move.  Deterministic,
standard library only.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from typing import Sequence

import holonomy_fixture as two
import representation as rp

Node = object
HopEdge = tuple[tuple[Node, Node], bool]


def subdivide(
    objs: Sequence[Node], hops: Sequence[HopEdge]
) -> tuple[list[Node], list[HopEdge]]:
    """One round: each hop `(a, b, flip)` becomes `(a, m, flip)` and
    `(m, b, False)` with `m` a fresh midpoint node."""

    new_objs: list[Node] = list(objs)
    new_hops: list[HopEdge] = []
    for (a, b), flip in hops:
        mid = ("mid", a, b)
        new_objs.append(mid)
        new_hops.append(((a, mid), flip))
        new_hops.append(((mid, b), False))
    return new_objs, new_hops


def rounds(
    sites: int, edges: Sequence[tuple[int, int]], depth: int
) -> list[dict[str, object]]:
    objs: list[Node] = list(two.configurations(sites))
    hops: list[HopEdge] = [((a, b), flip) for (a, b), flip in rp.undirected_hops(sites, edges)]
    out: list[dict[str, object]] = []
    for level in range(depth + 1):
        even, comps, odd = rp.components_even(objs, hops)  # type: ignore[arg-type]
        out.append(
            {
                "round": level,
                "objects": len(objs),
                "hops": len(hops),
                "components": comps,
                "odd_generators": odd,
                "section_exists": even,
            }
        )
        objs, hops = subdivide(objs, hops)
    return out


def report() -> dict[str, object]:
    fixtures = {
        "square_2x2": (4, two.grid(2, 2)),
        "chain_P4": (4, two.chain(4)),
        "star_K13": (4, two.star(3)),
    }
    body = {name: rounds(sites, edges, 2) for name, (sites, edges) in fixtures.items()}
    invariant = {
        name: len({r["section_exists"] for r in rs}) == 1 for name, rs in body.items()
    }
    return {
        "move": "each hop (a, b, flip) becomes (a, m, flip) and (m, b, False), m fresh",
        "rounds": body,
        "verdict_invariant_across_rounds": invariant,
    }
