"""Unit 09 check: a separating witness rules out collapse.

Runs Genesis's Python model on every regime with two data, one form of
arity 1 or 2, and any subset of its possible instances, with or without
the rule. For each pair: separable exactly when a witness exists, and a
witness exactly when the pair is not collapsed. Sample computation on a
finite family; the theorem is Derivation.separable_not_collapsed.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u09_witness.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from derivation.model import AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Event, replay  # noqa: E402
from derivation.observe import collapsed_pairs, contexts, derivable, plug, separable, witness  # noqa: E402


def main() -> int:
    failures: list[object] = []
    regimes = 0
    sep = 0
    for arity in (1, 2):
        all_args = list(itertools.product(range(2), repeat=arity))
        for k in range(len(all_args) + 1):
            for chosen in itertools.combinations(all_args, k):
                for rule in (False, True):
                    h: list[Event] = [AdmitDatum("<a>"), AdmitDatum("<ab>"), AdmitForm(arity)]
                    h += [AdmitInst(0, args) for args in chosen]
                    if rule:
                        h.append(AdmitRuleAll(0))
                    r = replay(h)
                    regimes += 1
                    w = witness(r, 0, 1)
                    s = separable(r, 0, 1)
                    col = (0, 1) in collapsed_pairs(r)
                    if s != (w is not None) or s == col:
                        failures.append(("mismatch", arity, chosen, rule))
                    if w is not None:
                        sep += 1
                        # the witness really does differ
                        if derivable(r, plug(w, 0)) == derivable(r, plug(w, 1)):
                            failures.append(("bad witness", arity, chosen, rule))
                    else:
                        # no context differs
                        if any(derivable(r, plug(c, 0)) != derivable(r, plug(c, 1)) for c in contexts(r)):
                            failures.append(("missed witness", arity, chosen, rule))
    print(f"regimes: {regimes}; separable (witness found): {sep}; collapsed: {regimes - sep}")
    print("separable <=> witness exists <=> not collapsed, on every one")

    # The rule never separates: every regime with the rule is collapsed.
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
