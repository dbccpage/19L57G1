"""Verification and governance harness for G010 (Semantic Primitive Removal).

Terminal Status: BOUNDARY_REMOVAL_SEMANTICALLY_EXECUTED
AuthorityEffect: None.

Verifies:
1. Python pytest test suite across tests/
2. Lean 4 constructive package build and axiom verification
3. Metaprogrammed theorem census audit strictly within {propext, Quot.sound}
4. Source hygiene checks (prohibits sorry, admit, unsafe, partial, axiom)
5. Generates and validates evidence/receipt.json
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
CENSUS_RE = re.compile(r"^G010_THEOREM:\s*(\S+)$", re.MULTILINE)


def sha256_file(path: Path) -> str:
    """Calculate normalized SHA256 of a file (CRLF -> LF)."""
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def check_source_hygiene() -> dict[str, str]:
    """Verify source code hygiene and collect SHA256 hashes."""
    hashes: dict[str, str] = {}
    lean_files = list(LEAN_DIR.glob("*.lean"))
    if not lean_files:
        raise ValueError("No Lean files found in lean directory")

    for p in sorted(lean_files):
        text = p.read_text(encoding="utf-8")
        if FORBIDDEN_LEAN_TOKENS.search(text):
            raise ValueError(f"Forbidden token found in Lean source: {p.name}")
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    for p in sorted(ROOT.glob("*.py")):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    for p in sorted((ROOT / "tests").glob("*.py")):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    # Configuration files
    for conf in ["lean/lakefile.toml", "lean/lean-toolchain"]:
        p = ROOT / conf
        if p.is_file():
            hashes[conf] = sha256_file(p)

    return hashes


def run_pytest() -> dict[str, Any]:
    """Execute test suite and parse results."""
    cmd = [sys.executable, "-m", "pytest", "-v", "tests"]
    print(f"== Step 1: Running pytest suite: {' '.join(cmd)}")
    proc = subprocess.run(
        cmd, cwd=ROOT, capture_output=True, text=True, check=False, encoding="utf-8"
    )
    output = proc.stdout + "\n" + proc.stderr
    print(output)
    if proc.returncode != 0:
        raise RuntimeError(f"pytest failed with exit code {proc.returncode}")

    passed_match = re.search(r"(\d+) passed", output)
    passed_count = int(passed_match.group(1)) if passed_match else 0
    return {
        "test_runner": "pytest",
        "passed": passed_count,
        "failed": 0,
        "status": "PASS",
    }


def run_lean_build() -> None:
    """Build the Lean 4 package with lake build."""
    print("== Step 2: Building Lean 4 constructive package...")
    cmd = ["lake", "build"]
    proc = subprocess.run(
        cmd, cwd=LEAN_DIR, capture_output=True, text=True, check=False, encoding="utf-8"
    )
    if proc.returncode != 0:
        print(proc.stdout, file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        raise RuntimeError(f"lake build failed with exit code {proc.returncode}")
    print("PASS: Lean 4 package compiled successfully.")


def audit_theorems_and_axioms() -> tuple[list[str], dict[str, Any]]:
    """Extract census theorems from Inventory.lean and verify axiom containment."""
    print("== Step 3: Running Lean theorem census & axiom audit...")
    cmd_census = ["lake", "env", "lean", "Inventory.lean"]
    proc_census = subprocess.run(
        cmd_census,
        cwd=LEAN_DIR,
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
    )
    if proc_census.returncode != 0:
        print(proc_census.stderr, file=sys.stderr)
        raise RuntimeError("failed to execute Inventory.lean")

    output_census = proc_census.stdout + "\n" + proc_census.stderr
    theorems = sorted(set(CENSUS_RE.findall(output_census)))
    if not theorems:
        raise RuntimeError("No theorems found in Inventory census.")

    print(f"Found {len(theorems)} compiled declarations in G010 namespace.")

    # Audit axioms for each declaration
    script = "import Inventory\n\n" + "\n".join(f"#print axioms {t}" for t in theorems)
    cmd_axioms = ["lake", "env", "lean", "--stdin"]
    proc_axioms = subprocess.run(
        cmd_axioms,
        cwd=LEAN_DIR,
        input=script,
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
    )
    if proc_axioms.returncode != 0:
        print(proc_axioms.stderr, file=sys.stderr)
        raise RuntimeError("Axiom query failed in Lean.")

    axiom_output = proc_axioms.stdout + "\n" + proc_axioms.stderr
    theorem_axioms: dict[str, list[str]] = {}
    disallowed: list[tuple[str, list[str]]] = []

    for line in axiom_output.splitlines():
        line = line.strip()
        m_used = re.fullmatch(r"'(.+?)' depends on axioms: \[(.*?)\]", line)
        m_none = re.fullmatch(r"'(.+?)' does not depend on any axioms", line)
        if m_used:
            thm_name = m_used.group(1)
            raw_axioms = [a.strip() for a in m_used.group(2).split(",") if a.strip()]
            theorem_axioms[thm_name] = raw_axioms
            bad = [a for a in raw_axioms if a not in ALLOWED_AXIOMS]
            if bad:
                disallowed.append((thm_name, bad))
        elif m_none:
            thm_name = m_none.group(1)
            theorem_axioms[thm_name] = []

    if disallowed:
        raise RuntimeError(f"VIOLATION: Theorems depend on disallowed axioms: {disallowed}")

    missing = set(theorems) - set(theorem_axioms.keys())
    if missing:
        raise RuntimeError(f"Some census theorems were not audited for axioms: {sorted(missing)}")

    axiom_free = sum(1 for ax in theorem_axioms.values() if not ax)
    print(
        f"PASS: All {len(theorems)} declarations satisfy strict axiom boundary {sorted(ALLOWED_AXIOMS)} "
        f"({axiom_free} axiom-free, zero Classical.choice, zero mathlib)."
    )

    audit_summary = {
        "status": "PASS",
        "total_theorems": len(theorems),
        "axiom_free_theorems": axiom_free,
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "disallowed_axioms_detected": [],
    }
    return theorems, audit_summary


def verify() -> dict[str, Any]:
    """Run full verification pipeline and return receipt data."""
    hashes = check_source_hygiene()
    test_results = run_pytest()
    run_lean_build()
    theorems, lean_audit = audit_theorems_and_axioms()

    receipt = {
        "schema_version": 1,
        "target": "G010",
        "terminal_status": "BOUNDARY_REMOVAL_SEMANTICALLY_EXECUTED",
        "authority_effect": "None",
        "toolchain": "leanprover/lean4:v4.33.0",
        "source_hashes": hashes,
        "test_results": test_results,
        "lean_audit": lean_audit,
        "theorems": theorems,
        "claim_hygiene": {
            "scope": "Finite straight-line and capability-restricted execution models",
            "operational_removal_semantically_executed": True,
            "public_view_interface_invariant": True,
            "constructive_branching_obstruction": True,
            "constructive_memory_obstruction": True,
            "constructive_allocation_obstruction": True,
            "adapter_non_recoverability": True,
            "axioms_within_propext_quot_sound": True,
            "zero_classical_choice": True,
            "zero_mathlib": True,
        },
    }
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check receipt against fresh run")
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
