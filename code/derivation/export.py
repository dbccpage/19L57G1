"""Machine-readable export of histories, regimes, trees, and claims.

Classification: metatheory apparatus.  Exports are deterministic: no
timestamps, no environment data, sorted keys.

Tree exports are normalized DAG records: nodes carry no per-node history;
instead each edge carries its event delta, and a node's replayable history
is the root history extended along its *creation edge* chain (the first
edge listed with that child).  Summaries (small, committed to Git) carry
the statistics and the SHA-256 of the full export; full exports are
written as reproducibly compressed ``.json.gz`` (fixed mtime, fixed
compression level), and ``verify_full_export`` replays every node from
the DAG and checks its regime hash.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
from typing import Mapping, Sequence, Union, cast

from .candidates import Delta, delta_events
from .engine import Edge, Node, Tree, delta_json_items
from .model import (
    AdmissionError,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Regime,
    Supply,
    replay,
)

Json = Union[
    None, bool, int, str, float, Sequence["Json"], Mapping[str, "Json"]
]


def event_json(e: Event) -> dict[str, Json]:
    if isinstance(e, Supply):
        return {"event": "supply", "token": e.token}
    if isinstance(e, AdmitDatum):
        return {"event": "admit_datum", "token": e.token}
    if isinstance(e, AdmitForm):
        return {"event": "admit_form", "arity": e.arity}
    if isinstance(e, AdmitInst):
        return {"event": "admit_inst", "form": e.form, "args": list(e.args)}
    if isinstance(e, AdmitRuleAll):
        return {"event": "admit_rule_all", "form": e.form}
    return {"event": "impose_separation", "i": e.i, "j": e.j}


def event_from_json(payload: Mapping[str, Json]) -> Event:
    kind = payload["event"]
    if kind == "supply":
        return Supply(cast(str, payload["token"]))
    if kind == "admit_datum":
        return AdmitDatum(cast(str, payload["token"]))
    if kind == "admit_form":
        return AdmitForm(cast(int, payload["arity"]))
    if kind == "admit_inst":
        return AdmitInst(
            cast(int, payload["form"]),
            tuple(cast(Sequence[int], payload["args"])),
        )
    if kind == "admit_rule_all":
        return AdmitRuleAll(cast(int, payload["form"]))
    if kind == "impose_separation":
        return Impose(cast(int, payload["i"]), cast(int, payload["j"]))
    raise ValueError(f"unknown event kind: {kind!r}")


def regime_json(r: Regime) -> dict[str, Json]:
    return {
        "data": list(r.data),
        "forms": list(r.forms),
        "insts": [[f, list(args)] for (f, args) in sorted(r.insts)],
        "rules": sorted(r.rules),
        "reqs": [list(p) for p in sorted(r.reqs)],
    }


def regime_sha256(r: Regime) -> str:
    return hashlib.sha256(
        json.dumps(regime_json(r), sort_keys=True).encode("utf-8")
    ).hexdigest()


def delta_json(delta: Delta) -> list[dict[str, Json]]:
    return delta_json_items(delta)  # type: ignore[return-value]


def edge_events(parent_regime: Regime, edge: Edge) -> tuple[Event, ...]:
    """The event delta an edge applies to its parent.  Uniform for
    creation and merge edges (for creation edges it equals the recorded
    history difference; asserted by ``verify_full_export``)."""
    if edge.challenge == "supply":
        token = f"g{parent_regime.n_data()}"
        return (Supply(token), AdmitDatum(token))
    i, j = edge.challenge.removeprefix("separate(").removesuffix(")").split(
        ", "
    )
    return (Impose(int(i), int(j)),) + delta_events(
        parent_regime, edge.response
    )


def node_json(n: Node) -> dict[str, Json]:
    return {
        "id": n.node_id,
        "depth": n.depth,
        "status": n.status,
        "merged_count": n.merged_count,
        "certified": n.certified,
        "regime_sha256": regime_sha256(n.regime),
    }


def edge_json(t: Tree, e: Edge) -> dict[str, Json]:
    parent_regime = t.nodes[e.parent].regime
    merge_iso: Json = None
    if e.kind == "merge":
        assert e.merge_dmap is not None and e.merge_fmap is not None
        merge_iso = {
            "dmap": list(e.merge_dmap),
            "fmap": list(e.merge_fmap),
        }
    return {
        "parent": e.parent,
        "child": e.child,
        "kind": e.kind,
        "merge_iso": merge_iso,
        "round": e.round_no,
        "challenge": e.challenge,
        "response_label": e.response_label,
        "response": delta_json(e.response),
        "events": [event_json(ev) for ev in edge_events(parent_regime, e)],
        "tie_classes": e.tie_classes,
        "class_size": e.class_size,
        "cost": list(e.cost),
        "orbits": e.orbits,
    }


def _tree_meta(t: Tree) -> dict[str, Json]:
    return {
        "reading": t.reading,
        "measure": t.measure,
        "bounds": {
            "max_items": t.bounds.max_items,
            "max_arity": t.bounds.max_arity,
        },
        "max_rounds": t.max_rounds,
        "pre_expansion_node_guard": t.pre_expansion_node_guard,
        "supply_enabled": t.supply,
        "stats": cast(Json, t.stats()),
    }


def tree_full_json(t: Tree) -> dict[str, Json]:
    """Normalized DAG export: root history + per-node hashes + per-edge
    event deltas.  No per-node histories (deduplicated)."""
    payload = _tree_meta(t)
    payload["root_history"] = [event_json(e) for e in t.nodes[0].history]
    payload["root_regime"] = regime_json(t.nodes[0].regime)
    payload["nodes"] = [node_json(n) for n in t.nodes]
    payload["edges"] = [edge_json(t, e) for e in t.edges]
    return payload


def tree_summary_json(t: Tree, full_sha256: str) -> dict[str, Json]:
    """Committed summary: statistics plus the hash pinning the full
    export."""
    payload = _tree_meta(t)
    payload["full_export_sha256"] = full_sha256
    return payload


def verify_full_export(payload: Mapping[str, Json]) -> bool:
    """Independent certification of a normalized DAG export.

    Every node's history reconstructs along its creation edge and its
    regime hash is checked; then **every edge** is certified: the parent
    history extended by the edge events is replayed, and

    * a creation edge must reproduce the stored child exactly (hash
      equality);
    * a merge edge must carry explicit datum/form bijections that map the
      replayed result exactly onto the stored child representative's
      structure (tokens excluded).
    """
    from .iso import serialize

    root_history = tuple(
        event_from_json(cast(Mapping[str, Json], e))
        for e in cast(Sequence[Json], payload["root_history"])
    )
    nodes = cast(Sequence[Mapping[str, Json]], payload["nodes"])
    edges = cast(Sequence[Mapping[str, Json]], payload["edges"])
    histories: dict[int, tuple[Event, ...]] = {0: root_history}
    regimes: dict[int, Regime] = {0: replay(root_history)}
    if regime_sha256(regimes[0]) != nodes[0]["regime_sha256"]:
        return False
    # Build histories along creation edges; all hash certification happens
    # in the per-edge pass below, so this pass only reconstructs.
    creation: dict[int, Mapping[str, Json]] = {}
    for edge in edges:
        if edge["kind"] == "creation":
            child = cast(int, edge["child"])
            if child in creation:
                return False  # two creation edges for one node
            creation[child] = edge
    for node in nodes:
        nid = cast(int, node["id"])
        if nid == 0:
            continue
        if nid not in creation:
            return False  # node without a creation path
        edge = creation[nid]
        parent = cast(int, edge["parent"])
        events = tuple(
            event_from_json(cast(Mapping[str, Json], e))
            for e in cast(Sequence[Json], edge["events"])
        )
        histories[nid] = histories[parent] + events
        try:
            regimes[nid] = replay(histories[nid])
        except AdmissionError:
            return False  # tampered creation events
    # Certify every edge, creation and merge alike.
    for edge in edges:
        parent = cast(int, edge["parent"])
        child = cast(int, edge["child"])
        events = tuple(
            event_from_json(cast(Mapping[str, Json], e))
            for e in cast(Sequence[Json], edge["events"])
        )
        try:
            result = replay(histories[parent] + events)
        except AdmissionError:
            return False  # tampered events: ill-formed admission
        if edge["kind"] == "creation":
            if regime_sha256(result) != nodes[child]["regime_sha256"]:
                return False
        elif edge["kind"] == "merge":
            iso_raw = edge["merge_iso"]
            if iso_raw is None:
                return False
            iso = cast(Mapping[str, Json], iso_raw)
            dmap = tuple(cast(Sequence[int], iso["dmap"]))
            fmap = tuple(cast(Sequence[int], iso["fmap"]))
            target = regimes[child]
            if len(dmap) != result.n_data() or len(fmap) != len(
                result.forms
            ):
                return False
            if sorted(dmap) != list(range(target.n_data())) or sorted(
                fmap
            ) != list(range(len(target.forms))):
                return False  # not bijections onto the child's indices
            if serialize(result, dmap, fmap) != serialize(
                target,
                tuple(range(target.n_data())),
                tuple(range(len(target.forms))),
            ):
                return False
        else:
            return False  # unknown edge kind
    return True


def dumps_deterministic(payload: Json) -> bytes:
    return (json.dumps(payload, indent=1, sort_keys=True) + "\n").encode(
        "utf-8"
    )


def write_json(path: Path, payload: Json) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(dumps_deterministic(payload))


def write_json_gz(path: Path, payload: Json) -> str:
    """Write a reproducibly compressed JSON export (fixed mtime and
    compression level); returns the SHA-256 of the uncompressed bytes."""
    raw = dumps_deterministic(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
    return hashlib.sha256(raw).hexdigest()


def read_json_gz(path: Path) -> Json:
    return cast(Json, json.loads(gzip.decompress(path.read_bytes())))
