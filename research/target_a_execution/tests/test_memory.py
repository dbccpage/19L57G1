"""Unit tests for retained internal records [p, x] and depth-2 ternary forms [b, p, x]."""

import pytest

from control import State
from memory import (
    TWIST2_TAPE,
    TWIST_TAPE,
    before,
    build_depth2_program,
    build_record_program,
    functional,
    previous,
    r2enabled,
    r2run_det,
    r2step_det,
    renabled,
    rrun_det,
    rstep_det,
    windows,
)
from runner import ExecutionError, Terminal


def test_previous_and_before_fallback() -> None:
    # Single element on tape
    s1 = State(graph=frozenset(), nops=1, active=0, tape=(0,), clock=0, fuel=5)
    assert previous(s1) == 0
    assert before(s1) == 0

    # Two elements on tape
    s2 = State(graph=frozenset(), nops=1, active=1, tape=(0, 1), clock=1, fuel=4)
    assert previous(s2) == 0
    assert before(s2) == 0

    # Three elements on tape
    s3 = State(graph=frozenset(), nops=1, active=2, tape=(0, 1, 2), clock=2, fuel=3)
    assert previous(s3) == 1
    assert before(s3) == 0

    # Four elements on tape
    s4 = State(graph=frozenset(), nops=1, active=3, tape=(0, 1, 2, 3), clock=3, fuel=2)
    assert previous(s4) == 2
    assert before(s4) == 1


def test_depth1_record_reading_twist() -> None:
    # 3 data, 2 ops:
    # Op 0: cycle (1, 2, 0)
    # Op 1: constant 0 (0, 0, 0)
    # Record enablements (p, x, op_k):
    # - At start: tape is (0,), previous=0, active=0.
    #   Enable op 0 at (0, 0): moves to 1 -> tape becomes (0, 1).
    # - Next: previous=0, active=1.
    #   Enable op 1 at (0, 1): moves to 0 -> tape becomes (0, 1, 0).
    # - Next: previous=1, active=0. Notice active is 0 again, but previous is 1!
    #   Enable op 1 at (1, 0): moves to 0 -> tape becomes (0, 1, 0, 0).
    hctrl = [
        (0, 0, 0),
        (0, 1, 1),
        (1, 0, 1),
    ]
    graph = build_record_program(
        n=3,
        ops=((1, 2, 0), (0, 0, 0)),
        hctrl=hctrl,
    )
    s = State(graph=graph, nops=2, active=0, tape=(0,), clock=0, fuel=3)
    term, final_s = rrun_det(3, s)
    assert term is Terminal.EXHAUSTED
    assert final_s.tape == (0, 1, 0, 0)
    assert final_s.clock == 3
    assert final_s.fuel == 0

    # Also test an enablement that halts: omit (1, 0, 1), so it halts at (0, 1, 0)
    hctrl_halting = [(0, 0, 0), (0, 1, 1)]
    g_halt = build_record_program(n=3, ops=((1, 2, 0), (0, 0, 0)), hctrl=hctrl_halting)
    s_halt = State(graph=g_halt, nops=2, active=0, tape=(0,), clock=0, fuel=10)
    term_h, final_h = rrun_det(10, s_halt)
    assert term_h is Terminal.HALT
    assert final_h.tape == (0, 1, 0)


def test_depth2_ternary_reading_twist2() -> None:
    # 3 data, 2 ops:
    # Op 0: cycle (1, 2, 0)
    # Op 1: constant 0 (0, 0, 0)
    # Target tape: 0, 1, 2, 0, 1, 0
    # Notice pair (0, 1) is followed by 2, then later by 0!
    # A depth-1 machine cannot do this; depth-2 uses ternary forms [b, p, x]:
    # (b, p, x):
    # start: (0, 0, 0) -> op 0 -> tape (0, 1)
    # (0, 0, 1) -> op 0 -> tape (0, 1, 2)
    # (0, 1, 2) -> op 0 -> tape (0, 1, 2, 0)
    # (1, 2, 0) -> op 0 -> tape (0, 1, 2, 0, 1)
    # Here, before is 2, previous is 0, active is 1: (2, 0, 1)
    # At (2, 0, 1) fire op 1 (constant 0) -> moves to 0! -> tape (0, 1, 2, 0, 1, 0)
    hctrl2 = [
        (0, 0, 0, 0),  # (0, 0, 0) -> 1
        (0, 0, 1, 0),  # (0, 0, 1) -> 2
        (0, 1, 2, 0),  # (0, 1, 2) -> 0
        (1, 2, 0, 0),  # (1, 2, 0) -> 1
        (2, 0, 1, 1),  # (2, 0, 1) -> 0 (diverges from earlier where (0, 1) -> 2)
    ]
    graph = build_depth2_program(
        n=3,
        ops=((1, 2, 0), (0, 0, 0)),
        hctrl2=hctrl2,
    )
    s = State(graph=graph, nops=2, active=0, tape=(0,), clock=0, fuel=10)
    term, final_s = r2run_det(10, s)
    assert term is Terminal.HALT
    assert final_s.tape == (0, 1, 2, 0, 1, 0)


def test_functionality_ceilings() -> None:
    # Memoryless ceiling:
    # TWIST_TAPE = (0, 1, 0, 0)
    # In TWIST_TAPE, 0 is followed by 1 at index 0, and by 0 at index 2.
    assert functional(1, TWIST_TAPE) is False
    # But in pairs: (0, 1) -> 0, (1, 0) -> 0. Each pair has a unique successor!
    assert functional(2, TWIST_TAPE) is True

    # Depth-1 pair ceiling:
    # TWIST2_TAPE = (0, 1, 2, 0, 1, 0)
    # In TWIST2_TAPE, pair (0, 1) is followed by 2, and later by 0.
    assert functional(2, TWIST2_TAPE) is False
    # But in triples: (0, 1, 2) -> 0, (1, 2, 0) -> 1, (2, 0, 1) -> 0.
    assert functional(3, TWIST2_TAPE) is True


def test_windows_and_edge_cases() -> None:
    tape = (0, 1, 2, 3)
    assert windows(2, tape) == ((0, 1), (1, 2), (2, 3))
    assert windows(4, tape) == ((0, 1, 2, 3),)
    assert windows(5, tape) == ()

    with pytest.raises(ExecutionError, match="window length must be >= 1"):
        windows(0, tape)
