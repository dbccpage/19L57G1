"""Build this tree's Lean package and audit the axiom reports it prints.

Stages pinned snapshot blobs into `lean/sealed/` (gitignored) and compiles
them here.  Does not path-require `lean4/` or `research/unboundedness/lean`.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import hashlib
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Iterable, Mapping, Sequence

import verify_pins

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
WRITE_ROOT = "research/diagonal_identity/"
LEAN_ROOT = HERE / "lean"
STAGED_ROOT = LEAN_ROOT / "sealed"
AXIOM_REPORT_MODULE = "DiagonalIdentity.AxiomReport"
AXIOM_REPORT_SOURCE = "DiagonalIdentity/AxiomReport.lean"

STAGED_SOURCES: tuple[tuple[str, str], ...] = (
    ("lean4/Derivation/PrimDiff.lean", "Derivation/PrimDiff.lean"),
    ("research/coherent_process_limits/lean/Limits.lean", "Limits.lean"),
)

AXIOM_REPORT_DECLARATIONS: tuple[str, ...] = (
    "DiagonalIdentity.Covering.diagonal_bool",
    "DiagonalIdentity.Covering.flipFin_ne",
    "DiagonalIdentity.Covering.diagSeq_diff_at",
    "DiagonalIdentity.Covering.seq_uncountable",
    "DiagonalIdentity.Covering.diagThread_diff_seq",
    "DiagonalIdentity.Covering.thread_uncountable",
    "DiagonalIdentity.Covering.not_surjective_nat_to_thread",
    "DiagonalIdentity.Combinator.diagBool_is_diagFlip",
    "DiagonalIdentity.Combinator.diagSeq_is_diagFlip",
    "DiagonalIdentity.Combinator.diagFlip_ne_row",
    "DiagonalIdentity.Collapse.d2_constant_obstructs",
    "DiagonalIdentity.Collapse.identifying_push_not_irrefl",
    "DiagonalIdentity.Collapse.identifying_push_self_loop",
    "DiagonalIdentity.Split.collapse_yes_covering_no",
    "DiagonalIdentity.Split.family_miss_and_identifying_push",
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
    return sorted(
        path
        for path in LEAN_ROOT.rglob("*.lean")
        if ".lake" not in path.parts and "sealed" not in path.parts
    )


def stage_sources(manifest: Mapping[str, object] | None = None) -> list[str]:
    if manifest is None:
        manifest = verify_pins.read_manifest()
    snapshot_block = manifest.get("source_snapshot")
    if not isinstance(snapshot_block, dict):
        raise ValueError("manifest must carry a 'source_snapshot' object")
    snapshot = snapshot_block.get("commit")
    if not isinstance(snapshot, str) or not re.fullmatch(r"[0-9a-f]{40}", snapshot):
        raise ValueError("manifest snapshot commit must be an exact 40-digit lowercase hex id")
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        raise ValueError("manifest must list sources")
    pins: dict[str, str] = {}
    for item in sources:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            pins[item["path"]] = str(item.get("sha256", ""))
    lines: list[str] = []
    for repo_path, staged_relative in STAGED_SOURCES:
        wanted = pins.get(repo_path)
        if wanted is None:
            raise ValueError(f"staged source is not pinned in the manifest: {repo_path}")
        blob = verify_pins._git_bytes("show", f"{snapshot}:{repo_path}")
        actual = hashlib.sha256(blob).hexdigest().upper()
        if actual != wanted:
            raise ValueError(
                f"staged source {repo_path} at {snapshot} hashes to {actual}, "
                f"manifest pins {wanted}"
            )
        target = (STAGED_ROOT / PurePosixPath(staged_relative)).resolve()
        if not target.is_relative_to(LEAN_ROOT.resolve()):
            raise ValueError(f"staged path escapes the tree: {staged_relative}")
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != blob:
            target.write_bytes(blob)
        lines.append(
            f"staged: {repo_path} at {snapshot[:12]} -> lean/sealed/{staged_relative} {actual}"
        )
    return lines


def repository_records() -> frozenset[str]:
    output = verify_pins._git_bytes(
        "status", "--porcelain=v1", "--untracked-files=all", "--ignored=matching"
    ).decode("utf-8")
    return frozenset(line for line in output.splitlines() if line.strip())


def writes_outside_root(
    before: Iterable[str], after: Iterable[str], root: str = WRITE_ROOT
) -> list[str]:
    new = sorted(set(after) - set(before))
    violations: list[str] = []
    for line in new:
        if len(line) < 4 or line[2] != " ":
            raise ValueError(f"malformed git status record: {line!r}")
        paths = [part.strip().strip('"') for part in line[3:].split(" -> ")]
        if any(not path.startswith(root) for path in paths):
            violations.append(line)
    return violations


def scan_forbidden_tokens(paths: Iterable[Path]) -> list[str]:
    failures: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_TOKENS:
            for match in re.finditer(pattern, text, flags=re.MULTILINE):
                failures.append(f"{path.name}: forbidden token {match.group(0).strip()!r}")
    return failures


def lakefile_has_no_require(text: str) -> bool:
    """Refuse a Lake `require` command; comments may mention the word."""
    for line in text.splitlines():
        stripped = line.split("--", 1)[0].strip()
        if stripped == "require" or stripped.startswith("require "):
            return False
    return True


def verify_axiom_report() -> list[str]:
    inventory = declared_report_inventory(
        (LEAN_ROOT / AXIOM_REPORT_SOURCE).read_text(encoding="utf-8")
    )
    if inventory != AXIOM_REPORT_DECLARATIONS:
        raise ValueError(
            f"{AXIOM_REPORT_SOURCE} names {list(inventory)}, "
            f"but this script expects {list(AXIOM_REPORT_DECLARATIONS)}"
        )
    lakefile = (LEAN_ROOT / "lakefile.lean").read_text(encoding="utf-8")
    if not lakefile_has_no_require(lakefile):
        raise ValueError("lakefile.lean must not declare a Lake require")
    sources = research_lean_sources()
    if not sources:
        raise ValueError(f"no Lean sources found under {LEAN_ROOT}")
    failures = scan_forbidden_tokens(sources)
    if failures:
        raise ValueError("forbidden tokens in research Lean sources:\n" + "\n".join(failures))
    before = repository_records()
    staged = stage_sources()
    _run_lake(("build",))
    output = _run_lake(("env", "lean", AXIOM_REPORT_SOURCE))
    escaped = writes_outside_root(before, repository_records())
    if escaped:
        raise ValueError(
            "the Lean build wrote outside the write root "
            f"{WRITE_ROOT}:\n  " + "\n  ".join(escaped)
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
