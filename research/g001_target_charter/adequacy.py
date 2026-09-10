"""Evaluation engine for candidate target systems against the 9 pre-registered criteria.

Evaluates candidate target systems without retrospective target shifting.
Enforces that evaluations are performed exclusively against frozen charters
(TOE_TARGET_CLASS_FROZEN) and detects circular self-definition or unencoded
oracle dependencies.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction
from typing import Any, Callable, Mapping, Sequence, Set

from charter import CriterionID, TargetClassCharter


class Verdict(str, Enum):
    """Evaluation verdict for a single criterion or overall system."""
    SATISFIED = "SATISFIED"
    PARTIALLY_SATISFIED = "PARTIALLY_SATISFIED"
    FAILED = "FAILED"
    REFUSED = "REFUSED"


@dataclass(frozen=True)
class CriterionResult:
    """Detailed evaluation result for a single criterion."""
    criterion_id: CriterionID
    verdict: Verdict
    score: Fraction
    details: str
    capabilities_met: tuple[str, ...]
    capabilities_missing: tuple[str, ...]
    falsification_detected: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "criterion_id": self.criterion_id.value,
            "verdict": self.verdict.value,
            "score": str(self.score),
            "details": self.details,
            "capabilities_met": list(self.capabilities_met),
            "capabilities_missing": list(self.capabilities_missing),
            "falsification_detected": self.falsification_detected,
        }


@dataclass
class TargetSystem:
    """Specification of a candidate formal system under evaluation."""
    name: str
    states: Sequence[Any]
    operations: Sequence[Any]
    step: Callable[[Any, Any], Any | None]
    observe: Callable[[Any], Any]
    capabilities: Set[str] = field(default_factory=set)
    evidence_receipts: dict[str, Any] = field(default_factory=dict)
    is_circular_definition: bool = False
    has_unencoded_oracle: bool = False
    description: str = ""

    def run_bounded(self, initial_state: Any, ops: Sequence[Any], max_steps: int = 100) -> tuple[list[Any], list[Any]]:
        """Executes a bounded sequence of operations from initial_state, recording states and observations."""
        current = initial_state
        state_trace = [current]
        obs_trace = [self.observe(current)]
        for i, op in enumerate(ops):
            if i >= max_steps:
                break
            nxt = self.step(current, op)
            if nxt is None:
                break
            current = nxt
            state_trace.append(current)
            obs_trace.append(self.observe(current))
        return state_trace, obs_trace


@dataclass(frozen=True)
class EvaluationReport:
    """Comprehensive evaluation report for a candidate target system."""
    candidate_name: str
    charter_hash: str
    charter_status: str
    results: dict[CriterionID, CriterionResult]
    total_criteria: int
    satisfied_count: int
    overall_verdict: Verdict
    non_retrospective: bool
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_name": self.candidate_name,
            "charter_hash": self.charter_hash,
            "charter_status": self.charter_status,
            "total_criteria": self.total_criteria,
            "satisfied_count": self.satisfied_count,
            "overall_verdict": self.overall_verdict.value,
            "non_retrospective": self.non_retrospective,
            "summary": self.summary,
            "results": {cid.value: res.to_dict() for cid, res in self.results.items()},
        }


class AdequacyEngine:
    """Evaluation engine evaluating candidate target systems against a frozen charter."""

    def __init__(self, charter: TargetClassCharter) -> None:
        if not charter.is_frozen:
            raise ValueError(
                "AdequacyEngine requires a frozen charter (TOE_TARGET_CLASS_FROZEN) "
                "to prevent retrospective target shifting."
            )
        self._charter = charter

    @property
    def charter(self) -> TargetClassCharter:
        return self._charter

    def evaluate(self, system: TargetSystem) -> EvaluationReport:
        """Evaluates candidate system against all 9 criteria without retrospective shifts."""
        is_circular = system.is_circular_definition or (
            "genesis_evaluator" in system.description.lower()
            or "target_class_charter" in system.description.lower()
        )
        if is_circular:
            refused_results = {}
            for cid in self._charter.criteria:
                refused_results[cid] = CriterionResult(
                    criterion_id=cid,
                    verdict=Verdict.REFUSED,
                    score=Fraction(0, 1),
                    details="Refused: candidate circularly defines adequacy standards via self-reference.",
                    capabilities_met=(),
                    capabilities_missing=tuple(self._charter.get_criterion(cid).required_capabilities),
                    falsification_detected=True,
                )
            return EvaluationReport(
                candidate_name=system.name,
                charter_hash=self._charter.freeze_hash or "",
                charter_status=self._charter.status,
                results=refused_results,
                total_criteria=9,
                satisfied_count=0,
                overall_verdict=Verdict.REFUSED,
                non_retrospective=True,
                summary="Refused: Candidate exhibits circular self-definition rather than independent adequacy.",
            )

        results: dict[CriterionID, CriterionResult] = {}
        for cid, criterion in self._charter.criteria.items():
            result = self._evaluate_single(system, criterion)
            results[cid] = result

        satisfied_count = sum(1 for r in results.values() if r.verdict == Verdict.SATISFIED)
        refused_count = sum(1 for r in results.values() if r.verdict == Verdict.REFUSED)
        failed_count = sum(1 for r in results.values() if r.verdict == Verdict.FAILED)

        if refused_count > 0:
            overall = Verdict.REFUSED
            summary = f"Evaluation Refused: {refused_count} criteria triggered refusal conditions."
        elif failed_count > 0 or satisfied_count < 9:
            if satisfied_count > 0:
                overall = Verdict.PARTIALLY_SATISFIED
                summary = f"Partially Satisfied: {satisfied_count}/9 criteria satisfied."
            else:
                overall = Verdict.FAILED
                summary = f"Failed: 0/9 criteria satisfied."
        else:
            overall = Verdict.SATISFIED
            summary = "Satisfied: Candidate satisfies all 9 pre-registered independent criteria."

        return EvaluationReport(
            candidate_name=system.name,
            charter_hash=self._charter.freeze_hash or "",
            charter_status=self._charter.status,
            results=results,
            total_criteria=len(results),
            satisfied_count=satisfied_count,
            overall_verdict=overall,
            non_retrospective=True,
            summary=summary,
        )

    def _evaluate_single(self, system: TargetSystem, criterion: Any) -> CriterionResult:
        cid = criterion.criterion_id
        required = criterion.required_capabilities

        # Check for unencoded oracle reliance (disallowed for computational & representational)
        has_oracle = system.has_unencoded_oracle or any(
            getattr(fn, "__name__", "") in ("oracle", "unencoded_oracle", "host_lookup")
            for fn in (system.step, system.observe)
        )
        if has_oracle and cid in (
            CriterionID.COMPUTATIONAL,
            CriterionID.REPRESENTATIONAL,
        ):
            return CriterionResult(
                criterion_id=cid,
                verdict=Verdict.REFUSED,
                score=Fraction(0, 1),
                details="Refused: System relies on unencoded host oracles.",
                capabilities_met=(),
                capabilities_missing=required,
                falsification_detected=True,
            )

        met = [c for c in required if c in system.capabilities]
        missing = [c for c in required if c not in system.capabilities]

        # Operational check: if transitions fail to execute or produce invalid trace
        operational_ok = True
        try:
            if system.states and system.operations:
                s0 = system.states[0]
                op0 = system.operations[0]
                _ = system.step(s0, op0)
                _ = system.observe(s0)
        except Exception as exc:
            operational_ok = False

        if not operational_ok:
            return CriterionResult(
                criterion_id=cid,
                verdict=Verdict.FAILED,
                score=Fraction(0, 1),
                details="Failed: Candidate runtime raised unexpected exception during step/observe.",
                capabilities_met=tuple(met),
                capabilities_missing=tuple(missing),
                falsification_detected=True,
            )

        fraction = Fraction(len(met), len(required)) if required else Fraction(1, 1)

        if fraction == Fraction(1, 1):
            verdict = Verdict.SATISFIED
            details = f"Satisfied: All {len(required)} required capabilities present."
        elif fraction > Fraction(0, 1):
            verdict = Verdict.PARTIALLY_SATISFIED
            details = f"Partially Satisfied: {len(met)}/{len(required)} capabilities present."
        else:
            verdict = Verdict.FAILED
            details = f"Failed: None of the {len(required)} required capabilities present."

        return CriterionResult(
            criterion_id=cid,
            verdict=verdict,
            score=fraction,
            details=details,
            capabilities_met=tuple(met),
            capabilities_missing=tuple(missing),
            falsification_detected=False,
        )
