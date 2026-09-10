#!/usr/bin/env python3
"""Master test runner for Genesis Cohort 2 E2E test suite.

Discovers and executes all 4 test tiers:
- Tier 1: Feature Coverage (suites/tier1_features.py)
- Tier 2: Boundary & Corner Cases (suites/tier2_boundaries.py)
- Tier 3: Pairwise Combinatorial (suites/tier3_pairwise.py)
- Tier 4: Real-World Workloads (suites/tier4_workloads.py)

Enforces exit code 0 on 100% pass, non-zero on any failure.
Adheres strictly to the Claim Hygiene Rule: local receipts only, no ungrounded claims.
"""

from __future__ import annotations

import importlib
import importlib.util
import inspect
import sys
import time
from pathlib import Path
from typing import Callable, List, Tuple

E2E_DIR = Path(__file__).resolve().parent
SUITES_DIR = E2E_DIR / "suites"

if str(E2E_DIR) not in sys.path:
    sys.path.insert(0, str(E2E_DIR))


TIER_CONFIGS = [
    ("Tier 1", "Feature Coverage (>=80 tests across 16 features)", SUITES_DIR / "tier1_features.py"),
    ("Tier 2", "Boundary & Corner Cases (>=80 tests across 16 features)", SUITES_DIR / "tier2_boundaries.py"),
    ("Tier 3", "Cross-Feature Combinations (Pairwise Integration)", SUITES_DIR / "tier3_pairwise.py"),
    ("Tier 4", "Real-World Workloads (End-to-End Scenarios)", SUITES_DIR / "tier4_workloads.py"),
]


def load_module_from_path(file_path: Path):
    module_name = file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot create module spec for {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_tier(tier_id: str, tier_name: str, file_path: Path) -> Tuple[int, int, List[str], float]:
    if not file_path.exists():
        return (0, 1, [f"File not found: {file_path}"], 0.0)

    start_time = time.perf_counter()
    module = load_module_from_path(file_path)

    test_funcs: List[Tuple[str, Callable]] = []
    for name, obj in inspect.getmembers(module):
        if name.startswith("test_") and inspect.isfunction(obj):
            test_funcs.append((name, obj))

    # Sort test functions to ensure deterministic execution order
    test_funcs.sort(key=lambda x: x[0])

    passed = 0
    failures: List[str] = []

    for name, func in test_funcs:
        try:
            func()
            passed += 1
        except Exception as ex:
            failures.append(f"{name}: {ex}")

    duration = time.perf_counter() - start_time
    return (passed, len(failures), failures, duration)


def main() -> int:
    print("=" * 80)
    print("GENESIS COHORT 2: MASTER E2E VERIFICATION RUNNER")
    print("=" * 80)
    print(f"Test Directory: {E2E_DIR}")
    print(f"Python Version: {sys.version.split()[0]}")
    print("-" * 80)

    total_passed = 0
    total_failed = 0
    total_duration = 0.0
    all_failures: List[Tuple[str, str]] = []

    report_rows = []

    for tier_id, description, file_path in TIER_CONFIGS:
        passed, failed, fails, duration = run_tier(tier_id, description, file_path)
        total_passed += passed
        total_failed += failed
        total_duration += duration
        status = "PASS" if failed == 0 else "FAIL"
        report_rows.append((tier_id, file_path.name, passed + failed, passed, failed, f"{duration:.3f}s", status))

        for f in fails:
            all_failures.append((tier_id, f))

    # Print summary table
    print(f"{'Tier':<8} {'Suite File':<24} {'Total':<8} {'Passed':<8} {'Failed':<8} {'Time':<10} {'Status':<6}")
    print("-" * 80)
    for row in report_rows:
        print(f"{row[0]:<8} {row[1]:<24} {row[2]:<8} {row[3]:<8} {row[4]:<8} {row[5]:<10} {row[6]:<6}")
    print("-" * 80)
    print(f"TOTAL:   {total_passed + total_failed} tests executed across {len(TIER_CONFIGS)} tiers in {total_duration:.3f}s")
    print(f"RESULT:  {total_passed} passed, {total_failed} failed")
    print("=" * 80)

    if total_failed > 0:
        print()
        print("FAILURE DETAILS:")
        for tier_id, fail_msg in all_failures:
            print(f"  [{tier_id}] {fail_msg}")
        print("=" * 80)
        return 1

    print("VERIFICATION RECEIPT: All 4 tiers passed with exit code 0.")
    print("Claim Hygiene Discipline: Scoped to constructive finite models without ungrounded universality.")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
