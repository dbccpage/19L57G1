"""Deterministic experiments using the unchanged source implementation.

Classification: metatheory apparatus and finite computation.
AuthorityEffect: None.
"""

from __future__ import annotations

from collections import Counter
import json
from typing import Any, Mapping, Sequence, cast

from derivation.candidates import Bounds, NewDatum, apply_delta, delta_events, min_responses
from derivation.engine import READING_L, READING_F, Reading, Tree, build_tree, closure_challenge_orbits
from derivation.export import Json, edge_json, event_from_json, event_json, node_json, regime_json, tree_full_json, verify_full_export
from derivation.iso import CanonKey, IsoBudgetError, canonical, rename
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Event, Impose, Pair, Regime, replay
from derivation.observe import collapsed_pairs, separable
from verify_sources import BASELINE_COMMIT


class AuditFailure(RuntimeError):
    """A declared witness failed its independent check."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AuditFailure(label)


def sample(*, supply: bool, rounds: int = 7, guard: int = 250) -> Tree:
    """Call the original driver without changing its grammar or policies."""
    return build_tree(READING_L, "mu2", Bounds(2, 2), rounds, guard, supply)


def descendant_nodes(tree: Tree, start: int) -> tuple[int, ...]:
    """Reachability in this finite exported graph, including the start."""
    if not 0 <= start < len(tree.nodes):
        raise ValueError("unknown start node")
    seen: set[int] = set()
    pending = [start]
    while pending:
        nid = pending.pop()
        if nid in seen:
            continue
        seen.add(nid)
        pending.extend(edge.child for edge in tree.edges if edge.parent == nid)
    return tuple(sorted(seen))


def descendant_keys(tree: Tree, start: int) -> tuple[CanonKey, ...]:
    """The canonical classes of those nodes, for comparison ACROSS trees.

    Node ids are local to one tree, so a cross-tree comparison has to use
    classes. Selection WITHIN one tree must not; see `normalized_records`.
    """
    return tuple(sorted({tree.nodes[nid].canon for nid in descendant_nodes(tree, start)}))


def replay_cuts(tree: Tree) -> dict[str, int]:
    """Check every edge against the child it names, and at every history split.

    The cut invariance on its own is a TAUTOLOGY and is reported as one. The
    pinned `replay` is a plain left fold, so splitting a history and resuming
    from the intermediate state agrees by construction whatever `step` does,
    and no engine defect can make that comparison fire. It is kept because it
    is the exact finite instance of `LocalReuse.replayE_restart`, and it is
    counted separately so no reader mistakes its size for evidence.

    What can fail here is the two checks ABOVE the loop, and that was measured
    rather than assumed. Against five mutations -- an edge repointed to another
    child, an edge response emptied, a node regime swapped for another node's,
    a node history emptied, an edge parent repointed -- `verify_full_export`
    caught four and the stored-history check caught the fifth, which
    `verify_full_export` passed. No mutation was found that the cut loop alone
    catches. An endpoint check comparing each edge to the child it names was
    written and then removed: it caught nothing the export gate had not
    already refused, and a second check that cannot fire is the same defect
    this docstring exists to record.

    So the loop stands as the finite instance of `LocalReuse.replayE_restart`
    and as nothing else, and its size is reported under a name that says so.
    """
    for node in tree.nodes:
        require(replay(node.history) == node.regime, f"node {node.node_id} stored history")
    require(verify_full_export(tree_full_json(tree)), "full export replay")
    cuts = 0
    for edge in tree.edges:
        parent = tree.nodes[edge.parent]
        record = edge_json(tree, edge)
        events = tuple(event_from_json(cast(Mapping[str, Json], raw))
                       for raw in cast(Sequence[Json], record["events"]))
        endpoint = replay(parent.history + events)
        for cut in range(len(parent.history) + 1):
            intermediate = replay(parent.history[:cut])
            restarted = replay(parent.history[cut:] + events, intermediate)
            require(restarted == endpoint, f"edge {edge.parent}/{edge.child} cut {cut}")
            cuts += 1
    return {"edges": len(tree.edges), "history_cuts_tautological": cuts}


def minimum_keys(base: Regime, target: Pair, measure: str) -> tuple[CanonKey, ...]:
    """All result classes of the actual bounded minimum computation."""
    result = min_responses(base, target, measure, Bounds(2, 2))
    if result is None:
        return ()
    return tuple(sorted({canonical(replay((Impose(*target),) + delta_events(base, delta), base))
                         for delta in result.deltas}))


def branch_widths() -> list[dict[str, Any]]:
    rows = []
    for reading in (READING_L, READING_F):
        base = replay(reading.genesis)
        for measure in ("mu1", "mu2"):
            result = min_responses(base, reading.target, measure, Bounds(2, 2))
            require(result is not None, "original target has a bounded response")
            if result is None:
                raise AuditFailure("missing response")
            rows.append({"reading": reading.name, "measure": measure,
                         "raw_minima": len(result.deltas),
                         "result_classes": len(minimum_keys(base, reading.target, measure)),
                         "cost": list(result.cost)})
    return rows


def normalized_records(tree: Tree, start: int) -> tuple[Counter[str], Counter[str]]:
    """Full exported node/edge multisets, with local IDs and depth normalized.

    Membership is the reachable node-id set. Selecting by canonical-key
    membership instead would admit any unreachable node that happened to share
    a class with a descendant, so the comparison would range over a population
    that is not the subtree it names. That the two currently coincide is a
    property of this engine, not of this function, and it is not assumed here.
    """
    reachable = set(descendant_nodes(tree, start))
    offset = tree.nodes[start].depth
    nodes: Counter[str] = Counter()
    edges: Counter[str] = Counter()
    for nid in sorted(reachable):
        node = tree.nodes[nid]
        payload = node_json(node)
        payload["id"] = node.canon
        payload["depth"] = node.depth - offset
        payload["regime"] = regime_json(node.regime)
        payload["history"] = [event_json(event) for event in node.history]
        nodes[json.dumps(payload, sort_keys=True)] += 1
    for edge in tree.edges:
        if edge.parent not in reachable:
            continue
        payload = edge_json(tree, edge)
        payload["parent"] = tree.nodes[edge.parent].canon
        payload["child"] = tree.nodes[edge.child].canon
        payload["round"] = edge.round_no - offset
        edges[json.dumps(payload, sort_keys=True)] += 1
    return nodes, edges


def restart_witness(original: Tree) -> tuple[Tree, dict[str, Any]]:
    """A concrete compatible root, not an automatic queue checkpoint API."""
    node = original.nodes[2]
    targets = closure_challenge_orbits(node.regime)
    require(node.depth == 2 and targets == ((1, 2),), "compatible intermediate node")
    restart = build_tree(Reading("local", "declared intermediate request", node.history, targets[0]),
                         original.measure, original.bounds,
                         original.max_rounds - node.depth,
                         original.pre_expansion_node_guard, original.supply)
    old_keys = descendant_keys(original, node.node_id)
    new_keys = descendant_keys(restart, 0)
    require(old_keys == new_keys, "bounded restart descendant classes")
    require(normalized_records(original, node.node_id) == normalized_records(restart, 0),
            "bounded restart complete exported-record correspondence")
    return restart, {"original_node": node.node_id, "original_depth": node.depth,
                     "remaining_rounds": original.max_rounds - node.depth,
                     "target": list(targets[0]), "descendant_classes": len(old_keys),
                     "same_transition_records": True, "scope": "this declared finite run"}


def phase_reset_witness(original: Tree) -> dict[str, Any]:
    node = original.nodes[1]
    require(not closure_challenge_orbits(node.regime), "separated intermediate state")
    restarted = build_tree(Reading("reset", "reissue old target", node.history, (0, 1)),
                           "mu2", Bounds(2, 2), 2, 250, True)
    original_moves = [e.challenge for e in original.edges if e.parent == node.node_id]
    restarted_moves = [e.challenge for e in restarted.edges if e.parent == 0]
    require(original_moves == ["supply"] and restarted_moves == ["separate(0, 1)"],
            "root target differs from continuation policy")
    require(len(restarted.nodes) == 1 and restarted.edges[0].kind == "merge",
            "empty response merges to the new root")
    return {"original_moves": original_moves, "restarted_moves": restarted_moves,
            "restart_stats": restarted.stats(), "export_replays": verify_full_export(tree_full_json(restarted)),
            "refuted": "fresh driver call always equals the original suffix"}


def name_collision_witness() -> dict[str, Any]:
    occupied = replay((AdmitDatum("w2"), AdmitDatum("b")))
    fresh = replay((AdmitDatum("x"), AdmitDatum("b")))
    require(canonical(occupied) == canonical(fresh), "same initial structural key")
    left = apply_delta(occupied, (NewDatum(),))
    right = apply_delta(fresh, (NewDatum(),))
    require(left == occupied and right.n_data() == 3, "generated candidate name collision")
    history: tuple[Event, ...] = (AdmitDatum("g2"), AdmitDatum("b"))
    supplied = build_tree(Reading("occupied", "existing generated name", history, (0, 1)),
                          "mu2", Bounds(2, 2), 3, 250, True)
    last = supplied.edges[-1]
    require(last.challenge == "supply" and last.parent == last.child,
            "generated supply name collision")
    return {"same_initial_key": True, "after_new_datum_counts": [left.n_data(), right.n_data()],
            "same_final_key": canonical(left) == canonical(right),
            "supply_stats": supplied.stats(), "supply_self_merge": [last.parent, last.child],
            "export_replays": verify_full_export(tree_full_json(supplied)),
            "refuted": "structural equality alone ensures fresh generated names"}


def domain_witnesses() -> dict[str, Any]:
    base = replay(READING_L.genesis)
    absent = [min_responses(base, (0, 1), "mu2", Bounds(n, 2)) is None for n in (0, 1)]
    require(all(absent), "absence below the declared two-item response")
    require(min_responses(base, (0, 1), "mu2", Bounds(2, 2)) is not None,
            "larger bound supplies a response")
    history: tuple[Event, ...] = (AdmitDatum("a"), AdmitDatum("b"), AdmitForm(1), AdmitRuleAll(0))
    rule_base = replay(history)
    require((0, 1) in collapsed_pairs(rule_base), "rule-bearing base has a collapsed pair")
    try:
        build_tree(Reading("rules", "reachable rule-bearing state", history, (0, 1)),
                   "mu2", Bounds(2, 2), 1)
    except ValueError as exc:
        refusal = str(exc)
    else:
        raise AuditFailure("rule-bearing base unexpectedly accepted")
    symmetric = tuple(AdmitDatum(f"d{i}") for i in range(9))
    try:
        build_tree(Reading("budget", "symmetric state", symmetric, (0, 1)),
                   "mu2", Bounds(2, 2), 0)
    except IsoBudgetError as exc:
        budget = str(exc)
    else:
        raise AuditFailure("default permutation budget unexpectedly accepted")
    guarded = build_tree(READING_L, "mu1", Bounds(2, 2), 7, 1, True)
    require(len(guarded.nodes) == 4, "pre-expansion guard is not a strict node cap")
    return {"no_response_at_item_bounds": [0, 1], "response_at_item_bound": 2,
            "rule_base": regime_json(rule_base), "rule_base_refusal": refusal,
            "permutation_budget_refusal_at_zero_rounds": budget,
            "guard_one_stats": guarded.stats(),
            "absence_scope": "supplied candidate bounds only"}


def transport_witness(original: Tree) -> dict[str, Any]:
    base = original.nodes[2].regime
    image = rename(base, (2, 0, 1), tuple(range(len(base.forms))))
    before = minimum_keys(base, (1, 2), "mu2")
    after = minimum_keys(image, (0, 1), "mu2")
    require(canonical(base) == canonical(image), "complete-state renaming")
    require(before == after, "finite renamed minimum class correspondence")
    return {"datum_bijection": [2, 0, 1], "source_target": [1, 2],
            "image_target": [0, 1], "source_requirements": sorted(base.reqs),
            "image_requirements": sorted(image.reqs), "same_result_classes": len(before),
            "scope": "this full-state bijection and the declared bounds"}


def multiple_challenges_witness() -> dict[str, Any]:
    history: tuple[Event, ...] = tuple(AdmitDatum(f"a{i}") for i in range(4)) + (
        AdmitForm(1), AdmitInst(0, (0,)), AdmitInst(0, (1,)))
    base = replay(history)
    targets = closure_challenge_orbits(base)
    require(targets == ((0, 1), (2, 3)), "two distinct closure challenge orbits")
    tree = build_tree(Reading("multiple", "one imposed root target", history, targets[0]),
                      "mu2", Bounds(2, 2), 1)
    moves = sorted({edge.challenge for edge in tree.edges if edge.parent == 0})
    require(moves == ["separate(0, 1)"], "one supplied target is not the whole closure policy")
    return {"closure_targets": targets, "fresh_root_moves": moves}


def evidence() -> dict[str, Any]:
    opened = sample(supply=True)
    closed = sample(supply=False)
    local, restart = restart_witness(opened)
    require(opened.stats()["max_depth"] == 7, "seven-round open example")
    require(closed.stats()["max_depth"] == 1, "closed example stops before round seven")
    require(separable(closed.nodes[-1].regime, 0, 1), "closed result answers the supplied separation")
    return {"schema_version": 1, "classification": "deterministic computation",
            "authority_effect": "None", "source_commit": BASELINE_COMMIT,
            "request": {"rounds": 7, "item_bound": 2, "arity_bound": 2, "node_guard": 250},
            "open_run": {"stats": opened.stats(), "replay_checks": replay_cuts(opened)},
            "closed_run": {"stats": closed.stats(), "replay_checks": replay_cuts(closed)},
            "restart": restart, "restart_replay_checks": replay_cuts(local),
            "branch_widths": branch_widths(), "phase_reset": phase_reset_witness(opened),
            "name_collisions": name_collision_witness(), "domain_limits": domain_witnesses(),
            "full_state_transport": transport_witness(opened),
            "multiple_challenges": multiple_challenges_witness(),
            "trees": {"open": tree_full_json(opened), "closed": tree_full_json(closed),
                      "restarted": tree_full_json(local)},
            "universal_python_refinement": "NOT_PROVED",
            "arbitrary_problem_encoding": "OPEN",
            "automatic_representation_or_carrier_repair": "NOT_ESTABLISHED",
            "undecidability": "NOT_PROVED"}
