"""Deterministic receipt for the local finite-alphabet G1 result.

Classification: metatheory apparatus and receipt binding.  The receipt
quotes the exact Lean declarations under review, resolves every new theorem
through the committed axiom inventory, and recomputes both supporting finite
artifacts.  It carries no timestamp or ambient environment value.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Sequence

from derivation.export import Json, dumps_deterministic
from derivation.g4_engine_import_branch import BOUNDS, FIRST_N, LAST_N, g4_report
from derivation.local_strategy import DEFAULT_MAX_CHAIN, STRATEGIES, artifact_payload

BASE_COMMIT = "24bd2464fc4546d8fb3d244809aa769b37c22964"
TASK_SHA256 = "E2CAF8EA7CD849F09BFF587EB31229AC678F5552EFA51F1B33AAE5A6D5F04559"
REQUIREMENTS_SHA256 = (
    "BFE7283F51A19B579FA08F8C7E6B19A714885166607277B94928BB8A23885BBF"
)
LEAN_VERSION = "4.33.0"
LAKE_VERSION = "5.0.0"
PYTHON_VERSION = "3.14.2"

NEW_THEOREMS = (
    "SeparationCapacity.filter_range_decide_eq",
    "SeparationCapacity.filter_range_succ_eq",
    "SeparationCapacity.filter_range_eq",
    "SeparationCapacity.incoming_edges_interior",
    "SeparationCapacity.outgoing_edges_interior",
    "SeparationCapacity.profile2_interior",
    "SeparationCapacity.profileD_radius_one",
    "SeparationCapacity.radius_one_agrees_with_sealed_depth2",
    "LocalFiniteAlphabet.fires_every_strategy",
    "LocalFiniteAlphabet.identityGrade_implies_clears",
    "LocalFiniteAlphabet.strategy_capacity_collision",
    "LocalFiniteAlphabet.finite_local_not_clears",
    "LocalFiniteAlphabet.finite_local_not_identityGrade",
    "LocalFiniteAlphabet.g1_local_finite_alphabet_class",
    "LocalFiniteAlphabet.profileCode_lt_eight",
    "LocalFiniteAlphabet.bare_finite",
    "LocalFiniteAlphabet.presence_finite",
    "LocalFiniteAlphabet.presence_eq_bare",
    "LocalFiniteAlphabet.depthTwo_finite",
    "LocalFiniteAlphabet.depthTwo_clears_n4",
    "LocalFiniteAlphabet.perPair_recurring",
    "LocalFiniteAlphabet.perPair_identityGrade",
    "LocalFiniteAlphabet.perPair_not_finite",
    "LocalFiniteAlphabet.valued_oneTimeIdentity",
    "LocalFiniteAlphabet.valued_not_finite",
    "LocalFiniteAlphabet.valued_clears",
    "LocalFiniteAlphabet.class_nonvacuity",
    "LocalFiniteAlphabet.bare_not_identityGrade",
    "LocalFiniteAlphabet.bare_classification",
    "LocalFiniteAlphabet.presence_classification",
    "LocalFiniteAlphabet.depthTwo_classification",
    "G1Class.local_strategy_cycle_impossible",
    "G1Class.g1_class_exclusion",
    "G1Class.clears_does_not_imply_not_fires",
)

TERMINALS = (
    "ENDOGENOUS_GENERATION_PROVED",
    "LOCAL_STRATEGY_CLASS_DEFINED",
    "FIVE_STRATEGIES_CLASSIFIED",
    "T5_PROFILE_CORRESPONDENCE_PROVED",
    "CAPACITY_APPLIES_TO_EVERY_CLASS_MEMBER",
    "G1_CLASS_EXCLUSION_PROVED",
    "G3_REMAINS_CONJECTURE",
    "G4_HOLDS_UNDER_MU2",
    "G4_FAILS_AT_<3,mu1,reading_F_outside_target_argument>",
    "OB1_UNCHANGED",
    "OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE",
    "HYGIENE_H1_SKIPPED",
    "HYGIENE_H2_SKIPPED",
    "HYGIENE_H3_SKIPPED",
    "HYGIENE_H4_DONE",
    "HYGIENE_H5_DONE",
    "HYGIENE_H6_SKIPPED",
)

OPEN_SENTENCES = (
    "OB-1 / CL-CLOSURE-POLICY remains OPEN outside the declared LocalStrategy class.",
    "G3 remains a CONJECTURE because no state-transition hypothesis connects post-repair clearing to the absence of future pre-repair demands.",
    "Strategies outside the fixed-radius finite-alphabet LocalStrategy class remain OPEN, including index-inspecting views and alphabets that grow with chain length.",
    "F4 chain initiality remains carried and OPEN.",
    "The definition-level axiom residual remains OPEN and is not addressed by this run.",
    "The comparison-heading conflict recorded as OB-3 remains OPEN for an author act.",
)

WITHDRAWN_SENTENCES = (
    "The previous three-line TERMINAL block is WITHDRAWN as the current complete terminal; its generation theorem remains supported.",
    "The statement that the general-n Generator.profile2/profileD radius-one correspondence remains OPEN is WITHDRAWN.",
    "The statement that the repair-strategy-class consequence of CapacityBound.capacity_bound remains OPEN is WITHDRAWN.",
    "The first T5 proof shape using generic Nat equality filtering is WITHDRAWN because its use-site axiom report exposed Classical.choice; the repaired proof uses decide.",
    "G4 as an unqualified conjecture is WITHDRAWN only for the declared finite check: mu2 holds, while reading-F/mu1 fails at n=3.",
)

_AXIOM_RE = re.compile(
    r"'(?P<name>[^']+)' (?P<status>does not depend on any axioms|"
    r"depends on axioms: \[(?P<axioms>[^\]]*)\])$"
)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest().upper()


def require_sha256(path: Path, expected: str, label: str) -> bytes:
    raw = path.read_bytes()
    actual = sha256_bytes(raw)
    if actual != expected:
        raise ValueError(
            f"{label} SHA-256 mismatch: expected {expected}, got {actual}"
        )
    return raw


def quote_between(source: str, start: str, end: str, label: str) -> str:
    start_index = source.find(start)
    if start_index < 0:
        raise ValueError(f"missing {label} start marker: {start}")
    end_index = source.find(end, start_index)
    if end_index < 0:
        raise ValueError(f"missing {label} end marker: {end}")
    return source[start_index:end_index].strip()


def quote_theorem_statement(source: str, theorem: str) -> str:
    start = f"theorem {theorem}"
    start_index = source.find(start)
    if start_index < 0:
        raise ValueError(f"missing theorem statement: {theorem}")
    end_index = source.find(":=", start_index)
    if end_index < 0:
        raise ValueError(f"missing theorem proof delimiter: {theorem}")
    return source[start_index : end_index + 2].strip()


def parse_axiom_reports(
    report_text: str, expected_names: Sequence[str] = NEW_THEOREMS
) -> list[dict[str, Json]]:
    found: dict[str, tuple[str, list[str]]] = {}
    for line in report_text.splitlines():
        match = _AXIOM_RE.search(line)
        if match is None:
            continue
        name = match.group("name")
        if name not in expected_names:
            continue
        if name in found:
            raise ValueError(f"duplicate axiom report: {name}")
        raw_axioms = match.group("axioms")
        axioms = [] if raw_axioms is None or raw_axioms == "" else raw_axioms.split(", ")
        found[name] = (match.group(0), axioms)

    rows: list[dict[str, Json]] = []
    for name in expected_names:
        if name not in found:
            raise ValueError(f"missing axiom report: {name}")
        normalized, axioms = found[name]
        outside = sorted(set(axioms) - {"propext", "Quot.sound"})
        if outside:
            raise ValueError(f"disallowed axioms for {name}: {outside}")
        rows.append(
            {
                "theorem": name,
                "axioms": axioms,
                "report": normalized,
            }
        )
    return rows


def _source_quotes(root: Path) -> dict[str, Json]:
    local = (root / "lean4/Derivation/LocalStrategy.lean").read_text(
        encoding="utf-8"
    )
    capacity = (root / "lean4/Derivation/CapacityBound.lean").read_text(
        encoding="utf-8"
    )
    g1 = (root / "lean4/Derivation/G1Class.lean").read_text(encoding="utf-8")
    return {
        "ViewLocal": quote_between(
            capacity,
            "def ViewLocal",
            "\n\n/-- A local view cannot separate",
            "ViewLocal",
        ),
        "LocalStrategy": quote_between(
            local,
            "structure LocalStrategy",
            "\n\n/-- One fixed `k`",
            "LocalStrategy",
        ),
        "FiniteDeclaration": quote_between(
            local,
            "def FiniteDeclaration",
            "\n\n/-- The strategy explicitly requests",
            "FiniteDeclaration",
        ),
        "RecurringImport": quote_between(
            local,
            "def RecurringImport",
            "\n\n/-- Two distinct carrier points",
            "RecurringImport",
        ),
        "Fires": quote_between(
            local,
            "def Fires",
            "\n\n/-- The proposed repair view separates",
            "Fires",
        ),
        "ClearsOn": quote_between(
            local,
            "def ClearsOn",
            "\n\n/-- The proposed repair view clears",
            "ClearsOn",
        ),
        "Clears": quote_between(
            local,
            "def Clears {",
            "\n\n/-- The repair view separates every distinct",
            "Clears",
        ),
        "IdentityGrade": quote_between(
            local,
            "def IdentityGrade",
            "\n\n/-- Identity-grade observation supplied",
            "IdentityGrade",
        ),
        "class_exclusion": quote_theorem_statement(g1, "g1_class_exclusion"),
    }


def build_receipt(root: Path) -> dict[str, Json]:
    requirements = require_sha256(
        root / "requirements.txt", REQUIREMENTS_SHA256, "Python lock"
    )
    prompt_hashes = {
        name: sha256_bytes((root / "prompt" / name).read_bytes())
        for name in ("prompt.md", "seed_prompt.md")
    }
    axiom_reports = parse_axiom_reports(
        (root / "artifacts/lean_axioms.txt").read_text(encoding="utf-8")
    )
    local = artifact_payload(DEFAULT_MAX_CHAIN)
    g4 = g4_report()
    strategies = local["strategies"]
    assert isinstance(strategies, list)
    g4_terminals = g4["terminals"]
    assert isinstance(g4_terminals, list)
    expected_g4 = [
        "G4_HOLDS_UNDER_MU2",
        "G4_FAILS_AT_<3,mu1,reading_F_outside_target_argument>",
    ]
    if g4_terminals != expected_g4:
        raise ValueError(f"unexpected G4 terminals: {g4_terminals}")
    if len(strategies) != len(STRATEGIES):
        raise ValueError("strategy membership table is incomplete")

    local_raw = dumps_deterministic(local)
    g4_raw = dumps_deterministic(g4)
    return {
        "schema": "g1-class-receipt-v1",
        "pins": {
            "g1_class_base_commit": BASE_COMMIT,
            "operator_task_sha256": TASK_SHA256,
            "toolchains": {
                "lean": LEAN_VERSION,
                "lake": LAKE_VERSION,
                "python": PYTHON_VERSION,
            },
            "python_lock": {
                "path": "requirements.txt",
                "sha256": REQUIREMENTS_SHA256,
                "lines": requirements.decode("utf-8").splitlines(),
            },
            "sealed_prompt_sha256": prompt_hashes,
        },
        "exact_source_quotes": _source_quotes(root),
        "new_theorem_axiom_reports": axiom_reports,
        "finite_bounds": {
            "strategy_checks_max_chain": DEFAULT_MAX_CHAIN,
            "strategy_count": len(STRATEGIES),
            "capacity_threshold_formula": "k ^ (2 * d + 1) + 2 * d + 2",
            "capacity_examples": local["capacity_witnesses"],
            "depth_two_nonvacuity_chain": 4,
            "g4_first_n": FIRST_N,
            "g4_last_n": LAST_N,
            "g4_max_items": BOUNDS.max_items,
            "g4_max_arity": BOUNDS.max_arity,
            "g4_obstructions_checked": g4["total_obstructions_checked"],
            "g4_measures": ["mu1", "mu2"],
            "g4_readings": ["L", "F"],
        },
        "supporting_artifacts": {
            "local_strategy.json": {
                "sha256": sha256_bytes(local_raw),
                "payload": local,
            },
            "g4_engine_import_branch.json": {
                "sha256": sha256_bytes(g4_raw),
                "payload": g4,
            },
        },
        "strategy_membership_verdicts": strategies,
        "statuses": {
            "t5": "T5_PROFILE_CORRESPONDENCE_PROVED",
            "g1": "G1_CLASS_EXCLUSION_PROVED",
            "g3": "G3_REMAINS_CONJECTURE",
            "g4": g4_terminals,
            "ob1": "OB1_UNCHANGED",
            "object_language": "OBJECT_LANGUAGE_GENERATOR_NOT_IN_SCOPE",
        },
        "open_sentences": list(OPEN_SENTENCES),
        "withdrawn_sentences": list(WITHDRAWN_SENTENCES),
        "hygiene": {
            "H1": "HYGIENE_H1_SKIPPED",
            "H2": "HYGIENE_H2_SKIPPED",
            "H3": "HYGIENE_H3_SKIPPED",
            "H4": "HYGIENE_H4_DONE",
            "H5": "HYGIENE_H5_DONE",
            "H6": "HYGIENE_H6_SKIPPED",
        },
        "terminals": list(TERMINALS),
        "nonclaims": [
            "No theorem ranges over strategies outside the quoted class.",
            "No object-language generator or self-origination from <> is claimed.",
            "No functoriality, initiality, canonical strategy, or unrestricted G1 is claimed.",
            "The finite G4 result is not an identification of the historical engine with a generator.",
        ],
    }

