"""Run the rung-five cross-check and write the receipt.

A hand copy of the shape of `research/second_iso/run_iso_index.py`, with
this rung's measurements and scoring.  Deterministic: no timestamp, no
environment value, keys sorted, LF only.  The receipt regenerates
byte-identically.  Predictions are scored mechanically from the computed
values; a miss is recorded next to its value and never edited.

Usage: python research/second_symmetry/run_symmetry.py [--receipts DIR] [--check]

``--check`` writes nothing: it rebuilds the payload and compares it with
the committed receipt, so a drifted receipt fails without the run being
able to bless itself by overwriting the bytes it is checked against.

The two frozen texts are hashed with line endings normalized to LF before
the digest is taken, so the digest recorded is that of the frozen bytes as
Git holds them, whatever the working tree holds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from typing import Any

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# `symmetry` puts the sealed kernel and the sibling trees on the path, so
# it is imported before anything drawn from either.
from symmetry import (  # noqa: E402
    ADDING_KINDS,
    ALPHABET,
    all_reports,
)
from iso_index import BASE_NAMES, ORBIT_BOUND  # noqa: E402

RECEIPT_NAME = "symmetry.json"
MEGABYTE = 1_000_000
FORBIDDEN_KEYS = frozenset(
    {"timestamp", "time", "date", "datetime", "created_at", "host", "hostname",
     "platform", "cwd", "env", "environment", "user", "path"}
)

__all__ = [
    "RECEIPT_NAME",
    "build",
    "forbidden_keys",
    "frozen_digest",
    "main",
    "render",
    "score",
    "write",
]

# The values the frozen predictions commit to, transcribed here so the
# scoring is mechanical.  A transcription error is visible as a miss
# against a value the receipt also records, never as a silent pass.
EXPECTED_SEQUENCES = {"EMPTY": 577, "L": 3928, "F": 14293}
EXPECTED_EDGES = 18795
EXPECTED_RISE = {"ratio": "5", "kinds": ["AdmitDatum"]}
EXPECTED_FALL = {"ratio": "20", "kinds": ["AdmitInst"]}
EXPECTED_SHORTEST_MIXED = 2
EXPECTED_EXTREMES = (1, 240)


def frozen_digest(name: str) -> str:
    raw = (HERE / name).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def forbidden_keys(value: object, where: str = "") -> list[str]:
    """Every key of the payload, at any depth, that names a temporal or
    environment value.  The receipt must carry none."""
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            here = f"{where}.{key}" if where else str(key)
            if str(key).lower() in FORBIDDEN_KEYS:
                found.append(here)
            found.extend(forbidden_keys(item, here))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(forbidden_keys(item, f"{where}[{index}]"))
    return found


def _verdict(hit: bool) -> str:
    return "HIT" if hit else "MISSED"


def _moves(tally: dict[str, dict[str, int]]) -> dict[str, int]:
    return {way: tally["changing"][way] for way in ("up", "equal", "down")}


def score(reports: dict[str, Any]) -> dict[str, Any]:
    """Score the computational predictions.  The Lean-side rows, the
    ledger rows and the gate-time row are scored where their evidence
    lives and are named here as scored elsewhere rather than omitted."""
    scored: dict[str, Any] = {}
    bases = reports["bases"]
    autos = reports["automorphisms"]
    sequences = {base: bases[base]["sequences"] for base in EXPECTED_SEQUENCES}
    edge_total = reports["edges"]["edges"]
    scored["K-10"] = {
        "value": {
            "sequences": sequences,
            "edges": edge_total,
            "replay_mismatches": reports["replay_mismatches"],
            "set_disagreements": autos["set_disagreements"],
            "count_disagreements": autos["count_disagreements"],
        },
        "verdict": _verdict(
            sequences == EXPECTED_SEQUENCES
            and edge_total == EXPECTED_EDGES
            and reports["replay_mismatches"] == 0
            and autos["set_disagreements"] == 0
            and autos["count_disagreements"] == 0
        ),
    }

    by_kind = reports["edges"]["by_kind"]
    unchanging_moves = sum(
        by_kind[kind]["unchanging"][way] for kind in by_kind for way in ("up", "down")
    )
    supply_moves = sum(by_kind["Supply"]["changing"].values())
    grow_down = by_kind["AdmitDatum"]["changing"]["down"] + by_kind["AdmitForm"]["changing"]["down"]
    both_ways = {
        kind: by_kind[kind]["changing"]["up"] >= 1 and by_kind[kind]["changing"]["down"] >= 1
        for kind in ADDING_KINDS
    }
    scored["K-11"] = {
        "value": {
            "unchanging_edges_moving": unchanging_moves,
            "supply_edges_changing": supply_moves,
            "datum_or_form_edges_lowering": grow_down,
            "adding_kinds": {kind: _moves(by_kind[kind]) for kind in ADDING_KINDS},
        },
        "verdict": _verdict(
            unchanging_moves == 0
            and supply_moves == 0
            and grow_down == 0
            and all(both_ways.values())
        ),
    }

    datum = reports["edges"]["datum_law"]
    form = reports["edges"]["form_law"]
    scored["K-12"] = {
        "value": {"datum": datum, "form": form},
        "verdict": _verdict(
            datum["violations"] == 0 and form["violations"] == 0
            and datum["checked"] >= 1 and form["checked"] >= 1
        ),
    }

    meet = reports["edges"]["meet_law"]
    scored["K-13"] = {
        "value": meet,
        "verdict": _verdict(
            meet["set_violations"] == 0 and meet["ratio_violations"] == 0
            and meet["checked"] >= 1
        ),
    }

    rise = reports["edges"]["largest_rise"]
    fall = reports["edges"]["largest_fall"]
    scored["K-14"] = {
        "value": {"largest_rise": rise, "largest_fall": fall},
        "verdict": _verdict(rise == EXPECTED_RISE and fall == EXPECTED_FALL),
    }

    seq = reports["sequences"]
    classes = seq["classes_by_base"]
    shortest = seq["shortest_mixed"]
    shortest_length = None if shortest is None else shortest["length"]
    scored["K-15"] = {
        "value": {"classes_by_base": classes, "shortest_mixed_length": shortest_length},
        "verdict": _verdict(
            all(classes[base][cls] >= 1 for base in ("L", "F") for cls in classes[base])
            and classes["EMPTY"]["FALLING"] == 0
            and shortest_length == EXPECTED_SHORTEST_MIXED
        ),
    }

    count_violations = reports["edges"]["element_count_violations"]
    revisits = seq["class_revisits_after_a_changing_event"]
    scored["K-16"] = {
        "value": {"element_count_violations": count_violations, "class_revisits": revisits},
        "verdict": _verdict(count_violations == 0 and revisits == 0),
    }

    extremes = (autos["smallest"], autos["largest"])
    scored["K-17"] = {
        "value": {"smallest": extremes[0], "largest": extremes[1]},
        "verdict": _verdict(extremes == EXPECTED_EXTREMES),
    }

    for pid, where in (
        ("K-1", "the committed Lean package, checked by verify_lean.py and test_census.py"),
        ("K-2", "the committed Lean package, checked by verify_lean.py and test_census.py"),
        ("K-3", "FWDEF_CENSUS.json, checked by test_census.py"),
        ("K-4", "the committed Lean package, checked by test_census.py"),
        ("K-5", "the committed Lean package and CLAIM_LEDGER.md, checked by test_census.py"),
        ("K-6", "the committed Lean package, checked by test_census.py"),
        ("K-7", "the committed Lean package, checked by test_census.py"),
        ("K-8", "the committed Lean package and CLAIM_LEDGER.md, checked by test_census.py"),
        ("K-9", "receipts/lean_axioms.txt, checked by verify_lean.py"),
        ("K-18", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("K-19", "CLAIM_LEDGER.md and this receipt's input_count_claim"),
        ("K-20", "the receipt bytes, --check and test_symmetry.py; the time in STATUS.md"),
    ):
        scored[pid] = {"value": f"scored elsewhere: {where}", "verdict": "ELSEWHERE"}
    return scored


def build() -> dict[str, Any]:
    reports = all_reports(ALPHABET)
    return {
        "alphabet": {
            "arities": list(ALPHABET.arities),
            "fresh_tokens": list(ALPHABET.fresh_tokens),
            "max_data": ALPHABET.max_data,
            "max_forms": ALPHABET.max_forms,
            "max_sequence_length": ALPHABET.max_length,
            "supply_token": ALPHABET.supply_token,
        },
        "authority_effect": "None",
        "bases": list(BASE_NAMES),
        "input_count_claim": "none",
        "orbit_bound": ORBIT_BOUND,
        "predictions_scored": score(reports),
        "predictions_sha256": frozen_digest("PREDICTIONS.md"),
        "prompt_sha256": frozen_digest("PROMPT.md"),
        "reports": reports,
        "rung": "five",
        "write_root": "research/second_symmetry",
    }


def render(payload: dict[str, Any]) -> bytes:
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    return text.encode("utf-8")


def write(payload: dict[str, Any], receipts: pathlib.Path) -> pathlib.Path:
    receipts.mkdir(parents=True, exist_ok=True)
    target = receipts / RECEIPT_NAME
    target.write_bytes(render(payload))
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the rung-five cross-check.")
    parser.add_argument(
        "--receipts", default=str(HERE / "receipts"), help="output directory"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare with the committed receipt and write nothing",
    )
    args = parser.parse_args(argv)
    receipts = pathlib.Path(args.receipts)
    payload = build()
    fresh = render(payload)
    bad = forbidden_keys(payload)
    if bad:
        print(f"FAIL: the receipt carries forbidden keys: {bad}")
        return 1
    if len(fresh) > MEGABYTE:
        print(f"FAIL: the receipt is {len(fresh)} bytes and must be split")
        return 1
    if args.check:
        target = receipts / RECEIPT_NAME
        if not target.exists():
            print(f"FAIL: {target} is missing")
            return 1
        committed = target.read_bytes().replace(b"\r\n", b"\n")
        if committed != fresh:
            print(f"FAIL: {target} differs from a fresh run")
            return 1
        print(f"receipt matches a fresh run ({len(fresh)} bytes)")
    else:
        target = write(payload, receipts)
        print(f"wrote {target} ({len(fresh)} bytes)")
    scored = payload["predictions_scored"]
    for pid in sorted(scored, key=lambda name: (len(name), name)):
        print(f"  {pid}: {scored[pid]['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
