"""Deterministic mirror of ``lean4/Derivation/BoundaryCancellation.lean``.

The Lean module proves, for EVERY list ``sigma`` and EVERY ``tau``,
that the composite boundary has coefficient zero at ``tau``, by pairing
the two orders of each unordered pair of deleted positions and
cancelling their signs.  Distinct unordered pairs can land on the same
presented face when vertices repeat.  This module re-checks the same
statements EXHAUSTIVELY over declared finite bounds (all strictly
ascending cells whose vertices are drawn from the first
``MAX_VERTICES`` numerals, in
dimensions ``MIN_DIM`` through ``MAX_DIM``), and mirrors both required
countermodels.

Correspondence with the Lean module:

* ``erase_swap``               -> ``eraseIdx_swap``
* ``sgn_cancel``               -> ``sgn_cancel``
* ``swap_pair``                -> the deletion-order involution
* ``rect_sum`` / ``coeff_n``   -> ``coeff_rect``
* ``pairs_cancel``             -> ``dterm_cancel`` / ``rect_zero``
* ``cell_cancels``             -> ``d2_zero_unrestricted``
* ``erase_inj``                -> ``eraseIdx_inj_of_asc``
* ``codim2_distinct``          -> ``codim2_distinct``
* ``renaming_report``          -> ``d2_zero_renamed``
* ``signless_countermodel``    -> ``signless_countermodel``
* ``illformed_countermodel``   -> ``illformed_countermodel``

Imported (declared, not derived) inputs, unchanged from
``LadderGeneral``: the ascending-list cell encoding, integer
coefficients, and the alternating sign convention.  The filler rule
does not force the coefficients or the signs; ``signless_countermodel``
records exactly that.

Recorded honestly, matching the Lean module: strict ascent is NOT
load-bearing for the coefficientwise vanishing (the pseudo-cell
``(0, 0, 1)`` still cancels).  It IS load-bearing for the distinctness
statements, which fail for that pseudo-cell.
"""

from __future__ import annotations

from itertools import combinations
from typing import Callable

from derivation.export import Json

Cell = tuple[int, ...]
Chain = list[tuple[int, Cell]]

# ---------------------------------------------------------------------------
# Declared finite bounds of the exhaustive check.

MAX_VERTICES: int = 8
MIN_DIM: int = 2
MAX_DIM: int = 6
SGN_RANGE: int = 64


# ---------------------------------------------------------------------------
# 1. The declared calculus (mirror of LadderGeneral)

def erase_idx(sigma: Cell, i: int) -> Cell:
    """Mirror of ``List.eraseIdx``: deleting an out-of-range position
    is the identity."""
    if i >= len(sigma):
        return sigma
    return sigma[:i] + sigma[i + 1:]


def sgn(i: int) -> int:
    """The DECLARED alternating sign."""
    return 1 if i % 2 == 0 else -1


def asc(sigma: Cell) -> bool:
    """Strict ascent — excludes repeated vertices."""
    return all(a < b for a, b in zip(sigma, sigma[1:]))


def facets(sigma: Cell) -> list[Cell]:
    return [erase_idx(sigma, i) for i in range(len(sigma))]


def bd_n(sigma: Cell) -> Chain:
    return [(sgn(i), erase_idx(sigma, i)) for i in range(len(sigma))]


def push_n(ch: Chain) -> Chain:
    return [(c * d, tau) for (c, s) in ch for (d, tau) in bd_n(s)]


def coeff_n(tau: Cell, ch: Chain) -> int:
    return sum(c for (c, t) in ch if t == tau)


def bd_no_sign(sigma: Cell) -> Chain:
    """The signless boundary: same facets, every coefficient 1."""
    return [(1, erase_idx(sigma, i)) for i in range(len(sigma))]


def push_no_sign(ch: Chain) -> Chain:
    return [(c * d, tau) for (c, s) in ch for (d, tau) in bd_no_sign(s)]


def dterm(sigma: Cell, tau: Cell, i: int, j: int) -> int:
    """The signed contribution of the ordered deletion pair ``(i, j)``."""
    if erase_idx(erase_idx(sigma, i), j) == tau:
        return sgn(i) * sgn(j)
    return 0


# ---------------------------------------------------------------------------
# 2. The pairing: the involution on ordered deletion pairs

def swap_pair(i: int, j: int) -> tuple[int, int]:
    """The deletion-order involution on the index rectangle
    ``{(i, j) : i < n, j < n - 1}``: the pair naming the same
    codimension-two face by the other deletion order."""
    if j < i:
        return (j, i - 1)
    return (j + 1, i)


