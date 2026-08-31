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
    push_rel,
    transpose,
)

SLOTS: tuple[str, ...] = (
    "K",
    "F",
    "R",
    "delta",
    "d0",
    "d1",
    "J",
    "M",
    "tau",
)

# Named citations of objects that live outside the two-element
# fragment.  Recorded as strings; not executed.
NAMED_ELSEWHERE: dict[str, list[str]] = {
    "K": ["PrimitivePassage.PState.occ"],
    "W": ["PrimitivePassage.PState.wit"],
    "delta": [
        "PrimDiff.CollapseCollision",
        "PrimDiff.FidelityObstruction",
        "PrimitivePassage.obstP",
    ],
    "d0_not_supply": ["Attachment.up_iff_legal"],
    "d1": ["PrimDiff.Clos"],
    "J": ["PrimitivePassage.PState.budget"],
    "M": ["PrimDiff.swap_auto_of_S2_not_of_D2"],
    "tau": [
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


def d0_report() -> dict[str, Json]:
    self_loop: Rel = frozenset({(0, 0)})
    pushed = push_rel(D2.rel, CARRIER_SWAP)
    return {
        "transpose_D2_is_D2rev": transpose(D2.rel) == D2_REV.rel,
        "transpose_D2rev_is_D2": transpose(D2_REV.rel) == D2.rel,
        "transpose_twice_D2": transpose(transpose(D2.rel)) == D2.rel,
        "push_swap_D2_is_D2rev": pushed == D2_REV.rel,
        "agree_on_D2": transpose(D2.rel) == pushed,
        "operations_differ_on_self_loop": (
            transpose(self_loop) != push_rel(self_loop, CARRIER_SWAP)
        ),
    }


def delta_report() -> dict[str, Json]:
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
    return len(rel)


def is_sym_bit(rel: Rel) -> int:
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
        "K": "Bool",
        "F": sorted(states),
        "R": "support of F",
        "delta": "collision of a map, versus obstruction relative to Irrefl",
        "d0": "Transpose, and pushforward along the carrier swap",
        "d1": "Clos; empty family is identity",
        "J": "edgeCount and isSymBit; neither unique",
        "M": "carrier swap is auto of S2 and not of D2",
        "tau": "not a function of F; empty and D2 are both irreflexive",
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
        "d0": d0_report(),
        "delta": delta_report(),
        "residuals": residuals_report(),
        "empty_ne_D2": states["empty"] != states["D2"],
        "witnesses_not_derived_as_necessary": True,
    }


def as_json(payload: Mapping[str, Json]) -> dict[str, Json]:
    return dict(payload)
