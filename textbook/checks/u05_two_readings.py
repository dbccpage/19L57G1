"""Unit 05 check: the two readings of what is admitted at genesis.

Runs Genesis's own Python model on its two recorded histories. Sample
computation, not a proof; the replay theorems are
Derivation.historyL_replays and historyF_replays. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u05_two_readings.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.engine import GENESIS_F, GENESIS_L, READING_F, READING_L  # noqa: E402
from derivation.model import AdmitDatum, Event, Impose, Supply, replay  # noqa: E402


def main() -> int:
    failures: list[object] = []

    # 1. The two readings end in two different regimes, one datum apart.
    rl = replay(GENESIS_L)
    rf = replay(GENESIS_F)
    print(f"reading L data: {rl.data}")
    print(f"reading F data: {rf.data}")
    if rl.data != ("<a>", "<ab>") or rf.data != ("<>", "<a>", "<ab>"):
        failures.append(("readings", rl.data, rf.data))
    if rl == rf:
        failures.append("readings coincide")

    # 2. The Challenge-3 demand names the pair by position, so its indices
    # depend on the reading: (0, 1) in L, (1, 2) in F.
    print(f"targets: L {READING_L.target}, F {READING_F.target}")
    r3l = replay(GENESIS_L + (Impose(*READING_L.target),))
    r3f = replay(GENESIS_F + (Impose(*READING_F.target),))
    print(f"after the demand: L reqs {sorted(r3l.reqs)}, F reqs {sorted(r3f.reqs)}")
    if sorted(r3l.reqs) != [(0, 1)] or sorted(r3f.reqs) != [(1, 2)]:
        failures.append(("reqs", r3l.reqs, r3f.reqs))
    if rl.data[0:1] != ("<a>",) or rf.data[1:2] != ("<a>",):
        failures.append("target index does not name <a>")

    # 3. The demand of one reading is ill formed in the other.
    try:
        replay(GENESIS_L + (Impose(1, 2),))
        failures.append("Impose(1, 2) accepted in reading L")
        cross = "accepted"
    except Exception as exc:  # AdmissionError
        cross = type(exc).__name__
    print(f"Impose(1, 2) in reading L: {cross}")

    # 4. Challenge 1 sub-readings: admit <a> on supply, or not. Both reach
    # the same regime once Challenge 2 retains <a> and <ab>.
    bare: tuple[Event, ...] = (Supply("<>"), Supply("<a>"))
    plus: tuple[Event, ...] = bare + (AdmitDatum("<a>"),)
    tail: tuple[Event, ...] = (Supply("<a>"), Supply("<ab>"),
                               AdmitDatum("<a>"), AdmitDatum("<ab>"))
    c1 = (replay(bare).data, replay(plus).data)
    c2 = (replay(bare + tail), replay(plus + tail))
    print(f"challenge 1 data, bare / with admission: {c1[0]} / {c1[1]}")
    print(f"challenge 2 close, same regime: {c2[0] == c2[1]}; data {c2[0].data}")
    if c1 != ((), ("<a>",)) or c2[0] != c2[1] or c2[0].data != ("<a>", "<ab>"):
        failures.append(("sub-readings", c1, c2))

    # 5. The committed artifact records the same convergence.
    art = json.loads((ROOT / "artifacts" / "challenges.json").read_text("utf-8"))
    conv = art["challenge1"]["sub_readings_converge_at_challenge2"]
    print(f"artifacts/challenges.json challenge1 converge flag: {conv}")
    if conv is not True:
        failures.append(("artifact", conv))

    # 6. Reading L and reading F do not converge: <> stays admitted in F.
    print(f"L and F converge: {rl == rf} (they do not; the question stays open)")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
