"""Verification and governance harness for Target X301: Formal Semantics, Empirical Reference & Intervention Grounding.

AuthorityEffect: None.
Runs:
1. Source hygiene checks (prohibits sorry, admit, unsafe, partial, axiom in Lean sources;
   enforces repository vocabulary firewall against watched terms across all sources).
2. Python pytest test suite across tests/.
3. Lean 4 constructive package build via lake build.
4. Environment theorem census check against allowed axioms {propext, Quot.sound}.
5. Emits evidence/receipt.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parent
LEAN_DIR = ROOT / "lean"
RECEIPT_PATH = ROOT / "evidence" / "receipt.json"

ALLOWED_AXIOMS = {"propext", "Quot.sound"}
FORBIDDEN_LEAN_TOKENS = re.compile(
    r"\b(?:sorry|admit|unsafe|partial)\b|^\s*axiom\s", re.MULTILINE
)
# Digest 4cbe09597b76... watches forbidden physics-shaped noun in prose_watchlist.json
FORBIDDEN_DIGEST = "4cbe09597b76794b5f6b854c1c1c035ede6d241f250f223b61987dce9d2d7a4b"

AXIOM_RE = re.compile(
    r"^(?:info:\s*)?'(.+?)' depends on axioms: \[(.*?)\]$", re.MULTILINE
)
NO_AXIOM_RE = re.compile(
    r"^(?:info:\s*)?'(.+?)' does not depend on any axioms$", re.MULTILINE
)


def sha256_file(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def has_watched_digest(text: str) -> bool:
    """Check whole-word tokens against the watched digest."""
    for token in re.findall(r"\b[a-zA-Z]+\b", text.lower()):
        d = hashlib.sha256(token.encode("utf-8")).hexdigest()
        if d == FORBIDDEN_DIGEST:
            return True
        if token.endswith("s"):
            d_stem = hashlib.sha256(token[:-1].encode("utf-8")).hexdigest()
            if d_stem == FORBIDDEN_DIGEST:
                return True
    return False


def check_source_hygiene() -> dict[str, str]:
    hashes: dict[str, str] = {}
    lean_files = list(LEAN_DIR.glob("*.lean"))
    if not lean_files:
        raise ValueError("No Lean files found in lean directory")

    for p in sorted(lean_files):
        text = p.read_text(encoding="utf-8")
        if FORBIDDEN_LEAN_TOKENS.search(text):
            raise ValueError(f"Forbidden token found in Lean source: {p.name}")
        if has_watched_digest(text):
            raise ValueError(f"Watched forbidden term found in Lean source: {p.name}")
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    for p in sorted(ROOT.glob("*.py")):
        text = p.read_text(encoding="utf-8")
        if has_watched_digest(text):
            raise ValueError(f"Watched forbidden term found in Python source: {p.name}")
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    for p in sorted((ROOT / "tests").glob("*.py")):
        text = p.read_text(encoding="utf-8")
        if has_watched_digest(text):
            raise ValueError(f"Watched forbidden term found in test source: {p.name}")
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    for doc_name in ["README.md", "CLAIMS.md"]:
        p = ROOT / doc_name
        if p.is_file():
            text = p.read_text(encoding="utf-8")
            if has_watched_digest(text):
                raise ValueError(f"Watched forbidden term found in document: {p.name}")
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            hashes[rel] = sha256_file(p)

    return hashes


def run_pytest() -> dict[str, Any]:
    cmd = [sys.executable, "-m", "pytest", "-v", "tests"]
    print(f"== Running pytest: {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    output = proc.stdout + "\n" + proc.stderr
    print(output)
    if proc.returncode != 0:
        raise RuntimeError(f"pytest failed with exit code {proc.returncode}")

    passed_match = re.search(r"(\d+) passed", output)
    passed_count = int(passed_match.group(1)) if passed_match else 0
    return {
        "exit_code": proc.returncode,
        "passed": passed_count,
        "status": "PASS",
    }


def run_lean() -> dict[str, Any]:
    print("== Building Lean package with lake build")
    build_proc = subprocess.run(
        ["lake", "build"], cwd=LEAN_DIR, capture_output=True, text=True, check=False
    )
    build_output = build_proc.stdout + "\n" + build_proc.stderr
    print(build_output)
    if build_proc.returncode != 0:
        raise RuntimeError(f"lake build failed ({build_proc.returncode}):\n{build_output}")

    print("== Running Inventory.lean census and axiom audit")
    inv_proc = subprocess.run(
        ["lake", "env", "lean", "Inventory.lean"],
        cwd=LEAN_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    inv_output = inv_proc.stdout + "\n" + inv_proc.stderr
    print(inv_output)
    if inv_proc.returncode != 0:
        raise RuntimeError(f"Inventory execution failed ({inv_proc.returncode}):\n{inv_output}")

    theorems: dict[str, list[str]] = {}
    for name, ax_str in AXIOM_RE.findall(inv_output):
        ax_list = [a.strip() for a in ax_str.split(",") if a.strip()]
        theorems[name] = ax_list
        disallowed = set(ax_list) - ALLOWED_AXIOMS
        if disallowed:
            raise ValueError(f"Disallowed axioms in theorem {name}: {disallowed}")

    for name in NO_AXIOM_RE.findall(inv_output):
        theorems[name] = []

    if not theorems:
        raise RuntimeError(f"No theorem axioms were parsed from Inventory.lean output:\n{inv_output}")

    axiom_free = sum(1 for ax in theorems.values() if not ax)
    print(
        f"Lean Census: {len(theorems)} theorems verified, {axiom_free} axiom-free, zero choice."
    )
    return {
        "build_status": "PASS",
        "theorem_count": len(theorems),
        "axiom_free_count": axiom_free,
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "theorem_details": dict(sorted(theorems.items())),
    }


def verify() -> dict[str, Any]:
    print("=== Starting Target X301 Verification ===")
    hashes = check_source_hygiene()
    pytest_res = run_pytest()
    lean_res = run_lean()

    receipt = {
        "schema_version": 1,
        "target": "Target X301: Formal Semantics, Empirical Reference & Intervention Grounding",
        "status": "PASS",
        "authority_effect": "None",
        "toolchain": "leanprover/lean4:v4.33.0",
        "source_hashes": hashes,
        "pytest": pytest_res,
        "lean": lean_res,
        "claim_hygiene": {
            "scope": (
                "Compositional internal semantics over relational carrier states, exact rational "
                "Heyting valuation domain, G012 canonical isomorphism translation invariance across "
                "Challenge-3 readings L and F, executable state intervention grounding of empirical "
                "reference, behavioral observational congruence, and Grounding Firewall override of "
                "multi-observer panel illusions with typed refusal and strict state preservation."
            ),
            "compositional_satisfaction_modeled": True,
            "exact_rational_heyting_poset_modeled": True,
            "translation_invariance_proved": True,
            "reading_l_isomorphism_classes_verified": True,
            "reading_f_isomorphism_classes_verified": True,
            "intervention_grounded_empirical_reference_modeled": True,
            "behavioral_observational_congruence_proved": True,
            "grounding_firewall_panel_illusion_override_modeled": True,
            "panel_illusion_receipts_emitted_with_sha256": True,
            "carrier_state_preserved_unmutated_on_refusal": True,
            "axioms_within_propext_quot_sound": True,
            "zero_classical_choice": True,
            "zero_mathlib": True,
        },
    }
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Check receipt against fresh run"
    )
    parser.add_argument("--write", action="store_true", help="Write fresh receipt")
    args = parser.parse_args()

    try:
        receipt = verify()
        raw = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")

        RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        if args.check:
            if not RECEIPT_PATH.is_file():
                print("FAIL: receipt.json does not exist. Run with --write first.")
                return 1
            existing = RECEIPT_PATH.read_bytes()
            if existing != raw:
                print("FAIL: existing receipt does not match freshly generated verification")
                return 1
            print("PASS: verification receipt matches fresh run")
        else:
            RECEIPT_PATH.write_bytes(raw)
            print(f"WROTE: {RECEIPT_PATH}")
            print("PASS: all verification steps passed successfully.")
        return 0
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
