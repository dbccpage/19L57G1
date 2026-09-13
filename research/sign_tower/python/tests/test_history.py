"""Tests for history action, commutativity taxonomy, and form fiber balance."""

from __future__ import annotations

import pytest
import sys
from pathlib import Path

PY_DIR = Path(__file__).resolve().parent.parent
if str(PY_DIR) not in sys.path:
    sys.path.insert(0, str(PY_DIR))

from history import (
    analyze_form_fiber_parity,
    classify_adjacent_pair,
    enumerate_valid_executions,
    verify_data_replay_erasure,
)
from derivation.model import (
    EMPTY,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    step,
)


def test_commutativity_taxonomy_replay_commuting() -> None:
    # Disjoint footprints commute identically on raw Regime
    e_data = AdmitDatum("d1")
    e_form = AdmitForm(1)
    tier_disjoint = classify_adjacent_pair(EMPTY, e_data, e_form)
    assert tier_disjoint == "ReplayCommuting"

    # Identical-arity forms commute identically on raw Regime
    e_f1 = AdmitForm(2)
    e_f2 = AdmitForm(2)
    tier_ident = classify_adjacent_pair(EMPTY, e_f1, e_f2)
    assert tier_ident == "ReplayCommuting"


def test_commutativity_taxonomy_causally_blocked() -> None:
    # Instance requiring datum 0 cannot be admitted before datum 0 exists
    r = step(EMPTY, AdmitForm(1))
    e_data = AdmitDatum("d0")
    e_inst = AdmitInst(0, (0,))

    tier = classify_adjacent_pair(r, e_data, e_inst)
    assert tier == "CausallyBlocked"


def test_commutativity_taxonomy_order_altering() -> None:
    # Two distinct-arity forms alter the form sequence
    e1 = AdmitForm(1)
    e2 = AdmitForm(2)
    tier = classify_adjacent_pair(EMPTY, e1, e2)
    assert tier == "OrderAltering"


def test_trace_monoid_non_group_executions() -> None:
    # 5 events with causal constraints:
    # 2 data, 1 binary form, 1 instance, 1 requirement
    e_d0 = AdmitDatum("d0")
    e_d1 = AdmitDatum("d1")
    e_f0 = AdmitForm(2)
    e_inst = AdmitInst(0, (0, 1))
    e_req = Impose(0, 1)

    events = [e_d0, e_d1, e_f0, e_inst, e_req]
    valid = enumerate_valid_executions(events)

    # In S(5), total permutations = 120. Valid executions are strictly fewer (14),
    # proving execution traces form a trace monoid, not a group (14 does not divide 120).
    assert len(valid) == 14
    assert 120 % len(valid) != 0


def test_data_replay_arrival_order_erased() -> None:
    # Permuting arrival order of data tokens yields identical canonical state
    tokens = ["alpha", "beta", "gamma"]
    continuation = [AdmitForm(1), AdmitInst(0, (0,))]
    assert verify_data_replay_erasure(tokens, continuation) is True


def test_form_fiber_parity_balance_m4() -> None:
    # For m=4 distinct arities, canonical key fibers are 100% parity balanced
    arities = [1, 2, 3, 4]
    analysis = analyze_form_fiber_parity(arities)
    assert analysis["m_forms"] == 4
    assert analysis["total_executions"] == 24
    assert analysis["all_fibers_balanced"] is True
    for fiber in analysis["fiber_summaries"].values():
        assert fiber["pos"] == fiber["neg"]
