"""Write the deterministic receipt for rung zero.

Usage: python research/second_inheritance/run_inheritance.py [--out PATH]

No timestamp, no environment value.  The frozen texts (the seed, the
rung's question, the predictions) are hashed at run time so an edit after
the freeze shows in the receipt.  Prediction scoring is mechanical.
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from inheritance import (  # noqa: E402
    MAX_DATA,
    MAX_SUPPLIES,
    REPO,
    absent_trees,
    all_free_growth,
    grammar_census,
    landed_replay_commit,
    remaining_inputs,
    replay_challenges,
    replay_closed,
    replay_dual_summary,
    replay_standing_summary,
    replay_two_sided_receipts,
    snapshot_commit,
    supplies_are_inert,
)

if str(REPO / "code") not in sys.path:
    sys.path.insert(0, str(REPO / "code"))
from derivation.engine import READINGS  # noqa: E402
from derivation.export import Json, write_json  # noqa: E402


def _sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _j(value: object) -> Json:
    if isinstance(value, dict):
        return {str(k): _j(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_j(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"not JSON: {value!r}")


def build_all() -> dict[str, Json]:
    snapshot = snapshot_commit()
    absent = absent_trees(snapshot)
    challenges = replay_challenges()
    closed = [replay_closed(rd) for rd in READINGS]
    dual_summary = replay_dual_summary()
    standing_summary = replay_standing_summary()
    two_sided_receipts = replay_two_sided_receipts()
    census = grammar_census()
    remaining = remaining_inputs(absent)
    supplies = [supplies_are_inert(rd) for rd in READINGS]
    growth = [all_free_growth(rd) for rd in READINGS]

    r1 = bool(challenges["byte_identical"]) and all(bool(c["match"]) for c in closed) and bool(dual_summary["byte_identical"])
    r2 = (
        census["sealed_event_count"] == 6
        and census["sealed_state_preserving_count"] == 1
        and census["sealed_policy_count"] == 2
        and census["dual_declared_count"] == 3
        and all(not bool(a["present_at_snapshot"]) for a in absent)
    )
    r3 = all(bool(s["regime_unchanged"]) for s in supplies) and all(
        bool(g["every_state_totally_collapsed"]) and int(str(g["forms_ever_admitted"])) == 0
        and int(str(g["responses"])) == 0 and bool(g["single_chain"])
        and bool(g["all_pair_labels_evaluated"])
        and all(
            int(str(row["demands_all_free"])) == 0
            and int(str(row["demands_undeclared"])) == 0
            for row in (g["chain"] if isinstance(g["chain"], list) else [])
            if isinstance(row, dict)
        )
        for g in growth
    )
    verdicts = {"R0-1": r1, "R0-2": r2, "R0-3": r3}
    return {
        "authority_effect": "None",
        "rung": 0,
        "snapshot_commit": snapshot,
        "bounds": {"max_items": 2, "max_arity": 2, "max_data": MAX_DATA, "max_supplies": MAX_SUPPLIES,
                   "sealed_closed_max_rounds": 15, "sealed_closed_guard": 1200},
        "seed_sha256": _sha(REPO / "research" / "second" / "SEED.md"),
        "prompt_sha256": _sha(HERE / "PROMPT.md"),
        "predictions_sha256": _sha(HERE / "PREDICTIONS.md"),
        "replay": {"challenges": _j(challenges), "closed_baselines": _j(closed), "dual_summary": _j(dual_summary),
                   "absent_at_snapshot": _j(absent),
                   "landed_commitments": {
                       "base_commit": landed_replay_commit(),
                       "standing_summary": _j(standing_summary),
                       "two_sided_receipts": _j(two_sided_receipts),
                       "custody_closed": bool(standing_summary["byte_identical"])
                       and bool(two_sided_receipts["summary_byte_identical"])
                       and bool(two_sided_receipts["full_content_identical"]),
                   }},
        "census": _j(census),
        "remaining_declared_inputs": _j(remaining),
        "inertia": {"supplies": _j(supplies), "all_free_growth": _j(growth)},
        "predictions_scored": {k: {"hit": v, "verdict": "HIT" if v else "MISS"} for k, v in verdicts.items()},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the rung-zero receipt.")
    parser.add_argument("--out", type=pathlib.Path, default=HERE / "receipts" / "inheritance.json")
    args = parser.parse_args()
    payload = build_all()
    write_json(args.out, payload)
    scored = payload["predictions_scored"]
    assert isinstance(scored, dict)
    for k in sorted(scored):
        v = scored[k]
        assert isinstance(v, dict)
        print(f"{k}: {v['verdict']}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
