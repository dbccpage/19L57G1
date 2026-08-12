"""Computational mirror of the native primitive-difference interface.

Classification: metatheory apparatus for
``paper/difference_interface.md``.  The theorem package lives in
``lean4/Derivation/DiffInterface.lean``; this module recomputes its
concrete realization deterministically and exports the trajectories:

* the reflective tower (kernel observers of horizon-capped ranks),
  its per-round obstruction pipeline (reflection certificate ->
  retained/protected zero-pair -> active obstruction -> map-saturated
  closure), the declared measure, and the uniform demand bound;
* the fuel driver and its termination behaviour;
* the bounded-grammar family (Boolean views over three protected
  points), where no view closes the stage, together with available
  extension-proposal data — checked exhaustively over all eight views;
* the five countermodels (freshness, tagging, an edge, a new hash,
  repetition), each showing the feature without observer-visible
  difference and without an active obstruction when protection is
  absent.

No model judgment decides anything: separability is view equality,
activity is the three-way conjunction, and every check is exhaustive
within its declared bounds.
"""

from __future__ import annotations

from itertools import product
from typing import Callable, Literal, Optional

ROUNDS = 15
State = tuple[int, int]
NextAction = (
    tuple[Literal["step"], State]
    | tuple[Literal["proposal"], object]
)
DriveResult = (
    tuple[Literal["closed", "out_of_fuel"], State, None]
    | tuple[Literal["proposal"], State, object]
)


def cview(h: int, i: int) -> int:
    return min(i, h)


def active_pairs(s: int, h: int) -> list[tuple[int, int]]:
    """Ordered retained, protected, observer-zero pairs: the declared
    measure counts these."""
    return [
        (i, j)
        for i in range(s)
        for j in range(s)
        if i != j and cview(h, i) == cview(h, j)
    ]


def measure(s: int, h: int) -> int:
    return len(active_pairs(s, h))


def swap_top(n: int, x: int) -> int:
    return x if x < n else 2 * n + 1 - x


def tower_demand_support(n: int) -> list[tuple[int, int]]:
    """Finite evidence enumerating the map-saturated demand predicate.

    The abstract interface uses a predicate; this sorted list is only
    the deterministic concrete witness used for checking and export.
    """
    base = [(n, n + 1), (n + 1, n)]
    support = {(x, y) for (x, y) in base}
    support |= {(swap_top(n, x), swap_top(n, y)) for (x, y) in base}
    return sorted(support)


def tower_round(n: int) -> dict[str, object]:
    """One pipeline round: closed stage -> bare reflection (stale
    observer) -> active obstruction -> map-saturated closure -> next closed
    stage."""
    closed_before = measure(n + 1, n)
    pre_close = measure(n + 2, n)
    support = tower_demand_support(n)
    parent_new_zero = cview(n, n) == cview(n, n + 1)
    after = measure(n + 2, n + 1)
    old_pairs_preserved = all(
        cview(n + 1, i) != cview(n + 1, j)
        for i in range(n + 1)
        for j in range(n + 1)
        if i != j and cview(n, i) != cview(n, j)
    )
    return {
        "round": n,
        "closed_measure_before": closed_before,
        "reflected_pair": [n, n + 1],
        "parent_new_zero_pre_closure": parent_new_zero,
        "preclose_measure": pre_close,
        "demand_support": [list(p) for p in support],
        "demand_support_size": len(support),
        "closed_measure_after": after,
        "strict_decrease": after < pre_close,
        "old_distinctions_preserved": old_pairs_preserved,
    }


def tower_report(rounds: int = ROUNDS) -> dict[str, object]:
    rows = [tower_round(n) for n in range(rounds)]
    support_sizes = [len(tower_demand_support(n)) for n in range(rounds)]
    return {
        "rounds": rows,
        "uniform_demand_bound": max(support_sizes),
        "all_strictly_decrease": all(r["strict_decrease"] for r in rows),
        "all_preserve_old": all(
            r["old_distinctions_preserved"] for r in rows
        ),
        "all_closed_before": all(
            r["closed_measure_before"] == 0 for r in rows
        ),
        "all_obstruct_after_reflection": all(
            measure(n + 2, n) > 0 for n in range(rounds)
        ),
    }


