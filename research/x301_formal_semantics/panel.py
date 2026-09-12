"""Multi-observer panel, SHA-256 receipts, and grounding firewall.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from collections.abc import Callable
from typing import Any, Mapping, Optional, Sequence

from formulas import Formula
from intervention import Intervention
from model import RelationalModel, evaluate
from valuation import FALSE, RationalValuation


@dataclass(frozen=True)
class Observer:
    """Independent observer evaluating assertions over a partial projection."""

    observer_id: str
    projection_fn: Callable[[RelationalModel], RelationalModel]
    description: str = ""

    def evaluate(
        self,
        model: RelationalModel,
        formula: Formula,
        assignment: Optional[Mapping[str, Any]] = None,
    ) -> RationalValuation:
        projected_carrier = self.projection_fn(model)
        return evaluate(projected_carrier, formula, assignment)


@dataclass(frozen=True)
class Panel:
    """Panel of N >= 3 independent observers evaluating assertions under partial projections."""

    observers: tuple[Observer, ...]

    def __init__(self, observers: Sequence[Observer]):
        obs_tuple = tuple(observers)
        if len(obs_tuple) < 3:
            raise ValueError(
                f"Panel protocol requires N >= 3 observers, got {len(obs_tuple)}"
            )
        object.__setattr__(self, "observers", obs_tuple)

    def unanimous_consensus(
        self,
        model: RelationalModel,
        formula: Formula,
        assignment: Optional[Mapping[str, Any]] = None,
    ) -> tuple[bool, RationalValuation]:
        """Compute whether all N observers unanimously agree on formula valuation."""
        verdicts = [obs.evaluate(model, formula, assignment) for obs in self.observers]
        first = verdicts[0]
        all_agree = all(v == first for v in verdicts)
        return (all_agree, first if all_agree else FALSE)

    def has_positive_consensus(
        self,
        model: RelationalModel,
        formula: Formula,
        assignment: Optional[Mapping[str, Any]] = None,
    ) -> bool:
        """Check if all observers unanimously certify True."""
        is_agree, val = self.unanimous_consensus(model, formula, assignment)
        return is_agree and val.is_true


@dataclass(frozen=True)
class PanelIllusionReceipt:
    """Immutable, byte-pinned receipt documenting false panel consensus overridden by ground intervention."""

    schema: str = "panel-illusion-v1"
    timestamp: str = ""
    formula_repr: str = ""
    panel_size: int = 0
    observer_ids: tuple[str, ...] = ()
    panel_verdict: bool = True
    refuting_intervention: str = ""
    observable_readout_before: str = ""
    observable_readout_after: str = ""
    ground_truth_verdict: bool = False
    firewall_action: str = "STEP_REFUSAL_STATE_PRESERVED"
    receipt_sha256: str = ""

    def compute_sha256(self) -> str:
        payload = {
            "schema": self.schema,
            "timestamp": self.timestamp,
            "formula_repr": self.formula_repr,
            "panel_size": self.panel_size,
            "observer_ids": list(self.observer_ids),
            "panel_verdict": self.panel_verdict,
            "refuting_intervention": self.refuting_intervention,
            "observable_readout_before": self.observable_readout_before,
            "observable_readout_after": self.observable_readout_after,
            "ground_truth_verdict": self.ground_truth_verdict,
            "firewall_action": self.firewall_action,
        }
        canonical_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(canonical_bytes).hexdigest()

    def verify_checksum(self) -> bool:
        return self.receipt_sha256 == self.compute_sha256()

    @classmethod
    def create(
        cls,
        formula_repr: str,
        panel_size: int,
        observer_ids: Sequence[str],
        refuting_intervention: str,
        observable_readout_before: str,
        observable_readout_after: str,
        panel_verdict: bool = True,
        ground_truth_verdict: bool = False,
        timestamp: Optional[str] = None,
    ) -> PanelIllusionReceipt:
        ts = timestamp or datetime.now(timezone.utc).isoformat()
        unhashed = cls(
            schema="panel-illusion-v1",
            timestamp=ts,
            formula_repr=formula_repr,
            panel_size=panel_size,
            observer_ids=tuple(observer_ids),
            panel_verdict=panel_verdict,
            refuting_intervention=refuting_intervention,
            observable_readout_before=observable_readout_before,
            observable_readout_after=observable_readout_after,
            ground_truth_verdict=ground_truth_verdict,
            firewall_action="STEP_REFUSAL_STATE_PRESERVED",
            receipt_sha256="",
        )
        digest = unhashed.compute_sha256()
        return cls(
            schema=unhashed.schema,
            timestamp=unhashed.timestamp,
            formula_repr=unhashed.formula_repr,
            panel_size=unhashed.panel_size,
            observer_ids=unhashed.observer_ids,
            panel_verdict=unhashed.panel_verdict,
            refuting_intervention=unhashed.refuting_intervention,
            observable_readout_before=unhashed.observable_readout_before,
            observable_readout_after=unhashed.observable_readout_after,
            ground_truth_verdict=unhashed.ground_truth_verdict,
            firewall_action=unhashed.firewall_action,
            receipt_sha256=digest,
        )


@dataclass(frozen=True)
class StepRefusalData:
    """Payload carried by a typed step refusal."""

    retained_state: RelationalModel
    reason: str
    receipt: Optional[PanelIllusionReceipt] = None


class _RefusalDescriptor:
    """Dual-mode descriptor supporting both class constructor and instance attribute access.

    Class access: StepResult.refusal(state, reason, receipt) -> StepResult
    Instance access: result.refusal -> Optional[StepRefusalData]
    """

    def __get__(self, instance: Optional[StepResult], owner: type[StepResult]) -> Any:
        if instance is None:
            # Called on class: StepResult.refusal(...)
            return owner._make_refusal
        # Called on instance: result.refusal
        if instance.is_refusal:
            return StepRefusalData(
                retained_state=instance.state,
                reason=instance.reason or "refusal",
                receipt=instance.receipt,
            )
        return None


@dataclass(frozen=True)
class StepResult:
    """Outcome of a state transition or grounding firewall step.

    Preserves state strictly unmutated on refusal.
    """

    is_success: bool
    is_refusal: bool
    state: RelationalModel
    reason: Optional[str] = None
    receipt: Optional[PanelIllusionReceipt] = None

    refusal = _RefusalDescriptor()

    @classmethod
    def success(cls, state: RelationalModel) -> StepResult:
        return cls(
            is_success=True,
            is_refusal=False,
            state=state,
            reason=None,
            receipt=None,
        )

    @classmethod
    def _make_refusal(
        cls,
        retained_state: RelationalModel,
        reason: str = "Grounding firewall refutation",
        receipt: Optional[PanelIllusionReceipt] = None,
    ) -> StepResult:
        return cls(
            is_success=False,
            is_refusal=True,
            state=retained_state,
            reason=reason,
            receipt=receipt,
        )


class GroundingFirewall:
    """The Grounding Firewall: enforces that empirical ground interventions override panel consensus."""

    @staticmethod
    def evaluate_and_step(
        model: RelationalModel,
        formula: Formula,
        panel: Panel,
        candidate_interventions: Sequence[Intervention],
        assignment: Optional[Mapping[str, Any]] = None,
        proposed_mutation: Optional[RelationalModel] = None,
    ) -> StepResult:
        """Evaluate formula under panel consensus vs ground intervention testing.

        If unanimous panel consensus certifies phi, but ground reality or a counterfactual
        intervention refutes phi:
        - Override committee consensus
        - Emit PanelIllusionReceipt
        - Return typed refusal StepResult.refusal, preserving model strictly unmutated
        """
        env = assignment or {}

        # 1. Evaluate panel unanimous consensus
        panel_certifies = panel.has_positive_consensus(model, formula, env)

        # 2. Evaluate ground truth on actual carrier state
        ground_val_before = evaluate(model, formula, env)

        # 3. Check counterfactual interventions
        refuting_intervention: Optional[Intervention] = None
        readout_after: Optional[RationalValuation] = None

        if panel_certifies and not ground_val_before.is_true:
            # Direct contradiction: panel says True, but carrier state is False
            for interv in candidate_interventions:
                pert = interv.apply(model)
                v_after = evaluate(pert, formula, env)
                if not v_after.is_true:
                    refuting_intervention = interv
                    readout_after = v_after
                    break
            if refuting_intervention is None and candidate_interventions:
                refuting_intervention = candidate_interventions[0]
                readout_after = ground_val_before

        # Also search candidate interventions if panel claims True
        if panel_certifies and refuting_intervention is None:
            for interv in candidate_interventions:
                pert = interv.apply(model)
                v_after = evaluate(pert, formula, env)
                if not v_after.is_true:
                    refuting_intervention = interv
                    readout_after = v_after
                    break

        # 4. Trigger Grounding Firewall if panel consensus is refuted by ground reality / intervention
        if panel_certifies and (refuting_intervention is not None or not ground_val_before.is_true):
            interv_name = refuting_intervention.name if refuting_intervention else "ground_carrier_check"
            after_str = str(readout_after) if readout_after is not None else str(ground_val_before)
            receipt = PanelIllusionReceipt.create(
                formula_repr=repr(formula),
                panel_size=len(panel.observers),
                observer_ids=[obs.observer_id for obs in panel.observers],
                refuting_intervention=interv_name,
                observable_readout_before=str(ground_val_before),
                observable_readout_after=after_str,
                panel_verdict=True,
                ground_truth_verdict=False,
            )
            # FIREWALL OVERRIDE: Refusal preserving original carrier state unmutated
            return StepResult.refusal(
                retained_state=model,
                reason="Grounding firewall override: unanimous panel consensus refuted by ground intervention",
                receipt=receipt,
            )

        # 5. If panel agrees and ground reality validates formula
        if panel_certifies and ground_val_before.is_true:
            next_state = proposed_mutation if proposed_mutation is not None else model
            return StepResult.success(state=next_state)

        # 6. Panel did not reach positive consensus
        return StepResult.refusal(
            retained_state=model,
            reason="Panel did not certify formula",
            receipt=None,
        )


def evaluate_with_grounding_firewall(
    model: RelationalModel,
    formula: Formula,
    panel: Panel,
    candidate_interventions: Sequence[Intervention],
    assignment: Optional[Mapping[str, Any]] = None,
    proposed_mutation: Optional[RelationalModel] = None,
) -> StepResult:
    """Convenience entry point for the Grounding Firewall protocol."""
    return GroundingFirewall.evaluate_and_step(
        model=model,
        formula=formula,
        panel=panel,
        candidate_interventions=candidate_interventions,
        assignment=assignment,
        proposed_mutation=proposed_mutation,
    )
