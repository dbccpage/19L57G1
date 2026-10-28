"""Unit 39 check: refusal routes and their prices.

Recomputes Genesis's protocol space (44 declared protocols), the per-route
milestones for the five routes the lesson names, the minimum table under
both cost orders, and the in-class normal-form checks, and compares them
with `artifacts/refusal_frontier.json`. Exhaustive only within the declared
6-event horizon. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u39_refusal_frontier.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.refusal_frontier import (  # noqa: E402
    Proto, cost_a, cost_b, enumerate_protocols, minimum_table,
    normal_form_check, protocol_report,
)

HORIZON = 6
ROUTES = {
    "silent": Proto(1, "none", False, False, False, 1),
    "judgment": Proto(1, "judgment", False, False, False, 1),
    "tag route": Proto(1, "datum", True, False, False, 1),
    "relation route (minimum)": Proto(1, "datum", False, False, True, 1),
    "tag + relation (stepP)": Proto(1, "datum", True, False, True, 1),
    "reflection": Proto(1, "datum", False, True, False, 1),
}
MILESTONES = ("two_carrier", "separable_pair", "oriented_pair",
              "witnessed_relation", "witnessed_irreflexive")


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "refusal_frontier.json").read_text())
    protos = enumerate_protocols()
    print(f"declared protocols: {len(protos)} (artifact {art['protocol_space_size']})")
    if len(protos) != 44 or art["protocol_space_size"] != 44:
        failures.append("space")
    by_json = {json.dumps(r["protocol"], sort_keys=True): r for r in art["protocols"]}
    print("route: min events to two_carrier / separable / oriented / witnessed / witnessed_irrefl; "
          "dynamics; cost A; cost B")
    for name, p in ROUTES.items():
        rep = protocol_report(p, HORIZON)
        m = rep["min_events_to"]
        print(f"  {name:26s} " + " / ".join(str(m[k]) for k in MILESTONES)
              + f"; {rep['dynamics']}; {cost_a(p)}; {cost_b(p)}")
        if rep != by_json[json.dumps(p.json(), sort_keys=True)]:
            failures.append(f"report {name}")
    mt = json.loads(json.dumps(minimum_table(HORIZON)))  # tuples -> lists, as the artifact
    if mt != art["minimum_table"]:
        failures.append("minimum_table")
    for order in ("A_total_imports", "B_lex"):
        for ms in MILESTONES:
            cell = mt[order][ms]
            ties = cell["tied_minima"]
            print(f"  {order:16s} {ms:21s} cost {cell['cost']}, {len(ties)} minimum protocol(s): "
                  + "; ".join(f"ret={t['retention']} tag={t['tagging']} rel={t['autorel']} tok={t['tokens']}"
                              for t in ties))
    for ms in ("witnessed_relation", "witnessed_irreflexive"):
        for order in ("A_total_imports", "B_lex"):
            ties = mt[order][ms]["tied_minima"]
            if len(ties) != 1 or ties[0] != ROUTES["relation route (minimum)"].json():
                failures.append(f"unique {order} {ms}")
    if len(mt["A_total_imports"]["two_carrier"]["tied_minima"]) != 3:
        failures.append("three ties two_carrier A")
    if len(mt["A_total_imports"]["separable_pair"]["tied_minima"]) != 2 \
            or len(mt["B_lex"]["separable_pair"]["tied_minima"]) != 1:
        failures.append("separable ties")
    nf = normal_form_check(HORIZON)
    print(f"normal form in class: holds {nf['normal_form_holds_in_class']}, every reacher made a purchase "
          f"{nf['all_made_a_purchase']}, witnessed_irreflexive reachers {nf['witnessed_irreflexive_reachers']}, "
          f"witnessed without a relation rule {nf['witnessed_without_relation_rule']}, "
          f"separable without tag or relation {nf['separable_without_tag_or_relation']}")
    if nf != art["normal_form"] or not nf["normal_form_holds_in_class"]:
        failures.append("normal_form")
    print(f"imports of the minimum route: {ROUTES['relation route (minimum)'].imports()}")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
