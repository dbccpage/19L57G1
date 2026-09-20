"""Verification script for research/redheffer (Target 3).

Audits source hygiene (no sorry, admit, unsafe, partial, or mathlib imports),
runs lake build, checks the emitted theorem reports for this package against
{"propext", "Quot.sound"}, and requires the fixed expected_theorems list.

2026-09-19: the former all-theorems wording is withdrawn. A local compiled
module census found 39 theorem constants with non-internal names, including
generated declarations; the required list names 35, leaving 4 outside
that list. This verifier does not establish that every theorem is reported.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ALLOWED_AXIOMS = {"propext", "Quot.sound"}
FORBIDDEN = re.compile(r"\b(?:sorry|admit|unsafe|partial)\b|^\s*axiom\s", re.MULTILINE)
MATHLIB = re.compile(r"\bmathlib\b", re.IGNORECASE)
AXIOM_USED = re.compile(r"'(.+?)' depends on axioms: \[(.*?)\]")
AXIOM_NONE = re.compile(r"'(.+?)' does not depend on any axioms")


def verify_hygiene() -> None:
    for lean_file in ROOT.glob("*.lean"):
        text = lean_file.read_text(encoding="utf-8")
        if FORBIDDEN.search(text):
            raise ValueError(f"Forbidden token in {lean_file.name}")
        if MATHLIB.search(text):
            raise ValueError(f"Mathlib import detected in {lean_file.name}")
    print("Source hygiene verified: no forbidden tokens or mathlib imports.")


def verify_lake_build() -> str:
    result = subprocess.run(
        ["lake", "build"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    output = result.stdout + result.stderr
    if result.returncode != 0:
        raise RuntimeError(f"lake build failed ({result.returncode}):\n{output}")
    print("Lake build completed cleanly.")
    return output


def verify_axioms(output: str) -> None:
    reports: dict[str, list[str]] = {}
    for line in output.splitlines():
        used = AXIOM_USED.search(line)
        none = AXIOM_NONE.search(line)
        if not used and not none:
            continue
        match = used or none
        name = match.group(1)
        if not name.startswith("RedhefferObstruction."):
            continue
        axioms = [a.strip() for a in used.group(2).split(",") if a.strip()] if used else []
        disallowed = set(axioms) - ALLOWED_AXIOMS
        if disallowed:
            raise ValueError(f"Disallowed axioms in {name}: {disallowed}")
        reports[name] = axioms

    expected_theorems = {
        "RedhefferObstruction.length_insertAll",
        "RedhefferObstruction.mem_insertAll_length",
        "RedhefferObstruction.arrangements_elements_length",
        "RedhefferObstruction.length_flatMap_insertAll",
        "RedhefferObstruction.arrangements_length",
        "RedhefferObstruction.leibniz_complexity_barrier",
        "RedhefferObstruction.factorial_horizon_values",
        "RedhefferObstruction.factorial_8_barrier",
        "RedhefferObstruction.det_redheffer_eq_running_balance_of_column_reduction",
        "RedhefferObstruction.balance_sign_values_to_6",
        "RedhefferObstruction.running_balance_values_to_6",
        "RedhefferObstruction.redheffer_det_values_to_6",
        "RedhefferObstruction.redheffer_det_matches_running_balance_to_6",
        "RedhefferObstruction.redheffer_bounded_obstruction",
        "RedhefferObstruction.redheffer_subdiagonal_zero",
        "RedhefferObstruction.redhefferReduced_upper",
        "RedhefferObstruction.redhefferReduced_diag_one",
        "RedhefferObstruction.redhefferReduced_diag_tail",
        "RedhefferObstruction.redheffer_col_reduction_to_6",
        "RedhefferObstruction.rowProduct_append_singleton",
        "RedhefferObstruction.rowProduct_zero_of_end",
        "RedhefferObstruction.diagProduct_redhefferReduced_step",
        "RedhefferObstruction.diagProduct_redhefferReduced_eq",
        "RedhefferObstruction.diagProduct_redhefferReduced",
        "RedhefferObstruction.redhefferReduced_det_values_to_6",
        "RedhefferObstruction.redheffer_det_eq_reduced_to_6",
        "RedhefferObstruction.leibniz_branch_reduction_to_5",
        "RedhefferObstruction.column_reduction_equivalence_witness",
        "RedhefferObstruction.column_reduction_equivalence_witness_1",
        "RedhefferObstruction.column_reduction_equivalence_witness_2",
        "RedhefferObstruction.column_reduction_equivalence_witness_3",
        "RedhefferObstruction.column_reduction_equivalence_witness_4",
        "RedhefferObstruction.column_reduction_equivalence_witness_5",
        "RedhefferObstruction.column_reduction_equivalence_witness_6",
        "RedhefferObstruction.redheffer_inductive_column_reduction",
    }

    missing = expected_theorems - set(reports)
    if missing:
        raise ValueError(f"Missing axiom reports for: {missing}")

    print(f"Verified {len(reports)} theorem axiom reports:")
    for name, axioms in sorted(reports.items()):
        print(f"  {name}: {axioms}")


def main() -> None:
    print("=== Verifying research/redheffer (Target 3) ===")
    verify_hygiene()
    output = verify_lake_build()
    verify_axioms(output)
    print("=== Target 3 verification PASSED ===")


def test_target3_redheffer() -> None:
    main()


if __name__ == "__main__":
    main()
