"""Run continuation two and write its receipts.

The shape of `research/second_engine/run_engine.py`, with this tree's
runs, census and scoring.  Deterministic: no timestamp, no environment
value, keys sorted, LF only.  The summary receipt regenerates
byte-identically whatever the number of worker processes: every run is
built by one worker from nothing but its engine and reading, and the
results are assembled in class order and reading order.  The full export
exceeds one megabyte, so it is written compressed with a fixed header and
the summary records its content hash.

Usage: python research/second_run/run_forward.py [--receipts DIR] [--check] [--workers N]

``--check`` writes nothing: it rebuilds the payload and compares it with
the committed receipts, so a drifted receipt fails without the run being
able to bless itself by overwriting the bytes it is checked against.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import pathlib
import sys
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Optional, Sequence

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
sys.path[:] = [str(HERE)] + [entry for entry in sys.path if entry != str(HERE)]

# `fwd_runs` puts the sealed kernel and the sibling trees on the path and
# this tree back at the front, so it is imported before anything drawn from
# either.
from fwd_runs import (  # noqa: E402
    BOUND,
    FIXPOINT,
    GUARD,
    NODE_GUARD,
    PERM_BUDGET,
    REFUSAL,
    ROUND_BOUND,
    TERMINALS,
    Edge,
    Run,
    build_run,
    carries_forward,
    closure_kind,
    cyclic_edges,
    elements,
    frontier,
    node_values,
    replay_mismatches,
    run_readings,
    sccs,
)
from fwd_census import (  # noqa: E402
    FAILS,
    HOLDS,
    HOLDS_AT_BOUND,
    UNDECIDED,
    Outcome,
    RunFacts,
    brute_run_isomorphic,
    every_run_reaches,
    forced_over,
    no_edge_violates,
    one_value_per_node,
    populations,
    run_signature,
    signature_digest,
    stage_verdict,
    supplementary_condensation,
)
from engine_decl import (  # noqa: E402
    Engine,
    SwitchMarker,
    count_minimal,
    engine_class,
    engine_named,
    inclusion_minimal,
    initial_members,
    input_tally,
)
from engine_probe import delta_json, event_json, key_brute_disagreements  # noqa: E402
from rules import label_of  # noqa: E402
from engine_decl import moded_rule  # noqa: E402
from derivation.export import regime_json  # noqa: E402
from derivation.model import Regime  # noqa: E402
from derivation.observe import profiles  # noqa: E402

_ENGINE_TREE = HERE.parents[0] / "second_engine"

RECEIPT_NAME = "forward.json"
FULL_NAME = "forward_full.json.gz"
MEGABYTE = 1_000_000
BRUTE_KEY_LIMIT = 1440
BRUTE_RUN_LIMIT = 8
FORBIDDEN_KEYS = frozenset(
    {"timestamp", "time", "date", "datetime", "created_at", "host", "hostname",
     "platform", "cwd", "env", "environment", "user", "path"}
)

__all__ = [
    "FULL_NAME",
    "RECEIPT_NAME",
    "analyse",
    "analyse_run",
    "build",
    "forbidden_keys",
    "frozen_digest",
    "main",
    "render",
    "refusal_shapes",
    "render_full",
    "score",
    "write",
]

READING_NAMES: tuple[str, ...] = tuple(reading.name for reading in run_readings())
STAGE_READINGS: tuple[str, ...] = ("two", "classes", "symmetry", "branching", "exhausted")
RUN_READINGS: tuple[str, ...] = (
    "one_two",
    "two_classes",
    "three_every",
    "three_changing",
    "four_duration",
    "five_adjacency",
    "six_reach",
    "seven_invariant",
    "eight_irreversibility",
    "twelve_recurrence",
)
CANDIDATES: tuple[str, ...] = (
    "elements", "data", "forms", "insts", "rules", "classes", "symmetry", "demands", "honoured",
)
CONDITIONS: tuple[str, ...] = ("preserved", "never_lowered", "never_raised")
SETS: tuple[str, ...] = ("class", "literal", "live", "two_kinded", "streamless", "streamless_live")
DEFINABLE: dict[str, str] = {
    "one_two": "DEFINABLE at every stage: holding two is read off the representative's regime",
    "two_classes": "DEFINABLE at every stage: the profile class count is read off the regime",
    "three_succession": "a function of the state within a run exactly when the run reading does not FAIL; recorded per run",
    "four_duration": "a function of the state within a run exactly when the run reading does not FAIL; recorded per run",
    "five_adjacency": "DEFINABLE relative to the engine's declaration, which declares the responder rung ten priced as a realization",
    "six_reach": "DEFINABLE relative to the engine's declaration, as adjacency",
    "seven_invariant": "DEFINABLE at every stage: the element count is read off the regime",
    "eight_irreversibility": "a property of the run graph, read off the run",
    "nine_symmetry": "DEFINABLE at every stage: the sealed automorphisms of the regime",
    "ten_branching": "DEFINABLE relative to the engine's declaration: the responder and continuation give the node's edges",
    "eleven_exhaustion": "DEFINABLE at every stage: the exhausted forms are read off the regime",
    "twelve_recurrence": "a property of the run graph, read off the run",
}


def frozen_digest(name: str) -> str:
    raw = (HERE / name).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def forbidden_keys(value: object, where: str = "") -> list[str]:
    """Every key of the payload, at any depth, that names a temporal or
    environment value.  The receipt must carry none."""
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            here = f"{where}.{key}" if where else str(key)
            if str(key).lower() in FORBIDDEN_KEYS:
                found.append(here)
            found.extend(forbidden_keys(item, here))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(forbidden_keys(item, f"{where}[{index}]"))
    return found


def _verdict(hit: bool) -> str:
    return "HIT" if hit else "MISSED"


def _digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()


# ---------------------------------------------------------------------------
# One run, analysed in a worker
# ---------------------------------------------------------------------------


def _outcome_json(outcome: Outcome) -> dict[str, Any]:
    out: dict[str, Any] = {"status": outcome.status}
    if outcome.witness:
        out["witness"] = json.loads(json.dumps(outcome.witness))
    if outcome.note:
        out["note"] = outcome.note
    return out


def _run_outcomes(run: Run, values: list[dict[str, Optional[int]]]) -> dict[str, Outcome]:
    comp = sccs(run)
    size: dict[int, int] = {}
    for c in comp:
        size[c] = size.get(c, 0) + 1
    self_loop = {edge.parent for edge in run.edges if edge.parent == edge.child}
    on_cycle = [size[comp[v]] > 1 or v in self_loop for v in range(len(run.nodes))]
    cyclic = set(cyclic_edges(run))

    def moves_two(edge: Edge) -> bool:
        return edge.kind == "response" and len(edge.moved) >= 2

    def reaches_third(edge: Edge) -> bool:
        if edge.kind != "response" or edge.pair is None:
            return False
        demanded = set(edge.pair)
        return any(not set(pair) <= demanded for pair, _ in edge.moved)

    def classes_lowered(index: int, edge: Edge) -> Optional[bool]:
        before = values[edge.parent]["classes"]
        after = values[edge.child]["classes"]
        if before is None or after is None:
            return None
        return after < before

    return {
        "one_two": every_run_reaches(run, lambda v: values[v]["two"] == 1, lambda _: False),
        "two_classes": no_edge_violates(run, classes_lowered),
        "three_every": one_value_per_node(run, lambda edge, v: v + 1),
        "three_changing": one_value_per_node(run, lambda edge, v: v + int(edge.changing)),
        "four_duration": one_value_per_node(
            run,
            lambda edge, v: 0 if edge.datum_round else v + int(edge.changing),
        ),
        "five_adjacency": every_run_reaches(run, lambda _: False, moves_two),
        "six_reach": every_run_reaches(run, lambda _: False, reaches_third),
        "seven_invariant": no_edge_violates(
            run,
            lambda index, edge: elements(edge.after) < elements(run.nodes[edge.parent].state.regime),
        ),
        "eight_irreversibility": no_edge_violates(
            run, lambda index, edge: edge.changing and index in cyclic
        ),
        "twelve_recurrence": every_run_reaches(run, lambda v: on_cycle[v], lambda _: False),
    }


def _candidate_outcomes(
    run: Run, values: list[dict[str, Optional[int]]]
) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for name in CANDIDATES:
        row: dict[str, str] = {}
        for condition in CONDITIONS:

            def violates(index: int, edge: Edge, name: str = name, condition: str = condition) -> Optional[bool]:
                before = values[edge.parent][name]
                after = values[edge.child][name]
                if before is None or after is None:
                    return None
                if condition == "preserved":
                    return after != before
                if condition == "never_lowered":
                    return after < before
                return after > before

            row[condition] = no_edge_violates(run, violates).status
        out[name] = row
    return out


def _node_json(run: Run, index: int) -> dict[str, Any]:
    node = run.nodes[index]
    return {
        "id": node.node_id,
        "stage": node.stage,
        "mode": node.state.mode,
        "key": hashlib.sha256(repr(node.key).encode("utf-8")).hexdigest()[:24],
        "regime": regime_json(node.state.regime),
        "terminal": node.terminal or None,
        "demands": [[kind, pair[0], pair[1]] for kind, pair in node.demands],
        "refused": [[kind, pair[0], pair[1]] for kind, pair in node.refused],
        "history_length": len(node.history),
        "budget_guard": node.budget_guard or None,
    }


def _edge_json(edge: Edge) -> dict[str, Any]:
    return {
        "parent": edge.parent,
        "child": edge.child,
        "kind": edge.kind,
        "demand_kind": edge.demand_kind,
        "pair": list(edge.pair) if edge.pair is not None else None,
        "delta": delta_json(edge.delta),
        "cost": list(edge.cost),
        "merge": edge.merge,
        "changing": edge.changing,
        "datum_round": edge.datum_round,
        "moved": [[pair[0], pair[1], apart] for pair, apart in edge.moved],
        "events": [event_json(event) for event in edge.events],
    }


def refusal_shapes(run: Run) -> dict[str, int]:
    """Every refused demand, by shape.  An apart demand is TRANSITIVE when
    some third datum is collapsed with both members and both of its pairs
    with them are labelled same in the node's mode: no-regress keeps both
    collapsed, and profile equality is transitive, so no delta of any size
    answers it.  Every other refused demand is counted by its kind and is
    not classified further."""
    out = {"apart_transitive": 0, "apart_other": 0, "same": 0}
    for node in run.nodes:
        if not node.refused:
            continue
        regime = node.state.regime
        table = profiles(regime)
        rule = moded_rule(run.engine.rule, node.state.mode)
        for kind, (i, j) in node.refused:
            if kind != "apart":
                out["same"] += 1
                continue
            transitive = any(
                table[i] == table[k] == table[j]
                and label_of(rule, regime, *sorted((i, k))) == "same"
                and label_of(rule, regime, *sorted((j, k))) == "same"
                for k in range(regime.n_data())
                if k not in (i, j)
            )
            out["apart_transitive" if transitive else "apart_other"] += 1
    return out


def run_payload(run: Run) -> dict[str, Any]:
    """The full run, every node and edge and the exact frontier, with no
    engine name: two engines with one run give one payload."""
    return {
        "reading": run.reading,
        "nodes": [_node_json(run, index) for index in range(len(run.nodes))],
        "edges": [_edge_json(edge) for edge in run.edges],
        "frontier": [
            {
                "id": node.node_id,
                "key": repr(node.key),
                "mode": node.state.mode,
                "stage": node.stage,
                "terminal": node.terminal,
                "demands": [[kind, pair[0], pair[1]] for kind, pair in node.demands],
            }
            for node in frontier(run)
        ],
    }


def analyse_run(engine: Engine, reading_name: str) -> dict[str, Any]:
    """Everything the summary and the full export need of one run."""
    reading = next(r for r in run_readings() if r.name == reading_name)
    run = build_run(engine, reading)
    values = node_values(run)
    outcomes = _run_outcomes(run, values)
    transfers = {
        "three_changing": lambda edge, v: v + int(edge.changing),
        "four_duration": lambda edge, v: 0 if edge.datum_round else v + int(edge.changing),
    }
    supplementary = {
        name: supplementary_condensation(run, transfer)
        for name, transfer in transfers.items()
        if outcomes[name].status == UNDECIDED
    }
    payload = run_payload(run)
    cyclic = cyclic_edges(run)
    regimes: dict[Regime, None] = {}
    for node in run.nodes:
        regimes.setdefault(node.state.regime, None)
    for edge in run.edges:
        regimes.setdefault(edge.after, None)
    return {
        "engine": engine.name,
        "reading": reading_name,
        "summary": {
            "nodes": len(run.nodes),
            "edges": len(run.edges),
            "merges": run.merges,
            "max_stage": max(node.stage for node in run.nodes),
            "terminals": {kind: sum(1 for n in run.nodes if n.terminal == kind) for kind in TERMINALS},
            "partial_refusals": sum(
                1 for n in run.nodes if n.refused and n.terminal != REFUSAL
            ),
            "closure": closure_kind(run),
            "carries_forward": carries_forward(run),
            "frontier": len(frontier(run)),
            "response_edges": sum(1 for e in run.edges if e.kind == "response"),
            "refusal_shapes": refusal_shapes(run),
            "datum_responses": sum(1 for e in run.edges if e.kind == "response" and e.carries_datum),
            "cyclic_edges": len(cyclic),
            "cyclic_non_switch": sum(1 for index in cyclic if run.edges[index].kind != "switch"),
            "replay_mismatches": replay_mismatches(run),
            "quotient_defects": list(run.quotient_defects),
            "unchecked_merges": list(run.unchecked_merges),
            "signature": signature_digest(run_signature(run)),
            "payload": _digest(payload),
        },
        "outcomes": {name: _outcome_json(outcome) for name, outcome in outcomes.items()},
        "supplementary": supplementary,
        "candidates": _candidate_outcomes(run, values),
        "facts": RunFacts(engine.name, reading_name, populations(run), values),
        "payload": payload,
        "regimes": list(regimes),
        "small_run": run if len(run.nodes) <= BRUTE_RUN_LIMIT else None,
    }


def _work(task: tuple[tuple[str, str], ...]) -> list[dict[str, Any]]:
    return [analyse_run(engine_named(name), reading) for name, reading in task]


def _tasks(engines: Sequence[Engine]) -> list[tuple[tuple[str, str], ...]]:
    """One task per rule, measure and reading, so a worker's caches serve
    the engines that share the most regimes."""
    groups: dict[tuple[str, str, str], list[tuple[str, str]]] = {}
    for engine in engines:
        for reading in READING_NAMES:
            groups.setdefault((engine.rule, engine.measure, reading), []).append((engine.name, reading))
    return [tuple(items) for _, items in sorted(groups.items())]


def run_all(engines: Sequence[Engine], workers: int) -> dict[tuple[str, str], dict[str, Any]]:
    tasks = _tasks(engines)
    results: list[list[dict[str, Any]]]
    if workers <= 1:
        results = [_work(task) for task in tasks]
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(_work, tasks))
    return {(r["engine"], r["reading"]): r for group in results for r in group}


# ---------------------------------------------------------------------------
# Supplied receipts, replayed before use
# ---------------------------------------------------------------------------


def continuation_one() -> dict[str, Any]:
    """Continuation one's reports, rebuilt by its public ``analyse`` and
    compared with its committed receipt; its LIVE and TWO-KINDED sets and
    probe signatures are used only if the two agree."""
    engine_tree = str(_ENGINE_TREE)
    sys.path[:] = [engine_tree] + [entry for entry in sys.path if entry != engine_tree]
    import run_engine  # the sibling runner, pinned by blob

    sys.path[:] = [str(HERE)] + [entry for entry in sys.path if entry != str(HERE)]
    reports = json.loads(json.dumps(run_engine.analyse(), sort_keys=True))
    committed = json.loads((_ENGINE_TREE / "receipts" / "engine.json").read_text(encoding="utf-8"))
    return {
        "replays": reports == committed["reports"],
        "live": list(reports["live"]),
        "two_kinded": list(reports["two_kinded"]),
        "probe_signature": {m["name"]: m["probe_signature"] for m in reports["members"]},
    }


# ---------------------------------------------------------------------------
# Analysis over the class
# ---------------------------------------------------------------------------


def _engine_outcome(statuses: Sequence[str]) -> str:
    if FAILS in statuses:
        return FAILS
    if all(s == HOLDS for s in statuses):
        return HOLDS
    if all(s in (HOLDS, HOLDS_AT_BOUND) for s in statuses):
        return HOLDS_AT_BOUND
    return UNDECIDED


def analyse(
    workers: int = 1, engines: Sequence[Engine] = ()
) -> tuple[dict[str, Any], dict[str, Any]]:
    """The summary reports and the full export, over the class unless a
    subset is named (the tests name one; the receipts never do)."""
    engines = tuple(engines) or engine_class()
    results = run_all(engines, workers)
    supplied = continuation_one()
    live = set(supplied["live"])
    two_kinded = set(supplied["two_kinded"])

    def members_of(name: str) -> list[Engine]:
        if name == "class":
            return list(engines)
        if name == "literal":
            return [e for e in engines if e.literal]
        if name == "live":
            return [e for e in engines if e.name in live]
        if name == "two_kinded":
            return [e for e in engines if e.name in two_kinded]
        if name == "streamless":
            return [e for e in engines if not e.growth]
        return [e for e in engines if not e.growth and e.name in live]

    def result(engine: Engine, reading: str) -> dict[str, Any]:
        return results[(engine.name, reading)]

    # --- the runs ---
    payloads: dict[str, Any] = {}
    runs: dict[str, Any] = {}
    for engine in engines:
        row: dict[str, Any] = {}
        for reading in READING_NAMES:
            r = result(engine, reading)
            payloads[r["summary"]["payload"]] = r["payload"]
            summary = dict(r["summary"])
            summary["outcomes"] = {k: v["status"] for k, v in r["outcomes"].items()}
            row[reading] = summary
        runs[engine.name] = row

    # --- the stage readings ---
    stage: dict[str, Any] = {}
    for set_name in SETS:
        pool = members_of(set_name)
        by_reading: dict[str, Any] = {}
        for reading in READING_NAMES:
            facts: list[RunFacts] = [result(e, reading)["facts"] for e in pool]
            by_reading[reading] = {
                name: [stage_verdict(facts, name, k) for k in range(ROUND_BOUND + 1)]
                for name in STAGE_READINGS
            }
        stage[set_name] = by_reading

    per_engine_forced: list[str] = []
    for engine in engines:
        forced_everywhere = True
        for reading in READING_NAMES:
            fact = result(engine, reading)["facts"]
            for name in STAGE_READINGS:
                for k in range(ROUND_BOUND + 1):
                    if not fact.populations[k][1]:
                        continue
                    if stage_verdict([fact], name, k)["verdict"] != "FORCED":
                        forced_everywhere = False
        if forced_everywhere:
            per_engine_forced.append(engine.name)

    # --- the run readings ---
    def outcome(engine: Engine, reading: str, name: str) -> Outcome:
        raw = result(engine, reading)["outcomes"][name]
        return Outcome(raw["status"], tuple(raw.get("witness", ())), raw.get("note", ""))

    run_verdicts: dict[str, Any] = {}
    for set_name in SETS:
        pool = members_of(set_name)
        run_verdicts[set_name] = {
            name: forced_over(
                (e.name, reading, outcome(e, reading, name))
                for e in pool
                for reading in READING_NAMES
            )
            for name in RUN_READINGS
        }
    per_reading_live: dict[str, Any] = {
        reading: {
            name: forced_over(
                (e.name, reading, outcome(e, reading, name)) for e in members_of("live")
            )
            for name in ("five_adjacency", "six_reach")
        }
        for reading in READING_NAMES
    }
    fails_anywhere = {
        name: sorted(
            f"{e.name}@{reading}"
            for e in engines
            for reading in READING_NAMES
            if outcome(e, reading, name).status == FAILS
        )
        for name in RUN_READINGS
    }
    supplementary = {
        name: {
            str(value): sum(
                1
                for e in engines
                for reading in READING_NAMES
                if result(e, reading)["supplementary"].get(name, "absent") == value
            )
            for value in (True, False, None)
        }
        for name in ("three_changing", "four_duration")
    }

    # --- the invariant candidates ---
    candidates: dict[str, Any] = {}
    for name in CANDIDATES:
        row = {}
        for condition in CONDITIONS:
            engine_status = {
                e.name: _engine_outcome(
                    [result(e, reading)["candidates"][name][condition] for reading in READING_NAMES]
                )
                for e in engines
            }
            row[condition] = {
                status: sorted(n for n, s in engine_status.items() if s == status)
                for status in (HOLDS, HOLDS_AT_BOUND, FAILS, UNDECIDED)
            }
        candidates[name] = row

    # --- carrying forward, and the minima among the carriers ---
    carriers = [
        e for e in engines
        if all(result(e, reading)["summary"]["carries_forward"] for reading in READING_NAMES)
    ]
    streamless_carriers = [e for e in carriers if not input_tally(e)["stream"]]
    not_closed = [
        e.name for e in engines
        if all(result(e, reading)["summary"]["closure"] == "NOT_CLOSED" for reading in READING_NAMES)
    ]
    carrying = {
        "carriers": [e.name for e in carriers],
        "streamless": [e.name for e in streamless_carriers],
        "not_closed_at_both": not_closed,
        "count_minimal": [e.name for e in count_minimal(carriers, 1)],
        "count_minimal_growth_as_two": [e.name for e in count_minimal(carriers, 2)],
        "inclusion_minimal": [e.name for e in inclusion_minimal(carriers)],
        "initial": [e.name for e in initial_members(carriers)],
        "counts": {e.name: e.count(1) for e in carriers},
        "streamless_count_minimal": [e.name for e in count_minimal(streamless_carriers, 1)],
    }

    # --- run-isomorphism ---
    run_class_of: dict[str, tuple[str, ...]] = {
        e.name: tuple(result(e, reading)["summary"]["signature"] for reading in READING_NAMES)
        for e in engines
    }
    classes: dict[tuple[str, ...], list[str]] = {}
    for e in engines:
        classes.setdefault(run_class_of[e.name], []).append(e.name)
    probe_of = {name: digest for name, digest in supplied["probe_signature"].items() if name in run_class_of}
    crossing = [
        members for members in classes.values()
        if len({probe_of[name] for name in members}) > 1
    ]
    probe_classes = len(set(probe_of.values()))
    coarsening = [
        sorted(set(members_by_probe))
        for members_by_probe in _probe_groups(probe_of).values()
        if len({run_class_of[name] for name in members_by_probe}) > 1
    ]
    v_pairs = []
    for e in engines:
        if e.validity != "V1":
            continue
        twin = engine_named(f"{e.rule}/{e.measure}/V2/{e.continuation}")
        if twin.name not in run_class_of:
            continue
        v_pairs.append(run_class_of[e.name] == run_class_of[twin.name])

    brute_agree = 0
    brute_disagree: list[str] = []
    for reading in READING_NAMES:
        small = [
            (e.name, result(e, reading)["small_run"])
            for e in engines
            if result(e, reading)["small_run"] is not None
        ]
        for i, (left_name, left) in enumerate(small):
            for right_name, right in small[i + 1 :]:
                decided = (
                    result(engine_named(left_name), reading)["summary"]["signature"]
                    == result(engine_named(right_name), reading)["summary"]["signature"]
                )
                if decided == brute_run_isomorphic(left, right):
                    brute_agree += 1
                else:
                    brute_disagree.append(f"{left_name}~{right_name}@{reading}")

    # --- the sealed key partition against the brute-force minimum ---
    distinct: dict[Regime, None] = {}
    for engine in engines:
        for reading in READING_NAMES:
            for regime in result(engine, reading)["regimes"]:
                distinct.setdefault(regime, None)
    within: list[Regime] = []
    above = 0
    for regime in distinct:
        count = 1
        for k in range(2, regime.n_data() + 1):
            count *= k
        for k in range(2, len(regime.forms) + 1):
            count *= k
        if count <= BRUTE_KEY_LIMIT:
            within.append(regime)
        else:
            above += 1
    key_check = key_brute_disagreements(within)
    key_check["above_limit"] = above

    reports = {
        "continuation_one_replays": supplied["replays"],
        "live": sorted(live),
        "two_kinded": sorted(two_kinded),
        "runs": runs,
        "stage": stage,
        "per_engine_forced": per_engine_forced,
        "run_verdicts": run_verdicts,
        "live_by_reading": per_reading_live,
        "fails_anywhere": fails_anywhere,
        "supplementary": supplementary,
        "candidates": candidates,
        "carrying": carrying,
        "run_classes": {
            "count": len(classes),
            "members": sorted(sorted(members) for members in classes.values()),
            "crossing_probe_classes": len(crossing),
            "probe_classes": probe_classes,
            "probe_classes_split": len(coarsening),
            "v_twins_isomorphic": sum(v_pairs),
            "v_twins": len(v_pairs),
            "brute_agreements": brute_agree,
            "brute_disagreements": brute_disagree,
        },
        "key_crosscheck": key_check,
        "definable": DEFINABLE,
        "totals": {
            "runs": len(results),
            "nodes": sum(r["summary"]["nodes"] for r in results.values()),
            "edges": sum(r["summary"]["edges"] for r in results.values()),
            "merges": sum(r["summary"]["merges"] for r in results.values()),
            "replay_mismatches": sum(len(r["summary"]["replay_mismatches"]) for r in results.values()),
            "quotient_defects": sum(len(r["summary"]["quotient_defects"]) for r in results.values()),
            "unchecked_merges": sum(len(r["summary"]["unchecked_merges"]) for r in results.values()),
            "datum_responses": sum(r["summary"]["datum_responses"] for r in results.values()),
            "cyclic_non_switch": sum(r["summary"]["cyclic_non_switch"] for r in results.values()),
            "refusal_shapes": {
                shape: sum(r["summary"]["refusal_shapes"][shape] for r in results.values())
                for shape in ("apart_transitive", "apart_other", "same")
            },
            "terminals": {
                kind: sum(r["summary"]["terminals"][kind] for r in results.values())
                for kind in TERMINALS
            },
            "closure": {
                kind: sum(1 for r in results.values() if r["summary"]["closure"] == kind)
                for kind in ("TERMINATES", "CYCLES", "NOT_CLOSED")
            },
            "distinct_payloads": len(payloads),
        },
    }
    full = {
        "engines": {
            e.name: {reading: result(e, reading)["summary"]["payload"] for reading in READING_NAMES}
            for e in engines
        },
        "payloads": payloads,
        "witnesses": {
            e.name: {reading: result(e, reading)["outcomes"] for reading in READING_NAMES}
            for e in engines
        },
    }
    return reports, full


def _probe_groups(probe_of: dict[str, str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for name, digest in sorted(probe_of.items()):
        groups.setdefault(digest, []).append(name)
    return groups


# ---------------------------------------------------------------------------
# The values the frozen predictions commit to, transcribed so the scoring is
# mechanical.  A transcription error is visible as a miss against a value
# the receipt also records, never as a silent pass.
# ---------------------------------------------------------------------------

MEASURES = ("mu1", "mu2")
VALIDITY = ("V1", "V2")
CONTS = ("halt", "growth", "switch", "growth+switch")
QUIET_RULES = ("E1", "E2", "E3", "E5", "E6", "E9")


def _names(rules: Sequence[str], measures: Sequence[str], validity: Sequence[str], conts: Sequence[str]) -> list[str]:
    return sorted(f"{r}/{m}/{v}/{c}" for r in rules for m in measures for v in validity for c in conts)


EXPECTED_QUIET = sorted(
    _names(("E7", "E8"), MEASURES, VALIDITY, CONTS)
    + _names(QUIET_RULES, MEASURES, VALIDITY, ("halt", "growth"))
)
EXPECTED_SHAPES: dict[str, dict[str, tuple[int, int, str]]] = {
    "halt": {"L": (1, 0, "TERMINATES"), "F": (1, 0, "TERMINATES")},
    "growth": {"L": (3, 2, "TERMINATES"), "F": (2, 1, "TERMINATES")},
    "switch": {"L": (2, 2, "CYCLES"), "F": (2, 2, "CYCLES")},
    "growth+switch": {"L": (6, 10, "CYCLES"), "F": (4, 6, "CYCLES")},
}
EXPECTED_CARRIERS = _names(("E4",), MEASURES, VALIDITY, ("halt", "growth"))
EXPECTED_STREAMLESS_CARRIERS = _names(("E4",), MEASURES, VALIDITY, ("halt",))
EXPECTED_CARRIER_MINIMA = _names(("E4",), MEASURES, ("V1",), ("halt",))
EXPECTED_PER_ENGINE_FORCED = sorted(
    [n for n in EXPECTED_QUIET if not (n.startswith(("E7/", "E8/")) and n.endswith("/growth+switch"))]
    + _names(("E6",), ("mu2",), VALIDITY, ("switch",))
)
ACTIVE_NON_E6 = sorted(
    _names(("E4",), MEASURES, VALIDITY, CONTS)
    + _names(("E1", "E2", "E3", "E5", "E9"), MEASURES, VALIDITY, ("switch", "growth+switch"))
)
SYMMETRY_AT_ROOT = {"L": 2, "F": 6}


def _all_not_forced(rows: list[dict[str, Any]], rounds: Sequence[int]) -> bool:
    return all(rows[k]["verdict"] == "NOT_FORCED" for k in rounds)


def _forced_value(rows: list[dict[str, Any]], k: int, value: int) -> bool:
    return bool(rows[k]["verdict"] == "FORCED" and rows[k]["value"] == value)


def score(reports: dict[str, Any]) -> dict[str, Any]:
    """Score every computational prediction mechanically.  The Lean rows
    and the gate-time row are scored where their evidence lives and are
    marked so rather than omitted."""
    scored: dict[str, Any] = {}
    runs = reports["runs"]
    totals = reports["totals"]
    live = reports["live"]

    scored["R-5"] = {
        "value": {"engines": len(runs), "literal": sum(1 for n in runs if not n.endswith("/halt")), "runs": totals["runs"]},
        "verdict": _verdict(len(runs) == 144 and totals["runs"] == 288
                            and sum(1 for n in runs if not n.endswith("/halt")) == 108),
    }
    key = reports["key_crosscheck"]
    scored["R-6"] = {
        "value": {
            "replay_mismatches": totals["replay_mismatches"],
            "quotient_defects": totals["quotient_defects"],
            "unchecked_merges": totals["unchecked_merges"],
            "key_disagreements": key["disagreements"],
        },
        "verdict": _verdict(
            totals["replay_mismatches"] == 0 and totals["quotient_defects"] == 0
            and totals["unchecked_merges"] == 0 and key["disagreements"] == 0
        ),
    }
    responding_both = sorted(
        n for n, row in runs.items() if all(row[r]["response_edges"] > 0 for r in READING_NAMES)
    )
    responding_any = sorted(
        n for n, row in runs.items() if any(row[r]["response_edges"] > 0 for r in READING_NAMES)
    )
    quiet = sorted(n for n in runs if n not in responding_any)
    scored["R-7"] = {
        "value": {"responding_at_both": len(responding_both), "responding_at_either": len(responding_any), "quiet": len(quiet)},
        "verdict": _verdict(responding_both == live and responding_any == live and quiet == EXPECTED_QUIET),
    }
    shape_misses = []
    for name in EXPECTED_QUIET:
        cont = name.split("/")[3]
        if name not in runs:
            shape_misses.append(f"{name}: not run")
            continue
        for reading in READING_NAMES:
            row = runs[name][reading]
            got = (row["nodes"], row["edges"], row["closure"])
            if got != EXPECTED_SHAPES[cont][reading]:
                shape_misses.append(f"{name}@{reading}: {got}")
    scored["R-8"] = {"value": {"shape_misses": shape_misses}, "verdict": _verdict(not shape_misses)}

    def run_shape(name: str, reading: str) -> tuple[int, ...]:
        if name not in runs:
            return ()
        row = runs[name][reading]
        t = row["terminals"]
        return (row["nodes"], row["edges"], t[FIXPOINT], t[BOUND], t[GUARD], t[REFUSAL])

    r9 = {v: run_shape(f"E4/mu2/{v}/halt", "L") for v in VALIDITY}
    scored["R-9"] = {"value": r9, "verdict": _verdict(all(s == (23, 30, 7, 1, 0, 0) for s in r9.values()))}
    r10 = {v: run_shape(f"E4/mu1/{v}/halt", "L") for v in VALIDITY}
    scored["R-10"] = {"value": r10, "verdict": _verdict(all(s == (53, 76, 21, 3, 0, 0) for s in r10.values()))}
    closed_wrong = []
    for name, row in runs.items():
        rule, _, _, cont = name.split("/")
        for reading in READING_NAMES:
            closed = row[reading]["closure"] != "NOT_CLOSED"
            if rule == "E4" and closed:
                closed_wrong.append(f"{name}@{reading}")
            if rule in ("E1", "E2", "E3", "E5", "E9") and "switch" in cont and closed:
                closed_wrong.append(f"{name}@{reading}")
            if rule == "E6" and cont == "switch" and reading == "L" and not closed:
                closed_wrong.append(f"{name}@{reading}")
    scored["R-11"] = {"value": {"wrong": closed_wrong}, "verdict": _verdict(not closed_wrong)}
    r12 = {
        n: runs[n]["F"]["terminals"][GUARD] if n in runs else 0
        for n in _names(("E4",), ("mu1",), VALIDITY, CONTS)
    }
    scored["R-12"] = {"value": r12, "verdict": _verdict(all(v > 0 for v in r12.values()))}
    carrying = reports["carrying"]
    scored["R-13"] = {
        "value": {k: carrying[k] for k in ("carriers", "streamless", "count_minimal", "count_minimal_growth_as_two", "inclusion_minimal", "initial")},
        "verdict": _verdict(
            sorted(carrying["carriers"]) == EXPECTED_CARRIERS
            and sorted(carrying["streamless"]) == EXPECTED_STREAMLESS_CARRIERS
            and sorted(carrying["count_minimal"]) == EXPECTED_CARRIER_MINIMA
            and sorted(carrying["count_minimal_growth_as_two"]) == EXPECTED_CARRIER_MINIMA
            and sorted(carrying["inclusion_minimal"]) == EXPECTED_CARRIER_MINIMA
            and carrying["initial"] == []
            and all(carrying["counts"][n] == 6 for n in EXPECTED_CARRIER_MINIMA if n in carrying["counts"])
        ),
    }
    scored["R-14"] = {"value": {"datum_responses": totals["datum_responses"]}, "verdict": _verdict(totals["datum_responses"] == 0)}
    rc = reports["run_classes"]
    scored["R-15"] = {"value": {"isomorphic": rc["v_twins_isomorphic"], "pairs": rc["v_twins"]}, "verdict": _verdict(rc["v_twins_isomorphic"] == rc["v_twins"] == 72)}
    scored["R-16"] = {
        "value": {"run_classes": rc["count"], "crossing_probe_classes": rc["crossing_probe_classes"]},
        "verdict": _verdict(rc["count"] == 36 and rc["crossing_probe_classes"] == 0),
    }

    stage = reports["stage"]["class"]
    r17 = []
    for reading in READING_NAMES:
        s = stage[reading]
        r17.append(_forced_value(s["two"], 0, 0) and _all_not_forced(s["two"], range(1, 16)))
        r17.append(_forced_value(s["classes"], 0, 1) and _all_not_forced(s["classes"], range(1, 16)))
        r17.append(_forced_value(s["symmetry"], 0, SYMMETRY_AT_ROOT[reading]) and _all_not_forced(s["symmetry"], range(1, 16)))
        r17.append(_forced_value(s["exhausted"], 0, 0) and _forced_value(s["exhausted"], 1, 0) and _all_not_forced(s["exhausted"], range(2, 16)))
        r17.append(_all_not_forced(s["branching"], range(0, 16)))
    scored["R-17"] = {
        "value": {
            reading: {name: [row["verdict"][0] for row in stage[reading][name]] for name in STAGE_READINGS}
            for reading in READING_NAMES
        },
        "verdict": _verdict(all(r17)),
    }
    rv = reports["run_verdicts"]["class"]
    first_halt = ["E1/mu1/V1/halt", "L"]
    r18 = (
        all(rv[n]["verdict"] == "NOT_FORCED" and rv[n]["first_failing"] == first_halt
            for n in ("one_two", "five_adjacency", "six_reach", "twelve_recurrence"))
        and rv["two_classes"]["verdict"] == "NOT_FORCED"
        and rv["two_classes"]["first_failing"] == ["E1/mu1/V1/switch", "L"]
        and rv["three_every"]["verdict"] == "NOT_FORCED"
        and rv["three_changing"]["verdict"] == "OPEN"
        and rv["four_duration"]["verdict"] == "OPEN"
        and not reports["fails_anywhere"]["three_changing"]
        and not reports["fails_anywhere"]["four_duration"]
    )
    scored["R-18"] = {
        "value": {n: [rv[n]["verdict"], rv[n].get("first_failing")] for n in RUN_READINGS},
        "verdict": _verdict(r18),
    }
    scored["R-19"] = {
        "value": {
            "seven": rv["seven_invariant"]["verdict"],
            "eight": rv["eight_irreversibility"]["verdict"],
            "cyclic_non_switch": totals["cyclic_non_switch"],
        },
        "verdict": _verdict(
            rv["seven_invariant"]["verdict"] == "FORCED_AT_BOUND"
            and rv["eight_irreversibility"]["verdict"] == "FORCED_AT_BOUND"
            and totals["cyclic_non_switch"] == 0
        ),
    }
    lv = reports["run_verdicts"]["live"]
    by_reading = reports["live_by_reading"]
    first_e4 = ["E4/mu1/V1/halt", "L"]
    scored["R-20"] = {
        "value": {
            "five": [lv["five_adjacency"]["verdict"], lv["five_adjacency"].get("first_failing")],
            "six": [lv["six_reach"]["verdict"], lv["six_reach"].get("first_failing")],
            "F": {n: by_reading["F"][n]["verdict"] for n in ("five_adjacency", "six_reach")},
        },
        "verdict": _verdict(
            lv["five_adjacency"]["verdict"] == "NOT_FORCED"
            and lv["five_adjacency"].get("first_failing") == first_e4
            and lv["six_reach"]["verdict"] == "NOT_FORCED"
            and lv["six_reach"].get("first_failing") == first_e4
            and by_reading["F"]["five_adjacency"]["verdict"] == "FORCED"
            and by_reading["F"]["six_reach"]["verdict"] == "FORCED"
        ),
    }
    scored["R-21"] = {
        "value": {"count": len(reports["per_engine_forced"]), "members": reports["per_engine_forced"]},
        "verdict": _verdict(sorted(reports["per_engine_forced"]) == EXPECTED_PER_ENGINE_FORCED),
    }
    cand = reports["candidates"]
    counts_never_lowered = all(
        not cand[name]["never_lowered"][FAILS] and not cand[name]["never_lowered"][UNDECIDED]
        for name in ("elements", "data", "forms", "insts", "rules")
    )
    classes_nl = cand["classes"]["never_lowered"]
    quiet_hold = all(
        n in classes_nl[HOLDS] or n in classes_nl[HOLDS_AT_BOUND] for n in EXPECTED_QUIET
    )
    active_fail = all(n in classes_nl[FAILS] for n in ACTIVE_NON_E6)
    scored["R-22"] = {
        "value": {
            "counts_never_lowered": counts_never_lowered,
            "classes_lowered_in": len(classes_nl[FAILS]),
        },
        "verdict": _verdict(counts_never_lowered and quiet_hold and active_fail),
    }
    scored["R-23"] = {
        "value": {"streamless_carriers": carrying["streamless"], "ledger": "checked by test_census.py"},
        "verdict": _verdict(sorted(carrying["streamless"]) == EXPECTED_STREAMLESS_CARRIERS),
    }
    for pid, where in (
        ("R-1", "verify_lean.py and test_census.py"),
        ("R-2", "verify_lean.py and test_census.py"),
        ("R-3", "the committed axiom log, checked by verify_lean.py"),
        ("R-4", "test_reconstruction.py"),
        ("R-24", "run_forward.py --check, the replay counts above, and the measured gate time"),
    ):
        scored[pid] = {"value": f"scored elsewhere: {where}", "verdict": "ELSEWHERE"}
    return scored


# ---------------------------------------------------------------------------
# Receipts
# ---------------------------------------------------------------------------


def render_full(full: dict[str, Any]) -> bytes:
    """The full export, compressed with a fixed header: no file name, a
    zero modification time, and a fixed level."""
    raw = json.dumps(full, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, compresslevel=9, mtime=0) as handle:
        handle.write(raw)
    return buffer.getvalue()


def build(workers: int = 1, engines: Sequence[Engine] = ()) -> tuple[dict[str, Any], bytes]:
    reports, full = analyse(workers, engines)
    compressed = render_full(full)
    raw_size = len(json.dumps(full, sort_keys=True, separators=(",", ":"), ensure_ascii=True))
    payload = {
        "authority_effect": "None",
        "attempt": "continuation two",
        "bounds": {
            "max_items": 2,
            "max_arity": 2,
            "max_data": 4,
            "rounds": ROUND_BOUND,
            "node_guard": NODE_GUARD,
            "permutation_budget": PERM_BUDGET,
            "brute_key_limit": BRUTE_KEY_LIMIT,
            "brute_run_limit": BRUTE_RUN_LIMIT,
        },
        "full_export": {
            "name": FULL_NAME,
            "compressed_sha256": hashlib.sha256(compressed).hexdigest(),
            "compressed_bytes": len(compressed),
            "content_sha256": hashlib.sha256(gzip.decompress(compressed)).hexdigest(),
            "content_bytes": raw_size,
        },
        "input_count_claim": "no floor proof and no unbounded reduction; see the ledger",
        "predictions_scored": score(reports),
        "predictions_sha256": frozen_digest("PREDICTIONS.md"),
        "prompt_sha256": frozen_digest("PROMPT.md"),
        "readings": list(READING_NAMES),
        "reports": reports,
        "write_root": "research/second_run",
    }
    return payload, compressed


def render(payload: dict[str, Any]) -> bytes:
    text = json.dumps(payload, indent=1, sort_keys=True, ensure_ascii=True) + "\n"
    return text.encode("utf-8")


def write(payload: dict[str, Any], compressed: bytes, receipts: pathlib.Path) -> pathlib.Path:
    receipts.mkdir(parents=True, exist_ok=True)
    target = receipts / RECEIPT_NAME
    target.write_bytes(render(payload))
    (receipts / FULL_NAME).write_bytes(compressed)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run continuation two.")
    parser.add_argument("--receipts", default=str(HERE / "receipts"), help="output directory")
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare with the committed receipts and write nothing",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=min(8, os.cpu_count() or 1),
        help="worker processes; the receipts do not depend on it",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="restrict to the named engines (tests only; never the committed receipts)",
    )
    args = parser.parse_args(argv)
    receipts = pathlib.Path(args.receipts)
    payload, compressed = build(args.workers, [engine_named(name) for name in args.only])
    fresh = render(payload)
    bad = forbidden_keys(payload)
    if bad:
        print(f"FAIL: the receipt carries forbidden keys: {bad}")
        return 1
    if len(fresh) > MEGABYTE:
        print(f"FAIL: the summary receipt is {len(fresh)} bytes and must be split further")
        return 1
    if args.check:
        failed = False
        for name, expected in ((RECEIPT_NAME, fresh), (FULL_NAME, compressed)):
            target = receipts / name
            if not target.exists():
                print(f"FAIL: {target} is missing")
                failed = True
                continue
            committed = target.read_bytes()
            if name == RECEIPT_NAME:
                committed = committed.replace(b"\r\n", b"\n")
            if committed != expected:
                print(f"FAIL: {target} differs from a fresh run")
                failed = True
        if failed:
            return 1
        print(f"receipts match a fresh run ({len(fresh)} and {len(compressed)} bytes)")
    else:
        target = write(payload, compressed, receipts)
        print(f"wrote {target} ({len(fresh)} bytes) and {FULL_NAME} ({len(compressed)} bytes)")
    scored = payload["predictions_scored"]
    for pid in sorted(scored, key=lambda name: (len(name), name)):
        print(f"  {pid}: {scored[pid]['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
