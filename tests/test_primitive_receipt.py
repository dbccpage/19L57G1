"""Tests for the PR #12 completion receipt, including the canonical
byte definition, the Git-blob/checkout distinction, and content
mutation sensitivity."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import pytest

import run_primitive_receipt
from run_primitive_receipt import canonical_sha256, receipt

REPO = Path(__file__).resolve().parent.parent

PROMPT_MD_CANONICAL = (
    "a613a1965e4f02fee0"
    "0df4d42041fceeca176abcfaa9202c3e769021305940b5")
SEED_CANONICAL = (
    "4ea4682e1da25363f9c7"
    "c1e9234b4b248f980097ae92d6f7dc1e8e8dd9bd4388")
SEED_ORIGINAL_SUPPLIED = (
    "ee3ba0583fea2a11f129"
    "4538c912c542b3faee5316355dc226efb92ef64646ab")


def test_receipt_binds_everything() -> None:
    r = receipt()
    assert r["blind_native_base"] == "ccd3a53"
    contact = r["contact"]
    assert isinstance(contact, dict)
    assert contact["status"] == "CONTACT_INPUT_ABSENT"
    assert contact["package_present"] is False
    prompts = r["prompt_sha256_canonical"]
    assert isinstance(prompts, dict)
    assert len(prompts) == 4
    assert all(len(str(v)) == 64 for v in prompts.values())
    # canonical values: repository blob bytes, platform-independent
    assert prompts["prompt/prompt.md"] == PROMPT_MD_CANONICAL
    assert prompts["prompt/seed_prompt.md"] == SEED_CANONICAL
    # provenance: the original supplied rendering, recorded alongside
    assert r["seed_prompt_original_supplied_sha256"] == \
        SEED_ORIGINAL_SUPPLIED
    ax = r["axiom_report"]
    assert isinstance(ax, dict)
    assert isinstance(ax["theorem_count"], int)
    assert ax["theorem_count"] >= 600
    terminals = r["terminals"]
    assert isinstance(terminals, list)
    codes = {t["code"] for t in terminals if isinstance(t, dict)}
    assert "CONTACT_INPUT_ABSENT" in codes
    assert "PRIMITIVE_DIFFERENCE_PASSAGE_COMPOSED" in codes
    assert "FINITE_CODE_FAMILY_NOT_EXTENSIONALLY_COMPLETE" in codes
    assert "DECLARED_BOUNDARY_MODEL_SATISFIES_A_AND_F" in codes
    assert "INTERPRETER_BOUNDARY_IS_PRIMITIVE_DIFFERENCE" not in codes
    assert "INTERPRETER_TOWER_PERSISTS" not in codes
    assert "HIGHER_STRUCTURE_OPTIONAL_NOT_FORCED" in codes
    for t in terminals:
        assert isinstance(t, dict) and t["evidence"]
    attacks = r["adversarial_record"]
    assert isinstance(attacks, list)
    assert len(attacks) == 20
    assert all(isinstance(a, dict) and a["disposition"]
               for a in attacks)
    opens = r["open_obligations"]
    assert isinstance(opens, list) and len(opens) == 4
    # audit repair: openTerminalPres2 was closed constructively by
    # no_terminal_pres2 and is no longer an open obligation
    assert not any("openTerminalPres2" in str(o) for o in opens)
    frontiers = r["frontier_conjectures"]
    assert isinstance(frontiers, list)
    boundary = next(
        row for row in frontiers
        if row["conjecture"] == "GENERAL_BOUNDARY_COMPOSITE_VANISHING")
    boundary_scope = str(boundary["missing_theorem"])
    assert "EVERY target presentation" in boundary_scope
    assert "unordered pair of deleted positions" in boundary_scope
    assert "every coefficient system" in boundary_scope
    assert "each codimension-two face" not in boundary_scope


def test_canonical_matches_checkout_on_every_rendering() -> None:
    """Canonical hashes are identical whether the checkout rendered
    LF (clean clone under ``prompt/** -text``) or CRLF (a legacy
    working tree from before the attribute existed)."""
    for rel, want in [("prompt/prompt.md", PROMPT_MD_CANONICAL),
                      ("prompt/seed_prompt.md", SEED_CANONICAL)]:
        assert canonical_sha256(REPO / rel) == want
        raw = hashlib.sha256((REPO / rel).read_bytes()).hexdigest()
        # the raw checkout bytes are one of the two sanctioned
        # renderings of the same canonical content
        if rel.endswith("seed_prompt.md"):
            assert raw in {SEED_CANONICAL, SEED_ORIGINAL_SUPPLIED}
        else:
            assert raw == want


def test_blob_checkout_distinction() -> None:
    """The canonical bytes ARE the Git blob bytes: for every hashed
    prompt file, canonical(checkout) == sha256(blob at HEAD)."""
    if shutil.which("git") is None:
        pytest.skip("git unavailable")
    for rel in ["prompt/prompt.md", "prompt/seed_prompt.md",
                "prompt/prompt_pr12.md",
                "prompt/ultra_prompt_pr12.md"]:
        proc = subprocess.run(
            ["git", "show", f"HEAD:{rel}"],
            capture_output=True, cwd=REPO)
        if proc.returncode != 0:
            pytest.skip(f"{rel} not in HEAD yet")
        blob_hash = hashlib.sha256(proc.stdout).hexdigest()
        assert canonical_sha256(REPO / rel) == blob_hash, rel


def test_mutation_detected(tmp_path: Path) -> None:
    """Canonicalization is content-sensitive: any real content
    mutation moves the hash; a pure line-ending change does not."""
    src = (REPO / "prompt/seed_prompt.md").read_bytes()
    base = tmp_path / "seed.md"
    base.write_bytes(src)
    baseline = canonical_sha256(base)
    assert baseline == SEED_CANONICAL
    # real mutation: flip one content byte
    mutated = tmp_path / "seed_mut.md"
    mutated.write_bytes(src.replace(b"e", b"E", 1))
    assert canonical_sha256(mutated) != baseline
    # appending content is detected
    appended = tmp_path / "seed_app.md"
    appended.write_bytes(src + b"x")
    assert canonical_sha256(appended) != baseline
    # a pure rendering change is NOT a content mutation
    crlf = tmp_path / "seed_crlf.md"
    crlf.write_bytes(
        src.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    assert canonical_sha256(crlf) == baseline


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
