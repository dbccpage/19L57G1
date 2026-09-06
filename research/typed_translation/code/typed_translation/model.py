"""Typed source and boundary carriers for the bounded translation experiment.

This is an independent kernel.  It deliberately imports no implementation
from the sealed package or from another research tree.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from typing import Iterable


class SourceEvent(StrEnum):
    """The eight frozen source events, in their declared census order."""

    SUPPLY_D0 = "supply_d0"
    ADMIT_D0 = "admit_d0"
    SUPPLY_D1 = "supply_d1"
    ADMIT_D1 = "admit_d1"
    ADMIT_FORM = "admit_form"
    ADMIT_INST0 = "admit_inst0"
    ADMIT_INST1 = "admit_inst1"
    ADMIT_RULE = "admit_rule"


EVENT_ORDER: tuple[SourceEvent, ...] = tuple(SourceEvent)


@dataclass(frozen=True)
class SourceState:
    """The admitted source state; presentation supply is not a state field."""

    data: frozenset[int] = frozenset()
    form: bool = False
    instances: frozenset[int] = frozenset()
    rule: bool = False

    def profile(self, datum: int) -> bool:
        """The one-bit observation, without discarding its source fields."""

        if datum not in (0, 1):
            raise ValueError(f"datum must be zero or one, got {datum}")
        return self.rule or datum in self.instances

    def task(self) -> bool | None:
        """Separation verdict, or ``None`` before both subjects are admitted."""

        if self.data != frozenset({0, 1}):
            return None
        return self.profile(0) != self.profile(1)

    def as_record(self) -> dict[str, object]:
        return {
            "data": sorted(self.data),
            "form": self.form,
            "instances": sorted(self.instances),
            "profile": [self.profile(i) for i in (0, 1)],
            "rule": self.rule,
            "task": self.task(),
        }


@dataclass(frozen=True)
class SourceReplay:
    """Replay state plus the metatheoretic supply needed for admission guards."""

    state: SourceState = SourceState()
    supplied: frozenset[int] = frozenset()


class SourceRefusal(ValueError):
    """A source event was not accepted by the frozen replay rule."""


def source_kind(event: SourceEvent) -> "RawKind":
    if event in (SourceEvent.SUPPLY_D0, SourceEvent.SUPPLY_D1):
        return RawKind.PRESENTATION
    return RawKind.ADMISSION


def source_label(event: SourceEvent) -> str:
    return {
        SourceEvent.SUPPLY_D0: "d0",
        SourceEvent.ADMIT_D0: "d0",
        SourceEvent.SUPPLY_D1: "d1",
        SourceEvent.ADMIT_D1: "d1",
        SourceEvent.ADMIT_FORM: "form",
        SourceEvent.ADMIT_INST0: "inst_0",
        SourceEvent.ADMIT_INST1: "inst_1",
        SourceEvent.ADMIT_RULE: "rule",
    }[event]


def source_accepts(replay: SourceReplay, event: SourceEvent) -> bool:
    """Whether ``event`` may be appended to the replay prefix."""

    state = replay.state
    supplied = replay.supplied
    if event is SourceEvent.SUPPLY_D0:
        return 0 not in supplied
    if event is SourceEvent.SUPPLY_D1:
        return 1 not in supplied
    if event is SourceEvent.ADMIT_D0:
        return 0 in supplied and 0 not in state.data
    if event is SourceEvent.ADMIT_D1:
        return 1 in supplied and 1 not in state.data
    if event is SourceEvent.ADMIT_FORM:
        return not state.form
    if event is SourceEvent.ADMIT_INST0:
        return state.form and 0 in state.data and 0 not in state.instances
    if event is SourceEvent.ADMIT_INST1:
        return state.form and 1 in state.data and 1 not in state.instances
    if event is SourceEvent.ADMIT_RULE:
        return state.form and not state.rule
    raise AssertionError(f"unhandled event {event}")


def source_step(replay: SourceReplay, event: SourceEvent) -> SourceReplay:
    """Apply one accepted source event."""

    if not source_accepts(replay, event):
        raise SourceRefusal(f"source replay refused {event.value}")
    state = replay.state
    supplied = replay.supplied
    if event is SourceEvent.SUPPLY_D0:
        return replace(replay, supplied=supplied | {0})
    if event is SourceEvent.SUPPLY_D1:
        return replace(replay, supplied=supplied | {1})
    if event is SourceEvent.ADMIT_D0:
        return replace(replay, state=replace(state, data=state.data | {0}))
    if event is SourceEvent.ADMIT_D1:
        return replace(replay, state=replace(state, data=state.data | {1}))
    if event is SourceEvent.ADMIT_FORM:
        return replace(replay, state=replace(state, form=True))
    if event is SourceEvent.ADMIT_INST0:
        return replace(replay, state=replace(state, instances=state.instances | {0}))
    if event is SourceEvent.ADMIT_INST1:
        return replace(replay, state=replace(state, instances=state.instances | {1}))
    if event is SourceEvent.ADMIT_RULE:
        return replace(replay, state=replace(state, rule=True))
    raise AssertionError(f"unhandled event {event}")


def replay_source(history: Iterable[SourceEvent]) -> SourceReplay:
    replay = SourceReplay()
    for event in history:
        replay = source_step(replay, event)
    return replay


class RawKind(StrEnum):
    PRESENTATION = "PRESENTATION"
    ADMISSION = "ADMISSION"


@dataclass(frozen=True, order=True)
class Mark:
    """A provenance label at one three-bit deep address."""

    label: str
    address: tuple[int, ...]

    def as_record(self) -> dict[str, object]:
        return {"address": list(self.address), "label": self.label}


@dataclass(frozen=True)
class BoundaryState:
    marks: frozenset[Mark] = frozenset()

    def as_record(self) -> dict[str, object]:
        return {"marks": [mark.as_record() for mark in sorted(self.marks)]}


@dataclass(frozen=True)
class RawEvent:
    """The one common raw-event protocol used by both cost measures."""

    kind: RawKind
    label: str
    mark: Mark | None = None

    def as_record(self) -> dict[str, object]:
        result: dict[str, object] = {"kind": self.kind.value, "label": self.label}
        if self.mark is not None:
            result["mark"] = self.mark.as_record()
        return result


@dataclass(frozen=True)
class Transaction:
    kind: RawKind
    raw: tuple[RawEvent, ...]

    def as_record(self) -> dict[str, object]:
        return {
            "kind": self.kind.value,
            "raw": [event.as_record() for event in self.raw],
        }


@dataclass(frozen=True)
class BoundaryReplay:
    state: BoundaryState = BoundaryState()
    presented: frozenset[str] = frozenset()


class BoundaryRefusal(ValueError):
    """A typed transaction or raw boundary event violates its grammar."""


def replay_boundary(transactions: Iterable[Transaction]) -> BoundaryReplay:
    """Replay transactions while retaining supply only as an admission guard."""

    replay = BoundaryReplay()
    for transaction in transactions:
        if not transaction.raw:
            raise BoundaryRefusal("EMPTY_TRANSACTION")
        admissions = sum(event.kind is RawKind.ADMISSION for event in transaction.raw)
        if transaction.kind is RawKind.PRESENTATION:
            if len(transaction.raw) != 1 or admissions:
                raise BoundaryRefusal("PRESENTATION_KIND_MISMATCH")
        elif admissions == 0:
            raise BoundaryRefusal("ADMISSION_WITHOUT_RAW_ADMISSION")

        presented = set(replay.presented)
        marks = set(replay.state.marks)
        previous: RawEvent | None = None
        for raw in transaction.raw:
            if raw.kind is RawKind.PRESENTATION:
                if raw.mark is not None:
                    raise BoundaryRefusal("PRESENTATION_CARRIES_MARK")
                presented.add(raw.label)
            else:
                if transaction.kind is not RawKind.ADMISSION or raw.mark is None:
                    raise BoundaryRefusal("ADMISSION_KIND_MISMATCH")
                paired = (
                    previous is not None
                    and previous.kind is RawKind.PRESENTATION
                    and previous.label == raw.label
                )
                if raw.label not in presented and not paired:
                    raise BoundaryRefusal("UNPRESENTED_LABEL")
                if raw.mark.label != raw.label:
                    raise BoundaryRefusal("LABEL_MARK_MISMATCH")
                if raw.mark in marks:
                    raise BoundaryRefusal("DUPLICATE_MARK")
                marks.add(raw.mark)
            previous = raw
        replay = BoundaryReplay(BoundaryState(frozenset(marks)), frozenset(presented))
    return replay


def flatten_transactions(transactions: Iterable[Transaction]) -> tuple[RawEvent, ...]:
    return tuple(raw for transaction in transactions for raw in transaction.raw)


def source_raw_trace(history: Iterable[SourceEvent]) -> tuple[RawEvent, ...]:
    return tuple(
        RawEvent(source_kind(event), source_label(event)) for event in history
    )


def measure(trace: Iterable[RawEvent], name: str) -> int:
    """The single implementation of each common measure for both carriers."""

    events = tuple(trace)
    if name == "mu1":
        return sum(event.kind is RawKind.ADMISSION for event in events)
    if name == "mu2":
        return len(events)
    raise ValueError(f"unknown measure {name!r}")
