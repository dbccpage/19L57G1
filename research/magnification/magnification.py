"""The sealed exports against the engine's class, and the restart and
magnification experiments — all through the sealed kernel.

AuthorityEffect: None.  Nothing here is a new primitive.  Every regime is the
sealed ``replay`` of a certified history; every demand is the sealed
``closure_challenge_orbits``; every response family is the sealed
``min_responses``; every quotient key is the sealed ``canonical``.

Three checks, one per bridge:

1. **Engine class.**  For each of the six exports: the sealed certification;
   every node's status re-derived from the engine's own decision order
   (targets, the round bound, the node guard, supply); at every expanded
   node the exported fan equals the fan the relation demands — one edge per
   orbit demand and per minimum class, a supply edge exactly when quiet, the
   seed target at the root — with the recorded costs, tie counts and class
   sizes; the completeness depth below which every fire-maximal history
   lands on an exported node.  Orbit demands are re-derived a second way on
   small nodes: automorphisms by brute force over every bijection pair.
2. **Restart.**  Two-step reachable classes from a node, recomputed from the
   node alone, against the classes two edges away in the exported DAG (a
   merge edge lands on the isomorphism representative and continues from
   it): equivariance of the quotient, tested on every node whose two-step
   neighbourhood is expanded.
3. **Magnification.**  At every exported round: the seed's three first-round
   responses remain valid at the target; the exported minimum is one item
   wherever an existing form serves; the share of rounds where context
   cheapens the minimum below the seed's cost of two.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from pathlib import Path
from typing import Iterable, Mapping, Optional, Sequence, cast

from derivation.candidates import (
    Bounds,
    Delta,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    delta_events,
    min_responses,
    response_valid_naive,
)
from derivation.engine import READING_F, READING_L, Reading, closure_challenge_orbits
from derivation.export import Json, event_from_json, read_json_gz, regime_sha256, verify_full_export
from derivation.iso import CanonKey, canonical, serialize
from derivation.model import AdmitDatum, Event, Impose, Pair, Regime, Supply, replay
from derivation.observe import collapsed_pairs, separable

JsonDict = dict[str, Json]
EXPORTS: tuple[str, ...] = ("closed_L", "closed_F", "tree_L_mu1", "tree_L_mu2", "tree_F_mu1", "tree_F_mu2")
READINGS: Mapping[str, Reading] = {"L": READING_L, "F": READING_F}


class ClassError(ValueError):
    """A named failure of an export against the relation."""


# ---------------------------------------------------------------------------
# Reconstruction
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Export:
    name: str
    reading: Reading
    measure: str
    bounds: Bounds
    max_rounds: int
    guard: int
    supply: bool
    nodes: tuple[Mapping[str, Json], ...]
    edges: tuple[Mapping[str, Json], ...]
    regimes: dict[int, Regime]
    histories: dict[int, tuple[Event, ...]]


def load(root: Path, name: str) -> Export:
    payload = cast(Mapping[str, Json], read_json_gz(root / "artifacts" / "full" / f"{name}.json.gz"))
    if not verify_full_export(payload):
        raise ClassError(f"{name}: the sealed certification failed")
    reading = READINGS[cast(str, payload["reading"])]
    bounds_json = cast(Mapping[str, Json], payload["bounds"])
    bounds = Bounds(cast(int, bounds_json["max_items"]), cast(int, bounds_json["max_arity"]))
    root_history = tuple(event_from_json(cast(Mapping[str, Json], e))
                         for e in cast(Sequence[Json], payload["root_history"]))
    nodes = tuple(cast(Sequence[Mapping[str, Json]], payload["nodes"]))
    edges = tuple(cast(Sequence[Mapping[str, Json]], payload["edges"]))
    histories: dict[int, tuple[Event, ...]] = {0: root_history}
    creation = {cast(int, e["child"]): e for e in edges if e["kind"] == "creation"}
    for node in nodes:
        nid = cast(int, node["id"])
        if nid == 0:
            continue
        edge = creation[nid]
        parent = cast(int, edge["parent"])
        events = tuple(event_from_json(cast(Mapping[str, Json], e))
                       for e in cast(Sequence[Json], edge["events"]))
        histories[nid] = histories[parent] + events
    regimes = {nid: replay(h) for nid, h in histories.items()}
    for node in nodes:
        nid = cast(int, node["id"])
        if regime_sha256(regimes[nid]) != node["regime_sha256"]:
            raise ClassError(f"{name} node {nid}: replayed regime hash differs from the record")
    if tuple(regimes[0].reqs) != ():
        raise ClassError(f"{name}: the root carries a requirement")
    return Export(name, reading, cast(str, payload["measure"]), bounds, cast(int, payload["max_rounds"]),
                  cast(int, payload["pre_expansion_node_guard"]), bool(payload["supply_enabled"]),
                  nodes, edges, regimes, histories)


# ---------------------------------------------------------------------------
# 1. The engine class: statuses and fans re-derived
# ---------------------------------------------------------------------------


def delta_from_json(items: Sequence[Json]) -> Delta:
    out: list[NewDatum | NewForm | NewInst | NewRuleAll] = []
    for raw in items:
        item = cast(Mapping[str, Json], raw)
        kind = item["kind"]
        if kind == "datum":
            out.append(NewDatum())
        elif kind == "form":
            out.append(NewForm(cast(int, item["arity"])))
        elif kind == "rule_all":
            out.append(NewRuleAll(cast(int, item["form"])))
        else:
            out.append(NewInst(cast(int, item["form"]), tuple(cast(Sequence[int], item["args"]))))
    return tuple(out)


def parse_target(challenge: str) -> Pair:
    i, j = challenge.removeprefix("separate(").removesuffix(")").split(", ")
    return (int(i), int(j))


def expected_status(ex: Export, nid: int, nodes_before: int) -> str:
    """The engine's decision order at a popped node, replayed."""
    r = ex.regimes[nid]
    depth = cast(int, ex.nodes[nid]["depth"])
    targets = (ex.reading.target,) if nid == 0 else closure_challenge_orbits(r)
    if not targets and not ex.supply:
        return "terminal_all_separated"
    if depth >= ex.max_rounds:
        return "completed"
    if nodes_before > ex.guard:
        return "frontier_guard"
    return "expanded"


