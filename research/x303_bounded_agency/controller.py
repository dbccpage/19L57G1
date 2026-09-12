"""Bounded agent controller. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Sequence, Union

from . import _bootstrap  # noqa: F401
from research.x301_formal_semantics.semantics import (
    Formula,
    Panel,
    PanelIllusionReceipt,
    RationalValuation,
    RelationalModel,
)
from .actions import CandidateAction
from .envelope import ViabilityEnvelope
from .evaluation import ActionEvaluation, CausalEvaluator, UtilityVector
from .keys import canonical_model_digest
from .licensing import AbilitySet, ActionAuthorizer, LicensedDriver
from .memory import BoundedMemory, MemoryRecord
from .receipts import AgencyReceipt
from .refusal import RefusalReason, UnlicensedActionError
from .selector import MulticriteriaSelector


@dataclass(frozen=True)
class AgentStepResult:
    """Typed result of one operational step. Distinct from x301 StepResult."""

    is_success: bool
    state: RelationalModel
    selected_action: Optional[CandidateAction] = None
    receipt: Optional[Union[AgencyReceipt, PanelIllusionReceipt]] = None
    utility: Optional[UtilityVector] = None
    reason: Optional[str] = None

    @property
    def is_refusal(self) -> bool:
        return not self.is_success

    @classmethod
    def success(
        cls,
        state: RelationalModel,
        selected_action: Optional[CandidateAction] = None,
        receipt: Optional[Union[AgencyReceipt, PanelIllusionReceipt]] = None,
        utility: Optional[UtilityVector] = None,
    ) -> AgentStepResult:
        return cls(
            is_success=True,
            state=state,
            selected_action=selected_action,
            receipt=receipt,
            utility=utility,
            reason=None,
        )

    @classmethod
    def refusal(
        cls,
        retained_state: RelationalModel,
        reason: str,
        receipt: Optional[Union[AgencyReceipt, PanelIllusionReceipt]] = None,
    ) -> AgentStepResult:
        return cls(
            is_success=False,
            state=retained_state,
            selected_action=None,
            receipt=receipt,
            utility=None,
            reason=reason,
        )


class AgentController:
    """Coordinates envelope, fuel, evaluation, authorization, and licensed apply."""

    def __init__(
        self,
        state: RelationalModel,
        envelope: ViabilityEnvelope,
        total_fuel: int,
        memory_horizon: int = 10,
        weights: tuple[Fraction, Fraction, Fraction] = (
            Fraction(1, 3),
            Fraction(1, 3),
            Fraction(1, 3),
        ),
        goal_formula: Optional[Formula] = None,
        timestamp_fixed: Optional[str] = None,
        abilities: Optional[AbilitySet] = None,
        authorizer: Optional[ActionAuthorizer] = None,
    ):
        if total_fuel < 0:
            raise ValueError(f"total_fuel cannot be negative: {total_fuel}")
        is_viable, reason = envelope.check_viability(state)
        if not is_viable:
            raise ValueError(f"Initial state violates viability envelope: {reason}")

        self.state = state
        self.envelope = envelope
        self.fuel = total_fuel
        self.total_fuel = total_fuel
        self.memory = BoundedMemory(horizon=memory_horizon)
        self.weights = weights
        self.goal_formula = goal_formula
        self.step_count = 0
        self.timestamp_fixed = timestamp_fixed
        self.abilities = abilities or AbilitySet()
        self.evaluator = CausalEvaluator()
        self.selector = MulticriteriaSelector(weights=weights)
        self.authorizer = authorizer or ActionAuthorizer()
        self.driver = LicensedDriver()

    def _refuse(
        self,
        current_state: RelationalModel,
        pre_digest: str,
        reason: str,
        receipt_obj: Optional[Union[AgencyReceipt, PanelIllusionReceipt]] = None,
    ) -> AgentStepResult:
        receipt = receipt_obj or AgencyReceipt.create(
            step_index=self.step_count,
            outcome="REFUSAL",
            refusal_reason=reason,
            pre_state_sha256=pre_digest,
            post_state_sha256=pre_digest,
            fuel_before=self.fuel,
            fuel_after=self.fuel,
            timestamp=self.timestamp_fixed,
        )
        return AgentStepResult.refusal(
            retained_state=current_state,
            reason=reason,
            receipt=receipt,
        )

    def step(
        self,
        candidates: Sequence[CandidateAction],
        panel: Optional[Panel] = None,
    ) -> AgentStepResult:
        current_state = self.state
        pre_digest = canonical_model_digest(current_state)

        if self.fuel <= 0:
            return self._refuse(current_state, pre_digest, RefusalReason.FUEL_EXHAUSTED)

        candidate_pool = self.abilities.filter_proposals(list(candidates))
        if not candidate_pool:
            return self._refuse(current_state, pre_digest, RefusalReason.NO_CANDIDATE_ACTIONS)

        evaluations: list[ActionEvaluation] = []
        for cand in candidate_pool:
            evaluations.append(
                self.evaluator.evaluate_candidate(
                    model=current_state,
                    action=cand,
                    envelope=self.envelope,
                    fuel_remaining=self.fuel,
                    total_fuel=self.total_fuel,
                    goal_formula=self.goal_formula,
                    panel=panel,
                )
            )

        viable_evals = [e for e in evaluations if e.viable]
        if not viable_evals:
            firewall_receipt = None
            for e in evaluations:
                if e.firewall_refuted and e.firewall_receipt:
                    firewall_receipt = e.firewall_receipt
                    break
            reason = (
                RefusalReason.FIREWALL_CONSENSUS_OVERRIDE
                if firewall_receipt
                else RefusalReason.VIABILITY_BOUNDARY_EXCEEDED
            )
            return self._refuse(current_state, pre_digest, reason, firewall_receipt)

        selected_eval = self.selector.select(viable_evals)
        if selected_eval is None:
            return self._refuse(current_state, pre_digest, RefusalReason.VIABILITY_BOUNDARY_EXCEEDED)

        selected_action = selected_eval.action
        license = self.authorizer.authorize_evaluation(selected_eval)
        if license is None:
            return self._refuse(current_state, pre_digest, RefusalReason.AUTHORIZATION_DENIED)

        try:
            new_state = self.driver.apply_licensed(
                model=current_state,
                action=selected_action,
                license=license,
            )
        except UnlicensedActionError as exc:
            return self._refuse(current_state, pre_digest, str(exc))

        post_digest = canonical_model_digest(new_state)
        fuel_before = self.fuel
        self.fuel -= selected_action.fuel_cost
        self.state = new_state
        self.memory = self.memory.append(
            MemoryRecord(
                step_index=self.step_count,
                pre_state_digest=pre_digest,
                action_repr=selected_action.name,
                readout=RationalValuation(selected_eval.u_goal),
                post_state_digest=post_digest,
                fuel_cost=selected_action.fuel_cost,
            )
        )
        self.step_count += 1
        receipt = AgencyReceipt.create(
            step_index=self.step_count - 1,
            outcome="SUCCESS",
            action_repr=selected_action.name,
            pre_state_sha256=pre_digest,
            post_state_sha256=post_digest,
            fuel_before=fuel_before,
            fuel_after=self.fuel,
            timestamp=self.timestamp_fixed,
        )
        return AgentStepResult.success(
            state=new_state,
            selected_action=selected_action,
            receipt=receipt,
            utility=selected_eval.utility,
        )
