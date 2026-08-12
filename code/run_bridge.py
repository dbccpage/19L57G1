"""Produce the bridge-provenance artifact deterministically.

Usage: python code/run_bridge.py [--artifacts DIR] [--max-events N]

Writes ``bridge.json``: reachability reports for the three admission
scenarios (single token with dedup; two tokens; occurrence discipline),
the equivariant-introduction scan, and the assembled per-ingredient
provenance table."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.bridge import (
    equivariant_scan,
    provenance_table,
    scenario_report,
)
from derivation.export import write_json


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--max-events", type=int, default=7)
    args = parser.parse_args(argv)
    payload = {
        "scenarios": [
            scenario_report(
                "single_dedup", ["<>"], args.max_events, False
            ),
            scenario_report(
                "two_dedup", ["<>", "<a>"], args.max_events, False
            ),
            scenario_report(
                "occurrence", ["<>"], args.max_events, True
            ),
        ],
        "equivariant_scan": equivariant_scan(),
        "provenance_table": provenance_table(),
    }
    write_json(args.artifacts / "bridge.json", payload)  # type: ignore[arg-type]
    for s in payload["scenarios"]:
        assert isinstance(s, dict)
        print(
            f"{s['scenario']}: states {s['states_reached']}, "
            f"max carrier {s['max_carrier']}, "
            f"min-events {s['min_events_to']}"
        )
    print(f"artifact written to {args.artifacts / 'bridge.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
