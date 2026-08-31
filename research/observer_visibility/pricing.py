"""OV6: chord-square Phi on Z_N, N in {2,3,4}.

Four objects 0,1,2,3.  Edges 0-1, 1-2, 2-3, 3-0, and chord 0-2.
Faces T1: 0-1-2-0, T2: 0-2-3-0.  Flux is the directed sum of cochain
values around the face.  Phi is the infimal l1 mass of w minus a
coboundary, over the finite fibre Z_N^4.  The table is the whole
cochain space C^1 = Z_N^5, not a slice of representatives.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from itertools import product

Edges = ((0, 1), (1, 2), (2, 3), (3, 0), (0, 2))
T1 = (0, 1, 2)
T2 = (0, 2, 3)


def coboundary(s: tuple[int, ...], n: int) -> tuple[int, ...]:
    out: list[int] = []
    for a, b in Edges:
        out.append((s[b] - s[a]) % n)
    return tuple(out)


def flux(w: tuple[int, ...], face: tuple[int, ...], n: int) -> int:
    idx = {Edges[i]: i for i in range(len(Edges))}
    total = 0
    for i in range(len(face)):
        a, b = face[i], face[(i + 1) % len(face)]
        if (a, b) in idx:
            total += w[idx[(a, b)]]
        else:
            total -= w[idx[(b, a)]]
    return total % n


def phi(w: tuple[int, ...], n: int) -> int:
    best = n * len(Edges)
    for s in product(range(n), repeat=4):
        d = coboundary(s, n)
        mass = 0
        for i in range(len(Edges)):
            mass += min((w[i] - d[i]) % n, (d[i] - w[i]) % n)
        if mass < best:
            best = mass
    return best


def table(n: int) -> dict[str, object]:
    rows: list[dict[str, int]] = []
    for w in product(range(n), repeat=len(Edges)):
        flux1 = flux(w, T1, n)
        flux2 = flux(w, T2, n)
        value = phi(w, n)
        rows.append({"flux1": flux1, "flux2": flux2, "phi": value})
    n_phi0 = sum(1 for row in rows if row["phi"] == 0)
    n_flux0 = sum(1 for row in rows if row["flux1"] == 0 and row["flux2"] == 0)
    both_iff = all(
        (row["phi"] == 0) == (row["flux1"] == 0 and row["flux2"] == 0) for row in rows
    )
    return {
        "n": n,
        "n_cochains": n ** len(Edges),
        "rows": rows,
        "zero_count": n_phi0,
        "flux_zero_count": n_flux0,
        "phi_zero_iff_fluxes_zero": both_iff,
    }


def report() -> dict[str, object]:
    return {
        "schema": "observer_visibility_pricing/v1",
        "Z2": table(2),
        "Z3": table(3),
        "Z4": table(4),
    }
