"""Tests for endpoint factorization across multiple graph regimes."""

import pytest
from factorization import (
    GraphRegimeGenerator,
    sweep_factorization_grid,
    witness_endpoint_factorization,
)
from trace import State, Trace, Transition


def test_endpoint_factorization_witness_basic() -> None:
    s_start1 = State.create("init1")
    s_start2 = State.create("init2")
    hub = State.create("hub")
    final = State.create("final")

    h1 = Trace.from_step(Transition(s_start1, hub, "path1"))
    h2 = Trace.from_step(Transition(s_start2, hub, "path2"))
    future = Trace.from_step(Transition(hub, final, "continuation"))

    w = witness_endpoint_factorization(h1, h2, future)
    assert w.is_valid()
    assert w.shared_endpoint == hub
    assert w.final_state == final
    assert w.future_segment_identical
    assert w.composite_1.replay() == [s_start1, hub, final]
    assert w.composite_2.replay() == [s_start2, hub, final]


def test_diamond_dag_factorization_sweep() -> None:
    states, transitions = GraphRegimeGenerator.diamond_dag(branches=3, depth=2)
    start = states[0]
    hub = states[1]
    end = states[2]

    # Collect branch paths to hub
    paths_to_hub = [
        Trace.from_steps([t1, t2])
        for t1 in transitions if t1.source == start
        for t2 in transitions if t2.source == t1.target and t2.target == hub
    ]
    assert len(paths_to_hub) == 3

    # Collect continuation paths from hub to end
    futures_from_hub = [
        Trace.from_steps([t1, t2])
        for t1 in transitions if t1.source == hub
        for t2 in transitions if t2.source == t1.target and t2.target == end
    ]
    assert len(futures_from_hub) == 3

    # Every pair of histories and each future must factor cleanly
    count = 0
    for i in range(len(paths_to_hub)):
        for j in range(i + 1, len(paths_to_hub)):
            for fut in futures_from_hub:
                w = witness_endpoint_factorization(paths_to_hub[i], paths_to_hub[j], fut)
                assert w.is_valid()
                count += 1
    assert count == 3 * 3  # (3 choose 2) * 3 = 9 combinations


def test_grid_regime_factorization_sweep() -> None:
    witnesses = sweep_factorization_grid(width=4, height=4)
    assert len(witnesses) > 0
    for w in witnesses:
        assert w.is_valid()
        assert w.future_segment_identical


def test_cyclic_state_machine_factorization() -> None:
    states, transitions = GraphRegimeGenerator.cyclic_state_machine(num_cycles=2, cycle_len=3)
    nexus = states[0]

    # Two distinct paths leading back to nexus through cycle 0 and cycle 1
    cycle0_steps = [t for t in transitions if "c0" in t.label]
    cycle1_steps = [t for t in transitions if "c1" in t.label]

    h0 = Trace.from_steps(cycle0_steps)
    h1 = Trace.from_steps(cycle1_steps)
    assert h0.target == nexus
    assert h1.target == nexus

    # Future: execute cycle 0 again
    fut = Trace.from_steps(cycle0_steps)

    w = witness_endpoint_factorization(h0, h1, fut)
    assert w.is_valid()
    assert w.final_state == nexus
    assert w.future_segment_identical
