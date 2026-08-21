"""Command-line writer for the finite symmetry--obstruction--repair report."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Sequence

from symmetry_obstruction_bridge import write_bridge_report


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="write the deterministic finite symmetry-obstruction-repair report"
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="destination JSON file; parent directories are created",
    )
    args = parser.parse_args(argv)
    write_bridge_report(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
