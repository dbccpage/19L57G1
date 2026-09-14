"""Higher-order diagonalization theorem and adversarial pair generation.

AuthorityEffect: None.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Sequence

from .observer_hierarchy import Observer, ScaleRegime, eval_observer, is_isomorphic
from .separation_capacity import capacity, capacity_gap, canonical_family_size, canonical_test_regime


def find_collision(values: Sequence[int]) -> tuple[int, int]:
    """Find first colliding pair (i, j) with i < j and values[i] == values[j]."""
    seen: dict[int, int] = {}
    for j, val in enumerate(values):
        if val in seen:
            return seen[val], j
        seen[val] = j
    raise ValueError("No collision found in given sequence")


def higher_order_diagonalization(
    observer: Observer, k: int
) -> tuple[ScaleRegime, ScaleRegime]:
    """Higher-Order Diagonalization Algorithm:
    Given observer of resolution depth k, constructs an adversarial pair of regimes (r1, r2)
    at scale depth k+2 such that:
    1. not is_isomorphic(r1, r2)
    2. eval_observer(observer, r1) == eval_observer(observer, r2).
    """
    if observer.resolution_depth > k:
        raise ValueError(
            f"observer depth {observer.resolution_depth} exceeds bound {k}"
        )
    family_size = canonical_family_size(k)
    regimes = [canonical_test_regime(k, i) for i in range(family_size)]
    signatures = [eval_observer(observer, r) for r in regimes]
    i, j = find_collision(signatures)
    r1, r2 = regimes[i], regimes[j]
    if is_isomorphic(r1, r2):
        raise RuntimeError(
            f"Adversarial construction failure: test regimes {i} and {j} are isomorphic"
        )
    if eval_observer(observer, r1) != eval_observer(observer, r2):
        raise RuntimeError(
            f"Adversarial construction failure: signatures differ ({eval_observer(observer, r1)} != {eval_observer(observer, r2)})"
        )
    return r1, r2


def diagonal_evaluation_fibers(
    observer: Observer, k: int
) -> dict[int, list[ScaleRegime]]:
    """Extract evaluation fibers {sig: [regimes]} across test family."""
    family_size = canonical_family_size(k)
    fibers: dict[int, list[ScaleRegime]] = defaultdict(list)
    for i in range(family_size):
        r = canonical_test_regime(k, i)
        sig = eval_observer(observer, r)
        fibers[sig].append(r)
    return dict(fibers)


def verify_duality(observer: Observer, k: int) -> dict[str, object]:
    """Verify simultaneous pair-id collapse and family-miss gap."""
    r1, r2 = higher_order_diagonalization(observer, k)
    sig1 = eval_observer(observer, r1)
    sig2 = eval_observer(observer, r2)
    gap = capacity_gap(k, k + 2)
    cap = capacity(k)
    fam_size = canonical_family_size(k)
    return {
        "k": k,
        "capacity": cap,
        "family_size": fam_size,
        "gap": gap,
        "pair_id_collapse": {
            "r1": r1.tokens,
            "r2": r2.tokens,
            "isomorphic": is_isomorphic(r1, r2),
            "signatures": (sig1, sig2),
            "indistinguishable": sig1 == sig2,
        },
        "family_miss": {
            "regimes_count": fam_size,
            "max_distinguishable": cap,
            "gap_positive": gap > 0,
        },
    }
