"""An instrumented section-decider and summation meter, against a declared budget.

The decider computes parity potentials over a two-label configuration graph
and checks every hop -- the fixed-pair criterion decided -- counting its
elementary steps.  The declared budget is LINEAR: ``steps <= 60 * (V + E)``.
The summation meter enumerates closed walks up to a declared length with
the same step accounting.  The pre-registered claims (STATUS.md, BC3): the
decider fits the declared budget on every fixture, across refinement
rounds and re-presentations; the meter does not, and grows by a factor
above two per added length two.  Deterministic, standard library only.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from collections import deque
from typing import Sequence

import holonomy_fixture as two
import refinement as rf
import representation as rp

Node = object
HopEdge = tuple[tuple[Node, Node], bool]

BUDGET_FACTOR = 60


class Meter:
    def __init__(self) -> None:
        self.steps = 0

    def tick(self, n: int = 1) -> None:
        self.steps += n


def decide_section_steps(objs: Sequence[Node], hops: Sequence[HopEdge]) -> tuple[bool, int]:
    """The fixed-pair criterion for a two-label family, with step accounting:
    one tick per neighbour insertion, per queue operation, and per hop check."""

    meter = Meter()
    nbrs: dict[Node, list[tuple[Node, bool]]] = {}
    for o in objs:
        meter.tick()
        nbrs[o] = []
    for (a, b), flip in hops:
        meter.tick(2)
        nbrs[a].append((b, flip))
        nbrs[b].append((a, flip))
    parity: dict[Node, int] = {}
    for base in objs:
        meter.tick()
        if base in parity:
            continue
        parity[base] = 0
        queue: deque[Node] = deque([base])
        while queue:
            meter.tick()
            x = queue.popleft()
            for y, flip in nbrs[x]:
                meter.tick()
                if y not in parity:
                    parity[y] = parity[x] ^ int(flip)
                    queue.append(y)
    ok = True
    for (a, b), flip in hops:
        meter.tick()
        if (parity[a] ^ int(flip)) != parity[b]:
            ok = False
    return ok, meter.steps


def sum_meter_steps(objs: Sequence[Node], hops: Sequence[HopEdge], max_len: int) -> tuple[int, int]:
    """Closed walks at the least object up to ``max_len``, with one tick per
    traversal step taken; returns (walk count, steps)."""

    meter = Meter()
    nbrs: dict[Node, list[Node]] = {o: [] for o in objs}
    for (a, b), _ in hops:
        nbrs[a].append(b)
        nbrs[b].append(a)
    for lst in nbrs.values():
        lst.sort(key=repr)
    base = sorted(objs, key=repr)[0]

    def go(at: Node, remaining: int) -> int:
        meter.tick()
        total = 1 if at == base else 0
        if remaining == 0:
            return total
        return total + sum(go(nxt, remaining - 1) for nxt in nbrs[at])

    count = go(base, max_len)
    return count, meter.steps


def instances() -> list[tuple[str, list[Node], list[HopEdge], bool]]:
    """(name, objects, hops, expected section) across fixtures, refinement
    rounds, and one nontrivial pointwise re-presentation each."""

    out: list[tuple[str, list[Node], list[HopEdge], bool]] = []
    for name, sites, edges in two.fixtures():
        if sites > 6:
            continue
        objs: list[Node] = list(two.configurations(sites))
        hops: list[HopEdge] = [
            ((a, b), flip) for (a, b), flip in rp.undirected_hops(sites, edges)
        ]
        expected = rp.components_even(objs, hops)[0]  # type: ignore[arg-type]
        for level in range(3):
            out.append((f"{name}_r{level}", list(objs), list(hops), expected))
            if objs:
                flipped = objs[0]
                conj = [
                    ((a, b), bool(int(flip) ^ int(a == flipped) ^ int(b == flipped)))
                    for (a, b), flip in hops
                ]
                out.append((f"{name}_r{level}_repres", list(objs), conj, expected))
            objs, hops = rf.subdivide(objs, hops)
    return out


def report() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for name, objs, hops, expected in instances():
        ok, steps = decide_section_steps(objs, hops)
        size = len(objs) + len(hops)
        rows.append(
            {
                "name": name,
                "V_plus_E": size,
                "steps": steps,
                "budget": BUDGET_FACTOR * size,
                "within_budget": steps <= BUDGET_FACTOR * size,
                "section_exists": ok,
                "verdict_matches": ok == expected,
            }
        )
    square_objs: list[Node] = list(two.configurations(4))
    square_hops: list[HopEdge] = [
        ((a, b), flip) for (a, b), flip in rp.undirected_hops(4, two.grid(2, 2))
    ]
    size = len(square_objs) + len(square_hops)
    meter_rows: list[dict[str, object]] = []
    for length in (2, 4, 6, 8):
        count, steps = sum_meter_steps(square_objs, square_hops, length)
        meter_rows.append(
            {
                "max_len": length,
                "closed_walks": count,
                "steps": steps,
                "linear_budget": BUDGET_FACTOR * size,
                "within_budget": steps <= BUDGET_FACTOR * size,
            }
        )
    growth = [
        round(meter_rows[i + 1]["steps"] / meter_rows[i]["steps"], 2)  # type: ignore[operator]
        for i in range(len(meter_rows) - 1)
    ]
    return {
        "budget": f"steps <= {BUDGET_FACTOR} * (V + E), declared before the run",
        "decider": rows,
        "decider_all_within_budget": all(r["within_budget"] for r in rows),
        "decider_all_verdicts_match": all(r["verdict_matches"] for r in rows),
        "sum_meter_square": meter_rows,
        "sum_meter_growth_factors": growth,
    }
