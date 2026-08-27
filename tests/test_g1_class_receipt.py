"""Tests for the deterministic G1 class receipt."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from derivation.g1_class_receipt import (
    NEW_THEOREMS,
    REQUIREMENTS_SHA256,
    TASK_SHA256,
    build_receipt,
    parse_axiom_reports,
    quote_between,
    quote_theorem_statement,
    require_sha256,
)

import run_g1_class_receipt


ROOT = Path(__file__).resolve().parent.parent


def test_receipt_binds_exact_class_theorem_reports_and_boundaries() -> None:
    payload = build_receipt(ROOT)
    assert payload["pins"]["operator_task_sha256"] == TASK_SHA256  # type: ignore[index]
    reports = payload["new_theorem_axiom_reports"]
    assert isinstance(reports, list)
    assert [row["theorem"] for row in reports] == list(NEW_THEOREMS)
    assert all(set(row["axioms"]) <= {"propext", "Quot.sound"} for row in reports)
    quotes = payload["exact_source_quotes"]
    assert isinstance(quotes, dict)
    assert "locality : ∀ n, ViewLocal" in quotes["LocalStrategy"]
    assert "¬ (Fires S ∧ Clears S ∧ ¬ RecurringImport S)" in quotes[
        "class_exclusion"
    ]
    terminals = payload["terminals"]
    assert isinstance(terminals, list)
    assert "G1_CLASS_EXCLUSION_PROVED" in terminals
    assert "OB1_UNCHANGED" in terminals
    assert payload["statuses"]["g3"] == "G3_REMAINS_CONJECTURE"  # type: ignore[index]
    assert payload["statuses"]["g4"] == "G4_REMAINS_CONJECTURE"  # type: ignore[index]
    assert "G4_HOLDS_UNDER_MU2" not in terminals
    assert "g4_engine_import_branch.json" not in payload["supporting_artifacts"]
    assert not any(
        str(key).startswith("g4_") for key in payload["finite_bounds"]  # type: ignore[union-attr]
    )


def test_python_lock_is_repository_canonical_lf() -> None:
    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8").splitlines()
    assert "requirements.txt -text" in attributes
    raw = require_sha256(
        ROOT / "requirements.txt", REQUIREMENTS_SHA256, "Python lock"
    )
    assert b"\r\n" not in raw
    assert raw.endswith(b"\n")


def test_python_lock_rejects_line_ending_conversion(tmp_path: Path) -> None:
    canonical = (ROOT / "requirements.txt").read_bytes()
    assert b"\r\n" not in canonical
    converted = tmp_path / "requirements.txt"
    converted.write_bytes(canonical.replace(b"\n", b"\r\n"))
    with pytest.raises(ValueError, match="Python lock SHA-256 mismatch"):
        require_sha256(converted, REQUIREMENTS_SHA256, "Python lock")


def test_hash_guard_fails_by_label(tmp_path: Path) -> None:
    lock = tmp_path / "requirements.txt"
    lock.write_text("changed\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Python lock SHA-256 mismatch"):
        require_sha256(lock, REQUIREMENTS_SHA256, "Python lock")


def test_axiom_parser_fails_by_missing_and_disallowed_theorem() -> None:
    name = NEW_THEOREMS[0]
    with pytest.raises(ValueError, match=f"missing axiom report: {name}"):
        parse_axiom_reports("", (name,))
    bad = f"'{'Example.bad'}' depends on axioms: [Classical.choice]"
    with pytest.raises(ValueError, match="disallowed axioms for Example.bad"):
        parse_axiom_reports(bad, ("Example.bad",))
    duplicate = f"'{name}' does not depend on any axioms\n'{name}' does not depend on any axioms"
    with pytest.raises(ValueError, match=f"duplicate axiom report: {name}"):
        parse_axiom_reports(duplicate, (name,))


def test_quote_guards_fail_by_declaration_name() -> None:
    with pytest.raises(ValueError, match="missing LocalStrategy start marker"):
        quote_between("", "structure LocalStrategy", "end", "LocalStrategy")
    with pytest.raises(ValueError, match="missing LocalStrategy end marker"):
        quote_between("structure LocalStrategy", "structure LocalStrategy", "end", "LocalStrategy")
    with pytest.raises(ValueError, match="missing theorem statement: target"):
        quote_theorem_statement("", "target")
    with pytest.raises(ValueError, match="missing theorem proof delimiter: target"):
        quote_theorem_statement("theorem target : True", "target")


def test_runner_is_byte_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    assert run_g1_class_receipt.main(["--artifacts", str(first)]) == 0
    assert run_g1_class_receipt.main(["--artifacts", str(second)]) == 0
    left = first / "g1_class_receipt.json"
    right = second / "g1_class_receipt.json"
    assert left.read_bytes() == right.read_bytes()
    payload = json.loads(left.read_text(encoding="utf-8"))
    assert payload["schema"] == "g1-class-receipt-v2"
    assert payload["pins"]["python_lock"]["sha256"] == REQUIREMENTS_SHA256

