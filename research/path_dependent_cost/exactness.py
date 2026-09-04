"""Deciding exactness, twice, by two methods that must agree.

A cost is **exact** when some state functional `P` has it as its difference:
`w(a, i) = P(a·i) - P(a)` for every move.  Two ways to decide it over a
finite graph:

* **potentials** -- walk the graph assigning `P` and check every edge for
  consistency.  This is constructive: when it succeeds it produces the
  functional, so the answer is a witness and not a verdict;
* **circulations** -- sum the cost around each fundamental cycle and check
  they all vanish.

The two are checked against each other on every candidate.  They are the
same theorem, but they are not the same code, and the estate's own habit is
that an invariant computed twice by one method has been computed once.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass

import costs as ct
import movegraph as mg

__all__ = [
    "Verdict",
    "circulations",
    "commuting_squares",
    "decide",
    "potentials",
    "square_witness",
]


@dataclass(frozen=True)
class Verdict:
    name: str
    exact_by_potentials: bool
    exact_by_circulations: bool
    methods_agree: bool
    nonzero_self_loop_cycles: int
    nonzero_nonself_cycles: int
    reads_the_base: bool
    witness: str | None


def edge_weights(graph: mg.MoveGraph, name: str) -> list[int]:
    weight = ct.CANDIDATES[name]
    return [weight(graph.states[e.source], e.item) for e in graph.edges]


def potentials(graph: mg.MoveGraph, weights: list[int]) -> tuple[bool, str | None]:
    """Try to build the functional.  Returns whether it exists, and the
    first inconsistent edge when it does not."""

    value: dict[int, int] = {}
    adjacency: dict[int, list[tuple[int, int, int]]] = {
        i: [] for i in range(len(graph.states))
    }
    for edge in graph.edges:
        adjacency[edge.source].append((edge.target, edge.index, 1))
        adjacency[edge.target].append((edge.source, edge.index, -1))
    for start in range(len(graph.states)):
        if start in value:
            continue
        value[start] = 0
        stack = [start]
        while stack:
            here = stack.pop()
            for nxt, index, sign in adjacency[here]:
                want = value[here] + sign * weights[index]
                if nxt not in value:
                    value[nxt] = want
                    stack.append(nxt)
                elif value[nxt] != want:
                    edge = graph.edges[index]
                    return False, (
                        f"{graph.names[edge.source]} --{mg.item_kind(edge.item)}-->"
                        f" {graph.names[edge.target]} wants {want},"
                        f" already {value[nxt]}"
                    )
    return True, None


def circulations(graph: mg.MoveGraph, weights: list[int]) -> list[int]:
    """The signed sum of the cost around each fundamental cycle."""

    return [
        sum(sign * weights[index] for index, sign in cycle.signed)
        for cycle in graph.cycles
    ]


def decide(graph: mg.MoveGraph, name: str) -> Verdict:
    weights = edge_weights(graph, name)
    by_potential, witness = potentials(graph, weights)
    circ = circulations(graph, weights)
    by_circulation = all(c == 0 for c in circ)
    self_loop_hits = sum(
        1 for cycle, c in zip(graph.cycles, circ, strict=True)
        if c != 0 and cycle.is_self_loop
    )
    nonself_hits = sum(
        1 for cycle, c in zip(graph.cycles, circ, strict=True)
        if c != 0 and not cycle.is_self_loop
    )
    samples = [(graph.states[e.source], e.item) for e in graph.edges]
    return Verdict(
        name=name,
        exact_by_potentials=by_potential,
        exact_by_circulations=by_circulation,
        methods_agree=by_potential == by_circulation,
        nonzero_self_loop_cycles=self_loop_hits,
        nonzero_nonself_cycles=nonself_hits,
        reads_the_base=ct.reads_the_base(name, samples),
        witness=witness,
    )


def nonself_cycle_witness(graph: mg.MoveGraph, name: str) -> dict[str, object] | None:
    """The shortest non-self fundamental cycle with nonzero circulation.

    Its signed walk may traverse tree edges backwards.  Use `square_witness`
    when a claim requires two actual directed routes with common endpoints.
    """

    weights = edge_weights(graph, name)
    best: dict[str, object] | None = None
    for cycle, total in zip(graph.cycles, circulations(graph, weights), strict=True):
        if total == 0 or cycle.is_self_loop:
            continue
        if best is not None and len(cycle.signed) >= int(str(best["length"])):
            continue
        forward = [
            (graph.edges[i], s) for i, s in cycle.signed
        ]
        best = {
            "length": len(cycle.signed),
            "circulation": total,
            "moves": [
                (
                    graph.names[e.source],
                    mg.item_kind(e.item),
                    graph.names[e.target],
                    weights[e.index],
                    "forwards" if s > 0 else "backwards",
                )
                for e, s in forward
            ],
        }
    return best


def commuting_squares(graph: mg.MoveGraph) -> list[tuple[int, tuple[int, int], tuple[int, int]]]:
    """Every pair of two-move routes leaving one state and landing on one
    state, as (start, route, route) with edge indices.

    This is the readable form of an order cycle: not a fundamental cycle
    threaded through a spanning forest, but two routes a reader can compare
    move by move.  Deterministic order; each unordered pair once."""

    out: list[tuple[int, tuple[int, int], tuple[int, int]]] = []
    by_source: dict[int, list[mg.Edge]] = {}
    for edge in graph.edges:
        by_source.setdefault(edge.source, []).append(edge)
    for start in range(len(graph.states)):
        routes: dict[int, list[tuple[int, int]]] = {}
        for first in by_source.get(start, []):
            for second in by_source.get(first.target, []):
                routes.setdefault(second.target, []).append((first.index, second.index))
        for _, found in sorted(routes.items()):
            for i in range(len(found)):
                for j in range(i + 1, len(found)):
                    out.append((start, found[i], found[j]))
    return out


def square_witness(graph: mg.MoveGraph, name: str) -> dict[str, object] | None:
    """The first commuting square on which the candidate prices the two
    routes differently, written out move by move."""

    weights = edge_weights(graph, name)
    for start, left, right in commuting_squares(graph):
        a = weights[left[0]] + weights[left[1]]
        b = weights[right[0]] + weights[right[1]]
        if a == b:
            continue

        def leg(route: tuple[int, int]) -> list[tuple[str, int]]:
            return [(mg.item_kind(graph.edges[k].item), weights[k]) for k in route]

        return {
            "start": graph.names[start],
            "end": graph.names[graph.edges[left[1]].target],
            "route_one": leg(left),
            "route_one_total": a,
            "route_two": leg(right),
            "route_two_total": b,
        }
    return None
