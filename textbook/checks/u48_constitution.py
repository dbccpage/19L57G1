"""Unit 48 check: the generated stream, the closure family, and the constitution family.

Runs Genesis's Stage V mirror in `code/derivation/completion.py`: the
driver against the supplied stream to 15 stages (the ladder's rungs
printed per stage), the closure family on the pigeonhole story and the
stop outcome, the fresh-name scope, the 64-member constitution family with
the kernel's description executing exactly as `step` on a battery of
worlds and events, how many descriptions differ from the kernel on that
battery, and `protocols_report(15)` against `artifacts/completion_protocols.json`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u48_constitution.py
"""
from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation import completion as C, represented as R  # noqa: E402


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "completion_protocols.json").read_text())

    print("the driver, stage by stage (prefix, family size, block head, carrier growth, reproduces):")
    for k in range(6):
        h, h1 = C.tower_gen(k), C.tower_gen(k + 1)
        w = R.replay(h)
        fam = C.next_family(w, "tower")
        prefix = h1[: len(h)] == h
        head = fam[0][0] if fam else None
        grows = len(R.replay(h1).data) > len(w.data)
        rep = h == R.hist_up_to(k)
        print(f"  k={k}: prefix {prefix}, family {len(fam)}, head {head}, grows {grows}, "
              f"reproduces {rep}, fresh {C.fresh_name(w)} not in data {C.fresh_name(w) not in w.data}")
        if not (prefix and len(fam) == 1 and head == ("setBudget", 1) and grows and rep):
            failures.append(f"ladder {k}")
    print(f"  towerGen 2: {C.tower_gen(2)}")
    print(f"  genWorld 2: {R.replay(C.tower_gen(2)).json()}")
    reproduces15 = all(C.tower_gen(k) == R.hist_up_to(k) for k in range(16))
    print(f"  reproduces to stage 15: {reproduces15}")
    if not reproduces15:
        failures.append("reproduce")

    print("the policy is an argument, not a field any event writes:")
    print(f"  next_family(w, policy) takes the policy by hand; the kernel's events: "
          f"{sorted({e[0] for e in C.tower_gen(3)})}")

    print("the closure family and the stop outcome:")
    story = R.replay(C.PIGEON)
    fam = C.next_family(story, "close")
    quiet = R.replay(C.tower_gen(3))
    print(f"  close on the story: {fam}; idle: {C.next_family(story, 'idle')}; "
          f"close on the quiescent stage-3 world: {C.next_family(quiet, 'close')}")
    if fam != [[("addView", (1,))], [("addView", (2,))]] or C.next_family(quiet, "close"):
        failures.append("close")

    print("fresh names off the tower:")
    bad = R.World(data=(1,))
    print(f"  world with data [1]: fresh_name {C.fresh_name(bad)} in data {C.fresh_name(bad) in bad.data}")
    if C.fresh_name(bad) not in bad.data:
        failures.append("fresh")

    print("the constitution family:")
    descs = C.all_descs()
    print(f"  members {len(descs)}; kernel description in it {C.KERNEL_DESC in descs}")
    worlds = [story, quiet, R.TRUNC_WORLD, R.HEAD_A, replace(story, budget=0),
              replace(story, aug_licensed=False), R.World(data=(5,), budget=9)]
    events: list[R.Event] = [("admit", 10), ("admit", 5), ("require", 1, 2), ("require", 2, 0),
                             ("mark", (0,), 1), ("mark", (), 0), ("addView", (1,)),
                             ("addView", (0,)), ("refuse", 1, 2), ("refuse", 0, 1),
                             ("note", 3), ("setBudget", 4), ("setAugLicense", False)]
    battery = [(w, e) for w in worlds for e in events]
    same = all(C.interp_step(C.KERNEL_DESC, w, e) == R.step(w, e) for w, e in battery)
    print(f"  kernel description = step on {len(battery)} (world, event) pairs: {same}")
    if len(descs) != 64 or C.KERNEL_DESC not in descs or not same:
        failures.append("family")
    differing = sum(1 for d in descs
                    if any(C.interp_step(d, w, e) != R.step(w, e) for w, e in battery))
    print(f"  descriptions that differ from the kernel somewhere on the battery: {differing} of 64")
    if differing != 63:
        failures.append("separation")
    relaxed = (False,) + C.KERNEL_DESC[1:]
    print(f"  dedup off, admit 10 on the story: data {C.interp_step(relaxed, story, ('admit', 10)).data}")

    rep = C.protocols_report(15)
    agree = rep == art
    print(f"  protocols_report(15) equals the artifact: {agree}")
    if not agree:
        failures.append("artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
