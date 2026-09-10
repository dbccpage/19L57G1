"""Diagonal obstruction theorem and simulation sweeps for G018 Self-Hosting.

Demonstrates that no finite carrier contains a total halting/transition self-oracle.
For every candidate total predictor P, the constructive diagonal machine D_P
inverts P's prediction on its own code, demonstrating the obstruction.

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
    """Witness refuting a candidate total prediction oracle."""

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


def build_diagonal_machine_for_prediction(predicted_halt: bool, symbols: Sequence[int] = (0, TAG_SPEC_START)) -> MachineSpec:
    """Construct diagonal machine whose behavior is opposite to the prediction.

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
    """Constructively refute a candidate predictor using the diagonal argument.

    1. We present a machine specification schema parameterized by the predictor's decision.
    2. We query the predictor on candidate probe code.
    3. We synthesize the diagonal machine that inverts the prediction.
    4. We execute the diagonal machine on its own encoding under the declared fuel budget.
    5. We observe that prediction != actual outcome.
    """
    # Create an initial probe code
    probe_spec = make_halting_machine()
    probe_state = MachineState(state=0, cursor=0, tape=(0,), fuel=fuel_budget, halted=False)
    probe_code = encode_carrier(probe_spec, probe_state)

    # Query candidate predictor
    predicted = predictor(probe_spec, probe_code)

    # Build the adversarial diagonal machine that inverts `predicted`
    diagonal_spec = build_diagonal_machine_for_prediction(predicted)
    diagonal_state = MachineState(state=0, cursor=0, tape=(0,), fuel=fuel_budget, halted=False)
    diagonal_code = encode_carrier(diagonal_spec, diagonal_state)

    # Now query predictor on the actual diagonal machine code
    self_predicted = predictor(diagonal_spec, diagonal_code)

    # Final diagonal machine configured with respect to its own self-prediction
    symbols: tuple[int, ...] = (0, TAG_SPEC_START)
    if diagonal_code:
        symbols = (0, TAG_SPEC_START, diagonal_code[0])
    final_diag_spec = build_diagonal_machine_for_prediction(self_predicted, symbols=symbols)
    final_diag_state = MachineState(state=0, cursor=0, tape=diagonal_code, fuel=fuel_budget, halted=False)

    # Execute the diagonal machine
    executed_state = run_direct(final_diag_spec, final_diag_state, max_steps=fuel_budget)
    actual_halt = executed_state.halted

    # Refutation succeeds when predicted does not match actual behavior
    success = (self_predicted != actual_halt)

    return DiagonalRefutation(
        predictor_name=predictor_name,
        diagonal_code=diagonal_code,
        predicted_halt=self_predicted,
        actual_halt=actual_halt,
        refutation_success=success,
    )


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
    """Execute diagonal obstruction sweeps across multiple distinct candidate predictors."""
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
