"""Run the rung-four cross-check and write the receipt.

Deterministic: no timestamp, no environment value, keys sorted, LF only.
The receipt regenerates byte-identically.  Predictions are scored
mechanically from the computed values; a miss is recorded next to its
value and never edited.

Usage: python research/second_iso/run_iso_index.py [--receipts DIR] [--check]

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

# `iso_index` puts the sealed kernel and the sibling trees on the path, so
# it is imported before anything drawn from either.
from iso_index import (  # noqa: E402
    ALPHABET,
    ORBIT_BOUND,
    RENAMED_SUPPLY_TOKEN,
    all_reports,
)
from index import BASE_NAMES, declared_stakes  # noqa: E402

RECEIPT_NAME = "iso_index.json"
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
EXPECTED_NODES = {"EMPTY": 577, "L": 3928, "F": 14293}
UNIFORM_LABELLED = ("free", "one_sided_total", "total_apart", "total_same")
NOT_UNIFORM = ("chain", "parity", "residue_three")
EXPECTED_AUTOMORPHISM_EXTREMES = (1, 24)
EXPECTED_EXHIBITED = {
    "P": {"length": 8, "data": 3, "forms": 2,
          "first_counts": {"chain": {"P1": None, "P2": 8},
                           "parity": {"P1": None, "P2": 8}}},
    "Q": {"length": 11, "data": 4, "forms": 3,
          "first_counts": {"residue_three": {"Q1": None, "Q2": 11}}},
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


def score(reports: dict[str, Any]) -> dict[str, Any]:
    """Score the computational predictions.  The Lean-side rows and the
    gate-time row are scored where their evidence lives -- the committed
    FW-DEF census, the committed axiom log, and `STATUS.md` -- and are
    named here as scored elsewhere rather than silently omitted."""
    scored: dict[str, Any] = {}
    bases = reports["bases"]
    nodes = {base: bases[base]["nodes"] for base in EXPECTED_NODES}
    mismatches = sum(int(bases[base]["replay_mismatches"]) for base in bases)
    scored["J-10"] = {
        "value": {"nodes": nodes, "replay_mismatches": mismatches},
        "verdict": _verdict(nodes == EXPECTED_NODES and mismatches == 0),
    }

    split = reports["class_split"]
    disagreements = reports["key_partition_disagreements"]
    classes = split["classes"]
    distinct = reports["distinct_regimes"]
    scored["J-11"] = {
        "value": {"disagreements": disagreements, "classes": classes,
                  "distinct_regimes": distinct},
        "verdict": _verdict(disagreements == 0 and classes < distinct),
    }

    autos = reports["automorphisms"]
    extremes = (autos["smallest"], autos["largest"])
    scored["J-12"] = {
        "value": {"disagreements": autos["disagreements"],
                  "smallest": extremes[0], "largest": extremes[1]},
        "verdict": _verdict(
            autos["disagreements"] == 0 and extremes == EXPECTED_AUTOMORPHISM_EXTREMES
        ),
    }

    reached = split["reached_split_classes"]
    orbital = split["orbit_split_classes"]
    uniform_values = {name: [reached[name], orbital[name]] for name in UNIFORM_LABELLED}
    scored["J-13"] = {
        "value": uniform_values,
        "verdict": _verdict(all(v == [0, 0] for v in uniform_values.values())),
    }
    other_values = {name: [reached[name], orbital[name]] for name in NOT_UNIFORM}
    scored["J-14"] = {
        "value": other_values,
        "verdict": _verdict(
            all(v[0] >= 1 and v[1] >= 1 for v in other_values.values())
        ),
    }

    traj = reports["trajectory"]
    varying = traj["trajectory_classes_with_varying_count"]
    scored["J-15"] = {
        "value": {"varying": varying,
                  "classes_with_two_members": traj["trajectory_classes_with_two_members"]},
        "verdict": _verdict(
            all(count == 0 for count in varying.values())
            and traj["trajectory_classes_with_two_members"] >= 1
        ),
    }
    final = traj["final_classes_with_two_counts"]
    scored["J-16"] = {
        "value": final,
        "verdict": _verdict(
            final["free"] == 0
            and all(final[name] >= 1 for name in final if name != "free")
        ),
    }

    tokens = reports["tokens"]
    scored["J-17"] = {
        "value": {
            "moved_counts": tokens["sequences_with_a_moved_count"],
            "moved_classes": tokens["sequences_with_a_moved_class"],
            "changed_presentations": tokens["sequences_whose_presentation_changed"],
        },
        "verdict": _verdict(
            tokens["sequences_with_a_moved_count"] == 0
            and tokens["sequences_with_a_moved_class"] == 0
            and tokens["sequences_whose_presentation_changed"] >= 1
        ),
    }

    exhibited = reports["exhibited"]
    shown = {
        pair: {key: exhibited[pair][key] for key in ("length", "data", "forms", "first_counts")}
        for pair in EXPECTED_EXHIBITED
    }
    scored["J-18"] = {
        "value": {pair: dict(shown[pair], prefix_pairs_in_two_classes=exhibited[pair][
            "prefix_pairs_in_two_classes"]) for pair in shown},
        "verdict": _verdict(
            shown == EXPECTED_EXHIBITED
            and all(exhibited[p]["prefix_pairs_in_two_classes"] == 0 for p in exhibited)
        ),
    }

    for pid, where in (
        ("J-1", "the committed Lean package, checked by verify_lean.py"),
        ("J-2", "the committed Lean package, checked by verify_lean.py"),
        ("J-3", "FWDEF_CENSUS.json, checked by test_census.py"),
        ("J-4", "the committed Lean package, checked by test_census.py"),
        ("J-5", "the committed Lean package, checked by test_census.py"),
        ("J-6", "the committed Lean package, checked by verify_lean.py"),
        ("J-7", "the committed Lean package, checked by test_census.py"),
        ("J-8", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("J-9", "FWDEF_CENSUS.json, checked by test_census.py"),
        ("J-19", "the receipt bytes, checked by --check and by test_iso_index.py"),
        ("J-20", "receipts/lean_axioms.txt, checked by verify_lean.py"),
        ("J-21", "CLAIM_LEDGER.md, checked by test_census.py"),
        ("J-22", "STATUS.md, measured by hand and recorded there"),
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
        "renamed_supply_token": RENAMED_SUPPLY_TOKEN,
        "reports": reports,
        "rung": "four",
        "stakes": [s.name for s in declared_stakes()],
        "write_root": "research/second_iso",
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
    parser = argparse.ArgumentParser(description="Run the rung-four cross-check.")
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
