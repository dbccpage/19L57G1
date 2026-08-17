"""Two sandcastles: ranking reverses when the measure changes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

Winner = Literal["A", "B", "tie"]
Measure = Callable[["Castle"], float]


@dataclass(frozen=True)
class Castle:
    name: str
    height: float
    width: float


def height_measure(c: Castle) -> float:
    return c.height


def width_measure(c: Castle) -> float:
    return c.width


def better(a: Castle, b: Castle, measure: Measure) -> Winner:
    va = measure(a)
    vb = measure(b)
    if va > vb:
        return "A"
    if vb > va:
        return "B"
    return "tie"
