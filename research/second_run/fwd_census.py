"""Continuation two: the census read off the runs.

Classification (assumption discipline):

* Metatheory apparatus over ``fwd_runs.py``.  Every reading here is the
  one ``PROMPT.md`` declares, with the readings applied that
  ``PREDICTIONS.md`` records before the first computation.
* A STAGE READING is a value at a node; its verdict at a round is decided
  over the round populations of a set of runs: FORCED (complete, one
  value), NOT FORCED (two values, both witnesses named), or UNDECIDED.
* A RUN READING is a property of a run with the outcomes HOLDS, FAILS
  (with an exported witness), HOLDS AT BOUND, or UNDECIDED, by the three
  kinds the prompt declares: EVERY RUN REACHES, NO EDGE VIOLATES and ONE
  VALUE PER NODE.  A FAILS outcome is an executable countermodel: its
  witness is a path of the run graph, every node of which replays.
* RUN-ISOMORPHISM is decided on the run graphs keyed by their node
  labels, which are pairwise distinct within a run, and cross-checked by
  an exhaustive search over node bijections on small runs.
* Nothing here is a theorem.
"""

from __future__ import annotations

import hashlib
from collections import deque
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Optional, Sequence

from fwd_runs import (
    BOUND,
    FIXPOINT,
    GUARD,
    REFUSAL,
    ROUND_BOUND,
    Edge,
    Node,
    Run,
    cyclic_edges,
    is_closed,
    sccs,
)

__all__ = [
    "FAILS",
    "HOLDS",
    "HOLDS_AT_BOUND",
    "UNDECIDED",
    "Outcome",
    "RunFacts",
    "brute_run_isomorphic",
    "every_run_reaches",
    "facts_of",
    "forced_over",
    "no_edge_violates",
    "one_value_per_node",
    "populations",
    "run_signature",
    "signature_digest",
    "stage_verdict",
    "supplementary_condensation",
]

HOLDS = "HOLDS"
FAILS = "FAILS"
HOLDS_AT_BOUND = "HOLDS_AT_BOUND"
UNDECIDED = "UNDECIDED"

Values = list[dict[str, Optional[int]]]


@dataclass(frozen=True)
class Outcome:
    """A run reading's outcome, with its witness when it FAILS."""

    status: str
    witness: tuple[Any, ...] = ()
    note: str = ""


# ---------------------------------------------------------------------------
# Paths, for witnesses
# ---------------------------------------------------------------------------


def _path_to(run: Run, target: int, allowed: Callable[[int], bool], edge_ok: Callable[[Edge], bool]) -> list[int]:
    """A shortest path of node ids from the root to ``target`` through
    allowed nodes and edges, or ``[]`` when none."""
    if not allowed(0):
        return []
    out = run.out_edges()
    previous: dict[int, int] = {0: -1}
    queue: deque[int] = deque([0])
    while queue:
        v = queue.popleft()
        if v == target:
            path = [v]
            while previous[path[-1]] != -1:
                path.append(previous[path[-1]])
            return list(reversed(path))
        for index in out[v]:
            edge = run.edges[index]
            w = edge.child
            if w in previous or not allowed(w) or not edge_ok(edge):
                continue
            previous[w] = v
            queue.append(w)
    return []


# ---------------------------------------------------------------------------
# EVERY RUN REACHES
# ---------------------------------------------------------------------------


def every_run_reaches(
    run: Run,
    node_good: Callable[[int], bool],
    edge_good: Callable[[Edge], bool],
) -> Outcome:
    """Every maximal run path takes a node or an edge with the property.

    HOLDS when every run path meets it before a BOUND or GUARD node: the
    least set W with n in W when n is good, or n was expanded, has an
    edge, and every edge out of n is good or leads into W.  FAILS when a
    path avoiding it ends at a FIXPOINT or REFUSAL node or enters a cycle
    of the graph that avoids it.  Otherwise UNDECIDED."""
    n = len(run.nodes)
    out = run.out_edges()
    good = [node_good(v) for v in range(n)]
    win = list(good)
    changed = True
    while changed:
        changed = False
        for v in range(n):
            if win[v] or not run.nodes[v].expanded or not out[v]:
                continue
            if all(edge_good(run.edges[e]) or win[run.edges[e].child] for e in out[v]):
                win[v] = True
                changed = True
    if win[0]:
        return Outcome(HOLDS)
    # The avoiding subgraph: bad nodes and bad edges between them.
    bad_edges = [
        e for e, edge in enumerate(run.edges)
        if not good[edge.parent] and not good[edge.child] and not edge_good(edge)
    ]
    succ: list[list[int]] = [[] for _ in range(n)]
    pred: list[list[int]] = [[] for _ in range(n)]
    for e in bad_edges:
        edge = run.edges[e]
        succ[edge.parent].append(edge.child)
        pred[edge.child].append(edge.parent)
    on_cycle = _cycle_nodes(n, succ)
    sinks = [
        v for v in range(n)
        if not good[v]
        and (run.nodes[v].terminal in (FIXPOINT, REFUSAL) or on_cycle[v])
    ]
    reach = [False] * n
    queue: deque[int] = deque(sinks)
    for v in sinks:
        reach[v] = True
    while queue:
        v = queue.popleft()
        for u in pred[v]:
            if not reach[u]:
                reach[u] = True
                queue.append(u)
    if reach[0]:
        best: list[int] = []
        for v in sinks:
            path = _path_to(run, v, lambda w: not good[w], lambda edge: not edge_good(edge))
            if path and (not best or len(path) < len(best)):
                best = path
        end = best[-1] if best else 0
        kind = run.nodes[end].terminal if run.nodes[end].terminal in (FIXPOINT, REFUSAL) else "cycle"
        return Outcome(FAILS, (tuple(best), kind))
    return Outcome(UNDECIDED)


