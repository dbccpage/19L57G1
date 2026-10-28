"""Unit 46 check: the common state and Rule 1 on the represented kernel.

Python (book) for the common state (`CommonState` has no Genesis Python
mirror): a transport of `World` with retention and protection fed from
one store, the three-condition obstruction, and the four independence
witnesses. Genesis's `code/derivation/completion.py` for the extension
family and the close family (`aug_family`, `close_blocks`), compared with
`artifacts/completion_protocols.json`. Genesis's `represented.py` for
refusal inertness, the signature dichotomy over every event kind, the
fidelity reduction and the retraction countermodel.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u46_completion.py
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation import completion as C  # noqa: E402
from derivation import represented as R  # noqa: E402

Pair = tuple[int, int]


@dataclass(frozen=True)
class Common:
    """Lean's `CommonState` (book)."""
    carrier: tuple[int, ...]
    meta_distinct: tuple[Pair, ...]
    pos_witness: tuple[Pair, ...]
    views: tuple[tuple[int, ...], ...]
    retained: tuple[Pair, ...]
    protected: tuple[Pair, ...]
    budget: int
    licensed: bool
    refusals: tuple[Pair, ...]


def sep_c(s: Common, i: int, j: int) -> bool:
    return any(R.sep(c, i, j) for c in s.views)


def obst_c(s: Common, i: int, j: int) -> bool:
    return (i, j) in s.retained and (i, j) in s.protected and not sep_c(s, i, j)


def of_world(w: R.World) -> Common:
    return Common(w.data, (), (), w.views, w.reqs, w.reqs, w.budget,
                  w.aug_licensed, w.refusals)


