"""Produce the apartness/indistinguishability artifact deterministically.

Usage: python code/run_apartness.py [--artifacts DIR] [--max-n N]

Writes ``apartness.json``: the exhaustive equivalence verification
(indistinguishability under positive apartness), the three
insufficiency countermodels with minimality checks, the orientation
separation, and the operation-preservation censuses."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.apartness import (
    equivalence_theorem_exhaustive,
    insufficiency_countermodels,
    operation_censuses,
    orientation_separation,
)
from derivation.export import Json, write_json


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path,
                        default=Path("artifacts"))
    parser.add_argument("--max-n", type=int, default=3)
    args = parser.parse_args(argv)
    payload: dict[str, Json] = {
        "bounds": {"equivalence_exhaustive_max_carrier": args.max_n,
                   "census_max_carrier": 4},
        "equivalence_exhaustive":
            equivalence_theorem_exhaustive(args.max_n),
        "insufficiency": insufficiency_countermodels(),
        "orientation": orientation_separation(),
        "operations": operation_censuses(4),
    }
    out_path = args.artifacts / "apartness.json"
    write_json(out_path, payload)
    print(f"equivalence exhaustive to n={args.max_n}: "
          f"{payload['equivalence_exhaustive']}")
    ops = payload["operations"]
    assert isinstance(ops, dict)
    print(f"operation censuses: formula_checked="
          f"{ops['formula_checked']}")
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
