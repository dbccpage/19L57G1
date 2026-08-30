"""What removes an obstruction and what cannot: pointwise re-presentation,
arrow deletion, and the cover, on the two-label square and chain.

The two-label family of a site graph has the sorted occupied pairs as
objects, ``Bool`` as carrier, and a flip bit per hop (``holonomy_fixture``).

* A POINTWISE re-presentation chooses, at each object, the identity or the
  swap of ``Bool`` and conjugates every hop: the new flip bit of ``a -> b``
  is ``flip xor g[a] xor g[b]``.  Same objects, same hops.
* ARROW DELETION keeps a subset of the undirected hops.
* The COVER drops the flip bit everywhere (labelled configurations read
  through unlabelled ones).

For each variant the class is decided per connected component by parity
potentials along a breadth-first tree, as in ``holonomy_fixture``: a
natural section exists iff every remaining cycle has even flip parity.
Deterministic, standard library only.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from collections import deque
from itertools import combinations, product
from typing import Sequence

import holonomy_fixture as two

Config = tuple[int, int]
Edge = tuple[int, int]
Hop = tuple[Config, Config]


def undirected_hops(sites: int, edges: Sequence[Edge]) -> list[tuple[Hop, bool]]:
    """Each undirected hop once (smaller object first), with its flip bit."""

    objs = two.configurations(sites)
    out: list[tuple[Hop, bool]] = []
    for a in objs:
        for b in objs:
            if a < b:
                is_hop, flip = two.hop(edges, a, b)
                if is_hop:
                    out.append(((a, b), flip))
    return out


def components_even(objs: Sequence[Config], hops: Sequence[tuple[Hop, bool]]) -> tuple[bool, int, int]:
    """(every component has even parity on every cycle, number of components,
    number of odd generators)."""

    nbrs: dict[Config, list[tuple[Config, bool]]] = {o: [] for o in objs}
    for (a, b), flip in hops:
        nbrs[a].append((b, flip))
        nbrs[b].append((a, flip))
    parity: dict[Config, int] = {}
    comps = 0
    odd = 0
    for base in objs:
        if base in parity:
            continue
        comps += 1
        parity[base] = 0
        queue: deque[Config] = deque([base])
        while queue:
            x = queue.popleft()
            for y, flip in nbrs[x]:
                if y not in parity:
                    parity[y] = parity[x] ^ int(flip)
                    queue.append(y)
    for (a, b), flip in hops:
        if (parity[a] ^ int(flip)) != parity[b]:
            odd += 1
    return (odd == 0, comps, odd)


def repres_all(sites: int, edges: Sequence[Edge]) -> dict[str, object]:
    """Every pointwise re-presentation: identity or swap at each object."""

    objs = two.configurations(sites)
    hops = undirected_hops(sites, edges)
    clean = 0
    total = 0
    for choice in product((0, 1), repeat=len(objs)):
        g = dict(zip(objs, choice))
        conj = [((a, b), bool(int(flip) ^ g[a] ^ g[b])) for (a, b), flip in hops]
        ok, _, _ = components_even(objs, conj)
        total += 1
        clean += int(ok)
    base_ok, _, _ = components_even(objs, hops)
    return {
        "objects": len(objs),
        "re_presentations": total,
        "with_section": clean,
        "original_has_section": base_ok,
        "class_invariant": clean in (0, total) and (clean == total) == base_ok,
    }


def deletions(sites: int, edges: Sequence[Edge]) -> dict[str, object]:
    """Every subset of the undirected hops; which make every component even,
    and the minimal deletion sets among them."""

    objs = two.configurations(sites)
    hops = undirected_hops(sites, edges)
    n = len(hops)
    good_deletions: list[tuple[int, ...]] = []
    for size in range(n + 1):
        for dele in combinations(range(n), size):
            keep = [hops[i] for i in range(n) if i not in dele]
            ok, _, _ = components_even(objs, keep)
            if ok:
                good_deletions.append(dele)
    minimum = min((len(d) for d in good_deletions), default=None)
    minimal = [d for d in good_deletions if len(d) == minimum]
    return {
        "hops": [{"from": list(a), "to": list(b), "flip": flip} for (a, b), flip in hops],
        "subsets": 2 ** n,
        "subsets_with_section": len(good_deletions),
        "minimum_deletion": minimum,
        "minimal_deletion_sets": [
            [{"from": list(hops[i][0][0]), "to": list(hops[i][0][1])} for i in d] for d in minimal
        ],
        "single_deletion_suffices": minimum == 1,
    }


def cover(sites: int, edges: Sequence[Edge]) -> dict[str, object]:
    objs = two.configurations(sites)
    hops = [((a, b), False) for (a, b), _ in undirected_hops(sites, edges)]
    ok, comps, odd = components_even(objs, hops)
    return {"section_exists": ok, "components": comps, "odd_generators": odd}


def report() -> dict[str, object]:
    return {
        "moves": {
            "pointwise_re_presentation": "identity or swap at each object; hop flips conjugated",
            "arrow_deletion": "a subset of the undirected hops is kept",
            "cover": "the flip bit dropped everywhere",
        },
        "square": {
            "re_presentation": repres_all(4, two.grid(2, 2)),
            "deletion": deletions(4, two.grid(2, 2)),
            "cover": cover(4, two.grid(2, 2)),
        },
        "chain": {
            "re_presentation": repres_all(4, two.chain(4)),
            "deletion": {
                "subsets_with_section": deletions(4, two.chain(4))["subsets_with_section"],
                "subsets": deletions(4, two.chain(4))["subsets"],
            },
            "cover": cover(4, two.chain(4)),
        },
        "star": {
            "re_presentation": repres_all(4, two.star(3)),
            "deletion": {
                "minimum_deletion": deletions(4, two.star(3))["minimum_deletion"],
                "subsets_with_section": deletions(4, two.star(3))["subsets_with_section"],
            },
        },
    }
