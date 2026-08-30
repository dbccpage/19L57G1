"""``k`` particles with a ``Z_N`` phase register each: the holonomy and the criterion.

Extends ``holonomy_group.py`` by a phase register per particle.  The
carrier at every object is ``label x Fin N``; the observer is the kernel of
the label projection, so the admissible pairs are the ordered pairs of
distinct labels; a hop's transport is ``(l, phi) -> (sigma l, phi +
theta_l)`` where the mover's register gains the declared edge phase
``A(u, v)`` and every other register is unchanged.  A holonomy is a pair
(permutation, shift vector); composition and inversion are the wreath
product's.  The criterion of ``natural_section_iff_holonomy`` reads: two
labels fixed by every holonomy's permutation with zero shift on both.

A continuous phase is refused by name (``refuse_continuous_phase``): the
phase group here is ``Z_N`` with ``N`` declared, and nothing below is a
statement about the circle.  Deterministic, standard library only.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from collections import deque
from dataclasses import dataclass
from itertools import combinations
from typing import Sequence

import holonomy_fixture as two
import holonomy_group as hg

Site = int
Config = tuple[Site, ...]
Perm = tuple[int, ...]
Shift = tuple[int, ...]
Edge = tuple[Site, Site]
Connection = dict[tuple[Site, Site], int]


def refuse_continuous_phase() -> None:
    """The circle is not a finite decidable type; this tree does not model it."""

    raise ValueError(
        "REFUSED: a continuous phase is not finite or decidable; declare a modulus N "
        "and use Z_N"
    )


def connection(edges: Sequence[Edge], phases: dict[tuple[Site, Site], int], modulus: int) -> Connection:
    """An antisymmetric ``Z_N`` phase on every directed edge; unlisted edges carry ``0``."""

    if modulus < 1:
        raise ValueError("the modulus must be at least 1")
    out: Connection = {}
    for u, v in edges:
        a = phases.get((u, v), -phases.get((v, u), 0)) % modulus
        out[(u, v)] = a
        out[(v, u)] = (-a) % modulus
    return out


def gauge_transform(conn: Connection, g: Sequence[int], modulus: int) -> Connection:
    """``A'(u, v) = A(u, v) + g(v) - g(u)``: same flux, different edge phases."""

    return {(u, v): (a + g[v] - g[u]) % modulus for (u, v), a in conn.items()}


def flux(conn: Connection, cycle: Sequence[Site], modulus: int) -> int:
    """The phase around a closed site walk."""

    total = 0
    for u, v in zip(cycle, cycle[1:]):
        total += conn[(u, v)]
    return total % modulus


Elem = tuple[Perm, Shift]


def identity(k: int) -> Elem:
    return (hg.identity(k), tuple(0 for _ in range(k)))


def compose(g2: Elem, g1: Elem, modulus: int) -> Elem:
    """``g2 . g1``: apply ``g1`` first.  ``(l, phi) -> (s1 l, phi + t1_l) -> (s2 s1 l, phi + t1_l + t2_{s1 l})``."""

    s2, t2 = g2
    s1, t1 = g1
    return (hg.compose(s2, s1), tuple((t1[i] + t2[s1[i]]) % modulus for i in range(len(s1))))


def inverse(g: Elem, modulus: int) -> Elem:
    s, t = g
    sinv = hg.inverse(s)
    return (sinv, tuple((-t[sinv[j]]) % modulus for j in range(len(s))))


def hop(edges: Sequence[Edge], conn: Connection, modulus: int, a: Config, b: Config) -> Elem | None:
    perm = hg.hop_perm(edges, a, b)
    if perm is None:
        return None
    mover = next(iter(set(a) - set(b)))
    target = next(iter(set(b) - set(a)))
    shift = tuple(conn[(mover, target)] % modulus if site == mover else 0 for site in a)
    return (perm, shift)


def closure(generators: Sequence[Elem], k: int, modulus: int) -> list[Elem]:
    group = {identity(k)}
    frontier = [identity(k)]
    while frontier:
        nxt: list[Elem] = []
        for g in frontier:
            for h in generators:
                gh = compose(h, g, modulus)
                if gh not in group:
                    group.add(gh)
                    nxt.append(gh)
        frontier = nxt
    return sorted(group)


@dataclass(frozen=True)
class PhaseComponent:
    base: Config
    size: int
    group_order: int
    permutation_part_trivial: bool
    phase_part_trivial: bool
    common_fixed_labels: tuple[int, ...]
    common_fixed_with_zero_shift: tuple[int, ...]
    fixed_pair_exists: bool
    witness: tuple[Config, ...] | None
    witness_elem: Elem | None

    def json(self) -> dict[str, object]:
        return {
            "base": list(self.base),
            "size": self.size,
            "group_order": self.group_order,
            "permutation_part_trivial": self.permutation_part_trivial,
            "phase_part_trivial": self.phase_part_trivial,
            "common_fixed_labels": list(self.common_fixed_labels),
            "common_fixed_with_zero_shift": list(self.common_fixed_with_zero_shift),
            "fixed_pair_exists": self.fixed_pair_exists,
            "witness_closed_walk": (
                None if self.witness is None else [list(c) for c in self.witness]
            ),
            "witness_element": (
                None
                if self.witness_elem is None
                else {"permutation": list(self.witness_elem[0]), "shift": list(self.witness_elem[1])}
            ),
        }


