"""Stage 4: the magnitude census, and the cancellation-certificate criterion
put to work on it.

Two family kinds, both declared in ``PREDICTIONS.md`` freeze 2 before this
file existed, because the criterion reads a list of integers and the terms of
a total are not always integers:

* the TERM family of one total -- the character's values at the fresh
  members, for the carriers whose values are integers;
* the ROW family at a part count -- the totals at every step of that layer,
  for the carriers whose totals are integers.

The criterion is per-magnitude domination, reconstructed from the pinned
`certificate_iff_dominated` and cross-checked against a brute-force search
for a pairing into exact opposites plus a single-signed residual.  A zero
term carries no magnitude.

Whether diversity appears, and whether any family refuses a certificate, is
recorded here and was not stated by the charter.  AuthorityEffect: None.
"""

from __future__ import annotations

from collections import Counter

import characters as ch

RECT_BOUND: int = 60
TERM_CARRIERS: tuple[str, ...] = ("V2", "V5")
ROW_CARRIERS: tuple[str, ...] = ("V2", "V5", "V6")


def magnitudes_present(weights: list[int]) -> set[int]:
    """Every positive magnitude carried by some term, whatever its sign."""

    return {abs(w) for w in weights if w != 0}


def dominated_nonneg(weights: list[int]) -> bool:
    counts = Counter(weights)
    return all(counts[-v] <= counts[v] for v in magnitudes_present(weights))


def dominated_nonpos(weights: list[int]) -> bool:
    counts = Counter(weights)
    return all(counts[v] <= counts[-v] for v in magnitudes_present(weights))


def certificate_decision(weights: list[int]) -> dict[str, object]:
    """The pinned criterion, reconstructed as computation."""

    nonneg = dominated_nonneg(weights)
    nonpos = dominated_nonpos(weights)
    return {
        "certificate_exists": nonneg or nonpos,
        "dominated_nonneg": nonneg,
        "dominated_nonpos": nonpos,
    }


def has_certificate_by_search(weights: list[int]) -> bool:
    """Brute force: pair terms into exact opposites, leaving a single-signed
    residual.  The criterion must agree with this."""

    def search(counter: Counter[int], residual_sign: int) -> bool:
        wrong = [v for v, c in counter.items() if c > 0 and v * residual_sign < 0]
        if not wrong:
            return True
        v = wrong[0]
        if counter[-v] <= 0:
            return False
        counter[v] -= 1
        counter[-v] -= 1
        ok = search(counter, residual_sign)
        counter[v] += 1
        counter[-v] += 1
        return ok

    base = Counter(weights)
    return search(Counter(base), 1) or search(Counter(base), -1)


def term_family(carrier: str, n: int, a: int) -> list[int] | None:
    rep = ch.total(carrier, n, a)
    if not rep.defined or rep.term_values is None:
        return None
    return list(rep.term_values)


def row_family(carrier: str, n: int) -> list[int] | None:
    out: list[int] = []
    for a in range(n):
        rep = ch.total(carrier, n, a)
        if not rep.defined or not rep.is_integer_total or rep.integer_total is None:
            return None
        out.append(rep.integer_total)
    return out


def census_row(kind: str, carrier: str, n: int, a: int | None,
               weights: list[int]) -> dict[str, object]:
    mags = sorted(Counter(abs(w) for w in weights if w != 0).items())
    decision = certificate_decision(weights)
    return {
        "kind": kind,
        "carrier": carrier,
        "n": n,
        "a": a,
        "terms": weights if len(weights) <= 24 else weights[:24],
        "term_count": len(weights),
        "magnitude_multiset": mags,
        "distinct_magnitudes": len(mags),
        "total": sum(weights),
        "certificate_exists": decision["certificate_exists"],
        "dominated_nonneg": decision["dominated_nonneg"],
        "dominated_nonpos": decision["dominated_nonpos"],
    }


