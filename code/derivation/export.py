"""Machine-readable export of histories, regimes, trees, and claims.

Classification: metatheory apparatus.  Exports are deterministic: no
timestamps, no environment data, sorted keys, and full per-node histories so
every certified regime can be replayed from genesis by a reader."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from .candidates import Delta
from .engine import Edge, Node, Tree, delta_json_items
from .model import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Regime,
    Supply,
)

Json = Union[None, bool, int, str, float, list["Json"], dict[str, "Json"]]


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


def regime_json(r: Regime) -> dict[str, Json]:
    return {
        "data": list(r.data),
        "forms": list(r.forms),
        "insts": [[f, list(args)] for (f, args) in sorted(r.insts)],
        "rules": sorted(r.rules),
        "reqs": [list(p) for p in sorted(r.reqs)],
    }


def delta_json(delta: Delta) -> list[dict[str, Json]]:
    return delta_json_items(delta)  # type: ignore[return-value]


def node_json(n: Node) -> dict[str, Json]:
    return {
        "id": n.node_id,
        "depth": n.depth,
        "status": n.status,
        "merged_count": n.merged_count,
        "certified": n.certified,
        "canonical": repr(n.canon),
        "regime": regime_json(n.regime),
        "history": [event_json(e) for e in n.history],
    }


def edge_json(e: Edge) -> dict[str, Json]:
    return {
        "parent": e.parent,
        "child": e.child,
        "round": e.round_no,
        "challenge": e.challenge,
        "response_label": e.response_label,
        "response": delta_json(e.response),
        "tie_classes": e.tie_classes,
        "class_size": e.class_size,
        "cost": list(e.cost),
    }


def tree_json(t: Tree) -> dict[str, Json]:
    return {
        "reading": t.reading,
        "measure": t.measure,
        "bounds": {
            "max_items": t.bounds.max_items,
            "max_arity": t.bounds.max_arity,
        },
        "max_rounds": t.max_rounds,
        "node_budget": t.node_budget,
        "supply_enabled": t.supply,
        "stats": t.stats(),  # type: ignore[dict-item]
        "nodes": [node_json(n) for n in t.nodes],
        "edges": [edge_json(e) for e in t.edges],
    }


def write_json(path: Path, payload: Json) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=1, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
