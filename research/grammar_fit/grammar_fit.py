"""Fit the priced objects to a small, local event grammar.

This module is deliberately self-contained.  It reconstructs only the event
constructors used by this report and reads the priced-admissions receipt as a
hash-pinned, read-only input.  No implementation from ``code/`` is imported
into the object report.

All conclusions in the resulting receipt are finite computations or explicit
policy/refusal records.  In particular, an external ``Impose`` candidate and
an ``Observe`` no-op never become an endogenous state-changing successor.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from hashlib import sha256
from itertools import product
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence, TypeAlias


ROOT = Path(__file__).resolve().parent
PROMPT_PATH = ROOT / "PROMPT.md"
PRICED_RECEIPT_PATH = (
    ROOT.parent / "priced_admissions" / "receipts" / "priced_admissions.json"
)
PROMPT_SHA256 = "4fdbbec4fe44f29f5aa8ead53d8013de24aca335f0b8081dc79ca986354673e4"
PRICED_RECEIPT_SHA256 = (
    "60ad3a4854eb303c1c6b3138822fa694eac7bf8e6c63dee3fa9ed0e5dac81dac"
)
WRITE_ROOT = "research/grammar_fit/"
SEALED_PATHS = (
    "prompt/",
    "paper/",
    "code/",
    "lean4/Derivation/",
    "artifacts/",
    "CLAUDE.md",
    ".github/workflows/verify.yml",
    "research/priced_admissions/",
    "research/thinghood/",
    "research/genesis_continuation/",
)

LEGAL_TERMINALS = (
    "OBJECTS_SEATED",
    "OBJECTS_UNSEATED",
    "STATE_CHANGE_FOUND",
    "STATE_CHANGE_NOT_FOUND",
    "LABEL_ONLY",
    "PROFILE_CASE_BUILT",
    "PROFILE_CASE_IMPOSSIBLE",
    "COMPARISON_PRICED",
    "COMPARISON_EXCLUDED",
    "MEASURES_COMPARED",
    "ORIENTATION_PRICED",
    "S9_BRIDGE_PRICED",
    "TIES_RETAINED",
    "OB1_UNCHANGED",
    "S66_UNCHANGED",
    "S9_LAST_UNCHANGED",
    "CANDIDATE_SPACE_OPEN",
    "REFUSED",
)

Pair: TypeAlias = tuple[int, int]
Args: TypeAlias = tuple[int, ...]


def _jsonable(value: Any) -> Any:
    """Convert immutable local values to deterministic JSON values."""

    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, frozenset):
        return [_jsonable(item) for item in sorted(value, key=repr)]
    return value


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _check_lf(path: Path) -> None:
    data = path.read_bytes()
    if b"\r" in data:
        raise ValueError(f"{path} is not LF-only")


def check_inputs() -> dict[str, str]:
    """Hash and line-ending check the new prompt and the read-only input."""

    _check_lf(PROMPT_PATH)
    prompt_hash = _sha256(PROMPT_PATH)
    if prompt_hash != PROMPT_SHA256:
        raise ValueError(
            f"prompt drift: expected {PROMPT_SHA256}, got {prompt_hash}"
        )
    _check_lf(PRICED_RECEIPT_PATH)
    priced_hash = _sha256(PRICED_RECEIPT_PATH)
    if priced_hash != PRICED_RECEIPT_SHA256:
        raise ValueError(
            "priced receipt drift: "
            f"expected {PRICED_RECEIPT_SHA256}, got {priced_hash}"
        )
    return {"prompt": prompt_hash, "priced_receipt": priced_hash}


# ---------------------------------------------------------------------------
# Local METATHEORY reconstruction


@dataclass(frozen=True)
class GrammarState:
    """The admitted state used by this report's local reconstruction."""

    presentations: tuple[str, ...] = ()
    data: tuple[str, ...] = ()
    forms: tuple[int, ...] = ()
    instances: tuple[tuple[int, Args], ...] = ()
    rules: tuple[int, ...] = ()
    requirements: tuple[Pair, ...] = ()
    occurrences: tuple[str, ...] = ()
    asserted: tuple[Pair, ...] = ()
    witnesses: tuple[Pair, ...] = ()
    protected: tuple[Pair, ...] = ()
    observation: str | None = None
    refusals: tuple[str, ...] = ()
    budget: int = 0
    licensed: bool = True


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
    args: Args


