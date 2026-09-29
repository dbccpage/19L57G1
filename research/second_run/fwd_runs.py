"""Continuation two: the run of every engine of the declared class.

Classification (assumption discipline):

* Everything here is metatheory apparatus layered on continuation one's
  declarations (``research/second_engine/engine_decl.py`` and
  ``engine_probe.py``), the sealed kernel, key procedure and
  automorphisms, rung two track two's profile class count
  (``research/second_stake/observables.py``) and rung ten's readings
  (``research/second_response/response_rows.py``), all imported read-only
  through their public functions and pinned by blob in
  ``SOURCE_MANIFEST.json``.  No sibling source is copied.
* THE RUN of an engine at a reading is the graph ``PROMPT.md`` declares:
  built breadth-first from the genesis state, a node a class of states
  under equal sealed keys and equal modes, every tied minimum and every
  enabled continuation one edge, fifteen rounds, a node guard of two
  hundred and fifty.  It is a FINITE COMPUTATION.
* A DEMAND is read off the state by the generator; no event emits it.  A
  RESPONSE is a model proposal until its admission events are replayed,
  which :func:`replay_mismatches` does for every node and edge.
* At every MERGE the generator's labels are compared across the sealed
  isomorphism witness; a disagreement is a QUOTIENT DEFECT and is
  counted, never repaired.
* Nothing here is a theorem.  The theorems of this tree are in ``lean/``.
"""

from __future__ import annotations

import pathlib
import sys
from collections import deque
from dataclasses import dataclass, field
from typing import Optional, Sequence

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_ENGINE_TREE = str(REPO / "research" / "second_engine")
_RESPONSE_TREE = str(REPO / "research" / "second_response")
for _tree in (_RESPONSE_TREE, _ENGINE_TREE):
    if _tree not in sys.path:
        sys.path.insert(0, _tree)

# Continuation one's module puts the sealed kernel and rung two's, rung
# one's and the two-sided tree on the path and its own tree at the front;
# rung ten's puts rungs three and four there and its own tree at the front.
# Each of those trees carries modules named `verify_pins`, `check_coverage`
# and `test_*`, so this tree goes back to the front AFTER the imports, or a
# sibling's module is silently loaded in place of this tree's -- the defect
# rung three found live and every later tree recorded.
from engine_decl import (  # noqa: E402
    Engine,
    EngineEvent,
    EState,
    SwitchMarker,
    Target,
    engine_class,
    engine_replay,
    growth_events,
    honoured_before,
    least_responses,
    moded_rule,
    response_events,
    state_demands,
)
from engine_probe import enabled_continuations, readings  # noqa: E402
from observables import ObservableGuardError, class_count  # noqa: E402
from rules import label_of  # noqa: E402
from response_rows import exhausted_count, holds_two, moved_pairs  # noqa: E402
from derivation.candidates import Delta, NewDatum  # noqa: E402
from derivation.engine import Reading  # noqa: E402
from derivation.iso import IsoBudgetError, automorphisms, canonical, find_iso  # noqa: E402
from derivation.model import AdmissionError, Pair, Regime, replay  # noqa: E402

sys.path[:] = [str(HERE)] + [entry for entry in sys.path if entry != str(HERE)]

__all__ = [
    "BOUND",
    "FIXPOINT",
    "GUARD",
    "NODE_GUARD",
    "PERM_BUDGET",
    "REFUSAL",
    "ROUND_BOUND",
    "TERMINALS",
    "Edge",
    "Node",
    "Run",
    "all_runs",
    "build_run",
    "carries_forward",
    "closure_kind",
    "cyclic_edges",
    "elements",
    "frontier",
    "is_closed",
    "node_values",
    "replay_mismatches",
    "run_readings",
    "sccs",
    "state_key",
]

ROUND_BOUND = 15
NODE_GUARD = 250
PERM_BUDGET = 100_000

FIXPOINT = "FIXPOINT"
REFUSAL = "REFUSAL"
BOUND = "BOUND"
GUARD = "GUARD"
TERMINALS: tuple[str, ...] = (FIXPOINT, REFUSAL, BOUND, GUARD)

