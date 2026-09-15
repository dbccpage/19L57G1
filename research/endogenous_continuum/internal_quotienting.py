"""Track 4: Confluence-Driven Internal Quotienting.

AuthorityEffect: None.

Provides internal quotienting of discrete states via local confluent rewrite
rules, critical pair joinability evaluation, and deterministic normal form
reduction without external global orbit minimizers.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction
from typing import Generic, Hashable, TypeVar

T = TypeVar("T", bound=Hashable)


@dataclass(frozen=True)
class RewriteRule(Generic[T]):
    """Explicit local rewrite rule over discrete states.

    AuthorityEffect: None.

    Attributes:
        name: Unique rule identifier.
        apply_fn: Deterministic mapping from a state to reachable one-step states.
        description: Informative description of the local transformation.
    """

    name: str
    apply_fn: Callable[[T], tuple[T, ...]]
    description: str = ""

    def apply(self, state: T) -> tuple[T, ...]:
        """Apply this rule to a state, returning deterministic successor states."""
        return self.apply_fn(state)


@dataclass(frozen=True)
class RewriteStep(Generic[T]):
    """Single-step transition record with applied rule identifier and exact cost."""

    rule_name: str
    target: T
    cost: Fraction | int = field(default_factory=lambda: Fraction(1, 1))

    def __post_init__(self) -> None:
        if isinstance(self.cost, bool) or not isinstance(self.cost, (Fraction, int)):
            raise TypeError(
                f"rewrite cost must be an exact Fraction or int, got {type(self.cost).__name__}"
            )
        exact_cost = Fraction(self.cost)
        if exact_cost < 0:
            raise ValueError(f"rewrite cost must be non-negative, got {exact_cost}")
        object.__setattr__(self, "cost", exact_cost)


@dataclass(frozen=True)
class Divergence(Generic[T]):
    """One-step branching divergence from a common predecessor state."""

    source: T
    branch_a: T
    branch_b: T
    rule_a: str
    rule_b: str


@dataclass(frozen=True)
class JoinProof(Generic[T]):
    """Constructive witness for joinability of a one-step divergence."""

    source: T
    branch_a: T
    branch_b: T
    joined: bool
    join_state: T | None
    path_a: tuple[T, ...]
    path_b: tuple[T, ...]
    rules_a: tuple[str, ...]
    rules_b: tuple[str, ...]
    cost_a: Fraction = field(default_factory=lambda: Fraction(0, 1))
    cost_b: Fraction = field(default_factory=lambda: Fraction(0, 1))


@dataclass(frozen=True)
class LocalConfluenceReport(Generic[T]):
    """Evaluation summary of local confluence on a tested domain of states."""

    is_locally_confluent: bool
    checked_states_count: int
    divergences_count: int
    joined_count: int
    unjoinable_divergences: tuple[Divergence[T], ...]
    join_proofs: tuple[JoinProof[T], ...]


class ReductionStrategy(Enum):
    """Selection strategy for reduction steps when multiple rules apply."""

    FIRST = "first"
    LAST = "last"
    SHORTEST_PATH = "shortest_path"


@dataclass(frozen=True)
class ReductionResult(Generic[T]):
    """Result of iteratively reducing a state to normal form."""

    initial_state: T
    normal_form: T
    steps_count: int
    trajectory: tuple[T, ...]
    rules_applied: tuple[str, ...]
    total_cost: Fraction
    is_normal_form: bool


@dataclass(frozen=True)
class EquivalenceClass(Generic[T]):
    """Equivalence class of states sharing an identical irreducible normal form."""

    normal_form: T
    members: tuple[T, ...]
    size: int


class RewriteSystem(Generic[T]):
    """Deterministic local rewrite system over discrete states.

    AuthorityEffect: None.
    """

    def __init__(
        self,
        rules: Sequence[RewriteRule[T]],
        name: str = "RewriteSystem",
        cost_fn: Callable[[str, T, T], Fraction] | None = None,
    ) -> None:
        """Initialize the rewrite system with an ordered sequence of rules."""
        self.rules: tuple[RewriteRule[T], ...] = tuple(rules)
        self.name: str = name
        self.cost_fn: Callable[[str, T, T], Fraction] | None = cost_fn

    def step_detailed(self, state: T) -> tuple[RewriteStep[T], ...]:
        """Collect all one-step transitions from the given state."""
        steps: list[RewriteStep[T]] = []
        for rule in self.rules:
            targets = rule.apply(state)
            for target in targets:
                if self.cost_fn is not None:
                    step_cost = self.cost_fn(rule.name, state, target)
                else:
                    step_cost = Fraction(1, 1)
                steps.append(RewriteStep(rule_name=rule.name, target=target, cost=step_cost))
        return tuple(steps)

    def step(self, state: T) -> tuple[T, ...]:
        """Return deduplicated one-step successor states in deterministic order."""
        seen: set[T] = set()
        successors: list[T] = []
        for step in self.step_detailed(state):
            if step.target not in seen:
                seen.add(step.target)
                successors.append(step.target)
        return tuple(successors)

    def is_irreducible(self, state: T) -> bool:
        """Check if a state cannot be reduced further under any declared rule."""
        return len(self.step(state)) == 0

    def is_normal_form(self, state: T) -> bool:
        """Alias for is_irreducible."""
        return self.is_irreducible(state)

    def find_divergences_at(self, state: T) -> tuple[Divergence[T], ...]:
        """Find all one-step branching divergences (critical pairs) from state."""
        steps = self.step_detailed(state)
        # Group by distinct target states
        distinct_targets: list[tuple[str, T]] = []
        seen: set[T] = set()
        for s in steps:
            if s.target not in seen:
                seen.add(s.target)
                distinct_targets.append((s.rule_name, s.target))

        divergences: list[Divergence[T]] = []
        n = len(distinct_targets)
        for i in range(n):
            for j in range(i + 1, n):
                r_a, b_a = distinct_targets[i]
                r_b, b_b = distinct_targets[j]
                divergences.append(
                    Divergence(
                        source=state,
                        branch_a=b_a,
                        branch_b=b_b,
                        rule_a=r_a,
                        rule_b=r_b,
                    )
                )
        return tuple(divergences)

    def find_join(
        self,
        branch_a: T,
        branch_b: T,
        source: T | None = None,
        max_depth: int = 50,
    ) -> JoinProof[T]:
        """Search for a common join state reachable from both branch_a and branch_b."""
        if not isinstance(max_depth, int) or isinstance(max_depth, bool) or max_depth < 0:
            raise ValueError(f"max_depth must be a non-negative int, got {max_depth!r}")
        dummy_source = source if source is not None else branch_a

        if branch_a == branch_b:
            return JoinProof(
                source=dummy_source,
                branch_a=branch_a,
                branch_b=branch_b,
                joined=True,
                join_state=branch_a,
                path_a=(branch_a,),
                path_b=(branch_b,),
                rules_a=(),
                rules_b=(),
                cost_a=Fraction(0, 1),
                cost_b=Fraction(0, 1),
            )

        # BFS tracking path, rules, and cumulative cost
        visited_a: dict[T, tuple[tuple[T, ...], tuple[str, ...], Fraction]] = {
            branch_a: ((branch_a,), (), Fraction(0, 1))
        }
        visited_b: dict[T, tuple[tuple[T, ...], tuple[str, ...], Fraction]] = {
            branch_b: ((branch_b,), (), Fraction(0, 1))
        }

        queue_a: deque[tuple[T, int]] = deque([(branch_a, 0)])
        queue_b: deque[tuple[T, int]] = deque([(branch_b, 0)])

        while queue_a or queue_b:
            # Advance side A by one node
            if queue_a:
                curr_a, depth_a = queue_a.popleft()
                if curr_a in visited_b:
                    path_a, rules_a, cost_a = visited_a[curr_a]
                    path_b, rules_b, cost_b = visited_b[curr_a]
                    return JoinProof(
                        source=dummy_source,
                        branch_a=branch_a,
                        branch_b=branch_b,
                        joined=True,
                        join_state=curr_a,
                        path_a=path_a,
                        path_b=path_b,
                        rules_a=rules_a,
                        rules_b=rules_b,
                        cost_a=cost_a,
                        cost_b=cost_b,
                    )
                if depth_a < max_depth:
                    for step in self.step_detailed(curr_a):
                        if step.target not in visited_a:
                            p_prev, r_prev, c_prev = visited_a[curr_a]
                            visited_a[step.target] = (
                                p_prev + (step.target,),
                                r_prev + (step.rule_name,),
                                c_prev + step.cost,
                            )
                            if step.target in visited_b:
                                path_a, rules_a, cost_a = visited_a[step.target]
                                path_b, rules_b, cost_b = visited_b[step.target]
                                return JoinProof(
                                    source=dummy_source,
                                    branch_a=branch_a,
                                    branch_b=branch_b,
                                    joined=True,
                                    join_state=step.target,
                                    path_a=path_a,
                                    path_b=path_b,
                                    rules_a=rules_a,
                                    rules_b=rules_b,
                                    cost_a=cost_a,
                                    cost_b=cost_b,
                                )
                            queue_a.append((step.target, depth_a + 1))

            # Advance side B by one node
            if queue_b:
                curr_b, depth_b = queue_b.popleft()
                if curr_b in visited_a:
                    path_a, rules_a, cost_a = visited_a[curr_b]
                    path_b, rules_b, cost_b = visited_b[curr_b]
                    return JoinProof(
                        source=dummy_source,
                        branch_a=branch_a,
                        branch_b=branch_b,
                        joined=True,
                        join_state=curr_b,
                        path_a=path_a,
                        path_b=path_b,
                        rules_a=rules_a,
                        rules_b=rules_b,
                        cost_a=cost_a,
                        cost_b=cost_b,
                    )
                if depth_b < max_depth:
                    for step in self.step_detailed(curr_b):
                        if step.target not in visited_b:
                            p_prev, r_prev, c_prev = visited_b[curr_b]
                            visited_b[step.target] = (
                                p_prev + (step.target,),
                                r_prev + (step.rule_name,),
                                c_prev + step.cost,
                            )
                            if step.target in visited_a:
                                path_a, rules_a, cost_a = visited_a[step.target]
                                path_b, rules_b, cost_b = visited_b[step.target]
                                return JoinProof(
                                    source=dummy_source,
                                    branch_a=branch_a,
                                    branch_b=branch_b,
                                    joined=True,
                                    join_state=step.target,
                                    path_a=path_a,
                                    path_b=path_b,
                                    rules_a=rules_a,
                                    rules_b=rules_b,
                                    cost_a=cost_a,
                                    cost_b=cost_b,
                                )
                            queue_b.append((step.target, depth_b + 1))

        # Divergence could not be joined within declared bounds
        return JoinProof(
            source=dummy_source,
            branch_a=branch_a,
            branch_b=branch_b,
            joined=False,
            join_state=None,
            path_a=(branch_a,),
            path_b=(branch_b,),
            rules_a=(),
            rules_b=(),
            cost_a=Fraction(0, 1),
            cost_b=Fraction(0, 1),
        )

    def check_local_confluence(
        self,
        states: Iterable[T],
        max_join_depth: int = 50,
    ) -> LocalConfluenceReport[T]:
        """Test local confluence across candidate states by checking all critical divergences."""
        if (
            not isinstance(max_join_depth, int)
            or isinstance(max_join_depth, bool)
            or max_join_depth < 0
        ):
            raise ValueError(
                f"max_join_depth must be a non-negative int, got {max_join_depth!r}"
            )
        checked_count = 0
        all_divergences: list[Divergence[T]] = []
        unjoinable: list[Divergence[T]] = []
        proofs: list[JoinProof[T]] = []

        for st in states:
            checked_count += 1
            divs = self.find_divergences_at(st)
            for d in divs:
                all_divergences.append(d)
                proof = self.find_join(
                    branch_a=d.branch_a,
                    branch_b=d.branch_b,
                    source=d.source,
                    max_depth=max_join_depth,
                )
                proofs.append(proof)
                if not proof.joined:
                    unjoinable.append(d)

        # An empty census provides no evidence for the bounded claim.
        is_confluent = checked_count > 0 and len(unjoinable) == 0
        joined_count = len(all_divergences) - len(unjoinable)

        return LocalConfluenceReport(
            is_locally_confluent=is_confluent,
            checked_states_count=checked_count,
            divergences_count=len(all_divergences),
            joined_count=joined_count,
            unjoinable_divergences=tuple(unjoinable),
            join_proofs=tuple(proofs),
        )

    def reduce_to_normal_form(
        self,
        state: T,
        strategy: ReductionStrategy = ReductionStrategy.FIRST,
        max_steps: int = 1000,
    ) -> ReductionResult[T]:
        """Reduce a state to an irreducible normal form under the chosen strategy."""
        if not isinstance(max_steps, int) or isinstance(max_steps, bool) or max_steps < 0:
            raise ValueError(f"max_steps must be a non-negative int, got {max_steps!r}")
        if self.is_irreducible(state):
            return ReductionResult(
                initial_state=state,
                normal_form=state,
                steps_count=0,
                trajectory=(state,),
                rules_applied=(),
                total_cost=Fraction(0, 1),
                is_normal_form=True,
            )
        if strategy == ReductionStrategy.SHORTEST_PATH:
            return self._reduce_shortest_path(state, max_steps)

        current = state
        trajectory: list[T] = [current]
        rules_applied: list[str] = []
        total_cost = Fraction(0, 1)
        visited: set[T] = {current}

        for _ in range(max_steps):
            if self.is_irreducible(current):
                return ReductionResult(
                    initial_state=state,
                    normal_form=current,
                    steps_count=len(rules_applied),
                    trajectory=tuple(trajectory),
                    rules_applied=tuple(rules_applied),
                    total_cost=total_cost,
                    is_normal_form=True,
                )
            steps = self.step_detailed(current)
            chosen = steps[0] if strategy == ReductionStrategy.FIRST else steps[-1]
            if chosen.target in visited:
                raise RuntimeError(
                    f"Reduction cycle detected at state {chosen.target!r} during {strategy.value} reduction."
                )
            current = chosen.target
            trajectory.append(current)
            rules_applied.append(chosen.rule_name)
            total_cost += chosen.cost
            visited.add(current)

        return ReductionResult(
            initial_state=state,
            normal_form=current,
            steps_count=len(rules_applied),
            trajectory=tuple(trajectory),
            rules_applied=tuple(rules_applied),
            total_cost=total_cost,
            is_normal_form=False,
        )

    def _reduce_shortest_path(self, state: T, max_steps: int) -> ReductionResult[T]:
        """Find the shortest reduction trajectory from state to an irreducible state via BFS."""
        if self.is_irreducible(state):
            return ReductionResult(
                initial_state=state,
                normal_form=state,
                steps_count=0,
                trajectory=(state,),
                rules_applied=(),
                total_cost=Fraction(0, 1),
                is_normal_form=True,
            )

        queue: deque[tuple[T, tuple[T, ...], tuple[str, ...], Fraction]] = deque([
            (state, (state,), (), Fraction(0, 1))
        ])
        visited: set[T] = {state}

        while queue:
            curr, traj, rules, cost = queue.popleft()
            if self.is_irreducible(curr):
                return ReductionResult(
                    initial_state=state,
                    normal_form=curr,
                    steps_count=len(rules),
                    trajectory=traj,
                    rules_applied=rules,
                    total_cost=cost,
                    is_normal_form=True,
                )
            if len(rules) < max_steps:
                for step in self.step_detailed(curr):
                    if step.target not in visited:
                        visited.add(step.target)
                        queue.append((
                            step.target,
                            traj + (step.target,),
                            rules + (step.rule_name,),
                            cost + step.cost,
                        ))

        # Max steps exceeded without finding irreducible state
        return ReductionResult(
            initial_state=state,
            normal_form=state,
            steps_count=0,
            trajectory=(state,),
            rules_applied=(),
            total_cost=Fraction(0, 1),
            is_normal_form=False,
        )

    def all_reduction_paths(
        self,
        state: T,
        max_depth: int = 50,
        max_paths: int = 500,
    ) -> tuple[ReductionResult[T], ...]:
        """Explore every maximal reduction sequence within declared finite bounds."""
        if not isinstance(max_depth, int) or isinstance(max_depth, bool) or max_depth < 0:
            raise ValueError(f"max_depth must be a non-negative int, got {max_depth!r}")
        if not isinstance(max_paths, int) or isinstance(max_paths, bool) or max_paths <= 0:
            raise ValueError(f"max_paths must be a positive int, got {max_paths!r}")
        results: list[ReductionResult[T]] = []
        truncated = False

        def dfs(
            curr: T,
            traj: list[T],
            rules: list[str],
            cost: Fraction,
            visited: set[T],
        ) -> None:
            nonlocal truncated
            if len(results) >= max_paths:
                truncated = True
                return

            if self.is_irreducible(curr):
                results.append(
                    ReductionResult(
                        initial_state=state,
                        normal_form=curr,
                        steps_count=len(rules),
                        trajectory=tuple(traj),
                        rules_applied=tuple(rules),
                        total_cost=cost,
                        is_normal_form=True,
                    )
                )
                return

            if len(rules) >= max_depth:
                results.append(
                    ReductionResult(
                        initial_state=state,
                        normal_form=curr,
                        steps_count=len(rules),
                        trajectory=tuple(traj),
                        rules_applied=tuple(rules),
                        total_cost=cost,
                        is_normal_form=False,
                    )
                )
                return

            steps = self.step_detailed(curr)
            for step in steps:
                if step.target in visited:
                    continue  # suppress cycle exploration
                traj.append(step.target)
                rules.append(step.rule_name)
                visited.add(step.target)

                dfs(step.target, traj, rules, cost + step.cost, visited)

                visited.remove(step.target)
                rules.pop()
                traj.pop()

        dfs(state, [state], [], Fraction(0, 1), {state})
        if truncated:
            raise RuntimeError(
                f"Reduction path census exceeded max_paths={max_paths}; no complete census returned"
            )
        return tuple(results)

    def all_normal_forms(
        self,
        state: T,
        max_depth: int = 50,
        max_paths: int = 500,
    ) -> frozenset[T]:
        """Return the set of all irreducible normal forms reachable from state."""
        paths = self.all_reduction_paths(state, max_depth=max_depth, max_paths=max_paths)
        return frozenset(r.normal_form for r in paths if r.is_normal_form)

    def are_equivalent(self, state_a: T, state_b: T, max_steps: int = 1000) -> bool:
        """Check equivalence: two states are equivalent iff their normal forms coincide."""
        res_a = self.reduce_to_normal_form(state_a, max_steps=max_steps)
        res_b = self.reduce_to_normal_form(state_b, max_steps=max_steps)
        return (
            res_a.is_normal_form
            and res_b.is_normal_form
            and res_a.normal_form == res_b.normal_form
        )

    def quotient_projection(self, state: T, max_steps: int = 1000) -> T:
        """Canonical projection to the endogenous normal form representative."""
        res = self.reduce_to_normal_form(state, max_steps=max_steps)
        if not res.is_normal_form:
            raise ValueError(f"State {state!r} did not reduce to an irreducible normal form.")
        return res.normal_form

    def partition_by_normal_form(
        self,
        states: Iterable[T],
        max_steps: int = 1000,
    ) -> tuple[EquivalenceClass[T], ...]:
        """Partition states into equivalence classes grouped by coinciding normal form."""
        groups: dict[T, list[T]] = {}
        for st in states:
            nf = self.quotient_projection(st, max_steps=max_steps)
            if nf not in groups:
                groups[nf] = []
            groups[nf].append(st)

        classes: list[EquivalenceClass[T]] = []
        for nf, members in groups.items():
            classes.append(
                EquivalenceClass(
                    normal_form=nf,
                    members=tuple(members),
                    size=len(members),
                )
            )
        # Deterministic sorting by size descending, then repr
        classes.sort(key=lambda c: (-c.size, repr(c.normal_form)))
        return tuple(classes)


# =============================================================================
# Concrete String and Word Rewrite Systems
# =============================================================================


def make_string_rule(lhs: str, rhs: str, name: str = "") -> RewriteRule[str]:
    """Construct an explicit string rewrite rule lhs -> rhs at all matching positions."""
    if not lhs:
        raise ValueError("lhs must be non-empty")
    rule_name = name if name else f"{lhs}->{rhs}"

    def apply_fn(s: str) -> tuple[str, ...]:
        results: list[str] = []
        start = 0
        while True:
            idx = s.find(lhs, start)
            if idx == -1:
                break
            replaced = s[:idx] + rhs + s[idx + len(lhs):]
            results.append(replaced)
            start = idx + 1
        return tuple(results)

    return RewriteRule(name=rule_name, apply_fn=apply_fn, description=f"Replace '{lhs}' with '{rhs}'")


def make_string_rewrite_system(
    rules: Sequence[tuple[str, str]],
    name: str = "StringRewriteSystem",
) -> RewriteSystem[str]:
    """Construct a string rewrite system from a list of (lhs, rhs) pairs."""
    rule_objs = [make_string_rule(lhs, rhs) for lhs, rhs in rules]
    return RewriteSystem(rules=rule_objs, name=name)


def make_sorting_rewrite_system(
    alphabet: Sequence[str] = ("a", "b", "c"),
) -> RewriteSystem[str]:
    """Construct canonical sorting rewrite rules for adjacent inversions."""
    rules: list[RewriteRule[str]] = []
    alpha_sorted = sorted(set(alphabet))
    n = len(alpha_sorted)
    for i in range(n):
        for j in range(i + 1, n):
            c1, c2 = alpha_sorted[i], alpha_sorted[j]
            # Inversion c2 c1 -> c1 c2
            rules.append(make_string_rule(c2 + c1, c1 + c2, name=f"swap_{c2}{c1}"))
    return RewriteSystem(rules=rules, name="AlphabeticalSortingRewriteSystem")


# =============================================================================
# Concrete Relational State Rewrite System
# =============================================================================


@dataclass(frozen=True)
class RelationalState:
    """Discrete relational state with token identities and binary relations.

    AuthorityEffect: None.

    Attributes:
        tokens: Tuple of admitted presentation tokens in deterministic order.
        relations: Frozen set of relational triples (relation_name, subject, object).
    """

    tokens: tuple[str, ...]
    relations: frozenset[tuple[str, str, str]]

    def __post_init__(self) -> None:
        """Normalize the finite carrier and reject relations outside it."""
        if any(not isinstance(token, str) for token in self.tokens):
            raise TypeError("RelationalState tokens must all be strings")
        normalized_tokens = tuple(sorted(set(self.tokens)))
        normalized_relations = frozenset(self.relations)
        token_set = set(normalized_tokens)
        for relation in normalized_relations:
            if len(relation) != 3 or any(not isinstance(part, str) for part in relation):
                raise TypeError("RelationalState relations must be string triples")
            _, subject, obj = relation
            if subject not in token_set or obj not in token_set:
                raise ValueError(
                    f"Relation endpoints must belong to tokens: {relation!r}"
                )
        object.__setattr__(self, "tokens", normalized_tokens)
        object.__setattr__(self, "relations", normalized_relations)

    def __lt__(self, other: RelationalState) -> bool:
        """Deterministic comparison for sorting."""
        return (self.tokens, sorted(self.relations)) < (other.tokens, sorted(other.relations))


def create_relational_state(
    tokens: Iterable[str],
    relations: Iterable[tuple[str, str, str]],
) -> RelationalState:
    """Convenience constructor for RelationalState."""
    return RelationalState(
        tokens=tuple(tokens),
        relations=frozenset(relations),
    )


def make_relational_quotient_system() -> RewriteSystem[RelationalState]:
    """Construct an endogenous relational rewrite system contracting identity assertions.

    Rules:
    1. eliminate_reflexive_identity: ('eq', a, a) is dropped.
    2. contract_alias_pair: for ('eq', a, b) with a != b, substitutes alias = max(a, b)
       with canon = min(a, b) across all tokens and relations, contracting the edge.
    """

    def apply_elim_reflexive(state: RelationalState) -> tuple[RelationalState, ...]:
        reflexive_found: list[tuple[str, str, str]] = []
        for rel in sorted(state.relations):
            if rel[0] == "eq" and rel[1] == rel[2]:
                reflexive_found.append(rel)

        if not reflexive_found:
            return ()

        # Each reflexive edge can be eliminated
        successors: list[RelationalState] = []
        for ref_edge in reflexive_found:
            new_relations = frozenset(r for r in state.relations if r != ref_edge)
            successors.append(RelationalState(tokens=state.tokens, relations=new_relations))
        return tuple(successors)

    def apply_contract_alias(state: RelationalState) -> tuple[RelationalState, ...]:
        candidate_edges: list[tuple[str, str, str]] = []
        for rel in sorted(state.relations):
            if rel[0] == "eq" and rel[1] != rel[2]:
                candidate_edges.append(rel)

        if not candidate_edges:
            return ()

        successors: list[RelationalState] = []
        for edge in candidate_edges:
            _, t1, t2 = edge
            canon = min(t1, t2)
            alias = max(t1, t2)

            # Contract alias into canon
            new_tokens = tuple(sorted(set(canon if t == alias else t for t in state.tokens)))
            new_relations_list: list[tuple[str, str, str]] = []
            for r in state.relations:
                if r == edge:
                    continue
                r_name, r_sub, r_obj = r
                n_sub = canon if r_sub == alias else r_sub
                n_obj = canon if r_obj == alias else r_obj
                # Drop reflexive eq if formed
                if r_name == "eq" and n_sub == n_obj:
                    continue
                new_relations_list.append((r_name, n_sub, n_obj))

            successors.append(
                RelationalState(
                    tokens=new_tokens,
                    relations=frozenset(new_relations_list),
                )
            )
        return tuple(successors)

    rules = [
        RewriteRule(
            name="eliminate_reflexive_identity",
            apply_fn=apply_elim_reflexive,
            description="Eliminates redundant reflexive equality assertions ('eq', a, a).",
        ),
        RewriteRule(
            name="contract_alias_pair",
            apply_fn=apply_contract_alias,
            description="Contracts alias token into canonical token along an explicit ('eq', a, b) relation.",
        ),
    ]

    return RewriteSystem(rules=rules, name="RelationalIdentityQuotientSystem")


# =============================================================================
# Partition Verification Helper
# =============================================================================


def verify_equivalence_partition(
    classes: Sequence[EquivalenceClass[T]],
    original_states: Iterable[T],
) -> bool:
    """Verify that candidate equivalence classes form an exact partition of input states."""
    states_set = set(original_states)
    covered: set[T] = set()

    for eq_cls in classes:
        if eq_cls.size == 0 or len(eq_cls.members) != eq_cls.size:
            return False
        for m in eq_cls.members:
            if m in covered:
                return False  # Overlapping classes
            if m not in states_set:
                return False  # Extraneous element
            covered.add(m)

    return covered == states_set
