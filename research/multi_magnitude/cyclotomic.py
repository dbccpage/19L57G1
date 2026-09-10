"""Cyclotomic reduction carrier (V6) and magnitude census.

Constructs integer-valued row families from cyclotomic reduction modulo
the layer's fresh part Phi_n(x). Reconstructs carrier V6 from fresh_characters
and evaluates the cancellation-certificate criterion.

AuthorityEffect: None.
"""

from __future__ import annotations

from collections import Counter
from math import gcd

Poly = list[int]


def trim(p: Poly) -> Poly:
    q = list(p)
    while q and q[-1] == 0:
        q.pop()
    return q


def padd(p: Poly, q: Poly) -> Poly:
    m = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(m)]


def psub(p: Poly, q: Poly) -> Poly:
    return padd(p, [-x for x in q])


def shift(k: int, p: Poly) -> Poly:
    return [0] * k + list(p)


def mono_one(k: int) -> Poly:
    return shift(k, [1])


def pdivmod(p: Poly, g: Poly) -> tuple[Poly, Poly]:
    """Division with remainder by a MONIC divisor from the top."""
    r = trim(p)
    tg = trim(g)
    q: Poly = []
    if not tg:
        return (q, r)
    while len(r) >= len(tg):
        k = len(r) - len(tg)
        c = r[-1]
        r = trim(psub(r, shift(k, [c * x for x in tg])))
        q = padd(q, shift(k, [c]))
    return (trim(q), r)


def divisors_below(n: int) -> list[int]:
    return [d for d in range(1, n) if n % d == 0]


def fresh_members(n: int) -> list[int]:
    return [c for c in range(n) if gcd(c, n) == 1]


_FRESH_PART_CACHE: dict[int, Poly] = {}


def fresh_part(n: int) -> Poly:
    """Phi_n(x) by divisor recursion: (x^n - 1) / prod_{d | n, d < n} Phi_d(x)."""
    hit = _FRESH_PART_CACHE.get(n)
    if hit is not None:
        return hit
    acc = psub(mono_one(n), [1])
    for d in divisors_below(n):
        quotient, remainder = pdivmod(acc, fresh_part(d))
        if remainder:
            raise AssertionError(f"Phi_{d} does not divide x^{n} - 1")
        acc = quotient
    _FRESH_PART_CACHE[n] = acc
    return acc


def fresh_poly(n: int, a: int) -> Poly:
    """Sum of x^{(a * c) mod n} over c in fresh_members(n)."""
    acc: Poly = []
    for c in fresh_members(n):
        exp = (a * c) % n
        acc = padd(acc, mono_one(exp))
    return trim(acc)


def v6_total(n: int, a: int) -> int | None:
    """Reduction of fresh_poly(n, a) modulo Phi_n(x). Constant remainder -> int."""
    rem = trim(pdivmod(fresh_poly(n, a), fresh_part(n))[1])
    if len(rem) <= 1:
        return rem[0] if rem else 0
    return None


def row_family_v6(n: int) -> list[int] | None:
    """The row of step totals for a in 0..n-1 under carrier V6."""
    out: list[int] = []
    for a in range(n):
        tot = v6_total(n, a)
        if tot is None:
            return None
        out.append(tot)
    return out


def magnitudes_present(weights: list[int]) -> set[int]:
    return {abs(w) for w in weights if w != 0}


def certificate_decision(weights: list[int]) -> dict[str, object]:
    """Per-magnitude domination on one side or the other."""
    mags = magnitudes_present(weights)
    counts = Counter(weights)
    neg_dominated = all(counts[-v] <= counts[v] for v in mags)
    pos_dominated = all(counts[v] <= counts[-v] for v in mags)
    return {
        "certificate_exists": neg_dominated or pos_dominated,
        "neg_dominated": neg_dominated,
        "pos_dominated": pos_dominated,
        "magnitudes": sorted(mags),
        "distinct_magnitudes": len(mags),
    }


def cyclotomic_census(limit: int = 60) -> dict[str, object]:
    """Census of row families under V6 up to limit."""
    rows: list[dict[str, object]] = []
    diverse_count = 0
    refused_count = 0
    distinct_mags: set[int] = set()

    for n in range(1, limit + 1):
        row = row_family_v6(n)
        if row is None:
            continue
        dec = certificate_decision(row)
        mags = dec["magnitudes"]
        assert isinstance(mags, list)
        for m in mags:
            distinct_mags.add(m)
        is_diverse = len(mags) >= 2
        is_refused = not dec["certificate_exists"]
        if is_diverse:
            diverse_count += 1
        if is_refused:
            refused_count += 1
        rows.append({
            "n": n,
            "row": row,
            "total": sum(row),
            "magnitudes": mags,
            "distinct_magnitudes": len(mags),
            "certificate_exists": dec["certificate_exists"],
        })

    return {
        "bound": limit,
        "total_families": len(rows),
        "diverse_families": diverse_count,
        "distinct_magnitudes_seen": sorted(distinct_mags),
        "refusals": refused_count,
        "rows": rows,
    }
