"""Model-layer replay and the complete in-class candidate matrix.

The model-layer stepper follows a supplied description.  An in-class
candidate instead has only its fixed base and event list; feeding it a
description validates the metatheoretic argument and then runs that fixed
process.  No candidate event reads, removes, or dispatches on the
description.  AuthorityEffect: None.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache

from description import (
    DecodeInvalid,
    DecodeValid,
    Description,
    Process,
    Regime,
    certify,
    decode_description_tagged,
    decoder_domain,
    description_json,
    description_sha256,
    encode_description,
    enumerate_description_regimes,
    enumerate_members,
    is_class_member,
    process_json,
    process_sha256,
    prepare_description,
    regime_sha256,
    replay,
)
from stepper import (
    Invalid,
    consume_prepared_events,
    initial_state_from_preparation,
)


@dataclass(frozen=True)
class ModelReplay:
    process: Process
    description: Description
    reproduced: Regime
    certified: bool


@dataclass(frozen=True)
class CandidateCell:
    candidate_index: int
    target_index: int
    candidate_sha256: str
    target_sha256: str
    description_sha256: str
    reproduced_regime_sha256: str
    target_regime_sha256: str
    candidate_execution_certified: bool
    target_reproduction_certified: bool


@lru_cache(maxsize=1)
def class_members() -> tuple[Process, ...]:
    return enumerate_members()


def model_replay(description: Description) -> ModelReplay | None:
    prepared = prepare_description(description)
    if isinstance(prepared, DecodeInvalid):
        return None
    consumed = consume_prepared_events(
        initial_state_from_preparation(description, prepared)
    )
    if isinstance(consumed, Invalid):
        return None
    reproduced = consumed.regime
    return ModelReplay(
        prepared.process,
        prepared.description,
        reproduced,
        certify(prepared.process.events, reproduced, prepared.process.base),
    )


@lru_cache(maxsize=178)
def execute_class_process(candidate: Process) -> Regime:
    """Run one fixed class history through its costed event steps."""

    if not is_class_member(candidate):
        raise ValueError("candidate is outside the declared class")
    own_description = encode_description(candidate)
    prepared = prepare_description(own_description)
    if not isinstance(prepared, DecodeValid):
        raise ValueError("encoded candidate did not prepare")
    consumed = consume_prepared_events(
        initial_state_from_preparation(own_description, prepared)
    )
    if isinstance(consumed, Invalid):
        raise ValueError(consumed.reason)
    return consumed.regime


@lru_cache(maxsize=178)
def _prepare_target_description(description: Description) -> DecodeValid:
    """Validate one immutable target once for repeated matrix rows."""

    prepared = prepare_description(description)
    if isinstance(prepared, DecodeInvalid):
        raise ValueError(prepared.reason)
    return prepared


def feed_candidate(candidate: Process, description: Description) -> Regime:
    """Validate the argument, then run the candidate from its fixed base."""

    _prepare_target_description(description)
    return execute_class_process(candidate)


def candidate_cell(
    candidate_index: int,
    candidate: Process,
    target_index: int,
    target: Process,
) -> CandidateCell:
    description = encode_description(target)
    reproduced = feed_candidate(candidate, description)
    target_endpoint = replay(target.events, target.base)
    return CandidateCell(
        candidate_index,
        target_index,
        process_sha256(candidate),
        process_sha256(target),
        description_sha256(description),
        regime_sha256(reproduced),
        regime_sha256(target_endpoint),
        certify(candidate.events, reproduced, candidate.base),
        certify(target.events, reproduced, target.base),
    )


@lru_cache(maxsize=1)
def complete_candidate_matrix() -> tuple[CandidateCell, ...]:
    members = class_members()
    return tuple(
        candidate_cell(candidate_index, candidate, target_index, target)
        for candidate_index, candidate in enumerate(members)
        for target_index, target in enumerate(members)
    )


def successful_candidate_indices() -> tuple[int, ...]:
    members = class_members()
    cells = complete_candidate_matrix()
    return tuple(
        index
        for index in range(len(members))
        if all(
            cell.target_reproduction_certified
            for cell in cells
            if cell.candidate_index == index
        )
    )


def _cell_json(cell: CandidateCell) -> dict[str, object]:
    return {
        "candidate_execution_certified": cell.candidate_execution_certified,
        "candidate_index": cell.candidate_index,
        "candidate_sha256": cell.candidate_sha256,
        "description_sha256": cell.description_sha256,
        "reproduced_regime_sha256": cell.reproduced_regime_sha256,
        "target_index": cell.target_index,
        "target_regime_sha256": cell.target_regime_sha256,
        "target_reproduction_certified": cell.target_reproduction_certified,
        "target_sha256": cell.target_sha256,
    }


def render_description_stage() -> dict[str, object]:
    members = class_members()
    encodings = [encode_description(member) for member in members]
    model_runs = [model_replay(description) for description in encodings]
    length_histogram = Counter(len(member.events) for member in members)
    endpoints = {regime_sha256(replay(member.events, member.base)) for member in members}
    description_words = enumerate_description_regimes()
    encoded_regimes = {description.regime for description in encodings}
    decoded_regimes = {regime for regime in description_words if decoder_domain(regime)}
    invalid_reasons = Counter(
        result.reason
        for regime in description_words
        if isinstance((result := decode_description_tagged(regime)), DecodeInvalid)
    )
    return {
        "authority_effect": None,
        "class": {
            "arity_bound": 1,
            "class_id": "DR-C-2-1-3",
            "class_size": len(members),
            "datum_alphabet_size": 2,
            "description_alphabet_size": 27,
            "event_alphabet_size": 9,
            "length_bound": 3,
            "length_histogram": {
                str(length): length_histogram[length]
                for length in sorted(length_histogram)
            },
            "literal_endpoint_count": len(endpoints),
        },
        "codec": {
            "all_admission_only": all(
                all(event.__class__.__name__ == "AdmitDatum" for event in item.admission_history)
                for item in encodings
            ),
            "all_decode_encode": all(
                decode_description_tagged(description).process == member  # type: ignore[union-attr]
                for member, description in zip(members, encodings, strict=True)
            ),
            "encoding_hashes_unique": len({description_sha256(item) for item in encodings})
            == len(encodings),
            "model_replay_certified_count": sum(
                run is not None and run.certified for run in model_runs
            ),
        },
        "decoder_domain": {
            "declared_word_count": len(description_words),
            "domain_equals_encoding_image": decoded_regimes == encoded_regimes,
            "invalid_reason_histogram": {
                reason: invalid_reasons[reason] for reason in sorted(invalid_reasons)
            },
            "valid_regime_count": len(decoded_regimes),
            "valid_regime_sha256": sorted(regime_sha256(item) for item in decoded_regimes),
        },
        "endpoint_countermodel": {
            "left": process_json(members[0]),
            "left_description": description_json(encodings[0]),
            "right": process_json(members[1]),
            "right_description": description_json(encodings[1]),
            "same_endpoint": replay(members[0].events) == replay(members[1].events),
            "different_histories": members[0].events != members[1].events,
        },
        "observation_evidence_class": "FINITE_COMPUTATION",
        "terminal": "DESCRIPTION_PROVED",
    }


def render_stepper_stage() -> dict[str, object]:
    members = class_members()
    rows: list[dict[str, object]] = []
    for index, member in enumerate(members):
        description = encode_description(member)
        run = model_replay(description)
        if run is None:
            raise ValueError(f"model replay failed for member {index}")
        rows.append(
            {
                "certified": run.certified,
                "consumed_event_step_count": len(member.events),
                "endpoint_sha256": regime_sha256(run.reproduced),
                "event_count": len(member.events),
                "member_index": index,
                "tagged_result_count_including_done": len(member.events) + 1,
            }
        )
    return {
        "authority_effect": None,
        "class_id": "DR-C-2-1-3",
        "defined_through_replay": False,
        "rows": rows,
        "terminal": "STEPPER_PROVED",
    }


def render_class_replay() -> dict[str, object]:
    members = class_members()
    matrix = complete_candidate_matrix()
    winners = successful_candidate_indices()
    terminal = (
        "MEMBER_REPLAYS_CLASS_PROVED"
        if winners
        else "NO_SUCH_MEMBER_IN_CLASS"
    )
    return {
        "authority_effect": None,
        "candidate_count": len(members),
        "certified_candidate_execution_count": sum(
            cell.candidate_execution_certified for cell in matrix
        ),
        "class_id": "DR-C-2-1-3",
        "class_reproduction_success_count": sum(
            cell.target_reproduction_certified for cell in matrix
        ),
        "class_scope": {
            "arity_bound": 1,
            "datum_alphabet_size": 2,
            "event_alphabet_size": 9,
            "history_length_bound": 3,
        },
        "member_description_catalog": [
            {
                "description": description_json(encode_description(member)),
                "description_sha256": description_sha256(encode_description(member)),
                "member_index": index,
                "member_process": process_json(member),
                "member_sha256": process_sha256(member),
            }
            for index, member in enumerate(members)
        ],
        "complete_matrix": [_cell_json(cell) for cell in matrix],
        "matrix_cell_count": len(matrix),
        "successful_candidate_indices": list(winners),
        "target_count": len(members),
        "terminal": terminal,
    }
