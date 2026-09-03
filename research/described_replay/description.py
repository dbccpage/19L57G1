"""Local finite event kernel and descriptions for ``DR-C-2-1-3``.

This module is a reconstruction inside the research tree.  It deliberately
does not import the sealed implementation.  The finite class, description
alphabet, and bounds are the declarations frozen in ``PREDICTIONS.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
import hashlib
from itertools import product
import json
from typing import Mapping, Sequence, TypeAlias, cast


Args: TypeAlias = tuple[int, ...]
Inst: TypeAlias = tuple[int, Args]
Pair: TypeAlias = tuple[int, int]
Json: TypeAlias = (
    None
    | bool
    | int
    | float
    | str
    | Sequence["Json"]
    | Mapping[str, "Json"]
)


class AdmissionError(ValueError):
    """An event is not well formed at the regime where it is applied."""


@dataclass(frozen=True)
class Regime:
    """The admitted state of the reconstructed finite kernel."""

    data: tuple[str, ...]
    forms: tuple[int, ...]
    insts: frozenset[Inst]
    rules: frozenset[int]
    reqs: frozenset[Pair]

    def n_data(self) -> int:
        return len(self.data)


EMPTY = Regime((), (), frozenset(), frozenset(), frozenset())


@dataclass(frozen=True)
class Supply:
    token: str


@dataclass(frozen=True)
class AdmitDatum:
    token: str


@dataclass(frozen=True)
class AdmitForm:
    arity: int


@dataclass(frozen=True)
class AdmitInst:
    form: int
    args: Args


@dataclass(frozen=True)
class AdmitRuleAll:
    form: int


@dataclass(frozen=True)
class Impose:
    i: int
    j: int


Event: TypeAlias = (
    Supply | AdmitDatum | AdmitForm | AdmitInst | AdmitRuleAll | Impose
)
History: TypeAlias = tuple[Event, ...]


def step(regime: Regime, event: Event) -> Regime:
    """Apply exactly one event to ``regime``.

    Presentation is inert.  Re-admission designates an existing datum.  All
    other malformed events fail rather than silently changing their meaning.
    """

    if isinstance(event, Supply):
        return regime
    if isinstance(event, AdmitDatum):
        if event.token in regime.data:
            return regime
        return Regime(
            regime.data + (event.token,),
            regime.forms,
            regime.insts,
            regime.rules,
            regime.reqs,
        )
    if isinstance(event, AdmitForm):
        if event.arity < 1:
            raise AdmissionError(
                f"form arity must be at least one, got {event.arity}"
            )
        return Regime(
            regime.data,
            regime.forms + (event.arity,),
            regime.insts,
            regime.rules,
            regime.reqs,
        )
    if isinstance(event, AdmitInst):
        if not 0 <= event.form < len(regime.forms):
            raise AdmissionError(f"unknown form {event.form}")
        expected_arity = regime.forms[event.form]
        if len(event.args) != expected_arity:
            raise AdmissionError(
                f"form {event.form} has arity {expected_arity}, "
                f"got {len(event.args)} arguments"
            )
        if not all(0 <= datum < regime.n_data() for datum in event.args):
            raise AdmissionError(
                f"instance arguments out of range: {event.args}"
            )
        return Regime(
            regime.data,
            regime.forms,
            regime.insts | {(event.form, event.args)},
            regime.rules,
            regime.reqs,
        )
    if isinstance(event, AdmitRuleAll):
        if not 0 <= event.form < len(regime.forms):
            raise AdmissionError(f"unknown form {event.form}")
        return Regime(
            regime.data,
            regime.forms,
            regime.insts,
            regime.rules | {event.form},
            regime.reqs,
        )
    if not 0 <= event.i < event.j < regime.n_data():
        raise AdmissionError(
            f"requirement out of range: ({event.i}, {event.j})"
        )
    return Regime(
        regime.data,
        regime.forms,
        regime.insts,
        regime.rules,
        regime.reqs | {(event.i, event.j)},
    )


def replay(events: Sequence[Event], base: Regime = EMPTY) -> Regime:
    """Fold a recorded event history from ``base``."""

    regime = base
    for event in events:
        regime = step(regime, event)
    return regime


def certify(
    events: Sequence[Event], claimed: Regime, base: Regime = EMPTY
) -> bool:
    """Check that ``claimed`` is the exact replayed endpoint."""

    return replay(events, base) == claimed


CLASS_ID = "DR-C-2-1-3"
CLASS_DATUM_TOKENS: tuple[str, str] = ("a", "b")
CLASS_FORM_ARITIES: tuple[int, ...] = (1,)
CLASS_LENGTH_BOUND = 3

# The tuple order is the declared event-symbol order.  The contained values
# are immutable, so returning one of them from the decoder is harmless.
EVENT_SYMBOLS: tuple[Event, ...] = (
    Supply("a"),
    Supply("b"),
    AdmitDatum("a"),
    AdmitDatum("b"),
    AdmitForm(1),
    AdmitInst(0, (0,)),
    AdmitInst(0, (1,)),
    AdmitRuleAll(0),
    Impose(0, 1),
)
EVENT_SYMBOL_COUNT = len(EVENT_SYMBOLS)
DESCRIPTION_TOKEN_ALPHABET: tuple[str, ...] = tuple(
    f"p{position}e{symbol}"
    for position in range(CLASS_LENGTH_BOUND)
    for symbol in range(EVENT_SYMBOL_COUNT)
)


@dataclass(frozen=True)
class Process:
    """A member candidate: fixed base, events, and the shared bound."""

    base: Regime
    events: History
    length_bound: int = CLASS_LENGTH_BOUND


def event_to_symbol(event: Event) -> int:
    """Return the declared symbol index, rejecting out-of-alphabet events."""

    try:
        return EVENT_SYMBOLS.index(event)
    except ValueError as exc:
        raise ValueError(f"event is outside {CLASS_ID}: {event!r}") from exc


@dataclass(frozen=True)
class EventSymbolValid:
    symbol: int
    event: Event


@dataclass(frozen=True)
class EventSymbolInvalid:
    symbol: object
    reason: str


EventSymbolResult: TypeAlias = EventSymbolValid | EventSymbolInvalid


def decode_event_symbol(symbol: object) -> EventSymbolResult:
    """Decode a symbol with an explicit validity tag."""

    if type(symbol) is not int:
        return EventSymbolInvalid(symbol, "event symbol is not an integer")
    index = symbol
    if not 0 <= index < EVENT_SYMBOL_COUNT:
        return EventSymbolInvalid(symbol, "event symbol is out of range")
    return EventSymbolValid(index, EVENT_SYMBOLS[index])


def event_from_symbol(symbol: int) -> Event | None:
    """Optional projection of ``decode_event_symbol``."""

    decoded = decode_event_symbol(symbol)
    return decoded.event if isinstance(decoded, EventSymbolValid) else None


def _well_formed_prefixes(events: Sequence[Event]) -> tuple[Regime, ...] | None:
    regime = EMPTY
    prefixes = [regime]
    try:
        for event in events:
            regime = step(regime, event)
            prefixes.append(regime)
    except AdmissionError:
        return None
    return tuple(prefixes)


def is_class_member(process: Process) -> bool:
    """Decide exact membership in the frozen finite class."""

    if process.base != EMPTY:
        return False
    if process.length_bound != CLASS_LENGTH_BOUND:
        return False
    if len(process.events) > CLASS_LENGTH_BOUND:
        return False
    try:
        for event in process.events:
            event_to_symbol(event)
    except ValueError:
        return False
    return _well_formed_prefixes(process.events) is not None


def process_key(process: Process) -> tuple[int, ...]:
    """The deterministic symbol word of a class member."""

    if not is_class_member(process):
        raise ValueError(f"process is not a member of {CLASS_ID}")
    return tuple(event_to_symbol(event) for event in process.events)


def enumerate_members() -> tuple[Process, ...]:
    """Enumerate all and only members, by length then symbol word."""

    members: list[Process] = [Process(EMPTY, ())]
    frontier: list[tuple[History, Regime]] = [((), EMPTY)]
    for _length in range(1, CLASS_LENGTH_BOUND + 1):
        next_frontier: list[tuple[History, Regime]] = []
        for history, regime in frontier:
            for event in EVENT_SYMBOLS:
                try:
                    endpoint = step(regime, event)
                except AdmissionError:
                    continue
                extended = history + (event,)
                next_frontier.append((extended, endpoint))
                members.append(Process(EMPTY, extended))
        frontier = next_frontier
    return tuple(members)


@lru_cache(maxsize=1)
def enumerate_description_regimes() -> tuple[Regime, ...]:
    """Enumerate every word of length at most three over the 27-token alphabet."""

    return tuple(
        Regime(tuple(tokens), (), frozenset(), frozenset(), frozenset())
        for length in range(CLASS_LENGTH_BOUND + 1)
        for tokens in product(DESCRIPTION_TOKEN_ALPHABET, repeat=length)
    )


def encode_token(position: int, symbol: int) -> str:
    """Encode one valid position-symbol pair as its declared fresh token."""

    if type(position) is not int or not 0 <= position < CLASS_LENGTH_BOUND:
        raise ValueError(f"position out of range: {position}")
    if type(symbol) is not int or not 0 <= symbol < EVENT_SYMBOL_COUNT:
        raise ValueError(f"event symbol out of range: {symbol}")
    return f"p{position}e{symbol}"


@dataclass(frozen=True)
class DescriptionTokenValid:
    position: int
    symbol: int
    event: Event


@dataclass(frozen=True)
class DescriptionTokenInvalid:
    position: int
    token: object
    reason: str


DescriptionTokenResult: TypeAlias = (
    DescriptionTokenValid | DescriptionTokenInvalid
)


def decode_token(token: object, position: int) -> DescriptionTokenResult:
    """Decode exactly the token expected at ``position``.

    Comparing against the finite canonical spellings rejects alternate
    decimal spellings, misplaced positions, and out-of-alphabet symbols.
    """

    if not 0 <= position < CLASS_LENGTH_BOUND:
        return DescriptionTokenInvalid(position, token, "position out of range")
    if not isinstance(token, str):
        return DescriptionTokenInvalid(position, token, "token is not text")
    for symbol, event in enumerate(EVENT_SYMBOLS):
        if token == encode_token(position, symbol):
            return DescriptionTokenValid(position, symbol, event)
    return DescriptionTokenInvalid(
        position, token, "token does not match its position and event symbol"
    )


@dataclass(frozen=True)
class Description:
    """Admission-only record of a process event list and its endpoint."""

    admission_history: tuple[AdmitDatum, ...]
    regime: Regime


DescriptionInput: TypeAlias = Description | Regime


@dataclass(frozen=True)
class DecodeValid:
    """Immutable witness produced by complete description validation.

    ``prefixes`` contains the sound fold from ``EMPTY`` through every event.
    The private preparation fields let the one-event stepper reject a copied
    or hand-built value without decoding or folding the history again.
    """

    description: Description
    process: Process
    prefixes: tuple[Regime, ...]
    _integrity: str = field(repr=False, compare=False)
    _preparation_token: object = field(repr=False, compare=False)

    @property
    def events(self) -> History:
        return self.process.events


@dataclass(frozen=True)
class DecodeInvalid:
    reason: str


DecodeResult: TypeAlias = DecodeValid | DecodeInvalid


_PREPARATION_TOKEN = object()


def encode_history(events: Sequence[Event]) -> tuple[AdmitDatum, ...]:
    """Encode a class event list as position-tagged admissions."""

    process = Process(EMPTY, tuple(events))
    if not is_class_member(process):
        raise ValueError(f"event list is not a member of {CLASS_ID}")
    return tuple(
        AdmitDatum(encode_token(position, event_to_symbol(event)))
        for position, event in enumerate(process.events)
    )


def encode_description(process: Process) -> Description:
    """Encode a class member using admission events only."""

    if not is_class_member(process):
        raise ValueError(f"process is not a member of {CLASS_ID}")
    admissions = encode_history(process.events)
    tokens = tuple(admission.token for admission in admissions)
    return Description(
        admissions,
        Regime(tokens, (), frozenset(), frozenset(), frozenset()),
    )


def encode(process: Process) -> Description:
    """Short name for the declared process encoding."""

    return encode_description(process)


def _normalize_description(value: DescriptionInput) -> Description:
    if isinstance(value, Description):
        return value
    return Description(tuple(AdmitDatum(token) for token in value.data), value)


def decode_description_tagged(value: DescriptionInput) -> DecodeResult:
    """Decide the exact decoder domain and retain the failure reason."""

    description = _normalize_description(value)
    regime = description.regime
    if regime.forms or regime.insts or regime.rules or regime.reqs:
        return DecodeInvalid(
            "description regime contains a non-description component"
        )
    if len(regime.data) > CLASS_LENGTH_BOUND:
        return DecodeInvalid("description exceeds the shared length bound")
    if len(description.admission_history) != len(regime.data):
        return DecodeInvalid(
            "admission history length does not match description data"
        )

    events: list[Event] = []
    for position, raw_admission in enumerate(description.admission_history):
        if not isinstance(raw_admission, AdmitDatum):
            return DecodeInvalid("description history is not admission-only")
        if raw_admission.token != regime.data[position]:
            return DecodeInvalid(
                "admission history does not reproduce description data"
            )
        decoded_token = decode_token(raw_admission.token, position)
        if isinstance(decoded_token, DescriptionTokenInvalid):
            return DecodeInvalid(decoded_token.reason)
        events.append(decoded_token.event)

    # Canonical position tags make all admitted tokens distinct.  This exact
    # expected regime check also rejects hand-built states that could not be
    # produced by the recorded admission history.
    expected_regime = Regime(
        tuple(admission.token for admission in description.admission_history),
        (),
        frozenset(),
        frozenset(),
        frozenset(),
    )
    if regime != expected_regime:
        return DecodeInvalid("description regime is not its recorded endpoint")

    process = Process(EMPTY, tuple(events))
    if not is_class_member(process):
        return DecodeInvalid("decoded event list is not a class member")
    prefixes = _well_formed_prefixes(process.events)
    if prefixes is None:
        return DecodeInvalid("decoded event list has an ill-formed prefix")
    return _make_decode_valid(description, process, prefixes)


def validate_description(value: DescriptionInput) -> DecodeResult:
    """Named tagged-domain helper used by callers that retain diagnostics."""

    return decode_description_tagged(value)


def prepare_description(value: DescriptionInput) -> DecodeResult:
    """Perform the complete decoder-domain and prefix validation once."""

    return decode_description_tagged(value)


def decode_description(value: DescriptionInput) -> Process | None:
    """Decode to a class member, or return ``None`` outside the domain."""

    result = decode_description_tagged(value)
    return result.process if isinstance(result, DecodeValid) else None


def decoder_domain(value: DescriptionInput) -> bool:
    """Whether ``value`` satisfies every declared decoder-domain clause."""

    return isinstance(decode_description_tagged(value), DecodeValid)


def description_is_admission_only(description: Description) -> bool:
    """Check the syntactic and state components of admission-only encoding."""

    return (
        all(
            isinstance(event, AdmitDatum)
            for event in description.admission_history
        )
        and not description.regime.forms
        and not description.regime.insts
        and not description.regime.rules
        and not description.regime.reqs
    )


def description_price(description: DescriptionInput) -> int | None:
    """Number of admission events, when the description is valid."""

    result = decode_description_tagged(description)
    if isinstance(result, DecodeInvalid):
        return None
    return len(result.description.admission_history)


def event_json(event: Event) -> dict[str, Json]:
    """Canonical JSON object for one event."""

    if isinstance(event, Supply):
        return {"event": "supply", "token": event.token}
    if isinstance(event, AdmitDatum):
        return {"event": "admit_datum", "token": event.token}
    if isinstance(event, AdmitForm):
        return {"arity": event.arity, "event": "admit_form"}
    if isinstance(event, AdmitInst):
        return {
            "args": list(event.args),
            "event": "admit_inst",
            "form": event.form,
        }
    if isinstance(event, AdmitRuleAll):
        return {"event": "admit_rule_all", "form": event.form}
    return {"event": "impose_separation", "i": event.i, "j": event.j}


def _require_exact_int(value: object, field: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{field} is not an integer")
    return value


def event_from_json(payload: Mapping[str, object]) -> Event:
    """Inverse of ``event_json`` on its exact output domain."""

    kind = payload.get("event")
    if kind == "supply" or kind == "admit_datum":
        token = payload.get("token")
        if not isinstance(token, str):
            raise ValueError("event token is not text")
        return Supply(token) if kind == "supply" else AdmitDatum(token)
    if kind == "admit_form":
        return AdmitForm(_require_exact_int(payload.get("arity"), "arity"))
    if kind == "admit_inst":
        form = _require_exact_int(payload.get("form"), "form")
        raw_args = payload.get("args")
        if not isinstance(raw_args, list) or not all(
            type(argument) is int for argument in raw_args
        ):
            raise ValueError("instance args are not an integer list")
        return AdmitInst(form, tuple(cast(list[int], raw_args)))
    if kind == "admit_rule_all":
        return AdmitRuleAll(_require_exact_int(payload.get("form"), "form"))
    if kind == "impose_separation":
        return Impose(
            _require_exact_int(payload.get("i"), "i"),
            _require_exact_int(payload.get("j"), "j"),
        )
    raise ValueError(f"unknown event kind: {kind!r}")


def regime_json(regime: Regime) -> dict[str, Json]:
    """Canonical JSON object for a regime."""

    return {
        "data": list(regime.data),
        "forms": list(regime.forms),
        "insts": [
            [form, list(args)] for form, args in sorted(regime.insts)
        ],
        "reqs": [list(pair) for pair in sorted(regime.reqs)],
        "rules": sorted(regime.rules),
    }


def deterministic_json_bytes(value: Json) -> bytes:
    """Stable UTF-8 serialization used by every hash in this module."""

    return json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def event_sha256(event: Event) -> str:
    return hashlib.sha256(deterministic_json_bytes(event_json(event))).hexdigest()


def regime_sha256(regime: Regime) -> str:
    return hashlib.sha256(
        deterministic_json_bytes(regime_json(regime))
    ).hexdigest()


def process_json(process: Process) -> dict[str, Json]:
    """Canonical JSON object for an exact class process."""

    return {
        "base": regime_json(process.base),
        "events": [event_json(event) for event in process.events],
        "length_bound": process.length_bound,
    }


def process_sha256(process: Process) -> str:
    return hashlib.sha256(
        deterministic_json_bytes(process_json(process))
    ).hexdigest()


def description_json(description: Description) -> dict[str, Json]:
    """Canonical JSON object retaining both description witnesses."""

    return {
        "admission_history": [
            event_json(event) for event in description.admission_history
        ],
        "regime": regime_json(description.regime),
    }


def _decode_valid_integrity(
    description: Description,
    process: Process,
    prefixes: tuple[Regime, ...],
) -> str:
    payload: dict[str, Json] = {
        "description": description_json(description),
        "prefixes": [regime_json(prefix) for prefix in prefixes],
        "process": process_json(process),
    }
    return hashlib.sha256(deterministic_json_bytes(payload)).hexdigest()


def _make_decode_valid(
    description: Description,
    process: Process,
    prefixes: tuple[Regime, ...],
) -> DecodeValid:
    return DecodeValid(
        description,
        process,
        prefixes,
        _decode_valid_integrity(description, process, prefixes),
        _PREPARATION_TOKEN,
    )


def prepared_decode_is_valid(prepared: DecodeValid) -> bool:
    """Check witness custody without decoding or folding the history.

    This is intentionally a structural integrity check over the immutable
    result of preparation.  Sound prefix construction occurs only inside the
    decoder; stepping merely verifies that the retained witness is unchanged.
    """

    return (
        prepared._preparation_token is _PREPARATION_TOKEN
        and prepared._integrity
        == _decode_valid_integrity(
            prepared.description,
            prepared.process,
            prepared.prefixes,
        )
    )


def description_sha256(description: Description) -> str:
    return hashlib.sha256(
        deterministic_json_bytes(description_json(description))
    ).hexdigest()
