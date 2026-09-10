"""Unit tests for data-driven control, enablement encoding, and fork refusal."""

import pytest

from control import (
    Controlled,
    State,
    build_program,
    ctrl_form,
    enabled,
    enabled_at,
    encode_c,
    fire,
    init,
    nops,
    run,
    run_det,
    step_det,
    successors,
    trace,
)
from runner import ExecutionError, Refusal, Terminal


def test_controlled_validation() -> None:
    # Invalid carrier bounds in op
    with pytest.raises(ExecutionError, match="lies outside carrier"):
        Controlled(n=2, ops=((0, 2),), ctrl=frozenset())

    # Invalid enablement
    with pytest.raises(ExecutionError, match="lies outside setting bounds"):
        Controlled(n=2, ops=((0, 1),), ctrl=frozenset({(2, 0)}))


def test_program_encoding() -> None:
    # 3 data, 2 ops: op 0 is cycle, op 1 is invert
    C = Controlled(
        n=3,
        ops=((1, 2, 0), (2, 1, 0)),
        ctrl=frozenset({(0, 0), (1, 1), (2, 0)}),
    )
    g = encode_c(C)
    assert nops(C) == 2
    
    # Operation edges:
    # Op 0 on form 3: (3, (0, 1)), (3, (1, 2)), (3, (2, 0))
    # Op 1 on form 4: (4, (0, 2)), (4, (1, 1)), (4, (2, 0))
    assert (3, (0, 1)) in g
    assert (4, (0, 2)) in g

    # Control self-instances:
    # ctrl_form(2, 0) = 3 + 2 + 0 = 5
    # ctrl_form(2, 1) = 3 + 2 + 1 = 6
    assert (5, (0, 0)) in g
    assert (6, (1, 1)) in g
    assert (5, (2, 2)) in g
    assert (5, (1, 1)) not in g


def test_enabled_and_enabled_at() -> None:
    C = Controlled(
        n=3,
        ops=((1, 2, 0), (2, 1, 0)),
        ctrl=frozenset({(0, 0), (0, 1), (1, 0)}),
    )
    g = encode_c(C)
    assert enabled(g, 2, 0, 0) is True
    assert enabled(g, 2, 0, 1) is True
    assert enabled(g, 2, 1, 0) is True
    assert enabled(g, 2, 1, 1) is False
    assert enabled(g, 2, 2, 0) is False

    # At datum 0, both ops 0 and 1 are enabled (non-deterministic fork)
    assert enabled_at(g, 2, 0) == (0, 1)
    # At datum 1, only op 0 is enabled
    assert enabled_at(g, 2, 1) == (0,)
    # At datum 2, no ops enabled (halt)
    assert enabled_at(g, 2, 2) == ()


def test_fire_monotonicity() -> None:
    g = frozenset({(3, (0, 1)), (5, (0, 0))})
    s = State(graph=g, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    
    res = fire(s, 0)
    assert isinstance(res, State)
    assert res.active == 1
    assert res.tape == (0, 1)
    assert res.clock == 1  # clock + 1
    assert res.fuel == 4   # fuel - 1

    # Firing with 0 fuel yields EXHAUSTED
    s_exhausted = State(graph=g, nops=1, active=0, tape=(0,), clock=1, fuel=0)
    assert fire(s_exhausted, 0) is Refusal.EXHAUSTED

    # Firing missing edge yields NO_EDGE
    assert fire(res, 0) is Refusal.NO_EDGE


def test_successors_family() -> None:
    # At datum 0, two operations enabled: op 0 -> 1, op 1 -> 2
    C = Controlled(
        n=3,
        ops=((1, 2, 0), (2, 1, 0)),
        ctrl=frozenset({(0, 0), (0, 1)}),
    )
    s = init(C, 0, fuel=10)
    succs = successors(s)
    assert len(succs) == 2
    active_succs = {st.active for st in succs}
    assert active_succs == {1, 2}
    for st in succs:
        assert st.fuel == 9
        assert st.clock == 1


def test_step_det_fork_refusal() -> None:
    # Explicit refusal to select when two ops enabled: returns Terminal.BRANCH
    C = Controlled(
        n=3,
        ops=((1, 2, 0), (2, 1, 0)),
        ctrl=frozenset({(0, 0), (0, 1)}),
    )
    s = init(C, 0, fuel=10)
    res = step_det(s)
    assert res is Terminal.BRANCH


def test_step_det_halt() -> None:
    # No ops enabled -> Terminal.HALT
    C = Controlled(
        n=3,
        ops=((1, 2, 0),),
        ctrl=frozenset(),
    )
    s = init(C, 0, fuel=10)
    assert step_det(s) is Terminal.HALT


def test_step_det_deterministic_execution() -> None:
    # Deterministic sequence: 0 -> 1 -> 2 -> halt
    # op 0: 0 -> 1, 1 -> 2, 2 -> 0
    # Enable op 0 at 0 and at 1, but NOT at 2
    C = Controlled(
        n=3,
        ops=((1, 2, 0),),
        ctrl=frozenset({(0, 0), (1, 0)}),
    )
    s = init(C, 0, fuel=5)
    term, final_s = trace(C, 0, fuel=5)
    assert term is Terminal.HALT
    assert final_s.active == 2
    assert final_s.tape == (0, 1, 2)
    assert final_s.clock == 2
    assert final_s.fuel == 3


def test_fuel_exhaustion_in_loop() -> None:
    # Infinite cycle 0 -> 1 -> 2 -> 0 with limited fuel 4
    C = Controlled(
        n=3,
        ops=((1, 2, 0),),
        ctrl=frozenset({(0, 0), (1, 0), (2, 0)}),
    )
    term, final_s = trace(C, 0, fuel=4)
    assert term is Terminal.EXHAUSTED
    assert final_s.clock == 4
    assert final_s.fuel == 0
    assert final_s.tape == (0, 1, 2, 0, 1)


def test_missing_edge_refusal() -> None:
    # Enabled op 0 at datum 0, but no edge in graph
    g = frozenset({(ctrl_form(1, 0), (0, 0))})
    s = State(graph=g, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    assert step_det(s) is Terminal.REFUSE
