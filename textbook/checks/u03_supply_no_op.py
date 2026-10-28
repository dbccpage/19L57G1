"""Unit 03 check: a supply never changes a regime; an admission does.

Runs Genesis's own Python model. This is sample computation, not a proof;
the proof is Derivation.supply_no_op. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u03_supply_no_op.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from derivation.engine import GENESIS_F, GENESIS_L  # noqa: E402
from derivation.model import (  # noqa: E402
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Regime,
    Supply,
    replay,
    step,
)

DATA_TOKENS = ("<>", "<a>", "<ab>")
TOKENS = ("<>", "<a>", "<ab>", "d0", "zz", "", "x" * 40)
FORM_LISTS: tuple[tuple[int, ...], ...] = ((), (1,), (1, 2))


def sample_regimes() -> list[tuple[str, Regime]]:
    """Regimes reached by replay: 0 to 3 data, a few form tables, and with
    or without an instance, the rule, and a demand where they are
    well formed."""
    out: list[tuple[str, Regime]] = []
    for n in range(4):
        for forms in FORM_LISTS:
            base: list[Event] = [AdmitDatum(t) for t in DATA_TOKENS[:n]]
            base += [AdmitForm(a) for a in forms]
            inst_opts: list[list[Event]] = [[]]
            if forms and n >= 1:
                inst_opts.append([AdmitInst(0, (0,))])
            rule_opts: list[list[Event]] = [[]]
            if forms:
                rule_opts.append([AdmitRuleAll(0)])
            req_opts: list[list[Event]] = [[]]
            if n >= 2:
                req_opts.append([Impose(0, 1)])
            for ins, rul, req in itertools.product(inst_opts, rule_opts, req_opts):
                label = (f"data={n} forms={list(forms)} inst={bool(ins)} "
                         f"rule={bool(rul)} req={bool(req)}")
                out.append((label, replay(base + ins + rul + req)))
    out.append(("GENESIS_L", replay(GENESIS_L)))
    out.append(("GENESIS_F", replay(GENESIS_F)))
    return out


def without_supplies(h: tuple[Event, ...] | list[Event]) -> list[Event]:
    return [e for e in h if not isinstance(e, Supply)]


def main() -> int:
    failures: list[object] = []
    regimes = sample_regimes()

    # 1. Supply returns the very regime, for every sampled regime and token.
    cases = 0
    for label, r in regimes:
        for tok in TOKENS:
            cases += 1
            if step(r, Supply(tok)) is not r:
                failures.append(("supply changed", label, tok))
    print(f"regimes: {len(regimes)}; tokens: {len(TOKENS)}; "
          f"supply cases: {cases}; unchanged (same object): "
          f"{cases - len(failures)}")

    # 2. Dropping the supplies from Genesis's histories changes nothing.
    h_bare: tuple[Event, ...] = (Supply("<>"), Supply("<a>"))
    h_admit: tuple[Event, ...] = h_bare + (AdmitDatum("<a>"),)
    histories = {"GENESIS_L": GENESIS_L, "GENESIS_F": GENESIS_F,
                 "challenge1 bare": h_bare, "challenge1 admit": h_admit}
    for name, h in histories.items():
        n_sup = sum(isinstance(e, Supply) for e in h)
        same = replay(h) == replay(without_supplies(h))
        print(f"{name}: {len(h)} events, {n_sup} supplies; "
              f"same regime without them: {same}")
        if not same:
            failures.append(("history", name))

    # 3. Every history of at most three supplies replays to EMPTY.
    supply_histories = [
        [Supply(t) for t in seq]
        for k in range(4)
        for seq in itertools.product(DATA_TOKENS, repeat=k)
    ]
    to_empty = sum(replay(h) == EMPTY for h in supply_histories)
    print(f"supply-only histories: {len(supply_histories)}; "
          f"replay to EMPTY: {to_empty}")
    if to_empty != len(supply_histories):
        failures.append(("supply-only", to_empty))

    # 4. Contrast: admitting a fresh token always changes the regime;
    # re-admitting an admitted token does not (designation, Unit 06).
    fresh_changes = sum(step(r, AdmitDatum("fresh")) != r for _, r in regimes)
    readmit = [(label, r) for label, r in regimes if r.data]
    readmit_same = sum(step(r, AdmitDatum(r.data[0])) == r for _, r in readmit)
    print(f"AdmitDatum(fresh) changes the regime: {fresh_changes} of "
          f"{len(regimes)}")
    print(f"AdmitDatum(already admitted) leaves it unchanged: {readmit_same} "
          f"of {len(readmit)} (a fact about AdmitDatum, not Supply)")
    if fresh_changes != len(regimes) or readmit_same != len(readmit):
        failures.append(("contrast", fresh_changes, readmit_same))

    # 5. Admission does not wait for a supply.
    r_x = replay([AdmitDatum("x")])
    print(f"replay([AdmitDatum('x')]).data = {r_x.data}")
    if r_x.data != ("x",):
        failures.append(("admit without supply", r_x.data))

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