def classes_of(r: Regime, target: Pair, deltas: Sequence[Delta]) -> dict[CanonKey, list[Delta]]:
    grouped: dict[CanonKey, list[Delta]] = {}
    for delta in deltas:
        child = replay((Impose(*target),) + delta_events(r, delta), r)
        grouped.setdefault(canonical(child), []).append(delta)
    return grouped


def check_export(ex: Export) -> JsonDict:
    """Every node's status and every expanded node's fan against the relation."""
    out_edges: dict[int, list[Mapping[str, Json]]] = {}
    for e in ex.edges:
        out_edges.setdefault(cast(int, e["parent"]), []).append(e)
    created_by: dict[int, int] = {}
    for e in ex.edges:
        if e["kind"] == "creation":
            created_by[cast(int, e["child"])] = cast(int, e["parent"])
    failures: list[str] = []
    fans = 0
    rounds = 0
    supplies = 0
    minima_agree = 0
    status_counts: dict[str, int] = {}
    depth_complete: Optional[int] = None
    cutoff_depths: list[int] = []
    for node in ex.nodes:
        nid = cast(int, node["id"])
        nodes_before = 1 + sum(1 for child, parent in created_by.items() if parent < nid)
        status = cast(str, node["status"])
        status_counts[status] = status_counts.get(status, 0) + 1
        expect = expected_status(ex, nid, nodes_before)
        if expect != status:
            failures.append(f"{ex.name} node {nid}: status {status!r}, the engine's order gives {expect!r}")
            continue
        edges = out_edges.get(nid, [])
        if status != "expanded":
            if edges:
                failures.append(f"{ex.name} node {nid}: {status!r} node has {len(edges)} edges")
            if status in ("completed", "frontier_guard"):
                cutoff_depths.append(cast(int, node["depth"]))
            continue
        r = ex.regimes[nid]
        targets = (ex.reading.target,) if nid == 0 else closure_challenge_orbits(r)
        if not targets:
            supplies += 1
            if len(edges) != 1 or edges[0]["challenge"] != "supply":
                failures.append(f"{ex.name} node {nid}: quiet node without exactly one supply edge")
                continue
            child = ex.regimes[cast(int, edges[0]["child"])]
            token = f"g{r.n_data()}"
            grown = replay((Supply(token), AdmitDatum(token)), r)
            if canonical(child) != canonical(grown):
                failures.append(f"{ex.name} node {nid}: supply edge lands off the grown class")
            continue
        fans += 1
        expected: dict[tuple[Pair, CanonKey], tuple[int, int, tuple[int, int]]] = {}
        for target in targets:
            mr = min_responses(r, target, ex.measure, ex.bounds)
            if mr is None:
                failures.append(f"{ex.name} node {nid}: no response to {target} within bounds")
                continue
            grouped = classes_of(r, target, mr.deltas)
            cost = (mr.cost[0], mr.cost[1]) if ex.measure == "mu2" else (mr.cost[0], -1)
            for key, members in grouped.items():
                expected[(target, key)] = (len(grouped), len(members), cost)
        seen: set[tuple[Pair, CanonKey]] = set()
        for e in edges:
            if e["challenge"] == "supply":
                failures.append(f"{ex.name} node {nid}: supply edge at a node with demands")
                continue
            rounds += 1
            target = parse_target(cast(str, e["challenge"]))
            delta = delta_from_json(cast(Sequence[Json], e["response"]))
            child = replay((Impose(*target),) + delta_events(r, delta), r)
            key = canonical(child)
            if (target, key) not in expected:
                failures.append(f"{ex.name} edge {nid}->{e['child']}: response is not a minimum class at {target}")
                continue
            tie_classes, class_size, cost = expected[(target, key)]
            if (cast(int, e["tie_classes"]), cast(int, e["class_size"]), tuple(cast(Sequence[int], e["cost"]))) != (tie_classes, class_size, cost):
                failures.append(f"{ex.name} edge {nid}->{e['child']}: recorded ties/size/cost differ")
                continue
            if cast(int, e["orbits"]) != len(targets):
                failures.append(f"{ex.name} edge {nid}->{e['child']}: recorded orbit count differs")
                continue
            if key != canonical(ex.regimes[cast(int, e["child"])]):
                failures.append(f"{ex.name} edge {nid}->{e['child']}: child is not the class representative")
                continue
            if not response_valid_naive(r, target, delta):
                failures.append(f"{ex.name} edge {nid}->{e['child']}: response fails the reference validity check")
                continue
            minima_agree += 1
            seen.add((target, key))
        missing = set(expected) - seen
        if missing:
            failures.append(f"{ex.name} node {nid}: {len(missing)} minimum classes have no edge (dropped ties)")
    first_cutoff = min(cutoff_depths) if cutoff_depths else None
    if first_cutoff is None:
        depth_complete = max(cast(int, n["depth"]) for n in ex.nodes)
    else:
        depth_complete = first_cutoff
    return {
        "nodes": len(ex.nodes),
        "edges": len(ex.edges),
        "statuses": dict(sorted(status_counts.items())),
        "fans_checked": fans,
        "rounds_checked": rounds,
        "rounds_minimum_and_representative": minima_agree,
        "supplies_checked": supplies,
        "completeness_depth": depth_complete,
        "first_cutoff_depth": first_cutoff,
        "failures": failures,
    }


