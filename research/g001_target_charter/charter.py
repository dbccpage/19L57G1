"""Target-Class Charter (G001) for Theory of Everything (TOE) candidate systems.

Pre-registers 9 independent adequacy criteria frozen before candidate evaluation:
1. Computational universality criteria (standard machine simulation, bounded overhead).
2. Reasoning adequacy (proof objects, deduction, refusal vs falsehood).
3. Representational & operational completeness (state, action, memory, observation).
4. Mathematical foundation recovery (constructive arithmetic, number towers, topology).
5. Physical adequacy (embedded observers, relativistic causality, transition valuations).
6. Empirical adequacy (dimensionless ratio recovery, precision calibration, error bounds).
7. Calculus uniqueness (presentation invariance, minimal bases).
8. Physical-model uniqueness (discriminating experiments against rival adequate models).
9. Comparison morphisms (simulation functors, faithful embeddings, distortion metrics).

Status: TOE_TARGET_CLASS_FROZEN upon freezing.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from typing import Any, Mapping


class CharterFreezeError(Exception):
    """Raised when an illegal modification is attempted on a frozen charter."""


class CriterionID(str, Enum):
    """The 9 independent adequacy criteria identifiers."""
    COMPUTATIONAL = "CRIT_01_COMPUTATIONAL"
    REASONING = "CRIT_02_REASONING"
    REPRESENTATIONAL = "CRIT_03_REPRESENTATIONAL"
    FOUNDATIONAL = "CRIT_04_FOUNDATIONAL"
    PHYSICAL = "CRIT_05_PHYSICAL"
    EMPIRICAL = "CRIT_06_EMPIRICAL"
    CALCULUS_UNIQUENESS = "CRIT_07_CALCULUS_UNIQUENESS"
    PHYSICAL_MODEL_UNIQUENESS = "CRIT_08_PHYSICAL_MODEL_UNIQUENESS"
    COMPARISON_MORPHISMS = "CRIT_09_COMPARISON_MORPHISMS"


@dataclass(frozen=True)
class AdequacyCriterion:
    """Specification of a single pre-registered adequacy criterion."""
    criterion_id: CriterionID
    name: str
    dimension: str
    description: str
    required_capabilities: tuple[str, ...]
    falsification_conditions: tuple[str, ...]
    weight: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "criterion_id": self.criterion_id.value,
            "name": self.name,
            "dimension": self.dimension,
            "description": self.description,
            "required_capabilities": list(self.required_capabilities),
            "falsification_conditions": list(self.falsification_conditions),
            "weight": self.weight,
        }


def default_criteria() -> dict[CriterionID, AdequacyCriterion]:
    """Canonical definitions of the 9 independent criteria."""
    return {
        CriterionID.COMPUTATIONAL: AdequacyCriterion(
            criterion_id=CriterionID.COMPUTATIONAL,
            name="Computational Universality Criteria",
            dimension="Computational",
            description="Simulation of standard discrete state transition systems with bounded space and step overhead.",
            required_capabilities=(
                "discrete_state_transition",
                "fuel_or_step_accounting",
                "termination_or_progress_detection",
            ),
            falsification_conditions=(
                "Requires unencoded host oracles to compute transitions",
                "Fails to execute deterministic word programs",
            ),
        ),
        CriterionID.REASONING: AdequacyCriterion(
            criterion_id=CriterionID.REASONING,
            name="Reasoning Adequacy",
            dimension="Reasoning",
            description="Explicit deduction tracking with strict separation between operational refusal and logical falsehood.",
            required_capabilities=(
                "explicit_deduction_steps",
                "refusal_distinct_from_falsehood",
                "witness_tracking",
            ),
            falsification_conditions=(
                "Silent mutation on invalid or refused inputs",
                "Conflation of refusal with contradiction or falsehood",
            ),
        ),
        CriterionID.REPRESENTATIONAL: AdequacyCriterion(
            criterion_id=CriterionID.REPRESENTATIONAL,
            name="Representational and Operational Completeness",
            dimension="Representational",
            description="Operations driven by stored carrier representations without reliance on external event scripts.",
            required_capabilities=(
                "carrier_stored_program",
                "data_driven_enablement",
                "retained_records_or_memory",
                "explicit_branch_on_fork",
            ),
            falsification_conditions=(
                "Interpreter consults unencoded host functions",
                "Runner silently chooses branch targets using list order",
            ),
        ),
        CriterionID.FOUNDATIONAL: AdequacyCriterion(
            criterion_id=CriterionID.FOUNDATIONAL,
            name="Mathematical Foundation Recovery",
            dimension="Mathematical",
            description="Constructive recovery of discrete mathematical substrates without classical shortcuts.",
            required_capabilities=(
                "endogenous_identity_and_ordinals",
                "discrete_order_structures",
                "inverse_limit_compatibility",
            ),
            falsification_conditions=(
                "Unjustified assumption of continuum density or real intervals",
                "Reliance on Classical.choice in core derivations",
            ),
        ),
        CriterionID.PHYSICAL: AdequacyCriterion(
            criterion_id=CriterionID.PHYSICAL,
            name="Physical Adequacy",
            dimension="Physical",
            description="Embedded observers, causal locality, and conserved resource accounting.",
            required_capabilities=(
                "embedded_observer_boundary",
                "causal_locality_independent_loci",
                "monotone_resource_consumption",
            ),
            falsification_conditions=(
                "Superluminal or non-local instantaneous coordinate transport",
                "Creation of fuel or resources by host runtime magic",
            ),
        ),
        CriterionID.EMPIRICAL: AdequacyCriterion(
            criterion_id=CriterionID.EMPIRICAL,
            name="Empirical Adequacy",
            dimension="Empirical",
            description="Finite observational resolution, dimensionless ratio calibration, and quantitative limiting bounds.",
            required_capabilities=(
                "finite_observation_resolution",
                "rational_frequency_readout",
                "effective_error_bounds",
            ),
            falsification_conditions=(
                "Assertion of infinite precision observation in finite time",
                "Absence of verifiable error bounds on limiting readouts",
            ),
        ),
        CriterionID.CALCULUS_UNIQUENESS: AdequacyCriterion(
            criterion_id=CriterionID.CALCULUS_UNIQUENESS,
            name="Calculus Uniqueness",
            dimension="Uniqueness",
            description="Presentation invariance under carrier isomorphism and minimality of admitted primitive bases.",
            required_capabilities=(
                "isomorphism_transport_invariance",
                "minimal_primitive_basis",
                "representation_independence",
            ),
            falsification_conditions=(
                "Behavioral dependence on arbitrary carrier label assignments",
                "Redundant unpriced primitives retained without necessity",
            ),
        ),
        CriterionID.PHYSICAL_MODEL_UNIQUENESS: AdequacyCriterion(
            criterion_id=CriterionID.PHYSICAL_MODEL_UNIQUENESS,
            name="Physical-Model Uniqueness",
            dimension="Uniqueness",
            description="Discriminating prospective experiments breaking observational degeneracy between rival models.",
            required_capabilities=(
                "bisimulation_breakdown_witness",
                "prospective_discriminating_observable",
                "countermodel_separation",
            ),
            falsification_conditions=(
                "Observational indistinguishability between rival target systems",
                "Ad-hoc tuning to accommodate rival empirical predictions",
            ),
        ),
        CriterionID.COMPARISON_MORPHISMS: AdequacyCriterion(
            criterion_id=CriterionID.COMPARISON_MORPHISMS,
            name="Comparison Morphisms",
            dimension="Categorical",
            description="Functorial morphisms between target systems preserving adequacy structures with quantified distortion.",
            required_capabilities=(
                "morphism_identity_and_composition",
                "faithful_observation_preservation",
                "quantified_distortion_metric",
            ),
            falsification_conditions=(
                "Failure of associative morphism composition",
                "Unbounded distortion in simulated state transitions",
            ),
        ),
    }


class TargetClassCharter:
    """TOE Target-Class Charter with strict freezing semantics."""

    FROZEN_STATUS = "TOE_TARGET_CLASS_FROZEN"
    UNFROZEN_STATUS = "UNFROZEN"

    def __init__(self, criteria: Mapping[CriterionID, AdequacyCriterion] | None = None) -> None:
        self._criteria: dict[CriterionID, AdequacyCriterion] = dict(criteria or default_criteria())
        self._status: str = self.UNFROZEN_STATUS
        self._freeze_hash: str | None = None

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_status", None) == self.FROZEN_STATUS:
            raise CharterFreezeError(
                f"Cannot mutate attribute '{name}': charter is frozen (TOE_TARGET_CLASS_FROZEN)."
            )
        super().__setattr__(name, value)

    @property
    def status(self) -> str:
        return self._status

    @property
    def is_frozen(self) -> bool:
        return self._status == self.FROZEN_STATUS

    @property
    def freeze_hash(self) -> str | None:
        return self._freeze_hash

    @property
    def criteria(self) -> dict[CriterionID, AdequacyCriterion]:
        return dict(self._criteria)

    def get_criterion(self, cid: CriterionID) -> AdequacyCriterion:
        if cid not in self._criteria:
            raise KeyError(f"Criterion not found: {cid}")
        return self._criteria[cid]

    def modify_criterion(self, criterion: AdequacyCriterion) -> None:
        if self.is_frozen:
            raise CharterFreezeError("Cannot modify criteria: charter is frozen (TOE_TARGET_CLASS_FROZEN).")
        self._criteria[criterion.criterion_id] = criterion

    def add_criterion(self, criterion: AdequacyCriterion) -> None:
        if self.is_frozen:
            raise CharterFreezeError("Cannot add criteria: charter is frozen (TOE_TARGET_CLASS_FROZEN).")
        self._criteria[criterion.criterion_id] = criterion

    def remove_criterion(self, cid: CriterionID) -> None:
        if self.is_frozen:
            raise CharterFreezeError("Cannot remove criteria: charter is frozen (TOE_TARGET_CLASS_FROZEN).")
        del self._criteria[cid]

    def compute_hash(self) -> str:
        """Deterministic cryptographic fingerprint of the criteria definitions."""
        canonical_items = [
            self._criteria[cid].to_dict()
            for cid in sorted(self._criteria.keys(), key=lambda k: k.value)
        ]
        serialized = json.dumps(canonical_items, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def freeze(self) -> str:
        """Freeze the charter, preventing retrospective target shifting."""
        if len(self._criteria) != 9:
            raise ValueError(f"Charter must have exactly 9 criteria to freeze, found {len(self._criteria)}")
        h = self.compute_hash()
        super().__setattr__("_freeze_hash", h)
        super().__setattr__("_status", self.FROZEN_STATUS)
        return h
