"""Stage 1, the computational side: the layer observer recomputed.

The Lean module ``lean/BalanceCarrier/LayerObserver.lean`` proves that
the raw observer ``(k + 1) / gcd(n, k + 1)`` is well defined on the
receiver, constant on a layer's fresh members, layer-separating, and
graded along divisor arrows.  This module recomputes the finite slices
pre-registered in ``PREDICTIONS.md`` (L6) by brute force, independently
of the proofs, in exact integer arithmetic: for every raw pair up to the
bound, the fresh representations are found by searching every layer up to
the bound with the pinned cross-multiplication relation, and their part
count is compared with the raw observer.  Nothing here uses floating
point.

AuthorityEffect: None.
"""

from __future__ import annotations

from functools import lru_cache
from math import gcd

BOUND: int = 40
WRAP_BOUND: int = 24
LAYER_TABLE_BOUND: int = 12
GRADE_QUOTIENT_BOUND: int = 6


def raw_observer(n: int, k: int) -> int:
    """The declared raw observer: ``(k + 1) / gcd(n, k + 1)`` (Lean ``rawObs``)."""

    d = k + 1
    return d // gcd(n, d)


def is_fresh(part: int, part_count: int) -> bool:
    """Fresh at a layer: the part shares no factor above one with the part count."""

    return gcd(part, part_count) == 1


def same_element(a: tuple[int, int], b: tuple[int, int]) -> bool:
    """The pinned relation ``R``: the cross difference is an integer multiple
    of the product of the two part counts."""

    n1, k1 = a
    n2, k2 = b
    d1, d2 = k1 + 1, k2 + 1
    return (n1 * d2 - n2 * d1) % (d1 * d2) == 0


def fresh_representations(n: int, k: int, bound: int) -> list[tuple[int, int]]:
    """Every fresh ``(part, index)`` with index at most ``bound`` naming the
    same receiver element as the raw pair ``(n, k)``; found by search."""

    found: list[tuple[int, int]] = []
    for k2 in range(bound + 1):
        for c in range(k2 + 1):
            if is_fresh(c, k2 + 1) and same_element((n, k), (c, k2)):
                found.append((c, k2))
    return found


def observer_misses(bound: int, wrapped: bool) -> list[list[int]]:
    """Raw pairs whose brute-force fresh representation is not unique or
    whose part count differs from the raw observer.  With ``wrapped`` the
    parts range past the part count (``k + 1 <= n <= 2k + 1``)."""

    misses: list[list[int]] = []
    for k in range(bound + 1):
        parts = range(k + 1, 2 * k + 2) if wrapped else range(k + 1)
        for n in parts:
            reps = fresh_representations(n, k, bound)
            if len(reps) != 1 or reps[0][1] + 1 != raw_observer(n, k):
                misses.append([n, k, len(reps)])
    return misses


def fresh_values_per_layer(bound: int) -> dict[str, list[int]]:
    """The set of observer values over the fresh members of each part count."""

    return {
        str(pc): sorted({raw_observer(c, pc - 1) for c in range(pc) if is_fresh(c, pc)})
        for pc in range(1, bound + 1)
    }


def grade_misses(bound: int, quotient_bound: int) -> list[list[int]]:
    """The declared grading: a fresh part ``c`` of part count ``pc`` carried
    along the arrow to ``q * pc`` reads ``pc`` at the image ``(q * c, q * pc - 1)``."""

    misses: list[list[int]] = []
    for pc in range(1, bound + 1):
        for c in range(pc):
            if not is_fresh(c, pc):
                continue
            for q in range(1, quotient_bound + 1):
                if raw_observer(q * c, q * pc - 1) != pc:
                    misses.append([pc, c, q])
    return misses


def divides_misses(bound: int) -> list[list[int]]:
    """The observer's value divides the part count of the layer it is read in."""

    return [
        [n, k]
        for k in range(bound + 1)
        for n in range(k + 1)
        if (k + 1) % raw_observer(n, k) != 0
    ]


@lru_cache(maxsize=1)
def report() -> dict[str, object]:
    return {
        "bound": BOUND,
        "wrap_bound": WRAP_BOUND,
        "observer_misses": observer_misses(BOUND, wrapped=False),
        "observer_misses_wrapped": observer_misses(WRAP_BOUND, wrapped=True),
        "fresh_values_per_layer_1_12": fresh_values_per_layer(LAYER_TABLE_BOUND),
        "grade_quotient_bound": GRADE_QUOTIENT_BOUND,
        "grade_misses": grade_misses(LAYER_TABLE_BOUND, GRADE_QUOTIENT_BOUND),
        "divides_misses": divides_misses(BOUND),
    }
