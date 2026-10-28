"""Unit 06 check: re-admitting an admitted token designates, it does not add.

Runs Genesis's own Python model. Sample computation; the convention is
declared (code/derivation/model.py, AdmitDatum docstring) and its Lean
form is Erasure.stepT. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u06_readmission.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from derivation.model import EMPTY, AdmitDatum, AdmitForm, Event, Supply, replay, step  # noqa: E402

TOKENS = ("<>", "<a>", "<ab>")


def main() -> int:
    failures: list[object] = []

    # 1. Twice is once.
    r = replay([AdmitDatum("<a>"), AdmitDatum("<a>")])
    print(f"admit <a> twice: data = {r.data}")
    if r.data != ("<a>",):
        failures.append(("twice", r.data))

    # 2. Re-admission returns the very same regime object.
    r1 = replay([AdmitDatum("<a>"), AdmitForm(1)])
    same = step(r1, AdmitDatum("<a>")) is r1
    print(f"re-admission returns the same object: {same}")
    if not same:
        failures.append("re-admission copied")

    # 3. Every history of up to four admissions over three tokens admits
    # exactly the distinct tokens, in first-admission order.
    cases = 0
    for k in range(5):
        for seq in itertools.product(TOKENS, repeat=k):
            cases += 1
            h: list[Event] = [AdmitDatum(t) for t in seq]
            want = tuple(dict.fromkeys(seq))
            got = replay(h).data
            if got != want:
                failures.append(("order", seq, got))
    print(f"admission histories checked: {cases}; data = distinct tokens in first-admission order")

    # 4. Different first-admission orders are different regimes (order is
    # kept by the token-aware state; Unit 11 says what that means).
    ra = replay([AdmitDatum("<a>"), AdmitDatum("<ab>")])
    rb = replay([AdmitDatum("<ab>"), AdmitDatum("<a>")])
    print(f"<a>,<ab> vs <ab>,<a>: equal regimes? {ra == rb}; counts {len(ra.data)}, {len(rb.data)}")
    if ra == rb or len(ra.data) != len(rb.data):
        failures.append("order")

    # 5. A re-admission behaves exactly like a supply of that token.
    for tok in TOKENS:
        base = replay([AdmitDatum(t) for t in TOKENS])
        if step(base, AdmitDatum(tok)) != step(base, Supply(tok)):
            failures.append(("readmit vs supply", tok))
    print("on a regime holding all three tokens, re-admission == supply: checked")

    # 6. Without the convention the count would differ: a naive counter.
    naive = sum(isinstance(e, AdmitDatum) for e in [AdmitDatum("<a>"), AdmitDatum("<a>")])
    print(f"naive count of admission events: {naive}; Genesis data count: {len(r.data)}")
    if naive != 2 or len(r.data) != 1:
        failures.append("naive")

    print(f"EMPTY.data = {EMPTY.data}; failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
