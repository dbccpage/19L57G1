"""Bounded specialization recovering the historical 1,459-history prefix census.

Specializes general multi-sorted signatures and typed structures to the
historical binary-carrier setup from research/typed_translation/, proving
that the general typed translation framework strictly recovers the 1,459
valid history prefixes under exact operational transition commutation.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from typing import Iterable, Sequence

try:
    from codec import decode, encode, step_commutation_holds
    from signature import (
        AddElement,
        AddRelationTuple,
        RelationSymbol,
        Signature,
        TypedStructure,
        step as structure_step,
    )
except ImportError:
    from .codec import decode, encode, step_commutation_holds
    from .signature import (
        AddElement,
        AddRelationTuple,
        RelationSymbol,
        Signature,
        TypedStructure,
        step as structure_step,
    )


class HistoricalEvent(StrEnum):
    """The eight frozen source events from research/typed_translation/."""

    SUPPLY_D0 = "supply_d0"
    ADMIT_D0 = "admit_d0"
    SUPPLY_D1 = "supply_d1"
    ADMIT_D1 = "admit_d1"
    ADMIT_FORM = "admit_form"
    ADMIT_INST0 = "admit_inst0"
    ADMIT_INST1 = "admit_inst1"
    ADMIT_RULE = "admit_rule"


EVENT_ORDER: tuple[HistoricalEvent, ...] = tuple(HistoricalEvent)

# Canonical historical signature
HISTORICAL_SIGNATURE = Signature(
    sorts=("datum",),
    constants=(),
    relations=(
        RelationSymbol("Form", ()),
        RelationSymbol("Instance", ("datum",)),
        RelationSymbol("Rule", ()),
    ),
    functions=(),
)


@dataclass(frozen=True)
class SpecializedReplay:
    """Replay machine pairing a TypedStructure with presentation supply."""

    struct: TypedStructure
    supplied: frozenset[str] = frozenset()


def initial_replay() -> SpecializedReplay:
    """Construct the initial empty specialized replay state."""
    init_struct = TypedStructure.create(
        signature=HISTORICAL_SIGNATURE,
        carriers={"datum": ()},
        relations={"Form": (), "Instance": (), "Rule": ()},
    )
    return SpecializedReplay(struct=init_struct, supplied=frozenset())


def accepts(replay: SpecializedReplay, event: HistoricalEvent) -> bool:
    """Whether event is admissible in the specialized replay state."""
    s = replay.struct
    sup = replay.supplied
    data = set(s.carrier_for("datum"))
    has_form = () in s.tuples_for("Form")
    insts = {t[0] for t in s.tuples_for("Instance")}
    has_rule = () in s.tuples_for("Rule")

    if event is HistoricalEvent.SUPPLY_D0:
        return "0" not in sup
    if event is HistoricalEvent.SUPPLY_D1:
        return "1" not in sup
    if event is HistoricalEvent.ADMIT_D0:
        return "0" in sup and "0" not in data
    if event is HistoricalEvent.ADMIT_D1:
        return "1" in sup and "1" not in data
    if event is HistoricalEvent.ADMIT_FORM:
        return not has_form
    if event is HistoricalEvent.ADMIT_INST0:
        return has_form and "0" in data and "0" not in insts
    if event is HistoricalEvent.ADMIT_INST1:
        return has_form and "1" in data and "1" not in insts
    if event is HistoricalEvent.ADMIT_RULE:
        return has_form and not has_rule
    return False


def step_replay(replay: SpecializedReplay, event: HistoricalEvent) -> SpecializedReplay:
    """Transition the specialized replay machine by applying event."""
    if not accepts(replay, event):
        raise ValueError(f"Historical event '{event.value}' refused by specialized replay")

    s = replay.struct
    sup = replay.supplied

    if event is HistoricalEvent.SUPPLY_D0:
        return replace(replay, supplied=sup | {"0"})
    if event is HistoricalEvent.SUPPLY_D1:
        return replace(replay, supplied=sup | {"1"})
    if event is HistoricalEvent.ADMIT_D0:
        return replace(replay, struct=structure_step(s, AddElement("datum", "0")))
    if event is HistoricalEvent.ADMIT_D1:
        return replace(replay, struct=structure_step(s, AddElement("datum", "1")))
    if event is HistoricalEvent.ADMIT_FORM:
        return replace(replay, struct=structure_step(s, AddRelationTuple("Form", ())))
    if event is HistoricalEvent.ADMIT_INST0:
        return replace(replay, struct=structure_step(s, AddRelationTuple("Instance", ("0",))))
    if event is HistoricalEvent.ADMIT_INST1:
        return replace(replay, struct=structure_step(s, AddRelationTuple("Instance", ("1",))))
    if event is HistoricalEvent.ADMIT_RULE:
        return replace(replay, struct=structure_step(s, AddRelationTuple("Rule", ())))
    raise ValueError(f"Unhandled historical event: {event}")


History = tuple[HistoricalEvent, ...]


def canonical_history_order(histories: Iterable[History]) -> tuple[History, ...]:
    """Sort histories canonically by length and frozen event index."""
    order = {event: idx for idx, event in enumerate(EVENT_ORDER)}
    return tuple(sorted(histories, key=lambda h: (len(h), tuple(order[e] for e in h))))


def enumerate_specialized_histories() -> tuple[History, ...]:
    """Depth-first replay-closed prefix census in frozen event order."""
    result: list[History] = []

    def visit(history: History, replay: SpecializedReplay) -> None:
        result.append(history)
        for event in EVENT_ORDER:
            if event not in history and accepts(replay, event):
                visit(history + (event,), step_replay(replay, event))

    visit((), initial_replay())
    return canonical_history_order(result)


def replay_history(history: Sequence[HistoricalEvent]) -> SpecializedReplay:
    """Replay an event sequence from the initial specialized state."""
    replay = initial_replay()
    for event in history:
        replay = step_replay(replay, event)
    return replay


def verify_specialization_recovery() -> dict[str, object]:
    """Verify recovery of the 1,459-history prefix case and codec properties.

    Checks:
    1. Total valid prefix histories == 1459.
    2. Every reached structure encodes and round-trips via decode(encode(S)) == S.
    3. Every admitted step commutes with relational encoding.
    """
    histories = enumerate_specialized_histories()
    if len(histories) != 1459:
        raise AssertionError(f"Expected 1459 histories, found {len(histories)}")

    unique_structures: set[TypedStructure] = set()
    step_commutations_tested = 0

    for h in histories:
        replay = replay_history(h)
        unique_structures.add(replay.struct)

        # Check round-trip on reached structure
        encoded = encode(replay.struct)
        dec_res = decode(encoded)
        if not dec_res.is_ok() or dec_res.unwrap() != replay.struct:
            raise AssertionError(f"Roundtrip failed for history {h}")

        # Check commutation on all admissible extensions
        for next_event in EVENT_ORDER:
            if next_event not in h and accepts(replay, next_event):
                # If it's an admission step (modifies structure), check commutation
                s_before = replay.struct
                rep_after = step_replay(replay, next_event)
                s_after = rep_after.struct
                if s_after != s_before:
                    # Find which StructureOp was executed
                    op = None
                    if next_event is HistoricalEvent.ADMIT_D0:
                        op = AddElement("datum", "0")
                    elif next_event is HistoricalEvent.ADMIT_D1:
                        op = AddElement("datum", "1")
                    elif next_event is HistoricalEvent.ADMIT_FORM:
                        op = AddRelationTuple("Form", ())
                    elif next_event is HistoricalEvent.ADMIT_INST0:
                        op = AddRelationTuple("Instance", ("0",))
                    elif next_event is HistoricalEvent.ADMIT_INST1:
                        op = AddRelationTuple("Instance", ("1",))
                    elif next_event is HistoricalEvent.ADMIT_RULE:
                        op = AddRelationTuple("Rule", ())

                    if op is not None:
                        if not step_commutation_holds(s_before, op):
                            raise AssertionError(f"Commutation failed on step {next_event} from {h}")
                        step_commutations_tested += 1

    return {
        "histories_count": len(histories),
        "unique_structures_count": len(unique_structures),
        "step_commutations_tested": step_commutations_tested,
        "roundtrip_all_passed": True,
    }
