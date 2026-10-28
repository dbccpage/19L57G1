"""Unit 14 check: non-factorization through a point is inequality.

Runs Genesis's own Python enumeration of pointed structures. This is sample
computation, not a proof; the proof is PrimDiff.factors_through_point_iff.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u14_factor_point.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.primdiff import (  # noqa: E402
    a3,
    all_functions_between,
    enumerate_pointed,
    implication_matrix,
)


def factors_through_point(n: int, a: int, b: int) -> bool:
    """Is there a map p from the one-point carrier range(1) into range(n)
    with p(0) = a and p(0) = b? Computed by listing all such maps."""
    return any(p[0] == a and p[0] == b for p in all_functions_between(1, n))


def main() -> int:
    failures: list[object] = []
    total = agree = a3_count = 0
    for n in range(1, 4):
        for s in enumerate_pointed(n):
            total += 1
            nonfactor = not factors_through_point(s.n, s.a, s.b)
            if nonfactor == a3(s) == (s.a != s.b):
                agree += 1
            else:
                failures.append(("disagree", s))
            if a3(s):
                a3_count += 1
    print(f"pointed structures with carrier <= 3: {total}; "
          f"non-factorization == (a != b) == a3 on {agree}; A3 extent {a3_count}")
    maps1 = all_functions_between(1, 3)
    print(f"maps from the point into a 3-element carrier: {len(maps1)} "
          f"(one per element: {sorted(maps1)})")
    if len(maps1) != 3:
        failures.append("maps")

    m = implication_matrix(3)
    art = json.loads((ROOT / "artifacts" / "primdiff.json").read_text())["implication_matrix"]
    ext = m["predicate_extents"]
    print(f"A3 extent: computed {ext['A3']}, artifact {art['predicate_extents']['A3']}; "
          f"A4_empty extent: {ext['A4_empty']} (A3 <-> A4(empty): "
          f"{m['implications']['A3->A4_empty']} and {m['implications']['A4_empty->A3']})")
    if ext != art["predicate_extents"] or m["implications"] != art["implications"]:
        failures.append("artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
