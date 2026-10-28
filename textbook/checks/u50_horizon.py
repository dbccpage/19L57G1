"""Unit 50 check: the generated run characterised at every stage, and the
budget pin shared with Lean.

Writes Lean's `specWorld` in Python (book) and checks it against Genesis's
`replay(hist_up_to(k))` to 15 stages; checks quiescence, well-formedness,
the four block events each changing the state and landing on the next
stage, the driver's reproduction of the stream, `productivity_report(15)`
against `artifacts/represented.json`; then the budget trichotomy on all
64 descriptors over a basis of worlds and events, the audit countermodel
(saturating decrement) on all 64, and the integer arithmetic that the
mirror once got wrong.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u50_horizon.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation import completion as C, represented as R  # noqa: E402


def spec_world(k: int) -> R.World:
    """Lean's `specWorld k` (Horizon.lean 53-56), Python (book)."""
    return R.World(data=tuple(range(k + 1)),
                   views=tuple((i + 1,) for i in range(k)),
                   reqs=tuple((0, i + 1) for i in range(k)),
                   refusals=(), budget=0, aug_licensed=True, notes=())


def intermediates(m: int) -> tuple[R.World, R.World, R.World]:
    """Lean's `w1 m`, `w2 m`, `w3 m` (Horizon.lean 59-74), Python (book)."""
    s = spec_world(m)
    w1 = R.replace(s, budget=1)
    w2 = R.replace(w1, data=s.data + (m + 1,))
    w3 = R.replace(w2, reqs=s.reqs + ((0, m + 1),))
    return w1, w2, w3


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "represented.json").read_text())

    print("the generated world against its specification, stage by stage:")
    for k in range(16):
        w = R.replay(R.hist_up_to(k))
        s = spec_world(k)
        same = w == s
        q, wf = R.quiescent(w), R.wf(w)
        acc = R.events_all_accepted(R.hist_up_to(k))
        if k <= 4 or k == 15:
            print(f"  k={k}: worldAt = specWorld {same}; data {list(w.data)}, views "
                  f"{[list(v) for v in w.views]}, reqs {[list(r) for r in w.reqs]}, "
                  f"budget {w.budget}; quiescent {q}, wf {wf}, all events accepted {acc}")
        if not (same and q and wf and acc):
            failures.append(f"stage {k}")

    print("block k+1 from stage k: each of the four events changes the state and the block lands on stage k+1:")
    for k in range(16):
        s = spec_world(k)
        w1, w2, w3 = intermediates(k)
        a = R.step(s, ("setBudget", 1))
        b = R.step(w1, ("admit", k + 1))
        c = R.step(w2, ("require", 0, k + 1))
        d = R.step(w3, ("addView", (k + 1,)))
        ok = (a == w1 != s) and (b == w2 != w1) and (c == w3 != w2) and (d == spec_world(k + 1) != w3)
        if k <= 2:
            print(f"  k={k}: setBudget -> w1 {a == w1}, admit -> w2 {b == w2}, require -> w3 {c == w3}, "
                  f"addView -> specWorld {d == spec_world(k + 1)}; each changed {a != s and b != w1 and c != w2 and d != w3}")
        if not ok:
            failures.append(f"block {k}")
    g = R.step(R.GENESIS, ("admit", 0))
    print(f"  genesis accepted: step genesis (admit 0) = {g.json()['data']} != genesis {g != R.GENESIS}")
    if g == R.GENESIS:
        failures.append("genesis")
    silent = R.step(R.GENESIS, ("setBudget", 0))
    print(f"  an unguarded event can change nothing: step genesis (setBudget 0) == genesis {silent == R.GENESIS} "
          f"(so 'changed' certifies 'accepted', not the converse)")
    if silent != R.GENESIS:
        failures.append("silent")

    print("the guards at every stage (old columns blind, the new column separates):")
    for m in range(6):
        blind = all(not R.sep(c, 0, m + 1) for c in spec_world(m).views)
        new = R.sep((m + 1,), 0, m + 1)
        _, w2, w3 = intermediates(m)
        req = R.req_ok(w2, 0, m + 1)
        unsat = not R.sat(w3, (0, m + 1))
        inc = R.increase(w3, (m + 1,))
        aug = R.aug_ok(w3, (m + 1,)) and w3.aug_licensed and w3.budget > 0
        print(f"  m={m}: old columns blind {blind}, new column separates {new}, reqOk {req}, "
              f"new req unsatisfied in w3 {unsat}, increase {inc}, full addView guard {aug}")
        if not (blind and new and req and unsat and inc and aug):
            failures.append(f"guards {m}")

    print("lifted to the driver:")
    for k in (0, 3, 10, 15):
        h = C.tower_gen(k)
        w = R.replay(h)
        print(f"  k={k}: towerGen = histUpTo {h == R.hist_up_to(k)}, quiescent {R.quiescent(w)}, wf {R.wf(w)}")
        if not (h == R.hist_up_to(k) and R.quiescent(w) and R.wf(w)):
            failures.append(f"driver {k}")
    rep = R.productivity_report(15)
    same = rep == art["productivity"]
    print(f"  productivity_report(15) equals the artifact: {same}; rows {len(rep['rows'])}, "
          f"all_quiescent {rep['all_quiescent']}, all_events_accepted {rep['all_events_accepted']}")
    if not same:
        failures.append("artifact")

    print("the budget pin on all 64 descriptors:")
    sat0 = R.World(data=(10, 20), views=((0,),), reqs=((0, 1),), budget=0)
    worlds = [w for (_, w, _) in C.PROBES] + [sat0, spec_world(3)]
    events = [e for (_, _, e) in C.PROBES] + [
        ("mark", (1,), 0), ("addView", (2,)), ("setBudget", 5), ("note", 1),
        ("setAugLicense", False), ("admit", 7), ("require", 0, 1), ("refuse", 0, 1)]
    kinds = {"same": 0, "decrement": 0, "set": 0}
    neg = 0
    for d in C.all_descs():
        for w in worlds:
            for e in events:
                b = C.interp_step(d, w, e).budget
                if b < 0:
                    neg += 1
                if e[0] == "setBudget" and b == e[1]:
                    kinds["set"] += 1
                elif b == w.budget:
                    kinds["same"] += 1
                elif b == max(0, w.budget - 1):
                    kinds["decrement"] += 1
                else:
                    failures.append(f"trichotomy {d} {w.budget} {e}")
    total = 64 * len(worlds) * len(events)
    print(f"  {total} (descriptor, world, event) triples: unchanged {kinds['same']}, saturating decrement "
          f"{kinds['decrement']}, set {kinds['set']}; negative budgets {neg}")
    if neg:
        failures.append("negative")
    noop = all(C.interp_step(d, sat0, ("mark", (1,), 0)) == sat0 for d in C.all_descs())
    audit = (True, True, False, False, True, True)
    print(f"  the audit countermodel: mark (1,) 0 at budget 0 is a no-op for all 64 {noop}; "
          f"for the audit descriptor {C.interp_step(audit, sat0, ('mark', (1,), 0)) == sat0}")
    if not noop:
        failures.append("saturation")
    print(f"  the arithmetic: Python 0 - 1 = {0 - 1}; max(0, 0 - 1) = {max(0, 0 - 1)}; Lean Nat 0 - 1 = 0")
    print(f"  markApply off the view store: views {[list(v) for v in R.mark_apply(sat0, (1,), 0).views]} "
          f"unchanged {R.mark_apply(sat0, (1,), 0) == sat0}")
    if R.mark_apply(sat0, (1,), 0) != sat0:
        failures.append("markApply")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
