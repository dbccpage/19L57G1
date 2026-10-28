"""Unit 02 check: knowing as factoring agrees with the signature test.

Exhaustive over range(n) for n <= 4, every family of at most two
partitions, and every partition as the claim: `model.knows` (equal
signatures force equal values) agrees with "the claim factors through the
representative" (the claim's value at x is its value at the representative
of x). That is `Institution.knows_iff_determined` on these carriers; the
proof for every carrier is the Lean. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i02_knowing.py
"""
from __future__ import annotations

import itertools

import _tree  # noqa: F401
from model import knows, partitions, representative  # noqa: E402


def factors(n: int, family: tuple[tuple[int, ...], ...], q: tuple[int, ...]) -> bool:
    """`FactorsOn D (pQ D Q) q`: q is a function of the representative.

    The witness `g` sends a representative r to q[r]; it exists exactly
    when q takes the same value at every datum and at its representative.
    """
    return all(q[x] == q[representative(n, family, x)] for x in range(n))


def main() -> int:
    checked = 0
    bad = []
    known = 0
    for n in range(1, 5):
        parts = partitions(n)
        families = [()] + [(p,) for p in parts] + list(itertools.combinations(parts, 2))
        for family in families:
            for q in parts:
                checked += 1
                k = knows(n, family, q)
                known += k
                if k != factors(n, family, q):
                    bad.append((n, family, q))
    print(f"(family, claim) pairs checked: {checked}; known: {known}")
    print(f"disagreements: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
