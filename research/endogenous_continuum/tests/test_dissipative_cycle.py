"""Tests for Track 3 Dissipative Cycle Filtering.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest

from research.endogenous_continuum.dissipative_cycle import (
    AttractorClassification,
    AttractorClassifier,
    AutonomousStepper,
    CarrierGraph,
    Cycle,
    CycleDetector,
    PathResult,
    PruningReport,
    StateSpacePruner,
    Transition,
    canonical_cycle,
    deterministic_key,
)


def test_transition_exact_integers_enforced() -> None:
    t = Transition(source="A", target="B", mu1=3, mu2=1)
    assert t.mu1 == 3
    assert t.mu2 == 1

    with pytest.raises(TypeError):
        Transition(source="A", target="B", mu1=3.5, mu2=1)  # type: ignore

    with pytest.raises(TypeError):
        Transition(source="A", target="B", mu1=3, mu2=1.2)  # type: ignore

    with pytest.raises(TypeError):
        Transition(source="A", target="B", mu1=True, mu2=1)

    with pytest.raises(ValueError):
        Transition(source="A", target="B", mu1=3, mu2=0)

    with pytest.raises(ValueError):
        Transition(source="A", target="B", mu1=3, mu2=-2)


def test_carrier_graph_potential_exact_integers() -> None:
    g = CarrierGraph[str]()
    g.add_state("A", 10)
    g.add_state("B", 7)

    t = g.add_transition("A", "B", mu2=2)
    assert t.mu1 == 3
    assert t.mu2 == 2

    with pytest.raises(TypeError):
        g.add_state("C", 4.5)  # type: ignore

    with pytest.raises(ValueError):
        g.add_transition("A", "B", mu2=1, mu1=5)

    g.add_state("A", 10)
    with pytest.raises(ValueError, match="already has potential"):
        g.add_state("A", 11)


def test_cycle_validates_closed_path_and_aggregate_costs() -> None:
    ab = Transition(source="A", target="B", mu1=1, mu2=1)
    ba = Transition(source="B", target="A", mu1=-1, mu2=2)

    with pytest.raises(ValueError, match="closed state path"):
        Cycle(
            states=("A", "B"),
            transitions=(ba, ab),
            total_mu1=0,
            total_mu2=3,
            period=2,
        )

    with pytest.raises(ValueError, match="total_mu2"):
        Cycle(
            states=("A", "B"),
            transitions=(ab, ba),
            total_mu1=0,
            total_mu2=4,
            period=2,
        )


def test_stepper_rejects_foreign_edges_graphs_and_invalid_bounds() -> None:
    graph = CarrierGraph[str]()
    graph.add_state("A", 1)
    graph.add_state("B", 0)
    graph.add_transition("A", "B")
    foreign = Transition(source="A", target="A", mu1=0, mu2=1)
    bad_stepper = AutonomousStepper(graph, selection_rule=lambda _: foreign)
    with pytest.raises(ValueError, match="outside the current"):
        bad_stepper.step("A")

    normal_stepper = AutonomousStepper(graph)
    with pytest.raises(ValueError, match="positive int"):
        normal_stepper.run_trajectory("A", max_steps=0)

    other_graph = CarrierGraph[str]()
    other_graph.add_state("A", 0)
    with pytest.raises(ValueError, match="different CarrierGraph"):
        CycleDetector.find_all_cycles_autonomous(other_graph, normal_stepper)
    with pytest.raises(ValueError, match="different CarrierGraph"):
        StateSpacePruner.prune_to_attractor_core(other_graph, normal_stepper)


def test_acyclic_path_termination_finite_steps() -> None:
    """Test acyclic path termination in finite steps."""
    g = CarrierGraph[str]()
    potentials = {"S0": 20, "S1": 15, "S2": 11, "S3": 8, "S4": 2}
    for s, p in potentials.items():
        g.add_state(s, p)

    g.add_transition("S0", "S1", mu2=1)
    g.add_transition("S1", "S2", mu2=2)
    g.add_transition("S2", "S3", mu2=1)
    g.add_transition("S3", "S4", mu2=3)

    stepper = AutonomousStepper(g)
    res = stepper.run_trajectory("S0", max_steps=10)

    assert res.terminated is True
    assert res.entered_cycle is False
    assert res.cycle is None
    assert res.transient_length == 4
    assert res.trajectory == ("S0", "S1", "S2", "S3", "S4")
    assert res.total_mu1 == 18
    assert res.total_mu2 == 7


def test_conservation_of_potential_along_cycles() -> None:
    """Test conservation of potential along cycles (sum of mu1 == 0)."""
    g = CarrierGraph[str]()
    g.add_state("C0", 10)
    g.add_state("C1", 14)
    g.add_state("C2", 8)

    g.add_transition("C0", "C1", mu2=1)
    g.add_transition("C1", "C2", mu2=2)
    g.add_transition("C2", "C0", mu2=3)

    stepper = AutonomousStepper(g)
    res = stepper.run_trajectory("C0")

    assert res.entered_cycle is True
    assert res.cycle is not None
    cycle = res.cycle

    assert cycle.total_mu1 == 0
    assert cycle.is_conservative is True
    assert sum(t.mu1 for t in cycle.transitions) == 0


def test_positivity_of_activity_along_cycles() -> None:
    """Test positivity of activity along cycles (sum of mu2 > 0)."""
    g = CarrierGraph[str]()
    for s in ["E0", "E1", "E2"]:
        g.add_state(s, 5)

    g.add_transition("E0", "E1", mu2=2)
    g.add_transition("E1", "E2", mu2=4)
    g.add_transition("E2", "E0", mu2=1)

    stepper = AutonomousStepper(g)
    res = stepper.run_trajectory("E0")

    assert res.entered_cycle is True
    assert res.cycle is not None
    cycle = res.cycle

    assert cycle.period == 3
    assert cycle.total_mu1 == 0
    assert cycle.total_mu2 == 7
    assert cycle.is_active is True
    assert cycle.total_mu2 >= cycle.period >= 1


def test_state_space_pruning_purges_dead_ends() -> None:
    """Test state-space pruning correctly purges dead ends."""
    g = CarrierGraph[str]()
    g.add_state("C0", 10)
    g.add_state("C1", 10)
    g.add_state("D1", 8)
    g.add_state("D2", 5)
    g.add_state("D3", 1)

    g.add_transition("C0", "C1", mu2=1)
    g.add_transition("C1", "C0", mu2=1)
    g.add_transition("C1", "D1", mu2=1)
    g.add_transition("D1", "D2", mu2=1)
    g.add_transition("D2", "D3", mu2=1)

    pruned_graph, rounds = StateSpacePruner.prune_dead_ends(g)

    assert len(rounds) == 3
    assert rounds[0] == frozenset({"D3"})
    assert rounds[1] == frozenset({"D2"})
    assert rounds[2] == frozenset({"D1"})

    assert set(pruned_graph.states()) == {"C0", "C1"}
    assert pruned_graph.out_degree("C0") == 1
    assert pruned_graph.out_degree("C1") == 1


def test_state_space_pruning_isolates_attractor_core() -> None:
    """Test state-space pruning correctly isolates attractors and purges feeder branches."""
    g = CarrierGraph[str]()
    for s in ["T0", "T1", "C0", "C1", "C2", "D0", "D1"]:
        g.add_state(s, 10)

    g.add_transition("T0", "T1", mu2=1)
    g.add_transition("T1", "C0", mu2=1)
    g.add_transition("C0", "C1", mu2=1)
    g.add_transition("C1", "C2", mu2=1)
    g.add_transition("C2", "C0", mu2=1)
    g.add_transition("C2", "D0", mu2=1)
    g.add_transition("D0", "D1", mu2=1)

    core_graph, report = StateSpacePruner.prune_to_attractor_core(g)

    assert report.initial_state_count == 7
    assert report.final_state_count == 3
    assert report.retained_states == frozenset({"C0", "C1", "C2"})
    assert report.is_pure_cycle_core is True
    assert len(report.retained_cycles) == 1

    cycle = report.retained_cycles[0]
    assert cycle.period == 3
    assert cycle.is_conservative is True
    assert cycle.is_active is True


def test_purely_acyclic_graph_pruning_empties_core() -> None:
    g = CarrierGraph[str]()
    g.add_state("A", 3)
    g.add_state("B", 2)
    g.add_state("C", 1)
    g.add_transition("A", "B", mu2=1)
    g.add_transition("B", "C", mu2=1)

    core_graph, report = StateSpacePruner.prune_to_attractor_core(g)
    assert report.final_state_count == 0
    assert report.retained_states == frozenset()
    assert report.retained_cycles == ()
    assert report.is_pure_cycle_core is True


def test_self_loop_attractor() -> None:
    g = CarrierGraph[str]()
    g.add_state("S0", 42)
    g.add_transition("S0", "S0", mu2=5)

    stepper = AutonomousStepper(g)
    res = stepper.run_trajectory("S0")
    assert res.entered_cycle is True
    assert res.cycle is not None
    assert res.cycle.period == 1
    assert res.cycle.states == ("S0",)
    assert res.cycle.total_mu1 == 0
    assert res.cycle.total_mu2 == 5


def test_attractor_classification_basins() -> None:
    g = CarrierGraph[str]()
    for s in ["F1", "K1", "K2", "F2", "M1", "M2", "D1", "D2"]:
        g.add_state(s, 10)

    g.add_transition("F1", "K1", mu2=1)
    g.add_transition("K1", "K2", mu2=1)
    g.add_transition("K2", "K1", mu2=1)

    g.add_transition("F2", "M1", mu2=1)
    g.add_transition("M1", "M2", mu2=1)
    g.add_transition("M2", "M1", mu2=1)

    g.add_transition("D1", "D2", mu2=1)

    classification = AttractorClassifier.classify(g)

    assert len(classification.cycles) == 2
    assert classification.cycle_states == frozenset({"K1", "K2", "M1", "M2"})
    assert classification.transient_to_cycle_states == frozenset({"F1", "F2"})
    assert classification.transient_to_sink_states == frozenset({"D1"})
    assert classification.sink_states == frozenset({"D2"})

    assert classification.state_classification["K1"] == "cycle"
    assert classification.state_classification["F1"] == "transient_to_cycle"
    assert classification.state_classification["D1"] == "transient_to_sink"
    assert classification.state_classification["D2"] == "sink"


def test_deterministic_ordering_invariance() -> None:
    g1 = CarrierGraph[int]()
    g2 = CarrierGraph[int]()

    for i in [3, 1, 4, 2]:
        g1.add_state(i, i * 10)
    for i in [1, 2, 3, 4]:
        g2.add_state(i, i * 10)

    for s, t in [(1, 2), (2, 3), (3, 1), (4, 3)]:
        g1.add_transition(s, t, mu2=1)
        g2.add_transition(s, t, mu2=1)

    core1, rep1 = StateSpacePruner.prune_to_attractor_core(g1)
    core2, rep2 = StateSpacePruner.prune_to_attractor_core(g2)

    assert core1.states() == core2.states()
    assert rep1.retained_states == rep2.retained_states
    assert rep1.retained_cycles == rep2.retained_cycles