# ---------------------------------------------------------------------------
# Orbit demands re-derived by brute force
# ---------------------------------------------------------------------------


def brute_automorphisms(r: Regime) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    n, nf = r.n_data(), len(r.forms)
    identity = serialize(r, tuple(range(n)), tuple(range(nf)))
    return [(pi, phi) for pi in permutations(range(n)) for phi in permutations(range(nf))
            if serialize(r, pi, phi) == identity]


def brute_orbit_demands(r: Regime) -> tuple[Pair, ...]:
    autos = brute_automorphisms(r)
    remaining = set(collapsed_pairs(r))
    reps: list[Pair] = []
    for pair in sorted(collapsed_pairs(r)):
        if pair not in remaining:
            continue
        orbit = {(min(pi[pair[0]], pi[pair[1]]), max(pi[pair[0]], pi[pair[1]])) for (pi, _) in autos}
        orbit &= remaining
        remaining -= orbit
        reps.append(min(orbit))
    return tuple(reps)


def brute_orbit_check(ex: Export, max_data: int = 5, max_forms: int = 3) -> JsonDict:
    checked = 0
    disagreements: list[str] = []
    automorphism_counts: dict[str, int] = {}
    for nid, r in sorted(ex.regimes.items()):
        if r.n_data() > max_data or len(r.forms) > max_forms:
            continue
        checked += 1
        count = len(brute_automorphisms(r))
        automorphism_counts[str(count)] = automorphism_counts.get(str(count), 0) + 1
        if brute_orbit_demands(r) != closure_challenge_orbits(r):
            disagreements.append(f"{ex.name} node {nid}")
    return {"nodes_checked": checked, "max_data": max_data, "max_forms": max_forms,
            "automorphism_count_histogram": dict(sorted(automorphism_counts.items(), key=lambda kv: int(kv[0]))),
            "disagreements": disagreements}


