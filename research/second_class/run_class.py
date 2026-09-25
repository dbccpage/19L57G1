"""Run the rung-eight cross-check and write the receipt.

A hand copy of the shape of `research/second_duration/run_duration.py`,
with this rung's measurements and scoring.  Deterministic: no timestamp,
no environment value, keys sorted, LF only.  The receipt regenerates
byte-identically.  Predictions are scored mechanically from the computed
values; a miss is recorded next to its value and never edited.

Usage: python research/second_class/run_class.py [--receipts DIR] [--check]

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

# `class_count` puts the sealed kernel and the sibling trees on the path,
# so it is imported before anything drawn from either.
from class_count import (  # noqa: E402
    ALPHABET,
    GROWING_KINDS,
    STUTTER_KINDS,
    all_reports,
)
from index import BASE_NAMES  # noqa: E402

RECEIPT_NAME = "class_count.json"
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
EXPECTED_REGIMES = {"EMPTY": 75, "L": 523, "F": 1718}
EXPECTED_CLASSES = {"EMPTY": 54, "L": 174, "F": 265}
EXPECTED_ALL_REGIMES = 2316
EXPECTED_ALL_CLASSES = 402
# P-12: the classes reached at more than one base, bounded by arithmetic
# on the within-base and union class counts of the receipts.
MULTI_BASE_LOW = 46
MULTI_BASE_HIGH = 91


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


def _per_base(bases: dict[str, Any], key: str) -> dict[str, Any]:
    return {base: bases[base][key] for base in EXPECTED_SEQUENCES}


def score(reports: dict[str, Any]) -> dict[str, Any]:
    """Score the computational predictions.  The Lean-side rows, the
    ledger rows and the gate-time row are scored where their evidence
    lives and are named here as scored elsewhere rather than omitted."""
    scored: dict[str, Any] = {}
    bases = reports["bases"]
    classes = reports["classes"]
    within = classes["within_base"]
    sequences = _per_base(bases, "sequences")
    regimes = _per_base(bases, "distinct_regimes")
    class_counts = {base: within[base]["classes"] for base in EXPECTED_SEQUENCES}
    scored["P-9"] = {
        "value": {
            "sequences": sequences,
            "distinct_regimes": regimes,
            "replay_mismatches": reports["replay_mismatches"],
            "classes_within_base": class_counts,
            "distinct_regimes_over_all_bases": reports["distinct_regimes_over_all_bases"],
            "classes_over_all_bases": classes["classes_over_all_bases"],
            "key_brute_disagreements": classes["key_brute_disagreements"],
        },
        "verdict": _verdict(
            sequences == EXPECTED_SEQUENCES
            and regimes == EXPECTED_REGIMES
            and reports["replay_mismatches"] == 0
            and class_counts == EXPECTED_CLASSES
            and reports["distinct_regimes_over_all_bases"] == EXPECTED_ALL_REGIMES
            and classes["classes_over_all_bases"] == EXPECTED_ALL_CLASSES
            and classes["key_brute_disagreements"] == 0
        ),
    }

    two_tuples = {
        base: within[base]["classes_with_two_component_tuples"]
        for base in EXPECTED_SEQUENCES
    }
    union_two = classes["classes_over_all_bases_with_two_component_tuples"]
    scored["P-10"] = {
        "value": {
            "classes_with_two_component_tuples": two_tuples,
            "classes_over_all_bases_with_two_component_tuples": union_two,
        },
        "verdict": _verdict(
            all(value == 0 for value in two_tuples.values()) and union_two == 0
        ),
    }

    recurrence = {
        base: {
            "returns": bases[base]["returns"],
            "recurs_iff_unchanging_mismatches":
                bases[base]["recurs_iff_unchanging_mismatches"],
            "stutter_kinds": sorted(bases[base]["stutters_by_kind"]),
        }
        for base in EXPECTED_SEQUENCES
    }
    scored["P-11"] = {
        "value": recurrence,
        "verdict": _verdict(
            all(
                row["returns"] == 0
                and row["recurs_iff_unchanging_mismatches"] == 0
                and row["stutter_kinds"] == sorted(STUTTER_KINDS)
                and not set(row["stutter_kinds"]) & set(GROWING_KINDS)
                for row in recurrence.values()
            )
        ),
    }

    multi = classes["classes_at_more_than_one_base"]
    multi_two = classes["classes_at_more_than_one_base_with_two_changing_counts"]
    scored["P-12"] = {
        "value": {
            "classes_at_more_than_one_base": multi,
            "classes_at_more_than_one_base_with_two_changing_counts": multi_two,
        },
        "verdict": _verdict(
            MULTI_BASE_LOW <= multi <= MULTI_BASE_HIGH and multi_two >= 1
        ),
    }

    witnesses = reports["lean_witnesses"]
    scored["P-13"] = {
        "value": {name: row["claim_holds"] for name, row in sorted(witnesses.items())},
        "verdict": _verdict(all(row["claim_holds"] for row in witnesses.values())),
    }

    for pid, where in (
        ("P-1", "the committed Lean package, checked by verify_lean.py and test_census.py"),
        ("P-2", "the committed Lean package, checked by test_census.py"),
        ("P-3", "the committed Lean package, checked by test_census.py; written in the Python grammar in lean_witnesses"),
        ("P-4", "the committed Lean package, checked by test_census.py"),
        ("P-5", "the committed Lean package, checked by test_census.py"),
        ("P-6", "the committed Lean package, checked by test_census.py"),
        ("P-7", "the committed Lean package, checked by test_census.py"),
        ("P-8", "receipts/lean_axioms.txt, checked by verify_lean.py"),
        ("P-14", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("P-15", "CLAIM_LEDGER.md and this receipt's input_count_claim"),
        ("P-16", "the receipt bytes, --check and test_class.py; the time in STATUS.md"),
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
        "predictions_scored": score(reports),
        "predictions_sha256": frozen_digest("PREDICTIONS.md"),
        "prompt_sha256": frozen_digest("PROMPT.md"),
        "reports": reports,
        "rung": "eight",
        "write_root": "research/second_class",
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
    parser = argparse.ArgumentParser(description="Run the rung-eight cross-check.")
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
