"""Verification and governance harness for Target X310: Vertical Integration Chain.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, narrow, receipt-grounded).

Lifecycle verification across all six integrated estate layers:
1. Substrate (Target A / G011)
2. Observers (P200 / G014)
3. Semantics & Grounding Firewall (X301)
4. Exact Rational Solvers & Farkas Dual Receipts in Q (M114)
5. DAG Truth Maintenance & AGM Belief Revision (X302)
6. Bounded Operational Agency & Committee Licensing (X303)

Audits:
- Source hygiene (no sorry/admit in Lean; zero unpinned watchlist hits).
- Python test suite across tests/.
- Programmatic 4-relation vertical commutation audit.
- Full end-to-end 6-stage pipeline execution with byte-pinned grand receipt.
- Lean 4 formalization build and axiom audit.
- Emits deterministic evidence/receipt.json.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Mapping, Optional

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent.parent
LEAN_DIR = ROOT / "lean"
EVIDENCE_DIR = ROOT / "evidence"
RECEIPT_PATH = EVIDENCE_DIR / "receipt.json"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "code") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code"))

for _sub in [
    "target_a_execution",
    "g011_finitary_substrate",
    "p200_operational_protocols",
    "g014_observer_descent",
    "x301_formal_semantics",
    "m114_solver_adapter",
    "x302_operational_reasoning",
    "x303_bounded_agency",
]:
    _sub_path = REPO_ROOT / "research" / _sub
    if str(_sub_path) not in sys.path:
        sys.path.insert(0, str(_sub_path))

import research.target_a_execution.runner as _tar_runner
sys.modules["runner"] = _tar_runner
import research.p200_operational_protocols.protocol as _p200_prot
sys.modules["protocol"] = _p200_prot
import research.p200_operational_protocols.embedded_observer as _p200_emb
sys.modules["embedded_observer"] = _p200_emb

from research.x310_vertical_integration.pipeline import (
    PipelineConfig,
    PipelineResult,
    canonical_grand_receipt_digest,
    canonical_json_dumps,
    run_commutation_audit,
    run_vertical_pipeline,
)

ALLOWED_AXIOMS = {"propext", "Quot.sound"}
FORBIDDEN_LEAN_TOKENS = re.compile(
    r"\b(?:sorry|admit|unsafe|partial)\b|^\s*axiom\s", re.MULTILINE
)
FORBIDDEN_DIGEST = "4cbe09597b76794b5f6b854c1c1c035ede6d241f250f223b61987dce9d2d7a4b"

AXIOM_RE = re.compile(
    r"^(?:info:\s*)?(?:[\w\.\-]+:\d+:\d+:\s*)?'(.+?)' depends on axioms: \[(.*?)\]$",
    re.MULTILINE,
)
NO_AXIOM_RE = re.compile(
    r"^(?:info:\s*)?(?:[\w\.\-]+:\d+:\d+:\s*)?'(.+?)' does not depend on any axioms$",
    re.MULTILINE,
)


def sha256_file(path: Path) -> str:
    """Deterministic file SHA-256 with newline normalization."""
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def has_watched_digest(text: str) -> bool:
    """Check whole-word tokens against watched digest."""
    for token in re.findall(r"\b[a-zA-Z]+\b", text.lower()):
        d = hashlib.sha256(token.encode("utf-8")).hexdigest()
        if d == FORBIDDEN_DIGEST:
            return True
        if token.endswith("s"):
            d_stem = hashlib.sha256(token[:-1].encode("utf-8")).hexdigest()
            if d_stem == FORBIDDEN_DIGEST:
                return True
    return False


def _assert_no_floats(obj: Any, path: str = "") -> None:
    """Recursively verify that zero floating-point numbers exist in receipt structures."""
    if isinstance(obj, float):
        raise AssertionError(f"Found float {obj} at path: {path}")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _assert_no_floats(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, (list, tuple)):
        for i, item in enumerate(obj):
            _assert_no_floats(item, f"{path}[{i}]")


def check_source_hygiene() -> dict[str, str]:
    """Verify source files: no unpinned forbidden tokens or disallowed Lean axioms."""
    hashes: dict[str, str] = {}

    # Check Lean files if present
    if LEAN_DIR.is_dir():
        for p in sorted(LEAN_DIR.glob("*.lean")):
            text = p.read_text(encoding="utf-8")
            if FORBIDDEN_LEAN_TOKENS.search(text):
                raise ValueError(f"Forbidden token found in Lean source: {p.name}")
            if has_watched_digest(text):
                raise ValueError(f"Watched forbidden term found in Lean source: {p.name}")
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            hashes[rel] = sha256_file(p)

    # Check Python engine files
    for p in sorted(ROOT.glob("*.py")):
        text = p.read_text(encoding="utf-8")
        if has_watched_digest(text):
            raise ValueError(f"Watched forbidden term found in Python source: {p.name}")
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        hashes[rel] = sha256_file(p)

    # Check test files
    tests_dir = ROOT / "tests"
    if tests_dir.is_dir():
        for p in sorted(tests_dir.glob("*.py")):
            text = p.read_text(encoding="utf-8")
            if has_watched_digest(text):
                raise ValueError(f"Watched forbidden term found in test source: {p.name}")
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            hashes[rel] = sha256_file(p)

    return hashes


def run_pytest() -> dict[str, Any]:
    """Run pytest suite on research/x310_vertical_integration/tests/."""
    tests_path = str(ROOT / "tests")
    cmd = [sys.executable, "-m", "pytest", "-v", tests_path]
    print(f"== Running pytest: {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
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


def run_commutation_audit_section() -> dict[str, Any]:
    """Execute the 4-relation vertical commutation audit."""
    print("== Running programmatic vertical commutation audit")
    audit_dict = run_commutation_audit()
    for rel_name, passed in audit_dict.items():
        if not isinstance(passed, bool):
            continue
        print(f"   - {rel_name}: {'PASS' if passed else 'FAIL'}")
        if not passed:
            raise RuntimeError(f"Commutation audit failed on relation: {rel_name}")
    return {
        "status": "PASS",
        "commutation_relations": audit_dict,
    }


def run_end_to_end_pipeline() -> PipelineResult:
    """Execute full 6-stage vertical pipeline under fixed configuration."""
    print("== Running full 6-stage vertical pipeline end-to-end")
    cfg = PipelineConfig(
        run_id="X310-VERIFY-CANONICAL",
        timestamp_fixed="2026-09-12T00:00:00Z",
        panel_size=3,
        fuel_budget=20,
        solver_fuel=50,
        memory_horizon=10,
    )
    result = run_vertical_pipeline(cfg)
    if not result.is_success:
        raise RuntimeError(f"Pipeline execution failed: {result.refusal_stage}: {result.refusal_reason}")

    # Certify absence of floats across receipt
    _assert_no_floats(result.grand_receipt)

    # Verify grand receipt cryptographic hash integrity
    expected_sha = canonical_grand_receipt_digest(result.grand_receipt)
    if expected_sha != result.grand_receipt_sha256:
        raise RuntimeError(f"Grand receipt digest mismatch: {expected_sha} != {result.grand_receipt_sha256}")

    print(f"   Pipeline completed successfully: SHA256={result.grand_receipt_sha256}")
    return result


def run_lean() -> dict[str, Any]:
    """Verify Lean formalization package if present."""
    lakefile = LEAN_DIR / "lakefile.toml"
    inventory = LEAN_DIR / "Inventory.lean"

    if not LEAN_DIR.is_dir() or not lakefile.is_file():
        return {
            "status": "NOT_PRESENT",
            "note": "Lean formalization package not present.",
        }

    print("== Building Lean package with lake build")
    build_proc = subprocess.run(
        ["lake", "build"], cwd=LEAN_DIR, capture_output=True, text=True, check=False
    )
    build_output = build_proc.stdout + "\n" + build_proc.stderr
    print(build_output)
    if build_proc.returncode != 0:
        raise RuntimeError(f"lake build failed ({build_proc.returncode}):\n{build_output}")

    theorems: dict[str, list[str]] = {}
    if inventory.is_file():
        print("== Running Inventory.lean census and axiom audit")
        for name, ax_str in AXIOM_RE.findall(build_output):
            ax_list = [a.strip() for a in ax_str.split(",") if a.strip()]
            theorems[name] = ax_list
            disallowed = set(ax_list) - ALLOWED_AXIOMS
            if disallowed:
                raise ValueError(f"Disallowed axioms in theorem {name}: {disallowed}")

        for name in NO_AXIOM_RE.findall(build_output):
            theorems[name] = []

    axiom_free = sum(1 for ax in theorems.values() if not ax)
    return {
        "build_status": "PASS",
        "theorem_count": len(theorems),
        "axiom_free_count": axiom_free,
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "theorems": dict(sorted(theorems.items())),
    }


def verify(write_receipt: bool = True, check_only: bool = False) -> dict[str, Any]:
    """Run full verification pipeline and emit/check grand receipt."""
    print("=== Starting Target X310 Verification Harness ===")
    hashes = check_source_hygiene()
    pytest_res = run_pytest()
    comm_res = run_commutation_audit_section()
    pipe_res = run_end_to_end_pipeline()
    lean_res = run_lean()

    combined_receipt: dict[str, Any] = {
        "schema": "x310-vertical-integration-v1",
        "receipt_version": "1.0.0",
        "target": "Target X310: Vertical Integration Chain",
        "status": "PASS",
        "authority_effect": "None",
        "timestamp_utc": "2026-09-12T00:00:00Z",
        "pipeline_run_id": "X310-VERIFY-CANONICAL",
        "source_hashes": hashes,
        "pytest": pytest_res,
        "commutation_audit": comm_res,
        "pipeline_execution": {
            "is_success": pipe_res.is_success,
            "is_refusal": pipe_res.is_refusal,
            "refusal_stage": pipe_res.refusal_stage,
            "refusal_reason": pipe_res.refusal_reason,
            "initial_carrier_hash": pipe_res.grand_receipt["initial_carrier_hash"],
            "final_carrier_hash": pipe_res.grand_receipt["final_carrier_hash"],
            "stage_receipts": pipe_res.stage_receipts,
        },
        "lean": lean_res,
        "claim_hygiene": {
            "scope": (
                "Harness that calls six sibling research packages under a fixed timestamp. "
                "Stages 1, 2, 3, and 6 share the encoded carrier. Stages 4 and 5 are sibling "
                "solver and TMS demos under the same receipt. Codec recovers clock/fuel/nops/tape "
                "from custom_domains. Lean is a Nat-field toy. See CLAIMS.md."
            ),
            "epistemic_posture": "Claim Hygiene Compliant (bounded, narrow, receipt-grounded)",
            "exact_rational_arithmetic_only": True,
            "zero_floating_point": True,
            "refusal_state_preservation": True,
        },
        "grand_receipt_sha256": pipe_res.grand_receipt_sha256,
    }

    _assert_no_floats(combined_receipt)

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    if check_only:
        if not RECEIPT_PATH.is_file():
            raise FileNotFoundError(f"Receipt file does not exist for --check: {RECEIPT_PATH}")
        existing = RECEIPT_PATH.read_bytes()
        fresh = (json.dumps(combined_receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")
        if existing != fresh:
            raise ValueError("evidence/receipt.json differs from the freshly generated receipt")
        print(f"Receipt verified against: {RECEIPT_PATH}")
    elif write_receipt:
        raw = (json.dumps(combined_receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")
        RECEIPT_PATH.write_bytes(raw)
        print(f"Wrote canonical receipt to: {RECEIPT_PATH}")

    print("=== Target X310 Verification: ALL GATES PASS ===")
    return combined_receipt


def main() -> None:
    parser = argparse.ArgumentParser(description="Target X310 Verification Harness")
    parser.add_argument("--write", action="store_true", default=True, help="Write evidence/receipt.json")
    parser.add_argument("--check", action="store_true", default=False, help="Check against existing receipt")
    parser.add_argument("--no-write", dest="write", action="store_false", help="Do not write receipt")
    args = parser.parse_args()

    try:
        verify(write_receipt=args.write and not args.check, check_only=args.check)
        sys.exit(0)
    except Exception as exc:
        print(f"Verification FAILED: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
