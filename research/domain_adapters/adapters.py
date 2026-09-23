"""Exact finite mirror of the domain adapters.

AuthorityEffect: None.  Consumes the sealed passage step, the
``native_bridge`` tree's core, and the ``conservation_ladder`` tree's
integer step read-only.  Every check runs over the declared bounds in
``input.json``; the general statements are the Lean theorems named in
``CLAIMS.md``.
"""

from __future__ import annotations

from dataclasses import replace
from itertools import product
import json
from pathlib import Path

from bridge import alphabet, core, reachable
from derivation.primitive_passage import GENESIS_P, PS, PEvent, preplay, pstep
from derivation.trace_algebra import named_states
from ladder import next_point

Json = dict[str, object]
Vec = tuple[int, int]
P = tuple[int, int]


def bounds() -> dict[str, int]:
    value = json.loads((Path(__file__).resolve().parent / "input.json")
                       .read_text(encoding="utf-8"))
    keys = {"counter_bound", "grid_radius", "battery_depth"}
    if (not isinstance(value, dict) or set(value) != keys
            or not all(isinstance(value[k], int) and not isinstance(value[k], bool)
                       and value[k] >= 0 for k in keys)):
        raise ValueError("input.json: expected three nonnegative integer bounds")
    return {k: int(value[k]) for k in sorted(keys)}


def counter_enc(n: int) -> PS:
    return replace(GENESIS_P, occ=tuple(range(n)))


def counter_report(bound: int) -> Json:
    for n in range(bound):
        if pstep(counter_enc(n), ("admitOcc", n)) != counter_enc(n + 1):
            raise AssertionError(f"counter square fails at {n}")
    cores = {core(counter_enc(n)) for n in range(bound + 1)}
    if len(cores) != bound + 1:
        raise AssertionError("counter encoding is not injective on the core")
    return {"squares": bound, "distinct_cores": len(cores)}


def h_step(v: Vec) -> Vec:
    """The matrix with rows (0, 1) and (1, 0) over the two-element field."""
    return (v[1], v[0])


def vec_code(v: Vec) -> int:
    return v[0] + 2 * v[1]


def quantum_report() -> Json:
    vectors = [(x, z) for x in (0, 1) for z in (0, 1)]
    if any(h_step(h_step(v)) != v for v in vectors):
        raise AssertionError("the matrix is not an involution")
    squares = 0
    for v in vectors:
        if preplay([("setBudget", vec_code(h_step(v)))], PS(budget=vec_code(v))) != \
                PS(budget=vec_code(h_step(v))):
            raise AssertionError("budget square fails")
        squares += 1
    encodings = {PS(budget=vec_code(v)) for v in vectors}
    return {"vectors": len(vectors), "moved": sum(h_step(v) != v for v in vectors),
            "budget_squares": squares, "distinct_encodings": len(encodings),
            "distinct_cores": len({core(p) for p in encodings})}


def tick(c: int, st: tuple[P, P]) -> tuple[P, P]:
    return (st[1], next_point(c, st[0], st[1]))


def mechanics_report(radius: int) -> Json:
    r = range(-radius, radius + 1)
    points = [(x, y) for x in r for y in r]
    moved = 0
    for a, b in product(points, repeat=2):
        st = (a, b)
        if tick(2, tick(2, tick(2, tick(2, st)))) != st:
            raise AssertionError("coefficient two does not have period four")
        moved += int(tick(2, st) != st)
    return {"pairs": len(points) ** 2, "moved": moved}


def pl_events(kind: str, arg: object) -> list[PEvent]:
    if kind == "propose":
        return []
    if kind == "grant":
        return [("setLicense", arg)]
    return [("addCol", arg)]


def license_report(states: list[PS]) -> Json:
    columns: list[tuple[int, ...]] = [(0,), (1,), (0, 1)]
    inert_proposals = gated = applied = 0
    for s in states:
        for c in columns:
            if preplay(pl_events("propose", c), s) != s:
                raise AssertionError("a proposal changed the state")
            inert_proposals += 1
            t = preplay(pl_events("apply", c), s)
            if not s.halted and (not s.licensed or s.budget == 0):
                if t != s:
                    raise AssertionError("an unlicensed or unfunded apply acted")
                gated += 1
            applied += int(t != s)
    return {"states": len(states), "inert_proposals": inert_proposals,
            "gated_applies": gated, "acting_applies": applied}


def receipt() -> Json:
    b = bounds()
    states = reachable(b["battery_depth"], alphabet(), named_states())
    return {
        "authority_effect": "None",
        "bounds": dict(b),
        "counter": counter_report(b["counter_bound"]),
        "quantum": quantum_report(),
        "mechanics": mechanics_report(b["grid_radius"]),
        "license": license_report(states),
    }
