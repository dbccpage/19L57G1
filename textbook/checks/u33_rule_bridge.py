"""Unit 33 check: a delta with a uniform-rule item is never a minimum.

Runs the full-space cross-check of tests/test_candidates.py on the mixed
regime, item by item: every valid rule-bearing two-item delta has a valid
rule-free part that is shorter with the same new-form arity sum. Sample
computation; the proof is RuleBridge.rule_item_never_minimal.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u33_rule_bridge.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import (  # noqa: E402
    Bounds, NewDatum, NewRuleAll, apply_delta, iter_cost2_deltas, iter_full_deltas,
    min_responses, mu1, mu2, response_valid_naive,
)
from derivation.engine import delta_label  # noqa: E402
from derivation.model import (  # noqa: E402
    AdmissionError, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Impose, replay,
)
from derivation.observe import collapsed_pairs  # noqa: E402

BOUNDS = Bounds(max_items=2, max_arity=2)


def has_rule(d) -> bool:
    return any(isinstance(it, NewRuleAll) for it in d)


def main() -> int:
    failures: list[object] = []
    base = replay([AdmitDatum("x"), AdmitDatum("y"), AdmitDatum("z"), Impose(0, 1),
                   AdmitForm(1), AdmitForm(2), AdmitInst(0, (1,)), AdmitInst(1, (0, 2))])
    target = (1, 2)
    bare = replay([AdmitDatum("x"), AdmitDatum("y"), AdmitDatum("z"), Impose(0, 1),
                   AdmitForm(1), AdmitForm(2)])
    for label, r in (("three data, two forms, nothing asserted", bare), ("mixed regime", base)):
        mr = min_responses(r, target, "mu1", BOUNDS)
        print(f"{label}, target {target}, collapsed pairs {collapsed_pairs(r)}: mu1 minimum "
              f"{mr.cost}, {len(mr.deltas)} deltas, any with a rule item: "
              f"{any(has_rule(d) for d in mr.deltas)}")
        if any(has_rule(d) for d in mr.deltas):
            failures.append("minimum has a rule")

    pruned = list(iter_cost2_deltas(base, BOUNDS, target))
    print(f"pruned two-item enumeration: {len(pruned)} deltas, rule items present: "
          f"{any(has_rule(d) for d in pruned)}")
    if any(has_rule(d) for d in pruned):
        failures.append("pruned has a rule")

    full = list(iter_full_deltas(base, 2, BOUNDS))
    rule_valid = []
    for d in full:
        if not has_rule(d):
            continue
        try:
            if response_valid_naive(base, target, d):
                rule_valid.append(d)
        except AdmissionError:
            pass
    ok_all = True
    example = None
    for d in rule_valid:
        rest = tuple(it for it in d if not isinstance(it, NewRuleAll))
        good = (response_valid_naive(base, target, rest) and mu1(rest) < mu1(d)
                and mu2(rest)[1] == mu2(d)[1])
        ok_all &= good
        if example is None:
            example = (d, rest)
    print(f"full two-item space: {len(full)} deltas, {sum(has_rule(d) for d in full)} with a rule "
          f"item, {len(rule_valid)} of those valid; every valid one has a valid rule-free part, "
          f"shorter, same arity sum: {ok_all}")
    if example:
        d, rest = example
        print(f"  example: {delta_label(base, d)} {mu2(d)} -> {delta_label(base, rest)} {mu2(rest)}")
    if not rule_valid or not ok_all:
        failures.append("drop")

    # A new datum need not be separable from every old datum.
    fresh_ruled = apply_delta(base, (NewDatum(), NewRuleAll(0)))
    fresh_pairs = collapsed_pairs(fresh_ruled)
    print(f"datum+rule@0 result: collapsed pairs {fresh_pairs}; "
          f"newcomer 3 remains collapsed with datum 1: {(1, 3) in fresh_pairs}")
    if (1, 3) not in fresh_pairs:
        failures.append("fresh datum collapse")

    # the subset direction: ADDING a uniform rule on the only form kills the separation
    u0 = replay([AdmitDatum("a"), AdmitDatum("b"), Impose(0, 1), AdmitForm(1), AdmitInst(0, (0,))])
    ruled = replay([AdmitRuleAll(0)], u0)
    print(f"U0 collapsed pairs {collapsed_pairs(u0)}; with the uniform rule on form 0: "
          f"{collapsed_pairs(ruled)}")
    if collapsed_pairs(u0) != () or collapsed_pairs(ruled) != ((0, 1),):
        failures.append("rule kills")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
