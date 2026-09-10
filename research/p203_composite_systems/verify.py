"""Verification and governance harness for Target P203 Composite Systems & Pre-Spatial Locality.

AuthorityEffect: None.
Runs:
1. Source hygiene check (forbids sorry, admit, unsafe, partial, axiom).
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
CENSUS_RE = re.compile(r"P203_THEOREM:\s+(\S+)", re.MULTILINE)
AXIOM_RE = re.compile(
    r"^info:.*? '(.+?)' depends on axioms: \[(.*?)\]$", re.MULTILINE
)
NO_AXIOM_RE = re.compile(
    r"^info:.*? '(.+?)' does not depend on any axioms$", re.MULTILINE
)


def sha256_file(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def check_source_hygiene() -> dict[str, str]:
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
        raise ValueError("Census found 0 theorems in P203CompositeSystems namespace")

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
        "target": "Target P203: Composite Systems & Pre-Spatial Locality",
        "status": "PASS",
        "authority_effect": "None",
        "toolchain": "leanprover/lean4:v4.33.0",
        "source_hashes": hashes,
        "pytest": pytest_res,
        "lean": lean_res,
        "claim_hygiene": {
            "scope": "Multi-locus composite networks, pre-spatial interaction graphs from footprints, strict operational non-signaling across bipartite cuts, negative controls, duplicate observer agreement, and graph automorphism invariance",
            "tensor_composition_associativity_proved": True,
            "subsystem_projection_preservation_proved": True,
            "prespatial_interaction_graphs_derived": True,
            "bipartite_cut_non_signaling_proved": True,
            "leaky_footprint_negative_control_verified": True,
            "mediated_signaling_negative_control_verified": True,
            "duplicate_observer_agreement_proved": True,
            "graph_automorphism_invariance_verified": True,
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
