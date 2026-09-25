"""Run the rung-ten cross-check and write the receipt.

A hand copy of the shape of `research/second_profile/run_profile.py`,
with this rung's measurements and scoring.  Deterministic: no timestamp,
no environment value, keys sorted, LF only.  The receipt regenerates
byte-identically.  Predictions are scored mechanically from the computed
values; a miss is recorded next to its value and never edited.

Usage: python research/second_response/run_response.py [--receipts DIR] [--check]

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

# `response_rows` puts the sealed kernel and the sibling trees on the path,
# so it is imported before anything drawn from either.
from response_rows import ALPHABET, MEASURES, all_reports  # noqa: E402
from index import BASE_NAMES  # noqa: E402

RECEIPT_NAME = "response.json"
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
EXPECTED_ALL_REGIMES = 2316
EXPECTED_ALL_CLASSES = 402
# R-15: the least length reaching a regime whose adjacency graph has an edge.
EXPECTED_EDGE = {"EMPTY": 3, "L": 1, "F": 0}
# R-16: the least length reaching a demand with two tie classes.
EXPECTED_BRANCH = {
    "mu1": {"EMPTY": 2, "L": 0, "F": 0},
    "mu2": {"EMPTY": 3, "L": 1, "F": 1},
}
# R-18: the changes of the exhausted count by kind, over all three bases.
EXPECTED_EXHAUSTION_CHANGES = {
    "AdmitDatum": [-1, 0],
    "AdmitForm": [1],
    "AdmitInst": [-1, 0, 1],
    "AdmitRuleAll": [0, 1],
    "Impose": [0],
    "Supply": [0],
}
# R-19: least lengths for an exhausted form, and for one beside holding two.
EXPECTED_EXHAUSTED_FIRST = {"EMPTY": 1, "L": 1, "F": 1}
EXPECTED_EXHAUSTED_WITH_TWO: dict[str, int | None] = {"EMPTY": None, "L": 3, "F": 3}


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


def _per_measure(bases: dict[str, Any], key: str) -> dict[str, dict[str, Any]]:
    return {
        m: {base: bases[base]["measures"][m][key] for base in EXPECTED_SEQUENCES}
        for m in MEASURES
    }


def _all_zero(table: dict[str, dict[str, Any]]) -> bool:
    return all(v == 0 for row in table.values() for v in row.values())


def _all_positive(table: dict[str, dict[str, Any]], bases: tuple[str, ...]) -> bool:
    return all(table[m][b] >= 1 for m in MEASURES for b in bases)


def score(reports: dict[str, Any]) -> dict[str, Any]:
    """Score the computational predictions.  The Lean-side rows, the
    ledger rows and the gate-time row are scored where their evidence
    lives and are named here as scored elsewhere rather than omitted."""
    scored: dict[str, Any] = {}
    bases = reports["bases"]
    classes = reports["classes"]
    union = classes["over_all_bases"]
    sequences = _per_base(bases, "sequences")
    regimes = _per_base(bases, "distinct_regimes")
    mismatches = _per_base(bases, "replay_mismatches")
    scored["R-9"] = {
        "value": {
            "sequences": sequences,
            "distinct_regimes": regimes,
            "replay_mismatches": mismatches,
            "distinct_regimes_over_all_bases": classes["distinct_regimes_over_all_bases"],
            "classes_over_all_bases": union["classes"],
            "key_brute_disagreements": classes["key_brute_disagreements"],
        },
        "verdict": _verdict(
            sequences == EXPECTED_SEQUENCES
            and regimes == EXPECTED_REGIMES
            and all(value == 0 for value in mismatches.values())
            and classes["distinct_regimes_over_all_bases"] == EXPECTED_ALL_REGIMES
            and union["classes"] == EXPECTED_ALL_CLASSES
            and classes["key_brute_disagreements"] == 0
        ),
    }

    inside = _per_base(bases, "regimes_in_domain")
    outside = _per_base(bases, "regimes_outside_domain")
    odd_out = _per_base(bases, "outside_domain_without_rules")
    odd_in = _per_base(bases, "inside_domain_with_rules")
    scored["R-10"] = {
        "value": {
            "regimes_in_domain": inside,
            "regimes_outside_domain": outside,
            "outside_domain_without_rules": odd_out,
            "inside_domain_with_rules": odd_in,
        },
        "verdict": _verdict(
            all(v > 0 for v in inside.values())
            and all(v > 0 for v in outside.values())
            and all(v == 0 for v in odd_out.values())
            and all(v == 0 for v in odd_in.values())
        ),
    }

    refused = _per_measure(bases, "refused")
    split = {b: bases[b]["refinement"]["refusal_disagreements"] for b in EXPECTED_SEQUENCES}
    scored["R-11"] = {
        "value": {"refused": refused, "refusal_disagreements": split},
        "verdict": _verdict(
            all(refused[m]["EMPTY"] == 0 for m in MEASURES)
            and _all_positive(refused, ("L", "F"))
            and all(v == 0 for v in split.values())
        ),
    }

    rule = _per_measure(bases, "responses_with_rule_item")
    nomention = _per_measure(bases, "responses_mentioning_no_demanded_datum")
    unmentioned = _per_measure(bases, "responses_moving_an_unmentioned_pair")
    scored["R-12"] = {
        "value": {
            "responses_with_rule_item": rule,
            "responses_mentioning_no_demanded_datum": nomention,
            "responses_moving_an_unmentioned_pair": unmentioned,
        },
        "verdict": _verdict(
            _all_zero(rule) and _all_zero(nomention) and _all_zero(unmentioned)
        ),
    }

    not_apart = _per_measure(bases, "responses_not_moving_their_demand_apart")
    together = _per_measure(bases, "responses_moving_a_pair_together")
    scored["R-13"] = {
        "value": {
            "responses_not_moving_their_demand_apart": not_apart,
            "responses_moving_a_pair_together": together,
        },
        "verdict": _verdict(
            _all_zero(not_apart)
            and all(together[m]["EMPTY"] == 0 for m in MEASURES)
            and _all_positive(together, ("L", "F"))
        ),
    }

    mismatch = _per_measure(bases, "reach_two_pair_mismatches")
    violations = _per_measure(bases, "reach_class_violations")
    empty_reach = _per_measure(bases, "responses_with_empty_reach")
    full_reach = _per_measure(bases, "responses_with_nonempty_reach")
    every = tuple(EXPECTED_SEQUENCES)
    scored["R-14"] = {
        "value": {
            "reach_two_pair_mismatches": mismatch,
            "reach_class_violations": violations,
            "responses_with_empty_reach": empty_reach,
            "responses_with_nonempty_reach": full_reach,
        },
        "verdict": _verdict(
            _all_zero(mismatch)
            and _all_zero(violations)
            and _all_positive(empty_reach, every)
            and _all_positive(full_reach, every)
        ),
    }

    edge = _per_measure(bases, "least_length_with_an_edge")
    distance = _per_measure(bases, "largest_finite_distance")
    scored["R-15"] = {
        "value": {"least_length_with_an_edge": edge, "largest_finite_distance": distance},
        "verdict": _verdict(
            all(edge[m] == EXPECTED_EDGE for m in MEASURES)
            and all(max(distance[m].values()) >= 2 for m in MEASURES)
        ),
    }

    branch = _per_measure(bases, "least_length_with_two_tie_classes")
    subset = {b: bases[b]["refinement"]["mu2_not_among_mu1"] for b in EXPECTED_SEQUENCES}
    ties_one = _per_measure(bases, "demands_with_tie_count_one")
    scored["R-16"] = {
        "value": {
            "least_length_with_two_tie_classes": branch,
            "mu2_not_among_mu1": subset,
            "demands_with_tie_count_one": ties_one,
        },
        "verdict": _verdict(
            branch == EXPECTED_BRANCH
            and all(v == 0 for v in subset.values())
            and _all_positive(ties_one, ("L", "F"))
        ),
    }

    lumped = {base: dict(classes["within_base"][base]) for base in EXPECTED_SEQUENCES}
    lumped["all"] = dict(union)
    scored["R-17"] = {
        "value": lumped,
        "verdict": _verdict(
            all(
                value == 0
                for row in lumped.values()
                for key, value in row.items()
                if key.startswith("classes_with_two_values_of_")
            )
        ),
    }

    ex = {base: bases[base]["exhaustion"] for base in EXPECTED_SEQUENCES}
    changes = reports["exhaustion_changes_over_all_bases"]
    scored["R-18"] = {
        "value": {
            "holds_two_mismatches": {b: ex[b]["holds_two_mismatches"] for b in ex},
            "ruled_forms_distinguishing": {
                b: ex[b]["ruled_forms_distinguishing"] for b in ex
            },
            "changes_by_kind": changes,
        },
        "verdict": _verdict(
            all(ex[b]["holds_two_mismatches"] == 0 for b in ex)
            and all(ex[b]["ruled_forms_distinguishing"] == 0 for b in ex)
            and changes == EXPECTED_EXHAUSTION_CHANGES
        ),
    }

    first = {b: ex[b]["least_length_with_an_exhausted_form"] for b in ex}
    with_two = {b: ex[b]["least_length_holding_two_with_an_exhausted_form"] for b in ex}
    scored["R-19"] = {
        "value": {
            "least_length_with_an_exhausted_form": first,
            "least_length_holding_two_with_an_exhausted_form": with_two,
        },
        "verdict": _verdict(
            first == EXPECTED_EXHAUSTED_FIRST and with_two == EXPECTED_EXHAUSTED_WITH_TWO
        ),
    }

    cross = reports["crosscheck_empty_base"]
    failures = _per_measure(bases, "reference_validity_failures")
    scored["R-20"] = {
        "value": {"crosscheck_empty_base": cross, "reference_validity_failures": failures},
        "verdict": _verdict(
            cross["situations"] > 0
            and cross["response_disagreements"] == 0
            and cross["refusal_disagreements"] == 0
            and cross["tie_partition_disagreements"] == 0
            and _all_zero(failures)
        ),
    }

    for pid, where in (
        ("R-1", "the committed Lean package, checked by verify_lean.py and test_census.py"),
        ("R-2", "the committed Lean package, checked by test_census.py"),
        ("R-3", "the committed Lean package, checked by test_census.py"),
        ("R-4", "the committed Lean package, checked by test_census.py"),
        ("R-5", "the committed Lean package, checked by test_census.py"),
        ("R-6", "the committed Lean package, checked by test_census.py"),
        ("R-7", "the committed Lean package, checked by test_census.py; written in the Python grammar in lean_witnesses"),
        ("R-8", "receipts/lean_axioms.txt, checked by verify_lean.py"),
        ("R-21", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("R-22", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("R-23", "CLAIM_LEDGER.md and this receipt's input_count_claim"),
        ("R-24", "the receipt bytes, --check and test_response.py; the time in STATUS.md"),
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
        "rung": "ten",
        "write_root": "research/second_response",
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
    parser = argparse.ArgumentParser(description="Run the rung-ten cross-check.")
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
