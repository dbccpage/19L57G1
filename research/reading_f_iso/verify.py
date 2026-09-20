"""Verification script for research/reading_f_iso (Target 2).

Audits source hygiene (no sorry, admit, unsafe, partial, or mathlib imports),
runs lake build, checks the emitted theorem reports for this package against
{"propext", "Quot.sound"}, and requires the fixed expected_theorems list.

2026-09-19: the former all-theorems wording is withdrawn. A local compiled
module census found 33 theorem constants with non-internal names, including
generated declarations; the required list names 13, leaving 20 outside
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
        if not name.startswith("ReadingFIso."):
            continue
        axioms = [a.strip() for a in used.group(2).split(",") if a.strip()] if used else []
        disallowed = set(axioms) - ALLOWED_AXIOMS
        if disallowed:
            raise ValueError(f"Disallowed axioms in {name}: {disallowed}")
        reports[name] = axioms

    expected_theorems = {
        "ReadingFIso.single_form_fmap",
        "ReadingFIso.not_iso_BD_F_U0F",
        "ReadingFIso.not_iso_BL_F_U0F",
        "ReadingFIso.not_iso_FOUT_F_U0F",
        "ReadingFIso.not_iso_FIN_F_U0F",
        "ReadingFIso.not_iso_BD_F_BL_F",
        "ReadingFIso.not_iso_BD_F_FOUT_F",
        "ReadingFIso.not_iso_BD_F_FIN_F",
        "ReadingFIso.not_iso_BL_F_FOUT_F",
        "ReadingFIso.not_iso_BL_F_FIN_F",
        "ReadingFIso.not_iso_FOUT_F_FIN_F",
        "ReadingFIso.ten_pairwise_non_isomorphic",
        "ReadingFIso.ten_pairwise_disequal",
    }

    missing = expected_theorems - set(reports)
    if missing:
        raise ValueError(f"Missing axiom reports for: {missing}")

    print(f"Verified {len(reports)} theorem axiom reports:")
    for name, axioms in sorted(reports.items()):
        print(f"  {name}: {axioms}")


def main() -> None:
    print("=== Verifying research/reading_f_iso (Target 2) ===")
    verify_hygiene()
    output = verify_lake_build()
    verify_axioms(output)
    print("=== Target 2 verification PASSED ===")


if __name__ == "__main__":
    main()
