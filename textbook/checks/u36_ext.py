"""Unit 36 check: lists that mean sets.

Genesis's Python keeps instances, rules and demands as frozensets, so two
admission orders give one regime; Lean keeps lists, so they give two
regimes related by `RegimeExt`. The check shows the Python side: equal
regimes, equal observables, equal minimum responses; duplicate admission
dedups; and that the datum and form orders are not quotiented (indices
are meaning). AuthorityEffect: None.
Run from the repository root: python textbook/checks/u36_ext.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import Bounds, min_responses  # noqa: E402
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, Impose, replay  # noqa: E402
from derivation.observe import collapsed_pairs, separable  # noqa: E402


def main() -> int:
    failures: list[str] = []
    head = [AdmitDatum("a"), AdmitDatum("b"), Impose(0, 1), AdmitForm(1), AdmitForm(1)]
    ra = replay(head + [AdmitInst(0, (0,)), AdmitInst(1, (1,))])
    rb = replay(head + [AdmitInst(1, (1,)), AdmitInst(0, (0,))])
    print(f"two admission orders of the same instances: equal regimes {ra == rb}; "
          f"insts {sorted(ra.insts)}; collapsed pairs {collapsed_pairs(ra)} {collapsed_pairs(rb)}")
    if ra != rb or collapsed_pairs(ra) != collapsed_pairs(rb):
        failures.append("insts order")
    rc = replay(head + [AdmitInst(0, (0,)), AdmitInst(0, (0,))])
    print(f"the same instance admitted twice: {len(rc.insts)} instance; "
          f"datum admitted twice: {replay([AdmitDatum('a'), AdmitDatum('a')]).data}")
    if len(rc.insts) != 1:
        failures.append("dedup")
    base_a = replay([AdmitDatum("x"), AdmitDatum("y"), AdmitDatum("z"), Impose(0, 1),
                     AdmitForm(1), AdmitForm(2), AdmitInst(0, (0,)), AdmitInst(1, (0, 0))])
    base_b = replay([AdmitDatum("x"), AdmitDatum("y"), AdmitDatum("z"), Impose(0, 1),
                     AdmitForm(1), AdmitForm(2), AdmitInst(1, (0, 0)), AdmitInst(0, (0,))])
    ma, mb = (min_responses(b, (1, 2), "mu2", Bounds(2, 2)) for b in (base_a, base_b))
    print(f"mixed regime, two orders: equal {base_a == base_b}; collapsed pairs {collapsed_pairs(base_a)}; "
          f"mu2 minimum for (1, 2): {ma.cost} {mb.cost}; "
          f"same deltas {set(ma.deltas) == set(mb.deltas)}")
    if base_a != base_b or ma.cost != mb.cost or set(ma.deltas) != set(mb.deltas):
        failures.append("responses")
    # what is NOT quotiented: datum order and form order carry the indices
    d1 = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitForm(1), AdmitInst(0, (0,))])
    d2 = replay([AdmitDatum("b"), AdmitDatum("a"), AdmitForm(1), AdmitInst(0, (0,))])
    f1 = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitForm(1), AdmitForm(2)])
    f2 = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitForm(2), AdmitForm(1)])
    print(f"datum order kept: data {d1.data} vs {d2.data}, equal {d1 == d2}; "
          f"the mark sits on {d1.data[0]!r} vs {d2.data[0]!r}; "
          f"form order kept: forms {f1.forms} vs {f2.forms}, equal {f1 == f2}")
    if d1 == d2 or f1 == f2 or not separable(d1, 0, 1):
        failures.append("indices")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
