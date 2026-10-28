"""Unit 04 check: the only way a ledger changes is by an event.

Runs Genesis's own Python model. Sample computation, not a proof; the
structural point is a property of the declared grammar (paper section 4).
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u04_no_forced_successor.py
"""
from __future__ import annotations

import inspect
import sys
import typing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from derivation import model  # noqa: E402
from derivation.model import (  # noqa: E402
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    AdmissionError,
    Event,
    Impose,
    Regime,
    Supply,
    replay,
    step,
)


def main() -> int:
    failures: list[object] = []

    # 1. The grammar has exactly six kinds of event.
    kinds = typing.get_args(Event)
    print(f"event kinds: {[k.__name__ for k in kinds]} ({len(kinds)})")
    if len(kinds) != 6:
        failures.append(("event kinds", len(kinds)))

    # 2. No function in model.py produces a Regime from a Regime alone.
    makers = []
    for name, fn in inspect.getmembers(model, inspect.isfunction):
        if fn.__module__ != model.__name__:
            continue
        params = list(inspect.signature(fn).parameters)
        makers.append((name, params))
    print(f"functions in model.py: {makers}")
    solo = [n for n, ps in makers if ps == ["r"]]
    if solo:
        failures.append(("regime-only function", solo))

    # 3. No events, no change.
    if replay([]) != EMPTY:
        failures.append(("replay([])", replay([])))
    print(f"replay([]) == EMPTY: {replay([]) == EMPTY}")

    # 4. On a small regime, every one-event history that changes the
    # regime is a non-Supply event, and every Supply changes nothing.
    r: Regime = replay([AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(1)])
    events: list[Event] = [
        Supply("<a>"), Supply("zz"), AdmitDatum("<a>"), AdmitDatum("x"),
        AdmitForm(2), AdmitInst(0, (0,)), AdmitRuleAll(0), Impose(0, 1),
        AdmitForm(0), AdmitInst(5, (0,)), Impose(1, 1),
    ]
    changed, unchanged, refused = [], [], []
    for e in events:
        try:
            s = step(r, e)
        except AdmissionError as exc:
            refused.append((e, str(exc)))
            continue
        (changed if s != r else unchanged).append(e)
    print(f"changed:   {changed}")
    print(f"unchanged: {unchanged}")
    print(f"refused:   {[e for e, _ in refused]}")
    if any(isinstance(e, Supply) for e in changed):
        failures.append(("a supply changed the regime", changed))
    if not all(isinstance(e, Supply) or isinstance(e, AdmitDatum)
               for e in unchanged):
        failures.append(("unexpected no-op", unchanged))

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
