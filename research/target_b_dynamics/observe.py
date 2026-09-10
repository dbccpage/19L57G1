"""Step-scale observations and prefix compatibility tracking Target A execution traces.

AuthorityEffect: None.
Mirrors Lean 4 constructive formalization in Observe.lean.

Key concepts:
- State & Step semantics: Fixed interpreter reading encoded graph data without external oracles.
- Deterministic stepping: step_det / next_state preserves state at terminals (HALT, BRANCH, EXHAUSTED, REFUSE).
- Observation at scale n: obs(n, s) is the tape after n steps of next_state.
- Prefix compatibility: obs(n, s) is a prefix of obs(n + k, s) because steps only append.
- Fuel independence: obs(n, s) is identical for all fuel amounts >= n.
- Lost fuel witness: Tape alone loses fuel; two states with identical tape diverge after 1 step.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence

Word = tuple[int, ...]
Inst = tuple[int, tuple[int, ...]]


class Terminal(Enum):
    HALT = "halt"
    EXHAUSTED = "exhausted"
    REFUSE = "refuse"
    BRANCH = "branch"


@dataclass(frozen=True)
class State:
    graph: tuple[Inst, ...]
    nops: int
    active: int
    tape: tuple[int, ...]
    clock: int
    fuel: int

    def with_fuel(self, new_fuel: int) -> State:
        return State(
            graph=self.graph,
            nops=self.nops,
            active=self.active,
            tape=self.tape,
            clock=self.clock,
            fuel=new_fuel,
        )


def lookup(form: int, x: int, graph: Sequence[Inst]) -> int | None:
    """Read graph: value y of first directed edge (form, (x, y))."""
    for g, args in graph:
        if g == form and len(args) == 2 and args[0] == x:
            return args[1]
    return None


def enabled_at(graph: Sequence[Inst], nops: int, x: int) -> list[int]:
    """Find operations k in 0..nops-1 enabled at x via self-instances (3 + nops + k, (x, x))."""
    enabled: list[int] = []
    for k in range(nops):
        form = 3 + nops + k
        if lookup(form, x, graph) == x:
            enabled.append(k)
    return enabled


def fire(s: State, k: int) -> tuple[str, State | None]:
    """Fire operation k: spends 1 fuel, advances active datum, ticks clock, appends to tape."""
    if s.fuel == 0:
        return "exhausted", None
    y = lookup(3 + k, s.active, s.graph)
    if y is None:
        return "noEdge", None
    next_s = State(
        graph=s.graph,
        nops=s.nops,
        active=y,
        tape=s.tape + (y,),
        clock=s.clock + 1,
        fuel=s.fuel - 1,
    )
    return "ok", next_s


def step_det(s: State) -> tuple[Terminal | None, State | None]:
    """Parameterized deterministic step:
    - 0 ops enabled => HALT
    - 1 op enabled => fire
    - >= 2 ops enabled => BRANCH (refuses to choose)
    """
    en = enabled_at(s.graph, s.nops, s.active)
    if len(en) == 0:
        return Terminal.HALT, None
    if len(en) == 1:
        status, s_next = fire(s, en[0])
        if status == "ok":
            return None, s_next
        if status == "exhausted":
            return Terminal.EXHAUSTED, None
        return Terminal.REFUSE, None
    return Terminal.BRANCH, None


def next_state(s: State) -> State:
    """Advance run by one deterministic step; hold state at a terminal."""
    terminal, s_next = step_det(s)
    return s_next if s_next is not None else s


def iterate(n: int, s: State) -> State:
    """Iterate next_state n times."""
    for _ in range(n):
        s = next_state(s)
    return s


def obs(n: int, s: State) -> Word:
    """The observation of the process at step-scale n: tape after n steps."""
    return iterate(n, s).tape


def obs_trace(n: int, s: State) -> tuple[Word, ...]:
    """Sequence of step-scale observations [obs(0, s), ..., obs(n, s)]."""
    return tuple(obs(i, s) for i in range(n + 1))


def is_prefix(a: Sequence[int], b: Sequence[int]) -> bool:
    """Whether a is a prefix of b."""
    return len(a) <= len(b) and tuple(b[: len(a)]) == tuple(a)


def verify_prefix_compatibility(s: State, max_steps: int) -> bool:
    """Verify that obs(n, s) is a prefix of obs(n + 1, s) for all n < max_steps."""
    for n in range(max_steps):
        o_n = obs(n, s)
        o_succ = obs(n + 1, s)
        if not is_prefix(o_n, o_succ):
            return False
    return True


def verify_fuel_independence(s: State, n: int, test_fuels: Sequence[int]) -> bool:
    """Verify that observations at scale n are invariant across all fuels >= n."""
    base_obs = obs(n, s.with_fuel(n))
    for f in test_fuels:
        if f < n:
            continue
        if obs(n, s.with_fuel(f)) != base_obs:
            return False
    return True


def lost_fuel_witness() -> tuple[State, State, Word, Word, Word, Word]:
    """Exhibit lost-fuel failure: states with fuel 0 and fuel 1 share tape [0]
    but diverge after 1 step.
    """
    cycle_graph = make_cycle_graph()
    s0 = State(graph=cycle_graph, nops=3, active=0, tape=(0,), clock=0, fuel=0)
    s1 = State(graph=cycle_graph, nops=3, active=0, tape=(0,), clock=0, fuel=1)

    t0_before = obs(0, s0)
    t1_before = obs(0, s1)
    assert t0_before == t1_before == (0,)

    t0_after = obs(1, s0)
    t1_after = obs(1, s1)
    assert t0_after == (0,)
    assert t1_after == (0, 1)

    return s0, s1, t0_before, t1_before, t0_after, t1_after


def make_cycle_graph() -> tuple[Inst, ...]:
    """Construct encoded graph for the 3-state cycle program (0 -> 1 -> 2 -> 0)
    with cycle enabled everywhere.

    Operation edges (form 3 + k, where k = 0 is cycle):
      (3, (0, 1)), (3, (1, 2)), (3, (2, 0))
    Operation 1 (constant zero):
      (4, (0, 0)), (4, (1, 0)), (4, (2, 0))
    Operation 2 (climb):
      (5, (0, 1)), (5, (1, 2)), (5, (2, 2))
    Control enablements for operation 0 (form 3 + nops + 0 = 6):
      (6, (0, 0)), (6, (1, 1)), (6, (2, 2))
    """
    edges: list[Inst] = [
        # op 0: cycle
        (3, (0, 1)),
        (3, (1, 2)),
        (3, (2, 0)),
        # op 1: zero
        (4, (0, 0)),
        (4, (1, 0)),
        (4, (2, 0)),
        # op 2: climb
        (5, (0, 1)),
        (5, (1, 2)),
        (5, (2, 2)),
        # enable op 0 everywhere
        (6, (0, 0)),
        (6, (1, 1)),
        (6, (2, 2)),
    ]
    return tuple(edges)
