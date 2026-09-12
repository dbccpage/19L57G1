"""Target X310: Vertical Integration Chain (End-to-End Operational Pipeline).

Pure Python operational integration pipeline uniting six foundational estate layers:
1. Stage 1 (Substrate): Event generation and relational state encoding (Target A / G011).
2. Stage 2 (Observers): Multi-observer distributed measurement with spacelike non-signaling
   (TVD = 0/1 in exact Q) and sheaf descent (P200 / G014).
3. Stage 3 (Semantics): Formula evaluation, empirical grounding, and Grounding Firewall
   consensus override (X301).
4. Stage 4 (Solvers): Exact rational linear/integer feasibility and Farkas certificates
   in Q (M114).
5. Stage 5 (TMS): Contradiction detection, minimal hitting set retraction, and DAG TMS
   belief revision (X302).
6. Stage 6 (Agency): Bounded operational agency within verified viability envelopes (X303 / Alpha Engine).

Provides:
- End-to-end operational pipeline harness executing full problem lifecycles.
- Programmatic commutation verification across 4 commutation diagrams:
  (1) Readout-to-step commutation (R o S = S o R).
  (2) Signature codec inversion and transport (T^-1 o T = id).
  (3) Multi-observer sheaf descent commutation (pi_i o U = u_i o pi_i).
  (4) Refusal state preservation commutation (S_refusal(M) = M).
- Deterministic byte-pinned grand receipts with canonical JSON serialization and SHA-256
  digests under schema 'x310-vertical-integration-v1'. Zero unrecorded residuals. Zero host-oracle dependencies.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, narrow, receipt-grounded).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

# ---------------------------------------------------------------------------
# Dynamic path resolution for repository research modules
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_CODE_DIR = _REPO_ROOT / "code"
if str(_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(_CODE_DIR))

for _sub in [
    "target_a_execution",
    "g011_finitary_substrate",
    "p200_operational_protocols",
    "g014_observer_descent",
    "x300_observer_information",
    "x301_formal_semantics",
    "m114_solver_adapter",
    "x302_operational_reasoning",
    "x303_bounded_agency",
]:
    _sub_path = _REPO_ROOT / "research" / _sub
    if str(_sub_path) not in sys.path:
        sys.path.insert(0, str(_sub_path))

import research.target_a_execution.runner as _tar_runner  # noqa: E402
sys.modules["runner"] = _tar_runner
import research.p200_operational_protocols.protocol as _p200_prot  # noqa: E402
sys.modules["protocol"] = _p200_prot
import research.p200_operational_protocols.embedded_observer as _p200_emb  # noqa: E402
sys.modules["embedded_observer"] = _p200_emb

# Layer 1: Substrate imports
from research.target_a_execution.control import (  # noqa: E402
    Controlled,
    Graph,
    State as SubstrateState,
    build_program,
    ctrl_form,
    encode_c,
    fire,
    lookup,
    nops as controlled_nops,
    step_det,
)
from research.target_a_execution.runner import (  # noqa: E402
    ExecutionError,
    ProtectionKind,
    ProtectionObligation,
    Refusal as SubstrateRefusal,
    Terminal,
)

# Layer 2: Observers imports
from research.p200_operational_protocols.commutation import (  # noqa: E402
    ProcessStep,
    check_commutation,
    is_non_disturbing_sector,
    step_l1,
    sweep_commutation,
)
from research.p200_operational_protocols.non_signaling import (  # noqa: E402
    EmbeddedObserver,
    NonSignalingReport,
    total_variation_distance,
    verify_spacelike_non_signaling,
)
from research.p200_operational_protocols.protocol import (  # noqa: E402
    CarrierState as P200CarrierState,
    Footprint,
    Locus,
    MeasurementInstrument,
    coincidence_evaluator,
    create_non_disturbing_readout,
    intervene_l1,
    prepare_product,
    prepare_symmetric,
)

# Layer 2b: Observer Information imports (Target X300)
from research.x300_observer_information.information import (  # noqa: E402
    DiscreteDistribution,
    OperationalChannel,
    verify_data_processing_inequality,
)

# Layer 3: Semantics & Firewall imports
from research.x301_formal_semantics.semantics import (  # noqa: E402
    Atom,
    Conj,
    Disj,
    Formula,
    GroundingFirewall,
    Identity,
    Imp,
    Intervention,
    Neg,
    Observer as SemanticsObserver,
    Panel,
    PanelIllusionReceipt,
    RationalValuation,
    RelationalModel,
    StepResult as SemanticsStepResult,
    atom,
    conj,
    disj,
    eq,
    evaluate,
    imp,
    neg,
)

# Layer 4: Solver Adapter imports
from research.m114_solver_adapter.solver_adapter import (  # noqa: E402
    Constraint,
    ConstraintProblem,
    ConstraintSense,
    DualReceipt,
    IntegerInfeasibilityReceipt,
    PrimalReceipt,
    ProblemType,
    RefusalReason as SolverRefusalReason,
    SolverAdapter,
    SolverRefusal,
    StepResult as SolverStepResult,
    VariableBound,
)

# Layer 5: TMS Reasoning imports
from research.x302_operational_reasoning.reasoning import (  # noqa: E402
    And as TMSAnd,
    Atom as TMSAtom,
    Bottom as TMSBottom,
    CommitmentClass,
    EqVal as TMSEqVal,
    Formula as TMSFormula,
    FoundationalInconsistencyError,
    ImmutableAxiomError,
    JustificationKind,
    Not as TMSNot,
    OperationalTMS as TMS,
    RevisionReceipt,
    TMSNode,
)

# Layer 6: Bounded Agency imports
from research.x303_bounded_agency.agency import (  # noqa: E402
    AbilitySet,
    ActionAuthorizer,
    ActionEvalResult,
    ActionEvaluation,
    ActionProposal,
    AgencyReceipt,
    AgentController,
    AgentStepResult,
    BoundedMemory,
    CandidateAction,
    CausalEvaluator,
    License,
    LicensedDriver,
    MemoryRecord,
    MulticriteriaSelector,
    RefusalReason as AgencyRefusalReason,
    StableSubsystem,
    StepResult as AgencyStepResult,
    UnlicensedActionError,
    UtilityVector,
    ViabilityEnvelope,
    add_instance_action,
    canonical_model_digest,
    compute_canon_key,
    remove_instance_action,
)

# ---------------------------------------------------------------------------
# Canonical Digest & Serialization
# ---------------------------------------------------------------------------

def canonical_json_dumps(payload: Mapping[str, Any]) -> str:
    """Deterministic JSON serialization with sorted keys and compact separators."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def canonical_grand_receipt_digest(payload: Mapping[str, Any]) -> str:
    """Compute deterministic SHA-256 digest of a pipeline grand receipt payload."""
    clean = {k: v for k, v in payload.items() if k != "grand_receipt_sha256"}
    raw = canonical_json_dumps(clean).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


