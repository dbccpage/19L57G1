"""Comparison morphisms connecting distinct candidate target systems.

Formalizes comparison morphisms as functors between target systems with:
- State mapping, operation mapping, observation mapping
- Preservation of adequacy properties
- Identity morphisms and associative composition
- Bounded distortion metrics

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Sequence, Set

from adequacy import CriterionResult, EvaluationReport, TargetSystem, Verdict
from charter import CriterionID


class MorphismCompositionError(Exception):
    """Raised when incompatible morphisms are composed."""


@dataclass
class ComparisonMorphism:
    """Functorial morphism between two candidate target systems."""
    name: str
    source: TargetSystem
    target: TargetSystem
    map_state: Callable[[Any], Any]
    map_op: Callable[[Any], Any]
    map_obs: Callable[[Any], Any]
    distortion: float = 0.0
    preserves_criteria: Set[CriterionID] = field(default_factory=set)

    def check_observation_commutativity(self, sample_states: Sequence[Any]) -> bool:
        """Checks if target.observe(map_state(s)) == map_obs(source.observe(s))."""
        for s in sample_states:
            lhs = self.target.observe(self.map_state(s))
            rhs = self.map_obs(self.source.observe(s))
            if lhs != rhs:
                return False
        return True

    def check_step_simulation(self, sample_states: Sequence[Any], sample_ops: Sequence[Any]) -> tuple[bool, int, int]:
        """Checks if step transitions in source simulate validly in target."""
        checked = 0
        passed = 0
        for s in sample_states:
            for op in sample_ops:
                checked += 1
                s_next = self.source.step(s, op)
                if s_next is None:
                    # If source refuses/halts, target should halt or be consistent
                    t_next = self.target.step(self.map_state(s), self.map_op(op))
                    if t_next is None:
                        passed += 1
                else:
                    t_expected = self.map_state(s_next)
                    t_actual = self.target.step(self.map_state(s), self.map_op(op))
                    if t_actual == t_expected:
                        passed += 1
        return (passed == checked, passed, checked)

    def check_faithful_observation(self, sample_obs: Sequence[Any]) -> bool:
        """Checks injectivity of observation mapping on distinct samples."""
        seen = {}
        for o in sample_obs:
            mapped = self.map_obs(o)
            if mapped in seen and seen[mapped] != o:
                return False
            seen[mapped] = o
        return True


def identity_morphism(system: TargetSystem) -> ComparisonMorphism:
    """Constructs the identity comparison morphism for a target system."""
    all_criteria = set(CriterionID)
    return ComparisonMorphism(
        name=f"id_{system.name}",
        source=system,
        target=system,
        map_state=lambda s: s,
        map_op=lambda op: op,
        map_obs=lambda obs: obs,
        distortion=0.0,
        preserves_criteria=all_criteria,
    )


def compose_morphisms(m1: ComparisonMorphism, m2: ComparisonMorphism) -> ComparisonMorphism:
    """Composes two morphisms: (m2 . m1) : m1.source -> m2.target."""
    if m1.target.name != m2.source.name:
        raise MorphismCompositionError(
            f"Cannot compose morphisms: target of m1 ({m1.target.name}) "
            f"does not match source of m2 ({m2.source.name})."
        )

    return ComparisonMorphism(
        name=f"({m2.name}_o_{m1.name})",
        source=m1.source,
        target=m2.target,
        map_state=lambda s: m2.map_state(m1.map_state(s)),
        map_op=lambda op: m2.map_op(m1.map_op(op)),
        map_obs=lambda obs: m2.map_obs(m1.map_obs(obs)),
        distortion=round(m1.distortion + m2.distortion, 10),
        preserves_criteria=m1.preserves_criteria.intersection(m2.preserves_criteria),
    )


def verify_category_laws(
    m_ab: ComparisonMorphism,
    m_bc: ComparisonMorphism,
    m_cd: ComparisonMorphism,
    test_states: Sequence[Any],
    test_ops: Sequence[Any],
    test_obs: Sequence[Any],
) -> dict[str, bool]:
    """Verifies categorical identity and associativity laws on test inputs."""
    id_a = identity_morphism(m_ab.source)
    id_b = identity_morphism(m_ab.target)

    # 1. Left identity: id_B . m_ab == m_ab
    comp_left = compose_morphisms(m_ab, id_b)
    left_id_ok = all(comp_left.map_state(s) == m_ab.map_state(s) for s in test_states) and \
                 all(comp_left.map_op(op) == m_ab.map_op(op) for op in test_ops) and \
                 all(comp_left.map_obs(o) == m_ab.map_obs(o) for o in test_obs)

    # 2. Right identity: m_ab . id_A == m_ab
    comp_right = compose_morphisms(id_a, m_ab)
    right_id_ok = all(comp_right.map_state(s) == m_ab.map_state(s) for s in test_states) and \
                  all(comp_right.map_op(op) == m_ab.map_op(op) for op in test_ops) and \
                  all(comp_right.map_obs(o) == m_ab.map_obs(o) for o in test_obs)

    # 3. Associativity: (m_cd . m_bc) . m_ab == m_cd . (m_bc . m_ab)
    comp_bc_ab = compose_morphisms(m_ab, m_bc)
    assoc_left = compose_morphisms(comp_bc_ab, m_cd)

    comp_cd_bc = compose_morphisms(m_bc, m_cd)
    assoc_right = compose_morphisms(m_ab, comp_cd_bc)

    assoc_ok = all(assoc_left.map_state(s) == assoc_right.map_state(s) for s in test_states) and \
               all(assoc_left.map_op(op) == assoc_right.map_op(op) for op in test_ops) and \
               all(assoc_left.map_obs(o) == assoc_right.map_obs(o) for o in test_obs)

    # 4. Distortion triangle inequality
    triangle_ok = (comp_bc_ab.distortion <= m_ab.distortion + m_bc.distortion + 1e-9)

    return {
        "left_identity": left_id_ok,
        "right_identity": right_id_ok,
        "associativity": assoc_ok,
        "distortion_triangle_bound": triangle_ok,
    }


def transfer_adequacy(report: EvaluationReport, morphism: ComparisonMorphism) -> dict[str, Any]:
    """Transfers evaluated adequacy criteria from source system across a comparison morphism."""
    transferred: dict[str, str] = {}
    for cid, result in report.results.items():
        if result.verdict == Verdict.SATISFIED:
            if cid in morphism.preserves_criteria:
                transferred[cid.value] = "PRESERVED_SATISFIED"
            else:
                transferred[cid.value] = "UNPRESERVED_OR_DILUTED"
        else:
            transferred[cid.value] = result.verdict.value
    return transferred
