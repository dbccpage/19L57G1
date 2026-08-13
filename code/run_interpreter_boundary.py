"""Produce the interpreter-boundary artifact deterministically.

Usage: python code/run_interpreter_boundary.py [--artifacts DIR]

Writes ``primitive_interpreter.json``: the 64-member code family with
its pairwise behavioral distinctness on the declared basis, the
exhaustive diagonal check (the mirror of ``tower_persists`` at the
sealed family), the typed-refusal top's verdict, and the boundary
setting (65-occurrence carrier, witnessed pair, candidate verdicts A
and F) with the exported terminal tags and their Lean evidence.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import write_json
from derivation.interpreter_boundary import interpreter_report


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    args = parser.parse_args(argv)
    payload = interpreter_report()
    out_path = args.artifacts / "primitive_interpreter.json"
    write_json(out_path, payload)
    print(f"family: size={payload['family_size']} "
          f"distinct_on_basis={payload['behaviorally_distinct_on_basis']} "
          f"self_description={payload['self_description_on_basis']}")
    print(f"diagonal: misses_all={payload['diagonal_misses_all']} "
          f"top={payload['partial_top']}")
    boundary = payload["boundary_setting"]
    assert isinstance(boundary, dict)
    print(f"boundary: candidates={boundary['candidates']} "
          f"collapse_obstructed={boundary['collapse_obstructed']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
