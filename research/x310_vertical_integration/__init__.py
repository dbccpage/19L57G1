"""Target X310: Vertical Integration Chain.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, narrow, receipt-grounded).
"""

from pathlib import Path
import sys

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
    "x301_formal_semantics",
    "m114_solver_adapter",
    "x302_operational_reasoning",
    "x303_bounded_agency",
]:
    _sub_path = _REPO_ROOT / "research" / _sub
    if str(_sub_path) not in sys.path:
        sys.path.insert(0, str(_sub_path))

from research.x310_vertical_integration.pipeline import (
    PipelineConfig,
    PipelineResult,
    Stage1Result,
    Stage2Result,
    Stage3Result,
    Stage4Result,
    Stage5Result,
    Stage6Result,
    audit_codec_roundtrip_commutation,
    audit_readout_step_commutation,
    audit_refusal_state_preservation,
    audit_sheaf_descent_commutation,
    canonical_grand_receipt_digest,
    canonical_json_dumps,
    decode_relational_to_substrate,
    encode_substrate_to_relational,
    execute_stage_1_substrate,
    execute_stage_2_measurement,
    execute_stage_3_grounding,
    execute_stage_4_solver,
    execute_stage_5_reasoning,
    execute_stage_6_agency,
    run_commutation_audit,
    run_vertical_pipeline,
)

__all__ = [
    "PipelineConfig",
    "PipelineResult",
    "Stage1Result",
    "Stage2Result",
    "Stage3Result",
    "Stage4Result",
    "Stage5Result",
    "Stage6Result",
    "audit_codec_roundtrip_commutation",
    "audit_readout_step_commutation",
    "audit_refusal_state_preservation",
    "audit_sheaf_descent_commutation",
    "canonical_grand_receipt_digest",
    "canonical_json_dumps",
    "decode_relational_to_substrate",
    "encode_substrate_to_relational",
    "execute_stage_1_substrate",
    "execute_stage_2_measurement",
    "execute_stage_3_grounding",
    "execute_stage_4_solver",
    "execute_stage_5_reasoning",
    "execute_stage_6_agency",
    "run_commutation_audit",
    "run_vertical_pipeline",
]
