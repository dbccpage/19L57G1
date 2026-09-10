"""Five reading-F Challenge-3 mu1 class representatives, and the L three.

Classification: deterministic computation mirroring the Lean distinctness
theorems.  Completeness of the catalog as all minima is the sealed engine
enumeration, not this module.

AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from pathlib import Path

_CODE = Path(__file__).resolve().parents[2] / "code"
if str(_CODE) not in sys.path:
    sys.path.insert(0, str(_CODE))

from derivation.candidates import Bounds, Delta, delta_events, min_responses
from derivation.engine import (
    READING_F,
    READING_L,
    Reading,
    challenge3_report,
    delta_label,
)
from derivation.iso import CanonKey, canonical, isomorphic
from derivation.model import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    Event,
    Impose,
    Regime,
    Supply,
    replay,
)

BOUNDS = Bounds(max_items=2, max_arity=2)
LEAN_THEOREM = "FClassDistinctness.five_classes_pairwise_noniso"
CATALOG_SCOPE = (
    "engine enumeration under Bounds(2,2); not this theorem"
)

# Lean field snapshots: (n_data, forms, insts, rules, reqs).
LEAN_F_FIELDS: dict[str, tuple[
    int,
    tuple[int, ...],
    tuple[tuple[int, tuple[int, ...]], ...],
    tuple[int, ...],
    tuple[tuple[int, int], ...],
]] = {
    "MarkF": (3, (1,), ((0, (1,)),), (), ((1, 2),)),
    "DiagF": (3, (2,), ((0, (1, 1)),), (), ((1, 2),)),
    "LinkF": (3, (2,), ((0, (1, 2)),), (), ((1, 2),)),
    "OutF": (3, (2,), ((0, (1, 0)),), (), ((1, 2),)),
    "InF": (3, (2,), ((0, (0, 1)),), (), ((1, 2),)),
}

LEAN_L_FIELDS: dict[str, tuple[
    int,
    tuple[int, ...],
    tuple[tuple[int, tuple[int, ...]], ...],
    tuple[int, ...],
    tuple[tuple[int, int], ...],
]] = {
    "U0": (2, (1,), ((0, (0,)),), (), ((0, 1),)),
    "BL": (2, (2,), ((0, (0, 1)),), (), ((0, 1),)),
    "BD": (2, (2,), ((0, (0, 0)),), (), ((0, 1),)),
}


def _mk(*events: Event) -> Regime:
    return replay(events)


def genesis_f() -> tuple[Event, ...]:
    return (
        Supply("<>"), AdmitDatum("<>"),
        Supply("<a>"), Supply("<a>"), Supply("<ab>"),
        AdmitDatum("<a>"), AdmitDatum("<ab>"),
        Impose(1, 2),
    )


def genesis_l() -> tuple[Event, ...]:
    return (
        Supply("<>"),
        Supply("<a>"), Supply("<a>"), Supply("<ab>"),
        AdmitDatum("<a>"), AdmitDatum("<ab>"),
        Impose(0, 1),
    )


def mark_f() -> Regime:
    return _mk(*genesis_f(), AdmitForm(1), AdmitInst(0, (1,)))


def diag_f() -> Regime:
    return _mk(*genesis_f(), AdmitForm(2), AdmitInst(0, (1, 1)))


def link_f() -> Regime:
    return _mk(*genesis_f(), AdmitForm(2), AdmitInst(0, (1, 2)))


def out_f() -> Regime:
    return _mk(*genesis_f(), AdmitForm(2), AdmitInst(0, (1, 0)))


def in_f() -> Regime:
    return _mk(*genesis_f(), AdmitForm(2), AdmitInst(0, (0, 1)))


def mark_f_swap() -> Regime:
    return _mk(*genesis_f(), AdmitForm(1), AdmitInst(0, (2,)))


def diag_f_swap() -> Regime:
    return _mk(*genesis_f(), AdmitForm(2), AdmitInst(0, (2, 2)))


def link_f_swap() -> Regime:
    return _mk(*genesis_f(), AdmitForm(2), AdmitInst(0, (2, 1)))


def out_f_swap() -> Regime:
    return _mk(*genesis_f(), AdmitForm(2), AdmitInst(0, (2, 0)))


def in_f_swap() -> Regime:
    return _mk(*genesis_f(), AdmitForm(2), AdmitInst(0, (0, 2)))


def mark_l() -> Regime:
    return _mk(*genesis_l(), AdmitForm(1), AdmitInst(0, (0,)))


def link_l() -> Regime:
    return _mk(*genesis_l(), AdmitForm(2), AdmitInst(0, (0, 1)))


def diag_l() -> Regime:
    return _mk(*genesis_l(), AdmitForm(2), AdmitInst(0, (0, 0)))


F_REPS: tuple[tuple[str, Regime], ...] = (
    ("MarkF", mark_f()),
    ("DiagF", diag_f()),
    ("LinkF", link_f()),
    ("OutF", out_f()),
    ("InF", in_f()),
)

L_REPS: tuple[tuple[str, Regime], ...] = (
    ("U0", mark_l()),
    ("BL", link_l()),
    ("BD", diag_l()),
)

F_SWAPS: tuple[tuple[str, Regime, Regime], ...] = (
    ("MarkF", mark_f(), mark_f_swap()),
    ("DiagF", diag_f(), diag_f_swap()),
    ("LinkF", link_f(), link_f_swap()),
    ("OutF", out_f(), out_f_swap()),
    ("InF", in_f(), in_f_swap()),
)


def regime_fields(
    r: Regime,
) -> tuple[
    int,
    tuple[int, ...],
    tuple[tuple[int, tuple[int, ...]], ...],
    tuple[int, ...],
    tuple[tuple[int, int], ...],
]:
    return (
        r.n_data(),
        r.forms,
        tuple(sorted(r.insts)),
        tuple(sorted(r.rules)),
        tuple(sorted(r.reqs)),
    )


def pairwise_noniso(reps: tuple[tuple[str, Regime], ...]) -> list[tuple[str, str]]:
    disagree: list[tuple[str, str]] = []
    for i, (na, a) in enumerate(reps):
        for nb, b in reps[i + 1 :]:
            if isomorphic(a, b):
                disagree.append((na, nb))
    return disagree


def mu1_class_regimes(
    reading: Reading,
) -> list[tuple[str, Regime, int]]:
    """Engine mu1 classes as (label, representative regime, class size)."""
    base = replay(reading.genesis)
    i, j = reading.target
    found = min_responses(base, (i, j), "mu1", BOUNDS)
    if found is None:
        raise RuntimeError(f"progress lemma violated for reading {reading.name}")
    grouped: dict[CanonKey, list[tuple[Delta, Regime]]] = {}
    for delta in found.deltas:
        child = replay((Impose(i, j),) + delta_events(base, delta), base)
        grouped.setdefault(canonical(child), []).append((delta, child))
    out: list[tuple[str, Regime, int]] = []
    for members in grouped.values():
        delta, child = members[0]
        out.append((delta_label(base, delta), child, len(members)))
    return sorted(out, key=lambda row: row[0])


def rep_engine_hits(
    reps: tuple[tuple[str, Regime], ...],
    classes: list[tuple[str, Regime, int]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for name, reg in reps:
        labels = [label for label, child, _ in classes if isomorphic(reg, child)]
        rows.append({"rep": name, "engine_labels": labels})
    return rows


def claim_errors(record: dict[str, object]) -> tuple[str, ...]:
    errors: list[str] = []
    if record.get("schema") != "f-class-distinctness-v1":
        errors.append("SCHEMA_GUARD")
    if record.get("authority_effect") != "None":
        errors.append("AUTHORITY_GUARD")
    if record.get("readings_carried") != ["L", "F"]:
        errors.append("READINGS_GUARD")
    if record.get("f_engine_class_count") != 5:
        errors.append("F_COUNT_GUARD")
    if record.get("l_engine_class_count") != 3:
        errors.append("L_COUNT_GUARD")
    if record.get("pairwise_noniso") is not True:
        errors.append("PAIRWISE_GUARD")
    hits = record.get("pairwise_iso_hits")
    if hits != []:
        errors.append("ISO_HITS_GUARD")
    if record.get("lean_theorem") != LEAN_THEOREM:
        errors.append("THEOREM_GUARD")
    if record.get("catalog_completeness") != CATALOG_SCOPE:
        errors.append("CATALOG_GUARD")
    if record.get("l_pairwise_iso_hits") != []:
        errors.append("L_ISO_HITS_GUARD")
    if record.get("within_class_iso_failures") != []:
        errors.append("WITHIN_GUARD")
    matches = record.get("f_rep_to_engine")
    if not isinstance(matches, list) or len(matches) != 5:
        errors.append("REP_ENGINE_GUARD")
    else:
        for row in matches:
            if not isinstance(row, dict):
                errors.append("REP_ENGINE_GUARD")
                break
            labels = row.get("engine_labels")
            if not isinstance(labels, list) or len(labels) != 1:
                errors.append("REP_ENGINE_GUARD")
                break
    return tuple(errors)


def class_record() -> dict[str, object]:
    report_f = challenge3_report(READING_F, BOUNDS)
    report_l = challenge3_report(READING_L, BOUNDS)
    mu1_f = report_f["mu1"]
    mu1_l = report_l["mu1"]
    assert isinstance(mu1_f, dict) and isinstance(mu1_l, dict)
    f_classes = mu1_f["iso_classes"]
    l_classes = mu1_l["iso_classes"]
    assert isinstance(f_classes, list) and isinstance(l_classes, list)
    f_engine = mu1_class_regimes(READING_F)
    l_engine = mu1_class_regimes(READING_L)
    disagree_f = pairwise_noniso(F_REPS)
    disagree_l = pairwise_noniso(L_REPS)
    within = [
        name for name, a, b in F_SWAPS if not isomorphic(a, b)
    ]
    matches = rep_engine_hits(F_REPS, f_engine)
    record: dict[str, object] = {
        "schema": "f-class-distinctness-v1",
        "authority_effect": "None",
        "readings_carried": ["L", "F"],
        "f_engine_class_count": len(f_classes),
        "l_engine_class_count": len(l_classes),
        "f_engine_labels": [label for label, _, _ in f_engine],
        "l_engine_labels": [label for label, _, _ in l_engine],
        "f_representatives": [name for name, _ in F_REPS],
        "l_representatives": [name for name, _ in L_REPS],
        "f_fields": {name: list(regime_fields(reg)) for name, reg in F_REPS},
        "l_fields": {name: list(regime_fields(reg)) for name, reg in L_REPS},
        "pairwise_iso_hits": [[a, b] for a, b in disagree_f],
        "l_pairwise_iso_hits": [[a, b] for a, b in disagree_l],
        "pairwise_noniso": len(disagree_f) == 0 and len(disagree_l) == 0,
        "within_class_iso_failures": within,
        "f_rep_to_engine": matches,
        "lean_theorem": LEAN_THEOREM,
        "catalog_completeness": CATALOG_SCOPE,
    }
    return record
