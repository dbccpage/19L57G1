"""A pedagogical cost-2 tie: three orientations, two iso-classes after flip.

This is an illustration of a tie, not a replay of FIG-TIED-L.
The sealed counts live in coda/figures.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Tuple


@dataclass(frozen=True)
class Orientation:
    """A cost-2 response: mark one of two demand slots, plus a label."""

    marked: str
    label: str

    def flipped(self) -> "Orientation":
        swap = {"L": "R", "R": "L"}
        return Orientation(marked=swap[self.marked], label=self.label)


def cost_two_orientations() -> Tuple[Orientation, ...]:
    """Three concrete cost-2 responses. The third is a flip of the first."""
    a = Orientation(marked="L", label="mark-left")
    b = Orientation(marked="R", label="mark-right")
    c = a.flipped()
    return (a, b, c)


def _canon(x: Orientation) -> Tuple[str, str]:
    y = x.flipped()
    left = (x.marked, x.label)
    right = (y.marked, y.label)
    return left if left <= right else right


def iso_classes(
    items: Tuple[Orientation, ...],
) -> FrozenSet[FrozenSet[Orientation]]:
    """Quotient by flip. a ~ flip(a); distinct labels stay distinct."""
    buckets: dict[Tuple[str, str], set[Orientation]] = {}
    for x in items:
        buckets.setdefault(_canon(x), set()).add(x)
    return frozenset(frozenset(v) for v in buckets.values())
