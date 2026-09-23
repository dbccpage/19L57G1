"""Exact finite mirror of the conservation ladder.

AuthorityEffect: None.  Integer arithmetic only.  The expression language,
dual evaluation and directional derivative mirror
``lean/ResearchConservationLadder/Dual.lean``; the action, variation,
charge and worked instance mirror ``Action.lean`` and ``Central.lean``.
Every check runs over the declared grid in ``input.json`` and reports its
counts; the general statements are the Lean theorems named in
``CLAIMS.md``.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from itertools import product
import json
from pathlib import Path
from typing import Union

Json = dict[str, object]
P = tuple[int, int]


@dataclass(frozen=True)
class Dual:
    re: int
    du: int

    def __add__(self, other: Dual) -> Dual:
        return Dual(self.re + other.re, self.du + other.du)

    def __mul__(self, other: Dual) -> Dual:
        return Dual(self.re * other.re, self.re * other.du + self.du * other.re)

    def __neg__(self) -> Dual:
        return Dual(-self.re, -self.du)


@dataclass(frozen=True)
class Var:
    i: int


@dataclass(frozen=True)
class Const:
    c: int


@dataclass(frozen=True)
class Add:
    a: Expr
    b: Expr


@dataclass(frozen=True)
class Mul:
    a: Expr
    b: Expr


@dataclass(frozen=True)
class Neg:
    a: Expr


Expr = Union[Var, Const, Add, Mul, Neg]


def var(i: int) -> Expr:
    return Var(i)


def const(c: int) -> Expr:
    return Const(c)


def add(a: Expr, b: Expr) -> Expr:
    return Add(a, b)


def mul(a: Expr, b: Expr) -> Expr:
    return Mul(a, b)


def neg(a: Expr) -> Expr:
    return Neg(a)


def sub(a: Expr, b: Expr) -> Expr:
    return add(a, neg(b))


def sq(a: Expr) -> Expr:
    return mul(a, a)


def evaluate(rho: Callable[[int], int], e: Expr) -> int:
    match e:
        case Var(i):
            return rho(i)
        case Const(c):
            return c
        case Add(a, b):
            return evaluate(rho, a) + evaluate(rho, b)
        case Mul(a, b):
            return evaluate(rho, a) * evaluate(rho, b)
        case Neg(a):
            return -evaluate(rho, a)


def evaluate_dual(sigma: Callable[[int], Dual], e: Expr) -> Dual:
    match e:
        case Var(i):
            return sigma(i)
        case Const(c):
            return Dual(c, 0)
        case Add(a, b):
            return evaluate_dual(sigma, a) + evaluate_dual(sigma, b)
        case Mul(a, b):
            return evaluate_dual(sigma, a) * evaluate_dual(sigma, b)
        case Neg(a):
            return -evaluate_dual(sigma, a)


def ddir(rho: Callable[[int], int], tau: Callable[[int], int], e: Expr) -> int:
    """Lean ``ddir``: the sum and product rules, syntactically."""
    match e:
        case Var(i):
            return tau(i)
        case Const(_):
            return 0
        case Add(a, b):
            return ddir(rho, tau, a) + ddir(rho, tau, b)
        case Mul(a, b):
            return evaluate(rho, a) * ddir(rho, tau, b) + ddir(rho, tau, a) * evaluate(rho, b)
        case Neg(a):
            return -ddir(rho, tau, a)


X0, Y0, X1, Y1 = var(0), var(1), var(2), var(3)


def central(c: int) -> Expr:
    return add(add(sq(sub(X1, X0)), sq(sub(Y1, Y0))), neg(mul(const(c), add(sq(X0), sq(Y0)))))


ANISO: Expr = add(add(sq(sub(X1, X0)), sq(sub(Y1, Y0))), neg(sq(X0)))


def slots(a: P, b: P) -> Callable[[int], int]:
    values = (a[0], a[1], b[0], b[1])
    return lambda i: values[i] if 0 <= i < 4 else 0


def first(v: P) -> Callable[[int], int]:
    return lambda i: v[i] if i in (0, 1) else 0


def second(v: P) -> Callable[[int], int]:
    return lambda i: v[i - 2] if i in (2, 3) else 0


def d1(e: Expr, a: P, b: P, v: P) -> int:
    return ddir(slots(a, b), first(v), e)


def d2(e: Expr, a: P, b: P, v: P) -> int:
    return ddir(slots(a, b), second(v), e)


def rot(p: P) -> P:
    return (-p[1], p[0])


def shift(_: P) -> P:
    return (1, 0)


def charge(e: Expr, xi: Callable[[P], P], a: P, b: P) -> int:
    return d2(e, a, b, xi(b))


def next_point(c: int, a: P, b: P) -> P:
    return ((2 - c) * b[0] - a[0], (2 - c) * b[1] - a[1])


def aniso_next(a: P, b: P) -> P:
    return (b[0] - a[0], 2 * b[1] - a[1])


def history(step: Callable[[P, P], P], a: P, b: P, length: int) -> list[P]:
    out = [a, b]
    while len(out) < length:
        out.append(step(out[-2], out[-1]))
    return out


def varied_action_du(e: Expr, q: list[P], k: int, v: P) -> int:
    """The dual coefficient of the action with point ``k`` moved by ``εv``."""
    def point(j: int) -> tuple[Dual, Dual]:
        dv = v if j == k else (0, 0)
        return Dual(q[j][0], dv[0]), Dual(q[j][1], dv[1])
    total = Dual(0, 0)
    for n in range(len(q) - 1):
        a, b = point(n), point(n + 1)
        values = (a[0], a[1], b[0], b[1])
        total = total + evaluate_dual(lambda i: values[i] if 0 <= i < 4 else Dual(0, 0), e)
    return total.du


def bounds() -> dict[str, int]:
    """The declared bounds, read from the pinned ``input.json``."""
    value = json.loads((Path(__file__).resolve().parent / "input.json")
                       .read_text(encoding="utf-8"))
    keys = {"grid_radius", "history_length", "coefficient_radius"}
    if (not isinstance(value, dict) or set(value) != keys
            or not all(isinstance(value[k], int) and not isinstance(value[k], bool)
                       and value[k] >= 0 for k in keys)):
        raise ValueError("input.json: expected three nonnegative integer bounds")
    return {k: int(value[k]) for k in sorted(keys)}


def grid(radius: int) -> list[P]:
    r = range(-radius, radius + 1)
    return [(x, y) for x in r for y in r]


def exactness_report(points: list[P], coefficients: list[int]) -> dict[str, int]:
    """Dual evaluation equals value plus derivative; closed forms agree."""
    checked = 0
    for c in coefficients:
        e = central(c)
        for a, b in product(points, repeat=2):
            for v in ((1, 0), (0, 1), (2, -1)):
                rho = slots(a, b)
                tau = first(v)
                dual = evaluate_dual(lambda i: Dual(rho(i), tau(i)), e)
                if dual != Dual(evaluate(rho, e), ddir(rho, tau, e)):
                    raise AssertionError("dual evaluation is not exact")
                formula1 = (-2 * ((b[0] - a[0]) * v[0] + (b[1] - a[1]) * v[1])
                            - 2 * c * (a[0] * v[0] + a[1] * v[1]))
                formula2 = 2 * ((b[0] - a[0]) * v[0] + (b[1] - a[1]) * v[1])
                if d1(e, a, b, v) != formula1 or d2(e, a, b, v) != formula2:
                    raise AssertionError("closed-form derivative mismatch")
                checked += 1
    return {"checked": checked}


def invariance_report(points: list[P], coefficients: list[int]) -> dict[str, int]:
    def failures(e: Expr, xi: Callable[[P], P]) -> int:
        return sum(d1(e, a, b, xi(a)) + d2(e, a, b, xi(b)) != 0
                   for a, b in product(points, repeat=2))
    central_rot = sum(failures(central(c), rot) for c in coefficients)
    if central_rot:
        raise AssertionError("the central weight is not rotation invariant")
    return {"pairs": len(points) ** 2, "central_rot_failures": central_rot,
            "aniso_rot_failures": failures(ANISO, rot),
            "central0_shift_failures": failures(central(0), shift),
            "central1_shift_failures": failures(central(1), shift)}


def conservation_report(points: list[P], coefficients: list[int],
                        length: int) -> dict[str, int]:
    histories = moved = variations = 0
    for c in coefficients:
        e = central(c)
        for a, b in product(points, repeat=2):
            q = history(lambda x, y: next_point(c, x, y), a, b, length)
            charges = {charge(e, rot, q[n], q[n + 1]) for n in range(length - 1)}
            if charges != {2 * (a[0] * b[1] - a[1] * b[0])}:
                raise AssertionError("charge moved on a stationary history")
            for k in range(1, length - 1):
                for v in ((1, 0), (0, 1)):
                    if varied_action_du(e, q, k, v) != 0:
                        raise AssertionError("stationary history has nonzero variation")
                    variations += 1
            histories += 1
    for a, b in product(points, repeat=2):
        q = history(aniso_next, a, b, length)
        moved += int(len({charge(ANISO, rot, q[n], q[n + 1]) for n in range(length - 1)}) > 1)
    return {"central_histories": histories, "variations_checked": variations,
            "aniso_histories_with_moving_charge": moved}


def nonstationary_report(points: list[P]) -> dict[str, int]:
    """On arbitrary three-point histories the charge usually moves."""
    e = central(0)
    triples = moving = 0
    for a, b, d in product(points[:: max(1, len(points) // 9)], repeat=3):
        triples += 1
        moving += int(charge(e, rot, a, b) != charge(e, rot, b, d))
    return {"triples": triples, "moving": moving}


def receipt() -> Json:
    b = bounds()
    points = grid(b["grid_radius"])
    coefficients = list(range(-b["coefficient_radius"], b["coefficient_radius"] + 1))
    return {
        "authority_effect": "None",
        "bounds": dict(b),
        "points": len(points),
        "coefficients": coefficients,
        "exactness": exactness_report(points, coefficients),
        "invariance": invariance_report(points, coefficients),
        "conservation": conservation_report(points, coefficients, b["history_length"]),
        "nonstationary": nonstationary_report(points),
    }
