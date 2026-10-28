"""Unit 47 check: support factorization over histories, and the panel on the books.

Python (book) for `supp`, `CWorld`, `stepC` and `PanelEquiv`, which have no
Genesis Python mirror; the kernel, its verdicts and the panel verdicts are
Genesis's `code/derivation/represented.py`. Checks, on the pigeonhole story:
beginnings differing only in notes replay to the same support, repair
family, certificate and verdict (the dichotomy); worlds whose verdicts
differ have different supports (the contrapositive, over a small set of
worlds); the extended kernel's conservativity and the admission's inertness;
the joint quotient is an equivalence on every pair of a small carrier for
every panel drawn from a small column set, and the negative certificate is
exactly non-empty-and-joint-quotient for each; the ceiling against
`artifacts/represented.json`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u47_no_outside.py
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, replace
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation import represented as R  # noqa: E402

View = tuple[int, ...]
Evaluator = tuple[View, ...]


def supp(w: R.World) -> tuple[object, ...]:
    """Lean's `supp`: every field but `notes`."""
    return (w.data, w.views, w.reqs, w.refusals, w.budget, w.aug_licensed)


@dataclass(frozen=True)
class CWorld:
    base: R.World
    panel: tuple[Evaluator, ...] = ()


def step_c(cw: CWorld, e: tuple[object, ...]) -> CWorld:
    """Lean's `stepC`: base events act by `step`; admission appends a fresh evaluator."""
    if e[0] == "admitEvaluator":
        ev = e[1]
        return cw if ev in cw.panel else replace(cw, panel=cw.panel + (ev,))
    return replace(cw, base=R.step(cw.base, e))


def replay_c(h: list[tuple[object, ...]], cw: CWorld) -> CWorld:
    for e in h:
        cw = step_c(cw, e)
    return cw


def panel_equiv(panel: list[Evaluator], i: int, j: int) -> bool:
    """Lean's `PanelEquiv`: no column of any evaluator tells i from j."""
    return all((i in c) == (j in c) for E in panel for c in E)


def results(w: R.World, r: R.Req) -> tuple[object, ...]:
    return (supp(w), tuple(R.repair_family(w, r)), R.obstructed(w, r), R.quiescent(w))


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "represented.json").read_text())
    hist = R.PIGEON_HISTORY
    story = R.replay(hist)

    print("the dichotomy: beginnings differing only in notes, the story history:")
    for notes in [(), (7, 8), (0, 0, 0), (999,)]:
        w = R.replay(hist, replace(R.GENESIS, notes=notes))
        same = results(w, (1, 2)) == results(story, (1, 2))
        print(f"  notes {notes}: results agree {same}; notes after {w.notes}")
        if not same or w.notes != notes:
            failures.append(f"dichotomy {notes}")

    print("the contrapositive over a small set of worlds:")
    pool = [story, R.step(story, ("addView", (1,))), R.step(story, ("addView", (2,))),
            R.step(story, ("admit", 40)), R.step(story, ("refuse", 1, 2)),
            R.step(story, ("note", 5)), R.step(story, ("setBudget", 0)), R.TRUNC_WORLD]
    pairs = checked = 0
    for a, b in combinations(pool, 2):
        pairs += 1
        if results(a, (1, 2)) != results(b, (1, 2)):
            checked += 1
            if supp(a) == supp(b):
                failures.append("contrapositive")
    print(f"  {pairs} pairs, {checked} with a differing result, all with differing support: "
          f"{'contrapositive' not in failures}")

    print("the extended kernel:")
    ev_a: Evaluator = ((0,),)
    ev_b: Evaluator = ((0, 1),)
    ch = list(hist) + [("admitEvaluator", ev_a), ("admitEvaluator", ev_b), ("admitEvaluator", ev_a)]
    cw = replay_c(ch, CWorld(R.GENESIS))
    print(f"  base is the story {cw.base == story}; panel {cw.panel}")
    if cw.base != story or cw.panel != (ev_a, ev_b):
        failures.append("cworld")
    cw2 = step_c(cw, ("admitEvaluator", ((1,),)))
    cw3 = step_c(cw, ("addView", (1,)))
    print(f"  admission leaves the base {cw2.base == cw.base}; "
          f"a base event leaves the panel {cw3.panel == cw.panel} and acts as step "
          f"{cw3.base == R.step(cw.base, ('addView', (1,)))}")
    if cw2.base != cw.base or cw3.panel != cw.panel:
        failures.append("conservative")
    print(f"  split panel on (0,1): certPos {R.cert_pos(list(cw.panel), 0, 1)}, "
          f"certNeg {R.cert_neg(list(cw.panel), 0, 1)}")
    if R.cert_pos(list(cw.panel), 0, 1) or R.cert_neg(list(cw.panel), 0, 1):
        failures.append("split")

    print("the joint quotient on carrier {0,1,2}, every panel of up to two evaluators")
    cols: list[View] = [(), (0,), (1,), (0, 1), (0, 2), (1, 2)]
    evals: list[Evaluator] = [tuple(cs) for k in range(3) for cs in combinations(cols, k)]
    panels: list[list[Evaluator]] = [list(p) for k in range(3) for p in product(evals, repeat=k)]
    carrier = range(3)
    bad_equiv = bad_iff = 0
    for p in panels:
        for i in carrier:
            if not panel_equiv(p, i, i):
                bad_equiv += 1
            for j in carrier:
                if panel_equiv(p, i, j) != panel_equiv(p, j, i):
                    bad_equiv += 1
                if R.cert_neg(p, i, j) != (bool(p) and panel_equiv(p, i, j)):
                    bad_iff += 1
                for k in carrier:
                    if panel_equiv(p, i, j) and panel_equiv(p, j, k) and not panel_equiv(p, i, k):
                        bad_equiv += 1
    print(f"  {len(panels)} panels: equivalence failures {bad_equiv}; "
          f"certNeg vs non-empty and joint quotient failures {bad_iff}")
    if bad_equiv or bad_iff:
        failures.append("quotient")
    print(f"  empty panel: joint quotient (0,1) {panel_equiv([], 0, 1)}, "
          f"certNeg {R.cert_neg([], 0, 1)}")

    print("the ceiling, against the artifact:")
    rep = R.certification_report()
    blind = [ev_b, ev_b]
    print(f"  blind panel certifies 0 ~ 1: {R.cert_neg(blind, 0, 1)}; the story's column "
          f"[0] separates: {R.sep((0,), 0, 1)}; artifact {art['certification']}")
    if rep != art["certification"] or not R.cert_neg(blind, 0, 1):
        failures.append("ceiling")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
