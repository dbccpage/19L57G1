"""Unit 31 check: the transition relation is carried by a renaming; the
index-least selection is not.

The regression regime of Genesis's test suite: four data, one unary form,
marks on data 2 and 3. Renaming by (2, 3, 0, 1) keeps the canonical key
and the collapsed pairs (0, 1), (2, 3), carries (0, 1) to (2, 3), and the
children of the index-least pair differ while the children of the
related pair agree. Over all 24 renamings the full expansion (every
orbit, every minimum response class) gives the same child classes.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u31_transition.py
"""
from __future__ import annotations

import sys
from itertools import permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import Bounds, delta_events, min_responses  # noqa: E402
from derivation.engine import _quotient, closure_challenge_orbits  # noqa: E402
from derivation.iso import CanonKey, canonical, rename  # noqa: E402
from derivation.model import AdmitDatum, AdmitForm, AdmitInst, Impose, Pair, Regime, replay  # noqa: E402
from derivation.observe import collapsed_pairs  # noqa: E402

BOUNDS = Bounds(max_items=2, max_arity=2)


def children(r: Regime, target: Pair) -> frozenset[CanonKey]:
    mr = min_responses(r, target, "mu1", BOUNDS)
    assert mr is not None
    return frozenset(
        canonical(replay((Impose(target[0], target[1]),) + delta_events(r, rep), r))
        for rep, _ in _quotient(r, target, mr)
    )


def expansion(r: Regime) -> frozenset[CanonKey]:
    out: set[CanonKey] = set()
    for target in closure_challenge_orbits(r):
        out |= children(r, target)
    return frozenset(out)


def main() -> int:
    failures: list[str] = []
    reg = replay([AdmitDatum("a"), AdmitDatum("b"), AdmitDatum("c"),
                  AdmitDatum("d"), AdmitForm(1), AdmitInst(0, (2,)),
                  AdmitInst(0, (3,))])
    pi = (2, 3, 0, 1)
    rr = rename(reg, pi, (0,))
    print(f"regRegime insts {sorted(reg.insts)}; renamed insts {sorted(rr.insts)}")
    print(f"collapsed: {collapsed_pairs(reg)} and {collapsed_pairs(rr)}; "
          f"same canonical key: {canonical(reg) == canonical(rr)}")
    if collapsed_pairs(reg) != ((0, 1), (2, 3)) or collapsed_pairs(rr) != ((0, 1), (2, 3)):
        failures.append("collapsed")
    if canonical(reg) != canonical(rr):
        failures.append("canonical")
    mapped = (min(pi[0], pi[1]), max(pi[0], pi[1]))
    print(f"mapReq of (0, 1) under the renaming: {mapped}")
    least_differ = children(reg, (0, 1)) != children(rr, (0, 1))
    related_agree = children(reg, (0, 1)) == children(rr, mapped)
    print(f"children of the index-least pair (0, 1) on both sides differ: {least_differ}; "
          f"children of (0, 1) and of its image {mapped} agree: {related_agree}")
    if not (least_differ and related_agree):
        failures.append("selection")
    orbits = closure_challenge_orbits(reg)
    print(f"challenge orbits of regRegime: {orbits}")
    if orbits != ((0, 1), (2, 3)):
        failures.append("orbits")
    base = expansion(reg)
    ok = all(expansion(rename(reg, p, (0,))) == base for p in permutations(range(4)))
    print(f"expansion has {len(base)} child classes; equal under all 24 renamings: {ok}")
    if not ok:
        failures.append("expansion")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
