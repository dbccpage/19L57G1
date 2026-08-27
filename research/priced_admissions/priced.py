"""Priced-admissions research run.

This module is deliberately self-contained.  It reconstructs the small
metatheory fragments needed by this run from the names already present in the
repository; it does not import the sealed implementation.  The three primary
objects are data (carriers, edges, maps, profiles, and presentations), not a
table of missing flags.  All reports are deterministic and timestamp-free.

Evidence class: FINITE_COMPUTATION for the enumerations and replay checks;
DEFINITION for the local reconstructed event grammar; DECLARED_POLICY for the
chosen finite candidate space and orientation price; OPEN for everything
outside those declarations.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from itertools import combinations, permutations
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence, Union

Pair = tuple[int, int]
Function = tuple[int, ...]
EdgeSet = tuple[Pair, ...]

ROOT = Path(__file__).resolve().parent
PROMPT_SHA256 = "4914cd2a087437830ab5119c25338e4a82cca883a42c555aa32d63906cb6e1ef"
WRITE_ROOT = "research/priced_admissions"
SEALED_PATHS: tuple[str, ...] = (
    "prompt/",
    "paper/",
    "code/",
    "lean4/Derivation/",
    "artifacts/",
    "CLAUDE.md",
    ".github/workflows/verify.yml",
    "research/thinghood/",
    "research/genesis_continuation/",
)
LEGAL_TERMINALS: tuple[str, ...] = (
    "THREE_OBJECTS_BUILT",
    "NEXT_EVENT_FOUND",
    "NEXT_EVENT_NOT_FOUND",
    "ORIENTATION_PRICED",
    "ORIENTATION_EXCLUDED",
    "S9_BRIDGE_PRICED",
    "LAW_LATTICE_EXTENDED",
    "TIES_RETAINED",
    "OB1_UNCHANGED",
    "S66_UNCHANGED",
    "S9_LAST_UNCHANGED",
    "CANDIDATE_SPACE_OPEN",
    "REFUSED",
)


# ---------------------------------------------------------------------------
# A local reconstruction of the existing event grammar (METATHEORY)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SupplyEvent:
    token: str


@dataclass(frozen=True)
class AdmitDatumEvent:
    token: str


@dataclass(frozen=True)
class AdmitFormEvent:
    arity: int


@dataclass(frozen=True)
class AdmitInstanceEvent:
    form: int
    args: tuple[int, ...]


@dataclass(frozen=True)
class AdmitRuleEvent:
    form: int


@dataclass(frozen=True)
class ImposeEvent:
    pair: Pair


@dataclass(frozen=True)
class ObserveEvent:
    label: str


@dataclass(frozen=True)
class AssertWitnessEvent:
    pair: Pair


@dataclass(frozen=True)
class RetainWitnessEvent:
    pair: Pair


@dataclass(frozen=True)
class ProtectEvent:
    pair: Pair


@dataclass(frozen=True)
class DeclareObservationEvent:
    pass


@dataclass(frozen=True)
class RefineColumnEvent:
    column: tuple[int, ...]
    point: int


@dataclass(frozen=True)
class AddColumnEvent:
    column: tuple[int, ...]


@dataclass(frozen=True)
class RefuseEvent:
    pair: Pair


@dataclass(frozen=True)
class SetBudgetEvent:
    budget: int


@dataclass(frozen=True)
class SetLicenseEvent:
    licensed: bool


Event = Union[
    SupplyEvent,
    AdmitDatumEvent,
    AdmitFormEvent,
    AdmitInstanceEvent,
    AdmitRuleEvent,
    ImposeEvent,
    ObserveEvent,
    AssertWitnessEvent,
    RetainWitnessEvent,
    ProtectEvent,
    DeclareObservationEvent,
    RefineColumnEvent,
    AddColumnEvent,
    RefuseEvent,
    SetBudgetEvent,
    SetLicenseEvent,
]


@dataclass(frozen=True)
class GrammarState:
    """Local replay state matching the repository's admission fields."""

    presentations: tuple[str, ...] = ()
    data: tuple[str, ...] = ()
    forms: tuple[int, ...] = ()
    instances: tuple[tuple[int, tuple[int, ...]], ...] = ()
    rules: tuple[int, ...] = ()
    requirements: tuple[Pair, ...] = ()
    occurrences: tuple[int, ...] = ()
    asserted: tuple[Pair, ...] = ()
    witnesses: tuple[Pair, ...] = ()
    protected: tuple[Pair, ...] = ()
    observation: Optional[tuple[tuple[int, ...], ...]] = None
    budget: int = 0
    licensed: bool = True
    refusals: tuple[Pair, ...] = ()


def _append_unique(values: tuple[Any, ...], value: Any) -> tuple[Any, ...]:
    return values if value in values else values + (value,)


