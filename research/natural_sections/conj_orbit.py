"""Twisted sums on holonomy orbits for a conjugation-closed weighting.

The repaired A2 (see ``STATUS.md`` and NS-38): the twisted sum is
constant on a holonomy orbit when the weighting is conjugation-closed
AND the declared list is closed under conjugation up to transport and
weight.  This module surveys the square at ``k = 2``: the holonomy set
of the closed walks up to the declared length, closed under composition
into a finite group; the orbits of the ordered index pairs under that
group; the unit-weighted twisted sum at every orbit member; a two-walk
mini list mirroring the Lean instance; and an exhaustive check that the
unit weighting is conjugation-closed over the walks up to a smaller
length bound.  The conjugate of a closed walk ``w`` by a closed walk
``u`` at the same base is ``u ++ w ++ reverse(u)``; every hop's reverse
is itself a declared hop, so the conjugate is a walk of the family.
Deterministic, standard library only.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import holonomy_fixture as two
import holonomy_group as hg
import weighted_sum as ws

Config = ws.Config
Perm = ws.Perm
Walk = ws.Walk
Edge = ws.Edge
Pair = tuple[int, int]


def holonomy_closure(perms: set[Perm]) -> set[Perm]:
    """The closure of a finite set of permutations under composition.

    A finite set of permutations closed under composition contains every
    inverse (each element has finite order), so this is the generated
    group whenever the set is nonempty."""

    group: set[Perm] = set(perms)
    frontier: set[Perm] = set(perms)
    while frontier:
        new: set[Perm] = set()
        for g in sorted(frontier):
            for f in sorted(group):
                for h in (hg.compose(g, f), hg.compose(f, g)):
                    if h not in group and h not in new:
                        new.add(h)
        group |= new
        frontier = new
    return group


def orbits(group: set[Perm], k: int) -> list[list[Pair]]:
    """The orbits of the ordered pairs of distinct indices under the group."""

    out: list[list[Pair]] = []
    seen: set[Pair] = set()
    for i in range(k):
        for j in range(k):
            if i == j or (i, j) in seen:
                continue
            orbit = sorted({(g[i], g[j]) for g in group})
            seen.update(orbit)
            out.append(orbit)
    return out


def reverse_walk(walk: Walk) -> Walk:
    return tuple((b, a) for a, b in reversed(walk))


def conjugate(u: Walk, w: Walk) -> Walk:
    """``u ++ w ++ reverse(u)``: the conjugate of ``w`` by ``u``."""

    return u + w + reverse_walk(u)


def walk_perm(edges: list[Edge], walk: Walk) -> Perm:
    """The holonomy of a walk, recomputed hop by hop (earliest hop first)."""

    perm = hg.identity(2)
    for a, b in walk:
        step = hg.hop_perm(edges, a, b)
        if step is None:
            raise ValueError(f"not a declared hop: {a} -> {b}")
        perm = hg.compose(step, perm)
    return perm


def unit_closure_check(walks: list[tuple[Walk, Perm]]) -> dict[str, int]:
    """Check ``weight(u ++ w ++ reverse(u)) = weight(w)`` for the unit
    weighting over every ordered pair of the given closed walks."""

    pairs = 0
    violations = 0
    for u, _ in walks:
        for w, _ in walks:
            pairs += 1
            if ws.weight(conjugate(u, w), ws.unit_amp) != ws.weight(w, ws.unit_amp):
                violations += 1
    return {"walks": len(walks), "pairs": pairs, "violations": violations}


def report() -> dict[str, object]:
    edges = two.grid(2, 2)
    adj = ws.arrows(4, edges, 2)
    base = sorted(adj)[0]
    walks = ws.closed_walks(adj, base, 6)
    group = holonomy_closure({perm for _, perm in walks})
    orbit_rows: list[dict[str, object]] = []
    all_agree = True
    for orbit in orbits(group, 2):
        sums = [ws.twisted(walks, ws.unit_amp, p) for p in orbit]
        agree = len(set(sums)) == 1
        all_agree = all_agree and agree
        orbit_rows.append(
            {
                "orbit": [list(p) for p in orbit],
                "twisted_unit": sums,
                "agree": agree,
            }
        )
    exchange, exchange_perm = next(
        (w, perm) for w, perm in walks if len(w) == 4 and perm == (1, 0)
    )
    mini: list[tuple[Walk, Perm]] = [((), hg.identity(2)), (exchange, exchange_perm)]
    walks4 = ws.closed_walks(adj, base, 4)
    return {
        "layer": {
            "conjugate": "u ++ w ++ reverse(u), closed walks at the base",
            "conjugation_closed": "weight(conjugate(u, w)) = weight(w) for all u, w",
            "orbit": "the ordered index pairs under the composition closure of the walk holonomies",
        },
        "square_k2": {
            "base": list(base),
            "max_len": 6,
            "closed_walks": len(walks),
            "holonomy_group": sorted(list(g) for g in group),
            "group_order": len(group),
            "orbits": orbit_rows,
            "all_orbits_agree": all_agree,
        },
        "mini_list": {
            "walks": [[[list(a), list(b)] for a, b in w] for w, _ in mini],
            "twisted_unit": {f"{i},{j}": ws.twisted(mini, ws.unit_amp, (i, j)) for i, j in ((0, 1), (1, 0))},
            "total_unit": ws.total(mini, ws.unit_amp),
        },
        "unit_conjugation_closure": {"max_len": 4, **unit_closure_check(walks4)},
        "cited_counterexample": (
            "receipts/weighted_sum.json key orbit_counterexample: the unit weighting is"
            " conjugation-closed, yet on the ladder at k = 4 a single generator walk has"
            " twisted sums 1 and 0 on one orbit -- the list-closure hypothesis cannot be"
            " dropped (NS-38, kept)"
        ),
    }
