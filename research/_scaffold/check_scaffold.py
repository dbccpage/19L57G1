"""Drift lint for the copied research-tree scaffold.

AuthorityEffect: None.  Not a sealed gate; a repository-wide check that the two
recurring scaffold bugs have not been copied into any `research/<tree>/`.  Run
from the repository root: `python research/_scaffold/check_scaffold.py`.

The research trees are deliberately self-contained: each keeps its own
`check_coverage.py` and `run.py` rather than importing a shared module, so the
same bug can be pasted into a new tree verbatim.  This lint keeps those copies
in sync with the canonical `research/_scaffold/` versions on the two defects
that have actually recurred, at two severities:

  ERROR (blocks) -- COVERAGE_LEAK by substring.  The recent coverage gate
    matched omit directories with `part in path` (a substring test), so a
    module under a directory like `clean/` was falsely flagged.  The marker of
    the buggy generation is the module-level name `OMIT_PARTS`; the fixed
    version uses `OMIT_DIRS` + a path-component `_directories()` helper.  This
    is a correctness bug and must never ship in a new tree.  (Older trees use a
    different, component-correct gate with no `OMIT_PARTS`; those are clean.)

  WARNING (reported, non-fatal) -- double custody scan.  `run.py`'s
    `receipt_bytes()` calls the expensive `verify_sources()` twice, once before
    and once after a pure record computation that writes no files, so the
    second scan is redundant.  This is efficiency only, and it CANNOT be
    retrofitted freely: several older trees pin each other's whole `.py` tree at
    a baseline commit (e.g. `record_reading` pins `setting_translation`,
    `represented_execution` and `coherent_process_limits`), so editing one
    tree's `run.py` breaks a consumer's custody and cascades repins.  A NEW tree
    should drop the second scan at creation, before any consumer pins it; an
    existing pinned tree is left until its family is deliberately repinned.

The lint prints every offender by path.  It exits non-zero only if an ERROR is
present, so a newly copied tree cannot re-introduce the correctness bug
unnoticed, while the known double-scans stay visible without wedging the check.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research"
SCAFFOLD = "_scaffold"


def _tree_dirs() -> list[Path]:
    return sorted(
        p for p in RESEARCH.iterdir()
        if p.is_dir() and p.name != SCAFFOLD and not p.name.startswith(".")
    )


def coverage_errors() -> list[str]:
    """Trees whose check_coverage.py carries the substring-leak generation."""
    out: list[str] = []
    for tree in _tree_dirs():
        gate = tree / "check_coverage.py"
        if not gate.is_file():
            continue
        text = gate.read_text(encoding="utf-8")
        if "OMIT_PARTS" in text and "_directories" not in text:
            out.append(f"{gate.relative_to(ROOT).as_posix()}: substring COVERAGE_LEAK (OMIT_PARTS)")
    return out


def run_warnings() -> list[str]:
    """Trees whose run.py scans custody twice per receipt."""
    out: list[str] = []
    for tree in _tree_dirs():
        runner = tree / "run.py"
        if not runner.is_file():
            continue
        n = runner.read_text(encoding="utf-8").count("verify_sources()")
        if n > 1:
            out.append(f"{runner.relative_to(ROOT).as_posix()}: {n} verify_sources() calls (double custody scan)")
    return out


def main() -> int:
    errors = coverage_errors()
    warnings = run_warnings()
    if errors:
        print("ERROR: substring COVERAGE_LEAK in a new tree (must fix):")
        for line in errors:
            print(f"  {line}")
    if warnings:
        print("WARNING: double custody scan (efficiency; fix in a NEW tree before it is pinned):")
        for line in warnings:
            print(f"  {line}")
    if errors:
        print(f"\n{len(errors)} error(s); sync with research/_scaffold/check_coverage.py.")
        return 1
    if warnings:
        print(f"\nscaffold clean of correctness drift; {len(warnings)} known double-scan warning(s).")
        return 0
    print("scaffold clean: no substring COVERAGE_LEAK and no double custody scan in any research tree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
