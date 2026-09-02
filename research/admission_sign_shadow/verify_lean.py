from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess


THEOREMS = (
    "AdmissionSignShadow.histories_distinct",
    "AdmissionSignShadow.same_erased_endpoint",
    "AdmissionSignShadow.exchange_involutive",
    "AdmissionSignShadow.exchange_has_no_fixed_point",
    "AdmissionSignShadow.act_identity",
    "AdmissionSignShadow.act_composition",
    "AdmissionSignShadow.unique_transporter",
    "AdmissionSignShadow.Polarity.toInt_mul",
    "AdmissionSignShadow.character_classification",
    "AdmissionSignShadow.trivial_and_sign_are_characters",
    "AdmissionSignShadow.character_laws_do_not_force_nontrivial",
    "AdmissionSignShadow.nontrivial_exchange_is_negative",
    "AdmissionSignShadow.nontrivial_character_unique",
    "AdmissionSignShadow.nontrivial_exchange_toInt",
    "AdmissionSignShadow.operational_nontrivial_iff_labels_separate",
    "AdmissionSignShadow.sign_exchange_relative",
    "AdmissionSignShadow.sign_global_basepoint_flip",
    "AdmissionSignShadow.relative_label_classification",
    "AdmissionSignShadow.relative_label_unique_after_basepoint",
    "AdmissionSignShadow.global_neg_preserves_relative",
    "AdmissionSignShadow.nodup_append_of_disjoint",
    "AdmissionSignShadow.occurrence_valid_append",
    "AdmissionSignShadow.countToken_nil",
    "AdmissionSignShadow.countToken_append",
    "AdmissionSignShadow.countToken_perm",
    "AdmissionSignShadow.occurrence_equivalent_refl",
    "AdmissionSignShadow.occurrence_equivalent_symm",
    "AdmissionSignShadow.occurrence_equivalent_trans",
    "AdmissionSignShadow.perm_occurrence_equivalent",
    "AdmissionSignShadow.once_valid",
    "AdmissionSignShadow.twice_valid",
    "AdmissionSignShadow.canonical_forget_same_count_differs",
    "AdmissionSignShadow.count_equivalent_but_ordered_forget_differs",
    "AdmissionSignShadow.canonical_data_does_not_determine_count",
    "AdmissionSignShadow.count_calibration_unique",
    "AdmissionSignShadow.calibrated_occurrence_weight",
    "AdmissionSignShadow.occurrenceWeight_zero",
    "AdmissionSignShadow.occurrenceWeight_append",
    "AdmissionSignShadow.separating_weight_does_not_factor",
    "AdmissionSignShadow.zero_weight_factors_through_forget",
    "AdmissionSignShadow.collapsed_pair_rejected",
    "AdmissionSignShadow.unequal_endpoints_rejected",
    "AdmissionSignShadow.induced_coordinate_squares_equal",
    "AdmissionSignShadow.conditional_mixing_separation",
    "AdmissionSignShadow.trivial_character_rejected",
    "AdmissionSignShadow.trivial_character_no_pair_change",
    "AdmissionSignShadow.square_mixing_separates",
    "AdmissionSignShadow.square_mixing_contact",
    "AdmissionSignShadow.coordinate_data_does_not_force_mixing",
    "AdmissionSignShadow.three_cycle_is_not_involution",
    "AdmissionSignShadow.three_involution_has_fixed_point",
    "AdmissionSignShadow.no_free_three_involution",
    "AdmissionSignShadow.two_coordinates_do_not_determine_third",
    "AdmissionSignShadow.flip_family_has_no_natural_choice",
    "AdmissionSignShadow.report_section_does_not_determine_natural_choice",
    "AdmissionSignShadow.flip_family_has_no_adapter_kernel",
    "AdmissionSignShadow.empty_report_has_no_section",
    "AdmissionSignShadow.natural_choice_does_not_determine_report_section",
)
ALLOWED_AXIOMS = frozenset({"propext", "Quot.sound"})
FORBIDDEN = re.compile(
    r"\b(sorry|admit|unsafe|partial|noncomputable)\b|^\s*axiom\s|\bClassical\.",
    re.MULTILINE,
)
NO_AXIOMS = re.compile(r"'([^']+)' does not depend on any axioms")
HAS_AXIOMS = re.compile(r"'([^']+)' depends on axioms: \[([^\]]*)\]")


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
        result[path.relative_to(lean_root).as_posix()] = sha256(path.read_bytes()).hexdigest()
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
    run([lake_exe, "build", "AdmissionSignShadow"], lean_root)
    report = run(
        [lake_exe, "env", "lean", "AdmissionSignShadow/AxiomReport.lean"], lean_root
    )
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
        "terminal": "CONDITIONAL_CONNECTOR_PROVED",
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
        if not path.exists() or path.read_bytes() != value:
            raise ValueError(f"Lean receipt differs: {path.name}")
    print(f"Lean receipt replay clean: {len(THEOREMS)} theorem reports")


if __name__ == "__main__":
    main()
