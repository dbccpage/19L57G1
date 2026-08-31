"""Aggregation survey on the chord square over ``Z_3``.

Three diagnostics over the five-edge chord square with the indicator
gauge (1 per nonzero edge phase): the EDGE SUM, the MAX aggregator, and
the DOUBLED sum.  For every assignment over ``Z_3`` and every pair of
disjoint edge subsets, additivity is checked; on every singleton,
calibration is checked.  The pre-registered claims (STATUS.md, AG3 and
AG4): the edge sum has zero additivity violations and zero calibration
failures; the max aggregator's additivity violations are positive with
a named witness; the doubled sum fails calibration on exactly ``810``
singleton instances (five edges times the ``162`` assignments with a
nonzero phase at that edge).  Deterministic, standard library only.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from itertools import combinations, product

EDGES: tuple[int, ...] = (0, 1, 2, 3, 4)
N = 3


def gauge(value: int) -> int:
    return 0 if value == 0 else 1


def edge_sum(subset: tuple[int, ...], w: tuple[int, ...]) -> int:
    return sum(gauge(w[e]) for e in subset)


def max_agg(subset: tuple[int, ...], w: tuple[int, ...]) -> int:
    return max((gauge(w[e]) for e in subset), default=0)


def doubled(subset: tuple[int, ...], w: tuple[int, ...]) -> int:
    return 2 * sum(gauge(w[e]) for e in subset)


def disjoint_pairs() -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    subsets: list[tuple[int, ...]] = []
    for r in range(len(EDGES) + 1):
        subsets.extend(combinations(EDGES, r))
    return [(a, b) for a in subsets for b in subsets if not (set(a) & set(b))]


def survey() -> dict[str, object]:
    pairs = disjoint_pairs()
    counts = {"edge_sum": 0, "max_agg": 0, "doubled": 0}
    cal_fail = {"edge_sum": 0, "max_agg": 0, "doubled": 0}
    diags = {"edge_sum": edge_sum, "max_agg": max_agg, "doubled": doubled}
    witness: dict[str, object] = {}
    for w in product(range(N), repeat=len(EDGES)):
        for name, fn in diags.items():
            for a, b in pairs:
                if fn(a + b, w) != fn(a, w) + fn(b, w):
                    counts[name] += 1
                    if name not in witness:
                        witness[name] = {"subsets": [list(a), list(b)], "w": list(w)}
            for e in EDGES:
                if fn((e,), w) != gauge(w[e]):
                    cal_fail[name] += 1
    return {
        "modulus": N,
        "assignments": N ** len(EDGES),
        "disjoint_subset_pairs": len(pairs),
        "additivity_violations": counts,
        "calibration_failures": cal_fail,
        "first_max_violation_witness": witness.get("max_agg"),
    }


def report() -> dict[str, object]:
    return {
        "fixture": "chord square over Z_3, indicator gauge; edge sum vs max vs doubled",
        "survey": survey(),
    }
