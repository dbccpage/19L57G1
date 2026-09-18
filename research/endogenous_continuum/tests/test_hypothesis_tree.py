"""Tests for branching hypothesis trees, the support record, and the tree coordinator.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats in logical decisions.
"""

from __future__ import annotations

from fractions import Fraction
from types import SimpleNamespace
from typing import Any

import pytest

from research.endogenous_continuum.dual_relaxation import ExactPathSolver
from research.endogenous_continuum.hierarchical_search import HierarchicalSearchEngine
from research.endogenous_continuum.hypothesis_tree import (
    AutonomousTreeReasoningCoordinator,
    BranchingHypothesisTree,
    SupportRecord,
    TreeReasoningCoordinatorReceipt,
)
from research.endogenous_continuum.interval_domain import DyadicInterval, create_interval_movegraph

SOURCE = DyadicInterval(scale=4, index=0)


def at(index: int) -> DyadicInterval:
    """A scale-4 state; from SOURCE its exact distance is index / 16."""
    return DyadicInterval(scale=4, index=index)


def coordinator(total: Fraction) -> AutonomousTreeReasoningCoordinator:
    return AutonomousTreeReasoningCoordinator(fine_scale=4, coarse_scale=2, total_budget=total)


class TestBranchingHypothesisTree:
    """Structure, subtree budgets, and subtree deactivation."""

    def test_tree_construction_and_hierarchy(self) -> None:
        tree = BranchingHypothesisTree("root", "state_0", root_budget=0)
        child1 = tree.add_child("n1", "root", "state_1", allocated_budget=Fraction(2, 1))
        tree.add_child("n2", "root", "state_2", allocated_budget=Fraction(3, 1))
        subchild = tree.add_child("n1_1", "n1", "state_1_1", allocated_budget=Fraction(1, 1))

        assert child1.parent_id == "root" and subchild.parent_id == "n1"
        assert tree.nodes["root"].children == ["n1", "n2"]
        assert tree.nodes["n1"].children == ["n1_1"]
        assert tree.ancestors("n1_1") == ("n1",)
        assert tree.ancestors("n1") == ()

    def test_subtree_budget_and_pruning(self) -> None:
        tree = BranchingHypothesisTree("root", "state_0")
        tree.add_child("b1", "root", "s", allocated_budget=Fraction(2, 1))
        tree.add_child("b1_1", "b1", "s", allocated_budget=Fraction(1, 1))
        tree.add_child("b1_2", "b1", "s", allocated_budget=Fraction(3, 2))
        tree.add_child("b2", "root", "s", allocated_budget=Fraction(5, 1))
        assert tree.get_subtree_budget("b1") == Fraction(9, 2)

        retracted, declared = tree.prune_subtree("b1")
        assert retracted == frozenset({"b1", "b1_1", "b1_2"})
        assert declared == Fraction(9, 2)
        assert not any(tree.nodes[n].is_active for n in retracted)
        assert tree.nodes["b2"].is_active
        assert tree.get_subtree_budget("b1") == 0

        assert tree.prune_subtree("b1") == (frozenset(), Fraction(0, 1))

    def test_negative_controls_tree(self) -> None:
        tree = BranchingHypothesisTree("root", "state_0")
        with pytest.raises(ValueError, match="already exists"):
            tree.add_child("root", "root", "s", allocated_budget=1)
        with pytest.raises(KeyError, match="not found"):
            tree.add_child("c1", "nonexistent", "s", allocated_budget=1)
        with pytest.raises(ValueError, match="negative"):
            tree.add_child("c2", "root", "s", allocated_budget=Fraction(-1, 1))
        with pytest.raises(KeyError, match="not in tree"):
            tree.get_subtree_nodes("ghost")
        with pytest.raises(KeyError, match="not in tree"):
            tree.ancestors("ghost")
        tree.add_child("p", "root", "s", allocated_budget=1)
        tree.prune_subtree("p")
        with pytest.raises(ValueError, match="retracted"):
            tree.add_child("late", "p", "s", allocated_budget=1)
        with pytest.raises(ValueError, match="non-empty strings"):
            tree.add_child("", "root", "s", allocated_budget=1)
        with pytest.raises(TypeError, match="exact rational"):
            tree.add_child("f", "root", "s", allocated_budget=0.5)  # type: ignore[arg-type]


