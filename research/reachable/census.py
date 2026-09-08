"""Replay every exported tower node and check the reachable-state invariants.

Classification: metatheory apparatus.  AuthorityEffect: None.

The six committed full exports under ``artifacts/full/`` are read and never
written.  For each export, in this order:

1. the sealed certification ``verify_full_export`` is run;
2. every node's regime is rebuilt by replaying its creation history from
   genesis and compared with the recorded regime hash;
3. the four invariants proved in ``lean/Reachable.lean`` are checked on every
   node: rule-free, well-formed, every standing requirement answered, every
   admitted form carrying an instance;
4. every edge is checked: a supply edge admits exactly one fresh datum; a
   round edge names a collapsed, fresh target and carries a response inside
   the declared bounds that the sealed ``min_responses`` enumeration, re-run
   on the parent, returns as one of its minima at the recorded cost;
5. the isomorphism-class census per depth is recomputed with the sealed
   canonical keys, and every node must be its own class.

Two states the Lean development proves unreachable are then compared with
every exported node, and the nearest exported node is recorded with its
replay certificate.

The output ``reachable.json`` is deterministic: sorted keys, no timestamps,
no environment data.  Any named failure raises ``CensusError``; nothing is
reported as a count when it should be reported as a name.

Usage::

    python census.py --write     regenerate reachable.json
    python census.py --check     recompute and compare byte for byte
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Mapping, Sequence, cast

ROOT = Path(__file__).resolve().parents[2]
PACKET = Path(__file__).resolve().parent
OUTPUT = PACKET / "reachable.json"
SCHEMA = "reachable-census-v1"

if str(ROOT / "code") not in sys.path:
    sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import (  # noqa: E402
    Bounds,
    Delta,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    canonical_delta,
    min_responses,
)
from derivation.export import (  # noqa: E402
    Json,
    event_from_json,
    event_json,
    read_json_gz,
    regime_json,
    regime_sha256,
    verify_full_export,
)
from derivation.iso import CanonKey, canonical  # noqa: E402
from derivation.model import AdmitDatum, Event, Pair, Regime, Supply, replay  # noqa: E402
from derivation.observe import collapsed_pairs, separable  # noqa: E402

EXPORTS = ("closed_L", "closed_F", "tree_L_mu1", "tree_L_mu2", "tree_F_mu1", "tree_F_mu2")
INVARIANTS = ("rule_free", "well_formed", "answered", "forms_used")

JsonDict = dict[str, object]


class CensusError(ValueError):
    """A named failure: the message says which node, edge or state failed."""


# ---------------------------------------------------------------------------
# The invariants, as decided on a regime
# ---------------------------------------------------------------------------


def rule_free(r: Regime) -> bool:
    return not r.rules


def well_formed(r: Regime) -> bool:
    n = r.n_data()
    if any(a < 1 for a in r.forms):
        return False
    for form, args in r.insts:
        if not (0 <= form < len(r.forms)):
            return False
        if len(args) != r.forms[form]:
            return False
        if any(not (0 <= a < n) for a in args):
            return False
    if any(not (0 <= f < len(r.forms)) for f in r.rules):
        return False
    return all(0 <= i < j < n for (i, j) in r.reqs)


def answered(r: Regime) -> bool:
    return all(separable(r, i, j) for (i, j) in r.reqs)


def forms_used(r: Regime) -> bool:
    used = {form for (form, _) in r.insts}
    return all(f in used for f in range(len(r.forms)))


def fixpoint(r: Regime) -> bool:
    n = r.n_data()
    return all((i, j) in r.reqs for i in range(n) for j in range(i + 1, n))


def invariants(r: Regime) -> dict[str, bool]:
    return {
        "rule_free": rule_free(r),
        "well_formed": well_formed(r),
        "answered": answered(r),
        "forms_used": forms_used(r),
    }


def within_arity(r: Regime, bounds: Bounds) -> bool:
    return all(a <= bounds.max_arity for a in r.forms)


# ---------------------------------------------------------------------------
# Reading an export
# ---------------------------------------------------------------------------


def _events(raw: object) -> tuple[Event, ...]:
    return tuple(event_from_json(cast(Mapping[str, Json], e)) for e in cast(Sequence[object], raw))


def reconstruct(name: str, payload: Mapping[str, object]) -> tuple[dict[int, tuple[Event, ...]], dict[int, Regime]]:
    """Histories and regimes of every node along creation edges, each regime
    checked against the recorded hash.  Independent of the sealed
    certification, which is run separately."""
    nodes = cast(Sequence[Mapping[str, object]], payload["nodes"])
    edges = cast(Sequence[Mapping[str, object]], payload["edges"])
    histories: dict[int, tuple[Event, ...]] = {0: _events(payload["root_history"])}
    regimes: dict[int, Regime] = {0: replay(histories[0])}
    creation: dict[int, Mapping[str, object]] = {}
    for edge in edges:
        if edge["kind"] == "creation":
            child = cast(int, edge["child"])
            if child in creation:
                raise CensusError(f"{name} node {child}: two creation edges")
            creation[child] = edge
    for node in nodes:
        nid = cast(int, node["id"])
        if nid != 0:
            if nid not in creation:
                raise CensusError(f"{name} node {nid}: no creation edge")
            edge = creation[nid]
            parent = cast(int, edge["parent"])
            histories[nid] = histories[parent] + _events(edge["events"])
            regimes[nid] = replay(histories[nid])
        if regime_sha256(regimes[nid]) != node["regime_sha256"]:
            raise CensusError(f"{name} node {nid}: replayed regime hash differs from the record")
    return histories, regimes


def delta_from_json(raw: object) -> Delta:
    items: list[NewDatum | NewForm | NewInst | NewRuleAll] = []
    for entry in cast(Sequence[Mapping[str, object]], raw):
        kind = entry["kind"]
        if kind == "datum":
            items.append(NewDatum())
        elif kind == "form":
            items.append(NewForm(cast(int, entry["arity"])))
        elif kind == "inst":
            items.append(NewInst(cast(int, entry["form"]), tuple(cast(Sequence[int], entry["args"]))))
        elif kind == "rule_all":
            items.append(NewRuleAll(cast(int, entry["form"])))
        else:
            raise CensusError(f"unknown response item kind {kind!r}")
    return tuple(items)


def in_bounds(delta: Delta, bounds: Bounds) -> bool:
    if len(delta) > bounds.max_items:
        return False
    return all(it.arity <= bounds.max_arity for it in delta if isinstance(it, NewForm))


def parse_target(challenge: str) -> Pair:
    inner = challenge.removeprefix("separate(").removesuffix(")")
    i, j = inner.split(", ")
    return (int(i), int(j))


# ---------------------------------------------------------------------------
# The checks
# ---------------------------------------------------------------------------


def node_failures(name: str, regimes: Mapping[int, Regime]) -> list[str]:
    """Every invariant that fails on any node, naming the node."""
    failures: list[str] = []
    for nid in sorted(regimes):
        verdicts = invariants(regimes[nid])
        for key in INVARIANTS:
            if not verdicts[key]:
                failures.append(f"{name} node {nid}: invariant {key} fails")
    return failures


def edge_failures(name: str, payload: Mapping[str, object], regimes: Mapping[int, Regime],
                  measure: str, bounds: Bounds) -> tuple[list[str], dict[str, int]]:
    """Every edge that is not a supply of one fresh datum or a shortest valid
    response to a collapsed fresh target, naming the edge."""
    failures: list[str] = []
    counts = {"supply": 0, "rounds": 0, "minimum_agreements": 0, "collapsed_targets": 0,
              "fresh_targets": 0, "creation": 0, "merge": 0}
    for edge in cast(Sequence[Mapping[str, object]], payload["edges"]):
        parent = cast(int, edge["parent"])
        child = cast(int, edge["child"])
        label = f"{name} edge {parent}->{child}"
        kind = cast(str, edge["kind"])
        if kind in counts:
            counts[kind] += 1
        base = regimes[parent]
        events = _events(edge["events"])
        challenge = cast(str, edge["challenge"])
        response = delta_from_json(edge["response"])
        if challenge == "supply":
            counts["supply"] += 1
            token = f"g{base.n_data()}"
            if events != (Supply(token), AdmitDatum(token)) or response:
                failures.append(f"{label}: supply edge does not admit exactly one fresh datum")
            continue
        counts["rounds"] += 1
        target = parse_target(challenge)
        if target in collapsed_pairs(base):
            counts["collapsed_targets"] += 1
        else:
            failures.append(f"{label}: target {target} is not collapsed on the parent")
        if target not in base.reqs:
            counts["fresh_targets"] += 1
        else:
            failures.append(f"{label}: target {target} already stands on the parent")
        if not in_bounds(response, bounds):
            failures.append(f"{label}: response outside the declared bounds")
            continue
        mr = min_responses(base, target, measure, bounds)
        if mr is None:
            failures.append(f"{label}: the parent admits no response inside the bounds")
            continue
        if canonical_delta(response) not in mr.deltas or list(mr.cost) != list(cast(Sequence[int], edge["cost"])):
            failures.append(f"{label}: response is not a minimum at the recorded cost")
            continue
        counts["minimum_agreements"] += 1
    return failures, counts


def class_census(name: str, nodes: Sequence[Mapping[str, object]],
                 regimes: Mapping[int, Regime]) -> tuple[list[str], dict[str, dict[str, int]], dict[int, CanonKey]]:
    """Nodes and distinct canonical keys per depth; every node its own class."""
    keys: dict[int, CanonKey] = {nid: canonical(regimes[nid]) for nid in sorted(regimes)}
    per_depth: dict[int, list[int]] = {}
    for node in nodes:
        per_depth.setdefault(cast(int, node["depth"]), []).append(cast(int, node["id"]))
    failures: list[str] = []
    seen: dict[CanonKey, int] = {}
    for nid in sorted(keys):
        if keys[nid] in seen:
            failures.append(f"{name} node {nid}: isomorphic to node {seen[keys[nid]]}")
        else:
            seen[keys[nid]] = nid
    census = {
        str(depth): {"nodes": len(ids), "classes": len({keys[nid] for nid in ids})}
        for depth, ids in sorted(per_depth.items())
    }
    return failures, census, keys


# ---------------------------------------------------------------------------
# The two unreachable states, against every exported node
# ---------------------------------------------------------------------------


def unreachable_states() -> dict[str, Regime]:
    two = ("<a>", "<ab>")
    return {
        "form_without_instance": Regime(two, (1,), frozenset(), frozenset(), frozenset({(0, 1)})),
        "ruled_mark": Regime(two, (1,), frozenset({(0, (0,))}), frozenset({0}), frozenset({(0, 1)})),
    }


def distance(a: Regime, b: Regime) -> int:
    """A structural edit count between two regimes on the same data count."""
    forms = abs(len(a.forms) - len(b.forms)) + sum(1 for x, y in zip(a.forms, b.forms) if x != y)
    return forms + len(a.insts ^ b.insts) + len(a.rules ^ b.rules) + len(a.reqs ^ b.reqs)


def nearest_node(state: Regime, trees: Mapping[str, tuple[Mapping[int, tuple[Event, ...]], Mapping[int, Regime]]]) -> JsonDict:
    best: tuple[int, str, int] | None = None
    for name in EXPORTS:
        histories, regimes = trees[name]
        for nid in sorted(regimes):
            r = regimes[nid]
            if r.n_data() != state.n_data():
                continue
            d = distance(state, r)
            if best is None or (d, name, nid) < best:
                best = (d, name, nid)
    if best is None:
        raise CensusError("no exported node shares the state's data count")
    d, name, nid = best
    histories, regimes = trees[name]
    history = histories[nid]
    return {
        "export": name,
        "node": nid,
        "distance": d,
        "regime": regime_json(regimes[nid]),
        "replay_certificate": {
            "history": [event_json(e) for e in history],
            "regime_sha256": regime_sha256(replay(history)),
        },
    }


# ---------------------------------------------------------------------------
# The census
# ---------------------------------------------------------------------------


def census(root: Path = ROOT) -> JsonDict:
    bounds = Bounds()
    trees: dict[str, tuple[dict[int, tuple[Event, ...]], dict[int, Regime]]] = {}
    exports: JsonDict = {}
    sources: JsonDict = {}
    all_keys: dict[CanonKey, tuple[str, int]] = {}
    totals = {"nodes": 0, "edges": 0, "rounds": 0, "supply": 0, "minimum_agreements": 0,
              "fixpoints": 0, "answered_fixpoints": 0}
    for name in EXPORTS:
        gz = root / "artifacts" / "full" / f"{name}.json.gz"
        raw = gz.read_bytes()
        payload = cast(Mapping[str, object], read_json_gz(gz))
        content = hashlib.sha256(json.dumps(payload, indent=1, sort_keys=True).encode("utf-8") + b"\n").hexdigest()
        summary = json.loads((root / "artifacts" / f"{name}_summary.json").read_text(encoding="utf-8"))
        pinned = summary["full_export_sha256"]
        if content != pinned:
            raise CensusError(f"{name}: decompressed export hash differs from its committed summary pin")
        sources[f"artifacts/full/{name}.json.gz"] = {
            "gz_sha256": hashlib.sha256(raw).hexdigest(),
            "content_sha256": content,
            "summary_pin_matches": True,
        }
        if not verify_full_export(cast(Mapping[str, Json], payload)):
            raise CensusError(f"{name}: the sealed certification verify_full_export rejects the export")
        histories, regimes = reconstruct(name, payload)
        trees[name] = (histories, regimes)
        nodes = cast(Sequence[Mapping[str, object]], payload["nodes"])
        node_fail = node_failures(name, regimes)
        if node_fail:
            raise CensusError(node_fail[0])
        measure = cast(str, payload["measure"])
        edge_fail, counts = edge_failures(name, payload, regimes, measure, bounds)
        if edge_fail:
            raise CensusError(edge_fail[0])
        class_fail, per_depth, keys = class_census(name, nodes, regimes)
        if class_fail:
            raise CensusError(class_fail[0])
        for nid, key in keys.items():
            all_keys.setdefault(key, (name, nid))
        fix = [nid for nid in sorted(regimes) if fixpoint(regimes[nid])]
        arity_fail = [nid for nid in sorted(regimes) if not within_arity(regimes[nid], bounds)]
        if arity_fail:
            raise CensusError(f"{name} node {arity_fail[0]}: a form exceeds the declared arity bound")
        exports[name] = {
            "reading": payload["reading"],
            "measure": measure,
            "supply_enabled": payload["supply_enabled"],
            "nodes": len(nodes),
            "edges": len(cast(Sequence[object], payload["edges"])),
            "sealed_certification": True,
            "replay_hash_recheck": len(regimes),
            "invariants": {key: {"holds_on": len(regimes), "fails_on": 0} for key in INVARIANTS},
            "edges_checked": counts,
            "classes_per_depth": per_depth,
            "max_depth": max(cast(int, n["depth"]) for n in nodes),
            "fixpoints": len(fix),
            "answered_fixpoints": len(fix),
        }
        totals["nodes"] += len(nodes)
        totals["edges"] += len(cast(Sequence[object], payload["edges"]))
        totals["rounds"] += counts["rounds"]
        totals["supply"] += counts["supply"]
        totals["minimum_agreements"] += counts["minimum_agreements"]
        totals["fixpoints"] += len(fix)
        totals["answered_fixpoints"] += len(fix)
    countermodels: list[JsonDict] = []
    for label, state in unreachable_states().items():
        key = canonical(state)
        countermodels.append({
            "name": label,
            "regime": regime_json(state),
            "well_formed": well_formed(state),
            "rule_free": rule_free(state),
            "within_arity_bound": within_arity(state, bounds),
            "invariants": invariants(state),
            "isomorphic_to_an_exported_node": key in all_keys,
            "lean": "Reachable.formNoInst_unreachable" if label == "form_without_instance" else "Reachable.ruledMark_unreachable",
            "nearest_exported_node": nearest_node(state, trees),
        })
        if key in all_keys:
            raise CensusError(f"{label}: isomorphic to exported node {all_keys[key]}")
    return {
        "schema": SCHEMA,
        "authority_effect": "None",
        "bounds": {"max_items": bounds.max_items, "max_arity": bounds.max_arity},
        "invariants_checked": list(INVARIANTS),
        "exports": exports,
        "totals": totals,
        "distinct_classes_over_all_exports": len(all_keys),
        "countermodels": countermodels,
        "sources": sources,
    }


def render(payload: JsonDict) -> bytes:
    return (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        fresh = render(census())
    except (CensusError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    if args.write:
        OUTPUT.write_bytes(fresh)
        print(f"WROTE: {OUTPUT.relative_to(ROOT).as_posix()}")
        return 0
    if not OUTPUT.is_file() or OUTPUT.read_bytes() != fresh:
        print("FAIL: reachable.json differs from a fresh census")
        return 1
    print("PASS: every exported node and edge agrees with reachable.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
