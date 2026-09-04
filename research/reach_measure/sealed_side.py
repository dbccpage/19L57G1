"""The reach measure applied to the sealed separation demand.

The sealed derivation proved that a uniform-rule item is never a minimum
valid response for a separation demand.  If that holds here, the sealed
side carries no local-versus-global choice at all and this measure cannot
say anything new about it -- which is itself worth recording, because it
locates exactly where the measure bites.

Also exhibits the two structural properties of reach on sealed material:
it is base-relative, and it is not a refinement of the item count.

AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_CODE = str(REPO / "code")
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

from derivation.candidates import (  # noqa: E402
    Bounds,
    Delta,
    NewInst,
    NewRuleAll,
    NodeView,
    iter_full_deltas,
    response_valid_fast,
)
from derivation.engine import READINGS  # noqa: E402
from derivation.model import Regime, replay  # noqa: E402

import reach as rch  # noqa: E402

BOUNDS = Bounds(max_items=2, max_arity=2)


def valid_responses(reading_name: str) -> tuple[Regime, list[Delta]]:
    """Every valid response to the sealed Challenge-3 demand at the first
    item count that admits one, over the UNPRUNED enumeration."""

    reading = next(r for r in READINGS if r.name == reading_name)
    base = replay(reading.genesis)
    target = reading.target
    view = NodeView.of(base)
    for cost in range(0, BOUNDS.max_items + 1):
        seen: set[Delta] = set()
        valid: list[Delta] = []
        for delta in iter_full_deltas(base, cost, BOUNDS):
            if delta in seen:
                continue
            seen.add(delta)
            if response_valid_fast(view, target, delta):
                valid.append(delta)
        if valid:
            return base, valid
    return base, []


def report() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for name in ("L", "F"):
        base, valid = valid_responses(name)
        priced = [rch.price(base, d) for d in valid]
        rows.append({
            "reading": name,
            "valid_at_minimum": len(valid),
            "kinds": sorted({p.kind for p in priced}),
            "any_rule_item": any(
                isinstance(it, NewRuleAll) for d in valid for it in d
            ),
            "mu1_minima": len(rch.minima_under(base, valid, "mu1")),
            "mu2_minima": len(rch.minima_under(base, valid, "mu2")),
            "mu3_minima": len(rch.minima_under(base, valid, "mu3")),
            "mu2_kinds": sorted({
                rch.delta_kind(d) for d in rch.minima_under(base, valid, "mu2")}),
            "mu3_kinds": sorted({
                rch.delta_kind(d) for d in rch.minima_under(base, valid, "mu3")}),
            "reach_values": sorted({p.reach for p in priced}),
            "mu2_and_mu3_agree": (
                set(map(rch.delta_kind, rch.minima_under(base, valid, "mu2")))
                == set(map(rch.delta_kind, rch.minima_under(base, valid, "mu3")))
            ),
        })
    base, _ = valid_responses("L")
    return {
        "readings": rows,
        "base_relative": base_relative_witness(),
        "order_inversion": order_inversion_witness(),
    }


def _pinned_bases() -> list[tuple[str, Regime]]:
    """The dual tree's pinned genesis regimes, which carry forms.  The
    sealed Challenge-3 base carries NONE -- which is why the first
    separation costs two items -- so a rule item is not even well formed
    there, and the witnesses below need bases that have forms."""

    import dual_side as ds

    receipt = ds.load_receipt()
    entries = receipt["genesis"]
    assert isinstance(entries, list)
    return [(str(e["id"]), ds.regime_of(e)) for e in entries]


def base_relative_witness() -> dict[str, object]:
    """SEARCHED, not hand-picked: two pinned bases on which the SAME
    response has different reach, while every sealed measure gives it the
    same cost on both."""

    bases = _pinned_bases()
    for form in range(3):
        probe: Delta = (NewRuleAll(form),)
        seen: list[tuple[str, int]] = []
        for name, base in bases:
            try:
                seen.append((name, rch.reach(base, probe)))
            except Exception:  # noqa: BLE001 - ill-formed on this base
                continue
        values = {v for _, v in seen}
        if len(values) > 1:
            lo = min(seen, key=lambda x: x[1])
            hi = max(seen, key=lambda x: x[1])
            return {
                "probe": rch.delta_kind(probe) + f"(form {form})",
                "low_base": lo[0], "low_reach": lo[1],
                "high_base": hi[0], "high_reach": hi[1],
                "mu1_on_both": rch.mu1(probe),
                "mu2_on_both": list(rch.mu2(probe)),
                "reach_differs_across_bases": True,
                "bases_searched": len(seen),
            }
    return {"reach_differs_across_bases": False, "note": "no witness found"}


def order_inversion_witness() -> dict[str, object]:
    """SEARCHED: a two-item response of STRICTLY POSITIVE reach that is
    still below a one-item response's reach, so the two orders are not
    nested and reach can prefer strictly more items.  Positive reach is
    required so the witness is not a response that does nothing."""

    for name, base in _pinned_bases():
        n = len(base.data)
        for form in range(len(base.forms)):
            if base.forms[form] != 1 or form in base.rules:
                continue
            one_rule: Delta = (NewRuleAll(form),)
            try:
                rule_reach = rch.reach(base, one_rule)
            except Exception:  # noqa: BLE001
                continue
            for x in range(n):
                for y in range(x + 1, n):
                    two: Delta = (NewInst(form, (x,)), NewInst(form, (y,)))
                    try:
                        a = rch.price(base, two)
                    except Exception:  # noqa: BLE001
                        continue
                    if a.reach >= 1 and a.reach < rule_reach:
                        b = rch.price(base, one_rule)
                        return {
                            "base": name,
                            "A_two_instances": {"kind": a.kind, "mu1": a.mu1,
                                                "mu2": list(a.mu2), "reach": a.reach},
                            "B_one_rule": {"kind": b.kind, "mu1": b.mu1,
                                           "mu2": list(b.mu2), "reach": b.reach},
                            "mu1_prefers_B": a.mu1 > b.mu1,
                            "reach_prefers_A": a.reach < b.reach,
                            "A_reach_is_positive": a.reach >= 1,
                            "orders_inverted": True,
                        }
    return {"orders_inverted": False, "note": "no witness found"}
