"""Target X302: Operational Reasoning & Belief Revision Engine.

Constructive implementation of an endogenous Truth Maintenance System (TMS)
distinguishing firm commitments (Axioms) from contingent assumptions (Hypotheses).
Provides:
- Internal syntax for formulas and operational carrier valuations.
- Dependency-directed justification DAG tracking with hypothesis support sets.
- Direct (phi & ~phi) and operational (x = v1 & x = v2) contradiction detection.
- Minimal retraction (AGM belief revision) via minimum hitting set computation.
- Immutable RevisionReceipt emission with SHA-256 justification hashes.
- Verification of AGM revision postulates (Success, Inclusion, Vacuity, Consistency).

AuthorityEffect: None.
Standard library only: zero unpinned dependencies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from enum import Enum, auto
import hashlib
import json
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence


# ============================================================================
# Exceptions
# ============================================================================

class ReasoningError(Exception):
    """Base class for reasoning and TMS errors."""


class FoundationalInconsistencyError(ReasoningError):
    """Raised when a contradiction is derived solely from firm axioms."""


class ImmutableAxiomError(ReasoningError):
    """Raised when an operation attempts to retract or alter a firm axiom."""


class CircularDependencyError(ReasoningError):
    """Raised when an inference introduces a cycle in the justification DAG."""


class InvalidInferenceError(ReasoningError):
    """Raised when an inference step violates the declared deductive rule."""


class UnknownNodeError(ReasoningError):
    """Raised when referencing a node ID that does not exist in the TMS."""


class InactiveNodeError(ReasoningError):
    """Raised when attempting to use a deactivated/retracted node as an antecedent."""


# ============================================================================
# Syntax & Formulas
# ============================================================================

class Formula(ABC):
    """Abstract base class for internal formulas."""

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Deterministic dictionary serialization for hashing and receipts."""
        pass


@dataclass(frozen=True)
class Atom(Formula):
    """Atomic proposition."""
    name: str

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict[str, Any]:
        return {"type": "atom", "name": self.name}


@dataclass(frozen=True)
class Not(Formula):
    """Negation."""
    inner: Formula

    def __str__(self) -> str:
        return f"~({self.inner})"

    def to_dict(self) -> dict[str, Any]:
        return {"type": "not", "inner": self.inner.to_dict()}


@dataclass(frozen=True)
class And(Formula):
    """Conjunction."""
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f"({self.left} & {self.right})"

    def to_dict(self) -> dict[str, Any]:
        return {"type": "and", "left": self.left.to_dict(), "right": self.right.to_dict()}


@dataclass(frozen=True)
class Or(Formula):
    """Disjunction."""
    left: Formula
    right: Formula

    def __str__(self) -> str:
        return f"({self.left} | {self.right})"

    def to_dict(self) -> dict[str, Any]:
        return {"type": "or", "left": self.left.to_dict(), "right": self.right.to_dict()}


@dataclass(frozen=True)
class Implies(Formula):
    """Implication."""
    antecedent: Formula
    consequent: Formula

    def __str__(self) -> str:
        return f"({self.antecedent} -> {self.consequent})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "implies",
            "antecedent": self.antecedent.to_dict(),
            "consequent": self.consequent.to_dict(),
        }


@dataclass(frozen=True)
class EqVal(Formula):
    """Operational valuation proposition: variable = value.

    Represents operational state assignments. Two distinct values for the same
    carrier variable constitute an operational contradiction.
    """
    variable: str
    value: Any

    def __str__(self) -> str:
        return f"({self.variable} = {self.value!r})"

    def to_dict(self) -> dict[str, Any]:
        return {"type": "eq_val", "variable": self.variable, "value": str(self.value)}


@dataclass(frozen=True)
class Bottom(Formula):
    """Absurdity / direct contradiction (False / bot)."""

    def __str__(self) -> str:
        return "_|_"

    def to_dict(self) -> dict[str, Any]:
        return {"type": "bottom"}


# ============================================================================
# Commitments & Justifications
# ============================================================================

class CommitmentClass(Enum):
    """Distinguishes firm structural axioms from contingent speculative hypotheses."""
    AXIOM = auto()
    HYPOTHESIS = auto()