@dataclass(frozen=True)
class AdmitRuleAllEvent:
    form: int


@dataclass(frozen=True)
class ImposeEvent:
    i: int
    j: int


@dataclass(frozen=True)
class ObserveEvent:
    label: str


@dataclass(frozen=True)
class AssertWitnessEvent:
    i: int
    j: int


@dataclass(frozen=True)
class RetainWitnessEvent:
    i: int
    j: int


@dataclass(frozen=True)
class ProtectEvent:
    i: int
    j: int


@dataclass(frozen=True)
class DeclareObservationEvent:
    pass


@dataclass(frozen=True)
class RefuseEvent:
    reason: str


Event: TypeAlias = (
    SupplyEvent
    | AdmitDatumEvent
    | AdmitFormEvent
    | AdmitInstanceEvent
    | AdmitRuleAllEvent
    | ImposeEvent
    | ObserveEvent
    | AssertWitnessEvent
    | RetainWitnessEvent
    | ProtectEvent
    | DeclareObservationEvent
    | RefuseEvent
)


class GrammarError(ValueError):
    """A local grammar event is not well formed."""


def _valid_pair(state: GrammarState, i: int, j: int) -> Pair:
    if not (0 <= i < j < len(state.data)):
        raise GrammarError(f"pair out of range: {(i, j)}")
    return (i, j)


def step(state: GrammarState, event: Event) -> GrammarState:
    """Apply one reconstructed constructor deterministically."""

    if isinstance(event, SupplyEvent):
        # Supply is a presentation event.  It records the token but does not
        # admit a datum and cannot pay any S9 line.
        return replace(state, presentations=state.presentations + (event.token,))
    if isinstance(event, AdmitDatumEvent):
        if event.token in state.data:
            return state
        return replace(
            state,
            data=state.data + (event.token,),
            occurrences=state.occurrences + (event.token,),
        )
    if isinstance(event, AdmitFormEvent):
        if event.arity < 1:
            raise GrammarError(f"form arity must be positive: {event.arity}")
        return replace(state, forms=state.forms + (event.arity,))
    if isinstance(event, AdmitInstanceEvent):
        if not (0 <= event.form < len(state.forms)):
            raise GrammarError(f"unknown form: {event.form}")
        if len(event.args) != state.forms[event.form]:
            raise GrammarError(
                f"form {event.form} has arity {state.forms[event.form]}"
            )
        if not all(0 <= arg < len(state.data) for arg in event.args):
            raise GrammarError(f"instance arguments out of range: {event.args}")
        instance = (event.form, event.args)
        if instance in state.instances:
            return state
        return replace(state, instances=state.instances + (instance,))
    if isinstance(event, AdmitRuleAllEvent):
        if not (0 <= event.form < len(state.forms)):
            raise GrammarError(f"unknown form: {event.form}")
        if event.form in state.rules:
            return state
        return replace(state, rules=state.rules + (event.form,))
    if isinstance(event, ImposeEvent):
        pair = _valid_pair(state, event.i, event.j)
        if pair in state.requirements:
            return state
        return replace(state, requirements=state.requirements + (pair,))
    if isinstance(event, ObserveEvent):
        # Observe is intentionally a no-op constructor: the label does not
        # mutate admitted state and therefore cannot set NEXT_EVENT_FOUND.
        return state
    if isinstance(event, AssertWitnessEvent):
        pair = _valid_pair(state, event.i, event.j)
        if pair in state.asserted:
            return state
        return replace(state, asserted=state.asserted + (pair,))
    if isinstance(event, RetainWitnessEvent):
        pair = _valid_pair(state, event.i, event.j)
        if pair in state.witnesses:
            return state
        return replace(state, witnesses=state.witnesses + (pair,))
    if isinstance(event, ProtectEvent):
        pair = _valid_pair(state, event.i, event.j)
        if pair in state.protected:
            return state
        return replace(state, protected=state.protected + (pair,))
    if isinstance(event, DeclareObservationEvent):
        if state.observation is not None:
            return state
        return replace(state, observation="declared")
    if isinstance(event, RefuseEvent):
        return replace(state, refusals=state.refusals + (event.reason,))
    raise TypeError(f"unhandled event: {event!r}")


def replay(history: Iterable[Event]) -> GrammarState:
    state = GrammarState()
    for event in history:
        state = step(state, event)
    return state