StateKey = tuple[object, str]


def elements(regime: Regime) -> int:
    """The element count: data plus the lengths of the four lists."""
    return (
        regime.n_data()
        + len(regime.forms)
        + len(regime.insts)
        + len(regime.rules)
        + len(regime.reqs)
    )


def state_key(state: EState) -> StateKey:
    """The state relation: the sealed key of the regime and the mode.
    Raises ``IsoBudgetError`` when the sealed key procedure exceeds its
    permutation budget."""
    return (canonical(state.regime, PERM_BUDGET), state.mode)


@dataclass
class Node:
    node_id: int
    stage: int
    history: tuple[EngineEvent, ...]
    state: EState
    key: StateKey
    demands: tuple[Target, ...]
    budget_guard: str = ""
    terminal: str = ""
    expanded: bool = False
    refused: tuple[Target, ...] = ()


@dataclass
class Edge:
    parent: int
    child: int
    kind: str
    demand_kind: str
    pair: Optional[Pair]
    delta: Delta
    cost: tuple[int, ...]
    events: tuple[EngineEvent, ...]
    after: Regime
    merge: bool
    changing: bool
    datum_round: bool
    carries_datum: bool
    moved: tuple[tuple[Pair, bool], ...]


@dataclass
class Run:
    engine: Engine
    reading: str
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    merges: int = 0
    quotient_defects: list[str] = field(default_factory=list)
    unchecked_merges: list[str] = field(default_factory=list)

    def out_edges(self) -> list[list[int]]:
        table: list[list[int]] = [[] for _ in self.nodes]
        for index, edge in enumerate(self.edges):
            table[edge.parent].append(index)
        return table


def _demands(rule_name: str, state: EState) -> tuple[tuple[Target, ...], str]:
    try:
        return state_demands(rule_name, state), ""
    except ObservableGuardError as exc:
        return (), f"observable budget: {exc}"


def _label_defects(
    rule_name: str,
    mode: str,
    after: Regime,
    representative: Regime,
) -> list[str]:
    """Compare the generator's label of every pair of ``after`` with the
    label of its witnessed image in ``representative``."""
    witness = find_iso(after, representative, PERM_BUDGET)
    if witness is None:
        return ["no isomorphism witness for a merge"]
    dmap, _ = witness
    rule = moded_rule(rule_name, mode)
    out: list[str] = []
    n = after.n_data()
    for i in range(n):
        for j in range(i + 1, n):
            a, b = sorted((dmap[i], dmap[j]))
            here = label_of(rule, after, i, j)
            there = label_of(rule, representative, a, b)
            if here != there:
                out.append(f"pair ({i}, {j}) reads {here} but its image ({a}, {b}) reads {there}")
    return out