class TestSupportRecord:
    """Holding, refuting, and retracting records."""

    def test_retraction_resolves_the_recorded_conflict(self) -> None:
        record = SupportRecord()
        record.register_hypothesis("h1", "t1", Fraction(2, 1))
        record.register_hypothesis("h2", "t2", Fraction(3, 1))
        ref_id, contra_id = record.record_refutation("h1", "t1", Fraction(5, 1), Fraction(2, 1))
        assert (ref_id, contra_id) == ("ref:h1", "bot:h1")
        assert record.active_conflicts == frozenset({frozenset({"h1"})})
        before = set(record.nodes[n].node_id for n in record.nodes if record.nodes[n].is_active)

        receipt = record.retract("h1")

        assert receipt.retracted_hypotheses == frozenset({"h1"})
        assert receipt.deactivated_nodes == ("bot:h1", "hyp:h1")
        assert receipt.conflict_sets == (frozenset({"h1"}),)
        assert record.active_conflicts == frozenset()
        assert record.active_hypotheses == frozenset({"h2"})
        # Nothing new is held after a retraction, and the refutation itself stays.
        assert set(receipt.active_records) <= before
        assert "ref:h1" in receipt.active_records and "hyp:h2" in receipt.active_records

    def test_retracting_a_hypothesis_retracts_its_dependents(self) -> None:
        record = SupportRecord()
        record.register_hypothesis("p", "tp", Fraction(1, 1))
        record.register_hypothesis("c", "tc", Fraction(1, 1), depends_on=("p",))
        record.register_hypothesis("other", "to", Fraction(1, 1))

        receipt = record.retract("p")

        assert receipt.retracted_hypotheses == frozenset({"p", "c"})
        assert record.active_hypotheses == frozenset({"other"})
        assert not record.nodes["hyp:c"].is_active
        # No refutation was recorded, so no conflict set is reported.
        assert receipt.conflict_sets == ()

    def test_retracting_an_unheld_hypothesis_changes_nothing(self) -> None:
        record = SupportRecord()
        record.register_hypothesis("h", "t", Fraction(1, 1))
        first = record.retract("ghost")
        assert first.retracted_hypotheses == frozenset() and first.deactivated_nodes == ()
        assert record.active_hypotheses == frozenset({"h"})
        record.register_hypothesis("h2", "t", Fraction(1, 1))
        second = record.retract("ghost")
        # The checksum records the state, so different states give different checksums.
        assert first.justification_hash != second.justification_hash

    def test_negative_controls_support_record(self) -> None:
        record = SupportRecord()
        record.register_hypothesis("h", "t", Fraction(2, 1))
        with pytest.raises(ValueError, match="already registered"):
            record.register_hypothesis("h", "t", Fraction(2, 1))
        with pytest.raises(KeyError, match="not held"):
            record.register_hypothesis("c", "t", Fraction(1, 1), depends_on=("missing",))
        with pytest.raises(KeyError, match="No held hypothesis"):
            record.record_refutation("ghost", "t", Fraction(3, 1), Fraction(2, 1))
        with pytest.raises(ValueError, match="Not a refutation"):
            record.record_refutation("h", "t", Fraction(2, 1), Fraction(2, 1))
        with pytest.raises(TypeError, match="exact rational"):
            record.register_hypothesis("f", "t", 0.1)  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="exact rational"):
            record.record_refutation("h", "t", 0.3, Fraction(2, 1))  # type: ignore[arg-type]
        # No path at all is a refutation whatever the budget.
        record.record_refutation("h", "t", None, Fraction(2, 1))
        assert record.nodes["ref:h"].formula.to_dict()["dual_bound"] == "unreachable"

    def test_records_are_replaced_not_mutated(self) -> None:
        record = SupportRecord()
        record.register_hypothesis("h", "t", Fraction(1, 1))
        old = record.nodes["hyp:h"]
        held = {old}
        record.retract("h")
        assert old.is_active and old in held
        assert record.nodes["hyp:h"] is not old
        assert not record.nodes["hyp:h"].is_active

    def test_checksum_binds_the_refutation(self) -> None:
        def run(bound: Fraction) -> str:
            record = SupportRecord()
            record.register_hypothesis("h", "t", Fraction(1, 1))
            record.record_refutation("h", "t", bound, Fraction(1, 1))
            return record.retract("h").justification_hash

        assert run(Fraction(2, 1)) == run(Fraction(2, 1))
        assert run(Fraction(2, 1)) != run(Fraction(3, 1))


