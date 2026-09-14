"""Track 2: Inverse Limit Projective System over discrete transition movegraphs.

AuthorityEffect: None.
Constructive: exact rational arithmetic via fractions.Fraction and int, zero floats.
"""

from __future__ import annotations

import heapq
from collections import defaultdict, deque
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, Dict, FrozenSet, Iterable, Iterator, List, Mapping, Optional, Sequence, Set, Tuple, Union



def _to_fraction(val: Any, field_name: str) -> Fraction:
    """Coerce an int or Fraction to exact Fraction; reject float explicitly."""
    if isinstance(val, float):
        raise TypeError(
            f"{field_name} must be exact rational (Fraction or int), received float: {val!r}"
        )
    if isinstance(val, Fraction):
        return val
    if isinstance(val, int):
        return Fraction(val, 1)
    raise TypeError(
        f"{field_name} must be exact rational (Fraction or int), received {type(val).__name__}: {val!r}"
    )


@dataclass(frozen=True)
class MoveEdge:
    """Directed transition edge between states in a discrete movegraph.

    Attributes:
        source: Source state identifier.
        target: Target state identifier.
        label: Descriptive transition label.
        mu1: Primary operational capability cost (exact rational >= 0).
        mu2: Secondary operational dissipation cost (exact rational >= 0).
    """

    source: Any
    target: Any
    label: str = ""
    mu1: Union[Fraction, int] = field(default_factory=lambda: Fraction(1, 1))
    mu2: Union[Fraction, int] = field(default_factory=lambda: Fraction(0, 1))

    def __post_init__(self) -> None:
        q_mu1 = _to_fraction(self.mu1, "mu1")
        q_mu2 = _to_fraction(self.mu2, "mu2")
        if q_mu1 < 0:
            raise ValueError(f"mu1 must be non-negative, got {q_mu1}")
        if q_mu2 < 0:
            raise ValueError(f"mu2 must be non-negative, got {q_mu2}")
        object.__setattr__(self, "mu1", q_mu1)
        object.__setattr__(self, "mu2", q_mu2)


@dataclass(frozen=True)
class OperationalPrice:
    """Operational pricing tuple (Sigma mu1, Sigma mu2) accumulated along a path or transition."""

    mu1_sum: Union[Fraction, int]
    mu2_sum: Union[Fraction, int]
    step_count: int


    def __post_init__(self) -> None:
        object.__setattr__(self, "mu1_sum", _to_fraction(self.mu1_sum, "mu1_sum"))
        object.__setattr__(self, "mu2_sum", _to_fraction(self.mu2_sum, "mu2_sum"))
        if not isinstance(self.step_count, int) or self.step_count < 0:
            raise ValueError(f"step_count must be non-negative int, got {self.step_count!r}")

    @classmethod
    def zero(cls) -> OperationalPrice:
        return cls(mu1_sum=Fraction(0, 1), mu2_sum=Fraction(0, 1), step_count=0)

    def add_edge(self, edge: MoveEdge) -> OperationalPrice:
        return OperationalPrice(
            mu1_sum=self.mu1_sum + edge.mu1,
            mu2_sum=self.mu2_sum + edge.mu2,
            step_count=self.step_count + 1,
        )

    def combine(self, other: OperationalPrice) -> OperationalPrice:
        return OperationalPrice(
            mu1_sum=self.mu1_sum + other.mu1_sum,
            mu2_sum=self.mu2_sum + other.mu2_sum,
            step_count=self.step_count + other.step_count,
        )


