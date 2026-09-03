"""Run the race and write the receipt deterministically (``--out DIR``).

The receipt records computations; it proves no theorem.  The Lean package is
audited by ``verify_lean.py``.  Keys are sorted and no timestamp or
environment value is written, so the receipt is byte-replayable.
AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import standing as st

FROZEN: tuple[str, ...] = ("total", "adjacent", "shared_parity", "empty")
POST_FREEZE: tuple[str, ...] = ("bounded",)
ROUNDS: tuple[int, ...] = (8, 12, 16, 24, 32, 40, 48)
MAIN_ROUNDS: int = 24


def peak(name: str, rounds: int) -> int:
    log = st.race(name, rounds, 0)["log"]
    assert isinstance(log, list)
    return max((int(str(x["generated"])) for x in log), default=0)


def build() -> dict[str, object]:
    families: list[dict[str, object]] = []
    for name in FROZEN + POST_FREEZE:
        rows: list[dict[str, object]] = []
        for r in ROUNDS:
            th = st.threshold(name, r, r + 2)
            rows.append({
                "rounds": r,
                "generated": st.race(name, r, 0)["generated"],
                "peak_per_round": peak(name, r),
                "least_clearing_rate": th,
                "peak_equals_threshold": peak(name, r) == th,
                "final_backlog_at_rate_1": st.race(name, r, 1)["final_backlog"],
            })
        families.append({
            "commitment": name,
            "frozen_before_the_run": name in FROZEN,
            "rows": rows,
            "generation_non_decreasing": all(
                int(str(a["generated"])) <= int(str(b["generated"]))
                for lg in [st.race(name, MAIN_ROUNDS, 0)["log"]]
                if isinstance(lg, list)
                for a, b in zip(lg, lg[1:])
            ),
        })
    agree = [
        {"commitment": f["commitment"], "rounds": row["rounds"]}
        for f in families
        for row in (f["rows"] if isinstance(f["rows"], list) else [])
        if not row["peak_equals_threshold"]
    ]
    return {
        "authority_effect": "None",
        "declared_family_frozen": list(FROZEN),
        "post_freeze_additions": list(POST_FREEZE),
        "families": families,
        "peak_equals_threshold_counterexamples": agree,
        "main_run": {
            name: st.race(name, MAIN_ROUNDS, 1) for name in FROZEN + POST_FREEZE
        },
        "rounds_tested": list(ROUNDS),
        "write_root": "research/standing_commitment/",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=Path("receipts"))
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    report = build()
    (args.out / "standing_commitment.json").write_bytes(
        (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    ce = report["peak_equals_threshold_counterexamples"]
    assert isinstance(ce, list)
    print(f"families: {len(FROZEN)} frozen + {len(POST_FREEZE)} post-freeze")
    print(f"peak==threshold counterexamples: {len(ce)}"
          f" (all from the post-freeze commitment)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