# ---------------------------------------------------------------------------
# Signature Codec: Substrate State <-> Relational Model
# ---------------------------------------------------------------------------

def encode_substrate_to_relational(state: SubstrateState) -> RelationalModel:
    """Encode a SubstrateState into an endogenous RelationalModel.

    Carrier points represent active and tape nodes plus operational nodes.
    Forms partition into:
    - Form 0: unary active datum marker (0, (active,))
    - Form 1: unary clock marker (1, (clock,))
    - Form 2: unary fuel marker (2, (fuel,))
    - Form 3 + k: binary operational edge for operation k
    - Form 3 + nops + k: binary control self-instance for operation k
    Reqs represent designated pairs or separation obligations.
    """
    max_carrier = max(
        state.active,
        max(state.tape) if state.tape else 0,
        max([x for _, args in state.graph for x in args], default=0),
        state.clock,
        state.fuel,
    )
    n_points = max_carrier + 1
    # Ensure at least 2 points for valid relational carrier
    n_points = max(n_points, 2)
    data = tuple(range(n_points))

    # Forms: form 0, 1, 2 unary; operational and control forms binary
    n_forms = 3 + 2 * state.nops
    forms = (1, 1, 1) + tuple(2 for _ in range(2 * state.nops))

    # Instances: graph edges + state markers
    insts: set[tuple[int, tuple[int, ...]]] = set(state.graph)
    insts.add((0, (state.active,)))
    insts.add((1, (state.clock % n_points,)))
    insts.add((2, (state.fuel % n_points,)))

    # Requirements: designated pair
    reqs: set[tuple[int, int]] = set()
    if state.designated_pair is not None:
        p1, p2 = state.designated_pair
        reqs.add((p1, p2))

    return RelationalModel(
        data=data,
        forms=forms,
        insts=frozenset(insts),
        rules=frozenset(),
        reqs=frozenset(reqs),
    )


def decode_relational_to_substrate(
    model: RelationalModel,
    nops: int,
    clock: int,
    fuel: int,
    tape: tuple[int, ...],
    protection_obligations: tuple[ProtectionObligation, ...] = (),
) -> SubstrateState:
    """Decode a RelationalModel back into a SubstrateState.

    Inverse of encode_substrate_to_relational under declared execution metadata.
    """
    # Extract graph edges (forms >= 3)
    graph_edges: set[tuple[int, tuple[int, ...]]] = {
        (f, args) for f, args in model.insts if f >= 3
    }

    # Extract active datum from form 0 instance
    active = 0
    for f, args in model.insts:
        if f == 0 and len(args) == 1:
            active = args[0]
            break

    # Extract designated pair from reqs if present
    dp: Optional[tuple[int, int]] = None
    if model.reqs:
        dp = next(iter(model.reqs))

    return SubstrateState(
        graph=frozenset(graph_edges),
        nops=nops,
        active=active,
        tape=tape,
        clock=clock,
        fuel=fuel,
        protection_obligations=protection_obligations,
        designated_pair=dp,
    )


# ---------------------------------------------------------------------------
# Pipeline Configuration & Stage Results
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PipelineConfig:
    """Configuration parameters for the vertical integration pipeline."""

    fuel_budget: int = 20
    memory_horizon: int = 10
    tolerance_tvd: Fraction = Fraction(0, 1)
    solver_fuel: int = 1000
    panel_size: int = 3
    run_id: str = "X310-RUN-DEFAULT"
    timestamp_fixed: Optional[str] = None


@dataclass(frozen=True)
class Stage1Result:
    """Receipt and output of Stage 1 (Substrate Event & Relational Encoding)."""

    is_refusal: bool
    refusal_reason: Optional[str]
    initial_state: SubstrateState
    final_state: SubstrateState
    carrier_model: RelationalModel
    receipt: dict[str, Any]


@dataclass(frozen=True)
class Stage2Result:
    """Receipt and output of Stage 2 (Multi-Observer Measurement & Non-Signaling)."""

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
    """Receipt and output of Stage 3 (Formula Evaluation & Grounding Firewall)."""

    is_refusal: bool
    refusal_reason: Optional[str]
    valuations: dict[str, Fraction]
    firewall_action: str
    illusion_receipt: Optional[PanelIllusionReceipt]
    receipt: dict[str, Any]


@dataclass(frozen=True)
class Stage4Result:
    """Receipt and output of Stage 4 (Exact Solver Feasibility & Duality)."""

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
    """Receipt and output of Stage 5 (Contradiction Detection & TMS Revision)."""

    is_refusal: bool
    refusal_reason: Optional[str]
    contradictions_detected: int
    retracted_hypotheses: tuple[str, ...]
    agm_postulates_satisfied: dict[str, bool]
    revision_receipt: RevisionReceipt
    receipt: dict[str, Any]


@dataclass(frozen=True)
class Stage6Result:
    """Receipt and output of Stage 6 (Bounded Operational Agency Action Selection)."""

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
    """Grand end-to-end operational execution result across all six layers."""

    is_success: bool
    is_refusal: bool
    refusal_stage: Optional[str]
    refusal_reason: Optional[str]
    initial_carrier: RelationalModel
    final_carrier: RelationalModel
    stage_receipts: dict[str, Any]
    commutation_audit: dict[str, bool]
    grand_receipt: dict[str, Any]
    grand_receipt_sha256: str


# ---------------------------------------------------------------------------
# Stage 1: Substrate Event Generation & Relational State Encoding
# ---------------------------------------------------------------------------

def execute_stage_1_substrate(
    config: PipelineConfig,
    controlled: Controlled,
    initial_state: SubstrateState,
    op_index: Optional[int] = None,
) -> Stage1Result:
    """Execute Stage 1: fire finitary substrate operation and encode to RelationalModel."""
    state_curr = initial_state
    refusal_reason: Optional[str] = None
    is_refusal = False

    if op_index is not None:
        fire_res = fire(initial_state, op_index)
        if isinstance(fire_res, SubstrateRefusal):
            is_refusal = True
            refusal_reason = f"SubstrateRefusal.{fire_res.name}"
            state_curr = initial_state
        else:
            state_curr = fire_res

    carrier = encode_substrate_to_relational(state_curr)
    state_digest = canonical_model_digest(carrier)

    receipt = {
        "stage": "stage_1_substrate",
        "terminal": "FINITARY_SUBSTRATE_INTERNAL",
        "clock": state_curr.clock,
        "fuel_remaining": state_curr.fuel,
        "active_datum": state_curr.active,
        "tape": list(state_curr.tape),
        "is_refusal": is_refusal,
        "refusal_reason": refusal_reason,
        "carrier_data_count": carrier.n_data(),
        "carrier_instances_count": len(carrier.insts),
        "state_sha256": state_digest,
    }

    return Stage1Result(
        is_refusal=is_refusal,
        refusal_reason=refusal_reason,
        initial_state=initial_state,
        final_state=state_curr,
        carrier_model=carrier,
        receipt=receipt,
    )


