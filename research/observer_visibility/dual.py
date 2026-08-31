"""OV8: dual certificate.  |y| bounded, annihilating All-Green coboundaries.

On the integer plane with first-coordinate watchers, y_e = 0 on the
watched first component (already zero) and the second-component pairing
against (0, ±1) recovers mass.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from typing import Sequence

from diagram import Edge, Section, cob, mass


def pairing(ys: Sequence[int], s: Section, edges: Sequence[Edge]) -> int:
    total = 0
    for y, e in zip(ys, edges, strict=True):
        d = cob(s, e)
        total += y * d[1]
    return total


def certifies(ys: Sequence[int], s: Section, edges: Sequence[Edge]) -> bool:
    if any(abs(y) > 1 for y in ys):
        return False
    return abs(pairing(ys, s, edges)) <= mass(s, edges)
