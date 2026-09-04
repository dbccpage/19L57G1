"""Rung zero of the second derivation: replay the inheritance.

Classification (assumption discipline):

* Everything here is metatheory apparatus.  It replays supplied receipts,
  censuses the supplied grammar by introspection, and computes inertia at
  the second level.  It derives no object-language content.
* Replay is the sealed rule: a receipt is trusted only if the pinned
  sources regenerate it.  A receipt whose sources are absent at the
  snapshot is OPEN, not trusted and not refused.
* The all-free stake is DECLARED here for the inertia computation only: a
  commitment that labels every pair free, so that growth under it has
  nothing to keep apart or together.  It is the two-sided analogue of the
  sibling standing commitment's empty commitment, reconstructed over the
  sealed kernel because the sibling tree is absent at this snapshot.
"""

from __future__ import annotations

import hashlib
import inspect
import pathlib
import subprocess
import sys
import typing

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (str(REPO / "code"), str(REPO / "research" / "identification_dual")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from derivation import engine as sealed_engine  # noqa: E402
from derivation import model as sealed_model  # noqa: E402
from derivation.candidates import Bounds  # noqa: E402
from derivation.engine import (  # noqa: E402
    READINGS,
    Reading,
    build_tree,
    challenge0_report,
    challenge1_report,
    challenge2_report,
    challenge3_report,
)
from derivation.export import dumps_deterministic, tree_full_json  # noqa: E402
from derivation.model import (  # noqa: E402
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Regime,
    Supply,
    replay,
    step,
)
from derivation.observe import collapsed_pairs, profiles  # noqa: E402
import dual  # noqa: E402

BOUNDS = Bounds(max_items=2, max_arity=2)
SEALED_MAX_ROUNDS = 15
SEALED_GUARD_MU1 = 1200
MAX_DATA = 5
MAX_SUPPLIES = 8
ARTIFACTS = REPO / "artifacts"
DUAL_RECEIPT = REPO / "research" / "identification_dual" / "receipts" / "identification_dual.json"


# ---------------------------------------------------------------------------
# Replay of supplied receipts
# ---------------------------------------------------------------------------


def replay_challenges() -> dict[str, object]:
    """Recompute the sealed challenge reports and compare with the committed
    artifact byte for byte, the way the sealed regeneration gate does."""
    computed: dict[str, object] = {
        "challenge0": challenge0_report(),
        "challenge1": challenge1_report(),
        "challenge2": challenge2_report(),
        "challenge3": {rd.name: challenge3_report(rd, BOUNDS) for rd in READINGS},
    }
    fresh = dumps_deterministic(typing.cast(typing.Any, computed))
    committed = (ARTIFACTS / "challenges.json").read_bytes()
    return {
        "artifact": "artifacts/challenges.json",
        "byte_identical": fresh == committed,
        "committed_sha256": hashlib.sha256(committed).hexdigest(),
        "fresh_sha256": hashlib.sha256(fresh).hexdigest(),
    }


def replay_closed(reading: Reading) -> dict[str, object]:
    """Rebuild the sealed closed-system baseline under the sealed run
    parameters and compare every field of the committed summary, including
    the full-export hash, which is the sha256 of the full DAG export."""
    import json

    tree = build_tree(
        reading, "mu1", BOUNDS, max_rounds=SEALED_MAX_ROUNDS,
        pre_expansion_node_guard=SEALED_GUARD_MU1, supply=False,
    )
    full_sha = hashlib.sha256(dumps_deterministic(tree_full_json(tree))).hexdigest()
    committed = json.loads((ARTIFACTS / f"closed_{reading.name}_summary.json").read_text(encoding="utf-8"))
    fresh: dict[str, object] = {
        "reading": tree.reading,
        "measure": tree.measure,
        "bounds": {"max_items": tree.bounds.max_items, "max_arity": tree.bounds.max_arity},
        "max_rounds": tree.max_rounds,
        "pre_expansion_node_guard": tree.pre_expansion_node_guard,
        "supply_enabled": tree.supply,
        "stats": tree.stats(),
        "full_export_sha256": full_sha,
    }
    diffs = sorted(k for k in set(committed) | set(fresh) if committed.get(k) != fresh.get(k))
    return {
        "artifact": f"artifacts/closed_{reading.name}_summary.json",
        "fields_compared": sorted(fresh),
        "differing_fields": diffs,
        "match": not diffs,
        "nodes": len(tree.nodes),
        "terminal_all_separated": sum(1 for n in tree.nodes if n.status == "terminal_all_separated"),
    }


def replay_dual_summary() -> dict[str, object]:
    """Regenerate the sibling dual's summary receipt with the sibling's own
    runner and compare byte for byte."""
    import run_dual

    summary, _full = run_dual.split(run_dual.build_all())
    fresh = dumps_deterministic(summary)
    committed = DUAL_RECEIPT.read_bytes()
    return {
        "artifact": "research/identification_dual/receipts/identification_dual.json",
        "byte_identical": fresh == committed,
        "committed_sha256": hashlib.sha256(committed).hexdigest(),
        "fresh_sha256": hashlib.sha256(fresh).hexdigest(),
    }


def absent_trees(snapshot: str) -> list[dict[str, object]]:
    """Trees the seed names, checked at the snapshot commit, never at HEAD,
    so that a later merge does not change this rung's record."""
    out: list[dict[str, object]] = []
    for path, pr in (("research/standing_commitment", 127), ("research/two_sided_commitment", 128)):
        result = subprocess.run(
            ["git", "ls-tree", "-d", "--name-only", snapshot, path],
            cwd=REPO, capture_output=True, text=True, check=False,
        )
        present = result.returncode == 0 and bool(result.stdout.strip())
        out.append({"path": path, "pull_request": pr, "present_at_snapshot": present,
                    "replay": "done" if present else "OPEN: absent at snapshot"})
    return out


# ---------------------------------------------------------------------------
# Census of declared inputs, by introspection
# ---------------------------------------------------------------------------


def _sample_regime() -> Regime:
    return replay((Supply("<>"), AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(1)))


def grammar_census() -> dict[str, object]:
    """Every event kind of the sealed grammar, from the ``Event`` union, and
    whether applying it to a sample regime changes the state."""
    kinds = list(typing.get_args(Event))
    sample = _sample_regime()
    probes: dict[type, Event] = {
        Supply: Supply("<z>"),
        AdmitDatum: AdmitDatum("<z>"),
        AdmitForm: AdmitForm(2),
        AdmitInst: AdmitInst(0, (0,)),
        AdmitRuleAll: AdmitRuleAll(0),
        Impose: Impose(0, 1),
    }
    rows: list[dict[str, object]] = []
    for k in kinds:
        e = probes[k]
        rows.append({"event": k.__name__, "changes_state": step(sample, e) != sample,
                     "role": "presentation" if k is Supply else ("external requirement" if k is Impose else "admission")})
    sig = inspect.signature(build_tree)
    policies = [
        {"policy": "pair-separation closure", "introduced_by": "engine.closure_challenge_orbits",
         "present": callable(getattr(sealed_engine, "closure_challenge_orbits", None))},
        {"policy": "external continuation (supply)", "introduced_by": "engine.build_tree(supply=...)",
         "present": "supply" in sig.parameters},
    ]
    dual_kinds = [k for k in typing.get_args(dual.DualEvent) if k not in kinds and k is not Event]
    dual_rows = [{"event": k.__name__, "role": "declared"} for k in dual_kinds]
    return {
        "sealed_event_kinds": rows,
        "sealed_event_count": len(rows),
        "sealed_state_preserving_count": sum(1 for r in rows if not r["changes_state"]),
        "sealed_policies": policies,
        "sealed_policy_count": len(policies),
        "dual_declared_events": dual_rows,
        "dual_declared_count": len(dual_rows),
        "model_module": sealed_model.__name__,
    }


def remaining_inputs(absent: list[dict[str, object]]) -> list[dict[str, object]]:
    by_path = {str(a["path"]): a for a in absent}
    stake = by_path["research/two_sided_commitment"]
    return [
        {"input": "stake", "kind": "two-sided standing commitment", "introduced_by": "Declare (two_sided_commitment)",
         "custody": "OPEN: absent at snapshot" if not stake["present_at_snapshot"] else "pinned"},
        {"input": "stream", "kind": "supply and admission of one fresh datum at a demand-free state",
         "introduced_by": "Supply + AdmitDatum (sealed grammar); growth edge (two_sided_commitment)",
         "custody": "sealed events pinned; growth policy OPEN: absent at snapshot" if not stake["present_at_snapshot"] else "pinned"},
    ]


# ---------------------------------------------------------------------------
# Inertia at the second level
# ---------------------------------------------------------------------------


def supplies_are_inert(reading: Reading) -> dict[str, object]:
    base = replay(reading.genesis)
    unchanged = True
    for k in range(1, MAX_SUPPLIES + 1):
        history: tuple[Event, ...] = tuple(reading.genesis) + tuple(Supply(f"s{i}") for i in range(k))
        if replay(history) != base:
            unchanged = False
    return {"reading": reading.name, "supplies_up_to": MAX_SUPPLIES, "regime_unchanged": unchanged,
            "data": base.n_data(), "forms": len(base.forms)}


def all_free_growth(reading: Reading) -> dict[str, object]:
    """Grow from the sealed genesis to the data bound under the all-free
    stake: every pair is free, so the demand set is empty by definition and
    no response is ever enumerated.  Record what the states look like."""
    r = replay(reading.genesis)
    chain: list[dict[str, object]] = []
    while True:
        n = r.n_data()
        profs = profiles(r)
        chain.append({
            "data": n, "forms": len(r.forms), "insts": len(r.insts), "rules": len(r.rules),
            "demands_all_free": 0, "demands_undeclared": 0,
            "collapsed_pairs": len(collapsed_pairs(r)), "all_pairs": n * (n - 1) // 2,
            "totally_collapsed": len(set(profs)) <= 1,
        })
        if n >= MAX_DATA:
            break
        r = replay((Supply(f"g{n}"), AdmitDatum(f"g{n}")), r)
    return {
        "reading": reading.name,
        "chain": chain,
        "nodes": len(chain),
        "growth_edges": len(chain) - 1,
        "responses": 0,
        "forms_ever_admitted": max(int(str(c["forms"])) for c in chain),
        "every_state_totally_collapsed": all(bool(c["totally_collapsed"]) for c in chain),
        "single_chain": True,
    }


def snapshot_commit() -> str:
    import json

    manifest = json.loads((HERE / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    value = manifest.get("snapshot_commit")
    assert isinstance(value, str) and len(value) == 40
    return value
