"""Build this tree's Lean package and audit the axiom reports it prints.

The package under ``lean/`` compiles the sealed import closure of
``Derivation.PresentationNaturality`` as STAGED copies: this script reads
each pinned module's blob at the manifest's snapshot commit, checks its
SHA-256 against ``SOURCE_MANIFEST.json``, and writes those exact bytes to
``lean/sealed/Derivation/<Module>.lean`` (gitignored), which the
``Derivation`` library of ``lakefile.lean`` compiles inside ``lean/.lake/``.
There is no Lake dependency on ``lean4/``: a path dependency is built in
the dependency's own directory and would write ``lean4/.lake/``, outside
this tree's write root.  The build is thereby bound to the pinned
snapshot, not to whatever ``lean4/`` currently holds.

The write-root boundary is checked, not assumed: the repository-wide
``git status --porcelain --untracked-files=all --ignored=matching`` is
taken before staging and again after the build, and any record that is
new and not under ``research/family_embedding/`` fails the run by name.

It then applies the sealed tree's forbidden-token scan to every ``.lean``
file under ``lean/`` outside ``.lake`` and ``sealed``, parses every
``#print axioms`` line with a non-greedy name capture, requires the set
of reported declarations to equal ``AXIOM_REPORT_DECLARATIONS`` below,
and requires every report to lie within ``{propext, Quot.sound}``.

Nothing in ``.github/workflows`` runs this script.  A pass is a manual
receipt for the sources present when it ran.  AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import re
import subprocess
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import verify_pins


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
WRITE_ROOT = "research/family_embedding/"
LEAN_ROOT = HERE / "lean"
STAGED_ROOT = LEAN_ROOT / "sealed"
AXIOM_REPORT_MODULE = "FamilyEmbedding.AxiomReport"
AXIOM_REPORT_SOURCE = "FamilyEmbedding/AxiomReport.lean"

AXIOM_REPORT_DECLARATIONS: tuple[str, ...] = (
    "FamilyEmbedding.mapPair_along",
    "FamilyEmbedding.isoAlong_rfl",
    "FamilyEmbedding.embedIso_rfl",
    "FamilyEmbedding.hnatural_of_natural",
    "FamilyEmbedding.natural_of_hnatural",
    "FamilyEmbedding.natural_section_iff_embed",
    "FamilyEmbedding.one_object_recovers",
    "FamilyEmbedding.autoFamily_hom_inhabited",
    "FamilyEmbedding.obstructed_loopA_is_neg",
    "FamilyEmbedding.obstructed_hom_inhabited",
    "FamilyEmbedding.obstructed_no_section",
    "FamilyEmbedding.obstructed_H_no_section",
    "FamilyEmbedding.clean_hom_inhabited",
    "FamilyEmbedding.clean_natural",
    "FamilyEmbedding.clean_has_section",
    "FamilyEmbedding.clean_H_has_section",
)

ALLOWED_AXIOMS = frozenset({"propext", "Quot.sound"})
FORBIDDEN_TOKENS = (
    r"\bsorry\b",
    r"\badmit\b",
    r"^\s*axiom\s",
    r"\bunsafe\b",
    r"\bpartial\b",
)

_REPORT_LINE = re.compile(
    r"^'(.+?)' (?:depends on axioms: \[(.*?)\]|does not depend on any axioms)\s*$",
    re.MULTILINE,
)
_PRINT_AXIOMS = re.compile(r"^#print axioms ([A-Za-z_][A-Za-z0-9_.']*)\s*$", re.MULTILINE)


def _run_lake(arguments: Sequence[str]) -> str:
    process = subprocess.run(
        ["lake", *arguments],
        cwd=LEAN_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
    )
    output = process.stdout or ""
    if process.returncode:
        raise RuntimeError(
            f"lake {' '.join(arguments)} failed with exit {process.returncode}:\n{output}"
        )
    return output


def parse_axiom_report(output: str) -> dict[str, frozenset[str]]:
    reports: dict[str, frozenset[str]] = {}
    for match in _REPORT_LINE.finditer(output):
        name = match.group(1)
        raw = match.group(2) or ""
        axioms = frozenset(axiom.strip() for axiom in raw.split(",") if axiom.strip())
        if name in reports:
            raise ValueError(f"duplicate axiom report: {name}")
        reports[name] = axioms
    return reports


def check_axiom_reports(
    reports: Mapping[str, frozenset[str]],
    expected: Sequence[str] = AXIOM_REPORT_DECLARATIONS,
    allowed: frozenset[str] = ALLOWED_AXIOMS,
) -> list[str]:
    missing = sorted(set(expected) - set(reports))
    unexpected = sorted(set(reports) - set(expected))
    if missing or unexpected:
        raise ValueError(
            f"axiom report inventory differs: missing {missing}, unexpected {unexpected}"
        )
    lines: list[str] = []
    for name in expected:
        extra = sorted(reports[name] - allowed)
        if extra:
            raise ValueError(f"{name} depends on disallowed axioms: {extra}")
        lines.append(f"{name}: {sorted(reports[name]) or 'no axioms'}")
    return lines


def declared_report_inventory(source: str) -> tuple[str, ...]:
    return tuple(_PRINT_AXIOMS.findall(source))


def research_lean_sources() -> list[Path]:
    """This tree's own Lean sources: not the build cache, not the staged copies."""

    return sorted(
        path
        for path in LEAN_ROOT.rglob("*.lean")
        if ".lake" not in path.parts and "sealed" not in path.parts
    )


