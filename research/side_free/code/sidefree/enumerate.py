"""The generic enumerator: one code path over two carriers.

Classification: METATHEORY APPARATUS.

This module imports NEITHER carrier module.  It is generic over the
``Carrier`` protocol below, and ``control.py`` wires the two carriers into
it.  The comparison this tree makes is therefore not two runs compared by
hand but two rows of one table — which is the direct repair of the defect
this control exists for, since the pinned world's own dependence claims live
in a hand-written dictionary its own ledger files as computed by nothing.

A test asserts that this module's own module-level imports name neither
carrier, so the genericity is checked and not merely intended.

Every measure is computed HERE, from carrier primitives:

* ``mu1`` is the number of coordinates the candidate moves off their own
  inherited values, one capability each;
* ``one_step`` is ``mu1 == 1`` and ``bundles`` is ``mu1 >= 2``;
* ``satisfies`` is the one shared verdict function applied to the carrier's
  own recorded automorphism permutations;
* ``mu2`` is the count of the carrier's own collateral facts the candidate
  makes available that its base did not;
* ``mu2_restricted`` is the same count over the facts BOTH worlds can state.
"""

from __future__ import annotations

from typing import Protocol, Sequence

from sidefree.requirement import RETAINED_MARKS, separates

Json = dict[str, object]


def key_json(value: object) -> object:
    """Render a serialization key as JSON: tuples become lists, atoms stay."""
    if isinstance(value, tuple):
        return [key_json(part) for part in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"not a serialization key part: {value!r}")


class Carrier(Protocol):
    """What the enumerator needs of a world.  Neither carrier is named here."""

    world: str
    coordinates: tuple[str, ...]
    collateral_fact_names: tuple[str, ...]
    restricted_fact_names: tuple[str, ...]

    def points(self) -> list[object]: ...

    def base_point(self) -> object: ...

    def point_name(self, aug: object) -> str: ...

    def coordinate_values(self, aug: object) -> Json: ...

    def changed_coordinates(self, aug: object) -> list[str]: ...

    def capability_of(self, name: str) -> str: ...

    def history(self, aug: object) -> list[Json]: ...

    def certified(self, aug: object) -> bool: ...

    def replays_from_genesis(self, aug: object) -> bool: ...

    def initial_datum_unchanged(self, aug: object) -> bool: ...

    def event_follows_relation_empty(self, aug: object) -> bool: ...

    def n_marks(self, aug: object) -> int: ...

    def labels(self, aug: object) -> list[str]: ...

    def permitted_renamings(self, aug: object) -> Json: ...

    def automorphism_entries(self, aug: object) -> list[Json]: ...

    def carrier_separability(self, aug: object) -> bool: ...

    def satisfies_second_reading(self, aug: object) -> bool: ...

    def orbit_size(self, aug: object) -> int: ...

    def no_permitted_renaming_moves_an_index(self, aug: object) -> bool: ...

    def effective_structure(self, aug: object) -> list[str]: ...

    def canonical_key(self, aug: object) -> object: ...

    def collateral_facts(self, aug: object) -> dict[str, bool]: ...

    def mark_property_facts(self, aug: object) -> dict[str, list[str]]: ...

    def census_verdicts(self, aug: object) -> list[bool]: ...

    def satisfies_under_key_choice(self, aug: object) -> dict[str, bool]: ...


def permutations_of(entries: Sequence[Json]) -> list[tuple[int, ...]]:
    """The permutations recorded in a list of automorphism entries."""
    out: list[tuple[int, ...]] = []
    for entry in entries:
        raw = entry["permutation"]
        if not isinstance(raw, (list, tuple)):
            raise TypeError(f"not a permutation: {raw!r}")
        out.append(tuple(int(part) for part in raw))
    return out


def newly_available(
    facts: dict[str, bool], base_facts: dict[str, bool], names: Sequence[str]
) -> int:
    """How many of ``names`` the candidate makes available that the base did not."""
    return sum(1 for name in names if facts[name] and not base_facts[name])


