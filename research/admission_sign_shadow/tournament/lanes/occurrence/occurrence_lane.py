from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal, TypeAlias


@dataclass(frozen=True)
class Supply:
    token: int


@dataclass(frozen=True)
class AdmitDatum:
    token: int


@dataclass(frozen=True)
class AdmitForm:
    arity: int


@dataclass(frozen=True)
class AdmitInst:
    form: int
    args: tuple[int, ...]


@dataclass(frozen=True)
class AdmitRuleAll:
    form: int


@dataclass(frozen=True)
class Impose:
    i: int
    j: int


Event: TypeAlias = Supply | AdmitDatum | AdmitForm | AdmitInst | AdmitRuleAll | Impose


@dataclass(frozen=True, order=True)
class Occurrence:
    occurrence_id: int
    token: int


def projected_tokens(history: tuple[Event, ...]) -> tuple[int, ...]:
    """Project only datum-admission occurrences from the declared event history."""
    return tuple(event.token for event in history if isinstance(event, AdmitDatum))


def canonical_datum_replay(history: tuple[Event, ...]) -> tuple[int, ...]:
    """Replay the frozen-Python-shaped deduplicating datum endpoint."""
    endpoint: list[int] = []
    for token in projected_tokens(history):
        if token not in endpoint:
            endpoint.append(token)
    return tuple(endpoint)


def occurrence_replay(history: tuple[Event, ...]) -> tuple[Occurrence, ...]:
    """Assign deterministic consecutive IDs to admission events, not endpoints."""
    return tuple(
        Occurrence(occurrence_id, token)
        for occurrence_id, token in enumerate(projected_tokens(history))
    )


def forget_occurrences(history: tuple[Occurrence, ...]) -> tuple[int, ...]:
    endpoint: list[int] = []
    for item in history:
        if item.token not in endpoint:
            endpoint.append(item.token)
    return tuple(endpoint)


def valid_occurrence_ids(history: tuple[Occurrence, ...]) -> bool:
    identifiers = tuple(item.occurrence_id for item in history)
    return len(identifiers) == len(set(identifiers))


def count_token(history: tuple[Occurrence, ...], token: int) -> int:
    return sum(item.token == token for item in history)


def rename_ids(
    history: tuple[Occurrence, ...], rename: Callable[[int], int]
) -> tuple[Occurrence, ...]:
    return tuple(Occurrence(rename(item.occurrence_id), item.token) for item in history)


def scaled_encoding(unit: int) -> Callable[[int], int]:
    return lambda count: unit * count


def additive_laws_hold(encode: Callable[[int], int], bound: int) -> bool:
    if bound < 0:
        raise ValueError("bound must be nonnegative")
    return encode(0) == 0 and all(
        encode(left + right) == encode(left) + encode(right)
        for left in range(bound + 1)
        for right in range(bound + 1 - left)
    )


Status: TypeAlias = Literal["PROVED", "CONDITIONAL", "REFUTED", "OPEN"]


def _entry(
    symbol: str,
    status: Status,
    evidence: tuple[str, ...],
    obligation: str,
) -> dict[str, object]:
    return {
        "symbol": symbol,
        "status": status,
        "evidence": list(evidence),
        "obligation": obligation,
    }