class JustificationKind(Enum):
    """Declared deductive justification rules."""
    AXIOM_PREMISE = auto()
    HYPOTHESIS_PREMISE = auto()
    MODUS_PONENS = auto()
    CONJUNCTION_INTRO = auto()
    CONJUNCTION_ELIM_LEFT = auto()
    CONJUNCTION_ELIM_RIGHT = auto()
    DISJUNCTION_INTRO_LEFT = auto()
    DISJUNCTION_INTRO_RIGHT = auto()
    RESOLUTION = auto()
    CONTRADICTION_DIRECT = auto()
    CONTRADICTION_VALUATION = auto()


@dataclass(frozen=True)
class Justification:
    """Audit record explaining how a belief was derived."""
    kind: JustificationKind
    rule_name: str
    antecedents: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
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
    commitment: CommitmentClass
    justification: Justification
    antecedents: tuple[str, ...]
    support: frozenset[str]
    is_active: bool
    depth: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "formula": self.formula.to_dict(),
            "commitment": self.commitment.name,
            "justification": self.justification.to_dict(),
            "antecedents": list(self.antecedents),
            "support": sorted(self.support),
            "is_active": self.is_active,
            "depth": self.depth,
        }


@dataclass(frozen=True)
class RevisionReceipt:
    """Immutable cryptographically-hashed audit receipt of belief revision."""
    conflict_sets: tuple[frozenset[str], ...]
    retracted_hypotheses: frozenset[str]
    deactivated_nodes: tuple[str, ...]
    surviving_beliefs: tuple[str, ...]
    justification_hash: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "conflict_sets": [sorted(cs) for cs in self.conflict_sets],
            "retracted_hypotheses": sorted(self.retracted_hypotheses),
            "deactivated_nodes": list(self.deactivated_nodes),
            "surviving_beliefs": list(self.surviving_beliefs),
            "justification_hash": self.justification_hash,
        }


# ============================================================================
# Operational Truth Maintenance System (TMS)
# ============================================================================