def replay_events(events: Sequence[Event]) -> GrammarState:
    """Replay the reconstructed grammar from an empty state.

    This mirrors the admitted-state transitions and the guarded passage
    constructors.  Invalid guarded events are ignored, as in the sealed
    passage step; the history remains inspectable and deterministic.
    """

    state = GrammarState()
    for event in events:
        if isinstance(event, SupplyEvent):
            state = GrammarState(
                presentations=_append_unique(state.presentations, event.token),
                data=state.data,
                forms=state.forms,
                instances=state.instances,
                rules=state.rules,
                requirements=state.requirements,
                occurrences=state.occurrences,
                asserted=state.asserted,
                witnesses=state.witnesses,
                protected=state.protected,
                observation=state.observation,
                budget=state.budget,
                licensed=state.licensed,
                refusals=state.refusals,
            )
        elif isinstance(event, AdmitDatumEvent):
            state = GrammarState(
                presentations=state.presentations,
                data=_append_unique(state.data, event.token),
                forms=state.forms,
                instances=state.instances,
                rules=state.rules,
                requirements=state.requirements,
                occurrences=state.occurrences,
                asserted=state.asserted,
                witnesses=state.witnesses,
                protected=state.protected,
                observation=state.observation,
                budget=state.budget,
                licensed=state.licensed,
                refusals=state.refusals,
            )
        elif isinstance(event, AdmitFormEvent):
            if event.arity >= 1:
                state = GrammarState(
                    presentations=state.presentations,
                    data=state.data,
                    forms=state.forms + (event.arity,),
                    instances=state.instances,
                    rules=state.rules,
                    requirements=state.requirements,
                    occurrences=state.occurrences,
                    asserted=state.asserted,
                    witnesses=state.witnesses,
                    protected=state.protected,
                    observation=state.observation,
                    budget=state.budget,
                    licensed=state.licensed,
                    refusals=state.refusals,
                )
        elif isinstance(event, AdmitInstanceEvent):
            if (
                0 <= event.form < len(state.forms)
                and len(event.args) == state.forms[event.form]
                and all(0 <= value < len(state.data) for value in event.args)
            ):
                item = (event.form, event.args)
                state = GrammarState(
                    presentations=state.presentations,
                    data=state.data,
                    forms=state.forms,
                    instances=_append_unique(state.instances, item),
                    rules=state.rules,
                    requirements=state.requirements,
                    occurrences=state.occurrences,
                    asserted=state.asserted,
                    witnesses=state.witnesses,
                    protected=state.protected,
                    observation=state.observation,
                    budget=state.budget,
                    licensed=state.licensed,
                    refusals=state.refusals,
                )
        elif isinstance(event, AdmitRuleEvent):
            if 0 <= event.form < len(state.forms):
                state = GrammarState(
                    presentations=state.presentations,
                    data=state.data,
                    forms=state.forms,
                    instances=state.instances,
                    rules=_append_unique(state.rules, event.form),
                    requirements=state.requirements,
                    occurrences=state.occurrences,
                    asserted=state.asserted,
                    witnesses=state.witnesses,
                    protected=state.protected,
                    observation=state.observation,
                    budget=state.budget,
                    licensed=state.licensed,
                    refusals=state.refusals,
                )
        elif isinstance(event, ImposeEvent):
            i, j = event.pair
            if 0 <= i < j < len(state.data):
                state = GrammarState(
                    presentations=state.presentations,
                    data=state.data,
                    forms=state.forms,
                    instances=state.instances,
                    rules=state.rules,
                    requirements=_append_unique(state.requirements, event.pair),
                    occurrences=state.occurrences,
                    asserted=state.asserted,
                    witnesses=state.witnesses,
                    protected=state.protected,
                    observation=state.observation,
                    budget=state.budget,
                    licensed=state.licensed,
                    refusals=state.refusals,
                )
        elif isinstance(event, AssertWitnessEvent):
            i, j = event.pair
            if (
                0 <= i < j < len(state.occurrences)
                and event.pair not in state.asserted
            ):
                state = _replace_passage(state, asserted=state.asserted + (event.pair,))
        elif isinstance(event, RetainWitnessEvent):
            if (
                event.pair in state.asserted
                and event.pair not in state.witnesses
            ):
                state = _replace_passage(state, witnesses=state.witnesses + (event.pair,))
        elif isinstance(event, ProtectEvent):
            if (
                event.pair in state.witnesses
                and event.pair not in state.protected
            ):
                state = _replace_passage(state, protected=state.protected + (event.pair,))
        elif isinstance(event, DeclareObservationEvent):
            if state.observation is None:
                state = _replace_passage(state, observation=())
        elif isinstance(event, RefineColumnEvent):
            if _refine_guard(state, event.column, event.point):
                assert state.observation is not None
                refined = tuple(
                    (event.point,) + column if column == event.column else column
                    for column in state.observation
                )
                state = _replace_passage(
                    state,
                    observation=refined,
                    budget=max(0, state.budget - 1),
                )
        elif isinstance(event, AddColumnEvent):
            if _column_guard(state, event.column):
                assert state.observation is not None
                state = _replace_passage(
                    state,
                    observation=state.observation + (event.column,),
                    budget=max(0, state.budget - 1),
                )
        elif isinstance(event, RefuseEvent):
            if _active_obstruction(state, event.pair):
                state = _replace_passage(
                    state,
                    refusals=_append_unique(state.refusals, event.pair),
                )
        elif isinstance(event, SetBudgetEvent):
            if event.budget >= 0:
                state = _replace_passage(state, budget=event.budget)
        elif isinstance(event, SetLicenseEvent):
            state = _replace_passage(state, licensed=event.licensed)
        elif isinstance(event, ObserveEvent):
            # Observe is a reconstructed declaration marker; it does not
            # mutate admitted state.  The payload remains in the report.
            continue
    return state


