"""Unit 01 check: a finite ledger does not bound the extension of derivable.

Builds R = <0, [1], [], [0], []> by Genesis's own replay (admit one unary
form, admit the all-instances rule on it) and shows that instances naming
no admitted datum, or with the wrong number of arguments, are derivable in R.
Runs Genesis's own Python model. A finite sample, not a proof.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u01_rule_extension.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from derivation.model import AdmitForm, AdmitRuleAll, replay  # noqa: E402
from derivation.observe import contexts, derivable, plug  # noqa: E402


def main() -> int:
    r = replay([AdmitForm(1), AdmitRuleAll(0)])
    print(f"R: data={r.data} forms={r.forms} insts={sorted(r.insts)} "
          f"rules={sorted(r.rules)} reqs={sorted(r.reqs)}")
    failures: list[object] = []

    expect_true = [
        (0, (99,)),       # names datum 99; R admits no datum at all
        (0, ()),          # wrong arity: form 0 has arity 1
        (0, (1, 2, 3)),   # wrong arity again
    ]
    expect_false = [
        (1, (0,)),        # form 1 was never admitted and carries no rule
    ]
    for inst in expect_true:
        got = derivable(r, inst)
        print(f"derivable(R, {inst}) = {got}")
        if not got:
            failures.append(inst)
    for inst in expect_false:
        got = derivable(r, inst)
        print(f"derivable(R, {inst}) = {got}")
        if got:
            failures.append(inst)

    if r.n_data() != 0:
        failures.append(("n_data", r.n_data()))

    # profiles() plugs only admitted data into contexts.
    # R has one context, (0, (None,)), but no admitted datum to plug in.
    queried = [plug(c, d) for c in contexts(r) for d in range(r.n_data())]
    print(f"contexts in R: {list(contexts(r))}")
    print(f"instances profiles() would query in R: {queried}")
    if queried:
        failures.append(("queried", queried))

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
