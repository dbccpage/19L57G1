"""Print or deliberately regenerate the verified partial-Decide receipt.

Bootstrap boundary: this small entry point and verify_pins.py necessarily run
before verify_pins can establish their own Git custody.  No renderer or
derivation module is imported until that early custody preflight succeeds.
"""

from __future__ import annotations

import argparse
import sys

from verify_pins import RECEIPT_PATH, render_verified_receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="overwrite the committed receipt with the current deterministic bytes",
    )
    args = parser.parse_args()
    try:
        payload = render_verified_receipt()
    except (
        ImportError,
        OSError,
        RuntimeError,
        ValueError,
    ) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1
    if args.write:
        RECEIPT_PATH.write_bytes(payload)
        print(f"wrote {RECEIPT_PATH}")
    else:
        sys.stdout.buffer.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
