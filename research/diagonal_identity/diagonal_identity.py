"""Deterministic record of the typed-split standing.

Does not import sealed `code/derivation`.  Formula identity with Continuum
is a source-text comparison, not a Lake import.
AuthorityEffect: None.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Mapping

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
COVERING = HERE / "lean" / "DiagonalIdentity" / "Covering.lean"
CONTINUUM = REPO / "research" / "unboundedness" / "lean" / "Continuum.lean"

TERMINAL = "DUAL_NOT_IDENTITY_ON_DECLARED_CARRIERS"

FORMULA_NAMES = (
    "diagBool",
    "flipFin",
    "diagSeq",
    "diagThread",
)


def _def_body(source: str, name: str) -> str:
    match = re.search(
        rf"^def {re.escape(name)}\b.*?(?=^(?:def|theorem|end)\b|\Z)",
        source,
        flags=re.M | re.S,
    )
    if match is None:
        raise ValueError(f"definition {name} not found")
    return re.sub(r"\s+", " ", match.group(0)).strip()


def formula_bodies(covering: str, continuum: str) -> dict[str, tuple[str, str]]:
    return {name: (_def_body(covering, name), _def_body(continuum, name)) for name in FORMULA_NAMES}


def formulas_match(covering: str, continuum: str) -> list[str]:
    """Names whose covering restatement is not the Continuum formula."""
    mismatches: list[str] = []
    for name, (ours, theirs) in formula_bodies(covering, continuum).items():
        ours_core = ours.replace("AuthorityEffect: None. ", "")
        theirs_core = theirs.replace("AuthorityEffect: None. ", "")
        if ours_core.split(":=", 1)[-1] != theirs_core.split(":=", 1)[-1]:
            mismatches.append(name)
    return mismatches


def record() -> dict[str, object]:
    covering = COVERING.read_text(encoding="utf-8")
    continuum = CONTINUUM.read_text(encoding="utf-8")
    mismatches = formulas_match(covering, continuum)
    return {
        "terminal": TERMINAL,
        "identity_proved": False,
        "formula_mismatches": mismatches,
        "theorems": [
            "DiagonalIdentity.Covering.diagonal_bool",
            "DiagonalIdentity.Covering.seq_uncountable",
            "DiagonalIdentity.Covering.thread_uncountable",
            "DiagonalIdentity.Combinator.diagFlip_ne_row",
            "DiagonalIdentity.Collapse.d2_constant_obstructs",
            "DiagonalIdentity.Split.collapse_yes_covering_no",
            "DiagonalIdentity.Split.family_miss_and_identifying_push",
            "DiagonalIdentity.Dual.d2Const_not_injective",
            "DiagonalIdentity.Dual.d2Const_not_as_covering_family",
            "DiagonalIdentity.Dual.family_not_surjective",
            "DiagonalIdentity.Dual.family_not_as_d2_const",
            "DiagonalIdentity.Dual.covering_miss_witness_is_diagFlip",
            "DiagonalIdentity.Dual.dual_on_declared_carriers",
        ],
        "open": [
            "a relation on Thread whose collapse recodes covering-miss",
        ],
    }


def standing(payload: Mapping[str, object] | None = None) -> str:
    data = dict(payload) if payload is not None else record()
    if data.get("identity_proved") is True:
        raise ValueError("identity_proved must stay False; identity is not proved")
    if data.get("formula_mismatches"):
        raise ValueError(f"covering formulas drifted: {data['formula_mismatches']}")
    terminal = data.get("terminal")
    if terminal != TERMINAL:
        raise ValueError(f"unexpected terminal {terminal!r}")
    return TERMINAL
