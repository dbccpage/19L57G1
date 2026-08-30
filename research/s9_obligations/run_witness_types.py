"""Write the P3 receipt: ``run_witness_types.py --out DIR`` (default
``receipts``).  Deterministic; no timestamps, paths, or environment data
in the output.  AuthorityEffect: None."""

from __future__ import annotations

import argparse
import sys

import witness_types


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="receipts", help="receipt directory inside the tree")
    args = parser.parse_args(argv)
    written = witness_types.write(args.out)
    print(f"wrote {written}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
