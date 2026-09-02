"""Stage 5: the register and the leftovers.

One row per candidate that met stage 2 -- menu index, count, bound
reached, Lean status, certificate cell -- a summary of the candidates
that did not, and the leftovers named and priced, executed nowhere.  The
next rung is named in this tree's own words so that it cannot later be
smuggled in as if it had been derived; nothing about it is claimed.

AuthorityEffect: None.
"""

from __future__ import annotations

LEAN_STATUS: dict[str, dict[str, str]] = {
    "S1b(W2)": {
        "status": "CARRIER_IDENTITY_PROVED",
        "theorem": "BalanceCarrier.Walk.totalWalkSum_neg_one_eq_runningBalance",
        "scope": "every N (Lean), from walkSum_neg_one_eq_balance and the pinned balance_unique",
    },
    "S2(W1,1,C1)": {
        "status": "CARRIER_IDENTITY_BOUNDED",
        "theorem": "BalanceCarrier.Walk.unit_table_matches_to_7",
        "scope": "N <= 12 exhaustive (Python); N <= 7 kernel-decided (Lean); N <= 1000 at every N and at the pinned checkpoints to 1000000 by the column route (Python); the general identity is CONJECTURE",
    },
    "S2(W3,1,Cbal)": {
        "status": "CARRIER_IDENTITY_BOUNDED",
        "theorem": "BalanceCarrier.Walk.balance_table_matches_to_7",
        "scope": "N <= 12 exhaustive (Python); N <= 7 kernel-decided (Lean); N <= 1000 at every N and at the pinned checkpoints to 1000000 by the column route (Python); the general identity is CONJECTURE",
    },
}

LEFTOVERS: list[dict[str, str]] = [
    {
        "name": "general table identity",
        "class": "CONJECTURE",
        "statement": "for every N the alternating sum of the unit table with unit first column, and of the balance-weighted table with balance first column, equals the running balance",
        "evidence": "exhaustive to N <= 12, kernel-decided to N <= 7, column route at every N <= 1000 and at the pinned checkpoints to 1000000; proved nowhere",
        "price": "a Lean development of the alternating sum over arrangements (sign under composition, the cycle decomposition of a supported arrangement) that this tree does not carry",
    },
    {
        "name": "enlarged menu",
        "class": "OPEN",
        "statement": "whether any weight reading an endpoint's balance, or any count beyond the four declared, meets stage 2 is unsearched",
        "evidence": "the menu is declared and finite (FW-SET); absence of a search is not absence of a carrier",
        "price": "a second frozen menu and a second exhaustive search",
    },
    {
        "name": "LP4, magnitude diversity",
        "class": "OPEN",
        "statement": "every family produced by the three carriers at N in {6, 7, 12} has every magnitude equal to 1, so the certificate criterion cannot refuse anything here; LP4 persists on these families",
        "evidence": "the stage-3 table",
        "price": "a carrier whose signed family carries at least two magnitudes; the enlarged-menu weights are the first place to look, and nothing about them is claimed",
    },
    {
        "name": "fresh character totals (the next rung, named, not started)",
        "class": "OPEN",
        "statement": "the signed total, over the fresh members of a layer, of one of that layer's characters -- a signed count indexed by a part count and a step -- and its relation to the balance and the divisor relation",
        "evidence": "none; named here so it cannot later be smuggled in as derived",
        "price": "a definition of the layer's characters in the receiver's own terms, a Lean statement of the total, and a frozen prediction before any value is computed",
    },
]

PROTECTED_OPENS: tuple[str, ...] = (
    "OB1_UNCHANGED",
    "S66_UNCHANGED",
    "S9_LAST_UNCHANGED",
    "NS95_GROWTH_UNCHANGED",
)


def register(
    search: dict[str, object], families: dict[str, object]
) -> dict[str, object]:
    candidates = search["candidates"]
    assert isinstance(candidates, list)
    rows_by_menu: dict[str, dict[str, object]] = {}
    for row in candidates:
        assert isinstance(row, dict)
        rows_by_menu[str(row["menu"])] = row
    family_rows = families["rows"]
    assert isinstance(family_rows, list)
    hit_rows: list[dict[str, object]] = []
    for label, status in LEAN_STATUS.items():
        cells = [
            {
                "N": r["N"],
                "certificate_exists": r["certificate"]["certificate_exists"]
                if isinstance(r["certificate"], dict)
                else None,
                "every_magnitude_is_one": r["every_magnitude_is_one"],
            }
            for r in family_rows
            if isinstance(r, dict) and r["menu"] == label
        ]
        hit_rows.append(
            {
                "menu": label,
                "count": label.split("(")[0],
                "values_1_12": rows_by_menu[label]["values_1_12"],
                "bound_python": 12,
                "lean": status,
                "certificate_cells": cells,
            }
        )
    summary: dict[str, dict[str, object]] = {}
    for row in candidates:
        assert isinstance(row, dict)
        if row["meets_stage_2"]:
            continue
        kind = str(row["kind"])
        agree = row["agreeing_N"]
        assert isinstance(agree, list)
        entry = summary.setdefault(kind, {"not_meeting": 0, "best_agreement": 0, "best_menu": []})
        entry["not_meeting"] = int(str(entry["not_meeting"])) + 1
        best = int(str(entry["best_agreement"]))
        if len(agree) > best:
            entry["best_agreement"] = len(agree)
            entry["best_menu"] = [row["menu"]]
        elif len(agree) == best:
            menus = entry["best_menu"]
            assert isinstance(menus, list)
            menus.append(row["menu"])
    return {
        "rows": hit_rows,
        "not_meeting_by_kind": summary,
        "leftovers": LEFTOVERS,
        "protected_opens_unchanged": list(PROTECTED_OPENS),
        "terminal": "REGISTER_WRITTEN",
    }
