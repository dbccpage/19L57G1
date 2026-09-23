"""Finite same-code counterexamples for selected predictor functions.

The Lean module proves a conditional boolean self-negation contradiction. This
Python sweep finds concrete prediction errors on the exact machine and code
executed. It does not construct a self-referential fixed point or refute every
possible total predictor.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

from carrier_repr import (
    TAG_SPEC_START,
    MachineSpec,
    MachineState,
    Transition,
    encode_carrier,
    run_direct,
    step_direct,
)


# Type alias for candidate total halting/transition predictors
PredictorFn = Callable[[MachineSpec, tuple[int, ...]], bool]


@dataclass(frozen=True)
class DiagonalRefutation:
    """Bounded witness for a named predictor; historical class name retained."""

    predictor_name: str
    diagonal_code: tuple[int, ...]
    predicted_halt: bool
    actual_halt: bool
    refutation_success: bool


def make_looping_machine(symbols: Sequence[int] = (0, TAG_SPEC_START)) -> MachineSpec:
    """Machine that cycles indefinitely between states 1 and 2 for any symbol in `symbols`."""
    trans_list: list[Transition] = []
    for s in set(symbols):
        trans_list.append(Transition(curr_state=0, read_sym=s, next_state=1, write_sym=s, move_cursor=0, halt=False))
        trans_list.append(Transition(curr_state=1, read_sym=s, next_state=2, write_sym=s, move_cursor=0, halt=False))
        trans_list.append(Transition(curr_state=2, read_sym=s, next_state=1, write_sym=s, move_cursor=0, halt=False))
    return MachineSpec(transitions=tuple(trans_list), default_sym=0)


def make_halting_machine(symbols: Sequence[int] = (0, TAG_SPEC_START)) -> MachineSpec:
    """Machine that halts immediately for any symbol in `symbols`."""
    trans_list: list[Transition] = []
    for s in set(symbols):
        trans_list.append(Transition(curr_state=0, read_sym=s, next_state=1, write_sym=s, move_cursor=0, halt=True))
    return MachineSpec(transitions=tuple(trans_list), default_sym=0)


def make_delayed_halting_machine(steps: int, symbols: Sequence[int] = (0, TAG_SPEC_START)) -> MachineSpec:
    """Halt on the given positive step count while staying on one tape cell."""
    if steps < 1:
        raise ValueError("steps must be positive")
    transitions = tuple(
        Transition(
            curr_state=i, read_sym=s, next_state=i + 1,
            write_sym=s, move_cursor=0, halt=(i + 1 == steps),
        )
        for i in range(steps) for s in sorted(set(symbols))
    )
    return MachineSpec(transitions=transitions, default_sym=0)


def make_unreachable_halt_machine(symbols: Sequence[int] = (0, TAG_SPEC_START)) -> MachineSpec:
    """Loop from state zero despite a syntactically present halt edge."""
    loop = make_looping_machine(symbols)
    unreachable = tuple(
        Transition(
            curr_state=99, read_sym=s, next_state=100,
            write_sym=s, move_cursor=0, halt=True,
        )
        for s in sorted(set(symbols))
    )
    return MachineSpec(transitions=loop.transitions + unreachable, default_sym=0)


def build_diagonal_machine_for_prediction(predicted_halt: bool, symbols: Sequence[int] = (0, TAG_SPEC_START)) -> MachineSpec:
    """Construct an opposite-behavior machine from a supplied prediction.

    This construction alone does not refute a predictor: the prediction may
    have been made for a different machine.

    If predicted_halt is True:
        The machine MUST NOT halt (enters an infinite cycle between state 1 and 2).
    If predicted_halt is False:
        The machine MUST halt immediately (state 0 -> state 1 with halt=True).
    """
    if predicted_halt:
        # Predictor said: "halts" -> Diagonal machine LOOPS
        return make_looping_machine(symbols=symbols)
    else:
        # Predictor said: "does not halt" -> Diagonal machine HALTS
        return make_halting_machine(symbols=symbols)


def evaluate_diagonal_obstruction(
    predictor_name: str,
    predictor: PredictorFn,
    fuel_budget: int = 100,
) -> DiagonalRefutation:
    """Search finite probes for an error on the very code given to predictor.

    `refutation_success` says only that this named predictor failed on a
    member of the bounded probe family. An exact predictor for this finite
    family can return False here without contradiction.
    """
    if fuel_budget < 1:
        raise ValueError("fuel_budget must be positive")
    probes = [make_looping_machine(), make_halting_machine(), make_unreachable_halt_machine()]
    probes.extend(make_delayed_halting_machine(n) for n in range(2, fuel_budget + 1))
    last: DiagonalRefutation | None = None
    for spec in probes:
        initial = MachineState(state=0, cursor=0, tape=(0,), fuel=fuel_budget, halted=False)
        code = encode_carrier(spec, initial)
        predicted = predictor(spec, code)
        execution = MachineState(state=0, cursor=0, tape=code, fuel=fuel_budget, halted=False)
        actual = run_direct(spec, execution, max_steps=fuel_budget).halted
        last = DiagonalRefutation(
            predictor_name=predictor_name,
            diagonal_code=code,
            predicted_halt=predicted,
            actual_halt=actual,
            refutation_success=(predicted != actual),
        )
        if last.refutation_success:
            return last
    assert last is not None
    return last


# --- Suite of Candidate Heuristic Predictors to Sweep ---

def predictor_always_halt(spec: MachineSpec, tape: tuple[int, ...]) -> bool:
    """Trivial oracle: predicts everything halts."""
    return True


def predictor_never_halt(spec: MachineSpec, tape: tuple[int, ...]) -> bool:
    """Trivial oracle: predicts nothing halts."""
    return False


def make_bounded_step_predictor(cutoff: int) -> PredictorFn:
    """Simulates up to cutoff steps: if halted by then, predicts True, else False."""
    def predictor(spec: MachineSpec, tape: tuple[int, ...]) -> bool:
        st = MachineState(state=0, cursor=0, tape=tape, fuel=cutoff, halted=False)
        end_st = run_direct(spec, st, max_steps=cutoff)
        return end_st.halted
    return predictor


def predictor_has_halt_transition(spec: MachineSpec, tape: tuple[int, ...]) -> bool:
    """Syntactic oracle: checks if any transition has halt=True."""
    return any(t.halt for t in spec.transitions)


def sweep_candidate_predictors(fuel_budget: int = 50) -> list[DiagonalRefutation]:
    """Find bounded same-code errors for the listed heuristic predictors."""
    candidates: list[tuple[str, PredictorFn]] = [
        ("AlwaysHaltOracle", predictor_always_halt),
        ("NeverHaltOracle", predictor_never_halt),
        ("SyntacticHaltEdgeOracle", predictor_has_halt_transition),
        ("BoundedStepOracle_k1", make_bounded_step_predictor(1)),
        ("BoundedStepOracle_k5", make_bounded_step_predictor(5)),
        ("BoundedStepOracle_k10", make_bounded_step_predictor(10)),
        ("BoundedStepOracle_k25", make_bounded_step_predictor(25)),
    ]

    results: list[DiagonalRefutation] = []
    for name, pred in candidates:
        ref = evaluate_diagonal_obstruction(name, pred, fuel_budget=fuel_budget)
        results.append(ref)

    return results
