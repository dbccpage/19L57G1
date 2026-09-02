from __future__ import annotations

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile
from typing import Final


FROZEN_COMMIT: Final = "3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a"
ALLOWED_AXIOMS: Final = frozenset({"propext", "Quot.sound"})
AXIOM_REPORT: Final = re.compile(
    r"'(?P<name>[^']+)' (?:(?:does not depend on any axioms)|"
    r"(?:depends on axioms: \[(?P<axioms>.*?)\]))",
    re.DOTALL,
)
DEFAULT_MODULES: Final = (
    "FrozenPairBridge.lean",
    "ReplayOccurrence.lean",
    "ActualSectionAdapter.lean",
)
EXPECTED_REPORTS: Final = {
    "FrozenPairBridge.lean": frozenset(
        {
            "AdmissionSignShadow.FrozenPairBridge.frozen_pair_observed_facts",
            "AdmissionSignShadow.FrozenPairBridge.chosen_pair_equivalence",
            "AdmissionSignShadow.FrozenPairBridge.erased_readout_cannot_separate",
            "AdmissionSignShadow.FrozenPairBridge.frozen_pair_supports_both_character_extensions",
        }
    ),
    "ReplayOccurrence.lean": frozenset(
        {
            "AdmissionSignShadow.ReplayOccurrence.occurrenceReplay_valid",
            "AdmissionSignShadow.ReplayOccurrence.occurrenceReplay_count",
            "AdmissionSignShadow.ReplayOccurrence.forget_occurrenceReplay_commutes",
            "AdmissionSignShadow.ReplayOccurrence.occurrenceValid_renameIds",
            "AdmissionSignShadow.ReplayOccurrence.duplicate_admission_endpoint_collision",
            "AdmissionSignShadow.ReplayOccurrence.endpoint_does_not_determine_occurrence_count",
            "AdmissionSignShadow.ReplayOccurrence.endpoint_does_not_determine_occurrence_history",
            "AdmissionSignShadow.ReplayOccurrence.additive_laws_do_not_select_integer_unit",
            "AdmissionSignShadow.ReplayOccurrence.unit_calibration_is_conditional",
        }
    ),
    "ActualSectionAdapter.lean": frozenset(
        {
            "AdmissionSignShadow.ActualSectionAdapter.Kernel.toSec_isNatural",
            "AdmissionSignShadow.ActualSectionAdapter.no_kernel_of_no_actual_section",
            "AdmissionSignShadow.ActualSectionAdapter.report_section_does_not_determine_actual_section",
            "AdmissionSignShadow.ActualSectionAdapter.fixed_point_free_family_has_no_kernel",
        }
    ),
}