def scan_forbidden_tokens(paths: Iterable[Path]) -> list[str]:
    failures: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_TOKENS:
            for match in re.finditer(pattern, text, flags=re.MULTILINE):
                failures.append(f"{path.name}: forbidden token {match.group(0).strip()!r}")
    return failures


def stage_sealed_sources(manifest: Mapping[str, object] | None = None) -> list[str]:
    """Write the pinned snapshot blob of every manifest module under ``lean/sealed``."""

    if manifest is None:
        manifest = verify_pins.read_manifest()
    block = manifest.get("source_snapshot")
    if not isinstance(block, dict):
        raise ValueError("manifest must carry a 'source_snapshot' object")
    snapshot = block.get("commit")
    if not isinstance(snapshot, str) or not re.fullmatch(r"[0-9a-f]{40}", snapshot):
        raise ValueError("manifest snapshot commit must be an exact 40-digit lowercase hex id")
    modules = manifest.get("modules")
    if not isinstance(modules, list) or not modules:
        raise ValueError("manifest must list modules")
    lines: list[str] = []
    for item in modules:
        if not isinstance(item, dict):
            raise ValueError("each module entry must be an object")
        module = item.get("module")
        wanted = item.get("sha256")
        if not isinstance(module, str) or not isinstance(wanted, str):
            raise ValueError("each module entry needs 'module' and 'sha256'")
        repo_path = verify_pins.module_path(module)
        blob = verify_pins._git_bytes("show", f"{snapshot}:{repo_path}")
        actual = verify_pins._sha256(blob)
        if actual != wanted:
            raise ValueError(
                f"staged module {module} at {snapshot} hashes to {actual}, manifest pins {wanted}"
            )
        target = (STAGED_ROOT / module.replace(".", "/")).with_suffix(".lean").resolve()
        if not target.is_relative_to(LEAN_ROOT.resolve()):
            raise ValueError(f"staged path escapes the tree: {module}")
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != blob:
            target.write_bytes(blob)
        lines.append(f"staged: {module} at {snapshot[:12]} {actual}")
    return lines


def repository_records() -> frozenset[str]:
    output = verify_pins._git_bytes(
        "status", "--porcelain=v1", "--untracked-files=all", "--ignored=matching"
    ).decode("utf-8")
    return frozenset(line for line in output.splitlines() if line.strip())


def writes_outside_root(
    before: Iterable[str], after: Iterable[str], root: str = WRITE_ROOT
) -> list[str]:
    """Records new in ``after`` whose path is not under ``root``; pure."""

    violations: list[str] = []
    for line in sorted(set(after) - set(before)):
        if len(line) < 4 or line[2] != " ":
            raise ValueError(f"malformed git status record: {line!r}")
        paths = [part.strip().strip('"') for part in line[3:].split(" -> ")]
        if any(not path.startswith(root) for path in paths):
            violations.append(line)
    return violations


def verify_axiom_report() -> list[str]:
    inventory = declared_report_inventory(
        (LEAN_ROOT / AXIOM_REPORT_SOURCE).read_text(encoding="utf-8")
    )
    if inventory != AXIOM_REPORT_DECLARATIONS:
        raise ValueError(
            f"{AXIOM_REPORT_SOURCE} names {list(inventory)}, "
            f"but this script expects {list(AXIOM_REPORT_DECLARATIONS)}"
        )
    sources = research_lean_sources()
    if not sources:
        raise ValueError(f"no Lean sources found under {LEAN_ROOT}")
    failures = scan_forbidden_tokens(sources)
    if failures:
        raise ValueError("forbidden tokens in research Lean sources:\n" + "\n".join(failures))
    before = repository_records()
    staged = stage_sealed_sources()
    _run_lake(("build",))
    output = _run_lake(("env", "lean", AXIOM_REPORT_SOURCE))
    escaped = writes_outside_root(before, repository_records())
    if escaped:
        raise ValueError(
            f"the Lean build wrote outside the write root {WRITE_ROOT}:\n  "
            + "\n  ".join(escaped)
        )
    report_lines = check_axiom_reports(parse_axiom_report(output))
    return [
        f"Lean sources scanned for forbidden tokens: {len(sources)}",
        *staged,
        "Lean package built: lake build (exit 0)",
        f"write root respected: no new file outside {WRITE_ROOT}",
        f"Lean axiom-report target: {AXIOM_REPORT_MODULE}",
        f"Lean #print axioms declarations: {len(report_lines)} within {sorted(ALLOWED_AXIOMS)}",
        *report_lines,
        "manual receipt: nothing in .github/workflows runs this script",
    ]


def main() -> int:
    try:
        print("\n".join(verify_axiom_report()))
    except (OSError, RuntimeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
