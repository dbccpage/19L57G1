"""Belief Revision Trees and Autonomous Multi-Hypothesis Reasoning.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats in logical decisions.
"""

from __future__ import annotations

import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from fractions import Fraction
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple, Union

from .dual_relaxation import (
    DualPotential,
    DualRefusalReceipt,
    DualityGapReceipt,
    ExactPathSolver,
    _default_cost_fn,
    _validated_cost,
)
from .hierarchical_search import (
    HierarchicalRefusalReceipt,
    HierarchicalSearchEngine,
    HierarchicalSearchResult,
)
from .interval_domain import (
    DyadicInterval,
    create_interval_coarsening_map,
    create_interval_movegraph,
)
from .projective_system import CoarseningMap, MoveEdge, MoveGraph, _to_fraction
from .reasoning_agent import BudgetLedger


# ============================================================================
# 1. Epistemic Formulas & Justifications for Tree TMS
# ============================================================================

class Formula(ABC):
    """Abstract base proposition in the belief revision system."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Deterministic dictionary serialization for hashing and receipts."""
        pass


@dataclass(frozen=True)
class ReachabilityHypothesis(Formula):
    """Speculative hypothesis asserting that target state is reachable within budget."""

    node_id: str
    target: Any
    budget: Fraction

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "reachability_hypothesis",
            "node_id": self.node_id,
            "target": str(self.target),
            "budget": str(self.budget),
        }


@dataclass(frozen=True)
class RefutationWitness(Formula):
    """Certified refutation witness showing exact dual lower bound strictly exceeds budget."""

    node_id: str
    target: Any
    dual_bound: Fraction
    budget: Fraction

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "refutation_witness",
            "node_id": self.node_id,
            "target": str(self.target),
            "dual_bound": str(self.dual_bound),
            "budget": str(self.budget),
        }


@dataclass(frozen=True)
class Contradiction(Formula):
    """Absurdity proposition derived from conflicting reachability and refutation."""

    node_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "contradiction", "node_id": self.node_id}


class JustificationKind(Enum):
    """Declared deductive justification rules for the Tree TMS."""

    HYPOTHESIS_PREMISE = auto()
    DUAL_REFUTATION = auto()
    CONTRADICTION_DETECTION = auto()


@dataclass(frozen=True)
class Justification:
    """Audit record explaining how a belief was derived."""

    kind: JustificationKind
    rule_name: str
    antecedents: Tuple[str, ...]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind.name,
            "rule_name": self.rule_name,
            "antecedents": list(self.antecedents),
        }


@dataclass(frozen=True)
class TMSNode:
    """A node in the Truth Maintenance System justification DAG."""

    node_id: str
    formula: Formula
    justification: Justification
    antecedents: Tuple[str, ...]
    support: frozenset[str]
    is_active: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "formula": self.formula.to_dict(),
            "justification": self.justification.to_dict(),
            "antecedents": list(self.antecedents),
            "support": sorted(self.support),
            "is_active": self.is_active,
        }


@dataclass(frozen=True)
class RevisionReceipt:
    """Immutable cryptographically-hashed audit receipt of belief revision."""

    conflict_sets: Tuple[frozenset[str], ...]
    retracted_hypotheses: frozenset[str]
    deactivated_nodes: Tuple[str, ...]
    surviving_beliefs: Tuple[str, ...]
    justification_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "conflict_sets": [sorted(cs) for cs in self.conflict_sets],
            "retracted_hypotheses": sorted(self.retracted_hypotheses),
            "deactivated_nodes": list(self.deactivated_nodes),
            "surviving_beliefs": list(self.surviving_beliefs),
            "justification_hash": self.justification_hash,
        }


# ============================================================================
# 2. Branching Hypothesis Tree Data Structure
# ============================================================================

@dataclass
class HypothesisTreeNode:
    """A node in the branching hypothesis tree."""

    node_id: str
    parent_id: Optional[str]
    target: Any
    allocated_budget: Fraction
    children: List[str] = field(default_factory=list)
    entrenchment: int = 1
    is_active: bool = True
    description: str = ""

    def __post_init__(self) -> None:
        if self.allocated_budget < 0:
            raise ValueError(f"Allocated budget cannot be negative: {self.allocated_budget}")
        if self.entrenchment < 1:
            raise ValueError(f"Entrenchment must be >= 1, got {self.entrenchment}")


