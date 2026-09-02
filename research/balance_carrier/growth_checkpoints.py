"""Stage 4: growth checkpoints -- a protected open.

The running balance recomputed three ways at every pinned checkpoint --
directly by the pinned divisor recursion, through the S1b identity (the
walk-sum recursion with weight ``-1``), and through the S2 unit table's
column route -- with agreement recorded; the ratio of the absolute
running balance to the square root of ``N`` recorded at each checkpoint
and at the running maximum over ``2..N``, as exact rationals (the square
of the ratio as a reduced fraction) and as a six-place decimal computed
with integer arithmetic.  Every value here is a checkpoint value, never a
rate; no sentence in this module or its receipt is about how the ratio
behaves beyond the last checkpoint.  Nothing here uses floating point.

AuthorityEffect: None.
"""

from __future__ import annotations

from math import gcd, isqrt

import walk_carrier as wc

CHECKPOINTS: tuple[int, ...] = wc.CHECKPOINTS
UNIT_TABLE: tuple[str, int, str] = ("W1", 1, "C1")
S1B_WEIGHT: str = "W2"


def reduced(num: int, den: int) -> list[int]:
    g = gcd(num, den) or 1
    return [num // g, den // g]


def ratio_decimal(value: int, n: int) -> str:
    """``|value| / sqrt(n)`` to six places, by integer square root."""

    scaled = isqrt(value * value * 10**12 // n)
    return f"{scaled // 10**6}.{scaled % 10**6:06d}"


def running_maximum(run: list[int], limit: int) -> dict[str, object]:
    """The maximum of ``run[n]^2 / n`` over ``2..limit`` as an exact
    fraction, its part count, and whether the square stays below ``n``
    throughout the window (a value about the window, not a bound)."""

    best_num, best_den, best_at = 0, 1, 0
    below = True
    for n in range(2, limit + 1):
        num = run[n] * run[n]
        if num * best_den > best_num * n:
            best_num, best_den, best_at = num, n, n
        if num >= n:
            below = False
    return {
        "max_squared_ratio": reduced(best_num, best_den),
        "at_part_count": best_at,
        "ratio_decimal_at_max": ratio_decimal(run[best_at], best_at) if best_at else "0.000000",
        "square_stays_below_n_in_window": below,
        "window": limit,
    }


def report(bal: list[int], run: list[int]) -> dict[str, object]:
    limit = len(run) - 1
    s1b = wc.total_walk_sums(S1B_WEIGHT, limit, bal)
    rows: list[dict[str, object]] = []
    misses: list[int] = []
    for n in CHECKPOINTS:
        if n > limit:
            continue
        direct = run[n]
        through_s1b = s1b[n]
        through_s2 = wc.table_count_column_route(*UNIT_TABLE, n, bal)
        agree = direct == through_s1b == through_s2
        if not agree:
            misses.append(n)
        rows.append(
            {
                "N": n,
                "direct": direct,
                "through_S1b_W2": through_s1b,
                "through_S2_unit_table": through_s2,
                "agree": agree,
                "squared_ratio": reduced(direct * direct, n),
                "ratio_decimal": ratio_decimal(direct, n),
            }
        )
    return {
        "checkpoints": rows,
        "checkpoint_misses": misses,
        "running_maximum": running_maximum(run, limit),
        "terminal": "GROWTH_OPEN_UNCHANGED",
    }
