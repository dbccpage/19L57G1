"""Produce the F5 composite-generator artifact deterministically.

Usage: python code/run_generator.py [--artifacts DIR] [--rounds N]

Writes ``generator.json``: per-strategy bounded trajectories of the
composite (reflective growth + pair-separation closure), the in-bounds
endogenous-cycle exclusion, and the Lean agreement checks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import write_json
from derivation.generator import (
    ROUNDS,
    STRATEGIES,
    exclusion_check,
    lean_agreement,
)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--rounds", type=int, default=ROUNDS)
    args = parser.parse_args(argv)
    exclusion = exclusion_check(args.rounds)
    agreement = lean_agreement(args.rounds)
    payload = {
        "bounds": {
            "rounds_per_branch": args.rounds,
            "observation_depths": [1, 2],
            "strategy_class_size": len(STRATEGIES),
        },
        "exclusion": exclusion,
        "lean_agreement": agreement,
    }
    out_path = args.artifacts / "generator.json"
    write_json(out_path, payload)
    table = exclusion["classification_table"]
    assert isinstance(table, dict)
    print(f"strategies: {len(table)}")
    for name, cls in table.items():
        print(f"  {name}: {cls}")
    print(
        "endogenous cycle found: "
        f"{exclusion['endogenous_cycle_found']}"
    )
    print(f"lean agreement: {all(agreement.values())}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
