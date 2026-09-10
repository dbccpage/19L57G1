"""Replay the reqs-channel computations without changing their source inputs.

AuthorityEffect: None.  ``--write`` creates ``evidence/grammar.json`` and
``evidence/candidates.json`` deliberately; ``--check`` recomputes them and
compares bytes.  The records carry no timestamps and no machine-specific
paths.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from verify_sources import verify_sources

ROOT = Path(__file__).resolve().parent
GRAMMAR = ROOT / "evidence" / "grammar.json"
CANDIDATES = ROOT / "evidence" / "candidates.json"


def grammar_bytes() -> bytes:
    from grammar import grammar_record
    return (json.dumps(grammar_record(), sort_keys=True, indent=1) + "\n").encode("utf-8")


def candidates_bytes() -> bytes:
    from candidates import candidate_record
    return (json.dumps(candidate_record(), sort_keys=True, indent=1) + "\n").encode("utf-8")


def receipt_bytes() -> dict[str, bytes]:
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed: " + "; ".join(failures))
    # The record computations import and replay only; they write no files, so a
    # second full custody scan here (dozens of git calls over the sealed tree)
    # would re-verify unchanged inputs for nothing.
    return {"grammar": grammar_bytes(), "candidates": candidates_bytes()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true",
                      help="deliberately create the computation records")
    args = parser.parse_args()
    fresh = receipt_bytes()
    targets = {"grammar": GRAMMAR, "candidates": CANDIDATES}
    if args.write:
        for name, path in targets.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(fresh[name])
        print("WROTE: deterministic grammar and candidate records")
        return 0
    for name, path in targets.items():
        if not path.is_file() or path.read_bytes() != fresh[name]:
            print(f"FAIL: evidence/{name}.json differs from fresh computation")
            return 1
    print("PASS: source pins and computation bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