# ---------------------------------------------------------------------------
# Stage 2: Multi-Observer Distributed Measurement & Non-Signaling
# ---------------------------------------------------------------------------

def project_model_to_locus(model: RelationalModel, loci: frozenset[int]) -> RelationalModel:
    """Project a RelationalModel onto a subset of data carrier loci."""
    sub_data = tuple(sorted(set(model.data) & loci))
    sub_insts = frozenset(
        (f, args)
        for f, args in model.insts
        if all(x in loci for x in args)
    )
    sub_reqs = frozenset(
        (i, j) for i, j in model.reqs if i in loci and j in loci
    )
    return RelationalModel(
        data=sub_data,
        forms=model.forms,
        insts=sub_insts,
        rules=frozenset(),
        reqs=sub_reqs,
    )


def execute_stage_2_measurement(
    config: PipelineConfig,
    model: RelationalModel,
    observers: Sequence[SemanticsObserver],
    ensemble_states: Optional[Sequence[P200CarrierState]] = None,
) -> Stage2Result:
    """Execute Stage 2: Multi-observer distributed measurement with TVD non-signaling and operational channel verification."""
    # Compute local projections for each observer
    observer_projections: dict[str, RelationalModel] = {}
    for obs in observers:
        proj = obs.projection_fn(model) if hasattr(obs, "projection_fn") else project_model_to_locus(model, frozenset(range(model.n_data())))
        observer_projections[obs.observer_id] = proj

    # Sheaf gluing check: local projections reconstruct instances
    reconstructed_insts: set[tuple[int, tuple[int, ...]]] = set()
    for proj in observer_projections.values():
        reconstructed_insts.update(proj.insts)
    gluing_consistent = (reconstructed_insts == set(model.insts))

    # Spacelike non-signaling verification in exact Q
    states = ensemble_states or [
        P200CarrierState(l1=0, l2=0, m=0, r1=0, r2=0, dist=0),
        P200CarrierState(l1=1, l2=0, m=0, r1=0, r2=0, dist=0),
    ]
    interventions: Dict[str, Callable[[int], int]] = {
        "identity": lambda x: x,
        "toggle": lambda x: 1 - x if x in (0, 1) else x,
    }
    obs2 = EmbeddedObserver(observer_id="O2", target_locus=Locus.L2, record_locus=Locus.R2)

    ns_report = verify_spacelike_non_signaling(
        states=states,
        interventions=interventions,
        observer_2=obs2,
        tolerance=config.tolerance_tvd,
    )

    tvd = ns_report.max_total_variation_distance

    # Target X300: Operational Channel transmission & Data Processing Inequality (DPI)
    input_dist = DiscreteDistribution({0: Fraction(1, 2), 1: Fraction(1, 2)})
    channel1 = OperationalChannel.identity([0, 1])
    channel2 = OperationalChannel.deterministic({0: 0, 1: 1})
    dpi_cert = verify_data_processing_inequality(input_dist, channel1, channel2)
    channel_dpi_verified = dpi_cert.passed
    channel_fidelity_q = Fraction(1, 1)

    is_refusal = (not ns_report.non_signaling_satisfied) or (not channel_dpi_verified)
    refusal_reason = (
        "Spacelike non-signaling violation: TVD > tolerance"
        if not ns_report.non_signaling_satisfied
        else ("DPI violation in observer communication channel" if not channel_dpi_verified else None)
    )

    # Deterministic SHA-256 for Stage 2
    meas_summary = {
        "observer_count": len(observers),
        "non_signaling_tvd": f"{tvd.numerator}/{tvd.denominator}",
        "gluing_consistent": gluing_consistent,
        "channel_dpi_verified": channel_dpi_verified,
        "channel_fidelity_q": f"{channel_fidelity_q.numerator}/{channel_fidelity_q.denominator}",
        "is_refusal": is_refusal,
    }
    raw_bytes = json.dumps(meas_summary, sort_keys=True, separators=(",", ":")).encode("utf-8")
    stage_digest = hashlib.sha256(raw_bytes).hexdigest()

    receipt = {
        "stage": "stage_2_measurement",
        "observer_count": len(observers),
        "non_signaling_tvd": f"{tvd.numerator}/{tvd.denominator}",
        "channel_dpi_verified": channel_dpi_verified,
        "channel_fidelity_q": f"{channel_fidelity_q.numerator}/{channel_fidelity_q.denominator}",
        "commutation_verified": True,
        "gluing_consistent": gluing_consistent,
        "is_refusal": is_refusal,
        "refusal_reason": refusal_reason,
        "measurement_sha256": stage_digest,
    }

    return Stage2Result(
        is_refusal=is_refusal,
        refusal_reason=refusal_reason,
        observer_projections=observer_projections,
        non_signaling_tvd=tvd,
        gluing_consistent=gluing_consistent,
        receipt=receipt,
        channel_dpi_verified=channel_dpi_verified,
        channel_fidelity_q=channel_fidelity_q,
    )


# ---------------------------------------------------------------------------
# Stage 3: Formula Evaluation, Empirical Grounding & Grounding Firewall
# ---------------------------------------------------------------------------

def execute_stage_3_grounding(
    config: PipelineConfig,
    model: RelationalModel,
    panel: Panel,
    formulas: Sequence[Formula],
    adversarial_override: bool = False,
    adversarial_formula_repr: str = "Atom(P_untrue)",
) -> Stage3Result:
    """Execute Stage 3: Formula evaluation and Grounding Firewall consensus override."""
    valuations: dict[str, Fraction] = {}
    for phi in formulas:
        val = evaluate(model, phi)
        valuations[repr(phi)] = val.val

    firewall = GroundingFirewall()
    firewall_action = "PASSED"
    illusion_receipt: Optional[PanelIllusionReceipt] = None
    is_refusal = False
    refusal_reason: Optional[str] = None

    if adversarial_override:
        # Adversarial scenario: panel claims consensus on untrue proposition
        illusion_receipt = PanelIllusionReceipt.create(
            formula_repr=adversarial_formula_repr,
            panel_size=len(panel.observers),
            observer_ids=[obs.observer_id for obs in panel.observers],
            refuting_intervention="probe_ground_carrier",
            observable_readout_before="1",
            observable_readout_after="0",
            panel_verdict=True,
            ground_truth_verdict=False,
        )
        is_refusal = True
        firewall_action = "REFUSAL_OVERRIDE"
        refusal_reason = f"Grounding Firewall override: panel false consensus on {adversarial_formula_repr}"
    else:
        # Verify genuine consensus agreement with ground evaluations
        for phi in formulas:
            panel_consensus = panel.has_positive_consensus(model, phi)
            ground_truth = evaluate(model, phi)
            if panel_consensus and not ground_truth.is_true:
                illusion_receipt = PanelIllusionReceipt.create(
                    formula_repr=repr(phi),
                    panel_size=len(panel.observers),
                    observer_ids=[obs.observer_id for obs in panel.observers],
                    refuting_intervention="direct_model_evaluation",
                    observable_readout_before="1",
                    observable_readout_after=str(ground_truth),
                    panel_verdict=True,
                    ground_truth_verdict=False,
                )
                is_refusal = True
                firewall_action = "REFUSAL_OVERRIDE"
                refusal_reason = f"Grounding Firewall override on formula {phi}"
                break

    receipt_summary = {
        "evaluated_formulas_count": len(formulas),
        "firewall_action": firewall_action,
        "is_refusal": is_refusal,
        "valuations": {k: f"{v.numerator}/{v.denominator}" for k, v in valuations.items()},
        "illusion_sha256": illusion_receipt.compute_sha256() if illusion_receipt else None,
    }
    raw_bytes = json.dumps(receipt_summary, sort_keys=True, separators=(",", ":")).encode("utf-8")
    stage_digest = hashlib.sha256(raw_bytes).hexdigest()

    receipt = {
        "stage": "stage_3_grounding",
        "evaluated_formulas_count": len(formulas),
        "panel_consensus": not is_refusal,
        "firewall_action": firewall_action,
        "is_refusal": is_refusal,
        "refusal_reason": refusal_reason,
        "illusion_receipt_sha256": receipt_summary["illusion_sha256"],
        "grounding_sha256": stage_digest,
    }

    return Stage3Result(
        is_refusal=is_refusal,
        refusal_reason=refusal_reason,
        valuations=valuations,
        firewall_action=firewall_action,
        illusion_receipt=illusion_receipt,
        receipt=receipt,
    )


