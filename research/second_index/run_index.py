"""Run the rung-three cross-check and write the receipt.

Deterministic: no timestamp, no environment value, keys sorted, LF only.
The receipt regenerates byte-identically.  Predictions are scored
mechanically from the computed values; a miss is recorded next to its
value and never edited.

Usage: python research/second_index/run_index.py [--receipts DIR] [--check]

``--check`` writes nothing: it rebuilds the payload and compares it with
the committed receipt, so a drifted receipt fails without the run being
able to bless itself by overwriting the bytes it is checked against.  The
sibling rung recorded that defect; this runner is written the other way
round from the start, and the workflow step uses ``--check``.

The two frozen texts are hashed with line endings normalized to LF before
the digest is taken.  A blob in this repository is stored with LF, and a
checkout convention may hand the working tree CRLF; hashing the raw bytes
would then make the receipt depend on the checkout rather than on the
frozen text.  The digest recorded here is therefore the digest of the
frozen bytes as Git holds them, whatever the working tree holds.
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

# `index` puts the sealed kernel and the sibling trees on the path, so it
# is imported before anything drawn from either.
from index import (  # noqa: E402
    ALPHABET,
    BASE_NAMES,
    CROSSCHECK_DEPTH,
    Alphabet,
    all_reports,
    cessation_kinds_over,
    declared_stakes,
)

RECEIPT_NAME = "index.json"

__all__ = [
    "RECEIPT_NAME",
    "all_reports",
    "build",
    "frozen_digest",
    "main",
    "render",
    "score",
    "write",
]

# The values the frozen predictions commit to, transcribed here so the
# scoring is mechanical.  A transcription error is visible as a miss
# against a value the receipt also records, never as a silent pass.
EXPECTED_NODES = {"L": 3928, "F": 14293}
EMPTY_EARLIEST = {
    "chain": 2,
    "free": None,
    "one_sided_total": 2,
    "parity": 2,
    "residue_three": 2,
    "total_apart": 2,
    "total_same": 4,
}
READING_EARLIEST = {
    "chain": 0,
    "free": None,
    "one_sided_total": 0,
    "parity": 0,
    "residue_three": 0,
    "total_apart": 0,
    "total_same": 2,
}
CESSATION_KINDS = ["AdmitInst", "AdmitRuleAll"]
EMPTY_APART_INDEX_SET = ["2", "3", "4"]


def frozen_digest(name: str) -> str:
    raw = (HERE / name).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest()


def _report(reports: list[dict[str, Any]], base: str) -> dict[str, Any]:
    for report in reports:
        if report["base"] == base:
            return report
    raise KeyError(base)


def _stake(report: dict[str, Any], name: str) -> dict[str, Any]:
    stakes = report["stakes"]
    if not isinstance(stakes, dict):
        raise TypeError("a base report must carry a stakes object")
    entry = stakes[name]
    if not isinstance(entry, dict):
        raise TypeError("a stake entry must be an object")
    return entry


def score(reports: list[dict[str, Any]]) -> dict[str, Any]:
    """Score the computational predictions.  The Lean-side rows and the
    gate-time row are scored where their evidence lives -- the committed
    FW-DEF census, the committed axiom log, and `STATUS.md` -- and are
    named here as scored elsewhere rather than silently omitted."""
    empty = _report(reports, "EMPTY")
    scored: dict[str, Any] = {}

    nodes = {base: _report(reports, base)["nodes"] for base in EXPECTED_NODES}
    scored["I-12"] = {
        "value": nodes,
        "verdict": "HIT" if nodes == EXPECTED_NODES else "MISSED",
    }

    empty_nodes = empty["nodes"]
    scored["I-13"] = {
        "value": empty_nodes,
        "verdict": "HIT" if 100 < empty_nodes < 3000 else "MISSED",
    }

    empty_earliest = {
        name: _stake(empty, name)["earliest_index"]
        for name in sorted(EMPTY_EARLIEST)
    }
    scored["I-14"] = {
        "value": empty_earliest,
        "verdict": "HIT" if empty_earliest == EMPTY_EARLIEST else "MISSED",
    }

    reading_earliest = {
        base: {
            name: _stake(_report(reports, base), name)["earliest_index"]
            for name in sorted(READING_EARLIEST)
        }
        for base in ("L", "F")
    }
    scored["I-15"] = {
        "value": reading_earliest,
        "verdict": "HIT"
        if all(value == READING_EARLIEST for value in reading_earliest.values())
        else "MISSED",
    }

    disagreements = sum(
        _stake(report, name)["procedure_disagreements"]
        for report in reports
        for name in sorted(EMPTY_EARLIEST)
    )
    scored["I-16"] = {
        "value": disagreements,
        "verdict": "HIT" if disagreements == 0 else "MISSED",
    }

    violations = sum(
        _stake(report, name)["inert_last_event_violations"]
        for report in reports
        for name in sorted(EMPTY_EARLIEST)
    )
    scored["I-17"] = {
        "value": violations,
        "verdict": "HIT" if violations == 0 else "MISSED",
    }

    kinds = cessation_kinds_over(reports)
    scored["I-18"] = {
        "value": kinds,
        "verdict": "HIT" if kinds == CESSATION_KINDS else "MISSED",
    }

    apart_indices = sorted(_stake(empty, "total_apart")["index_distribution"])
    scored["I-19"] = {
        "value": apart_indices,
        "verdict": "HIT" if apart_indices == EMPTY_APART_INDEX_SET else "MISSED",
    }

    colliding = _stake(empty, "total_apart")["colliding_regimes"]
    scored["I-20"] = {
        "value": colliding,
        "verdict": "HIT" if colliding >= 1 else "MISSED",
    }

    replay_clean = all(report["replay_mismatches"] == 0 for report in reports)
    reach_clean = all(report["crosscheck"]["reach_agrees"] for report in reports)
    scored["I-21"] = {
        "value": {
            "replay_mismatches": sum(
                int(report["replay_mismatches"]) for report in reports
            ),
            "reach_agrees_at_every_base": reach_clean,
            "byte_identity": "checked by --check and by the test suite,"
            " not by this field",
        },
        "verdict": "HIT" if replay_clean and reach_clean else "MISSED",
    }

    for pid, where in (
        ("I-1", "FWDEF_CENSUS.json, checked by test_census.py"),
        ("I-2", "FWDEF_CENSUS.json, checked by test_census.py"),
        ("I-3", "the committed Lean package, checked by verify_lean.py"),
        ("I-4", "the committed Lean package, checked by verify_lean.py"),
        ("I-5", "the committed Lean package, checked by verify_lean.py"),
        ("I-6", "the committed Lean package, checked by verify_lean.py"),
        ("I-7", "the committed Lean package, checked by test_census.py"),
        ("I-8", "the committed Lean package, checked by verify_lean.py"),
        ("I-9", "the committed Lean package, checked by verify_lean.py"),
        ("I-10", "the committed Lean package, checked by verify_lean.py"),
        ("I-11", "the committed Lean package, checked by verify_lean.py"),
        ("I-22", "receipts/lean_axioms.txt, checked by verify_lean.py"),
        ("I-23", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("I-24", "STATUS.md, measured by hand and recorded there"),
    ):
        scored[pid] = {"value": f"scored elsewhere: {where}", "verdict": "ELSEWHERE"}

    scored["I-X"] = {
        "value": "scored by the first later rung that declares a responder",
        "verdict": "PENDING",
    }
    return scored


def build(alphabet: Alphabet = ALPHABET) -> dict[str, Any]:
    reports = all_reports(alphabet)
    return {
        "alphabet": {
            "arities": list(alphabet.arities),
            "crosscheck_depth": CROSSCHECK_DEPTH,
            "fresh_tokens": list(alphabet.fresh_tokens),
            "max_data": alphabet.max_data,
            "max_forms": alphabet.max_forms,
            "max_sequence_length": alphabet.max_length,
            "supply_token": alphabet.supply_token,
        },
        "authority_effect": "None",
        "bases": list(BASE_NAMES),
        "input_count_claim": "none",
        "predictions_scored": score(reports),
        "predictions_sha256": frozen_digest("PREDICTIONS.md"),
        "prompt_sha256": frozen_digest("PROMPT.md"),
        "reports": reports,
        "rung": "three",
        "stakes": [s.name for s in declared_stakes()],
        "write_root": "research/second_index",
    }


def render(payload: dict[str, Any]) -> bytes:
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    return text.encode("utf-8")


def write(payload: dict[str, Any], receipts: pathlib.Path) -> pathlib.Path:
    receipts.mkdir(parents=True, exist_ok=True)
    target = receipts / RECEIPT_NAME
    target.write_bytes(render(payload))
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the rung-three cross-check.")
    parser.add_argument(
        "--receipts", default=str(HERE / "receipts"), help="output directory"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare with the committed receipt and write nothing",
    )
    args = parser.parse_args()
    receipts = pathlib.Path(args.receipts)
    payload = build()
    fresh = render(payload)
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
        if len(fresh) > 1_000_000:
            print("NOTE: the receipt exceeds one megabyte and must be split")
    scored = payload["predictions_scored"]
    if not isinstance(scored, dict):
        raise TypeError("predictions_scored must be an object")
    for pid in sorted(scored, key=lambda name: (len(name), name)):
        print(f"  {pid}: {scored[pid]['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
