"""Deterministic mirror of ``lean4/Derivation/Attachment.lean`` and
``lean4/Derivation/LadderGeneral.lean``.

Attachment: one-edge gluing along a represented parent under an
arbitrary policy; tree theorems (unique ascending parent, root
reachability, ``V - E = 1``); the complete ``Up`` family with
presentation invariance; orbit computation over the oriented-store
automorphisms (the star's leaves form one orbit; the oriented path
is rigid).  Generalized ladder: dimension-indexed complexes, one
shell guard uniform in the dimension, replayed demonstrations at
dimensions 4 and 5, and the boundary-composite checks.

Imported (declared, not derived): fresh occurrence supply,
protection, budget/activation, cell encoding, boundary signs.
"""

from __future__ import annotations

from itertools import permutations
from typing import Callable, Optional

from derivation.export import Json
from derivation.primitive_passage import (
    GENESIS_P,
    PS,
    PEvent,
    preplay,
)

Policy = Callable[[int], int]
Pair = tuple[int, int]


def par(pi: Policy, k: int) -> int:
    return min(pi(k + 1), k)


def attach_block(pi: Policy, k: int) -> list[PEvent]:
    p = par(pi, k)
    return [("admitOcc", k + 1), ("assertWit", p, k + 1),
            ("admitWit", p, k + 1), ("protect", p, k + 1)]


def attach_hist(pi: Policy, n: int) -> list[PEvent]:
    out: list[PEvent] = [("admitOcc", 0)]
    for k in range(n):
        out.extend(attach_block(pi, k))
    return out


def tree_at(pi: Policy, n: int) -> PS:
    return preplay(attach_hist(pi, n), GENESIS_P)


def tree_state(pi: Policy, n: int) -> PS:
    edges = tuple((par(pi, k), k + 1) for k in range(n))
    return PS(occ=tuple(range(n + 1)), asserted=edges, wit=edges,
              prot=edges, obs=None, budget=0, licensed=True,
              refusals=(), halted=False)


def path_pol(i: int) -> int:
    return i - 1


def star_pol(i: int) -> int:
    return 0


def zigzag_pol(i: int) -> int:
    """An arbitrary further policy (deterministic pseudo-shape)."""
    return (i * 7 + 3) % max(1, i)


def is_tree(s: PS) -> bool:
    """Unique ascending parent per non-root vertex, all reach 0."""
    n = len(s.occ)
    children = [c for (_, c) in s.wit]
    if sorted(children) != list(range(1, n)):
        return False
    if not all(p < c for (p, c) in s.wit):
        return False
    parent = {c: p for (p, c) in s.wit}
    for v in range(1, n):
        cur = v
        seen = 0
        while cur != 0 and seen <= n:
            cur = parent[cur]
            seen += 1
        if cur != 0:
            return False
    return True


def tree_report(rounds: int) -> dict[str, Json]:
    policies: list[tuple[str, Policy]] = [
        ("path", path_pol), ("star", star_pol),
        ("zigzag", zigzag_pol)]
    out: dict[str, Json] = {}
    for name, pi in policies:
        rows = []
        for n in range(rounds + 1):
            s = tree_at(pi, n)
            rows.append({
                "n": n,
                "spec_match": s == tree_state(pi, n),
                "V_minus_E": len(s.occ) - len(s.wit),
                "is_tree": is_tree(s),
                "pre_observational": s.obs is None,
            })
        out[name] = {
            "all_spec_match": all(bool(r["spec_match"]) for r in rows),
            "all_residue_one": all(r["V_minus_E"] == 1 for r in rows),
            "all_trees": all(bool(r["is_tree"]) for r in rows),
            "rows": rows,
        }
    return out


def undirected(edges: tuple[Pair, ...]) -> set[frozenset[int]]:
    return {frozenset(e) for e in edges}


def isomorphic_undirected(e1: tuple[Pair, ...],
                          e2: tuple[Pair, ...], n: int) -> bool:
    u1, u2 = undirected(e1), undirected(e2)
    if len(u1) != len(u2):
        return False
    for perm in permutations(range(n)):
        if {frozenset(perm[x] for x in e) for e in u1} == u2:
            return True
    return False


def shape_report() -> dict[str, Json]:
    p4 = tree_at(path_pol, 3).wit
    s4 = tree_at(star_pol, 3).wit
    return {
        "path4": [list(e) for e in p4],
        "star4": [list(e) for e in s4],
        "isomorphic_undirected": isomorphic_undirected(p4, s4, 4),
        "trees_but_shapes_differ": (
            is_tree(tree_at(path_pol, 3))
            and is_tree(tree_at(star_pol, 3))
            and not isomorphic_undirected(p4, s4, 4)),
    }


# ---------------------------------------------------------------------------
# Up: the complete family, presentation invariance, orbits


def attach_moves(s: PS) -> list[list[PEvent]]:
    n = len(s.occ)
    return [[("admitOcc", n), ("assertWit", p, n),
             ("admitWit", p, n), ("protect", p, n)]
            for p in range(n)]


def store_automorphisms(s: PS) -> list[tuple[int, ...]]:
    """Permutations of positions fixing the ORIENTED stores setwise
    (occurrence tokens follow positions in the drivers here)."""
    n = len(s.occ)
    out = []
    wit = set(s.wit)
    prot = set(s.prot)
    ass = set(s.asserted)
    for perm in permutations(range(n)):
        def r(p: Pair, perm: tuple[int, ...] = perm) -> Pair:
            return (perm[p[0]], perm[p[1]])
        if ({r(p) for p in wit} == wit
                and {r(p) for p in prot} == prot
                and {r(p) for p in ass} == ass):
            out.append(perm)
    return out


