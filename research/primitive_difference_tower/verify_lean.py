"""Build and replay the explicit Lean axiom-report target."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Sequence


HERE = Path(__file__).resolve().parent
LEAN_ROOT = HERE / "lean"
AXIOM_REPORT_MODULE = "PrimitiveDifferenceTower.AxiomReport"
AXIOM_REPORT_SOURCE = "PrimitiveDifferenceTower/AxiomReport.lean"
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
)


def _run_lake(arguments: Sequence[str]) -> str:
    process = subprocess.run(
        ["lake", *arguments],
        cwd=LEAN_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    output = process.stdout or ""
    if process.returncode:
        raise RuntimeError(
            f"lake {' '.join(arguments)} failed with exit {process.returncode}:\n{output}"
        )
    return output


def verify_axiom_report() -> list[str]:
    """Compile the report target and force its #print-axioms output."""

    _run_lake(("build", AXIOM_REPORT_MODULE))
    output = _run_lake(("env", "lean", AXIOM_REPORT_SOURCE))
    missing = [name for name in AXIOM_REPORT_DECLARATIONS if name not in output]
    if missing:
        raise ValueError(f"axiom report omitted declarations: {missing}")
    return [
        f"Lean axiom-report target: {AXIOM_REPORT_MODULE}",
        f"Lean #print axioms declarations: {len(AXIOM_REPORT_DECLARATIONS)}",
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
