"""Seal and axiom audits for Cohort 6."""
from __future__ import annotations

from fractions import Fraction
import math
from pathlib import Path
import random
import subprocess
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TARGET_DIRS = [
    REPO_ROOT / "research" / "p203_composite_systems",
    REPO_ROOT / "research" / "m108_internal_algebra",
    REPO_ROOT / "research" / "m109_obstruction_homology",
    REPO_ROOT / "research" / "x300_observer_information",
]
for p in reversed(TARGET_DIRS):
    p_str = str(p)
    if p_str in sys.path:
        sys.path.remove(p_str)
    sys.path.insert(0, p_str)

import composite_systems as p203
import algebra as m108
import homology as m109
import information as x300

def audit_repository_seal_and_axioms() -> int:
    """Audit repository blind seal integrity and Lean 4 axiom censuses across Cohort 6."""
    print(">>> Auditing Repository Seal & Lean 4 Axioms...")
    checks = 0

    SEALED_PATHS = [
        "prompt",
        "paper",
        "code",
        "lean4/Derivation",
        "artifacts",
        "CLAUDE.md",
    ]

    # 1. Seal audit: git status
    git_proc = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert git_proc.returncode == 0
    violations = []
    for line in git_proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        status = parts[0]
        path = parts[1].replace("\\", "/")

        for sp in SEALED_PATHS:
            if path == sp or path.startswith(sp + "/"):
                violations.append(path)

        # Tracked modifications outside research/ and .agents/
        if status in ("M", "D", "A", "R") and not (path.startswith("research/") or path.startswith(".agents/")):
            violations.append(path)

    assert len(violations) == 0, f"Repository seal violation detected: {violations}"
    checks += 1

    # 2. Lean packages build and axiom audit across all 4 targets
    lean_packages = [
        REPO_ROOT / "research" / "p203_composite_systems" / "lean",
        REPO_ROOT / "research" / "m108_internal_algebra" / "lean",
        REPO_ROOT / "research" / "m109_obstruction_homology" / "lean",
        REPO_ROOT / "research" / "x300_observer_information" / "lean",
    ]
    ALLOWED_AXIOMS = {"propext", "Quot.sound"}

    for pkg in lean_packages:
        # lake build
        proc = subprocess.run(["lake", "build"], cwd=pkg, capture_output=True, text=True, check=False)
        assert proc.returncode == 0, f"lake build failed for {pkg.parent.name}:\n{proc.stderr}"
        checks += 1

        # Inventory.lean census and axiom audit
        inv_proc = subprocess.run(
            ["lake", "env", "lean", "Inventory.lean"], cwd=pkg, capture_output=True, text=True, check=False
        )
        assert inv_proc.returncode == 0, f"Inventory.lean failed for {pkg.parent.name}:\n{inv_proc.stderr}"
        output = inv_proc.stdout + inv_proc.stderr

        # Check forbidden dependencies
        for forbidden in ["Classical.choice", "mathlib"]:
            assert forbidden not in output, f"Disallowed dependency '{forbidden}' found in {pkg.parent.name}"

        # Parse axioms
        for line in output.splitlines():
            if "depends on axioms: [" in line:
                ax_part = line.split("depends on axioms: [")[1].split("]")[0]
                axioms = [a.strip() for a in ax_part.split(",") if a.strip()]
                for a in axioms:
                    assert a in ALLOWED_AXIOMS, (
                        f"Disallowed axiom '{a}' in {pkg.parent.name}: not in {ALLOWED_AXIOMS}"
                    )
        checks += 1

    print(f"  Seal and axiom audits passed {checks} checks.")
    return checks


# ==============================================================================
# Main Runner & Receipt Generation
# ==============================================================================

