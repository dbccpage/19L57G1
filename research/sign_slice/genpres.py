"""The GenPres grammar: finite generator presentations, priced.

A GenPres is a tuple of priced ingredients: objects, declared arrows
with per-arrow fibre transports, one observer fibre size (the
kernel-of-identity observer: admissible pairs are ordered pairs of
distinct labels), a weighting (amp per arrow), a declared generator
list, a declared forest rule, and the derived occurrence-slot list.
Walks are computed from arrows; an infinite walk set is never data.

Everything is deterministic, exact, and typed.  The mover-family
builder reconstructs, natively, the configuration families the sibling
packet surveyed (METATHEORY: a reconstruction, not an import).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations
from typing import Iterable, Optional

Perm = tuple[int, ...]


def compose(p: Perm, q: Perm) -> Perm:
    """(p after q): apply q, then p."""

    return tuple(p[q[i]] for i in range(len(q)))


def inverse(p: Perm) -> Perm:
    out = [0] * len(p)
    for i, v in enumerate(p):
        out[v] = i
    return tuple(out)


def identity(n: int) -> Perm:
    return tuple(range(n))


@dataclass(frozen=True)
class Arrow:
    src: int
    dst: int
    transport: Perm
    amp: int


@dataclass(frozen=True)
class GenPres:
    """A finite generator presentation.  ``fibre`` is the label count of
    the kernel observer at every object; ``generators`` indexes into
    ``arrows``; the forest is the declared deterministic rule (breadth
    first from the least object of each component) and so is data by
    declaration rather than by table."""

    objects: tuple[int, ...]
    arrows: tuple[Arrow, ...]
    fibre: int
    generators: tuple[int, ...]

    def occurrence_slots(self) -> list[tuple[int, str]]:
        return [(i, end) for i in range(len(self.arrows)) for end in ("source", "target")]


def is_genpres(
    objects: Iterable[int],
    arrows: Iterable[tuple[int, int, Perm]],
    fibre: int,
    amps: Optional[Iterable[int]],
) -> tuple[bool, str]:
    """Grammar membership.  A missing weighting refuses the tuple: the
    weighting is on the bill (FW-BILL)."""

    objs = tuple(objects)
    arrs = tuple(arrows)
    if amps is None:
        return False, "REFUSED: weighting absent; the weighting is a priced ingredient"
    amp_list = tuple(amps)
    if len(amp_list) != len(arrs):
        return False, "REFUSED: weighting does not cover every arrow"
    if fibre < 1:
        return False, "REFUSED: empty fibre"
    for src, dst, transport in arrs:
        if src not in objs or dst not in objs:
            return False, "REFUSED: arrow endpoint outside the object list"
        if sorted(transport) != list(range(fibre)):
            return False, "REFUSED: transport is not a bijection of the fibre"
    return True, "ADMITTED"


def make(
    objects: Iterable[int],
    arrows: Iterable[tuple[int, int, Perm]],
    fibre: int,
    amps: Iterable[int],
) -> GenPres:
    objs = tuple(objects)
    arrs = tuple(
        Arrow(src, dst, transport, amp)
        for (src, dst, transport), amp in zip(arrows, amps, strict=True)
    )
    return GenPres(objs, arrs, fibre, tuple(range(len(arrs))))


def mu_g(p: GenPres) -> tuple[int, int, int]:
    """The declared cost measure: (object count, arrow count, distinct
    amp values), lexicographic."""

    return (len(p.objects), len(p.arrows), len({a.amp for a in p.arrows}))


def iso_key(p: GenPres) -> str:
    """Canonical key: minimum serialization over relabelings of the
    object tokens.  Object, arrow, weighting, and occurrence-slot
    structure is retained; only the presentation tokens are forgotten."""

    n = len(p.objects)
    best: Optional[str] = None
    for perm in permutations(range(n)):
        relabel = {obj: perm[i] for i, obj in enumerate(p.objects)}
        arrs = sorted(
            (relabel[a.src], relabel[a.dst], a.transport, a.amp) for a in p.arrows
        )
        key = repr((n, p.fibre, arrs))
        if best is None or key < best:
            best = key
    assert best is not None
    return best


# ---------------------------------------------------------------------------
# The mover-family reconstruction (METATHEORY)
# ---------------------------------------------------------------------------

Site = int
Edge = tuple[Site, Site]


def chain_sites(n: int) -> list[Edge]:
    return [(i, i + 1) for i in range(n - 1)]


def grid_sites(rows: int, cols: int) -> list[Edge]:
    edges: list[Edge] = []
    for r in range(rows):
        for c in range(cols):
            v = r * cols + c
            if c + 1 < cols:
                edges.append((v, v + 1))
            if r + 1 < rows:
                edges.append((v, v + cols))
    return edges


def star_sites(leaves: int) -> list[Edge]:
    return [(0, i + 1) for i in range(leaves)]


def mover_family(
    sites: int, edges: list[Edge], occupancy: int, signed: bool
) -> GenPres:
    """Objects are the sorted occupied-site tuples; an arrow moves one
    occupant along an edge to a free site; the fibre is the list of
    rank orderings (which mover holds which rank), and the transport is
    the rank cycle the move induces.  ``signed`` puts amp -1 on every
    transport that is not the identity, +1 otherwise; unsigned puts
    amp 1 everywhere."""

    adjacency: dict[Site, set[Site]] = {s: set() for s in range(sites)}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    configs = sorted(combinations(range(sites), occupancy))
    index = {c: i for i, c in enumerate(configs)}
    labels = sorted(permutations(range(occupancy)))
    label_index = {l: i for i, l in enumerate(labels)}
    arrows: list[tuple[int, int, Perm]] = []
    for c in configs:
        occupied = set(c)
        for rank, s in enumerate(c):
            for t in adjacency[s]:
                if t in occupied:
                    continue
                new = tuple(sorted((occupied - {s}) | {t}))
                new_rank = new.index(t)
                # the rank cycle: the mover at ``rank`` lands at
                # ``new_rank``; movers between shift by one
                cycle = list(range(occupancy))
                del cycle[rank]
                cycle.insert(new_rank, rank)
                # cycle[r'] = the old rank whose mover now holds r'
                transport = tuple(
                    label_index[tuple(l[cycle[r]] for r in range(occupancy))]
                    for l in labels
                )
                arrows.append((index[c], index[new], transport))
    fibre = len(labels)
    amps = [
        -1 if (signed and arrows[i][2] != identity(fibre)) else 1
        for i in range(len(arrows))
    ]
    return make(range(len(configs)), arrows, fibre, amps)
