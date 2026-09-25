"""Run the rung-six cross-check and write the receipt.

A hand copy of the shape of `research/second_symmetry/run_symmetry.py`,
with this rung's measurements and scoring.  Deterministic: no timestamp,
no environment value, keys sorted, LF only.  The receipt regenerates
byte-identically.  Predictions are scored mechanically from the computed
values; a miss is recorded next to its value and never edited.

Usage: python research/second_succession/run_succession.py [--receipts DIR] [--check]

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

# `succession` puts the sealed kernel and the sibling trees on the path,
# so it is imported before anything drawn from either.
from succession import ALPHABET, READINGS, all_reports  # noqa: E402
from index import BASE_NAMES  # noqa: E402

RECEIPT_NAME = "succession.json"
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
EXPECTED_ADMITTING_SHORTEST = {"EMPTY": 3, "L": 2, "F": 2}
EXPECTED_BASE_COUNTS = {"EMPTY": 0, "L": 2, "F": 3}
EXPECTED_GENESIS_COUNTS = {
    "L": {"EVERY": 6, "ADMITTING": 2, "CHANGING": 2},
    "F": {"EVERY": 7, "ADMITTING": 3, "CHANGING": 3},
}


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


def _shortest(bases: dict[str, Any], reading: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for base in EXPECTED_SEQUENCES:
        found = bases[base]["readings"][reading]["shortest_splitting_sequence"]
        out[base] = None if found is None else {
            "length": found["length"], "history": found["history"],
        }
    return out


def score(reports: dict[str, Any]) -> dict[str, Any]:
    """Score the computational predictions.  The Lean-side rows, the
    ledger rows and the gate-time row are scored where their evidence
    lives and are named here as scored elsewhere rather than omitted."""
    scored: dict[str, Any] = {}
    bases = reports["bases"]
    sequences = {base: bases[base]["sequences"] for base in EXPECTED_SEQUENCES}
    regimes = {base: bases[base]["distinct_regimes"] for base in EXPECTED_SEQUENCES}
    scored["M-8"] = {
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

    changing = {
        base: {
            "split_regimes": bases[base]["readings"]["CHANGING"]["split_regimes"],
            "law_violations": bases[base]["changing_law_violations"],
            "from_empty_violations": bases[base]["changing_from_empty_violations"],
        }
        for base in EXPECTED_SEQUENCES
    }
    scored["M-9"] = {
        "value": changing,
        "verdict": _verdict(
            all(value == 0 for row in changing.values() for value in row.values())
        ),
    }

    split = {
        reading: {
            base: bases[base]["readings"][reading]["split_regimes"]
            for base in EXPECTED_SEQUENCES
        }
        for reading in READINGS
    }
    every_short = _shortest(bases, "EVERY")
    admitting_short = _shortest(bases, "ADMITTING")
    every_ok = all(
        split["EVERY"][base] >= 1
        and every_short[base] is not None
        and every_short[base]["length"] == 1
        and every_short[base]["history"][0].startswith("Supply(")
        for base in EXPECTED_SEQUENCES
    )
    admitting_ok = all(
        split["ADMITTING"][base] >= 1
        and admitting_short[base] is not None
        and admitting_short[base]["length"] == EXPECTED_ADMITTING_SHORTEST[base]
        for base in EXPECTED_SEQUENCES
    )
    scored["M-10"] = {
        "value": {
            "split_regimes": {r: split[r] for r in ("EVERY", "ADMITTING")},
            "shortest_every": every_short,
            "shortest_admitting": admitting_short,
        },
        "verdict": _verdict(every_ok and admitting_ok),
    }

    scored["M-11"] = {
        "value": {r: split[r] for r in ("EVERY", "ADMITTING")},
        "verdict": _verdict(
            all(split["EVERY"][b] > split["ADMITTING"][b] for b in EXPECTED_SEQUENCES)
        ),
    }

    classes = reports["classes"]
    within = classes["classes_with_two_changing_counts_within_a_base"]
    scored["M-12"] = {
        "value": {
            "within_a_base": within,
            "shared": classes["classes_shared_by_bases"],
            "shared_agreeing_relative": classes["shared_classes_with_agreeing_relative_counts"],
            "shared_two_from_empty": classes["shared_classes_with_two_counts_from_empty"],
        },
        "verdict": _verdict(
            all(value == 0 for value in within.values())
            and classes["classes_shared_by_bases"] >= 1
            and classes["shared_classes_with_agreeing_relative_counts"] == 0
            and classes["shared_classes_with_two_counts_from_empty"] == 0
        ),
    }

    base_counts = {base: bases[base]["base_element_count"] for base in EXPECTED_SEQUENCES}
    genesis_counts = {base: bases[base]["genesis_counts"] for base in EXPECTED_GENESIS_COUNTS}
    scored["M-13"] = {
        "value": {"base_element_counts": base_counts, "genesis_counts": genesis_counts},
        "verdict": _verdict(
            base_counts == EXPECTED_BASE_COUNTS and genesis_counts == EXPECTED_GENESIS_COUNTS
        ),
    }

    for pid, where in (
        ("M-1", "the committed Lean package, checked by verify_lean.py and test_census.py"),
        ("M-2", "the committed Lean package, checked by test_census.py"),
        ("M-3", "the committed Lean package, checked by test_census.py; replayed in lean_witnesses"),
        ("M-4", "the committed Lean package, checked by test_census.py; replayed in lean_witnesses"),
        ("M-5", "the committed Lean package, checked by test_census.py"),
        ("M-6", "the committed Lean package and CLAIM_LEDGER.md, checked by test_census.py"),
        ("M-7", "receipts/lean_axioms.txt, checked by verify_lean.py"),
        ("M-14", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("M-15", "CLAIM_LEDGER.md and this receipt's input_count_claim"),
        ("M-16", "the receipt bytes, --check and test_succession.py; the time in STATUS.md"),
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
        "readings": list(READINGS),
        "reports": reports,
        "rung": "six",
        "write_root": "research/second_succession",
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
    parser = argparse.ArgumentParser(description="Run the rung-six cross-check.")
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
