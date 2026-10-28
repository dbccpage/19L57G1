"""Unit 44 check: the difference interface's concrete realization.

Runs Genesis's mirror (code/derivation/diff_interface.py): the tower
rounds against artifacts/diff_interface.json, the one-step fuel driver,
the eight Boolean views, the five countermodels, and two book
observations: the countermodel pairs become active as soon as the stage
is protected, and a three-valued view closes the three-point stage.
AuthorityEffect: None.
Run from the repository root: python textbook/checks/u44_diff_interface.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.diff_interface import (  # noqa: E402
    active_pairs, bool_grammar_report, countermodel_report, cview, drive, fuel_report,
    measure, obstruction_active, swap_top, tower_demand_support, tower_next, tower_report,
)


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "diff_interface.json").read_text())

    tr = tower_report(15)
    print("tower, rounds 0..14: closed measure before, pre-closure measure, demand support, measure after")
    for r in tr["rounds"][:4]:
        print(f"  round {r['round']}: {r['closed_measure_before']}, {r['preclose_measure']}, "
              f"{r['demand_support']}, {r['closed_measure_after']}")
    flags = {k: tr[k] for k in ("all_closed_before", "all_obstruct_after_reflection",
                                "all_strictly_decrease", "all_preserve_old")}
    print(f"  ... all 15 rounds: {flags}; uniform demand bound {tr['uniform_demand_bound']}; artifact agrees: "
          f"{tr['rounds'] == art['tower']['rounds']}")
    if not all(flags.values()) or tr["rounds"] != art["tower"]["rounds"]:
        failures.append("tower")

    print(f"active pairs of (s, h) = (4, 1): {active_pairs(4, 1)}; measure {measure(4, 1)}; "
          f"(4, 2): {active_pairs(4, 2)}; (4, 3): {active_pairs(4, 3)}")
    print(f"swap_top 3 on 0..5: {[swap_top(3, x) for x in range(6)]}; views under horizon 3: "
          f"{[cview(3, x) for x in range(6)]} -> {[cview(3, swap_top(3, x)) for x in range(6)]}")
    if active_pairs(4, 1) != [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)] or cview(3, swap_top(3, 5)) == cview(3, 5):
        failures.append("pairs")

    fr = fuel_report(15)
    one_step = [drive(tower_next, 2, (n + 2, n)) for n in range(15)]
    starved = [drive(tower_next, 1, (n + 2, n))[0] for n in range(15)]
    print(f"fuel driver from (n+2, n): measure {sorted({r['measure'] for r in fr['rows']})}, fuel measure+1 -> "
          f"{sorted({r['outcome'] for r in fr['rows']})}; fuel 2 -> closed at {one_step[3]}; fuel 1 -> {set(starved)}")
    if not fr["all_terminate_closed"] or any(o[0] != "closed" for o in one_step) or set(starved) != {"out_of_fuel"}:
        failures.append("fuel")

    bg = bool_grammar_report()
    print("Boolean views of three protected points and their surviving pairs:")
    for r in bg["rows"]:
        print(f"  {r['view']} -> {r['surviving_obstructions']}")
    print(f"  every view obstructed: {bg['every_view_obstructed']}; artifact agrees: {bg['rows'] == art['bool_grammar']['rows']}")
    if not bg["every_view_obstructed"] or bg["rows"] != art["bool_grammar"]["rows"]:
        failures.append("bool")
    three = [(i, j) for i in range(3) for j in range(i + 1, 3) if [0, 1, 2][i] == [0, 1, 2][j]]
    print(f"  a three-valued view (identity) leaves {three}: the grammar, not the points, forces the obstruction")

    cm = countermodel_report()
    print("countermodels (feature present, observer zero, guarded, active); active if the stage were protected:")
    for r in cm["rows"]:
        prot = obstruction_active(retained=r["retained"], zero=r["zero"], guarded=True)
        print(f"  {r['feature']}: {r['feature_present']}, {r['zero']}, {r['guarded']}, {r['active']}; protected -> {prot}")
        if r["active"] or not prot or not r["zero"]:
            failures.append(f"cm {r['feature']}")
    print(f"  artifact agrees: {cm['rows'] == art['countermodels']['rows']}")
    if cm["rows"] != art["countermodels"]["rows"]:
        failures.append("cm artifact")

    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
