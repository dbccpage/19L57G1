"""Replay the ignition computations without changing their source inputs.

AuthorityEffect: None.  ``--write`` creates ``evidence/ignition.json``
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
RECEIPT = ROOT / "evidence" / "ignition.json"
LINKED_STEPS = 10
REMOVAL_STEPS = 8


def evidence() -> dict[str, object]:
    # Imported here, after the custody check in receipt_bytes: importing the
    # model executes the seven pinned modules' top-level code.
    import ignition as ig
    from derivation.model import replay

    exhibits: dict[str, object] = {}
    for reading_name, reading in ig.READINGS.items():
        for measure in ("mu1", "mu2"):
            exhibits[f"linked_{reading_name}_{measure}"] = ig.linked_episodes(
                reading, measure, LINKED_STEPS)
        exhibits[f"removal_{reading_name}_mu2"] = ig.disabled_components(
            reading, "mu2", REMOVAL_STEPS)
    root_families = {
        f"{name}_{measure}": {
            "classes": len(steps),
            "raw_minima": steps[0].raw_minima,
            "cost": list(steps[0].cost),
            "labels": [s.label(root) for s in steps],
        }
        for name, reading in ig.READINGS.items()
        for measure in ("mu1", "mu2")
        for root in [replay(reading.genesis)]
        for steps in [ig.fire(root, measure, ig.BOUNDS, [reading.target])]
    }
    return {
        "schema": "ignition-evidence-v1",
        "authority_effect": "None",
        "bounds": {"max_items": ig.BOUNDS.max_items, "max_arity": ig.BOUNDS.max_arity},
        "laws_declared": ["growth: supply and admit one fresh datum",
                          "firing: a collapsed pair is the demand; a minimum valid "
                          "response answers it; every class retained"],
        "root_families": root_families,
        "route_pair": ig.route_pair(),
        "fixpoint_census": ig.fixpoint_census(REPO),
        "exhibits": exhibits,
    }


def receipt_bytes() -> bytes:
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed: " + "; ".join(failures))
    result = evidence()
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed after replay: " + "; ".join(failures))
    return (json.dumps(result, sort_keys=True, indent=1) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true",
                      help="deliberately create the computation record")
    args = parser.parse_args()
    fresh = receipt_bytes()
    if args.write:
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPT.write_bytes(fresh)
        print("WROTE: deterministic ignition computation record")
        return 0
    if not RECEIPT.is_file() or RECEIPT.read_bytes() != fresh:
        print("FAIL: evidence/ignition.json differs from fresh computation")
        return 1
    print("PASS: source pins, sealed-engine witnesses and computation bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
