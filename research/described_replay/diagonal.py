"""Self-description and bounded terminal reporting for the frozen class.

The terminal predicate and report marker are the declarations frozen before
the search.  Every result remains class- and cost-relative.
AuthorityEffect: None.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache

from class_replay import class_members, feed_candidate, model_replay
from description import (
    AdmitDatum,
    Description,
    EMPTY,
    Process,
    encode_description,
    is_class_member,
    process_sha256,
    regime_sha256,
    replay,
)


REPORT_COST_BOUND = 6


@dataclass(frozen=True)
class ReporterCell:
    candidate_index: int
    target_index: int
    cost: int
    report: bool
    target_terminal: bool
    correct: bool


def target_reaches_terminal(process: Process) -> bool:
    """The declared terminal: the endpoint has at least one datum."""

    return bool(replay(process.events, process.base).data)


def candidate_report(candidate: Process, target: Process) -> bool:
    """Read the frozen report datum after feeding the target description."""

    output = feed_candidate(candidate, encode_description(target))
    return "b" in output.data


def outside_report_cost(target: Process) -> int:
    """Decode-and-follow cost: one admission and one step per target event."""

    return len(target.events) + len(target.events)


def candidate_run_cost(candidate: Process, target: Process) -> int:
    """Fixed candidate steps plus admissions in the supplied target description."""

    return len(candidate.events) + len(target.events)


def outside_report(target: Process) -> bool:
    run = model_replay(encode_description(target))
    if run is None or not run.certified:
        raise ValueError("model-layer described replay failed")
    return bool(run.reproduced.data)


def description_as_class_process(description: Description) -> Process | None:
    candidate = Process(EMPTY, tuple(description.admission_history))
    return candidate if is_class_member(candidate) else None


def self_description_witness_indices() -> tuple[int, ...]:
    witnesses: list[int] = []
    for index, member in enumerate(class_members()):
        description = encode_description(member)
        description_member = description_as_class_process(description)
        if description_member is None:
            continue
        fed = feed_candidate(member, description)
        direct = replay(member.events, member.base)
        if fed == direct:
            witnesses.append(index)
    return tuple(witnesses)


def reporter_cell(
    candidate_index: int,
    candidate: Process,
    target_index: int,
    target: Process,
) -> ReporterCell:
    report = candidate_report(candidate, target)
    truth = target_reaches_terminal(target)
    return ReporterCell(
        candidate_index,
        target_index,
        candidate_run_cost(candidate, target),
        report,
        truth,
        report == truth,
    )


@lru_cache(maxsize=1)
def complete_reporter_matrix() -> tuple[ReporterCell, ...]:
    members = class_members()
    return tuple(
        reporter_cell(candidate_index, candidate, target_index, target)
        for candidate_index, candidate in enumerate(members)
        for target_index, target in enumerate(members)
        if candidate_run_cost(candidate, target) <= REPORT_COST_BOUND
    )


def successful_reporter_indices() -> tuple[int, ...]:
    members = class_members()
    matrix = complete_reporter_matrix()
    return tuple(
        index
        for index, member in enumerate(members)
        if sum(cell.candidate_index == index for cell in matrix) == len(members)
        and all(cell.correct for cell in matrix if cell.candidate_index == index)
    )


def _member_with_events(events: tuple[object, ...]) -> Process:
    for member in class_members():
        if member.events == events:
            return member
    raise ValueError("declared diagonal member is absent from the class")


def empty_member() -> Process:
    return _member_with_events(())


def one_datum_member() -> Process:
    return _member_with_events((AdmitDatum("a"),))


def diagonal_member(candidate: Process) -> Process:
    """Choose a class member whose terminal opposes a fixed report."""

    if candidate_report(candidate, empty_member()):
        return empty_member()
    return one_datum_member()


def diagonal_disagrees(candidate: Process) -> bool:
    target = diagonal_member(candidate)
    return candidate_report(candidate, target) != target_reaches_terminal(target)


def _reporter_cell_json(cell: ReporterCell) -> dict[str, object]:
    return {
        "candidate_index": cell.candidate_index,
        "cost": cell.cost,
        "correct": cell.correct,
        "report": cell.report,
        "target_index": cell.target_index,
        "target_terminal": cell.target_terminal,
    }


def render_diagonal_stage() -> dict[str, object]:
    members = class_members()
    self_witnesses = self_description_witness_indices()
    matrix = complete_reporter_matrix()
    reporter_winners = successful_reporter_indices()
    cost_histogram = Counter(outside_report_cost(member) for member in members)
    terminal_histogram = Counter(target_reaches_terminal(member) for member in members)
    diagonal_rows = []
    for candidate_index, candidate in enumerate(members):
        target = diagonal_member(candidate)
        cost = candidate_run_cost(candidate, target)
        if cost > REPORT_COST_BOUND:
            continue
        target_index = members.index(target)
        diagonal_rows.append(
            {
                "candidate_index": candidate_index,
                "candidate_sha256": process_sha256(candidate),
                "cost": cost,
                "disagrees": diagonal_disagrees(candidate),
                "target_index": target_index,
                "target_sha256": process_sha256(target),
            }
        )
    outside_rows = [
        {
            "cost": outside_report_cost(member),
            "member_index": index,
            "report": outside_report(member),
            "target_regime_sha256": regime_sha256(replay(member.events, member.base)),
        }
        for index, member in enumerate(members)
    ]
    return {
        "authority_effect": None,
        "class_id": "DR-C-2-1-3",
        "class_scope": {
            "arity_bound": 1,
            "datum_alphabet_size": 2,
            "event_alphabet_size": 9,
            "history_length_bound": 3,
        },
        "diagonal": {
            "all_candidates_disagree": all(
                row["disagrees"] is True for row in diagonal_rows
            ),
            "rows": diagonal_rows,
        },
        "outside_exhaustion": {
            "aggregate_cost": sum(outside_report_cost(member) for member in members),
            "cost_bound_per_target": REPORT_COST_BOUND,
            "cost_histogram": {
                str(cost): cost_histogram[cost] for cost in sorted(cost_histogram)
            },
            "rows": outside_rows,
            "terminal_false_count": terminal_histogram[False],
            "terminal_true_count": terminal_histogram[True],
        },
        "reporter_search": {
            "candidate_count_within_cost": sum(
                all(
                    candidate_run_cost(member, target) <= REPORT_COST_BOUND
                    for target in members
                )
                for member in members
            ),
            "cost_rule": "candidate_step_applications_plus_target_description_admissions",
            "complete_matrix": [_reporter_cell_json(cell) for cell in matrix],
            "matrix_cell_count": len(matrix),
            "successful_candidate_indices": list(reporter_winners),
            "terminal": (
                "DECIDER_WITHIN_COST_EXHIBITED"
                if reporter_winners
                else "DECIDER_REFUSED_WITHIN_COST"
            ),
            "within_cost_bound": REPORT_COST_BOUND,
        },
        "self_description": {
            "terminal": (
                "SELF_DESCRIBING_EXHIBITED"
                if self_witnesses
                else "SELF_DESCRIPTION_REFUSED_IN_CLASS"
            ),
            "witness_indices": list(self_witnesses),
        },
        "unbounded": "OPEN_UNBOUNDED",
    }
