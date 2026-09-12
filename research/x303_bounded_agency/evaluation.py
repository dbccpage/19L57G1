"""Counterfactual evaluation of candidate actions. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional

from . import _bootstrap  # noqa: F401
from derivation.iso import CanonKey
from research.x301_formal_semantics.semantics import (
    Formula,
    GroundingFirewall,
    Panel,
    PanelIllusionReceipt,
    RelationalModel,
    evaluate,
)
from .actions import CandidateAction
from .envelope import ViabilityEnvelope
from .keys import canonical_model_digest


@dataclass(frozen=True)
class UtilityVector:
    """Exact rational utility vector in [0, 1] cap Q across (u_margin, u_fuel, u_goal)."""

    u_margin: Fraction = Fraction(0, 1)
    u_fuel: Fraction = Fraction(0, 1)
    u_goal: Fraction = Fraction(0, 1)

    def as_tuple(self) -> tuple[Fraction, Fraction, Fraction]:
        return (self.u_margin, self.u_fuel, self.u_goal)

    def dominates(self, other: UtilityVector) -> bool:
        ge = (
            self.u_margin >= other.u_margin
            and self.u_fuel >= other.u_fuel
            and self.u_goal >= other.u_goal
        )
        gt = (
            self.u_margin > other.u_margin
            or self.u_fuel > other.u_fuel
            or self.u_goal > other.u_goal
        )
        return ge and gt


@dataclass(frozen=True)
class ActionEvaluation:
    """Counterfactual evaluation of a candidate action on an ephemeral branch."""

    action: CandidateAction
    viable: bool
    reason: Optional[str] = None
    projected_state: Optional[RelationalModel] = None
    utility: UtilityVector = field(default_factory=UtilityVector)
    canon_key: Optional[CanonKey] = None
    has_empirical_reference: bool = True
    firewall_refuted: bool = False
    firewall_receipt: Optional[PanelIllusionReceipt] = None

    def __init__(
        self,
        action: CandidateAction,
        viable: bool,
        reason: Optional[str] = None,
        projected_state: Optional[RelationalModel] = None,
        utility: Optional[UtilityVector] = None,
        utilities: Optional[tuple[Fraction, Fraction, Fraction]] = None,
        canon_key: Optional[CanonKey] = None,
        has_empirical_reference: bool = True,
        firewall_refuted: bool = False,
        firewall_receipt: Optional[PanelIllusionReceipt] = None,
    ):
        object.__setattr__(self, "action", action)
        object.__setattr__(self, "viable", viable)
        object.__setattr__(self, "reason", reason)
        object.__setattr__(self, "projected_state", projected_state)
        if utility is not None:
            util_obj = utility
        elif utilities is not None:
            util_obj = UtilityVector(*utilities)
        else:
            util_obj = UtilityVector()
        object.__setattr__(self, "utility", util_obj)
        object.__setattr__(self, "canon_key", canon_key)
        object.__setattr__(self, "has_empirical_reference", has_empirical_reference)
        object.__setattr__(self, "firewall_refuted", firewall_refuted)
        object.__setattr__(self, "firewall_receipt", firewall_receipt)

    @property
    def utilities(self) -> tuple[Fraction, Fraction, Fraction]:
        return self.utility.as_tuple()

    @property
    def u_margin(self) -> Fraction:
        return self.utility.u_margin

    @property
    def u_fuel(self) -> Fraction:
        return self.utility.u_fuel

    @property
    def u_goal(self) -> Fraction:
        return self.utility.u_goal


class CausalEvaluator:
    """Ephemeral counterfactual branch evaluator for candidate actions."""

    def project(self, model: RelationalModel, action: CandidateAction) -> RelationalModel:
        if action.fuel_cost < 0:
            raise ValueError(f"Negative fuel cost: {action.fuel_cost}")
        return action.apply(model)

    def check_empirical_reference(self, model: RelationalModel, action: CandidateAction) -> bool:
        projected = self.project(model, action)
        return canonical_model_digest(projected) != canonical_model_digest(model)

    def evaluate_candidate(
        self,
        model: RelationalModel,
        action: CandidateAction,
        envelope: ViabilityEnvelope,
        fuel_remaining: int,
        total_fuel: int,
        goal_formula: Optional[Formula] = None,
        panel: Optional[Panel] = None,
    ) -> ActionEvaluation:
        if action.fuel_cost > fuel_remaining:
            return ActionEvaluation(
                action=action,
                viable=False,
                reason=f"Action fuel cost {action.fuel_cost} exceeds remaining fuel {fuel_remaining}",
            )

        projected = self.project(model, action)

        is_viable, reason = envelope.check_viability(projected)
        if not is_viable:
            return ActionEvaluation(
                action=action,
                viable=False,
                reason=reason,
                projected_state=projected,
            )

        has_ref = self.check_empirical_reference(model, action)
        u_margin = envelope.compute_margin(projected)
        remaining_after = fuel_remaining - action.fuel_cost
        u_fuel = Fraction(remaining_after, total_fuel) if total_fuel > 0 else Fraction(0, 1)
        if u_fuel < Fraction(0, 1):
            u_fuel = Fraction(0, 1)

        if goal_formula is not None:
            val = evaluate(projected, goal_formula)
            u_goal = val.val
        else:
            u_goal = Fraction(1, 1)

        canon_k = action.get_canon_key(projected)

        firewall_refuted = False
        firewall_receipt: Optional[PanelIllusionReceipt] = None
        if panel is not None and goal_formula is not None:
            fw = GroundingFirewall.evaluate_and_step(
                model=projected,
                formula=goal_formula,
                panel=panel,
                candidate_interventions=(),
            )
            if fw.is_refusal:
                firewall_refuted = True
                rec = fw.receipt
                firewall_receipt = rec if isinstance(rec, PanelIllusionReceipt) else None

        return ActionEvaluation(
            action=action,
            viable=not firewall_refuted,
            reason="Firewall consensus override" if firewall_refuted else None,
            projected_state=projected,
            utility=UtilityVector(u_margin, u_fuel, u_goal),
            canon_key=canon_k,
            has_empirical_reference=has_ref,
            firewall_refuted=firewall_refuted,
            firewall_receipt=firewall_receipt,
        )