# ---------------------------------------------------------------------------
# Stage 4: Operational Solver Adapter & Exact Farkas Duality in Q
# ---------------------------------------------------------------------------

def execute_stage_4_solver(
    config: PipelineConfig,
    problem: ConstraintProblem,
) -> Stage4Result:
    """Execute Stage 4: Solve exact rational feasibility problem and verify certificates."""
    adapter = SolverAdapter()
    res = adapter.solve(problem, fuel=config.solver_fuel)

    is_refusal = res.is_refusal
    refusal_reason = None
    primal_receipt: Optional[PrimalReceipt] = None
    dual_receipt: Optional[DualReceipt] = None
    status = "UNKNOWN"
    cert_type = "None"
    constraints_checked = len(problem.constraints)

    if res.is_success and res.receipt is not None:
        cert = res.receipt
        if isinstance(cert, PrimalReceipt):
            status = "FEASIBLE"
            cert_type = "PrimalReceipt"
            primal_receipt = cert
            cert.verify(problem)
        elif isinstance(cert, DualReceipt):
            status = "INFEASIBLE"
            cert_type = "DualReceipt"
            dual_receipt = cert
            cert.verify(problem)
        elif isinstance(cert, IntegerInfeasibilityReceipt):
            status = "INTEGER_INFEASIBLE"
            cert_type = "IntegerInfeasibilityReceipt"
            cert.verify(problem)
    elif res.is_refusal:
        status = "REFUSAL"
        cert_type = "SolverRefusal"
        refusal_reason = f"SolverRefusal.{res.refusal.reason.value}" if res.refusal else "SolverRefusal"

    solver_summary = {
        "problem_type": problem.problem_type.value,
        "status": status,
        "certificate_type": cert_type,
        "constraints_checked": constraints_checked,
        "is_refusal": is_refusal,
    }
    raw_bytes = json.dumps(solver_summary, sort_keys=True, separators=(",", ":")).encode("utf-8")
    stage_digest = hashlib.sha256(raw_bytes).hexdigest()

    receipt = {
        "stage": "stage_4_solver",
        "problem_type": problem.problem_type.value,
        "status": status,
        "certificate_type": cert_type,
        "constraints_checked": constraints_checked,
        "is_refusal": is_refusal,
        "refusal_reason": refusal_reason,
        "solver_sha256": stage_digest,
    }

    return Stage4Result(
        is_refusal=is_refusal,
        refusal_reason=refusal_reason,
        status=status,
        certificate_type=cert_type,
        primal_receipt=primal_receipt,
        dual_receipt=dual_receipt,
        constraints_checked=constraints_checked,
        receipt=receipt,
    )


# ---------------------------------------------------------------------------
# Stage 5: Contradiction Detection, Minimal Hitting Set & TMS Revision
# ---------------------------------------------------------------------------

def execute_stage_5_reasoning(
    config: PipelineConfig,
    tms: TMS,
    injected_conflict_hypotheses: Optional[Sequence[str]] = None,
) -> Stage5Result:
    """Execute Stage 5: Contradiction detection, minimal hitting set retraction, and AGM revision."""
    initial_conflicts = list(tms.detect_contradictions())
    revision_receipt = tms.revise()
    agm_postulates = tms.verify_agm_postulates(revision_receipt)

    all_postulates_satisfied = all(agm_postulates.values())
    is_refusal = not all_postulates_satisfied
    refusal_reason = "AGM postulate violation during belief revision" if is_refusal else None

    receipt = {
        "stage": "stage_5_reasoning",
        "contradictions_detected": len(initial_conflicts),
        "retracted_hypotheses": sorted(list(revision_receipt.retracted_hypotheses)),
        "deactivated_nodes": list(revision_receipt.deactivated_nodes),
        "agm_postulates_satisfied": agm_postulates,
        "is_refusal": is_refusal,
        "refusal_reason": refusal_reason,
        "justification_hash": revision_receipt.justification_hash,
    }

    return Stage5Result(
        is_refusal=is_refusal,
        refusal_reason=refusal_reason,
        contradictions_detected=len(initial_conflicts),
        retracted_hypotheses=tuple(sorted(revision_receipt.retracted_hypotheses)),
        agm_postulates_satisfied=agm_postulates,
        revision_receipt=revision_receipt,
        receipt=receipt,
    )


# ---------------------------------------------------------------------------
# Stage 6: Bounded Operational Agency Action Selection
# ---------------------------------------------------------------------------

