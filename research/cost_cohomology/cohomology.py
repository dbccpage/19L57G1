"""Cellular 1-cohomology and 2-complex homology of additive costs on the move graph.

Computes the 1-cohomology group of additive costs modulo exact costs on the
depth-3 move graph (|V|=262, |E|=638), exhibits pure commuting squares
spanning the non-self cycle space, computes H_1(X; R), and exhibits native
cost cocycles detecting commitment growth.

AuthorityEffect: None.
"""

from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_CODE = str(REPO / "code")
_PDC = str(REPO / "research" / "path_dependent_cost")
for _p in (_CODE, _PDC):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from derivation.candidates import (  # noqa: E402
    Item,
    NewDatum,
    NewForm,
    NewInst,
    NewRuleAll,
    apply_delta,
)
from derivation.model import Regime  # noqa: E402
import costs as ct  # noqa: E402
import exactness as ex  # noqa: E402
import movegraph as mg  # noqa: E402

__all__ = [
    "CohomologyReport",
    "CommutingSquare",
    "compute_cohomology",
    "extract_pure_squares",
    "native_candidate_matrix",
]


@dataclass(frozen=True)
class CommutingSquare:
    index: int
    start: int
    end: int
    route_left: tuple[int, int]
    route_right: tuple[int, int]
    is_pure: bool
    left_items: tuple[str, str]
    right_items: tuple[str, str]


@dataclass(frozen=True)
class CohomologyReport:
    # 1-skeleton dimensions
    n_vertices: int
    n_edges: int
    n_components: int
    dim_c1: int
    dim_b1: int
    dim_z1: int
    dim_h1_quotient: int
    dim_waste_subspace: int
    dim_order_subspace: int

    # 2-complex dimensions
    n_all_squares: int
    n_pure_squares: int
    rank_pure_squares: int
    pure_squares_span_order_space: bool
    rank_d2_all_squares: int
    dim_h1_2complex: int

    # Native candidates evaluation
    candidate_pure_discrepancies: dict[str, int]
    rank_native_order_cocycles: int
    rule_span_witness: dict[str, object]


def extract_pure_squares(
    graph: mg.MoveGraph, squares: list[tuple[int, tuple[int, int], tuple[int, int]]]
) -> list[CommutingSquare]:
    """Extract and classify all commuting squares into pure vs impure."""
    out: list[CommutingSquare] = []
    for idx, (start, left, right) in enumerate(squares):
        e_l0 = graph.edges[left[0]]
        e_l1 = graph.edges[left[1]]
        e_r0 = graph.edges[right[0]]
        e_r1 = graph.edges[right[1]]

        is_pure = (
            e_l0.source != e_l0.target
            and e_l1.source != e_l1.target
            and e_r0.source != e_r0.target
            and e_r1.source != e_r1.target
        )

        out.append(
            CommutingSquare(
                index=idx,
                start=start,
                end=e_l1.target,
                route_left=left,
                route_right=right,
                is_pure=is_pure,
                left_items=(mg.item_kind(e_l0.item), mg.item_kind(e_l1.item)),
                right_items=(mg.item_kind(e_r0.item), mg.item_kind(e_r1.item)),
            )
        )
    return out


