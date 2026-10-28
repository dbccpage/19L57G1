"""Unit 16 check: the Challenge 3 demand is not met by the Challenge 2 regime.

Runs Genesis's own Python model. This is sample computation, not a proof;
the proof is Derivation.R2L_collapsed / R2F_collapsed with
separable_not_collapsed. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u16_demand_fails.py
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.candidates import Bounds  # noqa: E402
from derivation.engine import (  # noqa: E402
    GENESIS_F,
    GENESIS_L,
    READING_F,
    READING_L,
    challenge3_report,
)
from derivation.model import (  # noqa: E402
    AdmitDatum,
    AdmitForm,
    AdmitRuleAll,
    Impose,
    replay,
    step,
)
from derivation.observe import (  # noqa: E402
    collapsed_pairs,
    contexts,
    satisfies,
    separable,
    witness,
)


def main() -> int:
    failures: list[object] = []

    # 1. The two Challenge 2 regimes, the two demands.
    for name, hist, (i, j) in (("L", GENESIS_L, READING_L.target),
                               ("F", GENESIS_F, READING_F.target)):
        r = replay(hist)
        demanded = step(r, Impose(i, j))
        print(f"reading {name}: data={r.data} contexts={len(contexts(r))} "
              f"separable({i},{j})={separable(r, i, j)} "
              f"witness={witness(r, i, j)} collapsed_pairs="
              f"{collapsed_pairs(r)} satisfies(after Impose)="
              f"{satisfies(demanded)}")
        if (separable(r, i, j) or witness(r, i, j) is not None
                or contexts(r) or satisfies(demanded)):
            failures.append(("current regime", name))
        if r.reqs:
            failures.append(("python base carries no demand", name))
        if demanded.reqs != frozenset({(i, j)}):
            failures.append(("impose", name, demanded.reqs))

    # 2. Genesis's own report and artifact say the same.
    for reading in (READING_L, READING_F):
        rep = challenge3_report(reading, Bounds(2, 2))
        if rep["current_regime_satisfies"] is not False or rep["witness"]:
            failures.append(("report", reading.name))
    art = json.loads((ROOT / "artifacts" / "challenges.json").read_text())
    claims = json.loads((ROOT / "artifacts" / "claims.json").read_text())
    print(f"artifact challenge3 current_regime_satisfies: "
          f"L={art['challenge3']['L']['current_regime_satisfies']} "
          f"F={art['challenge3']['F']['current_regime_satisfies']}; "
          f"claims CL-3-FAIL-CURRENT={claims['CL-3-FAIL-CURRENT']}")
    if (art["challenge3"]["L"]["current_regime_satisfies"]
            or art["challenge3"]["F"]["current_regime_satisfies"]
            or claims["CL-3-FAIL-CURRENT"] != {"L": False, "F": False}):
        failures.append("artifact")

    # 3. Forms and rules do not help; only an instance would (Unit 10).
    # Every instance-free regime with 2..4 data, any forms up to arity 2
    # and any rules fails every demand it could carry.
    count = 0
    for n in (2, 3, 4):
        for forms in itertools.chain.from_iterable(
                itertools.product((1, 2), repeat=k) for k in range(3)):
            for rules in range(len(forms) + 1):
                hist = [AdmitDatum(f"t{k}") for k in range(n)]
                hist += [AdmitForm(a) for a in forms]
                hist += [AdmitRuleAll(f) for f in range(rules)]
                r = replay(hist)
                for i, j in itertools.combinations(range(n), 2):
                    count += 1
                    if satisfies(step(r, Impose(i, j))):
                        failures.append(("instance-free", n, forms, rules,
                                         (i, j)))
    print(f"instance-free regimes with a demand imposed: {count} cases, "
          f"none satisfied")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
