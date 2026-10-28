"""Unit 38 check: five re-admission disciplines on one token.

Replays the two-admission history under each discipline of Genesis's
`refusal` module, shows the swap test and the separability test on the
resulting states, recomputes the bounded reachability table and compares
it with `artifacts/refusal.json`. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u38_refusal.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.refusal import (  # noqa: E402
    DISCIPLINES, EMPTY, Adm, discipline_report, equivalence_check, orientation_check,
    separable, step, swap_two,
)


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "refusal.json").read_text())
    hist = [Adm("<>"), Adm("<>")]
    for name, readmit in DISCIPLINES.items():
        s = EMPTY
        for e in hist:
            s = step(s, e, readmit)
        two = len(s.data) == 2
        print(f"{name:15s} after two admissions: data {list(s.data)}, tags {sorted(s.tags)}, "
              f"refusals {s.refusals}; "
              + (f"swap-invariant {swap_two(s) == s}, separable(0, 1) {separable(s, 0, 1)}" if two
                 else "one datum"))
    occ = EMPTY
    for e in hist:
        occ = step(occ, e, DISCIPLINES["silent"], occurrence=True)
    ru = EMPTY
    for e in hist:
        ru = step(ru, e, DISCIPLINES["reify_untagged"])
    print(f"occurrence admission gives the reify_untagged state: {occ == ru}")
    if occ != ru:
        failures.append("occurrence")
    ori = orientation_check()
    if ori != art["orientation"]:
        failures.append("orientation")
    eq = equivalence_check(7)
    print(f"equivalence over 7 events: {eq}")
    if eq != art["equivalence"]:
        failures.append("equivalence")
    print("min events to carrier 2 / state difference / witnessed / oriented / witness without instances:")
    for row in art["disciplines"]:
        rep = discipline_report(row["discipline"], row["tokens"], row["max_events"])
        m = rep["min_events_to"]
        print(f"  {row['discipline']:15s} {m['carrier_2']} / {m['readmission_state_difference']} / "
              f"{m['witnessed_pair']} / {m['oriented_witnessed_pair']} / {m['witness_without_instances']}"
              f"  ({rep['states_reached']} states): {rep['outcome']}")
        if rep != row:
            failures.append(f"table {row['discipline']}")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