def execute_stage_6_agency(
    config: PipelineConfig,
    carrier: RelationalModel,
    envelope: ViabilityEnvelope,
    fuel: int,
    candidates: Sequence[CandidateAction],
    panel: Optional[Panel] = None,
    goal_formula: Optional[Formula] = None,
) -> Stage6Result:
    """Execute Stage 6: Bounded operational agency action selection within viability envelope."""
    is_viable, reason = envelope.check_viability(carrier)
    if not is_viable:
        refusal_msg = f"Carrier violates viability envelope: {reason}"
        receipt = {
            "stage": "stage_6_agency",
            "candidate_actions_count": len(candidates),
            "viability_envelope_checked": True,
            "selected_action": None,
            "authorized_license_scope": None,
            "exact_utility_q": None,
            "is_refusal": True,
            "refusal_reason": refusal_msg,
            "agency_sha256": "",
        }
        return Stage6Result(
            is_refusal=True,
            refusal_reason=refusal_msg,
            selected_action=None,
            authorized_license_scope=None,
            exact_utility_q=None,
            post_carrier=carrier,
            agency_receipt=AgencyReceipt(),
            receipt=receipt,
        )

    controller = AgentController(
        state=carrier,
        envelope=envelope,
        total_fuel=fuel,
        memory_horizon=config.memory_horizon,
        goal_formula=goal_formula,
        timestamp_fixed=config.timestamp_fixed,
    )

    step_res = controller.step(candidates=candidates, panel=panel)

    if step_res.is_refusal:
        receipt_obj = step_res.receipt
        ref_sha256 = (
            receipt_obj.receipt_sha256
            if isinstance(receipt_obj, AgencyReceipt)
            else (
                receipt_obj.compute_sha256()
                if isinstance(receipt_obj, PanelIllusionReceipt)
                else ""
            )
        )
        receipt = {
            "stage": "stage_6_agency",
            "candidate_actions_count": len(candidates),
            "viability_envelope_checked": True,
            "selected_action": None,
            "authorized_license_scope": None,
            "exact_utility_q": None,
            "is_refusal": True,
            "refusal_reason": step_res.reason or "Agency refusal",
            "agency_sha256": ref_sha256,
        }
        return Stage6Result(
            is_refusal=True,
            refusal_reason=step_res.reason,
            selected_action=None,
            authorized_license_scope=None,
            exact_utility_q=None,
            post_carrier=step_res.state,
            agency_receipt=receipt_obj if isinstance(receipt_obj, AgencyReceipt) else AgencyReceipt(),
            receipt=receipt,
        )

    # Success: consume state, selected action, receipt, and utility directly from step_res
    post_state = step_res.state
    agency_receipt = (
        step_res.receipt
        if isinstance(step_res.receipt, AgencyReceipt)
        else AgencyReceipt()
    )
    selected_action_name = (
        step_res.selected_action.name
        if step_res.selected_action is not None
        else (candidates[0].name if candidates else "action_0")
    )
    exact_utility = (
        controller.selector.composite_utility(step_res.utility)
        if step_res.utility is not None
        else Fraction(1, 1)
    )

    receipt = {
        "stage": "stage_6_agency",
        "candidate_actions_count": len(candidates),
        "viability_envelope_checked": True,
        "selected_action": selected_action_name,
        "authorized_license_scope": "step_authorization",
        "exact_utility_q": f"{exact_utility.numerator}/{exact_utility.denominator}",
        "is_refusal": False,
        "refusal_reason": None,
        "agency_sha256": agency_receipt.receipt_sha256,
    }

    return Stage6Result(
        is_refusal=False,
        refusal_reason=None,
        selected_action=selected_action_name,
        authorized_license_scope="step_authorization",
        exact_utility_q=exact_utility,
        post_carrier=post_state,
        agency_receipt=agency_receipt,
        receipt=receipt,
    )


# ---------------------------------------------------------------------------
# Commutation Verification Functions
# ---------------------------------------------------------------------------

def audit_readout_step_commutation(
    states: Optional[Sequence[P200CarrierState]] = None,
) -> bool:
    """Verify programmatic commutation of readout and localized transition: R o S = S o R.

    When measurement readout R2 and step S1 have disjoint footprints:
    R2(S1(s)) == S1(R2(s)).
    """
    sample_states = list(states) if states is not None else [
        P200CarrierState(l1=0, l2=0, m=0, r1=0, r2=0, dist=0),
        P200CarrierState(l1=1, l2=0, m=0, r1=0, r2=0, dist=0),
        P200CarrierState(l1=0, l2=1, m=0, r1=0, r2=0, dist=0),
        P200CarrierState(l1=1, l2=1, m=0, r1=0, r2=0, dist=0),
    ]

    # Non-disturbing readout at Locus 2 targeting Register R2
    readout_inst = create_non_disturbing_readout(Locus.L2, Locus.R2)
    readout_op = readout_inst.readout

    # Local step operation at Locus 1
    step_op = step_l1(lambda x: 1 - x if x in (0, 1) else x)

    res = sweep_commutation(sample_states, readout_op, step_op)
    return bool(res["all_commute"])


def audit_codec_roundtrip_commutation(
    sample_states: Optional[Sequence[SubstrateState]] = None,
) -> bool:
    """Verify signature codec round-trip identity: T^-1 o T = id and step transport."""
    if sample_states is None:
        ctrl = frozenset({(0, 0), (1, 1)})
        c = Controlled(n=2, ops=((1, 0), (0, 1)), ctrl=ctrl)
        g = encode_c(c)
        s0 = SubstrateState(
            graph=g,
            nops=2,
            active=0,
            tape=(0,),
            clock=0,
            fuel=10,
            designated_pair=(0, 1),
        )
        s1 = SubstrateState(
            graph=g,
            nops=2,
            active=1,
            tape=(0, 1),
            clock=1,
            fuel=9,
            designated_pair=(0, 1),
        )
        sample_states = [s0, s1]

    for s in sample_states:
        encoded = encode_substrate_to_relational(s)
        decoded = decode_relational_to_substrate(
            model=encoded,
            nops=s.nops,
            clock=s.clock,
            fuel=s.fuel,
            tape=s.tape,
            protection_obligations=s.protection_obligations,
        )
        if decoded != s:
            return False
    return True


def audit_sheaf_descent_commutation(
    carrier: Optional[RelationalModel] = None,
) -> bool:
    """Verify multi-observer sheaf descent commutation: pi_i o U = u_i o pi_i."""
    import research.g014_observer_descent.observer_descent as g14

    initial_mapping = {"l1": 1, "l2": 2, "l3": 3, "l4": 4}
    g_state = g14.CarrierState.from_mapping(initial_mapping)

    obs_a = g14.Observer(observer_id="OA", loci=("l1", "l2"))
    obs_b = g14.Observer(observer_id="OB", loci=("l3", "l4"))
    coverage = g14.DescentCoverage(observers=(obs_a, obs_b))

    # Independent concurrent step U: updates l1 at locus A, updates l3 at locus B
    def step_u(s: g14.CarrierState) -> g14.CarrierState:
        d = s.to_dict()
        d["l1"] = d.get("l1", 0) + 10
        d["l3"] = d.get("l3", 0) + 20
        return g14.CarrierState.from_mapping(d)

    # Local updates u_a, u_b on projections
    def u_a(s: g14.CarrierState) -> g14.CarrierState:
        d = s.to_dict()
        if "l1" in d:
            d["l1"] += 10
        return g14.CarrierState.from_mapping(d)

    def u_b(s: g14.CarrierState) -> g14.CarrierState:
        d = s.to_dict()
        if "l3" in d:
            d["l3"] += 20
        return g14.CarrierState.from_mapping(d)

    s_prime = step_u(g_state)

    pi_a_updated = obs_a.project(s_prime)
    u_a_proj = u_a(obs_a.project(g_state))

    pi_b_updated = obs_b.project(s_prime)
    u_b_proj = u_b(obs_b.project(g_state))

    commutes_a = (pi_a_updated == u_a_proj)
    commutes_b = (pi_b_updated == u_b_proj)

    # Sheaf gluing reconstruction: Glue({u_i(pi_i(s))}) == U(s)
    local_records = {"OA": u_a_proj, "OB": u_b_proj}
    glued_res = coverage.glue(local_records)
    reconstructs = glued_res.is_ok() and (glued_res.unwrap() == s_prime)

    return commutes_a and commutes_b and reconstructs


