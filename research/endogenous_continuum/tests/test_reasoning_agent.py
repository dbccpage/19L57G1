"""Tests for Autonomous Reasoning Agent with Adaptive Budget Re-allocation.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats in logical decisions.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from research.endogenous_continuum.interval_domain import (
    DyadicInterval,
    create_interval_coarsening_map,
    create_interval_movegraph,
)
from research.endogenous_continuum.reasoning_agent import (
    AutonomousReasoningAgent,
    BudgetLedger,
    CandidateGoal,
    GoalOutcome,
    ReasoningActionType,
    ReasoningAgentReceipt,
)


class TestBudgetLedger:
    """Test unit behavior and exact conservation invariants of BudgetLedger."""

    def test_budget_conservation_across_lifecycle(self) -> None:
        """Ledger must preserve exact budget conservation across allocation, consumption, and reclamation."""
        total = Fraction(10, 1)
        ledger = BudgetLedger(total_budget=total, unallocated_budget=total)
        assert ledger.audit_conservation()

        # Allocate to goal 1 and goal 2
        ledger.allocate("g1", Fraction(3, 1))
        ledger.allocate("g2", Fraction(4, 1))
        assert ledger.unallocated_budget == Fraction(3, 1)
        assert ledger.audit_conservation()

        # Consume part of g1
        ledger.consume("g1", Fraction(1, 1))
        assert ledger.consumed_budget == Fraction(1, 1)
        assert ledger.allocated_budgets["g1"] == Fraction(2, 1)
        assert ledger.audit_conservation()

        # Reclaim remaining g1
        reclaimed = ledger.reclaim("g1")
        assert reclaimed == Fraction(2, 1)
        assert ledger.unallocated_budget == Fraction(5, 1)
        assert "g1" not in ledger.allocated_budgets
        assert ledger.audit_conservation()

        # Redistribute unallocated to g2
        ledger.redistribute_unallocated(["g2"])
        assert ledger.unallocated_budget == Fraction(0, 1)
        assert ledger.allocated_budgets["g2"] == Fraction(9, 1)
        assert ledger.audit_conservation()

    def test_negative_controls_ledger(self) -> None:
        """Ledger must reject invalid values and budget overdraws."""
        total = Fraction(5, 1)
        ledger = BudgetLedger(total_budget=total, unallocated_budget=total)

        with pytest.raises(ValueError, match="negative"):
            ledger.allocate("g1", Fraction(-1, 1))

        with pytest.raises(ValueError, match="Insufficient unallocated budget"):
            ledger.allocate("g1", Fraction(6, 1))

        ledger.allocate("g1", Fraction(2, 1))
        with pytest.raises(ValueError, match="negative"):
            ledger.consume("g1", Fraction(-1, 1))

        with pytest.raises(ValueError, match="exceeded allocated budget"):
            ledger.consume("g1", Fraction(3, 1))

        with pytest.raises(ValueError, match="negative"):
            BudgetLedger(total_budget=Fraction(-1, 1), unallocated_budget=Fraction(0, 1))


class TestAutonomousReasoningAgent:
    """Test autonomous reasoning loop, hierarchical pruning, and adaptive re-allocation."""

    def test_starvation_avoidance_via_reallocation(self) -> None:
        """A reachable goal that would starve under static allocation succeeds via reclaimed budget."""
        # Scale 4 fine graph (16 intervals [i/16, (i+1)/16])
        # Coarse scale 2 (4 intervals [j/4, (j+1)/4])
        agent = AutonomousReasoningAgent(
            fine_scale=4,
            coarse_scale=2,
            total_budget=Fraction(1, 2),  # Total budget = 1/2
        )

        # Source at interval [0, 1/16]
        source = DyadicInterval(scale=4, index=0)

        # Goal A: Target at interval 14 (coarse index 2).
        # Coarse bound is 1/2. Under initial split 1/4, it is provably unreachable and refused.
        goal_a = CandidateGoal(
            goal_id="goal_unreachable",
            target=DyadicInterval(scale=4, index=14),
            priority=1,
            description="Far interval beyond initial budget",
        )

        # Goal B: Target at interval 5 (coarse index 1).
        # Coarse bound is 1/4 <= 1/4 (survives coarse probe).
        # Fine path requires 5 steps * 1/16 = 5/16 > 1/4 (would starve under static allocation).
        # With reclaimed budget from Goal A (boosted to 1/2), it succeeds.
        goal_b = CandidateGoal(
            goal_id="goal_reachable",
            target=DyadicInterval(scale=4, index=5),
            priority=1,
            description="Moderate interval reachable with boosted budget",
        )

        outcomes, receipt = agent.run(source=source, goals=[goal_a, goal_b])

        # Goal A must be certified refused at coarse level with 0 fine nodes explored
        assert outcomes["goal_unreachable"].status == "CERTIFIED_REFUSED"
        assert outcomes["goal_unreachable"].fine_nodes_explored == 0
        assert outcomes["goal_unreachable"].coarse_pruned is True

        # Goal B must be solved because it received the reclaimed budget from Goal A
        assert outcomes["goal_reachable"].status == "SOLVED"
        assert outcomes["goal_reachable"].path is not None
        assert outcomes["goal_reachable"].cost is not None

        # Verify receipt invariants
        assert receipt.budget_conservation_verified is True
        assert receipt.goals_total == 2
        assert receipt.goals_solved == 1
        assert receipt.goals_refused == 1
        assert receipt.goals_exhausted == 0
        assert receipt.reclaimed_budget > 0
        assert receipt.total_fine_nodes_explored > 0

    def test_all_goals_certified_refused(self) -> None:
        """When all goals are beyond budget, both are pruned in 0 fine nodes and full budget preserved."""
        agent = AutonomousReasoningAgent(
            fine_scale=4,
            coarse_scale=2,
            total_budget=Fraction(1, 8),  # Very small budget
        )
        source = DyadicInterval(scale=4, index=0)
        goal_1 = CandidateGoal(goal_id="far_1", target=DyadicInterval(scale=4, index=10))
        goal_2 = CandidateGoal(goal_id="far_2", target=DyadicInterval(scale=4, index=14))

        outcomes, receipt = agent.run(source=source, goals=[goal_1, goal_2])

        assert outcomes["far_1"].status == "CERTIFIED_REFUSED"
        assert outcomes["far_1"].fine_nodes_explored == 0
        assert outcomes["far_2"].status == "CERTIFIED_REFUSED"
        assert outcomes["far_2"].fine_nodes_explored == 0

        assert receipt.total_fine_nodes_explored == 0
        assert receipt.goals_refused == 2
        assert receipt.goals_solved == 0
        assert receipt.budget_conservation_verified is True

    def test_receipt_digest_determinism(self) -> None:
        """Repeated agent execution on identical inputs produces bit-for-bit identical trace digests."""
        source = DyadicInterval(scale=4, index=0)
        goals = [
            CandidateGoal(goal_id="g1", target=DyadicInterval(scale=4, index=1)),
            CandidateGoal(goal_id="g2", target=DyadicInterval(scale=4, index=2)),
        ]

        agent1 = AutonomousReasoningAgent(fine_scale=4, coarse_scale=2, total_budget=Fraction(1, 1))
        _, receipt1 = agent1.run(source=source, goals=goals)

        agent2 = AutonomousReasoningAgent(fine_scale=4, coarse_scale=2, total_budget=Fraction(1, 1))
        _, receipt2 = agent2.run(source=source, goals=goals)

        assert receipt1.trace_digest == receipt2.trace_digest
        assert receipt1.digest() == receipt2.digest()

    def test_empty_goals_behavior(self) -> None:
        """Empty goals list returns empty outcomes and clean receipt."""
        agent = AutonomousReasoningAgent(fine_scale=4, coarse_scale=2, total_budget=Fraction(1, 1))
        source = DyadicInterval(scale=4, index=0)
        outcomes, receipt = agent.run(source=source, goals=[])

        assert outcomes == {}
        assert receipt.goals_total == 0
        assert receipt.goals_solved == 0
        assert receipt.budget_conservation_verified is True

    def test_adversarial_rejections(self) -> None:
        """Negative controls: invalid priority, invalid budget types, etc."""
        with pytest.raises(ValueError, match="Priority must be strictly positive"):
            CandidateGoal(goal_id="bad", target=0, priority=0)

        with pytest.raises(ValueError, match="Priority must be strictly positive"):
            CandidateGoal(goal_id="bad", target=0, priority=-2)

        with pytest.raises(TypeError, match="float"):
            AutonomousReasoningAgent(total_budget=1.5)  # type: ignore[arg-type]
