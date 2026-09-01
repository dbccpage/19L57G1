"""Produce the primitive-difference artifact deterministically.

Usage: python code/run_primdiff.py [--artifacts DIR] [--max-n N]
       [--max-k K]

Writes ``primdiff.json``: the candidate implication matrix with
countermodels, the two-element analysis, the observer/orientation report,
the two-element transposition report, the collapse/obstruction
verification, minimal-carrier tables, and the obstruction-profile
frontier countermodel.  All exhaustive over declared finite scopes;
deterministic byte-for-byte.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import write_json
from derivation.primdiff import (
    carrier_table,
    collapse_report,
    frontier_profile_countermodel,
    implication_matrix,
    observer_report,
    transposition_report,
    two_element_report,
)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--max-n", type=int, default=3)
    parser.add_argument("--max-k", type=int, default=6)
    args = parser.parse_args(argv)

    payload = {
        "implication_matrix": implication_matrix(args.max_n),
        "two_element": two_element_report(args.max_n),
        "observer": observer_report(),
        "transposition": transposition_report(),
        "collapse": collapse_report(args.max_n),
        "carrier_table": carrier_table(args.max_k),
        "frontier_profile_countermodel": frontier_profile_countermodel(),
    }
    write_json(args.artifacts / "primdiff.json", payload)  # type: ignore[arg-type]
    matrix = payload["implication_matrix"]
    assert isinstance(matrix, dict)
    implications = matrix["implications"]
    assert isinstance(implications, dict)
    true_count = sum(1 for v in implications.values() if v)
    print(
        f"primdiff: {len(implications)} implication cells, "
        f"{true_count} hold, "
        f"{len(implications) - true_count} refuted with countermodels"
    )
    print(f"artifact written to {args.artifacts / 'primdiff.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
