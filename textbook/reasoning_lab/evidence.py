"""Supplied fictional logs and finite interpretation checks; AuthorityEffect: None.

These fixtures are not physical observations. No reader data is ingested.
"""
from collections import Counter
from itertools import combinations, product

ORIGIN = "supplied hypothetical log"
DOMAIN = ("K", "L", "M", "N")
PROTOCOL = "P1"
CONDITION = "front-desk"
CODES = {"Y": True, "N": False, "?": None}
FIELDS = {"id", "card", "protocol", "condition", "dot", "crease", "origin"}


def record(name, card, dot, crease, protocol=PROTOCOL, condition=CONDITION):
    return dict(id=name, card=card, protocol=protocol, condition=condition,
                dot=dot, crease=crease, origin=ORIGIN)


def supplied_records():
    return [
        record("first-K", "K", "Y", "Y"),
        record("first-L", "L", "N", "Y"),
        record("first-M", "M", "N", "N"),
        record("new-N", "N", "Y", "N"),
        record("repeat-N", "N", "Y", "Y"),
        record("unclear-N", "N", "Y", "?"),
        record("no-dot-L", "L", "N", "?"),
        record("crease-K", "K", "?", "Y"),
        record("unclear-K", "K", "?", "?"),
        record("outside-O", "O", "Y", "N"),
        record("other-protocol", "N", "Y", "N", protocol="P2"),
        record("other-condition", "N", "Y", "N", condition="back-view"),
    ]


def validate(row):
    if type(row) is not dict or set(row) != FIELDS:
        raise ValueError("A supplied record must have exactly the declared fields")
    if any(type(row[k]) is not str or not row[k] for k in FIELDS):
        raise ValueError("Record fields must be nonempty strings")
    if row["origin"] != ORIGIN:
        raise ValueError("Fictional fixtures cannot be relabeled as measurements")
    if row["dot"] not in CODES or row["crease"] not in CODES:
        raise ValueError("Unknown raw answer code; do not silently turn it into No")


def classify(row):
    """Classify this row against the declared conditional and protocol only."""
    validate(row)
    if row["protocol"] != PROTOCOL:
        return "protocol_mismatch"
    if row["card"] not in DOMAIN or row["condition"] != CONDITION:
        return "out_of_scope"
    dot, crease = CODES[row["dot"]], CODES[row["crease"]]
    if dot is True and crease is False:
        return "counterexample"
    if dot is False or crease is True:
        return "compatible"
    return "unresolved"


def repeat_conflicts(rows):
    """Find known answer conflicts for the same card/protocol/conditions.

    Unknowns do not become known differences. Out-of-scope rows are retained
    in the packet but excluded from this P1 comparison.
    """
    eligible = [r for r in rows if classify(r) not in ("protocol_mismatch", "out_of_scope")]
    conflicts = []
    for a, b in combinations(eligible, 2):
        if (a["card"], a["protocol"], a["condition"]) != (b["card"], b["protocol"], b["condition"]):
            continue
        changed = [q for q in ("dot", "crease")
                   if a[q] != "?" and b[q] != "?" and a[q] != b[q]]
        if changed:
            conflicts.append({"records": [a["id"], b["id"]], "changed": changed})
    return conflicts


def build_evidence_packet():
    rows = supplied_records()
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("Trial identifiers must be distinct; retain repeats as new rows")
    outcomes = {r["id"]: classify(r) for r in rows}
    totals = dict(Counter(outcomes.values()))
    assert totals == {"compatible": 6, "counterexample": 1, "unresolved": 2,
                      "out_of_scope": 2, "protocol_mismatch": 1}
    conflicts = repeat_conflicts(rows)
    assert conflicts == [{"records": ["new-N", "repeat-N"], "changed": ["crease"]}]
    return dict(origin=ORIGIN, physical_observations_recorded=0,
                domain=list(DOMAIN), protocol=PROTOCOL, condition=CONDITION,
                legend={"Y": "Yes", "N": "No", "?": "Unclear or not recorded"},
                claim="On K, L, M, N under P1/front-desk: if dot, then crease.",
                records=rows, outcomes=outcomes, totals=totals, repeat_conflicts=conflicts)


def check_evidence_population():
    """Independent completion oracle: 9 partial pairs × 8 metadata choices."""
    counts = Counter()
    for dot, crease, inside, protocol_ok, condition_ok in product(
            CODES, CODES, (False, True), (False, True), (False, True)):
        row = record("probe", "K" if inside else "O", dot, crease,
                     PROTOCOL if protocol_ok else "P2", CONDITION if condition_ok else "back-view")
        if not protocol_ok:
            wanted = "protocol_mismatch"
        elif not inside or not condition_ok:
            wanted = "out_of_scope"
        else:
            possible = lambda code: (False, True) if code == "?" else (code == "Y",)
            failures = {p and not q for p, q in product(possible(dot), possible(crease))}
            wanted = ("counterexample" if failures == {True} else
                      "compatible" if failures == {False} else "unresolved")
        assert classify(row) == wanted, row
        counts[wanted] += 1
    assert dict(counts) == {"protocol_mismatch": 36, "out_of_scope": 27,
                            "compatible": 5, "counterexample": 1, "unresolved": 3}
    return {"partial_answer_pairs": 9, "scoped_comparisons": sum(counts.values()),
            "fictional_logs": len(build_evidence_packet()["records"]),
            "physical_observations_recorded": 0}
