"""Tests for deterministic budgeted search and exact re-allocation.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats in logical decisions.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from research.endogenous_continuum.interval_domain import (
    DyadicInterval,
)
from research.endogenous_continuum.reasoning_agent import (
    BudgetedReasoningCoordinator,
    BudgetLedger,
    CandidateGoal,
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

        with pytest.raises(ValueError, match="violates conservation"):
            BudgetLedger(total_budget=Fraction(5, 1), unallocated_budget=Fraction(4, 1))

        with pytest.raises(TypeError, match="exact rational"):
            BudgetLedger(total_budget=5.0, unallocated_budget=5)  # type: ignore[arg-type]

        fresh = BudgetLedger(total_budget=total, unallocated_budget=total)
        with pytest.raises(ValueError, match="must be unique"):
            fresh.redistribute_unallocated(["g1", "g1"])

        with pytest.raises(ValueError, match="cannot be negative"):
            fresh.redistribute_unallocated(
                ["g1", "g2"],
                weights={"g1": Fraction(1, 1), "g2": Fraction(-1, 1)},
            )


class TestBudgetedReasoningCoordinator:
    """Test exact bound screening, checked search, and budget re-allocation."""

    def test_reclaimed_budget_is_reallocated_to_viable_goal(self) -> None:
        """A viable goal receives the exact budget reclaimed from a refusal."""
        agent = BudgetedReasoningCoordinator(
            fine_scale=4,
            coarse_scale=2,
            total_budget=Fraction(1, 2),
        )

        source = DyadicInterval(scale=4, index=0)

        # Priority weights allocate 1/6 to A and 1/3 to B. A's exact path
        # bound is 7/8, so its 1/6 is reclaimed.
        goal_a = CandidateGoal(
            goal_id="goal_unreachable",
            target=DyadicInterval(scale=4, index=14),
            priority=1,
            description="Far interval beyond initial budget",
        )

        # B's exact bound is 5/16, within its initial 1/3. Re-allocation then
        # raises the available budget to 1/2 before path search.
        goal_b = CandidateGoal(
            goal_id="goal_reachable",
            target=DyadicInterval(scale=4, index=5),
            priority=2,
            description="Moderate interval reachable with boosted budget",
        )

        outcomes, receipt = agent.run(source=source, goals=[goal_a, goal_b])

        # Screening computes an exact fine potential, then avoids a separate
        # path-search expansion for A.
        assert outcomes["goal_unreachable"].status == "CERTIFIED_REFUSED"
        assert outcomes["goal_unreachable"].fine_nodes_explored == 0
        assert outcomes["goal_unreachable"].coarse_pruned is False

        assert outcomes["goal_reachable"].status == "SOLVED"
        assert outcomes["goal_reachable"].path is not None
        assert outcomes["goal_reachable"].cost == Fraction(5, 16)
        assert outcomes["goal_reachable"].budget_allocated == Fraction(1, 2)

        # Verify receipt invariants
        assert receipt.budget_conservation_verified is True
        assert receipt.goals_total == 2
        assert receipt.goals_solved == 1
        assert receipt.goals_refused == 1
        assert receipt.goals_exhausted == 0
        assert receipt.reclaimed_budget > 0
        assert receipt.total_fine_nodes_explored > 0

    def test_all_goals_certified_refused(self) -> None:
        """Exact bounds can refuse every allocation before separate path search."""
        agent = BudgetedReasoningCoordinator(
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

        agent1 = BudgetedReasoningCoordinator(
            fine_scale=4, coarse_scale=2, total_budget=Fraction(1, 1)
        )
        _, receipt1 = agent1.run(source=source, goals=goals)

        agent2 = BudgetedReasoningCoordinator(
            fine_scale=4, coarse_scale=2, total_budget=Fraction(1, 1)
        )
        _, receipt2 = agent2.run(source=source, goals=goals)

        assert receipt1.trace_digest == receipt2.trace_digest
        assert receipt1.digest() == receipt2.digest()

    def test_empty_goals_behavior(self) -> None:
        """Empty goals list returns empty outcomes and clean receipt."""
        agent = BudgetedReasoningCoordinator(
            fine_scale=4, coarse_scale=2, total_budget=Fraction(1, 1)
        )
        source = DyadicInterval(scale=4, index=0)
        outcomes, receipt = agent.run(source=source, goals=[])

        assert outcomes == {}
        assert receipt.goals_total == 0
        assert receipt.goals_solved == 0
        assert receipt.budget_conservation_verified is True
        with pytest.raises(RuntimeError, match="one-shot"):
            agent.run(source=source, goals=[])

    def test_adversarial_rejections(self) -> None:
        """Negative controls: invalid priority, invalid budget types, etc."""
        with pytest.raises(ValueError, match="Priority must be strictly positive"):
            CandidateGoal(goal_id="bad", target=0, priority=0)

        with pytest.raises(ValueError, match="Priority must be strictly positive"):
            CandidateGoal(goal_id="bad", target=0, priority=-2)

        with pytest.raises(ValueError, match="non-empty"):
            CandidateGoal(goal_id="", target=0)

        with pytest.raises(TypeError, match="float"):
            BudgetedReasoningCoordinator(total_budget=1.5)  # type: ignore[arg-type]

        agent = BudgetedReasoningCoordinator()
        source = DyadicInterval(scale=4, index=0)
        duplicate_goals = [
            CandidateGoal(goal_id="same", target=DyadicInterval(scale=4, index=1)),
            CandidateGoal(goal_id="same", target=DyadicInterval(scale=4, index=2)),
        ]
        with pytest.raises(ValueError, match="must be unique"):
            agent.run(source=source, goals=duplicate_goals)

        fresh_agent = BudgetedReasoningCoordinator()
        with pytest.raises(KeyError, match="not in fine graph"):
            fresh_agent.run(
                source=source,
                goals=[CandidateGoal(goal_id="missing", target="not-a-state")],
            )
