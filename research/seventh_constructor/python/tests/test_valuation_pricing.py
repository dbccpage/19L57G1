"""Tests for operational valuation measures mu1 and mu2 pricing.

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path
import sys
import pytest

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(REPO_ROOT / "code") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.model import (
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Impose,
    Regime,
    Supply,
)
from research.seventh_constructor.python.conservative_grammar import (
    ExtendedEvent,
    SwapWitness,
    cardinal_potential,
)
from research.seventh_constructor.python.valuation_pricing import (
    capability_cost_mu1,
    evaluate_cycle_circulation,
    evaluate_trajectory_costs,
    transition_cost_mu2,
    verify_coboundary_identity,
)


@pytest.fixture
def base_regime() -> Regime:
    return Regime(("a", "b"), (2,), frozenset({(0, (0, 1))}), frozenset(), frozenset())


def test_base_event_pricing() -> None:
    """Theorems 3.1 & 3.5: mu1(swap) == 0 and mu2(swap) == 1."""
    swap = SwapWitness(0, 1)
    assert capability_cost_mu1(swap) == 0
    assert transition_cost_mu2(swap) == 1

    supply = Supply("ext")
    assert capability_cost_mu1(supply) == 0
    assert transition_cost_mu2(supply) == 0

    admit_d = AdmitDatum("c")
    assert capability_cost_mu1(admit_d) == 1
    assert transition_cost_mu2(admit_d) == 1


def test_exact_coboundary_identity(base_regime: Regime) -> None:
    """Theorem 3.2: mu1(e) == N(step(r, e)) - N(r) across all event types."""
    events: list[ExtendedEvent] = [
        Supply("c"),
        AdmitDatum("c"),
        AdmitForm(1),
        AdmitInst(0, (1, 0)),
        AdmitRuleAll(0),
        Impose(0, 1),
        SwapWitness(0, 1),
    ]
    for e in events:
        assert verify_coboundary_identity(base_regime, e)


def test_trajectory_cost_evaluation() -> None:
    """Theorem 3.3: Trajectory costs match sum of individual event valuations."""
    trajectory: list[ExtendedEvent] = [
        SwapWitness(0, 1),
        SwapWitness(0, 1),
        AdmitDatum("c"),
        SwapWitness(0, 2),
    ]
    c_mu1, c_mu2 = evaluate_trajectory_costs(trajectory)

    # 3 swaps (mu1=0) + 1 admit (mu1=1) = 1
    assert c_mu1 == 1
    # 3 swaps (mu2=1) + 1 admit (mu2=1) = 4
    assert c_mu2 == 4


def test_cycle_circulation_contrast() -> None:
    """Theorems 3.7-3.9: Circulation of mu1 vanishes (oint mu1 = 0) while mu2 is strictly positive."""
    cycle_2: list[ExtendedEvent] = [SwapWitness(0, 1), SwapWitness(0, 1)]
    report_2 = evaluate_cycle_circulation(cycle_2)

    assert report_2["oint_mu1"] == 0
    assert report_2["oint_mu2"] == 2
    assert report_2["is_mu1_exact_coboundary"] is True
    assert report_2["is_mu2_circulation_strictly_positive"] is True
    assert report_2["circulation_cost_contrast"] is True

    # 6-step cycle in S3
    cycle_6: list[ExtendedEvent] = [
        SwapWitness(0, 1), SwapWitness(1, 2),
        SwapWitness(0, 1), SwapWitness(1, 2),
        SwapWitness(0, 1), SwapWitness(1, 2),
    ]
    report_6 = evaluate_cycle_circulation(cycle_6)
    assert report_6["oint_mu1"] == 0
    assert report_6["oint_mu2"] == 6
    assert report_6["circulation_cost_contrast"] is True
