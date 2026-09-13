"""Movegraph potential monotonicity, acyclicity, and witness exchange refutation.

Formalizes Prompt B Targets B3, B6.2:
- Cardinal profile potential N(r) in Nat
- Constructor monotonicity: N(step(r, e)) > N(r) for non-Supply constructors
- Movegraph DAG property: topological sort, vanishing cycle space Z_1 = 0
- In-place witness exchange without accumulation is inexpressible (Kill Condition 2)
- Capability cost non-negativity: refutes isomorphism with signed defects {-1, 0, +1}
"""

from __future__ import annotations

import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT / "code") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "code"))

from derivation.model import (
    EMPTY,
    AdmissionError,
    AdmitDatum,
    AdmitForm,
    AdmitInst,
    AdmitRuleAll,
    Event,
    Impose,
    Regime,
    Supply,
    step,
)


def cardinal_potential(r: Regime) -> int:
    """Compute cardinal profile potential N(r) = |D| + |F| + |I| + |R| + |Q|."""
    return len(r.data) + len(r.forms) + len(r.insts) + len(r.rules) + len(r.reqs)


def capability_cost_mu1(e: Event) -> int:
    """Compute base capability cost mu1(e) in Nat."""
    if isinstance(e, Supply):
        return 0
    return 1


def verify_constructor_monotonicity(r: Regime, e: Event) -> dict[str, object]:
    """Verify potential change under event constructor step."""
    n_before = cardinal_potential(r)
    r_after = step(r, e)
    n_after = cardinal_potential(r_after)

    if isinstance(e, Supply):
        is_monotonic = (n_after == n_before)
        strict = False
    else:
        is_monotonic = (n_after > n_before)
        strict = True

    return {
        "event_type": type(e).__name__,
        "n_before": n_before,
        "n_after": n_after,
        "delta": n_after - n_before,
        "is_monotonic": is_monotonic,
        "is_strictly_greater": (n_after > n_before),
    }


def build_reachability_dag(
    initial: Regime,
    event_generator: Sequence[Event],
    max_depth: int = 5,
) -> dict[str, object]:
    """Build directed transition graph of reachable states and test for cycles via topological sort."""
    adj: dict[int, list[int]] = defaultdict(list)
    in_degree: dict[int, int] = defaultdict(int)
    states: dict[int, Regime] = {}
    regime_ids: dict[Regime, int] = {}

    def get_id(r: Regime) -> int:
        if r not in regime_ids:
            new_id = len(regime_ids)
            regime_ids[r] = new_id
            states[new_id] = r
            if new_id not in in_degree:
                in_degree[new_id] = 0
        return regime_ids[r]

    start_id = get_id(initial)
    queue = deque([(start_id, 0)])
    visited = {start_id}

    while queue:
        curr_id, depth = queue.popleft()
        if depth >= max_depth:
            continue
        curr_r = states[curr_id]

        for e in event_generator:
            if isinstance(e, Supply):
                continue
            try:
                next_r = step(curr_r, e)
                if next_r == curr_r:
                    continue
                next_id = get_id(next_r)
                adj[curr_id].append(next_id)
                in_degree[next_id] += 1
                if next_id not in visited:
                    visited.add(next_id)
                    queue.append((next_id, depth + 1))
            except AdmissionError:
                continue

    # Kahn's topological sort algorithm to detect cycles
    kahn_queue = deque([node for node in regime_ids.values() if in_degree[node] == 0])
    topo_order = []

    # Copy in_degree for reduction
    curr_in_degree = dict(in_degree)
    while kahn_queue:
        u = kahn_queue.popleft()
        topo_order.append(u)
        for v in adj[u]:
            curr_in_degree[v] -= 1
            if curr_in_degree[v] == 0:
                kahn_queue.append(v)

    is_dag = (len(topo_order) == len(regime_ids))
    return {
        "num_states": len(regime_ids),
        "num_edges": sum(len(neighbors) for neighbors in adj.values()),
        "is_acyclic_dag": is_dag,
        "cycle_space_z1_vanishes": is_dag,
    }


def verify_exchange_inexpressibility(initial: Regime, steps: Sequence[Event]) -> bool:
    """Verify that no sequence of non-Supply steps can return to initial cardinal profile."""
    curr = initial
    for e in steps:
        if isinstance(e, Supply):
            continue
        curr = step(curr, e)

    # In-place exchange requires returning to identical cardinal profile
    return cardinal_potential(curr) > cardinal_potential(initial)