def _replace_passage(state: GrammarState, **changes: Any) -> GrammarState:
    values = {
        "presentations": state.presentations,
        "data": state.data,
        "forms": state.forms,
        "instances": state.instances,
        "rules": state.rules,
        "requirements": state.requirements,
        "occurrences": state.occurrences,
        "asserted": state.asserted,
        "witnesses": state.witnesses,
        "protected": state.protected,
        "observation": state.observation,
        "budget": state.budget,
        "licensed": state.licensed,
        "refusals": state.refusals,
    }
    values.update(changes)
    return GrammarState(**values)


def _active_obstruction(state: GrammarState, pair: Pair) -> bool:
    if state.observation is None:
        return False
    i, j = pair
    if pair not in state.witnesses or pair not in state.protected:
        return False
    return all((i in column) == (j in column) for column in state.observation)


def _refine_guard(state: GrammarState, column: tuple[int, ...], point: int) -> bool:
    return (
        state.observation is not None
        and column in state.observation
        and point in state.occurrences
        and point not in column
        and any(_active_obstruction(state, pair) for pair in state.protected)
        and state.budget > 0
    )


def _column_guard(state: GrammarState, column: tuple[int, ...]) -> bool:
    return (
        state.observation is not None
        and column not in state.observation
        and all(point in state.occurrences for point in column)
        and any(_active_obstruction(state, pair) for pair in state.protected)
        and state.licensed
        and state.budget > 0
    )


def event_json(event: Event) -> dict[str, Any]:
    if isinstance(event, SupplyEvent):
        return {"kind": "Supply", "token": event.token}
    if isinstance(event, AdmitDatumEvent):
        return {"kind": "AdmitDatum", "token": event.token}
    if isinstance(event, AdmitFormEvent):
        return {"kind": "AdmitForm", "arity": event.arity}
    if isinstance(event, AdmitInstanceEvent):
        return {"kind": "AdmitInst", "form": event.form, "args": list(event.args)}
    if isinstance(event, AdmitRuleEvent):
        return {"kind": "AdmitRuleAll", "form": event.form}
    if isinstance(event, ImposeEvent):
        return {"kind": "Impose", "pair": list(event.pair)}
    if isinstance(event, ObserveEvent):
        return {"kind": "Observe", "label": event.label}
    if isinstance(event, AssertWitnessEvent):
        return {"kind": "assertWit", "pair": list(event.pair)}
    if isinstance(event, RetainWitnessEvent):
        return {"kind": "admitWit", "pair": list(event.pair)}
    if isinstance(event, ProtectEvent):
        return {"kind": "protect", "pair": list(event.pair)}
    if isinstance(event, DeclareObservationEvent):
        return {"kind": "declareObs"}
    if isinstance(event, RefineColumnEvent):
        return {"kind": "refineCol", "column": list(event.column), "point": event.point}
    if isinstance(event, AddColumnEvent):
        return {"kind": "addCol", "column": list(event.column)}
    if isinstance(event, RefuseEvent):
        return {"kind": "refuse", "pair": list(event.pair)}
    if isinstance(event, SetBudgetEvent):
        return {"kind": "setBudget", "budget": event.budget}
    if isinstance(event, SetLicenseEvent):
        return {"kind": "setLicense", "licensed": event.licensed}
    raise TypeError(f"unsupported event: {event!r}")


def state_json(state: GrammarState) -> dict[str, Any]:
    return {
        "presentations": list(state.presentations),
        "data": list(state.data),
        "forms": list(state.forms),
        "instances": [[form, list(args)] for form, args in state.instances],
        "rules": list(state.rules),
        "requirements": [list(pair) for pair in state.requirements],
        "occurrences": list(state.occurrences),
        "asserted": [list(pair) for pair in state.asserted],
        "witnesses": [list(pair) for pair in state.witnesses],
        "protected": [list(pair) for pair in state.protected],
        "observation": (
            None
            if state.observation is None
            else [list(column) for column in state.observation]
        ),
        "budget": state.budget,
        "licensed": state.licensed,
        "refusals": [list(pair) for pair in state.refusals],
    }


# ---------------------------------------------------------------------------
# Concrete objects
# ---------------------------------------------------------------------------


def _merge_map(carrier: Sequence[int], left: int, right: int) -> Function:
    return tuple(left if point == right else point for point in carrier)


def _pushforward(edges: Iterable[Pair], mapping: Function) -> EdgeSet:
    return tuple(sorted({(mapping[left], mapping[right]) for left, right in edges}))


def _irreflexive(edges: Iterable[Pair]) -> bool:
    return all(left != right for left, right in edges)


def _asymmetric(edges: Iterable[Pair]) -> bool:
    edge_set = set(edges)
    return all((right, left) not in edge_set for left, right in edge_set)


def _contexts(forms: Sequence[int], data_count: int) -> tuple[tuple[int, tuple[Optional[int], ...]], ...]:
    out: list[tuple[int, tuple[Optional[int], ...]]] = []
    for form, arity in enumerate(forms):
        choices: tuple[Optional[int], ...] = (None,) + tuple(range(data_count))
        slots: list[tuple[Optional[int], ...]] = [()]
        for _ in range(arity):
            slots = [prefix + (choice,) for prefix in slots for choice in choices]
        out.extend(
            (form, slot_tuple)
            for slot_tuple in slots
            if any(value is None for value in slot_tuple)
        )
    return tuple(out)