def _cycle_nodes(n: int, succ: list[list[int]]) -> list[bool]:
    """The nodes lying on a cycle of the given graph."""
    comp = _components(n, succ)
    size: dict[int, int] = {}
    for c in comp:
        size[c] = size.get(c, 0) + 1
    return [
        size[comp[v]] > 1 or v in succ[v]
        for v in range(n)
    ]


def _components(n: int, succ: list[list[int]]) -> list[int]:
    fake = _FakeRun(n, succ)
    return sccs(fake)  # type: ignore[arg-type]


class _FakeRun:
    """The minimal shape ``sccs`` reads, over an arbitrary successor list."""

    def __init__(self, n: int, succ: list[list[int]]) -> None:
        self.nodes = list(range(n))
        self.edges: list[_FakeEdge] = []
        self._out: list[list[int]] = [[] for _ in range(n)]
        for v, targets in enumerate(succ):
            for w in targets:
                self._out[v].append(len(self.edges))
                self.edges.append(_FakeEdge(v, w))

    def out_edges(self) -> list[list[int]]:
        return self._out


@dataclass(frozen=True)
class _FakeEdge:
    parent: int
    child: int


# ---------------------------------------------------------------------------
# NO EDGE VIOLATES
# ---------------------------------------------------------------------------


def no_edge_violates(run: Run, violates: Callable[[int, Edge], Optional[bool]]) -> Outcome:
    """FAILS when some edge violates the condition, naming the first; HOLDS
    when none does and the run is closed; HOLDS AT BOUND when none does
    and it is not.  An edge the condition cannot read (``None``) makes the
    outcome UNDECIDED unless another edge fails."""
    unreadable = False
    for index, edge in enumerate(run.edges):
        verdict = violates(index, edge)
        if verdict is None:
            unreadable = True
            continue
        if verdict:
            path = _path_to(run, edge.parent, lambda _: True, lambda _: True)
            return Outcome(FAILS, (tuple(path), index))
    if unreadable:
        return Outcome(UNDECIDED, note="an edge the condition cannot read")
    return Outcome(HOLDS if is_closed(run) else HOLDS_AT_BOUND)


# ---------------------------------------------------------------------------
# ONE VALUE PER NODE
# ---------------------------------------------------------------------------

Transfer = Callable[[Edge, int], int]


def _effect_free(edge: Edge, transfer: Transfer) -> bool:
    return transfer(edge, 0) == 0 and transfer(edge, 1) == 1


def one_value_per_node(run: Run, transfer: Transfer) -> Outcome:
    """A quantity carried along run paths from zero at the root.

    FAILS when two run paths of at most fifteen edges bring two values to
    one node, or when a closed run has a cycle holding an edge that changes
    the quantity.  HOLDS when the run is closed and acyclic and every node
    has one value over all its paths.  HOLDS AT BOUND when no failure is
    found and the run is not closed.  A closed run with a cycle and no
    failure is UNDECIDED (the reading applied)."""
    out = run.out_edges()
    # Paths of at most fifteen edges, layer by layer.
    seen: dict[int, dict[int, tuple[int, ...]]] = {0: {0: (0,)}}
    layer: dict[tuple[int, int], tuple[int, ...]] = {(0, 0): (0,)}
    for _ in range(ROUND_BOUND):
        nxt: dict[tuple[int, int], tuple[int, ...]] = {}
        for (v, value), path in sorted(layer.items()):
            for e in out[v]:
                edge = run.edges[e]
                w = edge.child
                new = transfer(edge, value)
                if (w, new) not in nxt:
                    nxt[(w, new)] = path + (w,)
        for (w, value), path in sorted(nxt.items()):
            known = seen.setdefault(w, {})
            if value not in known:
                known[value] = path
        layer = nxt
    for w in sorted(seen):
        if len(seen[w]) > 1:
            values = sorted(seen[w])
            return Outcome(
                FAILS,
                (w, values[0], seen[w][values[0]], values[1], seen[w][values[1]]),
                "two paths",
            )
    if not is_closed(run):
        return Outcome(HOLDS_AT_BOUND)
    cyc = cyclic_edges(run)
    changing = [e for e in cyc if not _effect_free(run.edges[e], transfer)]
    if changing:
        edge = run.edges[changing[0]]
        to_cycle = _path_to(run, edge.parent, lambda _: True, lambda _: True)
        return Outcome(FAILS, (tuple(to_cycle), changing[0]), "a changing cycle")
    if cyc:
        return Outcome(UNDECIDED, note="closed with a cycle that changes nothing")
    exact = _dag_values(run, transfer)
    for w, received in enumerate(exact):
        if len(received) > 1:
            ordered = sorted(received)
            return Outcome(FAILS, (w, ordered[0], (), ordered[1], ()), "two paths beyond fifteen")
    return Outcome(HOLDS)


