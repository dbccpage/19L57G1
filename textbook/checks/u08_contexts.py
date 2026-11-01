"""Unit 08 check: contexts, plugging, derivability, profiles, collapse.

Runs Genesis's own Python model (code/derivation/observe.py) on small
regimes and compares with the counts the definitions predict. Sample
computation; the definitions are admitted. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u08_contexts.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from derivation.model import AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, replay  # noqa: E402
from derivation.observe import (  # noqa: E402
    collapsed_pairs,
    contexts,
    derivable,
    plug,
    profile,
    separable,
    witness,
)


def main() -> int:
    failures: list[object] = []

    # 1. Contexts of a regime with two data and one unary form: one context.
    r = replay([AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(1)])
    cs = contexts(r)
    print(f"two data, forms [1]: contexts = {cs}")
    if cs != ((0, (None,)),):
        failures.append(("contexts unary", cs))

    # 2. Count formula: for arity a over n data, (n+1)^a - n^a contexts
    # (slot tuples over n data plus a hole, minus the hole-free ones).
    for n in range(4):
        for a in (1, 2, 3):
            h = [AdmitDatum(f"t{i}") for i in range(n)] + [AdmitForm(a)]
            got = len(contexts(replay(h)))
            want = (n + 1) ** a - n ** a
            if got != want:
                failures.append(("count", n, a, got, want))
    print("context counts match (n+1)^a - n^a for n <= 3, a <= 3")

    # 3. Plugging fills every hole with the same datum.
    c = (0, (None, 1, None))
    print(f"plug {c} with 0 -> {plug(c, 0)}")
    if plug(c, 0) != (0, (0, 1, 0)):
        failures.append("plug")

    # 4. Derivability: by instance, or by a uniform rule; nothing else.
    r_inst = replay([AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(1), AdmitInst(0, (1,))])
    r_rule = replay([AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(1), AdmitRuleAll(0)])
    d = (derivable(r_inst, (0, (1,))), derivable(r_inst, (0, (0,))),
         derivable(r_rule, (0, (0,))), derivable(r_rule, (0, (1,))))
    print(f"derivable: inst on 1 -> {d[0]}; inst absent on 0 -> {d[1]}; rule on 0, 1 -> {d[2]}, {d[3]}")
    if d != (True, False, True, True):
        failures.append(("derivable", d))

    # 5. Profiles, separability and the witness.
    p0, p1 = profile(r_inst, 0), profile(r_inst, 1)
    print(f"profiles under the instance: datum 0 {set(p0)}, datum 1 {set(p1)}")
    print(f"separable(0, 1) = {separable(r_inst, 0, 1)}; witness = {witness(r_inst, 0, 1)}")
    if p0 != frozenset() or p1 != frozenset({(0, (None,))}) or not separable(r_inst, 0, 1):
        failures.append("profiles inst")
    if witness(r_inst, 0, 1) != (0, (None,)):
        failures.append("witness")

    # 6. Under the rule both profiles are full: collapsed.
    print(f"under the rule: profiles equal? {profile(r_rule, 0) == profile(r_rule, 1)}; "
          f"collapsed pairs {collapsed_pairs(r_rule)}")
    if collapsed_pairs(r_rule) != ((0, 1),):
        failures.append("rule collapse")

    # 7. Collapse and separability are each other's complement on every pair
    # of a few regimes.
    for rr in (r, r_inst, r_rule, replay([AdmitDatum("x")])):
        n = rr.n_data()
        for i in range(n):
            for j in range(i + 1, n):
                if separable(rr, i, j) == ((i, j) in collapsed_pairs(rr)):
                    failures.append(("complement", i, j))
    print("separable == not collapsed on every pair of four regimes")

    # Changed practice: distinguish plugging from the context-validity guard.
    ternary = replay([AdmitDatum("A"), AdmitDatum("B"), AdmitForm(3)])
    c = (0, (None, 0, None))
    if c not in contexts(ternary) or plug(c, 1) != (0, (1, 0, 1)):
        failures.append("changed multi-hole plugging")
    binary = replay([AdmitDatum("A"), AdmitDatum("B"), AdmitForm(2)])
    ruled_binary = replay([AdmitDatum("A"), AdmitDatum("B"), AdmitForm(2), AdmitRuleAll(0)])
    for state in (binary, ruled_binary):
        if ((0, (None, 2)) in contexts(state) or (0, (0, 1)) in contexts(state)
                or (0, (None, None)) not in contexts(state)):
            failures.append("rule changed context-validity conditions")
    changed_mark = replay([AdmitDatum("A"), AdmitDatum("B"), AdmitForm(1), AdmitInst(0, (0,))])
    if (profile(changed_mark, 0) != frozenset({(0, (None,))}) or profile(changed_mark, 1)
            or witness(changed_mark, 0, 1) != (0, (None,))):
        failures.append("changed unary profile")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
