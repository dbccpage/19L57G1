"""Unit 01 check: the representative merges exactly the equal signatures.

Exhaustive over every carrier range(n) for n <= 4 and every family of at
most two partitions of it: `representative(x) == representative(y)` holds
exactly when the signatures of x and y agree. That is the content of
`Compression.pQ_exact` on these carriers; the proof for every carrier is
the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i01_representative.py
"""
from __future__ import annotations

import itertools

import _tree  # noqa: F401
from model import partitions, representative, sig  # noqa: E402


def main() -> int:
    checked = 0
    bad = []
    for n in range(1, 5):
        parts = partitions(n)
        families = [()] + [(p,) for p in parts] + list(itertools.combinations(parts, 2))
        for family in families:
            for x in range(n):
                for y in range(n):
                    checked += 1
                    same_rep = representative(n, family, x) == representative(n, family, y)
                    same_sig = sig(family, x) == sig(family, y)
                    if same_rep != same_sig:
                        bad.append((n, family, x, y))
    print(f"pairs checked: {checked}")
    print(f"disagreements: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
