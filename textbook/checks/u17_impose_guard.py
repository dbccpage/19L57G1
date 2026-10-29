"""Unit 17 check: the guard on `Impose` and what it keeps true.

Runs Genesis's own Python model. This is sample computation, not a proof;
the guard is a definition (Basic.stepE, impose case) and the invariant is
the book's Lean. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u17_impose_guard.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.engine import GENESIS_F, GENESIS_L  # noqa: E402
from derivation.model import (  # noqa: E402
    AdmissionError,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    Event,
    Impose,
    Regime,
    replay,
    step,
)


def main() -> int:
    failures: list[object] = []
    L = replay(GENESIS_L)
    F = replay(GENESIS_F)

    # 1. The accepted demand, and the three rejected shapes.
    ok = step(L, Impose(0, 1))
    print(f"Impose(0, 1) on reading L: reqs={sorted(ok.reqs)}, other fields "
          f"unchanged: {ok.data == L.data and ok.forms == L.forms}")
    if ok.reqs != frozenset({(0, 1)}) or ok.data != L.data:
        failures.append("accept")
    if step(ok, Impose(0, 1)) != ok:
        failures.append("repeated demand changed state")
    malformed = Regime(L.data, (), frozenset(), frozenset(), frozenset({(1, 0)}))
    still_malformed = step(malformed, Impose(0, 1))
    print(f"repeated demand unchanged; raw reversed pair survives: {sorted(still_malformed.reqs)}")
    if still_malformed.reqs != frozenset({(1, 0), (0, 1)}):
        failures.append("guard silently repaired base")
    rejected = 0
    for r, bad in ((L, Impose(0, 0)), (L, Impose(1, 1)), (L, Impose(1, 0)),
                   (L, Impose(0, 2)), (F, Impose(2, 2)), (F, Impose(2, 1)),
                   (F, Impose(1, 3))):
        try:
            step(r, bad)
            failures.append(("accepted", bad))
        except AdmissionError as e:
            rejected += 1
            print(f"{bad}: rejected ({e})")
    print(f"rejected: {rejected} of 7")

    # 2. Every demand a regime can carry is strictly ordered, on every
    # regime reached by replay of histories up to length 5 over a small
    # alphabet (the guard is the only way a demand enters).
    alphabet: list[Event] = [AdmitDatum("x"), AdmitDatum("y"), AdmitDatum("z"),
                             AdmitForm(1), AdmitInst(0, (0,)),
                             Impose(0, 1), Impose(1, 2), Impose(0, 2),
                             Impose(1, 1), Impose(2, 0)]
    histories = admissible = demands = 0
    for k in range(6):
        for h in itertools.product(alphabet, repeat=k):
            histories += 1
            try:
                r = replay(h)
            except AdmissionError:
                continue
            admissible += 1
            for (i, j) in r.reqs:
                demands += 1
                if not (0 <= i < j < len(r.data)):
                    failures.append(("unordered", h, (i, j)))
    print(f"histories: {histories}; admissible: {admissible}; recorded "
          f"demands: {demands}, all with i < j < data")

    # 3. The demand is on indices, not tokens: the same guard accepts the
    # demand in reading F at (1, 2) and rejects (1, 2) in reading L.
    try:
        step(L, Impose(1, 2))
        failures.append("L accepts (1,2)")
    except AdmissionError:
        pass
    fr = step(F, Impose(1, 2))
    print(f"reading F Impose(1, 2): reqs={sorted(fr.reqs)}; reading L "
          f"Impose(1, 2): rejected (only two data)")
    if fr.reqs != frozenset({(1, 2)}):
        failures.append("F")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
