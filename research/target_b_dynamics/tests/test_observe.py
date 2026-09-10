"""Tests for observe.py: Step-scale observations and prefix compatibility tracking Target A traces."""

import pytest

from observe import (
    State,
    Terminal,
    enabled_at,
    fire,
    is_prefix,
    iterate,
    lookup,
    lost_fuel_witness,
    make_cycle_graph,
    next_state,
    obs,
    obs_trace,
    step_det,
    verify_fuel_independence,
    verify_prefix_compatibility,
)


def test_lookup_and_enabled_at() -> None:
    g = make_cycle_graph()
    assert lookup(3, 0, g) == 1
    assert lookup(3, 1, g) == 2
    assert lookup(3, 2, g) == 0
    assert lookup(3, 99, g) is None

    # op 0 enabled everywhere
    assert enabled_at(g, 3, 0) == [0]
    assert enabled_at(g, 3, 1) == [0]
    assert enabled_at(g, 3, 2) == [0]


def test_fire_and_accounting() -> None:
    g = make_cycle_graph()
    s = State(graph=g, nops=3, active=0, tape=(0,), clock=0, fuel=5)
    status, s_next = fire(s, 0)
    assert status == "ok"
    assert s_next is not None
    assert s_next.active == 1
    assert s_next.tape == (0, 1)
    assert s_next.clock == 1
    assert s_next.fuel == 4


def test_fire_exhaustion() -> None:
    g = make_cycle_graph()
    s = State(graph=g, nops=3, active=0, tape=(0,), clock=0, fuel=0)
    status, s_next = fire(s, 0)
    assert status == "exhausted"
    assert s_next is None


def test_branch_refusal() -> None:
    # Graph where two operations (0 and 1) are enabled at datum 0
    # form 3 + nops + 0 = 5, form 3 + nops + 1 = 6
    g = (
        (3, (0, 1)),
        (4, (0, 2)),
        (5, (0, 0)),
        (6, (0, 0)),
    )
    s = State(graph=g, nops=2, active=0, tape=(0,), clock=0, fuel=10)
    terminal, s_next = step_det(s)
    assert terminal == Terminal.BRANCH
    assert s_next is None
    # next_state keeps state unchanged at terminal
    assert next_state(s) == s


def test_halt_on_no_enablement() -> None:
    # Graph with no enablements at all
    g = ((3, (0, 1)),)
    s = State(graph=g, nops=1, active=0, tape=(0,), clock=0, fuel=10)
    terminal, s_next = step_det(s)
    assert terminal == Terminal.HALT
    assert s_next is None
    assert next_state(s) == s


def test_prefix_compatibility() -> None:
    g = make_cycle_graph()
    s = State(graph=g, nops=3, active=0, tape=(0,), clock=0, fuel=20)
    assert verify_prefix_compatibility(s, max_steps=15) is True


def test_fuel_independence() -> None:
    g = make_cycle_graph()
    s = State(graph=g, nops=3, active=0, tape=(0,), clock=0, fuel=10)
    # Scale 5 requires fuel >= 5
    assert verify_fuel_independence(s, n=5, test_fuels=[5, 6, 10, 25]) is True


def test_lost_fuel_divergence() -> None:
    s0, s1, t0_pre, t1_pre, t0_post, t1_post = lost_fuel_witness()
    assert t0_pre == t1_pre == (0,)
    assert t0_post == (0,)
    assert t1_post == (0, 1)


def test_trace_sequence() -> None:
    g = make_cycle_graph()
    s = State(graph=g, nops=3, active=0, tape=(0,), clock=0, fuel=10)
    tr = obs_trace(3, s)
    assert len(tr) == 4
    assert tr[0] == (0,)
    assert tr[1] == (0, 1)
    assert tr[2] == (0, 1, 2)
    assert tr[3] == (0, 1, 2, 0)
