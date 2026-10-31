"""Unit 03 check: information is bounded, monotone, and stationary exactly
on known questions.

Enumerates range(n), 1 <= n <= 4, with the empty family, each single
partition and one ordering of each pair of distinct partitions, and every
partition as the added question. Not all ordered lists or repeated members:
  information <= n                                  (information_le_carrier)
  information(Q) <= information(Q ++ [q])           (information_mono)
  knows(Q, q)  iff  information(Q ++ [q]) == information(Q)
                                                    (knows_iff_information_eq)
  not knows(Q, q)  implies  information(Q) < information(Q ++ [q])
                                                    (information_lt_of_not_knows)
The proofs for every carrier are the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i03_information.py
"""
from __future__ import annotations

import itertools

import _tree  # noqa: F401
from model import information, knows, partitions  # noqa: E402


def main() -> int:
    checked = 0
    bad = []
    for n in range(1, 5):
        parts = partitions(n)
        families = [()] + [(p,) for p in parts] + list(itertools.combinations(parts, 2))
        for family in families:
            before = information(n, family)
            if before > n:
                bad.append(("bound", n, family))
            for q in parts:
                checked += 1
                after = information(n, family + (q,))
                if after < before:
                    bad.append(("mono", n, family, q))
                if knows(n, family, q) != (after == before):
                    bad.append(("stationary", n, family, q))
                if not knows(n, family, q) and not before < after:
                    bad.append(("strict", n, family, q))
    print(f"(family, question) pairs checked: {checked}")
    print(f"violations: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
