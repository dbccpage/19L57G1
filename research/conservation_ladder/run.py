"""Write the deterministic receipt of the finite mirror.

AuthorityEffect: None.  ``python run.py`` rewrites ``evidence/receipt.json``;
``python run.py --check`` compares a fresh computation with it.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]

from ladder import receipt  # noqa: E402

RECEIPT = HERE / "evidence" / "receipt.json"


def receipt_bytes() -> bytes:
    return (json.dumps(receipt(), indent=2, sort_keys=True) + "\n").encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    fresh = receipt_bytes()
    if args.check:
        if not RECEIPT.is_file() or RECEIPT.read_bytes() != fresh:
            print("FAIL: evidence/receipt.json differs from a fresh computation",
                  file=sys.stderr)
            return 1
        print("receipt matches")
        return 0
    RECEIPT.parent.mkdir(exist_ok=True)
    RECEIPT.write_bytes(fresh)
    print(f"wrote {RECEIPT.relative_to(HERE).as_posix()}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