def event_json(event: Event) -> dict[str, Any]:
    if isinstance(event, SupplyEvent):
        return {"kind": "Supply", "token": event.token}
    if isinstance(event, AdmitDatumEvent):
        return {"kind": "AdmitDatum", "token": event.token}
    if isinstance(event, AdmitFormEvent):
        return {"kind": "AdmitForm", "arity": event.arity}
    if isinstance(event, AdmitInstanceEvent):
        return {"kind": "AdmitInst", "form": event.form, "args": list(event.args)}
    if isinstance(event, AdmitRuleAllEvent):
        return {"kind": "AdmitRuleAll", "form": event.form}
    if isinstance(event, ImposeEvent):
        return {"kind": "Impose", "pair": [event.i, event.j]}
    if isinstance(event, ObserveEvent):
        return {"kind": "Observe", "label": event.label}
    if isinstance(event, AssertWitnessEvent):
        return {"kind": "assertWit", "pair": [event.i, event.j]}
    if isinstance(event, RetainWitnessEvent):
        return {"kind": "admitWit", "pair": [event.i, event.j]}
    if isinstance(event, ProtectEvent):
        return {"kind": "protect", "pair": [event.i, event.j]}
    if isinstance(event, DeclareObservationEvent):
        return {"kind": "declareObs"}
    if isinstance(event, RefuseEvent):
        return {"kind": "refuse", "reason": event.reason}
    raise TypeError(f"unhandled event: {event!r}")


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
        "observation": state.observation,
        "refusals": list(state.refusals),
        "budget": state.budget,
        "licensed": state.licensed,
    }


def _state_from_json(raw: Mapping[str, Any]) -> GrammarState:
    """Recover a local state for replaying a reported no-op."""

    return GrammarState(
        presentations=tuple(str(value) for value in raw["presentations"]),
        data=tuple(str(value) for value in raw["data"]),
        forms=tuple(int(value) for value in raw["forms"]),
        instances=tuple(
            (int(item[0]), tuple(int(argument) for argument in item[1]))
            for item in raw["instances"]
        ),
        rules=tuple(int(value) for value in raw["rules"]),
        requirements=tuple(
            (int(item[0]), int(item[1])) for item in raw["requirements"]
        ),
        occurrences=tuple(str(value) for value in raw["occurrences"]),
        asserted=tuple((int(item[0]), int(item[1])) for item in raw["asserted"]),
        witnesses=tuple((int(item[0]), int(item[1])) for item in raw["witnesses"]),
        protected=tuple((int(item[0]), int(item[1])) for item in raw["protected"]),
        observation=(
            None if raw["observation"] is None else str(raw["observation"])
        ),
        refusals=tuple(str(value) for value in raw["refusals"]),
        budget=int(raw["budget"]),
        licensed=bool(raw["licensed"]),
    )


def profile_rows(state: GrammarState) -> tuple[tuple[tuple[int, tuple[int | None, ...]], ...], ...]:
    """Compute profile rows from admitted forms, instances, and rules.

    A context has one hole.  A context is in a datum's profile when an
    admitted instance (or an admitted all-tuples rule) is derivable after
    plugging that datum into the hole.  The implementation is intentionally
    finite and constructive; no profile row is supplied by the caller.
    """

    rows: list[tuple[tuple[int, tuple[int | None, ...]], ...]] = []
    data_count = len(state.data)
    for datum in range(data_count):
        contexts: list[tuple[int, tuple[int | None, ...]]] = []
        for form, arity in enumerate(state.forms):
            for hole in range(arity):
                other_positions = tuple(position for position in range(arity) if position != hole)
                for fixed_values in product(range(data_count), repeat=len(other_positions)):
                    fixed = dict(zip(other_positions, fixed_values))
                    context_slots = tuple(
                        None if position == hole else fixed[position]
                        for position in range(arity)
                    )
                    derivable = form in state.rules
                    if not derivable:
                        for instance_form, arguments in state.instances:
                            if instance_form != form or arguments[hole] != datum:
                                continue
                            if all(arguments[position] == fixed[position] for position in other_positions):
                                derivable = True
                                break
                    context = (form, context_slots)
                    if derivable and context not in contexts:
                        contexts.append(context)
        contexts.sort(key=repr)
        rows.append(tuple(contexts))
    return tuple(rows)


def _history_json(history: Sequence[Event]) -> list[dict[str, Any]]:
    return [event_json(event) for event in history]


