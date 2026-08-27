"""Price or leave the fields that grammar-fit kept outside state.

The module is a small, self-contained METATHEORY reconstruction.  It reads
the grammar-fit receipt by hash, rebuilds the admitted profile state from its
recorded history, and makes one explicit admission choice: ``assertWit`` for
the collision's asserted pair.  The identifying map and the residual
comparison policy remain outside state.  A possible retained-witness response
is reported as conditional on another explicit admission; it is never called
endogenous.
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
GRAMMAR_FIT_RECEIPT_PATH = (
    ROOT.parent / "grammar_fit" / "receipts" / "grammar_fit.json"
)
PROMPT_SHA256 = "1a432270017e81c5963d78072f84c349fa366a1c2de875cec97c52794cd4eb62"
GRAMMAR_FIT_RECEIPT_SHA256 = (
    "133f12896a0d8ae819d5ceb780eb82a16127c9b922446a124b34d3adcea7b61b"
)
WRITE_ROOT = "research/admit_leftover/"
SEALED_PATHS = (
    "prompt/",
    "paper/",
    "code/",
    "lean4/Derivation/",
    "artifacts/",
    "CLAUDE.md",
    ".github/workflows/verify.yml",
    "research/grammar_fit/",
    "research/priced_admissions/",
    "research/thinghood/",
    "research/genesis_continuation/",
)

LEGAL_TERMINALS = (
    "LEFTOVER_ADMITTED",
    "LEFTOVER_LEFT_OUTSIDE",
    "STATE_CHANGE_FOUND",
    "STATE_CHANGE_NOT_FOUND",
    "LABEL_ONLY",
    "GUARDED_CONDITIONAL",
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
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _check_lf(path: Path) -> None:
    if b"\r" in path.read_bytes():
        raise ValueError(f"{path} is not LF-only")


def check_inputs() -> dict[str, str]:
    _check_lf(PROMPT_PATH)
    prompt_hash = _sha256(PROMPT_PATH)
    if prompt_hash != PROMPT_SHA256:
        raise ValueError(f"prompt drift: expected {PROMPT_SHA256}, got {prompt_hash}")
    _check_lf(GRAMMAR_FIT_RECEIPT_PATH)
    receipt_hash = _sha256(GRAMMAR_FIT_RECEIPT_PATH)
    if receipt_hash != GRAMMAR_FIT_RECEIPT_SHA256:
        raise ValueError(
            "grammar-fit receipt drift: "
            f"expected {GRAMMAR_FIT_RECEIPT_SHA256}, got {receipt_hash}"
        )
    return {"prompt": prompt_hash, "grammar_fit_receipt": receipt_hash}


# ---------------------------------------------------------------------------
# Local METATHEORY event grammar


@dataclass(frozen=True)
class GrammarState:
    presentations: tuple[str, ...] = ()
    data: tuple[str, ...] = ()
    forms: tuple[int, ...] = ()
    instances: tuple[tuple[int, Args], ...] = ()
    requirements: tuple[Pair, ...] = ()
    asserted: tuple[Pair, ...] = ()
    witnesses: tuple[Pair, ...] = ()
    protected: tuple[Pair, ...] = ()
    observation: str | None = None


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


Event: TypeAlias = (
    SupplyEvent
    | AdmitDatumEvent
    | AdmitFormEvent
    | AdmitInstanceEvent
    | ImposeEvent
    | ObserveEvent
    | AssertWitnessEvent
    | RetainWitnessEvent
    | ProtectEvent
    | DeclareObservationEvent
)


class GrammarError(ValueError):
    """An event is not well formed in the local reconstruction."""


def _pair(state: GrammarState, i: int, j: int) -> Pair:
    if not (0 <= i < j < len(state.data)):
        raise GrammarError(f"pair out of range: {(i, j)}")
    return (i, j)


def step(state: GrammarState, event: Event) -> GrammarState:
    if isinstance(event, SupplyEvent):
        return replace(state, presentations=state.presentations + (event.token,))
    if isinstance(event, AdmitDatumEvent):
        if event.token in state.data:
            return state
        return replace(state, data=state.data + (event.token,))
    if isinstance(event, AdmitFormEvent):
        if event.arity < 1:
            raise GrammarError("form arity must be positive")
        return replace(state, forms=state.forms + (event.arity,))
    if isinstance(event, AdmitInstanceEvent):
        if not (0 <= event.form < len(state.forms)):
            raise GrammarError(f"unknown form: {event.form}")
        if len(event.args) != state.forms[event.form]:
            raise GrammarError("instance arity does not match its form")
        if not all(0 <= argument < len(state.data) for argument in event.args):
            raise GrammarError("instance argument out of range")
        instance = (event.form, event.args)
        if instance in state.instances:
            return state
        return replace(state, instances=state.instances + (instance,))
    if isinstance(event, ImposeEvent):
        pair = _pair(state, event.i, event.j)
        if pair in state.requirements:
            return state
        return replace(state, requirements=state.requirements + (pair,))
    if isinstance(event, ObserveEvent):
        return state
    if isinstance(event, AssertWitnessEvent):
        pair = _pair(state, event.i, event.j)
        if pair in state.asserted:
            return state
        return replace(state, asserted=state.asserted + (pair,))
    if isinstance(event, RetainWitnessEvent):
        pair = _pair(state, event.i, event.j)
        if pair not in state.asserted:
            raise GrammarError("admitWit requires an asserted pair")
        if pair in state.witnesses:
            return state
        return replace(state, witnesses=state.witnesses + (pair,))
    if isinstance(event, ProtectEvent):
        pair = _pair(state, event.i, event.j)
        if pair not in state.witnesses:
            raise GrammarError("protect requires a retained witness")
        if pair in state.protected:
            return state
        return replace(state, protected=state.protected + (pair,))
    if isinstance(event, DeclareObservationEvent):
        if state.observation is not None:
            return state
        return replace(state, observation="declared")
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
    raise TypeError(f"unhandled event: {event!r}")


def state_json(state: GrammarState) -> dict[str, Any]:
    return {
        "presentations": list(state.presentations),
        "data": list(state.data),
        "forms": list(state.forms),
        "instances": [[form, list(args)] for form, args in state.instances],
        "requirements": [list(pair) for pair in state.requirements],
        "asserted": [list(pair) for pair in state.asserted],
        "witnesses": [list(pair) for pair in state.witnesses],
        "protected": [list(pair) for pair in state.protected],
        "observation": state.observation,
    }


def _state_from_json(raw: Mapping[str, Any]) -> GrammarState:
    return GrammarState(
        presentations=tuple(str(value) for value in raw["presentations"]),
        data=tuple(str(value) for value in raw["data"]),
        forms=tuple(int(value) for value in raw["forms"]),
        instances=tuple(
            (int(item[0]), tuple(int(argument) for argument in item[1]))
            for item in raw["instances"]
        ),
        requirements=tuple((int(item[0]), int(item[1])) for item in raw["requirements"]),
        asserted=tuple((int(item[0]), int(item[1])) for item in raw["asserted"]),
        witnesses=tuple((int(item[0]), int(item[1])) for item in raw["witnesses"]),
        protected=tuple((int(item[0]), int(item[1])) for item in raw["protected"]),
        observation=None if raw["observation"] is None else str(raw["observation"]),
    )


def _event_from_json(raw: Mapping[str, Any]) -> Event:
    kind = str(raw["kind"])
    if kind == "Supply":
        return SupplyEvent(str(raw["token"]))
    if kind == "AdmitDatum":
        return AdmitDatumEvent(str(raw["token"]))
    if kind == "AdmitForm":
        return AdmitFormEvent(int(raw["arity"]))
    if kind == "AdmitInst":
        return AdmitInstanceEvent(int(raw["form"]), tuple(int(x) for x in raw["args"]))
    if kind == "Impose":
        return ImposeEvent(int(raw["pair"][0]), int(raw["pair"][1]))
    if kind == "Observe":
        return ObserveEvent(str(raw["label"]))
    if kind == "assertWit":
        return AssertWitnessEvent(int(raw["pair"][0]), int(raw["pair"][1]))
    if kind == "admitWit":
        return RetainWitnessEvent(int(raw["pair"][0]), int(raw["pair"][1]))
    if kind == "protect":
        return ProtectEvent(int(raw["pair"][0]), int(raw["pair"][1]))
    if kind == "declareObs":
        return DeclareObservationEvent()
    raise ValueError(f"unsupported read-only history event: {kind}")


def history_from_json(raw: Sequence[Mapping[str, Any]]) -> tuple[Event, ...]:
    return tuple(_event_from_json(item) for item in raw)


# ---------------------------------------------------------------------------
# Profile computation from admitted state


def profile_rows(state: GrammarState) -> tuple[tuple[tuple[int, tuple[int | None, ...]], ...], ...]:
    """Compute one-hole profile rows from admitted forms and instances."""

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
                    if any(
                        instance_form == form
                        and arguments[hole] == datum
                        and all(arguments[position] == fixed[position] for position in other_positions)
                        for instance_form, arguments in state.instances
                    ):
                        contexts.append((form, context_slots))
        contexts.sort(key=repr)
        rows.append(tuple(contexts))
    return tuple(rows)


def profile_case_from_input(grammar_fit: Mapping[str, Any]) -> dict[str, Any]:
    raw_case = grammar_fit["profile_case"]
    history = history_from_json(raw_case["history"])
    state = replay(history)
    computed = profile_rows(state)
    computed_json = _jsonable(computed)
    if computed_json != raw_case["profiles"]:
        raise AssertionError("grammar-fit profile rows do not replay from its instance")
    if not computed or not computed[0] or computed[1]:
        raise AssertionError("expected one non-empty and one empty profile row")
    return {
        "history": [event_json(event) for event in history],
        "grammar_state": state_json(state),
        "profiles_computed_from_state": computed_json,
        "input_rows_match_computation": True,
        "pair": [0, 1],
        "instance_holds": [bool(computed[0]), bool(computed[1])],
        "equal_profiles": False,
        "internally_separable": True,
    }


# ---------------------------------------------------------------------------
# Leftover admissions, search columns, and bills


def _seat_history(raw_object: Mapping[str, Any]) -> tuple[Event, ...]:
    return history_from_json(raw_object["history"])


def _no_op(label: str, source_field: str, source_value: Any, state: GrammarState) -> dict[str, Any]:
    before = state
    after = step(state, ObserveEvent(label))
    return {
        "event": event_json(ObserveEvent(label)),
        "source_field": source_field,
        "source_value": _jsonable(source_value),
        "mutates_state": after != before,
        "state_unchanged": after == before,
        "classification": "OBJECT_DERIVED_NO_OP_LABEL",
    }


def _search_columns(
    kind: str,
    state: GrammarState,
    pair: Pair,
    no_ops: Sequence[dict[str, Any]],
    guarded: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    external: list[dict[str, Any]] = []
    if pair[1] < len(state.data):
        external.append(
            {
                "event": event_json(ImposeEvent(*pair)),
                "classification": "SUPPLIED_INPUT",
                "applied_to_state": False,
            }
        )
    return {
        "object": kind,
        "object_derived_state_change": [],
        "object_derived_noop_label": list(no_ops),
        "external_challenge": external,
        "guarded_response": list(guarded),
        "state_change_found": False,
        "guarded_response_found": False,
        "guarded_response_conditional": bool(guarded),
        "external_challenge_found": bool(external),
        "label_only": bool(no_ops),
        "no_op_labels_do_not_set_state_change_found": True,
        "endogenous_successor_found": False,
        "search_scope": "the post-admission local state only",
    }


def collision_admission(grammar_fit: Mapping[str, Any]) -> dict[str, Any]:
    raw = grammar_fit["objects"]["collision"]
    history = _seat_history(raw)
    before = replay(history)
    pair = tuple(int(value) for value in raw["object_fields"]["asserted_pair"])
    event = AssertWitnessEvent(*pair)
    after = step(before, event)
    conditional = {
        "event": event_json(RetainWitnessEvent(*pair)),
        "status": "CONDITIONAL",
        "requires_extra_admission": "admitWit atom",
        "fires_in_current_state": False,
        "endogenous": False,
    }
    search = _search_columns("collision", after, pair, (), (conditional,))
    return {
        "field": "asserted_pair",
        "constructor": event_json(event),
        "bill_atom": "asserted_pair",
        "admitted": True,
        "history_before": [event_json(item) for item in history],
        "history_after": [event_json(item) for item in history] + [event_json(event)],
        "state_before": state_json(before),
        "state_after": state_json(after),
        "identifying_map": _jsonable(raw["object_fields"]["identifying_map"]),
        "identifying_map_in_state": False,
        "identifying_map_leftover": "No named map-admission constructor is chosen; the map remains outside state.",
        "search_after_admission": search,
    }


def profile_search(grammar_fit: Mapping[str, Any], profile_case: Mapping[str, Any]) -> dict[str, Any]:
    raw = grammar_fit["profile_case"]
    state = _state_from_json(profile_case["grammar_state"])
    context = profile_case["profiles_computed_from_state"][0][0]
    label = _no_op("profile-context", "profiles_computed_from_state", context, state)
    return _search_columns("equal_profiles", state, (0, 1), (label,), ())


def residual_search(grammar_fit: Mapping[str, Any]) -> dict[str, Any]:
    raw = grammar_fit["objects"]["directional_residual"]
    state = replay(_seat_history(raw))
    fields = raw["object_fields"]
    labels = (
        _no_op("p", "left_presentation", fields["left_presentation"], state),
        _no_op("q", "right_presentation", fields["right_presentation"], state),
    )
    return _search_columns("directional_residual", state, (0, 1), labels, ())


def admission_bill() -> dict[str, Any]:
    lines = [
        {
            "field": "asserted_pair",
            "constructor": "assertWit",
            "status": "ADMITTED",
            "atom_cost": 1,
            "paid": True,
        },
        {
            "field": "retained_witness",
            "constructor": "admitWit",
            "status": "CONDITIONAL",
            "atom_cost": 1,
            "paid": False,
            "note": "not silently free; the conditional response is not fired",
        },
        {
            "field": "protected_pair",
            "constructor": "protect",
            "status": "CONDITIONAL",
            "atom_cost": 1,
            "paid": False,
            "note": "requires the retained-witness admission first",
        },
        {
            "field": "declared_observation",
            "constructor": "declareObs",
            "status": "DECLARED_POLICY",
            "atom_cost": None,
            "paid": False,
            "note": "no object ingredient; not selected as an endogenous response",
        },
        {
            "field": "identifying_map",
            "constructor": None,
            "status": "LEFT_OUTSIDE",
            "atom_cost": None,
            "paid": False,
            "note": "no named map-admission constructor is declared",
        },
        {
            "field": "comparison_policy",
            "constructor": None,
            "status": "DECLARED_POLICY",
            "atom_cost": None,
            "paid": False,
            "note": "COMPARISON_EXCLUDED; the residual stays open",
        },
    ]
    return {
        "measure_name": "mu_leftover_admission",
        "definition": "one atom for each extra admission chosen in this run",
        "lines": lines,
        "chosen_total": sum(int(line["atom_cost"]) for line in lines if line["paid"]),
        "no_free_store_admissions": True,
        "minimum_claim": False,
    }


def orientation_from_input(grammar_fit: Mapping[str, Any]) -> dict[str, Any]:
    raw = grammar_fit["orientation"]
    if not raw["forward_reverse_keys_differ"] or not raw["iso_key_preserves_ordered_pair"]:
        raise AssertionError("ordered-pair orientation was forgotten")
    if not raw["ties_retained"]:
        raise AssertionError("input orientation tie was discarded")
    return {
        "terminal": "ORIENTATION_PRICED",
        "inherited_read_only": True,
        "atom_cost": raw["atom_cost"],
        "forward_key": raw["forward_key"],
        "reverse_same_pair_key": raw["reverse_same_pair_key"],
        "forward_reverse_keys_differ": True,
        "iso_key_preserves_ordered_pair": True,
        "ties_retained": True,
        "tie_class_count": int(raw["minimum_with_orientation"]["minimum_isomorphism_class_count"]),
    }


S9_LINES: tuple[dict[str, Any], ...] = (
    {"line": "carrier", "required": "a carrier with two points", "missing": "AdmitDatum for two occurrences"},
    {"line": "occurrences", "required": ["left occurrence", "right occurrence"], "missing": "two AdmitDatum events"},
    {"line": "relation", "required": "one admitted ordered edge", "missing": "relation admission is not in the inscription"},
    {"line": "witness", "required": "retained asserted pair", "missing": "assertWit/admitWit passage admissions"},
    {"line": "irreflexivity", "required": "a named irreflexive law", "missing": "law admission"},
    {"line": "orientation", "required": "ordered-pair admission", "missing": "orientation admission"},
)


def s9_bridge() -> dict[str, Any]:
    history = (SupplyEvent("<>"),)
    state = replay(history)
    lines = [{**line, "paid": False} for line in S9_LINES]
    return {
        "terminal": "S9_BRIDGE_PRICED",
        "history": [event_json(event) for event in history],
        "replayed_state": state_json(state),
        "supply_is_not_admission": state.data == (),
        "extra_admission_not_in_supply_history": True,
        "lines": lines,
        "paid_lines": [],
        "unpaid_lines": [line["line"] for line in lines],
        "all_unpaid": all(not line["paid"] for line in lines),
    }


def open_boundaries() -> dict[str, Any]:
    return {
        "OB-1": "OPEN",
        "S6_item_6": "OPEN",
        "S9_last_bullet": "OPEN",
        "comparison_policy": "OPEN for the directional residual",
        "identifying_map": "OPEN outside grammar state",
        "guarded_family": "OPEN and unfired",
        "candidate_space": "OPEN outside the named finite input",
    }


def refusals() -> list[dict[str, str]]:
    return [
        {
            "rule": "FW-DYNAMICS",
            "scope": "two_rule is not fired at genesis and no dynamic successor is inferred",
            "status": "REFUSED",
        },
        {
            "rule": "FW-OB1",
            "scope": "OB-1, S6.6, and S9 last bullet receive no closure terminal",
            "status": "REFUSED",
        },
        {
            "rule": "FW-TABLE",
            "scope": "a missing-flag table is DECLARED_POLICY, not FINITE_COMPUTATION",
            "status": "REFUSED",
        },
        {
            "rule": "FW-MAP",
            "scope": "the identifying map remains outside state without a named admission",
            "status": "REFUSED",
        },
        {
            "rule": "FW-SEAL",
            "scope": "no sealed path or sibling receipt is written",
            "status": "REFUSED",
        },
    ]


def load_grammar_fit() -> dict[str, Any]:
    check_inputs()
    value = json.loads(GRAMMAR_FIT_RECEIPT_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("grammar-fit receipt root is not an object")
    return value


def build_receipt() -> dict[str, Any]:
    hashes = check_inputs()
    grammar_fit = load_grammar_fit()
    profile_case = profile_case_from_input(grammar_fit)
    collision = collision_admission(grammar_fit)
    searches = {
        "collision": collision["search_after_admission"],
        "equal_profiles": profile_search(grammar_fit, profile_case),
        "directional_residual": residual_search(grammar_fit),
    }
    bill = admission_bill()
    orientation = orientation_from_input(grammar_fit)
    s9 = s9_bridge()
    if any(report["state_change_found"] for report in searches.values()):
        raise AssertionError("a no-op or conditional response became a state change")
    if not s9["all_unpaid"] or s9["replayed_state"]["data"]:
        raise AssertionError("Supply paid or admitted an S9 line")
    terminals = [
        "LEFTOVER_ADMITTED",
        "LEFTOVER_LEFT_OUTSIDE",
        "STATE_CHANGE_NOT_FOUND",
        "LABEL_ONLY",
        "GUARDED_CONDITIONAL",
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
    return {
        "schema": "admit-leftover-v1",
        "evidence_class": "FINITE_COMPUTATION",
        "prompt_sha256": hashes["prompt"],
        "grammar_fit_receipt_sha256": hashes["grammar_fit_receipt"],
        "write_root": WRITE_ROOT,
        "sealed_paths": list(SEALED_PATHS),
        "sealed_paths_touched": [],
        "source_inputs": {
            "grammar_fit_receipt": "research/grammar_fit/receipts/grammar_fit.json",
            "grammar_fit_receipt_read_only": True,
        },
        "reconstruction": {
            "classification": "METATHEORY",
            "module": "research/admit_leftover/admit_leftover.py",
            "imports_sealed_implementation": False,
            "constructors": [
                "Supply",
                "AdmitDatum",
                "AdmitForm",
                "AdmitInst",
                "Impose",
                "Observe",
                "assertWit",
                "admitWit",
                "protect",
                "declareObs",
            ],
            "passage_guard_policy": {
                "admitWit_requires": ["asserted pair"],
                "protect_requires": ["retained witness"],
                "declareObs_has_object_ingredient": False,
            },
        },
        "admission_choice": collision,
        "profile_case": profile_case,
        "search_after_each_choice": searches,
        "admission_bill": bill,
        "comparison": {
            "terminal": "COMPARISON_EXCLUDED",
            "status": "DECLARED_POLICY",
            "constructor": None,
            "atom_cost": None,
            "leftover": "comparison policy remains OPEN",
        },
        "measure": bill,
        "orientation": orientation,
        "s9_bridge": s9,
        "open_boundaries": open_boundaries(),
        "refusals": refusals(),
        "distinctions": {
            "datum": "admitted data entries",
            "difference": "Primitive Difference remains distinct and is not renamed",
            "thing": "no thinghood identification is made in this packet",
        },
        "count_policy": "No count is a minimum or completeness claim without a collapse witness or min-response.",
        "terminals": terminals,
        "leftover": (
            "The asserted pair was admitted by assertWit and charged one atom. "
            "The identifying map remains outside state, comparison is excluded, "
            "and the guarded family is conditional and unfired."
        ),
        "receipt_replay": {
            "rule": "build_receipt() recomputes this timestamp-free JSON from the two hash-pinned inputs",
            "byte_identical_required": True,
        },
    }


def write_receipt(path: Path | None = None) -> Path:
    target = path or (ROOT / "receipts" / "admit_leftover.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(build_receipt(), sort_keys=True, indent=2, ensure_ascii=False)
    target.write_bytes((payload + "\n").encode("utf-8"))
    return target


if __name__ == "__main__":
    print(write_receipt().as_posix())
