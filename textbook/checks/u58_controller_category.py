"""Unit 58 check: the controller class, its live census, the three
countermodels, the constant simulations and the strict twist.

Runs Genesis's mirror of `ControllerCategory` and adds Python (book)
counts: how many of the 1024 controllers resolve OBST5 by the two-rule
block (more than the 128 live ones), and that both halted states are
inert under every one of the 1024 controllers on the declared basis.
Compares the report with `artifacts/primitive_controller_category.json`.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u58_controller_category.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.controller_category import (  # noqa: E402
    BASIS_EVENTS,
    BASIS_STATES,
    DUPSTATE,
    FULL_K,
    HALTED0,
    HALTED1,
    LOBST,
    NO_ADD_K,
    NO_BUDGET_K,
    NO_REFINE_K,
    NO_REFUSE_K,
    OBST0,
    OBST5,
    TWORULE_BLOCK,
    all_kinds,
    controller_category_report,
    erase_ref,
    has_dup,
    interp_k,
    live_behavior_classes,
    replay_k,
    response_kind_countermodels,
    response_live,
    twist_f,
)
from derivation.primitive_passage import GENESIS_P, grow_hist, next_family_p, obst_p, preplay  # noqa: E402


def main() -> int:
    failures: list[str] = []
    kinds = all_kinds()
    live = [d for d in kinds if response_live(d)]
    print(f"controllers {len(kinds)}; live {len(live)}; full live {response_live(FULL_K)}; "
          f"no-refuse live {response_live(NO_REFUSE_K)}")
    if len(kinds) != 1024 or len(live) != 128:
        failures.append("census")

    resolves = [d for d in kinds
                if not obst_p(replay_k(d, TWORULE_BLOCK, OBST5), 0, 1)]
    print(f"live controllers resolving OBST5 by the block: "
          f"{sum(1 for d in live if d in resolves)} of 128; "
          f"Python (book): all controllers resolving it: {len(resolves)}")
    if any(d not in resolves for d in live) or len(resolves) != 512:
        failures.append("tworule")

    cms = response_kind_countermodels()
    for name, dead, state in (("addCol", NO_ADD_K, OBST5), ("setBudget", NO_BUDGET_K, OBST0),
                              ("refineCol", NO_REFINE_K, LOBST)):
        rec = cms[name]
        battery = next_family_p(state)
        persists = battery != [] and all(obst_p(replay_k(dead, blk, state), 0, 1) for blk in battery)
        print(f"  without {name}: battery {len(battery)} blocks, obstruction persists {persists}, "
              f"full resolves {rec['full_controller_resolves']}")
        if not (persists and rec["obstruction_persists_on_all_blocks"] and rec["full_controller_resolves"]):
            failures.append(name)

    nonrefuse = [e for e in BASIS_EVENTS if e[0] != "refuse"]
    agree = all(interp_k(FULL_K, s, e) == interp_k(NO_REFUSE_K, s, e)
                for s in BASIS_STATES for e in nonrefuse)
    differ = interp_k(FULL_K, OBST5, ("refuse", 0, 1)) != interp_k(NO_REFUSE_K, OBST5, ("refuse", 0, 1))
    print(f"full vs no-refuse: agree on refusal-free cells {agree}; differ at refuse on OBST5 {differ}; "
          f"distinct live behaviours on the basis {live_behavior_classes()}")
    if not (agree and differ) or live_behavior_classes() != 128:
        failures.append("nonunique")

    inert_all = all(interp_k(d, h, e) == h for d in kinds for h in (HALTED0, HALTED1) for e in BASIS_EVENTS)
    print(f"Python (book): both halted states inert under all 1024 controllers on the basis: {inert_all}; "
          f"halted states distinct: {HALTED0 != HALTED1}")
    if not inert_all or HALTED0 == HALTED1:
        failures.append("constants")

    def comm(f, src, tgt):
        return all(f(interp_k(src, s, e)) == interp_k(tgt, f(s), e)
                   for s in BASIS_STATES + (DUPSTATE,) for e in BASIS_EVENTS)
    tw, er = comm(twist_f, FULL_K, NO_REFUSE_K), comm(erase_ref, FULL_K, NO_REFUSE_K)
    reach = [preplay(grow_hist(k), GENESIS_P) for k in range(6)]
    on_orbit = all(twist_f(s) == erase_ref(s) and not has_dup(s.occ) for s in reach)
    print(f"twist square {tw}; erase square {er}; twist != erase at DUPSTATE "
          f"{twist_f(DUPSTATE) != erase_ref(DUPSTATE)}; equal on {len(reach)} replayed states {on_orbit}")
    if not (tw and er and on_orbit) or twist_f(DUPSTATE) == erase_ref(DUPSTATE):
        failures.append("strict")

    art = json.loads((ROOT / "artifacts" / "primitive_controller_category.json").read_text())
    rep = controller_category_report()
    print(f"report equals artifact: {rep == art}; initiality {rep['initiality']}; "
          f"strict {rep['strict_refinement']['global_uniqueness']}")
    if rep != art:
        failures.append("artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
