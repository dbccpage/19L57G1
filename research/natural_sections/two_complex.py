"""The chord square with faces, surveyed over ``Z_N``.

Five edges (the square ``0-1, 1-3, 3-2, 2-0`` and the chord ``0-3``),
two triangular faces ``T1 = 0-1-3`` and ``T2 = 0-3-2``.  For every
edge-phase assignment over ``Z_N`` the survey computes both face fluxes
and the outer flux, decides section existence by BRUTE-FORCE potential
search (independent of the flux criterion), and counts.  The
pre-registered claims (STATUS.md, TC4): potential existence agrees with
``(fluxT1, fluxT2) = (0, 0)`` everywhere; the boundary identity
``outer = T1 + T2`` holds everywhere; section count ``N^3``; outer-zero
count ``N^4``; outer-zero-but-obstructed ``N^4 - N^3``; with ``T1``
filled, ``N^4`` assignments remain of which ``N^3`` admit sections.
Deterministic, standard library only.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from itertools import product

EDGES: tuple[str, ...] = ("e01", "e13", "e32", "e20", "e03")

# One orientation per edge: (source, target, edge index).
DIRECTED: tuple[tuple[int, int, int], ...] = (
    (0, 1, 0),
    (1, 3, 1),
    (3, 2, 2),
    (2, 0, 3),
    (0, 3, 4),
)

MODULI: tuple[int, ...] = (2, 3, 4)


def flux_t1(w: tuple[int, ...], n: int) -> int:
    return (w[0] + w[1] - w[4]) % n


def flux_t2(w: tuple[int, ...], n: int) -> int:
    return (w[4] + w[2] + w[3]) % n


def flux_outer(w: tuple[int, ...], n: int) -> int:
    return (w[0] + w[1] + w[2] + w[3]) % n


def potential_exists(w: tuple[int, ...], n: int) -> bool:
    """Brute-force search for ``theta`` with ``theta[0] = 0`` satisfying
    every directed edge equation -- independent of the flux criterion."""

    for t1 in range(n):
        for t2 in range(n):
            for t3 in range(n):
                theta = (0, t1, t2, t3)
                if all((theta[a] + w[e]) % n == theta[b] for a, b, e in DIRECTED):
                    return True
    return False


def survey(n: int) -> dict[str, object]:
    total = 0
    boundary_identity = True
    potential_matches = True
    sections = 0
    outer_zero = 0
    outer_zero_obstructed = 0
    t1_filled = 0
    t1_filled_with_section = 0
    for w in product(range(n), repeat=len(EDGES)):
        total += 1
        f1 = flux_t1(w, n)
        f2 = flux_t2(w, n)
        outer = flux_outer(w, n)
        if outer != (f1 + f2) % n:
            boundary_identity = False
        has_section = potential_exists(w, n)
        if has_section != (f1 == 0 and f2 == 0):
            potential_matches = False
        if has_section:
            sections += 1
        if outer == 0:
            outer_zero += 1
            if not has_section:
                outer_zero_obstructed += 1
        if f1 == 0:
            t1_filled += 1
            if has_section:
                t1_filled_with_section += 1
    return {
        "modulus": n,
        "total": total,
        "boundary_identity_everywhere": boundary_identity,
        "potential_matches_flux_criterion": potential_matches,
        "sections": sections,
        "outer_zero": outer_zero,
        "outer_zero_obstructed": outer_zero_obstructed,
        "t1_filled": t1_filled,
        "t1_filled_with_section": t1_filled_with_section,
    }


def report() -> dict[str, object]:
    return {
        "fixture": "chord square: square 0-1,1-3,3-2,2-0 plus chord 0-3; faces T1=0-1-3, T2=0-3-2",
        "surveys": [survey(n) for n in MODULI],
    }
