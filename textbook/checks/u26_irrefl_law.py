"""Unit 26 check: finite facts never entail the irreflexivity law. Sample
computation over Genesis's irreflexive relations and the bridge scenarios;
the proof is Bridge.irrefl_law_not_entailed. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u26_irrefl_law.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.primdiff import D2, irreflexive, irreflexive_relations_on  # noqa: E402


def main() -> int:
    failures: list[object] = []
    ext = D2.rel | {(0, 0)}
    print(f"D2 facts {sorted(D2.rel)}: irreflexive {irreflexive(D2.rel)}; "
          f"extension {sorted(ext)}: irreflexive {irreflexive(ext)}, contains the facts {D2.rel <= ext}")
    if irreflexive(ext) or not D2.rel <= ext:
        failures.append("D2")
    total = 0
    for n in range(1, 4):
        rels = irreflexive_relations_on(n)
        for rel in rels:
            total += 1
            e = rel | {(0, 0)}
            if irreflexive(e) or not rel <= e:
                failures.append(("extension", n, sorted(rel)))
        print(f"carrier {n}: {len(rels)} irreflexive fact sets, each with a non-irreflexive extension")
    print(f"total fact sets checked: {total}")
    art = json.loads((ROOT / "artifacts" / "bridge.json").read_text())
    for sc in art["scenarios"]:
        print(f"bridge scenario {sc['scenario']}: first self-edge after {sc['min_events_to']['self_edge']} events, "
              f"states reached {sc['states_reached']}")
        if sc["min_events_to"]["self_edge"] != 3:
            failures.append(("scenario", sc["scenario"]))
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
