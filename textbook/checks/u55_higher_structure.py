"""Unit 55 check: the growth driver and the declared cell calculus.

Replays `HigherStructure` through Genesis's mirrors
(`code/derivation/primitive_passage.py` for the growth driver,
`code/derivation/higher_structure.py` for the cells): the grown state at
every stage against `path_state`; each round's obstruction, extension
proposal and resolution; quiescence and the residue; the K4 passage
history against the complex's edges; the shell guards, the ladder at
dimensions 2 and 3, the unfilled shell, the alternating statistic, the cut
census, the composite boundary and the second convention; and the
module's `growth_report` and `cells_report` against
`artifacts/primitive_passage.json`. Python (book): a one-face-short
boundary is refused at every dimension, and the alternating statistic
moves when a vertex is admitted.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u55_higher_structure.py
"""
from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.higher_structure import (  # noqa: E402
    EMPTY_COMPLEX, Complex, alt_num, bd2, bd2_neg, boundary_not_forced,
    coeff_v, cstep, creplay, cut_census, d2_zero_tet, d2_zero_triangles,
    k4, k4_boundary, k4_events, push1, shell2, shell3,
)
from derivation.primitive_passage import (  # noqa: E402
    GENESIS_P, extension_proposals, graph_at, grow_block, grow_hist,
    growth_report, k4_passage_hist, obst_p, path_state, preplay, pstep,
)
from run_primitive_passage import cells_report  # noqa: E402

