"""Unit 02 check: no instances and no rules, nothing derivable; drop either
hypothesis and something is.

Runs Genesis's own Python model. Part 1 is a sample, not a proof; the proof
is Derivation.underivable_of_empty. Part 2 evaluates the two regimes that
show each hypothesis is needed. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u02_underivable_of_empty.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from derivation.model import (  # noqa: E402
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Inst,
    Regime,
    replay,
)
from derivation.observe import derivable  # noqa: E402

TOKENS = ("d0", "d1", "d2", "d3")
FORM_LISTS: tuple[tuple[int, ...], ...] = (
    (), (1,), (2,), (1, 1), (1, 2), (2, 1), (2, 2),
)


def sample_instances() -> list[Inst]:
    """Form 0 to 3, 0 to 3 arguments over data numbers 0 to 3: 340."""
    out: list[Inst] = []
    for form in range(4):
        for length in range(4):
            for args in itertools.product(range(4), repeat=length):
                out.append((form, tuple(args)))
    return out


def empty_regimes() -> list[tuple[str, Regime]]:
    """Regimes reached by replay from genesis with no AdmitInst and no
    AdmitRuleAll: 0 to 3 data, at most two forms of arity 1 or 2, and
    either no demand or every demand i < j."""
    out: list[tuple[str, Regime]] = []
    for n in range(4):
        for forms in FORM_LISTS:
            demand_sets = [()]
            if n >= 2:
                demand_sets.append(tuple(itertools.combinations(range(n), 2)))
            for demands in demand_sets:
                history: list[Event] = [AdmitDatum(t) for t in TOKENS[:n]]
                history += [AdmitForm(a) for a in forms]
                history += [Impose(i, j) for i, j in demands]
                label = f"data={n} forms={list(forms)} reqs={list(demands)}"
                out.append((label, replay(history)))
    return out


def main() -> int:
    failures: list[object] = []
    instances = sample_instances()

    # Part 1: the hypotheses hold, nothing in the sample is derivable.
    regimes = empty_regimes()
    regimes.append(("R2L (Challenge 3, reading L)", replay(
        [AdmitDatum("<a>"), AdmitDatum("<ab>"), Impose(0, 1)])))
    checked = 0
    found = 0
    for label, r in regimes:
        if r.insts or r.rules:
            failures.append(("hypothesis fails", label))
            continue
        for inst in instances:
            checked += 1
            if derivable(r, inst):
                found += 1
                failures.append((label, inst))
    print(f"regimes with no instances and no rules: {len(regimes)}")
    print(f"instance evaluations: {checked}, derivable: {found}")

    # Part 2: drop one hypothesis at a time.
    r_rule = replay([AdmitForm(1), AdmitRuleAll(0)])
    r_inst = replay([AdmitDatum("d0"), AdmitForm(1), AdmitInst(0, (0,))])
    cases: list[tuple[str, Regime, Inst, bool]] = [
        ("R  (rule, no instance)", r_rule, (0, (99,)), True),
        ("R' (instance, no rule)", r_inst, (0, (0,)), True),
        ("R' (instance, no rule)", r_inst, (0, (1,)), False),
    ]
    for label, r, inst, want in cases:
        got = derivable(r, inst)
        print(f"{label}: insts={sorted(r.insts)} rules={sorted(r.rules)} "
              f"derivable{inst} = {got}")
        if got != want:
            failures.append((label, inst, got))

    # The rule reaches every sampled instance of its form; the instance
    # reaches exactly itself.
    reach_rule = sum(1 for i in instances if derivable(r_rule, i))
    reach_inst = sum(1 for i in instances if derivable(r_inst, i))
    per_form = len(instances) // 4
    print(f"sampled instances derivable in R: {reach_rule} "
          f"(all {per_form} of form 0); in R': {reach_inst}")
    if reach_rule != per_form or reach_inst != 1:
        failures.append(("reach", reach_rule, reach_inst))

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
