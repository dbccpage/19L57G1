"""Cancellation certificates over the declared product carrier.

A configuration is a pair `(m, f)` with `m` in `{0, 1, 2}` (the declared
involution exchanges `0` and `1` and fixes `2`) and `f` in `{0, 1}`.  A
weight family assigns each configuration an integer bounded by `2` in
magnitude.  A **cancellation certificate** is a decomposition of the six
weights into exact-opposite pairs plus a single-signed residual -- the
list-level notion SX5 proved sums to its residual.  This module decides
certificates two independent ways (per-magnitude counting, and a full
search over pairings), decides separability against every bounded factor
pair, and answers the slot-exchange rung's registered OPEN question at
this bound.  Exact integer arithmetic; nothing uses floating point.

AuthorityEffect: None.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import product

BOUND = 2
MOVED = (0, 1)
FIXED_M = 2
F_VALUES = (0, 1)
POINTS: tuple[tuple[int, int], ...] = tuple(
    (m, f) for m in (0, 1, 2) for f in F_VALUES
)
VALUES = tuple(range(-BOUND, BOUND + 1))

Weights = tuple[int, ...]


def all_families() -> list[Weights]:
    return [w for w in product(VALUES, repeat=len(POINTS))]


def has_certificate_by_counting(w: Weights) -> bool:
    """Per-magnitude domination on one side or the other."""

    magnitudes = {abs(v) for v in w if v != 0}
    neg_dominated = all(
        sum(1 for v in w if v == -mag) <= sum(1 for v in w if v == mag)
        for mag in magnitudes
    )
    pos_dominated = all(
        sum(1 for v in w if v == mag) <= sum(1 for v in w if v == -mag)
        for mag in magnitudes
    )
    return neg_dominated or pos_dominated


def has_certificate_by_search(w: Weights) -> bool:
    """Independent decision: search every pairing into exact-opposite
    pairs, requiring the leftover to be single-signed."""

    def search(items: tuple[int, ...], residual: tuple[int, ...]) -> bool:
        if not items:
            return all(v >= 0 for v in residual) or all(v <= 0 for v in residual)
        head, rest = items[0], items[1:]
        # head joins the residual
        if search(rest, residual + (head,)):
            return True
        # head pairs with a later exact opposite
        for i, other in enumerate(rest):
            if other == -head:
                if search(rest[:i] + rest[i + 1 :], residual):
                    return True
        return False

    return search(w, ())


@lru_cache(maxsize=1)
def separable_families() -> frozenset[Weights]:
    """Every family of the form W(m, f) = A(m) * B(f) with all factors
    bounded by the declared bound."""

    out: set[Weights] = set()
    for a in product(VALUES, repeat=3):
        for b in product(VALUES, repeat=2):
            w = tuple(a[m] * b[f] for m in (0, 1, 2) for f in F_VALUES)
            if all(abs(v) <= BOUND for v in w):
                out.add(w)
    return frozenset(out)


def is_fibrewise_odd(w: Weights) -> bool:
    idx = {p: i for i, p in enumerate(POINTS)}
    return all(w[idx[(1, f)]] == -w[idx[(0, f)]] for f in F_VALUES)


def moved_sector_total(w: Weights) -> int:
    idx = {p: i for i, p in enumerate(POINTS)}
    return sum(w[idx[(m, f)]] for m in MOVED for f in F_VALUES)


PINNED_WITNESS: Weights = (1, 2, -1, -2, 1, 1)


@lru_cache(maxsize=1)
def report() -> dict[str, object]:
    families = all_families()
    separable = separable_families()

    odd_families = [w for w in families if is_fibrewise_odd(w)]
    odd_moved_total_misses = [w for w in odd_families if moved_sector_total(w) != 0]

    agreement_misses = 0
    certified = 0
    positive_total_uncertified: list[Weights] = []
    interacting_certified: list[Weights] = []
    for w in families:
        by_counting = has_certificate_by_counting(w)
        if by_counting != has_certificate_by_search(w):
            agreement_misses += 1
        if by_counting:
            certified += 1
            if w not in separable:
                interacting_certified.append(w)
        elif sum(w) > 0:
            positive_total_uncertified.append(w)

    pinned_interacting = PINNED_WITNESS not in separable
    pinned_certified = has_certificate_by_counting(PINNED_WITNESS)

    return {
        "bound": BOUND,
        "points": [list(p) for p in POINTS],
        "family_count": len(families),
        "fibrewise_odd_count": len(odd_families),
        "fibrewise_odd_moved_total_misses": len(odd_moved_total_misses),
        "certificate_agreement_misses": agreement_misses,
        "certified_count": certified,
        "uncertified_count": len(families) - certified,
        "separable_count": len(separable),
        "interacting_certified_count": len(interacting_certified),
        "positive_total_uncertified_count": len(positive_total_uncertified),
        "minimal_positive_total_uncertified": list(
            min(positive_total_uncertified) if positive_total_uncertified else ()
        ),
        "minimal_interacting_certified": list(
            min(interacting_certified) if interacting_certified else ()
        ),
        "pinned_witness": list(PINNED_WITNESS),
        "pinned_witness_is_interacting": pinned_interacting,
        "pinned_witness_has_certificate": pinned_certified,
        "open_question_answer_at_bound": len(interacting_certified) > 0,
    }