def build_run(
    engine: Engine,
    reading: Reading,
    *,
    round_bound: int = ROUND_BOUND,
    node_guard: int = NODE_GUARD,
) -> Run:
    """Build the run of one engine at one reading, as ``PROMPT.md``
    declares it."""
    run = Run(engine, reading.name)
    root_history: tuple[EngineEvent, ...] = tuple(reading.genesis)
    root_state = engine_replay(root_history)
    index: dict[StateKey, int] = {}

    def new_node(history: tuple[EngineEvent, ...], state: EState, stage: int) -> int:
        node_id = len(run.nodes)
        guard = ""
        try:
            key: StateKey = state_key(state)
        except IsoBudgetError as exc:
            key = (("budget", node_id), state.mode)
            guard = f"key budget: {exc}"
        demands, observable_guard = _demands(engine.rule, state)
        run.nodes.append(
            Node(node_id, stage, history, state, key, demands, guard or observable_guard)
        )
        if not guard:
            index[key] = node_id
        return node_id

    new_node(root_history, root_state, 0)
    queue: deque[int] = deque([0])

    def attach(
        parent: Node,
        kind: str,
        demand_kind: str,
        pair: Optional[Pair],
        delta: Delta,
        cost: tuple[int, ...],
        events: tuple[EngineEvent, ...],
    ) -> None:
        if kind == "switch":
            after = parent.state.regime
            mode = "flipped" if parent.state.mode == "plain" else "plain"
        else:
            after = replay([event for event in events if not isinstance(event, SwitchMarker)], parent.state.regime)
            mode = parent.state.mode
        state = EState(after, mode)
        try:
            key: Optional[StateKey] = state_key(state)
        except IsoBudgetError:
            key = None
        merge = key is not None and key in index
        if merge:
            assert key is not None
            child = index[key]
            run.merges += 1
            where = f"{engine.name}@{reading.name}: edge {len(run.edges)} into node {child}"
            try:
                defects = _label_defects(engine.rule, mode, after, run.nodes[child].state.regime)
            except (ObservableGuardError, IsoBudgetError) as exc:
                run.unchecked_merges.append(f"{where}: {exc}")
                defects = []
            for defect in defects:
                run.quotient_defects.append(f"{where}: {defect}")
        else:
            child = new_node(parent.history + events, state, parent.stage + 1)
            queue.append(child)
        run.edges.append(
            Edge(
                parent.node_id,
                child,
                kind,
                demand_kind,
                pair,
                delta,
                cost,
                events,
                after,
                merge,
                after != parent.state.regime,
                after.n_data() > parent.state.regime.n_data(),
                any(isinstance(item, NewDatum) for item in delta),
                moved_pairs(parent.state.regime, after),
            )
        )

    while queue:
        node = run.nodes[queue.popleft()]
        enabled = enabled_continuations(engine, node.state)
        if not node.budget_guard and not node.demands and not enabled:
            node.terminal = FIXPOINT
            continue
        if node.stage >= round_bound:
            node.terminal = BOUND
            continue
        if node.budget_guard or len(run.nodes) >= node_guard:
            node.terminal = GUARD
            continue
        node.expanded = True
        if node.demands:
            rule = moded_rule(engine.rule, node.state.mode)
            refused: list[Target] = []
            for target in node.demands:
                found = least_responses(node.state.regime, rule, target, engine.validity)
                if found is None:
                    refused.append(target)
                    continue
                chosen = found[engine.measure]
                for delta in chosen.deltas:
                    attach(
                        node,
                        "response",
                        target[0],
                        target[1],
                        delta,
                        chosen.cost,
                        response_events(node.state.regime, delta),
                    )
            node.refused = tuple(refused)
            if len(refused) == len(node.demands):
                node.terminal = REFUSAL
        else:
            for rule_name in enabled:
                if rule_name == "growth":
                    attach(node, "growth", "", None, (), (), growth_events(node.state.regime))
                else:
                    attach(node, "switch", "", None, (), (), (SwitchMarker(),))
    return run


# ---------------------------------------------------------------------------
# Replay
# ---------------------------------------------------------------------------


def replay_mismatches(run: Run) -> list[str]:
    """Every node whose history does not replay to its representative, and
    every edge whose events do not replay from its parent's representative
    to a state of its child node."""
    where = f"{run.engine.name}@{run.reading}"
    out: list[str] = []
    for node in run.nodes:
        try:
            replayed = engine_replay(node.history)
        except AdmissionError as exc:
            out.append(f"{where}: node {node.node_id} does not replay: {exc}")
            continue
        if replayed != node.state:
            out.append(f"{where}: node {node.node_id}")
    for number, edge in enumerate(run.edges):
        parent = run.nodes[edge.parent]
        child = run.nodes[edge.child]
        try:
            state = engine_replay(parent.history + edge.events)
        except AdmissionError as exc:
            out.append(f"{where}: edge {number} does not replay: {exc}")
            continue
        if state.regime != edge.after:
            out.append(f"{where}: edge {number} reaches another regime")
            continue
        try:
            same = state_key(state) == child.key
        except IsoBudgetError:
            same = False
        if not same:
            out.append(f"{where}: edge {number} does not reach its child node")
    return out


# ---------------------------------------------------------------------------
# Shape: closure, cycles, frontier
# ---------------------------------------------------------------------------