class TestAutonomousTreeReasoningCoordinator:
    """Screening, expansion, search, and retraction across a tree."""

    def test_refusal_records_a_witness_and_resolves_the_conflict(self) -> None:
        coord = coordinator(Fraction(1, 4))
        tree = BranchingHypothesisTree("root", SOURCE)
        tree.add_child("far", "root", at(14), allocated_budget=Fraction(1, 16))

        outcomes, receipt = coord.run_tree(SOURCE, tree)

        assert outcomes["far"]["status"] == "CERTIFIED_REFUSED"
        assert outcomes["far"]["exact_bound"] == Fraction(14, 16)
        # Refused against everything it could draw on: its slice plus the pool.
        assert outcomes["far"]["available"] == Fraction(1, 4)
        witness = coord.support.nodes["ref:far"].formula.to_dict()
        assert witness["dual_bound"] == "7/8"
        assert coord.support.active_conflicts == frozenset()
        assert receipt.nodes_refused == 1 and receipt.retraction_count == 1

    def test_reclaimed_budget_funds_a_later_hypothesis(self) -> None:
        # The declared slices use the whole budget, so the pool starts empty and
        # 'near' (exact cost 1/8, slice 1/16) can only be funded by reclaimed budget.
        def run(order: tuple[str, ...]) -> dict[str, Any]:
            coord = coordinator(Fraction(1, 8))
            tree = BranchingHypothesisTree("root", SOURCE)
            targets = {"far": at(14), "near": at(2)}
            for nid in order:
                tree.add_child(nid, "root", targets[nid], allocated_budget=Fraction(1, 16))
            outcomes, receipt = coord.run_tree(SOURCE, tree)
            return {"outcomes": outcomes, "receipt": receipt, "trace": coord.trace}

        far_first = run(("far", "near"))
        assert far_first["outcomes"]["near"]["status"] == "SOLVED"
        assert far_first["outcomes"]["near"]["cost"] == Fraction(1, 8)
        assert {"action": "DRAW", "node": "near", "drawn": "1/16"} in far_first["trace"]
        assert far_first["receipt"].reclaimed_budget == Fraction(1, 16)

        # Screened first, 'near' sees only its own slice and an empty pool.
        near_first = run(("near", "far"))
        assert near_first["outcomes"]["near"]["status"] == "CERTIFIED_REFUSED"

    def test_dependent_hypotheses_are_retracted_without_refutation(self) -> None:
        coord = coordinator(Fraction(1, 8))
        tree = BranchingHypothesisTree("root", SOURCE)
        tree.add_child("P", "root", at(14), allocated_budget=Fraction(1, 16))
        tree.add_child("C", "P", at(1), allocated_budget=Fraction(1, 16))

        outcomes, receipt = coord.run_tree(SOURCE, tree)

        assert outcomes["P"]["retracted_subtree"] == ["C", "P"]
        assert "C" not in outcomes
        assert "ref:C" not in coord.support.nodes
        assert coord.support.active_hypotheses == frozenset()
        # C is retracted because it rests on P, not because it was refuted: its
        # own target is reachable within its own slice.
        potential = ExactPathSolver.compute_dual_potential(coord.fine_graph, SOURCE)
        assert potential.potential_difference(SOURCE, at(1)) == Fraction(1, 16)
        assert receipt.nodes_refused == 1 and receipt.nodes_retracted == 2

    def test_expanded_node_releases_its_slice_to_its_children(self) -> None:
        coord = coordinator(Fraction(3, 16))
        tree = BranchingHypothesisTree("root", SOURCE)
        tree.add_child("P", "root", at(1), allocated_budget=Fraction(1, 8))
        tree.add_child("C", "P", at(3), allocated_budget=Fraction(1, 16))

        outcomes, receipt = coord.run_tree(SOURCE, tree)

        assert outcomes["P"]["status"] == "EXPANDED"
        assert outcomes["C"]["status"] == "SOLVED"
        assert outcomes["C"]["cost"] == Fraction(3, 16)
        assert coord.ledger.allocated_budgets == {}
        assert receipt.nodes_expanded == 1 and receipt.nodes_solved == 1

    def test_zero_budget_node_leaves_no_open_contradiction(self) -> None:
        coord = coordinator(Fraction(1, 16))
        tree = BranchingHypothesisTree("root", SOURCE)
        tree.add_child("Z", "root", at(14), allocated_budget=0)

        outcomes, _ = coord.run_tree(SOURCE, tree)

        assert outcomes["Z"]["status"] == "CERTIFIED_REFUSED"
        assert coord.support.active_conflicts == frozenset()
        assert not coord.support.nodes["bot:Z"].is_active

    def test_receipt_reports_what_the_ledger_moved(self) -> None:
        coord = coordinator(Fraction(1, 2))
        tree = BranchingHypothesisTree("root", SOURCE)
        tree.add_child("A", "root", at(14), allocated_budget=Fraction(1, 16))
        tree.add_child("B", "root", at(13), allocated_budget=Fraction(1, 16))

        reclaims: list[Fraction] = []
        original = coord.ledger.reclaim

        def spy(goal_id: str) -> Fraction:
            amount = original(goal_id)
            reclaims.append(amount)
            return amount

        coord.ledger.reclaim = spy  # type: ignore[method-assign]
        _, receipt = coord.run_tree(SOURCE, tree)

        assert receipt.reclaimed_budget == sum(reclaims, Fraction(0, 1))
        assert receipt.budget_conservation_verified

    def test_reclaimed_budget_never_exceeds_the_declared_slices(self) -> None:
        # Five solved leaves and a chain of expanded nodes: every node returns at
        # most its declared slice, once.
        coord = coordinator(Fraction(1, 1))
        tree = BranchingHypothesisTree("root", SOURCE)
        for i in range(5):
            tree.add_child(f"leaf{i}", "root", at(1), allocated_budget=Fraction(1, 5))
        _, receipt = coord.run_tree(SOURCE, tree)
        assert receipt.reclaimed_budget == 5 * (Fraction(1, 5) - Fraction(1, 16))

        chain = coordinator(Fraction(1, 1))
        deep = BranchingHypothesisTree("root", SOURCE)
        parent = "root"
        for i in range(20):
            deep.add_child(f"n{i}", parent, at(1), allocated_budget=0)
            parent = f"n{i}"
        outcomes, deep_receipt = chain.run_tree(SOURCE, deep)
        assert outcomes["n19"]["status"] == "SOLVED"
        assert deep_receipt.reclaimed_budget == 0
        assert deep_receipt.reclaimed_budget <= deep_receipt.total_initial_budget

    def test_trace_binds_what_was_solved(self) -> None:
        def run(index: int) -> TreeReasoningCoordinatorReceipt:
            coord = coordinator(Fraction(1, 2))
            tree = BranchingHypothesisTree("root", SOURCE)
            tree.add_child("g", "root", at(index), allocated_budget=Fraction(1, 2))
            return coord.run_tree(SOURCE, tree)[1]

        assert run(1).trace_digest == run(1).trace_digest
        assert run(1).digest() == run(1).digest()
        assert run(1).trace_digest != run(5).trace_digest

    def test_invalid_target_is_rejected_before_any_change(self) -> None:
        coord = coordinator(Fraction(1, 2))
        tree = BranchingHypothesisTree("root", SOURCE)
        tree.add_child("ok", "root", at(1), allocated_budget=Fraction(1, 16))
        tree.add_child("bad", "root", DyadicInterval(scale=4, index=15), allocated_budget=Fraction(1, 16))

        with pytest.raises(KeyError, match="not in fine graph"):
            coord.run_tree(SOURCE, tree)
        assert coord.ledger.allocated_budgets == {} and coord.trace == []
        assert coord.support.active_hypotheses == frozenset()
        assert all(n.is_active for n in tree.nodes.values())

    def test_preconditions_are_checked_before_any_change(self) -> None:
        tree = BranchingHypothesisTree("root", SOURCE)
        tree.add_child("a", "root", at(1), allocated_budget=Fraction(1, 2))
        tree.add_child("b", "root", at(2), allocated_budget=Fraction(1, 2))

        over = coordinator(Fraction(1, 2))
        with pytest.raises(ValueError, match="exceed the total budget"):
            over.run_tree(SOURCE, tree)
        assert over.ledger.allocated_budgets == {}

        with pytest.raises(KeyError, match="Source state"):
            coordinator(Fraction(1, 1)).run_tree("nowhere", tree)

        tree.prune_subtree("b")
        with pytest.raises(ValueError, match="already retracted"):
            coordinator(Fraction(1, 1)).run_tree(SOURCE, tree)

        elsewhere = BranchingHypothesisTree("root", at(14))
        elsewhere.add_child("a", "root", at(1), allocated_budget=Fraction(1, 16))
        with pytest.raises(ValueError, match="root state"):
            coordinator(Fraction(1, 1)).run_tree(SOURCE, elsewhere)

        funded_root = BranchingHypothesisTree("root", SOURCE, root_budget=Fraction(1, 4))
        funded_root.add_child("a", "root", at(1), allocated_budget=Fraction(1, 16))
        with pytest.raises(ValueError, match="root holds no hypothesis"):
            coordinator(Fraction(1, 1)).run_tree(SOURCE, funded_root)

    def test_mismatched_graphs_are_rejected_before_any_change(self) -> None:
        source = DyadicInterval(scale=3, index=0)
        coord = AutonomousTreeReasoningCoordinator(
            fine_scale=4,
            coarse_scale=2,
            total_budget=Fraction(1, 1),
            fine_graph=create_interval_movegraph(scale=3),
        )
        tree = BranchingHypothesisTree("root", source)
        tree.add_child("g", "root", DyadicInterval(scale=3, index=6), allocated_budget=Fraction(1, 8))

        with pytest.raises(ValueError, match="morphism"):
            coord.run_tree(source, tree)
        assert tree.nodes["g"].is_active and coord.trace == []

    def test_coordinator_is_one_shot(self) -> None:
        coord = coordinator(Fraction(1, 2))
        tree = BranchingHypothesisTree("root", SOURCE)
        tree.add_child("g", "root", at(1), allocated_budget=Fraction(1, 4))
        coord.run_tree(SOURCE, tree)

        fresh = BranchingHypothesisTree("root", SOURCE)
        fresh.add_child("g", "root", at(1), allocated_budget=Fraction(1, 4))
        with pytest.raises(RuntimeError, match="one-shot"):
            coord.run_tree(SOURCE, fresh)

    def test_search_failure_after_admission_is_a_consistency_defect(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def no_path(**_: Any) -> SimpleNamespace:
            return SimpleNamespace(path=None, receipt=None)

        monkeypatch.setattr(
            HierarchicalSearchEngine, "search_with_coarse_pruning", staticmethod(no_path)
        )
        coord = coordinator(Fraction(1, 2))
        tree = BranchingHypothesisTree("root", SOURCE)
        tree.add_child("g", "root", at(1), allocated_budget=Fraction(1, 4))

        with pytest.raises(RuntimeError, match="Consistency defect"):
            coord.run_tree(SOURCE, tree)
