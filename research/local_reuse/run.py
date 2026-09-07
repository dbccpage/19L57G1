"""Replay the local-reuse computations without changing their source inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from audit import evidence
from verify_sources import verify_sources

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / "evidence" / "computations.json"


def receipt_bytes() -> bytes:
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed: " + "; ".join(failures))
    result = evidence()
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed after replay: " + "; ".join(failures))
    return (json.dumps(result, sort_keys=True, indent=2) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true", help="deliberately create the computation record")
    args = parser.parse_args()
    fresh = receipt_bytes()
    if args.write:
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPT.write_bytes(fresh)
        print("WROTE: deterministic local-reuse computation record")
        return 0
    if not RECEIPT.is_file() or RECEIPT.read_bytes() != fresh:
        print("FAIL: evidence/computations.json differs from fresh computation")
        return 1
    print("PASS: all source pins, original-engine witnesses and computation bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
