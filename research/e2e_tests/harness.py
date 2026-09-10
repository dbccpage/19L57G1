"""Opaque-box test harness and canonical reference models for Genesis Cohort 2 E2E testing.

AuthorityEffect: None. Configuration status: DECLARED_HOST_CONFIG.
Adheres strictly to the Claim Hygiene Rule: demonstrates behaviors within declared
toy settings and finite scopes without ungrounded universality claims.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Sequence, Tuple

E2E_DIR = Path(__file__).resolve().parent
RESEARCH_ROOT = E2E_DIR.parent
CODE_ROOT = RESEARCH_ROOT.parent / "code"

for p in reversed([
    str(CODE_ROOT),
    str(RESEARCH_ROOT / "target_a_execution"),
    str(RESEARCH_ROOT / "target_b_dynamics"),
    str(RESEARCH_ROOT / "g001_target_charter"),
    str(RESEARCH_ROOT / "g010_primitive_removal"),
    str(RESEARCH_ROOT / "g011_finitary_substrate"),
]):
    if p not in sys.path:
        sys.path.insert(0, p)

import runner as target_a_runner
import control as target_a_control
import memory as target_a_memory
import limits as target_b_limits
import observe as target_b_observe
import commute as target_b_commute
import bounds as target_b_bounds
import charter as g001_charter
import adequacy as g001_adequacy
import morphism as g001_morphism
import capability as g010_capability
import restriction as g010_restriction
import obstruction as g010_obstruction
import ordinals as g011_ordinals
import address as g011_address
import freshness as g011_freshness
import recursion as g011_recursion


# ===========================================================================
# 1. Target A: Represented Execution Engine
# ===========================================================================

GraphInstance = Tuple[int, Tuple[int, ...]]
Graph = Tuple[GraphInstance, ...]


def lookup(form: int, datum: int, graph: Sequence[GraphInstance]) -> int | None:
    """Find edge (form, (datum, target)) in graph without consulting host functions."""
    for f, args in graph:
        if f == form and len(args) == 2 and args[0] == datum:
            return args[1]
    return None


class Terminal(Enum):
    HALT = "halt"
    EXHAUSTED = "exhausted"
    REFUSE = "refuse"
    BRANCH = "branch"


class Refusal(Enum):
    EXHAUSTED = "exhausted"
    NO_EDGE = "noEdge"


@dataclass(frozen=True)
class State:
    graph: Graph
    nops: int
    active: int
    tape: Tuple[int, ...]
    clock: int
    fuel: int


def enabled(g: Sequence[GraphInstance], count: int, x: int, k: int) -> bool:
    """Operation k is enabled at x if self-instance (3 + count + k, (x, x)) exists."""
    y = lookup(3 + count + k, x, g)
    return y is not None and y == x


def enabled_at(g: Sequence[GraphInstance], count: int, x: int) -> Tuple[int, ...]:
    """Return all enabled operations at x in index order."""
    return tuple(k for k in range(count) if enabled(g, count, x, k))


def fire(s: State, k: int) -> State | Refusal:
    """Fire operation k at active datum, decrementing fuel monotonically."""
    if s.fuel <= 0:
        return Refusal.EXHAUSTED
    y = lookup(3 + k, s.active, s.graph)
    if y is None:
        return Refusal.NO_EDGE
    return State(
        graph=s.graph,
        nops=s.nops,
        active=y,
        tape=s.tape + (y,),
        clock=s.clock + 1,
        fuel=s.fuel - 1,
    )


def step_det(s: State) -> Terminal | State:
    """Step deterministic interpreter: halt if none enabled, branch if >=2, fire if 1."""
    en = enabled_at(s.graph, s.nops, s.active)
    if not en:
        return Terminal.HALT
    if len(en) >= 2:
        return Terminal.BRANCH
    res = fire(s, en[0])
    if res is Refusal.EXHAUSTED:
        return Terminal.EXHAUSTED
    if res is Refusal.NO_EDGE:
        return Terminal.REFUSE
    assert isinstance(res, State)
    return res


def run_det(bound: int, s: State) -> Tuple[Terminal, State]:
    """Run interpreter bounded by step limit."""
    while True:
        nxt = step_det(s)
        if isinstance(nxt, Terminal):
            return (nxt, s)
        if bound <= 0:
            return (Terminal.EXHAUSTED, s)
        s = nxt
        bound -= 1


def run(s: State) -> Tuple[Terminal, State]:
    """Run bounded by initial fuel."""
    return run_det(s.fuel, s)


def make_program(
    nops: int,
    transitions: Sequence[Tuple[int, int, int]],  # (op, src, dst)
    enablements: Sequence[Tuple[int, int]],         # (datum, op)
) -> Graph:
    """Construct represented program graph."""
    insts: list[GraphInstance] = []
    # Operation edges: form 3 + op, (src, dst)
    for op, src, dst in sorted(transitions):
        insts.append((3 + op, (src, dst)))
    # Enablement edges: form 3 + nops + op, (datum, datum)
    for datum, op in sorted(enablements):
        insts.append((3 + nops + op, (datum, datum)))
    return tuple(insts)


# Target A Extensions: Retained Records & Multi-Locus
@dataclass(frozen=True)
class RetainedRecord:
    depth: int
    payload: Tuple[int, ...]


@dataclass(frozen=True)
class MemoryState:
    base_state: State
    records: Tuple[RetainedRecord, ...]


def step_with_memory(ms: MemoryState) -> MemoryState | Terminal:
    nxt = step_det(ms.base_state)
    if isinstance(nxt, Terminal):
        return nxt
    # Record depth-1 (previous, current)
    rec1 = RetainedRecord(depth=1, payload=(ms.base_state.active, nxt.active))
    new_recs = list(ms.records) + [rec1]
    if len(nxt.tape) >= 3:
        rec2 = RetainedRecord(depth=2, payload=(nxt.tape[-3], nxt.tape[-2], nxt.tape[-1]))
        new_recs.append(rec2)
    return MemoryState(base_state=nxt, records=tuple(new_recs))


def pack_locus(m: int, a: int, b: int) -> int:
    """Two-locus product pairing pack(m, a, b) = m * a + b."""
    return m * a + b


def unpack_locus(m: int, x: int) -> Tuple[int, int]:
    """Inverse of pack_locus."""
    return (x // m, x % m)


# ===========================================================================
# 2. Target B: Coherent Observation Scales and Dynamics
# ===========================================================================

def bond_scale(c: int, n: int, stage: Sequence[int]) -> Tuple[int, ...]:
    """Prefix projection: forgets the last element of stage of length n+1."""
    if len(stage) != n + 1:
        raise ValueError("Stage length must equal n+1")
    return tuple(target_b_limits.bond(tuple(stage)))


def is_compatible_thread(stages: Sequence[Sequence[int]], c: int) -> bool:
    """Verify thread compatibility condition: for all n, bond(n)(t(n+1)) == t(n)."""
    for i in range(len(stages) - 1):
        target_len = len(stages[i])
        if len(stages[i + 1]) != target_len + 1:
            return False
        if tuple(stages[i + 1][:target_len]) != tuple(stages[i]):
            return False
    return True


def obs_scale(n: int, s: State) -> Tuple[int, ...]:
    """Observe tape after n steps of deterministic execution."""
    curr = s
    for _ in range(n):
        nxt = step_det(curr)
        if isinstance(nxt, Terminal):
            break
        curr = nxt
    return curr.tape


def check_prefix_compatibility(obs_short: Sequence[int], obs_long: Sequence[int]) -> bool:
    """Check obs_short is a prefix of obs_long."""
    k = len(obs_short)
    return len(obs_long) >= k and tuple(obs_long[:k]) == tuple(obs_short)


def is_chain_functional(tape: Sequence[int]) -> bool:
    """Check chain functionality: each active datum determines at most one successor."""
    return target_b_bounds.is_functional(target_b_bounds.pairs_of(tape))


def check_zeros_bound(L: int, zeros_count: int) -> bool:
    """Verify rational frequency bound for 3-cycle: L <= 3 * zeros <= L + 2."""
    return L <= 3 * zeros_count <= L + 2


def rational_frequency(tape: Sequence[int], target: int) -> Tuple[int, int]:
    """Return count and length as rational pair (count, L)."""
    count = sum(1 for x in tape if x == target)
    return (count, len(tape))


# ===========================================================================
# 3. G001: TOE Target-Class Charter & Comparison Category
# ===========================================================================

class AdequacyDimension(Enum):
    COMPUTATIONAL_UNIVERSALITY = "computational_universality"
    REASONING_ADEQUACY = "reasoning_adequacy"
    REPRESENTATIONAL_COMPLETENESS = "representational_completeness"
    MATHEMATICAL_FOUNDATIONS = "mathematical_foundations"
    PHYSICAL_ADEQUACY = "physical_adequacy"
    EMPIRICAL_ADEQUACY = "empirical_adequacy"
    CALCULUS_UNIQUENESS = "calculus_uniqueness"
    PHYSICAL_MODEL_UNIQUENESS = "physical_model_uniqueness"
    COMPARISON_MORPHISMS = "comparison_morphisms"


@dataclass(frozen=True)
class TargetSystem:
    name: str
    dimension_scores: dict[AdequacyDimension, bool]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ComparisonMorphism:
    source: TargetSystem
    target: TargetSystem
    mapping_name: str
    preserves_adequacy: bool

    def compose(self, other: ComparisonMorphism) -> ComparisonMorphism:
        if self.target.name != other.source.name:
            raise ValueError("Morphism domain mismatch on composition")
        return ComparisonMorphism(
            source=self.source,
            target=other.target,
            mapping_name=f"{other.mapping_name} o {self.mapping_name}",
            preserves_adequacy=self.preserves_adequacy and other.preserves_adequacy,
        )


def evaluate_system(sys: TargetSystem) -> Tuple[bool, int]:
    """Check if all 9 frozen criteria are satisfied."""
    met = sum(1 for dim in AdequacyDimension if sys.dimension_scores.get(dim, False))
    return (met == 9, met)


# ===========================================================================
# 4. G010: Semantic Primitive Removal
# ===========================================================================

class Capability(Enum):
    STORE_MUTATION = "store_mutation"
    DIRECT_LOOKUP = "direct_lookup"
    CONDITIONAL_BRANCH = "conditional_branch"
    UNBOUNDED_RECURSION = "unbounded_recursion"


@dataclass(frozen=True)
class RestrictedExecutionResult:
    status: str
    output: Tuple[int, ...]
    capabilities_used: frozenset[Capability]


def execute_restricted(
    program: Graph,
    allowed_caps: frozenset[Capability],
    required_caps: frozenset[Capability],
    start: int,
    fuel: int,
    nops: int = 1,
) -> RestrictedExecutionResult:
    """Execute with candidate capabilities genuinely absent."""
    if not required_caps.issubset(allowed_caps):
        return RestrictedExecutionResult(
            status="OBSTRUCTED_CAPABILITY_ABSENT",
            output=(),
            capabilities_used=frozenset(),
        )
    s = State(graph=program, nops=nops, active=start, tape=(start,), clock=0, fuel=fuel)
    term, final_s = run_det(fuel, s)
    return RestrictedExecutionResult(
        status=term.value,
        output=final_s.tape,
        capabilities_used=required_caps,
    )


@dataclass(frozen=True)
class ObstructionWitness:
    task_name: str
    required_capability: Capability
    available_capabilities: frozenset[Capability]
    is_obstructed: bool


def verify_obstruction(
    task_name: str,
    required_cap: Capability,
    available_caps: frozenset[Capability],
) -> ObstructionWitness:
    return ObstructionWitness(
        task_name=task_name,
        required_capability=required_cap,
        available_capabilities=available_caps,
        is_obstructed=(required_cap not in available_caps),
    )


# ===========================================================================
# 5. G011: Internal Finitary Substrate
# ===========================================================================

@dataclass(frozen=True)
class Ordinal:
    """Endogenous inductive ordinal: Zero or Succ(pred)."""
    val: int

    @staticmethod
    def zero() -> Ordinal:
        return Ordinal(0)

    def succ(self) -> Ordinal:
        return Ordinal(self.val + 1)

    def is_zero(self) -> bool:
        return self.val == 0

    def pred(self) -> Ordinal:
        if self.val == 0:
            raise ValueError("Zero has no predecessor")
        return Ordinal(self.val - 1)

    def __lt__(self, other: Ordinal) -> bool:
        return self.val < other.val

    def __le__(self, other: Ordinal) -> bool:
        return self.val <= other.val

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ordinal) and self.val == other.val

    def add(self, other: Ordinal) -> Ordinal:
        return Ordinal(self.val + other.val)

    def mul(self, other: Ordinal) -> Ordinal:
        return Ordinal(self.val * other.val)


@dataclass(frozen=True)
class TreeAddress:
    """Endogenous hierarchical tree address."""
    path: Tuple[int, ...]

    @staticmethod
    def root() -> TreeAddress:
        return TreeAddress(())

    def extend(self, index: int) -> TreeAddress:
        return TreeAddress(self.path + (index,))


@dataclass
class FreshnessGenerator:
    counter: int = 0

    def fresh_address(self, parent: TreeAddress) -> TreeAddress:
        self.counter += 1
        return parent.extend(self.counter)


def endogenous_recursion(depth: Ordinal, fuel: int, acc: int) -> Tuple[int, bool]:
    """Fuel-bounded endogenous recursion over finitary ordinals."""
    if depth.is_zero():
        return (acc, True)
    if fuel <= 0:
        return (acc, False)
    return endogenous_recursion(depth.pred(), fuel - 1, acc + 1)


# ===========================================================================
# 6. Progressive Dynamic Resolver (Live Tree Integration)
# ===========================================================================

def resolve_target_a():
    """Bridge to live target_a_execution."""
    return target_a_runner


def resolve_target_b():
    """Bridge to live target_b_dynamics."""
    return target_b_limits


def resolve_g001():
    """Bridge to live g001_target_charter."""
    return g001_charter


def resolve_g010():
    """Bridge to live g010_primitive_removal."""
    return g010_capability


def resolve_g011():
    """Bridge to live g011_finitary_substrate."""
    return g011_ordinals
