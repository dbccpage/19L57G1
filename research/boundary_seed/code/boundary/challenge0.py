"""Challenge 0: the initial state ``<|>`` under readings U and O, with no
object-language operation.

Everything computed here is metatheory about the kernel in ``model.py``.
The receipt admits nothing: the hypothetical placements enumerated for
the reflection census are never admitted states, only inputs to a
function the object language cannot call.
"""

from __future__ import annotations

import inspect
from itertools import permutations, product
from typing import Any, Callable

from boundary import model
from boundary.model import (
    READING_O,
    READING_U,
    READINGS,
    AdmitMark,
    Regime,
    Supply,
    canonical,
    certify,
    genesis,
    is_automorphism_reflection,
    observations,
    reflect,
    rename_marks,
    replay,
    serialize,
    side_profile,
    sides_collapsed,
)

SEED_SHA256 = "ba30bcd600d8232f054f3b4d9a5d03caafaa7442dfd8095643f39cfcea1ad0be"
PREDICTIONS_SHA256 = "a03ee8127e83603af75c56c4061bcbe9dc1689c3b56b90854148dfb9856cc395"
CENSUS_MAX_MARKS = 4
EVENT_TYPES: tuple[type, ...] = (Supply, AdmitMark)
EVENT_NAMES = ("Event", "Supply", "AdmitMark")

Json = dict[str, Any]


def profile_json(profile: tuple[object, ...]) -> list[object]:
    out: list[object] = []
    for part in profile:
        if isinstance(part, frozenset):
            out.append(sorted(part))
        else:
            out.append(part)
    return out


def state_event_generators(module: object = model) -> list[str]:
    """Names of public functions in a module whose declared return type is
    an event.  The object language has no way to produce an event from a
    state; this census is how the receipt says so mechanically."""
    found: list[str] = []
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("_"):
            continue
        ret = inspect.signature(obj).return_annotation
        if ret in EVENT_TYPES or ret in EVENT_NAMES:
            found.append(name)
    return sorted(found)


def observation_vocabulary() -> list[str]:
    """The public functions that read a regime and return an observation,
    with their return annotations, so a reader can check that no negative
    or counting form is among them."""
    names = ("contents", "side_profile", "observations", "sides_collapsed")
    out: list[str] = []
    for name in names:
        obj: Callable[..., object] = getattr(model, name)
        out.append(f"{name} -> {inspect.signature(obj).return_annotation}")
    return out


def fixed_up_to_mark_renaming(r: Regime) -> bool:
    """Whether some permutation of the admitted marks carries the reflected
    regime back to ``r`` with tokens forgotten.  Brute force over every
    permutation.  A first draft compared regimes with their tokens, which
    made every renamed placement look moved; the census test caught it."""
    target = reflect(r)
    want = serialize(r)
    return any(
        serialize(rename_marks(target, pi)) == want
        for pi in permutations(range(r.n_marks()))
    )


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
    return {
        "reading": reading,
        "marks": g.n_marks(),
        "side_profiles": [profile_json(side_profile(g, 0)), profile_json(side_profile(g, 1))],
        "sides_collapsed": sides_collapsed(g),
        "observations": sorted(observations(g)),
        "supply_leaves_state_unchanged": replay(supplies, g) == g,
        "supply_history_certifies_genesis": certify(supplies, g, g),
        "reflection_is_permitted_renaming": reading == READING_U,
        "reflect_genesis_equals_genesis": reflect(g) == g,
        "reflection_automorphism_by_key": is_automorphism_reflection(g),
        "canonical_key": list(canonical(g)),
    }


def score(u: Json, o: Json, census: Json, generators: list[str]) -> Json:
    """Mechanical scoring of the frozen predictions against the facts."""
    c0_1 = bool(u["sides_collapsed"])
    o_profiles = o["side_profiles"]
    c0_2 = (not o["sides_collapsed"]) and o_profiles[0][1:] == o_profiles[1][1:]
    c0_3 = (
        u["supply_leaves_state_unchanged"]
        and o["supply_leaves_state_unchanged"]
        and generators == []
    )
    c0_4 = u["observations"] == [] and o["observations"] == []
    c0_5_genesis = (
        u["reflection_is_permitted_renaming"]
        and u["reflect_genesis_equals_genesis"]
        and not o["reflection_is_permitted_renaming"]
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
                "supply_leaves_state_unchanged under both readings; "
                "state_event_generators is empty"
            ),
        },
        "C0-4": {
            "status": verdict(c0_4),
            "label": "NOT FORCED, DEFINITION-level",
            "evidence": (
                "observations empty under both readings; the observation "
                "vocabulary has no negative or counting form"
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
                "status": "SHARPENED",
                "fact": (
                    "the reflection fixes a placement up to mark renaming exactly "
                    "when the two sides carry equally many marks, under both "
                    "readings; the prediction's 'same contents' names only the "
                    "empty case of that"
                ),
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
    return {
        "challenge": 0,
        "inscription": "<|>",
        "seed_sha256": SEED_SHA256,
        "predictions_sha256": PREDICTIONS_SHA256,
        "readings": {READING_U: u, READING_O: o},
        "event_kinds": [t.__name__ for t in EVENT_TYPES],
        "state_changing_event_kinds": ["AdmitMark"],
        "state_event_generators": generators,
        "observation_vocabulary": observation_vocabulary(),
        "reflection_census": census,
        "scores": score(u, o, census, generators),
        "authority_effect": "None",
    }
