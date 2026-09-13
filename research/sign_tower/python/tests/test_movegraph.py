"""Tests for movegraph monotonicity, DAG acyclicity, and exchange refutation."""

from __future__ import annotations

import pytest
import sys
from pathlib import Path

PY_DIR = Path(__file__).resolve().parent.parent
if str(PY_DIR) not in sys.path:
    sys.path.insert(0, str(PY_DIR))

from movegraph import (
    build_reachability_dag,
    capability_cost_mu1,
    cardinal_potential,
    verify_constructor_monotonicity,
    verify_exchange_inexpressibility,
)
from derivation.model import (
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Supply,
    step,
)


def test_constructor_monotonicity() -> None:
    # Test monotonicity across all non-Supply constructors
    r = EMPTY
    assert cardinal_potential(r) == 0

    res_d = verify_constructor_monotonicity(r, AdmitDatum("d0"))
    assert res_d["delta"] == 1
    assert res_d["is_strictly_greater"] is True

    r1 = step(r, AdmitDatum("d0"))
    res_f = verify_constructor_monotonicity(r1, AdmitForm(1))
    assert res_f["delta"] == 1
    assert res_f["is_strictly_greater"] is True

    r2 = step(r1, AdmitForm(1))
    res_i = verify_constructor_monotonicity(r2, AdmitInst(0, (0,)))
    assert res_i["delta"] == 1
    assert res_i["is_strictly_greater"] is True

    res_rule = verify_constructor_monotonicity(r2, AdmitRuleAll(0))
    assert res_rule["delta"] == 1
    assert res_rule["is_strictly_greater"] is True

    r3 = step(r2, AdmitDatum("d1"))
    res_req = verify_constructor_monotonicity(r3, Impose(0, 1))
    assert res_req["delta"] == 1
    assert res_req["is_strictly_greater"] is True


def test_supply_is_identity() -> None:
    r = step(EMPTY, AdmitDatum("d0"))
    res_sup = verify_constructor_monotonicity(r, Supply("d1"))
    assert res_sup["delta"] == 0
    assert res_sup["is_monotonic"] is True
    assert res_sup["is_strictly_greater"] is False


def test_movegraph_dag_acyclicity() -> None:
    # Build transition graph from events and verify topological order exists (no cycles)
    events = [
        AdmitDatum("d0"),
        AdmitDatum("d1"),
        AdmitForm(1),
        AdmitForm(2),
        AdmitInst(0, (0,)),
        Impose(0, 1),
    ]
    dag_analysis = build_reachability_dag(EMPTY, events, max_depth=4)
    assert dag_analysis["num_states"] > 1
    assert dag_analysis["num_edges"] > 0
    assert dag_analysis["is_acyclic_dag"] is True
    assert dag_analysis["cycle_space_z1_vanishes"] is True


def test_in_place_witness_exchange_inexpressible() -> None:
    # Any sequence of non-Supply steps strictly increases cardinal potential
    steps = [
        AdmitDatum("d0"),
        AdmitDatum("d1"),
        AdmitForm(2),
        AdmitInst(0, (0, 1)),
    ]
    assert verify_exchange_inexpressibility(EMPTY, steps) is True


def test_capability_cost_non_negative() -> None:
    events = [
        Supply("s"),
        AdmitDatum("d"),
        AdmitForm(1),
        AdmitInst(0, (0,)),
        AdmitRuleAll(0),
        Impose(0, 1),
    ]
    for e in events:
        assert capability_cost_mu1(e) >= 0
