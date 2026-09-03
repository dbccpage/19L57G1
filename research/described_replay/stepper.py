"""One-event described-state transition for ``DR-C-2-1-3``."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from description import (
    CLASS_LENGTH_BOUND,
    DecodeInvalid,
    DecodeResult,
    DecodeValid,
    Description,
    DescriptionInput,
    EMPTY,
    Event,
    Regime,
    prepare_description,
    prepared_decode_is_valid,
    step as apply_event,
)


@dataclass(frozen=True)
class DescribedState:
    """The frozen described-state triple."""

    description: DescriptionInput
    pointer: int
    regime: Regime


@dataclass(frozen=True)
class PreparedState:
    """Metatheoretic preparation evidence paired with a described state.

    The witness is deliberately outside ``DescribedState``: it is execution
    evidence, not another field of the described object.
    """

    described: DescribedState
    preparation: DecodeResult | None

    @property
    def description(self) -> DescriptionInput:
        return self.described.description

    @property
    def pointer(self) -> int:
        return self.described.pointer

    @property
    def regime(self) -> Regime:
        return self.described.regime


StepperInput: TypeAlias = DescribedState | PreparedState


@dataclass(frozen=True)
class Step:
    """One event was consumed, including an inert presentation event."""

    event: Event
    state: PreparedState


@dataclass(frozen=True)
class Done:
    """The pointer is exactly at the decoded history length."""

    state: PreparedState


@dataclass(frozen=True)
class Invalid:
    """The description, pointer, or recorded prefix state is invalid."""

    state: PreparedState
    reason: str


StepperResult: TypeAlias = Step | Done | Invalid


def initial_state(description: DescriptionInput) -> PreparedState:
    """Prepare a supplied description once at the declared genesis state."""

    return initial_state_from_preparation(
        description, prepare_description(description)
    )


def initial_state_from_preparation(
    description: DescriptionInput, preparation: DecodeResult
) -> PreparedState:
    """Attach already-computed metatheoretic evidence to the state triple."""

    return PreparedState(DescribedState(description, 0, EMPTY), preparation)


def _witness_matches_description(
    prepared: DecodeValid, description: DescriptionInput
) -> bool:
    if isinstance(description, Description):
        return prepared.description == description
    return prepared.description.regime == description


def _prepared_input(state: StepperInput) -> PreparedState:
    if isinstance(state, PreparedState):
        return state
    return PreparedState(state, None)


def _validated_witness(execution: PreparedState) -> DecodeValid | Invalid:
    prepared = execution.preparation
    if prepared is None:
        return Invalid(execution, "description has not been prepared")
    if isinstance(prepared, DecodeInvalid):
        return Invalid(execution, prepared.reason)
    if not prepared_decode_is_valid(prepared):
        return Invalid(execution, "prepared decode witness failed integrity")
    if not _witness_matches_description(prepared, execution.description):
        return Invalid(
            execution, "prepared witness belongs to another description"
        )
    return prepared


def step_described(state: StepperInput) -> StepperResult:
    """Check a prepared prefix and consume at most the pointed-to event."""

    execution = _prepared_input(state)
    prepared = _validated_witness(execution)
    if isinstance(prepared, Invalid):
        return prepared
    if execution.pointer < 0:
        return Invalid(execution, "pointer is negative")
    history_length = len(prepared.process.events)
    if execution.pointer > history_length:
        return Invalid(execution, "pointer is beyond the decoded history")
    if execution.regime != prepared.prefixes[execution.pointer]:
        return Invalid(
            execution, "recorded regime is not the decoded prefix fold"
        )
    if execution.pointer == history_length:
        return Done(execution)

    event = prepared.process.events[execution.pointer]
    next_regime = apply_event(execution.regime, event)
    return Step(
        event,
        PreparedState(
            DescribedState(
                execution.description,
                execution.pointer + 1,
                next_regime,
            ),
            prepared,
        ),
    )


def consume_prepared_events(
    state: StepperInput,
) -> PreparedState | Invalid:
    """Consume exactly the remaining decoded events, with no ``Done`` call.

    This is the costed execution helper: each remaining event yields exactly
    one successful ``step_described`` application.  Preparation and the final
    completion observation are outside that event count.
    """

    current = _prepared_input(state)
    prepared = _validated_witness(current)
    if isinstance(prepared, Invalid):
        return prepared
    if current.pointer < 0 or current.pointer > len(prepared.process.events):
        return Invalid(current, "pointer is outside the decoded history")
    if current.regime != prepared.prefixes[current.pointer]:
        return Invalid(current, "recorded regime is not the decoded prefix fold")
    remaining = len(prepared.process.events) - current.pointer
    for _ in range(remaining):
        result = step_described(current)
        if not isinstance(result, Step):
            if isinstance(result, Invalid):
                return result
            return Invalid(current, "event consumption ended before a step")
        current = result.state
    return current


def iterate_stepper(
    state: StepperInput,
    application_bound: int = CLASS_LENGTH_BOUND + 1,
) -> tuple[StepperResult, ...]:
    """Apply the stepper repeatedly, retaining every tagged result.

    The default bound is sufficient to consume any class history and observe
    its final ``Done`` tag.  Iteration stops immediately at ``Done`` or
    ``Invalid``.
    """

    if application_bound < 0:
        return (
            Invalid(_prepared_input(state), "application bound is negative"),
        )
    results: list[StepperResult] = []
    current = state
    for _ in range(application_bound):
        result = step_described(current)
        results.append(result)
        if not isinstance(result, Step):
            break
        current = result.state
    return tuple(results)


def terminal_result(state: StepperInput) -> Done | Invalid:
    """Run the finite state to its first terminal tag."""

    results = iterate_stepper(state)
    if not results:
        return Invalid(_prepared_input(state), "no stepper application was made")
    final = results[-1]
    if isinstance(final, Step):
        return Invalid(final.state, "application bound ended before a tag")
    return final


def stepper_total(state: StepperInput) -> bool:
    """Executable witness that every input receives exactly one tag."""

    return isinstance(step_described(state), (Step, Done, Invalid))
