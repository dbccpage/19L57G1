"""Verification harness for Target G015/G017 Autonomous Stepping & Demand Dynamics.

Runs:
1. Source hygiene check (forbids sorry, admit, unsafe, partial, axiom).
2. Python pytest test suite across tests/
3. Lean 4 constructive package build via lake build
4. Inventory.lean census check against allowed axioms {propext, Quot.sound}
5. Emits evidence/receipt.json
"""

from __future__ import annotations

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
AXIOM_RE = re.compile(
    r"^(?:info:\s*)?'(.+?)' depends on axioms: \[(.*?)\]$", re.MULTILINE
)
NO_AXIOM_RE = re.compile(
    r"^(?:info:\s*)?'(.+?)' does not depend on any axioms$", re.MULTILINE
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
    build_proc = subprocess.run(
        ["lake", "build"], cwd=LEAN_DIR, capture_output=True, text=True, check=False
    )
    build_output = build_proc.stdout + "\n" + build_proc.stderr
    print(build_output)
    if build_proc.returncode != 0:
        raise RuntimeError(f"lake build failed ({build_proc.returncode}):\n{build_output}")

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
        raise RuntimeError(f"Inventory execution failed:\n{inv_output}")

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

    return {
        "build_status": "PASS",
        "theorems_audited": len(theorems),
        "theorem_details": theorems,
    }


def main() -> None:
    print("=== Starting Target G015/G017 Verification ===")
    file_hashes = check_source_hygiene()
    pytest_res = run_pytest()
    lean_res = run_lean()

    receipt = {
        "target": "G015/G017 First-Demand, Invocation Bridge & Autonomous Stepping",
        "source_hashes": file_hashes,
        "pytest": pytest_res,
        "lean": lean_res,
        "verification_status": "VERIFIED_SOUND",
    }

    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"Receipt generated at {RECEIPT_PATH}")
    print("=== G015/G017 Verification Complete: PASS ===")


if __name__ == "__main__":
    main()
