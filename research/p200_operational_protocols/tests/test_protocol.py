"""Unit and integration tests for operational protocols and embedded instruments."""

import pytest
from protocol import (
    CarrierState,
    Footprint,
    Locus,
    MeasurementInstrument,
    coincidence_evaluator,
    disturbing_readout_1,
    intervene_l1,
    intervene_l2,
    intervene_m,
    marginal_2,
    non_disturbing_readout_1,
    non_disturbing_readout_2,
    prepare_product,
    prepare_symmetric,
    proj_1,
    proj_2,
    record_1,
    record_2,
    record_distance,
)


def test_carrier_state_creation_and_validity() -> None:
    s = CarrierState(l1=3, l2=4, m=1, r1=0, r2=0, dist=0)
    assert s.is_valid(n1=5, n2=5, nm=2, nr1=10, nr2=10)
    assert not s.is_valid(n1=3, n2=5, nm=2, nr1=10, nr2=10)
    assert s.to_tuple() == (3, 4, 1, 0, 0, 0)


def test_preparations() -> None:
    s0 = CarrierState(l1=9, l2=8, m=7, r1=5, r2=6, dist=3)
    sp = prepare_product(s0, v1=2, v2=4, m=1)
    assert sp.l1 == 2
    assert sp.l2 == 4
    assert sp.m == 1
    assert sp.r1 == 0
    assert sp.r2 == 0
    assert sp.dist == 0

    ss = prepare_symmetric(s0, v=7, m=3)
    assert ss.l1 == 7
    assert ss.l2 == 7
    assert ss.m == 3
    assert ss.r1 == 0
    assert ss.r2 == 0
    assert ss.dist == 0


def test_interventions() -> None:
    s = CarrierState(l1=2, l2=5, m=1)
    s1 = intervene_l1(s, lambda x: x * 3)
    assert s1.l1 == 6
    assert s1.l2 == 5
    assert s1.m == 1

    s2 = intervene_l2(s, lambda x: x + 10)
    assert s2.l1 == 2
    assert s2.l2 == 15
    assert s2.m == 1

    sm = intervene_m(s, lambda x: x + 4)
    assert sm.l1 == 2
    assert sm.l2 == 5
    assert sm.m == 5


def test_records_and_comparisons() -> None:
    s = CarrierState(l1=1, l2=2, r1=0, r2=0)
    s = record_1(s, 7)
    assert s.r1 == 7
    assert not coincidence_evaluator(s)
    assert record_distance(s) == 7

    s = record_2(s, 7)
    assert s.r2 == 7
    assert coincidence_evaluator(s)
    assert record_distance(s) == 0


def test_non_disturbing_readout() -> None:
    s = CarrierState(l1=4, l2=9, r1=0, r2=0, dist=0)
    s1 = non_disturbing_readout_1(s, lambda x: x * 2)
    assert s1.r1 == 8
    assert s1.l1 == 4  # Untouched
    assert s1.dist == 0

    s2 = non_disturbing_readout_2(s1, lambda x: x + 1)
    assert s2.r2 == 10
    assert s2.l2 == 9  # Untouched
    assert s2.dist == 0
    assert proj_1(s2) == (4, 8)
    assert proj_2(s2) == (9, 10)
    assert marginal_2(s2) == 10


def test_disturbing_readout() -> None:
    s = CarrierState(l1=4, l2=9, r1=0, r2=0, dist=0)
    sd = disturbing_readout_1(
        s,
        probe_fn=lambda x: x * 10,
        disturb_fn=lambda x: 0,
        cost=3,
    )
    assert sd.r1 == 40
    assert sd.l1 == 0  # Disturbed
    assert sd.dist == 3


def test_measurement_instrument_class() -> None:
    inst = MeasurementInstrument(
        name="probe_l1",
        target_locus=Locus.L1,
        record_locus=Locus.R1,
        probe_fn=lambda x: x + 5,
        is_disturbing=False,
    )
    fp = inst.footprint
    assert Locus.L1 in fp.reads
    assert Locus.R1 in fp.writes
    assert Locus.L1 not in fp.writes

    s = CarrierState(l1=10, l2=20)
    res = inst.execute(s)
    assert res.r1 == 15
    assert res.l1 == 10


def test_footprint_disjointness_bernstein() -> None:
    fp1 = Footprint(reads=frozenset({Locus.L1}), writes=frozenset({Locus.R1}))
    fp2 = Footprint(reads=frozenset({Locus.L2}), writes=frozenset({Locus.R2}))
    assert fp1.is_disjoint(fp2)
    assert fp2.is_disjoint(fp1)

    # Conflict: fp3 writes to L1 which fp1 reads
    fp3 = Footprint(reads=frozenset(), writes=frozenset({Locus.L1}))
    assert not fp1.is_disjoint(fp3)
    assert not fp3.is_disjoint(fp1)