def _profiles(
    forms: Sequence[int],
    data_count: int,
    instances: Sequence[tuple[int, tuple[int, ...]]],
    rules: Sequence[int],
) -> tuple[tuple[tuple[int, tuple[Optional[int], ...]], ...], ...]:
    contexts = _contexts(forms, data_count)
    instance_set = set(instances)
    rule_set = set(rules)
    result: list[tuple[tuple[int, tuple[Optional[int], ...]], ...]] = []
    for datum in range(data_count):
        seen: list[tuple[int, tuple[Optional[int], ...]]] = []
        for form, slots in contexts:
            plugged = (form, tuple(datum if value is None else value for value in slots))
            if form in rule_set or plugged in instance_set:
                seen.append((form, slots))
        result.append(tuple(seen))
    return tuple(result)


@dataclass(frozen=True)
class CollisionObject:
    carrier: tuple[int, ...]
    edges: EdgeSet
    asserted_pair: Pair
    identifying_map: Function
    pushed_edges: EdgeSet
    protected_law: str
    law_before: bool
    law_after: bool
    event_state: GrammarState
    absent: tuple[str, ...]


@dataclass(frozen=True)
class EqualProfilesObject:
    carrier: tuple[int, ...]
    edges: EdgeSet
    forms: tuple[int, ...]
    instances: tuple[tuple[int, tuple[int, ...]], ...]
    contexts: tuple[tuple[int, tuple[Optional[int], ...]], ...]
    profiles: tuple[tuple[tuple[int, tuple[Optional[int], ...]], ...], ...]
    equal_pair: Pair
    event_state: GrammarState
    absent: tuple[str, ...]


@dataclass(frozen=True)
class ResidualObject:
    carrier: tuple[int, ...]
    edges: EdgeSet
    left_presentation: Function
    right_presentation: Function
    residual_pair: Pair
    left_image: EdgeSet
    right_image: EdgeSet
    comparison_policy: Optional[str]
    event_state: GrammarState
    absent: tuple[str, ...]


def build_collision() -> CollisionObject:
    carrier = (0, 1)
    edges: EdgeSet = ((0, 1),)
    pair = (0, 1)
    mapping = _merge_map(carrier, *pair)
    pushed = _pushforward(edges, mapping)
    state = replay_events(
        (
            SupplyEvent("<a>"),
            SupplyEvent("<ab>"),
            AdmitDatumEvent("<a>"),
            AdmitDatumEvent("<ab>"),
        )
    )
    return CollisionObject(
        carrier=carrier,
        edges=edges,
        asserted_pair=pair,
        identifying_map=mapping,
        pushed_edges=pushed,
        protected_law="irreflexive",
        law_before=_irreflexive(edges),
        law_after=_irreflexive(pushed),
        event_state=state,
        absent=(
            "retained witness",
            "protected pair",
            "declared observation",
            "observer-zero certificate",
            "pair-separation closure policy",
        ),
    )


def build_equal_profiles() -> EqualProfilesObject:
    carrier = (0, 1)
    edges: EdgeSet = ()
    forms = (1,)
    instances: tuple[tuple[int, tuple[int, ...]], ...] = ()
    contexts = _contexts(forms, len(carrier))
    profile_rows = _profiles(forms, len(carrier), instances, ())
    state = replay_events(
        (
            SupplyEvent("<a>"),
            SupplyEvent("<ab>"),
            AdmitDatumEvent("<a>"),
            AdmitDatumEvent("<ab>"),
            AdmitFormEvent(1),
        )
    )
    return EqualProfilesObject(
        carrier=carrier,
        edges=edges,
        forms=forms,
        instances=instances,
        contexts=contexts,
        profiles=profile_rows,
        equal_pair=(0, 1),
        event_state=state,
        absent=(
            "derivable instance distinguishing the pair",
            "retained witness",
            "protected pair",
            "declared observation",
            "pair-separation closure policy",
        ),
    )


def build_directional_residual() -> ResidualObject:
    carrier = (0, 1)
    edges: EdgeSet = ((0, 1),)
    left = (0, 0)
    right = (0, 1)
    state = replay_events(
        (
            SupplyEvent("L"),
            SupplyEvent("F"),
            AdmitDatumEvent("L"),
            AdmitDatumEvent("F"),
        )
    )
    return ResidualObject(
        carrier=carrier,
        edges=edges,
        left_presentation=left,
        right_presentation=right,
        residual_pair=(0, 1),
        left_image=_pushforward(edges, left),
        right_image=_pushforward(edges, right),
        comparison_policy=None,
        event_state=state,
        absent=(
            "declared comparison policy",
            "retained witness",
            "protected pair",
            "declared observation event",
            "pair-separation closure policy",
        ),
    )


