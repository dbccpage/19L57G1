"""Finite growth machine driven by state-reading stake rules.

The candidate grammar, honour relation, response measure, and sealed genesis
histories are imported read-only.  A rule is re-read at every reached state.
"""

from __future__ import annotations

import hashlib
import json
import math
import pathlib
import sys
from collections import deque
from dataclasses import dataclass, field
from itertools import permutations
from typing import Hashable, Optional, Sequence

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _path in (
    REPO / "code",
    REPO / "research" / "identification_dual",
    REPO / "research" / "two_sided_commitment",
):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from derivation.candidates import (  # noqa: E402
    Bounds,
    Delta,
    NewRuleAll,
    apply_delta,
    delta_events,
    item_key,
    iter_full_deltas,
    mu2,
)
from derivation.engine import READINGS, Reading, delta_label  # noqa: E402
from derivation.export import Json, delta_json, event_json, regime_json  # noqa: E402
from derivation.iso import (  # noqa: E402
    IsoBudgetError,
    canonical,
    canonical_bruteforce,
    find_iso,
    serialize,
)
from derivation.model import (  # noqa: E402
    AdmissionError,
    AdmitDatum,
    Event,
    Pair,
    Regime,
    Supply,
    replay,
)
from two_sided import honoured  # noqa: E402

from observables import (  # noqa: E402
    ObservableGuardError,
    datum_permutations,
    form_permutations,
    held_pairs,
    one_orbit,
    profile_size,
    renamed,
)
from rules import (  # noqa: E402
    APART,
    FREE,
    SAME,
    Label,
    StakeRule,
    demands,
    honoured_labelled_pairs,
    label_map,
    label_of,
)

BOUNDS = Bounds(max_items=2, max_arity=2)
MEASURES: tuple[str, ...] = ("mu1", "mu2")
MAX_RESPONSE_ROUNDS = 15
NODE_GUARD = 250
MAX_DATA = 4
PERMUTATION_BUDGET = 100_000