def parent_orbits(s: PS) -> list[list[int]]:
    """Orbits of parent choices under the store automorphisms —
    orbit-valued choices where symmetry remains."""
    n = len(s.occ)
    autos = store_automorphisms(s)
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for p in range(n):
        if p in seen:
            continue
        orbit = sorted({perm[p] for perm in autos})
        orbits.append(orbit)
        seen.update(orbit)
    return orbits


def up_report() -> dict[str, Json]:
    star3 = tree_at(star_pol, 2)
    path3 = tree_at(path_pol, 2)
    return {
        "family_length_equals_parents": all(
            len(attach_moves(tree_at(path_pol, n))) == n + 1
            for n in range(6)),
        "presentation_invariant": (
            attach_moves(star3) == attach_moves(path3)),
        "star3_parent_orbits": parent_orbits(star3),
        "path3_parent_orbits": parent_orbits(path3),
        "star_leaves_one_orbit":
            parent_orbits(star3) == [[0], [1, 2]],
        "oriented_path_rigid":
            parent_orbits(path3) == [[0], [1], [2]],
    }


# ---------------------------------------------------------------------------
# The generalized ladder (mirror of LadderGeneral)

CellsN = dict[int, list[tuple[int, ...]]]


def facets(sigma: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [sigma[:i] + sigma[i + 1:] for i in range(len(sigma))]


def shell_n(cells: CellsN, k: int, sigma: tuple[int, ...]) -> bool:
    return (len(sigma) == k + 1 and k >= 1
            and all(tau in cells.get(k - 1, [])
                    for tau in facets(sigma))
            and sigma not in cells.get(k, []))


def step_v(cells: CellsN, v: int) -> CellsN:
    if (v,) in cells.get(0, []):
        return cells
    out = dict(cells)
    out[0] = cells.get(0, []) + [(v,)]
    return out


def step_n(cells: CellsN, k: int, sigma: tuple[int, ...]) -> CellsN:
    if shell_n(cells, k, sigma):
        out = dict(cells)
        out[k] = cells.get(k, []) + [sigma]
        return out
    return cells


def combs(n: int, m: int) -> list[tuple[int, ...]]:
    """All (m+1)-vertex ascending cells over the first n vertices."""
    def aux(need: int, pool: list[int]) -> list[tuple[int, ...]]:
        if need == 0:
            return [()]
        if not pool:
            return []
        x, rest = pool[0], pool[1:]
        return ([(x,) + t for t in aux(need - 1, rest)]
                + aux(need, rest))
    return aux(m + 1, list(range(n)))


def full_shell_complex(n: int, top: bool) -> CellsN:
    """Replay the complete complex on ``n`` vertices up to dimension
    ``n-1``, optionally with the top cell."""
    cells: CellsN = {}
    for v in range(n):
        cells = step_v(cells, v)
    for k in range(1, n - 1):
        for sigma in combs(n, k):
            cells = step_n(cells, k, sigma)
    if top:
        cells = step_n(cells, n - 1, tuple(range(n)))
    return cells


def sgn(i: int) -> int:
    return 1 if i % 2 == 0 else -1


def bd_n(sigma: tuple[int, ...]) -> list[tuple[int, tuple[int, ...]]]:
    return [(sgn(i), sigma[:i] + sigma[i + 1:])
            for i in range(len(sigma))]


def push_n(ch: list[tuple[int, tuple[int, ...]]]
           ) -> list[tuple[int, tuple[int, ...]]]:
    return [(c * d, tau) for (c, s) in ch for (d, tau) in bd_n(s)]


def coeff_n(tau: tuple[int, ...],
            ch: list[tuple[int, tuple[int, ...]]]) -> int:
    return sum(c for (c, t) in ch if t == tau)


def d2_zero_dim(sigma: tuple[int, ...]) -> bool:
    ch = push_n(bd_n(sigma))
    return all(coeff_n(t, ch) == 0
               for t in {t for (_, t) in ch})


def ladder_report(max_dim: int) -> dict[str, Json]:
    per_dim: dict[str, dict[str, Json]] = {}
    for d in range(2, max_dim + 1):
        n = d + 1
        shell = full_shell_complex(n, top=False)
        filled = full_shell_complex(n, top=True)
        top_cell = tuple(range(n))
        missing = dict(shell)
        missing[d - 1] = missing.get(d - 1, [])[1:]
        per_dim[str(d)] = {
            "shell_admits_top": shell_n(shell, d, top_cell),
            "filled_has_top": filled.get(d) == [top_cell],
            "guard_load_bearing":
                step_n(missing, d, top_cell) == missing,
            "d2_zero_top": d2_zero_dim(top_cell),
            "cells_per_dim": {
                str(k): len(filled.get(k, []))
                for k in range(0, d + 1)},
        }
    per_dim_json: dict[str, Json] = dict(per_dim)
    return {
        "dims_checked": list(range(2, max_dim + 1)),
        "all_ladders_fire": all(
            bool(per_dim[str(d)]["shell_admits_top"])
            and bool(per_dim[str(d)]["filled_has_top"])
            for d in range(2, max_dim + 1)),
        "all_guards_load_bearing": all(
            bool(per_dim[str(d)]["guard_load_bearing"])
            for d in range(2, max_dim + 1)),
        "all_d2_zero": all(
            bool(per_dim[str(d)]["d2_zero_top"])
            for d in range(2, max_dim + 1)),
        "per_dim": per_dim_json,
        "general_d2_zero":
            "conjecture beyond the checked dimensions; declared "
            "coefficients and signs carry the content",
    }
