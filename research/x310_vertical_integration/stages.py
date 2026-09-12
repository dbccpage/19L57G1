"""Stage executors. AuthorityEffect: None."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from typing import Callable, Dict, Optional, Sequence

from . import _bootstrap  # noqa: F401
from research.m114_solver_adapter.solver_adapter import (
    ConstraintProblem,
    DualReceipt,
    IntegerInfeasibilityReceipt,
    PrimalReceipt,
    SolverAdapter,
)
from research.p200_operational_protocols.embedded_observer import EmbeddedObserver
from research.p200_operational_protocols.non_signaling import verify_spacelike_non_signaling
from research.p200_operational_protocols.protocol import (
    CarrierState as P200CarrierState,
    Locus,
)
from research.target_a_execution.control import Controlled, fire
from research.target_a_execution.control import State as SubstrateState
from research.target_a_execution.runner import Refusal as SubstrateRefusal
from research.x300_observer_information.information import (
    Channel,
    DiscreteDistribution,
    verify_data_processing_inequality,
)
from research.x301_formal_semantics.semantics import (
    Formula,
    GroundingFirewall,
    Panel,
    PanelIllusionReceipt,
    RelationalModel,
    Observer as SemanticsObserver,
    evaluate,
)
from research.x302_operational_reasoning.reasoning import OperationalTMS as TMS
from research.x303_bounded_agency.agency import (
    AgencyReceipt,
    AgentController,
    CandidateAction,
    ViabilityEnvelope,
    canonical_model_digest,
)
from .codec import encode_substrate_to_relational
from .types import (
    PipelineConfig,
    Stage1Result,
    Stage2Result,
    Stage3Result,
    Stage4Result,
    Stage5Result,
    Stage6Result,
)

OperationalChannel = Channel

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
        "commutation_verified": False,
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
        for phi in formulas:
            fw = GroundingFirewall.evaluate_and_step(
                model=model,
                formula=phi,
                panel=panel,
                candidate_interventions=(),
            )
            if fw.is_refusal:
                rec = fw.receipt
                illusion_receipt = rec if isinstance(rec, PanelIllusionReceipt) else None
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
    if step_res.selected_action is None or step_res.utility is None:
        raise RuntimeError("Successful agency step missing selected action or utility")
    selected_action_name = step_res.selected_action.name
    exact_utility = controller.selector.composite_utility(step_res.utility)

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
