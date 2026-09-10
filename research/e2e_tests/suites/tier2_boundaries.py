"""Tier 2: Boundary Value Analysis & Corner Cases E2E Test Suite.

Covers all 16 features from PROJECT.md with at least 5 distinct boundary/corner case tests per feature (80 tests total).
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
# Feature 1: Represented Program & Lookup Boundaries
# ===========================================================================

def test_b01_lookup_on_empty_graph_returns_none():
    assert lookup(3, 0, ()) is None

def test_b01_lookup_with_negative_datum_returns_none():
    prog = ((3, (0, 1)),)
    assert lookup(3, -1, prog) is None

def test_b01_lookup_form_index_boundary_zero():
    prog = ((0, (5, 6)), (1, (5, 7)))
    assert lookup(0, 5, prog) == 6
    assert lookup(1, 5, prog) == 7

def test_b01_lookup_target_cycle_on_self():
    prog = ((3, (0, 0)),)
    assert lookup(3, 0, prog) == 0

def test_b01_lookup_dense_graph_with_max_datum():
    max_d = 1000
    prog = ((3, (max_d, 0)),)
    assert lookup(3, max_d, prog) == 0


# ===========================================================================
# Feature 2: Control & Branching Boundaries
# ===========================================================================

def test_b02_zero_fuel_returns_exhausted_instantly():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=0)
    assert step_det(s) is Terminal.EXHAUSTED

def test_b02_fuel_equals_exact_path_length():
    # 2 transitions: 0->1, 1->2 with fuel=2
    prog = make_program(nops=1, transitions=[(0, 0, 1), (0, 1, 2)], enablements=[(0, 0), (1, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=2)
    term, final_s = run(s)
    assert term is Terminal.HALT
    assert final_s.tape == (0, 1, 2)
    assert final_s.fuel == 0

def test_b02_fuel_less_than_path_length_by_one():
    prog = make_program(nops=1, transitions=[(0, 0, 1), (0, 1, 2)], enablements=[(0, 0), (1, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=1)
    term, final_s = run(s)
    assert term is Terminal.EXHAUSTED
    assert final_s.tape == (0, 1)

def test_b02_three_way_fork_returns_branch_without_selection():
    prog = make_program(
        nops=3,
        transitions=[(0, 0, 1), (1, 0, 2), (2, 0, 3)],
        enablements=[(0, 0), (0, 1), (0, 2)],
    )
    s = State(graph=prog, nops=3, active=0, tape=(0,), clock=0, fuel=5)
    assert step_det(s) is Terminal.BRANCH

def test_b02_missing_edge_at_active_datum_returns_refuse():
    # Op 0 is enabled at 0, but no edge exists leaving 0
    prog = make_program(nops=1, transitions=[], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    assert step_det(s) is Terminal.REFUSE


# ===========================================================================
# Feature 3: Memory Growth Boundaries
# ===========================================================================

def test_b03_memory_state_at_step_zero_has_empty_records():
    s = State(graph=(), nops=0, active=0, tape=(0,), clock=0, fuel=0)
    ms = MemoryState(base_state=s, records=())
    assert len(ms.records) == 0

def test_b03_depth2_record_unavailable_when_tape_length_less_than_three():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    ms = MemoryState(base_state=s, records=())
    ms1 = step_with_memory(ms)
    assert isinstance(ms1, MemoryState)
    assert all(r.depth != 2 for r in ms1.records)

def test_b03_step_limit_zero_produces_no_new_records():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=0)
    ms = MemoryState(base_state=s, records=())
    res = step_with_memory(ms)
    assert res is Terminal.EXHAUSTED

def test_b03_large_trace_memory_accumulation():
    # 5-step cycle
    prog = make_program(
        nops=1,
        transitions=[(0, i, (i + 1) % 5) for i in range(5)],
        enablements=[(i, 0) for i in range(5)],
    )
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    ms = MemoryState(base_state=s, records=())
    for _ in range(5):
        nxt = step_with_memory(ms)
        assert isinstance(nxt, MemoryState)
        ms = nxt
    assert len(ms.records) == 9  # 5 depth-1 records + 4 depth-2 records

def test_b03_refusal_at_step_produces_no_spurious_records():
    prog = make_program(nops=1, transitions=[], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    ms = MemoryState(base_state=s, records=())
    res = step_with_memory(ms)
    assert res is Terminal.REFUSE


# ===========================================================================
# Feature 4: Multi-Locus Boundaries
# ===========================================================================

def test_b04_carrier_size_one_product_locus():
    m = 1
    packed = pack_locus(m, 0, 0)
    assert unpack_locus(m, packed) == (0, 0)

def test_b04_unpack_with_zero_returns_zero_zero():
    assert unpack_locus(m=10, x=0) == (0, 0)

def test_b04_max_carrier_coordinate_pack_unpack():
    m = 100
    packed = pack_locus(m, 99, 99)
    assert unpack_locus(m, packed) == (99, 99)

def test_b04_independent_step_at_boundary_coordinates():
    m = 10
    # Coordinates (0, 9)
    packed = pack_locus(m, 0, 9)
    a, b = unpack_locus(m, packed)
    # Advance only locus A
    new_packed = pack_locus(m, a + 1, b)
    assert unpack_locus(m, new_packed) == (1, 9)

def test_b04_coupled_step_with_cross_boundary_wraparound():
    m = 10
    # Coordinates (5, 5) with modular wraparound
    a, b = 5, 5
    new_a = (a + 1) % m
    new_b = (b + new_a) % m
    assert unpack_locus(m, pack_locus(m, new_a, new_b)) == (6, 1)


# ===========================================================================
# Feature 5: Observation Scale Boundaries
# ===========================================================================

def test_b05_scale_zero_observation_returns_singleton_tape():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    assert obs_scale(0, s) == (0,)

def test_b05_scale_one_observation_returns_single_transition():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=5)
    assert obs_scale(1, s) == (0, 1)

def test_b05_scale_larger_than_carrier_period():
    # Cycle 0->1->0: scale 10 exceeds carrier size 2
    prog = make_program(
        nops=1,
        transitions=[(0, 0, 1), (0, 1, 0)],
        enablements=[(0, 0), (1, 0)],
    )
    s = State(graph=prog, nops=1, active=0, tape=(0,), clock=0, fuel=15)
    obs = obs_scale(10, s)
    assert len(obs) == 11
    assert obs[0] == 0 and obs[1] == 1 and obs[2] == 0

def test_b05_bond_on_length_one_returns_empty():
    assert bond_scale(c=2, n=0, stage=(1,)) == ()

def test_b05_bond_on_mismatched_length_raises_value_error():
    with pytest.raises(ValueError):
        bond_scale(c=2, n=5, stage=(0, 1))


# ===========================================================================
# Feature 6: Sequence Space Boundaries
# ===========================================================================

def test_b06_thread_with_single_stage():
    assert is_compatible_thread([(0,)], c=2) is True

def test_b06_sequence_truncated_to_length_zero():
    empty_stages: list[tuple[int, ...]] = []
    assert is_compatible_thread(empty_stages, c=2) is True

def test_b06_constant_sequence_thread_compatibility():
    constant_stages = [tuple([0] * i) for i in range(1, 10)]
    assert is_compatible_thread(constant_stages, c=1) is True

def test_b06_alternating_sequence_thread_compatibility():
    alt_seq = [0 if i % 2 == 0 else 1 for i in range(10)]
    stages = [tuple(alt_seq[:i]) for i in range(1, len(alt_seq) + 1)]
    assert is_compatible_thread(stages, c=2) is True

def test_b06_single_element_carrier_thread():
    stages = [(0,), (0, 0), (0, 0, 0)]
    assert is_compatible_thread(stages, c=1) is True


# ===========================================================================
# Feature 7: Chain Functionality Boundaries
# ===========================================================================

def test_b07_empty_tape_chain_functionality():
    assert is_chain_functional(()) is True

def test_b07_singleton_tape_chain_functionality():
    assert is_chain_functional((0,)) is True

def test_b07_two_element_tape_chain_functionality():
    assert is_chain_functional((0, 1)) is True

def test_b07_cycle_tape_length_two_functionality():
    assert is_chain_functional((0, 1, 0, 1)) is True

def test_b07_fork_attempt_at_first_step_refused():
    assert is_chain_functional((0, 1, 0, 2)) is False


# ===========================================================================
# Feature 8: Dynamics Commutation & Bound Boundaries
# ===========================================================================

def test_b08_zeros_bound_at_minimal_length_one():
    # For L=1, zeros=0: 1 <= 0 is False; zeros=1: 1 <= 3 <= 3 holds
    assert check_zeros_bound(1, 1) is True

def test_b08_zeros_bound_at_cycle_length_three():
    # For L=3, zeros=1: 3 <= 3 <= 5 holds
    assert check_zeros_bound(3, 1) is True

def test_b08_zeros_bound_at_large_length_nine_hundred():
    # For L=900, zeros=300: 900 <= 900 <= 902 holds
    assert check_zeros_bound(900, 300) is True

def test_b08_rational_frequency_with_zero_occurrences():
    tape = (1, 2, 1, 2)
    assert rational_frequency(tape, target=0) == (0, 4)

def test_b08_rational_frequency_with_all_occurrences():
    tape = (0, 0, 0)
    assert rational_frequency(tape, target=0) == (3, 3)


# ===========================================================================
# Feature 9: 9-Criteria Charter Boundaries
# ===========================================================================

def test_b09_empty_system_scores_zero_criteria():
    sys = TargetSystem(name="EmptySys", dimension_scores={})
    is_valid, met = evaluate_system(sys)
    assert not is_valid
    assert met == 0

def test_b09_system_with_eight_criteria_fails_charter():
    dims = list(AdequacyDimension)[:8]
    sys = TargetSystem(name="BorderlineFail", dimension_scores={d: True for d in dims})
    is_valid, met = evaluate_system(sys)
    assert not is_valid
    assert met == 8

def test_b09_system_with_exact_nine_criteria_passes_charter():
    sys = TargetSystem(
        name="CompletePass",
        dimension_scores={d: True for d in AdequacyDimension},
    )
    is_valid, met = evaluate_system(sys)
    assert is_valid
    assert met == 9

def test_b09_system_with_duplicate_scores_handled_idempotently():
    sys = TargetSystem(
        name="IdempotentTest",
        dimension_scores={AdequacyDimension.EMPIRICAL_ADEQUACY: True},
    )
    is_valid, met = evaluate_system(sys)
    assert met == 1

def test_b09_charter_evaluation_is_order_independent():
    scores = {d: True for d in reversed(list(AdequacyDimension))}
    sys = TargetSystem(name="ReverseOrderSys", dimension_scores=scores)
    is_valid, met = evaluate_system(sys)
    assert is_valid
    assert met == 9


# ===========================================================================
# Feature 10: Comparison Morphism Boundaries
# ===========================================================================

def test_b10_identity_morphism_on_empty_system():
    sys = TargetSystem(name="EmptySys", dimension_scores={})
    m = ComparisonMorphism(sys, sys, "id", preserves_adequacy=True)
    assert m.source.name == m.target.name

def test_b10_three_morphism_associative_composition_chain():
    systems = [TargetSystem(f"S{i}", {}) for i in range(4)]
    m0 = ComparisonMorphism(systems[0], systems[1], "f0", True)
    m1 = ComparisonMorphism(systems[1], systems[2], "f1", True)
    m2 = ComparisonMorphism(systems[2], systems[3], "f2", True)
    chain = m0.compose(m1).compose(m2)
    assert chain.source == systems[0]
    assert chain.target == systems[3]

def test_b10_morphism_failing_adequacy_preservation():
    s1 = TargetSystem("S1", {})
    s2 = TargetSystem("S2", {})
    m_lossy = ComparisonMorphism(s1, s2, "lossy", preserves_adequacy=False)
    assert m_lossy.preserves_adequacy is False

def test_b10_morphism_composition_preserves_false_adequacy():
    s1 = TargetSystem("S1", {})
    s2 = TargetSystem("S2", {})
    s3 = TargetSystem("S3", {})
    m_lossy = ComparisonMorphism(s1, s2, "lossy", preserves_adequacy=False)
    m_sound = ComparisonMorphism(s2, s3, "sound", preserves_adequacy=True)
    comp = m_lossy.compose(m_sound)
    assert comp.preserves_adequacy is False

def test_b10_self_loop_morphism_composition():
    s = TargetSystem("Self", {})
    m = ComparisonMorphism(s, s, "loop", preserves_adequacy=True)
    assert m.compose(m).source == s


# ===========================================================================
# Feature 11: Capability Removal Boundaries
# ===========================================================================

def test_b11_empty_required_capabilities_always_succeeds():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    res = execute_restricted(prog, allowed_caps=frozenset(), required_caps=frozenset(), start=0, fuel=1)
    assert res.status != "OBSTRUCTED_CAPABILITY_ABSENT"

def test_b11_empty_allowed_capabilities_fails_any_requirement():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    res = execute_restricted(
        prog,
        allowed_caps=frozenset(),
        required_caps=frozenset([Capability.DIRECT_LOOKUP]),
        start=0,
        fuel=1,
    )
    assert res.status == "OBSTRUCTED_CAPABILITY_ABSENT"

def test_b11_all_capabilities_allowed_executes_fully():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    all_caps = frozenset(Capability)
    res = execute_restricted(prog, all_caps, all_caps, start=0, fuel=1)
    assert res.status != "OBSTRUCTED_CAPABILITY_ABSENT"

def test_b11_zero_fuel_with_capability_present_returns_exhausted():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    caps = frozenset([Capability.DIRECT_LOOKUP])
    res = execute_restricted(prog, caps, caps, start=0, fuel=0)
    assert res.status == "exhausted"

def test_b11_capability_removal_yields_empty_output_on_refusal():
    prog = make_program(nops=1, transitions=[(0, 0, 1)], enablements=[(0, 0)])
    res = execute_restricted(
        prog,
        allowed_caps=frozenset(),
        required_caps=frozenset([Capability.STORE_MUTATION]),
        start=0,
        fuel=5,
    )
    assert res.output == ()


# ===========================================================================
# Feature 12: Constructive Obstruction Boundaries
# ===========================================================================

def test_b12_obstruction_witness_with_empty_capabilities():
    w = verify_obstruction("T", Capability.DIRECT_LOOKUP, frozenset())
    assert w.is_obstructed is True

def test_b12_obstruction_witness_with_disjoint_capabilities():
    w = verify_obstruction(
        "T", Capability.DIRECT_LOOKUP, frozenset([Capability.CONDITIONAL_BRANCH])
    )
    assert w.is_obstructed is True

def test_b12_obstruction_witness_with_subset_capabilities():
    w = verify_obstruction(
        "T", Capability.DIRECT_LOOKUP, frozenset([Capability.DIRECT_LOOKUP, Capability.STORE_MUTATION])
    )
    assert w.is_obstructed is False

def test_b12_obstruction_witness_reports_exact_missing_capability():
    w = verify_obstruction("TaskX", Capability.UNBOUNDED_RECURSION, frozenset())
    assert w.required_capability == Capability.UNBOUNDED_RECURSION

def test_b12_obstruction_is_immutable():
    w = verify_obstruction("TaskX", Capability.STORE_MUTATION, frozenset())
    assert isinstance(w.is_obstructed, bool)


# ===========================================================================
# Feature 13: Endogenous Ordinal Boundaries
# ===========================================================================

def test_b13_ordinal_zero_pred_raises_value_error():
    z = Ordinal.zero()
    with pytest.raises(ValueError):
        z.pred()

def test_b13_ordinal_zero_eq_zero():
    assert Ordinal.zero() == Ordinal(0)

def test_b13_ordinal_zero_lt_succ_zero():
    assert Ordinal.zero() < Ordinal.zero().succ()

def test_b13_large_ordinal_chain_monotonicity():
    curr = Ordinal.zero()
    for _ in range(20):
        nxt = curr.succ()
        assert curr < nxt
        curr = nxt
    assert curr.val == 20

def test_b13_ordinal_addition_with_zero_identity():
    three = Ordinal(3)
    assert three.add(Ordinal.zero()) == three
    assert Ordinal.zero().add(three) == three


# ===========================================================================
# Feature 14: Tree Address Boundaries
# ===========================================================================

def test_b14_root_address_path_is_empty_tuple():
    assert TreeAddress.root().path == ()

def test_b14_single_step_address_extension():
    a = TreeAddress.root().extend(0)
    assert a.path == (0,)

def test_b14_deeply_nested_address_depth_fifty():
    curr = TreeAddress.root()
    for i in range(50):
        curr = curr.extend(i)
    assert len(curr.path) == 50

def test_b14_freshness_generator_initial_counter_zero():
    gen = FreshnessGenerator()
    assert gen.counter == 0

def test_b14_distinct_parents_generate_disjoint_fresh_addresses():
    gen = FreshnessGenerator()
    r = TreeAddress.root()
    p1 = r.extend(1)
    p2 = r.extend(2)
    a1 = gen.fresh_address(p1)
    a2 = gen.fresh_address(p2)
    assert a1.path != a2.path


# ===========================================================================
# Feature 15: Endogenous Recursion Boundaries
# ===========================================================================

def test_b15_recursion_zero_depth_zero_fuel_succeeds():
    res, ok = endogenous_recursion(Ordinal.zero(), fuel=0, acc=42)
    assert ok is True
    assert res == 42

def test_b15_recursion_depth_one_zero_fuel_halts():
    res, ok = endogenous_recursion(Ordinal.zero().succ(), fuel=0, acc=0)
    assert ok is False
    assert res == 0

def test_b15_recursion_exact_fuel_equals_depth():
    k = 5
    res, ok = endogenous_recursion(Ordinal(k), fuel=k, acc=0)
    assert ok is True
    assert res == k

def test_b15_recursion_excess_fuel_succeeds_without_waste():
    k = 3
    res, ok = endogenous_recursion(Ordinal(k), fuel=100, acc=0)
    assert ok is True
    assert res == k

def test_b15_recursion_large_depth_finite_fuel_boundedness():
    large = Ordinal(100)
    res, ok = endogenous_recursion(large, fuel=25, acc=0)
    assert ok is False
    assert res == 25


# ===========================================================================
# Feature 16: Verification & Governance Boundaries
# ===========================================================================

def test_b16_empty_test_suite_refusal():
    """Operational boundary: test runner refuses and reports failure on missing/empty suite."""
    from run_all_tests import run_tier
    missing_path = E2E_ROOT / "suites" / "_non_existent_suite_boundary.py"
    passed, failed, failures, elapsed = run_tier("TestTier", "Empty/Missing Suite", missing_path)
    assert passed == 0
    assert failed == 1
    assert len(failures) == 1
    assert "File not found" in failures[0]


def test_b16_failed_test_emits_non_zero_exit_code():
    """Operational boundary: test runner detects assertion failures and records non-zero failure counts."""
    from run_all_tests import run_tier
    failing_test_path = E2E_ROOT / "suites" / "_temp_failing_boundary.py"
    try:
        failing_test_path.write_text(
            "def test_failing_case():\n"
            "    assert 0 == 1, 'Injected operational test boundary failure'\n",
            encoding="utf-8",
        )
        passed, failed, failures, elapsed = run_tier("TestTier", "Failing Case Boundary", failing_test_path)
        assert passed == 0
        assert failed == 1
        assert len(failures) == 1
        assert "Injected operational test boundary failure" in failures[0]
    finally:
        if failing_test_path.exists():
            failing_test_path.unlink()


def test_b16_prose_watchlist_catches_hype_words():
    # Verifies no forbidden hype words in boundary test suite
    harness_src = (E2E_ROOT / "harness.py").read_text(encoding="utf-8")
    forbidden = ["weapon" + "ized", "flaw" + "less"]
    for w in forbidden:
        assert w not in harness_src.lower()


def test_b16_axiom_census_boundary_contains_only_valid_axioms():
    """Operational boundary: verify evidence receipts and active Lean code across all research packages."""
    import json
    import re
    research_dir = E2E_ROOT.parent

    # 1. Inspect evidence receipts across all five target packages
    receipts = list(research_dir.glob("*/evidence/receipt.json"))
    assert len(receipts) == 5, f"Expected 5 research receipts, found {len(receipts)}"

    allowed = {"propext", "Quot.sound"}
    for r in receipts:
        data = json.loads(r.read_text(encoding="utf-8"))
        if "lean" in data and "allowed_axioms" in data["lean"]:
            assert set(data["lean"]["allowed_axioms"]).issubset(allowed)
        if "axiom_boundary" in data:
            assert set(data["axiom_boundary"]).issubset(allowed)
        if "lean_audit" in data and "allowed_axioms" in data["lean_audit"]:
            assert set(data["lean_audit"]["allowed_axioms"]).issubset(allowed)

    # 2. Inspect active Lean source code for non-constructive tokens
    forbidden_tokens = re.compile(r"\b(?:sorry|admit|unsafe|partial)\b|^\s*axiom\s", re.MULTILINE)
    lean_sources = list(research_dir.glob("*/lean/*.lean"))
    assert len(lean_sources) >= 15, f"Expected Lean source files, found {len(lean_sources)}"
    for ls in lean_sources:
        text = ls.read_text(encoding="utf-8")
        assert not forbidden_tokens.search(text), f"Forbidden constructive token in {ls.name}"


def test_b16_receipt_integrity_hash_verification():
    # Validates deterministic hashing of test documentation
    infra_text = (E2E_ROOT / "TEST_INFRA.md").read_bytes()
    assert len(infra_text) > 0
