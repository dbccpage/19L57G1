"""Quantitative rational frequency bounds on cycle programs and chain functionality showing topological non-density in this setting.

AuthorityEffect: None.
Mirrors Lean 4 constructive formalization in RationalBounds.lean.

Key concepts:
- Cycle Program Readout:
    Program visits 0 -> 1 -> 2 -> 0 -> ...
    zeros(L) is the count of datum 0 among first L entries of i |-> i % 3.
    Exact closed form: zeros(L) = (L + 2) // 3.
- Quantitative Rational Frequency Bound:
    L <= 3 * zeros(L) <= L + 2.
    Error budget in Q: |zeros(L) / L - 1/3| <= 2 / (3 * L).
    Precision budget: for any rational epsilon > 0, L >= ceil(2 / (3 * epsilon)) ensures error <= epsilon.
    Pure arithmetic in Q; zero reliance on real continuum (R).
- Chain Functionality & Topological Non-Density:
    Every deterministic tape is a chain where each entry's successor is a function of the datum.
    TWIST_TAPE = (0, 1, 0, 2) contains pairs (0, 1) and (0, 2). Since 1 != 2, it is not functional.
    No deterministic program can realize TWIST_TAPE.
    The open cylinder U_{[0, 1, 0, 2]} contains zero realized process tapes, showing topological non-density in this setting.
- Refusal of Unconstructed Completions:
    Explicit refusal to identify discrete thread spaces with R or circle S^1 without explicit construction.
"""

from __future__ import annotations

from fractions import Fraction
import math
from typing import Callable, Sequence

from limits import Word
from observe import State, make_cycle_graph, obs

TWIST_TAPE: Word = (0, 1, 0, 2)


class CompletionRefusal(ValueError):
    """Refusal to promote discrete limits into ungrounded continua or circle quotients."""


def cyc_step(x: int) -> int:
    """The 3-element cycle step: 0 -> 1 -> 2 -> 0."""
    return (x + 1) % 3


def cyc_tape(n: int) -> Word:
    """The first n + 1 entries of the cycle sequence i |-> i % 3."""
    return tuple(i % 3 for i in range(n + 1))


def zeros(length: int) -> int:
    """Number of zeros among the first `length` entries of i |-> i % 3."""
    return sum(1 for i in range(length) if i % 3 == 0)


def zeros_closed_form(length: int) -> int:
    """Constructive closed form: (L + 2) // 3."""
    return (length + 2) // 3


def verify_zeros_bounds(length: int) -> bool:
    """Verify that L <= 3 * zeros(L) <= L + 2 for a given length."""
    z = zeros(length)
    return length <= 3 * z <= length + 2


def rational_frequency(length: int) -> Fraction:
    """Rational frequency of datum 0 in first `length` entries."""
    if length <= 0:
        raise ValueError("Length must be positive for frequency evaluation")
    return Fraction(zeros(length), length)


def rational_frequency_error(length: int) -> Fraction:
    """Rational difference |zeros(L)/L - 1/3|."""
    return abs(rational_frequency(length) - Fraction(1, 3))


def verify_rational_error_bound(length: int) -> bool:
    """Verify that |zeros(L)/L - 1/3| <= 2 / (3 * L) in Q."""
    if length <= 0:
        return True
    error = rational_frequency_error(length)
    budget = Fraction(2, 3 * length)
    return error <= budget


def precision_budget(epsilon: Fraction) -> int:
    """Calculate minimum scale length L in Q such that error <= epsilon."""
    if epsilon <= 0:
        raise ValueError("Epsilon must be positive")
    # 2 / (3 * L) <= epsilon  <=>  L >= 2 / (3 * epsilon)
    threshold = Fraction(2, 3) / epsilon
    return max(1, math.ceil(threshold.numerator / threshold.denominator))


def pairs_of(tape: Sequence[int]) -> list[tuple[int, int]]:
    """Consecutive transition pairs (x_i, x_{i+1}) of a tape."""
    return [(tape[i], tape[i + 1]) for i in range(len(tape) - 1)]


def is_functional(pairs: Sequence[tuple[int, int]]) -> bool:
    """Check whether pairs define a single-valued function:
    (x, y) in pairs and (x, z) in pairs => y == z.
    """
    seen: dict[int, int] = {}
    for x, y in pairs:
        if x in seen:
            if seen[x] != y:
                return False
        else:
            seen[x] = y
    return True


def is_chain(next_func: Callable[[int], int | None], tape: Sequence[int]) -> bool:
    """Whether tape is a valid chain of the transition function."""
    for x, y in pairs_of(tape):
        if next_func(x) != y:
            return False
    return True


def verify_twist_tape_not_functional() -> bool:
    """Confirm TWIST_TAPE = (0, 1, 0, 2) is not functional."""
    pairs = pairs_of(TWIST_TAPE)
    return not is_functional(pairs)


def run_cycle_program(n_steps: int) -> tuple[Word, int, Fraction, bool]:
    """Execute the Target A cycle program from datum 0 with fuel >= n_steps,
    returning observed tape, zero count, frequency in Q, and bound satisfaction.
    """
    cycle_graph = make_cycle_graph()
    state = State(graph=cycle_graph, nops=3, active=0, tape=(0,), clock=0, fuel=n_steps)
    tape = obs(n_steps, state)
    length = len(tape)
    z_count = sum(1 for x in tape if x == 0)
    freq = Fraction(z_count, length)
    bound_ok = length <= 3 * z_count <= length + 2
    return tape, z_count, freq, bound_ok


def refuse_continuum_completion(claim: str) -> None:
    """Refuse claims that discrete thread spaces constitute R without Dedekind/Cauchy construction."""
    raise CompletionRefusal(
        f"Refused continuum completion: '{claim}'. "
        "The thread space under discrete finite observation maps is totally disconnected. "
        "Recovery of the real continuum R requires explicit Dedekind cuts or Cauchy completions."
    )


def refuse_circle_quotient(claim: str) -> None:
    """Refuse claims that the 3-element cycle program yields the continuous circle S^1 without quotient."""
    raise CompletionRefusal(
        f"Refused circle completion: '{claim}'. "
        "The cycle program operates on discrete carrier {0, 1, 2}. "
        "No topological quotient map or continuous character embedding into S^1 is constructed."
    )


def refuse_dyadic_quotient(claim: str) -> None:
    """Refuse identifying dyadic twins without an explicit declared quotient adapter."""
    raise CompletionRefusal(
        f"Refused dyadic twin identification: '{claim}'. "
        "The sequences 0111... and 1000... are separated at scale 1. "
        "They remain distinct threads unless an explicit adapter quotient is declared."
    )
