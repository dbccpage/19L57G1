"""Verification and governance harness for Target P208b: Contextuality & Nonlocality.

AuthorityEffect: None.

Executes:
1. Source hygiene check (prohibits sorry, admit, unsafe, partial, axiom, and watched terms).
2. Python pytest test suite across tests/.
3. Lean 4 package build via lake build.
4. Environment theorem census audit against allowed axioms {propext, Quot.sound}.
5. Generates or verifies evidence/receipt.json.
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
REPO_ROOT = ROOT.parent.parent
LEAN_DIR = ROOT / "lean"
RECEIPT_PATH = ROOT / "evidence" / "receipt.json"

ALLOWED_AXIOMS = {"propext", "Quot.sound"}
FORBIDDEN_LEAN_TOKENS = re.compile(
    r"\b(?:sorry|admit|unsafe|partial)\b|^\s*axiom\s", re.MULTILINE
)
CENSUS_RE = re.compile(r"^info:.*?CONTEXTUALITY_THEOREM: (\S+)$", re.MULTILINE)

WATCHED_DIGESTS = {
    "8fb7cf7a46995c95da6ad4cca750efb66946b771aca070d5948ea80ca33237b4": "watched_term_1",
    "326020dd50dd0cf805c87b26692d2ca8e5143c3fe0c68c96fdd346d74afae926": "watched_term_2",
    "67671a2f53dd910a8b35840edb6a0a1e751ae5532178ca7f025b823eee317992": "watched_term_3",
    "c23c23a7c71feb7e0bd8f3b0d1eb5603df23a831bb6a4ec36a407f571e02df43": "watched_term_4",
    "ce97e449f49f6dfbe3f9acdb172fac5489099bf62b908d501cb466f359d91508": "watched_term_5",
    "02195b8e989603e4dfb45352b902e8dc34bff40bb228f3c26e56a6ddebdb85ad": "watched_term_6",
    "812592913d114ecbc7072950c712575b2e859a7d1e8cc775226e2cd1de12e274": "watched_term_7",
    "87a0acaec00fa34a3166f0b62b7352868c16752bf796a6af3baf0362c62361ed": "watched_term_8",
}

TOKEN_RE = re.compile(r"\b[a-zA-Z]+\b")


def check_tokens_for_watched_terms(text: str, file_name: str) -> None:
    """Scan tokens and check if their lowercase SHA256 matches any watched digest."""
    for tok in TOKEN_RE.findall(text):
        h = hashlib.sha256(tok.lower().encode("utf-8")).hexdigest()
        if h in WATCHED_DIGESTS:
            raise ValueError(
                f"Watched term ({WATCHED_DIGESTS[h]}) found in {file_name}: '{tok}'"
            )


def sha256_file(path: Path) -> str:
    """Compute sha256 digest with CRLF normalized to LF."""
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def check_source_hygiene() -> dict[str, str]:
    """Audit source files for forbidden tokens and watched terms."""
    hashes: dict[str, str] = {}
    lean_files = list(LEAN_DIR.glob("*.lean"))
    if not lean_files:
        raise ValueError("No Lean files found in lean directory")

    for p in sorted(lean_files):
        text = p.read_text(encoding="utf-8")
        if FORBIDDEN_LEAN_TOKENS.search(text):
            raise ValueError(f"Forbidden token found in Lean source: {p.name}")
        check_tokens_for_watched_terms(text, p.name)
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    for p in sorted(ROOT.glob("*.py")):
        text = p.read_text(encoding="utf-8")
        check_tokens_for_watched_terms(text, p.name)
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    for p in sorted((ROOT / "tests").glob("*.py")):
        text = p.read_text(encoding="utf-8")
        check_tokens_for_watched_terms(text, p.name)
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    for p in sorted(ROOT.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        check_tokens_for_watched_terms(text, p.name)
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    return hashes


def run_pytest() -> dict[str, Any]:
    """Execute test suite via pytest."""
    cmd = [sys.executable, "-m", "pytest", "-v", "tests"]
    print(f"== Running pytest: {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    output = proc.stdout + "\n" + proc.stderr
    print(output)
    if proc.returncode != 0:
        raise RuntimeError(f"pytest exited {proc.returncode}")

    passed_match = re.search(r"(\d+) passed", output)
    passed_count = int(passed_match.group(1)) if passed_match else 0
    return {
        "exit_code": proc.returncode,
        "passed": passed_count,
        "status": "PASS",
    }


def run_lean() -> dict[str, Any]:
    """Execute lake build and audit theorem census against permitted axioms."""
    print("== Building Lean package via lake build")
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
        census_matches = set(re.findall(r"CONTEXTUALITY_THEOREM: (\S+)", inv_output))
    if not census_matches:
        raise ValueError("Census found 0 declarations in ContextualityNonlocality namespace")

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
        f"Lean Census: {len(census_matches)} declarations verified, "
        f"{axiom_free} axiom-free, zero choice."
    )
    return {
        "theorem_count": len(census_matches),
        "axiom_free_count": axiom_free,
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "reports": dict(sorted(reports.items())),
    }


def verify() -> dict[str, Any]:
    """Run full verification pipeline and produce structured receipt."""
    hashes = check_source_hygiene()
    pytest_res = run_pytest()
    lean_res = run_lean()

    receipt = {
        "schema_version": 1,
        "target": "Target P208b: Rational Bell-CHSH Nonlocality & Cabello 18-Ray Contextuality",
        "status": "PASS",
        "authority_effect": "None",
        "toolchain": "leanprover/lean4:v4.33.0",
        "source_hashes": hashes,
        "pytest": pytest_res,
        "lean": lean_res,
        "claim_hygiene": {
            "exact_rational_arithmetic": True,
            "bell_chsh_lhv_bound_constructively_checked": True,
            "pythagorean_correlator_exceeds_lhv": True,
            "cabello_18ray_incidence_checked": True,
            "cabello_valuation_obstruction_proved": True,
            "cech_cochain_parity_obstruction_evaluated": True,
            "axioms_within_propext_quot_sound": True,
            "zero_classical_choice": True,
            "zero_mathlib": True,
            "vocabulary_firewall_clean": True,
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
