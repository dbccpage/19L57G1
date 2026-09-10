"""Master Verification Script for G018 Self-Hosting.

Executes pytest test suite, builds Lean 4 constructive package,
runs Inventory metaprogrammed theorem census, verifies strict axiom boundary,
and generates/checks evidence/receipt.json.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
LEAN_DIR = ROOT / "lean"
EVIDENCE_DIR = ROOT / "evidence"
RECEIPT_FILE = EVIDENCE_DIR / "receipt.json"

ALLOWED_AXIOMS = {"propext", "Quot.sound"}


def compute_file_hash(path: Path) -> str:
    """Compute sha256 digest of file content normalized for line endings."""
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def run_pytest() -> int:
    """Run pytest suite on tests/."""
    print("== Step 1: Running pytest suite...")
    cmd = [sys.executable, "-m", "pytest", "tests", "-v"]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"pytest failed with exit code {result.returncode}")

    m = re.search(r"(\d+)\s+passed", result.stdout)
    test_count = int(m.group(1)) if m else 0
    print(f"PASS: {test_count} tests passed.")
    return test_count


def build_lean() -> None:
    """Build Lean 4 package with lake build."""
    print("== Step 2: Building Lean 4 constructive package...")
    cmd = ["lake", "build"]
    result = subprocess.run(cmd, cwd=LEAN_DIR, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"lake build failed with exit code {result.returncode}")
    print("PASS: Lean 4 package compiled successfully.")


def audit_theorems_and_axioms() -> tuple[list[str], dict[str, list[str]]]:
    """Extract census theorems from Inventory.lean and check their axioms."""
    print("== Step 3: Running Lean theorem census & axiom audit...")
    cmd_census = ["lake", "env", "lean", "Inventory.lean"]
    result_census = subprocess.run(cmd_census, cwd=LEAN_DIR, capture_output=True, text=True, encoding="utf-8")
    if result_census.returncode != 0:
        print(result_census.stderr, file=sys.stderr)
        raise RuntimeError("failed to run Inventory.lean")

    output_census = result_census.stdout + result_census.stderr
    theorems = sorted(set(re.findall(r"G018_SELF_HOSTING_THEOREM:\s*(\S+)", output_census)))
    if not theorems:
        raise RuntimeError("No theorems found in Inventory census.")

    print(f"Found {len(theorems)} compiled declarations in G018SelfHosting namespace.")

    # Check axioms for each theorem
    axiom_check_script = "import Inventory\n\n" + "\n".join(f"#print axioms {t}" for t in theorems)
    cmd_axioms = ["lake", "env", "lean", "--stdin"]
    result_axioms = subprocess.run(
        cmd_axioms,
        cwd=LEAN_DIR,
        input=axiom_check_script,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result_axioms.returncode != 0:
        print(result_axioms.stderr, file=sys.stderr)
        raise RuntimeError("Axiom query failed in Lean.")

    axiom_output = result_axioms.stdout + result_axioms.stderr
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

    print(f"PASS: All {len(theorems)} declarations satisfy strict axiom boundary {ALLOWED_AXIOMS}.")
    return theorems, theorem_axioms


def collect_source_hashes() -> dict[str, str]:
    """Collect SHA256 hashes of all source code files."""
    patterns = [
        "*.py",
        "tests/*.py",
        "lean/*.lean",
        "lean/lakefile.toml",
        "lean/lean-toolchain",
    ]
    hashes: dict[str, str] = {}
    for pat in patterns:
        for p in ROOT.glob(pat):
            rel = p.relative_to(ROOT).as_posix()
            hashes[rel] = compute_file_hash(p)
    return dict(sorted(hashes.items()))


def generate_receipt(test_count: int, theorems: list[str], axioms_map: dict[str, list[str]]) -> dict:
    """Construct receipt payload."""
    source_hashes = collect_source_hashes()
    axiom_free_count = sum(1 for ax in axioms_map.values() if len(ax) == 0)

    receipt = {
        "schema_version": 1,
        "target": "G018",
        "title": "Self-Hosting, Internal Simulation & Reflection Boundary",
        "terminal_status": "SELF_HOSTING_SIMULATION_ESTABLISHED",
        "authority_effect": "None",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "toolchains": {
            "lean": "leanprover/lean4:v4.33.0",
            "python": sys.version.split()[0],
        },
        "test_results": {
            "test_runner": "pytest",
            "passed": test_count,
            "failed": 0,
            "status": "PASS",
        },
        "lean_audit": {
            "total_theorems": len(theorems),
            "axiom_free_theorems": axiom_free_count,
            "allowed_axioms": sorted(ALLOWED_AXIOMS),
            "disallowed_axioms_detected": [],
            "status": "PASS",
        },
        "theorems": theorems,
        "source_hashes": source_hashes,
    }
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="Master verification for G018")
    parser.add_argument("--check", action="store_true", help="Check existing receipt without regenerating")
    args = parser.parse_args()

    test_count = run_pytest()
    build_lean()
    theorems, axioms_map = audit_theorems_and_axioms()
    receipt = generate_receipt(test_count, theorems, axioms_map)

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    receipt_json = json.dumps(receipt, indent=2, sort_keys=True) + "\n"

    if args.check:
        if not RECEIPT_FILE.is_file():
            print("FAIL: evidence/receipt.json missing in --check mode.", file=sys.stderr)
            return 1
        existing_receipt = RECEIPT_FILE.read_text(encoding="utf-8")
        existing_data = json.loads(existing_receipt)
        if (
            existing_data.get("terminal_status") != receipt["terminal_status"]
            or existing_data.get("test_results", {}).get("passed") != receipt["test_results"]["passed"]
            or existing_data.get("lean_audit", {}).get("total_theorems") != receipt["lean_audit"]["total_theorems"]
        ):
            print("FAIL: existing receipt mismatch.", file=sys.stderr)
            return 1
        print("PASS: --check verified existing receipt.")
    else:
        RECEIPT_FILE.write_text(receipt_json, encoding="utf-8")
        print(f"WROTE: {RECEIPT_FILE}")
        print("VERIFICATION COMPLETE: PASS")

    return 0


if __name__ == "__main__":
    sys.exit(main())
