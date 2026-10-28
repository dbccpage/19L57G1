"""Unit 37 check: the nine-slot inventory on the two-point carrier.

Recomputes Genesis's `observer_inventory` reports and compares them with
`artifacts/observer_inventory.json`; recounts the irreflexive relations on
two points by brute force; shows the two reversal maps agreeing on D2 and
differing on a self-loop, the two residuals disagreeing on D2, and the two
witness assignments. AuthorityEffect: None.
Run from the repository root: python textbook/checks/u37_inventory.py
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))

from derivation.observer_inventory import (  # noqa: E402
    defect_report, edge_count, irrefl_census_on_two, is_sym_bit, local_states,
    residuals_report, reversal_report, witnesses_report,
)
from derivation.primdiff import CARRIER_SWAP, pushforward, transpose  # noqa: E402


def main() -> int:
    failures: list[str] = []
    art = json.loads((ROOT / "artifacts" / "observer_inventory.json").read_text())
    pairs = [(x, y) for x in range(2) for y in range(2)]
    brute = [frozenset(p for p, on in zip(pairs, bits) if on)
             for bits in itertools.product((False, True), repeat=4)]
    irr = [r for r in brute if all((x, x) not in r for x in range(2))]
    states = local_states()
    print(f"relations on two points: {len(brute)}; irreflexive: {len(irr)}; "
          f"they are exactly {sorted(states)}: {frozenset(irr) == frozenset(states.values())}")
    census = irrefl_census_on_two()
    if census != art["irrefl_census"] or len(irr) != 4 or frozenset(irr) != frozenset(states.values()):
        failures.append("census")
    rev = reversal_report()
    loop = frozenset({(0, 0)})
    print(f"reversal: transpose(D2) = D2rev {rev['transpose_D2_is_D2rev']}, push_swap(D2) = D2rev "
          f"{rev['push_swap_D2_is_D2rev']}, agree on D2 {rev['agree_on_D2']}; on the self-loop "
          f"{set(loop)}: transpose {set(transpose(loop))}, push_swap {set(pushforward(loop, CARRIER_SWAP))}")
    if rev != art["reversal"] or not rev["operations_differ_on_self_loop"]:
        failures.append("reversal")
    res = residuals_report()
    print(f"residuals: edge_count D2 {edge_count(states['D2'])}, S2 {edge_count(states['S2'])}; "
          f"is_sym_bit D2 {is_sym_bit(states['D2'])}, S2 {is_sym_bit(states['S2'])}; "
          f"disagree on D2 {res['residuals_disagree_on_D2']}")
    if res != art["residuals"]:
        failures.append("residuals")
    wit = witnesses_report()
    dfc = defect_report()
    print(f"witnesses: zero != one {wit['zero_ne_one']}, presence of one is D2 {wit['one_presence_is_D2']}; "
          f"defect: D2 collides under the merge {dfc['D2_collides_under_merge']} and stays irreflexive "
          f"{dfc['source_D2_still_irreflexive']}; the one-point self-loop is not irreflexive "
          f"{dfc['unit_self_loop_not_irreflexive']}")
    if wit != art["witnesses"] or dfc != art["defect"]:
        failures.append("witness/defect")
    print(f"slots: {art['slot_count']} {art['slots']}")
    if art["slot_count"] != 9 or len(set(art["slots"])) != 9:
        failures.append("slots")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
