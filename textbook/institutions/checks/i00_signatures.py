"""Unit 00 check: the signature table of a family on a carrier.

Runs the research tree's own Python (`research/actor_institution/model.py`).
A worked example, not a proof and not a verification: it prints what the
definitions say about one family on three data. AuthorityEffect: None.
Run from the repository root: python textbook/institutions/checks/i00_signatures.py
"""
from __future__ import annotations

import _tree  # noqa: F401
from model import P1, P2, Q3, sig  # noqa: E402


def main() -> int:
    carrier = [0, 1, 2]
    family = (P1, P2)
    print(f"carrier {carrier}; members p1={P1}, p2={P2}; claim q3={Q3}")
    for x in carrier:
        print(f"datum {x}: signature {sig(family, x)}  q3 {Q3[x]}")
    merged = [(x, y) for x in carrier for y in carrier if x < y and sig(family, x) == sig(family, y)]
    print(f"pairs the family cannot tell apart: {merged}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
