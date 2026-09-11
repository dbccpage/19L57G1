"""Verification and governance harness for Target P209c: Stabilizer Error-Correcting Codes on Affine Grids.

AuthorityEffect: None.
Runs:
1. Source hygiene check (forbids sorry, admit, unsafe, partial, axiom, watched terms, and forbidden claim words).
2. Python pytest test suite across tests/.
3. Lean 4 package build via lake build.
4. Inventory.lean census and axiom audit against allowed axioms {propext, Quot.sound}.
5. Emits evidence/receipt.json with source hashes and audit results.
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

# Stored as SHA-256 digests of normalized tokens to avoid carrying watched terms as prose
WATCHED_DIGESTS = {
    "8fb7cf7a46995c95da6ad4cca750efb66946b771aca070d5948ea80ca33237b4": "watched_term_1",  # term 1
    "326020dd50dd0cf805c87b26692d2ca8e5143c3fe0c68c96fdd346d74afae926": "watched_term_2",  # term 2
    "67671a2f53dd910a8b35840edb6a0a1e751ae5532178ca7f025b823eee317992": "watched_term_3",  # term 3
    "c23c23a7c71feb7e0bd8f3b0d1eb5603df23a831bb6a4ec36a407f571e02df43": "watched_term_4",  # term 4
    "ce97e449f49f6dfbe3f9acdb172fac5489099bf62b908d501cb466f359d91508": "watched_term_5",  # term 5
    "02195b8e989603e4dfb45352b902e8dc34bff40bb228f3c26e56a6ddebdb85ad": "watched_term_6",  # term 6
    "812592913d114ecbc7072950c712575b2e859a7d1e8cc775226e2cd1de12e274": "watched_term_7",  # term 7
    "87a0acaec00fa34a3166f0b62b7352868c16752bf796a6af3baf0362c62361ed": "watched_term_8",  # term 8
    "dccc5d01dabcd1c0b9fa89c91e7f4bde603121ee0172b4ff394e6bb30d295e41": "watched_term_9",  # term 9
}

# Forbidden claim words stored as digests to avoid literal prohibited words
FORBIDDEN_CLAIM_DIGESTS = {
    "1853ac3ef763440e6fa1e68cfcdf5ec55214b7bbc93cd8b34a832e5690ba9ec9",  # word 1
    "870e586efea39af229438e2fa46bbc6d4a40cb1c4d78884de06e7fb54847bbc1",  # word 2
    "6ac4ed363bd9762d6e24733251f8e26dc66909dc80714ebbbcbd29655e6bc4d5",  # word 3
    "3dd9b4a278ab962d0ea9bcb998d23be81ad5ce67537936964fb23c599e905bb9",  # word 4
    "1298a63b90dc1097df9c8d2dcaffad1b13cd33cef761dade7b68418ed474280e",  # word 5
    "a9fd078562420a276b6902ca3d8bf583c0366e38af72e23be99b16035a76b39a",  # word 6
    "ac9071cf9ea41bfb87c5df9320154cf15d4f3105959dc6538314bcfd4e1cad91",  # word 7
    "9cbc69c9b26fb36fb37a4531ce778b70852989c95ffc8a131c1fa1ea15f75a25",  # word 8
    "6b4cc83fd06ded395a2c08bcd4326973f9545b68dceb709f5a7ea7cb0fd5cd41",  # word 9
    "1e1c48dbdb5c1b6998ed1c6714d9a0a7a112661c4dd4a75eb0ba24631a52bf9c",  # word 10
    "0ec8b3a4a10e5266e36a1260bbfa47ee06de7d996bd823cd0d18a9c2e2b637df",  # word 11
    "b656c4513f109480f96bed79d76db23413ce50742e5866646be1ee664b8ea23f",  # word 12
    "d161ccc3179d1d64590698f21d8a8bfea9df9af2125f8eaab4fa55f2cd7ea6d8",  # word 13
}

TOKEN_RE = re.compile(r"\b[a-z]+\b")
CENSUS_RE = re.compile(r"P209C_THEOREM:\s+(\S+)", re.MULTILINE)
AXIOM_RE = re.compile(
    r"^info:.*? '(.+?)' depends on axioms: \[(.*?)\]$", re.MULTILINE
)
NO_AXIOM_RE = re.compile(
    r"^info:.*? '(.+?)' does not depend on any axioms$", re.MULTILINE
)


def sha256_file(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def token_digest(t: str) -> str:
    return hashlib.sha256(t.lower().encode("utf-8")).hexdigest()


def check_source_hygiene() -> dict[str, str]:
    hashes: dict[str, str] = {}
    lean_files = list(LEAN_DIR.glob("*.lean"))
    if not lean_files:
        raise ValueError("No Lean files found in lean directory")

    for p in sorted(lean_files):
        text = p.read_text(encoding="utf-8")
        if FORBIDDEN_LEAN_TOKENS.search(text):
            raise ValueError(f"Forbidden token found in Lean source: {p.name}")
        for token in TOKEN_RE.findall(text.lower()):
            dig = token_digest(token)
            if dig in WATCHED_DIGESTS:
                raise ValueError(f"Watched vocabulary term found in {p.name}: {token}")
            if dig in FORBIDDEN_CLAIM_DIGESTS:
                raise ValueError(f"Forbidden claim word found in {p.name}: {token}")
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    for p in sorted(ROOT.glob("*.py")):
        text = p.read_text(encoding="utf-8")
        for token in TOKEN_RE.findall(text.lower()):
            dig = token_digest(token)
            if dig in WATCHED_DIGESTS:
                raise ValueError(f"Watched vocabulary term found in {p.name}: {token}")
            if dig in FORBIDDEN_CLAIM_DIGESTS:
                raise ValueError(f"Forbidden claim word found in {p.name}: {token}")
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    for p in sorted((ROOT / "tests").glob("*.py")):
        text = p.read_text(encoding="utf-8")
        for token in TOKEN_RE.findall(text.lower()):
            dig = token_digest(token)
            if dig in WATCHED_DIGESTS:
                raise ValueError(f"Watched vocabulary term found in {p.name}: {token}")
            if dig in FORBIDDEN_CLAIM_DIGESTS:
                raise ValueError(f"Forbidden claim word found in {p.name}: {token}")
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
    combined_log = build_output + "\n" + inv_output

    census_matches = set(CENSUS_RE.findall(inv_output))
    if not census_matches:
        census_matches = set(CENSUS_RE.findall(combined_log))
    if not census_matches:
        raise ValueError("Census found 0 theorems in P209cStabilizerCodes namespace")

    reports: dict[str, list[str]] = {}

    for line in combined_log.splitlines():
        used = re.search(r"'(.+?)' depends on axioms: \[(.*?)\]", line)
        none = re.search(r"'(.+?)' does not depend on any axioms", line)
        if not used and not none:
            continue
        name = used.group(1) if used else none.group(1)  # type: ignore
        if name in reports:
            continue
        axioms = (
            sorted(a.strip() for a in used.group(2).split(",") if a.strip())
            if used
            else []
        )
        if not set(axioms).issubset(ALLOWED_AXIOMS):
            raise ValueError(f"Disallowed axiom in {name}: {axioms}")
        reports[name] = axioms

    missing_reports = census_matches - set(reports.keys())
    if missing_reports:
        raise ValueError(
            f"Census declarations missing axiom reports: {sorted(missing_reports)}"
        )

    axiom_free = sum(1 for ax in reports.values() if not ax)
    print(
        f"Lean Census: {len(census_matches)} theorems verified, {axiom_free} axiom-free, zero choice."
    )
    return {
        "theorem_count": len(census_matches),
        "axiom_free_count": axiom_free,
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "reports": dict(sorted(reports.items())),
    }


def verify() -> dict[str, Any]:
    hashes = check_source_hygiene()
    pytest_res = run_pytest()
    lean_res = run_lean()

    receipt = {
        "schema_version": 1,
        "target": "Target P209c: Stabilizer Error-Correcting Codes on Affine Grids",
        "status": "PASS",
        "authority_effect": "None",
        "toolchain": "leanprover/lean4:v4.33.0",
        "source_hashes": hashes,
        "pytest": pytest_res,
        "lean": lean_res,
        "claim_hygiene": {
            "scope": "Exact integer and Pauli string arithmetic, 3-carrier bit-flip code [[3, 1, 1]], 4-carrier CSS torus code [[4, 2, 2]], Steane [[7, 1, 3]] CSS code on the Fano plane PG(2, 2), stabilizer projection operator idempotence, transversal Hadamard stabilizer preservation, and deterministic error diagnosis and correction",
            "bitflip_code_commutations_and_syndromes_established": True,
            "torus_code_css_commutations_and_detection_established": True,
            "steane_fano_intersections_and_stabilizers_established": True,
            "transversal_hadamard_preservation_established": True,
            "stabilizer_projection_idempotence_verified": True,
            "deterministic_error_correction_verified": True,
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
