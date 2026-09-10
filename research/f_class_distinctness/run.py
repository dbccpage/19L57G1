"""Replay the F-class distinctness computation without changing its inputs.

AuthorityEffect: None.  ``--write`` creates ``evidence/classes.json``
deliberately; ``--check`` recomputes it and compares bytes.  The record
carries no timestamps and no machine-specific paths.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from verify_sources import verify_sources

ROOT = Path(__file__).resolve().parent
RECORD = ROOT / "evidence" / "classes.json"


def class_bytes() -> bytes:
    from classes import class_record
    return (json.dumps(class_record(), sort_keys=True, indent=1) + "\n").encode("utf-8")


def receipt_bytes() -> bytes:
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed: " + "; ".join(failures))
    payload = class_bytes()
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed after computation: " + "; ".join(failures))
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true",
                      help="deliberately create the class record")
    args = parser.parse_args()
    fresh = receipt_bytes()
    if args.write:
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_bytes(fresh)
        print("WROTE: deterministic F-class distinctness record")
        return 0
    if not RECORD.is_file() or RECORD.read_bytes() != fresh:
        print("FAIL: evidence/classes.json differs from fresh computation")
        return 1
    print("PASS: source pins and class-record bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
