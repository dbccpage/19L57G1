"""Soviet invariant test suite for CausalEvaluator and MulticriteriaSelector.

Tested Invariants:
1. Invariant Class 1 (Counterfactual Non-Mutation): Ephemeral branch projection
   evaluates prospective candidate actions without mutating the base carrier state.
2. Invariant Class 1 (Exact Rational Valuation): Multi-criteria utility metrics
   (u_margin, u_fuel, u_goal) are computed in exact rational arithmetic in [0, 1] cap Q.
3. Invariant Class 1 (Pareto Dominance & Canonical Tie-Breaking): Dominated actions
   are eliminated from the Pareto frontier; ties among optimal actions are resolved
   deterministically by CanonKey ordering.
4. Invariant Class 2 (Separation of Roles): Proposal, evaluation, authority, and execution
   remain distinct operational stages.
5. Invariant Class 2 (Bounded Memory Horizon): Memory depth is strictly bounded at H
   with deterministic FIFO eviction preserving data processing bounds.

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

from research.x301_formal_semantics.semantics import Atom, Identity, RationalValuation, RelationalModel
from research.x303_bounded_agency.agency import (
    ActionEvaluation,
    ActionProposal,
    BoundedMemory,
    CandidateAction,
    CausalEvaluator,
    MemoryRecord,
    MulticriteriaSelector,
    ViabilityEnvelope,
    add_instance_action,
    canonical_model_digest,
    remove_instance_action,
)


def _make_base_model() -> RelationalModel:
    return RelationalModel(
        data=("d0", "d1", "d2"),
        forms=(1, 2),
        insts=frozenset({(0, (0,))}),
        rules=frozenset(),
        reqs=frozenset(),
    )


# ---------------------------------------------------------------------------
# Invariant Class 1: Counterfactual Non-Mutation
# ---------------------------------------------------------------------------

def test_ephemeral_projection_preserves_base_state() -> None:
    """Invariant: Projecting a candidate action does not mutate the base carrier state."""
    base = _make_base_model()
    digest_before = canonical_model_digest(base)
    insts_before = frozenset(base.insts)

    evaluator = CausalEvaluator()
    action = add_instance_action(form=0, args=(1,), fuel_cost=2)

    # Perform counterfactual projection
    projected = evaluator.project(base, action)

    # Projected state has new instance
    assert (0, (1,)) in projected.insts
    assert len(projected.insts) == 2

    # Base state is strictly unmutated
    assert base.insts == insts_before
    assert (0, (1,)) not in base.insts
    assert canonical_model_digest(base) == digest_before


def test_causal_evaluation_leaves_base_state_untouched() -> None:
    """Invariant: Full candidate evaluation on an ephemeral branch does not mutate base state."""
    base = _make_base_model()
    digest_before = canonical_model_digest(base)

    env = ViabilityEnvelope(max_data=10, max_forms=5, max_arity=3, max_insts=10)
    evaluator = CausalEvaluator()
    action = add_instance_action(form=0, args=(2,), fuel_cost=1)

    eval_res = evaluator.evaluate_candidate(
        model=base,
        action=action,
        envelope=env,
        fuel_remaining=5,
        total_fuel=10,
    )

    assert eval_res.viable
    assert canonical_model_digest(base) == digest_before


# ---------------------------------------------------------------------------
# Invariant Class 2: Separation of Proposal vs Execution
# ---------------------------------------------------------------------------

def test_proposal_is_supply_shaped_zero_state_mutation() -> None:
    """Invariant: Creating an ActionProposal changes no carrier state."""
    base = _make_base_model()
    digest_before = canonical_model_digest(base)

    action1 = add_instance_action(form=0, args=(1,))
    action2 = remove_instance_action(form=0, args=(0,))
    proposal = ActionProposal(token="prop_1", offerings=(action1, action2))

    assert proposal.token == "prop_1"
    assert len(proposal.offerings) == 2
    assert canonical_model_digest(base) == digest_before


# ---------------------------------------------------------------------------
# Empirical Reference Discrimination
# ---------------------------------------------------------------------------

def test_empirical_reference_detection() -> None:
    """Invariant: Actions with observable relational effects have empirical reference;
    noop actions do not.
    """
    base = _make_base_model()
    evaluator = CausalEvaluator()

    # Action that adds an already existing instance is a noop
    noop_action = add_instance_action(form=0, args=(0,), name="noop_add_existing")
    assert not evaluator.check_empirical_reference(base, noop_action)

    # Action that adds a genuinely new instance has empirical reference
    real_action = add_instance_action(form=0, args=(1,), name="real_add")
    assert evaluator.check_empirical_reference(base, real_action)


# ---------------------------------------------------------------------------
# Invariant Class 1: Exact Rational Utility Metrics
# ---------------------------------------------------------------------------

def test_exact_rational_utility_metrics_zero_floats() -> None:
    """Invariant: Utility metrics u_margin, u_fuel, u_goal are strictly in [0, 1] cap Q."""
    base = _make_base_model()
    env = ViabilityEnvelope(max_data=6, max_forms=4, max_arity=3, max_insts=5)
    evaluator = CausalEvaluator()

    # Action costs 2 fuel out of 6 remaining, with total fuel 10
    action = add_instance_action(form=0, args=(1,), fuel_cost=2)

    eval_res = evaluator.evaluate_candidate(
        model=base,
        action=action,
        envelope=env,
        fuel_remaining=6,
        total_fuel=10,
        goal_formula=Identity("0", "0"),  # Evaluates to 1
    )

    assert eval_res.viable
    u_margin = eval_res.u_margin
    u_fuel = eval_res.u_fuel
    u_goal = eval_res.u_goal

    # Verify exact types
    assert isinstance(u_margin, Fraction)
    assert isinstance(u_fuel, Fraction)
    assert isinstance(u_goal, Fraction)
    assert not isinstance(u_margin, float)
    assert not isinstance(u_fuel, float)
    assert not isinstance(u_goal, float)

    # Check exact values:
    # In projected state: n_data=3, n_forms=2, insts=2. Ceilings: data=6, forms=4, insts=5.
    # Ratios: 3/6 = 1/2, 2/4 = 1/2, 2/5. Max ratio = 1/2. Margin = 1 - 1/2 = 1/2.
    assert u_margin == Fraction(1, 2)
    # Fuel: remaining after = 6 - 2 = 4. Total = 10. u_fuel = 4/10 = 2/5.
    assert u_fuel == Fraction(2, 5)
    # Goal: 1/1
    assert u_goal == Fraction(1, 1)


# ---------------------------------------------------------------------------
# Invariant Class 1: Pareto Dominance & Selection
# ---------------------------------------------------------------------------

def test_pareto_dominance_logic() -> None:
    """Invariant: u dominates v iff for all k u_k >= v_k and for some k u_k > v_k."""
    selector = MulticriteriaSelector()

    u = (Fraction(3, 4), Fraction(1, 2), Fraction(1, 1))
    v = (Fraction(1, 2), Fraction(1, 2), Fraction(1, 1))
    w = (Fraction(3, 4), Fraction(1, 2), Fraction(1, 1))  # identical to u
    z = (Fraction(1, 1), Fraction(1, 4), Fraction(1, 1))  # incomparable with u

    # u dominates v (strictly better in first coordinate, equal in rest)
    assert selector.dominates(u, v)
    assert not selector.dominates(v, u)

    # u does not dominate itself
    assert not selector.dominates(u, w)

    # u and z are incomparable (trade-off)
    assert not selector.dominates(u, z)
    assert not selector.dominates(z, u)


def test_pareto_frontier_filters_dominated_candidates() -> None:
    """Invariant: The Pareto frontier prunes dominated evaluations."""
    selector = MulticriteriaSelector()

    act1 = CandidateAction(name="a1", fuel_cost=1, delta_fn=lambda m: m)
    act2 = CandidateAction(name="a2", fuel_cost=2, delta_fn=lambda m: m)
    act3 = CandidateAction(name="a3", fuel_cost=3, delta_fn=lambda m: m)

    # e1 dominates e2; e3 is incomparable with e1
    e1 = ActionEvaluation(
        action=act1,
        viable=True,
        utilities=(Fraction(3, 4), Fraction(3, 4), Fraction(1, 1)),
    )
    e2 = ActionEvaluation(
        action=act2,
        viable=True,
        utilities=(Fraction(1, 2), Fraction(1, 2), Fraction(1, 1)),  # dominated by e1
    )
    e3 = ActionEvaluation(
        action=act3,
        viable=True,
        utilities=(Fraction(1, 1), Fraction(1, 2), Fraction(1, 1)),  # higher margin, lower fuel
    )

    frontier = selector.pareto_frontier([e1, e2, e3])
    names = [e.action.name for e in frontier]

    assert "a1" in names
    assert "a3" in names
    assert "a2" not in names  # Dominated candidate eliminated


def test_canonical_tie_breaking() -> None:
    """Invariant: When multiple Pareto-optimal actions share maximal utility,
    tie-breaking is deterministically resolved by canonical key order.
    """
    selector = MulticriteriaSelector(
        weights=(Fraction(1, 2), Fraction(1, 2), Fraction(0, 1))
    )

    # Two actions with identical utility vectors
    act_beta = CandidateAction(name="action_beta", fuel_cost=1, delta_fn=lambda m: m)
    act_alpha = CandidateAction(name="action_alpha", fuel_cost=1, delta_fn=lambda m: m)

    canon_beta = (2, (1,), ((0, (1,)),), (), ())
    canon_alpha = (2, (1,), ((0, (0,)),), (), ())

    e_beta = ActionEvaluation(
        action=act_beta,
        viable=True,
        utilities=(Fraction(1, 2), Fraction(1, 2), Fraction(1, 1)),
        canon_key=canon_beta,
    )
    e_alpha = ActionEvaluation(
        action=act_alpha,
        viable=True,
        utilities=(Fraction(1, 2), Fraction(1, 2), Fraction(1, 1)),
        canon_key=canon_alpha,
    )

    # Regardless of input presentation order, the canonical key winner is selected deterministically
    selected_1 = selector.select([e_beta, e_alpha])
    selected_2 = selector.select([e_alpha, e_beta])

    assert selected_1 is not None
    assert selected_2 is not None
    assert selected_1.action.name == selected_2.action.name
    # CanonKey canon_alpha sorts before canon_beta
    assert selected_1.action.name == "action_alpha"


# ---------------------------------------------------------------------------
# Invariant Class 2: Finite Memory Horizon & FIFO Eviction
# ---------------------------------------------------------------------------

def test_finite_memory_horizon_fifo_eviction() -> None:
    """Invariant: BoundedMemory of depth H deterministically retains at most H records,
    evicting the oldest record upon capacity overflow.
    """
    H = 3
    mem = BoundedMemory(horizon=H)
    assert len(mem) == 0
    assert not mem.is_full()

    def _rec(i: int) -> MemoryRecord:
        return MemoryRecord(
            step_index=i,
            pre_state_digest=f"pre_{i}",
            action_repr=f"act_{i}",
            readout=RationalValuation(Fraction(1, 1)),
            post_state_digest=f"post_{i}",
            fuel_cost=1,
        )

    mem = mem.append(_rec(1))
    mem = mem.append(_rec(2))
    assert len(mem) == 2
    assert not mem.is_full()

    mem = mem.append(_rec(3))
    assert len(mem) == 3
    assert mem.is_full()
    assert [r.step_index for r in mem.records] == [1, 2, 3]

    # Append 4th record: oldest (1) is evicted
    mem = mem.append(_rec(4))
    assert len(mem) == 3
    assert [r.step_index for r in mem.records] == [2, 3, 4]

    # Append 5th record: oldest (2) is evicted
    mem = mem.append(_rec(5))
    assert len(mem) == 3
    assert [r.step_index for r in mem.records] == [3, 4, 5]