@dataclass(frozen=True)
class MoveGraph:
    """Discrete transition movegraph at refinement level k.

    Attributes:
        level: Non-negative integer refinement level k.
        states: Frozenset of state identifiers.
        edges: Frozenset of MoveEdge transitions.
    """

    level: int
    states: FrozenSet[Any]
    edges: FrozenSet[MoveEdge]
    _outgoing: Mapping[Any, Tuple[MoveEdge, ...]] = field(
        default_factory=dict, init=False, repr=False, compare=False
    )
    _incoming: Mapping[Any, Tuple[MoveEdge, ...]] = field(
        default_factory=dict, init=False, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        if not isinstance(self.level, int) or self.level < 0:
            raise ValueError(f"level must be non-negative int, got {self.level!r}")

        # Validate that all edge endpoints belong to states
        out_map: Dict[Any, List[MoveEdge]] = {s: [] for s in self.states}
        in_map: Dict[Any, List[MoveEdge]] = {s: [] for s in self.states}

        for e in self.edges:
            if e.source not in self.states:
                raise ValueError(
                    f"Edge source {e.source!r} not in graph states at level {self.level}"
                )
            if e.target not in self.states:
                raise ValueError(
                    f"Edge target {e.target!r} not in graph states at level {self.level}"
                )
            out_map[e.source].append(e)
            in_map[e.target].append(e)

        frozen_out = {s: tuple(edges) for s, edges in out_map.items()}
        frozen_in = {s: tuple(edges) for s, edges in in_map.items()}

        object.__setattr__(self, "_outgoing", frozen_out)
        object.__setattr__(self, "_incoming", frozen_in)

    @classmethod
    def build(
        cls,
        level: int,
        states: Iterable[Any],
        edges: Iterable[MoveEdge] = (),
    ) -> MoveGraph:
        """Construct a MoveGraph from state and edge iterables."""
        return cls(
            level=level,
            states=frozenset(states),
            edges=frozenset(edges),
        )

    def has_state(self, state: Any) -> bool:
        return state in self.states

    def outgoing(self, state: Any) -> Tuple[MoveEdge, ...]:
        if state not in self.states:
            raise KeyError(f"State {state!r} not in MoveGraph at level {self.level}")
        return self._outgoing.get(state, ())

    def incoming(self, state: Any) -> Tuple[MoveEdge, ...]:
        if state not in self.states:
            raise KeyError(f"State {state!r} not in MoveGraph at level {self.level}")
        return self._incoming.get(state, ())

    def has_edge(self, source: Any, target: Any) -> bool:
        if source not in self.states or target not in self.states:
            return False
        return any(e.target == target for e in self.outgoing(source))

    def find_edges(self, source: Any, target: Any) -> Tuple[MoveEdge, ...]:
        if source not in self.states:
            return ()
        return tuple(e for e in self.outgoing(source) if e.target == target)

    @property
    def state_count(self) -> int:
        return len(self.states)

    @property
    def edge_count(self) -> int:
        return len(self.edges)


@dataclass(frozen=True)
class MorphismCheckResult:
    """Outcome of structural morphism verification between movegraphs."""

    is_valid: bool
    source_level: int
    target_level: int
    defects: Tuple[str, ...]

    def __bool__(self) -> bool:
        return self.is_valid


@dataclass(frozen=True)
class CoarseningMap:
    """Coarsening projection map pi_{j, k} from fine level k to coarse level j (j <= k).

    Attributes:
        source_level: Fine level k.
        target_level: Coarse level j.
        state_map: Mapping sending each fine state to its coarse image.
        edge_map: Optional mapping sending fine edges to coarse edges or None (collapsed).
    """

    source_level: int
    target_level: int
    state_map: Mapping[Any, Any]
    edge_map: Optional[Mapping[MoveEdge, Optional[MoveEdge]]] = None

    def __post_init__(self) -> None:
        if not isinstance(self.source_level, int) or self.source_level < 0:
            raise ValueError(f"source_level must be non-negative int, got {self.source_level!r}")
        if not isinstance(self.target_level, int) or self.target_level < 0:
            raise ValueError(f"target_level must be non-negative int, got {self.target_level!r}")
        if self.target_level > self.source_level:
            raise ValueError(
                f"Coarsening projection requires target_level <= source_level, "
                f"got {self.target_level} > {self.source_level}"
            )
        # Freeze state_map
        object.__setattr__(self, "state_map", dict(self.state_map))
        if self.edge_map is not None:
            object.__setattr__(self, "edge_map", dict(self.edge_map))

    @classmethod
    def identity(cls, graph: MoveGraph) -> CoarseningMap:
        """Construct the canonical identity coarsening map pi_{k, k} on a movegraph."""
        s_map = {s: s for s in graph.states}
        e_map = {e: e for e in graph.edges}
        return cls(
            source_level=graph.level,
            target_level=graph.level,
            state_map=s_map,
            edge_map=e_map,
        )

    def apply_state(self, state: Any) -> Any:
        """Project a state from level k to level j."""
        if state not in self.state_map:
            raise KeyError(
                f"State {state!r} not in domain of CoarseningMap({self.source_level} -> {self.target_level})"
            )
        return self.state_map[state]

    def apply_edge(self, edge: MoveEdge) -> Optional[MoveEdge]:
        """Project a transition edge from level k to level j.

        Returns None if the edge collapses under coarsening to an identity micro-step.
        """
        if self.edge_map is not None:
            if edge not in self.edge_map:
                raise KeyError(
                    f"Edge {edge!r} not in explicit edge_map of CoarseningMap({self.source_level} -> {self.target_level})"
                )
            return self.edge_map[edge]

        u_img = self.apply_state(edge.source)
        v_img = self.apply_state(edge.target)
        if u_img == v_img:
            return None
        return MoveEdge(source=u_img, target=v_img, label=edge.label, mu1=edge.mu1, mu2=edge.mu2)

    def compose(self, prior: CoarseningMap) -> CoarseningMap:
        """Compose self (pi_{i, j}) with prior (pi_{j, k}) to obtain pi_{i, k}.

        (self o prior)(x) = self(prior(x)).
        """
        if prior.target_level != self.source_level:
            raise ValueError(
                f"Composition level mismatch: prior targets level {prior.target_level} "
                f"but self sources level {self.source_level}"
            )

        new_state_map = {}
        for s_k, s_j in prior.state_map.items():
            if s_j not in self.state_map:
                raise ValueError(
                    f"State {s_k!r} mapped to intermediate state {s_j!r} which is outside domain of self"
                )
            new_state_map[s_k] = self.apply_state(s_j)

        new_edge_map: Optional[Dict[MoveEdge, Optional[MoveEdge]]] = None
        if prior.edge_map is not None and self.edge_map is not None:
            new_edge_map = {}
            for e_k, e_j in prior.edge_map.items():
                if e_j is None:
                    new_edge_map[e_k] = None
                else:
                    if e_j not in self.edge_map:
                        raise ValueError(
                            f"Intermediate edge {e_j!r} not in domain of self edge_map"
                        )
                    new_edge_map[e_k] = self.edge_map[e_j]

        return CoarseningMap(
            source_level=prior.source_level,
            target_level=self.target_level,
            state_map=new_state_map,
            edge_map=new_edge_map,
        )

    def is_surjective_on_states(self, target_graph: MoveGraph) -> bool:
        """Check whether coarsening map projects surjectively onto all states of target_graph."""
        return set(target_graph.states).issubset(set(self.state_map.values()))


    def check_morphism(
        self, source_graph: MoveGraph, target_graph: MoveGraph
    ) -> MorphismCheckResult:
        """Verify that this coarsening map is an admitted movegraph morphism source_graph -> target_graph."""
        defects: List[str] = []

        if self.source_level != source_graph.level:
            defects.append(
                f"Source level mismatch: map states {self.source_level}, graph is {source_graph.level}"
            )
        if self.target_level != target_graph.level:
            defects.append(
                f"Target level mismatch: map states {self.target_level}, graph is {target_graph.level}"
            )

        # Domain completeness
        missing_states = source_graph.states - set(self.state_map.keys())
        if missing_states:
            defects.append(
                f"State map domain incomplete; missing {len(missing_states)} states: {sorted(map(repr, missing_states))[:3]}"
            )

        # Codomain validity
        for s in source_graph.states:
            if s in self.state_map:
                img = self.state_map[s]
                if not target_graph.has_state(img):
                    defects.append(
                        f"State image {img!r} for source state {s!r} not in target graph states"
                    )

        # Transition preservation
        for e in source_graph.edges:
            if e.source in self.state_map and e.target in self.state_map:
                u_img = self.state_map[e.source]
                v_img = self.state_map[e.target]

                if self.edge_map is not None:
                    if e not in self.edge_map:
                        defects.append(f"Edge {e!r} missing from explicit edge_map")
                    else:
                        e_img = self.edge_map[e]
                        if e_img is None:
                            if u_img != v_img:
                                defects.append(
                                    f"Edge {e!r} marked collapsed to None, but endpoints map to distinct states ({u_img!r} != {v_img!r})"
                                )
                        else:
                            if e_img.source != u_img or e_img.target != v_img:
                                defects.append(
                                    f"Edge {e!r} mapped to {e_img!r}, but endpoint images are ({u_img!r}, {v_img!r})"
                                )
                            if e_img not in target_graph.edges:
                                defects.append(
                                    f"Mapped edge {e_img!r} does not belong to target graph edges"
                                )
                else:
                    # Structural homomorphism: image must be either identity collapse or admitted edge
                    if u_img != v_img:
                        if not target_graph.has_edge(u_img, v_img):
                            defects.append(
                                f"Transition {e.source!r} -> {e.target!r} maps to ({u_img!r}, {v_img!r}) which is not an edge in target graph"
                            )

        return MorphismCheckResult(
            is_valid=len(defects) == 0,
            source_level=self.source_level,
            target_level=self.target_level,
            defects=tuple(defects),
        )


@dataclass(frozen=True)
class CommutativityResult:
    """Outcome of functorial commutativity check pi_{j, k} o pi_{k, m} == pi_{j, m}."""

    commutes: bool
    levels: Tuple[int, int, int]
    discrepancies: Tuple[str, ...]

    def __bool__(self) -> bool:
        return self.commutes


def verify_commutativity(
    pi_jk: CoarseningMap,
    pi_km: CoarseningMap,
    pi_jm: CoarseningMap,
    domain_graph: Optional[MoveGraph] = None,
) -> CommutativityResult:
    """Verify functorial bonding commutativity: pi_{j, k} o pi_{k, m} == pi_{j, m} for j <= k <= m."""
    discrepancies: List[str] = []
    j = pi_jk.target_level
    k = pi_jk.source_level
    m = pi_km.source_level

    if pi_km.target_level != k:
        discrepancies.append(
            f"Level chain broken: pi_km targets {pi_km.target_level}, expected intermediate {k}"
        )
    if pi_jm.source_level != m or pi_jm.target_level != j:
        discrepancies.append(
            f"Direct map pi_jm has levels ({pi_jm.target_level}, {pi_jm.source_level}), expected ({j}, {m})"
        )

    states_to_check: Iterable[Any]
    if domain_graph is not None:
        if domain_graph.level != m:
            discrepancies.append(
                f"Domain graph level {domain_graph.level} does not match fine level {m}"
            )
        states_to_check = domain_graph.states
    else:
        states_to_check = set(pi_km.state_map.keys()) | set(pi_jm.state_map.keys())

    for s in states_to_check:
        # Evaluate composite
        if s not in pi_km.state_map:
            discrepancies.append(f"State {s!r} missing from pi_km state map")
            continue
        inter = pi_km.apply_state(s)

        if inter not in pi_jk.state_map:
            discrepancies.append(
                f"Intermediate state {inter!r} (from {s!r}) missing from pi_jk state map"
            )
            continue
        comp_img = pi_jk.apply_state(inter)

        if s not in pi_jm.state_map:
            discrepancies.append(f"State {s!r} missing from direct pi_jm state map")
            continue
        dir_img = pi_jm.apply_state(s)

        if comp_img != dir_img:
            discrepancies.append(
                f"State {s!r}: composite (pi_{j},{k} o pi_{k},{m})({s!r}) = {comp_img!r} != direct pi_{j},{m}({s!r}) = {dir_img!r}"
            )

    # Edge commutativity if edge maps exist
    if pi_km.edge_map is not None and pi_jk.edge_map is not None and pi_jm.edge_map is not None:
        edges_to_check: Iterable[MoveEdge]
        if domain_graph is not None:
            edges_to_check = domain_graph.edges
        else:
            edges_to_check = set(pi_km.edge_map.keys()) | set(pi_jm.edge_map.keys())

        for e in edges_to_check:
            e_inter = pi_km.edge_map.get(e)
            if e_inter is None:
                comp_e = None
            else:
                comp_e = pi_jk.edge_map.get(e_inter)
            dir_e = pi_jm.edge_map.get(e)

            if comp_e != dir_e:
                discrepancies.append(
                    f"Edge {e!r}: composite edge {comp_e!r} != direct edge {dir_e!r}"
                )

    return CommutativityResult(
        commutes=len(discrepancies) == 0,
        levels=(j, k, m),
        discrepancies=tuple(discrepancies),
    )


@dataclass(frozen=True)
class ThreadValidationResult:
    """Outcome of coherent thread verification in the projective limit."""

    is_coherent: bool
    levels: Tuple[int, ...]
    defects: Tuple[str, ...]

    def __bool__(self) -> bool:
        return self.is_coherent


@dataclass(frozen=True)
class OperationalPriceAtLevel:
    """Operational pricing calculated at a specific refinement level."""

    level: int
    price: OperationalPrice


@dataclass(frozen=True)
class MetricAxiomResult:
    """Verification receipt for endogenous metric axioms on a movegraph."""

    satisfies_axioms: bool
    level: int
    tested_pairs: int
    tested_triples: int
    defects: Tuple[str, ...]

    def __bool__(self) -> bool:
        return self.satisfies_axioms


@dataclass(frozen=True)
class ProjectiveSystem:
    """Inverse limit projective system over a directed family of discrete movegraphs.

    Attributes:
        graphs: Mapping from refinement level k to MoveGraph M_k.
        bonding_maps: Mapping from pair (j, k) with j <= k to CoarseningMap pi_{j, k}.
    """

    graphs: Mapping[int, MoveGraph]
    bonding_maps: Mapping[Tuple[int, int], CoarseningMap]

    def __post_init__(self) -> None:
        # Defensive copy
        object.__setattr__(self, "graphs", dict(self.graphs))
        object.__setattr__(self, "bonding_maps", dict(self.bonding_maps))

    @classmethod
    def build(
        cls,
        graphs: Sequence[MoveGraph],
        bonding_maps: Sequence[CoarseningMap] = (),
    ) -> ProjectiveSystem:
        """Construct a ProjectiveSystem, automatically computing identities and compositions if only consecutive maps are given."""
        g_map = {g.level: g for g in graphs}
        sorted_levels = sorted(g_map.keys())

        b_map: Dict[Tuple[int, int], CoarseningMap] = {}

        # Insert supplied bonding maps
        for bm in bonding_maps:
            b_map[(bm.target_level, bm.source_level)] = bm

        # Ensure canonical identity map for every level
        for lvl in sorted_levels:
            if (lvl, lvl) not in b_map:
                b_map[(lvl, lvl)] = CoarseningMap.identity(g_map[lvl])

        # If consecutive maps exist, compute transitive closures
        for length in range(2, len(sorted_levels) + 1):
            for i in range(len(sorted_levels) - length + 1):
                j_idx = i
                m_idx = i + length - 1
                j_lvl = sorted_levels[j_idx]
                m_lvl = sorted_levels[m_idx]

                if (j_lvl, m_lvl) not in b_map:
                    # Find an intermediate k to compose
                    for k_idx in range(j_idx + 1, m_idx + 1):
                        k_lvl = sorted_levels[k_idx]
                        if (j_lvl, k_lvl) in b_map and (k_lvl, m_lvl) in b_map:
                            pi_jk = b_map[(j_lvl, k_lvl)]
                            pi_km = b_map[(k_lvl, m_lvl)]
                            b_map[(j_lvl, m_lvl)] = pi_jk.compose(pi_km)
                            break

        return cls(graphs=g_map, bonding_maps=b_map)

    @property
    def levels(self) -> Tuple[int, ...]:
        return tuple(sorted(self.graphs.keys()))

    def get_bonding_map(self, target_level: int, source_level: int) -> CoarseningMap:
        pair = (target_level, source_level)
        if pair not in self.bonding_maps:
            raise KeyError(
                f"No bonding map pi_{target_level},{source_level} in ProjectiveSystem"
            )
        return self.bonding_maps[pair]

    def verify_system(self) -> Tuple[bool, Tuple[str, ...]]:
        """Verify full system consistency: morphism validity, identities, and pairwise commutativity."""
        defects: List[str] = []
        lvls = self.levels

        # 1. Morphism verification for all bonding maps
        for (j, k), bm in self.bonding_maps.items():
            if j not in self.graphs:
                defects.append(f"Bonding map target level {j} has no corresponding graph")
                continue
            if k not in self.graphs:
                defects.append(f"Bonding map source level {k} has no corresponding graph")
                continue
            res = bm.check_morphism(self.graphs[k], self.graphs[j])
            if not res.is_valid:
                defects.extend([f"pi_{j},{k} invalid morphism: {err}" for err in res.defects])

        # 2. Identity map verification
        for k in lvls:
            if (k, k) not in self.bonding_maps:
                defects.append(f"Missing identity bonding map at level {k}")
            else:
                id_map = self.bonding_maps[(k, k)]
                g_k = self.graphs[k]
                for s in g_k.states:
                    if id_map.apply_state(s) != s:
                        defects.append(f"Identity map at level {k} mutates state {s!r}")

        # 3. Functorial commutativity across all triples j <= k <= m
        for i_idx, j in enumerate(lvls):
            for k_idx in range(i_idx, len(lvls)):
                k = lvls[k_idx]
                for m_idx in range(k_idx, len(lvls)):
                    m = lvls[m_idx]
                    if (j, k) in self.bonding_maps and (k, m) in self.bonding_maps and (j, m) in self.bonding_maps:
                        pi_jk = self.bonding_maps[(j, k)]
                        pi_km = self.bonding_maps[(k, m)]
                        pi_jm = self.bonding_maps[(j, m)]
                        c_res = verify_commutativity(pi_jk, pi_km, pi_jm, self.graphs[m])
                        if not c_res.commutes:
                            defects.extend([
                                f"Commutativity defect ({j} <= {k} <= {m}): {d}"
                                for d in c_res.discrepancies
                            ])

        return len(defects) == 0, tuple(defects)

    def validate_thread(
        self, thread: Mapping[int, Any] | Sequence[Any]
    ) -> ThreadValidationResult:
        """Validate whether a state sequence or mapping forms a coherent thread in varprojlim M_k.

        A thread (x_k)_k is coherent if for all j <= k, pi_{j, k}(x_k) == x_j.
        """
        defects: List[str] = []

        thread_dict: Dict[int, Any]
        if isinstance(thread, (list, tuple)):
            if len(thread) != len(self.levels):
                defects.append(
                    f"Thread sequence length {len(thread)} does not match system levels count {len(self.levels)}"
                )
            thread_dict = {lvl: thread[idx] for idx, lvl in enumerate(self.levels[:len(thread)])}
        else:
            thread_dict = dict(thread)

        # Check state presence in corresponding graphs
        for lvl, s in thread_dict.items():
            if lvl not in self.graphs:
                defects.append(f"Thread specifies level {lvl} which is not in the system")
            elif not self.graphs[lvl].has_state(s):
                defects.append(f"Thread state {s!r} at level {lvl} is not in M_{lvl}.states")

        # Check bonding coherence pi_{j, k}(x_k) == x_j
        sorted_thread_lvls = sorted(thread_dict.keys())
        for i_idx, j in enumerate(sorted_thread_lvls):
            for k in sorted_thread_lvls[i_idx + 1:]:
                if (j, k) in self.bonding_maps:
                    pi_jk = self.bonding_maps[(j, k)]
                    x_k = thread_dict[k]
                    x_j = thread_dict[j]
                    try:
                        projected = pi_jk.apply_state(x_k)
                        if projected != x_j:
                            defects.append(
                                f"Thread coherence failure at ({j} <= {k}): "
                                f"pi_{j},{k}({x_k!r}) = {projected!r} != x_{j} = {x_j!r}"
                            )
                    except KeyError as exc:
                        defects.append(f"Bonding projection error: {exc}")

        return ThreadValidationResult(
            is_coherent=len(defects) == 0,
            levels=tuple(sorted_thread_lvls),
            defects=tuple(defects),
        )

    def enumerate_coherent_threads(
        self, levels: Optional[Sequence[int]] = None
    ) -> Tuple[Dict[int, Any], ...]:
        """Exhaustively enumerate all coherent threads in varprojlim M_k for the requested levels."""
        target_levels = tuple(levels) if levels is not None else self.levels
        if not target_levels:
            return ()

        # Backtracking search from coarse to fine
        results: List[Dict[int, Any]] = []

        def search(idx: int, current_thread: Dict[int, Any]) -> None:
            if idx == len(target_levels):
                results.append(dict(current_thread))
                return

            curr_lvl = target_levels[idx]
            g_curr = self.graphs[curr_lvl]

            if idx == 0:
                # Root level: try all states
                for s in sorted(g_curr.states, key=repr):
                    current_thread[curr_lvl] = s
                    search(idx + 1, current_thread)
                    del current_thread[curr_lvl]
            else:
                # Finer level: filter states that project onto all earlier chosen states
                for s in sorted(g_curr.states, key=repr):
                    compatible = True
                    for prev_idx in range(idx):
                        prev_lvl = target_levels[prev_idx]
                        pi = self.get_bonding_map(prev_lvl, curr_lvl)
                        if pi.apply_state(s) != current_thread[prev_lvl]:
                            compatible = False
                            break
                    if compatible:
                        current_thread[curr_lvl] = s
                        search(idx + 1, current_thread)
                        del current_thread[curr_lvl]

        search(0, {})
        return tuple(results)

    def compute_path_pricing(self, path: Sequence[MoveEdge]) -> OperationalPrice:
        """Calculate exact rational operational price accumulation (Sigma mu1, Sigma mu2) along a transition path."""
        price = OperationalPrice.zero()
        for edge in path:
            price = price.add_edge(edge)
        return price

    def operational_distance(
        self,
        level: int,
        source: Any,
        target: Any,
        cost_func: Callable[[MoveEdge], Union[Fraction, int]] = lambda e: e.mu1,
    ) -> Optional[Fraction]:
        """Compute the endogenous operational distance d_k(source, target) = min Sigma mu1.

        Uses exact rational Dijkstra search on M_k without external coordinates.
        Returns None if target is unreachable from source.
        """
        graph = self.graphs[level]
        if source not in graph.states or target not in graph.states:
            return None
        if source == target:
            return Fraction(0, 1)

        dist: Dict[Any, Fraction] = {source: Fraction(0, 1)}
        visited: Set[Any] = set()

        # Priority queue stores tuples of (Fraction, tie_breaker_int, state)
        pq: List[Tuple[Fraction, int, Any]] = [(Fraction(0, 1), 0, source)]
        counter = 1

        while pq:
            d, _, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)

            if u == target:
                return d

            for edge in graph.outgoing(u):
                v = edge.target
                w = _to_fraction(cost_func(edge), "edge cost")
                new_d = d + w
                if v not in dist or new_d < dist[v]:
                    dist[v] = new_d
                    heapq.heappush(pq, (new_d, counter, v))
                    counter += 1

        return dist.get(target, None)


    def verify_endogenous_metric(self, level: int) -> MetricAxiomResult:
        """Verify metric axioms on M_k without external Euclidean space:

        1. Non-negativity: d_k(u, v) >= 0.
        2. Identity of indiscernibles: d_k(u, u) == 0.
        3. Triangle inequality: d_k(u, w) <= d_k(u, v) + d_k(v, w) (for all reachable paths).
        """
        graph = self.graphs[level]
        states = sorted(graph.states, key=repr)
        n = len(states)
        defects: List[str] = []

        # Precompute all-pairs operational distance table
        dist_table: Dict[Tuple[Any, Any], Optional[Fraction]] = {}
        for u in states:
            for v in states:
                dist_table[(u, v)] = self.operational_distance(level, u, v)

        # 1 & 2. Non-negativity and identity
        pair_count = 0
        for u in states:
            for v in states:
                d = dist_table[(u, v)]
                pair_count += 1
                if u == v:
                    if d != Fraction(0, 1):
                        defects.append(f"Identity failure: d({u!r}, {u!r}) = {d} != 0")
                elif d is not None and d < 0:
                    defects.append(f"Negative distance: d({u!r}, {v!r}) = {d} < 0")

        # 3. Triangle inequality across all triples
        triple_count = 0
        for u in states:
            for v in states:
                d_uv = dist_table[(u, v)]
                if d_uv is None:
                    continue
                for w in states:
                    triple_count += 1
                    d_vw = dist_table[(v, w)]
                    d_uw = dist_table[(u, w)]
                    if d_vw is not None:
                        direct_bound = d_uv + d_vw
                        if d_uw is None:
                            defects.append(
                                f"Reachability anomaly: path u->v and v->w exist but u->w unreachable: "
                                f"d({u!r}, {v!r})={d_uv}, d({v!r}, {w!r})={d_vw}"
                            )
                        elif d_uw > direct_bound:
                            defects.append(
                                f"Triangle inequality violated: d({u!r}, {w!r}) = {d_uw} > "
                                f"d({u!r}, {v!r}) + d({v!r}, {w!r}) = {d_uv} + {d_vw} = {direct_bound}"
                            )

        return MetricAxiomResult(
            satisfies_axioms=len(defects) == 0,
            level=level,
            tested_pairs=pair_count,
            tested_triples=triple_count,
            defects=tuple(defects),
        )

    def pricing_along_threads(
        self,
        thread_x: Mapping[int, Any],
        thread_y: Mapping[int, Any],
    ) -> Tuple[OperationalPriceAtLevel, ...]:
        """Calculate the operational pricing sequence connecting thread states x_k to y_k across refinement levels."""
        shared_levels = sorted(set(thread_x.keys()) & set(thread_y.keys()) & set(self.graphs.keys()))
        sequence: List[OperationalPriceAtLevel] = []

        for lvl in shared_levels:
            u = thread_x[lvl]
            v = thread_y[lvl]
            dist_mu1 = self.operational_distance(lvl, u, v, cost_func=lambda e: e.mu1)
            dist_mu2 = self.operational_distance(lvl, u, v, cost_func=lambda e: e.mu2)

            if dist_mu1 is not None and dist_mu2 is not None:
                price = OperationalPrice(mu1_sum=dist_mu1, mu2_sum=dist_mu2, step_count=1)
            else:
                price = OperationalPrice.zero()

            sequence.append(OperationalPriceAtLevel(level=lvl, price=price))

        return tuple(sequence)

    def pricing_along_path_sequence(
        self,
        paths: Mapping[int, Sequence[MoveEdge]],
    ) -> Tuple[OperationalPriceAtLevel, ...]:
        """Calculate the operational pricing accumulation along a projective sequence of refinement paths."""
        sequence: List[OperationalPriceAtLevel] = []
        for lvl in sorted(paths.keys()):
            if lvl in self.graphs:
                p = paths[lvl]
                price = self.compute_path_pricing(p)
                sequence.append(OperationalPriceAtLevel(level=lvl, price=price))
        return tuple(sequence)

    def verify_pricing_stabilization(
        self,
        sequence: Sequence[OperationalPriceAtLevel],
        tolerance: Optional[Fraction] = None,
    ) -> Dict[str, Any]:
        """Analyze Cauchy variation and stabilization of operational pricing along a refinement sequence."""
        if len(sequence) < 2:
            return {
                "stabilized": True,
                "is_cauchy": True,
                "consecutive_deltas": (),
                "max_delta": Fraction(0, 1),
            }

        deltas: List[Tuple[int, int, Fraction]] = []
        for i in range(len(sequence) - 1):
            p1 = sequence[i]
            p2 = sequence[i + 1]
            q1 = _to_fraction(p1.price.mu1_sum, "mu1_sum")
            q2 = _to_fraction(p2.price.mu1_sum, "mu1_sum")
            d = abs(q2 - q1)
            deltas.append((p1.level, p2.level, d))


        max_delta = max(d for _, _, d in deltas)
        tol = tolerance if tolerance is not None else Fraction(0, 1)
        is_cauchy = all(d <= tol for _, _, d in deltas[-1:])


        return {
            "stabilized": max_delta == Fraction(0, 1),
            "is_cauchy": is_cauchy,
            "consecutive_deltas": tuple(deltas),
            "max_delta": max_delta,
        }