def row(carrier: Carrier, aug: object, base_facts: dict[str, bool]) -> Json:
    """One point of a declared space, as one row of the shared table."""
    moved = carrier.changed_coordinates(aug)
    entries = carrier.automorphism_entries(aug)
    perms = permutations_of(entries)
    i, j = RETAINED_MARKS
    satisfies = separates(perms, i, j)
    facts = carrier.collateral_facts(aug)
    verdicts = carrier.census_verdicts(aug)
    return {
        "name": carrier.point_name(aug),
        "world": carrier.world,
        "coordinates": carrier.coordinate_values(aug),
        "capability_coordinates": moved,
        "capabilities": [carrier.capability_of(name) for name in moved],
        "mu1": len(moved),
        "mu2": newly_available(facts, base_facts, carrier.collateral_fact_names),
        "mu2_restricted": newly_available(
            facts, base_facts, carrier.restricted_fact_names
        ),
        "one_step": len(moved) == 1,
        "bundles": len(moved) >= 2,
        "satisfies": satisfies,
        "satisfies_second_reading": carrier.satisfies_second_reading(aug),
        "carrier_separability_agrees": carrier.carrier_separability(aug) == satisfies,
        "automorphism_count": len(entries),
        "automorphism_entries": entries,
        "no_permitted_renaming_moves_an_index": (
            carrier.no_permitted_renaming_moves_an_index(aug)
        ),
        "effective_structure": carrier.effective_structure(aug),
        "class_key": [*carrier.effective_structure(aug), carrier.canonical_key(aug)],
        "collateral_facts": facts,
        "orbit_size": carrier.orbit_size(aug),
        "history": carrier.history(aug),
        "certified": carrier.certified(aug),
        "replays_from_genesis": carrier.replays_from_genesis(aug),
        "initial_datum_unchanged": carrier.initial_datum_unchanged(aug),
        "event_follows_relation_empty": carrier.event_follows_relation_empty(aug),
        "marks": carrier.n_marks(aug),
        "labels": carrier.labels(aug),
        "permitted_renamings": carrier.permitted_renamings(aug),
        "route_census": {
            "cells": len(verdicts),
            "separating": sum(1 for v in verdicts if v),
        },
        "satisfies_under_key_choice": carrier.satisfies_under_key_choice(aug),
        **carrier.mark_property_facts(aug),
    }


def enumerate_rows(carrier: Carrier) -> list[Json]:
    """Every point of the carrier's declared space, as rows of one table."""
    base_facts = carrier.collateral_facts(carrier.base_point())
    return [row(carrier, aug, base_facts) for aug in carrier.points()]


def eligible(rows: Sequence[Json]) -> list[Json]:
    """Base-or-one-step candidates.  A bundle is refused as one step, so it is
    not eligible to be a minimum of the enumeration the requirement asks for."""
    return [r for r in rows if r["one_step"] or r["mu1"] == 0]


def minima(rows: Sequence[Json], measure: str, exclude: Sequence[str] = ()) -> Json:
    """The satisfying candidates of least cost, quotiented by the class key.

    Every tied class is retained; ``unique`` is true only at one class.  A
    candidate whose name is in ``exclude`` is dropped before the minimum is
    taken; that is how the declared secondary computation is expressed, and
    it never touches the primary.
    """
    satisfying = [
        r for r in eligible(rows) if r["satisfies"] and str(r["name"]) not in exclude
    ]
    if not satisfying:
        return {
            "measure": measure,
            "minimum": None,
            "points": [],
            "classes": [],
            "class_count": 0,
            "unique": False,
        }
    least = min(int(str(r[measure])) for r in satisfying)
    attaining = [r for r in satisfying if int(str(r[measure])) == least]
    grouped: dict[str, list[str]] = {}
    for r in attaining:
        grouped.setdefault(repr(r["class_key"]), []).append(str(r["name"]))
    ordered = sorted(grouped.items())
    return {
        "measure": measure,
        "minimum": least,
        "points": [str(r["name"]) for r in attaining],
        "classes": [
            {
                "class_key": next(
                    r["class_key"] for r in attaining if str(r["name"]) == members[0]
                ),
                "members": members,
            }
            for _key, members in ordered
        ],
        "class_count": len(ordered),
        "unique": len(ordered) == 1,
    }


def named(rows: Sequence[Json], name: str) -> Json:
    """The one row of a table with this point name."""
    for r in rows:
        if str(r["name"]) == name:
            return r
    raise KeyError(f"no row named {name!r}")


def everywhere_satisfying(rows: Sequence[Json]) -> list[str]:
    """Names of the candidates that separate at every cell of the route census.

    Computed in both worlds by this one function over each world's own census.
    """
    out: list[str] = []
    for r in rows:
        census = r["route_census"]
        if not isinstance(census, dict):
            raise TypeError("route_census must be an object")
        cells = int(str(census["cells"]))
        separating = int(str(census["separating"]))
        if cells > 0 and separating == cells:
            out.append(str(r["name"]))
    return out
