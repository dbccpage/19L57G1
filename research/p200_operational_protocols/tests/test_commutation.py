"""Tests for readout-to-step commutation on non-disturbing sectors and disturbance detection."""

import pytest
from commutation import (
    ProcessStep,
    check_commutation,
    evaluate_disturbance_pricing,
    is_non_disturbing_sector,
    step_l1,
    step_m,
    sweep_commutation,
)
from protocol import (
    CarrierState,
    Footprint,
    Locus,
    MeasurementInstrument,
    disturbing_readout_1,
    non_disturbing_readout_1,
    non_disturbing_readout_2,
)


def test_sector_disjointness_detection() -> None:
    # Readout at Locus 2 reads L2, writes R2
    inst2 = MeasurementInstrument(
        name="readout2",
        target_locus=Locus.L2,
        record_locus=Locus.R2,
        probe_fn=lambda x: x,
        is_disturbing=False,
    )
    # Step at Locus 1 reads L1, writes L1
    step1 = ProcessStep(
        name="step1",
        target_locus=Locus.L1,
        transition_fn=lambda x: (x + 1) % 10,
        reads=frozenset({Locus.L1}),
        writes=frozenset({Locus.L1}),
    )
    assert is_non_disturbing_sector(inst2.footprint, step1.footprint)

    # Disturbing readout at L1 reads and writes L1
    inst1_disturb = MeasurementInstrument(
        name="disturb1",
        target_locus=Locus.L1,
        record_locus=Locus.R1,
        probe_fn=lambda x: x,
        is_disturbing=True,
        disturb_fn=lambda x: 0,
        disturbance_cost=1,
    )
    assert not is_non_disturbing_sector(inst1_disturb.footprint, step1.footprint)


def test_commutation_grid_sweep_non_disturbing() -> None:
    # Sweep 1,000 states across L1, L2, M, R1, R2
    states = [
        CarrierState(l1=a, l2=b, m=c, r1=d, r2=e, dist=0)
        for a in range(5)
        for b in range(5)
        for c in range(2)
        for d in range(2)
        for e in range(2)
    ]
    assert len(states) == 200

    readout_op = lambda s: non_disturbing_readout_2(s, lambda x: (x * 3) % 7)
    step_op = step_l1(lambda x: (x + 2) % 10)

    res = sweep_commutation(states, readout_op, step_op)
    assert res["all_commute"]
    assert res["commuting_count"] == 200
    assert res["failing_count"] == 0


def test_commutation_with_message_step() -> None:
    states = [
        CarrierState(l1=a, l2=b, m=c, r1=0, r2=0)
        for a in range(4)
        for b in range(4)
        for c in range(4)
    ]
    readout_op = lambda s: non_disturbing_readout_1(s, lambda x: x + 1)
    step_m_op = step_m(lambda m: (m * 2) % 5)

    res = sweep_commutation(states, readout_op, step_m_op)
    assert res["all_commute"]
    assert res["commuting_count"] == len(states)


def test_disturbance_causes_commutation_failure() -> None:
    # A step modifying L1 and a disturbing readout at L1 that alters L1
    s = CarrierState(l1=3, l2=0, m=0, r1=0, r2=0, dist=0)

    # opA: disturbing readout on L1 (records probe, sets L1 to 0)
    opA = lambda st: disturbing_readout_1(
        st,
        probe_fn=lambda x: x,
        disturb_fn=lambda x: 0,
        cost=1,
    )
    # opB: step increments L1
    opB = step_l1(lambda x: x + 10)

    # Check non-commutation:
    # opA(opB(s)): step first makes l1=13, then opA records 13, sets l1=0
    s_AB = opA(opB(s))
    # opB(opA(s)): opA first records 3, sets l1=0, then step makes l1=10
    s_BA = opB(opA(s))

    assert s_AB.r1 == 13
    assert s_BA.r1 == 3
    assert s_AB != s_BA
    assert not check_commutation(s, opA, opB)

    # Disturbance receipt verification
    receipt = evaluate_disturbance_pricing(s, opA, opB)
    assert receipt.interfering
    assert receipt.disturbance_cost == 1
    assert receipt.diagnostic_mark == 1
