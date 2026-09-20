"""Verify Lean 4 proofs, axiom dependencies, and receipts for CL-ISO-SOUND.

Usage:
    python research/iso_sound_lean/verify_lean.py --write
    python research/iso_sound_lean/verify_lean.py --check

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
import sys

THEOREMS = (
    "IsoSoundLean.Perm.ext",
    "IsoSoundLean.Perm.id_comp",
    "IsoSoundLean.Perm.comp_id",
    "IsoSoundLean.Perm.comp_assoc",
    "IsoSoundLean.Perm.comp_left_inv",
    "IsoSoundLean.Perm.comp_right_inv",
    "IsoSoundLean.Perm.inv_id",
    "IsoSoundLean.Perm.inv_inv",
    "IsoSoundLean.Perm.inv_comp",
    "IsoSoundLean.inv_act_act",
    "IsoSoundLean.act_inv_act",
    "IsoSoundLean.act_inj",
    "IsoSoundLean.act_eq_iff",
    "IsoSoundLean.iso_refl",
    "IsoSoundLean.iso_symm",
    "IsoSoundLean.iso_trans",
    "IsoSoundLean.mem_orbit_iff",
    "IsoSoundLean.iso_iff_same_orbit",
    "IsoSoundLean.witness_extract",
    "IsoSoundLean.iso_witness_of_orbit_choice",
    "IsoSoundLean.cl_iso_sound",
    "IsoSoundLean.cl_iso_complete",
    "IsoSoundLean.canonical_classification",
    "IsoSoundLean.key_soundness",
    "IsoSoundLean.key_classification",
    "IsoSoundLean.equivariant_search_same_image",
    "IsoSoundLean.minimizer_isomorphism_sound",
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
        command, cwd=cwd, check=False, capture_output=True, text=True, encoding="utf-8"
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
        if ".lake" in path.parts:
            continue
        raw = path.read_bytes().replace(b"\r\n", b"\n")
        text = raw.decode("utf-8")
        match = FORBIDDEN.search(text)
        if match is not None:
            raise ValueError(f"forbidden Lean token in {path.name}: {match.group(0)}")
        result[path.relative_to(lean_root).as_posix()] = sha256(raw).hexdigest()
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
    run([lake_exe, "build"], lean_root)
    report = run([lake_exe, "env", "lean", "Inventory.lean"], lean_root)
    axioms = parse_axioms(report)
    text = (
        "\n".join(f"{name}: {','.join(axioms[name]) or 'none'}" for name in THEOREMS)
        + "\n"
    ).encode("utf-8")
    payload = {
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "authority_effect": None,
        "axiom_inventory": axioms,
        "source_hashes": source_hashes(lean_root),
        "terminal": "ORBIT_CHOICE_SOUND_CONDITIONAL",
    }
    return text, (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write receipt files")
    mode.add_argument("--check", action="store_true", help="verify receipts against fresh build")
    args = parser.parse_args()

    is_write = args.write
    is_check = args.check or (not args.write)

    try:
        text, payload = render()
        receipt_root = tree_root() / "receipts"
        receipt_root.mkdir(parents=True, exist_ok=True)
        paths = {
            receipt_root / "lean_axioms.txt": text,
            receipt_root / "lean.json": payload,
        }
        if is_write:
            for path, value in paths.items():
                path.write_bytes(value)
            print(f"Lean receipts written: {len(THEOREMS)} theorem reports recorded")
            return 0
        if is_check:
            for path, value in paths.items():
                if not path.exists():
                    raise ValueError(f"Lean receipt missing: {path.name}")
                disk_bytes = path.read_bytes().replace(b"\r\n", b"\n")
                if disk_bytes != value:
                    raise ValueError(f"Lean receipt differs: {path.name}")
            print(f"Lean receipt replay clean: {len(THEOREMS)} theorem reports verified")
            return 0
        return 0
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