@dataclass(frozen=True)
class PhaseVerdict:
    name: str
    sites: int
    k: int
    modulus: int
    edges: tuple[Edge, ...]
    conn: tuple[tuple[Site, Site, int], ...]
    objects: int
    arrows: int
    components: tuple[PhaseComponent, ...]

    @property
    def section_exists(self) -> bool:
        return all(c.fixed_pair_exists for c in self.components)

    def json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "sites": self.sites,
            "k": self.k,
            "modulus": self.modulus,
            "edges": [list(e) for e in self.edges],
            "connection": [[u, v, a] for u, v, a in self.conn],
            "objects": self.objects,
            "arrows": self.arrows,
            "components": [c.json() for c in self.components],
            "section_exists": self.section_exists,
        }


def analyse_phase(
    name: str, sites: int, edges: Sequence[Edge], conn: Connection, k: int, modulus: int
) -> PhaseVerdict:
    canonical = tuple(sorted((min(u, v), max(u, v)) for u, v in edges))
    objs: list[Config] = [tuple(c) for c in combinations(range(sites), k)]
    arrows: list[tuple[Config, Config, Elem]] = []
    for a in objs:
        for b in objs:
            elem = hop(canonical, conn, modulus, a, b)
            if elem is not None:
                arrows.append((a, b, elem))
    neighbours: dict[Config, list[tuple[Config, Elem]]] = {o: [] for o in objs}
    for a, b, elem in arrows:
        neighbours[a].append((b, elem))
    done: set[Config] = set()
    components: list[PhaseComponent] = []
    for base in objs:
        if base in done:
            continue
        parent: dict[Config, Config | None] = {base: None}
        pot: dict[Config, Elem] = {base: identity(k)}
        queue: deque[Config] = deque([base])
        while queue:
            a = queue.popleft()
            for b, elem in neighbours[a]:
                if b not in pot:
                    pot[b] = compose(elem, pot[a], modulus)
                    parent[b] = a
                    queue.append(b)
        done.update(pot)
        generators: list[Elem] = []
        witness: tuple[Config, ...] | None = None
        witness_elem: Elem | None = None
        for a, b, elem in arrows:
            if a in pot and b in pot:
                g = compose(inverse(pot[b], modulus), compose(elem, pot[a], modulus), modulus)
                if g != identity(k):
                    generators.append(g)
                    if witness is None:
                        witness = tuple(hg._tree_path(parent, a)) + tuple(
                            reversed(hg._tree_path(parent, b))
                        )
                        witness_elem = g
        group = closure(generators, k, modulus)
        fixed_labels = tuple(i for i in range(k) if all(s[i] == i for s, _ in group))
        fixed_zero = tuple(i for i in fixed_labels if all(t[i] == 0 for _, t in group))
        components.append(
            PhaseComponent(
                base=base,
                size=len(pot),
                group_order=len(group),
                permutation_part_trivial=all(s == hg.identity(k) for s, _ in group),
                phase_part_trivial=all(all(x == 0 for x in t) for _, t in group),
                common_fixed_labels=fixed_labels,
                common_fixed_with_zero_shift=fixed_zero,
                fixed_pair_exists=len(fixed_zero) >= 2,
                witness=witness,
                witness_elem=witness_elem,
            )
        )
    return PhaseVerdict(
        name=name,
        sites=sites,
        k=k,
        modulus=modulus,
        edges=canonical,
        conn=tuple(sorted((u, v, a) for (u, v), a in conn.items())),
        objects=len(objs),
        arrows=len(arrows),
        components=tuple(components),
    )


N = 4


def square_conn(phi: int, modulus: int = N) -> Connection:
    return connection(two.grid(2, 2), {(0, 1): phi}, modulus)


def square_edge_conn(phi: int, modulus: int = N) -> Connection:
    return connection(hg.square_plus_edge(), {(0, 1): phi}, modulus)


def tree_conn(edges: Sequence[Edge], modulus: int = N) -> Connection:
    return connection(edges, {(u, v): v for u, v in edges}, modulus)


def fixtures() -> list[tuple[str, int, list[Edge], Connection, int, int]]:
    """(name, sites, edges, connection, k, modulus), the pre-registered set."""

    out: list[tuple[str, int, list[Edge], Connection, int, int]] = [
        ("chain_P4_k2_tree_phases", 4, two.chain(4), tree_conn(two.chain(4)), 2, N),
        ("star_K13_k3_tree_phases", 4, two.star(3), tree_conn(two.star(3)), 3, N),
    ]
    for phi in range(N):
        out.append((f"square_k2_flux{phi}", 4, two.grid(2, 2), square_conn(phi), 2, N))
    for phi in range(N + 1):
        out.append(
            (f"square_edge_k2_flux{phi}", 6, hg.square_plus_edge(), square_edge_conn(phi), 2, N)
        )
    for phi in range(N):
        out.append(
            (f"square_edge_k4_flux{phi}", 6, hg.square_plus_edge(), square_edge_conn(phi), 4, N)
        )
    return out