def _topological(run: Run, succ: list[list[int]]) -> list[int]:
    indegree = [0] * len(run.nodes)
    for targets in succ:
        for w in targets:
            indegree[w] += 1
    queue: deque[int] = deque(v for v in range(len(run.nodes)) if indegree[v] == 0)
    order: list[int] = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for w in succ[v]:
            indegree[w] -= 1
            if indegree[w] == 0:
                queue.append(w)
    return order


def _dag_values(run: Run, transfer: Transfer) -> list[set[int]]:
    """Every value each node receives over every path of an acyclic run."""
    out = run.out_edges()
    succ = [[run.edges[e].child for e in out[v]] for v in range(len(run.nodes))]
    values: list[set[int]] = [set() for _ in run.nodes]
    values[0].add(0)
    for v in _topological(run, succ):
        for e in out[v]:
            edge = run.edges[e]
            for value in values[v]:
                values[edge.child].add(transfer(edge, value))
    return values


def supplementary_condensation(run: Run, transfer: Transfer) -> Optional[bool]:
    """Reported beside an UNDECIDED closed cyclic run, never as a verdict:
    whether, when every cycle changes nothing, each node receives one value
    over every path.  ``None`` when the run is not closed or some cycle
    changes the quantity."""
    if not is_closed(run):
        return None
    comp = sccs(run)
    for edge in run.edges:
        if comp[edge.parent] == comp[edge.child] and not _effect_free(edge, transfer):
            return None
    count = max(comp) + 1 if comp else 0
    succ: list[set[int]] = [set() for _ in range(count)]
    for edge in run.edges:
        if comp[edge.parent] != comp[edge.child]:
            succ[comp[edge.parent]].add(comp[edge.child])
    indegree = [0] * count
    for targets in succ:
        for w in targets:
            indegree[w] += 1
    values: list[set[int]] = [set() for _ in range(count)]
    values[comp[0]].add(0)
    queue: deque[int] = deque(c for c in range(count) if indegree[c] == 0)
    by_comp: dict[int, list[Edge]] = {}
    for edge in run.edges:
        if comp[edge.parent] != comp[edge.child]:
            by_comp.setdefault(comp[edge.parent], []).append(edge)
    while queue:
        c = queue.popleft()
        for edge in by_comp.get(c, []):
            for value in values[c]:
                values[comp[edge.child]].add(transfer(edge, value))
        for w in succ[c]:
            indegree[w] -= 1
            if indegree[w] == 0:
                queue.append(w)
    return all(len(v) <= 1 for v in values)


# ---------------------------------------------------------------------------
# Round populations and stage verdicts
# ---------------------------------------------------------------------------


def populations(run: Run) -> list[tuple[frozenset[int], bool]]:
    """The round population at every round from zero to fifteen, with
    whether it is complete: no node at the end of a shorter run path is a
    BOUND or GUARD node."""
    out = run.out_edges()
    current: frozenset[int] = frozenset({0})
    seen_before: set[int] = set()
    result: list[tuple[frozenset[int], bool]] = []
    for _ in range(ROUND_BOUND + 1):
        complete = not any(run.nodes[v].terminal in (BOUND, GUARD) for v in seen_before)
        result.append((current, complete))
        seen_before |= current
        nxt: set[int] = set()
        for v in current:
            if run.nodes[v].terminal in (FIXPOINT, REFUSAL):
                nxt.add(v)
            for e in out[v]:
                nxt.add(run.edges[e].child)
        current = frozenset(nxt)
    return result


@dataclass
class RunFacts:
    """What the census needs of one run: its populations and values."""

    engine: str
    reading: str
    populations: list[tuple[frozenset[int], bool]]
    values: Values


