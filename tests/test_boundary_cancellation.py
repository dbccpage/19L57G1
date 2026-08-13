"""Tests for the general boundary-cancellation mirror.

Mirrors ``lean4/Derivation/BoundaryCancellation.lean``: the exhaustive
cancellation check over the declared bounds, the deletion-order
involution, the identity between collected coefficient and rectangle
double sum, the distinctness statements that strict ascent buys, the
renaming scope, and both required countermodels — including the
negative tests that keep the report honest (the signless composite is
nonzero; the ill-formed cell breaks distinctness but NOT the
cancellation).
"""

from __future__ import annotations

from pathlib import Path

import run_boundary_cancellation
from derivation.boundary_cancellation import (
    MAX_DIM,
    MAX_VERTICES,
    MIN_DIM,
    PSEUDO_CELL,
    SGN_RANGE,
    SIGNLESS_CELLS,
    WELL_FORMED_CELL,
    asc,
    ascending_cells,
    bd_n,
    bd_no_sign,
    cancellation_report,
    cell_cancels,
    cell_pairs_cancel,
    cell_rect_identity,
    codim2_distinct,
    codim2_faces,
    coeff_n,
    control_tau,
    dterm,
    erase_idx,
    erase_inj,
    erase_swap,
    facets,
    illformed_countermodel,
    involution_report,
    monotone_rename,
    pairs_cancel,
    perfect_matching,
    push_n,
    push_no_sign,
    rect_sum,
    rectangle,
    rename,
    renaming_report,
    sgn,
    sgn_cancel,
    signless_countermodel,
    slot_multiplicity,
    support,
    swap01,
    swap_pair,
)


def test_declared_calculus_mirrors_lean() -> None:
    # eraseIdx, including the out-of-range identity case
    assert erase_idx((0, 1, 2), 1) == (0, 2)
    assert erase_idx((0, 1, 2), 3) == (0, 1, 2)
    assert erase_idx((), 0) == ()
    # the declared alternating sign
    assert sgn(0) == 1
    assert sgn(1) == -1
    assert all(sgn(c + 1) == -sgn(c) for c in range(SGN_RANGE))
    # ascent, facets, boundary, pushforward, coefficients
    assert asc((0, 2, 5))
    assert not asc((0, 0, 1))
    assert facets((0, 1, 2)) == [(1, 2), (0, 2), (0, 1)]
    assert bd_n((0, 1, 2)) == [(1, (1, 2)), (-1, (0, 2)), (1, (0, 1))]
    assert bd_no_sign((0, 1, 2)) == [
        (1, (1, 2)), (1, (0, 2)), (1, (0, 1))]
    assert len(push_n(bd_n((0, 1, 2)))) == 6
    assert len(push_no_sign(bd_no_sign((0, 1, 2)))) == 6
    assert coeff_n((1,), bd_n((0, 1))) == 1
    assert coeff_n((0,), bd_n((0, 1))) == -1
    assert coeff_n((9,), bd_n((0, 1))) == 0
    # the signed contribution of an ordered deletion pair
    assert dterm((0, 1, 2), (0,), 0, 0) == 0        # face is (2,)
    assert dterm((0, 1, 2), (2,), 0, 0) == 1
    assert dterm((0, 1, 2), (0,), 1, 1) == -1 * -1
    # the control presentation, on a nonempty and on an empty cell
    assert control_tau((0, 1, 2)) == (3,)
    assert control_tau(()) == (0,)
    assert support(bd_n((0, 1, 2))) == [(0, 1), (0, 2), (1, 2)]


def test_involution_is_the_pairing() -> None:
    # both branches of the involution
    assert swap_pair(2, 0) == (0, 1)
    assert swap_pair(0, 2) == (3, 0)
    for n in range(2, 8):
        rep = involution_report(n)
        assert rep["rectangle_size"] == n * (n - 1)
        assert rep["maps_into_rectangle"] is True
        assert rep["is_involution"] is True
        assert rep["fixed_point_free"] is True
        assert rep["is_bijection"] is True
        assert rep["sign_reversing"] is True
    assert rectangle(3) == [(0, 0), (0, 1), (1, 0), (1, 1),
                            (2, 0), (2, 1)]
    # the two identities the pairing rests on
    for b in range(1, 9):
        for a in range(b):
            assert sgn_cancel(a, b)
            assert erase_swap((0, 1, 2, 3, 4, 5, 6, 7, 8), a, b)


def test_exhaustive_cancellation_over_declared_bounds() -> None:
    rep = cancellation_report()
    bounds = rep["bounds"]
    assert isinstance(bounds, dict)
    assert bounds["max_vertices"] == MAX_VERTICES
    assert bounds["min_dim"] == MIN_DIM
    assert bounds["max_dim"] == MAX_DIM
    assert bounds["cells_checked"] == 218
    assert rep["all_cancel"] is True
    assert rep["all_distinct"] is True
    assert rep["sgn_alternates"] is True
    assert rep["sgn_cancel_pairs"] is True
    per_dim = rep["per_dim"]
    assert isinstance(per_dim, dict)
    assert sorted(per_dim) == ["2", "3", "4", "5", "6"]
    for dim in range(MIN_DIM, MAX_DIM + 1):
        entry = per_dim[str(dim)]
        assert isinstance(entry, dict)
        assert entry["vertices_per_cell"] == dim + 1
        assert entry["all_ascending"] is True
        assert entry["all_cancel"] is True
        assert entry["all_rect_identity"] is True
        assert entry["all_pairs_cancel"] is True
        assert entry["all_swap_identity"] is True
        assert entry["all_erase_injective"] is True
        assert entry["all_codim2_distinct"] is True
        assert entry["all_perfect_matching"] is True
    # a smaller bound is a genuine sub-check, not a different claim
    small = cancellation_report(4, 2, 2)
    small_bounds = small["bounds"]
    assert isinstance(small_bounds, dict)
    assert small_bounds["cells_checked"] == 4
    assert small["all_cancel"] is True


