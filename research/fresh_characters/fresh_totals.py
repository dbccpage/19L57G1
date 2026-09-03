"""Stage 2: the exhaustive search for a menu member and a step rule whose
fresh total is the balance.

The class is frozen in ``PREDICTIONS.md``: six value carriers times four step
rules, twenty-four pairs, searched at every part count up to the declared
bound.  A pair meets the stage only if its total is a plain integer at every
part count in the bound AND equals the pinned balance there.  Ties are
retained.

Nothing here extends a bounded agreement past its bound.  AuthorityEffect:
None.
"""

from __future__ import annotations

import characters as ch

SEARCH_BOUND: int = 60
CROSS_CHECK_BOUND: int = 600
CHECKPOINTS: tuple[int, ...] = (10, 30, 100, 1_000, 10_000, 100_000, 1_000_000)
PINNED_CHECKPOINTS: dict[int, int] = {
    10: -1, 30: -3, 100: 1, 1_000: 2, 10_000: -23, 100_000: -48, 1_000_000: 212,
}


def pair_label(carrier: str, rule: str) -> str:
    return f"{carrier}/{rule}"


def evaluate_pair(carrier: str, rule: str, limit: int, bal: list[int]) -> dict[str, object]:
    """One menu pair against the balance, part count by part count."""

    first_non_integer: int | None = None
    first_undefined: int | None = None
    first_mismatch: int | None = None
    agreements = 0
    values: list[int | None] = []
    for n in range(1, limit + 1):
        rep = ch.total(carrier, n, ch.step_of(rule, n))
        if not rep.defined:
            if first_undefined is None:
                first_undefined = n
            values.append(None)
            continue
        if not rep.is_integer_total:
            if first_non_integer is None:
                first_non_integer = n
            values.append(None)
            continue
        values.append(rep.integer_total)
        if rep.integer_total == bal[n]:
            agreements += 1
        elif first_mismatch is None:
            first_mismatch = n
    meets = (
        first_undefined is None
        and first_non_integer is None
        and first_mismatch is None
        and agreements == limit
    )
    return {
        "pair": pair_label(carrier, rule),
        "carrier": carrier,
        "rule": rule,
        "meets_stage_2": meets,
        "agreements": agreements,
        "bound": limit,
        "first_undefined_at": first_undefined,
        "first_non_integer_at": first_non_integer,
        "first_mismatch_at": first_mismatch,
        "values_head": values[:12],
    }


def running_balance(bal: list[int], n: int) -> int:
    return sum(bal[1 : n + 1])


def search(limit: int = SEARCH_BOUND) -> dict[str, object]:
    bal = ch.balance_table(limit)
    rows = [
        evaluate_pair(carrier, rule, limit, bal)
        for carrier in ch.MENU
        for rule in ch.STEP_RULES
    ]
    hits = [row["pair"] for row in rows if row["meets_stage_2"]]
    if hits:
        terminal = "TOTAL_IDENTITY_BOUNDED"
    else:
        terminal = "NO_TOTAL_IN_CLASS"
    return {
        "menu_size": len(rows),
        "bound": limit,
        "hits": hits,
        "terminal": terminal,
        "candidates": rows,
    }


def cross_check(hits: list[str], limit: int = CROSS_CHECK_BOUND) -> dict[str, object]:
    """Every hit recomputed against the pinned balance to a larger bound, and
    the pinned running-balance checkpoints recomputed by the balance recursion
    alone.

    The checkpoints beyond the direct bound are recomputed from the balance,
    which is the pinned object; the totals are not recomputed there, and no
    sentence says they were."""

    bal = ch.balance_table(max(limit, CHECKPOINTS[-1]))
    rows: list[dict[str, object]] = []
    for label in hits:
        carrier, rule = label.split("/")
        misses = [
            n
            for n in range(1, limit + 1)
            if ch.total(carrier, n, ch.step_of(rule, n)).integer_total != bal[n]
        ]
        rows.append({"pair": label, "bound": limit, "misses": misses[:8],
                     "miss_count": len(misses)})
    checkpoints = []
    for n in CHECKPOINTS:
        got = running_balance(bal, n)
        checkpoints.append({
            "N": n,
            "running_balance": got,
            "pinned": PINNED_CHECKPOINTS[n],
            "agrees": got == PINNED_CHECKPOINTS[n],
        })
    return {
        "direct_bound": limit,
        "totals_vs_balance": rows,
        "checkpoints": checkpoints,
        "checkpoint_misses": [c["N"] for c in checkpoints if not c["agrees"]],
        "note": (
            "the checkpoints recompute the pinned running balance from the balance "
            "recursion; the totals themselves are recomputed only to the direct bound"
        ),
    }


def report(limit: int = SEARCH_BOUND) -> dict[str, object]:
    found = search(limit)
    hits = found["hits"]
    assert isinstance(hits, list)
    checks = cross_check([str(h) for h in hits])
    return {"search": found, "cross_check": checks}
