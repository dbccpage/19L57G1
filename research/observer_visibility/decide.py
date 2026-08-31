"""OV5 decision: sound iff im(D) meets the joint-kernel product only at 0.

Linear decision is the rational nullspace of W ∘ D.  Brute force is a
separate enumeration that only calls diagram.all_green and diagram.mass.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import math
from fractions import Fraction
from itertools import product
from typing import Sequence

import diagram as dg
from diagram import Edge, Section

Watch = dict[Edge, tuple[bool, bool]]
Matrix = list[list[Fraction]]
Vector = list[Fraction]


def flatten(s: Section, n_obj: int) -> tuple[int, ...]:
    out: list[int] = []
    for i in range(n_obj):
        p = s[i]
        out.extend([p[0], p[1]])
    return tuple(out)


def unflatten(coords: Sequence[int], n_obj: int) -> Section:
    s: Section = {}
    for i in range(n_obj):
        s[i] = (coords[2 * i], coords[2 * i + 1])
    return s


def support(s: Section) -> int:
    return sum(1 for v in s.values() if v != (0, 0))


def watch_matrix(n_obj: int, edges: Sequence[Edge], watch: Watch) -> Matrix:
    cols = 2 * n_obj
    rows: Matrix = []
    for edge in edges:
        src, tgt = edge
        wx, wy = watch.get(edge, (True, False))
        if wx:
            row = [Fraction(0)] * cols
            row[2 * tgt] += 1
            row[2 * src] -= 1
            rows.append(row)
        if wy:
            row = [Fraction(0)] * cols
            row[2 * tgt + 1] += 1
            row[2 * src + 1] -= 1
            rows.append(row)
    return rows


def coboundary_matrix(n_obj: int, edges: Sequence[Edge]) -> Matrix:
    cols = 2 * n_obj
    rows: Matrix = []
    for src, tgt in edges:
        rx = [Fraction(0)] * cols
        rx[2 * tgt] += 1
        rx[2 * src] -= 1
        rows.append(rx)
        ry = [Fraction(0)] * cols
        ry[2 * tgt + 1] += 1
        ry[2 * src + 1] -= 1
        rows.append(ry)
    return rows


def rref(matrix: Matrix) -> tuple[Matrix, list[int]]:
    if not matrix:
        return [], []
    m = len(matrix)
    n = len(matrix[0])
    reduced = [row[:] for row in matrix]
    pivots: list[int] = []
    row = 0
    for col in range(n):
        pivot_row: int | None = None
        for candidate in range(row, m):
            if reduced[candidate][col] != 0:
                pivot_row = candidate
                break
        if pivot_row is None:
            continue
        reduced[row], reduced[pivot_row] = reduced[pivot_row], reduced[row]
        divisor = reduced[row][col]
        reduced[row] = [entry / divisor for entry in reduced[row]]
        for other in range(m):
            if other == row:
                continue
            factor = reduced[other][col]
            if factor == 0:
                continue
            reduced[other] = [
                a - factor * b for a, b in zip(reduced[other], reduced[row], strict=True)
            ]
        pivots.append(col)
        row += 1
        if row == m:
            break
    return reduced, pivots


def nullspace(matrix: Matrix, n_cols: int) -> list[Vector]:
    """Right-kernel basis of a matrix with ``n_cols`` columns, over Q."""

    if n_cols == 0:
        return []
    if not matrix:
        return [
            [Fraction(int(i == j)) for i in range(n_cols)] for j in range(n_cols)
        ]
    reduced, pivots = rref(matrix)
    pivot_set = set(pivots)
    free = [col for col in range(n_cols) if col not in pivot_set]
    pivot_row = {pivots[index]: index for index in range(len(pivots))}
    basis: list[Vector] = []
    for free_col in free:
        vector = [Fraction(0)] * n_cols
        vector[free_col] = Fraction(1)
        for pivot_col, index in pivot_row.items():
            vector[pivot_col] = -reduced[index][free_col]
        basis.append(vector)
    return basis


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum((a * x for a, x in zip(row, vector, strict=True)), Fraction(0))
        for row in matrix
    ]


def scale_to_int(vector: Vector) -> list[int]:
    if not vector:
        return []
    lcm = 1
    for entry in vector:
        lcm = lcm * entry.denominator // math.gcd(lcm, entry.denominator)
    ints = [int(entry * lcm) for entry in vector]
    gcd = 0
    for value in ints:
        gcd = math.gcd(gcd, abs(value))
    if gcd > 1:
        ints = [value // gcd for value in ints]
    return ints


def decide(
    n_obj: int,
    edges: Sequence[Edge],
    watch: Watch,
    bound: int,
) -> dict[str, object]:
    """SOUND iff the Q-nullspace of W ∘ D is contained in ker D.

    An unsound witness is chosen among the RREF nullspace generators
    only (cleared denominators), by least support, then least mass, then
    lexicographic flatten.  That is min-over-generators, not min over
    the integer kernel: a combination of generators may have smaller
    support.  ``bound`` is accepted for the same calling convention as
    brute force and is unused: the linear certificate is unbounded.
    """

    del bound
    n_cols = 2 * n_obj
    watched = watch_matrix(n_obj, edges, watch)
    kernel = nullspace(watched, n_cols)
    cob = coboundary_matrix(n_obj, edges)
    best: tuple[int, int, tuple[int, ...]] | None = None
    best_s: Section | None = None
    for vector in kernel:
        image = matvec(cob, vector) if cob else []
        if all(entry == 0 for entry in image):
            continue
        ints = scale_to_int(vector)
        section = unflatten(ints, n_obj)
        key = (support(section), dg.mass(section, edges), flatten(section, n_obj))
        if best is None or key < best:
            best = key
            best_s = section
    if best_s is None:
        return {"verdict": "SOUND", "witness": None, "mass": 0, "support": 0}
    assert best is not None
    return {
        "verdict": "UNSOUND",
        "witness": {str(i): best_s[i] for i in range(n_obj)},
        "mass": best[1],
        "support": best[0],
    }


def min_unsound_on_box(
    n_obj: int,
    edges: Sequence[Edge],
    watch: Watch,
    bound: int,
) -> dict[str, object]:
    """Box scan: min support then mass among All-Green positive-mass sections.

    Independent of the Q-nullspace generators.  Certifies global
    minimality of a generator witness on a declared finite box.
    """

    flags = [watch.get(edge, (True, False)) for edge in edges]
    rng = range(-bound, bound + 1)
    best: tuple[int, int, tuple[int, ...]] | None = None
    best_s: Section | None = None
    for coords in product(rng, repeat=2 * n_obj):
        section = unflatten(coords, n_obj)
        if not dg.all_green(section, edges, flags):
            continue
        mass = dg.mass(section, edges)
        if mass == 0:
            continue
        key = (support(section), mass, flatten(section, n_obj))
        if best is None or key < best:
            best = key
            best_s = section
    if best_s is None:
        return {"verdict": "SOUND", "witness": None, "mass": 0, "support": 0}
    assert best is not None
    return {
        "verdict": "UNSOUND",
        "witness": {str(i): best_s[i] for i in range(n_obj)},
        "mass": best[1],
        "support": best[0],
    }


def brute(
    n_obj: int,
    edges: Sequence[Edge],
    watch: Watch,
    bound: int,
) -> str:
    """Independent scan: SOUND iff no All-Green coboundary of positive mass."""

    flags = [watch.get(edge, (True, False)) for edge in edges]
    rng = range(-bound, bound + 1)
    for coords in product(rng, repeat=2 * n_obj):
        section = unflatten(coords, n_obj)
        if dg.all_green(section, edges, flags) and dg.mass(section, edges) > 0:
            return "UNSOUND"
    return "SOUND"


def patch3_watch() -> Watch:
    return {edge: (True, False) for edge in dg.PATCH3_EDGES}


def extra_watch_kills_kernel() -> Watch:
    """First and second coordinates watched, so each K_e is {0}."""

    return {edge: (True, True) for edge in dg.PATCH3_EDGES}


def decide_trivial_kernels(
    n_obj: int, edges: Sequence[Edge], bound: int
) -> dict[str, object]:
    watch: Watch = {edge: (True, True) for edge in edges}
    return decide(n_obj, edges, watch, bound)
