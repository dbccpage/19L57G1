"""Unit 49 check: the six probes, the 64-member class, and the retract.

Runs Genesis's `code/derivation/completion.py` minimality mirror: the six
probes on the sealed step, the single-toggle outcomes, the probe-toggle
correspondence on all 64 descriptors (each probe fails exactly when its
guard is off), the histogram of passed probes, uniqueness of the compliant
member, the two cost orders on the compliant set, and
`minimality_report()` against `artifacts/completion_minimality.json`. The
retract is checked with a Python (book) `CWorld`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u49_initiality.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation import completion as C, represented as R  # noqa: E402

TOGGLE = {"dedup": 0, "require_guard": 1, "accept_guard": 2,
          "budget_gate": 3, "license_gate": 4, "refusal_certificate": 5}


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "completion_minimality.json").read_text())
    K = C.KERNEL_DESC

    print("the six probes on the sealed step (each must be a no-op):")
    for name, w, e in C.PROBES:
        noop = R.step(w, e) == w
        print(f"  {name}: event {e} on {w.json()['data']}/{w.json()['views']}/budget {w.budget}"
              f"/licensed {w.aug_licensed}: no-op {noop}")
        if not noop:
            failures.append(f"probe {name}")

    print("one guard off, on its probe world:")
    for name, w, e in C.PROBES:
        off = list(K)
        off[TOGGLE[name]] = False
        out = C.interp_step(tuple(off), w, e)
        res = C.probe_results(tuple(off))
        print(f"  {name} off: {out.json()}; fails {[n for n, v in res.items() if not v]}")
        if out == w or [n for n, v in res.items() if not v] != [name]:
            failures.append(f"off {name}")

    print("all 64 descriptors:")
    descs = C.all_descs()
    corr = all(
        {n for n, v in C.probe_results(d).items() if not v} == {n for n, i in TOGGLE.items() if not d[i]}
        for d in descs)
    hist = Counter(sum(C.probe_results(d).values()) for d in descs)
    comp = [d for d in descs if C.compliant(d)]
    print(f"  each probe fails exactly when its guard is off: {corr}")
    print(f"  passed-probe histogram {dict(sorted(hist.items()))} (binomial, 1 6 15 20 15 6 1)")
    print(f"  compliant: {comp}; is the kernel: {comp == [K]}")
    if not corr or comp != [K] or dict(hist) != {0: 1, 1: 6, 2: 15, 3: 20, 4: 15, 5: 6, 6: 1}:
        failures.append("class")
    print(f"  cost orders on the compliant set: capabilities {[C.cost_capabilities(d) for d in comp]}, "
          f"lexicographic {[C.cost_lex(d) for d in comp]}; the all-off member costs "
          f"{C.cost_capabilities(descs[0])}, {C.cost_lex(descs[0])}")

    rep = C.minimality_report()
    agree = rep == art
    print(f"  minimality_report() equals the artifact: {agree}; keys {sorted(art)}")
    if not agree:
        failures.append("artifact")

    print("the retract (CWorld as Python (book)):")
    base, panel = R.GENESIS, (((0,),),)
    for e in C.PIGEON:
        base = R.step(base, e)
    story = R.replay(C.PIGEON)
    print(f"  base after the story's events through the panel kernel equals the story: {base == story}; "
          f"panel untouched: {panel == (((0,),),)}")
    if base != story:
        failures.append("retract")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
