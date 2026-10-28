"""Unit 43 check: the local finite-alphabet class and its five members.

Runs Genesis's own mirror (code/derivation/local_strategy.py): the five
rows against artifacts/local_strategy.json, the capacity collisions at
the exact thresholds, the facts the lesson flags (`Fires` ignores the
strategy; per-pair and valued are the same functions under two tags;
depth-two clears length 4 and not length 5; the negative locality probe),
and one book member (parity, two colours, threshold 4).
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u43_local_strategy.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.local_strategy import (  # noqa: E402
    BARE, DEPTH_TWO, PER_PAIR, PRESENCE, STRATEGIES, VALUED, ImportDiscipline,
    LocalStrategy, base_obstructions, capacity_collision, capacity_threshold,
    classification, clears_within, finite_declaration_within, finite_factor_table,
    fires_within, identity_grade_within,
)


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "local_strategy.json").read_text())
    rows = {r["name"]: r for r in art["strategies"]}

    print("five members through chain length 15 (name: radius, alphabet, tag -> classification; artifact agrees):")
    for s in STRATEGIES:
        c = classification(s, 15)
        r = rows[s.name]
        agree = (c == r["classification"] and clears_within(s, 15) == r["clears_within_bound"]
                 and identity_grade_within(s, 15) == r["identity_grade_within_bound"]
                 and finite_declaration_within(s, 15) == r["finite_declaration_within_bound"])
        print(f"  {s.name}: {s.radius}, {s.alphabet_size}, {s.import_discipline.value} -> {c}; {agree}")
        if not agree:
            failures.append(f"row {s.name}")

    print("Fires ignores the strategy: base obstructions at length 3 are", base_obstructions(3),
          "; fires_within(S, 3) for every S:", [fires_within(s, 3) for s in STRATEGIES])
    if base_obstructions(3) != ((1, 2),) or not all(fires_within(s, 3) for s in STRATEGIES):
        failures.append("fires")

    same = all(PER_PAIR.view(n, i) == VALUED.view(n, i) and PER_PAIR.colour(n, i) == VALUED.colour(n, i)
               for n in range(16) for i in range(n + 1))
    print(f"per-pair and valued: same colour and view through 15: {same}; tags "
          f"{PER_PAIR.import_discipline.value} / {VALUED.import_discipline.value}; "
          f"classifications {classification(PER_PAIR, 15)} / {classification(VALUED, 15)}")
    if not same or PER_PAIR.import_discipline == VALUED.import_discipline:
        failures.append("tags")

    thr = {s.name: capacity_threshold(s) for s in STRATEGIES}
    col = {s.name: capacity_collision(s) for s in STRATEGIES}
    print(f"thresholds k^(2d+1)+2d+2: {thr}")
    print(f"collisions at the threshold (deep pair with equal views): {col}")
    expect = {w["name"]: (w["threshold"], tuple(w["collision"])) for w in art["capacity_witnesses"]}
    for name, (t, c) in expect.items():
        if thr[name] != t or col[name] != c:
            failures.append(f"capacity {name}")
    if thr["per_pair_fresh_mark"] is not None or thr["automark_valued"] is not None:
        failures.append("non-finite threshold")

    d2 = {n: [DEPTH_TWO.view(n, i) for i in range(n + 1)] for n in (4, 5)}
    print(f"depth-two views at length 4: {d2[4]}; clears length 4: {clears_within(DEPTH_TWO, 4)}")
    print(f"depth-two views at length 5: {d2[5]}; base pairs {base_obstructions(5)}; "
          f"clears through 5: {clears_within(DEPTH_TWO, 5)}")
    if not clears_within(DEPTH_TWO, 4) or clears_within(DEPTH_TWO, 5):
        failures.append("depth-two")
    print(f"bare views at length 3: {[BARE.view(3, i) for i in range(4)]}; identity grade through 3: "
          f"{identity_grade_within(BARE, 3)}; presence is bare: {PRESENCE.view(7, 3) == BARE.view(7, 3)}")
    if identity_grade_within(BARE, 3):
        failures.append("bare identity")

    probe = finite_factor_table(0, lambda n, i: 0, lambda n, i: i, 3)
    print(f"negative locality probe (constant colour, identity view, radius 0): factor table {probe}; "
          f"artifact: {art['negative_locality_probe']}")
    if probe is not None or art["negative_locality_probe"]["constant_colour_identity_view_accepted"]:
        failures.append("probe")

    parity = LocalStrategy("parity", 0, ImportDiscipline.ONE_TIME, 2, lambda n, i: i % 2, lambda xs: xs[0])
    print(f"book member parity (2 colours, radius 0): threshold {capacity_threshold(parity)}, "
          f"collision {capacity_collision(parity)}, clears length 3: {clears_within(parity, 3)}, "
          f"clears through 4: {clears_within(parity, 4)}, classification {classification(parity, 15)}")
    if capacity_threshold(parity) != 4 or capacity_collision(parity) != (1, 3) or not clears_within(parity, 3) \
            or clears_within(parity, 4):
        failures.append("parity")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
