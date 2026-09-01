"""Parity bookkeeping (METATHEORY): the Lean parity model echoed in
Python for concrete cross-checks.  The Lean package proves the laws on
the abstract model; this module computes parities of concrete fibre
transports so promotion.py can check, hop by hop, that the concrete
conjugation obeys the proved law rather than assuming it does.

Requires the pinned sign_slice modules on the path (`../sign_slice`).
AuthorityEffect: None.
"""

from __future__ import annotations

from genpres import Perm, compose, inverse


def perm_parity(p: Perm) -> int:
    """0 for an even bijection, 1 for an odd one, by inversion count."""

    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                inv += 1
    return inv & 1


def relabelled_parity(t: int, a: int, b: int) -> int:
    """The proved law `relabelled_eq`, echoed: conjugation adds both
    slot parities (mod 2)."""

    return t ^ a ^ b


def conjugated(t: Perm, g_src: Perm, g_dst: Perm) -> Perm:
    """The concrete conjugation the relabel applies to one arrow."""

    return compose(g_dst, compose(t, inverse(g_src)))


def conjugation_obeys_parity_law(t: Perm, g_src: Perm, g_dst: Perm) -> bool:
    """Check one concrete instance of the proved law."""

    return perm_parity(conjugated(t, g_src, g_dst)) == relabelled_parity(
        perm_parity(t), perm_parity(g_src), perm_parity(g_dst)
    )
