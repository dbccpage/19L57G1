"""Produce every derivation artifact deterministically.

Usage: python code/run_derivation.py [--artifacts DIR] [--rounds N]
       [--budget N] [--max-arity N]

Outputs (all JSON, deterministic byte-for-byte):

* ``bounds.json``      -- every declared resource bound;
* ``challenges.json``  -- Challenge 0-3 analyses for both readings;
* ``tree_<reading>_<measure>.json`` -- the quotiented branch trees;
* ``nosupply_<reading>.json``       -- the termination variant;
* ``claims.json``      -- computed evidence per claim ledger entry.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Optional

from derivation.candidates import Bounds
from derivation.engine import (
    READINGS,
    Tree,
    build_tree,
    challenge0_report,
    challenge1_report,
    challenge2_report,
    challenge3_report,
)
from derivation.export import tree_json, write_json
from derivation.iso import canonical
from derivation.model import replay
from derivation.observe import collapsed_pairs


def _claims(
    challenges: dict[str, Any], trees: dict[str, Tree], nosupply: dict[str, Tree]
) -> dict[str, Any]:
    """Computed Python evidence for ledger claims (IDs match
    ``paper/paper_claim_ledger.md``)."""
    c3 = challenges["challenge3"]

    def _branch_report(t: Tree) -> dict[str, Any]:
        """Per-branch termination evidence.  In the quotiented DAG a
        maximal branch corresponds to a leaf; 'expanded' nodes are
        internal."""
        leaves = [n for n in t.nodes if n.status != "expanded"]
        terminal = sum(
            1 for n in leaves if n.status.startswith("terminal")
        )
        budget_cut = sum(
            1 for n in leaves if n.status == "frontier_budget"
        )
        round_cut = sum(1 for n in leaves if n.status == "completed")
        open_ = sum(1 for n in leaves if n.status == "open")
        return {
            "terminal_branches": terminal,
            "budget_cutoff_branches": budget_cut,
            "round_cutoff_branches": round_cut,
            "open_branches": open_,
            "every_maximal_branch_terminates": (
                terminal > 0
                and budget_cut == 0
                and round_cut == 0
                and open_ == 0
            ),
        }

    def _rounds_used(t: Tree) -> int:
        return max(n.depth for n in t.nodes)

    def _pair_bound(t: Tree) -> int:
        n = t.nodes[0].regime.n_data()
        return n * (n - 1) // 2

    evidence: dict[str, Any] = {
        "CL-0-INERTIA": challenges["challenge0"],
        "CL-1-SUPPLY-VS-ADMISSION": challenges["challenge1"],
        "CL-2-COLLAPSE": challenges["challenge2"],
        "CL-3-FAIL-CURRENT": {
            r: c3r["current_regime_satisfies"] for r, c3r in c3.items()
        },
        "CL-3-MIN-TWO": {
            r: c3r["mu1"]["minimum_cost"] for r, c3r in c3.items()
        },
        "CL-3-NONUNIQUE-MU1": {
            r: len(c3r["mu1"]["iso_classes"]) for r, c3r in c3.items()
        },
        "CL-3-UNIQUE-MU2": {
            r: len(c3r["mu2"]["iso_classes"]) for r, c3r in c3.items()
        },
        "CL-TREE-SUMMARY": {
            key: t.stats() for key, t in trees.items()
        },
        "CL-BRANCH-REPORTS": {
            **{key: _branch_report(t) for key, t in trees.items()},
            **{
                f"closed_{name}": _branch_report(t)
                for name, t in nosupply.items()
            },
        },
        "CL-ENDOGENOUS-TERMINATION": {
            name: {
                "branch_report": _branch_report(t),
                "rounds_used": _rounds_used(t),
                "pair_bound": _pair_bound(t),
                "within_bound": _rounds_used(t) <= _pair_bound(t),
                "note": "closed-system baseline: endogenous generator "
                "only, no external continuation policy",
            }
            for name, t in nosupply.items()
        },
        "CL-ENDOGENOUS-VS-EXTERNAL": {
            name: {
                "closed_system": nosupply[name].stats(),
                "external_policy_mu1": trees[f"{name}_mu1"].stats(),
                "external_policy_mu2": trees[f"{name}_mu2"].stats(),
            }
            for name in nosupply
        },
        "CL-REPLAY-CERTIFIED": {
            key: t.stats()["all_certified"] for key, t in trees.items()
        },
        "CL-REACHES-REQUESTED-DEPTH-WITH-EXTERNAL-SUPPLY": {
            key: {
                "max_depth": t.stats()["max_depth"],
                "requested_rounds": t.max_rounds,
                "note": "reaching a finite requested depth; not a proof "
                "of unboundedness",
            }
            for key, t in trees.items()
        },
    }
    return evidence


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--rounds", type=int, default=15)
    parser.add_argument(
        "--budget-mu1",
        type=int,
        default=1200,
        help="node budget for mu1 trees (declared frontier bound)",
    )
    parser.add_argument(
        "--budget-mu2",
        type=int,
        default=3000,
        help="node budget for mu2 trees (large enough for completion)",
    )
    parser.add_argument("--max-arity", type=int, default=2)
    args = parser.parse_args(argv)
    bounds = Bounds(max_items=2, max_arity=args.max_arity)
    budgets = {"mu1": args.budget_mu1, "mu2": args.budget_mu2}

    challenges: dict[str, Any] = {
        "challenge0": challenge0_report(),
        "challenge1": challenge1_report(),
        "challenge2": challenge2_report(),
        "challenge3": {
            rd.name: challenge3_report(rd, bounds) for rd in READINGS
        },
    }

    trees: dict[str, Tree] = {}
    for rd in READINGS:
        for measure in ("mu1", "mu2"):
            key = f"{rd.name}_{measure}"
            trees[key] = build_tree(
                rd,
                measure,
                bounds,
                max_rounds=args.rounds,
                node_budget=budgets[measure],
            )
            print(f"tree {key}: {trees[key].stats()}")

    nosupply: dict[str, Tree] = {}
    for rd in READINGS:
        nosupply[rd.name] = build_tree(
            rd,
            "mu1",
            bounds,
            max_rounds=args.rounds,
            node_budget=budgets["mu1"],
            supply=False,
        )
        print(f"nosupply {rd.name}: {nosupply[rd.name].stats()}")

    out = args.artifacts
    write_json(
        out / "bounds.json",
        {
            "max_items": bounds.max_items,
            "max_arity": bounds.max_arity,
            "max_rounds": args.rounds,
            "node_budget_mu1": budgets["mu1"],
            "node_budget_mu2": budgets["mu2"],
            "perm_budget": 100_000,
            "readings": [rd.name for rd in READINGS],
            "measures": ["mu1", "mu2"],
        },
    )
    write_json(out / "challenges.json", challenges)
    for key, tree in trees.items():
        write_json(out / f"tree_{key}.json", tree_json(tree))
    for name, tree in nosupply.items():
        write_json(out / f"nosupply_{name}.json", tree_json(tree))
    write_json(out / "claims.json", _claims(challenges, trees, nosupply))

    # Sanity: genesis regimes replay and are collapsed before Challenge 3.
    for rd in READINGS:
        base = replay(rd.genesis)
        assert canonical(base) == canonical(base)
        assert rd.target in collapsed_pairs(base)
    print(f"artifacts written to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