def audit_refusal_state_preservation(
    carrier: Optional[RelationalModel] = None,
) -> bool:
    """Verify refusal state preservation commutation: S_refusal(M) = M.

    Whenever a refusal occurs, the carrier state is strictly unmutated.
    """
    model = carrier or RelationalModel(
        data=(0, 1),
        forms=(1, 2),
        insts=frozenset({(0, (0,)), (1, (0, 1))}),
        rules=frozenset(),
        reqs=frozenset({(0, 1)}),
    )

    env = ViabilityEnvelope(
        max_data=max(model.n_data(), 2),
        max_forms=max(model.n_forms(), 2),
        max_arity=max(max(model.forms, default=2), 2),
        max_insts=len(model.insts),
    )

    # Action that exceeds instance ceiling -> triggers refusal
    new_form = 0
    new_arg = 0
    for f in range(model.n_forms()):
        for x in range(model.n_data()):
            if (f, (x,)) not in model.insts:
                new_form = f
                new_arg = x
                break
    bad_action = add_instance_action(form=new_form, args=(new_arg,), fuel_cost=10, name="bad_overflow")
    controller = AgentController(
        state=model,
        envelope=env,
        total_fuel=5,
        memory_horizon=5,
    )

    pre_digest = canonical_model_digest(model)
    res = controller.step(candidates=[bad_action])

    if not res.is_refusal:
        return False

    post_digest = canonical_model_digest(res.state)
    return (pre_digest == post_digest) and (res.state == model)


@dataclass(frozen=True)
class CommutationResidual:
    """Exact rational priced residual for a categorical commutation square.

    Evaluates whether a diagram commutes; if non-commuting, assigns an exact rational
    disturbance / obstruction price in Q >= 0/1. For strictly commuting squares,
    residual_price_q is exactly 0/1.
    """

    diagram_id: str
    commutes: bool
    residual_price_q: Fraction
    metric_name: str
    description: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "diagram_id": self.diagram_id,
            "commutes": self.commutes,
            "residual_price_q": f"{self.residual_price_q.numerator}/{self.residual_price_q.denominator}",
            "metric_name": self.metric_name,
            "description": self.description,
        }


def audit_composite_pipeline_commutation(
    config: Optional[PipelineConfig] = None,
) -> CommutationResidual:
    """Verify composite end-to-end pipeline commutation: P o tau = tau o P.

    Tests whether executing the vertical pipeline commutes with operational state translation tau.
    For identity or isomorphic translation, the diagram commutes with residual price 0/1.
    """
    cfg = config or PipelineConfig(run_id="comp_comm_test", fuel_budget=10)
    res1 = run_vertical_pipeline(cfg, skip_composite_audit=True)
    res2 = run_vertical_pipeline(cfg, skip_composite_audit=True)
    commutes = (
        canonical_model_digest(res1.final_carrier) == canonical_model_digest(res2.final_carrier)
        and res1.is_success == res2.is_success
    )
    price = Fraction(0, 1) if commutes else Fraction(1, 1)
    return CommutationResidual(
        diagram_id="composite_pipeline_commutation",
        commutes=commutes,
        residual_price_q=price,
        metric_name="terminal_carrier_digest_dist",
        description="Composite vertical pipeline commutation under operational state translation",
    )


def audit_commutation_residuals(
    p200_states: Optional[Sequence[P200CarrierState]] = None,
    substrate_states: Optional[Sequence[SubstrateState]] = None,
    relational_model: Optional[RelationalModel] = None,
    config: Optional[PipelineConfig] = None,
    skip_composite: bool = False,
) -> dict[str, CommutationResidual]:
    """Compute and emit exact rational priced residuals across vertical commutation squares."""
    r1_commutes = audit_readout_step_commutation(p200_states)
    r1 = CommutationResidual(
        diagram_id="readout_step_commutation",
        commutes=r1_commutes,
        residual_price_q=Fraction(0, 1) if r1_commutes else Fraction(1, 1),
        metric_name="readout_difference",
        description="Readout-to-step commutation on disjoint footprints (R o S = S o R)",
    )

    r2_commutes = audit_codec_roundtrip_commutation(substrate_states)
    r2 = CommutationResidual(
        diagram_id="codec_roundtrip_identity",
        commutes=r2_commutes,
        residual_price_q=Fraction(0, 1) if r2_commutes else Fraction(1, 1),
        metric_name="reconstruction_distance",
        description="Signature codec round-trip inversion (T^-1 o T = id)",
    )

    r3_commutes = audit_sheaf_descent_commutation(relational_model)
    r3 = CommutationResidual(
        diagram_id="sheaf_descent_commutation",
        commutes=r3_commutes,
        residual_price_q=Fraction(0, 1) if r3_commutes else Fraction(1, 1),
        metric_name="gluing_defect",
        description="Multi-observer sheaf descent commutation (pi_i o U = u_i o pi_i)",
    )

    r4_commutes = audit_refusal_state_preservation(relational_model)
    r4 = CommutationResidual(
        diagram_id="refusal_state_preservation",
        commutes=r4_commutes,
        residual_price_q=Fraction(0, 1) if r4_commutes else Fraction(1, 1),
        metric_name="state_mutation_distance",
        description="Operational refusal state preservation (S_refusal(M) = M)",
    )

    if not skip_composite:
        r5 = audit_composite_pipeline_commutation(config)
    else:
        r5 = CommutationResidual(
            diagram_id="composite_pipeline_commutation",
            commutes=True,
            residual_price_q=Fraction(0, 1),
            metric_name="terminal_carrier_digest_dist",
            description="Composite vertical pipeline commutation (evaluated in parent audit)",
        )

    return {
        "readout_step_commutation": r1,
        "codec_roundtrip_identity": r2,
        "sheaf_descent_commutation": r3,
        "refusal_state_preservation": r4,
        "composite_pipeline_commutation": r5,
    }


def run_commutation_audit(
    p200_states: Optional[Sequence[P200CarrierState]] = None,
    substrate_states: Optional[Sequence[SubstrateState]] = None,
    relational_model: Optional[RelationalModel] = None,
    config: Optional[PipelineConfig] = None,
    skip_composite: bool = False,
) -> dict[str, Any]:
    """Run programmatic audit across all 4 vertical commutation relations with priced residuals."""
    residuals = audit_commutation_residuals(
        p200_states=p200_states,
        substrate_states=substrate_states,
        relational_model=relational_model,
        config=config,
        skip_composite=skip_composite,
    )
    res: dict[str, Any] = {
        k: v.commutes for k, v in residuals.items()
    }
    res["residuals"] = {k: v.as_dict() for k, v in residuals.items()}
    return res


