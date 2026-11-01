"""Unit 12 check: a fresh datum changes the state and no old pair's status.

Runs Genesis's own Python model. This is sample computation, not a proof;
the proofs are Derivation.admission_without_expressive_increase and
Derivation.collapsed_fresh_datum. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u12_fresh_datum.py
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.engine import GENESIS_L, challenge2_report  # noqa: E402
from derivation.model import (  # noqa: E402
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    AdmissionError,
    Event,
    Regime,
    replay,
    step,
)
from derivation.observe import collapsed_pairs, contexts, profiles, separable  # noqa: E402

DATA = ("<>", "<a>", "<ab>")


def wf_regimes() -> list[Regime]:
    """Regimes with 1-3 data, form tables over arities 1-2, every subset of
    up to two instances on those forms over the admitted data, with or
    without a rule on form 0. All well formed by construction."""
    out: list[Regime] = []
    for n in range(1, 4):
        for forms in ((1,), (2,), (1, 2)):
            base: list[Event] = [AdmitDatum(t) for t in DATA[:n]]
            base += [AdmitForm(a) for a in forms]
            insts = [AdmitInst(f, args)
                     for f, a in enumerate(forms)
                     for args in itertools.product(range(n), repeat=a)]
            for k in range(3):
                for chosen in itertools.combinations(insts, k):
                    for rule in ([], [AdmitRuleAll(0)]):
                        out.append(replay(base + list(chosen) + rule))
    return out


def main() -> int:
    failures: list[object] = []

    # 1. The Genesis counterexample on reading L.
    r2 = replay(GENESIS_L)
    r3 = step(r2, AdmitDatum("<abc>"))
    print(f"R2L data {r2.data}; after a fresh datum {r3.data}; changed: {r3 != r2}")
    print(f"collapsed pairs before {collapsed_pairs(r2)}, after {collapsed_pairs(r3)}")
    print(f"observational classes before {len(set(profiles(r2)))}, "
          f"after {len(set(profiles(r3)))}")
    if r3 == r2 or (0, 1) not in collapsed_pairs(r3):
        failures.append("counterexample")
    if len(set(profiles(r3))) != 1:
        failures.append("classes")

    # 2. R1 over a family of well-formed regimes: every old pair keeps its
    # status exactly; and the fresh datum's own pairs are not covered.
    regs = wf_regimes()
    old_pairs = kept = fresh_sep = fresh_coll = 0
    for r in regs:
        r1 = step(r, AdmitDatum("fresh"))
        n = r.n_data()
        for i, j in itertools.combinations(range(n), 2):
            old_pairs += 1
            if separable(r, i, j) == separable(r1, i, j):
                kept += 1
            else:
                failures.append(("R1", r, i, j))
        for i in range(n):
            if separable(r1, i, n):
                fresh_sep += 1
            else:
                fresh_coll += 1
    print(f"well-formed regimes: {len(regs)}; old pairs: {old_pairs}; "
          f"status kept after a fresh datum: {kept}")
    print(f"pairs with the fresh datum: separable {fresh_sep}, "
          f"collapsed {fresh_coll} (R1 says nothing about these)")
    if fresh_sep == 0 or fresh_coll == 0:
        failures.append("fresh pairs should go both ways")

    # 3. The BL contrast of the Lean check.
    bl = replay([AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(2),
                 AdmitInst(0, (0, 1))])
    bl3 = step(bl, AdmitDatum("fresh"))
    print(f"BL: separable(0,1) {separable(bl, 0, 1)}; BL3: separable(0,1) "
          f"{separable(bl3, 0, 1)}, separable(0,2) {separable(bl3, 0, 2)}, "
          f"separable(1,2) {separable(bl3, 1, 2)}")
    if not (separable(bl3, 0, 1) and separable(bl3, 0, 2) and separable(bl3, 1, 2)):
        failures.append("BL3")

    # Scope counterexamples: old comparisons can stay fixed while the
    # newcomer forms another class. Unary contexts need not grow at all.
    both_marked = replay([AdmitDatum("A"), AdmitDatum("B"), AdmitForm(1),
                          AdmitInst(0, (0,)), AdmitInst(0, (1,))])
    newcomer = step(both_marked, AdmitDatum("C"))
    sizes = (len(contexts(both_marked)), len(contexts(newcomer)))
    classes = (len(set(profiles(both_marked))), len(set(profiles(newcomer))))
    print(f"both marked then a newcomer: contexts {sizes}, classes {classes}")
    if sizes != (1, 1) or classes != (1, 2) or separable(newcomer, 0, 1):
        failures.append(("old pair versus class count", sizes, classes))
    blank_three = replay([AdmitDatum(t) for t in ("A", "B", "C")] + [AdmitForm(1)])
    mentions_one = step(blank_three, AdmitInst(0, (1,)))
    mentions_neither = step(blank_three, AdmitInst(0, (2,)))
    if separable(blank_three, 0, 1) or not separable(mentions_one, 0, 1):
        failures.append("avoiding one target does not protect the pair")
    if separable(mentions_neither, 0, 1):
        failures.append("avoiding both targets must protect this pair")
    print("marking target 1 changes pair (0,1); marking only 2 does not")
    if (len(contexts(bl)), len(contexts(bl3))) != (5, 7):
        failures.append("binary fresh-datum contexts should grow from five to seven")

    # A raw record can violate the range hypothesis of the preservation theorem.
    latent = Regime(data=("A", "B"), forms=(2,),
                    insts=frozenset({(0, (2, 0))}),
                    rules=frozenset(), reqs=frozenset())
    if separable(latent, 0, 1) or not separable(step(latent, AdmitDatum("C")), 0, 1):
        failures.append("latent out-of-range instance counterexample")
    try:
        step(replay([AdmitDatum("A"), AdmitDatum("B"), AdmitForm(2)]),
             AdmitInst(0, (2, 0)))
    except AdmissionError:
        pass
    else:
        failures.append("invalid instance admitted through the guarded API")
    print("raw out-of-range instance changes an old pair; guarded admission rejects it")

    # 4. The committed artifact agrees with a fresh computation.
    rep = challenge2_report()["readings"]
    art = json.loads((ROOT / "artifacts" / "challenges.json").read_text())
    art2 = art["challenge2"]["readings"]
    for name in ("L", "F"):
        flag = rep[name]["expressive_increase_over_challenge0"]  # type: ignore[index]
        print(f"challenge2 {name}: expressive_increase_over_challenge0 = {flag} "
              f"(artifact {art2[name]['expressive_increase_over_challenge0']})")
        if flag is not False or art2[name]["expressive_increase_over_challenge0"] is not False:
            failures.append(("artifact", name))

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
