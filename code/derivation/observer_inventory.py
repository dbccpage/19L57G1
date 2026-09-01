"""Nine-slot inventory of existing primitive-difference objects.

Classification: metatheory apparatus for
``paper/observer_inventory.md``.  The nine slots are a declared
classification of objects the derivation already has.  Nothing here
authorizes a next challenge.  Witness assignments are present as data
when supplied; they are not derived as a unique inhabitant.

The two-element fragment is exhaustive: every irreflexive relation on
``range(2)`` is empty, ``D2``, ``D2rev``, or ``S2``.  Relation
transpose and carrier-swap pushforward agree on ``D2`` and are not
the same operation.
"""

from __future__ import annotations

from typing import Mapping

from derivation.export import Json
from derivation.primdiff import (
    CARRIER_SWAP,
    D2,
    D2_REV,
    S2,
    Rel,
    collision,
    irreflexive,
    irreflexive_relations_on,
    merge_map,
    pushforward,
    transpose,
)

SLOTS: tuple[str, ...] = (
    "carrier",
    "local_state",
    "support",
    "defect",
    "reversal",
    "closure",
    "residual",
    "maps",
    "terminal",
)

# Named citations of objects that live outside the two-element
# fragment.  Recorded as strings; not executed.
NAMED_ELSEWHERE: dict[str, list[str]] = {
    "carrier": ["PrimitivePassage.PState.occ"],
    "witness": ["PrimitivePassage.PState.wit"],
    "defect": [
        "PrimDiff.CollapseCollision",
        "PrimDiff.FidelityObstruction",
        "PrimitivePassage.obstP",
    ],
    "supply_not_reversal": ["Attachment.up_iff_legal"],
    "closure": ["PrimDiff.Clos"],
    "residual": ["PrimitivePassage.PState.budget"],
    "maps": ["PrimDiff.swap_auto_of_S2_not_of_D2"],
    "terminal": [
        "Attachment.AttachOutcome",
        "PrimitivePassage.PState.licensed",
        "PrimitivePassage.PState.halted",
        "Horizon.worldAt_quiescent",
    ],
}


def local_states() -> dict[str, Rel]:
    return {
        "empty": frozenset(),
        "D2": D2.rel,
        "D2rev": D2_REV.rel,
        "S2": S2.rel,
    }


def irrefl_census_on_two() -> dict[str, Json]:
    rels = irreflexive_relations_on(2)
    states = local_states()
    return {
        "count": len(rels),
        "are_exactly_the_four": frozenset(rels) == frozenset(states.values()),
        "names": sorted(states),
    }


def witnesses_report() -> dict[str, Json]:
    zero: dict[tuple[int, int], int] = {(0, 1): 0, (1, 0): 0}
    one: dict[tuple[int, int], int] = {(0, 1): 1, (1, 0): 0}
    presence_one = frozenset(p for p, v in one.items() if v > 0)
    return {
        "zero_ne_one": zero != one,
        "one_forward": one[(0, 1)] == 1,
        "one_reverse": one[(1, 0)] == 0,
        "zero_presence_empty": not any(v > 0 for v in zero.values()),
        "one_presence_is_D2": presence_one == D2.rel,
    }


def reversal_report() -> dict[str, Json]:
    self_loop: Rel = frozenset({(0, 0)})
    pushed = pushforward(D2.rel, CARRIER_SWAP)
    return {
        "transpose_D2_is_D2rev": transpose(D2.rel) == D2_REV.rel,
        "transpose_D2rev_is_D2": transpose(D2_REV.rel) == D2.rel,
        "transpose_twice_D2": transpose(transpose(D2.rel)) == D2.rel,
        "push_swap_D2_is_D2rev": pushed == D2_REV.rel,
        "agree_on_D2": transpose(D2.rel) == pushed,
        "operations_differ_on_self_loop": (
            transpose(self_loop) != pushforward(self_loop, CARRIER_SWAP)
        ),
    }


def defect_report() -> dict[str, Json]:
    merge = merge_map(2, 0, 1)
    unit_rel: Rel = frozenset({(0, 0)})
    return {
        "D2_collides_under_merge": collision(D2.rel, merge),
        "S2_collides_under_merge": collision(S2.rel, merge),
        "empty_does_not_collide_under_merge": not collision(
            frozenset(), merge
        ),
        "unit_self_loop_not_irreflexive": not irreflexive(unit_rel),
        "source_D2_still_irreflexive": irreflexive(D2.rel),
    }


def edge_count(rel: Rel) -> int:
    """Off-diagonal occupancy: how many off-diagonal pairs are present.

    Matches the Lean ``edgeCount``, which reads only the two
    off-diagonal slots of the two-element carrier; diagonal (self-loop)
    pairs are never counted, so the value agrees with ``len(rel)``
    exactly on irreflexive relations."""
    return sum(1 for (x, y) in rel if x != y)


def is_sym_bit(rel: Rel) -> int:
    """Both-orientations bit on the two-element carrier's off-diagonal
    slots.  Matches the Lean ``isSymBit``; diagonal pairs are never
    read."""
    return 1 if (0, 1) in rel and (1, 0) in rel else 0


def residuals_report() -> dict[str, Json]:
    d2 = D2.rel
    s2 = S2.rel
    return {
        "edge_count_D2": edge_count(d2),
        "edge_count_S2": edge_count(s2),
        "is_sym_bit_D2": is_sym_bit(d2),
        "is_sym_bit_S2": is_sym_bit(s2),
        "residuals_disagree_on_D2": edge_count(d2) != is_sym_bit(d2),
    }


def inventory_report() -> dict[str, Json]:
    states = local_states()
    bindings: dict[str, Json] = {
        "carrier": "Bool",
        "local_state": sorted(states),
        "support": "the local state, read as support",
        "defect": "collision of a map, versus obstruction relative to Irrefl",
        "reversal": "Transpose, and pushforward along the carrier swap",
        "closure": "Clos; empty family is identity",
        "residual": "edgeCount and isSymBit; neither unique",
        "maps": "carrier swap is auto of S2 and not of D2",
        "terminal": (
            "Irrefl does not determine the local state; "
            "empty and D2 are both irreflexive"
        ),
    }
    named: dict[str, Json] = {
        key: list(vals) for key, vals in NAMED_ELSEWHERE.items()
    }
    census = irrefl_census_on_two()
    return {
        "slots": list(SLOTS),
        "slot_count": len(SLOTS),
        "bindings": bindings,
        "named_elsewhere": named,
        "irrefl_census": census,
        "witnesses": witnesses_report(),
        "reversal": reversal_report(),
        "defect": defect_report(),
        "residuals": residuals_report(),
        "empty_ne_D2": states["empty"] != states["D2"],
        "witnesses_not_derived_as_necessary": True,
    }


def as_json(payload: Mapping[str, Json]) -> dict[str, Json]:
    return dict(payload)
