"""Verification script for G001 TOE Target-Class Charter.

Executes:
1. Python unit and property tests (pytest)
2. Lean 4 package build via Lake
3. Metaprogrammed theorem census & strict axiom verification
4. Claim hygiene scan for forbidden tokens
5. Evidence receipt generation in evidence/receipt.json

AuthorityEffect: None.
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
EVIDENCE_DIR = ROOT / "evidence"
RECEIPT_FILE = EVIDENCE_DIR / "receipt.json"

MODULES = ("Charter", "Adequacy", "Morphism")
EXPECTED_LEAN_FILES = {f"{m}.lean" for m in MODULES} | {"Inventory.lean"}
ALLOWED_AXIOMS = {"propext", "Quot.sound"}
CENSUS_LINE_PATTERN = re.compile(r"^.*CHARTER_THEOREM:\s*(\S+)\s*$", re.MULTILINE)

FORBIDDEN_LEAN_TOKENS = re.compile(r"\b(?:sorry|admit|unsafe|partial)\b|^\s*axiom\s", re.MULTILINE)

FORBIDDEN_CLAIM_WORDS = [
    r"\bproves\b",
    r"\bguarantees\b",
    r"\bmathematically verifies\b",
    r"\bfundamentally\b",
    r"\btrue intelligence\b",
    r"\bflawless\b",
    r"\bperfectly\b",
    r"\bweaponized\b",
]


def run_cmd(cmd: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output


def check_source_hygiene() -> list[str]:
    violations: list[str] = []
    for fpath in LEAN_DIR.glob("*.lean"):
        text = fpath.read_text(encoding="utf-8")
        for match in FORBIDDEN_LEAN_TOKENS.finditer(text):
            violations.append(f"Forbidden Lean token '{match.group(0)}' in {fpath.name}")
    return violations


def check_claim_hygiene() -> list[str]:
    violations: list[str] = []
    docs_to_check = [
        ROOT / "README.md",
        ROOT / "CLAIMS.md",
        ROOT / "charter.py",
        ROOT / "adequacy.py",
        ROOT / "morphism.py",
    ]
    for doc in docs_to_check:
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8")
        # Allow mentions inside explicit rule definitions or negative explanations
        lines = text.splitlines()
        for idx, line in enumerate(lines, 1):
            if "Forbidden words" in line or "Replacement defaults" in line or "forbidden" in line.lower():
                continue
            for pat in FORBIDDEN_CLAIM_WORDS:
                if re.search(pat, line, re.IGNORECASE):
                    violations.append(f"Claim Hygiene breach at {doc.name}:{idx}: '{line.strip()}' (matched {pat})")
    return violations


def parse_axiom_reports(log: str, census_names: list[str]) -> dict[str, list[str]]:
    reports: dict[str, list[str]] = {}
    for line in log.splitlines():
        used = re.search(r"'(.+?)' depends on axioms: \[(.*?)\]", line)
        none = re.search(r"'(.+?)' does not depend on any axioms", line)
        if not used and not none:
            continue
        match = used or none
        if match is None:
            continue
        name = match.group(1)
        axioms = [a.strip() for a in used.group(2).split(",") if a.strip()] if used else []
        for ax in axioms:
            if ax not in ALLOWED_AXIOMS:
                raise ValueError(f"Strict axiom boundary violated by '{name}': relies on disallowed '{ax}'")
        reports[name] = sorted(axioms)

    missing = set(census_names) - set(reports)
    if missing:
        raise ValueError(f"Census contains declarations missing axiom reports: {sorted(missing)}")
    return reports


def run_verification() -> dict[str, Any]:
    # 1. Check Lean source hygiene
    lean_violations = check_source_hygiene()
    if lean_violations:
        raise RuntimeError(f"Lean source hygiene failed: {lean_violations}")

    # 2. Run pytest suite
    py_code, py_out = run_cmd([sys.executable, "-m", "pytest", "tests", "-v"], cwd=ROOT)
    if py_code != 0:
        raise RuntimeError(f"Pytest failed (exit {py_code}):\n{py_out}")
    print("PASS: Python tests (pytest)")

    # 3. Build Lean targets
    lake_code, lake_out = run_cmd(["lake", "build", *MODULES, "Inventory"], cwd=LEAN_DIR)
    if lake_code != 0:
        raise RuntimeError(f"Lake build failed (exit {lake_code}):\n{lake_out}")
    print("PASS: Lake build")

    # 4. Run Inventory census
    inv_code, inv_out = run_cmd(["lake", "env", "lean", "Inventory.lean"], cwd=LEAN_DIR)
    if inv_code != 0:
        raise RuntimeError(f"Inventory execution failed (exit {inv_code}):\n{inv_out}")

    census_names = CENSUS_LINE_PATTERN.findall(inv_out)
    if not census_names:
        raise ValueError("Census produced 0 declarations.")
    if len(census_names) != len(set(census_names)):
        raise ValueError("Duplicate declarations detected in census.")

    # 5. Gather all axiom reports
    all_logs = [inv_out]
    for m in MODULES:
        m_code, m_out = run_cmd(["lake", "env", "lean", f"{m}.lean"], cwd=LEAN_DIR)
        if m_code != 0:
            raise RuntimeError(f"Lean execution failed for {m}.lean:\n{m_out}")
        all_logs.append(m_out)

    combined_log = "\n".join(all_logs)
    reports = parse_axiom_reports(combined_log, census_names)
    print(f"PASS: Lean theorem census ({len(reports)} declarations verified within {{propext, Quot.sound}})")

    # 6. Check Claim Hygiene
    claim_violations = check_claim_hygiene()
    if claim_violations:
        raise RuntimeError(f"Claim hygiene violations detected:\n" + "\n".join(claim_violations))
    print("PASS: Claim hygiene scan")

    # 7. Compute frozen charter hash in Python
    from charter import TargetClassCharter
    charter = TargetClassCharter()
    freeze_hash = charter.freeze()

    axiom_free_count = sum(1 for ax in reports.values() if len(ax) == 0)
    propext_count = sum(1 for ax in reports.values() if ax == ["propext"])

    receipt = {
        "status": "PASS",
        "gate": "G001_TOE_TARGET_CLASS_CHARTER",
        "charter_status": "TOE_TARGET_CLASS_FROZEN",
        "charter_freeze_hash": freeze_hash,
        "criteria_count": 9,
        "lean_toolchain": "leanprover/lean4:v4.33.0",
        "axiom_boundary": ["propext", "Quot.sound"],
        "census_theorem_count": len(reports),
        "axiom_free_theorem_count": axiom_free_count,
        "propext_only_theorem_count": propext_count,
        "reports": reports,
    }
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="G001 Verification")
    parser.add_argument("--write", action="store_true", help="Write receipt to evidence/receipt.json")
    args = parser.parse_args()

    try:
        receipt = run_verification()
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        RECEIPT_FILE.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"WROTE: {RECEIPT_FILE}")
        return 0
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
