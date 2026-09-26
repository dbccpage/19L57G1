"""Continuation one: the probe of every engine of the declared class.

Classification (assumption discipline):

* Metatheory apparatus over ``engine_decl.py`` and the sealed kernel,
  genesis readings and key procedure, imported read-only.
* THE PROBE of an engine at a reading is the one ``PROMPT.md`` declares:
  the root is the genesis state; at level one a root with demands is
  answered -- every demand, every tied minimum, one edge each -- and a
  demand-free root fires every enabled continuation rule, one edge each;
  at level two the demands of every level-one state are read, and at a
  level-one state reached by a continuation edge every demand is
  answered too and the enabled continuations are named.  Nothing beyond
  level two is built.  It is a FINITE COMPUTATION, and it runs no engine
  forward: that is challenge four's.
* Every node replays from genesis by the engine's replay rule, and every
  edge is checked to hold only the events of the capability it is
  attributed to.
* PROBE-ISOMORPHISM is the rooted labelled-tree isomorphism of
  ``PROMPT.md``.  It is decided by comparing signatures, and the decision
  is cross-checked against an exhaustive search over the bijections of
  the level-one states.
* Nothing here is a theorem.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Optional, Sequence

from engine_decl import (
    BOUNDS,
    MAX_DATA,
    EState,
    Engine,
    EngineEvent,
    Minima,
    SwitchMarker,
    Target,
    engine_replay,
    growth_events,
    least_responses,
    moded_rule,
    response_events,
    state_demands,
)
from generation import minimum_responses as rung_two_minimum_responses
from derivation.candidates import Delta, NewDatum, NewForm, NewInst, NewRuleAll
from derivation.engine import READINGS, Reading
from derivation.iso import canonical, canonical_bruteforce
from derivation.model import AdmitDatum, Impose, Pair, Regime, Supply

__all__ = [
    "DemandAnswer",
    "PEdge",
    "PNode",
    "Probe",
    "attribution_violations",
    "brute_isomorphic",
    "build_probe",
    "delta_json",
    "edge_label",
    "enabled_continuations",
    "event_json",
    "key_brute_disagreements",
    "node_label",
    "probe_payload",
    "probe_signature",
    "readings",
    "replay_mismatches",
    "responder_crosscheck",
    "signature_digest",
]

Label = tuple[Any, ...]


def readings() -> tuple[Reading, ...]:
    return tuple(READINGS)


@dataclass(frozen=True)
class DemandAnswer:
    """One demand and what the responder did with it."""

    kind: str
    pair: Pair
    answered: bool
    cost: Optional[tuple[int, ...]]
    ties: int


@dataclass
class PNode:
    node_id: int
    level: int
    history: tuple[EngineEvent, ...]
    state: EState
    demands: tuple[Target, ...]
    via: str
    answers: Optional[tuple[DemandAnswer, ...]] = None
    enabled: Optional[tuple[str, ...]] = None


@dataclass
class PEdge:
    parent: int
    child: int
    kind: str
    demand_kind: str
    pair: Optional[Pair]
    delta: Delta
    cost: tuple[int, ...]
    events: tuple[EngineEvent, ...]


@dataclass
class Probe:
    engine: Engine
    reading: str
    nodes: list[PNode] = field(default_factory=list)
    edges: list[PEdge] = field(default_factory=list)
    root_terminal: str = ""
    minima: dict[tuple[int, str, Pair], Optional[Minima]] = field(default_factory=dict)


def enabled_continuations(engine: Engine, state: EState) -> tuple[str, ...]:
    """The continuation rules of the engine enabled at a demand-free state."""
    out: list[str] = []
    if engine.growth and state.regime.n_data() < MAX_DATA:
        out.append("growth")
    if engine.switch:
        out.append("switch")
    return tuple(out)


def _answer(
    engine: Engine, state: EState
) -> tuple[tuple[DemandAnswer, ...], list[tuple[Target, Optional[Minima]]]]:
    rule = moded_rule(engine.rule, state.mode)
    records: list[DemandAnswer] = []
    raw: list[tuple[Target, Optional[Minima]]] = []
    for target in state_demands(engine.rule, state):
        found = least_responses(state.regime, rule, target, engine.validity)
        chosen = None if found is None else found[engine.measure]
        raw.append((target, chosen))
        if chosen is None:
            records.append(DemandAnswer(target[0], target[1], False, None, 0))
        else:
            records.append(
                DemandAnswer(target[0], target[1], True, chosen.cost, len(chosen.deltas))
            )
    return tuple(records), raw


def build_probe(engine: Engine, reading: Reading) -> Probe:
    """Build the probe of one engine at one reading."""
    probe = Probe(engine, reading.name)
    root_history: tuple[EngineEvent, ...] = tuple(reading.genesis)
    root_state = engine_replay(root_history)
    root = PNode(0, 0, root_history, root_state, state_demands(engine.rule, root_state), "root")
    probe.nodes.append(root)
    index: dict[EState, int] = {}

    def attach(
        history: tuple[EngineEvent, ...],
        via: str,
        kind: str,
        demand_kind: str,
        pair: Optional[Pair],
        delta: Delta,
        cost: tuple[int, ...],
    ) -> None:
        state = engine_replay(history)
        if state not in index:
            node = PNode(
                len(probe.nodes),
                1,
                history,
                state,
                state_demands(engine.rule, state),
                via,
            )
            probe.nodes.append(node)
            index[state] = node.node_id
        probe.edges.append(
            PEdge(
                0,
                index[state],
                kind,
                demand_kind,
                pair,
                delta,
                cost,
                history[len(root_history) :],
            )
        )

    if root.demands:
        records, raw = _answer(engine, root_state)
        root.answers = records
        for target, chosen in raw:
            probe.minima[(0, target[0], target[1])] = chosen
            if chosen is None:
                continue
            for delta in chosen.deltas:
                events = response_events(root_state.regime, delta)
                attach(
                    root_history + events,
                    "response",
                    "response",
                    target[0],
                    target[1],
                    delta,
                    chosen.cost,
                )
        probe.root_terminal = (
            "responded" if any(record.answered for record in records) else "refused"
        )
    else:
        enabled = enabled_continuations(engine, root_state)
        root.enabled = enabled
        for rule_name in enabled:
            if rule_name == "growth":
                attach(
                    root_history + growth_events(root_state.regime),
                    "growth",
                    "growth",
                    "",
                    None,
                    (),
                    (),
                )
            else:
                attach(root_history + (SwitchMarker(),), "switch", "switch", "", None, (), ())
        probe.root_terminal = "continued" if enabled else "fixpoint"

    for node in probe.nodes[1:]:
        if node.via == "response":
            continue
        if node.demands:
            records, raw = _answer(engine, node.state)
            node.answers = records
            for target, chosen in raw:
                probe.minima[(node.node_id, target[0], target[1])] = chosen
        else:
            node.enabled = enabled_continuations(engine, node.state)
    return probe


# ---------------------------------------------------------------------------
# Replay and attribution
# ---------------------------------------------------------------------------


def replay_mismatches(probe: Probe) -> list[str]:
    """Every node whose recorded history does not replay to its state."""
    return [
        f"{probe.engine.name}@{probe.reading}: node {node.node_id}"
        for node in probe.nodes
        if engine_replay(node.history) != node.state
    ]


def attribution_violations(probe: Probe) -> list[str]:
    """Every edge holding an event its attributed capability does not emit.

    A response edge must start at a state with the demand it answers, its
    delta must be one of that demand's recorded minima, and its events
    must be the delta's admission events; a growth edge must start at a
    demand-free state below the data bound of an engine declaring growth
    and hold exactly the supply and admission of one fresh token; a switch
    edge must start at a demand-free state of an engine declaring switch
    and hold exactly one marker.  Anything else is named."""
    out: list[str] = []
    where = f"{probe.engine.name}@{probe.reading}"
    for number, edge in enumerate(probe.edges):
        parent = probe.nodes[edge.parent]
        regime = parent.state.regime
        tag = f"{where}: edge {number}"
        foreign = [
            type(event).__name__
            for event in edge.events
            if isinstance(event, Impose)
        ]
        if foreign:
            out.append(f"{tag} holds an event no capability emits: {', '.join(foreign)}")
            continue
        if edge.kind == "response":
            if edge.pair is None or (edge.demand_kind, edge.pair) not in parent.demands:
                out.append(f"{tag} answers no demand of its parent")
                continue
            chosen = probe.minima.get((parent.node_id, edge.demand_kind, edge.pair))
            if chosen is None or edge.delta not in chosen.deltas:
                out.append(f"{tag} holds a delta that is not a recorded minimum")
                continue
            if edge.events != response_events(regime, edge.delta):
                out.append(f"{tag} holds events other than its delta's admissions")
        elif edge.kind == "growth":
            if parent.demands or not probe.engine.growth or regime.n_data() >= MAX_DATA:
                out.append(f"{tag} grows where growth is not enabled")
                continue
            if (
                len(edge.events) != 2
                or not isinstance(edge.events[0], Supply)
                or not isinstance(edge.events[1], AdmitDatum)
                or edge.events[0].token != edge.events[1].token
                or edge.events[0].token in regime.data
            ):
                out.append(f"{tag} is not the supply and admission of one fresh token")
        elif edge.kind == "switch":
            if parent.demands or not probe.engine.switch:
                out.append(f"{tag} switches where switch is not enabled")
                continue
            if edge.events != (SwitchMarker(),):
                out.append(f"{tag} is not one switch marker")
        else:
            out.append(f"{tag} has an unknown kind {edge.kind!r}")
    return out


# ---------------------------------------------------------------------------
# Labels, signatures and probe-isomorphism
# ---------------------------------------------------------------------------


@lru_cache(maxsize=None)
def _key(regime: Regime) -> str:
    return repr(canonical(regime))


def node_label(node: PNode) -> Label:
    """The node label of ``PROMPT.md``: the sealed key of the regime, the
    mode, the kinds and number of the demands and, where the demands were
    answered at a level-one state reached by continuation, the kind, cost
    and tie count of each."""
    kinds = tuple(sorted(kind for kind, _ in node.demands))
    answers: tuple[Any, ...] = ()
    if node.level == 1 and node.answers is not None:
        answers = tuple(
            sorted(
                (record.kind, record.answered, record.cost or (), record.ties)
                for record in node.answers
            )
        )
    return (_key(node.state.regime), node.state.mode, kinds, answers)


def edge_label(edge: PEdge) -> Label:
    if edge.kind == "response":
        return (edge.kind, edge.demand_kind, edge.cost)
    return (edge.kind,)


def probe_signature(probe: Probe) -> Label:
    """Root label, and the sorted list over level-one states of each
    state's label with the sorted labels of the edges into it."""
    children: list[Label] = []
    for node in probe.nodes[1:]:
        into = tuple(
            sorted(edge_label(edge) for edge in probe.edges if edge.child == node.node_id)
        )
        children.append((node_label(node), into))
    return (node_label(probe.nodes[0]), tuple(sorted(children)))


