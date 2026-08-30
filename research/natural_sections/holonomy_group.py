"""``k`` hard-core particles on a site graph: the holonomy group and the criterion.

Generalises ``holonomy_fixture.py`` from two labels to ``k``.  An object is
a sorted ``k``-subset of occupied sites; the carrier at every object is
``Fin k`` (index ``i`` the ``i``-th smallest occupied site); the admissible
pairs are the ordered pairs of distinct indices; an arrow is one particle
hopping to an adjacent empty site; its transport is the induced
permutation of sorted indices, computed from positions.

For each connected component of the configuration graph a breadth-first
tree from the least object gives a potential (a permutation from the base
to every object) and, for every hop, a generator at the base
``pot[b]^-1 . T(a -> b) . pot[a]``.  The holonomy group is the closure of
the generators under composition (finite).  The criterion of
``natural_section_iff_holonomy`` is: the group has at least two common
fixed points.  Parity ("every element even") is reported next to it so
the two can be seen to agree or come apart.  Deterministic, standard
library only.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from collections import deque
from dataclasses import dataclass
from itertools import combinations
from typing import Sequence

import holonomy_fixture as two

Site = int
Config = tuple[Site, ...]
Perm = tuple[int, ...]
Edge = tuple[Site, Site]


def identity(k: int) -> Perm:
    return tuple(range(k))


def compose(g: Perm, f: Perm) -> Perm:
    """``g . f``: apply ``f`` first."""

    return tuple(g[f[i]] for i in range(len(f)))


def inverse(f: Perm) -> Perm:
    out = [0] * len(f)
    for i, j in enumerate(f):
        out[j] = i
    return tuple(out)


def is_even(f: Perm) -> bool:
    seen = [False] * len(f)
    transpositions = 0
    for i in range(len(f)):
        if seen[i]:
            continue
        length = 0
        j = i
        while not seen[j]:
            seen[j] = True
            j = f[j]
            length += 1
        transpositions += length - 1
    return transpositions % 2 == 0


def hop_perm(edges: Sequence[Edge], a: Config, b: Config) -> Perm | None:
    """The transport of the hop ``a -> b`` on sorted indices, or ``None``."""

    if len(a) != len(b) or a == b:
        return None
    left = sorted(set(a) - set(b))
    right = sorted(set(b) - set(a))
    if len(left) != 1 or len(right) != 1:
        return None
    mover, target = left[0], right[0]
    if not two._adjacent(edges, mover, target):
        return None
    perm: list[int] = []
    for site in a:
        new_site = target if site == mover else site
        perm.append(b.index(new_site))
    return tuple(perm)


def closure(generators: Sequence[Perm], k: int) -> list[Perm]:
    group = {identity(k)}
    frontier = [identity(k)]
    while frontier:
        nxt: list[Perm] = []
        for g in frontier:
            for h in generators:
                gh = compose(h, g)
                if gh not in group:
                    group.add(gh)
                    nxt.append(gh)
        frontier = nxt
    return sorted(group)


@dataclass(frozen=True)
class Component:
    base: Config
    size: int
    group_order: int
    all_even: bool
    common_fixed: tuple[int, ...]
    fixed_pair_exists: bool
    trivial: bool
    witness: tuple[Config, ...] | None
    witness_perm: Perm | None

    def json(self) -> dict[str, object]:
        return {
            "base": list(self.base),
            "size": self.size,
            "group_order": self.group_order,
            "all_even": self.all_even,
            "common_fixed_points": list(self.common_fixed),
            "fixed_pair_exists": self.fixed_pair_exists,
            "trivial": self.trivial,
            "witness_closed_walk": (
                None if self.witness is None else [list(c) for c in self.witness]
            ),
            "witness_permutation": None if self.witness_perm is None else list(self.witness_perm),
        }


@dataclass(frozen=True)
class VerdictK:
    name: str
    sites: int
    k: int
    edges: tuple[Edge, ...]
    objects: int
    arrows: int
    components: tuple[Component, ...]

    @property
    def section_exists(self) -> bool:
        return all(c.fixed_pair_exists for c in self.components)

    @property
    def parity_says_clean(self) -> bool:
        return all(c.all_even for c in self.components)

    def json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "sites": self.sites,
            "k": self.k,
            "edges": [list(e) for e in self.edges],
            "objects": self.objects,
            "arrows": self.arrows,
            "components": [c.json() for c in self.components],
            "section_exists": self.section_exists,
            "parity_says_clean": self.parity_says_clean,
            "parity_and_fixed_pair_agree": self.section_exists == self.parity_says_clean,
        }


def analyse_k(name: str, sites: int, edges: Sequence[Edge], k: int) -> VerdictK:
    canonical = tuple(sorted((min(u, v), max(u, v)) for u, v in edges))
    objs: list[Config] = [tuple(c) for c in combinations(range(sites), k)]
    arrows: list[tuple[Config, Config, Perm]] = []
    for a in objs:
        for b in objs:
            perm = hop_perm(canonical, a, b)
            if perm is not None:
                arrows.append((a, b, perm))
    neighbours: dict[Config, list[tuple[Config, Perm]]] = {o: [] for o in objs}
    for a, b, perm in arrows:
        neighbours[a].append((b, perm))
    done: set[Config] = set()
    components: list[Component] = []
    for base in objs:
        if base in done:
            continue
        parent: dict[Config, Config | None] = {base: None}
        pot: dict[Config, Perm] = {base: identity(k)}
        queue: deque[Config] = deque([base])
        while queue:
            a = queue.popleft()
            for b, perm in neighbours[a]:
                if b not in pot:
                    pot[b] = compose(perm, pot[a])
                    parent[b] = a
                    queue.append(b)
        done.update(pot)
        generators: list[Perm] = []
        witness: tuple[Config, ...] | None = None
        witness_perm: Perm | None = None
        for a, b, perm in arrows:
            if a in pot and b in pot:
                g = compose(inverse(pot[b]), compose(perm, pot[a]))
                if g != identity(k):
                    generators.append(g)
                    if witness is None:
                        witness = tuple(_tree_path(parent, a)) + tuple(
                            reversed(_tree_path(parent, b))
                        )
                        witness_perm = g
        group = closure(generators, k)
        common = tuple(i for i in range(k) if all(g[i] == i for g in group))
        components.append(
            Component(
                base=base,
                size=len(pot),
                group_order=len(group),
                all_even=all(is_even(g) for g in group),
                common_fixed=common,
                fixed_pair_exists=len(common) >= 2,
                trivial=len(group) == 1,
                witness=witness,
                witness_perm=witness_perm,
            )
        )
    return VerdictK(
        name=name,
        sites=sites,
        k=k,
        edges=canonical,
        objects=len(objs),
        arrows=len(arrows),
        components=tuple(components),
    )


def _tree_path(parent: dict[Config, Config | None], a: Config) -> list[Config]:
    path: list[Config] = []
    cursor: Config | None = a
    while cursor is not None:
        path.append(cursor)
        cursor = parent[cursor]
    path.reverse()
    return path


def k2_agreement() -> dict[str, bool]:
    """Per fixture: the general code at k = 2 agrees with the flip-bit verdict."""

    return {
        name: analyse_k(name, sites, edges, 2).section_exists
        == two.analyse(name, sites, edges).section_exists
        for name, sites, edges in two.fixtures()
    }


def summary_k3() -> dict[str, dict[str, bool]]:
    out: dict[str, dict[str, bool]] = {}
    for name, sites, edges in two.fixtures():
        v = analyse_k(name, sites, edges, 3)
        out[name] = {"section_exists": v.section_exists, "parity_says_clean": v.parity_says_clean}
    return out


def report() -> dict[str, object]:
    runs: dict[str, list[dict[str, object]]] = {"k2": [], "k3": []}
    for name, sites, edges in two.fixtures():
        runs["k2"].append(analyse_k(name, sites, edges, 2).json())
        runs["k3"].append(analyse_k(name, sites, edges, 3).json())
    return {
        "family": {
            "object": "sorted k-subset of occupied sites (unlabelled)",
            "carrier": "Fin k: index i the i-th smallest occupied site",
            "observer": "kernel of the identity; admissible pairs are ordered pairs of distinct indices",
            "arrow": "one particle hops to an adjacent empty site",
            "transport": "the induced permutation of sorted indices, computed from positions",
            "criterion": "natural_section_iff_holonomy: the holonomy group has two common fixed points",
        },
        "k2_agrees_with_flip_bit_receipt": k2_agreement(),
        "runs": runs,
        "summary_k3": summary_k3(),
    }
