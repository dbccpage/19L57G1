"""Tests for Target G014 Multi-Observer Descent & Natural Transport."""

from __future__ import annotations

import pytest
try:
    from research.g014_observer_descent.observer_descent import (
        CarrierState,
        DescentCoverage,
        GluingObstruction,
        Observer,
        natural_transport,
        verify_descent_and_gluing_invariants,
    )
except ModuleNotFoundError:
    from observer_descent import (
        CarrierState,
        DescentCoverage,
        GluingObstruction,
        Observer,
        natural_transport,
        verify_descent_and_gluing_invariants,
    )


def test_carrier_state_basic() -> None:
    state = CarrierState.from_mapping({"l1": 10, "l2": 20, "l3": 30})
    assert state.get("l1") == 10
    assert state.get("l2") == 20
    assert state.get("l4") is None
    assert state.loci == ("l1", "l2", "l3")


def test_observer_projection() -> None:
    state = CarrierState.from_mapping({"l1": 1, "l2": 2, "l3": 3, "l4": 4})
    obs = Observer(observer_id="obs_12", loci=("l2", "l1"))
    # Observer loci are sorted canonically
    assert obs.loci == ("l1", "l2")
    proj = obs.project(state)
    assert proj.to_dict() == {"l1": 1, "l2": 2}


def test_gluing_compatible_coverage() -> None:
    state = CarrierState.from_mapping({"l1": 100, "l2": 200, "l3": 300, "l4": 400})
    obs1 = Observer("O1", ("l1", "l2"))
    obs2 = Observer("O2", ("l2", "l3"))
    obs3 = Observer("O3", ("l3", "l4"))
    cov = DescentCoverage(observers=(obs1, obs2, obs3))

    assert cov.is_total_cover_for(state)

    records = {
        "O1": obs1.project(state),
        "O2": obs2.project(state),
        "O3": obs3.project(state),
    }
    compat_res = cov.check_compatibility(records)
    assert compat_res.is_ok()

    glue_res = cov.glue(records)
    assert glue_res.is_ok()
    glued_state = glue_res.unwrap()
    assert glued_state == state

    # Observation preservation
    for obs in (obs1, obs2, obs3):
        assert obs.project(glued_state) == records[obs.observer_id]


def test_gluing_obstruction_witness() -> None:
    obs1 = Observer("O1", ("l1", "l2"))
    obs2 = Observer("O2", ("l2", "l3"))
    cov = DescentCoverage(observers=(obs1, obs2))

    # Incompatible records on overlap "l2"
    rec1 = CarrierState.from_mapping({"l1": 10, "l2": 20})
    rec2 = CarrierState.from_mapping({"l2": 99, "l3": 30})  # 99 != 20

    glue_res = cov.glue({"O1": rec1, "O2": rec2})
    assert glue_res.is_err()
    err = glue_res.unwrap_err()
    assert isinstance(err, GluingObstruction)
    assert err.overlap_locus == "l2"
    assert (err.value_1, err.value_2) in ((20, 99), (99, 20))
    assert "Obstruction" in err.summary()


def test_natural_transport_commutation() -> None:
    state = CarrierState.from_mapping({"a": 1, "b": 2, "c": 3})
    obs = Observer("obs_ab", ("a", "b"))
    perm = {"a": "x", "b": "y", "c": "z"}

    t_obs, t_state, t_readout = natural_transport(obs, state, perm)

    assert t_obs.loci == ("x", "y")
    assert t_state.to_dict() == {"x": 1, "y": 2, "z": 3}
    assert t_readout.to_dict() == {"x": 1, "y": 2}

    # Verify commutation: readout on transported state matches transported readout
    direct_readout = t_obs.project(t_state)
    assert direct_readout == t_readout


def test_symmetric_duplicate_observers() -> None:
    # State symmetric under swap of l1 <-> l2
    state = CarrierState.from_mapping({"l1": 42, "l2": 42, "center": 0})
    obs_a = Observer("OA", ("l1", "center"))
    obs_b = Observer("OB", ("l2", "center"))

    r_a = obs_a.project(state)
    r_b = obs_b.project(state)

    # Values on corresponding loci match
    assert r_a.get("l1") == r_b.get("l2")
    assert r_a.get("center") == r_b.get("center")


def test_descent_and_gluing_invariants_sweep() -> None:
    for n in range(3, 10):
        mapping = {f"loc_{i}": i * 10 for i in range(n)}
        state = CarrierState.from_mapping(mapping)

        # Build overlapping chain coverage
        observers = []
        for i in range(n - 1):
            observers.append(Observer(f"O_{i}", (f"loc_{i}", f"loc_{i+1}")))
        cov = DescentCoverage(observers=tuple(observers))

        res = verify_descent_and_gluing_invariants(cov, state)
        assert res["status"] == "PASS"
        assert res["glued_state_equality"] is True
        assert res["obstruction_witness_verified"] is True
        assert res["natural_transport_commutes"] is True
