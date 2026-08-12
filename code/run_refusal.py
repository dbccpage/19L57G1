"""Produce the refusal-comparison artifact deterministically.

Usage: python code/run_refusal.py [--artifacts DIR] [--max-events N]

Writes ``refusal.json``: per-discipline reachability reports with the
four-way outcome determination, the reify/occurrence equivalence check,
the orientation check, and the capability price table."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from derivation.export import write_json
from derivation.refusal import (
    capability_prices,
    discipline_report,
    equivalence_check,
    orientation_check,
)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--max-events", type=int, default=7)
    args = parser.parse_args(argv)
    reports = [
        discipline_report("silent", ["<>"], args.max_events),
        discipline_report("meta", ["<>"], args.max_events),
        discipline_report("fact", ["<>"], args.max_events),
        discipline_report("reify_untagged", ["<>"], args.max_events),
        discipline_report("reify_tagged", ["<>"], args.max_events),
        discipline_report("occurrence", ["<>"], args.max_events),
        discipline_report(
            "second_token", ["<>", "<a>"], args.max_events
        ),
    ]
    payload = {
        "disciplines": reports,
        "equivalence": equivalence_check(args.max_events),
        "orientation": orientation_check(),
        "capability_prices": capability_prices(),
    }
    write_json(args.artifacts / "refusal.json", payload)  # type: ignore[arg-type]
    for r in reports:
        print(
            f"{r['discipline']}: {r['outcome']}; "
            f"min-events {r['min_events_to']}"
        )
    print(f"artifact written to {args.artifacts / 'refusal.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
