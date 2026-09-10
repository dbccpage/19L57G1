"""Tests for commute.py: Commuting dynamics squares and fuel boundaries."""

from limits import of_seq
from observe import State, make_cycle_graph
from commute import (
    fuel_exhaustion_commute_obstruction,
    step_stage,
    step_thread,
    verify_iter_next_commute,
    verify_stage_commuting_square,
    verify_thread_sequence_commute,
    verify_thread_step_compatibility,
    verify_trace_commuting_square,
)


def test_stage_commuting_square() -> None:
    f = lambda x: (x + 1) % 5
    words = [
        (0,),
        (0, 1),
        (0, 1, 2),
        (4, 3, 2, 1, 0),
        (1, 4, 2, 3, 0, 4, 1),
    ]
    for w in words:
        assert verify_stage_commuting_square(f, w) is True


def test_thread_step_lifts() -> None:
    f = lambda x: (x * 2) % 7
    thread = of_seq(lambda i: i % 7, upto=15)
    assert verify_thread_step_compatibility(f, thread) is True
    assert verify_thread_sequence_commute(f, thread, max_idx=10) is True


def test_observation_trace_commuting_square() -> None:
    g = make_cycle_graph()
    s = State(graph=g, nops=3, active=0, tape=(0,), clock=0, fuel=20)
    for n in range(12):
        assert verify_trace_commuting_square(s, n) is True


def test_iter_next_commute() -> None:
    g = make_cycle_graph()
    s = State(graph=g, nops=3, active=0, tape=(0,), clock=0, fuel=20)
    for n in range(15):
        assert verify_iter_next_commute(s, n) is True


def test_fuel_exhaustion_boundary() -> None:
    g = make_cycle_graph()
    s = State(graph=g, nops=3, active=0, tape=(0,), clock=0, fuel=5)
    # At n=5, s_starved has fuel 5, so taking 6 steps stalls, while s_ample takes 6 steps
    commutes, starved, ample = fuel_exhaustion_commute_obstruction(s, n=5)
    assert commutes is False
    assert len(starved) == 6  # initial + 5 steps, halted
    assert len(ample) == 7    # initial + 6 steps