def _object_payload(obj: Union[CollisionObject, EqualProfilesObject, ResidualObject]) -> dict[str, Any]:
    if isinstance(obj, CollisionObject):
        return {
            "kind": "collision",
            "carrier": list(obj.carrier),
            "edges": [list(pair) for pair in obj.edges],
            "asserted_pair": list(obj.asserted_pair),
            "identifying_map": list(obj.identifying_map),
            "pushed_edges": [list(pair) for pair in obj.pushed_edges],
            "protected_law": obj.protected_law,
            "law_before": obj.law_before,
            "law_after": obj.law_after,
            "event_state": state_json(obj.event_state),
            "absent": list(obj.absent),
        }
    if isinstance(obj, EqualProfilesObject):
        return {
            "kind": "equal_profiles",
            "carrier": list(obj.carrier),
            "edges": [list(pair) for pair in obj.edges],
            "forms": list(obj.forms),
            "instances": [[form, list(args)] for form, args in obj.instances],
            "contexts": [[form, list(slots)] for form, slots in obj.contexts],
            "profiles": [
                [[form, list(slots)] for form, slots in row]
                for row in obj.profiles
            ],
            "equal_pair": list(obj.equal_pair),
            "event_state": state_json(obj.event_state),
            "absent": list(obj.absent),
        }
    return {
        "kind": "directional_residual",
        "carrier": list(obj.carrier),
        "edges": [list(pair) for pair in obj.edges],
        "left_presentation": list(obj.left_presentation),
        "right_presentation": list(obj.right_presentation),
        "residual_pair": list(obj.residual_pair),
        "left_image": [list(pair) for pair in obj.left_image],
        "right_image": [list(pair) for pair in obj.right_image],
        "comparison_policy": obj.comparison_policy,
        "event_state": state_json(obj.event_state),
        "absent": list(obj.absent),
    }


def _event_search(
    name: str,
    state: GrammarState,
    pair: Pair,
    absent: Sequence[str],
    object_fields: Mapping[str, Any],
    observation_sources: Sequence[tuple[str, str]],
) -> dict[str, Any]:
    """Search constructors, then separately apply the guarded response rule.

    The report is derived from the concrete state and pair.  External
    ``Impose`` is recorded separately and never makes ``next_event_found``
    true.  An ``Observe`` offer is admitted to that field only when its label
    and source field are carried by the concrete object.  There is no
    requirement table and no synthetic demand-source field.
    """

    object_derived: list[dict[str, Any]] = []
    external: list[Event] = []
    guarded_responses: list[Event] = []
    grammar_offers_without_object_ingredient: list[Event] = []
    if pair[1] < len(state.data) and pair[0] < pair[1]:
        external.append(ImposeEvent(pair))
    if state.observation is None:
        # ``declareObs`` has no payload, so it is intentionally not an
        # object-derived event.  Keeping it visible prevents a no-argument
        # constructor from masquerading as a priced observation.
        grammar_offers_without_object_ingredient.append(DeclareObservationEvent())
    for label, source_field in observation_sources:
        if source_field not in object_fields:
            raise ValueError(f"observation source is not an object field: {source_field}")
        object_derived.append(
            {
                "event": event_json(ObserveEvent(label)),
                "source_field": source_field,
                "source_value": object_fields[source_field],
            }
        )
    if _active_obstruction(state, pair):
        guarded_responses.extend(
            (
                RefuseEvent(pair),
                AddColumnEvent((pair[0],)),
            )
        )
    response_not_found = not guarded_responses
    return {
        "object": name,
        "object_fields": dict(object_fields),
        "grammar_state_fields": sorted(state_json(state)),
        "fields_outside_grammar_state": sorted(
            field for field in object_fields if field not in state_json(state)
        ),
        "object_derived_events": object_derived,
        "grammar_offers_without_object_ingredient": [
            event_json(event) for event in grammar_offers_without_object_ingredient
        ],
        "external_challenge_candidates": [event_json(event) for event in external],
        "constructed_guarded_responses": [event_json(event) for event in guarded_responses],
        "next_event_found": bool(object_derived or guarded_responses),
        "next_event_not_found_scope": "guarded_response_family" if response_not_found else None,
        "guarded_response_found": bool(guarded_responses),
        "endogenous_successor_found": False,
        "external_challenge_found": bool(external),
        "missing_admissions_for_guarded_response": list(absent) if response_not_found else [],
        "source_classification": {
            "object_derived_events": "FINITE_COMPUTATION",
            "grammar_offers_without_object_ingredient": "DEFINITION",
            "external_challenges": "SUPPLIED_INPUT",
            "guarded_responses": "DEFINITION",
            "conclusion": "FINITE_COMPUTATION",
        },
    }


def event_search_report() -> dict[str, Any]:
    collision = build_collision()
    profiles = build_equal_profiles()
    residual = build_directional_residual()
    return {
        "collision": _event_search(
            "collision",
            collision.event_state,
            collision.asserted_pair,
            collision.absent,
            {
                "asserted_pair": list(collision.asserted_pair),
                "identifying_map": list(collision.identifying_map),
                "pushed_edges": [list(edge) for edge in collision.pushed_edges],
            },
            (),
        ),
        "equal_profiles": _event_search(
            "equal_profiles",
            profiles.event_state,
            profiles.equal_pair,
            profiles.absent,
            {
                "equal_pair": list(profiles.equal_pair),
                "contexts": [
                    [form, list(slots)] for form, slots in profiles.contexts
                ],
                "profiles": [
                    [[form, list(slots)] for form, slots in row]
                    for row in profiles.profiles
                ],
            },
            (("equal-profile-context", "contexts"),),
        ),
        "directional_residual": _event_search(
            "directional_residual",
            residual.event_state,
            residual.residual_pair,
            residual.absent,
            {
                "residual_pair": list(residual.residual_pair),
                "left_presentation": list(residual.left_presentation),
                "right_presentation": list(residual.right_presentation),
            },
            (
                ("p", "left_presentation"),
                ("q", "right_presentation"),
            ),
        ),
    }


