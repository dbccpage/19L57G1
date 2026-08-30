"""Two hard-core particles on a finite site graph: does a natural section exist?

The declared family (see STATUS.md, "Hop fixture"): objects are sorted
pairs ``{x < y}`` of distinct occupied sites, the carrier at every object
is ``Bool`` (``False`` the smaller site, ``True`` the larger), the admissible
pairs are the two orientations, and an arrow is a hop of one particle to an
adjacent site not occupied by the other.  A hop's transport is the swap
exactly when the mover ends on the far side of the stayer (``flip``); it is
the identity otherwise.  Every transport is therefore the identity or the
swap, so the transport of a walk is the parity of its flips, and a natural
section exists iff every closed walk has even parity -- which by the
generator form of the criterion (Lean ``natural_section_iff_generators``)
is: relative to a breadth-first tree from the base, every non-tree hop's
generator has even parity.

Deterministic, standard library only.  This is finite computation; the
Lean fixture carries the chain and the square as theorems.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from collections import deque
from dataclasses import dataclass
from typing import Iterator, Sequence

Site = int
Config = tuple[Site, Site]
Edge = tuple[Site, Site]


def _adjacent(edges: Sequence[Edge], u: Site, v: Site) -> bool:
    return (u, v) in edges or (v, u) in edges


def hop(edges: Sequence[Edge], a: Config, b: Config) -> tuple[bool, bool]:
    """Whether ``b`` is one hop from ``a``, and whether that hop flips.

    Cases, with ``a = (x, y)`` and ``b = (x', y')`` both sorted:
    the stayer keeps its index (no flip) when ``x' = x`` and ``y`` moved, or
    ``y' = y`` and ``x`` moved; the stayer changes index (flip) when
    ``y' = x`` (``y`` moved below ``x``) or ``x' = y`` (``x`` moved above
    ``y``).  At most one case holds because the pairs are sorted and the
    site graph has no loops.
    """

    x, y = a
    xp, yp = b
    if a == b:
        return (False, False)
    if xp == x and _adjacent(edges, y, yp):
        return (True, False)
    if yp == y and _adjacent(edges, x, xp):
        return (True, False)
    if yp == x and _adjacent(edges, y, xp):
        return (True, True)
    if xp == y and _adjacent(edges, x, yp):
        return (True, True)
    return (False, False)


def configurations(sites: int) -> list[Config]:
    return [(x, y) for x in range(sites) for y in range(x + 1, sites)]


@dataclass(frozen=True)
class Verdict:
    name: str
    sites: int
    edges: tuple[Edge, ...]
    objects: int
    arrows: int
    base: Config
    reachable: int
    section_exists: bool
    odd_generators: int
    witness: tuple[Config, ...] | None

    def json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "sites": self.sites,
            "edges": [list(e) for e in self.edges],
            "objects": self.objects,
            "arrows": self.arrows,
            "base": list(self.base),
            "reachable_from_base": self.reachable,
            "section_exists": self.section_exists,
            "odd_generators": self.odd_generators,
            "witness_closed_walk": (
                None if self.witness is None else [list(c) for c in self.witness]
            ),
        }


def _arrows(edges: Sequence[Edge], objs: Sequence[Config]) -> list[tuple[Config, Config, bool]]:
    out: list[tuple[Config, Config, bool]] = []
    for a in objs:
        for b in objs:
            is_hop, flip = hop(edges, a, b)
            if is_hop:
                out.append((a, b, flip))
    return out


def analyse(name: str, sites: int, edges: Sequence[Edge]) -> Verdict:
    """Decide the criterion for two particles on the given site graph."""

    canonical = tuple(sorted((min(u, v), max(u, v)) for u, v in edges))
    objs = configurations(sites)
    arrows = _arrows(canonical, objs)
    base = objs[0]
    # Breadth-first tree from the base: parent and parity potential.
    parent: dict[Config, Config | None] = {base: None}
    parity: dict[Config, int] = {base: 0}
    queue: deque[Config] = deque([base])
    neighbours: dict[Config, list[tuple[Config, bool]]] = {o: [] for o in objs}
    for a, b, flip in arrows:
        neighbours[a].append((b, flip))
    while queue:
        a = queue.popleft()
        for b, flip in neighbours[a]:
            if b not in parity:
                parity[b] = parity[a] ^ int(flip)
                parent[b] = a
                queue.append(b)
    # Generator check: every hop between reached objects must respect the potential.
    odd: list[tuple[Config, Config]] = []
    for a, b, flip in arrows:
        if a in parity and b in parity and (parity[a] ^ int(flip)) != parity[b]:
            odd.append((a, b))
    witness: tuple[Config, ...] | None = None
    if odd:
        a, b = odd[0]
        witness = tuple(_tree_path(parent, a)) + tuple(reversed(_tree_path(parent, b)))
    return Verdict(
        name=name,
        sites=sites,
        edges=canonical,
        objects=len(objs),
        arrows=len(arrows),
        base=base,
        reachable=len(parity),
        section_exists=not odd,
        odd_generators=len(odd),
        witness=witness,
    )


def _tree_path(parent: dict[Config, Config | None], a: Config) -> list[Config]:
    path: list[Config] = []
    cursor: Config | None = a
    while cursor is not None:
        path.append(cursor)
        cursor = parent[cursor]
    path.reverse()
    return path


def chain(n: int) -> list[Edge]:
    return [(i, i + 1) for i in range(n - 1)]


def grid(rows: int, cols: int) -> list[Edge]:
    edges: list[Edge] = []
    for r in range(rows):
        for c in range(cols):
            s = r * cols + c
            if c + 1 < cols:
                edges.append((s, s + 1))
            if r + 1 < rows:
                edges.append((s, s + cols))
    return edges


def star(leaves: int) -> list[Edge]:
    return [(0, i) for i in range(1, leaves + 1)]


def fixtures() -> Iterator[tuple[str, int, list[Edge]]]:
    yield "chain_P2", 2, chain(2)
    yield "chain_P3", 3, chain(3)
    yield "chain_P4", 4, chain(4)
    yield "chain_P5", 5, chain(5)
    yield "chain_P6", 6, chain(6)
    yield "square_2x2", 4, grid(2, 2)
    yield "ladder_2x3", 6, grid(2, 3)
    yield "star_K13", 4, star(3)
    yield "triangle_C3", 3, [(0, 1), (1, 2), (0, 2)]


def summary() -> dict[str, bool]:
    """Fixture name to "a natural section exists", in fixture order."""

    return {name: analyse(name, sites, edges).section_exists for name, sites, edges in fixtures()}


def report() -> dict[str, object]:
    verdicts = [analyse(name, sites, edges) for name, sites, edges in fixtures()]
    return {
        "family": {
            "object": "sorted pair {x < y} of distinct occupied sites (unlabelled)",
            "carrier": "Bool: false the smaller site, true the larger",
            "observer": "boolEqObs; admissible pairs (false,true) and (true,false)",
            "arrow": "a hop of one particle to an adjacent site not occupied by the other",
            "transport": "swap iff the mover ends on the far side of the stayer, else identity",
            "criterion": "natural_section_iff_generators, breadth-first tree from the base",
        },
        "fixtures": [v.json() for v in verdicts],
        "summary": summary(),
    }