def sig(w: R.World) -> Pair:
    return (len(w.data), len(w.views))


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "completion_protocols.json").read_text())

    w = R.replay(R.PIGEON_HISTORY)
    s = of_world(w)
    print("transport of the story world:")
    rows = [(r, obst_c(s, *r), R.viol(w, r)) for r in w.reqs]
    for r, o, v in rows:
        print(f"  pair {r}: obstC {o}, violB {v}")
    print(f"  retained is protected: {s.retained == s.protected}")
    if not all(o == v for _, o, v in rows) or s.retained != s.protected:
        failures.append("transport")

    print("the three conditions, independently (retained, protected, view):")
    base = Common((0, 1), (), (), (), (), (), 0, True, ())
    cases = [
        ("retained only", replace(base, retained=((0, 1),))),
        ("protected only", replace(base, protected=((0, 1),))),
        ("both, but separated", replace(base, retained=((0, 1),), protected=((0, 1),), views=((0,),))),
        ("both, no view", replace(base, retained=((0, 1),), protected=((0, 1),))),
    ]
    verdicts = [(name, obst_c(c, 0, 1)) for name, c in cases]
    for name, v in verdicts:
        print(f"  {name}: obstC {v}")
    if [v for _, v in verdicts] != [False, False, False, True]:
        failures.append("independence")

    print("extension family (Genesis completion.aug_family) and close family:")
    fam12 = C.aug_family(w, (1, 2))
    fam01 = C.aug_family(w, (0, 1))
    blocks = C.close_blocks(w)
    print(f"  augFamily (1,2) {fam12}; augFamily (0,1) {fam01}; close blocks {blocks}")
    w1 = R.step(w, ("addView", (1,)))
    w2 = R.step(w, ("addView", (2,)))
    print(f"  both orientations discharge and quiesce: {R.quiescent(w1)}, {R.quiescent(w2)}; "
          f"the two outcomes differ: {w1 != w2}")
    prot = C.protocols_report(15)
    keys = ["close_family_retains_both_orientations", "close_family_size_on_pigeonhole",
            "stop_outcome_empty_family", "G2_driver_reproduces_supplied_stream"]
    agree = {k: prot[k] == art[k] for k in keys}
    print(f"  artifact agrees on {agree}; values {[prot[k] for k in keys]}")
    if not (fam12 == [(1,), (2,)] and fam01 == [(1,)] and len(blocks) == 2
            and R.quiescent(w1) and R.quiescent(w2) and w1 != w2 and all(agree.values())):
        failures.append("family")

    print("refusal is a record:")
    wr = R.step(w, ("refuse", 1, 2))
    inert = (wr.data, wr.views, wr.reqs, wr.budget, wr.aug_licensed) == \
        (w.data, w.views, w.reqs, w.budget, w.aug_licensed)
    same_verdicts = all(R.sat(wr, r) == R.sat(w, r) and R.viol(wr, r) == R.viol(w, r) for r in w.reqs) \
        and all(R.mark_ok(wr, v, p) == R.mark_ok(w, v, p) for (v, p) in R.response_menu(w)) \
        and all(R.aug_ok(wr, c) == R.aug_ok(w, c) for c in [(0,), (1,), (2,), (1, 2)])
    print(f"  recorded {wr.refusals}; object fields unchanged {inert}; every verdict unchanged {same_verdicts}; "
          f"extension after refusal quiesces {R.quiescent(R.step(wr, ('addView', (1,))))}")
    if not (wr.refusals == ((1, 2),) and inert and same_verdicts):
        failures.append("refusal")

    print("signature dichotomy over every event kind on the story world:")
    events = [("admit", 40), ("admit", 10), ("require", 2, 0), ("mark", (0,), 1), ("addView", (1,)),
              ("refuse", 1, 2), ("note", 3), ("setBudget", 0), ("setAugLicense", False)]
    tw = R.TRUNC_WORLD
    events_t = [("mark", (0,), 1)]
    ok = True
    for base_w, evs in ((w, events), (tw, events_t)):
        for e in evs:
            a, b = sig(base_w), sig(R.step(base_w, e))
            kind = "same" if a == b else ("carrier grows" if b[0] > a[0] else "views grow")
            print(f"  {e}: {a} -> {b} ({kind})")
            ok &= a == b or (b[0] > a[0] and b[1] == a[1]) or (b[1] > a[1] and b[0] == a[0])
    if not ok:
        failures.append("dichotomy")

    print("fidelity reduction and the retraction countermodel:")
    w0 = replace(w, reqs=())
    fid = not any(R.viol(w0, r) or R.obstructed(w0, r) for r in [(0, 1), (1, 2), (0, 2)])
    ow = R.OW_WORLD
    retracted = replace(ow, views=(ow.views[0][1:],) + ow.views[1:])
    print(f"  no requirement, no violation or obstruction: {fid}")
    print(f"  retraction keeps the signature {sig(retracted) == sig(ow)} and breaks (0,1): "
          f"{R.sat(ow, (0, 1))} -> {R.sat(retracted, (0, 1))}")
    if not (fid and sig(retracted) == sig(ow) and R.sat(ow, (0, 1)) and not R.sat(retracted, (0, 1))):
        failures.append("fidelity")

    print("witness is not separation, and back:")
    d2 = Common((0, 1), ((0, 1),), ((0, 1),), (), ((0, 1),), ((0, 1),), 0, True, ())
    tag = Common((0, 1), (), (), ((0,),), (), (), 0, True, ())
    print(f"  d2: witness {(0, 1) in d2.pos_witness}, separated {sep_c(d2, 0, 1)}, obstructed {obst_c(d2, 0, 1)}")
    print(f"  tagOnly: witness {(0, 1) in tag.pos_witness}, separated {sep_c(tag, 0, 1)}")
    print(f"  d2 with one column: obstructed {obst_c(replace(d2, views=((0,),)), 0, 1)}")
    if not (not sep_c(d2, 0, 1) and obst_c(d2, 0, 1) and sep_c(tag, 0, 1)
            and not obst_c(replace(d2, views=((0,),)), 0, 1)):
        failures.append("witness")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