def rectangle(n: int) -> list[tuple[int, int]]:
    """The index set of the double sum."""
    return [(i, j) for i in range(n) for j in range(n - 1)]


def involution_report(n: int) -> dict[str, Json]:
    """The involution is a fixed-point-free, face-preserving,
    sign-reversing bijection of the index rectangle."""
    rect = rectangle(n)
    seen = set(rect)
    images = [swap_pair(i, j) for (i, j) in rect]
    return {
        "n": n,
        "rectangle_size": len(rect),
        "maps_into_rectangle": all(p in seen for p in images),
        "is_involution": all(
            swap_pair(*swap_pair(i, j)) == (i, j) for (i, j) in rect),
        "fixed_point_free": all(
            swap_pair(i, j) != (i, j) for (i, j) in rect),
        "is_bijection": sorted(images) == sorted(rect),
        "sign_reversing": all(
            sgn(i) * sgn(j)
            == -(sgn(swap_pair(i, j)[0]) * sgn(swap_pair(i, j)[1]))
            for (i, j) in rect),
    }


def erase_swap(sigma: Cell, a: int, b: int) -> bool:
    """The pairing identity: for ``a < b`` the two deletion orders give
    the same codimension-two face."""
    return (erase_idx(erase_idx(sigma, b), a)
            == erase_idx(erase_idx(sigma, a), b - 1))


def sgn_cancel(a: int, b: int) -> bool:
    """The sign cancellation for ``a < b``."""
    return sgn(b) * sgn(a) + sgn(a) * sgn(b - 1) == 0


def rect_sum(sigma: Cell, tau: Cell) -> int:
    """The double sum over ordered deletion pairs."""
    n = len(sigma)
    return sum(dterm(sigma, tau, i, j)
               for i in range(n) for j in range(n - 1))


def pairs_cancel(sigma: Cell, tau: Cell) -> bool:
    """Every unordered position pair contributes zero at ``tau``."""
    n = len(sigma)
    return all(dterm(sigma, tau, b, a) + dterm(sigma, tau, a, b - 1) == 0
               for b in range(n) for a in range(b))


def support(ch: Chain) -> list[Cell]:
    """The presentations occurring in a chain, deterministically
    ordered."""
    return sorted({t for (_, t) in ch})


def control_tau(sigma: Cell) -> Cell:
    """A presentation guaranteed absent from the composite's support:
    the vanishing must hold there too, trivially."""
    return (max(sigma) + 1,) if sigma else (0,)


def cell_cancels(sigma: Cell) -> bool:
    """The composite boundary vanishes at EVERY presentation: at every
    element of the support, at every facet, and at a control
    presentation outside the support."""
    ch = push_n(bd_n(sigma))
    taus = support(ch) + facets(sigma) + [control_tau(sigma), ()]
    return all(coeff_n(tau, ch) == 0 for tau in taus)


def cell_rect_identity(sigma: Cell) -> bool:
    """The composite's coefficient IS the rectangle double sum."""
    ch = push_n(bd_n(sigma))
    taus = support(ch) + [control_tau(sigma)]
    return all(coeff_n(tau, ch) == rect_sum(sigma, tau) for tau in taus)


def cell_pairs_cancel(sigma: Cell) -> bool:
    ch = push_n(bd_n(sigma))
    taus = support(ch) + [control_tau(sigma)]
    return all(pairs_cancel(sigma, tau) for tau in taus)


# ---------------------------------------------------------------------------
# 3. Distinctness: what strict ascent really buys

def erase_inj(sigma: Cell) -> bool:
    """Distinct positions give distinct facets.  True for ascending
    cells (``eraseIdx_inj_of_asc``); false for repeated-vertex lists."""
    n = len(sigma)
    return all(erase_idx(sigma, i) != erase_idx(sigma, j)
               for i in range(n) for j in range(i))


def codim2_distinct(sigma: Cell) -> bool:
    """Distinct unordered position pairs give distinct codimension-two
    faces, so the pairing is a perfect matching on faces."""
    n = len(sigma)
    pairs = [(a, b) for b in range(n) for a in range(b)]
    faces = [erase_idx(erase_idx(sigma, b), a) for (a, b) in pairs]
    return len(set(faces)) == len(faces)


def slot_multiplicity(sigma: Cell, tau: Cell) -> int:
    """How many ordered deletion pairs land in the coefficient slot of
    ``tau``.  Exactly two for a codimension-two face of an ascending
    cell."""
    n = len(sigma)
    return sum(1 for i in range(n) for j in range(n - 1)
               if erase_idx(erase_idx(sigma, i), j) == tau)