GAUGE = (0, 1, 2, 3, 0, 0)


def gauge_check() -> dict[str, bool]:
    """Every fixture keeps its verdict and its component orders under the gauge transformation."""

    out: dict[str, bool] = {}
    for name, sites, edges, conn, k, modulus in fixtures():
        v = analyse_phase(name, sites, edges, conn, k, modulus)
        w = analyse_phase(name, sites, edges, gauge_transform(conn, GAUGE[:sites], modulus), k, modulus)
        out[name] = v.section_exists == w.section_exists and [
            (c.base, c.group_order, c.fixed_pair_exists) for c in v.components
        ] == [(c.base, c.group_order, c.fixed_pair_exists) for c in w.components]
    return out


ONE_ON_EACH: Config = (0, 4)


def one_on_each(phi: int, modulus: int) -> PhaseComponent:
    """The component of the square-plus-edge graph at ``k = 2`` with one particle on
    the square and one on the edge, for flux ``phi`` in ``Z_modulus``.

    The whole fixture also contains the both-on-square component (the two-label
    exchange, obstructed for every flux) and the frozen both-on-edge component;
    the fixture-level verdict is the conjunction over all three and so is
    always "no section".  The question this file asks is about THIS
    component, and a first version of the checks below read the fixture-level
    verdict by mistake; that is recorded in STATUS.md.
    """

    verdict = analyse_phase("c", 6, hg.square_plus_edge(), square_edge_conn(phi, modulus), 2, modulus)
    for component in verdict.components:
        if component.base == ONE_ON_EACH:
            return component
    raise AssertionError("the one-on-each component is missing")


def periodicity_check() -> dict[str, bool]:
    """One on each: flux ``N`` behaves as flux ``0`` and flux ``1`` obstructs, at several ``N``."""

    out: dict[str, bool] = {}
    for modulus in (2, 3, 4, 6):
        zero = one_on_each(0, modulus)
        full = one_on_each(modulus, modulus)
        one = one_on_each(1, modulus)
        out[f"N{modulus}"] = (
            zero.fixed_pair_exists
            and full.fixed_pair_exists
            and not one.fixed_pair_exists
            and one.permutation_part_trivial
        )
    return out


def refinement_check() -> dict[str, bool]:
    """Compatibility with refinement of the modulus.

    The moduli form a directed system under divisibility: for ``N | M`` the
    phase ``phi`` in ``Z_N`` is carried to ``(M / N) phi`` in ``Z_M``.  If the
    one-on-each verdict at ``(phi, N)`` always equals the verdict at
    ``((M / N) phi, M)``, the verdict is an invariant of the directed system --
    the finite form of "the same in the limit"; a continuous phase would add
    only non-torsion values, which no closed walk with ``Z_N`` edge phases
    produces.  Checked for every ``phi`` in ``Z_N`` on several pairs ``N | M``.
    """

    out: dict[str, bool] = {}
    for small, large in ((2, 4), (2, 6), (3, 6), (4, 8), (4, 12)):
        ok = True
        for phi in range(small):
            a = one_on_each(phi, small)
            b = one_on_each(phi * (large // small), large)
            ok = ok and a.fixed_pair_exists == b.fixed_pair_exists
            ok = ok and a.permutation_part_trivial == b.permutation_part_trivial
        out[f"N{small}_into_N{large}"] = ok
    return out


def summary() -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for name, sites, edges, conn, k, modulus in fixtures():
        v = analyse_phase(name, sites, edges, conn, k, modulus)
        out[name] = {
            "section_exists": v.section_exists,
            "components": [
                {
                    "base": list(c.base),
                    "group_order": c.group_order,
                    "permutation_part_trivial": c.permutation_part_trivial,
                    "phase_part_trivial": c.phase_part_trivial,
                    "fixed_pair_exists": c.fixed_pair_exists,
                }
                for c in v.components
            ],
        }
    return out


def report() -> dict[str, object]:
    return {
        "family": {
            "phase_group": f"Z_{N} (a continuous phase is refused by name)",
            "carrier": "label x Fin N: one phase register per particle",
            "observer": "kernel of the label projection: phases invisible to distinctness",
            "arrow": "a hop; the mover's register gains the edge phase A(u, v), A(v, u) = -A(u, v)",
            "holonomy": "(permutation, shift vector) in the wreath product of Z_N by the symmetric group",
            "criterion": "two labels fixed by every holonomy's permutation with zero shift on both",
        },
        "fixtures": [
            analyse_phase(name, sites, edges, conn, k, modulus).json()
            for name, sites, edges, conn, k, modulus in fixtures()
        ],
        "summary": summary(),
        "gauge_invariance": gauge_check(),
        "periodicity": periodicity_check(),
        "refinement_compatibility": refinement_check(),
        "one_on_each_by_flux": {
            f"flux{phi}": one_on_each(phi, N).json() for phi in range(N + 1)
        },
    }
