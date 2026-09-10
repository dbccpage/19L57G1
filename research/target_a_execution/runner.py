"""Fixed graph interpreter reading encoded instructions from graph edges.

AuthorityEffect: None.
Configuration status: DECLARED_HOST_CONFIG.

The interpreter executes encoded program graphs directly by reading instance
edges of the form `(3 + k, (x, y))` without consulting unencoded host operation
functions (F.ops).

Key invariants:
- Zero unencoded operation oracles: all transitions consult only stored graph instances.
- Deterministic edge enforcement: ambiguous outgoing edges on an operation form are refused.
- Word machine execution: step, run, iterate, and reference fold (eval_word).
- Parameterized deterministic runner: step_det_of, run_det_of, next_of, iter_of, obs_of.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Protocol, Sequence, runtime_checkable

from derivation.model import Inst

Graph = frozenset[Inst]


class ExecutionError(ValueError):
    """A named refusal or validation failure of the interpreter."""


@runtime_checkable
class TapeCarrier(Protocol):
    """Protocol for state objects carrying an execution tape."""

    tape: tuple[int, ...]


@runtime_checkable
class StateCarrier(TapeCarrier, Protocol):
    """Protocol for state objects carrying full execution state."""

    graph: Graph
    active: int
    tape: tuple[int, ...]
    clock: int
    fuel: int


class Terminal(Enum):
    """Execution terminals, strictly kept apart."""

    HALT = "halt"
    EXHAUSTED = "exhausted"
    REFUSE = "refuse"
    REFUSAL = "refuse"
    BRANCH = "branch"


class Refusal(Enum):
    """Operational refusals during step firing."""

    EXHAUSTED = "exhausted"
    NO_EDGE = "noEdge"
    PROTECTION_VIOLATION = "protectionViolation"
    MALFORMED_OBLIGATION = "malformedObligation"


class ProtectionKind(Enum):
    """The kind of protection policy.

    - SEPARATED: (u, v) with u != v; must remain distinct across state transitions.
    - COLLAPSED: (u, v) representing an identified/collapsed pair (u == v), which
      explicitly fails or refuses under protection evaluation.
    - REFLEXIVE: (x, x) self-protection / boundary stability; x must map to x (x' == x).
    """

    SEPARATED = "separated"
    COLLAPSED = "collapsed"
    REFLEXIVE = "reflexive"


@dataclass(frozen=True)
class ProtectionObligation:
    """A typed operational protection obligation (Spec 1504, W03).

    Key properties:
    - SEPARATED requires u != v.
    - COLLAPSED represents an identified pair (u == v).
    - REFLEXIVE requires u == v (self-protection / boundary stability).
    """

    kind: ProtectionKind
    u: int
    v: int

    def __post_init__(self) -> None:
        if self.u < 0 or self.v < 0:
            raise ExecutionError("obligation datum must be non-negative")
        if self.kind == ProtectionKind.REFLEXIVE and self.u != self.v:
            raise ExecutionError("reflexive obligation must have u == v")
        if self.kind == ProtectionKind.SEPARATED and self.u == self.v:
            raise ExecutionError("separated obligation cannot have u == v")


@dataclass(frozen=True)
class Config:
    """The word machine configuration carrying graph, word, active datum, tape,
    and represented protection obligations and designated pair constraints (Spec 1504)."""

    graph: Graph
    word: tuple[int, ...]
    active: int
    output: tuple[int, ...]
    protection_obligations: tuple[ProtectionObligation, ...] = ()
    designated_pair: tuple[int, int] | None = None


def lookup(f: int, x: int, graph: Graph) -> int | None:
    """Look up the unique target of the edge of form f leaving x.

    Consults only the graph instances. If more than one edge leaves x on form f,
    the graph is not a deterministic function graph and is refused by name.
    """
    ys = sorted(
        args[1]
        for form, args in graph
        if form == f and len(args) == 2 and args[0] == x
    )
    if len(ys) > 1:
        raise ExecutionError(f"form {f} has {len(ys)} edges leaving {x}: ambiguous graph")
    return ys[0] if ys else None


def check_word(word: Sequence[int]) -> None:
    """Validate that every letter in the word is a valid operation index (>= 0)."""
    for k in word:
        if k < 0:
            raise ExecutionError(f"negative operation index {k} is invalid")


def check_obligation(
    g: Graph, k: int, obl: Any
) -> ProtectionObligation | Refusal:
    """Evaluate a protection obligation against operation k and graph g."""
    if not isinstance(obl, ProtectionObligation):
        return Refusal.MALFORMED_OBLIGATION
    if obl.kind == ProtectionKind.SEPARATED:
        if obl.u == obl.v:
            return Refusal.PROTECTION_VIOLATION
        u_nxt = lookup(3 + k, obl.u, g)
        v_nxt = lookup(3 + k, obl.v, g)
        if u_nxt is None or v_nxt is None:
            return Refusal.NO_EDGE
        if u_nxt == v_nxt:
            return Refusal.PROTECTION_VIOLATION
        return ProtectionObligation(ProtectionKind.SEPARATED, u_nxt, v_nxt)
    elif obl.kind == ProtectionKind.COLLAPSED:
        # A collapsed pair explicitly refuses when protection distinctness is enforced
        return Refusal.PROTECTION_VIOLATION
    elif obl.kind == ProtectionKind.REFLEXIVE:
        if obl.u != obl.v:
            return Refusal.MALFORMED_OBLIGATION
        u_nxt = lookup(3 + k, obl.u, g)
        if u_nxt is None:
            return Refusal.NO_EDGE
        if u_nxt != obl.u:
            return Refusal.PROTECTION_VIOLATION
        return ProtectionObligation(ProtectionKind.REFLEXIVE, obl.u, obl.u)
    return Refusal.MALFORMED_OBLIGATION


def check_designated_pair(
    g: Graph, k: int, dp: Any
) -> tuple[int, int] | Refusal:
    """Evaluate designated pair against operation k and graph g."""
    if not (isinstance(dp, tuple) and len(dp) == 2):
        return Refusal.MALFORMED_OBLIGATION
    a, b = dp
    if not (isinstance(a, int) and isinstance(b, int)):
        return Refusal.MALFORMED_OBLIGATION
    if a < 0 or b < 0:
        return Refusal.MALFORMED_OBLIGATION
    if a == b:
        return Refusal.PROTECTION_VIOLATION
    a_nxt = lookup(3 + k, a, g)
    b_nxt = lookup(3 + k, b, g)
    if a_nxt is None or b_nxt is None:
        return Refusal.NO_EDGE
    if a_nxt == b_nxt:
        return Refusal.PROTECTION_VIOLATION
    return (a_nxt, b_nxt)


def step_word(c: Config) -> Config | None:
    """Consume the head operation index k from word, look up edge 3 + k from active, and move."""
    if not c.word:
        return None
    k, rest = c.word[0], c.word[1:]
    check_word((k,))
    y = lookup(3 + k, c.active, c.graph)
    if y is None:
        return None

    new_dp = c.designated_pair
    if c.designated_pair is not None:
        dp_res = check_designated_pair(c.graph, k, c.designated_pair)
        if isinstance(dp_res, Refusal):
            return None
        new_dp = dp_res

    new_obls: list[ProtectionObligation] = []
    for obl in c.protection_obligations:
        obl_res = check_obligation(c.graph, k, obl)
        if isinstance(obl_res, Refusal):
            return None
        new_obls.append(obl_res)

    return Config(
        c.graph,
        rest,
        y,
        c.output + (y,),
        tuple(new_obls),
        new_dp,
    )


def iterate_word(n: int, c: Config) -> Config | None:
    """Iterate step_word n times; failure to step yields None."""
    curr: Config | None = c
    for _ in range(n):
        if curr is None:
            return None
        curr = step_word(curr)
    return curr


def run_word(c: Config) -> Config | None:
    """Run word machine for the entire length of c.word."""
    return iterate_word(len(c.word), c)


def eval_word(graph: Graph, word: Sequence[int], a: int) -> int | None:
    """Reference fold reading the encoded graph instances through lookup.

    Crucially, this never consults unencoded operation functions.
    """
    check_word(word)
    curr = a
    for k in word:
        nxt = lookup(3 + k, curr, graph)
        if nxt is None:
            return None
        curr = nxt
    return curr


def resume_word(c: Config, further_word: Sequence[int]) -> Config | None:
    """Resume execution of a halted config on additional operation letters."""
    check_word(further_word)
    return run_word(Config(c.graph, tuple(further_word), c.active, c.output))


# ---------------------------------------------------------------------------
# Parameterized deterministic runner
# ---------------------------------------------------------------------------

Reader = Callable[[Any], tuple[int, ...]]


def step_det_of(read: Reader, s: Any, fire_fn: Callable[[Any, int], Any]) -> Terminal | Any:
    """Execute one deterministic step parameterized by a reader.

    Rules:
    - If read(s) is empty: halts immediately with Terminal.HALT.
    - If read(s) has >= 2 operations: explicitly refuses to select, returning Terminal.BRANCH.
    - If read(s) has exactly 1 operation: fires that operation via fire_fn.
      - Refusal.EXHAUSTED -> Terminal.EXHAUSTED
      - Refusal.NO_EDGE -> Terminal.REFUSE
      - Refusal.PROTECTION_VIOLATION -> Terminal.REFUSE
      - Refusal.MALFORMED_OBLIGATION -> Terminal.REFUSE
      - State -> returns next State.
    """
    enabled_ops = read(s)
    if not enabled_ops:
        return Terminal.HALT
    if len(enabled_ops) >= 2:
        return Terminal.BRANCH
    op = enabled_ops[0]
    result = fire_fn(s, op)
    if result is Refusal.EXHAUSTED:
        return Terminal.EXHAUSTED
    if result in (
        Refusal.NO_EDGE,
        Refusal.PROTECTION_VIOLATION,
        Refusal.MALFORMED_OBLIGATION,
    ):
        return Terminal.REFUSE
    return result


def next_of(read: Reader, s: Any, fire_fn: Callable[[Any, int], Any]) -> Any:
    """Step the state; on terminal halt/branch/refusal, retain the current state."""
    nxt = step_det_of(read, s, fire_fn)
    return s if isinstance(nxt, Terminal) else nxt


def iter_of(read: Reader, n: int, s: Any, fire_fn: Callable[[Any, int], Any]) -> Any:
    """Iterate next_of n times."""
    curr = s
    for _ in range(n):
        curr = next_of(read, curr, fire_fn)
    return curr


def obs_of(read: Reader, n: int, s: Any, fire_fn: Callable[[Any, int], Any]) -> tuple[int, ...]:
    """Observation at scale n: the tape of data visited after n steps."""
    res = iter_of(read, n, s, fire_fn)
    return cast_tape(res)


def cast_tape(s: Any) -> tuple[int, ...]:
    """Extract execution tape from state object adhering to TapeCarrier protocol."""
    if isinstance(s, TapeCarrier):
        return s.tape
    return getattr(s, "tape", ())


def run_det_of(
    read: Reader, bound: int, s: Any, fire_fn: Callable[[Any, int], Any]
) -> tuple[Terminal, Any]:
    """Run runner with fuel/step bound; returns terminal reason and terminal state."""
    curr = s
    remaining = bound
    while True:
        nxt = step_det_of(read, curr, fire_fn)
        if isinstance(nxt, Terminal):
            return (nxt, curr)
        if remaining <= 0:
            return (Terminal.EXHAUSTED, curr)
        curr = nxt
        remaining -= 1


def blind_reader(_: Any) -> tuple[int, ...]:
    """A reader that reports no operations enabled; runner halts at once."""
    return ()


def forking_reader(_: Any) -> tuple[int, ...]:
    """A reader that reports multiple operations enabled; runner refuses selection."""
    return (0, 1)


def next_value_of(read: Reader, s: Any) -> int | None:
    """Return the destination datum from graph lookup if exactly one op is enabled."""
    enabled_ops = read(s)
    if len(enabled_ops) != 1:
        return None
    active = s.active if isinstance(s, StateCarrier) else getattr(s, "active", 0)
    graph = s.graph if isinstance(s, StateCarrier) else getattr(s, "graph", frozenset())
    return lookup(3 + enabled_ops[0], active, graph)
