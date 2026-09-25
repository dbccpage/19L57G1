"""Run the rung-seven cross-check and write the receipt.

A hand copy of the shape of `research/second_succession/run_succession.py`,
with this rung's measurements and scoring.  Deterministic: no timestamp,
no environment value, keys sorted, LF only.  The receipt regenerates
byte-identically.  Predictions are scored mechanically from the computed
values; a miss is recorded next to its value and never edited.

Usage: python research/second_duration/run_duration.py [--receipts DIR] [--check]

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

# `duration` puts the sealed kernel and the sibling trees on the path, so
# it is imported before anything drawn from either.
from duration import ALPHABET, all_reports  # noqa: E402
from index import BASE_NAMES  # noqa: E402

RECEIPT_NAME = "duration.json"
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
EXPECTED_SHORTEST_VECTOR = 2
EXPECTED_SHORTEST_GAP = 3


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


def _length(found: Any) -> Any:
    return None if found is None else found["length"]


def score(reports: dict[str, Any]) -> dict[str, Any]:
    """Score the computational predictions.  The Lean-side rows, the
    ledger rows and the gate-time row are scored where their evidence
    lives and are named here as scored elsewhere rather than omitted."""
    scored: dict[str, Any] = {}
    bases = reports["bases"]
    sequences = _per_base(bases, "sequences")
    regimes = _per_base(bases, "distinct_regimes")
    scored["N-8"] = {
        "value": {
            "sequences": sequences,
            "distinct_regimes": regimes,
            "replay_mismatches": reports["replay_mismatches"],
        },
        "verdict": _verdict(
            sequences == EXPECTED_SEQUENCES
            and regimes == EXPECTED_REGIMES
            and reports["replay_mismatches"] == 0
        ),
    }

    shape = {
        base: {
            "length_violations": bases[base]["length_violations"],
            "sum_violations": bases[base]["sum_violations"],
        }
        for base in EXPECTED_SEQUENCES
    }
    scored["N-9"] = {
        "value": shape,
        "verdict": _verdict(
            all(value == 0 for row in shape.values() for value in row.values())
        ),
    }

    envelope_rows = {
        base: {
            "vectors_outside_envelope": bases[base]["vectors_outside_envelope"],
            "regimes_with_unreached_or_extra_tuples":
                bases[base]["regimes_with_unreached_or_extra_tuples"],
            "one_tuple_iff_one_vector_violations":
                bases[base]["one_tuple_iff_one_vector_violations"],
        }
        for base in EXPECTED_SEQUENCES
    }
    scored["N-10"] = {
        "value": envelope_rows,
        "verdict": _verdict(
            all(value == 0 for row in envelope_rows.values() for value in row.values())
        ),
    }

    vector_split = _per_base(bases, "vector_split_regimes")
    gap_split = _per_base(bases, "gap_split_regimes")
    shortest_vector = {
        base: _length(bases[base]["shortest_vector_splitting_sequence"])
        for base in EXPECTED_SEQUENCES
    }
    shortest_gap = {
        base: _length(bases[base]["shortest_gap_splitting_sequence"])
        for base in EXPECTED_SEQUENCES
    }
    scored["N-11"] = {
        "value": {
            "vector_split_regimes": vector_split,
            "gap_split_regimes": gap_split,
            "shortest_vector_splitting_length": shortest_vector,
            "shortest_gap_splitting_length": shortest_gap,
        },
        "verdict": _verdict(
            all(
                vector_split[base] >= 1
                and gap_split[base] >= 1
                and gap_split[base] <= vector_split[base]
                and shortest_vector[base] == EXPECTED_SHORTEST_VECTOR
                and shortest_gap[base] == EXPECTED_SHORTEST_GAP
                for base in EXPECTED_SEQUENCES
            )
        ),
    }

    tail_only = _per_base(bases, "tail_only_regimes")
    scored["N-12"] = {
        "value": {"tail_only_regimes": tail_only},
        "verdict": _verdict(all(value >= 1 for value in tail_only.values())),
    }

    classes = reports["classes"]
    scored["N-13"] = {
        "value": {
            "classes": classes["classes"],
            "classes_with_two_vectors": classes["classes_with_two_vectors"],
            "classes_with_two_sums": classes["classes_with_two_sums"],
            "classes_with_two_envelopes": classes["classes_with_two_envelopes"],
        },
        "verdict": _verdict(
            all(
                classes["classes_with_two_vectors"][base] >= 1
                and classes["classes_with_two_sums"][base] == 0
                and classes["classes_with_two_envelopes"][base] >= 1
                for base in EXPECTED_SEQUENCES
            )
        ),
    }

    witnesses = reports["lean_witnesses"]
    scored["N-14"] = {
        "value": {name: row["claim_holds"] for name, row in sorted(witnesses.items())},
        "verdict": _verdict(all(row["claim_holds"] for row in witnesses.values())),
    }

    for pid, where in (
        ("N-1", "the committed Lean package, checked by verify_lean.py and test_census.py"),
        ("N-2", "the committed Lean package, checked by test_census.py; replayed in lean_witnesses"),
        ("N-3", "the committed Lean package, checked by test_census.py; replayed in lean_witnesses"),
        ("N-4", "the committed Lean package, checked by test_census.py"),
        ("N-5", "the committed Lean package, checked by test_census.py; replayed in lean_witnesses"),
        ("N-6", "the committed Lean package and CLAIM_LEDGER.md, checked by test_census.py"),
        ("N-7", "receipts/lean_axioms.txt, checked by verify_lean.py"),
        ("N-15", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("N-16", "CLAIM_LEDGER.md and this receipt's input_count_claim"),
        ("N-17", "the receipt bytes, --check and test_duration.py; the time in STATUS.md"),
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
        "reading": "CHANGING",
        "reports": reports,
        "rung": "seven",
        "write_root": "research/second_duration",
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
    parser = argparse.ArgumentParser(description="Run the rung-seven cross-check.")
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