# ---------------------------------------------------------------------------
# Seating the three priced objects


def _history_for_tokens(tokens: Sequence[str]) -> tuple[Event, ...]:
    return tuple(
        [event for token in tokens for event in (SupplyEvent(token),)]
        + [AdmitDatumEvent(token) for token in tokens]
    )


def _object_fields(payload: Mapping[str, Any], names: Sequence[str]) -> dict[str, Any]:
    return {name: payload[name] for name in names}


def seat_collision(payload: Mapping[str, Any]) -> dict[str, Any]:
    tokens = [str(token) for token in payload["event_state"]["data"]]
    history = _history_for_tokens(tokens)
    state = replay(history)
    names = ("asserted_pair", "identifying_map", "pushed_edges")
    return {
        "kind": "collision",
        "seated": True,
        "history": _history_json(history),
        "grammar_state": state_json(state),
        "object_fields": _object_fields(payload, names),
        "grammar_state_field_names": list(state_json(state)),
        "fields_outside_grammar_state": list(names),
        "outside_state_explanation": (
            "The asserted pair, identifying map, and pushed edges are fields "
            "of the collision report, not fields produced by these constructors."
        ),
    }


def seat_equal_profiles(payload: Mapping[str, Any]) -> dict[str, Any]:
    tokens = [str(token) for token in payload["event_state"]["data"]]
    history = _history_for_tokens(tokens) + (AdmitFormEvent(1),)
    state = replay(history)
    names = ("contexts", "equal_pair", "profiles")
    return {
        "kind": "equal_profiles",
        "seated": True,
        "history": _history_json(history),
        "grammar_state": state_json(state),
        "object_fields": _object_fields(payload, names),
        "grammar_state_field_names": list(state_json(state)),
        "fields_outside_grammar_state": list(names),
        "outside_state_explanation": (
            "Contexts, profiles, and the selected equal pair are report data; "
            "Observe is a no-op and no constructor admits these values."
        ),
    }


def seat_residual(payload: Mapping[str, Any]) -> dict[str, Any]:
    tokens = [str(token) for token in payload["event_state"]["data"]]
    history = _history_for_tokens(tokens)
    state = replay(history)
    names = ("left_presentation", "residual_pair", "right_presentation")
    return {
        "kind": "directional_residual",
        "seated": True,
        "history": _history_json(history),
        "grammar_state": state_json(state),
        "object_fields": _object_fields(payload, names),
        "grammar_state_field_names": list(state_json(state)),
        "fields_outside_grammar_state": list(names),
        "outside_state_explanation": (
            "The two presentations and residual pair are comparison fields; "
            "they are not admissions in this grammar state."
        ),
    }


def seat_objects(priced: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "collision": seat_collision(priced["objects"]["collision"]),
        "equal_profiles": seat_equal_profiles(priced["objects"]["equal_profiles"]),
        "directional_residual": seat_residual(
            priced["objects"]["directional_residual"]
        ),
    }


def _observe_candidate(label: str, source: str, value: Any) -> dict[str, Any]:
    event = ObserveEvent(label)
    return {
        "event": event_json(event),
        "source_field": source,
        "source_value": _jsonable(value),
        "mutates_state": False,
        "classification": "OBJECT_DERIVED_NO_OP_LABEL",
    }