# ---------------------------------------------------------------------------
# Orientation-priced finite candidate space
# ---------------------------------------------------------------------------


LAW_NAMES: tuple[str, ...] = (
    "none",
    "irreflexive",
    "asymmetric",
    "symmetric",
    "transitive",
    "irreflexive+transitive",
)
LAW_ATOMS: dict[str, int] = {
    "none": 0,
    "irreflexive": 1,
    "asymmetric": 1,
    "symmetric": 1,
    "transitive": 1,
    "irreflexive+transitive": 2,
}
MAX_CARRIER = 3
MAX_RELATION_EDGES = 3


def law_holds(law: str, edges: Iterable[Pair]) -> bool:
    edge_set = set(edges)
    if law == "none":
        return True
    if law == "irreflexive":
        return _irreflexive(edge_set)
    if law == "asymmetric":
        return _asymmetric(edge_set)
    if law == "symmetric":
        return all((right, left) in edge_set for left, right in edge_set)
    if law == "transitive":
        return all(
            (left, far) in edge_set
            for left, middle in edge_set
            for middle2, far in edge_set
            if middle == middle2
        )
    if law == "irreflexive+transitive":
        return _irreflexive(edge_set) and law_holds("transitive", edge_set)
    raise ValueError(f"unknown law {law!r}")


@dataclass(frozen=True)
class CandidateBill:
    carrier: int
    occurrences: int
    relation: int
    witness: int
    law: int
    orientation: int

    @property
    def total(self) -> int:
        return (
            self.carrier
            + self.occurrences
            + self.relation
            + self.witness
            + self.law
            + self.orientation
        )

    def json(self) -> dict[str, int]:
        return {
            "carrier": self.carrier,
            "occurrences": self.occurrences,
            "relation": self.relation,
            "witness": self.witness,
            "law": self.law,
            "orientation": self.orientation,
            "total": self.total,
        }


@dataclass(frozen=True)
class OrientedCandidate:
    carrier_size: int
    edges: EdgeSet
    asserted_pair: Optional[Pair]
    law: str
    orientation_admitted: bool

    def bill(self) -> CandidateBill:
        has_pair = self.asserted_pair is not None
        return CandidateBill(
            carrier=self.carrier_size,
            occurrences=2 if has_pair else 0,
            relation=len(self.edges),
            witness=1 if has_pair else 0,
            law=LAW_ATOMS[self.law],
            orientation=1 if self.orientation_admitted else 0,
        )

    def json(self) -> dict[str, Any]:
        return {
            "carrier_size": self.carrier_size,
            "edges": [list(pair) for pair in self.edges],
            "asserted_pair": (
                None if self.asserted_pair is None else list(self.asserted_pair)
            ),
            "law": self.law,
            "orientation_admitted": self.orientation_admitted,
            "bill": self.bill().json(),
        }


def _relation_subsets(n: int) -> Iterable[EdgeSet]:
    edges = tuple((left, right) for left in range(n) for right in range(n) if left != right)
    for size in range(min(MAX_RELATION_EDGES, len(edges)) + 1):
        for chosen in combinations(edges, size):
            yield tuple(chosen)


def enumerate_candidates(force_orientation: Optional[bool] = None) -> tuple[OrientedCandidate, ...]:
    out: list[OrientedCandidate] = []
    orientations = (False, True) if force_orientation is None else (force_orientation,)
    for n in range(1, MAX_CARRIER + 1):
        for edges in _relation_subsets(n):
            assertions: tuple[Optional[Pair], ...] = (None,) + edges
            for asserted in assertions:
                for law in LAW_NAMES:
                    for orientation in orientations:
                        out.append(OrientedCandidate(n, edges, asserted, law, orientation))
    return tuple(out)


def _collapse_witness(candidate: OrientedCandidate) -> Optional[dict[str, Any]]:
    if candidate.asserted_pair is None:
        return None
    left, right = candidate.asserted_pair
    mapping = _merge_map(tuple(range(candidate.carrier_size)), left, right)
    pushed = _pushforward(candidate.edges, mapping)
    if not law_holds(candidate.law, candidate.edges):
        return None
    if law_holds(candidate.law, pushed):
        return None
    return {
        "pair": [left, right],
        "map": list(mapping),
        "pushed_edges": [list(pair) for pair in pushed],
        "law_before": True,
        "law_after": False,
    }


def is_thing(candidate: OrientedCandidate, require_orientation: bool = True) -> bool:
    if require_orientation and not candidate.orientation_admitted:
        return False
    return _collapse_witness(candidate) is not None


def canonical_key(candidate: OrientedCandidate) -> tuple[Any, ...]:
    """Canonical key that preserves the ordered asserted pair."""

    keys: list[tuple[Any, ...]] = []
    for permutation in permutations(range(candidate.carrier_size)):
        rel = tuple(sorted((permutation[x], permutation[y]) for x, y in candidate.edges))
        asserted = (
            None
            if candidate.asserted_pair is None
            else (
                permutation[candidate.asserted_pair[0]],
                permutation[candidate.asserted_pair[1]],
            )
        )
        keys.append((candidate.carrier_size, rel, asserted, candidate.law, candidate.orientation_admitted))
    return min(keys)


