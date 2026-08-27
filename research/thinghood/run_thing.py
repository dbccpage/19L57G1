"""Write the deterministic thinghood receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

try:  # Package import when called by a test runner.
    from .thing import build_receipt
except ImportError:  # Direct ``python run_thing.py`` from this directory.
    from thing import build_receipt


def receipt_bytes() -> bytes:
    """Render the receipt with sorted keys, no timestamp, and LF only."""

    payload = build_receipt()
    rendered = json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    )
    return rendered.encode("utf-8") + b"\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--artifacts",
        type=Path,
        default=Path("receipts"),
        help="directory receiving thing.json (default: receipts)",
    )
    args = parser.parse_args(argv)
    try:
        args.artifacts.mkdir(parents=True, exist_ok=True)
        output = args.artifacts / "thing.json"
        output.write_bytes(receipt_bytes())
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}")
        return 1
    print(f"wrote {output.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main", "receipt_bytes"]
