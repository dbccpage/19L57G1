"""Write the deterministic priced-admissions receipt."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from priced import write_receipt  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--receipts",
        type=Path,
        default=HERE / "receipts",
        help="directory receiving priced_admissions.json",
    )
    args = parser.parse_args()
    write_receipt(args.receipts / "priced_admissions.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