def compute_cohomology(graph: mg.MoveGraph | None = None) -> CohomologyReport:
    """Compute the full cohomology and cellular homology report on the move graph."""
    if graph is None:
        graph = mg.build()

    n_v = len(graph.states)
    n_e = len(graph.edges)
    n_c = graph.components

    dim_c1 = n_e
    dim_b1 = n_v - n_c
    dim_z1 = graph.rank
    dim_h1_quotient = dim_c1 - dim_b1
    assert dim_h1_quotient == dim_z1

    dim_waste = len(graph.self_loop_edges)
    dim_order = len(graph.nonself_cycles)
    assert dim_waste + dim_order == dim_z1

    # Commuting squares
    raw_squares = ex.commuting_squares(graph)
    squares = extract_pure_squares(graph, raw_squares)
    pure_squares = [s for s in squares if s.is_pure]

    # Boundary matrix of pure squares in C_1
    M_pure = np.zeros((len(pure_squares), n_e), dtype=np.float64)
    for i, sq in enumerate(pure_squares):
        M_pure[i, sq.route_left[0]] += 1.0
        M_pure[i, sq.route_left[1]] += 1.0
        M_pure[i, sq.route_right[0]] -= 1.0
        M_pure[i, sq.route_right[1]] -= 1.0

    rank_pure = int(np.linalg.matrix_rank(M_pure))

    # Boundary matrix of all 770 squares (d_2 operator)
    M_all = np.zeros((len(squares), n_e), dtype=np.float64)
    for i, sq in enumerate(squares):
        M_all[i, sq.route_left[0]] += 1.0
        M_all[i, sq.route_left[1]] += 1.0
        M_all[i, sq.route_right[0]] -= 1.0
        M_all[i, sq.route_right[1]] -= 1.0

    rank_d2 = int(np.linalg.matrix_rank(M_all))
    dim_h1_2complex = dim_z1 - rank_d2

    # Native candidates evaluation on pure squares
    cand_names = sorted(ct.CANDIDATES)
    discrepancies: dict[str, int] = {}
    for name in cand_names:
        w = ex.edge_weights(graph, name)
        disc = sum(
            1
            for sq in pure_squares
            if w[sq.route_left[0]] + w[sq.route_left[1]]
            != w[sq.route_right[0]] + w[sq.route_right[1]]
        )
        discrepancies[name] = disc

    # Matrix of 4 order candidates on pure squares
    order_cands = [
        "width_at_admission",
        "rule_span",
        "empty_admission",
        "mention_deficit",
    ]
    C_order = np.zeros((len(order_cands), len(pure_squares)), dtype=np.float64)
    for i, name in enumerate(order_cands):
        w = ex.edge_weights(graph, name)
        for j, sq in enumerate(pure_squares):
            C_order[i, j] = (w[sq.route_left[0]] + w[sq.route_left[1]]) - (
                w[sq.route_right[0]] + w[sq.route_right[1]]
            )
    rank_order_cocycles = int(np.linalg.matrix_rank(C_order))

    # rule_span witness
    witness = ex.square_witness(graph, "rule_span")
    assert witness is not None

    return CohomologyReport(
        n_vertices=n_v,
        n_edges=n_e,
        n_components=n_c,
        dim_c1=dim_c1,
        dim_b1=dim_b1,
        dim_z1=dim_z1,
        dim_h1_quotient=dim_h1_quotient,
        dim_waste_subspace=dim_waste,
        dim_order_subspace=dim_order,
        n_all_squares=len(squares),
        n_pure_squares=len(pure_squares),
        rank_pure_squares=rank_pure,
        pure_squares_span_order_space=(rank_pure == dim_order),
        rank_d2_all_squares=rank_d2,
        dim_h1_2complex=dim_h1_2complex,
        candidate_pure_discrepancies=discrepancies,
        rank_native_order_cocycles=rank_order_cocycles,
        rule_span_witness=witness,
    )


def native_candidate_matrix(
    graph: mg.MoveGraph, candidates: Sequence[str]
) -> np.ndarray:
    """Compute the circulation matrix of candidates on pure commuting squares."""
    squares = extract_pure_squares(graph, ex.commuting_squares(graph))
    pure = [s for s in squares if s.is_pure]
    mat = np.zeros((len(candidates), len(pure)), dtype=np.int64)
    for i, name in enumerate(candidates):
        w = ex.edge_weights(graph, name)
        for j, sq in enumerate(pure):
            mat[i, j] = (w[sq.route_left[0]] + w[sq.route_left[1]]) - (
                w[sq.route_right[0]] + w[sq.route_right[1]]
            )
    return mat
