"""Command-line writer for the finite replay/lift/descent report."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Sequence

from finite_tower import MAX_HORIZON, write_report


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="write the deterministic finite replay/lift/descent report"
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="destination JSON file; parent directories are created",
    )
    parser.add_argument(
        "--horizon",
        default=MAX_HORIZON,
        type=int,
        help="completed largest stage to emit (0 through 15)",
    )
    args = parser.parse_args(argv)
    write_report(args.output, args.horizon)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
