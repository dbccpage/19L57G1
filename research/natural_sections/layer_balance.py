"""Layer balance: fresh counts, the signed inversion, and its running sum.

The Lean module ``lean/NaturalSections/LayerBalance.lean`` proves the
divisor recursion's laws and decides small instances; this module
recomputes the finite slices pre-registered in ``STATUS.md`` by brute
force, independently of the proofs, in exact integer arithmetic.  Two
independent computations of the balance are compared at every part
count up to the declared bound: the divisor recursion, faithful to the
definition, and a smallest-factor table that never performs a divisor
sum.  Nothing here uses floating point.

AuthorityEffect: None.
"""

from __future__ import annotations

from functools import lru_cache
from math import gcd

BOUND: int = 1_000_000
SMALL_BOUND: int = 2_000
CHECKPOINTS: tuple[int, ...] = (10, 30, 100, 1_000, 10_000, 100_000, 1_000_000)


def fresh_count(n: int) -> int:
    """The number of parts at part count ``n`` sharing no factor with it."""

    return sum(1 for j in range(n) if gcd(j, n) == 1)


def balance_by_recursion(limit: int) -> list[int]:
    """The balance at ``0..limit`` by the divisor recursion itself.

    ``vals[1] = 1``; every proper divisor ``d`` of ``m`` contributes
    ``-vals[d]`` to ``vals[m]``.  Processing ``d`` in increasing order
    makes each entry final before it is used.
    """

    vals = [0] * (limit + 1)
    if limit >= 1:
        vals[1] = 1
    for d in range(1, limit + 1):
        contribution = vals[d]
        if contribution != 0:
            for m in range(2 * d, limit + 1, d):
                vals[m] -= contribution
    return vals


def balance_by_factors(limit: int) -> list[int]:
    """The balance at ``0..limit`` from a smallest-factor table.

    No divisor sums anywhere: a part count with a repeated smallest
    factor gets ``0``; otherwise the sign flips per factor.
    """

    smallest = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if smallest[i] == 0:
            for j in range(i, limit + 1, i):
                if smallest[j] == 0:
                    smallest[j] = i
    vals = [0] * (limit + 1)
    if limit >= 1:
        vals[1] = 1
    for n in range(2, limit + 1):
        f = smallest[n]
        m = n // f
        vals[n] = 0 if m % f == 0 else -vals[m]
    return vals


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def running_balance(vals: list[int], n: int) -> int:
    return sum(vals[1 : n + 1])


@lru_cache(maxsize=1)
def report() -> dict[str, object]:
    by_recursion = balance_by_recursion(BOUND)
    by_factors = balance_by_factors(BOUND)
    agreement_misses = sum(
        1 for n in range(BOUND + 1) if by_recursion[n] != by_factors[n]
    )

    fresh_counts = [fresh_count(n) for n in range(1, SMALL_BOUND + 1)]
    partition_misses = [
        n
        for n in range(1, SMALL_BOUND + 1)
        if sum(fresh_counts[d - 1] for d in divisors(n)) != n
    ]
    inversion_misses = [
        n
        for n in range(1, SMALL_BOUND + 1)
        if sum(by_recursion[d] * (n // d) for d in divisors(n)) != fresh_counts[n - 1]
    ]

    running = 0
    checkpoint_values: dict[str, int] = {}
    wanted = set(CHECKPOINTS)
    best_num = 0  # running balance squared at the best part count
    best_den = 1  # that part count
    best_at = 0
    below_one = True
    for n in range(1, BOUND + 1):
        running += by_recursion[n]
        if n in wanted:
            checkpoint_values[str(n)] = running
        if n >= 2:
            num = running * running
            if num * best_den > best_num * n:
                best_num = num
                best_den = n
                best_at = n
            if num >= n:
                below_one = False

    return {
        "bound": BOUND,
        "small_bound": SMALL_BOUND,
        "balance_1_12": by_recursion[1:13],
        "fresh_counts_1_12": fresh_counts[:12],
        "agreement_misses": agreement_misses,
        "partition_misses": partition_misses,
        "inversion_misses": inversion_misses,
        "running_balance_checkpoints": checkpoint_values,
        "growth": {
            "max_squared_ratio_num": best_num,
            "max_squared_ratio_den": best_den,
            "at_part_count": best_at,
            "stays_below_the_square_root": below_one,
        },
    }