def drive(
    next_fn: Callable[[State], Optional[NextAction]],
    fuel: int,
    state: State,
) -> DriveResult:
    """Return the terminal state and preserve any proposal payload."""
    for _ in range(fuel):
        action = next_fn(state)
        if action is None:
            return ("closed", state, None)
        if action[0] == "proposal":
            return ("proposal", state, action[1])
        state = action[1]
    return ("out_of_fuel", state, None)


def tower_next(
    state: State,
) -> Optional[tuple[Literal["step"], State]]:
    s, h = state
    if not active_pairs(s, h):
        return None
    return ("step", (s, s - 1))


def fuel_report(rounds: int = ROUNDS) -> dict[str, object]:
    """Termination with fuel exceeding the declared measure, per
    pre-closure stage of the tower."""
    rows = []
    for n in range(rounds):
        mu = measure(n + 2, n)
        outcome, final, _proposal = drive(
            tower_next, mu + 1, (n + 2, n)
        )
        rows.append(
            {
                "round": n,
                "measure": mu,
                "fuel": mu + 1,
                "outcome": outcome,
                "final_state": list(final),
            }
        )
    return {
        "rows": rows,
        "all_terminate_closed": all(
            r["outcome"] == "closed" for r in rows
        ),
    }


def bool_views() -> list[tuple[int, ...]]:
    """All observers of the bounded grammar: Boolean views of the three
    protected points, as value tuples."""
    return [tuple(v) for v in product((0, 1), repeat=3)]


def bool_grammar_report() -> dict[str, object]:
    """Exhaustive over the grammar: every view (hence every in-grammar
    replacement view) leaves an active obstruction among three protected
    points.  Proposal data is available, but no decision procedure is
    claimed here."""
    rows = []
    for view in bool_views():
        collisions = [
            (i, j)
            for i in range(3)
            for j in range(i + 1, 3)
            if view[i] == view[j]
        ]
        rows.append(
            {
                "view": list(view),
                "surviving_obstructions": [list(p) for p in collisions],
            }
        )
    return {
        "views_checked": len(rows),
        "rows": rows,
        "every_view_obstructed": all(
            bool(r["surviving_obstructions"]) for r in rows
        ),
        "no_view_closed": all(
            bool(r["surviving_obstructions"]) for r in rows
        ),
        "available_proposal_kind": "observerStructure",
    }


def obstruction_active(*, retained: bool, zero: bool, guarded: bool) -> bool:
    """Compute the three-conjunct activity definition used by the report."""
    return retained and zero and guarded


def countermodel_report() -> dict[str, object]:
    """The five separations.  ``zero`` records observer-blindness on a
    distinct pair.  Every row records an unprotected stage and computes
    activity from the three conjuncts rather than storing the result."""
    fresh_zero = cview(0, 0) == cview(0, 1)
    tag = [int(0 < i) for i in range(3)]
    tag_zero = tag[1] == tag[2]
    edges = [(0, 1)]
    incid = [
        int(any(a == i or b == i for (a, b) in edges)) for i in range(2)
    ]
    edge_zero = incid[0] == incid[1]
    hashes = [0, 1]  # metatheoretically injective labels
    hash_distinct = hashes[0] != hashes[1]
    hash_zero = True  # constant view: delta lands on the diagonal
    token = ["<>", "<>"]
    rep_zero = token[0] == token[1]
    features = [
        ("freshness", True, fresh_zero),
        ("tagging", tag[1] == 1 and tag[2] == 1, tag_zero),
        ("edge", bool(edges), edge_zero),
        ("new_hash", hash_distinct, hash_zero),
        ("repetition", len(token) == 2, rep_zero),
    ]
    rows = []
    for feature, feature_present, zero in features:
        retained = True
        guarded = False
        rows.append(
            {
                "feature": feature,
                "feature_present": feature_present,
                "retained": retained,
                "zero": zero,
                "guarded": guarded,
                "active": obstruction_active(
                    retained=retained, zero=zero, guarded=guarded
                ),
            }
        )
    return {
        "rows": rows,
        "all_zero_despite_feature": all(bool(r["zero"]) for r in rows),
        "all_unprotected_and_inactive": all(
            not bool(r["guarded"]) and not bool(r["active"]) for r in rows
        ),
    }
