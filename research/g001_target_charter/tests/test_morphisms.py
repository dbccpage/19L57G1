"""Tests for Comparison Morphisms between Candidate Target Systems."""

from __future__ import annotations

import pytest

from adequacy import (
    AdequacyEngine,
    CriterionResult,
    EvaluationReport,
    TargetSystem,
    Verdict,
)
from charter import CriterionID, TargetClassCharter
from morphism import (
    ComparisonMorphism,
    MorphismCompositionError,
    compose_morphisms,
    identity_morphism,
    transfer_adequacy,
    verify_category_laws,
)


def create_target_system(name: str, offset: int = 0) -> TargetSystem:
    """Helper to create distinct test target systems."""
    return TargetSystem(
        name=name,
        states=[offset + 0, offset + 1, offset + 2],
        operations=["step_op"],
        step=lambda s, op: s + 1 if s < offset + 2 else None,
        observe=lambda s: f"view_{s}",
        capabilities={
            "discrete_state_transition",
            "fuel_or_step_accounting",
            "termination_or_progress_detection",
        },
        description=f"System {name} with offset {offset}",
    )


def test_identity_morphism_properties() -> None:
    sys = create_target_system("SystemA", offset=0)
    id_m = identity_morphism(sys)

    assert id_m.source == sys
    assert id_m.target == sys
    assert id_m.distortion == 0.0
    assert len(id_m.preserves_criteria) == len(CriterionID)

    for s in sys.states:
        assert id_m.map_state(s) == s
        assert id_m.map_obs(sys.observe(s)) == sys.observe(s)

    assert id_m.check_observation_commutativity(sys.states) is True
    ok, passed, checked = id_m.check_step_simulation(sys.states, sys.operations)
    assert ok is True
    assert passed == checked


def test_morphism_composition_and_distortion() -> None:
    sys_a = create_target_system("SystemA", offset=0)
    sys_b = create_target_system("SystemB", offset=10)
    sys_c = create_target_system("SystemC", offset=100)

    # m1: A -> B maps state s -> s + 10, obs "view_s" -> "view_{s+10}"
    m1 = ComparisonMorphism(
        name="m_AB",
        source=sys_a,
        target=sys_b,
        map_state=lambda s: s + 10,
        map_op=lambda op: op,
        map_obs=lambda o: f"view_{int(o.split('_')[1]) + 10}",
        distortion=0.25,
        preserves_criteria={CriterionID.COMPUTATIONAL, CriterionID.REPRESENTATIONAL},
    )

    # m2: B -> C maps state s -> s + 90, obs "view_s" -> "view_{s+90}"
    m2 = ComparisonMorphism(
        name="m_BC",
        source=sys_b,
        target=sys_c,
        map_state=lambda s: s + 90,
        map_op=lambda op: op,
        map_obs=lambda o: f"view_{int(o.split('_')[1]) + 90}",
        distortion=0.50,
        preserves_criteria={CriterionID.COMPUTATIONAL, CriterionID.EMPIRICAL},
    )

    m_comp = compose_morphisms(m1, m2)

    assert m_comp.source == sys_a
    assert m_comp.target == sys_c
    assert m_comp.distortion == pytest.approx(0.75)
    # Preserved criteria is the intersection
    assert m_comp.preserves_criteria == {CriterionID.COMPUTATIONAL}

    # State map checks
    assert m_comp.map_state(1) == 101
    assert m_comp.map_obs("view_1") == "view_101"

    # Simulation check
    ok, passed, checked = m_comp.check_step_simulation(sys_a.states, sys_a.operations)
    assert ok is True
    assert m_comp.check_observation_commutativity(sys_a.states) is True


def test_incompatible_composition_fails() -> None:
    sys_a = create_target_system("SystemA", offset=0)
    sys_b = create_target_system("SystemB", offset=10)
    sys_d = create_target_system("SystemD", offset=50)

    m1 = ComparisonMorphism("m_AB", sys_a, sys_b, lambda s: s, lambda op: op, lambda o: o)
    m2 = ComparisonMorphism("m_DA", sys_d, sys_a, lambda s: s, lambda op: op, lambda o: o)

    # m1.target is SystemB, m2.source is SystemD != SystemB
    with pytest.raises(MorphismCompositionError):
        _ = compose_morphisms(m1, m2)