def signature_digest(signature: Label) -> str:
    return hashlib.sha256(repr(signature).encode("ascii")).hexdigest()


def brute_isomorphic(left: Probe, right: Probe) -> bool:
    """Exhaustive search over the bijections of the level-one states: a
    bijection preserving each state's label and the multiset of labels of
    the edges into it, with equal root labels.  Independent of the
    sorting in ``probe_signature``: it compares labels pairwise and never
    sorts a signature."""
    if node_label(left.nodes[0]) != node_label(right.nodes[0]):
        return False
    a = left.nodes[1:]
    b = right.nodes[1:]
    if len(a) != len(b):
        return False

    def into(probe: Probe, node: PNode) -> list[Label]:
        return [edge_label(edge) for edge in probe.edges if edge.child == node.node_id]

    def same_multiset(x: list[Label], y: list[Label]) -> bool:
        rest = list(y)
        for item in x:
            if item not in rest:
                return False
            rest.remove(item)
        return not rest

    compatible = [
        [
            node_label(p) == node_label(q) and same_multiset(into(left, p), into(right, q))
            for q in b
        ]
        for p in a
    ]
    seen: dict[tuple[int, int], bool] = {}

    def extend(position: int, used: int) -> bool:
        if position == len(a):
            return True
        memo_key = (position, used)
        if memo_key in seen:
            return seen[memo_key]
        result = False
        for index in range(len(b)):
            if used & (1 << index) or not compatible[position][index]:
                continue
            if extend(position + 1, used | (1 << index)):
                result = True
                break
        seen[memo_key] = result
        return result

    return extend(0, 0)


