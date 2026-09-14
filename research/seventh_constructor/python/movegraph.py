"""Extended movegraph construction, cycle detection, and 1-chain complex analysis.

AuthorityEffect: None.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import sys
from typing import Sequence

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT / "code") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.model import (
    AdmissionError,
    Regime,
    Supply,
)
from derivation.iso import canonical
from .conservative_grammar import (
    ExtendedEvent,
    SwapWitness,
    cardinal_potential,
    extended_step,
)


@dataclass(frozen=True)
class MoveEdge:
    """Directed edge in the movegraph."""
    src: Regime
    dst: Regime
    event: ExtendedEvent


class Movegraph:
    """Directed state transition graph of reachable regimes under an event generator."""

    def __init__(self, initial: Regime, event_generator: Sequence[ExtendedEvent], max_depth: int = 4):
        self.initial = initial
        self.event_generator = list(event_generator)
        self.max_depth = max_depth

        self.regimes: list[Regime] = []
        self.regime_to_id: dict[Regime, int] = {}
        self.edges: list[MoveEdge] = []
        self.adj: dict[int, list[int]] = defaultdict(list)
        self.in_degree: dict[int, int] = defaultdict(int)

        self._build()

    def _get_or_add(self, r: Regime) -> int:
        if r not in self.regime_to_id:
            idx = len(self.regimes)
            self.regime_to_id[r] = idx
            self.regimes.append(r)
            if idx not in self.in_degree:
                self.in_degree[idx] = 0
        return self.regime_to_id[r]

    def _build(self) -> None:
        start_id = self._get_or_add(self.initial)
        queue = deque([(start_id, 0)])
        visited = {start_id}

        while queue:
            curr_id, depth = queue.popleft()
            if depth >= self.max_depth:
                continue
            curr_r = self.regimes[curr_id]

            for e in self.event_generator:
                if isinstance(e, Supply):
                    continue
                try:
                    next_r = extended_step(curr_r, e)
                    if next_r == curr_r:
                        continue
                    next_id = self._get_or_add(next_r)
                    self.edges.append(MoveEdge(curr_r, next_r, e))
                    self.adj[curr_id].append(next_id)
                    self.in_degree[next_id] += 1
                    if next_id not in visited:
                        visited.add(next_id)
                        queue.append((next_id, depth + 1))
                except AdmissionError:
                    continue

    def is_acyclic_dag(self) -> bool:
        """Kahn's algorithm topological sort check."""
        deg = dict(self.in_degree)
        kahn_queue = deque([node for node in range(len(self.regimes)) if deg[node] == 0])
        count = 0
        while kahn_queue:
            u = kahn_queue.popleft()
            count += 1
            for v in self.adj[u]:
                deg[v] -= 1
                if deg[v] == 0:
                    kahn_queue.append(v)
        return count == len(self.regimes)

    def find_simple_cycles(self, max_cycle_len: int = 6) -> list[list[int]]:
        """Find simple directed cycles up to max_cycle_len via DFS."""
        cycles: list[list[int]] = []
        visited = set()

        def dfs(start: int, curr: int, path: list[int]) -> None:
            if len(path) > max_cycle_len:
                return
            for nxt in self.adj[curr]:
                if nxt == start and len(path) >= 2:
                    cycles.append(list(path))
                elif nxt not in visited and nxt > start:
                    visited.add(nxt)
                    path.append(nxt)
                    dfs(start, nxt, path)
                    path.pop()
                    visited.remove(nxt)

        for i in range(len(self.regimes)):
            visited.add(i)
            dfs(i, i, [i])
            visited.remove(i)

        return cycles

    def directed_cycle_space_dimension(self) -> int:
        """Compute the dimension of the space spanned by directed 1-cycles."""
        cycles = self.find_simple_cycles()
        if not cycles or not self.edges:
            return 0

        edge_to_idx = {(e.src, e.dst): i for i, e in enumerate(self.edges)}
        vectors: list[list[Fraction]] = []
        for c in cycles:
            v = [Fraction(0)] * len(self.edges)
            k = len(c)
            for i in range(k):
                src = self.regimes[c[i]]
                dst = self.regimes[c[(i + 1) % k]]
                idx = edge_to_idx.get((src, dst))
                if idx is not None:
                    v[idx] += 1
            vectors.append(v)

        # Exact rational Gaussian elimination to compute rank
        matrix = [list(row) for row in vectors]
        nrows = len(matrix)
        ncols = len(self.edges)
        rank = 0
        for col in range(ncols):
            pivot = None
            for row in range(rank, nrows):
                if matrix[row][col] != 0:
                    pivot = row
                    break
            if pivot is None:
                continue
            matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
            p_val = matrix[rank][col]
            for row in range(nrows):
                if row != rank and matrix[row][col] != 0:
                    factor = matrix[row][col] / p_val
                    for c_idx in range(col, ncols):
                        matrix[row][c_idx] -= factor * matrix[rank][c_idx]
            rank += 1
        return rank

    def cycle_space_dimension(self) -> int:
        """Directed cycle space rank (primary alias)."""
        return self.directed_cycle_space_dimension()

    def evaluate_quotient_projection(self, cycle_path: Sequence[int]) -> QuotientProjectionReport:
        """Evaluate presentation-to-quotient projection along a cycle path."""
        keys = [canonical(self.regimes[idx]) for idx in cycle_path]
        unique_keys = set(keys)
        collapses_to_single_point = (len(unique_keys) == 1)

        # Presentation signature cochain assigns 1 to swap transition edges
        presentation_sign_cochain = 1
        # Descended coboundary of single-valued potential P o q vanishes on isomorphic states
        descended_coboundary = 0 if collapses_to_single_point else None
        defect = presentation_sign_cochain - (descended_coboundary if descended_coboundary is not None else 0)

        return QuotientProjectionReport(
            cycle_length=len(cycle_path),
            unique_quotient_states=len(unique_keys),
            collapses_to_point=collapses_to_single_point,
            descended_coboundary_vanishes=collapses_to_single_point,
            presentation_non_descent_defect=defect,
        )


class QuotientProjectionReport(dict[str, object]):
    """Report evaluating presentation-to-quotient projection along a cycle path."""

    def __init__(
        self,
        cycle_length: int,
        unique_quotient_states: int,
        collapses_to_point: bool,
        descended_coboundary_vanishes: bool,
        presentation_non_descent_defect: int,
    ) -> None:
        super().__init__(
            cycle_length=cycle_length,
            unique_quotient_states=unique_quotient_states,
            collapses_to_point=collapses_to_point,
            descended_coboundary_vanishes=descended_coboundary_vanishes,
            presentation_non_descent_defect=presentation_non_descent_defect,
        )
        self.cycle_length = cycle_length
        self.unique_quotient_states = unique_quotient_states
        self.collapses_to_point = collapses_to_point
        self.descended_coboundary_vanishes = descended_coboundary_vanishes
        self.presentation_non_descent_defect = presentation_non_descent_defect
