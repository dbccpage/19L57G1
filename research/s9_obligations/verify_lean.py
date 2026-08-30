"""Build this tree's Lean package and audit the axiom reports it prints.

The package under ``lean/`` requires the sealed package as a read-only
dependency and adds no module under ``lean4/Derivation/`` (PROMPT.md step
27).  This script builds it with ``lake build``, applies the sealed tree's
forbidden-token scan to every ``.lean`` file under ``lean/`` outside
``.lake``, parses every ``#print axioms`` line with a non-greedy name
capture, requires the set of reported declarations to equal the inventory
``AXIOM_REPORT_DECLARATIONS`` declared below, and requires every report to
lie within ``{propext, Quot.sound}`` (PROMPT.md step 28).

The inventory starts empty and the Lean stage appends to it, one name per
exported theorem, in the same order as ``S9Obligations/AxiomReport.lean``.
An empty inventory with an empty report set passes and is a receipt for
nothing; an empty inventory with a non-empty report set fails, because a
report this script does not list is a declaration nobody audited.

Nothing in ``.github/workflows`` runs this script.  A pass is a manual
receipt for the sources present when it ran (PROMPT.md step 29).
AuthorityEffect: None.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Mapping, Sequence


HERE = Path(__file__).resolve().parent
LEAN_ROOT = HERE / "lean"
AXIOM_REPORT_MODULE = "S9Obligations.AxiomReport"
AXIOM_REPORT_SOURCE = "S9Obligations/AxiomReport.lean"

# Appended per part by the Lean stage.  Initially empty on purpose.
AXIOM_REPORT_DECLARATIONS: tuple[str, ...] = (
    # P1 (S9.1, the axiom lattice): S9Obligations/AxiomLattice.lean, in file order.
    "S9Obligations.AxiomLattice.irreflClause_holds_iff",
    "S9Obligations.AxiomLattice.atom_head_clause_holds_on_full",
    "S9Obligations.AxiomLattice.non_falsum_clause_set_admits_selfdiff",
    "S9Obligations.AxiomLattice.falsum_clause_entails_irrefl",
    "S9Obligations.AxiomLattice.has_falsum_clause_entails_irrefl",
    "S9Obligations.AxiomLattice.transfers_iff_entails_irrefl",
    "S9Obligations.AxiomLattice.transfers_iff_has_falsum_clause",
    "S9Obligations.AxiomLattice.atom_head_clause_does_not_transfer",
    "S9Obligations.AxiomLattice.entails_irrefl_iff_has_falsum_clause",
    "S9Obligations.AxiomLattice.transfers_above_point_iff",
    "S9Obligations.AxiomLattice.reflexivePointForcesSingleton_holds_iff",
    "S9Obligations.AxiomLattice.reflexive_point_forces_singleton_irrefl_of_two_points",
    "S9Obligations.AxiomLattice.reflexive_point_forces_singleton_transfers_above_point",
    "S9Obligations.AxiomLattice.reflexive_point_forces_singleton_admits_selfdiff",
    "S9Obligations.AxiomLattice.reflexive_point_forces_singleton_not_entails_irrefl",
    "S9Obligations.AxiomLattice.reflexive_point_forces_singleton_f3_countermodel_above_point",
    "S9Obligations.AxiomLattice.pure_non_falsum_clause_set_holds_on_full",
    "S9Obligations.AxiomLattice.pure_one_point_full_implies_two_point_full",
    "S9Obligations.AxiomLattice.pure_transfer_above_point_iff_has_falsum_clause",
    "S9Obligations.AxiomLattice.pure_transfers_above_point_iff_entails_irrefl",
    "S9Obligations.AxiomLattice.reflexivePointForcesSingleton_holds_iff_of_decidableEq",
    "S9Obligations.AxiomLattice.transfers_above_point_of_entails_reflexive_point_forces_singleton",
    "S9Obligations.AxiomLattice.transfers_above_point_imp_entails_reflexive_point_forces_singleton",
    # P2 (S9.2, morphism classes): S9Obligations/MorphismClasses.lean, in file order.
    "S9Obligations.MorphismClasses.not_both",
    "S9Obligations.MorphismClasses.injective_of_ne",
    "S9Obligations.MorphismClasses.two_element_pointed_map_unique",
    "S9Obligations.MorphismClasses.D2_initial_P_E",
    "S9Obligations.MorphismClasses.FULL2_initial_P_NE",
    "S9Obligations.MorphismClasses.no_injection_into_point",
    "S9Obligations.MorphismClasses.no_surjection_onto_three",
    "S9Obligations.MorphismClasses.two_copies_not_unique",
    "S9Obligations.MorphismClasses.diagonal_candidate_not_pointed_into_D2",
    "S9Obligations.MorphismClasses.extra_edge_not_into_D2",
    "S9Obligations.MorphismClasses.non_edge_not_into_point",
    "S9Obligations.MorphismClasses.pointed_map_injective_of_irrefl",
    "S9Obligations.MorphismClasses.two_element_initial_P_I_irrefl",
    "S9Obligations.MorphismClasses.D2_initial_P_E_I_irrefl",
    "S9Obligations.MorphismClasses.S2_initial_P_NE_irrefl",
    "S9Obligations.MorphismClasses.S2_initial_P_NE_I_irrefl",
    "S9Obligations.MorphismClasses.S2_not_P_E_into_D2",
    "S9Obligations.MorphismClasses.D2_not_P_NE_into_S2",
    "S9Obligations.MorphismClasses.no_surjection_onto_three_irrefl",
    "S9Obligations.MorphismClasses.two_irrefl_copies_not_unique",
    "S9Obligations.MorphismClasses.initial_P_iff",
    "S9Obligations.MorphismClasses.initial_P_E_iff",
    "S9Obligations.MorphismClasses.initial_P_NE_iff",
    "S9Obligations.MorphismClasses.not_initial_P_E_NE",
    "S9Obligations.MorphismClasses.admits_primary_iff",
    "S9Obligations.MorphismClasses.admits_primary_exactly",
    "S9Obligations.MorphismClasses.admits_secondary_iff",
    "S9Obligations.MorphismClasses.admits_secondary_exactly",
    # P3 (S9.3, witness types): S9Obligations/WitnessTypes.lean, in file order.
    "S9Obligations.WitnessTypes.cardTwo",
    "S9Obligations.WitnessTypes.cardPosIff",
    "S9Obligations.WitnessTypes.v1ListLength",
    "S9Obligations.WitnessTypes.v2AnonListLength",
    "S9Obligations.WitnessTypes.v1V2AnonListLength",
    "S9Obligations.WitnessTypes.v1V2AnonListNodup",
    "S9Obligations.WitnessTypes.v1ListNodup",
    "S9Obligations.WitnessTypes.v2AnonListNodup",
    "S9Obligations.WitnessTypes.v1ListReadsCountsOnly",
    "S9Obligations.WitnessTypes.sharedTransport",
    "S9Obligations.WitnessTypes.someSharedTransport",
    "S9Obligations.WitnessTypes.twoSharedTransport",
    "S9Obligations.WitnessTypes.S9_3_sep_presence_equal",
    "S9Obligations.WitnessTypes.S9_3_sep_count_equal",
    "S9Obligations.WitnessTypes.S9_3_sep_V1_indistinguishable",
    "S9Obligations.WitnessTypes.S9_3_sep_V2_ANON_separates",
    "S9Obligations.WitnessTypes.sepExactlyOneV2AnonQuestionDiffers",
    "S9Obligations.WitnessTypes.S9_3_sep_not_isomorphic",
    "S9Obligations.WitnessTypes.sepRawDataDiffer",
    "S9Obligations.WitnessTypes.sepPresenceS2",
    "S9Obligations.WitnessTypes.sepPresenceIrrefl",
    "S9Obligations.WitnessTypes.S9_3_inv_V1_V2_ANON_indistinguishable",
    "S9Obligations.WitnessTypes.S9_3_inv_count_equal",
    "S9Obligations.WitnessTypes.invSharedCounts",
    "S9Obligations.WitnessTypes.invTwoShared",
    "S9Obligations.WitnessTypes.S9_3_inv_not_isomorphic",
    "S9Obligations.WitnessTypes.invRawDataDiffer",
    "S9Obligations.WitnessTypes.invPresenceS2",
    "S9Obligations.WitnessTypes.invPresenceIrrefl",
    "S9Obligations.WitnessTypes.evalReadsCounts",
    "S9Obligations.WitnessTypes.v1ListReadsCounts",
    "S9Obligations.WitnessTypes.sepV1IndistinguishableViaCounts",
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
    """Require exactly the expected inventory, each within the allowed axioms.

    With an empty ``expected`` this passes only when ``reports`` is empty
    too: a printed report that is not listed is an unaudited declaration.
    """

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
    """Scan the sources, build the package, and audit what the report file prints."""

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
    _run_lake(("build",))
    output = _run_lake(("env", "lean", AXIOM_REPORT_SOURCE))
    report_lines = check_axiom_reports(parse_axiom_report(output))
    lines = [
        f"Lean sources scanned for forbidden tokens: {len(sources)}",
        "Lean package built: lake build (exit 0)",
        f"Lean axiom-report target: {AXIOM_REPORT_MODULE}",
        f"Lean #print axioms declarations: {len(report_lines)} within {sorted(ALLOWED_AXIOMS)}",
        *report_lines,
    ]
    if not report_lines:
        lines.append(
            "no declaration reported yet: a build receipt, not an axiom receipt"
        )
    lines.append("manual receipt: nothing in .github/workflows runs this script")
    return lines


def main() -> int:
    try:
        print("\n".join(verify_axiom_report()))
    except (OSError, RuntimeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
