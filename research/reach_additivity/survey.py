"""The rectangle, and every check run over it.

The rectangle is built from the sealed readings' genesis states and every
state one valid response away from them, so that no base here was chosen to
make a result come out.

AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_CODE = str(REPO / "code")
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

from derivation.candidates import Bounds, Delta, iter_full_deltas  # noqa: E402
from derivation.engine import READINGS  # noqa: E402
from derivation.model import Regime, replay  # noqa: E402

import additivity as add  # noqa: E402

BOUNDS = Bounds(max_items=2, max_arity=2)

__all__ = [
    "BOUNDS",
    "DEPTH",
    "add",
    "additivity_survey",
    "circulation_witness",
    "rectangle",
    "self_loop_survey",
    "sequential_survey",
]


DEPTH = 2


def rectangle(depth: int = DEPTH) -> list[tuple[str, Regime]]:
    """Genesis under both sealed readings, plus every state reachable by up
    to `depth` valid one-item responses.  Deduplicated by regime equality,
    named by the route that first reached them.

    Depth is declared and is 2 rather than 1 for a reason worth recording:
    at depth 1 the rectangle carries no standing instance and no standing
    rule, because the sealed genesis states declare no form and the one-item
    enumerator offers an instance only over a form that already exists.  A
    depth-1 rectangle therefore answers the self-loop question vacuously,
    and a vacuous answer is exactly what `FW-VACUOUS` refuses to report as a
    finding."""

    seen: dict[Regime, str] = {}
    out: list[tuple[str, Regime]] = []
    for reading in READINGS:
        root = replay(reading.genesis)
        if root not in seen:
            name = f"{reading.name}0"
            seen[root] = name
            out.append((name, root))
    frontier = list(out)
    for _ in range(depth):
        nxt: list[tuple[str, Regime]] = []
        for base_name, base in frontier:
            index = 0
            for delta in iter_full_deltas(base, 1, BOUNDS):
                after = add.act(base, delta)
                if after is None or after in seen:
                    continue
                name = f"{base_name}.{index}"
                index += 1
                seen[after] = name
                out.append((name, after))
                nxt.append((name, after))
        frontier = nxt
    return out


def sequential_survey() -> dict[str, object]:
    """Every (base, d, e) over the rectangle: does the composite equal the
    stepwise application, and do the event tuples agree?"""

    triples = 0
    both_defined = 0
    states_agree = 0
    events_agree = 0
    disagreements: list[str] = []
    composite_defined_only = 0
    stepwise_defined_only = 0
    e_ill_formed_alone = 0
    for base_name, base in rectangle():
        for cost in (1, 2):
            for d in iter_full_deltas(base, cost, BOUNDS):
                middle = add.act(base, d)
                if middle is None:
                    continue
                for e in iter_full_deltas(middle, 1, BOUNDS):
                    triples += 1
                    check = add.sequential_check(base, d, e)
                    if check.composite_defined and check.stepwise_defined:
                        both_defined += 1
                        if check.states_agree:
                            states_agree += 1
                        else:
                            disagreements.append(f"{base_name} {d!r} ; {e!r}")
                    elif check.composite_defined:
                        composite_defined_only += 1
                        disagreements.append(f"composite-only {base_name}")
                    elif check.stepwise_defined:
                        stepwise_defined_only += 1
                        disagreements.append(f"stepwise-only {base_name}")
                    if check.events_agree:
                        events_agree += 1
                    if not check.e_alone_defined:
                        e_ill_formed_alone += 1
    return {
        "triples": triples,
        "both_sides_defined": both_defined,
        "states_agree": states_agree,
        "event_tuples_agree": events_agree,
        "composite_defined_but_not_stepwise": composite_defined_only,
        "stepwise_defined_but_not_composite": stepwise_defined_only,
        "second_response_ill_formed_at_the_original_base": e_ill_formed_alone,
        "disagreements": disagreements[:20],
    }


def additivity_survey() -> dict[str, object]:
    """The same triples, priced under three state functionals and under the
    sealed item count."""

    rows: dict[str, dict[str, int]] = {
        name: {"checked": 0, "additive": 0, "not_additive": 0}
        for name in add.FUNCTIONALS
    }
    count_rows = {"checked": 0, "additive": 0, "not_additive": 0}
    min_step_cost: dict[str, int | None] = {
        name: None for name in add.FUNCTIONALS
    }
    for _, base in rectangle():
        for cost in (1, 2):
            for d in iter_full_deltas(base, cost, BOUNDS):
                middle = add.act(base, d)
                if middle is None:
                    continue
                for e in iter_full_deltas(middle, 1, BOUNDS):
                    for name, functional in add.FUNCTIONALS.items():
                        verdict = add.additivity_check(functional, base, d, e)
                        if verdict is None:
                            continue
                        rows[name]["checked"] += 1
                        rows[name]["additive" if verdict else "not_additive"] += 1
                        step = add.diff_cost(functional, base, d)
                        current = min_step_cost[name]
                        if step is not None and (current is None or step < current):
                            min_step_cost[name] = step
                    whole = add.mu1(add.compose(d, e))
                    count_rows["checked"] += 1
                    if whole == add.mu1(d) + add.mu1(e):
                        count_rows["additive"] += 1
                    else:
                        count_rows["not_additive"] += 1
    assert all(value is not None for value in min_step_cost.values())
    observed_minima = {
        name: value for name, value in min_step_cost.items() if value is not None
    }
    return {
        "by_functional": rows,
        "item_count": count_rows,
        "least_step_cost_seen": observed_minima,
    }


def self_loop_survey() -> dict[str, object]:
    """Where a closed walk of length one exists, and of which item kind."""

    enumerated: dict[str, int] = {}
    constructed: dict[str, int] = {}
    bases_with_a_loop = 0
    example: str | None = None
    for base_name, base in rectangle():
        loops = add.self_loops(base, BOUNDS)
        if loops:
            bases_with_a_loop += 1
            if example is None:
                example = f"{base_name}: {loops[0][1]!r}"
        for kind, _ in loops:
            enumerated[kind] = enumerated.get(kind, 0) + 1
        for kind, _ in add.constructed_self_loops(base):
            constructed[kind] = constructed.get(kind, 0) + 1
    return {
        "bases": len(rectangle()),
        "bases_carrying_a_self_loop": bases_with_a_loop,
        "enumerated_self_loops_by_kind": dict(sorted(enumerated.items())),
        "constructed_self_loops_by_kind": dict(sorted(constructed.items())),
        "example": example,
    }


def circulation_witness() -> dict[str, object]:
    """Two paths with the same endpoints, priced two ways.

    The second path is the first with a self-loop appended, so the endpoints
    are equal by construction and the only question is what each cost says
    about the pair."""

    for base_name, base in rectangle():
        loops = add.self_loops(base, BOUNDS)
        if not loops:
            continue
        loop = loops[0][1]
        for delta in iter_full_deltas(base, 1, BOUNDS):
            after = add.act(base, delta)
            if after is None or after == base:
                continue
            short: list[Delta] = [delta]
            long: list[Delta] = [loop, delta]
            if add.path_end(base, short) != add.path_end(base, long):
                continue
            costs = {
                name: [
                    add.path_total_diff(f, base, short),
                    add.path_total_diff(f, base, long),
                ]
                for name, f in add.FUNCTIONALS.items()
            }
            return {
                "base": base_name,
                "short_path": [repr(m) for m in short],
                "long_path": [repr(m) for m in long],
                "endpoints_equal": True,
                "difference_cost_totals": costs,
                "item_count_totals": [
                    add.path_total_items(short),
                    add.path_total_items(long),
                ],
                "every_difference_cost_agrees": all(
                    pair[0] == pair[1] for pair in costs.values()
                ),
                "item_count_differs": (
                    add.path_total_items(short) != add.path_total_items(long)
                ),
            }
    return {"found": False}
