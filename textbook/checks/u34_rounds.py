"""Unit 34 check: the declared round shape holds on every exported closed
round, and the bound follows.

For both closed baselines (no supply) every creation edge imposes one fresh
demand, admits no fresh datum, keeps the demands ordered, bounded and
duplicate-free, and the deepest round is within n(n-1)/2. Sample
computation; the theorems are Rounds.round_reqs_succ, round_data_eq and
closedRun_round_bound_from_empty. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u34_rounds.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import Bounds, NewDatum, NewForm, NewInst, delta_events  # noqa: E402
from derivation.engine import READING_F, READING_L, build_tree  # noqa: E402
from derivation.model import AdmitDatum, Impose, replay  # noqa: E402
from derivation.observe import satisfies  # noqa: E402

BOUNDS = Bounds(max_items=2, max_arity=2)


def respond(r, i, j, delta):
    """Lean's `respond`: impose, then apply the delta."""
    return replay((Impose(i, j),) + delta_events(r, delta), r)


def main() -> int:
    failures: list[str] = []
    bare2 = replay([AdmitDatum("a"), AdmitDatum("b")])
    u0 = respond(bare2, 0, 1, (NewForm(1), NewInst(0, (0,))))
    print(f"bare2 reqs {sorted(bare2.reqs)}; one round at (0, 1) with the mark: reqs "
          f"{sorted(u0.reqs)}, data {u0.n_data()}")
    if set(u0.reqs) != {(0, 1)} or u0.n_data() != 2:
        failures.append("anatomy")
    unanswered = respond(bare2, 0, 1, ())
    print(f"empty response replays, reqs {sorted(unanswered.reqs)}, "
          f"recorded demands met: {satisfies(unanswered)}")
    if set(unanswered.reqs) != {(0, 1)} or satisfies(unanswered):
        failures.append("replay versus validity")
    grown = respond(bare2, 0, 1, (NewDatum(), NewForm(1), NewInst(0, (0,))))
    print(f"a round whose response admits a datum: data {grown.n_data()} (not a closed round)")
    if grown.n_data() != 3:
        failures.append("newDatum")

    for reading, name in ((READING_L, "L"), (READING_F, "F")):
        t = build_tree(reading, "mu1", BOUNDS, max_rounds=15,
                       pre_expansion_node_guard=200, supply=False)
        n = t.nodes[0].regime.n_data()
        rounds = 0
        shape = True
        for e in t.edges:
            if e.kind != "creation":
                continue
            rounds += 1
            p, c = t.nodes[e.parent].regime, t.nodes[e.child].regime
            new = [q for q in c.reqs if q not in p.reqs]
            fresh = len(new) == 1 and len(c.reqs) == len(p.reqs) + 1
            no_datum = not any(isinstance(it, NewDatum) for it in e.response)
            ordered = all(q[0] < q[1] < c.n_data() for q in c.reqs)
            nodup = len(set(c.reqs)) == len(c.reqs)
            shape &= fresh and no_datum and ordered and nodup and c.n_data() == p.n_data()
        depth = t.stats()["max_depth"]
        print(f"reading {name}: {n} data, {rounds} creation edges, every round fresh, "
              f"datum-fixed, ordered, nodup: {shape}; deepest round {depth}, "
              f"2*{depth} <= {n}*{n - 1}: {2 * depth <= n * (n - 1)}")
        if not shape or 2 * depth > n * (n - 1):
            failures.append(name)
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
