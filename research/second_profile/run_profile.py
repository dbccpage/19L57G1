"""Run the rung-nine cross-check and write the receipt.

A hand copy of the shape of `research/second_class/run_class.py`,
with this rung's measurements and scoring.  Deterministic: no timestamp,
no environment value, keys sorted, LF only.  The receipt regenerates
byte-identically.  Predictions are scored mechanically from the computed
values; a miss is recorded next to its value and never edited.

Usage: python research/second_profile/run_profile.py [--receipts DIR] [--check]

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

# `profile_rows` puts the sealed kernel and the sibling trees on the path,
# so it is imported before anything drawn from either.
from profile_rows import (  # noqa: E402
    ALPHABET,
    ENDING_KINDS,
    KEEPING_KINDS,
    all_reports,
)
from index import BASE_NAMES  # noqa: E402

RECEIPT_NAME = "profile.json"
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
# Q-9: the least length holding two, and the three EMPTY counts.
EXPECTED_LEAST = {"EMPTY": 4, "L": 2, "F": 2}
EXPECTED_EMPTY_TWO = {"sequences": 22, "regimes": 6, "classes": 3}
# Q-11: the largest class count at each base.
EXPECTED_LARGEST = {"EMPTY": 2, "L": 3, "F": 4}
# Q-14: the changes of the class count by kind, over all three bases.
EXPECTED_ZERO_KINDS = ("AdmitForm", "Impose", "Supply")
EXPECTED_DATUM_CHANGES = [0, 1]
EXPECTED_RULE_CHANGES = [-2, -1, 0]
EXPECTED_INST_INCLUDES = (-1, 0, 1, 2)
INST_RANGE = (-2, 2)
ALL_KINDS = ("AdmitDatum", "AdmitForm", "AdmitInst", "AdmitRuleAll", "Impose", "Supply")


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
    mismatches = _per_base(bases, "replay_mismatches")
    class_counts = {base: within[base]["classes"] for base in EXPECTED_SEQUENCES}
    union = classes["over_all_bases"]
    scored["Q-8"] = {
        "value": {
            "sequences": sequences,
            "distinct_regimes": regimes,
            "replay_mismatches": mismatches,
            "classes_within_base": class_counts,
            "distinct_regimes_over_all_bases": classes["distinct_regimes_over_all_bases"],
            "classes_over_all_bases": union["classes"],
            "key_brute_disagreements": classes["key_brute_disagreements"],
        },
        "verdict": _verdict(
            sequences == EXPECTED_SEQUENCES
            and regimes == EXPECTED_REGIMES
            and all(value == 0 for value in mismatches.values())
            and class_counts == EXPECTED_CLASSES
            and classes["distinct_regimes_over_all_bases"] == EXPECTED_ALL_REGIMES
            and union["classes"] == EXPECTED_ALL_CLASSES
            and classes["key_brute_disagreements"] == 0
        ),
    }

    least = _per_base(bases, "least_length_holding_two")
    empty = bases["EMPTY"]
    empty_two = {
        "sequences": empty["sequences_holding_two"],
        "regimes": empty["regimes_holding_two"],
        "classes": empty["classes_holding_two"],
    }
    scored["Q-9"] = {
        "value": {"least_length_holding_two": least, "empty_holding_two": empty_two},
        "verdict": _verdict(least == EXPECTED_LEAST and empty_two == EXPECTED_EMPTY_TWO),
    }

    two_count = _per_base(bases, "two_count_mismatches")
    scored["Q-10"] = {
        "value": {"two_count_mismatches": two_count},
        "verdict": _verdict(all(value == 0 for value in two_count.values())),
    }

    largest = _per_base(bases, "largest_class_count")
    above_data = _per_base(bases, "count_above_data")
    above_named = _per_base(bases, "count_above_named_plus_one")
    scored["Q-11"] = {
        "value": {
            "largest_class_count": largest,
            "count_above_data": above_data,
            "count_above_named_plus_one": above_named,
        },
        "verdict": _verdict(
            largest == EXPECTED_LARGEST
            and all(value == 0 for value in above_data.values())
            and all(value == 0 for value in above_named.values())
        ),
    }

    lumped = {
        base: {
            "holding_two": within[base]["classes_with_two_values_of_holding_two"],
            "class_count": within[base]["classes_with_two_class_counts"],
        }
        for base in EXPECTED_SEQUENCES
    }
    lumped["all"] = {
        "holding_two": union["classes_with_two_values_of_holding_two"],
        "class_count": union["classes_with_two_class_counts"],
    }
    scored["Q-12"] = {
        "value": lumped,
        "verdict": _verdict(
            all(row["holding_two"] == 0 and row["class_count"] == 0 for row in lumped.values())
        ),
    }

    ending = {
        base: sorted(bases[base]["ending_transitions_by_kind"]) for base in EXPECTED_SEQUENCES
    }
    scored["Q-13"] = {
        "value": ending,
        "verdict": _verdict(
            ending["EMPTY"] == []
            and ending["L"] == sorted(ENDING_KINDS)
            and ending["F"] == sorted(ENDING_KINDS)
            and not set(ending["L"] + ending["F"]) & set(KEEPING_KINDS)
        ),
    }

    changes = reports["changes_by_kind_over_all_bases"]
    inst = changes.get("AdmitInst", [])
    scored["Q-14"] = {
        "value": changes,
        "verdict": _verdict(
            sorted(changes) == sorted(ALL_KINDS)
            and all(changes[kind] == [0] for kind in EXPECTED_ZERO_KINDS)
            and changes["AdmitDatum"] == EXPECTED_DATUM_CHANGES
            and changes["AdmitRuleAll"] == EXPECTED_RULE_CHANGES
            and all(value in inst for value in EXPECTED_INST_INCLUDES)
            and all(INST_RANGE[0] <= value <= INST_RANGE[1] for value in inst)
        ),
    }

    for pid, where in (
        ("Q-1", "the committed Lean package, checked by verify_lean.py and test_census.py"),
        ("Q-2", "the committed Lean package, checked by test_census.py"),
        ("Q-3", "the committed Lean package, checked by test_census.py"),
        ("Q-4", "the committed Lean package, checked by test_census.py; the witness is written in the Python grammar in lean_witnesses"),
        ("Q-5", "the committed Lean package, checked by test_census.py"),
        ("Q-6", "the committed Lean package, checked by test_census.py; written in the Python grammar in lean_witnesses"),
        ("Q-7", "receipts/lean_axioms.txt, checked by verify_lean.py"),
        ("Q-15", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("Q-16", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("Q-17", "CLAIM_LEDGER.md and this receipt's input_count_claim"),
        ("Q-18", "the receipt bytes, --check and test_profile.py; the time in STATUS.md"),
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
        "rung": "nine",
        "write_root": "research/second_profile",
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
    parser = argparse.ArgumentParser(description="Run the rung-nine cross-check.")
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
