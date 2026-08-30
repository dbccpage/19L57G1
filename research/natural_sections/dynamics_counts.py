"""Counts are blind to the class: the square and its cover share every
closed-walk count; only counts read in a convention differ.

The square's two-label family and its cover have the same objects and the
same hops; they differ only in the transports (the flip bit versus none).
Their closed-walk counts at the base therefore agree at every length.  The
convention-read count (the walks whose holonomy fixes a pair -- ``twisted``
with unit weights, B1 of the weighted layer) differs.  Deterministic,
standard library only.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from typing import Sequence

import holonomy_fixture as two
import weighted_sum as ws

Edge = tuple[int, int]


def counts_by_length(
    sites: int, edges: Sequence[Edge], drop_flips: bool, max_len: int
) -> tuple[list[int], list[int]]:
    """(closed-walk count per length 0..max_len, convention-read count per
    length at the pair (0, 1)); ``drop_flips`` reads the cover."""

    adj = ws.arrows(sites, edges, 2)
    base = sorted(adj)[0]
    walks = ws.closed_walks(adj, base, max_len)
    totals = [0] * (max_len + 1)
    fixed = [0] * (max_len + 1)
    for walk, perm in walks:
        length = len(walk)
        totals[length] += 1
        effective = (0, 1) if drop_flips else perm
        if ws.fixes(effective, (0, 1)):
            fixed[length] += 1
    return totals, fixed


def report() -> dict[str, object]:
    sq_totals, sq_fixed = counts_by_length(4, two.grid(2, 2), False, 6)
    cov_totals, cov_fixed = counts_by_length(4, two.grid(2, 2), True, 6)
    return {
        "claim": "the square and its cover share every closed-walk count; the convention-read counts differ",
        "square": {"counts_by_length": sq_totals, "convention_read_at_01": sq_fixed},
        "cover": {"counts_by_length": cov_totals, "convention_read_at_01": cov_fixed},
        "counts_identical": sq_totals == cov_totals,
        "convention_read_identical": sq_fixed == cov_fixed,
    }