# =============================================================================
# Canonical Projective Systems & Generators
# =============================================================================


def create_dyadic_movegraph(level: int, length: int = 1) -> MoveGraph:
    """Create a discrete dyadic refinement movegraph representing a subdivided interval.

    Refinement level k has length * 2^k + 1 states {0, 1, ..., length * 2^k}.
    Transitions have exact operational step costs:
      mu1 = 1 / 2^k  (dyadic length unit)
      mu2 = 1 / 4^k  (higher-order quadratic dissipation)
    """
    if level < 0:
        raise ValueError(f"level must be non-negative, got {level}")
    if length <= 0:
        raise ValueError(f"length must be positive, got {length}")

    n_segments = length * (2**level)
    states = list(range(n_segments + 1))
    step_mu1 = Fraction(1, 2**level)
    step_mu2 = Fraction(1, 4**level)

    edges: List[MoveEdge] = []
    for i in range(n_segments):
        # Forward transition
        edges.append(
            MoveEdge(
                source=i,
                target=i + 1,
                label=f"step_{i}->{i+1}",
                mu1=step_mu1,
                mu2=step_mu2,
            )
        )
        # Backward transition
        edges.append(
            MoveEdge(
                source=i + 1,
                target=i,
                label=f"step_{i+1}->{i}",
                mu1=step_mu1,
                mu2=step_mu2,
            )
        )

    return MoveGraph.build(level=level, states=states, edges=edges)


