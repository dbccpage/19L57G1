"""Soviet invariant test suite for ViabilityEnvelope and RefusalSemantics.

Tested Invariants:
1. Invariant Class 1 (Operational Immutability): On operational refusal, the carrier
   state is preserved strictly unmutated (state_after is state_before).
2. Invariant Class 1 (Monotonic Invariant Preservation): Imposed separation requirements
   are preserved monotonically, and required pairs maintain distinct observable profiles.
3. Invariant Class 2 (Resource Ceilings): Carrier states exceeding hard resource bounds
   (data sort, form declarations, arity limits, instance set cardinality) are rejected.
4. Invariant Class 2 (Core Sort Inhabitation): Carrier states with empty core sorts are rejected.
5. Invariant Class 3 (Negative Controls & Fuel Exhaustion): Fuel exhaustion (fuel = 0)
   triggers typed refusal without state modification.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, receipt-grounded).
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
CODE_DIR = REPO_ROOT / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
for _sub in ["x301_formal_semantics"]:
    _sub_path = REPO_ROOT / "research" / _sub
    if str(_sub_path) not in sys.path:
        sys.path.insert(0, str(_sub_path))

from research.x301_formal_semantics.semantics import Atom, Identity, RelationalModel
from research.x303_bounded_agency.agency import (
    AgentController,
    RefusalReason,
    StepResult,
    ViabilityEnvelope,
    add_instance_action,
)


def _make_sample_model(
    n_data: int = 3,
    forms: tuple[int, ...] = (1, 2),
    insts: tuple[tuple[int, tuple[int, ...]], ...] = (),
    reqs: tuple[tuple[int, int], ...] = (),
) -> RelationalModel:
    """Helper to construct a valid relational carrier state."""
    data = tuple(f"d{i}" for i in range(n_data))
    return RelationalModel(
        data=data,
        forms=forms,
        insts=frozenset(insts),
        rules=frozenset(),
        reqs=frozenset(reqs),
    )


# ---------------------------------------------------------------------------
# Invariant Class 2: Core Sort Non-Empty Requirements
# ---------------------------------------------------------------------------

def test_core_sort_non_empty_data() -> None:
    """Invariant: Data sort count must be at least min_data."""
    env = ViabilityEnvelope(
        max_data=10,
        max_forms=5,
        max_arity=3,
        max_insts=20,
        min_data=2,
        min_forms=1,
    )
    # Empty data sort
    m_empty = RelationalModel(data=(), forms=(1,))
    is_ok, reason = env.check_viability(m_empty)
    assert not is_ok
    assert reason is not None
    assert "below minimum" in reason

    # Single datum when minimum is 2
    m_one = RelationalModel(data=("d0",), forms=(1,))
    is_ok, _ = env.check_viability(m_one)
    assert not is_ok

    # Two data satisfies minimum
    m_valid = _make_sample_model(n_data=2)
    is_ok, _ = env.check_viability(m_valid)
    assert is_ok


def test_core_sort_non_empty_forms() -> None:
    """Invariant: Form sort count must be at least min_forms."""
    env = ViabilityEnvelope(
        max_data=10,
        max_forms=5,
        max_arity=3,
        max_insts=20,
        min_data=1,
        min_forms=1,
    )
    m_no_forms = RelationalModel(data=("d0",), forms=())
    is_ok, reason = env.check_viability(m_no_forms)
    assert not is_ok
    assert reason is not None
    assert "Form sort count" in reason


# ---------------------------------------------------------------------------
# Invariant Class 2: Resource Ceilings
# ---------------------------------------------------------------------------

def test_resource_ceilings_data_sort() -> None:
    """Invariant: Data sort cardinality must not exceed max_data."""
    env = ViabilityEnvelope(
        max_data=4,
        max_forms=5,
        max_arity=3,
        max_insts=20,
    )
    m_boundary = _make_sample_model(n_data=4)
    assert env.is_viable(m_boundary)

    m_exceeded = _make_sample_model(n_data=5)
    is_ok, reason = env.check_viability(m_exceeded)
    assert not is_ok
    assert reason is not None
    assert "exceeds ceiling" in reason


def test_resource_ceilings_forms_count() -> None:
    """Invariant: Form declarations count must not exceed max_forms."""
    env = ViabilityEnvelope(
        max_data=10,
        max_forms=2,
        max_arity=3,
        max_insts=20,
    )
    m_valid = _make_sample_model(forms=(1, 2))
    assert env.is_viable(m_valid)

    m_exceeded = _make_sample_model(forms=(1, 2, 1))
    is_ok, reason = env.check_viability(m_exceeded)
    assert not is_ok
    assert reason is not None
    assert "Form sort count" in reason


def test_resource_ceilings_form_arity() -> None:
    """Invariant: Every form arity must not exceed max_arity."""
    env = ViabilityEnvelope(
        max_data=10,
        max_forms=5,
        max_arity=2,
        max_insts=20,
    )
    m_valid = _make_sample_model(forms=(1, 2))
    assert env.is_viable(m_valid)

    m_exceeded = _make_sample_model(forms=(1, 3))
    is_ok, reason = env.check_viability(m_exceeded)
    assert not is_ok
    assert reason is not None
    assert "Form arity exceeds ceiling" in reason


def test_resource_ceilings_instances_cardinality() -> None:
    """Invariant: Instances dictionary size must not exceed max_insts."""
    env = ViabilityEnvelope(
        max_data=10,
        max_forms=5,
        max_arity=2,
        max_insts=2,
    )
    insts_valid = ((0, (0,)), (0, (1,)))
    m_valid = _make_sample_model(insts=insts_valid)
    assert env.is_viable(m_valid)

    insts_exceeded = ((0, (0,)), (0, (1,)), (0, (2,)))
    m_exceeded = _make_sample_model(insts=insts_exceeded)
    is_ok, reason = env.check_viability(m_exceeded)
    assert not is_ok
    assert reason is not None
    assert "Instance count" in reason


# ---------------------------------------------------------------------------
# Invariant Class 1 & 3: Monotonic Separation Requirements
# ---------------------------------------------------------------------------

def test_monotonic_separation_requirement_preservation() -> None:
    """Invariant: State must retain all declared required separation pairs."""
    env = ViabilityEnvelope(
        max_data=10,
        max_forms=5,
        max_arity=2,
        max_insts=20,
        required_reqs=frozenset({(0, 1)}),
    )
    # Model with required separation pair (and instance separating them)
    m_valid = _make_sample_model(
        n_data=3,
        insts=((0, (0,)),),  # datum 0 is in form 0; datum 1 is not -> separable
        reqs=((0, 1),),
    )
    assert env.is_viable(m_valid)

    # Model missing required separation pair
    m_missing = _make_sample_model(
        n_data=3,
        insts=((0, (0,)),),
        reqs=(),
    )
    is_ok, reason = env.check_viability(m_missing)
    assert not is_ok
    assert reason is not None
    assert "missing required separation pairs" in reason


def test_separation_collapse_detection() -> None:
    """Negative Control: Required separation pair with identical context profiles is refused."""
    env = ViabilityEnvelope(
        max_data=10,
        max_forms=5,
        max_arity=2,
        max_insts=20,
        required_reqs=frozenset({(0, 1)}),
    )
    # Model where datum 0 and datum 1 have identical profiles (no instances distinguish them)
    m_collapsed = _make_sample_model(
        n_data=3,
        insts=(),  # neither datum 0 nor 1 appears in any instance -> identical profiles!
        reqs=((0, 1),),
    )
    is_ok, reason = env.check_viability(m_collapsed)
    assert not is_ok
    assert reason is not None
    assert "collapsed" in reason


# ---------------------------------------------------------------------------
# Invariant Class 1: Firm Structural Invariants
# ---------------------------------------------------------------------------

def test_firm_structural_invariants() -> None:
    """Invariant: Firm invariant formulas must evaluate to TRUE (1 in Q)."""
    # Firm invariant: Identity("0", "0") is always TRUE
    inv_tautology = Identity("0", "0")
    # Firm invariant: Identity("0", "1") is FALSE
    inv_contradiction = Identity("0", "1")

    env_valid = ViabilityEnvelope(
        max_data=10,
        max_forms=5,
        max_arity=2,
        max_insts=20,
        firm_invariants=(inv_tautology,),
    )
    m = _make_sample_model()
    assert env_valid.is_viable(m)

    env_invalid = ViabilityEnvelope(
        max_data=10,
        max_forms=5,
        max_arity=2,
        max_insts=20,
        firm_invariants=(inv_contradiction,),
    )
    is_ok, reason = env_invalid.check_viability(m)
    assert not is_ok
    assert reason is not None
    assert "Firm invariant violated" in reason


# ---------------------------------------------------------------------------
# Exact Rational Arithmetic Discipline
# ---------------------------------------------------------------------------

def test_exact_rational_margin_zero_floats() -> None:
    """Invariant: Viability margin must be computed in exact Fraction in [0, 1] cap Q."""
    env = ViabilityEnvelope(
        max_data=10,
        max_forms=10,
        max_arity=3,
        max_insts=10,
    )
    m = _make_sample_model(n_data=3, forms=(1, 2), insts=((0, (0,)),))
    margin = env.compute_margin(m)

    assert isinstance(margin, Fraction)
    # |data|/10 = 3/10, |forms|/10 = 2/10, |insts|/10 = 1/10
    # max ratio = 3/10; margin = 1 - 3/10 = 7/10
    assert margin == Fraction(7, 10)
    assert not isinstance(margin, float)


# ---------------------------------------------------------------------------
# Invariant Class 1 & 3: Refusal Semantics & Strict State Immutability
# ---------------------------------------------------------------------------

def test_refusal_on_envelope_boundary_preserves_state() -> None:
    """Invariant: When all candidate actions exceed the viability envelope,
    the controller emits StepResult.refusal and preserves carrier state strictly unmutated.
    """
    env = ViabilityEnvelope(
        max_data=3,
        max_forms=2,
        max_arity=2,
        max_insts=1,  # ceiling allows at most 1 instance
    )
    initial_model = _make_sample_model(n_data=3, forms=(1,), insts=((0, (0,)),))
    assert env.is_viable(initial_model)

    controller = AgentController(
        state=initial_model,
        envelope=env,
        total_fuel=10,
    )

    # Candidate action adds a second instance, exceeding max_insts=1
    action_violator = add_instance_action(form=0, args=(1,), fuel_cost=1)
    result = controller.step([action_violator])

    # Result must be typed refusal
    assert result.is_refusal
    assert not result.is_success
    assert result.reason == RefusalReason.VIABILITY_BOUNDARY_EXCEEDED

    # Crucial property: state_after is state_before (strict reference identity)
    assert result.state is initial_model
    assert controller.state is initial_model


def test_refusal_on_fuel_exhaustion_preserves_state() -> None:
    """Invariant: When operational fuel is exhausted (fuel = 0),
    the controller emits StepResult.refusal and preserves carrier state strictly unmutated.
    """
    env = ViabilityEnvelope(
        max_data=10,
        max_forms=5,
        max_arity=3,
        max_insts=20,
    )
    initial_model = _make_sample_model(n_data=3, forms=(1,))

    controller = AgentController(
        state=initial_model,
        envelope=env,
        total_fuel=0,  # Zero initial fuel
    )

    valid_action = add_instance_action(form=0, args=(0,), fuel_cost=1)
    result = controller.step([valid_action])

    assert result.is_refusal
    assert result.reason == RefusalReason.FUEL_EXHAUSTED
    assert result.state is initial_model
    assert controller.state is initial_model
