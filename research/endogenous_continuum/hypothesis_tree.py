"""Branching hypothesis trees, a support record, and a tree coordinator.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats in logical decisions.

A child hypothesis is conditional on its parent: it is screened only after its
parent is admitted, and it is retracted when its parent is refused. Retracting a
refused hypothesis therefore retracts the hypotheses that depend on it without
testing their own targets; such a target may still be reachable within its own
budget (see ``tests/test_hypothesis_tree.py``).

A hypothesis is refused when the exact fine-graph distance to its target exceeds
every fund it could draw on at that moment: its own allocation plus the
unallocated pool. The distance comes from one exact search of the fine graph
(``ExactPathSolver.compute_dual_potential``), not from a coarse certificate.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from enum import Enum, auto
from fractions import Fraction
from typing import Any, Callable, Deque, Dict, List, Mapping, Optional, Sequence, Set, Tuple, Union

from .dual_relaxation import ExactPathSolver, _default_cost_fn, _validated_cost
from .hierarchical_search import HierarchicalSearchEngine
from .interval_domain import create_interval_coarsening_map, create_interval_movegraph
from .projective_system import CoarseningMap, MoveEdge, MoveGraph, _to_fraction
from .reasoning_agent import BudgetLedger


def _check_node_id(node_id: Any) -> None:
    if not isinstance(node_id, str) or not node_id:
        raise ValueError(f"Node ids must be non-empty strings, got {node_id!r}")


def _digest(payload: object) -> str:
    """SHA-256 of the canonical JSON form: a deterministic content checksum, not a signature."""
    text = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ============================================================================
# 1. Statements and justifications in the support record
# ============================================================================

class Formula(ABC):
    """A statement held in the support record."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Dictionary form used in checksums.

        Targets are written with ``repr``, so the form is deterministic only for
        targets whose ``repr`` is; the movegraph states of this package are.
        """


@dataclass(frozen=True)
class ReachabilityHypothesis(Formula):
    """Hypothesis: the target is reachable from the source within the budget."""

    node_id: str
    target: Any
    budget: Fraction

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "reachability_hypothesis",
            "node_id": self.node_id,
            "target": repr(self.target),
            "budget": str(self.budget),
        }


@dataclass(frozen=True)
class RefutationWitness(Formula):
    """Exact fine-graph distance exceeding the funds available, or no path at all.

    ``dual_bound`` is ``None`` when the target is a graph state that the source
    cannot reach.
    """

    node_id: str
    target: Any
    dual_bound: Optional[Fraction]
    budget: Fraction

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "refutation_witness",
            "node_id": self.node_id,
            "target": repr(self.target),
            "dual_bound": "unreachable" if self.dual_bound is None else str(self.dual_bound),
            "budget": str(self.budget),
        }


@dataclass(frozen=True)
class Contradiction(Formula):
    """A hypothesis and a refutation of it are both held."""

    node_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "contradiction", "node_id": self.node_id}


class JustificationKind(Enum):
    """How a record entered the support record."""

    HYPOTHESIS_PREMISE = auto()
    DUAL_REFUTATION = auto()
    CONTRADICTION_DETECTION = auto()


@dataclass(frozen=True)
class Justification:
    """Why a record is held: its kind, the rule, and the records it rests on."""

    kind: JustificationKind
    rule_name: str
    antecedents: Tuple[str, ...]


@dataclass(frozen=True)
class SupportNode:
    """A record and the hypotheses it rests on (``support``).

    Records are never mutated: retraction replaces a record with an inactive copy.
    """

    node_id: str
    formula: Formula
    justification: Justification
    support: frozenset[str]
    is_active: bool


@dataclass(frozen=True)
class RetractionReceipt:
    """Deterministic summary of one retraction, with a SHA-256 content checksum.

    The checksum is not an authenticity proof.
    """

    conflict_sets: Tuple[frozenset[str], ...]
    retracted_hypotheses: frozenset[str]
    deactivated_nodes: Tuple[str, ...]
    active_records: Tuple[str, ...]
    justification_hash: str


# ============================================================================
# 2. Branching hypothesis tree
# ============================================================================

@dataclass
class HypothesisTreeNode:
    """A node of the branching hypothesis tree."""

    node_id: str
    parent_id: Optional[str]
    target: Any
    allocated_budget: Fraction
    children: List[str] = field(default_factory=list)
    is_active: bool = True
    description: str = ""

    def __post_init__(self) -> None:
        _check_node_id(self.node_id)
        self.allocated_budget = _to_fraction(self.allocated_budget, "allocated_budget")
        if self.allocated_budget < 0:
            raise ValueError(f"Allocated budget cannot be negative: {self.allocated_budget}")


class BranchingHypothesisTree:
    """Rooted tree of hypotheses; a child is conditional on its parent."""

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
        description: str = "",
    ) -> HypothesisTreeNode:
        """Add a child hypothesis under an existing, active parent."""
        _check_node_id(node_id)
        if node_id in self._nodes:
            raise ValueError(f"Node {node_id!r} already exists in tree")
        if parent_id not in self._nodes:
            raise KeyError(f"Parent node {parent_id!r} not found in tree")
        if not self._nodes[parent_id].is_active:
            raise ValueError(f"Parent node {parent_id!r} has been retracted")

        q_budget = _to_fraction(allocated_budget, "allocated_budget")
        new_node = HypothesisTreeNode(
            node_id=node_id,
            parent_id=parent_id,
            target=target,
            allocated_budget=q_budget,
            description=description,
        )
        self._nodes[node_id] = new_node
        self._nodes[parent_id].children.append(node_id)
        return new_node

    def ancestors(self, node_id: str) -> Tuple[str, ...]:
        """Non-root ancestors of ``node_id``, nearest first."""
        if node_id not in self._nodes:
            raise KeyError(f"Node {node_id!r} not in tree")
        out: List[str] = []
        parent = self._nodes[node_id].parent_id
        while parent is not None and parent != self.root_id:
            out.append(parent)
            parent = self._nodes[parent].parent_id
        return tuple(out)

    def get_subtree_nodes(self, root_id: str) -> List[str]:
        """Every node ID in the subtree rooted at ``root_id``, the root included."""
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
        """Sum of the declared budgets of the active nodes in the subtree."""
        return sum(
            (
                self._nodes[nid].allocated_budget
                for nid in self.get_subtree_nodes(root_id)
                if self._nodes[nid].is_active
            ),
            Fraction(0, 1),
        )

    def prune_subtree(self, target_id: str) -> Tuple[frozenset[str], Fraction]:
        """Deactivate ``target_id`` and its active descendants.

        Returns the deactivated IDs and the sum of their declared budgets. The
        declared budgets are what the tree records; a coordinator's ledger may
        hold different amounts for the same nodes.
        """
        retracted: Set[str] = set()
        declared = Fraction(0, 1)
        for nid in self.get_subtree_nodes(target_id):
            node = self._nodes[nid]
            if node.is_active:
                node.is_active = False
                retracted.add(nid)
                declared += node.allocated_budget
        return frozenset(retracted), declared


# ============================================================================
# 3. Support record
# ============================================================================

class SupportRecord:
    """Hypotheses, refutations and contradictions, each with the hypotheses it rests on.

    Retracting a hypothesis deactivates every active record whose support
    contains it, including the hypotheses that depend on it.
    """

    def __init__(self) -> None:
        self._nodes: Dict[str, SupportNode] = {}
        self._active_hypotheses: Set[str] = set()
        self._active_conflicts: Set[frozenset[str]] = set()
        self._history: List[RetractionReceipt] = []

    @property
    def nodes(self) -> Mapping[str, SupportNode]:
        return self._nodes

    @property
    def active_hypotheses(self) -> frozenset[str]:
        return frozenset(self._active_hypotheses)

    @property
    def active_conflicts(self) -> frozenset[frozenset[str]]:
        return frozenset(self._active_conflicts)

    @property
    def history(self) -> Tuple[RetractionReceipt, ...]:
        return tuple(self._history)

    def _active_record_ids(self) -> Tuple[str, ...]:
        return tuple(sorted(nid for nid, n in self._nodes.items() if n.is_active))

    def register_hypothesis(
        self,
        node_id: str,
        target: Any,
        budget: Fraction,
        depends_on: Sequence[str] = (),
    ) -> str:
        """Hold a reachability hypothesis resting on itself and on ``depends_on``."""
        budget = _to_fraction(budget, "budget")
        tms_id = f"hyp:{node_id}"
        if tms_id in self._nodes:
            raise ValueError(f"Hypothesis {node_id!r} is already registered")
        for dep in depends_on:
            if dep not in self._active_hypotheses:
                raise KeyError(f"Hypothesis {node_id!r} depends on {dep!r}, which is not held")
        self._nodes[tms_id] = SupportNode(
            node_id=tms_id,
            formula=ReachabilityHypothesis(node_id=node_id, target=target, budget=budget),
            justification=Justification(
                kind=JustificationKind.HYPOTHESIS_PREMISE,
                rule_name="TreeHypothesisPremise",
                antecedents=tuple(f"hyp:{dep}" for dep in depends_on),
            ),
            support=frozenset({node_id, *depends_on}),
            is_active=True,
        )
        self._active_hypotheses.add(node_id)
        return tms_id

    def record_refutation(
        self,
        node_id: str,
        target: Any,
        dual_bound: Optional[Fraction],
        budget: Fraction,
    ) -> Tuple[str, str]:
        """Record a refutation of a held hypothesis and the contradiction it creates.

        ``dual_bound`` must exceed ``budget``, or be ``None`` (no path at all).
        """
        budget = _to_fraction(budget, "budget")
        if dual_bound is not None:
            dual_bound = _to_fraction(dual_bound, "dual_bound")
        hyp_id = f"hyp:{node_id}"
        if node_id not in self._active_hypotheses:
            raise KeyError(f"No held hypothesis {node_id!r} to refute")
        if dual_bound is not None and dual_bound <= budget:
            raise ValueError(
                f"Not a refutation: bound {dual_bound} does not exceed budget {budget}"
            )
        ref_id = f"ref:{node_id}"
        self._nodes[ref_id] = SupportNode(
            node_id=ref_id,
            formula=RefutationWitness(
                node_id=node_id, target=target, dual_bound=dual_bound, budget=budget
            ),
            justification=Justification(
                kind=JustificationKind.DUAL_REFUTATION,
                rule_name="ExactDistanceRefutation",
                antecedents=(),
            ),
            support=frozenset(),
            is_active=True,
        )
        contra_id = f"bot:{node_id}"
        self._nodes[contra_id] = SupportNode(
            node_id=contra_id,
            formula=Contradiction(node_id=node_id),
            justification=Justification(
                kind=JustificationKind.CONTRADICTION_DETECTION,
                rule_name="DirectRefutationContradiction",
                antecedents=(hyp_id, ref_id),
            ),
            support=self._nodes[hyp_id].support,
            is_active=True,
        )
        self._active_conflicts.add(frozenset({node_id}))
        return ref_id, contra_id

    def retract(self, node_id: str) -> RetractionReceipt:
        """Retract ``node_id`` and every record that rests on it."""
        if node_id not in self._active_hypotheses:
            active = self._active_record_ids()
            receipt = RetractionReceipt(
                conflict_sets=(),
                retracted_hypotheses=frozenset(),
                deactivated_nodes=(),
                active_records=active,
                justification_hash=_digest({"unchanged": node_id, "active": list(active)}),
            )
            self._history.append(receipt)
            return receipt

        deactivated: List[str] = []
        for nid, node in list(self._nodes.items()):
            if node.is_active and node_id in node.support:
                self._nodes[nid] = dataclasses.replace(node, is_active=False)
                deactivated.append(nid)
        retracted = frozenset(
            h for h in self._active_hypotheses if not self._nodes[f"hyp:{h}"].is_active
        )
        self._active_hypotheses -= retracted

        resolved = tuple(
            sorted((cs for cs in self._active_conflicts if cs & retracted), key=sorted)
        )
        self._active_conflicts.difference_update(resolved)

        witnesses = [
            self._nodes[f"ref:{h}"].formula.to_dict()
            for h in sorted(retracted)
            if f"ref:{h}" in self._nodes
        ]
        active = self._active_record_ids()
        receipt = RetractionReceipt(
            conflict_sets=resolved,
            retracted_hypotheses=retracted,
            deactivated_nodes=tuple(sorted(deactivated)),
            active_records=active,
            justification_hash=_digest(
                {
                    "retracted": node_id,
                    "retracted_hypotheses": sorted(retracted),
                    "deactivated": sorted(deactivated),
                    "resolved_conflicts": [sorted(cs) for cs in resolved],
                    "witnesses": witnesses,
                    "active": list(active),
                }
            ),
        )
        self._history.append(receipt)
        return receipt


# ============================================================================
# 4. Tree coordinator
# ============================================================================

@dataclass(frozen=True)
class TreeReasoningCoordinatorReceipt:
    """Deterministic run summary with SHA-256 content checksums, not an authenticity proof."""

    total_initial_budget: Fraction
    consumed_budget: Fraction
    unallocated_budget: Fraction
    reclaimed_budget: Fraction
    nodes_total: int
    nodes_refused: int
    nodes_retracted: int
    nodes_expanded: int
    nodes_solved: int
    retraction_count: int
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
            "nodes_refused": self.nodes_refused,
            "nodes_retracted": self.nodes_retracted,
            "nodes_expanded": self.nodes_expanded,
            "nodes_solved": self.nodes_solved,
            "retraction_count": self.retraction_count,
            "trace_length": self.trace_length,
            "trace_digest": self.trace_digest,
            "budget_conservation_verified": self.budget_conservation_verified,
        }

    def digest(self) -> str:
        return _digest(self.to_dict())


class AutonomousTreeReasoningCoordinator:
    """One-shot coordinator exploring a branching hypothesis tree under one ledger."""

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
            fine_graph if fine_graph is not None else create_interval_movegraph(scale=fine_scale)
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
        self.support = SupportRecord()
        self.trace: List[Dict[str, Any]] = []
        self._total_reclaimed = Fraction(0, 1)
        self._has_run = False

    def _validate(self, source: Any, tree: BranchingHypothesisTree) -> None:
        """Every check runs before any state changes."""
        if self._has_run:
            raise RuntimeError("AutonomousTreeReasoningCoordinator instances are one-shot")
        if not self.fine_graph.has_state(source):
            raise KeyError(f"Source state {source!r} not in fine graph")
        root = tree.nodes[tree.root_id]
        if root.target != source:
            raise ValueError(f"Source {source!r} is not the tree's root state {root.target!r}")
        if root.allocated_budget != 0:
            raise ValueError("The root holds no hypothesis, so its budget must be 0")
        declared = Fraction(0, 1)
        for nid, node in tree.nodes.items():
            if nid == tree.root_id:
                continue
            if not node.is_active:
                raise ValueError(f"Node {nid!r} is already retracted; run a fresh tree")
            if not self.fine_graph.has_state(node.target):
                raise KeyError(f"Target state {node.target!r} for node {nid!r} not in fine graph")
            declared += node.allocated_budget
        if declared > self.total_budget:
            raise ValueError(
                f"Declared node budgets {declared} exceed the total budget {self.total_budget}"
            )
        morphism = self.coarsening_map.check_morphism(self.fine_graph, self.coarse_graph)
        if not morphism.is_valid:
            detail = "; ".join(morphism.defects)
            raise ValueError(f"Coarsening map failed morphism verification: {detail}")

    def _record(self, action: str, node_id: str, data: Dict[str, Any]) -> None:
        self.trace.append({"action": action, "node": node_id, **data})

    def run_tree(
        self,
        source: Any,
        tree: BranchingHypothesisTree,
    ) -> Tuple[Dict[str, Any], TreeReasoningCoordinatorReceipt]:
        """Screen, expand, search and retract across the tree; mutates ``tree``."""
        self._validate(source, tree)
        self._has_run = True

        # 1. Allocate every declared budget and hold every hypothesis, children
        #    resting on their non-root ancestors.
        for nid, node in tree.nodes.items():
            if nid == tree.root_id:
                continue
            self.ledger.allocate(nid, node.allocated_budget)
            self.support.register_hypothesis(
                node_id=nid,
                target=node.target,
                budget=node.allocated_budget,
                depends_on=tree.ancestors(nid),
            )

        # 2. One exact search of the fine graph from the source.
        fine_potential = ExactPathSolver.compute_dual_potential(
            self.fine_graph, source, cost_fn=self.cost_fn
        )

        # 3. Breadth-first over the tree; a child is screened only after its
        #    parent is admitted.
        queue: Deque[str] = deque(tree.nodes[tree.root_id].children)
        outcomes: Dict[str, Any] = {}
        refused = 0
        retracted_total = 0

        while queue:
            nid = queue.popleft()
            node = tree.nodes[nid]
            if not node.is_active:
                continue

            alloc = self.ledger.allocated_budgets.get(nid, Fraction(0, 1))
            available = alloc + self.ledger.unallocated_budget
            exact_bound = fine_potential.potential_difference(source, node.target)

            if exact_bound is None or exact_bound > available:
                refused += 1
                self.support.record_refutation(
                    node_id=nid, target=node.target, dual_bound=exact_bound, budget=available
                )
                receipt = self.support.retract(nid)
                retracted_ids, _declared = tree.prune_subtree(nid)
                reclaimed = sum(
                    (self.ledger.reclaim(r_id) for r_id in sorted(retracted_ids)),
                    Fraction(0, 1),
                )
                self._total_reclaimed += reclaimed
                retracted_total += len(retracted_ids)
                self._record(
                    "REFUSE_AND_RETRACT",
                    nid,
                    {
                        "exact_bound": "unreachable" if exact_bound is None else str(exact_bound),
                        "available": str(available),
                        "retracted_nodes": sorted(retracted_ids),
                        "reclaimed": str(reclaimed),
                        "justification_hash": receipt.justification_hash,
                    },
                )
                outcomes[nid] = {
                    "status": "CERTIFIED_REFUSED",
                    "exact_bound": exact_bound,
                    "available": available,
                    "retracted_subtree": sorted(retracted_ids),
                    "reclaimed_budget": reclaimed,
                    "retraction_receipt": receipt,
                }
                continue

            if node.children:
                # Admitted without a search of its own: release the allocation so
                # the children can draw on it.
                released = self.ledger.reclaim(nid)
                self._total_reclaimed += released
                queue.extend(node.children)
                self._record(
                    "EXPAND",
                    nid,
                    {"exact_bound": str(exact_bound), "released": str(released)},
                )
                outcomes[nid] = {"status": "EXPANDED", "exact_bound": exact_bound}
                continue

            if exact_bound > alloc:
                drawn = exact_bound - alloc
                self.ledger.allocate(nid, drawn)
                self._record("DRAW", nid, {"drawn": str(drawn)})

            search_res = HierarchicalSearchEngine.search_with_coarse_pruning(
                fine_graph=self.fine_graph,
                coarse_graph=self.coarse_graph,
                coarsening_map=self.coarsening_map,
                source=source,
                target=node.target,
                budget=self.ledger.allocated_budgets[nid],
                cost_fn=self.cost_fn,
            )
            if search_res.path is None:
                raise RuntimeError(
                    f"Consistency defect: exact screening admitted node {nid!r} at bound "
                    f"{exact_bound}, but checked search returned no path"
                )
            actual_cost = sum(
                (_validated_cost(e, self.cost_fn) for e in search_res.path),
                Fraction(0, 1),
            )
            self.ledger.consume(nid, actual_cost)
            remainder = self.ledger.reclaim(nid)
            self._total_reclaimed += remainder
            self._record(
                "SOLVE",
                nid,
                {
                    "cost": str(actual_cost),
                    "path_length": len(search_res.path),
                    "released": str(remainder),
                },
            )
            outcomes[nid] = {
                "status": "SOLVED",
                "cost": actual_cost,
                "path_length": len(search_res.path),
                "receipt": search_res.receipt,
            }

        conservation_ok = self.ledger.audit_conservation()
        if not conservation_ok:
            raise RuntimeError(
                f"Budget conservation violated in tree coordinator: "
                f"total={self.ledger.total_budget}, unallocated={self.ledger.unallocated_budget}, "
                f"allocated={self.ledger.allocated_budgets}, consumed={self.ledger.consumed_budget}"
            )

        receipt_out = TreeReasoningCoordinatorReceipt(
            total_initial_budget=self.total_budget,
            consumed_budget=self.ledger.consumed_budget,
            unallocated_budget=self.ledger.unallocated_budget,
            reclaimed_budget=self._total_reclaimed,
            nodes_total=len(tree.nodes) - 1,
            nodes_refused=refused,
            nodes_retracted=retracted_total,
            nodes_expanded=sum(1 for o in outcomes.values() if o["status"] == "EXPANDED"),
            nodes_solved=sum(1 for o in outcomes.values() if o["status"] == "SOLVED"),
            retraction_count=sum(1 for r in self.support.history if r.retracted_hypotheses),
            trace_length=len(self.trace),
            trace_digest=_digest(self.trace),
            budget_conservation_verified=conservation_ok,
        )
        return outcomes, receipt_out