def create_dyadic_coarsening_map(
    coarse_level: int, fine_level: int, length: int = 1
) -> CoarseningMap:
    """Construct the canonical coarsening projection pi_{j, k} from fine dyadic level k to coarse level j.

    Each micro-state x in M_k projects to floor(x / 2^(k-j)) in M_j.
    """
    if coarse_level > fine_level:
        raise ValueError(
            f"coarse_level must be <= fine_level, got {coarse_level} > {fine_level}"
        )

    scale = 2 ** (fine_level - coarse_level)
    fine_segments = length * (2**fine_level)

    state_map: Dict[int, int] = {}
    for x in range(fine_segments + 1):
        state_map[x] = x // scale

    return CoarseningMap(
        source_level=fine_level,
        target_level=coarse_level,
        state_map=state_map,
    )


def create_dyadic_projective_system(max_level: int, length: int = 1) -> ProjectiveSystem:
    """Construct an endogenously refined dyadic projective system across levels 0 <= k <= max_level."""
    graphs = [create_dyadic_movegraph(k, length=length) for k in range(max_level + 1)]
    bonding_maps: List[CoarseningMap] = []

    for j in range(max_level + 1):
        for k in range(j, max_level + 1):
            bonding_maps.append(create_dyadic_coarsening_map(j, k, length=length))

    return ProjectiveSystem.build(graphs=graphs, bonding_maps=bonding_maps)


def create_discrete_circle_movegraph(level: int) -> MoveGraph:
    """Create a discrete circle movegraph C_{2^k} with 2^k states in a directed cycle."""
    if level < 0:
        raise ValueError(f"level must be non-negative, got {level}")

    num_states = max(3, 2**level) if level > 0 else 3
    states = list(range(num_states))
    step_mu1 = Fraction(1, num_states)
    step_mu2 = Fraction(1, num_states**2)

    edges: List[MoveEdge] = []
    for i in range(num_states):
        nxt = (i + 1) % num_states
        edges.append(
            MoveEdge(
                source=i,
                target=nxt,
                label=f"circle_{i}->{nxt}",
                mu1=step_mu1,
                mu2=step_mu2,
            )
        )

    return MoveGraph.build(level=level, states=states, edges=edges)
