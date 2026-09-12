"""Target X310: six-stage research harness. AuthorityEffect: None.

Stages 1, 2, 3, and 6 share the substrate-encoded carrier. Stages 4 and 5
run sibling solver/TMS demos under the same receipt; they are not a
carrier-threaded translation of that model.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Optional, Sequence

from . import _bootstrap  # noqa: F401
from research.m114_solver_adapter.solver_adapter import (
    Constraint,
    ConstraintProblem,
    ConstraintSense,
    ProblemType,
    VariableBound,
)
from research.target_a_execution.control import Controlled, encode_c, nops as controlled_nops
from research.target_a_execution.control import State as SubstrateState
from research.x301_formal_semantics.semantics import (
    Formula,
    Observer as SemanticsObserver,
    Panel,
    atom,
    eq,
)
from research.x302_operational_reasoning.reasoning import Atom as TMSAtom
from research.x302_operational_reasoning.reasoning import OperationalTMS as TMS
from research.x303_bounded_agency.agency import (
    CandidateAction,
    ViabilityEnvelope,
    add_instance_action,
    canonical_model_digest,
)
from .commutation import (
    CommutationResidual,
    audit_codec_roundtrip_commutation,
    audit_commutation_residuals,
    audit_pipeline_run_determinism,
    audit_readout_step_commutation,
    audit_refusal_state_preservation,
    audit_sheaf_descent_commutation,
    run_commutation_audit,
)
from .codec import decode_relational_to_substrate, encode_substrate_to_relational
from .receipts import canonical_grand_receipt_digest, canonical_json_dumps
from .stages import (
    execute_stage_1_substrate,
    execute_stage_2_measurement,
    execute_stage_3_grounding,
    execute_stage_4_solver,
    execute_stage_5_reasoning,
    execute_stage_6_agency,
    project_model_to_locus,
)
from .types import (
    PipelineConfig,
    PipelineResult,
    Stage1Result,
    Stage2Result,
    Stage3Result,
    Stage4Result,
    Stage5Result,
    Stage6Result,
)


def _grand(
    config: PipelineConfig,
    initial_carrier,
    init_digest: str,
    stage_receipts: dict,
    final_carrier,
    skip_composite: bool,
    refusal_stage: Optional[str],
    refusal_reason: Optional[str],
    is_refusal: bool,
) -> PipelineResult:
    comm_audit = run_commutation_audit(
        relational_model=initial_carrier,
        config=config,
        skip_composite=skip_composite,
    )
    final_digest = canonical_model_digest(final_carrier)
    grand = {
        "schema": "x310-vertical-integration-v1",
        "receipt_version": "1.0.0",
        "timestamp_utc": config.timestamp_fixed,
        "pipeline_run_id": config.run_id,
        "initial_carrier_hash": init_digest,
        "stage_receipts": stage_receipts,
        "commutation_audit": comm_audit,
        "final_carrier_hash": final_digest,
    }
    sha = canonical_grand_receipt_digest(grand)
    grand["grand_receipt_sha256"] = sha
    return PipelineResult(
        is_success=not is_refusal,
        is_refusal=is_refusal,
        refusal_stage=refusal_stage,
        refusal_reason=refusal_reason,
        initial_carrier=initial_carrier,
        final_carrier=final_carrier,
        stage_receipts=stage_receipts,
        commutation_audit=comm_audit,
        grand_receipt=grand,
        grand_receipt_sha256=sha,
    )


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

    s1 = execute_stage_1_substrate(
        config=config,
        controlled=controlled,
        initial_state=initial_substrate,
        op_index=op_index,
    )
    initial_carrier = s1.carrier_model
    init_digest = canonical_model_digest(initial_carrier)
    receipts: dict = {"stage_1_substrate": s1.receipt}
    if s1.is_refusal:
        return _grand(
            config, initial_carrier, init_digest, receipts, initial_carrier,
            skip_composite_audit, "stage_1_substrate", s1.refusal_reason, True,
        )

    obs_list = list(observers) if observers is not None else [
        SemanticsObserver(
            observer_id=f"O{i}",
            projection_fn=lambda m: m,
            description=f"Standard observer {i}",
        )
        for i in range(config.panel_size)
    ]
    s2 = execute_stage_2_measurement(config=config, model=s1.carrier_model, observers=obs_list)
    receipts["stage_2_measurement"] = s2.receipt
    if s2.is_refusal:
        return _grand(
            config, initial_carrier, init_digest, receipts, initial_carrier,
            skip_composite_audit, "stage_2_measurement", s2.refusal_reason, True,
        )

    panel = Panel(observers=tuple(obs_list))
    form_list = list(formulas) if formulas is not None else [eq("0", "0"), atom("inst", "0", "0")]
    s3 = execute_stage_3_grounding(
        config=config,
        model=s1.carrier_model,
        panel=panel,
        formulas=form_list,
        adversarial_override=adversarial_firewall,
    )
    receipts["stage_3_grounding"] = s3.receipt
    if s3.is_refusal:
        return _grand(
            config, initial_carrier, init_digest, receipts, initial_carrier,
            skip_composite_audit, "stage_3_grounding", s3.refusal_reason, True,
        )

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
    receipts["stage_4_solver"] = s4.receipt
    if s4.is_refusal:
        return _grand(
            config, initial_carrier, init_digest, receipts, initial_carrier,
            skip_composite_audit, "stage_4_solver", s4.refusal_reason, True,
        )

    if tms is None:
        tms = TMS()
        tms.add_axiom("ax_id", TMSAtom("CarrierIdNonEmpty"))
        tms.add_hypothesis("h_opt", TMSAtom("PolicyAlpha"), entrenchment=2)
    s5 = execute_stage_5_reasoning(config=config, tms=tms)
    receipts["stage_5_reasoning"] = s5.receipt
    if s5.is_refusal:
        return _grand(
            config, initial_carrier, init_digest, receipts, initial_carrier,
            skip_composite_audit, "stage_5_reasoning", s5.refusal_reason, True,
        )

    if agency_envelope is None:
        agency_envelope = ViabilityEnvelope(
            max_data=max(initial_carrier.n_data() + 2, 10),
            max_forms=max(initial_carrier.n_forms() + 2, 10),
            max_arity=4,
            max_insts=len(initial_carrier.insts) + 5,
        )
    if agency_actions is None:
        agency_actions = [add_instance_action(form=3, args=(1, 1), fuel_cost=1, name="action_alpha")]

    s6 = execute_stage_6_agency(
        config=config,
        carrier=s1.carrier_model,
        envelope=agency_envelope,
        fuel=s1.final_state.fuel,
        candidates=agency_actions,
        panel=panel,
    )
    receipts["stage_6_agency"] = s6.receipt
    return _grand(
        config,
        initial_carrier,
        init_digest,
        receipts,
        s6.post_carrier,
        skip_composite_audit,
        "stage_6_agency" if s6.is_refusal else None,
        s6.refusal_reason,
        s6.is_refusal,
    )


audit_composite_pipeline_commutation = audit_pipeline_run_determinism
