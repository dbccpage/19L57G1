"""Verify Lean 4 formalization receipts for research/higher_order_diagonalization.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess

THEOREMS = (
    # ObserverHierarchy
    "HigherOrderDiagonalization.flip_token_involutive",
    "HigherOrderDiagonalization.flip_seq_involutive",
    "HigherOrderDiagonalization.flip_seq_length",
    "HigherOrderDiagonalization.canon_seq_length",
    "HigherOrderDiagonalization.iso_refl",
    "HigherOrderDiagonalization.iso_symm",
    "HigherOrderDiagonalization.iso_trans",
    "HigherOrderDiagonalization.iso_equivalence",
    "HigherOrderDiagonalization.prefixK_canon_respects_iso",
    "HigherOrderDiagonalization.eval_lt_capacity",
    "HigherOrderDiagonalization.eval_respects_iso",
    "HigherOrderDiagonalization.observer_equiv_equivalence",
    "HigherOrderDiagonalization.observer_equiv_coarsening",
    "HigherOrderDiagonalization.compose_higher_order_respects_iso",
    # SeparationCapacity
    "HigherOrderDiagonalization.natToBits_length",
    "HigherOrderDiagonalization.bitsToNat_natToBits",
    "HigherOrderDiagonalization.natToBits_injective",
    "HigherOrderDiagonalization.canonSeq_zero_head",
    "HigherOrderDiagonalization.testRegime_canon",
    "HigherOrderDiagonalization.testRegime_pairwise_non_isomorphic",
    "HigherOrderDiagonalization.test_family_size_gt_capacity",
    "HigherOrderDiagonalization.capacity_gap_strictly_positive",
    "HigherOrderDiagonalization.capacity_gap_asymptotic",
    "HigherOrderDiagonalization.capacity_gap_at_k_plus_2",
    # Diagonalization
    "HigherOrderDiagonalization.length_filter_split",
    "HigherOrderDiagonalization.filter_nodup",
    "HigherOrderDiagonalization.nodup_filter_eq_le_one",
    "HigherOrderDiagonalization.nodup_length_le",
    "HigherOrderDiagonalization.upto_length",
    "HigherOrderDiagonalization.upto_mem",
    "HigherOrderDiagonalization.map_nodup_of_inj",
    "HigherOrderDiagonalization.pigeonhole",
    "HigherOrderDiagonalization.higher_order_diagonalization",
    "HigherOrderDiagonalization.diagonal_fiber_non_singleton",
    "HigherOrderDiagonalization.higher_order_diagonal_duality",
)

ALLOWED_AXIOMS = frozenset({"propext", "Quot.sound"})
FORBIDDEN = re.compile(
    r"\b(sorry|admit|unsafe|partial|noncomputable)\b|^\s*axiom\s|\bClassical\.",
    re.MULTILINE,
)
# `.+?` and not `[^']+`: a primed theorem name ends in a quote
# character, and the character-class pattern cannot capture it --
# the recorded primed-names parser defect.  `.` stops at a line end,
# so one capture never spans two reports.  Repaired 2026-09-18.
NO_AXIOMS = re.compile(r"'(.+?)' does not depend on any axioms")
HAS_AXIOMS = re.compile(r"'(.+?)' depends on axioms: \[([^\]]*)\]")


def tree_root() -> Path:
    return Path(__file__).resolve().parent


def lake() -> str:
    located = shutil.which("lake")
    if located is None:
        fallback = Path.home() / ".elan" / "bin" / "lake.exe"
        if not fallback.exists():
            raise ValueError("lake executable is unavailable")
        return str(fallback)
    return located


def run(command: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        command, cwd=cwd, check=False, capture_output=True, text=True
    )
    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        raise ValueError(
            f"command failed with {completed.returncode}: {' '.join(command)}\n{output}"
        )
    return output


def source_hashes(lean_root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(lean_root.rglob("*.lean")):
        text = path.read_text(encoding="utf-8")
        match = FORBIDDEN.search(text)
        if match is not None:
            raise ValueError(f"forbidden Lean token in {path.name}: {match.group(0)}")
        result[path.relative_to(lean_root).as_posix()] = sha256(
            text.encode("utf-8")
        ).hexdigest()
    return result


def parse_axioms(output: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for name in NO_AXIOMS.findall(output):
        result[name] = []
    for name, values in HAS_AXIOMS.findall(output):
        result[name] = sorted(value.strip() for value in values.split(",") if value.strip())
    if set(result) != set(THEOREMS):
        raise ValueError(
            f"axiom report population differs: missing={sorted(set(THEOREMS) - set(result))} "
            f"extra={sorted(set(result) - set(THEOREMS))}"
        )
    disallowed = sorted(
        {axiom for values in result.values() for axiom in values} - ALLOWED_AXIOMS
    )
    if disallowed:
        raise ValueError(f"disallowed axioms: {disallowed}")
    return result


def render() -> tuple[bytes, bytes]:
    root = tree_root()
    lean_root = root / "lean"
    lake_exe = lake()
    # Clean and build to capture inventory replay output
    run([lake_exe, "clean"], lean_root)
    output = run([lake_exe, "build"], lean_root)
    axioms = parse_axioms(output)
    text = (
        "\n".join(f"{name}: {','.join(axioms[name]) or 'none'}" for name in THEOREMS)
        + "\n"
    ).encode("utf-8")
    payload = {
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "authority_effect": None,
        "axiom_inventory": axioms,
        "source_hashes": source_hashes(lean_root),
        "terminal": "HIGHER_ORDER_DIAGONALIZATION_BOUNDED_CAPACITY_AND_FIBER_COLLAPSE",
    }
    return text, (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    text, payload = render()
    receipt_root = tree_root() / "receipts"
    receipt_root.mkdir(parents=True, exist_ok=True)
    paths = {
        receipt_root / "lean_axioms.txt": text,
        receipt_root / "lean.json": payload,
    }
    if args.write:
        for path, value in paths.items():
            path.write_bytes(value)
    for path, value in paths.items():
        if not path.exists():
            raise ValueError(f"Lean receipt missing: {path.name}")
        disk_bytes = path.read_bytes().replace(b"\r\n", b"\n")
        if disk_bytes != value:
            raise ValueError(f"Lean receipt differs: {path.name}")
    print(f"Lean receipt replay clean: {len(THEOREMS)} theorem reports")


if __name__ == "__main__":
    main()
