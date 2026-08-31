"""The phase receiver, recomputed exhaustively in exact integer arithmetic.

The Lean module ``lean/NaturalSections/PhaseReceiver.lean`` proves the
receiver's laws once and for all; this module re-checks the finite
slices pre-registered in ``STATUS.md`` by brute force, independently of
the proofs.  An element is an indexed pair ``(n, k)`` -- the ``n``-th
part of ``k + 1`` -- and two pairs are equivalent when their cross
difference is a multiple of the product of the part counts.  Nothing
here uses floating point.

AuthorityEffect: None.
"""

from __future__ import annotations

from math import gcd


def den(k: int) -> int:
    return k + 1


def equiv(a: tuple[int, int], b: tuple[int, int]) -> bool:
    """Cross-multiplication equivalence of indexed pairs."""

    return (a[0] * den(b[1]) - b[0] * den(a[1])) % (den(a[1]) * den(b[1])) == 0


def raw_add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] * den(b[1]) + b[0] * den(a[1]), a[1] * b[1] + a[1] + b[1])


def raw_neg(a: tuple[int, int]) -> tuple[int, int]:
    return (a[0] * a[1], a[1])


def pairs_up_to(max_k: int) -> list[tuple[int, int]]:
    return [(n, k) for k in range(max_k + 1) for n in range(den(k))]


def group_law_survey(max_k: int) -> dict[str, int]:
    """Exhaustive associativity, commutativity, and inverse checks over
    all pairs with index at most ``max_k``, up to equivalence."""

    pairs = pairs_up_to(max_k)
    assoc_misses = 0
    comm_misses = 0
    inv_misses = 0
    for a in pairs:
        if not equiv(raw_add(a, raw_neg(a)), (0, 0)):
            inv_misses += 1
        for b in pairs:
            if not equiv(raw_add(a, b), raw_add(b, a)):
                comm_misses += 1
            for c in pairs:
                if not equiv(raw_add(raw_add(a, b), c), raw_add(a, raw_add(b, c))):
                    assoc_misses += 1
    return {
        "max_index": max_k,
        "pairs": len(pairs),
        "assoc_misses": assoc_misses,
        "comm_misses": comm_misses,
        "inv_misses": inv_misses,
    }


def layer_compat_survey(max_k: int) -> dict[str, int]:
    """Each layer factors through every multiple: ``(c, k)`` is
    equivalent to ``(c * (m + 1), (k + 1) * (m + 1) - 1)``."""

    misses = 0
    checks = 0
    for k in range(max_k + 1):
        for m in range(max_k + 1):
            for c in range(den(k)):
                checks += 1
                if not equiv((c, k), (c * (m + 1), k * m + k + m)):
                    misses += 1
    return {"max_index": max_k, "checks": checks, "misses": misses}


def order_of_layer_one(k: int) -> int:
    """The additive order of ``(1, k)`` -- iterated raw addition until
    the class of zero is reached."""

    acc = (1, k)
    steps = 1
    while not equiv(acc, (0, 0)):
        acc = raw_add(acc, (1, k))
        steps += 1
    return steps


def reduced_count_at(d: int) -> int:
    """New elements first appearing at part count ``d``: parts coprime
    to ``d``, computed from scratch."""

    return sum(1 for n in range(d) if gcd(n, d) == 1)


def joint_layer(elements: list[tuple[int, int]]) -> int:
    """The least part count whose layer contains every listed element:
    the least common multiple of the reduced part counts."""

    out = 1
    for n, k in elements:
        d = den(k)
        g = gcd(n % d, d)
        rd = d // g
        out = out * rd // gcd(out, rd)
    return out


def report() -> dict[str, object]:
    orders = [order_of_layer_one(k) for k in range(8)]
    reduced = [reduced_count_at(d) for d in range(1, 9)]
    joint_cases = [
        {"elements": [[1, 1], [1, 2]], "joint": joint_layer([(1, 1), (1, 2)])},
        {"elements": [[1, 3], [1, 5]], "joint": joint_layer([(1, 3), (1, 5)])},
        {"elements": [[2, 3], [3, 5]], "joint": joint_layer([(2, 3), (3, 5)])},
        {"elements": [[0, 6]], "joint": joint_layer([(0, 6)])},
        {"elements": [[2, 5], [3, 5], [1, 1]], "joint": joint_layer([(2, 5), (3, 5), (1, 1)])},
    ]
    return {
        "group_laws": group_law_survey(6),
        "layer_compat": layer_compat_survey(6),
        "orders_of_layer_one": orders,
        "reduced_counts": reduced,
        "joint_layers": joint_cases,
    }
