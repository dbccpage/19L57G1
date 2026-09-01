"""Register: one inspectable row per obstructed census member, with
the phase-2 price data (two-label members), the phase-3 outcome (the
occupancy-3 square), or the named bound refusal (everything else); the
member's channel cell; and the priced leftovers, executed nowhere.

Requires the pinned sign_slice modules on the path (`../sign_slice`).
AuthorityEffect: None.
"""

from __future__ import annotations

LEFTOVER_PRICE_FORM = (
    "LP1 price form: the conjectured closed form -- the price equals the"
    " least per-hop disagreement between a flipping consumed class and a"
    " pointwise consumed class -- is CONJECTURE, supported by two-route"
    " agreement at every exhausted member and proved nowhere; admitting"
    " it costs a Lean development of cycle-space bookkeeping this run"
    " does not carry."
)
LEFTOVER_SIX_BOUND = (
    "LP2 enlarged six-label bound: the exhaustion covered four maps per"
    " slot; slot maps outside that set are unsearched, and absence of a"
    " search is not invariance; admitting the enlarged question costs a"
    " declared larger map set and its exhaustion."
)
LEFTOVER_LARGER_FIBRE = (
    "LP3 larger-fibre promotion: SS-09's second half stays OPEN --"
    " no theorem here covers fibres above two; admitting it costs a"
    " fibre-general cure theorem over a declared slot-map group, in"
    " Lean."
)
LEFTOVER_MAGNITUDE = (
    "LP4 magnitude diversity: every walk magnitude on this census is 1,"
    " so channel (b) cannot refuse and the channels cannot separate"
    " here; admitting a separating census costs new members with amp"
    " magnitudes above 1 under declared bounds."
)


def build(
    obstructed: list[dict[str, object]],
    phase2: dict[str, dict[str, object]],
    phase3: dict[str, object],
    channel_rows: list[dict[str, object]],
    magnitude_degeneracy: bool,
) -> list[dict[str, object]]:
    by_variant = {str(r["name"]): r for r in channel_rows}
    out: list[dict[str, object]] = []
    for entry in obstructed:
        name = str(entry["name"])
        fibre = int(str(entry["fibre"]))
        row: dict[str, object] = {
            "name": name,
            "fibre": fibre,
        }
        leftovers: list[str] = []
        if fibre == 2:
            ex = phase2[name]
            row["cure"] = {
                "within_bound": True,
                "flip_count": ex["flip_count"],
                "price_min_slots_from_pointwise": ex[
                    "price_min_slots_from_pointwise"
                ],
                "price_tie_count": ex["price_tie_count"],
                "source": "phase_2_exhaustion",
            }
            leftovers.append(LEFTOVER_PRICE_FORM)
        elif name == "square_2x2_occ3":
            row["cure"] = {
                "within_bound": phase3["terminal"] == "SIXLABEL_MOVES",
                "terminal": phase3["terminal"],
                "source": "phase_3_exhaustion",
            }
            if phase3["terminal"] == "SIXLABEL_INVARIANT_BOUNDED":
                leftovers.append(LEFTOVER_SIX_BOUND)
            leftovers.append(LEFTOVER_LARGER_FIBRE)
        else:
            row["cure"] = {
                "within_bound": None,
                "refused": "REFUSED: outside the phase-2 slot bound and"
                " the phase-3 member bound, by name",
                "source": "none",
            }
            leftovers.append(LEFTOVER_LARGER_FIBRE)
        variant = f"signed_variant_of_{name}"
        if variant in by_variant:
            row["channel_cell"] = by_variant[variant]["cell"]
        if magnitude_degeneracy:
            leftovers.append(LEFTOVER_MAGNITUDE)
        row["leftovers"] = leftovers
        out.append(row)
    return out
