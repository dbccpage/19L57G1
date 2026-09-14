"""Adversarial negative controls and property tests across all 4 tracks.

AuthorityEffect: None.

Covers:
1. Track 1 (Observer Enclosure):
   - Tampering detection: mutation of past records in InternalTrace raises error.
   - Retrocausal modification attempt is caught and rejected.
   - External history rewriting is detected via cryptographic hash chain mismatch.
   - State digest discrepancy rejection.
2. Track 2 (Projective System):
   - Non-commuting coarsening projections (pi_{j, k} o pi_{k, m} != pi_{j, m}) caught and rejected.
   - Incoherent threads (nodes failing projection matching) rejected by validate_thread.
   - Floating point injection for operational costs mu1, mu2 rejected at instantiation.
   - Non-surjective or invalid coarsening maps flagged.
3. Track 3 (Dissipative Cycle Filtering):
   - Broken cycles where net potential drop != 0 are rejected by Cycle.
   - Cycles with non-positive operational activity (total mu2 <= 0) are rejected.
   - Floating point potential or cost injection is strictly rejected.
   - Disconnected and complex graphs tested under state space pruning.
4. Track 4 (Internal Quotienting):
   - Non-confluent rewrite systems with unjoinable critical pairs detected and rejected.
   - Malicious non-terminating rewrite loops caught by depth/step safeguards.
   - Cross-equivalence class contamination tested and rejected.
5. Randomized property fuzzing:
   - Invariant checks emit zero false positives on valid sequences.
   - Invariant checks emit zero false negatives on perturbed/tampered sequences.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from fractions import Fraction
import random
from typing import Any

import pytest

# Track 1 imports
from research.endogenous_continuum.observer_enclosure import (
    EnclosedCarrier,
    InternalTrace,
    LocalAdmitDatum,
    LocalAdmitForm,
    LocalAdmitInst,
    LocalEvalDerivable,
    LocalizedTransition,
    LocalRegisterAdd,
    LocalRegisterWrite,
    ObserverRecord,
    TraceInvariantChecker,
    compute_carrier_digest,
    compute_record_hash,
)

# Track 2 imports
from research.endogenous_continuum.projective_system import (
    CoarseningMap,
    MoveEdge,
    MoveGraph,
    OperationalPrice,
    ProjectiveSystem,
    create_dyadic_coarsening_map,
    create_dyadic_movegraph,
    create_dyadic_projective_system,
    verify_commutativity,
)

# Track 3 imports
from research.endogenous_continuum.dissipative_cycle import (
    AttractorClassifier,
    AutonomousStepper,
    CarrierGraph,
    Cycle,
    StateSpacePruner,
    Transition,
)

# Track 4 imports
from research.endogenous_continuum.internal_quotienting import (
    ReductionStrategy,
    RelationalState,
    RewriteRule,
    RewriteSystem,
    make_relational_quotient_system,
    make_sorting_rewrite_system,
    make_string_rewrite_system,
    make_string_rule,
    verify_equivalence_partition,
)


# =============================================================================
# 1. Track 1: Observer Enclosure Adversarial Negative Controls
# =============================================================================


def test_track1_tampering_mutation_past_records_raises_error() -> None:
    """Tampering detection: mutation of past records in InternalTrace raises error."""
    carrier = EnclosedCarrier.genesis()
    c1 = carrier.step_localized(LocalAdmitDatum("d0"))
    c2 = c1.step_localized(LocalAdmitDatum("d1"))

    trace = c2.trace
    assert trace.length == 2

    # Immutability Check 1: tuple item assignment raises TypeError
    with pytest.raises(TypeError, match="'tuple' object does not support item assignment"):
        trace.records[0] = trace.records[1]  # type: ignore[index]

    # Immutability Check 2: modifying frozen dataclass field raises FrozenInstanceError
    with pytest.raises((FrozenInstanceError, AttributeError)):
        trace.records = ()  # type: ignore[misc]

    # Immutability Check 3: forged InternalTrace with mutated past record fails chain integrity
    orig_rec0 = trace.records[0]
    tampered_rec0 = ObserverRecord(
        step=orig_rec0.step,
        transition_kind=orig_rec0.transition_kind,
        local_input=orig_rec0.local_input,
        local_readout=(999,),
        state_digest=orig_rec0.state_digest,
        prev_record_hash=orig_rec0.prev_record_hash,
        record_hash=orig_rec0.record_hash,
    )
    tampered_trace = InternalTrace((tampered_rec0, trace.records[1]))
    assert tampered_trace.is_valid_chain() is False

    integrity_res = TraceInvariantChecker.check_trace_integrity(tampered_trace)
    assert integrity_res.valid is False
    assert any("chain validity" in v for v in integrity_res.violations)


def test_track1_retrocausal_modification_caught_and_rejected() -> None:
    """Retrocausal modification attempt is caught and rejected by invariant checkers."""
    c0 = EnclosedCarrier.genesis()
    c1 = c0.step_localized(LocalAdmitDatum("d0"))
    c2 = c1.step_localized(LocalAdmitDatum("d1"))
    c3 = c2.step_localized(LocalAdmitForm(arity=1))

    # Path consistency before tampering
    path = [c0, c1, c2, c3]
    res_clean = TraceInvariantChecker.check_carrier_path(path)
    assert res_clean.valid is True

    # Construct retrocausally tampered carrier where an earlier record in history is altered
    tampered_records = list(c3.trace.records)
    r1 = tampered_records[1]
    tampered_r1 = ObserverRecord.create(
        step=r1.step,
        transition_kind=r1.transition_kind,
        local_input=("forged_token",),
        local_readout=r1.local_readout,
        state_digest=r1.state_digest,
        prev_record_hash=r1.prev_record_hash,
    )
    tampered_records[1] = tampered_r1
    tampered_trace = InternalTrace(tuple(tampered_records))

    tampered_c3 = EnclosedCarrier(
        regime=c3.regime,
        trace=tampered_trace,
        local_registers=c3.local_registers,
        step_count=c3.step_count,
    )

    # Invariant violation 1: is_monotone_extension_of fails against c2
    assert tampered_c3.trace.is_monotone_extension_of(c2.trace) is False

    # Invariant violation 2: detect_retrocausal_tampering flags the mutation
    assert TraceInvariantChecker.detect_retrocausal_tampering(tampered_c3, 1) is True

    # Invariant violation 3: check_carrier_path rejects the path containing tampered carrier
    tampered_path = [c0, c1, c2, tampered_c3]
    res_tampered = TraceInvariantChecker.check_carrier_path(tampered_path)
    assert res_tampered.valid is False
    assert any("past record at index 1 was modified" in v for v in res_tampered.violations)


def test_track1_external_history_rewriting_detected_via_hash_chain_mismatch() -> None:
    """External history rewriting is detected via cryptographic hash chain mismatch."""
    c0 = EnclosedCarrier.genesis()
    c1 = c0.step_localized(LocalAdmitDatum("x"))
    c2 = c1.step_localized(LocalAdmitDatum("y"))
    c3 = c2.step_localized(LocalAdmitDatum("z"))

    # Attacker mutates step 1 and recomputes record_hash for step 1,
    # but does not rewrite step 2's prev_record_hash pointer.
    r1 = c3.trace.records[1]
    forged_r1 = ObserverRecord.create(
        step=r1.step,
        transition_kind=r1.transition_kind,
        local_input=("injected_x",),
        local_readout=r1.local_readout,
        state_digest=r1.state_digest,
        prev_record_hash=r1.prev_record_hash,
    )
    broken_chain = InternalTrace((c3.trace.records[0], forged_r1, c3.trace.records[2]))

    # Broken chain fails validation
    assert broken_chain.is_valid_chain() is False

    res_integrity = TraceInvariantChecker.check_trace_integrity(broken_chain)
    assert res_integrity.valid is False

    # Single-step transition validation from c1 to forged next carrier fails chaining
    forged_c2 = EnclosedCarrier(
        regime=c2.regime,
        trace=InternalTrace((c3.trace.records[0], forged_r1)),
        local_registers=c2.local_registers,
        step_count=2,
    )
    # Step transition between forged_c2 and c3 fails chaining check
    trans = LocalAdmitDatum("z")
    step_check = TraceInvariantChecker.check_step_transition(forged_c2, c3, trans)
    assert step_check.valid is False
    assert any("Chaining failure" in v for v in step_check.violations)


def test_track1_state_digest_discrepancy_rejection() -> None:
    """State digest discrepancy between recorded hash and carrier state is rejected."""
    c0 = EnclosedCarrier.genesis()
    t1 = LocalAdmitDatum("token_a")
    c1 = c0.step_localized(t1)

    # Forged carrier: register value is modified without updating state digest in record
    forged_carrier = EnclosedCarrier(
        regime=c1.regime,
        trace=c1.trace,
        local_registers=(999, 0, 0, 0),  # modified register
        step_count=c1.step_count,
    )

    actual_digest = forged_carrier.carrier_digest()
    record_digest = forged_carrier.trace.latest.state_digest if forged_carrier.trace.latest else ""
    assert actual_digest != record_digest

    res = TraceInvariantChecker.check_step_transition(c0, forged_carrier, t1)
    assert res.valid is False
    assert any("state digest does not match" in v for v in res.violations)


# =============================================================================
# 2. Track 2: Projective System Adversarial Negative Controls
# =============================================================================


def test_track2_non_commuting_coarsening_projections_rejected() -> None:
    """Non-commuting coarsening projections (pi_{j, k} o pi_{k, m} != pi_{j, m}) are caught and rejected."""
    g2 = create_dyadic_movegraph(level=2)
    pi_01 = create_dyadic_coarsening_map(0, 1)
    pi_12 = create_dyadic_coarsening_map(1, 2)

    # Deliberately non-commuting direct map pi_{0, 2}
    divergent_map = dict(create_dyadic_coarsening_map(0, 2).state_map)
    divergent_map[2] = 99  # deliberate discrepancy at state 2

    bad_pi_02 = CoarseningMap(
        source_level=2,
        target_level=0,
        state_map=divergent_map,
    )

    res = verify_commutativity(pi_01, pi_12, bad_pi_02, domain_graph=g2)
    assert res.commutes is False
    assert not bool(res)
    assert any("State 2" in d for d in res.discrepancies)

    # Also verify that a ProjectiveSystem built with non-commuting map reports defects
    g0 = create_dyadic_movegraph(level=0)
    g1 = create_dyadic_movegraph(level=1)
    sys = ProjectiveSystem.build(
        graphs=[g0, g1, g2],
        bonding_maps=[pi_01, pi_12, bad_pi_02],
    )
    is_valid, defects = sys.verify_system()
    assert is_valid is False
    assert any("Commutativity defect" in d for d in defects)


def test_track2_incoherent_threads_rejected_by_validate_thread() -> None:
    """Incoherent threads (nodes failing projection matching) are rejected by validate_thread."""
    sys = create_dyadic_projective_system(max_level=3, length=1)

    # Incoherent thread: at level 3, state 8 projects down to 4 at level 2,
    # but we deliberately specify state 1 at level 2.
    incoherent_thread = {0: 0, 1: 0, 2: 1, 3: 8}
    res = sys.validate_thread(incoherent_thread)
    assert res.is_coherent is False
    assert not bool(res)
    assert any("Thread coherence failure" in d for d in res.defects)

    # Invalid state outside graph bounds
    out_of_bounds_thread = {0: 0, 1: 0, 2: 0, 3: 9999}
    res_oob = sys.validate_thread(out_of_bounds_thread)
    assert res_oob.is_coherent is False
    assert any("not in M_3.states" in d for d in res_oob.defects)


def test_track2_floating_point_injection_rejected() -> None:
    """Floating point injection for operational costs mu1, mu2 is rejected at instantiation."""
    # MoveEdge mu1 float injection
    with pytest.raises(TypeError, match="must be exact rational"):
        MoveEdge(source=0, target=1, mu1=1.5)  # type: ignore[arg-type]

    # MoveEdge mu2 float injection
    with pytest.raises(TypeError, match="must be exact rational"):
        MoveEdge(source=0, target=1, mu2=0.25)  # type: ignore[arg-type]

    # OperationalPrice float injection
    with pytest.raises(TypeError, match="must be exact rational"):
        OperationalPrice(mu1_sum=1.2, mu2_sum=0, step_count=1)  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="must be exact rational"):
        OperationalPrice(mu1_sum=0, mu2_sum=3.14159, step_count=1)  # type: ignore[arg-type]


def test_track2_non_surjective_or_invalid_coarsening_maps_flagged() -> None:
    """Non-surjective or invalid coarsening maps are flagged by morphism checks."""
    g_coarse = create_dyadic_movegraph(level=0, length=1)  # states: {0, 1}
    g_fine = create_dyadic_movegraph(level=1, length=1)    # states: {0, 1, 2}

    # Non-surjective map: all fine states collapsed to state 0 only (state 1 has empty preimage)
    non_surj_map = CoarseningMap(
        source_level=1,
        target_level=0,
        state_map={0: 0, 1: 0, 2: 0},
    )
    assert non_surj_map.is_surjective_on_states(g_coarse) is False

    # Incomplete domain: missing state 2
    incomplete_map = CoarseningMap(
        source_level=1,
        target_level=0,
        state_map={0: 0, 1: 1},
    )
    res_incomplete = incomplete_map.check_morphism(g_fine, g_coarse)
    assert res_incomplete.is_valid is False
    assert any("domain incomplete" in d for d in res_incomplete.defects)

    # Codomain violation: maps state to non-existent state 42
    invalid_codomain_map = CoarseningMap(
        source_level=1,
        target_level=0,
        state_map={0: 0, 1: 1, 2: 42},
    )
    res_codomain = invalid_codomain_map.check_morphism(g_fine, g_coarse)
    assert res_codomain.is_valid is False
    assert any("not in target graph states" in d for d in res_codomain.defects)


# =============================================================================
# 3. Track 3: Dissipative Cycle Filtering Adversarial Negative Controls
# =============================================================================


def test_track3_broken_cycles_rejected_by_cycle() -> None:
    """Broken cycles where net potential drop != 0 are rejected by Cycle."""
    t1 = Transition(source="A", target="B", mu1=2, mu2=1)
    t2 = Transition(source="B", target="A", mu1=-1, mu2=1)  # net potential is 2 - 1 = 1 != 0

    with pytest.raises(ValueError, match="Broken cycle: net potential.*must be 0"):
        Cycle(
            states=("A", "B"),
            transitions=(t1, t2),
            total_mu1=1,  # broken cycle
            total_mu2=2,
            period=2,
        )


def test_track3_non_positive_activity_rejected_by_cycle() -> None:
    """Cycles with non-positive operational activity (total mu2 <= 0) are rejected."""
    t1 = Transition(source="X", target="Y", mu1=1, mu2=1)
    t2 = Transition(source="Y", target="X", mu1=-1, mu2=1)

    # Zero activity rejection
    with pytest.raises(ValueError, match="strictly positive operational activity"):
        Cycle(
            states=("X", "Y"),
            transitions=(t1, t2),
            total_mu1=0,
            total_mu2=0,  # invalid activity
            period=2,
        )

    # Negative activity rejection
    with pytest.raises(ValueError, match="strictly positive operational activity"):
        Cycle(
            states=("X", "Y"),
            transitions=(t1, t2),
            total_mu1=0,
            total_mu2=-4,  # invalid activity
            period=2,
        )


def test_track3_floating_point_potential_and_cost_rejected() -> None:
    """Floating point potential or cost injection is strictly rejected."""
    g = CarrierGraph[str]()

    # Potential injection as float
    with pytest.raises(TypeError, match="Potential Phi must be an int"):
        g.add_state("S0", 3.14159)  # type: ignore[arg-type]

    # Boolean masquerading as int
    with pytest.raises(TypeError, match="Potential Phi must be an int"):
        g.add_state("S1", True)  # type: ignore[arg-type]

    # Transition float mu1
    with pytest.raises(TypeError, match="mu1 must be an int"):
        Transition(source="A", target="B", mu1=1.5, mu2=1)  # type: ignore[arg-type]

    # Transition float mu2
    with pytest.raises(TypeError, match="mu2 must be an int"):
        Transition(source="A", target="B", mu1=1, mu2=2.5)  # type: ignore[arg-type]

    # Cycle float cost
    t = Transition(source="A", target="A", mu1=0, mu2=1)
    with pytest.raises(TypeError, match="total_mu1 must be an int"):
        Cycle(states=("A",), transitions=(t,), total_mu1=0.0, total_mu2=1, period=1)  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="total_mu2 must be an int"):
        Cycle(states=("A",), transitions=(t,), total_mu1=0, total_mu2=1.5, period=1)  # type: ignore[arg-type]


def test_track3_disconnected_and_complex_graphs_under_pruning() -> None:
    """Disconnected and complex graphs are verified under state-space pruning."""
    g = CarrierGraph[str]()

    # Component 1: Transient acyclic chain terminating in dead-end sink
    g.add_state("T0", 30)
    g.add_state("T1", 20)
    g.add_state("T2", 10)
    g.add_transition("T0", "T1", mu2=1)
    g.add_transition("T1", "T2", mu2=1)

    # Component 2: Disconnected conservative cycle attractor
    g.add_state("C0", 5)
    g.add_state("C1", 8)
    g.add_state("C2", 2)
    g.add_transition("C0", "C1", mu2=2)
    g.add_transition("C1", "C2", mu2=3)
    g.add_transition("C2", "C0", mu2=1)

    # Component 3: Isolated isolated vertices (sinks)
    g.add_state("ISO_1", 100)
    g.add_state("ISO_2", 200)

    # Component 4: Transient feeder branching into Component 2's cycle
    g.add_state("FEED_0", 15)
    g.add_transition("FEED_0", "C0", mu2=1)

    # Run state space pruning to attractor core
    core_graph, report = StateSpacePruner.prune_to_attractor_core(g)

    # Only Component 2's cycle states survive in the core
    assert report.initial_state_count == 9
    assert report.final_state_count == 3
    assert report.retained_states == frozenset({"C0", "C1", "C2"})
    assert report.is_pure_cycle_core is True
    assert len(report.retained_cycles) == 1

    cycle = report.retained_cycles[0]
    assert cycle.is_conservative is True
    assert cycle.total_mu1 == 0
    assert cycle.total_mu2 == 6
    assert cycle.period == 3

    # Classification partitions all states correctly
    classification = AttractorClassifier.classify(g)
    assert classification.cycle_states == frozenset({"C0", "C1", "C2"})
    assert classification.sink_states == frozenset({"T2", "ISO_1", "ISO_2"})
    assert classification.transient_to_sink_states == frozenset({"T0", "T1"})
    assert classification.transient_to_cycle_states == frozenset({"FEED_0"})


# =============================================================================
# 4. Track 4: Internal Quotienting Adversarial Negative Controls
# =============================================================================


def test_track4_non_confluent_rewrite_systems_rejected() -> None:
    """Non-confluent rewrite systems with unjoinable critical pairs are detected and rejected."""
    # Critical pair overlap: rule1 'xy' -> 'a', rule2 'yz' -> 'b'
    # State 'xyz' branches to 'az' and 'xb', which are both terminal and cannot join.
    r1 = make_string_rule("xy", "a", name="xy_to_a")
    r2 = make_string_rule("yz", "b", name="yz_to_b")
    non_confluent = RewriteSystem(rules=[r1, r2], name="OverlappingNonConfluent")

    report = non_confluent.check_local_confluence(["xyz"], max_join_depth=10)
    assert report.is_locally_confluent is False
    assert report.divergences_count == 1
    assert report.joined_count == 0
    assert len(report.unjoinable_divergences) == 1

    unjoinable = report.unjoinable_divergences[0]
    assert unjoinable.source == "xyz"
    assert {unjoinable.branch_a, unjoinable.branch_b} == {"az", "xb"}

    # Multiple distinct normal forms exist for 'xyz'
    nfs = non_confluent.all_normal_forms("xyz", max_depth=10)
    assert len(nfs) == 2
    assert nfs == frozenset({"az", "xb"})


def test_track4_malicious_non_terminating_rewrite_loops_caught() -> None:
    """Malicious non-terminating rewrite loops are caught by depth/step safeguards."""
    # 1. Circular oscillating loop: a -> b, b -> c, c -> a
    r_ab = make_string_rule("a", "b", name="a_to_b")
    r_bc = make_string_rule("b", "c", name="b_to_c")
    r_ca = make_string_rule("c", "a", name="c_to_a")
    circ_sys = RewriteSystem(rules=[r_ab, r_bc, r_ca], name="CircularSystem")

    with pytest.raises(RuntimeError, match="Reduction cycle detected"):
        circ_sys.reduce_to_normal_form("a", strategy=ReductionStrategy.FIRST, max_steps=50)

    # 2. Infinite expansive loop: x -> xx
    r_expand = make_string_rule("x", "xx", name="expand_x")
    expand_sys = RewriteSystem(rules=[r_expand], name="InfiniteExpansiveSystem")

    # Shortest path BFS terminates safely when max_steps budget is reached
    res = expand_sys.reduce_to_normal_form("x", strategy=ReductionStrategy.SHORTEST_PATH, max_steps=4)
    assert res.is_normal_form is False

    # 3. Infinite divergent branches: xa* vs xb* never join within max_depth
    r_xa = make_string_rule("x", "xa", name="expand_xa")
    r_xb = make_string_rule("x", "xb", name="expand_xb")
    diverge_sys = RewriteSystem(rules=[r_xa, r_xb], name="InfiniteDivergentSystem")
    join_res = diverge_sys.find_join("xa", "xb", max_depth=5)
    assert join_res.joined is False


def test_track4_cross_equivalence_class_contamination_rejected() -> None:
    """Cross-equivalence class contamination is tested and rejected."""
    system = make_sorting_rewrite_system(alphabet=("a", "b", "c"))

    # Distinct multiset equivalence classes
    assert system.are_equivalent("abc", "cba") is True
    assert system.are_equivalent("aab", "baa") is True
    assert system.are_equivalent("abb", "bba") is True

    # Cross-class comparisons must strictly be False
    assert system.are_equivalent("abc", "aab") is False
    assert system.are_equivalent("abc", "abb") is False
    assert system.are_equivalent("aab", "abb") is False

    words = ["abc", "cba", "aab", "baa", "abb", "bba"]
    classes = system.partition_by_normal_form(words)
    assert verify_equivalence_partition(classes, words) is True

    # Artificially contaminate an equivalence class by inserting an alien member
    class_dict = {c.normal_form: c for c in classes}
    contaminated_abc = class_dict["abc"].members + ("aab",)  # inject alien word
    all_contaminated_members = contaminated_abc + class_dict["aab"].members + class_dict["abb"].members

    # Partition verification fails due to duplicate element across classes
    from research.endogenous_continuum.internal_quotienting import EquivalenceClass
    contaminated_classes = (
        EquivalenceClass("abc", contaminated_abc, len(contaminated_abc)),
        class_dict["aab"],
        class_dict["abb"],
    )
    assert verify_equivalence_partition(contaminated_classes, words) is False


# =============================================================================
# 5. Randomized Property Fuzzing across All Tracks
# =============================================================================


def test_property_fuzzing_observer_enclosure_invariants() -> None:
    """Randomized sequence of carrier transitions verifies zero false positives or false negatives."""
    rng = random.Random(42)
    c = EnclosedCarrier.genesis(num_registers=4)
    path = [c]
    transitions: list[LocalizedTransition] = []

    available_data = ["tok0", "tok1", "tok2", "tok3"]

    for step_idx in range(60):
        choice = rng.randint(0, 4)
        trans: LocalizedTransition
        if choice == 0:
            tok = rng.choice(available_data)
            trans = LocalAdmitDatum(tok)
        elif choice == 1:
            trans = LocalAdmitForm(arity=rng.randint(1, 2))
        elif choice == 2:
            reg_idx = rng.randint(0, 3)
            trans = LocalRegisterWrite(register_index=reg_idx, value=rng.randint(1, 50))
        elif choice == 3:
            t_idx = rng.randint(0, 3)
            s_idx = rng.randint(0, 3)
            trans = LocalRegisterAdd(target_index=t_idx, source_index=s_idx)
        else:
            trans = LocalAdmitDatum(f"rand_tok_{step_idx}")

        c_next = path[-1].step_localized(trans)
        transitions.append(trans)
        path.append(c_next)

    # 1. Zero False Positives: Valid execution satisfies all invariants
    res = TraceInvariantChecker.check_carrier_path(path, transitions)
    assert res.valid is True
    assert res.steps_verified == 60
    assert len(res.violations) == 0

    # 2. Zero False Negatives: Inject random corruption at an arbitrary past step
    tampered_step = rng.randint(5, 55)
    carrier_to_tamper = path[tampered_step]
    tampered_recs = list(carrier_to_tamper.trace.records)
    mutated_rec = ObserverRecord(
        step=tampered_recs[2].step,
        transition_kind=tampered_recs[2].transition_kind,
        local_input=tampered_recs[2].local_input,
        local_readout=(77777,),  # corrupted readout
        state_digest=tampered_recs[2].state_digest,
        prev_record_hash=tampered_recs[2].prev_record_hash,
        record_hash=tampered_recs[2].record_hash,
    )
    tampered_recs[2] = mutated_rec
    corrupted_carrier = EnclosedCarrier(
        regime=carrier_to_tamper.regime,
        trace=InternalTrace(tuple(tampered_recs)),
        local_registers=carrier_to_tamper.local_registers,
        step_count=carrier_to_tamper.step_count,
    )

    # Verify that corruption is unconditionally detected
    assert corrupted_carrier.trace.is_valid_chain() is False
    assert TraceInvariantChecker.detect_retrocausal_tampering(corrupted_carrier, 2) is True


def test_property_fuzzing_projective_system_functoriality() -> None:
    """Randomized projective system sequences verify functorial commutativity and thread coherence."""
    sys = create_dyadic_projective_system(max_level=3, length=1)
    is_valid, defects = sys.verify_system()
    assert is_valid is True
    assert len(defects) == 0

    rng = random.Random(1337)
    threads = list(sys.enumerate_coherent_threads())
    assert len(threads) > 0

    # All enumerated threads validate as coherent (Zero False Positives)
    for th in threads:
        val = sys.validate_thread(th)
        assert val.is_coherent is True
        assert len(val.defects) == 0

    # Perturb every thread: mutate state at level 2 or 3 (Zero False Negatives)
    for th in threads[:10]:
        perturbed = dict(th)
        perturbed[3] = (perturbed[3] + 1) % 100 + 50
        val_bad = sys.validate_thread(perturbed)
        assert val_bad.is_coherent is False
        assert len(val_bad.defects) > 0


def test_property_fuzzing_internal_quotienting_confluence() -> None:
    """Randomized word sequences verify confluence, normal form uniqueness, and idempotence."""
    system = make_sorting_rewrite_system(alphabet=("a", "b", "c", "d"))
    rng = random.Random(2026)

    chars = ["a", "b", "c", "d"]
    for _ in range(25):
        length = rng.randint(3, 8)
        word = "".join(rng.choice(chars) for _ in range(length))

        res_first = system.reduce_to_normal_form(word, strategy=ReductionStrategy.FIRST)
        res_last = system.reduce_to_normal_form(word, strategy=ReductionStrategy.LAST)
        res_short = system.reduce_to_normal_form(word, strategy=ReductionStrategy.SHORTEST_PATH)

        # All strategies must agree on the exact same normal form
        assert res_first.is_normal_form is True
        assert res_last.is_normal_form is True
        assert res_short.is_normal_form is True
        assert res_first.normal_form == res_last.normal_form == res_short.normal_form

        # Normal form must be sorted alphabetically
        expected_sorted = "".join(sorted(word))
        assert res_first.normal_form == expected_sorted

        # Quotient projection idempotence: q(q(w)) == q(w)
        q_w = system.quotient_projection(word)
        assert q_w == expected_sorted
        assert system.quotient_projection(q_w) == q_w
