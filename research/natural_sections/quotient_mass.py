"""Repair mass on the chord square, surveyed over ``Z_N``.

For every edge-phase assignment ``w`` over ``Z_N`` the survey computes
its gauge class ``(fluxT1, fluxT2)``, the minimum SUPPORT mass over the
whole gauge orbit (how many edges any equivalent assignment must still
carry), and the minimum CIRCULAR mass under ``cd(k) = min(k, N - k)``.
The pre-registered claims (STATUS.md, QM2 and QM4): every class has
exactly ``N^3`` members; the support-mass price is ``0`` iff the class
is ``(0, 0)``, ``<= 1`` iff ``f1 = 0`` or ``f2 = 0`` or ``f2 = -f1``,
and ``<= 2`` always, with class counts at price ``0 / 1 / 2`` equal to
``1 / 3(N-1) / (N-1)(N-2)``; the circular price is ``0`` iff ``(0, 0)``,
is at most ``cd(f1) + cd(f2)``, and equals ``cd(f)`` exactly on the
anti-diagonal ``(f, -f)``.  Deterministic, standard library only.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from itertools import product

# Edge order: e01, e13, e32, e20, e03.
EDGES: tuple[str, ...] = ("e01", "e13", "e32", "e20", "e03")
MODULI: tuple[int, ...] = (2, 3, 4)


def flux_t1(w: tuple[int, ...], n: int) -> int:
    return (w[0] + w[1] - w[4]) % n


def flux_t2(w: tuple[int, ...], n: int) -> int:
    return (w[4] + w[2] + w[3]) % n


def d0(theta: tuple[int, ...], n: int) -> tuple[int, ...]:
    """The gauge coboundary: potential differences per oriented edge."""

    t0, t1, t2, t3 = theta
    return (
        (t1 - t0) % n,
        (t3 - t1) % n,
        (t2 - t3) % n,
        (t0 - t2) % n,
        (t3 - t0) % n,
    )


def supp_mass(w: tuple[int, ...]) -> int:
    return sum(1 for x in w if x != 0)


def circ(k: int, n: int) -> int:
    return min(k % n, (-k) % n)


def circ_mass(w: tuple[int, ...], n: int) -> int:
    return sum(circ(x, n) for x in w)


def survey(n: int) -> dict[str, object]:
    classes: dict[tuple[int, int], dict[str, int]] = {}
    for w in product(range(n), repeat=len(EDGES)):
        key = (flux_t1(w, n), flux_t2(w, n))
        row = classes.setdefault(
            key, {"members": 0, "min_supp": len(EDGES), "min_circ": len(EDGES) * n}
        )
        row["members"] += 1
        row["min_supp"] = min(row["min_supp"], supp_mass(w))
        row["min_circ"] = min(row["min_circ"], circ_mass(w, n))

    orbit_check = all(row["members"] == n**3 for row in classes.values())

    def predicted_supp(f1: int, f2: int) -> int:
        if f1 == 0 and f2 == 0:
            return 0
        if f1 == 0 or f2 == 0 or f2 == (-f1) % n:
            return 1
        return 2

    supp_matches = all(
        row["min_supp"] == predicted_supp(f1, f2) for (f1, f2), row in classes.items()
    )
    supp_counts = {
        k: sum(1 for row in classes.values() if row["min_supp"] == k) for k in (0, 1, 2)
    }
    circ_zero_only_origin = all(
        (row["min_circ"] == 0) == (key == (0, 0)) for key, row in classes.items()
    )
    circ_le_pair = all(
        row["min_circ"] <= circ(f1, n) + circ(f2, n)
        for (f1, f2), row in classes.items()
    )
    circ_antidiagonal_exact = all(
        classes[(f, (-f) % n)]["min_circ"] == circ(f, n) for f in range(n)
    )
    # An independent replay: the orbit of the zero assignment is exactly im(d0).
    d0_orbit = {d0(theta, n) for theta in product(range(n), repeat=4)}
    d0_is_zero_class = (
        len(d0_orbit) == n**3
        and all(flux_t1(v, n) == 0 and flux_t2(v, n) == 0 for v in d0_orbit)
    )
    return {
        "modulus": n,
        "class_count": len(classes),
        "orbit_sizes_all_n_cubed": orbit_check,
        "supp_price_matches_qm3": supp_matches,
        "supp_price_counts": supp_counts,
        "circ_zero_only_at_origin": circ_zero_only_origin,
        "circ_le_pair_bound": circ_le_pair,
        "circ_antidiagonal_exact": circ_antidiagonal_exact,
        "d0_image_is_the_zero_class": d0_is_zero_class,
        "price_table": {
            f"({f1},{f2})": [row["min_supp"], row["min_circ"]]
            for (f1, f2), row in sorted(classes.items())
        },
    }


def report() -> dict[str, object]:
    return {
        "fixture": "chord square; gauge d0 theta; support and circular masses over Z_N",
        "surveys": [survey(n) for n in MODULI],
    }