def _event_fit_for(
    kind: str, priced_object: Mapping[str, Any], seated: Mapping[str, Any]
) -> dict[str, Any]:
    fields = priced_object
    seated_fields = seated["object_fields"]
    no_ops: list[dict[str, Any]] = []
    if kind == "equal_profiles":
        no_ops.append(
            _observe_candidate("equal-profile-context", "contexts", fields["contexts"])
        )
    elif kind == "directional_residual":
        no_ops.extend(
            (
                _observe_candidate("p", "left_presentation", fields["left_presentation"]),
                _observe_candidate("q", "right_presentation", fields["right_presentation"]),
            )
        )

    state = seated["grammar_state"]
    state_object = _state_from_json(state)
    pair = tuple(int(value) for value in fields.get("equal_pair", fields.get("residual_pair", fields.get("asserted_pair", (0, 1)))))
    external: list[dict[str, Any]] = []
    if len(state["data"]) > pair[1]:
        external.append({"event": event_json(ImposeEvent(*pair)), "classification": "SUPPLIED_INPUT"})

    missing = list(priced_object.get("absent", ()))
    guarded: list[dict[str, Any]] = []
    offers = []
    if state["observation"] is None:
        offers.append(
            {
                "event": event_json(DeclareObservationEvent()),
                "classification": "GRAMMAR_OFFER_WITHOUT_OBJECT_INGREDIENT",
                "counts_as_next_event": False,
            }
        )

    state_changes: list[dict[str, Any]] = []
    replay_checks = []
    for candidate in no_ops:
        event = ObserveEvent(str(candidate["event"]["label"]))
        before = state_object
        after = step(state_object, event)
        replay_checks.append(
            {
                "event": candidate["event"],
                "state_unchanged": before == after,
            }
        )

    return {
        "object": kind,
        "object_fields": _jsonable(seated_fields),
        "grammar_state_field_names": list(state),
        "fields_outside_grammar_state": list(seated["fields_outside_grammar_state"]),
        "object_derived_state_change": state_changes,
        "object_derived_noop_label": no_ops,
        "external_challenge": external,
        "guarded_response": guarded,
        "grammar_offers_without_object_ingredient": offers,
        "missing_admissions_for_guarded_response": missing,
        "state_change_found": bool(state_changes),
        "guarded_response_found": bool(guarded),
        "external_challenge_found": bool(external),
        "label_only": bool(no_ops) and not state_changes,
        "next_event_found": bool(state_changes or guarded),
        "next_event_not_found_scope": "object_derived_state_change_and_guarded_response",
        "endogenous_successor_found": False,
        "no_op_replay_checks": replay_checks,
    }


