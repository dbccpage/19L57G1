"""Replay the CL-ISO-SOUND hunt without changing its source inputs.

AuthorityEffect: None.  ``--write`` creates ``evidence/hunt.json``
deliberately; ``--check`` recomputes it and compares bytes.  The record
carries no timestamps and no machine-specific paths.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from verify_sources import verify_sources

ROOT = Path(__file__).resolve().parent
HUNT = ROOT / "evidence" / "hunt.json"


def hunt_bytes() -> bytes:
    from hunt import hunt
    return (json.dumps(hunt(), sort_keys=True, indent=1) + "\n").encode("utf-8")


def receipt_bytes() -> bytes:
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed: " + "; ".join(failures))
    payload = hunt_bytes()
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed after hunt: " + "; ".join(failures))
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true",
                      help="deliberately create the hunt record")
    args = parser.parse_args()
    fresh = receipt_bytes()
    if args.write:
        HUNT.parent.mkdir(parents=True, exist_ok=True)
        HUNT.write_bytes(fresh)
        print("WROTE: deterministic iso-sound hunt record")
        return 0
    if not HUNT.is_file() or HUNT.read_bytes() != fresh:
        print("FAIL: evidence/hunt.json differs from fresh computation")
        return 1
    print("PASS: source pins and hunt bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
