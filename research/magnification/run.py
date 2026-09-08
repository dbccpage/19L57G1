"""Replay the census without changing its source inputs.

AuthorityEffect: None.  ``--write`` creates ``evidence/census.json``
deliberately; ``--check`` recomputes it and compares bytes.  The record
carries no timestamps and no machine-specific paths.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from verify_sources import verify_sources

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
RECEIPT = ROOT / "evidence" / "census.json"


def receipt_bytes() -> bytes:
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed: " + "; ".join(failures))
    # Imported here, after the custody check: importing the census executes
    # the seven pinned modules' top-level code.
    import magnification

    result = magnification.census(REPO)
    totals = result["totals"]
    assert isinstance(totals, dict)
    if totals["failures"] != 0:
        raise RuntimeError("census reports semantic failures")
    exports = result["exports"]
    assert isinstance(exports, dict)
    for name, export in exports.items():
        assert isinstance(export, dict)
        mag = export["magnification"]
        assert isinstance(mag, dict)
        if mag["seed_responses_valid"] != mag["creation_rounds"]:
            raise RuntimeError(f"{name}: a seed response is invalid")
    samples = result["restart_samples"]
    assert isinstance(samples, dict)
    runs = samples["runs"]
    assert isinstance(runs, list)
    for sample in runs:
        assert isinstance(sample, dict)
        layers = sample["layers"]
        assert isinstance(layers, list)
        if not layers or any(not isinstance(layer, dict) or layer.get("equal") is not True
                             for layer in layers):
            raise RuntimeError("sampled restart is unequal or incomplete")
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
    print("PASS: source pins, sealed-export census and record bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
