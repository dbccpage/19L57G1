"""Tests for G001 Target-Class Charter and Adequacy Evaluation Engine."""

from __future__ import annotations

import pytest

from charter import (
    AdequacyCriterion,
    CharterFreezeError,
    CriterionID,
    TargetClassCharter,
    default_criteria,
)
from adequacy import (
    AdequacyEngine,
    CriterionResult,
    EvaluationReport,
    TargetSystem,
    Verdict,
)


def make_mock_system(
    name: str = "MockSystem",
    capabilities: set[str] | None = None,
    is_circular: bool = False,
    has_oracle: bool = False,
    failing_step: bool = False,
) -> TargetSystem:
    """Helper creating a test TargetSystem."""
    if capabilities is None:
        capabilities = set()

    def step_fn(s: int, op: str) -> int | None:
        if failing_step:
            raise RuntimeError("Intentional operational failure")
        if op == "inc":
            return s + 1
        if op == "halt":
            return None
        return s

    return TargetSystem(
        name=name,
        states=[0, 1, 2, 3],
        operations=["inc", "halt"],
        step=step_fn,
        observe=lambda s: f"obs_{s}",
        capabilities=capabilities,
        is_circular_definition=is_circular,
        has_unencoded_oracle=has_oracle,
        description="Test target system instance",
    )


def all_capabilities_set() -> set[str]:
    """Returns the union of all required capabilities across the 9 criteria."""
    crit_dict = default_criteria()
    caps = set()
    for c in crit_dict.values():
        caps.update(c.required_capabilities)
    return caps


def test_default_criteria_count_and_keys() -> None:
    charter = TargetClassCharter()
    assert len(charter.criteria) == 9
    for cid in CriterionID:
        assert cid in charter.criteria
        crit = charter.get_criterion(cid)
        assert len(crit.required_capabilities) > 0
        assert len(crit.falsification_conditions) > 0


def test_freeze_sets_status_and_hash() -> None:
    charter = TargetClassCharter()
    assert not charter.is_frozen
    assert charter.freeze_hash is None

    h = charter.freeze()
    assert charter.is_frozen
    assert charter.status == TargetClassCharter.FROZEN_STATUS
    assert charter.freeze_hash == h
    assert len(h) == 64  # sha256 hex string


def test_modification_on_frozen_charter_fails() -> None:
    charter = TargetClassCharter()
    charter.freeze()

    new_crit = AdequacyCriterion(
        criterion_id=CriterionID.COMPUTATIONAL,
        name="Mutated",
        dimension="Computational",
        description="Mutated description",
        required_capabilities=("fake",),
        falsification_conditions=("fake",),
    )

    with pytest.raises(CharterFreezeError):
        charter.modify_criterion(new_crit)

    with pytest.raises(CharterFreezeError):
        charter.add_criterion(new_crit)

    with pytest.raises(CharterFreezeError):
        charter.remove_criterion(CriterionID.COMPUTATIONAL)


def test_unfrozen_evaluation_rejected() -> None:
    charter = TargetClassCharter()
    assert not charter.is_frozen
    with pytest.raises(ValueError, match="requires a frozen charter"):
        _ = AdequacyEngine(charter)


def test_evaluation_against_circular_system_refused() -> None:
    charter = TargetClassCharter()
    charter.freeze()
    engine = AdequacyEngine(charter)

    system = make_mock_system("CircularSys", capabilities=all_capabilities_set(), is_circular=True)
    report = engine.evaluate(system)

    assert report.overall_verdict == Verdict.REFUSED
    assert report.satisfied_count == 0
    assert report.non_retrospective is True
    for cid, res in report.results.items():
        assert res.verdict == Verdict.REFUSED
        assert res.falsification_detected is True


def test_evaluation_against_unencoded_oracle_refused() -> None:
    charter = TargetClassCharter()
    charter.freeze()
    engine = AdequacyEngine(charter)

    system = make_mock_system("OracleSys", capabilities=all_capabilities_set(), has_oracle=True)
    report = engine.evaluate(system)

    assert report.overall_verdict == Verdict.REFUSED
    assert report.results[CriterionID.COMPUTATIONAL].verdict == Verdict.REFUSED
    assert report.results[CriterionID.REPRESENTATIONAL].verdict == Verdict.REFUSED


def test_fully_adequate_candidate_system() -> None:
    charter = TargetClassCharter()
    charter.freeze()
    engine = AdequacyEngine(charter)

    system = make_mock_system("AdequateSys", capabilities=all_capabilities_set())
    report = engine.evaluate(system)

    assert report.overall_verdict == Verdict.SATISFIED
    assert report.satisfied_count == 9
    assert report.total_criteria == 9
    assert report.non_retrospective is True
    for res in report.results.values():
        assert res.verdict == Verdict.SATISFIED
        assert res.score == 1.0


def test_partially_adequate_candidate_system() -> None:
    charter = TargetClassCharter()
    charter.freeze()
    engine = AdequacyEngine(charter)

    # Only provide capabilities for computational capacity
    comp_caps = set(charter.get_criterion(CriterionID.COMPUTATIONAL).required_capabilities)
    system = make_mock_system("PartialSys", capabilities=comp_caps)
    report = engine.evaluate(system)

    assert report.overall_verdict == Verdict.PARTIALLY_SATISFIED
    assert report.satisfied_count == 1
    assert report.results[CriterionID.COMPUTATIONAL].verdict == Verdict.SATISFIED
    assert report.results[CriterionID.REASONING].verdict == Verdict.FAILED


def test_runtime_crash_in_step_handled() -> None:
    charter = TargetClassCharter()
    charter.freeze()
    engine = AdequacyEngine(charter)

    system = make_mock_system("CrashingSys", capabilities=all_capabilities_set(), failing_step=True)
    report = engine.evaluate(system)

    # Crashing step should mark operational test as failed
    assert report.overall_verdict in (Verdict.FAILED, Verdict.PARTIALLY_SATISFIED)
    for res in report.results.values():
        assert res.verdict == Verdict.FAILED
        assert res.falsification_detected is True


def test_hash_reproducibility_and_sensitivity() -> None:
    c1 = TargetClassCharter()
    c2 = TargetClassCharter()
    h1 = c1.compute_hash()
    h2 = c2.compute_hash()
    assert h1 == h2

    # Mutating an unfrozen charter changes the hash
    modified_crit = AdequacyCriterion(
        criterion_id=CriterionID.COMPUTATIONAL,
        name="Modified Computational",
        dimension="Computational",
        description="Modified text",
        required_capabilities=("custom_cap",),
        falsification_conditions=("custom_falsifier",),
    )
    c1.modify_criterion(modified_crit)
    assert c1.compute_hash() != h2
