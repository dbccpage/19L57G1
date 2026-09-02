"""Stage 3: the signed family table -- LP4 on the carrier's own families.

For each (weights, count) pair that met stage 2, the signed family of its
terms at ``N = 6``, ``12``, and the largest ``N`` the Lean instances
reach: the magnitude multiset, the total (which must equal the count),
the certificate decision by per-magnitude domination -- the pinned
``certificate_iff_dominated`` reconstructed as computation, cited as
CONDITIONAL_THEOREM -- and the LP4 check.  For an S2 pair the terms are
the nonzero signed terms of the alternating sum; for the S1b pair the
terms are the chain weights of every chain to every endpoint ``1..N``.
A magnitude-1 family records LP4's persistence, never a result, and no
certificate decision here is a statement about growth.

AuthorityEffect: None.
"""

from __future__ import annotations

from collections import Counter

import walk_carrier as wc

FAMILY_SIZES: tuple[int, ...] = (6, 12)
LEAN_INSTANCE_BOUND: int = 7  # the bound of `unit_table_matches_to_7` / `balance_table_matches_to_7`


def magnitudes_present(weights: list[int]) -> set[int]:
    """Every positive magnitude carried by some weight, whatever its sign.
    A magnitude present only with one sign must still be checked: the
    first version iterated over the positive VALUES present and so never
    checked a magnitude that appeared only negatively -- the pinned wedge
    was wrongly certified, and the test suite caught it."""

    return {abs(w) for w in weights if w != 0}


def dominated_nonneg(weights: list[int]) -> bool:
    """For every positive magnitude, at least as many positive as negative."""

    counts = Counter(weights)
    return all(counts[-v] <= counts[v] for v in magnitudes_present(weights))


def dominated_nonpos(weights: list[int]) -> bool:
    """For every positive magnitude, at least as many negative as positive."""

    counts = Counter(weights)
    return all(counts[v] <= counts[-v] for v in magnitudes_present(weights))


def certificate_decision(weights: list[int]) -> dict[str, object]:
    """The pinned criterion, reconstructed: a cancellation certificate with
    a single-signed residual exists exactly when one side dominates at
    every magnitude.  Both sides are recorded."""

    nonneg = dominated_nonneg(weights)
    nonpos = dominated_nonpos(weights)
    return {
        "certificate_exists": nonneg or nonpos,
        "dominated_side_nonneg_residual": nonneg,
        "dominated_side_nonpos_residual": nonpos,
    }


def s1b_terms(windex: str, n: int, bal: list[int]) -> list[int]:
    """The chain weights of every chain to every endpoint ``1..n``."""

    terms: list[int] = []
    for m in range(1, n + 1):
        for chain in wc.chains_to(m):
            terms.append(wc.chain_weight(windex, chain, bal))
    return terms


def s2_terms(label: str, n: int, bal: list[int]) -> tuple[list[int], int]:
    """The nonzero signed terms of the alternating sum, and the count of
    supported arrangements whose product is zero (recorded, excluded)."""

    windex, delta, cindex = wc.parse_s2(label)
    rows = wc.table(windex, delta, cindex, n, bal)
    all_terms = wc.nonzero_terms(rows)
    return [t for t in all_terms if t != 0], sum(1 for t in all_terms if t == 0)


def family_row(label: str, n: int, bal: list[int], run: list[int]) -> dict[str, object]:
    if label.startswith("S2("):
        terms, zero_count = s2_terms(label, n, bal)
    elif label.startswith("S1b("):
        terms = s1b_terms(wc.parse_weight_only(label), n, bal)
        zero_count = sum(1 for t in terms if t == 0)
        terms = [t for t in terms if t != 0]
    else:
        raise ValueError(label)
    magnitudes = sorted(Counter(abs(t) for t in terms).items())
    decision = certificate_decision(terms)
    return {
        "menu": label,
        "N": n,
        "term_count": len(terms),
        "zero_terms_excluded": zero_count,
        "positive_count": sum(1 for t in terms if t > 0),
        "negative_count": sum(1 for t in terms if t < 0),
        "magnitude_multiset": [[m, c] for m, c in magnitudes],
        "every_magnitude_is_one": all(m == 1 for m, _ in magnitudes),
        "total": sum(terms),
        "total_equals_running_balance": sum(terms) == run[n],
        "certificate": decision,
    }


def report(hits: list[str], bal: list[int], run: list[int]) -> dict[str, object]:
    sizes = sorted(set(FAMILY_SIZES) | {LEAN_INSTANCE_BOUND})
    rows = [family_row(label, n, bal, run) for label in hits for n in sizes]
    degenerate = all(bool(r["every_magnitude_is_one"]) for r in rows)
    return {
        "family_sizes": sizes,
        "lean_instance_bound": LEAN_INSTANCE_BOUND,
        "rows": rows,
        "every_family_degenerate": degenerate,
        "terminal": "DEGENERACY_PERSISTS" if degenerate else "CERTIFICATE_DECIDED",
        "pinned_fixtures": {
            "wedge": certificate_decision([-2, -2, -1, 2, 2, 2]),
            "witness": certificate_decision([1, 2, -1, -2, 1, 1]),
        },
    }
