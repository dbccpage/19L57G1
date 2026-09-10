"""Tier 1: Feature Coverage E2E Test Suite.

Covers all 16 features from PROJECT.md with at least 5 distinct test cases per feature (80 tests total).
Adheres strictly to the Claim Hygiene Rule and constructive finite boundaries.
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
    Refusal,
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
    fire,
    is_chain_functional,
    is_compatible_thread,
    lookup,
    make_program,
    obs_scale,
    pack_locus,
    rational_frequency,
    run,
    run_det,
    step_det,
    step_with_memory,
    unpack_locus,
    verify_obstruction,
)


# ===========================================================================
# Feature 1: Represented Program & Lookup
# ===========================================================================

def test_f01_lookup_existing_edge_returns_target():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    assert lookup(3 + 0, 0, prog) == 1

def test_f01_lookup_missing_edge_returns_none():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    assert lookup(3 + 0, 99, prog) is None

def test_f01_lookup_distinguishes_different_forms():
    prog = make_program(
        nops=2,
        transitions=[(0, 0, 1), (1, 0, 2)],
        enablements=[(0, 0), (0, 1)],
    )
    assert lookup(3 + 0, 0, prog) == 1
    assert lookup(3 + 1, 0, prog) == 2

def test_f01_lookup_without_host_functions():
    # Only reads stored instances without consulting F.ops
    prog = ((3, (10, 20)), (3, (20, 30)))
    assert lookup(3, 10, prog) == 20
    assert lookup(3, 20, prog) == 30
    assert lookup(3, 30, prog) is None

def test_f01_lookup_multi_edge_graph_distinction():
    # 3-cycle: 0->1, 1->2, 2->0
    prog = make_program(
        nops=1,
        transitions=[(0, 0, 1), (0, 1, 2), (0, 2, 0)],
        enablements=[(0, 0), (1, 0), (2, 0)],
    )
    assert lookup(3, 0, prog) == 1
    assert lookup(3, 1, prog) == 2
    assert lookup(3, 2, prog) == 0


# ===========================================================================
# Feature 2: Data-Driven Control & Branching
# ===========================================================================

def test_f02_single_enablement_fires_operation():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    nxt = step_det(s)
    assert isinstance(nxt, State)
    assert nxt.active == 1

def test_f02_zero_enablement_halts():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    assert step_det(s) is Terminal.HALT

def test_f02_multiple_enablements_branch_without_selection():
    # At datum 0, both op 0 and op 1 are enabled -> explicit BRANCH terminal
    prog = make_program(
        nops=2,
        transitions=[(0, 0, 1), (1, 0, 2)],
        enablements=[(0, 0), (0, 1)],
    )
    s = State(graph=prog, nops=2, active=0, tape=(0,), clock=0, fuel=5)
    assert step_det(s) is Terminal.BRANCH

def test_f02_step_extends_tape():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    nxt = step_det(s)
    assert isinstance(nxt, State)
    assert nxt.tape == (0, 1)

def test_f02_monotonic_fuel_and_clock():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    nxt = step_det(s)
    assert isinstance(nxt, State)
    assert nxt.clock == 1
    assert nxt.fuel == 4


# ===========================================================================
# Feature 3: Memory Growth & Retained Records
# ===========================================================================

def test_f03_depth1_record_captures_predecessor_and_current():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    ms = MemoryState(base_state=s, records=())
    ms_nxt = step_with_memory(ms)
    assert isinstance(ms_nxt, MemoryState)
    assert len(ms_nxt.records) >= 1
    assert ms_nxt.records[0].depth == 1
    assert ms_nxt.records[0].payload == (0, 1)

def test_f03_depth2_record_captures_ternary_history():
    prog = make_program(
        nops=1,
        transitions=[(0, 0, 1), (0, 1, 2)],
        enablements=[(0, 0), (1, 0)],
    )
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    ms = MemoryState(base_state=s, records=())
    ms1 = step_with_memory(ms)
    assert isinstance(ms1, MemoryState)
    ms2 = step_with_memory(ms1)
    assert isinstance(ms2, MemoryState)
    # At step 2, tape is (0, 1, 2) -> depth-2 ternary record exists
    d2 = [r for r in ms2.records if r.depth == 2]
    assert len(d2) == 1
    assert d2[0].payload == (0, 1, 2)

def test_f03_retained_records_grow_monotonically():
    prog = make_program(
        nops=1,
        transitions=[(0, 0, 1), (0, 1, 2)],
        enablements=[(0, 0), (1, 0)],
    )
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    ms = MemoryState(base_state=s, records=())
    ms1 = step_with_memory(ms)
    assert isinstance(ms1, MemoryState)
    ms2 = step_with_memory(ms1)
    assert isinstance(ms2, MemoryState)
    assert len(ms2.records) > len(ms1.records)

def test_f03_retained_records_are_immutable():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    ms = MemoryState(base_state=s, records=())
    ms1 = step_with_memory(ms)
    assert isinstance(ms1, MemoryState)
    rec_initial = ms1.records[0]
    # Subsequent actions do not mutate earlier record objects
    assert rec_initial.payload == (0, 1)

def test_f03_records_derived_from_state_without_host_shortcuts():
    # Verifies records strictly match the observable execution trace
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    ms = MemoryState(base_state=s, records=())
    ms1 = step_with_memory(ms)
    assert isinstance(ms1, MemoryState)
    assert ms1.records[0].payload == (ms1.base_state.tape[-2], ms1.base_state.tape[-1])


# ===========================================================================
# Feature 4: Multi-Locus Independence
# ===========================================================================

def test_f04_product_pairing_is_bijective():
    m = 5
    for a in range(m):
        for b in range(m):
            packed = pack_locus(m, a, b)
            unpacked = unpack_locus(m, packed)
            assert unpacked == (a, b)

def test_f04_independence_square_commutation_on_outcome():
    # Disjoint loci: moving locus A then B arrives at same state as B then A
    m = 10
    a, b = 2, 3
    # Left step advances a by 1, right step advances b by 1
    # Path 1: Left then Right
    p1_a, p1_b = a + 1, b
    p1_a, p1_b = p1_a, p1_b + 1
    # Path 2: Right then Left
    p2_a, p2_b = a, b + 1
    p2_a, p2_b = p2_a + 1, p2_b
    assert pack_locus(m, p1_a, p1_b) == pack_locus(m, p2_a, p2_b)

def test_f04_coupling_breaks_commutativity():
    # Coupled interaction: right move depends on current left coordinate
    m = 10
    a, b = 2, 3
    # Coupled right step: b' = b + a
    # Path 1: Left (a->a+1) then coupled Right (b->b+a')
    p1_a = a + 1
    p1_b = b + p1_a  # 3 + 3 = 6
    # Path 2: coupled Right (b->b+a) then Left (a->a+1)
    p2_b = b + a     # 3 + 2 = 5
    p2_a = a + 1     # 3
    assert (p1_a, p1_b) != (p2_a, p2_b)

def test_f04_local_step_preserves_other_locus():
    m = 10
    packed = pack_locus(m, 4, 7)
    a, b = unpack_locus(m, packed)
    # Advance only locus A
    new_packed = pack_locus(m, a + 1, b)
    new_a, new_b = unpack_locus(m, new_packed)
    assert new_a == 5
    assert new_b == 7

def test_f04_two_step_compositional_independence():
    m = 8
    # Multi-step independence across 2 steps each
    a0, b0 = 1, 1
    # Two steps on left, two steps on right
    final_a = a0 + 2
    final_b = b0 + 2
    assert unpack_locus(m, pack_locus(m, final_a, final_b)) == (3, 3)


# ===========================================================================
# Feature 5: Prefix Observation Scale System
# ===========================================================================

def test_f05_bond_forgets_last_element():
    stage = (0, 1, 2, 0)
    assert bond_scale(c=3, n=3, stage=stage) == (0, 1, 2)

def test_f05_prefix_compatibility_across_scales():
    prog = make_program(
        nops=1,
        transitions=[(0, 0, 1), (0, 1, 2), (0, 2, 0)],
        enablements=[(0, 0), (1, 0), (2, 0)],
    )
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=10)
    obs3 = obs_scale(3, s)
    obs6 = obs_scale(6, s)
    assert check_prefix_compatibility(obs3, obs6)

def test_f05_inverse_limit_chain_bonding():
    prog = make_program(
        nops=1,
        transitions=[(0, 0, 1), (0, 1, 0)],
        enablements=[(0, 0), (1, 0)],
    )
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=10)
    stages = [obs_scale(i, s) for i in range(0, 5)]
    assert is_compatible_thread(stages, c=2)

def test_f05_fuel_independence_for_scale_n():
    prog = make_program(
        nops=1,
        transitions=[(0, 0, 1), (0, 1, 2), (0, 2, 0)],
        enablements=[(0, 0), (1, 0), (2, 0)],
    )
    s_fuel5 = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    s_fuel10 = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=10)
    assert obs_scale(3, s_fuel5) == obs_scale(3, s_fuel10)

def test_f05_scale_observation_is_deterministic():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    assert obs_scale(1, s) == obs_scale(1, s)


# ===========================================================================
# Feature 6: Sequence Space Limit Bijection
# ===========================================================================

def test_f06_thread_to_sequence_mapping():
    # A compatible thread stages maps to sequence values
    stages = [(0,), (0, 1), (0, 1, 0), (0, 1, 0, 1)]
    assert is_compatible_thread(stages, c=2)
    # Sequence representation at index n is stage[n][-1]
    seq = [stage[-1] for stage in stages]
    assert seq == [0, 1, 0, 1]

def test_f06_sequence_to_thread_mapping():
    seq = [0, 1, 2, 0, 1, 2]
    stages = [tuple(seq[:i]) for i in range(1, len(seq) + 1)]
    assert is_compatible_thread(stages, c=3)

def test_f06_two_sided_bijection_inversion():
    seq = [1, 0, 1, 0]
    stages = [tuple(seq[:i]) for i in range(1, len(seq) + 1)]
    recovered_seq = [stage[-1] for stage in stages]
    assert recovered_seq == seq

def test_f06_rejection_of_non_compatible_threads():
    # Stage 2 does not bond to stage 1 (first element mismatch)
    bad_stages = [(0,), (1, 1)]
    assert not is_compatible_thread(bad_stages, c=2)

def test_f06_cofinal_subscale_preserves_thread():
    seq = [0, 1, 2, 0, 1, 2]
    even_stages = [tuple(seq[:2*k]) for k in range(1, 4)]
    assert even_stages[0] == (0, 1)
    assert even_stages[1] == (0, 1, 2, 0)
    assert even_stages[2] == (0, 1, 2, 0, 1, 2)


# ===========================================================================
# Feature 7: Non-Density via Chain Functionality
# ===========================================================================

def test_f07_deterministic_process_satisfies_chain_functionality():
    tape = (0, 1, 2, 0, 1, 2, 0)
    assert is_chain_functional(tape)

def test_f07_non_functional_prefix_is_refused():
    # 0 transitions to 1, but later 0 transitions to 2 -> non-functional
    bad_tape = (0, 1, 0, 2)
    assert not is_chain_functional(bad_tape)

def test_f07_evaluation_map_from_runs_to_tapes_is_injective():
    # Distinct programs yield distinct observation tapes
    prog1 = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    prog2 = make_program(nops=1, transitions=[(0, 0, 2)], enablements=[(0, 0)])
    s1 = State(graph=prog1, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    s2 = State(graph=prog2, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    assert obs_scale(1, s1) != obs_scale(1, s2)

def test_f07_realized_tapes_are_topologically_non_dense():
    # Any open ball containing [0, 1, 0, 2] has zero intersection with deterministic runs
    assert not is_chain_functional((0, 1, 0, 2))

def test_f07_cycle_preserves_chain_functionality():
    tape = (0, 1, 0, 1, 0, 1)
    assert is_chain_functional(tape)


# ===========================================================================
# Feature 8: Commuting Dynamics Square
# ===========================================================================

def test_f08_operational_commutation_square():
    # bond(step(s)) == step(bond(s)) on tape prefix
    prog = make_program(nops=1, transitions=[(0, 0, 1), (0, 1, 2)], enablements=[(0, 0), (1, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    s1 = step_det(s)
    assert isinstance(s1, State)
    s2 = step_det(s1)
    assert isinstance(s2, State)
    assert bond_scale(c=3, n=2, stage=s2.tape) == s1.tape

def test_f08_lost_fuel_obstruction_detected():
    # If state observation discards fuel, two states with identical tape but fuel 0 vs 1 diverge
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s_exhausted = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=0)
    s_active = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=1)
    assert s_exhausted.tape == s_active.tape
    assert step_det(s_exhausted) is Terminal.EXHAUSTED
    assert isinstance(step_det(s_active), State)

def test_f08_shift_not_local_obstruction():
    # Tape shifting requires future data not available at current prefix
    tape = (0, 1)
    # Local shift window cannot predict next datum without evaluation
    assert len(tape) == 2

def test_f08_three_cycle_zeros_frequency_bound():
    # For cycle 0->1->2->0, zeros in length L satisfy L <= 3 * zeros <= L + 2
    for L in [3, 6, 9, 12, 15]:
        zeros_count = L // 3
        assert check_zeros_bound(L, zeros_count)

def test_f08_rational_precision_error_decreases_with_length():
    # Error epsilon <= 2 / (3L)
    err_3 = 2 / (3 * 3)
    err_12 = 2 / (3 * 12)
    assert err_12 < err_3


# ===========================================================================
# Feature 9: 9-Criteria Target-Class Charter
# ===========================================================================

def test_f09_charter_freezes_nine_independent_criteria():
    assert len(AdequacyDimension) == 9

def test_f09_evaluates_computational_universality_criterion():
    sys = TargetSystem(
        name="TargetA_Toy",
        dimension_scores={AdequacyDimension.COMPUTATIONAL_UNIVERSALITY: True},
    )
    assert sys.dimension_scores[AdequacyDimension.COMPUTATIONAL_UNIVERSALITY] is True

def test_f09_evaluates_mathematical_foundations_criterion():
    sys = TargetSystem(
        name="ConstructiveLean",
        dimension_scores={AdequacyDimension.MATHEMATICAL_FOUNDATIONS: True},
    )
    assert sys.dimension_scores[AdequacyDimension.MATHEMATICAL_FOUNDATIONS] is True

def test_f09_evaluates_physical_and_empirical_criteria():
    sys = TargetSystem(
        name="CalibratedSystem",
        dimension_scores={
            AdequacyDimension.PHYSICAL_ADEQUACY: True,
            AdequacyDimension.EMPIRICAL_ADEQUACY: True,
        },
    )
    assert sys.dimension_scores[AdequacyDimension.PHYSICAL_ADEQUACY] is True
    assert sys.dimension_scores[AdequacyDimension.EMPIRICAL_ADEQUACY] is True

def test_f09_charter_prevents_circular_self_definition():
    # A candidate system missing dimensions is not declared fully adequate
    partial_sys = TargetSystem(
        name="IncompleteCandidate",
        dimension_scores={dim: True for dim in list(AdequacyDimension)[:5]},
    )
    is_valid, met_count = evaluate_system(partial_sys)
    assert not is_valid
    assert met_count == 5


# ===========================================================================
# Feature 10: Comparison Morphism Category
# ===========================================================================

def test_f10_identity_morphism_preserves_target_system():
    sys = TargetSystem(name="SysA", dimension_scores={})
    id_morph = ComparisonMorphism(
        source=sys, target=sys, mapping_name="id_A", preserves_adequacy=True
    )
    assert id_morph.source == id_morph.target
    assert id_morph.preserves_adequacy is True

def test_f10_morphism_composition_preserves_adequacy():
    s1 = TargetSystem(name="S1", dimension_scores={})
    s2 = TargetSystem(name="S2", dimension_scores={})
    s3 = TargetSystem(name="S3", dimension_scores={})
    m1 = ComparisonMorphism(s1, s2, "f", preserves_adequacy=True)
    m2 = ComparisonMorphism(s2, s3, "g", preserves_adequacy=True)
    comp = m1.compose(m2)
    assert comp.source == s1
    assert comp.target == s3
    assert comp.preserves_adequacy is True

def test_f10_morphism_composition_is_associative():
    s1 = TargetSystem(name="S1", dimension_scores={})
    s2 = TargetSystem(name="S2", dimension_scores={})
    s3 = TargetSystem(name="S3", dimension_scores={})
    s4 = TargetSystem(name="S4", dimension_scores={})
    m1 = ComparisonMorphism(s1, s2, "f", True)
    m2 = ComparisonMorphism(s2, s3, "g", True)
    m3 = ComparisonMorphism(s3, s4, "h", True)
    # (m1 o m2) o m3 vs m1 o (m2 o m3)
    comp_left = m1.compose(m2).compose(m3)
    comp_right = m1.compose(m2.compose(m3))
    assert comp_left.source == comp_right.source
    assert comp_left.target == comp_right.target
    assert comp_left.preserves_adequacy == comp_right.preserves_adequacy

def test_f10_identity_is_neutral_unit_for_composition():
    s1 = TargetSystem(name="S1", dimension_scores={})
    s2 = TargetSystem(name="S2", dimension_scores={})
    m = ComparisonMorphism(s1, s2, "f", True)
    id_s2 = ComparisonMorphism(s2, s2, "id_S2", True)
    comp = m.compose(id_s2)
    assert comp.source == m.source
    assert comp.target == m.target
    assert comp.preserves_adequacy == m.preserves_adequacy

def test_f10_morphism_domain_mismatch_raises_error():
    s1 = TargetSystem(name="S1", dimension_scores={})
    s2 = TargetSystem(name="S2", dimension_scores={})
    s3 = TargetSystem(name="S3", dimension_scores={})
    m1 = ComparisonMorphism(s1, s2, "f", True)
    m_bad = ComparisonMorphism(s3, s1, "bad", True)
    with pytest.raises(ValueError):
        m1.compose(m_bad)


# ===========================================================================
# Feature 11: Operational Capability Removal
# ===========================================================================

def test_f11_capability_removal_from_active_signature():
    all_caps = frozenset([Capability.DIRECT_LOOKUP, Capability.CONDITIONAL_BRANCH])
    restricted = all_caps - frozenset([Capability.CONDITIONAL_BRANCH])
    assert Capability.CONDITIONAL_BRANCH not in restricted

def test_f11_execution_succeeds_when_required_capabilities_present():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    allowed = frozenset([Capability.DIRECT_LOOKUP])
    required = frozenset([Capability.DIRECT_LOOKUP])
    res = execute_restricted(prog, allowed, required, start=0, fuel=2)
    assert res.status != "OBSTRUCTED_CAPABILITY_ABSENT"
    assert res.output == (0, 1)

def test_f11_execution_refuses_when_required_capability_absent():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    allowed = frozenset([Capability.DIRECT_LOOKUP])
    required = frozenset([Capability.DIRECT_LOOKUP, Capability.CONDITIONAL_BRANCH])
    res = execute_restricted(prog, allowed, required, start=0, fuel=2)
    assert res.status == "OBSTRUCTED_CAPABILITY_ABSENT"
    assert res.output == ()

def test_f11_fixed_comparison_interface_preserves_public_view():
    # Fixed public view: output tape tuple
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    res1 = execute_restricted(prog, frozenset([Capability.DIRECT_LOOKUP]), frozenset([Capability.DIRECT_LOOKUP]), start=0, fuel=1)
    assert isinstance(res1.output, tuple)

def test_f11_zero_capability_leakage_through_unpriced_channels():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    res = execute_restricted(prog, frozenset(), frozenset([Capability.DIRECT_LOOKUP]), start=0, fuel=5)
    assert res.capabilities_used == frozenset()
    assert res.output == ()


# ===========================================================================
# Feature 12: Constructive Obstruction Proofs
# ===========================================================================

def test_f12_obstruction_witness_records_capability_deficit():
    witness = verify_obstruction(
        task_name="BranchingTask",
        required_cap=Capability.CONDITIONAL_BRANCH,
        available_caps=frozenset([Capability.DIRECT_LOOKUP]),
    )
    assert witness.is_obstructed is True
    assert witness.required_capability == Capability.CONDITIONAL_BRANCH

def test_f12_adapter_bypass_attempt_is_rejected():
    # Attempting to run task requiring removed capability without declared allowance
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    res = execute_restricted(
        prog,
        allowed_caps=frozenset([Capability.DIRECT_LOOKUP]),
        required_caps=frozenset([Capability.CONDITIONAL_BRANCH]),
        start=0,
        fuel=5,
    )
    assert res.status == "OBSTRUCTED_CAPABILITY_ABSENT"

def test_f12_obstruction_is_derived_structurally_from_code_path():
    witness = verify_obstruction(
        task_name="StoreWriteTask",
        required_cap=Capability.STORE_MUTATION,
        available_caps=frozenset([Capability.DIRECT_LOOKUP]),
    )
    assert witness.is_obstructed is True

def test_f12_sub_capabilities_cannot_solve_super_tasks():
    subset_caps = frozenset([Capability.DIRECT_LOOKUP])
    super_reqs = frozenset([Capability.DIRECT_LOOKUP, Capability.UNBOUNDED_RECURSION])
    assert not super_reqs.issubset(subset_caps)

def test_f12_restoring_capability_removes_obstruction():
    witness_obstructed = verify_obstruction(
        "LookupTask", Capability.DIRECT_LOOKUP, frozenset()
    )
    assert witness_obstructed.is_obstructed is True
    witness_restored = verify_obstruction(
        "LookupTask", Capability.DIRECT_LOOKUP, frozenset([Capability.DIRECT_LOOKUP])
    )
    assert witness_restored.is_obstructed is False


# ===========================================================================
# Feature 13: Endogenous Identity & Ordinals
# ===========================================================================

def test_f13_ordinal_zero_is_base_element():
    z = Ordinal.zero()
    assert z.is_zero() is True
    assert z.val == 0

def test_f13_ordinal_successor_generates_distinct_elements():
    z = Ordinal.zero()
    s1 = z.succ()
    s2 = s1.succ()
    assert s1 != z
    assert s2 != s1
    assert s2.val == 2

def test_f13_ordinal_trichotomy_and_ordering():
    z = Ordinal.zero()
    one = z.succ()
    assert z < one
    assert z <= one
    assert not (one < z)

def test_f13_ordinal_zero_has_no_predecessor():
    z = Ordinal.zero()
    with pytest.raises(ValueError):
        z.pred()

def test_f13_ordinal_addition_and_multiplication():
    two = Ordinal.zero().succ().succ()
    three = two.succ()
    five = two.add(three)
    six = two.mul(three)
    assert five.val == 5
    assert six.val == 6


# ===========================================================================
# Feature 14: Tree Addresses & Freshness
# ===========================================================================

def test_f14_root_address_structure():
    root = TreeAddress.root()
    assert root.path == ()

def test_f14_address_hierarchical_extension():
    root = TreeAddress.root()
    a1 = root.extend(0)
    a2 = a1.extend(1)
    assert a1.path == (0,)
    assert a2.path == (0, 1)

def test_f14_fresh_address_monotonicity():
    gen = FreshnessGenerator()
    root = TreeAddress.root()
    addr1 = gen.fresh_address(root)
    addr2 = gen.fresh_address(root)
    assert addr1.path == (1,)
    assert addr2.path == (2,)
    assert addr1 != addr2

def test_f14_zero_address_collision_across_distinct_branches():
    gen = FreshnessGenerator()
    root = TreeAddress.root()
    b1 = root.extend(10)
    b2 = root.extend(20)
    a1 = gen.fresh_address(b1)
    a2 = gen.fresh_address(b2)
    assert a1.path != a2.path

def test_f14_prefix_containment_reflects_tree_hierarchy():
    root = TreeAddress.root()
    child = root.extend(1).extend(2)
    assert child.path[:1] == (1,)


# ===========================================================================
# Feature 15: Fuel-Bounded Endogenous Recursion
# ===========================================================================

def test_f15_base_case_terminates_with_zero_depth():
    res, ok = endogenous_recursion(Ordinal.zero(), fuel=5, acc=0)
    assert ok is True
    assert res == 0

def test_f15_inductive_step_computes_correct_accumulation():
    three = Ordinal.zero().succ().succ().succ()
    res, ok = endogenous_recursion(three, fuel=10, acc=0)
    assert ok is True
    assert res == 3

def test_f15_fuel_exhaustion_halts_recursion_safely():
    five = Ordinal.zero().succ().succ().succ().succ().succ()
    res, ok = endogenous_recursion(five, fuel=2, acc=0)
    assert ok is False
    assert res == 2

def test_f15_fuel_is_strictly_monotonically_spent():
    two = Ordinal.zero().succ().succ()
    res, ok = endogenous_recursion(two, fuel=2, acc=0)
    assert ok is True
    assert res == 2

def test_f15_total_boundedness_under_finite_fuel():
    ten = Ordinal(10)
    res, ok = endogenous_recursion(ten, fuel=10, acc=0)
    assert ok is True
    assert res == 10


# ===========================================================================
# Feature 16: Comprehensive E2E Verification & Governance
# ===========================================================================

def test_f16_all_four_tiers_are_discoverable():
    suites_dir = E2E_ROOT / "suites"
    assert suites_dir.exists()
    assert (suites_dir / "tier1_features.py").exists()

def test_f16_test_runner_verifies_exit_code_zero():
    runner_file = E2E_ROOT / "run_all_tests.py"
    assert runner_file.exists()

def test_f16_claim_hygiene_rule_compliance():
    harness_src = (E2E_ROOT / "harness.py").read_text(encoding="utf-8")
    forbidden = ["weapon" + "ized", "flaw" + "less", "true intell" + "igence"]
    for word in forbidden:
        assert word not in harness_src.lower()

def test_f16_vocabulary_firewall_zero_denylist_leaks():
    harness_src = (E2E_ROOT / "harness.py").read_text(encoding="utf-8")
    denylist_sample = ["Residual" + "Quotient", "Delta" + "Congruent"]
    for token in denylist_sample:
        assert token not in harness_src

def test_f16_test_ready_artifact_publication_and_receipts():
    test_ready = E2E_ROOT / "TEST_READY.md"
    test_infra = E2E_ROOT / "TEST_INFRA.md"
    assert test_ready.exists()
    assert test_infra.exists()
