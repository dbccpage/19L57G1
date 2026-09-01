"""Register: one inspectable row per obstructed census member.

The register records why each obstructed member fails the section
criterion.  It does not delete arrows, does not add covers, and does
not close anything: those remain the packet's two priced rules (cited
as CONDITIONAL_THEOREM: the cut theorem and the re-presentation
theorems), and the leftover column prices what a repair would have to
admit without executing it.  AuthorityEffect: None.
"""

from __future__ import annotations

from cone_section import (
    closed_walks,
    components,
    cone_section,
    fixed_labels,
    holonomy_group,
    twisted_and_total,
)
from genpres import GenPres

WALK_BOUND = 6
NAMED_PAIR = (0, 1)


def witness_walk(p: GenPres, base: int) -> dict[str, object]:
    """A closed walk at the base whose transport moves every admissible
    pair (fixes at most one label), or a named bound-hit."""

    walks = closed_walks(p, base, WALK_BOUND)
    for transport, _amp in walks:
        if len([l for l in range(p.fibre) if transport[l] == l]) <= 1:
            return {
                "found": True,
                "transport": list(transport),
            }
    return {
        "found": False,
        "reason": f"no all-pair-moving closed walk within length {WALK_BOUND}",
    }


def row(name: str, p: GenPres, occ_outcome: str) -> dict[str, object]:
    base = sorted(p.objects)[0]
    walks = closed_walks(p, base, WALK_BOUND)
    twisted, total, movers = twisted_and_total(walks, NAMED_PAIR)
    comp = components(p)[0]
    fixed = fixed_labels(holonomy_group(p, comp), p.fibre)
    leftover = (
        "one occurrence-slot convention change (priced by the exhaustion)"
        if occ_outcome.startswith("MOVES")
        else "an occurrence-slot relabel exhaustion, or an arrow deletion"
        " (the packet's cut rule, cited, not executed) -- both priced"
        " bill lines, neither admitted here"
    )
    return {
        "name": name,
        "witness_walk": witness_walk(p, base),
        "mover_count_unit_weights": movers,
        "twisted_at_named_pair": twisted,
        "total": total,
        "named_pair": list(NAMED_PAIR),
        "holonomy_fixed_labels": fixed,
        "repair_mass": "NOT_APPLICABLE: the faces/pricing layer is proved"
        " on the packet's chord-square family; no census member is that"
        " family",
        "occ_relabel_outcome": occ_outcome,
        "leftover": leftover,
    }


def build(
    census_rows: list[dict[str, object]],
    presentations: dict[str, GenPres],
    occ_outcomes: dict[str, str],
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for entry in census_rows:
        name = str(entry["name"])
        if bool(entry["sectioned"]):
            continue
        p = presentations[name]
        assert not cone_section(p)
        out.append(row(name, p, occ_outcomes.get(name, "SPACE_OPEN: not priced this run")))
    return out
