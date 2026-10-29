"""Unit 18 check: no delta of at most one item answers the demand.

Runs Genesis's own Python candidate enumeration, within and beyond the
declared bounds. This is sample computation, not a proof; the proof is
Derivation.cost1_insufficient_general. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u18_cost1.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import (  # noqa: E402
    Bounds,
    Delta,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    NodeView,
    apply_delta,
    iter_cost1_items,
    min_responses,
    response_valid_fast,
    response_valid_naive,
)
from derivation.engine import GENESIS_F, GENESIS_L, READING_F, READING_L  # noqa: E402
from derivation.model import AdmissionError, AdmitDatum, Regime, replay  # noqa: E402
from derivation.observe import collapsed_pairs, contexts, satisfies, separable  # noqa: E402


def main() -> int:
    failures: list[object] = []

    for reading, hist in ((READING_L, GENESIS_L), (READING_F, GENESIS_F)):
        base = replay(hist)
        target = reading.target
        view = NodeView.of(base)

        # 1. Within the declared bounds: the empty delta and every one-item
        # delta, by both validity checks.
        items = list(iter_cost1_items(base, Bounds(2, 2)))
        bad = [it for it in items
               if response_valid_fast(view, target, (it,))
               or response_valid_naive(base, target, (it,))]
        empty_ok = response_valid_fast(view, target, ())
        print(f"reading {reading.name}: one-item deltas within bounds: "
              f"{len(items)} ({items}); valid: {len(bad)}; empty delta "
              f"valid: {empty_ok}")
        if bad or empty_ok:
            failures.append(("bounded", reading.name))

        # 2. Beyond the bounds: forms of arity 1..5, instances and rules on
        # any form index 0..2 with arguments over the data. An instance or
        # a rule is rejected (no form to refer to); a datum or a form
        # applies and leaves the pair collapsed.
        applied = rejected = 0
        n = len(base.data)
        single: list[Delta] = [(NewDatum(),)]
        single += [(NewForm(a),) for a in range(1, 6)]
        single += [(NewRuleAll(f),) for f in range(3)]
        for f in range(3):
            for k in range(1, 3):
                for args in itertools.product(range(n + 1), repeat=k):
                    single.append((NewInst(f, args),))
        for delta in single:
            try:
                r = apply_delta(base, delta)
            except AdmissionError:
                rejected += 1
                if not isinstance(delta[0], (NewInst, NewRuleAll)):
                    failures.append(("rejected", delta))
                continue
            applied += 1
            if r.insts:
                failures.append(("instance appeared", delta))
            if target not in collapsed_pairs(r):
                failures.append(("separated", delta))
        print(f"  beyond bounds: {len(single)} one-item deltas; applied "
              f"{applied} (datum or form, pair still collapsed); rejected "
              f"{rejected} (instance or rule without a form)")

        # 3. Two items do suffice: the minimum under mu1 is exactly 2.
        mr = min_responses(base, target, "mu1", Bounds(2, 2))
        assert mr is not None
        print(f"  minimum under mu1: cost {mr.cost}, "
              f"{len(mr.deltas)} valid two-item deltas")
        if mr.cost != (2, -1):
            failures.append(("min", reading.name, mr.cost))

    # 4. The general theorem's hypotheses are used: with a form already
    # admitted, one item can answer.
    from derivation.model import AdmitForm  # noqa: E402
    r2f = replay(list(GENESIS_L) + [AdmitForm(1)])
    one = apply_delta(r2f, (NewInst(0, (0,)),))
    print(f"with a form admitted first: one instance separates (0, 1): "
          f"{(0, 1) not in collapsed_pairs(one)}")
    if (0, 1) in collapsed_pairs(one):
        failures.append("form-first")

    # 5. A five-datum regime with no forms: still nothing below two items.
    r5 = replay([AdmitDatum(t) for t in "abcde"])
    view5 = NodeView.of(r5)
    n_bad = sum(response_valid_fast(view5, (2, 4), (it,))
                for it in iter_cost1_items(r5, Bounds(2, 3)))
    print(f"five data, no forms, target (2, 4): valid one-item deltas "
          f"within arity 3: {n_bad}")
    if n_bad:
        failures.append("r5")

    # Removing the form-range conjunct does not remove the arity check.
    remaining_guard = len((0, 1)) == 0 and all(d < 2 for d in (0, 1))
    raw = Regime(("a", "b"), (), frozenset({(0, (0, 1))}), frozenset(), frozenset())
    print(f"unknown-form instance: remaining arity guard={remaining_guard}; "
          f"forced raw record contexts={len(contexts(raw))}; separable={separable(raw, 0, 1)}")
    if remaining_guard or contexts(raw) or separable(raw, 0, 1):
        failures.append("unknown-form counterfactual")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
