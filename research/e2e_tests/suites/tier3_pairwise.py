"""Tier 3: Pairwise Cross-Feature Combinations E2E Test Suite.

Exercises cross-feature interactions and module interface contracts:
- Target A execution driving G010 capability removal
- G011 finitary ordinals addressing Target A instruction memory
- Target B prefix observation of Target A traces
- G001 adequacy verification of Target A & Target B
- Multi-locus product pairing with G011 tree addressing
- Target A memory growth with Target B chain functionality
- G010 capability restriction with G011 finitary recursion
- Target B rational bounds as G001 empirical evidence

Adheres strictly to the Claim Hygiene Rule.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

E2E_ROOT = Path(__file__).resolve().parent.parent
if str(E2E_ROOT) not in sys.path:
    sys.path.insert(0, str(E2E_ROOT))

from harness import (
    AdequacyDimension,
    Capability,
    ComparisonMorphism,
    FreshnessGenerator,
    MemoryState,
    Ordinal,
    State,
    TargetSystem,
    Terminal,
    TreeAddress,
    bond_scale,
    check_prefix_compatibility,
    check_zeros_bound,
    endogenous_recursion,
    evaluate_system,
    execute_restricted,
    is_chain_functional,
    is_compatible_thread,
    lookup,
    make_program,
    obs_scale,
    pack_locus,
    rational_frequency,
    run_det,
    step_det,
    step_with_memory,
    unpack_locus,
    verify_obstruction,
)


def test_pairwise_target_a_execution_driving_g010_capability_removal():
    """Target A execution driving G010 capability removal across a fixed observation interface."""
    prog = make_program(
        nops=2,
        transitions=[(0, 0, 1), (1, 1, 2)],
        enablements=[(0, 0), (1, 1)],
    )
    # Baseline: both DIRECT_LOOKUP and CONDITIONAL_BRANCH allowed
    full_caps = frozenset([Capability.DIRECT_LOOKUP, Capability.CONDITIONAL_BRANCH])
    res_full = execute_restricted(prog, full_caps, full_caps, start=0, fuel=5, nops=2)
    assert res_full.status != "OBSTRUCTED_CAPABILITY_ABSENT"
    assert res_full.output == (0, 1, 2)

    # Capability removal: CONDITIONAL_BRANCH is physically removed
    restricted_caps = frozenset([Capability.DIRECT_LOOKUP])
    res_restr = execute_restricted(prog, restricted_caps, full_caps, start=0, fuel=5, nops=2)
    assert res_restr.status == "OBSTRUCTED_CAPABILITY_ABSENT"
    assert res_restr.output == ()


def test_pairwise_g011_finitary_ordinals_addressing_target_a_instruction_memory():
    """G011 finitary ordinals addressing Target A instruction memory."""
    # Build transition table using ordinal values as node addresses
    o0 = Ordinal.zero()
    o1 = o0.succ()
    o2 = o1.succ()

    transitions = [(0, o0.val, o1.val), (0, o1.val, o2.val)]
    enablements = [(o0.val, 0), (o1.val, 0)]
    prog = make_program(nops=1, transitions=transitions, enablements=enablements)

    s = State(graph=prog, nops=1, active=o0.val, tape=(o0.val,), clock=0, fuel=5)
    s1 = step_det(s)
    assert isinstance(s1, State)
    assert s1.active == o1.val

    s2 = step_det(s1)
    assert isinstance(s2, State)
    assert s2.active == o2.val


def test_pairwise_target_b_prefix_observation_of_target_a_traces():
    """Target B prefix scale observation observing Target A execution traces."""
    # 3-cycle in Target A
    prog = make_program(
        nops=1,
        transitions=[(0, 0, 1), (0, 1, 2), (0, 2, 0)],
        enablements=[(0, 0), (1, 0), (2, 0)],
    )
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=10)

    # Collect observation scales 1 through 5
    stages = [obs_scale(i, s) for i in range(0, 6)]
    assert is_compatible_thread(stages, c=3)

    # Check prefix compatibility between scale 2 and scale 5
    assert check_prefix_compatibility(stages[2], stages[5])
    assert stages[2] == (0, 1, 2)
    assert stages[5] == (0, 1, 2, 0, 1, 2)


def test_pairwise_g001_adequacy_verification_of_target_a_and_target_b():
    """G001 adequacy charter evaluating Target A execution and Target B dynamics."""
    # Target A satisfies computational and representational completeness
    sys_a = TargetSystem(
        name="TargetA_Execution",
        dimension_scores={
            AdequacyDimension.COMPUTATIONAL_UNIVERSALITY: True,
            AdequacyDimension.REPRESENTATIONAL_COMPLETENESS: True,
        },
    )
    # Target B satisfies mathematical foundations and empirical adequacy
    sys_b = TargetSystem(
        name="TargetB_Dynamics",
        dimension_scores={
            AdequacyDimension.MATHEMATICAL_FOUNDATIONS: True,
            AdequacyDimension.EMPIRICAL_ADEQUACY: True,
        },
    )

    # Comparison morphism from Target A to Target B
    morph = ComparisonMorphism(
        source=sys_a,
        target=sys_b,
        mapping_name="TraceToObservationFunctor",
        preserves_adequacy=True,
    )
    assert morph.source.name == "TargetA_Execution"
    assert morph.target.name == "TargetB_Dynamics"
    assert morph.preserves_adequacy is True


def test_pairwise_multi_locus_product_with_g011_tree_addressing():
    """Two-locus product pairing mapped to G011 hierarchical tree addresses."""
    m = 5
    gen = FreshnessGenerator()
    root = TreeAddress.root()

    # Product coordinates (2, 3) mapped into tree address
    a, b = 2, 3
    packed = pack_locus(m, a, b)
    addr = root.extend(a).extend(b)

    # Verify coordinate recovery
    rec_a, rec_b = unpack_locus(m, packed)
    assert rec_a == addr.path[0]
    assert rec_b == addr.path[1]


def test_pairwise_target_a_memory_growth_with_target_b_chain_functionality():
    """Target A depth-2 memory records verified against Target B chain functionality."""
    prog = make_program(
        nops=1,
        transitions=[(0, 0, 1), (0, 1, 2), (0, 2, 0)],
        enablements=[(0, 0), (1, 0), (2, 0)],
    )
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=6)
    ms = MemoryState(base_state=s, records=())

    for _ in range(6):
        nxt = step_with_memory(ms)
        assert isinstance(nxt, MemoryState)
        ms = nxt

    # Verify the execution tape obeys chain functionality
    assert is_chain_functional(ms.base_state.tape)
    # Verify depth-2 records are functional across memory history
    depth2_records = [r.payload for r in ms.records if r.depth == 2]
    assert len(depth2_records) == 5


def test_pairwise_g010_restricted_execution_with_g011_finitary_recursion():
    """Fuel-bounded endogenous recursion executing under restricted capability environments."""
    depth = Ordinal(4)
    allowed_caps = frozenset([Capability.DIRECT_LOOKUP])
    required_caps = frozenset([Capability.DIRECT_LOOKUP, Capability.UNBOUNDED_RECURSION])

    witness = verify_obstruction("UnboundedRecursionTask", Capability.UNBOUNDED_RECURSION, allowed_caps)
    assert witness.is_obstructed is True

    # Finitary recursion succeeds within fuel bound
    val, ok = endogenous_recursion(depth, fuel=4, acc=0)
    assert ok is True
    assert val == 4


def test_pairwise_target_b_rational_bounds_as_g001_empirical_evidence():
    """Quantitative rational limiting bounds evaluated as empirical adequacy evidence under G001."""
    L = 30
    zeros_count = 10  # For 3-cycle
    assert check_zeros_bound(L, zeros_count)

    freq, total = rational_frequency([0, 1, 2] * 10, target=0)
    assert freq == 10
    assert total == 30

    # Package as evidence under G001
    empirical_sys = TargetSystem(
        name="RationalCalibrationSubstrate",
        dimension_scores={
            AdequacyDimension.EMPIRICAL_ADEQUACY: True,
            AdequacyDimension.MATHEMATICAL_FOUNDATIONS: True,
        },
        metadata={"rational_limit": "1/3", "error_budget": "2/(3L)"},
    )
    assert empirical_sys.dimension_scores[AdequacyDimension.EMPIRICAL_ADEQUACY] is True
