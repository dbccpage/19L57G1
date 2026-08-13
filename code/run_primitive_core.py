"""Produce the primitive-difference candidate-lattice artifacts
deterministically.

Usage: python code/run_primitive_core.py [--artifacts DIR]

Writes:
  primitive_candidates.json          declared bounds, candidate
                                     extents, the two-element
                                     classification, the locatedness
                                     note, presentation branching
                                     (finite mirror)
  primitive_implication_matrix.json  all 72 ordered candidate cells:
                                     resolved status, raw search
                                     status, key-minimal witnesses,
                                     Lean tags; the computed table is
                                     verified against the expected
                                     table (mismatch raises)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import write_json
from derivation.primitive_core import (
    candidates_payload,
    matrix_report,
    scan_settings,
)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    args = parser.parse_args(argv)
    scan = scan_settings()
    candidates = candidates_payload(scan)
    matrix = matrix_report(scan)
    out = args.artifacts
    write_json(out / "primitive_candidates.json", candidates)  # type: ignore[arg-type]
    write_json(out / "primitive_implication_matrix.json", matrix)  # type: ignore[arg-type]
    status_counts = matrix["status_counts"]
    assert isinstance(status_counts, dict)
    print(
        f"primitive_core: {scan.total} settings enumerated; "
        + ", ".join(f"{k}={v}" for k, v in sorted(status_counts.items()))
    )
    print(
        "expected matrix equals computed matrix: "
        f"{matrix['expected_equals_computed']}"
    )
    print(f"artifacts written to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