def codim2_faces(sigma: Cell) -> list[Cell]:
    n = len(sigma)
    return sorted({erase_idx(erase_idx(sigma, b), a)
                   for b in range(n) for a in range(b)})


def perfect_matching(sigma: Cell) -> bool:
    """Every codimension-two face of an ascending cell collects exactly
    the two cancelling terms — no third term in its slot."""
    return all(slot_multiplicity(sigma, tau) == 2
               for tau in codim2_faces(sigma))


# ---------------------------------------------------------------------------
# 4. The exhaustive check over the declared bounds

def ascending_cells(max_vertices: int, dim: int) -> list[Cell]:
    """All strictly ascending ``dim``-cells whose vertices are drawn
    from the first ``max_vertices`` numerals."""
    return [tuple(c) for c in combinations(range(max_vertices), dim + 1)]


def cancellation_report(max_vertices: int = MAX_VERTICES,
                        min_dim: int = MIN_DIM,
                        max_dim: int = MAX_DIM) -> dict[str, Json]:
    per_dim: dict[str, Json] = {}
    total_cells = 0
    total_coeff_checks = 0
    every_cancel = True
    every_distinct = True
    for dim in range(min_dim, max_dim + 1):
        cells = ascending_cells(max_vertices, dim)
        checks = 0
        for sigma in cells:
            ch = push_n(bd_n(sigma))
            checks += len(support(ch)) + len(facets(sigma)) + 2
        total_cells += len(cells)
        total_coeff_checks += checks
        dim_cancel = all(cell_cancels(s) for s in cells)
        dim_inj = all(erase_inj(s) for s in cells)
        dim_c2 = all(codim2_distinct(s) for s in cells)
        dim_match = all(perfect_matching(s) for s in cells)
        every_cancel = every_cancel and dim_cancel
        every_distinct = (every_distinct and dim_inj and dim_c2
                          and dim_match)
        per_dim[str(dim)] = {
            "cells": len(cells),
            "vertices_per_cell": dim + 1,
            "coefficient_checks": checks,
            "all_ascending": all(asc(s) for s in cells),
            "all_cancel": dim_cancel,
            "all_rect_identity": all(cell_rect_identity(s) for s in cells),
            "all_pairs_cancel": all(cell_pairs_cancel(s) for s in cells),
            "all_swap_identity": all(
                erase_swap(s, a, b)
                for s in cells
                for b in range(len(s)) for a in range(b)),
            "all_erase_injective": dim_inj,
            "all_codim2_distinct": dim_c2,
            "all_perfect_matching": dim_match,
            "involution": involution_report(dim + 1),
        }
    return {
        "bounds": {
            "max_vertices": max_vertices,
            "min_dim": min_dim,
            "max_dim": max_dim,
            "cells_checked": total_cells,
            "coefficient_checks": total_coeff_checks,
            "sgn_range": SGN_RANGE,
        },
        "all_cancel": every_cancel,
        "all_distinct": every_distinct,
        "sgn_alternates": all(
            sgn(c + 1) == -sgn(c) for c in range(SGN_RANGE)),
        "sgn_cancel_pairs": all(
            sgn_cancel(a, b)
            for b in range(1, SGN_RANGE) for a in range(b)),
        "per_dim": per_dim,
    }


# ---------------------------------------------------------------------------
# 5. Renaming independence (exact scope)

def rename(sigma: Cell, r: Callable[[int], int]) -> Cell:
    return tuple(r(x) for x in sigma)


def monotone_rename(x: int) -> int:
    """A strictly monotone renaming of vertices."""
    return 2 * x + 3


def swap01(x: int) -> int:
    """An INJECTIVE but non-monotone renaming: it destroys strict
    ascent, and the vanishing survives anyway."""
    if x == 0:
        return 1
    if x == 1:
        return 0
    return x


