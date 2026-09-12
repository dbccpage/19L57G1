"""Pipeline configuration and stage result types. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Optional

from . import _bootstrap  # noqa: F401
from research.m114_solver_adapter.solver_adapter import DualReceipt, PrimalReceipt
from research.target_a_execution.control import State as SubstrateState
from research.x301_formal_semantics.semantics import PanelIllusionReceipt, RelationalModel
from research.x302_operational_reasoning.reasoning import RevisionReceipt
from research.x303_bounded_agency.agency import AgencyReceipt
from .receipts import FIXED_TIMESTAMP


@dataclass(frozen=True)
class PipelineConfig:
    fuel_budget: int = 20
    memory_horizon: int = 10
    tolerance_tvd: Fraction = Fraction(0, 1)
    solver_fuel: int = 1000
    panel_size: int = 3
    run_id: str = "X310-RUN-DEFAULT"
    timestamp_fixed: str = FIXED_TIMESTAMP


@dataclass(frozen=True)
class Stage1Result:
    is_refusal: bool
    refusal_reason: Optional[str]
    initial_state: SubstrateState
    final_state: SubstrateState
    carrier_model: RelationalModel
    receipt: dict[str, Any]


@dataclass(frozen=True)
class Stage2Result:
    is_refusal: bool
    refusal_reason: Optional[str]
    observer_projections: dict[str, RelationalModel]
    non_signaling_tvd: Fraction
    gluing_consistent: bool
    receipt: dict[str, Any]
    channel_dpi_verified: bool = True
    channel_fidelity_q: Fraction = Fraction(1, 1)


@dataclass(frozen=True)
class Stage3Result:
    is_refusal: bool
    refusal_reason: Optional[str]
    valuations: dict[str, Fraction]
    firewall_action: str
    illusion_receipt: Optional[PanelIllusionReceipt]
    receipt: dict[str, Any]


@dataclass(frozen=True)
class Stage4Result:
    is_refusal: bool
    refusal_reason: Optional[str]
    status: str
    certificate_type: str
    primal_receipt: Optional[PrimalReceipt]
    dual_receipt: Optional[DualReceipt]
    constraints_checked: int
    receipt: dict[str, Any]


@dataclass(frozen=True)
class Stage5Result:
    is_refusal: bool
    refusal_reason: Optional[str]
    contradictions_detected: int
    retracted_hypotheses: tuple[str, ...]
    agm_postulates_satisfied: dict[str, bool]
    revision_receipt: RevisionReceipt
    receipt: dict[str, Any]


@dataclass(frozen=True)
class Stage6Result:
    is_refusal: bool
    refusal_reason: Optional[str]
    selected_action: Optional[str]
    authorized_license_scope: Optional[str]
    exact_utility_q: Optional[Fraction]
    post_carrier: RelationalModel
    agency_receipt: AgencyReceipt
    receipt: dict[str, Any]


@dataclass(frozen=True)
class PipelineResult:
    is_success: bool
    is_refusal: bool
    refusal_stage: Optional[str]
    refusal_reason: Optional[str]
    initial_carrier: RelationalModel
    final_carrier: RelationalModel
    stage_receipts: dict[str, Any]
    commutation_audit: dict[str, Any]
    grand_receipt: dict[str, Any]
    grand_receipt_sha256: str
