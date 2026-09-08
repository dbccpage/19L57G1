"""Replay the census without changing its source inputs.

AuthorityEffect: None.  ``--write`` creates ``evidence/census.json``
deliberately; ``--check`` recomputes it and compares bytes.  The record
carries no timestamps and no machine-specific paths.  Beyond the byte
comparison, the receipt refuses to record a census whose semantic content
contradicts the claims: a failure of any kind, an unfaithful concrete
setting, a sealed theorem verdict not reproduced, a visibility verdict that
contradicts the sealed collapse verdict at the root, a visible pair whose
root round is not the empty response, or a collapsed pair whose root round
is not exactly the self-instance and link classes at one item.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import cast

from verify_sources import verify_sources

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
RECEIPT = ROOT / "evidence" / "census.json"
JsonObj = dict[str, object]


def _obj(value: object) -> JsonObj:
    if not isinstance(value, dict):
        raise RuntimeError("census record shape")
    return cast(JsonObj, value)


def refuse(result: JsonObj) -> None:
    """Raise on any semantic content the claims exclude."""
    totals = _obj(result["totals"])
    if totals["failures"] != 0:
        raise RuntimeError("census reports semantic failures")
    universe = _obj(result["universe"])
    if universe["settings"] == 0:
        raise RuntimeError("the sealed universe enumerated nothing")
    thirteen = _obj(_obj(result["sealed_settings"])["settings"])
    if len(thirteen) != 13:
        raise RuntimeError("the sealed concrete settings are not thirteen")
    for name, raw in thirteen.items():
        entry = _obj(raw)
        if entry["faithful"] is not True:
            raise RuntimeError(f"{name}: the encoding is not faithful")
        for check in cast(list[object], entry["sealed_theorems"]):
            if _obj(check)["agrees"] is not True:
                raise RuntimeError(f"{name}: a sealed theorem verdict is not reproduced")
        if "restart" in entry:
            for measure, raw_restart in _obj(entry["restart"]).items():
                refuse_restart(f"{name}/{measure}", bool(entry["pair_visible"]), _obj(raw_restart))
    for name, raw in _obj(_obj(result["two_point"])["exhibits"]).items():
        entry = _obj(raw)
        for variant, raw_restart in _obj(entry["restart"]).items():
            refuse_restart(f"{name}/{variant}", bool(entry["visible"]), _obj(raw_restart))


def refuse_restart(where: str, pair_visible: bool, record: JsonObj) -> None:
    if record["target_collapsed_at_root"] is pair_visible:
        raise RuntimeError(f"{where}: visibility contradicts the sealed collapse verdict at the root")
    classes = [_obj(c) for c in cast(list[object], record["root_round"])]
    labels = sorted(str(c["label"]) for c in classes)
    if pair_visible and labels != ["empty"]:
        raise RuntimeError(f"{where}: a visible pair whose root round is not the empty response")
    if not pair_visible and (labels != ["inst2", "inst2diag"] or any(c["items"] != 1 for c in classes)):
        raise RuntimeError(f"{where}: a collapsed pair whose root round is not the two one-item classes")


def receipt_bytes() -> bytes:
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed: " + "; ".join(failures))
    # The custody check imported the eight pinned modules; put the sealed
    # kernel on the path explicitly so the census does not depend on that
    # side effect.
    code = str(REPO / "code")
    if code not in sys.path:
        sys.path.insert(0, code)
    import translation

    result = cast(JsonObj, translation.census())
    refuse(result)
    failures = verify_sources()
    if failures:
        raise RuntimeError("source verification failed after replay: " + "; ".join(failures))
    return (json.dumps(result, sort_keys=True, indent=1) + "\n").encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true",
                      help="deliberately create the census record")
    args = parser.parse_args(argv)
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
