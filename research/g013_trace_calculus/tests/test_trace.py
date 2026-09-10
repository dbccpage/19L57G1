"""Tests for 0-cells, 1-cells, trace concatenation, and replay execution."""

import pytest
from trace import State, Trace, Transition


def test_state_construction_and_updates() -> None:
    s0 = State.create("s0", {"x": 10, "mode": "idle"})
    assert s0.state_id == "s0"
    assert s0.get("x") == 10
    assert s0.get("mode") == "idle"
    assert s0.get("missing", 99) == 99

    s1 = s0.with_update("s1", x=11, status="active")
    assert s1.state_id == "s1"
    assert s1.get("x") == 11
    assert s1.get("mode") == "idle"
    assert s1.get("status") == "active"


def test_transition_properties() -> None:
    s0 = State.create("s0")
    s1 = State.create("s1")
    t = Transition(source=s0, target=s1, label="tick", cost=1.5)
    assert t.source == s0
    assert t.target == s1
    assert t.label == "tick"
    assert t.cost == 1.5

    with pytest.raises(ValueError, match="non-negative"):
        Transition(source=s0, target=s1, label="bad", cost=-0.5)


def test_trace_identity_and_basic_construction() -> None:
    s0 = State.create("s0")
    id_tr = Trace.id_trace(s0)
    assert id_tr.is_identity
    assert id_tr.length == 0
    assert id_tr.source == s0
    assert id_tr.target == s0
    assert id_tr.replay() == [s0]


def test_trace_concatenation_and_associativity() -> None:
    s0 = State.create("s0")
    s1 = State.create("s1")
    s2 = State.create("s2")
    s3 = State.create("s3")

    t1 = Transition(s0, s1, "step1", cost=1.0)
    t2 = Transition(s1, s2, "step2", cost=2.0)
    t3 = Transition(s2, s3, "step3", cost=3.0)

    tr1 = Trace.from_step(t1)
    tr2 = Trace.from_step(t2)
    tr3 = Trace.from_step(t3)

    # Left and right identity
    assert tr1.concat(Trace.id_trace(s1)) == tr1
    assert Trace.id_trace(s0).concat(tr1) == tr1

    # Associativity: (tr1 * tr2) * tr3 == tr1 * (tr2 * tr3)
    left_assoc = (tr1 + tr2) + tr3
    right_assoc = tr1 + (tr2 + tr3)
    assert left_assoc == right_assoc
    assert left_assoc.length == 3
    assert left_assoc.labels() == ["step1", "step2", "step3"]
    assert left_assoc.replay() == [s0, s1, s2, s3]


def test_trace_endpoint_mismatch_refusal() -> None:
    s0 = State.create("s0")
    s1 = State.create("s1")
    s2 = State.create("s2")

    tr1 = Trace.from_step(Transition(s0, s1, "a"))
    tr2 = Trace.from_step(Transition(s2, s0, "b"))

    with pytest.raises(ValueError, match="Cannot concatenate traces with mismatched endpoints"):
        tr1.concat(tr2)


def test_trace_slice_and_intermediate_states() -> None:
    states = [State.create(f"s{i}") for i in range(5)]
    steps = [Transition(states[i], states[i + 1], f"step_{i}") for i in range(4)]
    full_trace = Trace.from_steps(steps)

    assert full_trace.length == 4
    sub = full_trace.slice_trace(1, 3)
    assert sub.length == 2
    assert sub.source == states[1]
    assert sub.target == states[3]
    assert sub.labels() == ["step_1", "step_2"]
    assert sub.replay() == [states[1], states[2], states[3]]