def test_category_laws_and_associativity() -> None:
    sys_a = create_target_system("SystemA", offset=0)
    sys_b = create_target_system("SystemB", offset=10)
    sys_c = create_target_system("SystemC", offset=100)
    sys_d = create_target_system("SystemD", offset=1000)

    m_ab = ComparisonMorphism(
        "m_AB", sys_a, sys_b,
        map_state=lambda s: s + 10,
        map_op=lambda op: op,
        map_obs=lambda o: f"view_{int(o.split('_')[1]) + 10}",
        distortion=0.1,
    )
    m_bc = ComparisonMorphism(
        "m_BC", sys_b, sys_c,
        map_state=lambda s: s + 90,
        map_op=lambda op: op,
        map_obs=lambda o: f"view_{int(o.split('_')[1]) + 90}",
        distortion=0.2,
    )
    m_cd = ComparisonMorphism(
        "m_CD", sys_c, sys_d,
        map_state=lambda s: s + 900,
        map_op=lambda op: op,
        map_obs=lambda o: f"view_{int(o.split('_')[1]) + 900}",
        distortion=0.3,
    )

    test_states = [0, 1, 2]
    test_ops = ["step_op"]
    test_obs = ["view_0", "view_1", "view_2"]

    verdicts = verify_category_laws(m_ab, m_bc, m_cd, test_states, test_ops, test_obs)
    assert verdicts["left_identity"] is True
    assert verdicts["right_identity"] is True
    assert verdicts["associativity"] is True
    assert verdicts["distortion_triangle_bound"] is True


def test_step_simulation_falsification_detected() -> None:
    sys_a = create_target_system("SystemA", offset=0)
    sys_b = create_target_system("SystemB", offset=10)

    # Inconsistent mapping: maps state s -> s + 10, but step in target doesn't match
    m_bad = ComparisonMorphism(
        "m_bad", sys_a, sys_b,
        map_state=lambda s: s + 5,  # Bad offset: lands outside expected state alignment
        map_op=lambda op: op,
        map_obs=lambda o: o,
    )

    ok, passed, checked = m_bad.check_step_simulation(sys_a.states, sys_a.operations)
    assert ok is False
    assert passed < checked


def test_transfer_adequacy_along_morphism() -> None:
    charter = TargetClassCharter()
    charter.freeze()
    engine = AdequacyEngine(charter)

    # System A with computational capability
    sys_a = TargetSystem(
        name="SystemA",
        states=[0, 1],
        operations=["step"],
        step=lambda s, op: 1 if s == 0 else None,
        observe=lambda s: s,
        capabilities=set(charter.get_criterion(CriterionID.COMPUTATIONAL).required_capabilities),
    )
    sys_b = create_target_system("SystemB")

    report_a = engine.evaluate(sys_a)
    assert report_a.results[CriterionID.COMPUTATIONAL].verdict == Verdict.SATISFIED

    # Morphism preserving computational adequacy
    m_preserving = ComparisonMorphism(
        "m_pres", sys_a, sys_b,
        lambda s: s, lambda op: op, lambda o: o,
        preserves_criteria={CriterionID.COMPUTATIONAL},
    )
    transferred = transfer_adequacy(report_a, m_preserving)
    assert transferred[CriterionID.COMPUTATIONAL.value] == "PRESERVED_SATISFIED"

    # Morphism not preserving computational adequacy
    m_not_preserving = ComparisonMorphism(
        "m_unpres", sys_a, sys_b,
        lambda s: s, lambda op: op, lambda o: o,
        preserves_criteria=set(),
    )
    transferred_unpres = transfer_adequacy(report_a, m_not_preserving)
    assert transferred_unpres[CriterionID.COMPUTATIONAL.value] == "UNPRESERVED_OR_DILUTED"
