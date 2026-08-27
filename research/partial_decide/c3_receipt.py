"""Deterministic Challenge-3 receipt for the partial decision grade.

The readings, targets, candidate measures, and bounds consumed here are the
ones already declared by the sealed engine.  The bounded computation
enumerates candidates and replays their admission-event values only into
ephemeral comparison children used for quotienting.  This module records the
four predeclared outputs; it derives no input from the panel, authorizes no
candidate, persistently applies no response, commits no event to the declared
base, and supplies no object-language demand generator.

AuthorityEffect: None
"""

from __future__ import annotations

import json
from pathlib import Path

from derivation.candidates import Bounds
from derivation.engine import READING_F, READING_L, Reading
from derivation.model import replay

from partial_decide import (
    Grade,
    Measure,
    UniqueClass,
    UniqueDelta,
    decide,
    grade_kind,
    grade_payload,
)

BOUNDS = Bounds(max_items=2, max_arity=2)
ISO_PERM_BUDGET = 100_000
MEASURES: tuple[Measure, Measure] = ("mu1", "mu2")
HERE = Path(__file__).resolve().parent
PINS_PATH = HERE / "SOURCE_PINS.json"


def _source_snapshot() -> dict[str, str]:
    payload: object = json.loads(PINS_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("SOURCE_PINS.json must contain an object")
    snapshot = payload.get("source_snapshot")
    if not isinstance(snapshot, dict):
        raise RuntimeError("SOURCE_PINS.json has no source_snapshot object")
    commit = snapshot.get("commit")
    tree = snapshot.get("tree")
    if not isinstance(commit, str) or not isinstance(tree, str):
        raise RuntimeError("source_snapshot commit and tree must be strings")
    return {"commit": commit, "tree": tree}


def _option_payload(grade: Grade | None) -> dict[str, object]:
    if grade is None:
        return {
            "option": "none",
            "reason": "no_minimum_within_declared_bounds",
        }
    return {"grade": grade_payload(grade), "option": "some"}


def _reading_payload(reading: Reading) -> dict[str, object]:
    regime = replay(reading.genesis)
    grades: dict[str, Grade | None] = {
        measure: decide(
            regime,
            reading.target[0],
            reading.target[1],
            measure,
            BOUNDS,
            perm_budget=ISO_PERM_BUDGET,
        )
        for measure in MEASURES
    }
    return {
        "grades": {
            measure: _option_payload(grade) for measure, grade in grades.items()
        },
        "reading": reading.name,
        "target": list(reading.target),
    }


def receipt_payload() -> dict[str, object]:
    """Return the exact bounded C3 grade record for both retained readings."""

    readings = [_reading_payload(READING_L), _reading_payload(READING_F)]
    all_grades = [
        grade
        for reading in (READING_L, READING_F)
        for grade in (
            decide(
                replay(reading.genesis),
                reading.target[0],
                reading.target[1],
                measure,
                BOUNDS,
                perm_budget=ISO_PERM_BUDGET,
            )
            for measure in MEASURES
        )
    ]
    mu2_grades = [
        decide(
            replay(reading.genesis),
            reading.target[0],
            reading.target[1],
            "mu2",
            BOUNDS,
            perm_budget=ISO_PERM_BUDGET,
        )
        for reading in (READING_L, READING_F)
    ]
    if any(isinstance(grade, UniqueDelta) for grade in all_grades):
        raise RuntimeError("C3 unexpectedly acquired a unique literal delta")
    if not all(isinstance(grade, UniqueClass) for grade in mu2_grades):
        raise RuntimeError("C3 mu2 no longer has one inhabited quotient class")
    return {
        "authority_effect": "None",
        "classification": "deterministic metatheoretic computation",
        "contract": {
            "none": "no minimum inside the declared finite candidate bounds",
            "tie": "at least two quotient classes",
            "unique_class": "one quotient class with multiple raw deltas",
            "unique_delta": "one literal raw minimum",
        },
        "panel_input": {
            "status": "not_connected_without_a_declared_correspondence",
            "meaning": (
                "certNeg and PanelEquiv may motivate a separately declared "
                "request but do not choose this engine pair"
            ),
        },
        "readings": readings,
        "schema": "partial_decide_c3_receipt/v1",
        "source_snapshot": _source_snapshot(),
        "terminals": [
            "C3_UNIQUE_DELTA_EMPTY",
            "C3_MU2_UNIQUE_CLASS_INHABITED",
            "G3_REMAINS_CONJECTURE",
            "G4_REMAINS_CONJECTURE",
            "NO_AUTHORIZED_OR_PERSISTENT_RESPONSE_APPLICATION",
            "NO_EVENT_COMMITTED_TO_DECLARED_BASE",
            "NO_PANEL_DERIVED_INPUT",
            "NO_PANEL_ENGINE_ADAPTER",
            "NO_RESPONSE_AUTHORIZATION",
            "OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE",
            "PANEL_TO_ENGINE_LINK_NOT_DEFINED",
        ],
    }


def receipt_bytes() -> bytes:
    return (
        json.dumps(receipt_payload(), indent=2, sort_keys=True, ensure_ascii=True)
        + "\n"
    ).encode("utf-8")


def terminal_grade_tags() -> tuple[str, ...]:
    """Small stable summary used only by tests."""

    return tuple(
        grade_kind(
            decide(
                replay(reading.genesis),
                reading.target[0],
                reading.target[1],
                measure,
                BOUNDS,
                perm_budget=ISO_PERM_BUDGET,
            )
        )
        for reading in (READING_L, READING_F)
        for measure in MEASURES
    )


__all__ = [
    "BOUNDS",
    "ISO_PERM_BUDGET",
    "MEASURES",
    "receipt_bytes",
    "receipt_payload",
]
