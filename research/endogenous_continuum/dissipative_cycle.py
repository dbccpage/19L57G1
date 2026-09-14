"""Target Endogenous Continuum: Track 3 Dissipative Cycle Filtering.

AuthorityEffect: None.

Discrete carrier transition dynamics with:
1. Integer potential function Phi: S -> int.
2. Dual operational cost measures:
   mu1 (potential drop): mu1(u, v) = Phi(u) - Phi(v) in int.
   mu2 (operational activity cost): mu2(u, v) >= 1 in int.
3. Cycle detection and attractor classification:
   Conservative-potential cycles: closed loop mu1 == 0, closed loop mu2 > 0.
   Transient acyclic branches and dead-end sinks.
4. State-space pruning engine:
   Iteratively strips transient acyclic sinks and branches to isolate
   the cycle attractor core.

All calculations use exact integer arithmetic with strict typing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generic, Hashable, Sequence, TypeVar

S = TypeVar("S", bound=Hashable)


def deterministic_key(state: Any) -> str:
    """Produce a deterministic string key for stable ordering across runs."""
    if isinstance(state, (int, str)):
        return f"{type(state).__name__}:{state}"
    if isinstance(state, tuple):
        inner = ",".join(deterministic_key(x) for x in state)
        return f"tuple:({inner})"
    return f"{type(state).__name__}:{repr(state)}"


@dataclass(frozen=True)
class Transition(Generic[S]):
    """Directed transition between carrier states.

    mu1 represents the potential drop Phi(source) - Phi(target).
    mu2 represents the operational activity cost expended in the transition.
    """

    source: S
    target: S
    mu1: int
    mu2: int
    action_label: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.mu1, int) or isinstance(self.mu1, bool):
            raise TypeError(f"mu1 must be an int, got {type(self.mu1)}")
        if not isinstance(self.mu2, int) or isinstance(self.mu2, bool):
            raise TypeError(f"mu2 must be an int, got {type(self.mu2)}")
        if self.mu2 < 1:
            raise ValueError(f"mu2 activity cost must be >= 1, got {self.mu2}")


@dataclass(frozen=True)
class Cycle(Generic[S]):
    """Directed cycle attractor in the carrier transition graph.

    Represents a periodic orbit satisfying potential conservation and positive activity.
    """

    states: tuple[S, ...]
    transitions: tuple[Transition[S], ...]
    total_mu1: int
    total_mu2: int
    period: int

    def __post_init__(self) -> None:
        if isinstance(self.total_mu1, float) or not isinstance(self.total_mu1, int) or isinstance(self.total_mu1, bool):
            raise TypeError(f"total_mu1 must be an int, got {type(self.total_mu1)}")
        if isinstance(self.total_mu2, float) or not isinstance(self.total_mu2, int) or isinstance(self.total_mu2, bool):
            raise TypeError(f"total_mu2 must be an int, got {type(self.total_mu2)}")
        if isinstance(self.period, float) or not isinstance(self.period, int) or isinstance(self.period, bool):
            raise TypeError(f"period must be an int, got {type(self.period)}")
        if self.total_mu1 != 0:
            raise ValueError(f"Broken cycle: net potential ∮ μ1 must be 0, got {self.total_mu1}")
        if self.total_mu2 <= 0:
            raise ValueError(f"Cycle must have strictly positive operational activity (∮ μ2 > 0), got {self.total_mu2}")
        if self.period <= 0:
            raise ValueError(f"Cycle period must be >= 1, got {self.period}")
        if len(self.states) != self.period:
            raise ValueError(f"Cycle period {self.period} does not match states length {len(self.states)}")

    def __hash__(self) -> int:
        return hash((self.states, self.total_mu1, self.total_mu2, self.period))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cycle):
            return False
        return (
            self.states == other.states
            and self.total_mu1 == other.total_mu1
            and self.total_mu2 == other.total_mu2
            and self.period == other.period
        )

    @property
    def is_conservative(self) -> bool:
        """Return True if closed-path potential drop sums to 0."""
        return self.total_mu1 == 0

    @property
    def is_active(self) -> bool:
        """Return True if operational activity cost is strictly positive."""
        return self.total_mu2 > 0


@dataclass(frozen=True)
class PathResult(Generic[S]):
    """Outcome of an autonomous stepping trajectory."""

    initial_state: S
    trajectory: tuple[S, ...]
    transitions: tuple[Transition[S], ...]
    total_mu1: int
    total_mu2: int
    terminated: bool
    entered_cycle: bool
    cycle: Cycle[S] | None
    transient_length: int


@dataclass(frozen=True)
class AttractorClassification(Generic[S]):
    """Partition of carrier states into attractors and transient components."""

    cycles: tuple[Cycle[S], ...]
    cycle_states: frozenset[S]
    transient_to_cycle_states: frozenset[S]
    transient_to_sink_states: frozenset[S]
    sink_states: frozenset[S]
    state_classification: dict[S, str]
    cycle_basins: dict[Cycle[S], frozenset[S]]


@dataclass(frozen=True)
class PruningReport(Generic[S]):
    """Telemetry report emitted by the state-space pruning engine."""

    initial_state_count: int
    final_state_count: int
    sink_pruning_rounds: tuple[frozenset[S], ...]
    branch_pruning_rounds: tuple[frozenset[S], ...]
    retained_states: frozenset[S]
    retained_cycles: tuple[Cycle[S], ...]
    is_pure_cycle_core: bool


class CarrierGraph(Generic[S]):
    """Carrier transition graph equipped with integer potentials and cost measures."""

    def __init__(self) -> None:
        self._potentials: dict[S, int] = {}
        self._out_edges: dict[S, list[Transition[S]]] = {}
        self._in_edges: dict[S, list[Transition[S]]] = {}

    def add_state(self, state: S, potential: int) -> None:
        """Register a state with an exact integer potential Phi."""
        if not isinstance(potential, int) or isinstance(potential, bool):
            raise TypeError(f"Potential Phi must be an int, got {type(potential)}")
        self._potentials[state] = potential
        if state not in self._out_edges:
            self._out_edges[state] = []
        if state not in self._in_edges:
            self._in_edges[state] = []

    def add_transition(
        self,
        source: S,
        target: S,
        mu2: int = 1,
        action_label: str = "",
        mu1: int | None = None,
    ) -> Transition[S]:
        """Add directed transition with verified potential drop mu1 and activity cost mu2."""
        if source not in self._potentials:
            raise KeyError(f"Source state {source} not registered in CarrierGraph")
        if target not in self._potentials:
            raise KeyError(f"Target state {target} not registered in CarrierGraph")

        expected_mu1 = self._potentials[source] - self._potentials[target]
        if mu1 is not None and mu1 != expected_mu1:
            raise ValueError(
                f"Explicit mu1 {mu1} does not match potential drop {expected_mu1}"
            )

        trans = Transition(
            source=source,
            target=target,
            mu1=expected_mu1,
            mu2=mu2,
            action_label=action_label,
        )
        self._out_edges[source].append(trans)
        self._in_edges[target].append(trans)
        return trans

    def get_potential(self, state: S) -> int:
        """Retrieve potential Phi(state)."""
        if state not in self._potentials:
            raise KeyError(f"State {state} not found in CarrierGraph")
        return self._potentials[state]

    def has_state(self, state: S) -> bool:
        """Return True if state is registered in the graph."""
        return state in self._potentials

    def states(self) -> tuple[S, ...]:
        """Return all registered states sorted by deterministic key."""
        return tuple(sorted(self._potentials.keys(), key=deterministic_key))

    def transitions(self, source: S) -> tuple[Transition[S], ...]:
        """Return outgoing transitions for source state sorted deterministically."""
        edges = self._out_edges.get(source, [])
        return tuple(
            sorted(
                edges,
                key=lambda t: (
                    0 - t.mu1,
                    t.mu2,
                    deterministic_key(t.target),
                    t.action_label,
                ),
            )
        )

    def incoming_transitions(self, target: S) -> tuple[Transition[S], ...]:
        """Return incoming transitions for target state sorted deterministically."""
        edges = self._in_edges.get(target, [])
        return tuple(
            sorted(
                edges,
                key=lambda t: (
                    0 - t.mu1,
                    t.mu2,
                    deterministic_key(t.source),
                    t.action_label,
                ),
            )
        )

    def all_transitions(self) -> tuple[Transition[S], ...]:
        """Return all transitions in graph sorted deterministically."""
        out: list[Transition[S]] = []
        for s in self.states():
            out.extend(self.transitions(s))
        return tuple(out)

    def successors(self, source: S) -> tuple[S, ...]:
        """Return successor states of source."""
        return tuple(t.target for t in self.transitions(source))

    def predecessors(self, target: S) -> tuple[S, ...]:
        """Return predecessor states of target."""
        return tuple(t.source for t in self.incoming_transitions(target))

    def out_degree(self, state: S) -> int:
        """Number of outgoing transitions from state."""
        return len(self._out_edges.get(state, []))

    def in_degree(self, state: S) -> int:
        """Number of incoming transitions to state."""
        return len(self._in_edges.get(state, []))

    def is_sink(self, state: S) -> bool:
        """Check if state is a dead-end sink with out_degree == 0."""
        return self.out_degree(state) == 0

    def is_source(self, state: S) -> bool:
        """Check if state is an entry point with in_degree == 0."""
        return self.in_degree(state) == 0

    def induced_subgraph(self, subset: Sequence[S] | set[S] | frozenset[S]) -> CarrierGraph[S]:
        """Construct the induced subgraph on a subset of states."""
        sub = CarrierGraph[S]()
        subset_set = set(subset)
        for s in subset:
            if s in self._potentials:
                sub.add_state(s, self._potentials[s])
        for s in subset:
            if s in self._out_edges:
                for t in self._out_edges[s]:
                    if t.target in subset_set:
                        sub.add_transition(
                            source=t.source,
                            target=t.target,
                            mu2=t.mu2,
                            action_label=t.action_label,
                        )
        return sub


def canonical_cycle(states: Sequence[S], transitions: Sequence[Transition[S]]) -> Cycle[S]:
    """Construct canonical Cycle by cyclically rotating to the minimal state."""
    if not states:
        raise ValueError("Cycle cannot be empty")
    if len(states) != len(transitions):
        raise ValueError("Number of cycle states must match number of transitions")

    keys = [deterministic_key(s) for s in states]
    min_idx = min(range(len(keys)), key=lambda i: keys[i])

    rot_states = tuple(states[min_idx:] + states[:min_idx])
    rot_trans = tuple(transitions[min_idx:] + transitions[:min_idx])
    total_mu1 = sum(t.mu1 for t in rot_trans)
    total_mu2 = sum(t.mu2 for t in rot_trans)

    return Cycle(
        states=rot_states,
        transitions=rot_trans,
        total_mu1=total_mu1,
        total_mu2=total_mu2,
        period=len(rot_states),
    )


class AutonomousStepper(Generic[S]):
    """Autonomous stepping engine executing deterministic dynamics on carrier graphs."""

    def __init__(
        self,
        graph: CarrierGraph[S],
        selection_rule: Callable[[tuple[Transition[S], ...]], Transition[S]] | None = None,
    ) -> None:
        self.graph = graph
        self.selection_rule = selection_rule or self._default_rule

    @staticmethod
    def _default_rule(edges: tuple[Transition[S], ...]) -> Transition[S]:
        """Deterministic selection: highest potential drop, then lowest mu2, then sorted target."""
        return edges[0]

    def step(self, state: S) -> Transition[S] | None:
        """Compute next autonomous step. Returns None if state is a dead-end sink."""
        edges = self.graph.transitions(state)
        if not edges:
            return None
        return self.selection_rule(edges)

    def run_trajectory(self, initial_state: S, max_steps: int = 1000) -> PathResult[S]:
        """Execute stepping trajectory from initial_state until sink termination or cycle entry."""
        if not self.graph.has_state(initial_state):
            raise KeyError(f"Initial state {initial_state} not found in graph")

        visited_order: dict[S, int] = {initial_state: 0}
        path_states: list[S] = [initial_state]
        path_transitions: list[Transition[S]] = []

        curr = initial_state
        step_idx = 0

        while step_idx < max_steps:
            t = self.step(curr)
            if t is None:
                tot_mu1 = sum(e.mu1 for e in path_transitions)
                tot_mu2 = sum(e.mu2 for e in path_transitions)
                return PathResult(
                    initial_state=initial_state,
                    trajectory=tuple(path_states),
                    transitions=tuple(path_transitions),
                    total_mu1=tot_mu1,
                    total_mu2=tot_mu2,
                    terminated=True,
                    entered_cycle=False,
                    cycle=None,
                    transient_length=len(path_transitions),
                )

            path_transitions.append(t)
            nxt = t.target
            curr = nxt
            step_idx += 1

            if nxt in visited_order:
                cycle_start = visited_order[nxt]
                cycle_states = path_states[cycle_start:]
                cycle_edges = path_transitions[cycle_start:]
                detected_cycle = canonical_cycle(cycle_states, cycle_edges)

                tot_mu1 = sum(e.mu1 for e in path_transitions)
                tot_mu2 = sum(e.mu2 for e in path_transitions)
                return PathResult(
                    initial_state=initial_state,
                    trajectory=tuple(path_states),
                    transitions=tuple(path_transitions),
                    total_mu1=tot_mu1,
                    total_mu2=tot_mu2,
                    terminated=False,
                    entered_cycle=True,
                    cycle=detected_cycle,
                    transient_length=cycle_start,
                )

            visited_order[nxt] = step_idx
            path_states.append(nxt)

        tot_mu1 = sum(e.mu1 for e in path_transitions)
        tot_mu2 = sum(e.mu2 for e in path_transitions)
        return PathResult(
            initial_state=initial_state,
            trajectory=tuple(path_states),
            transitions=tuple(path_transitions),
            total_mu1=tot_mu1,
            total_mu2=tot_mu2,
            terminated=False,
            entered_cycle=False,
            cycle=None,
            transient_length=len(path_transitions),
        )


def find_all_cycles_autonomous(
    graph: CarrierGraph[S],
    stepper: AutonomousStepper[S] | None = None,
) -> tuple[Cycle[S], ...]:
    """Identify all unique cycles reachable under autonomous stepping dynamics."""
    if stepper is None:
        stepper = AutonomousStepper(graph)

    detected_map: dict[tuple[S, ...], Cycle[S]] = {}
    all_states = graph.states()
    max_bound = len(all_states) + 2

    for s in all_states:
        res = stepper.run_trajectory(s, max_steps=max_bound)
        if res.entered_cycle and res.cycle is not None:
            detected_map[res.cycle.states] = res.cycle

    sorted_cycles = sorted(
        detected_map.values(),
        key=lambda c: (c.period, deterministic_key(c.states[0])),
    )
    return tuple(sorted_cycles)


class CycleDetector(Generic[S]):
    """Detects directed cycles in carrier graphs."""

    find_all_cycles_autonomous = staticmethod(find_all_cycles_autonomous)


class AttractorClassifier(Generic[S]):
    """Classifies carrier states into attractors, transient branches, and sinks."""

    @staticmethod
    def classify(
        graph: CarrierGraph[S],
        stepper: AutonomousStepper[S] | None = None,
    ) -> AttractorClassification[S]:
        """Classify every state under autonomous stepping dynamics."""
        if stepper is None:
            stepper = AutonomousStepper(graph)

        all_states = graph.states()
        max_bound = len(all_states) + 2

        cycles = CycleDetector.find_all_cycles_autonomous(graph, stepper)
        cycle_state_set: set[S] = set()
        for c in cycles:
            cycle_state_set.update(c.states)

        transient_to_cycle: set[S] = set()
        transient_to_sink: set[S] = set()
        sinks: set[S] = set()
        class_map: dict[S, str] = {}
        basins: dict[Cycle[S], set[S]] = {c: set() for c in cycles}

        for s in all_states:
            if graph.is_sink(s):
                sinks.add(s)

            res = stepper.run_trajectory(s, max_steps=max_bound)
            if res.entered_cycle and res.cycle is not None:
                basins[res.cycle].add(s)
                if s in cycle_state_set:
                    class_map[s] = "cycle"
                else:
                    transient_to_cycle.add(s)
                    class_map[s] = "transient_to_cycle"
            elif res.terminated:
                if graph.is_sink(s):
                    if graph.in_degree(s) == 0:
                        class_map[s] = "isolated"
                    else:
                        class_map[s] = "sink"
                else:
                    transient_to_sink.add(s)
                    class_map[s] = "transient_to_sink"
            else:
                class_map[s] = "unresolved"

        return AttractorClassification(
            cycles=cycles,
            cycle_states=frozenset(cycle_state_set),
            transient_to_cycle_states=frozenset(transient_to_cycle),
            transient_to_sink_states=frozenset(transient_to_sink),
            sink_states=frozenset(sinks),
            state_classification=class_map,
            cycle_basins={c: frozenset(b) for c, b in basins.items()},
        )


class StateSpacePruner(Generic[S]):
    """Iterative pruning engine stripping dead-end sinks and transient branches."""

    @staticmethod
    def _strip_by_predicate(
        graph: CarrierGraph[S],
        predicate: Callable[[CarrierGraph[S], S], bool],
    ) -> tuple[CarrierGraph[S], frozenset[S]]:
        """Single pass removing states matching the given predicate."""
        purged = frozenset(s for s in graph.states() if predicate(graph, s))
        if not purged:
            return graph, purged
        retained = [s for s in graph.states() if s not in purged]
        return graph.induced_subgraph(retained), purged

    @classmethod
    def strip_sinks_single_round(
        cls,
        graph: CarrierGraph[S],
    ) -> tuple[CarrierGraph[S], frozenset[S]]:
        """Single pass removing states with out_degree == 0."""
        return cls._strip_by_predicate(graph, lambda g, s: g.is_sink(s))

    @classmethod
    def strip_transient_sources_single_round(
        cls,
        graph: CarrierGraph[S],
    ) -> tuple[CarrierGraph[S], frozenset[S]]:
        """Single pass removing states with in_degree == 0."""
        return cls._strip_by_predicate(graph, lambda g, s: g.is_source(s))

    @classmethod
    def _prune_iterative(
        cls,
        graph: CarrierGraph[S],
        strip_fn: Callable[[CarrierGraph[S]], tuple[CarrierGraph[S], frozenset[S]]],
    ) -> tuple[CarrierGraph[S], list[frozenset[S]]]:
        """Iteratively strip states using strip_fn until a fixed point is reached."""
        current = graph
        rounds: list[frozenset[S]] = []
        while True:
            current, purged = strip_fn(current)
            if not purged:
                break
            rounds.append(purged)
        return current, rounds

    @classmethod
    def prune_dead_ends(
        cls,
        graph: CarrierGraph[S],
    ) -> tuple[CarrierGraph[S], list[frozenset[S]]]:
        """Iteratively remove dead-end sinks until all remaining states have out_degree >= 1."""
        return cls._prune_iterative(graph, cls.strip_sinks_single_round)

    @classmethod
    def prune_transient_branches(
        cls,
        graph: CarrierGraph[S],
    ) -> tuple[CarrierGraph[S], list[frozenset[S]]]:
        """Iteratively remove source states until all remaining states have in_degree >= 1."""
        return cls._prune_iterative(graph, cls.strip_transient_sources_single_round)

    @classmethod
    def prune_to_attractor_core(
        cls,
        graph: CarrierGraph[S],
        stepper: AutonomousStepper[S] | None = None,
    ) -> tuple[CarrierGraph[S], PruningReport[S]]:
        """Isolate the cycle attractor core by stripping dead ends and transient feeders.

        1. Iteratively purges dead ends (out_degree == 0).
        2. In autonomous dynamics, applies autonomous transition selection.
        3. Iteratively purges transient feeder branches (in_degree == 0).
        """
        initial_count = len(graph.states())

        # Step 1: purge all dead ends
        no_sinks_graph, sink_rounds = cls.prune_dead_ends(graph)

        # Step 2: if stepper or autonomous, construct autonomous transition graph
        if stepper is not None or any(no_sinks_graph.out_degree(s) > 1 for s in no_sinks_graph.states()):
            auto_stepper = stepper or AutonomousStepper(no_sinks_graph)
            auto_graph = CarrierGraph[S]()
            for s in no_sinks_graph.states():
                auto_graph.add_state(s, no_sinks_graph.get_potential(s))
            for s in no_sinks_graph.states():
                t = auto_stepper.step(s)
                if t is not None:
                    auto_graph.add_transition(
                        source=t.source,
                        target=t.target,
                        mu2=t.mu2,
                        action_label=t.action_label,
                    )
            current_stage = auto_graph
        else:
            current_stage = no_sinks_graph

        # Step 3: purge transient entry branches (sources)
        core_graph, branch_rounds = cls.prune_transient_branches(current_stage)

        # Identify cycles in the remaining core
        core_cycles = CycleDetector.find_all_cycles_autonomous(core_graph)
        cycle_states_union: set[S] = set()
        for c in core_cycles:
            cycle_states_union.update(c.states)

        retained = frozenset(core_graph.states())
        is_pure_cycle_core = (
            retained == frozenset(cycle_states_union)
            and all(c.is_conservative for c in core_cycles)
            and all(c.is_active for c in core_cycles)
        )

        report = PruningReport(
            initial_state_count=initial_count,
            final_state_count=len(retained),
            sink_pruning_rounds=tuple(sink_rounds),
            branch_pruning_rounds=tuple(branch_rounds),
            retained_states=retained,
            retained_cycles=core_cycles,
            is_pure_cycle_core=is_pure_cycle_core,
        )
        return core_graph, report