def key_brute_disagreements(regimes: Sequence[Regime]) -> dict[str, int]:
    """Compare the partition of the regimes by the sealed key procedure
    with the partition by the sealed brute-force minimum."""
    key_to_brute: dict[str, set[str]] = {}
    brute_to_key: dict[str, set[str]] = {}
    for regime in regimes:
        key = _key(regime)
        brute = repr(canonical_bruteforce(regime))
        key_to_brute.setdefault(key, set()).add(brute)
        brute_to_key.setdefault(brute, set()).add(key)
    disagreements = sum(len(v) > 1 for v in key_to_brute.values()) + sum(
        len(v) > 1 for v in brute_to_key.values()
    )
    return {
        "regimes": len(regimes),
        "classes": len(key_to_brute),
        "disagreements": disagreements,
    }


# ---------------------------------------------------------------------------
# The responder cross-check against rung two
# ---------------------------------------------------------------------------


def responder_crosscheck(
    regime: Regime, rule_name: str, mode: str, target: Target
) -> dict[str, bool]:
    """Compare, under each measure, this tree's responder with the clause
    of member two switched off against rung two's ``minimum_responses``,
    on the same regime, rule, mode and demand."""
    rule = moded_rule(rule_name, mode)
    ours = least_responses(regime, rule, target, "V1", memo=False)
    out: dict[str, bool] = {}
    for measure in ("mu1", "mu2"):
        theirs = rung_two_minimum_responses(regime, rule, target, measure, BOUNDS)
        if ours is None or theirs is None:
            out[measure] = ours is None and theirs is None
            continue
        mine = ours[measure]
        cost = (mine.item_count, -1) if measure == "mu1" else mine.cost
        out[measure] = tuple(theirs.deltas) == mine.deltas and tuple(theirs.cost) == tuple(cost)
    return out