class BranchingHypothesisTree:
    """Rooted tree of conditional hypothesis nodes managing branching exploration."""

    def __init__(self, root_id: str, root_target: Any, root_budget: Union[Fraction, int] = 0) -> None:
        q_root_budget = _to_fraction(root_budget, "root_budget")
        self.root_id = root_id
        self._nodes: Dict[str, HypothesisTreeNode] = {
            root_id: HypothesisTreeNode(
                node_id=root_id,
                parent_id=None,
                target=root_target,
                allocated_budget=q_root_budget,
                description="Root state",
            )
        }

    @property
    def nodes(self) -> Mapping[str, HypothesisTreeNode]:
        return self._nodes

    def add_child(
        self,
        node_id: str,
        parent_id: str,
        target: Any,
        allocated_budget: Union[Fraction, int],
        entrenchment: int = 1,
        description: str = "",
    ) -> HypothesisTreeNode:
        """Add a child hypothesis branching off an existing parent node."""
        if node_id in self._nodes:
            raise ValueError(f"Node {node_id!r} already exists in tree")
        if parent_id not in self._nodes:
            raise KeyError(f"Parent node {parent_id!r} not found in tree")

        q_budget = _to_fraction(allocated_budget, "allocated_budget")
        new_node = HypothesisTreeNode(
            node_id=node_id,
            parent_id=parent_id,
            target=target,
            allocated_budget=q_budget,
            entrenchment=entrenchment,
            description=description,
        )
        self._nodes[node_id] = new_node
        self._nodes[parent_id].children.append(node_id)
        return new_node

    def get_subtree_nodes(self, root_id: str) -> List[str]:
        """Return list of all descendant node IDs in the subtree rooted at root_id (inclusive)."""
        if root_id not in self._nodes:
            raise KeyError(f"Node {root_id!r} not in tree")
        result: List[str] = []
        stack = [root_id]
        while stack:
            curr = stack.pop()
            result.append(curr)
            stack.extend(self._nodes[curr].children)
        return result

    def get_subtree_budget(self, root_id: str) -> Fraction:
        """Sum of all allocated budgets across active nodes in the subtree rooted at root_id."""
        subtree_ids = self.get_subtree_nodes(root_id)
        return sum(
            (self._nodes[nid].allocated_budget for nid in subtree_ids if self._nodes[nid].is_active),
            Fraction(0, 1),
        )

    def prune_subtree(self, target_id: str) -> Tuple[frozenset[str], Fraction]:
        """Deactivate target_id and all its active descendants, returning retracted IDs and reclaimed budget."""
        subtree_ids = self.get_subtree_nodes(target_id)
        retracted: Set[str] = set()
        reclaimed = Fraction(0, 1)

        for nid in subtree_ids:
            node = self._nodes[nid]
            if node.is_active:
                node.is_active = False
                retracted.add(nid)
                reclaimed += node.allocated_budget

        return frozenset(retracted), reclaimed


# ============================================================================
# 3. Tree Truth Maintenance System (TreeTMS)
# ============================================================================

