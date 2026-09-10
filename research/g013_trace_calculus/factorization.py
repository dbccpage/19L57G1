"""Endpoint factorization theorem and graph regime sweeps.

Formalizes the principle that future state trajectories from any history
factor strictly through the terminal 0-cell endpoint:
  future_factors_through_endpoint : (target(h1) == target(h2) == source(f))
    => replay(h1 * f) and replay(h2 * f) coincide on the future segment.

Target G013: Coherent Trace Calculus & Higher Cell Algebra.
AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple

from trace import State, Trace, Transition


@dataclass(frozen=True)
class FactorizationWitness:
    """Witness certificate that a future trajectory factors through a shared endpoint.

    Attributes:
        history_1: First history trace ending at endpoint.
        history_2: Second history trace ending at endpoint.
        shared_endpoint: Common terminal 0-cell target(h1) == target(h2).
        future: Continuation trace starting from shared_endpoint.
        composite_1: Full trace h1 * future.
        composite_2: Full trace h2 * future.
        final_state: Shared terminal state reached by both composites.
        future_segment_identical: Whether the state sequence during the future segment is identical.
    """

    history_1: Trace
    history_2: Trace
    shared_endpoint: State
    future: Trace
    composite_1: Trace
    composite_2: Trace
    final_state: State
    future_segment_identical: bool

    def is_valid(self) -> bool:
        """Validate all factorization requirements."""
        return (
            self.history_1.target == self.shared_endpoint
            and self.history_2.target == self.shared_endpoint
            and self.future.source == self.shared_endpoint
            and self.composite_1.target == self.final_state
            and self.composite_2.target == self.final_state
            and self.future_segment_identical
        )


def witness_endpoint_factorization(
    h1: Trace,
    h2: Trace,
    future: Trace,
) -> FactorizationWitness:
    """Construct and verify an endpoint factorization witness for two histories and a future."""
    if h1.target != h2.target:
        raise ValueError(
            f"Histories do not share terminal endpoint: "
            f"h1 target={h1.target.state_id!r}, h2 target={h2.target.state_id!r}"
        )
    shared_endpoint = h1.target
    if future.source != shared_endpoint:
        raise ValueError(
            f"Future source {future.source.state_id!r} does not match shared endpoint {shared_endpoint.state_id!r}"
        )

    comp1 = h1.concat(future)
    comp2 = h2.concat(future)

    # Replay both full traces
    states1 = comp1.replay()
    states2 = comp2.replay()

    # Extract the future sub-sequences: length of future + 1 states
    len_f = future.length
    future_states1 = states1[len(states1) - len_f - 1 :]
    future_states2 = states2[len(states2) - len_f - 1 :]

    identical_future = (future_states1 == future_states2)
    final_st = future.target

    return FactorizationWitness(
        history_1=h1,
        history_2=h2,
        shared_endpoint=shared_endpoint,
        future=future,
        composite_1=comp1,
        composite_2=comp2,
        final_state=final_st,
        future_segment_identical=identical_future,
    )


class GraphRegimeGenerator:
    """Generates synthetic graph topologies to sweep endpoint factorization."""

    @staticmethod
    def linear_pipeline(depth: int) -> Tuple[List[State], List[Transition]]:
        """Generate a linear pipeline of states s_0 -> s_1 -> ... -> s_depth."""
        states = [State.create(f"L{i}", {"index": i}) for i in range(depth + 1)]
        transitions = [
            Transition(source=states[i], target=states[i + 1], label=f"step_{i}", cost=1.0)
            for i in range(depth)
        ]
        return states, transitions

    @staticmethod
    def diamond_dag(branches: int, depth: int) -> Tuple[List[State], List[Transition]]:
        """Generate a diamond network with multiple concurrent paths joining at intermediate hubs."""
        states: List[State] = []
        transitions: List[Transition] = []

        start = State.create("diamond_start", {"stage": 0})
        hub = State.create("diamond_hub", {"stage": 1})
        end = State.create("diamond_end", {"stage": 2})
        states.extend([start, hub, end])

        # Stage 0 -> 1: multiple routes
        for b in range(branches):
            mid1 = State.create(f"diamond_mid_A{b}", {"stage": 0.5, "branch": b})
            states.append(mid1)
            transitions.append(Transition(start, mid1, f"split_A{b}", cost=1.0))
            transitions.append(Transition(mid1, hub, f"join_A{b}", cost=1.0))

        # Stage 1 -> 2: multiple continuation routes
        for b in range(branches):
            mid2 = State.create(f"diamond_mid_B{b}", {"stage": 1.5, "branch": b})
            states.append(mid2)
            transitions.append(Transition(hub, mid2, f"split_B{b}", cost=1.0))
            transitions.append(Transition(mid2, end, f"join_B{b}", cost=1.0))

        return states, transitions

    @staticmethod
    def grid_graph(width: int, height: int) -> Tuple[Dict[Tuple[int, int], State], List[Transition]]:
        """Generate a 2D rectangular grid graph with right and down transitions."""
        grid: Dict[Tuple[int, int], State] = {}
        for x in range(width):
            for y in range(height):
                grid[(x, y)] = State.create(f"grid_{x}_{y}", {"x": x, "y": y})

        transitions: List[Transition] = []
        for x in range(width):
            for y in range(height):
                current = grid[(x, y)]
                if x + 1 < width:
                    transitions.append(Transition(current, grid[(x + 1, y)], "right", cost=1.0))
                if y + 1 < height:
                    transitions.append(Transition(current, grid[(x, y + 1)], "down", cost=1.0))

        return grid, transitions

    @staticmethod
    def cyclic_state_machine(num_cycles: int, cycle_len: int) -> Tuple[List[State], List[Transition]]:
        """Generate a cyclic graph with a shared nexus node."""
        nexus = State.create("nexus", {"type": "nexus"})
        states = [nexus]
        transitions: List[Transition] = []

        for c in range(num_cycles):
            cycle_nodes = [State.create(f"cycle_{c}_{i}", {"cycle": c, "pos": i}) for i in range(cycle_len - 1)]
            states.extend(cycle_nodes)
            if not cycle_nodes:
                continue
            transitions.append(Transition(nexus, cycle_nodes[0], f"enter_c{c}", cost=1.0))
            for i in range(len(cycle_nodes) - 1):
                transitions.append(Transition(cycle_nodes[i], cycle_nodes[i + 1], f"step_c{c}_{i}", cost=1.0))
            transitions.append(Transition(cycle_nodes[-1], nexus, f"return_c{c}", cost=1.0))

        return states, transitions


def sweep_factorization_grid(
    width: int = 3,
    height: int = 3,
) -> List[FactorizationWitness]:
    """Exhaustive sweep of endpoint factorization over a 2D grid DAG.
    For each intermediate hub (x, y), collects all paths from (0,0) to (x,y),
    and all paths from (x,y) to (width-1, height-1), verifying factorization for all pairs.
    """
    grid, transitions = GraphRegimeGenerator.grid_graph(width, height)

    # Build adjacency
    adj: Dict[State, List[Transition]] = {s: [] for s in grid.values()}
    for t in transitions:
        adj[t.source].append(t)

    # Helper: find all paths between two states
    def find_all_traces(src: State, dst: State, current_path: List[Transition]) -> List[Trace]:
        if src == dst:
            if not current_path:
                return [Trace.id_trace(src)]
            return [Trace.from_steps(current_path)]
        results: List[Trace] = []
        for step in adj.get(src, []):
            results.extend(find_all_traces(step.target, dst, current_path + [step]))
        return results

    start_node = grid[(0, 0)]
    end_node = grid[(width - 1, height - 1)]

    witnesses: List[FactorizationWitness] = []

    for (x, y), hub in grid.items():
        if (x, y) == (0, 0) or (x, y) == (width - 1, height - 1):
            continue

        histories = find_all_traces(start_node, hub, [])
        futures = find_all_traces(hub, end_node, [])

        if len(histories) >= 2 and len(futures) >= 1:
            for i in range(len(histories) - 1):
                h1 = histories[i]
                h2 = histories[i + 1]
                for fut in futures:
                    w = witness_endpoint_factorization(h1, h2, fut)
                    if not w.is_valid():
                        raise RuntimeError(f"Factorization failed for hub {hub.state_id}!")
                    witnesses.append(w)

    return witnesses
