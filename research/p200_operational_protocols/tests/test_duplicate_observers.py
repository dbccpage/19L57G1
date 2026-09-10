"""Tests for presentation symmetries and recorded inter-observer agreement."""

import pytest
from embedded_observer import (
    check_equivariance,
    check_inter_observer_agreement,
    create_duplicate_observers,
    is_symmetric_state,
    run_joint_protocol,
    swap_symmetry,
    translate_symmetry,
)
from protocol import CarrierState, prepare_symmetric


def test_swap_involution() -> None:
    for a in range(4):
        for b in range(4):
            for r1 in range(2):
                for r2 in range(2):
                    s = CarrierState(l1=a, l2=b, m=1, r1=r1, r2=r2, dist=0)
                    assert swap_symmetry(swap_symmetry(s)) == s


def test_swap_preserves_m_and_dist() -> None:
    s = CarrierState(l1=2, l2=5, m=9, r1=1, r2=8, dist=4)
    sw = swap_symmetry(s)
    assert sw.l1 == 5
    assert sw.l2 == 2
    assert sw.r1 == 8
    assert sw.r2 == 1
    assert sw.m == 9
    assert sw.dist == 4


def test_translation_symmetry() -> None:
    s = CarrierState(l1=2, l2=5, m=0)
    st = translate_symmetry(s, shift=3, modulus=10)
    assert st.l1 == 5
    assert st.l2 == 8


def test_equivariance_under_swap() -> None:
    obs1, obs2 = create_duplicate_observers(probe_fn=lambda x: (x * 7 + 3) % 11)

    states = [
        CarrierState(l1=a, l2=b, m=c, r1=0, r2=0)
        for a in range(5)
        for b in range(5)
        for c in range(2)
    ]
    for s in states:
        assert check_equivariance(obs1, obs2, s)


def test_inter_observer_agreement_on_symmetric_preparations() -> None:
    obs1, obs2 = create_duplicate_observers(probe_fn=lambda x: (x * 2 + 1) % 13)

    # Generate 50 symmetric states
    symmetric_states = [prepare_symmetric(CarrierState(), v=val) for val in range(50)]

    for s in symmetric_states:
        assert is_symmetric_state(s)
        assert check_inter_observer_agreement(obs1, obs2, s)
        final_state = run_joint_protocol(obs1, obs2, s)
        assert final_state.r1 == final_state.r2


def test_asymmetric_states_yield_record_divergence() -> None:
    obs1, obs2 = create_duplicate_observers(probe_fn=lambda x: x)

    # Injective probe on distinct loci coordinates
    asymmetric_states = [
        CarrierState(l1=a, l2=b, m=0, r1=0, r2=0)
        for a in range(5)
        for b in range(5)
        if a != b
    ]
    assert len(asymmetric_states) == 20

    for s in asymmetric_states:
        assert not is_symmetric_state(s)
        assert not check_inter_observer_agreement(obs1, obs2, s)
        final_state = run_joint_protocol(obs1, obs2, s)
        assert final_state.r1 != final_state.r2