def test_per_cell_statements() -> None:
    sigma = (0, 1, 2, 3)
    ch = push_n(bd_n(sigma))
    # the coefficient IS the rectangle double sum, and it is zero
    for tau in support(ch) + [control_tau(sigma)]:
        assert coeff_n(tau, ch) == rect_sum(sigma, tau)
        assert coeff_n(tau, ch) == 0
        assert pairs_cancel(sigma, tau)
    assert cell_cancels(sigma)
    assert cell_rect_identity(sigma)
    assert cell_pairs_cancel(sigma)
    # the vanishing needs no well-formedness at all
    assert cell_cancels(PSEUDO_CELL)
    assert cell_cancels((5, 5, 5, 5))
    assert cell_cancels((3, 1, 2))
    assert ascending_cells(4, 2) == [
        (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]


def test_distinctness_is_what_ascent_buys() -> None:
    good = WELL_FORMED_CELL
    assert erase_inj(good)
    assert codim2_distinct(good)
    assert perfect_matching(good)
    assert codim2_faces(good) == [(0,), (1,), (2,)]
    assert slot_multiplicity(good, (0,)) == 2
    # ... and all three fail on the repeated-vertex pseudo-cell
    assert not erase_inj(PSEUDO_CELL)
    assert not codim2_distinct(PSEUDO_CELL)
    assert not perfect_matching(PSEUDO_CELL)
    assert slot_multiplicity(PSEUDO_CELL, (0,)) == 4
    # The four terms are two deletion orders for each of TWO distinct
    # unordered position pairs that collapse to the same presented face.
    # This prevents the false unrestricted gloss "each face has two".
    pseudo_pairs_for_zero = [
        (a, b) for b in range(len(PSEUDO_CELL)) for a in range(b)
        if erase_idx(erase_idx(PSEUDO_CELL, b), a) == (0,)]
    assert len(pseudo_pairs_for_zero) == 2


def test_renaming_scope() -> None:
    rep = renaming_report(6, 2, 3)
    assert rep["monotone_preserves_ascent"] is True
    assert rep["monotone_preserves_length"] is True
    assert rep["faces_transport"] is True
    assert rep["monotone_cancels"] is True
    assert rep["monotone_keeps_distinctness"] is True
    # exact scope: an injective non-monotone renaming can break ascent,
    # and the vanishing survives regardless
    assert rep["non_monotone_breaks_ascent"] is True
    assert rep["non_monotone_still_cancels"] is True
    assert rename((0, 1, 2), monotone_rename) == (3, 5, 7)
    assert rename((0, 1, 2), swap01) == (1, 0, 2)
    assert swap01(0) == 1
    assert swap01(1) == 0
    assert swap01(7) == 7
    assert not asc(rename((0, 1), swap01))
    assert cell_cancels(rename((0, 1, 2), swap01))


def test_signless_countermodel() -> None:
    rep = signless_countermodel()
    assert rep["all_signless_nonzero"] is True
    assert rep["all_signed_zero"] is True
    cells = rep["cells"]
    assert isinstance(cells, dict)
    assert sorted(cells) == sorted(str(list(s)) for s in SIGNLESS_CELLS)
    tri = cells["[0, 1, 2]"]
    assert isinstance(tri, dict)
    assert tri["ascending"] is True
    assert tri["signless_coefficients"] == [
        [[0], 2], [[1], 2], [[2], 2]]
    assert tri["signless_nonzero_somewhere"] is True
    assert tri["signed_zero_everywhere"] is True
    # the direct exhibit: signless coefficient 2, signed coefficient 0
    signless = push_no_sign(bd_no_sign((0, 1, 2)))
    assert coeff_n((0,), signless) == 2
    assert coeff_n((0,), push_n(bd_n((0, 1, 2)))) == 0


def test_illformed_countermodel_states_exactly_what_fails() -> None:
    rep = illformed_countermodel()
    assert rep["ascending"] is False
    assert rep["two_positions_one_facet"] is True
    # what fails: distinctness
    assert rep["erase_injective"] is False
    assert rep["codim2_distinct"] is False
    assert rep["perfect_matching"] is False
    assert rep["slot_multiplicity_pseudo"] == 4
    assert rep["slot_multiplicity_well_formed"] == 2
    # the boundary chain is degenerate: a facet with coefficient zero
    assert rep["boundary_forgets_a_facet"] is True
    assert (0, 1) in facets(PSEUDO_CELL)
    assert coeff_n((0, 1), bd_n(PSEUDO_CELL)) == 0
    # what does NOT fail: the coefficientwise composite still vanishes
    assert rep["composite_still_vanishes"] is True


def test_runner_byte_stable(tmp_path: Path) -> None:
    d1 = tmp_path / "a"
    d2 = tmp_path / "b"
    argv = ["--max-vertices", "5", "--min-dim", "2", "--max-dim", "3"]
    assert run_boundary_cancellation.main(
        ["--artifacts", str(d1)] + argv) == 0
    assert run_boundary_cancellation.main(
        ["--artifacts", str(d2)] + argv) == 0
    assert (d1 / "boundary_cancellation.json").read_bytes() == \
        (d2 / "boundary_cancellation.json").read_bytes()


def test_runner_default_bounds(tmp_path: Path) -> None:
    out = tmp_path / "full"
    assert run_boundary_cancellation.main(["--artifacts", str(out)]) == 0
    assert (out / "boundary_cancellation.json").exists()