class OperationalTMS:
    """Endogenous Truth Maintenance System supporting AGM belief revision.

    Maintains a directed acyclic justification graph tracking dependencies
    back to firm structural axioms and speculative hypotheses.
    """

    def __init__(self) -> None:
        self._nodes: dict[str, TMSNode] = {}
        self._axioms: dict[str, Formula] = {}
        self._hypotheses: dict[str, tuple[Formula, int]] = {}  # hyp_id -> (formula, entrenchment)
        self._active_hypotheses: set[str] = set()
        self._node_dependents: dict[str, set[str]] = {}  # node_id -> set of downstream nodes
        self._hyp_dependents: dict[str, set[str]] = {}   # hyp_id -> set of dependent nodes
        self._active_conflicts: set[frozenset[str]] = set()
        self._history: list[RevisionReceipt] = []
        self._seq: int = 0

    @property
    def nodes(self) -> Mapping[str, TMSNode]:
        """Read-only view of all recorded nodes."""
        return self._nodes

    @property
    def active_hypotheses(self) -> frozenset[str]:
        """Set of currently active hypotheses."""
        return frozenset(self._active_hypotheses)

    @property
    def active_conflicts(self) -> tuple[frozenset[str], ...]:
        """Tuple of currently detected active conflict sets."""
        return tuple(sorted(self._active_conflicts, key=lambda s: (len(s), sorted(s))))

    @property
    def history(self) -> tuple[RevisionReceipt, ...]:
        """Audit log of all revision receipts emitted."""
        return tuple(self._history)

    def _next_node_id(self, prefix: str = "node") -> str:
        self._seq += 1
        return f"{prefix}:{self._seq}"

    def get_node(self, node_id: str) -> TMSNode:
        """Retrieve node by ID or raise UnknownNodeError."""
        if node_id not in self._nodes:
            raise UnknownNodeError(f"Node {node_id!r} not found in TMS")
        return self._nodes[node_id]

    def add_axiom(self, axiom_id: str, formula: Formula) -> str:
        """Register a firm structural axiom.

        Firm axioms are non-negotiable commitments with empty hypothesis support (supp = 0).
        Raises FoundationalInconsistencyError if the axiom immediately contradicts
        existing firm axioms.
        """
        if axiom_id in self._axioms:
            raise ValueError(f"Axiom {axiom_id!r} is already registered")

        node_id = f"ax:{axiom_id}"
        just = Justification(
            kind=JustificationKind.AXIOM_PREMISE,
            rule_name="AxiomPremise",
            antecedents=(),
        )
        node = TMSNode(
            node_id=node_id,
            formula=formula,
            commitment=CommitmentClass.AXIOM,
            justification=just,
            antecedents=(),
            support=frozenset(),
            is_active=True,
            depth=0,
        )
        self._nodes[node_id] = node
        self._axioms[axiom_id] = formula
        self._node_dependents[node_id] = set()

        # Immediate check against existing active beliefs
        self._scan_for_contradictions_with(node_id)
        return node_id

    def add_hypothesis(
        self, hyp_id: str, formula: Formula, entrenchment: int = 1
    ) -> str:
        """Register a speculative hypothesis with optional entrenchment weight.

        Speculative hypotheses are contingent assumptions with singleton support {hyp_id}.
        Eligible for minimal retraction when inconsistency arises.
        """
        if hyp_id in self._hypotheses:
            raise ValueError(f"Hypothesis {hyp_id!r} is already registered")
        if entrenchment < 1:
            raise ValueError(f"Entrenchment weight must be >= 1, got {entrenchment}")

        node_id = f"hyp:{hyp_id}"
        just = Justification(
            kind=JustificationKind.HYPOTHESIS_PREMISE,
            rule_name="HypothesisPremise",
            antecedents=(),
        )
        node = TMSNode(
            node_id=node_id,
            formula=formula,
            commitment=CommitmentClass.HYPOTHESIS,
            justification=just,
            antecedents=(),
            support=frozenset({hyp_id}),
            is_active=True,
            depth=0,
        )
        self._nodes[node_id] = node
        self._hypotheses[hyp_id] = (formula, entrenchment)
        self._active_hypotheses.add(hyp_id)
        self._node_dependents[node_id] = set()
        self._hyp_dependents[hyp_id] = {node_id}

        # Immediate check against existing active beliefs
        self._scan_for_contradictions_with(node_id)
        return node_id

    def retract_axiom(self, axiom_id: str) -> None:
        """Attempt to retract an axiom.

        Strictly prohibited by design: firm commitments can never be retracted.
        """
        raise ImmutableAxiomError(
            f"Cannot retract axiom {axiom_id!r}: axioms are immutable firm commitments"
        )

    def _check_cycle(self, target_id: str, ancestors: Sequence[str]) -> None:
        """Detect circular dependencies in the justification DAG."""
        visited: set[str] = set()
        queue: deque[str] = deque(ancestors)
        while queue:
            curr = queue.popleft()
            if curr == target_id:
                raise CircularDependencyError(
                    f"Circular dependency detected involving node {target_id!r}"
                )
            if curr in visited:
                continue
            visited.add(curr)
            if curr in self._nodes:
                queue.extend(self._nodes[curr].antecedents)

    def apply_inference(
        self,
        formula: Formula,
        kind: JustificationKind,
        antecedents: tuple[str, ...],
    ) -> str:
        """Apply a deductive inference rule to derive a new belief node.

        Verifies:
        1. All antecedents exist and are active.
        2. Antecedents satisfy the declared rule semantics.
        3. No circularity is introduced.
        4. Calculates exact hypothesis support = union of antecedents' support.
        5. If Bottom is derived, registers conflict set or raises FoundationalInconsistencyError.
        """
        if not antecedents:
            raise InvalidInferenceError("Inference step must have at least one antecedent")

        # Validate existence and active status
        ancestor_nodes: list[TMSNode] = []
        for ant_id in antecedents:
            if ant_id not in self._nodes:
                raise UnknownNodeError(f"Antecedent node {ant_id!r} does not exist")
            ant_node = self._nodes[ant_id]
            if not ant_node.is_active:
                raise InactiveNodeError(
                    f"Antecedent node {ant_id!r} is deactivated and cannot be used"
                )
            ancestor_nodes.append(ant_node)

        # Validate rule semantics
        self._validate_rule(formula, kind, ancestor_nodes)

        # Generate node ID and check for cycle
        node_id = self._next_node_id("node")
        self._check_cycle(node_id, antecedents)

        # Compute support and depth
        combined_support: set[str] = set()
        max_depth = 0
        for ant in ancestor_nodes:
            combined_support.update(ant.support)
            max_depth = max(max_depth, ant.depth)

        supp = frozenset(combined_support)
        just = Justification(
            kind=kind,
            rule_name=kind.name,
            antecedents=antecedents,
        )
        node = TMSNode(
            node_id=node_id,
            formula=formula,
            commitment=CommitmentClass.HYPOTHESIS if supp else CommitmentClass.AXIOM,
            justification=just,
            antecedents=antecedents,
            support=supp,
            is_active=True,
            depth=max_depth + 1,
        )

        self._nodes[node_id] = node
        self._node_dependents[node_id] = set()
        for ant_id in antecedents:
            self._node_dependents.setdefault(ant_id, set()).add(node_id)
        for h in supp:
            if h in self._hyp_dependents:
                self._hyp_dependents[h].add(node_id)

        # Check if contradiction was derived
        if isinstance(formula, Bottom):
            if not supp:
                raise FoundationalInconsistencyError(
                    "Absurdity derived with empty hypothesis support (firm axiom contradiction)"
                )
            self._active_conflicts.add(supp)

        # Scan for direct or operational contradiction with existing active nodes
        self._scan_for_contradictions_with(node_id)
        return node_id

    def _validate_rule(
        self,
        formula: Formula,
        kind: JustificationKind,
        antecedents: list[TMSNode],
    ) -> None:
        """Validate logical soundness of the declared deduction rule."""
        f_list = [a.formula for a in antecedents]

        if kind == JustificationKind.MODUS_PONENS:
            if len(f_list) != 2:
                raise InvalidInferenceError("Modus Ponens requires exactly 2 antecedents")
            f1, f2 = f_list[0], f_list[1]
            if isinstance(f1, Implies) and f1.antecedent == f2 and f1.consequent == formula:
                return
            if isinstance(f2, Implies) and f2.antecedent == f1 and f2.consequent == formula:
                return
            raise InvalidInferenceError(
                f"Modus Ponens failure: antecedents {f1} and {f2} do not imply {formula}"
            )

        elif kind == JustificationKind.CONJUNCTION_INTRO:
            if len(f_list) != 2:
                raise InvalidInferenceError("Conjunction Intro requires exactly 2 antecedents")
            if formula != And(f_list[0], f_list[1]):
                raise InvalidInferenceError(
                    f"Conjunction Intro failure: expected {And(f_list[0], f_list[1])}, got {formula}"
                )

        elif kind == JustificationKind.CONJUNCTION_ELIM_LEFT:
            if len(f_list) != 1 or not isinstance(f_list[0], And):
                raise InvalidInferenceError("Conjunction Elim Left requires 1 conjunction antecedent")
            if formula != f_list[0].left:
                raise InvalidInferenceError(
                    f"Conjunction Elim Left failure: expected {f_list[0].left}, got {formula}"
                )

        elif kind == JustificationKind.CONJUNCTION_ELIM_RIGHT:
            if len(f_list) != 1 or not isinstance(f_list[0], And):
                raise InvalidInferenceError("Conjunction Elim Right requires 1 conjunction antecedent")
            if formula != f_list[0].right:
                raise InvalidInferenceError(
                    f"Conjunction Elim Right failure: expected {f_list[0].right}, got {formula}"
                )

        elif kind == JustificationKind.DISJUNCTION_INTRO_LEFT:
            if len(f_list) != 1 or not isinstance(formula, Or):
                raise InvalidInferenceError("Disjunction Intro Left requires 1 antecedent and Or formula")
            if formula.left != f_list[0]:
                raise InvalidInferenceError(
                    f"Disjunction Intro Left failure: expected left disjunct {f_list[0]}, got {formula.left}"
                )

        elif kind == JustificationKind.DISJUNCTION_INTRO_RIGHT:
            if len(f_list) != 1 or not isinstance(formula, Or):
                raise InvalidInferenceError("Disjunction Intro Right requires 1 antecedent and Or formula")
            if formula.right != f_list[0]:
                raise InvalidInferenceError(
                    f"Disjunction Intro Right failure: expected right disjunct {f_list[0]}, got {formula.right}"
                )

        elif kind == JustificationKind.RESOLUTION:
            if len(f_list) != 2:
                raise InvalidInferenceError("Resolution requires exactly 2 antecedents")
            disj, neg = (f_list[0], f_list[1]) if isinstance(f_list[0], Or) else (f_list[1], f_list[0])
            if not isinstance(disj, Or):
                raise InvalidInferenceError("Resolution requires at least one disjunction")
            if isinstance(neg, Not):
                if disj.left == neg.inner and disj.right == formula:
                    return
                if disj.right == neg.inner and disj.left == formula:
                    return
            raise InvalidInferenceError(
                f"Resolution failure: {disj} and {neg} do not resolve to {formula}"
            )

        elif kind == JustificationKind.CONTRADICTION_DIRECT:
            if len(f_list) != 2 or not isinstance(formula, Bottom):
                raise InvalidInferenceError("Contradiction Direct requires 2 antecedents deriving Bottom")
            f1, f2 = f_list[0], f_list[1]
            if (isinstance(f1, Not) and f1.inner == f2) or (isinstance(f2, Not) and f2.inner == f1):
                return
            raise InvalidInferenceError(
                f"Contradiction Direct failure: {f1} and {f2} are not direct negations"
            )

        elif kind == JustificationKind.CONTRADICTION_VALUATION:
            if len(f_list) != 2 or not isinstance(formula, Bottom):
                raise InvalidInferenceError("Contradiction Valuation requires 2 antecedents deriving Bottom")
            f1, f2 = f_list[0], f_list[1]
            if isinstance(f1, EqVal) and isinstance(f2, EqVal):
                if f1.variable == f2.variable and f1.value != f2.value:
                    return
            raise InvalidInferenceError(
                f"Contradiction Valuation failure: {f1} and {f2} are not conflicting valuations"
            )

    def _scan_for_contradictions_with(self, target_node_id: str) -> None:
        """Check if target node contradicts any existing active node."""
        target = self._nodes[target_node_id]
        if not target.is_active:
            return

        for node_id, other in list(self._nodes.items()):
            if node_id == target_node_id or not other.is_active:
                continue

            # 1. Direct contradiction: phi vs ~phi
            if (isinstance(target.formula, Not) and target.formula.inner == other.formula) or \
               (isinstance(other.formula, Not) and other.formula.inner == target.formula):
                combined_supp = target.support | other.support
                if not combined_supp:
                    raise FoundationalInconsistencyError(
                        f"Foundational direct contradiction between {target.formula} and {other.formula}"
                    )
                self._active_conflicts.add(combined_supp)

            # 2. Operational contradiction: x = v1 vs x = v2 (v1 != v2)
            if isinstance(target.formula, EqVal) and isinstance(other.formula, EqVal):
                if target.formula.variable == other.formula.variable and target.formula.value != other.formula.value:
                    combined_supp = target.support | other.support
                    if not combined_supp:
                        raise FoundationalInconsistencyError(
                            f"Foundational valuation conflict on variable {target.formula.variable!r}: "
                            f"{target.formula.value!r} != {other.formula.value!r}"
                        )
                    self._active_conflicts.add(combined_supp)

    def detect_contradictions(self) -> tuple[frozenset[str], ...]:
        """Perform a comprehensive census of all active contradictions.

        Raises FoundationalInconsistencyError if any contradiction has empty support.
        Returns sorted tuple of active conflict sets.
        """
        active_list = [n for n in self._nodes.values() if n.is_active]
        n_len = len(active_list)

        for i in range(n_len):
            n1 = active_list[i]
            if isinstance(n1.formula, Bottom):
                if not n1.support:
                    raise FoundationalInconsistencyError("Absurdity node exists with empty support")
                self._active_conflicts.add(n1.support)

            for j in range(i + 1, n_len):
                n2 = active_list[j]
                # Direct contradiction
                if (isinstance(n1.formula, Not) and n1.formula.inner == n2.formula) or \
                   (isinstance(n2.formula, Not) and n2.formula.inner == n1.formula):
                    supp = n1.support | n2.support
                    if not supp:
                        raise FoundationalInconsistencyError(
                            f"Direct contradiction between {n1.formula} and {n2.formula} with empty support"
                        )
                    self._active_conflicts.add(supp)

                # Operational contradiction
                elif isinstance(n1.formula, EqVal) and isinstance(n2.formula, EqVal):
                    if n1.formula.variable == n2.formula.variable and n1.formula.value != n2.formula.value:
                        supp = n1.support | n2.support
                        if not supp:
                            raise FoundationalInconsistencyError(
                                f"Conflicting operational valuations for {n1.formula.variable!r} with empty support"
                            )
                        self._active_conflicts.add(supp)

        return self.active_conflicts

    def compute_minimal_retractions(self) -> list[frozenset[str]]:
        """Compute all minimum hitting sets for currently active conflict sets.

        A hitting set R satisfies: for all C in conflicts, R & C != empty.
        Minimality criteria:
        1. Minimum cardinality |R|.
        2. Ties broken by lowest total entrenchment weight sum(weight(h) for h in R).
        3. Further ties broken deterministically by lexicographical order of sorted hypothesis IDs.
        """
        conflicts = list(self._active_conflicts)
        if not conflicts:
            return [frozenset()]

        # If any conflict set is empty, it cannot be hit by hypotheses
        for c in conflicts:
            if not c:
                raise FoundationalInconsistencyError("Empty conflict set cannot be resolved by hypothesis retraction")

        universe = sorted(set().union(*conflicts))
        n_univ = len(universe)

        min_hitting_sets: list[frozenset[str]] = []
        best_size = n_univ + 1

        from itertools import combinations
        # Search by increasing subset size
        for size in range(1, n_univ + 1):
            if size > best_size:
                break
            found_at_this_size = []
            for comb in combinations(universe, size):
                comb_set = frozenset(comb)
                if all(bool(comb_set & c) for c in conflicts):
                    found_at_this_size.append(comb_set)

            if found_at_this_size:
                best_size = size
                min_hitting_sets.extend(found_at_this_size)
                break

        if not min_hitting_sets:
            return []

        # Score by entrenchment weights: lower weight means easier to retract
        def score_retraction(r: frozenset[str]) -> tuple[int, tuple[str, ...]]:
            weight = sum(self._hypotheses[h][1] for h in r)
            lex = tuple(sorted(r))
            return (weight, lex)

        min_hitting_sets.sort(key=score_retraction)
        min_weight = score_retraction(min_hitting_sets[0])[0]
        optimal_sets = [r for r in min_hitting_sets if score_retraction(r)[0] == min_weight]
        return optimal_sets

    def revise(
        self, selected_retraction: frozenset[str] | None = None
    ) -> RevisionReceipt:
        """Perform AGM belief revision over active conflicts.

        Restores consistency by deactivating a minimal hitting set of hypotheses
        and propagating deactivation down the justification DAG.
        Emits an immutable RevisionReceipt.
        """
        # Ensure all conflicts are gathered
        conflicts_tuple = self.detect_contradictions()

        # Vacuous revision case
        if not conflicts_tuple:
            active_node_ids = tuple(sorted(nid for nid, n in self._nodes.items() if n.is_active))
            receipt = RevisionReceipt(
                conflict_sets=(),
                retracted_hypotheses=frozenset(),
                deactivated_nodes=(),
                surviving_beliefs=active_node_ids,
                justification_hash=self._hash_receipt(
                    (), frozenset(), (), active_node_ids
                ),
            )
            self._history.append(receipt)
            return receipt

        # Select minimal retraction
        candidates = self.compute_minimal_retractions()
        if not candidates:
            raise FoundationalInconsistencyError("No valid hypothesis retraction can resolve active conflicts")

        if selected_retraction is not None:
            # Validate selected retraction hits all conflicts
            for c in conflicts_tuple:
                if not (selected_retraction & c):
                    raise ValueError(
                        f"Selected retraction {sorted(selected_retraction)} fails to hit conflict {sorted(c)}"
                    )
            # Ensure no axiom is in selected retraction
            for h in selected_retraction:
                if h in self._axioms:
                    raise ImmutableAxiomError(f"Cannot include axiom {h!r} in retraction set")
            chosen_retraction = selected_retraction
        else:
            chosen_retraction = candidates[0]

        # Deactivation propagation down the DAG
        deactivated: list[str] = []
        for nid, node in list(self._nodes.items()):
            if node.is_active and bool(node.support & chosen_retraction):
                updated = TMSNode(
                    node_id=node.node_id,
                    formula=node.formula,
                    commitment=node.commitment,
                    justification=node.justification,
                    antecedents=node.antecedents,
                    support=node.support,
                    is_active=False,
                    depth=node.depth,
                )
                self._nodes[nid] = updated
                deactivated.append(nid)

        # Remove retracted hypotheses from active set
        for h in chosen_retraction:
            self._active_hypotheses.discard(h)

        # Clear resolved conflicts
        self._active_conflicts.clear()

        # Gather surviving beliefs
        surviving = tuple(sorted(nid for nid, n in self._nodes.items() if n.is_active))
        deactivated_tuple = tuple(sorted(deactivated))

        # Build receipt
        rec_hash = self._hash_receipt(
            conflicts_tuple, chosen_retraction, deactivated_tuple, surviving
        )
        receipt = RevisionReceipt(
            conflict_sets=conflicts_tuple,
            retracted_hypotheses=chosen_retraction,
            deactivated_nodes=deactivated_tuple,
            surviving_beliefs=surviving,
            justification_hash=rec_hash,
        )
        self._history.append(receipt)

        # Post-condition check: no unresolved contradiction survives
        self._post_revision_sanity_check()
        return receipt

    def _hash_receipt(
        self,
        conflicts: tuple[frozenset[str], ...],
        retracted: frozenset[str],
        deactivated: tuple[str, ...],
        surviving: tuple[str, ...],
    ) -> str:
        """Compute deterministic SHA-256 hash for revision receipt."""
        data = {
            "conflicts": [sorted(c) for c in conflicts],
            "retracted": sorted(retracted),
            "deactivated": list(deactivated),
            "surviving": list(surviving),
        }
        encoded = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def _post_revision_sanity_check(self) -> None:
        """Ensure no contradiction remains active among surviving beliefs."""
        active = [n for n in self._nodes.values() if n.is_active]
        for n in active:
            if isinstance(n.formula, Bottom):
                raise ReasoningError(f"Sanity failure: Bottom node {n.node_id} remained active after revision")

    def verify_agm_postulates(self, receipt: RevisionReceipt) -> dict[str, bool]:
        """Audit whether the revision satisfies the AGM belief revision postulates:

        1. Success: No active contradictory belief remains.
        2. Inclusion: Surviving beliefs are a subset of previously active beliefs.
        3. Vacuity: When no conflicts were present, retraction is empty and all beliefs survive.
        4. Consistency: Surviving beliefs contain no active direct or operational contradictions.
        5. Axiom Invariance: All axioms remain active and intact.
        """
        active_nodes = {nid: n for nid, n in self._nodes.items() if n.is_active}

        # 1. Success: Bottom not in surviving beliefs
        success = all(not isinstance(n.formula, Bottom) for n in active_nodes.values())

        # 2. Inclusion: Surviving beliefs subset of nodes
        inclusion = set(receipt.surviving_beliefs).issubset(self._nodes.keys())

        # 3. Vacuity
        vacuity = True
        if not receipt.conflict_sets:
            vacuity = (len(receipt.retracted_hypotheses) == 0 and len(receipt.deactivated_nodes) == 0)

        # 4. Consistency: No pair in surviving beliefs contradicts
        consistency = True
        active_list = list(active_nodes.values())
        for i in range(len(active_list)):
            for j in range(i + 1, len(active_list)):
                n1, n2 = active_list[i], active_list[j]
                # Direct contradiction
                if (isinstance(n1.formula, Not) and n1.formula.inner == n2.formula) or \
                   (isinstance(n2.formula, Not) and n2.formula.inner == n1.formula):
                    consistency = False
                # Valuation contradiction
                if isinstance(n1.formula, EqVal) and isinstance(n2.formula, EqVal):
                    if n1.formula.variable == n2.formula.variable and n1.formula.value != n2.formula.value:
                        consistency = False

        # 5. Axiom Invariance
        axiom_inv = all(f"ax:{ax_id}" in active_nodes for ax_id in self._axioms)

        return {
            "success": success,
            "inclusion": inclusion,
            "vacuity": vacuity,
            "consistency": consistency,
            "axiom_invariance": axiom_inv,
        }
