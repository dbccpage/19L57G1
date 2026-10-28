"""Unit 45 check: the represented kernel, replayed and compared with its artifact.

Runs Genesis's mirror `code/derivation/represented.py`: the pigeonhole
progress story (violation, empty repair family, obstruction certificate,
canonical augmentation, discharge), the budget and license gates and the
unguarded replenishment, the refusal certificate, the supplied productive
run to 15 stages, the seven decided countermodels and the kernel's
behaviour on the same worlds, the panel-relative certification and the
per-length witnesses, and compares the recorded parts with
`artifacts/represented.json`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u45_represented.py
"""
from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation import represented as R  # noqa: E402


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "represented.json").read_text())

    story = R.progress_story()
    w = R.replay(R.PIGEON_HISTORY)
    print("story world:", w.json())
    print(f"  wf {R.wf(w)}; violated (1,2) {R.viol(w, (1, 2))}; "
          f"repair family (1,2) {R.repair_family(w, (1, 2))}; "
          f"obstructed (1,2) {R.obstructed(w, (1, 2))}")
    print(f"  menu: {R.response_menu(w)}")
    w2 = R.step(w, ("addView", (1,)))
    print(f"  addView [1] accepted {w2 != w}; sat (1,2) after {R.sat(w2, (1, 2))}; "
          f"quiescent after {R.quiescent(w2)}; budget {w.budget} -> {w2.budget}")
    print(f"  artifact agrees: {story == art['progress_story']}")
    if not (R.wf(w) and R.viol(w, (1, 2)) and not R.repair_family(w, (1, 2))
            and R.obstructed(w, (1, 2)) and w2 != w and R.sat(w2, (1, 2))
            and R.quiescent(w2) and story == art["progress_story"]):
        failures.append("story")

    print("gates:")
    w0 = replace(w, budget=0)
    nob = R.step(w0, ("addView", (1,))) == w0
    nom = R.step(w0, ("mark", (0,), 1)) == w0
    repl = R.step(w0, ("setBudget", 4)).budget
    wl = replace(w, aug_licensed=False)
    nol = R.step(wl, ("addView", (1,))) == wl
    print(f"  budget 0: addView no-op {nob}, mark no-op {nom}; setBudget 4 -> budget {repl} (no guard)")
    print(f"  license off: addView no-op {nol}")
    if not (nob and nom and repl == 4 and nol):
        failures.append("gates")

    print("refusal:")
    r12 = R.step(w, ("refuse", 1, 2)).refusals
    r01 = R.step(w, ("refuse", 0, 1)) == w
    after = R.step(R.step(w, ("refuse", 1, 2)), ("addView", (1,)))
    print(f"  refuse (1,2) records {r12}; refuse (0,1) (satisfied) no-op {r01}; "
          f"after refusal the augmentation still fires: {R.quiescent(after)}, refusals kept {after.refusals}")
    if not (r12 == ((1, 2),) and r01 and R.quiescent(after)):
        failures.append("refusal")

    prod = R.productivity_report(15)
    print("productive run, stages 0..15:")
    for row in prod["rows"][:4]:
        print(f"  k={row['k']}: history {row['history_length']} events, carrier {row['carrier']}, "
              f"quiescent {row['quiescent']}, prefix of next {row['prefix_of_next']}")
    flags = {k: v for k, v in prod.items() if k != "rows"}
    print(f"  ... all 16: {flags}; artifact agrees: {prod == art['productivity']}")
    if not (all(flags.values()) and prod == art["productivity"]):
        failures.append("productivity")

    cm = R.countermodel_report()
    print("countermodels (name, kind, differs):")
    for row in cm["rows"]:
        print(f"  {row['name']}: {row['kind']}, {row['differs']}")
    print(f"  artifact agrees: {cm == art['countermodels']}")
    kern_a = R.sat(R.step(R.HEAD_A, ("mark", (), 1)), (0, 1))
    kern_b = R.sat(R.step(R.HEAD_B, ("mark", (), 1)), (0, 1))
    print(f"  the kernel on the two equivalent worlds: {kern_a} and {kern_b} (equal: {kern_a == kern_b})")
    fam = R.repair_family(R.TRUNC_WORLD, (1, 2))
    print(f"  the repairs the truncated search missed: {fam}")
    if not (cm["all_exhibited"] and cm == art["countermodels"] and kern_a == kern_b
            and fam == [((0,), 1), ((0,), 2)]):
        failures.append("countermodels")

    cert = R.certification_report()
    p1 = R.cert_pos([((0,),)], 0, 1)
    p2 = R.cert_pos([((0,),), ((0, 1),)], 0, 1)
    p3 = R.cert_pos([((0,),), ((0,), (0, 1))], 0, 1)
    print(f"certification: {cert}; artifact agrees: {cert == art['certification']}")
    print(f"  panel [[0]] certifies (0,1): {p1}; add a blind evaluator: {p2}; give it the column: {p3}")
    if not (cert == art["certification"] and p1 and not p2 and p3):
        failures.append("certification")

    ko = R.koenig_report(15)
    print(f"per-length witnesses: {ko}; artifact agrees: {ko == art['koenig']}")
    print(f"  wit_valid [3,3,3] {R.wit_valid([3, 3, 3])}; wit_valid [0] {R.wit_valid([0])}")
    if not (ko == art["koenig"] and R.wit_valid([3, 3, 3]) and not R.wit_valid([0])):
        failures.append("koenig")

    mut = R.mutation_report()
    print(f"mutation: {mut}; artifact agrees: {mut == art['mutation']}")
    if mut != art["mutation"]:
        failures.append("mutation")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
