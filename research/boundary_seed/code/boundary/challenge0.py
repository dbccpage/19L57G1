"""Challenge 0: the initial state ``<|>`` under readings U and O, with no
object-language operation.

Everything computed here is metatheory about the kernel in ``model.py``.
The receipt admits nothing: the hypothetical placements enumerated for
the reflection census are never admitted states, only inputs to a
function the object language cannot call.
"""

from __future__ import annotations

import inspect
from itertools import product
from typing import Any, get_args, get_type_hints

from boundary import model
from boundary.model import (
    READING_O,
    READING_U,
    READINGS,
    OBSERVATION_TYPES,
    AdmitMark,
    Observation,
    Regime,
    Supply,
    canonical,
    certify,
    event_follows,
    fixed_up_to_mark_renaming,
    genesis,
    is_automorphism_reflection,
    mark_observations,
    name_observations,
    observations,
    reflect,
    replay,
    side_profile,
    sides_collapsed,
)

SEED_SHA256 = "ba30bcd600d8232f054f3b4d9a5d03caafaa7442dfd8095643f39cfcea1ad0be"
PREDICTIONS_SHA256 = "a03ee8127e83603af75c56c4061bcbe9dc1689c3b56b90854148dfb9856cc395"
CENSUS_MAX_MARKS = 4
EVENT_TYPES: tuple[type, ...] = (Supply, AdmitMark)

BOUNDARY_DEPENDENCE: dict[str, str] = {
    "initial opaque datum": "does not depend on the admitted boundary",
    "supply inertia": "does not depend on the admitted boundary",
    "empty event-follows relation": "does not depend on the admitted boundary",
    "side profiles, collapse, names, reflection, and class counts": (
        "require the admitted boundary and are not formulated after removing it"
    ),
}

Json = dict[str, Any]


def profile_json(profile: tuple[object, ...]) -> list[object]:
    out: list[object] = []
    for part in profile:
        if isinstance(part, frozenset):
            out.append(sorted(part))
        else:
            out.append(part)
    return out


def annotation_contains_event(
    annotation: object, event_types: tuple[type, ...] = EVENT_TYPES
) -> bool:
    """Whether a resolved return annotation contains a direct event type.

    ``event_types`` defaults to the Challenge 0 event grammar, which is what
    the Challenge 0 and Challenge 1 receipts report.  A later challenge that
    declares a further event kind passes its own enlarged tuple, so that the
    census sees the grammar of the challenge running it.
    """
    if annotation in event_types:
        return True
    return any(annotation_contains_event(part, event_types) for part in get_args(annotation))


def state_event_generators(
    module: object = model, event_types: tuple[type, ...] = EVENT_TYPES
) -> list[str]:
    """Public module functions whose resolved annotation contains an event.

    This is a supplementary Python API census.  The semantic statement that
    no event follows from state is instead the explicit empty
    ``event_follows`` relation and its Lean counterpart.
    """
    found: list[str] = []
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("_"):
            continue
        try:
            ret = get_type_hints(obj).get("return", inspect.Signature.empty)
        except (NameError, TypeError):
            ret = inspect.signature(obj).return_annotation
        if annotation_contains_event(ret, event_types):
            found.append(name)
    return sorted(found)


def observation_vocabulary() -> list[str]:
    """Derive the closed object-language judgment constructors from the sum."""
    members = get_args(Observation)
    if tuple(members) != OBSERVATION_TYPES:
        raise AssertionError("Observation alias and OBSERVATION_TYPES disagree")
    return [member.__name__ for member in members]


def judgment_json(judgment: object) -> dict[str, object]:
    if isinstance(judgment, model.OnSide):
        return {"kind": "OnSide", "mark": judgment.mark, "side": judgment.side}
    if isinstance(judgment, model.SideNamed):
        return {"kind": "SideNamed", "side": judgment.side, "name": judgment.name}
    raise TypeError(f"unknown observation judgment: {judgment!r}")


def reflection_census(max_marks: int) -> Json:
    """Over every hypothetical placement of up to ``max_marks`` marks: how
    many placements the reflection fixes up to mark renaming, whether that
    coincides with equal counts on the two sides, and how many classes the
    canonical key sees under each reading."""
    rows: list[Json] = []
    fixed_iff_equal_counts = True
    for n in range(max_marks + 1):
        placements = list(product((0, 1), repeat=n))
        fixed = 0
        classes: dict[str, set[tuple[object, ...]]] = {rd: set() for rd in READINGS}
        for placement in placements:
            marks = tuple(f"m{i}" for i in range(n))
            for rd in READINGS:
                classes[rd].add(canonical(Regime(rd, marks, placement)))
            is_fixed = fixed_up_to_mark_renaming(Regime(READING_U, marks, placement))
            equal_counts = placement.count(0) == placement.count(1)
            if is_fixed != equal_counts:
                fixed_iff_equal_counts = False
            if is_fixed:
                fixed += 1
        rows.append(
            {
                "marks": n,
                "placements": len(placements),
                "fixed_by_reflection_up_to_mark_renaming": fixed,
                "classes_under_U": len(classes[READING_U]),
                "classes_under_O": len(classes[READING_O]),
            }
        )
    return {
        "max_marks": max_marks,
        "rows": rows,
        "fixed_iff_equal_counts": fixed_iff_equal_counts,
        "note": (
            "hypothetical placements; nothing here is admitted. Mark renaming "
            "is permitted under both readings; the side exchange is a permitted "
            "renaming under U only, which is what separates the class counts."
        ),
    }


