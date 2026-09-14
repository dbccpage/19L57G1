"""Unit and adversarial tests for Track 2: Inverse Limit Projective System.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict, List, Tuple
import pytest

from research.endogenous_continuum.projective_system import (
    CoarseningMap,
    CommutativityResult,
    MetricAxiomResult,
    MorphismCheckResult,
    MoveEdge,
    MoveGraph,
    OperationalPrice,
    OperationalPriceAtLevel,
    ProjectiveSystem,
    ThreadValidationResult,
    create_discrete_circle_movegraph,
    create_dyadic_coarsening_map,
    create_dyadic_movegraph,
    create_dyadic_projective_system,
    verify_commutativity,
)


# =============================================================================
# 1. MoveEdge & MoveGraph Tests
# =============================================================================


def test_move_edge_exact_rational_coercion() -> None:
    """MoveEdge coerces ints to exact Fractions and rejects float arguments."""
    e = MoveEdge(source=0, target=1, mu1=2, mu2=Fraction(1, 3))
    assert isinstance(e.mu1, Fraction)
    assert e.mu1 == Fraction(2, 1)
    assert e.mu2 == Fraction(1, 3)

    # Float rejection
    with pytest.raises(TypeError, match="exact rational"):
        MoveEdge(source=0, target=1, mu1=1.5)  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="exact rational"):
        MoveEdge(source=0, target=1, mu2=0.25)  # type: ignore[arg-type]

    # Negative cost rejection
    with pytest.raises(ValueError, match="non-negative"):
        MoveEdge(source=0, target=1, mu1=-1)

    with pytest.raises(ValueError, match="non-negative"):
        MoveEdge(source=0, target=1, mu2=Fraction(-1, 2))


def test_move_graph_construction_and_validation() -> None:
    """MoveGraph validates that all edge endpoints belong to states."""
    e1 = MoveEdge(source="A", target="B", mu1=1)
    e2 = MoveEdge(source="B", target="C", mu1=2)
    g = MoveGraph.build(level=0, states=["A", "B", "C"], edges=[e1, e2])

    assert g.level == 0
    assert g.state_count == 3
    assert g.edge_count == 2
    assert g.has_state("A")
    assert g.has_edge("A", "B")
    assert not g.has_edge("A", "C")
    assert g.outgoing("A") == (e1,)
    assert g.incoming("B") == (e1,)

    # Invalid edge with endpoint outside states
    bad_edge = MoveEdge(source="A", target="D", mu1=1)
    with pytest.raises(ValueError, match="not in graph states"):
        MoveGraph.build(level=0, states=["A", "B"], edges=[bad_edge])


# =============================================================================
# 2. CoarseningMap Identity & Composition Commutativity
# =============================================================================


def test_coarsening_map_identity_and_morphism() -> None:
    """Canonical identity coarsening map pi_{k, k} preserves all states and edges."""
    g = create_dyadic_movegraph(level=1, length=1)
    id_map = CoarseningMap.identity(g)

    assert id_map.source_level == 1
    assert id_map.target_level == 1

    for s in g.states:
        assert id_map.apply_state(s) == s

    for e in g.edges:
        assert id_map.apply_edge(e) == e

    check = id_map.check_morphism(g, g)
    assert check.is_valid
    assert not check.defects


def test_coarsening_map_composition_and_associativity() -> None:
    """Composition of coarsening maps satisfies (pi_01 o pi_12) == pi_02 and associativity."""
    g0 = create_dyadic_movegraph(level=0)
    g1 = create_dyadic_movegraph(level=1)
    g2 = create_dyadic_movegraph(level=2)
    g3 = create_dyadic_movegraph(level=3)

    pi_01 = create_dyadic_coarsening_map(0, 1)
    pi_12 = create_dyadic_coarsening_map(1, 2)
    pi_23 = create_dyadic_coarsening_map(2, 3)

    # Individual morphism validity
    assert pi_01.check_morphism(g1, g0).is_valid
    assert pi_12.check_morphism(g2, g1).is_valid
    assert pi_23.check_morphism(g3, g2).is_valid

    # Composite pi_02 = pi_01 o pi_12
    pi_02_comp = pi_01.compose(pi_12)
    pi_02_direct = create_dyadic_coarsening_map(0, 2)

    for s in g2.states:
        assert pi_02_comp.apply_state(s) == pi_02_direct.apply_state(s)

    # Associativity: (pi_01 o pi_12) o pi_23 == pi_01 o (pi_12 o pi_23)
    comp_left = (pi_01.compose(pi_12)).compose(pi_23)
    comp_right = pi_01.compose(pi_12.compose(pi_23))

    for s in g3.states:
        assert comp_left.apply_state(s) == comp_right.apply_state(s)


def test_functorial_commutativity_verifier() -> None:
    """verify_commutativity checks pi_{j, k} o pi_{k, m} == pi_{j, m} for j <= k <= m."""
    g2 = create_dyadic_movegraph(level=2)
    pi_01 = create_dyadic_coarsening_map(0, 1)
    pi_12 = create_dyadic_coarsening_map(1, 2)
    pi_02 = create_dyadic_coarsening_map(0, 2)

    res = verify_commutativity(pi_01, pi_12, pi_02, domain_graph=g2)
    assert res.commutes
    assert bool(res)
    assert res.levels == (0, 1, 2)
    assert not res.discrepancies


def test_functorial_commutativity_detects_mismatch() -> None:
    """verify_commutativity detects discrepancies when a direct bonding map diverges."""
    g2 = create_dyadic_movegraph(level=2)
    pi_01 = create_dyadic_coarsening_map(0, 1)
    pi_12 = create_dyadic_coarsening_map(1, 2)

    # Mutate direct map to create an intentional discrepancy
    divergent_state_map = dict(create_dyadic_coarsening_map(0, 2).state_map)
    divergent_state_map[4] = 99  # State 4 mapped to invalid state 99 instead of 1

    bad_pi_02 = CoarseningMap(
        source_level=2,
        target_level=0,
        state_map=divergent_state_map,
    )

    res = verify_commutativity(pi_01, pi_12, bad_pi_02, domain_graph=g2)
    assert not res.commutes
    assert not bool(res)
    assert any("State 4" in d for d in res.discrepancies)


# =============================================================================
# 3. ProjectiveSystem System Verification & Coherent Threads
# =============================================================================


def test_dyadic_projective_system_full_verification() -> None:
    """Dyadic projective system verifies across all levels: morphisms, identities, and commutativity."""
    sys = create_dyadic_projective_system(max_level=3, length=1)
    assert sys.levels == (0, 1, 2, 3)

    is_valid, defects = sys.verify_system()
    assert is_valid, f"System defects found: {defects}"
    assert not defects


def test_coherent_thread_validation_on_canonical_points() -> None:
    """Threads corresponding to dyadic continuum points [0, 1] validate as coherent."""
    sys = create_dyadic_projective_system(max_level=3, length=1)

    # Point 0: at level k, state is 0
    thread_zero = {k: 0 for k in range(4)}
    v_zero = sys.validate_thread(thread_zero)
    assert v_zero.is_coherent
    assert not v_zero.defects

    # Point 1: at level k, state is 2^k
    thread_one = {k: 2**k for k in range(4)}
    v_one = sys.validate_thread(thread_one)
    assert v_one.is_coherent
    assert not v_one.defects

    # Point 1/2:
    # Level 0: 0 // scale => 0
    # Level 1: 1
    # Level 2: 2 (since 2 // 2 = 1)
    # Level 3: 4 (since 4 // 4 = 1)
    thread_half = {0: 0, 1: 1, 2: 2, 3: 4}
    v_half = sys.validate_thread(thread_half)
    assert v_half.is_coherent
    assert not v_half.defects


def test_coherent_thread_enumeration() -> None:
    """enumerate_coherent_threads constructs all compatible threads in varprojlim M_k."""
    # Test on small system: levels 0 and 1
    sys = create_dyadic_projective_system(max_level=1, length=1)
    threads = sys.enumerate_coherent_threads()

    # Level 1 has 3 states: 0, 1, 2
    # Projection pi_{0, 1}(0) = 0, pi_{0, 1}(1) = 0, pi_{0, 1}(2) = 1
    # Hence exactly 3 coherent threads exist:
    # (0, 0), (0, 1), (1, 2)
    assert len(threads) == 3
    expected_threads = [
        {0: 0, 1: 0},
        {0: 0, 1: 1},
        {0: 1, 1: 2},
    ]
    assert list(threads) == expected_threads

    # Verify every enumerated thread passes validate_thread
    for th in threads:
        assert sys.validate_thread(th).is_coherent


def test_rejection_of_incoherent_threads() -> None:
    """validate_thread detects and rejects incoherent or ill-formed sequences."""
    sys = create_dyadic_projective_system(max_level=2, length=1)

    # Incoherent state choice: at level 2 choose 4 (which projects to 4//2=2 at level 1),
    # but specify 0 at level 1
    incoherent = {0: 0, 1: 0, 2: 4}
    res = sys.validate_thread(incoherent)
    assert not res.is_coherent
    assert any("Thread coherence failure" in d for d in res.defects)

    # State not in graph
    out_of_bounds = {0: 0, 1: 1, 2: 999}
    res_oob = sys.validate_thread(out_of_bounds)
    assert not res_oob.is_coherent
    assert any("not in M_2.states" in d for d in res_oob.defects)

    # Level not in system
    bad_level = {0: 0, 5: 1}
    res_bad_lvl = sys.validate_thread(bad_level)
    assert not res_bad_lvl.is_coherent
    assert any("not in the system" in d for d in res_bad_lvl.defects)


# =============================================================================
# 4. Operational Pricing & Endogenous Metric without Euclidean Coordinates
# =============================================================================


def test_operational_distance_and_path_pricing() -> None:
    """Operational pricing calculates exact rational sums (Sigma mu1, Sigma mu2)."""
    e1 = MoveEdge(source="A", target="B", mu1=Fraction(1, 2), mu2=Fraction(1, 4))
    e2 = MoveEdge(source="B", target="C", mu1=Fraction(3, 2), mu2=Fraction(3, 4))
    g = MoveGraph.build(level=0, states=["A", "B", "C"], edges=[e1, e2])
    sys = ProjectiveSystem.build(graphs=[g])

    path_price = sys.compute_path_pricing([e1, e2])
    assert path_price.mu1_sum == Fraction(2, 1)
    assert path_price.mu2_sum == Fraction(1, 1)
    assert path_price.step_count == 2

    # Shortest path distance via exact rational Dijkstra
    d_ac = sys.operational_distance(0, "A", "C")
    assert d_ac == Fraction(2, 1)

    # Unreachable state returns None
    g_disjoint = MoveGraph.build(level=0, states=["A", "B", "X"], edges=[e1])
    sys_disjoint = ProjectiveSystem.build(graphs=[g_disjoint])
    assert sys_disjoint.operational_distance(0, "A", "X") is None


def test_endogenous_metric_axioms_without_euclidean_coordinates() -> None:
    """Discrete movegraph satisfies metric axioms derived solely from path concatenation."""
    # Test on dyadic movegraph at level 2
    sys = create_dyadic_projective_system(max_level=2)
    metric_check = sys.verify_endogenous_metric(level=2)

    assert metric_check.satisfies_axioms
    assert not metric_check.defects
    assert metric_check.tested_pairs > 0
    assert metric_check.tested_triples > 0


def test_pricing_accumulation_along_projective_sequences() -> None:
    """Refinement path sequence exhibits macroscopic price invariance while dissipation decays."""
    sys = create_dyadic_projective_system(max_level=3, length=1)

    # Projective sequence of paths traversing from interval start (0) to end (2^k)
    paths: Dict[int, List[MoveEdge]] = {}
    for lvl in range(4):
        g = sys.graphs[lvl]
        p = []
        for i in range(2**lvl):
            # Forward edge i -> i+1
            edges = g.find_edges(i, i + 1)
            assert len(edges) > 0
            p.append(edges[0])
        paths[lvl] = p

    sequence = sys.pricing_along_path_sequence(paths)
    assert len(sequence) == 4

    # At every refinement level k:
    # Sigma mu1 = 2^k * (1 / 2^k) = 1 (exact rational macroscopic length invariant!)
    # Sigma mu2 = 2^k * (1 / 4^k) = 1 / 2^k (dissipation decreases geometrically to 0)
    for item in sequence:
        k = item.level
        assert item.price.mu1_sum == Fraction(1, 1)
        assert item.price.mu2_sum == Fraction(1, 2**k)

    # Verify stabilization of Sigma mu1
    stab = sys.verify_pricing_stabilization(sequence)
    assert stab["stabilized"]
    assert stab["max_delta"] == Fraction(0, 1)


def test_pricing_along_threads_sequence() -> None:
    """Operational distance between thread 0 and thread 1 across levels."""
    sys = create_dyadic_projective_system(max_level=3, length=1)

    thread_zero = {k: 0 for k in range(4)}
    thread_one = {k: 2**k for k in range(4)}

    thread_pricing = sys.pricing_along_threads(thread_zero, thread_one)
    assert len(thread_pricing) == 4

    # Distance between thread 0 and thread 1 is 1 at all levels
    for item in thread_pricing:
        assert item.price.mu1_sum == Fraction(1, 1)


# =============================================================================
# 5. Rejection of Incompatible and Non-Commuting Projection Families
# =============================================================================


def test_rejection_of_inverted_level_bonding_map() -> None:
    """CoarseningMap requires target_level <= source_level; rejects target_level > source_level."""
    with pytest.raises(ValueError, match="target_level <= source_level"):
        CoarseningMap(source_level=0, target_level=1, state_map={0: 0})


def test_rejection_of_non_morphic_bonding_map() -> None:
    """check_morphism rejects state maps that map transitions to non-edges."""
    g0 = create_dyadic_movegraph(level=0)
    g1 = create_dyadic_movegraph(level=1)

    # In g1, edge exists between 0 and 1.
    # If state_map maps 0 -> 0 and 1 -> 999 (not a state), it is rejected.
    bad_map_states = CoarseningMap(
        source_level=1,
        target_level=0,
        state_map={0: 0, 1: 999, 2: 1},
    )
    res_states = bad_map_states.check_morphism(g1, g0)
    assert not res_states.is_valid
    assert any("not in target graph states" in d for d in res_states.defects)

    # If state_map breaks edge structure:
    # Say g0 had disjoint states without edge, but edge mapped to it
    g_disconnected = MoveGraph.build(level=0, states=[0, 1], edges=[])
    normal_map = create_dyadic_coarsening_map(0, 1)
    res_edges = normal_map.check_morphism(g1, g_disconnected)
    assert not res_edges.is_valid
    assert any("not an edge in target graph" in d for d in res_edges.defects)


def test_rejection_of_non_commuting_projective_system() -> None:
    """verify_system detects when bonding maps do not satisfy functorial commutativity."""
    g0 = create_dyadic_movegraph(level=0)
    g1 = create_dyadic_movegraph(level=1)
    g2 = create_dyadic_movegraph(level=2)

    pi_01 = create_dyadic_coarsening_map(0, 1)
    pi_12 = create_dyadic_coarsening_map(1, 2)

    # Non-commuting direct map pi_02: map all states to 0 except state 4 to 0 (diverges from pi_01(pi_12(4))=1)
    broken_pi_02 = CoarseningMap(
        source_level=2,
        target_level=0,
        state_map={s: 0 for s in g2.states},  # maps all to 0!
    )

    sys_bad = ProjectiveSystem(
        graphs={0: g0, 1: g1, 2: g2},
        bonding_maps={
            (0, 0): CoarseningMap.identity(g0),
            (1, 1): CoarseningMap.identity(g1),
            (2, 2): CoarseningMap.identity(g2),
            (0, 1): pi_01,
            (1, 2): pi_12,
            (0, 2): broken_pi_02,
        },
    )

    is_valid, defects = sys_bad.verify_system()
    assert not is_valid
    assert any("Commutativity defect" in d for d in defects)