# ---------------------------------------------------------------------------
# 2. Restart: two-step classes recomputed against the exported DAG
# ---------------------------------------------------------------------------


def successor_classes(ex: Export, r: Regime, is_root: bool) -> set[CanonKey]:
    targets = (ex.reading.target,) if is_root else closure_challenge_orbits(r)
    if not targets:
        if not ex.supply:
            return set()
        token = f"g{r.n_data()}"
        return {canonical(replay((Supply(token), AdmitDatum(token)), r))}
    out: set[CanonKey] = set()
    for target in targets:
        mr = min_responses(r, target, ex.measure, ex.bounds)
        if mr is None:
            raise ClassError("no response within bounds")
        out |= set(classes_of(r, target, mr.deltas))
    return out


def restart_check(ex: Export) -> JsonDict:
    """For every expanded node whose children are all expanded: the classes
    two engine steps away, recomputed from the node's regime alone, equal
    the classes two edges away in the exported DAG."""
    out_edges: dict[int, list[int]] = {}
    for e in ex.edges:
        out_edges.setdefault(cast(int, e["parent"]), []).append(cast(int, e["child"]))
    status = {cast(int, n["id"]): cast(str, n["status"]) for n in ex.nodes}
    keys = {nid: canonical(r) for nid, r in ex.regimes.items()}
    checked = 0
    failures: list[str] = []
    cache: dict[int, set[CanonKey]] = {}

    def successors(node: int) -> set[CanonKey]:
        if node not in cache:
            cache[node] = successor_classes(ex, ex.regimes[node], node == 0)
        return cache[node]

    for nid, children in sorted(out_edges.items()):
        if status[nid] != "expanded" or any(status[c] != "expanded" for c in children):
            continue
        dag_two = {keys[g] for c in children for g in out_edges.get(c, [])}
        recomputed: set[CanonKey] = set()
        for child_key in successors(nid):
            # the child's own regime: the exported representative of its class
            rep = next(c for c in children if keys[c] == child_key)
            recomputed |= successors(rep)
        checked += 1
        if dag_two != recomputed:
            failures.append(f"{ex.name} node {nid}: two-step classes differ "
                            f"(dag {len(dag_two)}, recomputed {len(recomputed)})")
    return {"nodes_checked": checked, "failures": failures}


def restart_from_node(ex: Export, nid: int, rounds: int) -> JsonDict:
    """Restart the class at one exported node with its complete regime and
    run `rounds` fire-maximal engine steps, quotiented by isomorphism; then
    read the same depths off the exported DAG.  Equal class sets at every
    depth is the fractal statement, tested on one node."""
    out_edges: dict[int, list[int]] = {}
    for e in ex.edges:
        out_edges.setdefault(cast(int, e["parent"]), []).append(cast(int, e["child"]))
    keys = {n: canonical(r) for n, r in ex.regimes.items()}
    status = {cast(int, n["id"]): cast(str, n["status"]) for n in ex.nodes}
    rep_of: dict[CanonKey, int] = {}
    for n in sorted(keys):
        rep_of.setdefault(keys[n], n)
    frontier: dict[CanonKey, Regime] = {keys[nid]: ex.regimes[nid]}
    dag_frontier: set[int] = {nid}
    layers: list[Json] = []
    for depth in range(1, rounds + 1):
        next_frontier: dict[CanonKey, Regime] = {}
        for key, r in frontier.items():
            targets = closure_challenge_orbits(r)
            if not targets:
                if ex.supply:
                    token = f"g{r.n_data()}"
                    child = replay((Supply(token), AdmitDatum(token)), r)
                    next_frontier.setdefault(canonical(child), child)
                continue
            for target in targets:
                mr = min_responses(r, target, ex.measure, ex.bounds)
                assert mr is not None
                for ckey, members in classes_of(r, target, mr.deltas).items():
                    child = replay((Impose(*target),) + delta_events(r, members[0]), r)
                    next_frontier.setdefault(ckey, child)
        if any(status[n] != "expanded" for n in dag_frontier):
            layers.append({"depth": depth, "recomputed_classes": len(next_frontier),
                           "dag_incomplete": True})
            break
        dag_next = {rep_of[keys[c]] for n in dag_frontier for c in out_edges.get(n, [])}
        dag_keys = {keys[n] for n in dag_next}
        layers.append({"depth": depth, "recomputed_classes": len(next_frontier),
                       "dag_classes": len(dag_keys), "equal": set(next_frontier) == dag_keys})
        frontier = next_frontier
        dag_frontier = dag_next
    return {"node": nid, "node_depth": cast(int, ex.nodes[nid]["depth"]), "rounds": rounds, "layers": layers}


