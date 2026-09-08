"""Replay the census without changing its source inputs.

AuthorityEffect: None.  ``--write`` creates ``evidence/census.json``
deliberately; ``--check`` recomputes it and compares bytes.  The record
carries no timestamps and no machine-specific paths.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

from verify_sources import verify_sources

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / "evidence" / "census.json"


def receipt_bytes() -> bytes:
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed: " + "; ".join(failures))
    # Imported here, after the custody check: importing the census executes
    # the eight pinned modules' top-level code.
    import translation

    result = translation.census()
    totals = cast(dict[str, object], result["totals"])
    if totals["failures"] != 0:
        raise RuntimeError("census reports semantic failures")
    universe = cast(dict[str, object], result["universe"])
    if universe["settings"] == 0:
        raise RuntimeError("the sealed universe enumerated nothing")
    thirteen = cast(dict[str, object], cast(dict[str, object], result["sealed_settings"])["settings"])
    if len(thirteen) != 13:
        raise RuntimeError("the sealed concrete settings are not thirteen")
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed after replay: " + "; ".join(failures))
    return (json.dumps(result, sort_keys=True, indent=1) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true",
                      help="deliberately create the census record")
    args = parser.parse_args()
    fresh = receipt_bytes()
    if args.write:
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPT.write_bytes(fresh)
        print("WROTE: deterministic census record")
        return 0
    if not RECEIPT.is_file() or RECEIPT.read_bytes() != fresh:
        print("FAIL: evidence/census.json differs from fresh computation")
        return 1
    print("PASS: source pins, translation census and record bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