def symbol_packet() -> dict[str, object]:
    once = (AdmitDatum(7),)
    duplicate = (AdmitDatum(7), AdmitDatum(7))
    once_occurrences = occurrence_replay(once)
    duplicate_occurrences = occurrence_replay(duplicate)
    return {
        "authority_effect": None,
        "declared_event_surface": [
            "Supply",
            "AdmitDatum",
            "AdmitForm",
            "AdmitInst",
            "AdmitRuleAll",
            "Impose",
        ],
        "lean_imports": [
            "Derivation.Erasure",
            "AdmissionSignShadow.Core",
            "Std (transitive)",
        ],
        "symbols": [
            _entry(
                "REPLAY_DERIVED_OCCURRENCE_PROJECTION",
                "PROVED",
                (
                    "Derivation.TEvent",
                    "Derivation.replayT",
                    "replayT_tokens",
                    "occurrenceReplay_valid",
                    "occurrenceReplay_count",
                ),
                "Scoped to the retained exact TEvent trace, not its endpoint.",
            ),
            _entry(
                "FORGET_REPLAY_COMMUTES",
                "PROVED",
                ("forget_occurrenceReplay_commutes",),
                "Canonical replay is the ordered deduplicating datum projection.",
            ),
            _entry(
                "DETERMINISTIC_IDS_AND_COUNT",
                "PROVED",
                ("ids_withIdsFrom", "occurrenceReplay_count"),
                "IDs count datum-admission events and skip non-datum events.",
            ),
            _entry(
                "DUPLICATE_ADMISSION_ENDPOINT_COLLISION",
                "PROVED",
                ("duplicate_admission_endpoint_collision",),
                "The endpoint deduplicates while the event-derived count remains 1 versus 2.",
            ),
            _entry(
                "ID_RENAMING_INVARIANCE",
                "PROVED",
                (
                    "countToken_renameIds",
                    "forgetOccurrences_renameIds",
                    "occurrenceValid_renameIds",
                ),
                "Validity preservation requires an injective renaming.",
            ),
            _entry(
                "ENDPOINT_DETERMINES_OCCURRENCE_HISTORY",
                "REFUTED",
                ("endpoint_does_not_determine_occurrence_history",),
                "No recovery function from canonical datum endpoints works for all histories.",
            ),
            _entry(
                "ENDPOINT_DETERMINES_OCCURRENCE_COUNT",
                "REFUTED",
                ("endpoint_does_not_determine_occurrence_count",),
                "No recovery function from canonical datum endpoints returns the token-7 count.",
            ),
            _entry(
                "ADDITIVE_LAWS_SELECT_INTEGER_UNIT",
                "REFUTED",
                ("additive_laws_do_not_select_integer_unit",),
                "Every integer unit gives an additive scaled encoding.",
            ),
            _entry(
                "UNIT_CALIBRATED_ENCODING_UNIQUE",
                "CONDITIONAL",
                ("unit_calibration_is_conditional",),
                "Requires the additional premise encode(1) = 1.",
            ),
            _entry(
                "EXACT_FROZEN_TEVENT_REPLAY_USE",
                "PROVED",
                (
                    "Derivation.TEvent",
                    "Derivation.stepT",
                    "Derivation.replayT",
                    "replayT_tokens",
                    "forget_occurrenceReplay_commutes",
                ),
                "The ephemeral verifier pins and imports the frozen Erasure.lean blob directly.",
            ),
            _entry(
                "ENDPOINT_DETERMINES_RETAINED_TEVENT_TRACE",
                "OPEN",
                (),
                "No recovery of a retained event trace from a deduplicated replay endpoint is supplied.",
            ),
            _entry(
                "OCCURRENCE_TRACE_CONNECTOR_INTEGRATION",
                "OPEN",
                ("occurrenceReplay", "forget_occurrenceReplay_commutes"),
                "The projection is proved, but the current connector does not consume the retained exact TEvent trace.",
            ),
        ],
        "witness": {
            "once_endpoint": list(canonical_datum_replay(once)),
            "duplicate_endpoint": list(canonical_datum_replay(duplicate)),
            "once_count": count_token(once_occurrences, 7),
            "duplicate_count": count_token(duplicate_occurrences, 7),
            "same_endpoint": canonical_datum_replay(once)
            == canonical_datum_replay(duplicate),
            "different_occurrence_history": once_occurrences != duplicate_occurrences,
        },
        "terminal": "TRACE_PROJECTION_PROVED_CONNECTOR_INTEGRATION_OPEN",
    }
