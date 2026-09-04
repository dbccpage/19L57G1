"""The reach measure applied to the identification demands.

The sealed derivation proved that a uniform-rule item is never a minimum
valid response for a separation demand, so the sealed side carries no
local-versus-global choice at all.  The identification demands do: the
dual tree's own census records 164 minima that are a single uniform rule
and 58 that are a single instance, and 182 of its 288 accepted edges sit in
a tie.

This module reconstructs the dual tree's pinned genesis states from its
pinned receipt, asks its pinned enumerator for the whole valid set at each
demand, and re-prices that set under reach.  The enumerator remains the
authority on validity; nothing here widens it.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (str(REPO / "code"), str(REPO / "research" / "identification_dual")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import dual  # noqa: E402
from derivation.candidates import Bounds, Delta  # noqa: E402
from derivation.model import Regime  # noqa: E402

import reach as rch  # noqa: E402

RECEIPT = REPO / "research" / "identification_dual" / "receipts" / "identification_dual.json"


def load_receipt() -> dict[str, object]:
    data = json.loads(RECEIPT.read_text("utf-8"))
    assert isinstance(data, dict)
    return data


def regime_of(entry: dict[str, object]) -> Regime:
    """Rebuild a pinned genesis regime from the receipt's record."""

    r = entry["regime"]
    assert isinstance(r, dict)
    return Regime(
        data=tuple(str(t) for t in r["data"]),
        forms=tuple(int(a) for a in r["forms"]),
        insts=frozenset((int(f), tuple(int(x) for x in args)) for f, args in r["insts"]),
        rules=frozenset(int(f) for f in r["rules"]),
        reqs=frozenset((int(i), int(j)) for i, j in r["reqs"]),
    )


def bounds_of(receipt: dict[str, object]) -> Bounds:
    b = receipt["bounds"]
    assert isinstance(b, dict)
    return Bounds(max_items=int(b["max_items"]), max_arity=int(b["max_arity"]))


def demand_rows(limit_genesis: int | None = None) -> list[dict[str, object]]:
    """One row per identification demand: the whole valid set at the
    minimum item count, priced under all three measures."""

    receipt = load_receipt()
    bounds = bounds_of(receipt)
    entries = receipt["genesis"]
    assert isinstance(entries, list)
    if limit_genesis is not None:
        entries = entries[:limit_genesis]
    rows: list[dict[str, object]] = []
    for entry in entries:
        assert isinstance(entry, dict)
        pinned = regime_of(entry)
        # Reading R: the declared retraction discards the standing sealed
        # separations at genesis, using the dual tree's own event rather
        # than editing the regime by hand.  Reading P is reproduced below
        # for the record and carries no response at any root, which is the
        # dual tree's own P6 finding reached from a second code path.
        state = dual.dual_step(
            dual.State(pinned, frozenset(), dual.IDENTIFY), dual.Retract()
        )
        base = state.regime
        for target in dual.demanded_pairs(state):
            got = dual.min_responses(state, target, "mu1", bounds)
            if got is None:
                rows.append({
                    "genesis": entry["id"], "reading": entry["reading"],
                    "target": list(target), "no_response": True,
                })
                continue
            valid: list[Delta] = list(got.deltas)
            priced = [rch.price(base, d) for d in valid]
            mu1_min = rch.minima_under(base, valid, "mu1")
            mu2_min = rch.minima_under(base, valid, "mu2")
            mu3_min = rch.minima_under(base, valid, "mu3")
            kinds = sorted({rch.delta_kind(d) for d in valid})
            rows.append({
                "genesis": entry["id"],
                "reading": entry["reading"],
                "target": list(target),
                "no_response": False,
                "valid_at_min_items": len(valid),
                "kinds_available": kinds,
                "inst_available": any(k == "inst" for k in kinds),
                "rule_available": any(k == "rule" for k in kinds),
                "mu1_minima": len(mu1_min),
                "mu2_minima": len(mu2_min),
                "mu3_minima": len(mu3_min),
                "mu1_kinds": sorted({rch.delta_kind(d) for d in mu1_min}),
                "mu3_kinds": sorted({rch.delta_kind(d) for d in mu3_min}),
                "reach_values": sorted({p.reach for p in priced}),
                "mu3_narrows": len(mu3_min) < len(mu1_min),
                "mu3_selected_inst_over_rule": (
                    any(k == "inst" for k in {rch.delta_kind(d) for d in mu3_min})
                    and not any(k == "rule" for k in {rch.delta_kind(d) for d in mu3_min})
                    and any(k == "rule" for k in {rch.delta_kind(d) for d in mu1_min})
                ),
            })
    return rows


def report(limit_genesis: int | None = None) -> dict[str, object]:
    rows = demand_rows(limit_genesis)
    answered = [r for r in rows if not r["no_response"]]
    mixed = [r for r in answered if r["inst_available"] and r["rule_available"]]
    rule_only = [r for r in answered if r["rule_available"] and not r["inst_available"]]
    inst_only = [r for r in answered if r["inst_available"] and not r["rule_available"]]
    narrowed = [r for r in answered if r["mu3_narrows"]]
    reselected = [r for r in answered if r["mu3_selected_inst_over_rule"]]
    # a measure that never separates the kinds cannot make this choice
    mu1_ties_across_kinds = [
        r for r in answered if len(r["mu1_kinds"]) > 1  # type: ignore[arg-type]
    ]
    mu3_ties_across_kinds = [
        r for r in answered if len(r["mu3_kinds"]) > 1  # type: ignore[arg-type]
    ]
    return {
        "demands": len(rows),
        "answered": len(answered),
        "no_response": len(rows) - len(answered),
        "demands_where_both_kinds_are_valid": len(mixed),
        "demands_where_only_rules_are_valid": len(rule_only),
        "demands_where_only_instances_are_valid": len(inst_only),
        "demands_where_reach_narrows_the_tie": len(narrowed),
        "demands_where_reach_picks_the_instance_over_the_rule": len(reselected),
        "mu1_ties_spanning_two_item_kinds": len(mu1_ties_across_kinds),
        "mu3_ties_spanning_two_item_kinds": len(mu3_ties_across_kinds),
        "rows": rows,
    }
