"""Unit 04 check: a family knows what no member knows.

Two exhaustive checks on range(n), n <= 4, families of at most three
distinct partitions, every partition as the claim:
  1. `exceeds` agrees with the two clauses of `Inst.exceeds_iff` (every
     pair the claim tells apart is told apart by some member; every member
     merges some pair the claim tells apart);
  2. the census: no nonempty family exceeds on fewer than three data, no
     one-member family exceeds, and the three-point example does.
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i04_exceeds.py
"""
from __future__ import annotations

import itertools

import _tree  # noqa: F401
from model import P1, P2, Q3, exceeds, exceeding_census, exceeding_minimum, information, partitions  # noqa: E402


def clauses(n: int, family: tuple[tuple[int, ...], ...], q: tuple[int, ...]) -> bool:
    apart = [(x, y) for x in range(n) for y in range(n) if q[x] != q[y]]
    first = all(any(p[x] != p[y] for p in family) for x, y in apart)
    second = all(any(p[x] == p[y] for x, y in apart) for p in family)
    return first and second


def main() -> int:
    checked = 0
    bad = []
    for n in range(1, 5):
        parts = partitions(n)
        families = [()] + [(p,) for p in parts] + list(itertools.combinations(parts, 2)) + list(itertools.combinations(parts, 3))
        for family in families:
            for q in parts:
                checked += 1
                if exceeds(n, family, q) != clauses(n, family, q):
                    bad.append((n, family, q))
    print(f"(family, claim) pairs checked against exceeds_iff: {checked}; disagreements: {bad}")
    census = exceeding_census(4, 3)
    minimum = exceeding_minimum(census)
    print(f"census minimum (nonempty families): {minimum}")
    example = exceeds(3, (P1, P2), Q3)
    counts = [information(3, (P1,)), information(3, (P2,)), information(3, (Q3,)), information(3, (P1, P2))]
    print(f"three-point example exceeds: {example}; class counts p1, p2, q3, family: {counts}")
    ok = (not bad and minimum["min_data"] == 3 and minimum["min_members"] == 2
          and example and counts == [2, 2, 2, 3])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
