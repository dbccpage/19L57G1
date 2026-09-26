"""Run continuation one and write the receipt.

The shape of `research/second_response/run_response.py`, with this
tree's measurements and scoring.  Deterministic: no timestamp, no
environment value, keys sorted, LF only.  The receipt regenerates
byte-identically.  Predictions are scored mechanically from the computed
values; a miss is recorded next to its value and never edited.

Usage: python research/second_engine/run_engine.py [--receipts DIR] [--check]

``--check`` writes nothing: it rebuilds the payload and compares it with
the committed receipt, so a drifted receipt fails without the run being
able to bless itself by overwriting the bytes it is checked against.

The two frozen texts are hashed with line endings normalized to LF before
the digest is taken, so the digest recorded is that of the frozen bytes as
Git holds them, whatever the working tree holds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from typing import Any, Sequence

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
sys.path[:] = [str(HERE)] + [entry for entry in sys.path if entry != str(HERE)]

# `engine_decl` puts the sealed kernel and the sibling trees on the path and
# this tree back at the front, so it is imported before anything drawn from
# either.
from engine_decl import (  # noqa: E402
    FLIPPED,
    MEASURES,
    RULE_NAMES,
    BundleRefused,
    Engine,
    EState,
    check_declaration_label,
    count_minimal,
    engine_class,
    honoured_before,
    inclusion_minimal,
    initial_members,
    input_tally,
    least_responses,
    moded_rule,
    shared_capability_pairs,
    Target,
    state_demands,
)
from engine_probe import (  # noqa: E402
    Probe,
    attribution_violations,
    brute_isomorphic,
    build_probe,
    key_brute_disagreements,
    probe_payload,
    probe_signature,
    readings,
    replay_mismatches,
    responder_crosscheck,
    signature_digest,
)
from derivation.candidates import NewDatum, NewForm, NewInst, NewRuleAll  # noqa: E402
from derivation.model import Pair, Regime  # noqa: E402

RECEIPT_NAME = "engine.json"
MEGABYTE = 1_000_000
FORBIDDEN_KEYS = frozenset(
    {"timestamp", "time", "date", "datetime", "created_at", "host", "hostname",
     "platform", "cwd", "env", "environment", "user", "path"}
)

__all__ = [
    "RECEIPT_NAME",
    "analyse",
    "build",
    "forbidden_keys",
    "frozen_digest",
    "main",
    "render",
    "score",
    "write",
]

READING_NAMES: tuple[str, ...] = tuple(reading.name for reading in readings())
SUBCLASSES: tuple[str, ...] = ("class", "literal")
FILTERS: tuple[str, ...] = ("all", "live", "two_kinded")
WEIGHTS: tuple[int, ...] = (1, 2)

# ---------------------------------------------------------------------------
# The values the frozen predictions commit to, transcribed so the scoring is
# mechanical.  A transcription error is visible as a miss against a value
# the receipt also records, never as a silent pass.
# ---------------------------------------------------------------------------

EIGHT = ("E1", "E2", "E3", "E4", "E5", "E7", "E8", "E9")


def _names(rules: Sequence[str], measures: Sequence[str], validity: str, conts: Sequence[str]) -> list[str]:
    return sorted(f"{r}/{m}/{validity}/{c}" for r in rules for m in measures for c in conts)


EXPECTED_MINIMA: dict[str, list[str]] = {
    "class/all/1": _names(EIGHT, MEASURES, "V1", ("halt",)),
    "class/all/2": _names(EIGHT, MEASURES, "V1", ("halt",)),
    "literal/all/1": _names(EIGHT, MEASURES, "V1", ("growth", "switch")),
    "literal/all/2": _names(EIGHT, MEASURES, "V1", ("switch",)),
    "class/live/1": _names(("E4",), MEASURES, "V1", ("halt",)),
    "class/live/2": _names(("E4",), MEASURES, "V1", ("halt",)),
    "literal/live/1": sorted(
        _names(("E4",), MEASURES, "V1", ("growth", "switch"))
        + _names(("E1", "E2", "E3", "E5", "E9"), MEASURES, "V1", ("switch",))
    ),
    "literal/live/2": sorted(
        _names(("E4",), MEASURES, "V1", ("switch",))
        + _names(("E1", "E2", "E3", "E5", "E9"), MEASURES, "V1", ("switch",))
    ),
    "class/two_kinded/1": _names(("E4",), MEASURES, "V1", ("halt",)),
    "class/two_kinded/2": _names(("E4",), MEASURES, "V1", ("halt",)),
    "literal/two_kinded/1": _names(("E4",), MEASURES, "V1", ("growth", "switch")),
    "literal/two_kinded/2": _names(("E4",), MEASURES, "V1", ("switch",)),
}
EXPECTED_PROBE_CLASSES: dict[str, int] = {
    "class/all/1": 3,
    "class/all/2": 3,
    "literal/all/1": 6,
    "literal/all/2": 5,
    "class/live/1": 2,
    "class/live/2": 2,
    "literal/live/1": 4,
    "literal/live/2": 4,
    "class/two_kinded/1": 2,
    "class/two_kinded/2": 2,
    "literal/two_kinded/1": 2,
    "literal/two_kinded/2": 2,
}
ALL_CONTS = ("halt", "growth", "switch", "growth+switch")
EXPECTED_LIVE = sorted(
    _names(("E4",), MEASURES, "V1", ALL_CONTS)
    + _names(("E4",), MEASURES, "V2", ALL_CONTS)
    + _names(("E1", "E2", "E3", "E5", "E6", "E9"), MEASURES, "V1", ("switch", "growth+switch"))
    + _names(("E1", "E2", "E3", "E5", "E6", "E9"), MEASURES, "V2", ("switch", "growth+switch"))
)
EXPECTED_TWO_KINDED = sorted(
    _names(("E4",), MEASURES, "V1", ALL_CONTS) + _names(("E4",), MEASURES, "V2", ALL_CONTS)
)
EXPECTED_STREAMLESS_LIVE = sorted(
    _names(("E4",), MEASURES, "V1", ("halt", "switch"))
    + _names(("E4",), MEASURES, "V2", ("halt", "switch"))
    + _names(("E1", "E2", "E3", "E5", "E6", "E9"), MEASURES, "V1", ("switch",))
    + _names(("E1", "E2", "E3", "E5", "E6", "E9"), MEASURES, "V2", ("switch",))
)
EXPECTED_ROOT_DEMANDS = {"L": 1, "F": 3}
EXPECTED_TIES = {"L": {"mu1": 6, "mu2": 2}, "F": {"mu1": 10, "mu2": 2}}
FLIPPED_DEMANDING = ("E1", "E2", "E3", "E5", "E6", "E9")


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


# ---------------------------------------------------------------------------
# Reading the probes
# ---------------------------------------------------------------------------


def _answered(probe: Probe) -> bool:
    return any(
        record.answered
        for node in probe.nodes
        if node.answers is not None
        for record in node.answers
    )


def _kinds_read(probe: Probe) -> set[str]:
    return {kind for node in probe.nodes for kind, _ in node.demands}


def _item_shape(delta: Any) -> str:
    kinds = []
    for item in delta:
        if isinstance(item, NewDatum):
            kinds.append("datum")
        elif isinstance(item, NewForm):
            kinds.append("form")
        elif isinstance(item, NewRuleAll):
            kinds.append("rule")
        elif isinstance(item, NewInst):
            kinds.append("inst")
    return "+".join(sorted(kinds))


Situation = tuple[str, str, Regime, Target, str]


def _situations(probes: dict[tuple[str, str], Probe]) -> list[Situation]:
    """Every (rule, mode, regime, demand, validity) the probes answered, in
    first-seen order."""
    seen: dict[Situation, None] = {}
    for probe in probes.values():
        for node in probe.nodes:
            if node.answers is None:
                continue
            for target in node.demands:
                situation = (
                    probe.engine.rule,
                    node.state.mode,
                    node.state.regime,
                    target,
                    probe.engine.validity,
                )
                seen.setdefault(situation, None)
    return list(seen)


def demand_census(probes: Sequence[Probe]) -> dict[str, Any]:
    """What the probes read: the plain demands of every root, by reading
    and rule; the demands of every growth state; and, at every level-one
    state an E-four response reaches, how many demands are of kind same,
    with the number of such states at L that read anything other than one
    demand of kind same."""
    root_demands: dict[str, dict[str, list[str]]] = {r: {} for r in READING_NAMES}
    growth_state_demands = 0
    same_after_e4: dict[str, list[int]] = {r: [] for r in READING_NAMES}
    l_children_other = 0
    for probe in probes:
        rule = probe.engine.rule
        root_demands[probe.reading][rule] = sorted(kind for kind, _ in probe.nodes[0].demands)
        for node in probe.nodes[1:]:
            if node.via == "growth":
                growth_state_demands += len(node.demands)
            if node.via == "response" and rule == "E4":
                kinds = [kind for kind, _ in node.demands]
                same_after_e4[probe.reading].append(kinds.count("same"))
                if probe.reading == "L" and kinds != ["same"]:
                    l_children_other += 1
    return {
        "root_demands_plain": root_demands,
        "demands_at_growth_states": growth_state_demands,
        "same_demands_after_an_e4_response": {
            r: sorted(set(v)) for r, v in same_after_e4.items()
        },
        "e4_children_at_L_reading_other_than_one_same": l_children_other,
    }


def flipped_at_genesis(genesis: dict[str, Regime]) -> dict[str, dict[str, list[str]]]:
    """The demands every rule reads in flipped mode at each genesis
    regime, read directly rather than through a probe."""
    return {
        reading: {
            rule: sorted(kind for kind, _ in state_demands(rule, EState(base, FLIPPED)))
            for rule in RULE_NAMES
        }
        for reading, base in genesis.items()
    }


def analyse() -> dict[str, Any]:
    engines = engine_class()
    probes: dict[tuple[str, str], Probe] = {
        (engine.name, reading.name): build_probe(engine, reading)
        for engine in engines
        for reading in readings()
    }

    def probe_of(engine: Engine, reading: str) -> Probe:
        return probes[(engine.name, reading)]

    live = {e.name: all(_answered(probe_of(e, r)) for r in READING_NAMES) for e in engines}
    two_kinded = {
        e.name: all(_kinds_read(probe_of(e, r)) >= {"apart", "same"} for r in READING_NAMES)
        for e in engines
    }
    signatures = {
        e.name: tuple(probe_signature(probe_of(e, r)) for r in READING_NAMES) for e in engines
    }

    # --- the full probes, deduplicated by content ---
    payloads: dict[str, Any] = {}
    engine_probe_digests: dict[str, dict[str, str]] = {}
    for engine in engines:
        row: dict[str, str] = {}
        for reading in READING_NAMES:
            payload = probe_payload(probe_of(engine, reading))
            digest = hashlib.sha256(
                json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")
            ).hexdigest()
            payloads[digest] = payload
            row[reading] = digest
        engine_probe_digests[engine.name] = row

    # --- the members ---
    members = []
    for engine in engines:
        members.append(
            {
                "name": engine.name,
                "rule": engine.rule,
                "measure": engine.measure,
                "validity": engine.validity,
                "continuation": engine.continuation,
                "literal": engine.literal,
                "capabilities": list(engine.capabilities()),
                "count": engine.count(1),
                "count_growth_as_two": engine.count(2),
                "input_tally": input_tally(engine),
                "live": live[engine.name],
                "two_kinded": two_kinded[engine.name],
                "probe_signature": signature_digest(signatures[engine.name]),
                "probes": engine_probe_digests[engine.name],
            }
        )

    # --- the minimum sets ---
    def subclass(name: str) -> list[Engine]:
        return [e for e in engines if name == "class" or e.literal]

    def filtered(pool: list[Engine], name: str) -> list[Engine]:
        if name == "live":
            return [e for e in pool if live[e.name]]
        if name == "two_kinded":
            return [e for e in pool if two_kinded[e.name]]
        return pool

    minima: dict[str, Any] = {}
    compared: list[tuple[Engine, Engine]] = []
    for sub in SUBCLASSES:
        for flt in FILTERS:
            pool = filtered(subclass(sub), flt)
            for weight in WEIGHTS:
                least = count_minimal(pool, weight)
                classes: dict[Any, list[str]] = {}
                for engine in least:
                    classes.setdefault(signatures[engine.name], []).append(engine.name)
                minima[f"{sub}/{flt}/{weight}"] = {
                    "pool": len(pool),
                    "least_count": least[0].count(weight) if least else None,
                    "members": sorted(e.name for e in least),
                    "probe_classes": len(classes),
                    "probe_class_members": sorted(sorted(v) for v in classes.values()),
                    "initial_in_minima": sorted(e.name for e in initial_members(least)),
                    "initial_in_pool": sorted(e.name for e in initial_members(pool)),
                    "inclusion_minimal": sorted(e.name for e in inclusion_minimal(pool)),
                    "measures_present": sorted({e.measure for e in least}),
                }
                for index, left in enumerate(least):
                    for right in least[index + 1 :]:
                        compared.append((left, right))

    # --- probe-isomorphism, labels against the exhaustive search ---
    unique_pairs = sorted({(a.name, b.name) for a, b in compared})
    iso_disagreements: list[str] = []
    iso_equal = 0
    for left_name, right_name in unique_pairs:
        left = next(e for e in engines if e.name == left_name)
        right = next(e for e in engines if e.name == right_name)
        for index, reading in enumerate(READING_NAMES):
            by_label = signatures[left_name][index] == signatures[right_name][index]
            by_search = brute_isomorphic(probe_of(left, reading), probe_of(right, reading))
            iso_equal += int(by_search)
            if by_label != by_search:
                iso_disagreements.append(f"{left_name} ~ {right_name} @ {reading}")

    # --- the regime keys, against the brute-force minimum ---
    regimes: dict[Regime, None] = {}
    for probe in probes.values():
        for node in probe.nodes:
            regimes.setdefault(node.state.regime, None)
    key_check = key_brute_disagreements(list(regimes))

    # --- replay and attribution ---
    replay_bad = [m for probe in probes.values() for m in replay_mismatches(probe)]
    attribution_bad = [v for probe in probes.values() for v in attribution_violations(probe)]

    # --- the responder: situations, representatives, rung two ---
    situations = _situations(probes)
    by_key: dict[tuple[Regime, Target, frozenset[Target]], list[Situation]] = {}
    for situation in situations:
        rule, mode, regime, target, validity = situation
        before = honoured_before(rule, EState(regime, mode))
        by_key.setdefault((regime, target, before), []).append(situation)
    rung_two_disagreements: list[str] = []
    representative_disagreements: list[str] = []
    member_disagreements: list[str] = []
    refused = 0
    for number, (key, group) in enumerate(by_key.items()):
        rule, mode, regime, target, _ = group[0]
        check = responder_crosscheck(regime, rule, mode, target)
        for measure, agrees in sorted(check.items()):
            if not agrees:
                rung_two_disagreements.append(f"situation {number} under {measure}")
        reference = least_responses(regime, moded_rule(rule, mode), target, "V1")
        for other in group:
            o_rule, o_mode, o_regime, o_target, o_validity = other
            mine = least_responses(o_regime, moded_rule(o_rule, o_mode), o_target, "V1")
            if mine != reference:
                representative_disagreements.append(f"{o_rule}/{o_mode} at situation {number}")
            strict = least_responses(o_regime, moded_rule(o_rule, o_mode), o_target, "V2")
            if strict is None or mine is None:
                refused += int(mine is None) + int(strict is None)
                if (strict is None) != (mine is None):
                    member_disagreements.append(f"{o_rule}/{o_mode} at situation {number}")
                continue
            if any(
                strict[m].deltas != mine[m].deltas or strict[m].cost != mine[m].cost
                for m in MEASURES
            ):
                member_disagreements.append(f"{o_rule}/{o_mode} at situation {number}")

    # --- the shape of every minimum, and the ties at the genesis regimes ---
    shapes: dict[str, int] = {}
    ties: dict[str, dict[str, list[int]]] = {r: {m: [] for m in MEASURES} for r in READING_NAMES}
    genesis = {reading.name: build_probe(engines[0], reading).nodes[0].state.regime for reading in readings()}
    for situation in situations:
        rule, mode, regime, target, validity = situation
        found = least_responses(regime, moded_rule(rule, mode), target, validity)
        if found is None:
            continue
        for measure in MEASURES:
            for delta in found[measure].deltas:
                shape = f"{found[measure].item_count}:{_item_shape(delta)}"
                shapes[shape] = shapes.get(shape, 0) + 1
            for reading, base in genesis.items():
                if regime == base:
                    ties[reading][measure].append(len(found[measure].deltas))
    ties_seen = {r: {m: sorted(set(v)) for m, v in row.items()} for r, row in ties.items()}

    # --- the demands the probe reads ---
    demands_read = demand_census(list(probes.values()))
    flipped_demands = flipped_at_genesis(genesis)

    refusals_in_probe = sum(
        1
        for probe in probes.values()
        for node in probe.nodes
        if node.answers is not None
        for record in node.answers
        if not record.answered
    )

    refused_labels = 0
    for engine in engines:
        try:
            check_declaration_label(engine, 1)
        except BundleRefused:
            refused_labels += 1

    counts = [engine.count(1) for engine in engines]
    shared = shared_capability_pairs(engines)
    shared_rules = sorted(
        {
            "/".join(sorted({left.split("/")[0], right.split("/")[0]}))
            for left, right in shared
        }
    )

    return {
        "class": {
            "members": len(engines),
            "literal_members": sum(e.literal for e in engines),
            "least_count": min(counts),
            "greatest_count": max(counts),
            "count_histogram": {str(c): counts.count(c) for c in sorted(set(counts))},
            "members_of_count_one": sum(c == 1 for c in counts),
            "labels_calling_one_declaration_refused": refused_labels,
            "shared_capability_pairs": len(shared),
            "shared_capability_rule_pairs": shared_rules,
            "shared_capability_settings": len({"/".join(p[0].split("/")[1:]) for p in shared}),
        },
        "members": members,
        "minima": minima,
        "live": sorted(n for n, v in live.items() if v),
        "two_kinded": sorted(n for n, v in two_kinded.items() if v),
        "streamless_live": sorted(
            e.name for e in engines if live[e.name] and not input_tally(e)["stream"]
        ),
        "probe": {
            "probes": len(probes),
            "distinct_probe_payloads": len(payloads),
            "member_classes_by_signature": len(
                {signature_digest(signatures[e.name]) for e in engines}
            ),
            "member_classes_by_content": len(
                {tuple(sorted(engine_probe_digests[e.name].items())) for e in engines}
            ),
            "nodes": sum(len(p.nodes) for p in probes.values()),
            "edges": sum(len(p.edges) for p in probes.values()),
            "root_terminals": {
                r: {
                    t: sum(1 for p in probes.values() if p.reading == r and p.root_terminal == t)
                    for t in sorted({p.root_terminal for p in probes.values()})
                }
                for r in READING_NAMES
            },
            "root_demands_plain": demands_read["root_demands_plain"],
            "demands_flipped_at_genesis": flipped_demands,
            "demands_at_growth_states": demands_read["demands_at_growth_states"],
            "same_demands_after_an_e4_response": demands_read["same_demands_after_an_e4_response"],
            "e4_children_at_L_reading_other_than_one_same": demands_read[
                "e4_children_at_L_reading_other_than_one_same"
            ],
            "refusals": refusals_in_probe,
            "minimum_shapes": dict(sorted(shapes.items())),
            "tie_counts_at_genesis": ties_seen,
            "replay_mismatches": replay_bad,
            "attribution_violations": attribution_bad,
        },
        "crosscheck": {
            "situations": len(situations),
            "distinct_member_one_situations": len(by_key),
            "rung_two_disagreements": rung_two_disagreements,
            "representative_disagreements": representative_disagreements,
            "member_one_two_disagreements": member_disagreements,
            "refused_situations": refused,
            "key_brute": key_check,
            "iso_pairs_compared": len(unique_pairs),
            "iso_comparisons": len(unique_pairs) * len(READING_NAMES),
            "iso_disagreements": iso_disagreements,
            "iso_comparisons_isomorphic": iso_equal,
            "iso_comparisons_not_isomorphic": len(unique_pairs) * len(READING_NAMES) - iso_equal,
        },
        "probe_payloads": dict(sorted(payloads.items())),
    }


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def score(reports: dict[str, Any]) -> dict[str, Any]:
    """Score the computational predictions.  The Lean rows, the ledger rows
    and the gate-time row are scored where their evidence lives and are
    named here as scored elsewhere rather than omitted."""
    scored: dict[str, Any] = {}
    cls = reports["class"]
    minima = reports["minima"]
    probe = reports["probe"]
    cross = reports["crosscheck"]

    def members(key: str) -> list[str]:
        return list(minima[key]["members"])

    c8 = {
        key: members(key)
        for key in ("class/all/1", "class/all/2", "literal/all/1", "literal/all/2")
    }
    scored["C-8"] = {
        "value": {
            "members": cls["members"],
            "literal_members": cls["literal_members"],
            "least_count": cls["least_count"],
            "greatest_count": cls["greatest_count"],
            "minima": c8,
        },
        "verdict": _verdict(
            cls["members"] == 144
            and cls["literal_members"] == 108
            and cls["least_count"] == 6
            and cls["greatest_count"] == 10
            and all(c8[key] == EXPECTED_MINIMA[key] for key in c8)
        ),
    }

    incl = {key: minima[key]["inclusion_minimal"] for key in ("class/all/1", "literal/all/1")}
    scored["C-9"] = {
        "value": {
            "inclusion_minimal": incl,
            "shared_capability_pairs": cls["shared_capability_pairs"],
            "shared_capability_rule_pairs": cls["shared_capability_rule_pairs"],
            "shared_capability_settings": cls["shared_capability_settings"],
        },
        "verdict": _verdict(
            all(incl[key] == members(key) for key in incl)
            and cls["shared_capability_pairs"] == 32
            and cls["shared_capability_rule_pairs"] == ["E2/E7", "E3/E4"]
            and cls["shared_capability_settings"] == 16
        ),
    }

    scored["C-10"] = {
        "value": {
            "members_of_count_one": cls["members_of_count_one"],
            "labels_calling_one_declaration_refused": cls["labels_calling_one_declaration_refused"],
        },
        "verdict": _verdict(
            cls["members_of_count_one"] == 0
            and cls["labels_calling_one_declaration_refused"] == cls["members"]
        ),
    }

    plain = probe["root_demands_plain"]
    flipped = probe["demands_flipped_at_genesis"]
    plain_ok = all(
        plain[r][rule] == (["apart"] * EXPECTED_ROOT_DEMANDS[r] if rule == "E4" else [])
        for r in READING_NAMES
        for rule in RULE_NAMES
    )
    flipped_ok = all(
        flipped[r][rule]
        == (["apart"] * EXPECTED_ROOT_DEMANDS[r] if rule in FLIPPED_DEMANDING else [])
        for r in READING_NAMES
        for rule in RULE_NAMES
    )
    scored["C-11"] = {
        "value": {
            "root_demands_plain": plain,
            "demands_flipped_at_genesis": flipped,
            "demands_at_growth_states": probe["demands_at_growth_states"],
        },
        "verdict": _verdict(plain_ok and flipped_ok and probe["demands_at_growth_states"] == 0),
    }

    shapes = probe["minimum_shapes"]
    ties = probe["tie_counts_at_genesis"]
    scored["C-12"] = {
        "value": {
            "minimum_shapes": shapes,
            "tie_counts_at_genesis": ties,
            "member_one_two_disagreements": len(cross["member_one_two_disagreements"]),
            "refusals": probe["refusals"],
        },
        "verdict": _verdict(
            set(shapes) == {"2:form+inst"}
            and all(ties[r][m] == [EXPECTED_TIES[r][m]] for r in READING_NAMES for m in MEASURES)
            and not cross["member_one_two_disagreements"]
            and probe["refusals"] == 0
            and cross["refused_situations"] == 0
        ),
    }

    after = probe["same_demands_after_an_e4_response"]
    scored["C-13"] = {
        "value": {
            "same_demands_after_an_e4_response": after,
            "e4_children_at_L_reading_other_than_one_same": probe[
                "e4_children_at_L_reading_other_than_one_same"
            ],
        },
        "verdict": _verdict(
            all(after[r] and min(after[r]) >= 1 for r in READING_NAMES)
            and probe["e4_children_at_L_reading_other_than_one_same"] == 0
        ),
    }

    scored["C-14"] = {
        "value": {"live": len(reports["live"]), "two_kinded": len(reports["two_kinded"])},
        "verdict": _verdict(
            reports["live"] == EXPECTED_LIVE and reports["two_kinded"] == EXPECTED_TWO_KINDED
        ),
    }

    c15_keys = [k for k in EXPECTED_MINIMA if "/all/" not in k]
    scored["C-15"] = {
        "value": {key: members(key) for key in c15_keys},
        "verdict": _verdict(all(members(key) == EXPECTED_MINIMA[key] for key in c15_keys)),
    }

    classes = {key: minima[key]["probe_classes"] for key in EXPECTED_PROBE_CLASSES}
    scored["C-16"] = {
        "value": classes,
        "verdict": _verdict(classes == EXPECTED_PROBE_CLASSES),
    }

    initial = {
        key: {
            "in_minima": minima[key]["initial_in_minima"],
            "in_pool": minima[key]["initial_in_pool"],
            "measures_present": minima[key]["measures_present"],
        }
        for key in EXPECTED_MINIMA
    }
    scored["C-17"] = {
        "value": initial,
        "verdict": _verdict(
            all(
                not row["in_minima"] and not row["in_pool"] and row["measures_present"] == ["mu1", "mu2"]
                for row in initial.values()
            )
        ),
    }

    scored["C-18"] = {
        "value": {
            "replay_mismatches": len(probe["replay_mismatches"]),
            "attribution_violations": len(probe["attribution_violations"]),
            "nodes": probe["nodes"],
            "edges": probe["edges"],
        },
        "verdict": _verdict(
            not probe["replay_mismatches"] and not probe["attribution_violations"]
        ),
    }

    scored["C-19"] = {
        "value": {
            "distinct_member_one_situations": cross["distinct_member_one_situations"],
            "situations": cross["situations"],
            "rung_two_disagreements": len(cross["rung_two_disagreements"]),
            "representative_disagreements": len(cross["representative_disagreements"]),
            "key_brute": cross["key_brute"],
            "iso_comparisons": cross["iso_comparisons"],
            "iso_disagreements": len(cross["iso_disagreements"]),
            "iso_comparisons_isomorphic": cross["iso_comparisons_isomorphic"],
            "iso_comparisons_not_isomorphic": cross["iso_comparisons_not_isomorphic"],
        },
        "verdict": _verdict(
            cross["distinct_member_one_situations"] == 4
            and not cross["rung_two_disagreements"]
            and not cross["representative_disagreements"]
            and cross["key_brute"]["disagreements"] == 0
            and cross["iso_comparisons_isomorphic"] > 0
            and cross["iso_comparisons_not_isomorphic"] > 0
            and not cross["iso_disagreements"]
        ),
    }

    scored["C-22"] = {
        "value": {"streamless_live": len(reports["streamless_live"]), "input_count_claim": "none"},
        "verdict": _verdict(reports["streamless_live"] == EXPECTED_STREAMLESS_LIVE),
    }

    for pid, where in (
        ("C-1", "the committed Lean package, checked by verify_lean.py and test_census.py"),
        ("C-2", "the committed Lean package, checked by test_census.py"),
        ("C-3", "the committed Lean package, checked by test_census.py"),
        ("C-4", "the committed Lean package, checked by test_census.py"),
        ("C-5", "the committed Lean package, checked by test_census.py"),
        ("C-6", "the committed Lean package, checked by test_census.py"),
        ("C-7", "receipts/lean_axioms.txt, checked by verify_lean.py"),
        ("C-20", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("C-21", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("C-23", "the receipt bytes, --check and test_engine.py; the time in STATUS.md"),
    ):
        scored[pid] = {"value": f"scored elsewhere: {where}", "verdict": "ELSEWHERE"}
    return scored


def build() -> dict[str, Any]:
    reports = analyse()
    return {
        "authority_effect": "None",
        "attempt": "continuation one",
        "bounds": {"max_items": 2, "max_arity": 2, "max_data": 4, "probe_levels": 2},
        "input_count_claim": "none",
        "predictions_scored": score(reports),
        "predictions_sha256": frozen_digest("PREDICTIONS.md"),
        "prompt_sha256": frozen_digest("PROMPT.md"),
        "readings": list(READING_NAMES),
        "reports": reports,
        "write_root": "research/second_engine",
    }


def render(payload: dict[str, Any]) -> bytes:
    text = json.dumps(payload, indent=1, sort_keys=True, ensure_ascii=True) + "\n"
    return text.encode("utf-8")


def write(payload: dict[str, Any], receipts: pathlib.Path) -> pathlib.Path:
    receipts.mkdir(parents=True, exist_ok=True)
    target = receipts / RECEIPT_NAME
    target.write_bytes(render(payload))
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run continuation one.")
    parser.add_argument("--receipts", default=str(HERE / "receipts"), help="output directory")
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare with the committed receipt and write nothing",
    )
    args = parser.parse_args(argv)
    receipts = pathlib.Path(args.receipts)
    payload = build()
    fresh = render(payload)
    bad = forbidden_keys(payload)
    if bad:
        print(f"FAIL: the receipt carries forbidden keys: {bad}")
        return 1
    if len(fresh) > MEGABYTE:
        print(f"FAIL: the receipt is {len(fresh)} bytes and must be split")
        return 1
    if args.check:
        target = receipts / RECEIPT_NAME
        if not target.exists():
            print(f"FAIL: {target} is missing")
            return 1
        committed = target.read_bytes().replace(b"\r\n", b"\n")
        if committed != fresh:
            print(f"FAIL: {target} differs from a fresh run")
            return 1
        print(f"receipt matches a fresh run ({len(fresh)} bytes)")
    else:
        target = write(payload, receipts)
        print(f"wrote {target} ({len(fresh)} bytes)")
    scored = payload["predictions_scored"]
    for pid in sorted(scored, key=lambda name: (len(name), name)):
        print(f"  {pid}: {scored[pid]['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

