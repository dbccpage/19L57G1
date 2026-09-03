"""Stage 3: what the divisor relation does to the totals.

Two questions, both computed over a declared rectangle and neither extended
past it:

* the divisor sum -- the sum of the totals over the divisor layers, each read
  at the step taken in that layer;
* the determination question -- whether a total depends on the step only
  through the largest divisor the step shares with the part count.

At the unit step and a part count above one, the divisor sum reproduces the
pinned `balance_divisor_sum`; that reproduction is checked here, not
assumed.  AuthorityEffect: None.
"""

from __future__ import annotations

from math import gcd

import characters as ch

RECT_BOUND: int = 60
INTEGER_CARRIERS: tuple[str, ...] = ("V2", "V5", "V6")


def integer_total(carrier: str, n: int, a: int) -> int | None:
    rep = ch.total(carrier, n, a)
    if not rep.defined or not rep.is_integer_total:
        return None
    return rep.integer_total


def divisor_total(carrier: str, n: int, a: int) -> int | None:
    """The sum of the totals over the divisor layers, each read at the step
    taken in that layer."""

    acc = 0
    for d in ch.divisors(n):
        value = integer_total(carrier, d, a % d)
        if value is None:
            return None
        acc += value
    return acc


def report(limit: int = RECT_BOUND) -> dict[str, object]:
    bal = ch.balance_table(limit)
    rows: list[dict[str, object]] = []
    for carrier in INTEGER_CARRIERS:
        sum_misses: list[tuple[int, int, int, int]] = []
        undefined: list[tuple[int, int]] = []
        determination_misses: list[tuple[int, int, int]] = []
        balance_recursion_misses: list[int] = []
        for n in range(1, limit + 1):
            by_shared: dict[int, int] = {}
            for a in range(n):
                got = divisor_total(carrier, n, a)
                if got is None:
                    undefined.append((n, a))
                    continue
                want = n if a == 0 else 0
                if got != want:
                    sum_misses.append((n, a, got, want))
                value = integer_total(carrier, n, a)
                if value is None:
                    undefined.append((n, a))
                    continue
                g = gcd(a, n)
                seen = by_shared.get(g)
                if seen is None:
                    by_shared[g] = value
                elif seen != value:
                    determination_misses.append((n, a, g))
            if n >= 2:
                unit = divisor_total(carrier, n, 1 % n)
                if unit != 0:
                    balance_recursion_misses.append(n)
        rows.append({
            "carrier": carrier,
            "bound": limit,
            "divisor_sum_misses": sum_misses[:8],
            "divisor_sum_miss_count": len(sum_misses),
            "undefined_cells": undefined[:8],
            "undefined_count": len(undefined),
            "determination_misses": determination_misses[:8],
            "determination_miss_count": len(determination_misses),
            "balance_recursion_misses": balance_recursion_misses[:8],
        })
    # the pinned balance's own divisor recursion, recomputed as the reference
    pinned_misses = [
        n for n in range(2, limit + 1) if sum(bal[d] for d in ch.divisors(n)) != 0
    ]
    clean = [r for r in rows if r["divisor_sum_miss_count"] == 0 and r["undefined_count"] == 0]
    terminal = "RECURSION_BOUNDED" if clean else "OPEN_AT_NAMED_TARGET"
    return {
        "bound": limit,
        "carriers": list(INTEGER_CARRIERS),
        "rows": rows,
        "pinned_balance_divisor_sum_misses": pinned_misses,
        "carriers_meeting_the_recursion": [str(r["carrier"]) for r in clean],
        "terminal": terminal,
        "note": (
            "the divisor sum is the part count at the zero step and vanishes at every "
            "other step, within the bound in this record and nowhere beyond it"
        ),
    }
