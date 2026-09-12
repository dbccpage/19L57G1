"""Target X303: Agency & Control (Bounded Operational Agency).

Pure Python bounded agency engine providing:
1. Discrete Viability Envelopes over relational carrier states in exact rational arithmetic.
2. Finite Memory Horizons with deterministic FIFO eviction preserving data processing bounds.
3. Strict Refusal Semantics (StepResult.refusal) preserving carrier state strictly unmutated.
4. Causal Counterfactual Evaluation with ephemeral branch projection and X301 Grounding Firewall.
5. Alpha Engine Licensing contract (Proposal -> EvalResult -> License) with zero unilateral authority.
6. Exact Rational Multicriteria Selection in [0, 1] cap Q with canonical tie-breaking.

AuthorityEffect: None.
Epistemic Posture: Claim Hygiene Compliant (bounded, narrow, receipt-grounded).
"""

from __future__ import annotations

from pathlib import Path
import sys

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
for _sub in ["x301_formal_semantics"]:
    _sub_path = _REPO_ROOT / "research" / _sub
    if str(_sub_path) not in sys.path:
        sys.path.insert(0, str(_sub_path))

from .agency import (
    ActionAuthorizer,
    ActionEvalResult,
    ActionEvaluation,
    ActionProposal,
    AgencyReceipt,
    AgentController,
    BoundedMemory,
    CandidateAction,
    CausalEvaluator,
    License,
    LicensedDriver,
    MemoryRecord,
    MulticriteriaSelector,
    RefusalReason,
    RetainedActionClass,
    StepRefusalData,
    StepResult,
    UnlicensedActionError,
    ViabilityEnvelope,
    add_instance_action,
    add_requirement_action,
    canonical_model_digest,
    compute_canon_key,
    remove_instance_action,
    toggle_rule_action,
)

__all__ = [
    "ActionAuthorizer",
    "ActionEvalResult",
    "ActionEvaluation",
    "ActionProposal",
    "AgencyReceipt",
    "AgentController",
    "BoundedMemory",
    "CandidateAction",
    "CausalEvaluator",
    "License",
    "LicensedDriver",
    "MemoryRecord",
    "MulticriteriaSelector",
    "RefusalReason",
    "RetainedActionClass",
    "StepRefusalData",
    "StepResult",
    "UnlicensedActionError",
    "ViabilityEnvelope",
    "add_instance_action",
    "add_requirement_action",
    "canonical_model_digest",
    "compute_canon_key",
    "remove_instance_action",
    "toggle_rule_action",
]
