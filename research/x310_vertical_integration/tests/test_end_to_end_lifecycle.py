"""Target X310: Comprehensive end-to-end lifecycle integration and negative control matrix.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, narrow, receipt-grounded).

Covers:
1. Complete standard lifecycle execution (Substrate -> Observers -> Grounding -> Solver -> TMS -> Agency).
2. Negative Control 1: Substrate protection obligation violation -> Stage 1 typed refusal, state unmutated.
3. Negative Control 2: Grounding Firewall false consensus override -> Stage 3 typed refusal, PanelIllusionReceipt.
4. Negative Control 3: Infeasible linear constraints -> Stage 4 Farkas DualReceipt verification.
5. Negative Control 4: Active TMS contradiction resolution -> Stage 5 minimal hitting set retraction.
6. Negative Control 5: Agency viability envelope violation -> Stage 6 typed refusal, state unmutated.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
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
    "x301_formal_semantics",
    "m114_solver_adapter",
    "x302_operational_reasoning",
    "x303_bounded_agency",
]:
    _sub_path = _REPO_ROOT / "research" / _sub
    if str(_sub_path) not in sys.path:
        sys.path.insert(0, str(_sub_path))

import research.target_a_execution.runner as _tar_runner
sys.modules["runner"] = _tar_runner
import research.p200_operational_protocols.protocol as _p200_prot
sys.modules["protocol"] = _p200_prot
import research.p200_operational_protocols.embedded_observer as _p200_emb
sys.modules["embedded_observer"] = _p200_emb

from research.target_a_execution.control import (
    Controlled,
    State as SubstrateState,
    build_program,
    encode_c,
    nops as controlled_nops,
)
from research.target_a_execution.runner import (
    ProtectionKind,
    ProtectionObligation,
    Refusal as SubstrateRefusal,
)
from research.x301_formal_semantics.semantics import (
    PanelIllusionReceipt,
    RelationalModel,
    atom,
    eq,
)
from research.m114_solver_adapter.solver_adapter import (
    Constraint,
    ConstraintProblem,
    ConstraintSense,
    DualReceipt,
    PrimalReceipt,
    ProblemType,
    VariableBound,
)
from research.x302_operational_reasoning.reasoning import (
    Atom as TMSAtom,
    OperationalTMS,
)
from research.x303_bounded_agency.agency import (
    AgencyReceipt,
    ViabilityEnvelope,
    add_instance_action,
    canonical_model_digest,
)

from research.x310_vertical_integration.pipeline import (
    PipelineConfig,
    run_vertical_pipeline,
)


def test_standard_lifecycle_end_to_end():
    """Verify complete vertical lifecycle execution from genesis substrate to licensed agency mutation."""
    cfg = PipelineConfig(
        fuel_budget=15,
        memory_horizon=5,
        run_id="TEST-E2E-SUCCESS-001",
        timestamp_fixed="2026-09-12T00:00:00Z",
    )

    res = run_vertical_pipeline(cfg)

    # 1. Pipeline success audit
    assert res.is_success
    assert not res.is_refusal
    assert res.refusal_stage is None
    assert res.refusal_reason is None

    # 2. State transition audit
    init_hash = res.grand_receipt["initial_carrier_hash"]
    final_hash = res.grand_receipt["final_carrier_hash"]
    assert init_hash != final_hash
    assert final_hash == canonical_model_digest(res.final_carrier)

    # 3. Stage receipts presence and schema audit
    receipts = res.stage_receipts
    assert receipts["stage_1_substrate"]["terminal"] == "FINITARY_SUBSTRATE_INTERNAL"
    assert receipts["stage_2_measurement"]["non_signaling_tvd"] == "0/1"
    assert receipts["stage_3_grounding"]["firewall_action"] == "PASSED"
    assert receipts["stage_4_solver"]["status"] == "FEASIBLE"
    assert receipts["stage_5_reasoning"]["agm_postulates_satisfied"]["success"]
    assert receipts["stage_6_agency"]["selected_action"] == "action_alpha"

    # 4. Commutation audit verified
    assert res.commutation_audit["readout_step_commutation"]
    assert res.commutation_audit["codec_roundtrip_identity"]
    assert res.commutation_audit["sheaf_descent_commutation"]
    assert res.commutation_audit["refusal_state_preservation"]

    # 5. Grand receipt cryptographic hash
    assert res.grand_receipt_sha256 == res.grand_receipt["grand_receipt_sha256"]


def test_negative_control_1_substrate_protection_obligation_refusal():
    """Negative Control 1: Violation of protection obligation halts pipeline at Stage 1, state unmutated."""
    ctrl = frozenset({(0, 0), (1, 0)})
    c = Controlled(n=2, ops=((0, 0),), ctrl=ctrl)  # Operation collapses 1 to 0
    g = encode_c(c)

    # Protection obligation forbidding collapse of pair (0, 1)
    obl = ProtectionObligation(kind=ProtectionKind.SEPARATED, u=0, v=1)
    s0 = SubstrateState(
        graph=g,
        nops=1,
        active=0,
        tape=(0,),
        clock=0,
        fuel=10,
        protection_obligations=(obl,),
    )

    cfg = PipelineConfig(run_id="TEST-NEG-1", timestamp_fixed="2026-09-12T00:00:00Z")
    res = run_vertical_pipeline(cfg, controlled=c, initial_substrate=s0, op_index=0)

    assert not res.is_success
    assert res.is_refusal
    assert res.refusal_stage == "stage_1_substrate"
    assert "PROTECTION_VIOLATION" in str(res.refusal_reason)

    # State preservation invariant: carrier is strictly unmutated
    assert res.final_carrier == res.initial_carrier
    assert res.grand_receipt["initial_carrier_hash"] == res.grand_receipt["final_carrier_hash"]


def test_negative_control_2_grounding_firewall_consensus_override():
    """Negative Control 2: Grounding Firewall override halts pipeline at Stage 3 with PanelIllusionReceipt."""
    cfg = PipelineConfig(run_id="TEST-NEG-2", timestamp_fixed="2026-09-12T00:00:00Z")

    res = run_vertical_pipeline(cfg, adversarial_firewall=True)

    assert not res.is_success
    assert res.is_refusal
    assert res.refusal_stage == "stage_3_grounding"
    assert "Grounding Firewall override" in str(res.refusal_reason)

    # Panel illusion receipt recorded in stage receipt
    s3_receipt = res.stage_receipts["stage_3_grounding"]
    assert s3_receipt["firewall_action"] == "REFUSAL_OVERRIDE"
    assert s3_receipt["illusion_receipt_sha256"] is not None

    # State preservation invariant: carrier is strictly unmutated
    assert res.final_carrier == res.initial_carrier
    assert res.grand_receipt["initial_carrier_hash"] == res.grand_receipt["final_carrier_hash"]


def test_negative_control_3_solver_infeasibility_and_farkas_dual():
    """Negative Control 3: Infeasible linear constraints produces verified Farkas DualReceipt."""
    cfg = PipelineConfig(run_id="TEST-NEG-3", timestamp_fixed="2026-09-12T00:00:00Z")

    infeas_problem = ConstraintProblem(
        problem_type=ProblemType.LINEAR_FEASIBILITY,
        variables=("fuel",),
        constraints=(
            Constraint("c_min", {"fuel": Fraction(1, 1)}, ConstraintSense.GE, Fraction(50, 1)),
            Constraint("c_max", {"fuel": Fraction(1, 1)}, ConstraintSense.LE, Fraction(20, 1)),
        ),
        bounds={"fuel": VariableBound(lower=Fraction(0, 1), upper=Fraction(100, 1))},
    )

    res = run_vertical_pipeline(cfg, solver_problem=infeas_problem)

    # Solver reports INFEASIBLE and emits verified DualReceipt
    assert res.stage_receipts["stage_4_solver"]["status"] == "INFEASIBLE"
    assert res.stage_receipts["stage_4_solver"]["certificate_type"] == "DualReceipt"


def test_negative_control_4_tms_contradiction_resolution():
    """Negative Control 4: Active contradiction triggers minimal hitting set retraction in Stage 5."""
    cfg = PipelineConfig(run_id="TEST-NEG-4", timestamp_fixed="2026-09-12T00:00:00Z")

    tms = OperationalTMS()
    tms.add_axiom("ax_base", TMSAtom("BaseAxiom"))
    # Ingest contradictory hypotheses
    tms.add_hypothesis("h_active", TMSAtom("P"), entrenchment=2)
    tms.add_hypothesis("h_inactive", TMSAtom("NotP"), entrenchment=1)

    res = run_vertical_pipeline(cfg, tms=tms)

    # Pipeline continues and TMS resolved contradiction via retraction
    s5_receipt = res.stage_receipts["stage_5_reasoning"]
    assert s5_receipt["agm_postulates_satisfied"]["success"]
    assert s5_receipt["agm_postulates_satisfied"]["consistency"]
    assert s5_receipt["agm_postulates_satisfied"]["axiom_invariance"]


def test_negative_control_5_agency_viability_envelope_refusal():
    """Negative Control 5: Action violating viability envelope halts pipeline at Stage 6 in refusal."""
    cfg = PipelineConfig(run_id="TEST-NEG-5", timestamp_fixed="2026-09-12T00:00:00Z")

    # Tight envelope: maximum 5 instances
    strict_envelope = ViabilityEnvelope(
        max_data=10,
        max_forms=10,
        max_arity=4,
        max_insts=5,  # Substrate initial carrier already has 9 instances!
    )

    res = run_vertical_pipeline(cfg, agency_envelope=strict_envelope)

    assert not res.is_success
    assert res.is_refusal
    assert res.refusal_stage == "stage_6_agency"
    assert "exceeds ceiling" in str(res.refusal_reason) or "viability" in str(res.refusal_reason).lower()

    # State preservation invariant: carrier is strictly unmutated
    assert res.final_carrier == res.initial_carrier
    assert res.grand_receipt["initial_carrier_hash"] == res.grand_receipt["final_carrier_hash"]