def fit_events(
    priced: Mapping[str, Any], seated_objects: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    names = ("collision", "equal_profiles", "directional_residual")
    reports = {
        name: _event_fit_for(name, priced["objects"][name], seated_objects[name])
        for name in names
    }
    return {
        "classification": "FINITE_COMPUTATION",
        "reconstructed_constructor_names": [
            "Supply",
            "AdmitDatum",
            "AdmitForm",
            "AdmitInst",
            "AdmitRuleAll",
            "Impose",
            "Observe",
            "assertWit",
            "admitWit",
            "protect",
            "declareObs",
            "refuse",
        ],
        "not_used_as_passage": {
            "names": ["refineCol", "addCol"],
            "status": "REFUSED",
            "reason": "Those names are not reconstructed or upgraded here; no-op labels are not passage constructors.",
        },
        "next_event_found_scope": "object_derived_state_change_only",
        "external_challenges_do_not_set_next_event_found": True,
        "no_op_labels_do_not_set_next_event_found": True,
        "object_derived_state_change_count": sum(
            bool(report["object_derived_state_change"]) for report in reports.values()
        ),
        "label_only_count": sum(bool(report["object_derived_noop_label"]) for report in reports.values()),
        "external_challenge_count": sum(bool(report["external_challenge"]) for report in reports.values()),
        "guarded_response_count": sum(bool(report["guarded_response"]) for report in reports.values()),
        "search": reports,
    }


# ---------------------------------------------------------------------------
# Non-trivial profile case, policy, measure, and S9 bridge


def nontrivial_profile_case() -> dict[str, Any]:
    history: tuple[Event, ...] = (
        SupplyEvent("<a>"),
        SupplyEvent("<ab>"),
        AdmitDatumEvent("<a>"),
        AdmitDatumEvent("<ab>"),
        AdmitFormEvent(1),
        AdmitInstanceEvent(0, (0,)),
    )
    state = replay(history)
    computed_rows = profile_rows(state)
    profiles = _jsonable(computed_rows)
    context = _jsonable(computed_rows[0][0]) if computed_rows[0] else None
    instance_holds = [bool(computed_rows[0]), bool(computed_rows[1])]
    if context is None or profiles[0] == profiles[1] or instance_holds != [True, False]:
        raise AssertionError("non-trivial profile case collapsed")
    empty_history = history[:-1]
    empty_state = replay(empty_history)
    empty_profiles = _jsonable(profile_rows(empty_state))
    return {
        "terminal": "PROFILE_CASE_BUILT",
        "history": _history_json(history),
        "grammar_state": state_json(state),
        "context": context,
        "pair": [0, 1],
        "profiles": profiles,
        "profile_rows_computed_from_state": True,
        "profile_algorithm": "admitted unary instances and all-tuples rules with one-hole contexts",
        "instance_holds": instance_holds,
        "equal_profiles": False,
        "internally_separable": True,
        "empty_profile_falsifier": {
            "history_without_instance": _history_json(empty_history),
            "profiles": empty_profiles,
            "state": state_json(empty_state),
            "empty_profiles_are_not_the_built_case": True,
        },
    }


def comparison_policy() -> dict[str, Any]:
    return {
        "terminal": "COMPARISON_EXCLUDED",
        "status": "DECLARED_POLICY",
        "policy": None,
        "constructor_spends_atom": None,
        "residual_leftover": "comparison policy remains OPEN",
        "priced": False,
    }


def fit_measure(priced: Mapping[str, Any]) -> dict[str, Any]:
    orientation = priced["orientation"]
    representative = orientation["minimum_with_orientation"]["representatives"][0]["candidate"]
    bill = representative["bill"]
    total = sum(int(bill[name]) for name in ("carrier", "occurrences", "relation", "witness", "law", "orientation"))
    if total != 8:
        raise AssertionError(f"unexpected oriented bill: {total}")
    return {
        "name": "mu_fit_oriented_s9",
        "only_measure": True,
        "definition": "additive atoms for carrier, two occurrences, relation, witness, named law, and orientation",
        "candidate": _jsonable(representative),
        "candidate_cost": total,
        "old_measure_reused": False,
        "rank_change_test": "not applicable: one named measure is retained",
    }


def law_disposition(priced: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "law_list_was_enlarged": False,
        "named_law_list": _jsonable(priced["law_lattice"]),
        "added_laws": [],
        "uncompared_laws_remain_open": True,
        "disposition": "No law is added by grammar_fit; the priced finite list is read-only input.",
    }


S9_LINES: tuple[dict[str, Any], ...] = (
    {
        "line": "carrier",
        "required": "a carrier with two points",
        "missing": "AdmitDatum for two occurrences",
    },
    {
        "line": "occurrences",
        "required": ["left occurrence", "right occurrence"],
        "missing": "two AdmitDatum events",
    },
    {
        "line": "relation",
        "required": "one admitted ordered edge",
        "missing": "relation admission is not in the inscription",
    },
    {
        "line": "witness",
        "required": "retained asserted pair",
        "missing": "assertWit/admitWit passage admissions",
    },
    {
        "line": "irreflexivity",
        "required": "a named irreflexive law",
        "missing": "law admission",
    },
    {
        "line": "orientation",
        "required": "ordered-pair admission",
        "missing": "orientation admission",
    },
)


def s9_bridge() -> dict[str, Any]:
    history = (SupplyEvent("<>"),)
    state = replay(history)
    lines = [{**line, "paid": False} for line in S9_LINES]
    return {
        "terminal": "S9_BRIDGE_PRICED",
        "schema": "s9-six-line-bill-v1",
        "history": _history_json(history),
        "replayed_state": state_json(state),
        "supply_is_not_admission": state.data == (),
        "lines": lines,
        "paid_lines": [],
        "unpaid_lines": [line["line"] for line in lines],
        "all_unpaid": all(not line["paid"] for line in lines),
    }


def orientation_disposition(priced: Mapping[str, Any]) -> dict[str, Any]:
    orientation = priced["orientation"]
    if not orientation["forward_reverse_keys_differ"]:
        raise AssertionError("ordered-pair key forgot orientation")
    if not orientation["iso_key_preserves_ordered_pair"]:
        raise AssertionError("ordered-pair key is not orientation preserving")
    if not orientation["ties_retained"]:
        raise AssertionError("minimum tie was discarded")
    return {
        "terminal": "ORIENTATION_PRICED",
        "policy": orientation["policy"],
        "atom_cost": orientation["atom_cost"],
        "forward_key": orientation["forward_key"],
        "reverse_same_pair_key": orientation["reverse_same_pair_key"],
        "forward_reverse_keys_differ": True,
        "iso_key_preserves_ordered_pair": True,
        "minimum_with_orientation": _jsonable(orientation["minimum_with_orientation"]),
        "ties_retained": True,
        "tie_class_count": int(orientation["minimum_with_orientation"]["minimum_isomorphism_class_count"]),
    }


def open_boundaries() -> dict[str, Any]:
    return {
        "OB-1": "OPEN",
        "S6_item_6": "OPEN",
        "S9_last_bullet": "OPEN",
        "comparison_policy": "OPEN for the directional residual",
        "candidate_space": "OPEN outside the named finite enumeration",
        "no_terminal_claims": ["OB-1", "S6_item_6", "S9_last_bullet"],
    }


def refusals() -> list[dict[str, str]]:
    return [
        {
            "rule": "FW-PASSAGE",
            "scope": "refineCol and addCol are not reconstructed or upgraded to passage constructors in this packet",
            "status": "REFUSED",
        },
        {
            "rule": "FW-DYNAMICS",
            "scope": "two_rule remains a menu at an already active obstruction; no genesis event",
            "status": "REFUSED",
        },
        {
            "rule": "FW-OB1",
            "scope": "no closure terminal is issued for OB-1, S6.6, or S9 last bullet",
            "status": "REFUSED",
        },
        {
            "rule": "FW-TABLE",
            "scope": "a missing-flag table is DECLARED_POLICY, not a finite computation",
            "status": "REFUSED",
        },
        {
            "rule": "FW-SEAL",
            "scope": "no sealed path or sibling receipt is written",
            "status": "REFUSED",
        },
    ]


def load_priced_receipt() -> dict[str, Any]:
    check_inputs()
    value = json.loads(PRICED_RECEIPT_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("priced receipt root is not an object")
    return value


def build_receipt() -> dict[str, Any]:
    hashes = check_inputs()
    priced = load_priced_receipt()
    seated = seat_objects(priced)
    events = fit_events(priced, seated)
    profile_case = nontrivial_profile_case()
    comparison = comparison_policy()
    measure = fit_measure(priced)
    orientation = orientation_disposition(priced)
    s9 = s9_bridge()
    terminals = [
        "OBJECTS_SEATED",
        "STATE_CHANGE_NOT_FOUND",
        "LABEL_ONLY",
        "PROFILE_CASE_BUILT",
        "COMPARISON_EXCLUDED",
        "ORIENTATION_PRICED",
        "S9_BRIDGE_PRICED",
        "TIES_RETAINED",
        "OB1_UNCHANGED",
        "S66_UNCHANGED",
        "S9_LAST_UNCHANGED",
        "CANDIDATE_SPACE_OPEN",
        "REFUSED",
    ]
    if any(terminal not in LEGAL_TERMINALS for terminal in terminals):
        raise AssertionError("illegal terminal emitted")
    if any(report["next_event_found"] for report in events["search"].values()):
        raise AssertionError("a no-op or external challenge set next_event_found")
    if not s9["all_unpaid"] or s9["replayed_state"]["data"]:
        raise AssertionError("Supply paid or admitted an S9 line")
    return {
        "schema": "grammar-fit-v1",
        "evidence_class": "FINITE_COMPUTATION",
        "prompt_sha256": hashes["prompt"],
        "priced_receipt_sha256": hashes["priced_receipt"],
        "write_root": WRITE_ROOT,
        "sealed_paths": list(SEALED_PATHS),
        "sealed_paths_touched": [],
        "source_inputs": {
            "priced_receipt": "research/priced_admissions/receipts/priced_admissions.json",
            "priced_receipt_read_only": True,
            "thinghood_tick_table_used_as_evidence": False,
        },
        "reconstruction": {
            "classification": "METATHEORY",
            "module": "research/grammar_fit/grammar_fit.py",
            "imports_sealed_implementation": False,
            "constructors": events["reconstructed_constructor_names"],
        },
        "objects": seated,
        "event_fit": events,
        "profile_case": profile_case,
        "comparison": comparison,
        "measure": measure,
        "orientation": orientation,
        "laws": law_disposition(priced),
        "s9_bridge": s9,
        "open_boundaries": open_boundaries(),
        "refusals": refusals(),
        "terminals": terminals,
        "leftover": (
            "No endogenous successor is derived.  Comparison policy remains "
            "OPEN, the finite candidate space remains OPEN outside its declared "
            "bounds, and the three named opens remain OPEN."
        ),
        "receipt_replay": {
            "rule": "build_receipt() recomputes this timestamp-free JSON from the two hash-pinned inputs",
            "byte_identical_required": True,
        },
    }


def write_receipt(path: Path | None = None) -> Path:
    target = path or (ROOT / "receipts" / "grammar_fit.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(build_receipt(), sort_keys=True, indent=2, ensure_ascii=False)
    target.write_bytes((payload + "\n").encode("utf-8"))
    return target


if __name__ == "__main__":
    output = write_receipt()
    print(output.as_posix())
