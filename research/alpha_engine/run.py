"""Proposal-evaluation-authorization record runner.

Copied from ``research/_scaffold/run.py``.  Edit only ``RECORD``, the
``compute()`` body, and the messages.  Keep the single custody scan.

``--write`` creates ``evidence/three_phase.json`` deliberately;
``--check`` recomputes it and compares bytes.  The record carries no
timestamps and no machine-specific paths.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Mapping

from verify_sources import verify_sources

ROOT = Path(__file__).resolve().parent
RECORD = ROOT / "evidence" / "three_phase.json"


def compute() -> object:
    """Import the fold after the custody scan; replay only, write nothing."""
    from driver_a import three_phase_record
    return three_phase_record()


def _reject_duplicate_keys(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for name, value in pairs:
        if name in result:
            raise ValueError(f"duplicate JSON key {name}")
        result[name] = value
    return result


def load_receipt(raw: bytes) -> Mapping[str, object]:
    """Refuse CR bytes and duplicate JSON names."""
    if b"\r" in raw:
        raise ValueError("CR bytes")
    payload: object = json.loads(
        raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys
    )
    if not isinstance(payload, dict):
        raise ValueError("receipt must be an object")
    return payload


def receipt_bytes() -> bytes:
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed: " + "; ".join(failures))
    # ONE custody scan.  compute() imports and replays only; it writes no files,
    # so a second scan here would re-verify unchanged inputs for nothing.
    record = compute()
    return (json.dumps(record, sort_keys=True, indent=1) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true",
                      help="deliberately create the record")
    args = parser.parse_args()
    fresh = receipt_bytes()
    load_receipt(fresh)
    if args.write:
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_bytes(fresh)
        print("WROTE: deterministic PEA record")
        return 0
    if not RECORD.is_file() or RECORD.read_bytes() != fresh:
        print("FAIL: evidence/three_phase.json differs from fresh computation")
        return 1
    print("PASS: source pins and PEA record bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