def sccs(run: Run) -> list[int]:
    """The strongly connected component of every node (an index per
    node), by an iterative Tarjan search over the run's edges."""
    succ = [[run.edges[e].child for e in out] for out in run.out_edges()]
    n = len(run.nodes)
    number = [-1] * n
    low = [0] * n
    comp = [-1] * n
    on_stack = [False] * n
    stack: list[int] = []
    counter = 0
    components = 0
    for start in range(n):
        if number[start] != -1:
            continue
        work: list[tuple[int, int]] = [(start, 0)]
        number[start] = low[start] = counter
        counter += 1
        stack.append(start)
        on_stack[start] = True
        while work:
            v, i = work[-1]
            if i < len(succ[v]):
                work[-1] = (v, i + 1)
                w = succ[v][i]
                if number[w] == -1:
                    number[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack[w] = True
                    work.append((w, 0))
                elif on_stack[w]:
                    low[v] = min(low[v], number[w])
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[v])
            if low[v] == number[v]:
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    comp[w] = components
                    if w == v:
                        break
                components += 1
    return comp


def cyclic_edges(run: Run) -> list[int]:
    """Every edge lying on a cycle: its two ends in one component."""
    comp = sccs(run)
    return [
        index
        for index, edge in enumerate(run.edges)
        if comp[edge.parent] == comp[edge.child]
    ]


def frontier(run: Run) -> list[Node]:
    return [node for node in run.nodes if node.terminal in (BOUND, GUARD)]


def is_closed(run: Run) -> bool:
    return not frontier(run)


def closure_kind(run: Run) -> str:
    """TERMINATES, CYCLES, or NOT_CLOSED."""
    if not is_closed(run):
        return "NOT_CLOSED"
    return "CYCLES" if cyclic_edges(run) else "TERMINATES"


def carries_forward(run: Run) -> bool:
    """Not closed, and the history of every BOUND or GUARD node's
    representative holds no switch marker (the reading applied)."""
    nodes = frontier(run)
    return bool(nodes) and all(
        not any(isinstance(event, SwitchMarker) for event in node.history) for node in nodes
    )


# ---------------------------------------------------------------------------
# Values read at a node
# ---------------------------------------------------------------------------


def _automorphism_count(regime: Regime) -> Optional[int]:
    try:
        return len(automorphisms(regime, PERM_BUDGET))
    except IsoBudgetError:
        return None


def node_values(run: Run) -> list[dict[str, Optional[int]]]:
    """The stage readings and invariant candidates at every node, read off
    its representative (and, for branching, off the run)."""
    out_edges = run.out_edges()
    rule_name = run.engine.rule
    values: list[dict[str, Optional[int]]] = []
    for node in run.nodes:
        regime = node.state.regime
        if node.terminal in (FIXPOINT, REFUSAL):
            branching: Optional[int] = 0
        elif node.terminal in (BOUND, GUARD):
            branching = None
        else:
            branching = len({run.edges[e].child for e in out_edges[node.node_id]})
        guarded = bool(node.budget_guard)
        values.append(
            {
                "two": int(holds_two(regime)),
                "classes": class_count(regime),
                "symmetry": _automorphism_count(regime),
                "branching": branching,
                "exhausted": exhausted_count(regime),
                "elements": elements(regime),
                "data": regime.n_data(),
                "forms": len(regime.forms),
                "insts": len(regime.insts),
                "rules": len(regime.rules),
                "demands": None if guarded else len(node.demands),
                "honoured": None if guarded else len(honoured_before(rule_name, node.state)),
            }
        )
    return values


def run_readings() -> tuple[Reading, ...]:
    return readings()


def all_runs(engines: Sequence[Engine] = ()) -> dict[tuple[str, str], Run]:
    """Every run of the given engines (the class when none are given), at
    both readings, in class order and reading order."""
    pool = tuple(engines) or engine_class()
    return {
        (engine.name, reading.name): build_run(engine, reading)
        for engine in pool
        for reading in run_readings()
    }

