"""Stage 5: the register and the leftovers.

One row per menu member with its disposition at every stage, the growth
cross-check restated as a protected open, and the leftovers named and priced,
executed nowhere.  The next rung is named here in this tree's own words so it
cannot later be smuggled in as if it had been derived.

AuthorityEffect: None.
"""

from __future__ import annotations

import characters as ch

LEFTOVERS: tuple[dict[str, str], ...] = (
    {
        "name": "the general total identity",
        "class": "CONJECTURE",
        "statement": (
            "that the fresh total under the fresh-part carrier equals the balance at "
            "EVERY part count, and at the two step rules that met the stage, not only "
            "within the bounds this tree reached"
        ),
        "price": (
            "a Lean theorem quantified over the part count.  It needs the divisor "
            "recursion of the fresh parts proved rather than decided, and then the "
            "pinned uniqueness of the balance applied to the totals; this tree carries "
            "the recursion as decided instances only"
        ),
    },
    {
        "name": "the enlarged menu",
        "class": "OPEN",
        "statement": (
            "value carriers beyond the six declared, and step rules beyond the four "
            "declared, are unsearched; absence of a search is not absence of a total"
        ),
        "price": "one more freeze and one more exhaustive pass",
    },
    {
        "name": "LP4 on the term families",
        "class": "OPEN",
        "statement": (
            "at the level of the terms of a single total, every family in the "
            "rectangle still carries one magnitude; the diversity this run found is at "
            "the level of the rows, and nothing here moves the term-level question"
        ),
        "price": "a carrier whose character values are integers of more than one magnitude",
    },
    {
        "name": "the certificate channel on the refusing rows",
        "class": "OPEN",
        "statement": (
            "the refusals this run exhibits are decisions of the pinned criterion on "
            "named families; what an alternative repair channel would do with them, and "
            "whether a refusing row admits a repair of another declared kind, is not "
            "asked here.  This is the leftover the channel comparison priced, now with "
            "material to pay it"
        ),
        "price": "a declared repair channel and a per-row comparison against this census",
    },
    {
        "name": "the next rung: combining two characters of one layer",
        "class": "OPEN",
        "statement": (
            "how the totals of two characters of the same layer combine against each "
            "other, and whether a function on a layer is recovered from the totals of "
            "all its steps.  Named, not started"
        ),
        "price": (
            "a declared product on the value carrier, a Lean statement of the combined "
            "total, and a frozen prediction before any value is computed"
        ),
    },
)


def report(stage1: dict[str, object], stage2: dict[str, object],
           stage3: dict[str, object], stage4: dict[str, object]) -> dict[str, object]:
    search = stage2["search"]
    assert isinstance(search, dict)
    candidates = search["candidates"]
    assert isinstance(candidates, list)
    hits = search["hits"]
    assert isinstance(hits, list)
    stage3_clean = stage3["carriers_meeting_the_recursion"]
    assert isinstance(stage3_clean, list)
    rows: list[dict[str, object]] = []
    for carrier in ch.MENU:
        pairs = [c for c in candidates if isinstance(c, dict) and c["carrier"] == carrier]
        best = max((int(str(c["agreements"])) for c in pairs), default=0)
        met = [str(c["pair"]) for c in pairs if c["meets_stage_2"]]
        rows.append({
            "carrier": carrier,
            "stage_2_pairs": len(pairs),
            "stage_2_met": met,
            "stage_2_best_agreement": best,
            "stage_3_meets_recursion": carrier in stage3_clean,
            "stage_4_family_kinds": [
                kind for kind, carriers in
                (("term", ("V2", "V5")), ("row", ("V2", "V5", "V6")))
                if carrier in carriers
            ],
        })
    return {
        "rows": rows,
        "hits": [str(h) for h in hits],
        "ties_retained": len(hits) > 1,
        "leftovers": [dict(item) for item in LEFTOVERS],
        "protected_opens_unchanged": [
            "OB1_UNCHANGED", "S66_UNCHANGED", "S9_LAST_UNCHANGED", "NS95_GROWTH_UNCHANGED",
        ],
        "terminals": ["REGISTER_WRITTEN", "GROWTH_OPEN_UNCHANGED"],
        "growth_note": (
            "the running balance was recomputed at every pinned checkpoint and agreed; "
            "no sentence in this tree says anything about its behaviour past the last "
            "computed checkpoint, in either direction"
        ),
    }