def _json(value: object) -> Json:
    if isinstance(value, dict):
        return {str(key): _json(item) for key, item in value.items()}
    if isinstance(value, (set, frozenset)):
        return [_json(item) for item in sorted(value, key=repr)]
    if isinstance(value, (list, tuple)):
        return [_json(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"value is not JSON-compatible: {value!r}")


def _delta_key(delta: Delta) -> tuple[tuple[int, int, tuple[int, ...]], ...]:
    return tuple(item_key(item) for item in delta)


def _has_noop_item(regime: Regime, delta: Delta) -> bool:
    return any(
        isinstance(item, NewRuleAll) and item.form in regime.rules
        for item in delta
    )


@dataclass(frozen=True)
class Minima:
    measure: str
    cost: tuple[int, int]
    deltas: tuple[Delta, ...]
    valid_at_cost: int


def response_valid(
    regime: Regime,
    rule: StakeRule,
    target: tuple[Label, Pair],
    delta: Delta,
) -> bool:
    """Pinned no-regress validity under the pre-response labels.

    The target's old label must become honoured.  Every pair honoured before
    the response must remain honoured under its old label.  The rule is then
    re-read for the next state's demand computation.
    """

    try:
        after = apply_delta(regime, delta)
    except AdmissionError:
        return False
    label, pair = target
    if not honoured(after, label, pair):
        return False
    return all(
        honoured(after, old_label, old_pair)
        for old_label, old_pair in honoured_labelled_pairs(regime, rule)
    )


def minimum_responses(
    regime: Regime,
    rule: StakeRule,
    target: tuple[Label, Pair],
    measure: str,
    bounds: Bounds = BOUNDS,
) -> Optional[Minima]:
    """Unpruned minimum responses under one sealed measure."""

    if measure not in MEASURES:
        raise ValueError(f"unknown measure: {measure}")
    for item_count in range(bounds.max_items + 1):
        valid: list[Delta] = []
        seen: set[Delta] = set()
        for delta in iter_full_deltas(regime, item_count, bounds):
            if delta in seen or _has_noop_item(regime, delta):
                continue
            seen.add(delta)
            if response_valid(regime, rule, target, delta):
                valid.append(delta)
        if not valid:
            continue
        if measure == "mu1":
            chosen = tuple(sorted(valid, key=_delta_key))
            return Minima(measure, (item_count, -1), chosen, len(valid))
        best = min(mu2(delta) for delta in valid)
        chosen = tuple(
            sorted((delta for delta in valid if mu2(delta) == best), key=_delta_key)
        )
        return Minima(measure, best, chosen, len(valid))
    return None


IndexedKey = tuple[
    int,
    tuple[int, ...],
    tuple[tuple[int, tuple[int, ...]], ...],
    tuple[int, ...],
    tuple[Pair, ...],
]


def indexed_key(regime: Regime) -> IndexedKey:
    return (
        regime.n_data(),
        tuple(regime.forms),
        tuple(sorted(regime.insts)),
        tuple(sorted(regime.rules)),
        tuple(sorted(regime.reqs)),
    )


def quotient_key(regime: Regime, rule: StakeRule) -> Hashable:
    """State quotient for the declared rule class.

    Menu rules use the sealed isomorphism key.  Controls retain the indexed
    component used by their pinned sibling because three controls read index
    values and future labels are then not determined by the isomorphism key.
    """

    base = canonical(regime, PERMUTATION_BUDGET)
    if rule.source == "menu":
        return base
    return (base, indexed_key(regime))


SearchKey = tuple[Hashable, int]


def search_key(regime: Regime, rule: StakeRule, response_rounds: int) -> SearchKey:
    """Quotient key for the bounded search state.

    The remaining response budget affects future expansion, so two isomorphic
    regimes reached after different numbers of responses are not the same
    bounded-search node.
    """

    return (quotient_key(regime, rule), response_rounds)


@dataclass
class Node:
    node_id: int
    history: tuple[Event, ...]
    regime: Regime
    response_rounds: int
    depth: int
    key: Hashable
    status: str = "open"
    merged_count: int = 1
    certified: bool = False


@dataclass
class Edge:
    parent: int
    child: int
    challenge: str
    target_kind: str
    target_pair: Optional[Pair]
    response: Delta
    cost: tuple[int, int]
    tie_classes: int
    class_size: int
    events: tuple[Event, ...]
    datum_transport: tuple[int, ...]
    form_transport: tuple[int, ...]
    info: dict[str, object] = field(default_factory=dict)


@dataclass
class Tree:
    reading: str
    rule: str
    measure: str
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    refusals: list[dict[str, object]] = field(default_factory=list)


def edge_replay_failure(tree: Tree, edge: Edge) -> Optional[str]:
    """Return a diagnostic unless an edge replays to its quotient child.

    The event suffix is replayed from the stored parent.  The resulting regime
    must transport to the stored child representative through the exported
    datum/form bijections, and the response-round counter must agree exactly.
    """

    if not 0 <= edge.parent < len(tree.nodes):
        return "edge parent is outside the node table"
    if not 0 <= edge.child < len(tree.nodes):
        return "edge child is outside the node table"
    parent = tree.nodes[edge.parent]
    child = tree.nodes[edge.child]
    try:
        after = replay(edge.events, parent.regime)
    except AdmissionError as exc:
        return f"edge event replay failed: {exc}"
    expected_rounds = parent.response_rounds + int(edge.target_pair is not None)
    if child.response_rounds != expected_rounds:
        return (
            "edge response-round mismatch: "
            f"expected {expected_rounds}, got {child.response_rounds}"
        )
    if tuple(sorted(edge.datum_transport)) != tuple(range(after.n_data())):
        return "edge datum transport is not a bijection"
    if tuple(sorted(edge.form_transport)) != tuple(range(len(after.forms))):
        return "edge form transport is not a bijection"
    target_datum_identity = tuple(range(child.regime.n_data()))
    target_form_identity = tuple(range(len(child.regime.forms)))
    if serialize(after, edge.datum_transport, edge.form_transport) != serialize(
        child.regime, target_datum_identity, target_form_identity
    ):
        return "edge transport does not reach the stored child structure"
    return None


def _fresh_token(regime: Regime) -> str:
    stem = f"stake_g{regime.n_data()}"
    token = stem
    suffix = 0
    while token in regime.data:
        suffix += 1
        token = f"{stem}_{suffix}"
    return token


def _edge_info(
    before: Regime,
    after: Regime,
    rule: StakeRule,
    target: Optional[tuple[Label, Pair]],
) -> dict[str, object]:
    before_demands = demands(before, rule)
    try:
        after_demands = demands(after, rule)
    except ObservableGuardError as exc:
        return {
            "demands_before": len(before_demands),
            "observable_guard_after": str(exc),
            "relabelled_pairs": [],
            "new_demands": [],
            **(
                {"kind": target[0], "target": list(target[1])}
                if target is not None
                else {}
            ),
        }
    after_pairs = {(kind, pair) for kind, pair in after_demands}
    before_labels = dict(label_map(before, rule))
    relabelled = [
        [pair[0], pair[1], old, label_of(rule, after, *pair)]
        for pair, old in before_labels.items()
        if old != label_of(rule, after, *pair)
    ]
    information: dict[str, object] = {
        "demands_before": len(before_demands),
        "demands_after": len(after_demands),
        "honoured_at_once": sum(
            1 for item in before_demands if item not in after_pairs
        ),
        "relabelled_pairs": relabelled,
        "new_demands": [
            [kind, pair[0], pair[1]]
            for kind, pair in after_demands
            if (kind, pair) not in set(before_demands)
        ],
    }
    if target is not None:
        information["kind"] = target[0]
        information["target"] = list(target[1])
    return information


def _attach(
    tree: Tree,
    rule: StakeRule,
    key_map: dict[SearchKey, int],
    queue: deque[int],
    parent: Node,
    history: tuple[Event, ...],
    response_rounds: int,
    challenge: str,
    target: Optional[tuple[Label, Pair]],
    response: Delta,
    cost: tuple[int, int],
    tie_classes: int,
    class_size: int,
) -> None:
    after = replay(history)
    if history[: len(parent.history)] != parent.history:
        raise AssertionError("edge history does not extend its parent history")
    events = history[len(parent.history) :]
    if replay(events, parent.regime) != after:
        raise AssertionError("edge event suffix does not replay from its parent")
    try:
        key = search_key(after, rule, response_rounds)
        iso_guard = False
    except IsoBudgetError:
        key = (("iso_guard", indexed_key(after), len(tree.nodes)), response_rounds)
        iso_guard = True
    if key in key_map:
        child_id = key_map[key]
        tree.nodes[child_id].merged_count += 1
        witness = find_iso(after, tree.nodes[child_id].regime, PERMUTATION_BUDGET)
        if witness is None:
            raise AssertionError("quotient collision has no isomorphism witness")
        datum_transport, form_transport = witness
    else:
        child_id = len(tree.nodes)
        child = Node(
            child_id,
            history,
            after,
            response_rounds,
            parent.depth + 1,
            key,
            "frontier_iso_guard" if iso_guard else "open",
            certified=(replay(history) == after),
        )
        tree.nodes.append(child)
        key_map[key] = child_id
        datum_transport = tuple(range(after.n_data()))
        form_transport = tuple(range(len(after.forms)))
        if not iso_guard:
            queue.append(child_id)
    info = _edge_info(parent.regime, after, rule, target)
    edge = Edge(
        parent.node_id,
        child_id,
        challenge,
        target[0] if target is not None else "grow",
        target[1] if target is not None else None,
        response,
        cost,
        tie_classes,
        class_size,
        events,
        datum_transport,
        form_transport,
        info,
    )
    failure = edge_replay_failure(tree, edge)
    if failure is not None:
        raise AssertionError(failure)
    tree.edges.append(edge)


def _quotient_deltas(
    regime: Regime, rule: StakeRule, deltas: Sequence[Delta]
) -> list[tuple[Delta, int]]:
    grouped: dict[Hashable, list[Delta]] = {}
    for delta in deltas:
        after = apply_delta(regime, delta)
        try:
            key = quotient_key(after, rule)
        except IsoBudgetError:
            key = ("iso_guard", indexed_key(after), _delta_key(delta))
        grouped.setdefault(key, []).append(delta)
    return [
        (sorted(items, key=_delta_key)[0], len(items))
        for _, items in sorted(grouped.items(), key=lambda item: repr(item[0]))
    ]


def build_tree(
    reading: Reading,
    rule: StakeRule,
    measure: str,
    *,
    bounds: Bounds = BOUNDS,
    max_response_rounds: int = MAX_RESPONSE_ROUNDS,
    node_guard: int = NODE_GUARD,
    max_data: int = MAX_DATA,
) -> Tree:
    """Build one deterministic finite tree from a sealed genesis."""

    register_rules((rule,))
    history = tuple(reading.genesis)
    regime = replay(history)
    root_key = search_key(regime, rule, 0)
    root = Node(0, history, regime, 0, 0, root_key)
    root.certified = replay(root.history) == root.regime
    tree = Tree(reading.name, rule.name, measure, [root])
    key_map: dict[SearchKey, int] = {root_key: 0}
    queue: deque[int] = deque([0])
    while queue:
        node = tree.nodes[queue.popleft()]
        try:
            open_demands = demands(node.regime, rule)
        except ObservableGuardError:
            node.status = "frontier_observable_guard"
            continue
        if len(tree.nodes) >= node_guard:
            node.status = "frontier_guard"
            continue
        if not open_demands:
            if node.regime.n_data() >= max_data:
                node.status = "terminal_data_bound"
                continue
            token = _fresh_token(node.regime)
            grown = node.history + (Supply(token), AdmitDatum(token))
            _attach(
                tree,
                rule,
                key_map,
                queue,
                node,
                grown,
                node.response_rounds,
                "grow",
                None,
                (),
                (0, 0),
                1,
                1,
            )
            node.status = "expanded"
            continue
        if node.response_rounds >= max_response_rounds:
            node.status = "terminal_round_bound"
            continue
        gathered: list[tuple[tuple[Label, Pair], Minima]] = []
        refused_targets: list[tuple[Label, Pair]] = []
        for target in open_demands:
            result = minimum_responses(node.regime, rule, target, measure, bounds)
            if result is None:
                refused_targets.append(target)
                continue
            gathered.append((target, result))
        for target in refused_targets:
            tree.refusals.append(
                {
                    "node": node.node_id,
                    "kind": target[0],
                    "pair": list(target[1]),
                    "data": node.regime.n_data(),
                    "open_demands": len(open_demands),
                    "answerable_demands": len(gathered),
                    "terminal": not gathered,
                }
            )
        if not gathered:
            node.status = "terminal_no_response"
            continue
        for target, result in gathered:
            classes = _quotient_deltas(node.regime, rule, result.deltas)
            for representative, class_size in classes:
                if not response_valid(node.regime, rule, target, representative):
                    raise AssertionError("selected response failed revalidation")
                history2 = node.history + tuple(delta_events(node.regime, representative))
                _attach(
                    tree,
                    rule,
                    key_map,
                    queue,
                    node,
                    history2,
                    node.response_rounds + 1,
                    delta_label(node.regime, representative),
                    target,
                    representative,
                    result.cost,
                    len(classes),
                    class_size,
                )
        node.status = "expanded_with_refusals" if refused_targets else "expanded"
    return tree


def node_payload(node: Node) -> dict[str, Json]:
    return {
        "id": node.node_id,
        "history": [event_json(event) for event in node.history],
        "regime": regime_json(node.regime),
        "response_rounds": node.response_rounds,
        "depth": node.depth,
        "status": node.status,
        "merged_count": node.merged_count,
        "certified": node.certified,
    }


def edge_payload(tree: Tree, edge: Edge) -> dict[str, Json]:
    return {
        "parent": edge.parent,
        "child": edge.child,
        "challenge": edge.challenge,
        "target_kind": edge.target_kind,
        "target_pair": list(edge.target_pair) if edge.target_pair is not None else None,
        "response": delta_json(edge.response),
        "cost": list(edge.cost),
        "tie_classes": edge.tie_classes,
        "class_size": edge.class_size,
        "events": [event_json(event) for event in edge.events],
        "datum_transport": list(edge.datum_transport),
        "form_transport": list(edge.form_transport),
        "certified": edge_replay_failure(tree, edge) is None,
        "info": _json(edge.info),
    }


def tree_stats(tree: Tree) -> dict[str, Json]:
    statuses: dict[str, int] = {}
    for node in tree.nodes:
        statuses[node.status] = statuses.get(node.status, 0) + 1
    response_edges = [edge for edge in tree.edges if edge.target_pair is not None]
    growth_demand_kinds: set[str] = set()
    for edge in tree.edges:
        if edge.target_pair is not None:
            continue
        new_demands = edge.info.get("new_demands")
        if not isinstance(new_demands, list):
            raise TypeError("growth edge new_demands must be a list")
        for demand in new_demands:
            if (
                not isinstance(demand, list)
                or len(demand) != 3
                or not isinstance(demand[0], str)
            ):
                raise TypeError("growth edge demand must be [kind, left, right]")
            growth_demand_kinds.add(demand[0])
    fixpoints: list[Node] = []
    for node in tree.nodes:
        try:
            if not demands(node.regime, _tree_rule(tree)):
                fixpoints.append(node)
        except ObservableGuardError:
            pass
    relabellings = 0
    for edge in tree.edges:
        value = edge.info.get("relabelled_pairs")
        if isinstance(value, list):
            relabellings += len(value)
    return {
        "nodes": len(tree.nodes),
        "edges": len(tree.edges),
        "statuses": statuses,
        "response_edges": len(response_edges),
        "growth_edges": sum(edge.target_pair is None for edge in tree.edges),
        "growth_demand_kinds": sorted(growth_demand_kinds),
        "response_target_kinds": sorted(
            {edge.target_kind for edge in response_edges}
        ),
        "relabellings": relabellings,
        "refusals": len(tree.refusals),
        "fixpoints": len(fixpoints),
        "guard_nodes": statuses.get("frontier_guard", 0)
        + statuses.get("frontier_iso_guard", 0)
        + statuses.get("frontier_observable_guard", 0),
        "all_certified": all(node.certified for node in tree.nodes),
        "all_edges_certified": all(
            edge_replay_failure(tree, edge) is None for edge in tree.edges
        ),
        "max_data": max(node.regime.n_data() for node in tree.nodes),
        "max_response_rounds": max(node.response_rounds for node in tree.nodes),
    }


_RULE_LOOKUP: dict[str, StakeRule] = {}


def register_rules(rules: Sequence[StakeRule]) -> None:
    _RULE_LOOKUP.update((rule.name, rule) for rule in rules)


def _tree_rule(tree: Tree) -> StakeRule:
    try:
        return _RULE_LOOKUP[tree.rule]
    except KeyError as exc:
        raise ValueError(f"tree rule is not registered: {tree.rule}") from exc


def tree_payload(tree: Tree) -> dict[str, Json]:
    return {
        "reading": tree.reading,
        "rule": tree.rule,
        "measure": tree.measure,
        "stats": tree_stats(tree),
        "refusals": _json(tree.refusals),
        "nodes": [node_payload(node) for node in tree.nodes],
        "edges": [edge_payload(tree, edge) for edge in tree.edges],
    }


def tree_signature(tree: Tree) -> str:
    """Rule-name-free digest of one deterministic tree."""

    payload = tree_payload(tree)
    payload.pop("rule")
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def reached_regimes(trees: Sequence[Tree]) -> tuple[Regime, ...]:
    unique: dict[IndexedKey, Regime] = {}
    for tree in trees:
        for node in tree.nodes:
            unique.setdefault(indexed_key(node.regime), node.regime)
    return tuple(regime for _, regime in sorted(unique.items(), key=lambda item: repr(item[0])))


def invariance_records(
    rules: Sequence[StakeRule], regimes: Sequence[Regime]
) -> list[dict[str, Json]]:
    """Check all rules in one shared traversal of the frozen population.

    Reconstructing a renamed regime is the expensive step.  Evaluating each
    rule in a separate pass repeated that reconstruction once per rule.  This
    routine preserves the exact population and evaluates every non-orbit rule
    against each reconstructed regime before advancing to the next renaming.

    Rules reading O4 are evaluated on every source pair, but are not upgraded
    to CHECKED by a prose conjugation argument.  A CHECKED finite transport
    claim requires executable target-regime replay.  Until that replay exists,
    those rules remain OPEN even when the source automorphism guard does not
    fire.
    """

    orbit_rules = tuple(rule for rule in rules if "O4" in rule.observables)
    direct_rules = tuple(rule for rule in rules if "O4" not in rule.observables)
    results: dict[str, dict[str, Json]] = {}
    checks = {rule.name: 0 for rule in direct_rules}
    active = {rule.name: rule for rule in direct_rules}

    for regime_index, regime in enumerate(regimes):
        pairs = held_pairs(regime)
        before = {
            rule.name: {pair: label_of(rule, regime, *pair) for pair in pairs}
            for rule in direct_rules
            if rule.name in active
        }
        for pi in datum_permutations(regime):
            for phi in form_permutations(regime):
                transported = renamed(regime, pi, phi)
                for pair in pairs:
                    mapped_values = sorted((pi[pair[0]], pi[pair[1]]))
                    mapped = (mapped_values[0], mapped_values[1])
                    for name, rule in tuple(active.items()):
                        checks[name] += 1
                        after = label_of(rule, transported, *mapped)
                        label_before = before[name][pair]
                        if label_before != after:
                            results[name] = {
                                "disposition": "REFUTED",
                                "checks_before_refutation": checks[name],
                                "regime_index": regime_index,
                                "source_regime": regime_json(regime),
                                "pair": list(pair),
                                "datum_renaming": list(pi),
                                "form_renaming": list(phi),
                                "label_before": label_before,
                                "label_after": after,
                            }
                            del active[name]
                if not active:
                    break
            if not active:
                break

    for name in active:
        results[name] = {
            "disposition": "CHECKED",
            "checks": checks[name],
            "regimes": len(regimes),
            "scope": "every renaming of every reached regime within the rectangle",
            "orbit_transport": None,
        }

    if orbit_rules:
        covered = 0
        source_pairs = 0
        obstruction: tuple[int, str] | None = None
        for regime_index, regime in enumerate(regimes):
            pairs = held_pairs(regime)
            try:
                for pair in pairs:
                    for rule in orbit_rules:
                        label_of(rule, regime, *pair)
                    source_pairs += 1
            except ObservableGuardError as exc:
                obstruction = (regime_index, str(exc))
                break
            covered += (
                math.factorial(regime.n_data())
                * math.factorial(len(regime.forms))
                * len(pairs)
            )
        for rule in orbit_rules:
            if obstruction is not None:
                results[rule.name] = {
                    "disposition": "OPEN_AT_OBSERVABLE_GUARD",
                    "regime_index": obstruction[0],
                    "pairs_checked_before_guard": source_pairs,
                    "obstruction": obstruction[1],
                }
            else:
                results[rule.name] = {
                    "disposition": "OPEN_AT_TRANSPORT_REPLAY",
                    "regimes": len(regimes),
                    "renaming_cases_priced": covered,
                    "source_pairs_checked": source_pairs,
                    "obstruction": (
                        "O4 source values were computed, but target-regime labels "
                        "were not exhaustively replayed"
                    ),
                }

    return [{"rule": rule.name, **results[rule.name]} for rule in rules]


def invariance_record(rule: StakeRule, regimes: Sequence[Regime]) -> dict[str, Json]:
    """Compatibility wrapper for a one-rule invariance check."""

    record = invariance_records((rule,), regimes)[0]
    return {key: value for key, value in record.items() if key != "rule"}


def canonical_crosscheck(regimes: Sequence[Regime]) -> dict[str, Json]:
    """Compare refined and brute-force isomorphism partitions in scope."""

    refined_to_brute: dict[str, set[str]] = {}
    brute_to_refined: dict[str, set[str]] = {}
    checked = 0
    skipped = 0
    for regime in regimes:
        permutations_total = math.factorial(regime.n_data()) * math.factorial(len(regime.forms))
        if permutations_total > PERMUTATION_BUDGET:
            skipped += 1
            continue
        refined = repr(canonical(regime, PERMUTATION_BUDGET))
        brute = repr(canonical_bruteforce(regime))
        refined_to_brute.setdefault(refined, set()).add(brute)
        brute_to_refined.setdefault(brute, set()).add(refined)
        checked += 1
    agrees = all(len(values) == 1 for values in refined_to_brute.values()) and all(
        len(values) == 1 for values in brute_to_refined.values()
    )
    return {
        "regimes_checked": checked,
        "regimes_above_permutation_budget": skipped,
        "relation_agrees": agrees,
        "permutation_budget": PERMUTATION_BUDGET,
    }


def build_all(rules: Sequence[StakeRule]) -> list[Tree]:
    register_rules(rules)
    return [
        build_tree(reading, rule, measure)
        for rule in rules
        for reading in READINGS
        for measure in MEASURES
    ]


def rule_generation_record(rule: StakeRule, trees: Sequence[Tree]) -> dict[str, Json]:
    own = [tree for tree in trees if tree.rule == rule.name]
    stats = [tree_stats(tree) for tree in own]
    growth_kind_values: set[str] = set()
    response_kind_values: set[str] = set()
    for stat in stats:
        raw_growth_kinds = stat["growth_demand_kinds"]
        raw_response_kinds = stat["response_target_kinds"]
        if not isinstance(raw_growth_kinds, list):
            raise TypeError("tree growth kinds must be a list")
        if not isinstance(raw_response_kinds, list):
            raise TypeError("tree response kinds must be a list")
        growth_kind_values.update(
            kind for kind in raw_growth_kinds if isinstance(kind, str)
        )
        response_kind_values.update(
            kind for kind in raw_response_kinds if isinstance(kind, str)
        )
    growth_kinds = sorted(growth_kind_values)
    response_kinds = sorted(response_kind_values)
    signatures = {
        f"{tree.reading}/{tree.measure}": tree_signature(tree) for tree in own
    }
    return {
        "rule": rule.name,
        "source": rule.source,
        "observables": list(rule.observables),
        "capability_count": rule.capability_count,
        "growth_kinds": growth_kinds,
        "response_target_kinds": response_kinds,
        "kind_populations_agree": growth_kinds == response_kinds,
        "relabellings": sum(_json_int(stat["relabellings"]) for stat in stats),
        "refusals": sum(_json_int(stat["refusals"]) for stat in stats),
        "fixpoints": sum(_json_int(stat["fixpoints"]) for stat in stats),
        "guard_nodes": sum(_json_int(stat["guard_nodes"]) for stat in stats),
        "nodes": sum(_json_int(stat["nodes"]) for stat in stats),
        "tree_signatures": signatures,
    }


def _json_int(value: Json) -> int:
    if not isinstance(value, int):
        raise TypeError("tree statistic must be an integer")
    return value
