"""Unit 40 check: the reflective chain under depth-1 observation.

Prints the depth-1 profile table of the chain, checks that the
obstructions are exactly the interior pairs (the Lean iff, on lengths
1..15), runs the five declared repair strategies for 15 rounds and
compares every classification with `artifacts/generator.json`, shows one
instance of the outrun theorem and of the depth-2 instances, and checks
the artifact's Lean-agreement block. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u40_generator.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.generator import (  # noqa: E402
    ROUNDS, STRATEGIES, exclusion_check, lean_agreement, middle_pairs,
    obstructions, profile1, profile2, run_branch, view,
)


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "generator.json").read_text())

    print("depth-1 profiles (tagged, entered, left) of the chain of length 5:")
    for i in range(6):
        print(f"  element {i}: {profile1(5, i)}")
    classes = {profile1(5, i) for i in range(1, 5)}
    if classes != {(True, True, True)} or profile1(5, 0) != (False, False, True) \
            or profile1(5, 5) != (True, True, False):
        failures.append("profile classes")

    print("obstructions of the bare chain == interior pairs, lengths 1..15:")
    exact = all(obstructions("none", n, {}) == middle_pairs(n) for n in range(1, ROUNDS + 1))
    print(f"  {exact}; length 2: {obstructions('none', 2, {})}; length 3: {obstructions('none', 3, {})}")
    if not exact or obstructions("none", 2, {}) or obstructions("none", 3, {}) != [(1, 2)]:
        failures.append("exactness")

    print(f"five strategies, {ROUNDS} rounds: fired, first fire, repaired every round, "
          "rounds that imported, classification")
    ex = exclusion_check(ROUNDS)
    for s in STRATEGIES:
        rep = run_branch(s, ROUNDS)
        print(f"  {s:22s} {rep.fired_ever()!s:5s} {rep.first_fire_round()!s:4s} "
              f"{rep.repaired_every_round()!s:5s} {rep.per_round_import_rounds():2d} "
              f"{rep.classification()}")
        if art["exclusion"]["classification_table"][s] != rep.classification():
            failures.append(f"classification {s}")
    print(f"  endogenous cycle found: {ex['endogenous_cycle_found']} "
          f"(artifact {art['exclusion']['endogenous_cycle_found']})")
    if ex["endogenous_cycle_found"] or art["exclusion"]["endogenous_cycle_found"]:
        failures.append("cycle")

    rep = run_branch("per_pair_fresh_mark", ROUNDS)
    rows = [(r.round_no, r.obstructions_before, r.imports_this_round, r.obstructions_after)
            for r in rep.rounds]
    print("per-pair marking (round, obstructions before, imports, after): "
          f"{rows[:5]} ... {rows[-1]}")
    if any(imp == 0 for (_, before, imp, _) in rows if before) or rows[-1][1] == 0:
        failures.append("per-pair imports")

    print("outrun: marks [1, 2, 3]; at length 6 the unmarked pair (4, 5) has equal profiles: "
          f"{profile1(6, 4) == profile1(6, 5)}; presence view of 1 and 2 at length 3 equal: "
          f"{view('automark_presence', 3, 1, {}) == view('automark_presence', 3, 2, {})}; "
          f"valued view: {view('automark_valued', 3, 1, {})} vs {view('automark_valued', 3, 2, {})}")
    if profile1(6, 4) != profile1(6, 5) or \
            view("automark_presence", 3, 1, {}) != view("automark_presence", 3, 2, {}) or \
            view("automark_valued", 3, 1, {}) == view("automark_valued", 3, 2, {}):
        failures.append("repair views")

    print(f"depth 2: length 4, elements 1 and 3 differ: {profile2(4, 1) != profile2(4, 3)}; "
          f"length 5, elements 2 and 3 equal: {profile2(5, 2) == profile2(5, 3)}; "
          f"depth-2 obstructions at lengths 4..7: "
          f"{[len(obstructions('depth2', n, {})) for n in range(4, 8)]}")
    if profile2(4, 1) == profile2(4, 3) or profile2(5, 2) != profile2(5, 3):
        failures.append("depth 2")

    la = lean_agreement(ROUNDS)
    print(f"Lean agreement block: {la} (matches artifact: {la == art['lean_agreement']})")
    if la != art["lean_agreement"] or not all(la.values()):
        failures.append("lean agreement")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
