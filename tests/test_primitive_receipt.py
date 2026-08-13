"""Tests for the PR #12 completion receipt."""

from __future__ import annotations

import json
from pathlib import Path

import run_primitive_receipt
from run_primitive_receipt import receipt

REPO = Path(__file__).resolve().parent.parent


def test_receipt_binds_everything() -> None:
    r = receipt()
    assert r["blind_native_base"] == "ccd3a53"
    contact = r["contact"]
    assert isinstance(contact, dict)
    assert contact["status"] == "CONTACT_INPUT_ABSENT"
    assert contact["package_present"] is False
    prompts = r["prompt_sha256"]
    assert isinstance(prompts, dict)
    assert len(prompts) == 3
    assert all(len(str(v)) == 64 for v in prompts.values())
    ax = r["axiom_report"]
    assert isinstance(ax, dict)
    assert isinstance(ax["theorem_count"], int)
    assert ax["theorem_count"] >= 600
    terminals = r["terminals"]
    assert isinstance(terminals, list)
    codes = {t["code"] for t in terminals if isinstance(t, dict)}
    assert "CONTACT_INPUT_ABSENT" in codes
    assert "PRIMITIVE_DIFFERENCE_PASSAGE_COMPOSED" in codes
    assert "INTERPRETER_BOUNDARY_IS_PRIMITIVE_DIFFERENCE" in codes
    assert "HIGHER_STRUCTURE_OPTIONAL_NOT_FORCED" in codes
    for t in terminals:
        assert isinstance(t, dict) and t["evidence"]
    attacks = r["adversarial_record"]
    assert isinstance(attacks, list)
    assert len(attacks) == 20
    assert all(isinstance(a, dict) and a["disposition"]
               for a in attacks)
    opens = r["open_obligations"]
    assert isinstance(opens, list) and len(opens) == 5


def test_prompt_hashes_match_files() -> None:
    import hashlib

    r = receipt()
    prompts = r["prompt_sha256"]
    assert isinstance(prompts, dict)
    for rel, digest in prompts.items():
        assert isinstance(rel, str)
        actual = hashlib.sha256(
            (REPO / rel).read_bytes()).hexdigest()
        assert actual == digest


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    assert run_primitive_receipt.main(["--artifacts", str(d1)]) == 0
    assert run_primitive_receipt.main(["--artifacts", str(d2)]) == 0
    b1 = (d1 / "primitive_completion_receipt.json").read_bytes()
    assert b1 == (d2 / "primitive_completion_receipt.json"
                  ).read_bytes()
    payload = json.loads(b1)
    assert payload["graph_scope"].startswith("dependency records")
