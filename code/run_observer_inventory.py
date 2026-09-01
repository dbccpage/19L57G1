"""Produce the nine-slot inventory artifact deterministically.

Usage: python code/run_observer_inventory.py [--artifacts DIR]

Writes ``observer_inventory.json``: slot bindings on the two-element
fragment, the irreflexive census, witness-as-data checks, the two
reversal maps, the two defect readings, and the two residuals.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import Json, write_json
from derivation.observer_inventory import inventory_report


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--artifacts", type=Path, default=Path("artifacts")
    )
    args = parser.parse_args(argv)
    payload: dict[str, Json] = inventory_report()
    out_path = args.artifacts / "observer_inventory.json"
    write_json(out_path, payload)
    census = payload["irrefl_census"]
    assert isinstance(census, dict)
    print(
        f"observer_inventory: {payload['slot_count']} slots, "
        f"irrefl census count={census['count']}"
    )
    print(f"artifact written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