def genesis_facts(reading: str) -> Json:
    g = genesis(reading)
    supplies = [Supply("a"), Supply("b"), Supply("a")]
    mark_judgments = mark_observations(g)
    name_judgments = name_observations(g)
    return {
        "reading": reading,
        "initial_datum": {"internal_id": g.initial_datum.internal_id, "present": True},
        "marks": g.n_marks(),
        "side_profiles": [profile_json(side_profile(g, 0)), profile_json(side_profile(g, 1))],
        "sides_collapsed": sides_collapsed(g),
        "mark_observations": [judgment_json(j) for j in sorted(mark_judgments, key=repr)],
        "name_observations": [judgment_json(j) for j in sorted(name_judgments, key=repr)],
        "all_observations": [
            judgment_json(j) for j in sorted(observations(g), key=repr)
        ],
        "supply_leaves_state_unchanged": replay(supplies, g) == g,
        "supply_history_certifies_genesis": certify(supplies, g, g),
        "event_follows_relation_empty": all(
            not event_follows(g, event)
            for event in (Supply("probe"), AdmitMark("probe", 0), AdmitMark("probe", 1))
        ),
        "reflection_is_permitted_renaming": reading == READING_U,
        "reflect_genesis_equals_genesis": reflect(g) == g,
        "reflection_is_permitted_automorphism": is_automorphism_reflection(g),
        "canonical_key": list(canonical(g)),
    }


def score(
    u: Json,
    o: Json,
    census: Json,
    observation_kinds: list[str],
) -> Json:
    """Mechanical scoring of the frozen predictions against the facts."""
    c0_1 = bool(u["sides_collapsed"])
    o_profiles = o["side_profiles"]
    c0_2 = (not o["sides_collapsed"]) and o_profiles[0][1:] == o_profiles[1][1:]
    c0_3 = (
        u["supply_leaves_state_unchanged"]
        and o["supply_leaves_state_unchanged"]
        and u["event_follows_relation_empty"]
        and o["event_follows_relation_empty"]
    )
    c0_4_target = (
        u["mark_observations"] == []
        and o["mark_observations"] == []
        and observation_kinds == ["OnSide", "SideNamed"]
    )
    c0_4_no_observation_fires = (
        u["all_observations"] == [] and o["all_observations"] == []
    )
    c0_5_genesis = (
        u["reflection_is_permitted_renaming"]
        and u["reflect_genesis_equals_genesis"]
        and u["reflection_is_permitted_automorphism"]
        and not o["reflection_is_permitted_renaming"]
        and not o["reflection_is_permitted_automorphism"]
        and o["reflect_genesis_equals_genesis"]
    )

    def verdict(hit: bool) -> str:
        return "HIT" if hit else "MISSED"

    return {
        "C0-1": {
            "status": verdict(c0_1),
            "label": "FORCED",
            "evidence": "U.sides_collapsed",
        },
        "C0-2": {
            "status": verdict(c0_2),
            "label": "FORCED, DEFINITION-level",
            "evidence": "O.side_profiles differ in the name component only",
        },
        "C0-3": {
            "status": verdict(c0_3),
            "label": "FORCED",
            "evidence": (
                "supply is inert and the declared event-follows relation is "
                "empty; the state_event_generators census is supplementary and "
                "is reported but not scored"
            ),
        },
        "C0-4": {
            "status": (
                "MISSED"
                if not c0_4_target
                else "HIT"
                if c0_4_no_observation_fires
                else "PARTIAL"
            ),
            "label": "NOT FORCED",
            "result_basis": "DEFINITION-level closed judgment grammar",
            "target_status": verdict(c0_4_target),
            "no_observation_fires_status": verdict(c0_4_no_observation_fires),
            "evidence": (
                "the emptiness target holds because no OnSide judgment fires and "
                "the closed grammar has no empty or counting form; the frozen "
                "rationale 'no observation fires' is false under O because its two "
                "SideNamed judgments hold"
            ),
        },
        "C0-5": {
            "status": verdict(c0_5_genesis),
            "label": "FORCED for genesis",
            "evidence": (
                "U: reflect(genesis) == genesis and the exchange is a permitted "
                "renaming; O: the exchange is not a permitted renaming"
            ),
            "general_clause": {
                "status": (
                    "SHARPENED" if census["fixed_iff_equal_counts"] else "MISSED"
                ),
                "fact": (
                    "within the enumerated bound 0 through "
                    f"{census['max_marks']} marks, reflection followed by mark "
                    "renaming fixes exactly the equal-count placements; this is "
                    "a permitted automorphism only under U"
                    if census["fixed_iff_equal_counts"]
                    else "the equal-count characterization failed within the "
                    f"enumerated bound 0 through {census['max_marks']} marks"
                ),
                "max_marks": census["max_marks"],
                "census_fixed_iff_equal_counts": census["fixed_iff_equal_counts"],
            },
        },
        "C0-X": {
            "status": "PENDING",
            "label": "NOT FORCED",
            "evidence": "scored by Challenge 1",
        },
    }


def build() -> Json:
    u = genesis_facts(READING_U)
    o = genesis_facts(READING_O)
    census = reflection_census(CENSUS_MAX_MARKS)
    generators = state_event_generators()
    observation_kinds = observation_vocabulary()
    return {
        "challenge": 0,
        "inscription": "<|>",
        "seed_sha256": SEED_SHA256,
        "predictions_sha256": PREDICTIONS_SHA256,
        "readings": {READING_U: u, READING_O: o},
        "event_kinds": [t.__name__ for t in EVENT_TYPES],
        "state_changing_event_kinds": ["AdmitMark"],
        "state_event_generators": generators,
        "observation_vocabulary": observation_kinds,
        "boundary_dependence": BOUNDARY_DEPENDENCE,
        "reflection_census": census,
        "scores": score(u, o, census, observation_kinds),
        "authority_effect": "None",
    }
