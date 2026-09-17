"""Tests for belief revision trees and autonomous multi-hypothesis reasoning.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats in logical decisions.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import pytest

from research.endogenous_continuum.belief_revision_tree import (
    AutonomousTreeReasoningCoordinator,
    BranchingHypothesisTree,
    Contradiction,
    Formula,
    HypothesisTreeNode,
    Justification,
    JustificationKind,
    ReachabilityHypothesis,
    RefutationWitness,
    RevisionReceipt,
    TMSNode,
    TreeReasoningCoordinatorReceipt,
    TreeTMS,
)
from research.endogenous_continuum.interval_domain import DyadicInterval


class TestBranchingHypothesisTree:
    """Test structural operations, subtree budgeting, and pruning on hypothesis trees."""

    def test_tree_construction_and_hierarchy(self) -> None:
        """Tree properly records parent-child relationships and node metadata."""
        tree = BranchingHypothesisTree("root", "state_0", root_budget=0)
        assert tree.root_id == "root"
        assert len(tree.nodes) == 1

        child1 = tree.add_child("n1", "root", "state_1", allocated_budget=Fraction(2, 1), entrenchment=2)
        child2 = tree.add_child("n2", "root", "state_2", allocated_budget=Fraction(3, 1), entrenchment=1)
        subchild1 = tree.add_child("n1_1", "n1", "state_1_1", allocated_budget=Fraction(1, 1))

        assert child1.parent_id == "root"
        assert child2.parent_id == "root"
        assert subchild1.parent_id == "n1"
        assert tree.nodes["root"].children == ["n1", "n2"]
        assert tree.nodes["n1"].children == ["n1_1"]

    def test_subtree_budget_and_pruning(self) -> None:
        """Pruning a branch deactivates the entire subtree and reclaims 100% of its budget."""
        tree = BranchingHypothesisTree("root", "state_0")
        tree.add_child("b1", "root", "state_b1", allocated_budget=Fraction(2, 1))
        tree.add_child("b1_1", "b1", "state_b1_1", allocated_budget=Fraction(1, 1))
        tree.add_child("b1_2", "b1", "state_b1_2", allocated_budget=Fraction(3, 2))
        tree.add_child("b2", "root", "state_b2", allocated_budget=Fraction(5, 1))

        # Subtree budget under b1 is 2 + 1 + 3/2 = 9/2
        assert tree.get_subtree_budget("b1") == Fraction(9, 2)
        assert tree.get_subtree_budget("b2") == Fraction(5, 1)

        # Prune subtree b1
        retracted, reclaimed = tree.prune_subtree("b1")
        assert retracted == frozenset({"b1", "b1_1", "b1_2"})
        assert reclaimed == Fraction(9, 2)

        # Descendants must be inactive
        assert not tree.nodes["b1"].is_active
        assert not tree.nodes["b1_1"].is_active
        assert not tree.nodes["b1_2"].is_active

        # Surviving branch b2 remains active
        assert tree.nodes["b2"].is_active
        assert tree.get_subtree_budget("b1") == Fraction(0, 1)
        assert tree.get_subtree_budget("b2") == Fraction(5, 1)

        # Pruning already inactive subtree returns empty
        retracted_again, reclaimed_again = tree.prune_subtree("b1")
        assert retracted_again == frozenset()
        assert reclaimed_again == Fraction(0, 1)

    def test_negative_controls_tree(self) -> None:
        """Tree must reject duplicates, nonexistent parents, negative budgets, and invalid entrenchment."""
        tree = BranchingHypothesisTree("root", "state_0")

        # Duplicate ID
        with pytest.raises(ValueError, match="already exists"):
            tree.add_child("root", "root", "state_dup", allocated_budget=1)

        # Nonexistent parent
        with pytest.raises(KeyError, match="not found"):
            tree.add_child("c1", "nonexistent", "state_c1", allocated_budget=1)

        # Negative budget
        with pytest.raises(ValueError, match="negative"):
            tree.add_child("c2", "root", "state_c2", allocated_budget=Fraction(-1, 1))

        # Entrenchment < 1
        with pytest.raises(ValueError, match="Entrenchment must be >= 1"):
            tree.add_child("c3", "root", "state_c3", allocated_budget=1, entrenchment=0)

        # Nonexistent subtree queries
        with pytest.raises(KeyError, match="not in tree"):
            tree.get_subtree_nodes("ghost")


class TestTreeTMS:
    """Test endogenous Truth Maintenance System and AGM belief revision postulates."""

    def test_agm_postulates_and_conflict_resolution(self) -> None:
        """TMS must satisfy AGM Inclusion, Consistency, Success, and Vacuity."""
        tms = TreeTMS()

        # 1. Register hypotheses
        tms.register_tree_hypothesis("h1", "target_1", Fraction(2, 1), entrenchment=1)
        tms.register_tree_hypothesis("h2", "target_2", Fraction(3, 1), entrenchment=2)
        assert tms.active_hypotheses == frozenset({"h1", "h2"})

        # Record dual refutation for h1
        ref_id, contra_id = tms.record_dual_refutation(
            "h1", "target_1", dual_bound=Fraction(5, 1), budget=Fraction(2, 1)
        )
        assert "h1" in tms.active_hypotheses

        # 2. Revise h1 (AGM Retraction)
        receipt = tms.revise("h1")

        # AGM Success: retracted hypothesis is no longer active
        assert "h1" not in tms.active_hypotheses
        assert receipt.retracted_hypotheses == frozenset({"h1"})

        # AGM Consistency: the conflict set is resolved
        assert "hyp:h1" in receipt.deactivated_nodes
        assert "bot:h1" in receipt.deactivated_nodes
        assert all("h1" not in cs for cs in tms._active_conflicts)
        assert receipt.conflict_sets == (frozenset({"h1"}),)

        # AGM Inclusion: surviving beliefs are a subset of initial beliefs
        assert "hyp:h2" in receipt.surviving_beliefs
        assert "hyp:h1" not in receipt.surviving_beliefs

        # 3. AGM Vacuity: retracting an unasserted hypothesis changes nothing
        vacuous_receipt = tms.revise("h_unasserted")
        assert vacuous_receipt.retracted_hypotheses == frozenset()
        assert vacuous_receipt.deactivated_nodes == ()
        assert vacuous_receipt.justification_hash == hashlib.sha256(b"vacuous").hexdigest()

    def test_tms_receipt_determinism(self) -> None:
        """Identical sequences of TMS operations produce bit-for-bit identical hashes."""
        def run_sim() -> RevisionReceipt:
            tms = TreeTMS()
            tms.register_tree_hypothesis("node_A", "target_A", Fraction(4, 1))
            tms.record_dual_refutation("node_A", "target_A", Fraction(6, 1), Fraction(4, 1))
            return tms.revise("node_A")

        rec1 = run_sim()
        rec2 = run_sim()
        assert rec1.justification_hash == rec2.justification_hash
        assert rec1.deactivated_nodes == rec2.deactivated_nodes


class TestAutonomousTreeReasoningCoordinator:
    """Test full multi-hypothesis tree exploration, pruning, and budget reallocation."""

    def test_subtree_pruning_and_starvation_avoidance(self) -> None:
        """Refuted subtree yields 100% budget reclamation and prevents starvation in alternative branch."""
        # Domain: Scale 4 interval movegraph (step cost = 1/16 per edge)
        # Root interval: [0/16, 1/16]
        # Branch 1 (Unreachable within budget): target index 15 (bound = 15/16) with initial budget 1/16
        #   Subchild 1_1: target index 14 with budget 1/16
        # Branch 2 (Reachable): target index 2 (requires 2 * 1/16 = 1/8) with initial budget 1/16
        #   Under initial allocation (1/16 < 1/8), Branch 2 would starve!
        # Reclaiming 1/16 + 1/16 from Branch 1 transfers budget to Branch 2, enabling solution.
        coordinator = AutonomousTreeReasoningCoordinator(
            fine_scale=4,
            coarse_scale=2,
            total_budget=Fraction(1, 2),
        )

        root_interval = DyadicInterval(scale=4, index=0)
        tree = BranchingHypothesisTree("root", root_interval)

        # Branch 1: allocated 1/16 + 1/16 = 1/8 total
        tree.add_child(
            "branch_far",
            "root",
            DyadicInterval(scale=4, index=15),
            allocated_budget=Fraction(1, 16),
            description="Far target",
        )
        tree.add_child(
            "branch_far_sub",
            "branch_far",
            DyadicInterval(scale=4, index=14),
            allocated_budget=Fraction(1, 16),
            description="Far subtarget",
        )

        # Branch 2: allocated initial 1/16, but traversal to index 2 needs 1/8!
        tree.add_child(
            "branch_near",
            "root",
            DyadicInterval(scale=4, index=2),
            allocated_budget=Fraction(1, 16),
            description="Reachable target requiring cost 1/8",
        )

        outcomes, receipt = coordinator.run_tree(root_interval, tree)

        # Verification:
        # 1. Branch far was certified refused because dual bound (15/16) > budget (1/16)
        assert outcomes["branch_far"]["status"] == "CERTIFIED_REFUSED"
        assert "branch_far_sub" in outcomes["branch_far"]["retracted_subtree"]

        # 2. Reclaimed budget from branch_far subtree was transferred to branch_near
        # Initial branch_near budget was 1/16. Reclaimed from far branch: 1/16 + 1/16 = 1/8.
        # Plus unallocated initial leftover (1/2 - 3/16 = 5/16).
        # branch_near received enough budget and SOLVED!
        assert outcomes["branch_near"]["status"] == "SOLVED"
        assert outcomes["branch_near"]["cost"] == Fraction(1, 8)

        # 3. Full conservation
        assert receipt.budget_conservation_verified
        assert receipt.nodes_pruned >= 1
        assert receipt.nodes_solved == 1
        assert receipt.revision_count >= 1
        assert coordinator.ledger.audit_conservation()

    def test_cryptographic_receipt_determinism(self) -> None:
        """Coordinator produces bit-for-bit identical trace digests and receipts on identical inputs."""
        def execute() -> TreeReasoningCoordinatorReceipt:
            coord = AutonomousTreeReasoningCoordinator(
                fine_scale=4,
                coarse_scale=2,
                total_budget=Fraction(1, 2),
            )
            root_interval = DyadicInterval(scale=4, index=0)
            t = BranchingHypothesisTree("root", root_interval)
            t.add_child(
                "far", "root", DyadicInterval(scale=4, index=12), allocated_budget=Fraction(1, 16)
            )
            t.add_child(
                "near", "root", DyadicInterval(scale=4, index=1), allocated_budget=Fraction(1, 16)
            )
            _, rec = coord.run_tree(root_interval, t)
            return rec

        r1 = execute()
        r2 = execute()
        assert r1.trace_digest == r2.trace_digest
        assert r1.digest() == r2.digest()
        assert r1.nodes_solved == r2.nodes_solved
        assert r1.nodes_pruned == r2.nodes_pruned