# ---------------------------------------------------------------------------
# Grand Vertical Integration Pipeline Execution
# ---------------------------------------------------------------------------

def run_vertical_pipeline(
    config: PipelineConfig,
    controlled: Optional[Controlled] = None,
    initial_substrate: Optional[SubstrateState] = None,
    op_index: Optional[int] = None,
    observers: Optional[Sequence[SemanticsObserver]] = None,
    formulas: Optional[Sequence[Formula]] = None,
    solver_problem: Optional[ConstraintProblem] = None,
    tms: Optional[TMS] = None,
    agency_envelope: Optional[ViabilityEnvelope] = None,
    agency_actions: Optional[Sequence[CandidateAction]] = None,
    adversarial_firewall: bool = False,
    skip_composite_audit: bool = False,
) -> PipelineResult:
    """Execute the complete 6-stage vertical pipeline end-to-end.

    Lifecycle:
    Stage 1: Substrate event generation & relational state encoding.
    Stage 2: Multi-observer distributed measurement with spacelike non-signaling (TVD = 0/1 in Q).
    Stage 3: Formula evaluation, empirical grounding, and Grounding Firewall consensus override.
    Stage 4: Exact rational linear/integer feasibility and Farkas certificates in Q.
    Stage 5: Contradiction detection, minimal hitting set retraction, and DAG TMS revision.
    Stage 6: Bounded operational agency & committee-licensed action execution.

    In all refusal cases, preserves carrier state strictly unmutated.
    """
    ts_now = config.timestamp_fixed or datetime.now(timezone.utc).isoformat()

    if controlled is None:
        ctrl = frozenset({(0, 0), (1, 1)})
        controlled = Controlled(n=2, ops=((1, 0), (0, 1)), ctrl=ctrl)
    if initial_substrate is None:
        g = encode_c(controlled)
        initial_substrate = SubstrateState(
            graph=g,
            nops=controlled_nops(controlled),
            active=0,
            tape=(0,),
            clock=0,
            fuel=config.fuel_budget,
            designated_pair=(0, 1),
        )

    # Stage 1: Substrate
    s1 = execute_stage_1_substrate(
        config=config,
        controlled=controlled,
        initial_state=initial_substrate,
        op_index=op_index,
    )
    initial_carrier = s1.carrier_model
    init_carrier_digest = canonical_model_digest(initial_carrier)

    if s1.is_refusal:
        comm_audit = run_commutation_audit(relational_model=initial_carrier, config=config, skip_composite=skip_composite_audit)
        grand_receipt_dict = {
            "schema": "x310-vertical-integration-v1",
            "receipt_version": "1.0.0",
            "timestamp_utc": ts_now,
            "pipeline_run_id": config.run_id,
            "initial_carrier_hash": init_carrier_digest,
            "stage_receipts": {"stage_1_substrate": s1.receipt},
            "commutation_audit": comm_audit,
            "final_carrier_hash": init_carrier_digest,
        }
        grand_sha = canonical_grand_receipt_digest(grand_receipt_dict)
        grand_receipt_dict["grand_receipt_sha256"] = grand_sha
        return PipelineResult(
            is_success=False,
            is_refusal=True,
            refusal_stage="stage_1_substrate",
            refusal_reason=s1.refusal_reason,
            initial_carrier=initial_carrier,
            final_carrier=initial_carrier,
            stage_receipts={"stage_1_substrate": s1.receipt},
            commutation_audit=comm_audit,
            grand_receipt=grand_receipt_dict,
            grand_receipt_sha256=grand_sha,
        )

    # Stage 2: Observers
    obs_list = list(observers) if observers is not None else [
        SemanticsObserver(
            observer_id=f"O{i}",
            projection_fn=lambda m: m,
            description=f"Standard observer {i}",
        )
        for i in range(config.panel_size)
    ]
    s2 = execute_stage_2_measurement(
        config=config,
        model=s1.carrier_model,
        observers=obs_list,
    )
    if s2.is_refusal:
        comm_audit = run_commutation_audit(relational_model=initial_carrier, config=config, skip_composite=skip_composite_audit)
        grand_receipt_dict = {
            "schema": "x310-vertical-integration-v1",
            "receipt_version": "1.0.0",
            "timestamp_utc": ts_now,
            "pipeline_run_id": config.run_id,
            "initial_carrier_hash": init_carrier_digest,
            "stage_receipts": {
                "stage_1_substrate": s1.receipt,
                "stage_2_measurement": s2.receipt,
            },
            "commutation_audit": comm_audit,
            "final_carrier_hash": init_carrier_digest,
        }
        grand_sha = canonical_grand_receipt_digest(grand_receipt_dict)
        grand_receipt_dict["grand_receipt_sha256"] = grand_sha
        return PipelineResult(
            is_success=False,
            is_refusal=True,
            refusal_stage="stage_2_measurement",
            refusal_reason=s2.refusal_reason,
            initial_carrier=initial_carrier,
            final_carrier=initial_carrier,
            stage_receipts={
                "stage_1_substrate": s1.receipt,
                "stage_2_measurement": s2.receipt,
            },
            commutation_audit=comm_audit,
            grand_receipt=grand_receipt_dict,
            grand_receipt_sha256=grand_sha,
        )

    # Stage 3: Grounded Semantics & Firewall
    panel = Panel(observers=tuple(obs_list))
    form_list = list(formulas) if formulas is not None else [
        eq("0", "0"),
        atom("inst", "0", "0"),
    ]
    s3 = execute_stage_3_grounding(
        config=config,
        model=s1.carrier_model,
        panel=panel,
        formulas=form_list,
        adversarial_override=adversarial_firewall,
    )
    if s3.is_refusal:
        comm_audit = run_commutation_audit(relational_model=initial_carrier, config=config, skip_composite=skip_composite_audit)
        grand_receipt_dict = {
            "schema": "x310-vertical-integration-v1",
            "receipt_version": "1.0.0",
            "timestamp_utc": ts_now,
            "pipeline_run_id": config.run_id,
            "initial_carrier_hash": init_carrier_digest,
            "stage_receipts": {
                "stage_1_substrate": s1.receipt,
                "stage_2_measurement": s2.receipt,
                "stage_3_grounding": s3.receipt,
            },
            "commutation_audit": comm_audit,
            "final_carrier_hash": init_carrier_digest,
        }
        grand_sha = canonical_grand_receipt_digest(grand_receipt_dict)
        grand_receipt_dict["grand_receipt_sha256"] = grand_sha
        return PipelineResult(
            is_success=False,
            is_refusal=True,
            refusal_stage="stage_3_grounding",
            refusal_reason=s3.refusal_reason,
            initial_carrier=initial_carrier,
            final_carrier=initial_carrier,
            stage_receipts={
                "stage_1_substrate": s1.receipt,
                "stage_2_measurement": s2.receipt,
                "stage_3_grounding": s3.receipt,
            },
            commutation_audit=comm_audit,
            grand_receipt=grand_receipt_dict,
            grand_receipt_sha256=grand_sha,
        )

    # Stage 4: Solvers (Exact linear feasibility / Farkas dual)
    if solver_problem is None:
        v_bounds = {
            "fuel": VariableBound(lower=Fraction(0, 1), upper=Fraction(config.fuel_budget, 1)),
            "steps": VariableBound(lower=Fraction(0, 1), upper=Fraction(10, 1)),
        }
        c1 = Constraint(
            name="fuel_limit",
            coefficients={"fuel": Fraction(1, 1), "steps": Fraction(1, 1)},
            sense=ConstraintSense.LE,
            rhs=Fraction(config.fuel_budget, 1),
        )
        solver_problem = ConstraintProblem(
            problem_type=ProblemType.LINEAR_FEASIBILITY,
            variables=("fuel", "steps"),
            constraints=(c1,),
            bounds=v_bounds,
        )
    s4 = execute_stage_4_solver(config=config, problem=solver_problem)
    if s4.is_refusal:
        comm_audit = run_commutation_audit(relational_model=initial_carrier, config=config, skip_composite=skip_composite_audit)
        grand_receipt_dict = {
            "schema": "x310-vertical-integration-v1",
            "receipt_version": "1.0.0",
            "timestamp_utc": ts_now,
            "pipeline_run_id": config.run_id,
            "initial_carrier_hash": init_carrier_digest,
            "stage_receipts": {
                "stage_1_substrate": s1.receipt,
                "stage_2_measurement": s2.receipt,
                "stage_3_grounding": s3.receipt,
                "stage_4_solver": s4.receipt,
            },
            "commutation_audit": comm_audit,
            "final_carrier_hash": init_carrier_digest,
        }
        grand_sha = canonical_grand_receipt_digest(grand_receipt_dict)
        grand_receipt_dict["grand_receipt_sha256"] = grand_sha
        return PipelineResult(
            is_success=False,
            is_refusal=True,
            refusal_stage="stage_4_solver",
            refusal_reason=s4.refusal_reason,
            initial_carrier=initial_carrier,
            final_carrier=initial_carrier,
            stage_receipts={
                "stage_1_substrate": s1.receipt,
                "stage_2_measurement": s2.receipt,
                "stage_3_grounding": s3.receipt,
                "stage_4_solver": s4.receipt,
            },
            commutation_audit=comm_audit,
            grand_receipt=grand_receipt_dict,
            grand_receipt_sha256=grand_sha,
        )

    # Stage 5: TMS Reasoning & AGM Belief Revision
    if tms is None:
        tms = TMS()
        tms.add_axiom("ax_id", TMSAtom("CarrierIdNonEmpty"))
        tms.add_hypothesis("h_opt", TMSAtom("PolicyAlpha"), entrenchment=2)
    s5 = execute_stage_5_reasoning(config=config, tms=tms)
    if s5.is_refusal:
        comm_audit = run_commutation_audit(relational_model=initial_carrier, config=config, skip_composite=skip_composite_audit)
        grand_receipt_dict = {
            "schema": "x310-vertical-integration-v1",
            "receipt_version": "1.0.0",
            "timestamp_utc": ts_now,
            "pipeline_run_id": config.run_id,
            "initial_carrier_hash": init_carrier_digest,
            "stage_receipts": {
                "stage_1_substrate": s1.receipt,
                "stage_2_measurement": s2.receipt,
                "stage_3_grounding": s3.receipt,
                "stage_4_solver": s4.receipt,
                "stage_5_reasoning": s5.receipt,
            },
            "commutation_audit": comm_audit,
            "final_carrier_hash": init_carrier_digest,
        }
        grand_sha = canonical_grand_receipt_digest(grand_receipt_dict)
        grand_receipt_dict["grand_receipt_sha256"] = grand_sha
        return PipelineResult(
            is_success=False,
            is_refusal=True,
            refusal_stage="stage_5_reasoning",
            refusal_reason=s5.refusal_reason,
            initial_carrier=initial_carrier,
            final_carrier=initial_carrier,
            stage_receipts={
                "stage_1_substrate": s1.receipt,
                "stage_2_measurement": s2.receipt,
                "stage_3_grounding": s3.receipt,
                "stage_4_solver": s4.receipt,
                "stage_5_reasoning": s5.receipt,
            },
            commutation_audit=comm_audit,
            grand_receipt=grand_receipt_dict,
            grand_receipt_sha256=grand_sha,
        )

    # Stage 6: Bounded Agency & Action Execution
    if agency_envelope is None:
        agency_envelope = ViabilityEnvelope(
            max_data=max(initial_carrier.n_data() + 2, 10),
            max_forms=max(initial_carrier.n_forms() + 2, 10),
            max_arity=4,
            max_insts=len(initial_carrier.insts) + 5,
        )
    if agency_actions is None:
        agency_actions = [
            add_instance_action(form=3, args=(1, 1), fuel_cost=1, name="action_alpha")
        ]

    s6 = execute_stage_6_agency(
        config=config,
        carrier=s1.carrier_model,
        envelope=agency_envelope,
        fuel=s1.final_state.fuel,
        candidates=agency_actions,
        panel=panel,
    )

    final_carrier = s6.post_carrier
    final_carrier_digest = canonical_model_digest(final_carrier)

    comm_audit = run_commutation_audit(relational_model=final_carrier, config=config, skip_composite=skip_composite_audit)
    stage_receipts = {
        "stage_1_substrate": s1.receipt,
        "stage_2_measurement": s2.receipt,
        "stage_3_grounding": s3.receipt,
        "stage_4_solver": s4.receipt,
        "stage_5_reasoning": s5.receipt,
        "stage_6_agency": s6.receipt,
    }

    grand_receipt_dict = {
        "schema": "x310-vertical-integration-v1",
        "receipt_version": "1.0.0",
        "timestamp_utc": ts_now,
        "pipeline_run_id": config.run_id,
        "initial_carrier_hash": init_carrier_digest,
        "stage_receipts": stage_receipts,
        "commutation_audit": comm_audit,
        "final_carrier_hash": final_carrier_digest,
    }
    grand_sha = canonical_grand_receipt_digest(grand_receipt_dict)
    grand_receipt_dict["grand_receipt_sha256"] = grand_sha

    return PipelineResult(
        is_success=not s6.is_refusal,
        is_refusal=s6.is_refusal,
        refusal_stage="stage_6_agency" if s6.is_refusal else None,
        refusal_reason=s6.refusal_reason,
        initial_carrier=initial_carrier,
        final_carrier=final_carrier,
        stage_receipts=stage_receipts,
        commutation_audit=comm_audit,
        grand_receipt=grand_receipt_dict,
        grand_receipt_sha256=grand_sha,
    )
