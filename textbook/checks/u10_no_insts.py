"""Unit 10 check: with no admitted instances, every pair is collapsed.

Runs Genesis's Python model on regimes with up to three data, any of
several form tables, any subset of rules, and no instances: every pair of
data is collapsed. Then the contrast: one instance separates. Sample
computation; the theorem is Derivation.collapsed_of_no_insts.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u10_no_insts.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from derivation.engine import GENESIS_F, GENESIS_L  # noqa: E402
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Event, replay, step  # noqa: E402
from derivation.observe import collapsed_pairs, profiles  # noqa: E402

FORM_TABLES = ((), (1,), (2,), (1, 2), (3,), (1, 1, 2))


def main() -> int:
    failures: list[object] = []
    regimes = 0
    pairs = 0
    for n in range(4):
        for forms in FORM_TABLES:
            for k in range(len(forms) + 1):
                for rules in itertools.combinations(range(len(forms)), k):
                    h: list[Event] = [AdmitDatum(f"t{i}") for i in range(n)]
                    h += [AdmitForm(a) for a in forms]
                    h += [AdmitRuleAll(f) for f in rules]
                    r = replay(h)
                    regimes += 1
                    cp = collapsed_pairs(r)
                    allpairs = tuple((i, j) for i in range(n) for j in range(i + 1, n))
                    pairs += len(allpairs)
                    if cp != allpairs:
                        failures.append(("not collapsed", n, forms, rules, cp))
                    profs = profiles(r)
                    if len(set(profs)) > 1:
                        failures.append(("profiles differ", n, forms, rules))
    print(f"instance-free regimes: {regimes}; pairs: {pairs}; all collapsed; at most one profile each")

    # Genesis's two Challenge-2 regimes.
    for name, g in (("GENESIS_L", GENESIS_L), ("GENESIS_F", GENESIS_F)):
        r = replay(g)
        print(f"{name}: insts {r.insts}, collapsed pairs {collapsed_pairs(r)}")
        n = r.n_data()
        if collapsed_pairs(r) != tuple((i, j) for i in range(n) for j in range(i + 1, n)):
            failures.append(name)

    # Contrast: one instance on one datum separates the pair.
    r1 = replay([AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(1), AdmitInst(0, (1,))])
    print(f"one instance (0, (1,)): collapsed pairs {collapsed_pairs(r1)}")
    if collapsed_pairs(r1) != ():
        failures.append("instance did not separate")
    ruled = replay([AdmitDatum("A"), AdmitDatum("B"), AdmitForm(1), AdmitRuleAll(0)])
    ruled_inst = step(ruled, AdmitInst(0, (0,)))
    if profiles(ruled) != profiles(ruled_inst) or collapsed_pairs(ruled_inst) != ((0, 1),):
        failures.append("an instance is not sufficient under a uniform rule")
    print("one redundant instance under a uniform rule leaves the pair collapsed")
    no_forms = replay([AdmitDatum("A"), AdmitDatum("B")])
    form_only = step(no_forms, AdmitForm(1))
    all_marked = step(form_only, AdmitRuleAll(0))
    if profiles(no_forms) != (frozenset(), frozenset()) or profiles(form_only) != profiles(no_forms):
        failures.append("empty profiles contrast")
    full = frozenset({(0, (None,))})
    if profiles(all_marked) != (full, full):
        failures.append("full profiles contrast")
    masked = step(r1, AdmitRuleAll(0))
    if collapsed_pairs(r1) or collapsed_pairs(masked) != ((0, 1),):
        failures.append("uniform-rule addition did not mask the existing separation")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
