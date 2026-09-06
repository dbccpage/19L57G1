"""Unpruned source-history and translation-candidate censuses."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from typing import Iterable, Iterator

from .model import EVENT_ORDER, SourceEvent, SourceReplay, SourceState, source_accepts, source_step


History = tuple[SourceEvent, ...]


def enumerate_histories() -> tuple[History, ...]:
    """Depth-first replay-closed prefix census in frozen event order."""

    result: list[History] = []

    def visit(history: History, replay: SourceReplay) -> None:
        result.append(history)
        for event in EVENT_ORDER:
            if event not in history and source_accepts(replay, event):
                visit(history + (event,), source_step(replay, event))

    visit((), SourceReplay())
    return canonical_history_order(result)


def enumerate_histories_unpruned() -> tuple[History, ...]:
    """Independent permutation-of-subsets census, filtered only by replay."""

    accepted: list[History] = []
    for length in range(len(EVENT_ORDER) + 1):
        for history in permutations(EVENT_ORDER, length):
            replay = SourceReplay()
            for event in history:
                if not source_accepts(replay, event):
                    break
                replay = source_step(replay, event)
            else:
                accepted.append(history)
    order = {event: index for index, event in enumerate(EVENT_ORDER)}
    return tuple(sorted(accepted, key=lambda h: (len(h), tuple(order[e] for e in h))))


def canonical_history_order(histories: Iterable[History]) -> tuple[History, ...]:
    order = {event: index for index, event in enumerate(EVENT_ORDER)}
    return tuple(sorted(histories, key=lambda h: (len(h), tuple(order[e] for e in h))))


def unique_states(histories: Iterable[History]) -> tuple[SourceState, ...]:
    from .model import replay_source

    states = {replay_source(history).state for history in histories}
    return tuple(
        sorted(
            states,
            key=lambda state: (
                tuple(sorted(state.data)),
                state.form,
                tuple(sorted(state.instances)),
                state.rule,
            ),
        )
    )


@dataclass(frozen=True, order=True)
class Candidate:
    event_context: str
    synthetic_supply: bool
    outer_exchange: bool
    mark_permutations: bool
    keep_labels: bool
    tag_levels_named: bool
    address_family: str

    def coordinates(self) -> tuple[object, ...]:
        return (
            self.event_context,
            self.synthetic_supply,
            self.outer_exchange,
            self.mark_permutations,
            self.keep_labels,
            self.tag_levels_named,
            self.address_family,
        )

    def as_record(self) -> dict[str, object]:
        return {
            "address_family": self.address_family,
            "event_context": self.event_context,
            "keep_labels": self.keep_labels,
            "mark_permutations": self.mark_permutations,
            "outer_exchange": self.outer_exchange,
            "synthetic_supply": self.synthetic_supply,
            "tag_levels_named": self.tag_levels_named,
        }


COORDINATE_VALUES: tuple[tuple[object, ...], ...] = (
    ("memoryless", "state_sensitive"),
    (False, True),
    (False, True),
    (False, True),
    (False, True),
    (False, True),
    ("direct", "complemented"),
)


def _candidate(values: tuple[object, ...]) -> Candidate:
    return Candidate(
        event_context=str(values[0]),
        synthetic_supply=bool(values[1]),
        outer_exchange=bool(values[2]),
        mark_permutations=bool(values[3]),
        keep_labels=bool(values[4]),
        tag_levels_named=bool(values[5]),
        address_family=str(values[6]),
    )


def enumerate_candidates() -> tuple[Candidate, ...]:
    """Recursive Cartesian enumerator; no candidate is evaluated or pruned."""

    result: list[Candidate] = []

    def visit(axis: int, prefix: tuple[object, ...]) -> None:
        if axis == len(COORDINATE_VALUES):
            result.append(_candidate(prefix))
            return
        for value in COORDINATE_VALUES[axis]:
            visit(axis + 1, prefix + (value,))

    visit(0, ())
    return tuple(result)


def enumerate_candidates_product() -> tuple[Candidate, ...]:
    """Independent standard-library product cross-check."""

    return tuple(_candidate(tuple(values)) for values in product(*COORDINATE_VALUES))


def iter_permutations(items: tuple[object, ...]) -> Iterator[tuple[object, ...]]:
    """Small public wrapper used by negative and census tests."""

    yield from permutations(items)
