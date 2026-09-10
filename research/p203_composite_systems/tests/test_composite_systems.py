"""Comprehensive test suite for Target P203: Composite Systems & Pre-Spatial Locality.

AuthorityEffect: None.
Tests:
1. Multi-locus carrier states and associative tensor composition.
2. Pre-spatial interaction graph derivation from read/write footprints.
3. Strict operational non-signaling across bipartite network cuts (TVD = 0.0).
4. Negative controls: leaky intervention and mediated coupling (TVD > 0).
5. Duplicate observer agreement and graph automorphism symmetry relations.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from composite_systems import (
    BipartiteCut,
    CarrierState,
    DuplicateObserverPair,
    InteractionGraph,
    Observable,
    Transition,
    compute_marginal_distribution,
    is_symmetric_state,
    total_variation_distance,
    verify_associativity_isomorphism,
    verify_duplicate_observer_agreement,
    verify_leaky_intervention_divergence,
    verify_mediated_coupling_divergence,
    verify_operational_non_signaling,
)


class TestTensorCompositionAssociativity:
    """Tests for multi-locus carrier networks and associative composition."""

    def test_tensor_disjoint_composition(self) -> None:
        s_a = CarrierState({"a1": 1, "a2": 2})
        s_b = CarrierState({"b1": 3, "b2": 4})
        s_ab = s_a.tensor(s_b)

        assert s_ab.loci == frozenset({"a1", "a2", "b1", "b2"})
        assert s_ab["a1"] == 1
        assert s_ab["a2"] == 2
        assert s_ab["b1"] == 3
        assert s_ab["b2"] == 4

    def test_tensor_overlapping_loci_raises_error(self) -> None:
        s_a = CarrierState({"x": 1, "y": 2})
        s_b = CarrierState({"y": 3, "z": 4})
        with pytest.raises(ValueError, match="overlapping loci"):
            s_a.tensor(s_b)

    def test_associativity_isomorphism(self) -> None:
        s_a = CarrierState({"a1": 10, "a2": 20})
        s_b = CarrierState({"b1": 30, "b2": 40})
        s_c = CarrierState({"c1": 50, "c2": 60})

        res = verify_associativity_isomorphism(s_a, s_b, s_c)
        assert res["associativity_satisfied"] is True
        assert res["identical_valuations"] is True
        assert res["proj_a_preserved"] is True
        assert res["proj_b_preserved"] is True
        assert res["proj_c_preserved"] is True

    def test_subsystem_projections(self) -> None:
        state = CarrierState({"a1": 1, "a2": 2, "b1": 3, "b2": 4, "c1": 5})
        proj_a = state.project(["a1", "a2"])
        assert proj_a.values == {"a1": 1, "a2": 2}

        proj_b = state.project(["b1", "b2"])
        assert proj_b.values == {"b1": 3, "b2": 4}

        proj_empty = state.project([])
        assert proj_empty.values == {}


class TestPreSpatialInteractionGraph:
    """Tests for interaction graph derivation from read/write footprints."""

    def test_derive_from_operations(self) -> None:
        loci = ["a1", "a2", "b1", "b2"]
        # Operation 1: coupling a1 -> a2 (read a1, write a2)
        op1 = Transition(
            name="couple_a1_a2",
            reads=frozenset({"a1"}),
            writes=frozenset({"a2"}),
            transform=lambda s: {"a2": s["a1"]},
        )
        # Operation 2: coupling b1 -> b2 (read b1, write b2)
        op2 = Transition(
            name="couple_b1_b2",
            reads=frozenset({"b1"}),
            writes=frozenset({"b2"}),
            transform=lambda s: {"b2": s["b1"]},
        )
        graph = InteractionGraph.derive_from_operations(loci, [op1, op2])

        assert graph.vertices == frozenset(loci)
        assert frozenset({"a1", "a2"}) in graph.edges
        assert frozenset({"b1", "b2"}) in graph.edges
        assert frozenset({"a2", "b1"}) not in graph.edges

        # Subsystems A and B are disconnected
        assert graph.shortest_path_distance("a1", "b2") is None
        assert graph.are_connected("a1", "b1") is False

        comps = graph.connected_components()
        assert len(comps) == 2
        assert frozenset({"a1", "a2"}) in comps
        assert frozenset({"b1", "b2"}) in comps

    def test_bridge_transition_creates_path(self) -> None:
        loci = ["a1", "a2", "b1", "b2"]
        op1 = Transition(
            name="couple_a1_a2",
            reads=frozenset({"a1"}),
            writes=frozenset({"a2"}),
            transform=lambda s: {"a2": s["a1"]},
        )
        op_bridge = Transition(
            name="bridge_a2_b1",
            reads=frozenset({"a2"}),
            writes=frozenset({"b1"}),
            transform=lambda s: {"b1": s["a2"]},
        )
        op2 = Transition(
            name="couple_b1_b2",
            reads=frozenset({"b1"}),
            writes=frozenset({"b2"}),
            transform=lambda s: {"b2": s["b1"]},
        )
        graph = InteractionGraph.derive_from_operations(loci, [op1, op_bridge, op2])

        assert graph.are_connected("a1", "b2") is True
        assert graph.shortest_path_distance("a1", "a2") == 1
        assert graph.shortest_path_distance("a1", "b1") == 2
        assert graph.shortest_path_distance("a1", "b2") == 3

    def test_graph_automorphism_verification(self) -> None:
        loci = ["a1", "a2", "b1", "b2"]
        # Symmetric 4-vertex graph: a1 - a2, b1 - b2, with bridge a2 - b1 and loop-back a1 - b2
        op_a = Transition("a", frozenset({"a1"}), frozenset({"a2"}), lambda s: {"a2": s["a1"]})
        op_b = Transition("b", frozenset({"b1"}), frozenset({"b2"}), lambda s: {"b2": s["b1"]})
        op_bridge1 = Transition("br1", frozenset({"a2"}), frozenset({"b1"}), lambda s: {"b1": s["a2"]})
        op_bridge2 = Transition("br2", frozenset({"a1"}), frozenset({"b2"}), lambda s: {"b2": s["a1"]})

        graph = InteractionGraph.derive_from_operations(loci, [op_a, op_b, op_bridge1, op_bridge2])

        # Permutation swapping A <-> B: a1 <-> b2, a2 <-> b1
        automorphism = {"a1": "b2", "a2": "b1", "b1": "a2", "b2": "a1"}
        assert graph.is_automorphism(automorphism) is True

        # Non-automorphism permutation: maps a1 to a2, breaking cycle structure
        invalid_perm = {"a1": "a2", "a2": "a1", "b1": "b2", "b2": "b1"}
        assert graph.is_automorphism(invalid_perm) is True  # also an automorphism (swap within parts)

        broken_perm = {"a1": "b1", "a2": "a1", "b1": "a2", "b2": "b2"}
        assert graph.is_automorphism(broken_perm) is False


class TestOperationalNonSignaling:
    """Tests for strict operational non-signaling across bipartite network cuts."""

    @pytest.fixture
    def network_setup(self) -> tuple[BipartiteCut, list[CarrierState], Observable]:
        cut = BipartiteCut(
            part_a=frozenset({"a1", "a2"}),
            part_b=frozenset({"b1", "b2"}),
        )
        # Ensemble of 100 correlated states
        ensemble = [
            CarrierState({
                "a1": i % 4,
                "a2": (i * 2) % 4,
                "b1": (i + 1) % 4,
                "b2": (i * 3) % 4,
            })
            for i in range(100)
        ]
        # Observable strictly on Part B
        obs_b = Observable(
            name="joint_readout_B",
            footprint=frozenset({"b1", "b2"}),
            measure=lambda s: (s["b1"], s["b2"]),
        )
        return cut, ensemble, obs_b

    def test_strict_non_signaling_tvd_zero(
        self, network_setup: tuple[BipartiteCut, list[CarrierState], Observable]
    ) -> None:
        cut, ensemble, obs_b = network_setup

        interventions_a = [
            Transition(
                name="const_write_a1",
                reads=frozenset({"a1"}),
                writes=frozenset({"a1"}),
                transform=lambda s: {"a1": 99},
            ),
            Transition(
                name="bit_invert_a2",
                reads=frozenset({"a2"}),
                writes=frozenset({"a2"}),
                transform=lambda s: {"a2": 3 - s["a2"]},
            ),
            Transition(
                name="joint_permute_a1_a2",
                reads=frozenset({"a1", "a2"}),
                writes=frozenset({"a1", "a2"}),
                transform=lambda s: {"a1": (s["a1"] + s["a2"]) % 4, "a2": (s["a1"] * 2) % 4},
            ),
        ]

        report = verify_operational_non_signaling(ensemble, cut, interventions_a, obs_b)
        assert report["non_signaling_satisfied"] is True
        assert report["max_tvd"] == Fraction(0, 1)
        for name in report["interventions_tested"]:
            assert report["tvd_by_intervention"][name] == Fraction(0, 1)

    def test_invalid_intervention_leak_raises_error(
        self, network_setup: tuple[BipartiteCut, list[CarrierState], Observable]
    ) -> None:
        cut, ensemble, obs_b = network_setup
        leaky_op = Transition(
            name="leaky_op",
            reads=frozenset({"a1"}),
            writes=frozenset({"b1"}),
            transform=lambda s: {"b1": s["a1"]},
        )
        with pytest.raises(ValueError, match="leaks outside Part A"):
            verify_operational_non_signaling(ensemble, cut, [leaky_op], obs_b)

    def test_negative_control_leaky_footprint(
        self, network_setup: tuple[BipartiteCut, list[CarrierState], Observable]
    ) -> None:
        cut, ensemble, obs_b = network_setup
        leaky_intervention = Transition(
            name="leaky_intervention",
            reads=frozenset({"a1"}),
            writes=frozenset({"b1"}),
            transform=lambda s: {"b1": (s["b1"] + 1) % 4},
        )
        tvd = verify_leaky_intervention_divergence(ensemble, cut, leaky_intervention, obs_b)
        assert tvd > Fraction(0, 1)

    def test_negative_control_mediated_causal_signaling(
        self, network_setup: tuple[BipartiteCut, list[CarrierState], Observable]
    ) -> None:
        cut, ensemble, obs_b = network_setup
        intervention_a = Transition(
            name="set_a1_extreme",
            reads=frozenset({"a1"}),
            writes=frozenset({"a1"}),
            transform=lambda s: {"a1": 7},
        )
        mediating_relay = Transition(
            name="relay_a1_to_b1",
            reads=frozenset({"a1"}),
            writes=frozenset({"b1"}),
            transform=lambda s: {"b1": s["a1"]},
        )
        tvd = verify_mediated_coupling_divergence(
            ensemble, cut, intervention_a, mediating_relay, obs_b
        )
        assert tvd > Fraction(0, 1)


class TestDuplicateObserversAndAutomorphismInvariance:
    """Tests for duplicate observer agreement and symmetry invariance under graph automorphisms."""

    def test_duplicate_observer_agreement_on_symmetric_ensemble(self) -> None:
        # Automorphism exchanging a1 <-> b1 and a2 <-> b2
        automorphism = {"a1": "b1", "b1": "a1", "a2": "b2", "b2": "a2"}

        # Mixed ensemble: 80 symmetric states, 20 asymmetric states
        symmetric_states = [
            CarrierState({"a1": i % 3, "a2": (i * 2) % 3, "b1": i % 3, "b2": (i * 2) % 3})
            for i in range(80)
        ]
        asymmetric_states = [
            CarrierState({"a1": 0, "a2": 1, "b1": 2, "b2": 0})
            for _ in range(20)
        ]
        ensemble = symmetric_states + asymmetric_states

        obs_pair = DuplicateObserverPair(
            locus_u="a1",
            locus_v="b1",
            readout_probe=lambda val: val * 10,
        )

        report = verify_duplicate_observer_agreement(ensemble, obs_pair, automorphism)
        assert report["duplicate_agreement_satisfied"] is True
        assert report["symmetric_count"] == 80
        assert report["symmetric_agreement_rate"] == Fraction(1, 1)
        assert report["asymmetric_count"] == 20
        assert report["asymmetric_divergence_rate"] == Fraction(1, 1)

    def test_automorphism_distance_invariance(self) -> None:
        loci = ["a1", "a2", "b1", "b2"]
        op1 = Transition("1", frozenset({"a1"}), frozenset({"a2"}), lambda s: {"a2": s["a1"]})
        op2 = Transition("2", frozenset({"a2"}), frozenset({"b1"}), lambda s: {"b1": s["a2"]})
        op3 = Transition("3", frozenset({"b1"}), frozenset({"b2"}), lambda s: {"b2": s["b1"]})

        graph = InteractionGraph.derive_from_operations(loci, [op1, op2, op3])

        # Reversal automorphism: a1 <-> b2, a2 <-> b1
        reversal = {"a1": "b2", "a2": "b1", "b1": "a2", "b2": "a1"}
        assert graph.is_automorphism(reversal) is True

        for u in loci:
            for v in loci:
                d_orig = graph.shortest_path_distance(u, v)
                d_mapped = graph.shortest_path_distance(reversal[u], reversal[v])
                assert d_orig == d_mapped
