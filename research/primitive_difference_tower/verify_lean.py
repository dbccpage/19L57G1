"""Build the explicit Lean axiom-report target and audit what it prints.

The audit parses every ``#print axioms`` line and compares the axiom list of
each declaration with the allowed set, so a declaration that came to depend on
``Classical.choice`` fails even though its name is still present in the
output.  Its reach is exactly the inventory written in ``AxiomReport.lean``,
which must agree with the list below; it says nothing about declarations that
file does not name.  The sealed tree's forbidden-token scan is applied to the
research Lean sources as well.

Nothing in ``.github/workflows`` runs this script.  A pass is a manual receipt
for the sources present when it ran.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Mapping, Sequence


HERE = Path(__file__).resolve().parent
LEAN_ROOT = HERE / "lean"
AXIOM_REPORT_MODULE = "PrimitiveDifferenceTower.AxiomReport"
AXIOM_REPORT_SOURCE = "PrimitiveDifferenceTower/AxiomReport.lean"
BRIDGE_AXIOM_REPORT_DECLARATIONS = (
    "SymmetryObstructionBridge.swap_involutive",
    "SymmetryObstructionBridge.residual_orbit_has_no_fixed_singleton",
    "SymmetryObstructionBridge.residual_not_in_declared_boundary_image",
    "SymmetryObstructionBridge.anchoredChoice_retains_import",
    "SymmetryObstructionBridge.continuation_cases",
    "SymmetryObstructionBridge.nonanchored_continuations_have_no_singleton",
)

AXIOM_REPORT_DECLARATIONS = (
    "PrimitiveDifferenceTower.towerDown_after_towerUp",
    "PrimitiveDifferenceTower.towerUpMorphism_comp_certified",
    "PrimitiveDifferenceTower.down_freshPoint",
    "PrimitiveDifferenceTower.replay_rounds_succ",
    "PrimitiveDifferenceTower.replay_rounds_level",
    "PrimitiveDifferenceTower.replay_rounds_closed",
    "PrimitiveDifferenceTower.no_bool_single_pair_selector",
    "PrimitiveDifferenceTower.raw_bool_single_pair_selector_exists",
    "PrimitiveDifferenceTower.collapsed_source_has_no_witness",
    *BRIDGE_AXIOM_REPORT_DECLARATIONS,
)
ALLOWED_AXIOMS = frozenset({"propext", "Quot.sound"})
FORBIDDEN_TOKENS = (
    r"\bsorry\b",
    r"\badmit\b",
    r"^\s*axiom\s",
    r"\bunsafe\b",
    r"\bpartial\b",
)

# Non-greedy name capture: a primed declaration such as ``foo'`` otherwise
# swallows its own closing quote, which is how the sealed tree once lost four
# reports while its match gate stayed green.
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
    """Map each reported declaration to the exact set of axioms it depends on."""

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
    """Require exactly the expected inventory, each within the allowed axioms."""

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
    """The declarations named by ``#print axioms`` lines, in file order."""

    return tuple(_PRINT_AXIOMS.findall(source))


def research_lean_sources() -> list[Path]:
    return sorted(path for path in LEAN_ROOT.rglob("*.lean") if ".lake" not in path.parts)


def scan_forbidden_tokens(paths: Iterable[Path]) -> list[str]:
    """Plain-text scan over whole files, matching the sealed tree's audit."""

    failures: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_TOKENS:
            for match in re.finditer(pattern, text, flags=re.MULTILINE):
                failures.append(f"{path.name}: forbidden token {match.group(0).strip()!r}")
    return failures


def verify_axiom_report() -> list[str]:
    """Scan the sources, build the report target, and audit its output."""

    inventory = declared_report_inventory(
        (LEAN_ROOT / AXIOM_REPORT_SOURCE).read_text(encoding="utf-8")
    )
    if inventory != AXIOM_REPORT_DECLARATIONS:
        raise ValueError(
            f"{AXIOM_REPORT_SOURCE} names {list(inventory)}, "
            f"but this script expects {list(AXIOM_REPORT_DECLARATIONS)}"
        )
    sources = research_lean_sources()
    failures = scan_forbidden_tokens(sources)
    if failures:
        raise ValueError("forbidden tokens in research Lean sources:\n" + "\n".join(failures))
    _run_lake(("build", AXIOM_REPORT_MODULE))
    output = _run_lake(("env", "lean", AXIOM_REPORT_SOURCE))
    report_lines = check_axiom_reports(parse_axiom_report(output))
    return [
        f"Lean sources scanned for forbidden tokens: {len(sources)}",
        f"Lean axiom-report target: {AXIOM_REPORT_MODULE}",
        f"Lean #print axioms declarations: {len(report_lines)} within {sorted(ALLOWED_AXIOMS)}",
        *report_lines,
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