def facts_of(run: Run, values: Values) -> RunFacts:
    return RunFacts(run.engine.name, run.reading, populations(run), values)


def stage_verdict(facts: Sequence[RunFacts], reading_name: str, round_k: int) -> dict[str, Any]:
    """FORCED, NOT FORCED or UNDECIDED at one round over a set of runs.

    NOT FORCED is decided by two nodes carrying two values, both named,
    whatever the completeness.  FORCED needs every population complete and
    one value at every node, every node having one."""
    reference: Optional[tuple[str, str, int, int]] = None
    complete = True
    missing = False
    for fact in facts:
        population, is_complete = fact.populations[round_k]
        complete = complete and is_complete
        for node in sorted(population):
            value = fact.values[node][reading_name]
            if value is None:
                missing = True
                continue
            if reference is None:
                reference = (fact.engine, fact.reading, node, value)
            elif value != reference[3]:
                return {
                    "verdict": "NOT_FORCED",
                    "witnesses": [
                        list(reference),
                        [fact.engine, fact.reading, node, value],
                    ],
                }
    if complete and not missing and reference is not None:
        return {"verdict": "FORCED", "value": reference[3]}
    return {"verdict": "UNDECIDED"}


def forced_over(outcomes: Iterable[tuple[str, str, Outcome]]) -> dict[str, Any]:
    """A run reading over a set of engines, from the outcomes of every run
    of every member, in class order and reading order."""
    listed = list(outcomes)
    for engine, reading, outcome in listed:
        if outcome.status == FAILS:
            return {
                "verdict": "NOT_FORCED",
                "first_failing": [engine, reading],
                "witness": _jsonable(outcome.witness),
                "note": outcome.note,
            }
    statuses = [outcome.status for _, _, outcome in listed]
    if statuses and all(s == HOLDS for s in statuses):
        return {"verdict": "FORCED"}
    if statuses and all(s in (HOLDS, HOLDS_AT_BOUND) for s in statuses):
        return {"verdict": "FORCED_AT_BOUND", "at_bound": statuses.count(HOLDS_AT_BOUND)}
    return {"verdict": "OPEN", "undecided": statuses.count(UNDECIDED)}


def _jsonable(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


# ---------------------------------------------------------------------------
# Run-isomorphism
# ---------------------------------------------------------------------------


def _node_label(node: Node) -> str:
    return repr((node.key, node.terminal or None))


def _edge_label(edge: Edge) -> tuple[str, str, tuple[int, ...]]:
    return (edge.kind, edge.demand_kind, tuple(edge.cost))


def run_signature(run: Run) -> tuple[Any, ...]:
    """The run graph keyed by its node labels: the root's label, the sorted
    node labels, and the sorted labelled edges with their counts."""
    labels = [_node_label(node) for node in run.nodes]
    counts: dict[tuple[str, str, tuple[str, str, tuple[int, ...]]], int] = {}
    for edge in run.edges:
        key = (labels[edge.parent], labels[edge.child], _edge_label(edge))
        counts[key] = counts.get(key, 0) + 1
    return (labels[0], tuple(sorted(labels)), tuple(sorted(counts.items())))


def signature_digest(signature: tuple[Any, ...]) -> str:
    return hashlib.sha256(repr(signature).encode("utf-8")).hexdigest()


def brute_run_isomorphic(left: Run, right: Run) -> bool:
    """Exhaustive search over node bijections preserving the root, the node
    labels, and the multiset of labelled edges between every two nodes.
    It never compares signatures."""
    a, b = left.nodes, right.nodes
    if len(a) != len(b) or len(left.edges) != len(right.edges):
        return False

    def edge_table(run: Run) -> dict[tuple[int, int], list[tuple[str, str, tuple[int, ...]]]]:
        table: dict[tuple[int, int], list[tuple[str, str, tuple[int, ...]]]] = {}
        for edge in run.edges:
            table.setdefault((edge.parent, edge.child), []).append(_edge_label(edge))
        for key in table:
            table[key].sort()
        return table

    ta, tb = edge_table(left), edge_table(right)
    la = [_node_label(node) for node in a]
    lb = [_node_label(node) for node in b]
    image = [-1] * len(a)
    used = [False] * len(b)

    def consistent(v: int) -> bool:
        for u in range(len(a)):
            if image[u] == -1:
                continue
            if ta.get((u, v), []) != tb.get((image[u], image[v]), []):
                return False
            if ta.get((v, u), []) != tb.get((image[v], image[u]), []):
                return False
        return True

    def extend(v: int) -> bool:
        if v == len(a):
            return True
        for w in range(len(b)):
            if used[w] or la[v] != lb[w] or (v == 0) != (w == 0):
                continue
            image[v] = w
            used[w] = True
            if consistent(v) and extend(v + 1):
                return True
            image[v] = -1
            used[w] = False
        return False

    return extend(0)
