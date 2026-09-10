"""Unit tests for observer.py: W06 Observer record exchange, symmetry, and decision divergence."""

from __future__ import annotations

import pytest
from carrier import State3, proj1, proj2
from observer import (
    Observer,
    exchange_round,
    is_symmetric,
    local_step_l1,
    receive_m,
    run_decision_divergence_experiment,
    run_negative_control_experiment,
    run_symmetric_agreement_experiment,
    transmit_l1,
    transmit_val,
)


def test_symmetry_definition() -> None:
    assert is_symmetric(State3(0, 0, 5)) is True
    assert is_symmetric(State3(3, 3, 0)) is True
    assert is_symmetric(State3(1, 2, 0)) is False


def test_symmetry_agreement_on_observations() -> None:
    """When state is symmetric under swap (s.l1 == s.l2), proj1 == proj2."""
    for val in range(10):
        for m in range(5):
            s = State3(l1=val, l2=val, m=m)
            assert proj1(s) == proj2(s)


def test_symmetry_agreement_with_decision_policies() -> None:
    """Under state symmetry, arbitrary deterministic decision policies yield identical choices."""
    policies = [
        lambda obs: obs[0] % 2 == 0,  # Parity of local state
        lambda obs: obs[0] > 5,  # Threshold check
        lambda obs: obs[0] * 10 + obs[1],  # Compound scoring
        lambda obs: (obs[0] + obs[1]) % 3,  # Modular projection
    ]

    symmetric_states = [
        State3(l1=v, l2=v, m=m) for v in range(8) for m in range(4)
    ]

    for policy in policies:
        res = run_symmetric_agreement_experiment(symmetric_states, policy)
        assert res["perfect_agreement"] is True
        assert res["agreement_rate"] == 1.0


def test_w06_decision_divergence_minimal_pair() -> None:
    """The canonical minimal divergence pair: s0 = (0, 0, 0), s1 = (1, 0, 0).

    Observer 2 begins in the EXACT same local state (0) with the buffer in the
    EXACT same state (0). Observer 1 sends its local state to M, and Observer 2
    subsequently decides/branches on M, diverging solely due to the transmitted message.
    """
    s0 = State3(l1=0, l2=0, m=0)
    s1 = State3(l1=1, l2=0, m=0)

    # Initial agreement of O2 and buffer
    assert s0.l2 == s1.l2 == 0
    assert s0.m == s1.m == 0

    exp = run_decision_divergence_experiment(s0, s1)
    assert exp["o2_initial_agreed"] is True
    assert exp["o2_final_diverged"] is True
    assert exp["o2_final_values"] == (0, 1)


@pytest.mark.parametrize("msg_a, msg_b", [(0, 1), (5, 9), (42, 100), (3, 7)])
def test_w06_decision_divergence_sweeps(msg_a: int, msg_b: int) -> None:
    """Verify decision divergence across multiple transmitted message values."""
    s0 = State3(l1=msg_a, l2=0, m=0)
    s1 = State3(l1=msg_b, l2=0, m=0)

    exp = run_decision_divergence_experiment(s0, s1)
    assert exp["o2_final_diverged"] is True
    assert exp["o2_final_values"] == (msg_a, msg_b)


def test_negative_control_information_isolation() -> None:
    """Negative Control: When Observer 1 performs a local update without writing to M,
    Observer 2's subsequent state does NOT diverge, confirming causal isolation.
    """
    s0 = State3(l1=0, l2=0, m=99)
    s1 = State3(l1=42, l2=0, m=99)

    # Observer 1 executes local mutation
    local_mutations = [
        lambda x: x + 1,
        lambda x: x * 3,
        lambda x: 1000,
    ]

    for fn in local_mutations:
        exp = run_negative_control_experiment(s0, s1, fn)
        assert exp["o2_remained_identical"] is True


def test_observer_class_integration() -> None:
    """Test the Observer class encapsulation."""
    policy = lambda obs: f"action_{obs[0]}_{obs[1]}"
    o1 = Observer("Alice", proj1, policy)
    o2 = Observer("Bob", proj2, policy)

    s_symm = State3(3, 3, 7)
    assert o1.decide(s_symm) == o2.decide(s_symm) == "action_3_7"

    s_asymm = State3(1, 2, 7)
    assert o1.decide(s_asymm) == "action_1_7"
    assert o2.decide(s_asymm) == "action_2_7"
    assert o1.decide(s_asymm) != o2.decide(s_asymm)