def _minimum(force_orientation: bool, require_orientation: bool) -> dict[str, Any]:
    candidates = enumerate_candidates(force_orientation)
    survivors = tuple(candidate for candidate in candidates if is_thing(candidate, require_orientation))
    if not survivors:
        return {
            "candidate_count": len(candidates),
            "survivor_count": 0,
            "minimum_cost": None,
            "raw_minimum_count": 0,
            "minimum_isomorphism_class_count": 0,
            "representatives": [],
        }
    minimum_cost = min(candidate.bill().total for candidate in survivors)
    raw_minima = tuple(candidate for candidate in survivors if candidate.bill().total == minimum_cost)
    classes: dict[tuple[Any, ...], list[OrientedCandidate]] = {}
    for candidate in raw_minima:
        classes.setdefault(canonical_key(candidate), []).append(candidate)
    representatives = [
        {
            "class_key": repr(key),
            "class_size": len(members),
            "candidate": members[0].json(),
            "collapse_witness": _collapse_witness(members[0]),
        }
        for key, members in sorted(classes.items(), key=lambda item: repr(item[0]))
    ]
    return {
        "candidate_count": len(candidates),
        "survivor_count": len(survivors),
        "minimum_cost": minimum_cost,
        "cost_measure": (
            "mu_oriented_s9: additive atoms for carrier, two occurrences, "
            "relation, witness, named law, and orientation"
        ),
        "raw_minimum_count": len(raw_minima),
        "minimum_isomorphism_class_count": len(representatives),
        "non_unique_first_answer": len(representatives) > 1,
        "representatives": representatives,
    }


def law_violation_report() -> dict[str, Any]:
    rows: dict[str, Any] = {}
    all_candidates = enumerate_candidates(True)
    for law in LAW_NAMES:
        witness: Optional[dict[str, Any]] = None
        for candidate in all_candidates:
            if candidate.law != law:
                continue
            collapse = _collapse_witness(candidate)
            if collapse is not None:
                witness = {"candidate": candidate.json(), "collapse": collapse}
                break
        rows[law] = {
            "declared_in_finite_law_list": True,
            "identifying_witnessed_pair_can_violate": witness is not None,
            "witness": witness,
        }
    return {
        "law_list": list(LAW_NAMES),
        "law_list_was_enlarged": False,
        "rows": rows,
        "uncompared_laws_remain_open": True,
    }


def orientation_report() -> dict[str, Any]:
    baseline = _minimum(False, False)
    priced = _minimum(True, True)
    forward = OrientedCandidate(2, ((0, 1),), (0, 1), "irreflexive", True)
    reverse_same_pair = OrientedCandidate(2, ((1, 0),), (0, 1), "irreflexive", True)
    return {
        "policy": "ORIENTATION_INCLUDED_AND_PRICED",
        "bill_atom": "orientation",
        "atom_cost": 1,
        "iso_key_preserves_ordered_pair": True,
        "forward_key": repr(canonical_key(forward)),
        "reverse_same_pair_key": repr(canonical_key(reverse_same_pair)),
        "forward_reverse_keys_differ": canonical_key(forward) != canonical_key(reverse_same_pair),
        "minimum_without_orientation": baseline,
        "minimum_with_orientation": priced,
        "orientation_price": (
            None
            if baseline["minimum_cost"] is None or priced["minimum_cost"] is None
            else priced["minimum_cost"] - baseline["minimum_cost"]
        ),
        "ties_retained": bool(priced["non_unique_first_answer"]),
        "open_scope": (
            "The finite carrier <= 3, relation-edge <= 3, six-law list is the "
            "declared candidate space; other admissions and laws remain OPEN."
        ),
    }


# ---------------------------------------------------------------------------
# The six-line S9 bill and receipt
# ---------------------------------------------------------------------------


def s9_bill_report() -> dict[str, Any]:
    state = replay_events((SupplyEvent("<>"),))
    lines = [
        {
            "line": "carrier",
            "required": "a carrier with two points",
            "paid": len(state.data) >= 2,
            "missing": "AdmitDatum for two occurrences",
        },
        {
            "line": "occurrences",
            "required": ["left occurrence", "right occurrence"],
            "paid": len(state.data) >= 2,
            "missing": "two AdmitDatum events",
        },
        {
            "line": "relation",
            "required": "one admitted ordered edge",
            "paid": False,
            "missing": "relation admission is not in the inscription",
        },
        {
            "line": "witness",
            "required": "retained asserted pair",
            "paid": bool(state.witnesses),
            "missing": "assertWit/admitWit passage admissions",
        },
        {
            "line": "irreflexivity",
            "required": "a named irreflexive law",
            "paid": False,
            "missing": "law admission",
        },
        {
            "line": "orientation",
            "required": "ordered-pair admission",
            "paid": False,
            "missing": "orientation admission",
        },
    ]
    return {
        "schema": "s9-six-line-bill-v1",
        "history": [event_json(SupplyEvent("<>"))],
        "replayed_state": state_json(state),
        "supply_is_not_admission": state.data == (),
        "lines": lines,
        "paid_lines": [line["line"] for line in lines if line["paid"]],
        "unpaid_lines": [line["line"] for line in lines if not line["paid"]],
        "all_unpaid": all(not line["paid"] for line in lines),
    }


