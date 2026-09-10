"""Runner for cost cohomology computation and receipt emission.

AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.dont_write_bytecode = True

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_CODE = str(REPO / "code")
_PDC = str(REPO / "research" / "path_dependent_cost")
for _p in (str(HERE), _CODE, _PDC):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from cohomology import compute_cohomology  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute cost cohomology receipts.")
    parser.add_argument("--out", default=str(HERE / "receipts"))
    args = parser.parse_args()

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Computing cost cohomology and 2-complex cellular homology...")
    rep = compute_cohomology()

    data = {
        "move_graph": {
            "vertices": rep.n_vertices,
            "edges": rep.n_edges,
            "components": rep.n_components,
            "dim_C1": rep.dim_c1,
            "dim_B1_exact": rep.dim_b1,
            "dim_Z1_cycles": rep.dim_z1,
            "dim_H1_quotient": rep.dim_h1_quotient,
            "waste_subspace_dim": rep.dim_waste_subspace,
            "order_subspace_dim": rep.dim_order_subspace,
            "quotient_decomposition": f"R^{rep.dim_h1_quotient} = R^{rep.dim_waste_subspace}_waste + R^{rep.dim_order_subspace}_order",
        },
        "commuting_squares_2complex": {
            "all_commuting_squares": rep.n_all_squares,
            "pure_commuting_squares": rep.n_pure_squares,
            "rank_pure_squares": rep.rank_pure_squares,
            "pure_squares_span_order_subspace": rep.pure_squares_span_order_space,
            "rank_d2_boundary_all_squares": rep.rank_d2_all_squares,
            "dim_H1_cellular_2complex": rep.dim_h1_2complex,
            "homology_group_statement": f"H_1(X; R) = Z_1 / im(d_2) = R^{rep.dim_h1_2complex}, supported on uncancelled self-loops",
        },
        "native_candidates": {
            "pure_square_discrepancies": rep.candidate_pure_discrepancies,
            "order_cocycles_rank": rep.rank_native_order_cocycles,
            "rule_span_commitment_growth_witness": rep.rule_span_witness,
        },
    }

    out_file = out_dir / "cost_cohomology.json"
    content = json.dumps(data, indent=2, sort_keys=True) + "\n"
    out_file.write_text(content, encoding="utf-8")
    print(f"Receipts written to {out_file}")
    print(f"Summary: H^1 quotient dim = {rep.dim_h1_quotient}")
    print(f"Pure squares rank = {rep.rank_pure_squares} (spans order space: {rep.pure_squares_span_order_space})")
    print(f"H_1(X; R) dim = {rep.dim_h1_2complex}")
    print(f"Rank of 4 native order cocycles = {rep.rank_native_order_cocycles}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
