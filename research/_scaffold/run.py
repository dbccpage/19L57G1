"""CANONICAL research-tree record runner — copy this into a new tree.

``--write`` creates the tree's ``evidence/<record>.json`` deliberately;
``--check`` recomputes it and compares bytes.  The record carries no timestamps
and no machine-specific paths.

Copy this into a new ``research/<tree>/`` and edit ONLY ``RECORD``, the
``compute()`` body, and the messages.  Keep the single custody scan below: do
NOT copy an older tree's ``run.py``, which scans custody twice in
``receipt_bytes`` (once before and once after the record computation).  The
record computation imports and replays only — it writes no files — so the
second scan is pure redundant work over the sealed tree.  A new tree must drop
it at creation, before any consumer pins this tree's ``.py`` at a baseline (once
pinned, editing ``run.py`` cascades custody repins).
``research/_scaffold/check_scaffold.py`` warns if the double scan reappears.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from verify_sources import verify_sources

ROOT = Path(__file__).resolve().parent
RECORD = ROOT / "evidence" / "REPLACE_ME.json"


def compute() -> object:
    """EDIT THIS: import the tree's record module and return its record object.

    The import must happen INSIDE this function (after the custody scan in
    ``receipt_bytes``), because importing a module that loads the pinned
    derivation modules executes their top-level code; at module scope that would
    run before the custody check.
    """
    raise NotImplementedError("replace with: from <module> import record; return record()")


def receipt_bytes() -> bytes:
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed: " + "; ".join(failures))
    # ONE custody scan.  compute() imports and replays only; it writes no files,
    # so a second verify_sources() here would re-verify unchanged inputs for
    # nothing.
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
    if args.write:
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_bytes(fresh)
        print("WROTE: deterministic record")
        return 0
    if not RECORD.is_file() or RECORD.read_bytes() != fresh:
        print("FAIL: evidence record differs from fresh computation")
        return 1
    print("PASS: source pins and record bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