# ---------------------------------------------------------------------------
# 3. Magnification: the seed's responses at every exported round
# ---------------------------------------------------------------------------


def seed_responses(r: Regime, i: int, j: int) -> tuple[Delta, Delta, Delta]:
    f = len(r.forms)
    return ((NewForm(1), NewInst(f, (i,))), (NewForm(2), NewInst(f, (i, j))), (NewForm(2), NewInst(f, (i, i))))


def magnification_check(ex: Export) -> JsonDict:
    rounds = 0
    embeds = 0
    one_item = 0
    two_item = 0
    seed_min = 0
    cheaper = 0
    for e in ex.edges:
        if e["challenge"] == "supply" or e["kind"] != "creation":
            continue
        rounds += 1
        parent = ex.regimes[cast(int, e["parent"])]
        target = parse_target(cast(str, e["challenge"]))
        delta = delta_from_json(cast(Sequence[Json], e["response"]))
        if all(response_valid_naive(parent, target, d) for d in seed_responses(parent, *target)):
            embeds += 1
        if len(delta) == 1:
            one_item += 1
        else:
            two_item += 1
        mr = min_responses(parent, target, ex.measure, ex.bounds)
        assert mr is not None
        seeds = set(seed_responses(parent, *target))
        if seeds & set(mr.deltas):
            seed_min += 1
        if mr.cost[0] < 2:
            cheaper += 1
    return {"creation_rounds": rounds, "seed_responses_valid": embeds,
            "one_item_minima": one_item, "two_item_minima": two_item,
            "rounds_with_a_seed_response_among_the_minima": seed_min,
            "rounds_cheaper_than_the_seed": cheaper}


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


def census(root: Path) -> JsonDict:
    exports: JsonDict = {}
    totals = {"nodes": 0, "edges": 0, "fans": 0, "rounds": 0, "minima": 0, "supplies": 0, "failures": 0}
    for name in EXPORTS:
        ex = load(root, name)
        engine = check_export(ex)
        orbits = brute_orbit_check(ex)
        restart = restart_check(ex)
        magnified = magnification_check(ex)
        exports[name] = {"reading": ex.reading.name, "measure": ex.measure, "supply": ex.supply,
                         "max_rounds": ex.max_rounds, "guard": ex.guard,
                         "engine_class": engine, "orbit_brute_force": orbits,
                         "restart_two_step": restart, "magnification": magnified}
        totals["nodes"] += cast(int, engine["nodes"])
        totals["edges"] += cast(int, engine["edges"])
        totals["fans"] += cast(int, engine["fans_checked"])
        totals["rounds"] += cast(int, engine["rounds_checked"])
        totals["minima"] += cast(int, engine["rounds_minimum_and_representative"])
        totals["supplies"] += cast(int, engine["supplies_checked"])
        totals["failures"] += len(cast(list[str], engine["failures"])) + len(cast(list[str], orbits["disagreements"])) + len(cast(list[str], restart["failures"]))
    ex = load(root, "tree_L_mu2")
    samples: list[Json] = [restart_from_node(ex, nid, 4) for nid in (1, 2, 3)]
    root_f = replay(READING_F.genesis)
    return {
        "schema": "magnification-census-v1",
        "authority_effect": "None",
        "totals": totals,
        "exports": exports,
        "restart_samples": {"export": "tree_L_mu2", "runs": samples},
        "root_orbit_demands": {
            "L": [list(p) for p in closure_challenge_orbits(replay(READING_L.genesis))],
            "F": [list(p) for p in closure_challenge_orbits(root_f)],
            "F_seed_target": list(READING_F.target),
            "F_seed_is_orbit_representative": READING_F.target in closure_challenge_orbits(root_f),
        },
    }


__all__ = ["EXPORTS", "ClassError", "Export", "load", "check_export", "brute_orbit_check",
           "restart_check", "restart_from_node", "magnification_check", "census",
           "seed_responses", "delta_from_json", "parse_target", "classes_of", "expected_status",
           "brute_automorphisms", "brute_orbit_demands", "successor_classes"]
