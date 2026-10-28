"""Independent finite model of B1(i)-(iii).  AuthorityEffect: None.

Nothing here is imported from the Lean library or from another tree.  The
model recomputes, by exhaustive search on the bounds pinned in input.json:

* Gaussian-integer polarization on a box of amplitudes;
* the instance carrier: its weight and readout presentations, their class
  counts, whether the weights know the readout, and the interference
  challenge;
* the conjugation classes of each cyclic phase group up to max_order, and
  for each multiplicity the least order whose classes can be separated.

A passing check is a finite receipt on these bounds, not a proof.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import json
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class GI:
    """A Gaussian integer re + im*i."""

    re: int
    im: int

    def __add__(self, other: GI) -> GI:
        return GI(self.re + other.re, self.im + other.im)

    def __mul__(self, other: GI) -> GI:
        return GI(self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re)

    def conj(self) -> GI:
        return GI(self.re, -self.im)

    def norm(self) -> int:
        return self.re * self.re + self.im * self.im


def cross(a: GI, b: GI) -> int:
    return (a * b.conj()).re


Prep = tuple[GI, GI]
Presentation = Callable[[int], int]


def mix(p: Prep) -> int:
    return (p[0] + p[1]).norm()


def weights(p: Prep) -> tuple[int, int]:
    return (p[0].norm(), p[1].norm())


def load() -> dict[str, Any]:
    value = json.loads((HERE / "input.json").read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("input.json must hold an object")
    return value


def polarization_failures(box: int) -> list[tuple[GI, GI]]:
    """Pairs in the box where norm(a+b) differs from norm a + norm b + 2 cross."""
    values = [GI(x, y) for x in range(-box, box + 1) for y in range(-box, box + 1)]
    return [(a, b) for a, b in product(values, values)
            if (a + b).norm() != a.norm() + b.norm() + 2 * cross(a, b)]


def fiber_pairs_without_cross_criterion(box: int) -> int:
    """Weight-equal pairs of preparations on which 'readouts differ' and
    'cross terms differ' disagree (expected: none)."""
    values = [GI(x, y) for x in range(-box, box + 1) for y in range(-box, box + 1)]
    preps = [(a, b) for a in values[:: max(1, len(values) // 7)] for b in values]
    bad = 0
    for p, q in product(preps, preps):
        if weights(p) == weights(q):
            if (mix(p) != mix(q)) != (cross(*p) != cross(*q)):
                bad += 1
    return bad


def instance() -> tuple[list[int], dict[int, Prep]]:
    spec = load()["instance"]
    carrier = [int(x) for x in spec["carrier"]]
    amps = {int(k): (GI(*v[0]), GI(*v[1])) for k, v in spec["amplitudes"].items()}
    return carrier, amps


def class_count(carrier: list[int], questions: list[Presentation]) -> int:
    return len({tuple(q(x) for q in questions) for x in carrier})


def knows(carrier: list[int], questions: list[Presentation], q: Presentation) -> bool:
    answer: dict[tuple[int, ...], int] = {}
    for x in carrier:
        key = tuple(f(x) for f in questions)
        if answer.setdefault(key, q(x)) != q(x):
            return False
    return True


def challenge(carrier: list[int], questions: list[Presentation], q: Presentation) -> bool:
    return any(all(f(x) == f(y) for f in questions) and q(x) != q(y)
               for x in carrier for y in carrier)


def instance_report() -> dict[str, Any]:
    carrier, amps = instance()

    def w1(x: int) -> int:
        return amps[x][0].norm()

    def w2(x: int) -> int:
        return amps[x][1].norm()

    def readout(x: int) -> int:
        return mix(amps[x])

    return {
        "information_weights": class_count(carrier, [w1, w2]),
        "information_with_readout": class_count(carrier, [w1, w2, readout]),
        "knows": knows(carrier, [w1, w2], readout),
        "challenge": challenge(carrier, [w1, w2], readout),
        "readouts": [readout(x) for x in carrier],
    }


def orbits(order: int) -> int:
    """Number of classes of the exponents 0..order-1 under j -> -j mod order."""
    seen: set[frozenset[int]] = set()
    for j in range(order):
        seen.add(frozenset({j, (-j) % order}))
    return len(seen)


def least_order(multiplicity: int, max_order: int) -> int | None:
    """Least order whose conjugation classes can carry `multiplicity`
    pairwise different invariant readouts (an invariant readout separates
    phases exactly when they lie in different classes)."""
    for order in range(1, max_order + 1):
        if orbits(order) >= multiplicity:
            return order
    return None


def mu4_readouts() -> list[int]:
    one, i = GI(1, 0), GI(0, 1)
    units = [one, i, i * i, i * i * i]
    return [mix((one, u)) for u in units]