class TreeTMS:
    """Endogenous Truth Maintenance System supporting AGM belief revision over hypothesis trees."""

    def __init__(self) -> None:
        self._nodes: Dict[str, TMSNode] = {}
        self._hypotheses: Dict[str, Tuple[ReachabilityHypothesis, int]] = {}
        self._active_hypotheses: Set[str] = set()
        self._active_conflicts: Set[frozenset[str]] = set()
        self._history: List[RevisionReceipt] = []
        self._seq = 0

    @property
    def active_hypotheses(self) -> frozenset[str]:
        return frozenset(self._active_hypotheses)

    @property
    def history(self) -> Tuple[RevisionReceipt, ...]:
        return tuple(self._history)

    def register_tree_hypothesis(
        self,
        node_id: str,
        target: Any,
        budget: Fraction,
        entrenchment: int = 1,
    ) -> str:
        """Register a speculative reachability hypothesis for a tree node."""
        formula = ReachabilityHypothesis(node_id=node_id, target=target, budget=budget)
        just = Justification(
            kind=JustificationKind.HYPOTHESIS_PREMISE,
            rule_name="TreeHypothesisPremise",
            antecedents=(),
        )
        tms_id = f"hyp:{node_id}"
        node = TMSNode(
            node_id=tms_id,
            formula=formula,
            justification=just,
            antecedents=(),
            support=frozenset({node_id}),
            is_active=True,
        )
        self._nodes[tms_id] = node
        self._hypotheses[node_id] = (formula, entrenchment)
        self._active_hypotheses.add(node_id)
        return tms_id

    def record_dual_refutation(
        self,
        node_id: str,
        target: Any,
        dual_bound: Fraction,
        budget: Fraction,
    ) -> Tuple[str, str]:
        """Record a certified dual lower bound refutation and derive contradiction."""
        refutation_formula = RefutationWitness(
            node_id=node_id,
            target=target,
            dual_bound=dual_bound,
            budget=budget,
        )
        ref_id = f"ref:{node_id}"
        ref_node = TMSNode(
            node_id=ref_id,
            formula=refutation_formula,
            justification=Justification(
                kind=JustificationKind.DUAL_REFUTATION,
                rule_name="DualCertificateRefutation",
                antecedents=(),
            ),
            antecedents=(),
            support=frozenset(),
            is_active=True,
        )
        self._nodes[ref_id] = ref_node

        # Derive contradiction between hyp:node_id and ref:node_id
        hyp_id = f"hyp:{node_id}"
        contra_formula = Contradiction(node_id=node_id)
        contra_id = f"bot:{node_id}"
        contra_node = TMSNode(
            node_id=contra_id,
            formula=contra_formula,
            justification=Justification(
                kind=JustificationKind.CONTRADICTION_DETECTION,
                rule_name="DirectRefutationContradiction",
                antecedents=(hyp_id, ref_id),
            ),
            antecedents=(hyp_id, ref_id),
            support=frozenset({node_id}),
            is_active=True,
        )
        self._nodes[contra_id] = contra_node
        self._active_conflicts.add(frozenset({node_id}))
        return ref_id, contra_id

    def revise(self, target_node_id: str) -> RevisionReceipt:
        """Perform AGM belief revision retracting target_node_id and deactivating its beliefs."""
        if target_node_id not in self._active_hypotheses:
            # Vacuous revision
            receipt = RevisionReceipt(
                conflict_sets=(),
                retracted_hypotheses=frozenset(),
                deactivated_nodes=(),
                surviving_beliefs=tuple(sorted(nid for nid, n in self._nodes.items() if n.is_active)),
                justification_hash=hashlib.sha256(b"vacuous").hexdigest(),
            )
            self._history.append(receipt)
            return receipt

        # Retract hypothesis
        self._active_hypotheses.remove(target_node_id)
        deactivated: List[str] = []

        # Deactivate all nodes supported by target_node_id
        for nid, node in list(self._nodes.items()):
            if node.is_active and target_node_id in node.support:
                object.__setattr__(node, "is_active", False)
                deactivated.append(nid)

        # Remove resolved conflicts
        self._active_conflicts = {
            cs for cs in self._active_conflicts if target_node_id not in cs
        }

        surviving = tuple(sorted(nid for nid, n in self._nodes.items() if n.is_active))
        raw_receipt_json = json.dumps(
            {
                "retracted": target_node_id,
                "deactivated": sorted(deactivated),
                "surviving": list(surviving),
            },
            sort_keys=True,
        )
        just_hash = hashlib.sha256(raw_receipt_json.encode("utf-8")).hexdigest()

        receipt = RevisionReceipt(
            conflict_sets=(frozenset({target_node_id}),),
            retracted_hypotheses=frozenset({target_node_id}),
            deactivated_nodes=tuple(sorted(deactivated)),
            surviving_beliefs=surviving,
            justification_hash=just_hash,
        )
        self._history.append(receipt)
        return receipt


# ============================================================================
# 4. Autonomous Tree Reasoning Coordinator
# ============================================================================