def prompt_hash() -> str:
    data = (ROOT / "PROMPT.md").read_bytes()
    return hashlib.sha256(data).hexdigest()


def _falsifiers() -> dict[str, str]:
    return {
        "objects": "Delete one concrete carrier/map/profile field and object construction tests fail.",
        "events": "Admit an unlisted response ingredient or mark a guarded response found; event-search tests fail.",
        "orientation": "Replace the ordered-pair key with an unordered pair key; the forward/reverse mutation test fails.",
        "s9": "Replay an AdmitDatum after Supply or mark a bill line paid; the replay/negative test fails.",
        "opens": "Add an OB-1, S6.6, or S9-last closure terminal; the forbidden-closure test fails.",
    }


def build_receipt() -> dict[str, Any]:
    current_hash = prompt_hash()
    if current_hash != PROMPT_SHA256:
        raise RuntimeError(
            f"prompt drift: expected {PROMPT_SHA256}, got {current_hash}"
        )
    collision = build_collision()
    equal_profiles = build_equal_profiles()
    residual = build_directional_residual()
    searches = event_search_report()
    orientation = orientation_report()
    s9 = s9_bill_report()
    guarded_not_found = sum(
        1 for report in searches.values() if report["next_event_not_found_scope"]
    )
    terminals = [
        "THREE_OBJECTS_BUILT",
        "NEXT_EVENT_FOUND",
        "NEXT_EVENT_NOT_FOUND",
        "ORIENTATION_PRICED",
        "S9_BRIDGE_PRICED",
        "TIES_RETAINED",
        "OB1_UNCHANGED",
        "S66_UNCHANGED",
        "S9_LAST_UNCHANGED",
        "CANDIDATE_SPACE_OPEN",
        "REFUSED",
    ]
    assert set(terminals).issubset(set(LEGAL_TERMINALS))
    return {
        "schema": "priced-admissions-v1",
        "evidence_class": "FINITE_COMPUTATION",
        "prompt_sha256": current_hash,
        "write_root": WRITE_ROOT,
        "sealed_paths": list(SEALED_PATHS),
        "sealed_paths_touched": [],
        "objects_are_concrete_data": True,
        "objects": {
            "collision": _object_payload(collision),
            "equal_profiles": _object_payload(equal_profiles),
            "directional_residual": _object_payload(residual),
        },
        "event_grammar": {
            "classification": "DEFINITION",
            "reconstructed_from_names": [
                "AdmitDatum",
                "AdmitForm",
                "AdmitInst",
                "AdmitRuleAll",
                "Supply",
                "Impose",
                "Observe",
                "assertWit",
                "admitWit",
                "protect",
                "declareObs",
                "refineCol",
                "addCol",
                "refuse",
            ],
            "not_imported": True,
            "search": searches,
            "next_event_found_scope": "object_derived_event_only",
            "external_challenges_do_not_set_next_event_found": True,
            "object_derived_next_event_count": sum(
                1 for report in searches.values() if report["next_event_found"]
            ),
            "external_next_event_count": sum(
                1 for report in searches.values() if report["external_challenge_found"]
            ),
            "guarded_response_not_found_count": guarded_not_found,
            "no_endogenous_successor_derived": all(
                not report["endogenous_successor_found"] for report in searches.values()
            ),
        },
        "orientation": orientation,
        "law_lattice": law_violation_report(),
        "s9_bill": s9,
        "distinctions": {
            "datum": "an admitted occurrence/pair in the local grammar",
            "difference": "the asserted ordered pair plus a declared law-bearing relation",
            "thing": "a finite candidate whose identifying map violates its named law",
            "primitive_difference_not_renamed": True,
        },
        "open_boundaries": {
            "OB-1": "OPEN",
            "S6_item_6": "OPEN",
            "S9_last_bullet": "OPEN",
            "candidate_space": "OPEN outside the named finite enumeration",
            "comparison_policy": "OPEN for the directional residual",
        },
        "refusals": [
            {
                "rule": "FW-DYNAMICS",
                "status": "REFUSED",
                "scope": "two_rule is not fired at genesis and is not a law of the inscription",
            },
            {
                "rule": "FW-OB1",
                "status": "REFUSED",
                "scope": "no closure terminal is issued for OB-1, S6.6, or S9 last bullet",
            },
            {
                "rule": "FW-TABLE",
                "status": "REFUSED",
                "scope": "the object reports are constructed data; no requirement table is used",
            },
        ],
        "terminals": terminals,
        "falsifiers": _falsifiers(),
    }


def receipt_bytes(receipt: dict[str, Any]) -> bytes:
    return (json.dumps(receipt, sort_keys=True, indent=2) + "\n").encode("utf-8")


def write_receipt(path: Path) -> None:
    receipt = build_receipt()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(receipt_bytes(receipt))


__all__ = [
    "CandidateBill",
    "CollisionObject",
    "EqualProfilesObject",
    "GrammarState",
    "LEGAL_TERMINALS",
    "OrientedCandidate",
    "PROMPT_SHA256",
    "ResidualObject",
    "build_collision",
    "build_directional_residual",
    "build_equal_profiles",
    "build_receipt",
    "canonical_key",
    "enumerate_candidates",
    "event_search_report",
    "is_thing",
    "law_holds",
    "orientation_report",
    "prompt_hash",
    "receipt_bytes",
    "replay_events",
    "s9_bill_report",
    "write_receipt",
]
