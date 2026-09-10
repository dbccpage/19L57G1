"""Control-Flow Graph (CFG) branching and jump tables represented directly as graph data.

AuthorityEffect: None.
Configuration status: DECLARED_HOST_CONFIG.

This module represents program control flow (conditional branching, indirect jump tables,
and loop structures) directly as encoded graph instances:
- Sequence / Step edges: (FORM_CFG_STEP, (pc, next_pc))
- Conditional branch edges: (FORM_CFG_BRANCH, (pc, condition_value, target_pc))
- Jump table entries: (FORM_JUMP_TABLE, (table_id, index, target_pc))
- Indirect jump instruction: (FORM_CFG_INDIRECT, (pc, table_id))

Execution invariants:
1. All routing information is read strictly from graph instances without external dispatch tables.
2. Non-deterministic fork refusal: If two or more branch paths are simultaneously valid
   for the current state, the runner explicitly refuses to select, returning Terminal.BRANCH.
3. Jump tables are fully data-driven: indexing out of bounds or missing a table entry
   results in a named refusal (Terminal.REFUSE).
4. Monotonic accounting: Each control transfer decrements fuel by 1 and increments clock by 1.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from runner import ExecutionError, Graph, Terminal

# Form identifiers reserved for CFG and jump table primitives
FORM_CFG_STEP = 10
FORM_CFG_BRANCH = 11
FORM_JUMP_TABLE = 12
FORM_CFG_INDIRECT = 13
FORM_CFG_ASSIGN = 14


@dataclass(frozen=True)
class CFGState:
    """State of an execution traversing a represented CFG."""

    graph: Graph
    pc: int
    data: int
    history: tuple[tuple[int, int], ...]  # trace of (pc, data)
    clock: int
    fuel: int

    def __post_init__(self) -> None:
        if self.pc < 0:
            raise ExecutionError(f"negative pc {self.pc}")
        if self.clock < 0:
            raise ExecutionError("negative clock")
        if self.fuel < 0:
            raise ExecutionError("negative fuel")


class CFGBuilder:
    """Builder that compiles high-level CFG structures into graph instances."""

    def __init__(self) -> None:
        self.edges: set[tuple[int, tuple[int, ...]]] = set()

    def add_step(self, src_pc: int, next_pc: int) -> CFGBuilder:
        """Add an unconditional sequential step from src_pc to next_pc."""
        self.edges.add((FORM_CFG_STEP, (src_pc, next_pc)))
        return self

    def add_branch(self, pc: int, cond_val: int, target_pc: int) -> CFGBuilder:
        """Add a conditional branch edge: from pc, if data == cond_val, jump to target_pc."""
        self.edges.add((FORM_CFG_BRANCH, (pc, cond_val, target_pc)))
        return self

    def add_if_then_else(
        self, pc: int, true_target: int, false_target: int
    ) -> CFGBuilder:
        """Convenience: branch to true_target on 1, false_target on 0."""
        self.add_branch(pc, 1, true_target)
        self.add_branch(pc, 0, false_target)
        return self

    def add_jump_table_entry(self, table_id: int, index: int, target_pc: int) -> CFGBuilder:
        """Add an entry to a jump table."""
        self.edges.add((FORM_JUMP_TABLE, (table_id, index, target_pc)))
        return self

    def add_jump_table(self, table_id: int, targets: Sequence[int]) -> CFGBuilder:
        """Add an entire array of jump table targets."""
        for idx, target in enumerate(targets):
            self.add_jump_table_entry(table_id, idx, target)
        return self

    def add_indirect_jump(self, pc: int, table_id: int) -> CFGBuilder:
        """At pc, perform an indirect jump indexed by current data through table_id."""
        self.edges.add((FORM_CFG_INDIRECT, (pc, table_id)))
        return self

    def add_assignment(self, pc: int, new_data: int, next_pc: int) -> CFGBuilder:
        """Add an instruction mutating active data to new_data and advancing to next_pc."""
        self.edges.add((FORM_CFG_ASSIGN, (pc, new_data, next_pc)))
        return self

    def to_graph(self) -> Graph:
        """Return the immutable frozen graph of all encoded CFG edges."""
        return frozenset(self.edges)


def resolve_jump_table_target(graph: Graph, table_id: int, index: int) -> int | None:
    """Read target from graph for jump table entry (FORM_JUMP_TABLE, (table_id, index, target))."""
    matches = sorted(
        args[2]
        for form, args in graph
        if form == FORM_JUMP_TABLE
        and len(args) == 3
        and args[0] == table_id
        and args[1] == index
    )
    if len(matches) > 1:
        raise ExecutionError(f"jump table {table_id} index {index} has multiple targets: ambiguous")
    return matches[0] if matches else None


def get_cfg_transitions(graph: Graph, pc: int, data: int) -> tuple[tuple[int, int], ...]:
    """Find all valid successor transitions (target_pc, next_data) from current state.

    Searches across:
    1. Unconditional steps: (FORM_CFG_STEP, (pc, next_pc)) -> preserves data
    2. Matching conditional branches: (FORM_CFG_BRANCH, (pc, cond, target_pc)) -> preserves data
    3. Indirect jump tables: (FORM_CFG_INDIRECT, (pc, table_id)) resolved at index=data -> preserves data
    4. Data assignments: (FORM_CFG_ASSIGN, (pc, new_data, target_pc)) -> mutates data to new_data
    """
    transitions: set[tuple[int, int]] = set()

    for form, args in graph:
        if form == FORM_CFG_STEP and len(args) == 2 and args[0] == pc:
            transitions.add((args[1], data))
        elif form == FORM_CFG_BRANCH and len(args) == 3 and args[0] == pc and args[1] == data:
            transitions.add((args[2], data))
        elif form == FORM_CFG_INDIRECT and len(args) == 2 and args[0] == pc:
            resolved = resolve_jump_table_target(graph, args[1], data)
            if resolved is not None:
                transitions.add((resolved, data))
        elif form == FORM_CFG_ASSIGN and len(args) == 3 and args[0] == pc:
            transitions.add((args[2], args[1]))

    return tuple(sorted(transitions))


def get_cfg_successors(graph: Graph, pc: int, data: int) -> tuple[int, ...]:
    """Find all valid successor PCs from current pc given data value."""
    transitions = get_cfg_transitions(graph, pc, data)
    return tuple(sorted(set(target for target, _ in transitions)))


def step_cfg(s: CFGState) -> Terminal | CFGState:
    """Perform one deterministic step in the represented CFG.

    Enforces strict non-selection on forks:
    - 0 transitions -> Terminal.HALT
    - >= 2 transitions -> Terminal.BRANCH (refusal to silently choose a path)
    - 1 transition:
      - if fuel <= 0 -> Terminal.EXHAUSTED
      - else -> advances to target_pc, updates data to next_data, clock + 1, fuel - 1.
    """
    transitions = get_cfg_transitions(s.graph, s.pc, s.data)

    if not transitions:
        return Terminal.HALT
    if len(transitions) >= 2:
        return Terminal.BRANCH

    if s.fuel <= 0:
        return Terminal.EXHAUSTED

    next_pc, next_data = transitions[0]
    next_history = s.history + ((next_pc, next_data),)
    return CFGState(
        graph=s.graph,
        pc=next_pc,
        data=next_data,
        history=next_history,
        clock=s.clock + 1,
        fuel=s.fuel - 1,
    )


def run_cfg(bound: int, s: CFGState) -> tuple[Terminal, CFGState]:
    """Run CFG execution bounded by bound steps / fuel."""
    curr = s
    remaining = bound
    while True:
        nxt = step_cfg(curr)
        if isinstance(nxt, Terminal):
            return (nxt, curr)
        if remaining <= 0:
            return (Terminal.EXHAUSTED, curr)
        curr = nxt
        remaining -= 1


def init_cfg(graph: Graph, start_pc: int, initial_data: int, fuel: int) -> CFGState:
    """Initialize a CFG execution state."""
    return CFGState(
        graph=graph,
        pc=start_pc,
        data=initial_data,
        history=((start_pc, initial_data),),
        clock=0,
        fuel=fuel,
    )