def repository_root(start: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def frozen_archive(repo: Path) -> bytes:
    result = subprocess.run(
        ["git", "archive", "--format=tar", FROZEN_COMMIT, "lean4"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    return result.stdout


def verify_frozen_sources(repo: Path, manifest: dict[str, object]) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        raise ValueError("SOURCE_MANIFEST.json sources must be a list")
    for raw in sources:
        if not isinstance(raw, dict) or raw.get("revision") != "frozen":
            continue
        path = raw.get("path")
        expected_blob = raw.get("git_blob")
        expected_sha256 = raw.get("sha256")
        if not all(isinstance(value, str) for value in (path, expected_blob, expected_sha256)):
            raise ValueError("frozen source manifest row is malformed")
        blob = subprocess.run(
            ["git", "rev-parse", f"{FROZEN_COMMIT}:{path}"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        payload = subprocess.run(
            ["git", "show", f"{FROZEN_COMMIT}:{path}"],
            cwd=repo,
            check=True,
            capture_output=True,
        ).stdout
        digest = hashlib.sha256(payload).hexdigest()
        checks.append(
            {
                "path": path,
                "git_blob": blob,
                "sha256": digest,
                "ok": blob == expected_blob and digest == expected_sha256,
            }
        )
    return checks


def exact_source_identity(repo: Path, manifest: dict[str, object]) -> dict[str, object]:
    observed_tree = subprocess.run(
        ["git", "rev-parse", f"{FROZEN_COMMIT}^{{tree}}"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    expected_tree = manifest.get("frozen_tree")
    if observed_tree != expected_tree:
        raise ValueError("frozen tree differs from SOURCE_MANIFEST.json")
    return {
        "commit": FROZEN_COMMIT,
        "tree": observed_tree,
        "scope": "entire exact frozen lean4 tree",
    }


def persistent_exact_copy_matches(
    repo: Path, frozen_checks: list[dict[str, object]]
) -> dict[str, list[str]]:
    population = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            "research/admission_sign_shadow",
        ],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    frozen_digests = {str(check["sha256"]) for check in frozen_checks}
    matches: list[str] = []
    for relative in population:
        path = repo / relative
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() in frozen_digests:
            matches.append(relative.replace("\\", "/"))
    apparatus = [
        path for path in matches
        if path == "research/admission_sign_shadow/lean/lean-toolchain"
    ]
    return {
        "permitted_toolchain_text": sorted(apparatus),
        "frozen_source_matches": sorted(set(matches) - set(apparatus)),
    }


def extract_archive(payload: bytes, destination: Path) -> None:
    with tarfile.open(fileobj=BytesIO(payload), mode="r:") as archive:
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise ValueError(f"archive member escapes destination: {member.name}")
        archive.extractall(destination, filter="data")


def parse_axiom_reports(output: str) -> list[dict[str, object]]:
    reports: list[dict[str, object]] = []
    for match in AXIOM_REPORT.finditer(output):
        raw = match.group("axioms")
        axioms = [] if raw is None else sorted(
            item.strip() for item in raw.split(",") if item.strip()
        )
        reports.append(
            {
                "declaration": match.group("name"),
                "axioms": axioms,
                "allowed": set(axioms) <= ALLOWED_AXIOMS,
            }
        )
    return reports


def audit_axiom_reports(
    module_name: str, reports: list[dict[str, object]]
) -> tuple[bool, bool]:
    names = [str(report["declaration"]) for report in reports]
    expected = EXPECTED_REPORTS.get(module_name, frozenset())
    population_exact = len(names) == len(set(names)) and set(names) == expected
    allowed = population_exact and all(bool(report["allowed"]) for report in reports)
    return population_exact, allowed


def compile_modules(package: Path, modules: list[Path]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for module in modules:
        target = module.with_suffix("").as_posix().replace("/", ".")
        result = subprocess.run(
            ["lake", "build", target],
            cwd=package,
            check=False,
            capture_output=True,
            text=True,
        )
        output = result.stdout + result.stderr
        reports = parse_axiom_reports(output)
        expected = EXPECTED_REPORTS.get(module.name, frozenset())
        population_exact, allowed = audit_axiom_reports(module.name, reports)
        results.append(
            {
                "module": module.as_posix(),
                "sha256": hashlib.sha256((package / module).read_bytes()).hexdigest(),
                "returncode": result.returncode,
                "axiom_reports": reports,
                "axiom_audit_ok": allowed,
                "expected_declarations": sorted(expected),
                "report_population_exact": population_exact,
                "diagnostics": "" if result.returncode == 0 else output,
            }
        )
        if result.returncode or not allowed:
            break
    return results


def run(selected: tuple[str, ...]) -> dict[str, object]:
    research_root = Path(__file__).resolve().parent
    repo = repository_root(research_root)
    manifest = json.loads((research_root / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("frozen_commit") != FROZEN_COMMIT:
        raise ValueError("frozen commit differs from SOURCE_MANIFEST.json")
    source_checks = verify_frozen_sources(repo, manifest)
    if not source_checks or not all(bool(check["ok"]) for check in source_checks):
        raise ValueError("frozen source manifest verification failed")
    frozen_identity = exact_source_identity(repo, manifest)
    source_dir = research_root / "lean" / "AdmissionSignShadow"
    present = [name for name in selected if (source_dir / name).is_file()]
    missing = [name for name in selected if name not in present]
    with tempfile.TemporaryDirectory(prefix="admission-sign-shadow-frozen-") as raw:
        temporary = Path(raw)
        extract_archive(frozen_archive(repo), temporary)
        package = temporary / "lean4"
        lakefile = package / "lakefile.toml"
        with lakefile.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write("\n[[lean_lib]]\nname = \"AdmissionSignShadow\"\n")
        bridge_dir = package / "AdmissionSignShadow"
        bridge_dir.mkdir()
        shutil.copy2(source_dir / "Core.lean", bridge_dir / "Core.lean")
        for name in present:
            shutil.copy2(source_dir / name, bridge_dir / name)
        compiled = compile_modules(
            package,
            [Path("AdmissionSignShadow") / name for name in present],
        )
    return {
        "schema": "frozen-compatibility-receipt-v1",
        "frozen_commit": FROZEN_COMMIT,
        "materialization": "ephemeral_git_archive_removed_on_exit",
        "frozen_input": frozen_identity,
        "persistent_exact_matches": persistent_exact_copy_matches(
            repo, source_checks
        ),
        "source_blob_checks": source_checks,
        "local_source_hashes": {
            "lean/AdmissionSignShadow/Core.lean": hashlib.sha256(
                (source_dir / "Core.lean").read_bytes()
            ).hexdigest(),
            **{
                f"lean/AdmissionSignShadow/{name}": hashlib.sha256(
                    (source_dir / name).read_bytes()
                ).hexdigest()
                for name in present
            },
            "verify_frozen_compatibility.py": hashlib.sha256(
                Path(__file__).read_bytes()
            ).hexdigest(),
        },
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "requested_modules": list(selected),
        "missing_modules": missing,
        "compiled_modules": compiled,
        "success": not missing
        and len(compiled) == len(present)
        and all(
            item["returncode"] == 0 and bool(item["axiom_audit_ok"])
            for item in compiled
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", action="append", dest="modules")
    parser.add_argument("--receipt", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    selected = tuple(args.modules) if args.modules else DEFAULT_MODULES
    receipt = run(selected)
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    receipt_path = args.receipt
    if receipt_path is None and (args.write or args.check):
        receipt_path = Path(__file__).resolve().parent / "receipts" / "frozen_compatibility.json"
    if args.write and receipt_path is not None:
        receipt_path.write_text(rendered, encoding="utf-8", newline="\n")
    if args.check and (
        receipt_path is None
        or not receipt_path.is_file()
        or receipt_path.read_text(encoding="utf-8") != rendered
    ):
        print("FAIL: frozen compatibility receipt differs")
        return 1
    if not args.write and not args.check:
        print(rendered, end="")
    elif receipt["success"]:
        compiled_modules = receipt["compiled_modules"]
        if not isinstance(compiled_modules, list):
            raise TypeError("compiled_modules must be a list")
        print(
            "frozen compatibility receipt clean: "
            f"{len(compiled_modules)} modules"
        )
    return 0 if receipt["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
