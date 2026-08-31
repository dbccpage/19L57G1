"""Slot exchange: character counts and odd-pairing cancellation, exhaustively.

The Lean module ``lean/NaturalSections/SlotExchange.lean`` proves the
rung's claims; this module recomputes the finite ones by brute force so
the receipts are independent of the proofs.  Everything is exact
integer arithmetic; nothing is sampled.

Computations (all pre-registered in ``STATUS.md``):

* character counts over ``Fin k`` for ``k = 1..8``: every value is
  admissible for the rotation generator (``k`` iterated additions
  return to zero), while the swap generator's constraint ``c + c = 0``
  admits ``2`` values for even ``k`` and ``1`` for odd ``k``;
* odd families on the two-point carrier with entries bounded by ``3``:
  enumerated exhaustively, each checked for total zero and for exact
  cancellation of each off-diagonal entry against its transpose
  partner;
* the discard countermodel: the full four-element list totals zero,
  the discarded-partner list totals four.

AuthorityEffect: None.
"""

from __future__ import annotations


def rotation_admissible(k: int) -> list[int]:
    """Values ``c`` in ``Fin k`` whose ``k``-fold iterated addition is zero."""

    out: list[int] = []
    for c in range(k):
        acc = 0
        for _ in range(k):
            acc = (acc + c) % k
        if acc == 0:
            out.append(c)
    return out


def swap_admissible(k: int) -> list[int]:
    """Values ``c`` in ``Fin k`` with ``c + c = 0``."""

    return [c for c in range(k) if (c + c) % k == 0]


def character_counts(max_k: int) -> dict[str, object]:
    rotation = [len(rotation_admissible(k)) for k in range(1, max_k + 1)]
    swap = [len(swap_admissible(k)) for k in range(1, max_k + 1)]
    return {
        "ks": list(range(1, max_k + 1)),
        "rotation_counts": rotation,
        "swap_counts": swap,
    }


def odd_families(bound: int) -> list[dict[str, int]]:
    """All odd integer families on the two-point carrier, entries in
    ``[-bound, bound]``: the diagonal is forced to zero and the two
    off-diagonal entries are transpose-negatives, so one free entry."""

    families: list[dict[str, int]] = []
    for x in range(-bound, bound + 1):
        family = {"ff": 0, "ft": x, "tf": -x, "tt": 0}
        families.append(family)
    return families


def odd_family_checks(bound: int) -> dict[str, object]:
    families = odd_families(bound)
    totals = [f["ff"] + f["ft"] + f["tf"] + f["tt"] for f in families]
    pairing_misses = 0
    for f in families:
        if f["ft"] + f["tf"] != 0:
            pairing_misses += 1
        if f["ff"] != 0 or f["tt"] != 0:
            pairing_misses += 1
    return {
        "bound": bound,
        "count": len(families),
        "totals": totals,
        "all_totals_zero": all(t == 0 for t in totals),
        "pairing_misses": pairing_misses,
    }


def discard_countermodel() -> dict[str, object]:
    full = [3, -3, 1, -1]
    discarded = [3, 1]
    return {
        "full_list": full,
        "full_total": sum(full),
        "discarded_list": discarded,
        "discarded_total": sum(discarded),
        "conflatable": sum(full) == sum(discarded),
    }


def report() -> dict[str, object]:
    return {
        "characters": character_counts(8),
        "odd_families": odd_family_checks(3),
        "discard": discard_countermodel(),
    }