def renaming_report(max_vertices: int = MAX_VERTICES,
                    min_dim: int = MIN_DIM,
                    max_dim: int = MAX_DIM) -> dict[str, Json]:
    cells: list[Cell] = []
    for dim in range(min_dim, max_dim + 1):
        cells.extend(ascending_cells(max_vertices, dim))
    renamed = [rename(s, monotone_rename) for s in cells]
    scrambled = [rename(s, swap01) for s in cells]
    return {
        "renaming": "x |-> 2 * x + 3 (strictly monotone, injective)",
        "cells": len(cells),
        "monotone_preserves_ascent": all(asc(s) for s in renamed),
        "monotone_preserves_length": all(
            len(rename(s, monotone_rename)) == len(s) for s in cells),
        "faces_transport": all(
            erase_idx(rename(s, monotone_rename), i)
            == rename(erase_idx(s, i), monotone_rename)
            for s in cells for i in range(len(s) + 1)),
        "monotone_cancels": all(cell_cancels(s) for s in renamed),
        "monotone_keeps_distinctness": all(
            erase_inj(s) and codim2_distinct(s) for s in renamed),
        # exact scope: injective but non-monotone renamings can destroy
        # ascent; the vanishing does not depend on ascent at all
        "non_monotone_breaks_ascent": any(not asc(s) for s in scrambled),
        "non_monotone_still_cancels": all(cell_cancels(s)
                                          for s in scrambled),
        "scope": (
            "the vanishing needs no hypothesis on the renaming; strict "
            "monotonicity is what transports the well-formedness "
            "hypotheses (ascent, arity) and the distinctness statements"),
    }


# ---------------------------------------------------------------------------
# 6. Countermodel: the declared signs are load-bearing

SIGNLESS_CELLS: tuple[Cell, ...] = ((0, 1, 2), (0, 1, 2, 3), (0, 1, 2, 3, 4))


def signless_countermodel() -> dict[str, Json]:
    """Without the DECLARED alternating sign there is no cancellation:
    on every ascending cell below, the signless composite is nonzero at
    some face while the signed composite vanishes everywhere."""
    rows: dict[str, Json] = {}
    every_nonzero = True
    every_signed_zero = True
    for sigma in SIGNLESS_CELLS:
        signed = push_n(bd_n(sigma))
        signless = push_no_sign(bd_no_sign(sigma))
        taus = support(signless)
        nonzero = any(coeff_n(t, signless) != 0 for t in taus)
        signed_zero = all(coeff_n(t, signed) == 0 for t in taus)
        every_nonzero = every_nonzero and nonzero
        every_signed_zero = every_signed_zero and signed_zero
        rows[str(list(sigma))] = {
            "ascending": asc(sigma),
            "signless_coefficients": [
                [list(t), coeff_n(t, signless)] for t in taus],
            "signless_nonzero_somewhere": nonzero,
            "signed_zero_everywhere": signed_zero,
        }
    return {
        "cells": rows,
        "all_signless_nonzero": every_nonzero,
        "all_signed_zero": every_signed_zero,
        "verdict": (
            "the alternating sign convention is a DECLARED input; the "
            "uniform guarded filler rule does not force it, and the "
            "signless calculus refutes the vanishing"),
    }


# ---------------------------------------------------------------------------
# 7. Countermodel: the ill-formed (repeated-vertex) cell

PSEUDO_CELL: Cell = (0, 0, 1)
WELL_FORMED_CELL: Cell = (0, 1, 2)


def illformed_countermodel() -> dict[str, Json]:
    """Stated exactly, because the expected failure does NOT occur.

    What fails is DISTINCTNESS (two positions give one facet; the
    coefficient slot of ``(0,)`` collects four ordered pairs instead of
    two) and the boundary chain is degenerate (the facet ``(0, 1)`` has
    boundary coefficient zero).  What does NOT fail is the
    coefficientwise composite: it still vanishes, because the pairing
    argument never needed distinctness."""
    bad = PSEUDO_CELL
    good = WELL_FORMED_CELL
    bad_ch = push_n(bd_n(bad))
    return {
        "pseudo_cell": list(bad),
        "ascending": asc(bad),
        "facets": [list(t) for t in facets(bad)],
        "erase_injective": erase_inj(bad),
        "two_positions_one_facet": (
            erase_idx(bad, 0) == erase_idx(bad, 1)),
        "codim2_distinct": codim2_distinct(bad),
        "perfect_matching": perfect_matching(bad),
        "boundary_forgets_a_facet": (
            (0, 1) in facets(bad) and coeff_n((0, 1), bd_n(bad)) == 0),
        "slot_multiplicity_pseudo": slot_multiplicity(bad, (0,)),
        "slot_multiplicity_well_formed": slot_multiplicity(good, (0,)),
        "composite_still_vanishes": all(
            coeff_n(t, bad_ch) == 0 for t in support(bad_ch)),
        "verdict": (
            "strict ascent is not load-bearing for the coefficientwise "
            "vanishing (it still holds); it is load-bearing for "
            "distinctness, which fails here"),
    }
