"""Write the deterministic receipt for the path_dependent_cost run.

No timestamps, no environment data, sorted keys: the file must regenerate
byte-identically.  AuthorityEffect: None.
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import costs as ct  # noqa: E402
import exactness as ex  # noqa: E402
import movegraph as mg  # noqa: E402

RECEIPT = HERE / "receipts" / "path_dependent_cost.json"


def depth_table() -> list[dict[str, object]]:
    """The graph at each depth, so the declared depth is visibly a choice
    and the shallower ones are visibly vacuous."""

    rows: list[dict[str, object]] = []
    for depth in range(1, mg.DEPTH + 1):
        graph = mg.build(depth)
        rows.append({
            "depth": depth,
            "states": len(graph.states),
            "moves": len(graph.edges),
            "components": graph.components,
            "cycle_rank": graph.rank,
            "self_loop_cycles": sum(1 for c in graph.cycles if c.is_self_loop),
            "nonself_cycles": len(graph.nonself_cycles),
            "moves_leaving_the_rectangle": mg.boundary_moves(depth),
        })
    return rows


def candidate_table(graph: mg.MoveGraph) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for name in sorted(ct.CANDIDATES):
        verdict = ex.decide(graph, name)
        rows.append({
            "name": name,
            "reading": ct.READINGS[name],
            "reads_the_base": verdict.reads_the_base,
            "exact": verdict.exact_by_potentials,
            "methods_agree": verdict.methods_agree,
            "nonzero_on_self_loops": verdict.nonzero_self_loop_cycles,
            "nonzero_on_nonself_cycles": verdict.nonzero_nonself_cycles,
            "first_inconsistent_move": verdict.witness,
            "square_witness": ex.square_witness(graph, name),
        })
    return rows


def quadrants(rows: list[dict[str, object]]) -> dict[str, list[str]]:
    """The two properties are independent axes, and this says which cells
    the candidates actually occupy rather than asserting they all do."""

    cells: dict[str, list[str]] = {
        "base_free_and_exact": [],
        "base_free_and_not_exact": [],
        "base_relative_and_exact": [],
        "base_relative_and_not_exact": [],
    }
    for row in rows:
        base = "base_relative" if row["reads_the_base"] else "base_free"
        kind = "exact" if row["exact"] else "not_exact"
        cells[f"{base}_and_{kind}"].append(str(row["name"]))
    return cells


def build() -> dict[str, object]:
    graph = mg.build()
    rows = candidate_table(graph)
    nonself_only = [
        r["name"] for r in rows
        if not r["exact"] and r["nonzero_on_self_loops"] == 0
    ]
    self_loop_only = [
        r["name"] for r in rows
        if not r["exact"] and r["nonzero_on_nonself_cycles"] == 0
    ]
    return {
        "authority_effect": "None",
        "write_root": "research/path_dependent_cost/",
        "snapshot": "7fcd72f6",
        "declared": {
            "node": "a state reachable from a sealed reading's genesis by one-item moves",
            "edge": "exactly what iter_cost1_items offers at that state; no move is invented",
            "depth": mg.DEPTH,
            "cost": "a weighting of single moves, extended by summation -- which is every additive cost, by the characterisation in lean/PathDependentCost/Cochain.lean",
            "exact": "some state functional P has the cost as its difference",
        },
        "graph_by_depth": depth_table(),
        "commuting_squares": len(ex.commuting_squares(graph)),
        "candidates": rows,
        "quadrants": quadrants(rows),
        "nonexact_through_nonself_cycles_only": sorted(str(n) for n in nonself_only),
        "nonexact_through_self_loops_only": sorted(str(n) for n in self_loop_only),
        "assumptions": {
            "A1": (
                "the rectangle is reachability-bounded at the declared depth; every"
                " count is a count over it, and the number of moves leaving it is"
                " reported at each depth rather than hidden"
            ),
            "A2": (
                "the cycle rank is the rank of this finite graph and of nothing"
                " larger; FW-CLASS forbids reading it as the rank of the estate"
            ),
            "A3": (
                "every candidate was declared with its reading before its"
                " circulation was computed, and the ones that turned out exact are"
                " reported as exact rather than dropped"
            ),
            "A4": (
                "exactness is decided twice, by potentials and by circulations,"
                " and the two must agree on every candidate; agreement is recorded"
                " per candidate rather than assumed"
            ),
            "A5": (
                "a cost that is nonzero only on moves that change nothing is"
                " reported as pricing waste, not as pricing order"
            ),
        },
    }


def main() -> int:
    data = build()
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        "utf-8",
        newline="\n",
    )
    rows = data["graph_by_depth"]
    assert isinstance(rows, list)
    last = rows[-1]
    print(
        f"graph at depth {last['depth']}: {last['states']} states,"
        f" {last['moves']} moves, rank {last['cycle_rank']}"
        f" = {last['self_loop_cycles']} self-loop + {last['nonself_cycles']} non-self"
    )
    print(f"nonexact through non-self cycles only: {data['nonexact_through_nonself_cycles_only']}")
    print(f"nonexact through self-loops only: {data['nonexact_through_self_loops_only']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