# ---------------------------------------------------------------------------
# JSON
# ---------------------------------------------------------------------------


def delta_json(delta: Delta) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in delta:
        if isinstance(item, NewDatum):
            out.append({"item": "datum"})
        elif isinstance(item, NewForm):
            out.append({"item": "form", "arity": item.arity})
        elif isinstance(item, NewRuleAll):
            out.append({"item": "rule", "form": item.form})
        else:
            out.append({"item": "inst", "form": item.form, "args": list(item.args)})
    return out


def event_json(event: EngineEvent) -> dict[str, Any]:
    if isinstance(event, SwitchMarker):
        return {"event": "switch"}
    payload: dict[str, Any] = {"event": type(event).__name__}
    for name in ("token", "arity", "form", "args", "i", "j"):
        if hasattr(event, name):
            value = getattr(event, name)
            payload[name] = list(value) if isinstance(value, tuple) else value
    return payload


def _regime_json(regime: Regime) -> dict[str, Any]:
    return {
        "data": regime.n_data(),
        "forms": list(regime.forms),
        "insts": sorted([form, list(args)] for form, args in regime.insts),
        "rules": sorted(regime.rules),
        "reqs": sorted(list(pair) for pair in regime.reqs),
    }


def probe_payload(probe: Probe) -> dict[str, Any]:
    """The full probe, every node and edge, with no engine name: two
    engines with one probe give one payload."""

    def answers(node: PNode) -> Optional[list[dict[str, Any]]]:
        if node.answers is None:
            return None
        return [
            {
                "kind": record.kind,
                "pair": list(record.pair),
                "answered": record.answered,
                "cost": list(record.cost) if record.cost is not None else None,
                "ties": record.ties,
            }
            for record in node.answers
        ]

    return {
        "reading": probe.reading,
        "root_terminal": probe.root_terminal,
        "nodes": [
            {
                "id": node.node_id,
                "level": node.level,
                "via": node.via,
                "mode": node.state.mode,
                "regime": _regime_json(node.state.regime),
                "demands": [[kind, pair[0], pair[1]] for kind, pair in node.demands],
                "answers": answers(node),
                "enabled": list(node.enabled) if node.enabled is not None else None,
                "history_length": len(node.history),
            }
            for node in probe.nodes
        ],
        "edges": [
            {
                "parent": edge.parent,
                "child": edge.child,
                "kind": edge.kind,
                "demand_kind": edge.demand_kind,
                "pair": list(edge.pair) if edge.pair is not None else None,
                "delta": delta_json(edge.delta),
                "cost": list(edge.cost),
                "events": [event_json(event) for event in edge.events],
            }
            for edge in probe.edges
        ],
    }