ROUNDS = 15


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "primitive_passage.json").read_text())

    # --- the growth driver, round by round (Lean 72-540)
    print(f"growBlock 0 = {grow_block(0)}\ngrowBlock 1 = {grow_block(1)}\n"
          f"growBlock 2 = {grow_block(2)}")
    print(f"stage: occ wit cols spec quiescent residue | obstructed extension resolves")
    for k in range(ROUNDS):
        g = graph_at(k + 1)
        spec = path_state(k)
        pre = preplay(grow_block(k + 2)[:5], spec)  # up to setBudget 1
        obstructed = obst_p(pre, k + 1, k + 2)
        ext = (k + 1,) in extension_proposals(pre, k + 1, k + 2)
        lands = pstep(pre, ("addCol", (k + 1,))) == path_state(k + 1)
        quiet = all(not obst_p(g, r[0], r[1]) for r in g.prot)
        cols = 0 if g.obs is None else len(g.obs)
        if k < 4 or k == ROUNDS - 1:
            print(f"  {k + 1:2}: {len(g.occ):3} {len(g.wit):3} {cols:4} "
                  f"{g == spec!s:5} {quiet!s:5} {len(g.occ) - len(g.wit):7} | "
                  f"{obstructed!s:10} {ext!s:9} {lands}")
        if not (g == spec and quiet and obstructed and ext and lands
                and len(g.occ) == k + 2 and len(g.wit) == k + 1
                and grow_block(k + 2)[-1] == ("addCol", (k + 1,))):
            failures.append(f"round {k + 1}")
    print(f"  (stages 5-{ROUNDS - 1} elided; all {ROUNDS} checked)")
    # the obstruction is not there before the budget: g3 has budget 0, still obstructed;
    # what the budget gates is the resolution, not the obstruction
    g3 = preplay(grow_block(2)[:4], path_state(0))
    print(f"inside round 2 before funding: budget={g3.budget} obst(1,2)={obst_p(g3, 1, 2)} "
          f"addCol [1] inert={pstep(g3, ('addCol', (1,))) == g3}")
    if not (obst_p(g3, 1, 2) and pstep(g3, ("addCol", (1,))) == g3):
        failures.append("budget gates the resolution")
    gr = growth_report(ROUNDS)
    print(f"growth_report({ROUNDS}) matches artifact: {gr == art['growth']}")
    if gr != art["growth"]:
        failures.append("growth_report vs artifact")

    # --- the K4 skeleton from the passage (Lean 664-680, 708-712)
    ps = preplay(k4_passage_hist(), GENESIS_P)
    full = k4()
    print(f"K4 passage: wit={ps.wit} quiescent="
          f"{all(not obst_p(ps, r[0], r[1]) for r in ps.prot)} "
          f"c1 agrees={tuple(ps.wit) == full.c1}")
    if tuple(ps.wit) != full.c1 or tuple(ps.prot) != full.c1:
        failures.append("k4 skeleton")

    # --- the cell calculus (Lean 555-716)
    print(f"k4 = c0 {full.c0} c1 {len(full.c1)} edges c2 {full.c2} c3 {full.c3}")
    if full != Complex((0, 1, 2, 3), ((0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (0, 3)),
                       ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)), ((0, 1, 2, 3),)):
        failures.append("k4_builds")
    shell = k4_boundary()
    print(f"k4Boundary: shell3(0,1,2,3)={shell3(shell, 0, 1, 2, 3)} c3={shell.c3}")
    if not (shell3(shell, 0, 1, 2, 3) and shell.c3 == ()):
        failures.append("filling_not_forced")
    guard = Complex(c0=(0, 1, 2), c1=((0, 1),))
    print(f"shell guard: addT over one edge is inert: {cstep(guard, ('addT', 0, 1, 2)) == guard}")
    if cstep(guard, ("addT", 0, 1, 2)) != guard:
        failures.append("shell_guard_load_bearing")
    # ladder_dim2/dim3 instances: the step adds exactly the cell and changes the complex
    edges = creplay(k4_events()[:10], EMPTY_COMPLEX)
    t = cstep(edges, ("addT", 0, 1, 2))
    q = cstep(shell, ("addQ", 0, 1, 2, 3))
    print(f"ladder dim 2 at the edge stage: shell2={shell2(edges, 0, 1, 2)} "
          f"added={(0, 1, 2) in t.c2} changed={t != edges}")
    print(f"ladder dim 3 at k4Boundary: added={(0, 1, 2, 3) in q.c3} changed={q != shell} "
          f"equals k4={q == full}")
    if not (shell2(edges, 0, 1, 2) and (0, 1, 2) in t.c2 and t != edges
            and (0, 1, 2, 3) in q.c3 and q == full):
        failures.append("ladder instances")

    # Python (book): a boundary short of one face is refused, at every dimension.
    horn1 = Complex(c0=(0,))                       # one endpoint absent
    horn2 = Complex(c0=(0, 1, 2), c1=((0, 1), (1, 2)))  # edge (0,2) absent
    horn3 = creplay(k4_events()[:13], EMPTY_COMPLEX)  # triangle (1,2,3) absent
    refused = (cstep(horn1, ("addE", 0, 1)) == horn1
               and cstep(horn2, ("addT", 0, 1, 2)) == horn2
               and cstep(horn3, ("addQ", 0, 1, 2, 3)) == horn3)
    print(f"Python (book): one face short, refused at dimensions 1, 2, 3: {refused}")
    if not refused:
        failures.append("horn refused")

    # --- the alternating statistic and the cut census (Lean 722-754)
    stages = {"vertices": alt_num(creplay(k4_events()[:4], EMPTY_COMPLEX)),
              "edges": alt_num(edges), "shell": alt_num(shell), "solid": alt_num(full)}
    print(f"alt_num along the stages: {stages}")
    if stages != {"vertices": 4, "edges": -2, "shell": 2, "solid": 1}:
        failures.append("altNum_stages")
    plus_v = cstep(full, ("addV", 4))
    print(f"Python (book): alt_num after admitting a fifth vertex to k4: {alt_num(plus_v)} "
          f"(was {alt_num(full)}): the statistic moves under admission")
    if alt_num(plus_v) == alt_num(full):
        failures.append("altNum moves")
    census = {n: cut_census(n, 0, 1) for n in (2, 3, 4, 5)}
    print(f"cut census (two-block observations of n points separating 0 from 1): {census}")
    if census != {2: 1, 3: 2, 4: 4, 5: 8}:
        failures.append("cut_census")

    # --- the boundary calculus (Lean 765-813)
    print(f"d2 zero on the four triangles: {d2_zero_triangles(full)}; "
          f"on the solid cell: {d2_zero_tet(full, (0, 1, 2, 3))}")
    print(f"push1(bd2 (0,1,2)) = {push1(bd2((0, 1, 2)))}; coefficients at 0,1,2 = "
          f"{[coeff_v(v, push1(bd2((0, 1, 2)))) for v in (0, 1, 2)]}")
    print(f"bd2 != bd2_neg on (0,1,2): {bd2((0, 1, 2)) != bd2_neg((0, 1, 2))}; "
          f"boundary_not_forced: {boundary_not_forced((0, 1, 2))}")
    if not (d2_zero_triangles(full) and d2_zero_tet(full, (0, 1, 2, 3))
            and boundary_not_forced((0, 1, 2))):
        failures.append("boundary calculus")

    cr = cells_report()
    inv = art["cells"]["invariants"]
    print(f"cells_report() matches artifact cells: {cr == art['cells']}; "
          f"artifact cut_census {inv['cut_census']} alt_num_stages {inv['alt_num_stages']}")
    if cr != art["cells"]:
        failures.append("cells_report vs artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