@dataclass(frozen=True)
class TreeReasoningCoordinatorReceipt:
    """Execution receipt for the autonomous multi-hypothesis tree reasoning coordinator."""

    total_initial_budget: Fraction
    consumed_budget: Fraction
    unallocated_budget: Fraction
    reclaimed_budget: Fraction
    nodes_total: int
    nodes_pruned: int
    nodes_solved: int
    revision_count: int
    trace_length: int
    trace_digest: str
    budget_conservation_verified: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_initial_budget": str(self.total_initial_budget),
            "consumed_budget": str(self.consumed_budget),
            "unallocated_budget": str(self.unallocated_budget),
            "reclaimed_budget": str(self.reclaimed_budget),
            "nodes_total": self.nodes_total,
            "nodes_pruned": self.nodes_pruned,
            "nodes_solved": self.nodes_solved,
            "revision_count": self.revision_count,
            "trace_length": self.trace_length,
            "trace_digest": self.trace_digest,
            "budget_conservation_verified": self.budget_conservation_verified,
        }

    def digest(self) -> str:
        canonical_json = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


class AutonomousTreeReasoningCoordinator:
    """Coordinates autonomous exploration of branching hypothesis trees with AGM revision."""

    def __init__(
        self,
        fine_scale: int = 4,
        coarse_scale: int = 2,
        total_budget: Union[Fraction, int] = Fraction(1, 1),
        fine_graph: Optional[MoveGraph] = None,
        coarse_graph: Optional[MoveGraph] = None,
        coarsening_map: Optional[CoarseningMap] = None,
        cost_fn: Callable[[MoveEdge], Fraction] = _default_cost_fn,
    ) -> None:
        self.fine_scale = fine_scale
        self.coarse_scale = coarse_scale
        self.total_budget = _to_fraction(total_budget, "total_budget")
        self.cost_fn = cost_fn

        self.fine_graph = (
            fine_graph
            if fine_graph is not None
            else create_interval_movegraph(scale=fine_scale)
        )
        self.coarse_graph = (
            coarse_graph
            if coarse_graph is not None
            else create_interval_movegraph(scale=coarse_scale)
        )
        self.coarsening_map = (
            coarsening_map
            if coarsening_map is not None
            else create_interval_coarsening_map(coarse_scale, fine_scale)
        )

        self.ledger = BudgetLedger(
            total_budget=self.total_budget,
            unallocated_budget=self.total_budget,
        )
        self.tms = TreeTMS()
        self.trace: List[Dict[str, Any]] = []
        self._total_reclaimed = Fraction(0, 1)
        self._solved_nodes: Set[str] = set()
        self._pruned_nodes: Set[str] = set()

    def run_tree(
        self,
        source: Any,
        tree: BranchingHypothesisTree,
    ) -> Tuple[Dict[str, Any], TreeReasoningCoordinatorReceipt]:
        """Execute autonomous exploration across the branching hypothesis tree."""
        # 1. Allocate initial budgets to all tree nodes
        for nid, node in tree.nodes.items():
            if nid != tree.root_id and node.allocated_budget > 0:
                self.ledger.allocate(nid, node.allocated_budget)
                self.tms.register_tree_hypothesis(
                    node_id=nid,
                    target=node.target,
                    budget=node.allocated_budget,
                    entrenchment=node.entrenchment,
                )

        # 2. Compute exact fine-graph potential from source
        fine_potential = ExactPathSolver.compute_dual_potential(
            self.fine_graph, source, cost_fn=self.cost_fn
        )

        # 3. Explore tree level by level or depth-first
        queue = list(tree.nodes[tree.root_id].children)
        outcomes: Dict[str, Any] = {}

        while queue:
            nid = queue.pop(0)
            node = tree.nodes[nid]
            if not node.is_active:
                continue

            current_alloc = self.ledger.allocated_budgets.get(nid, Fraction(0, 1))
            exact_bound = fine_potential.potential_difference(source, node.target)

            if exact_bound is None or exact_bound > current_alloc:
                # Certified refusal of this hypothesis!
                self._pruned_nodes.add(nid)
                if exact_bound is not None:
                    self.tms.record_dual_refutation(
                        node_id=nid,
                        target=node.target,
                        dual_bound=exact_bound,
                        budget=current_alloc,
                    )

                # AGM belief revision: retract hypothesis and deactivate beliefs
                rev_receipt = self.tms.revise(nid)

                # Prune entire subtree in tree data structure and reclaim 100% budget
                retracted_ids, reclaimed = tree.prune_subtree(nid)
                self._total_reclaimed += reclaimed

                # Reclaim in ledger for all retracted nodes
                for r_id in retracted_ids:
                    if r_id in self.ledger.allocated_budgets:
                        self.ledger.reclaim(r_id)

                self.trace.append({
                    "action": "PRUNE_SUBTREE_AGM_REVISION",
                    "target_node": nid,
                    "retracted_nodes": sorted(retracted_ids),
                    "reclaimed_budget": str(reclaimed),
                    "justification_hash": rev_receipt.justification_hash,
                })

                outcomes[nid] = {
                    "status": "CERTIFIED_REFUSED",
                    "retracted_subtree": sorted(retracted_ids),
                    "reclaimed_budget": reclaimed,
                    "revision_receipt": rev_receipt,
                }

                # Dynamically redistribute reclaimed funds to surviving active queue candidates
                surviving_queue = [q_id for q_id in queue if tree.nodes[q_id].is_active]
                if surviving_queue and self.ledger.unallocated_budget > 0:
                    self.ledger.redistribute_unallocated(surviving_queue)

            else:
                # Hypothesis admitted at this stage
                if not node.children:
                    # Leaf node: execute coarse-guided fine search
                    fine_budget = self.ledger.allocated_budgets.get(nid, current_alloc)
                    search_res = HierarchicalSearchEngine.search_with_coarse_pruning(
                        fine_graph=self.fine_graph,
                        coarse_graph=self.coarse_graph,
                        coarsening_map=self.coarsening_map,
                        source=source,
                        target=node.target,
                        budget=fine_budget,
                        cost_fn=self.cost_fn,
                    )

                    if search_res.path is not None:
                        actual_cost = sum(
                            (_validated_cost(e, self.cost_fn) for e in search_res.path),
                            Fraction(0, 1),
                        )
                        self.ledger.consume(nid, actual_cost)
                        reclaimed_remainder = self.ledger.reclaim(nid)
                        self._total_reclaimed += reclaimed_remainder
                        self._solved_nodes.add(nid)

                        outcomes[nid] = {
                            "status": "SOLVED",
                            "cost": actual_cost,
                            "path_length": len(search_res.path),
                            "receipt": search_res.receipt,
                        }

                        # Redistribute leftover to remaining queue
                        remaining_queue = [q_id for q_id in queue if tree.nodes[q_id].is_active]
                        if remaining_queue and self.ledger.unallocated_budget > 0:
                            self.ledger.redistribute_unallocated(remaining_queue)
                    else:
                        outcomes[nid] = {"status": "BUDGET_EXHAUSTED"}
                else:
                    # Internal node: expand children into queue
                    queue.extend(node.children)

        # 4. Final Conservation Audit
        conservation_ok = self.ledger.audit_conservation()
        if not conservation_ok:
            raise RuntimeError(
                f"Budget conservation violated in tree coordinator: "
                f"total={self.ledger.total_budget}, unallocated={self.ledger.unallocated_budget}, "
                f"allocated={self.ledger.allocated_budgets}, consumed={self.ledger.consumed_budget}"
            )

        raw_trace_json = json.dumps(self.trace, sort_keys=True)
        trace_digest = hashlib.sha256(raw_trace_json.encode("utf-8")).hexdigest()

        receipt = TreeReasoningCoordinatorReceipt(
            total_initial_budget=self.total_budget,
            consumed_budget=self.ledger.consumed_budget,
            unallocated_budget=self.ledger.unallocated_budget,
            reclaimed_budget=self._total_reclaimed,
            nodes_total=len(tree.nodes) - 1,  # exclude root
            nodes_pruned=len(self._pruned_nodes),
            nodes_solved=len(self._solved_nodes),
            revision_count=len(self.tms.history),
            trace_length=len(self.trace),
            trace_digest=trace_digest,
            budget_conservation_verified=conservation_ok,
        )

        return outcomes, receipt