def report(limit: int = RECT_BOUND) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for carrier in TERM_CARRIERS:
        for n in range(1, limit + 1):
            for a in range(n):
                weights = term_family(carrier, n, a)
                if weights is None:
                    continue
                rows.append(census_row("term", carrier, n, a, weights))
    for carrier in ROW_CARRIERS:
        for n in range(1, limit + 1):
            weights = row_family(carrier, n)
            if weights is None:
                continue
            rows.append(census_row("row", carrier, n, None, weights))

    def summarise(kind: str) -> dict[str, object]:
        sel = [r for r in rows if r["kind"] == kind]
        diverse = [r for r in sel if int(str(r["distinct_magnitudes"])) >= 2]
        refused = [r for r in sel if not r["certificate_exists"]]
        mags: set[int] = set()
        for r in sel:
            multiset = r["magnitude_multiset"]
            assert isinstance(multiset, list)
            for pair in multiset:
                mags.add(int(pair[0]))
        first_diverse = None
        if diverse:
            head = min(diverse, key=lambda r: (int(str(r["n"])), str(r["carrier"])))
            first_diverse = {"carrier": head["carrier"], "n": head["n"], "a": head["a"],
                             "magnitude_multiset": head["magnitude_multiset"]}
        first_refusal = None
        if refused:
            head = min(refused, key=lambda r: (int(str(r["n"])), str(r["carrier"])))
            first_refusal = {"carrier": head["carrier"], "n": head["n"], "a": head["a"],
                             "terms": head["terms"], "total": head["total"],
                             "magnitude_multiset": head["magnitude_multiset"]}
        return {
            "families": len(sel),
            "diverse_families": len(diverse),
            "distinct_magnitudes_seen": sorted(mags),
            "smallest_diverse_witness": first_diverse,
            "certificate_refusals": len(refused),
            "smallest_refusal_witness": first_refusal,
        }

    term = summarise("term")
    row = summarise("row")
    # every row family above part count one should total to zero; checked
    row_total_misses = [
        {"carrier": r["carrier"], "n": r["n"], "total": r["total"]}
        for r in rows
        if r["kind"] == "row" and int(str(r["n"])) >= 2 and r["total"] != 0
    ]
    row_total_misses_by_carrier = {
        carrier: len([m for m in row_total_misses if m["carrier"] == carrier])
        for carrier in ROW_CARRIERS
    }
    # the criterion against the brute force, on the whole rectangle
    criterion_misses: list[dict[str, object]] = []
    for r in rows:
        kind = str(r["kind"])
        carrier = str(r["carrier"])
        n = int(str(r["n"]))
        if kind == "term":
            a_raw = r["a"]
            assert a_raw is not None
            family = term_family(carrier, n, int(str(a_raw)))
        else:
            family = row_family(carrier, n)
        if family is None:
            continue
        if bool(r["certificate_exists"]) != has_certificate_by_search(family):
            criterion_misses.append(
                {"kind": kind, "carrier": carrier, "n": n, "a": r["a"]}
            )

    terminals = []
    if int(str(row["diverse_families"])) or int(str(term["diverse_families"])):
        terminals.append("DIVERSITY_EXHIBITED")
    if not int(str(row["diverse_families"])) and not int(str(term["diverse_families"])):
        terminals.append("DEGENERACY_PERSISTS")
    if int(str(row["certificate_refusals"])) or int(str(term["certificate_refusals"])):
        terminals.append("CERTIFICATE_REFUSED")
    return {
        "bound": limit,
        "term_family_kind": term,
        "row_family_kind": row,
        "row_total_misses": row_total_misses[:8],
        "row_total_miss_count": len(row_total_misses),
        "row_total_misses_by_carrier": row_total_misses_by_carrier,
        "criterion_vs_brute_force_misses": criterion_misses[:8],
        "criterion_miss_count": len(criterion_misses),
        "terminals": terminals,
        "refusal_part_counts": sorted({
            int(str(r["n"])) for r in rows
            if r["kind"] == "row" and not r["certificate_exists"]
        }),
        "rows_head": [r for r in rows if r["kind"] == "row" and int(str(r["n"])) <= 12
                      and r["carrier"] == "V6"],
    }
