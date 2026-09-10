r"""Higher Chain Complexes & Obstruction Homology (Target M109).

This module formalizes and computes:
1. Graded chain complexes C_k and boundary operators \partial_k: C_k \to C_{k-1}
   over discrete relational move complexes.
2. Fundamental nilpotency verification: \partial_k \circ \partial_{k+1} = 0.
3. Dual cochain complexes C^k with coboundary operators \delta^k = (\partial_{k+1})^T,
   verifying \delta^{k+1} \circ \delta^k = 0.
4. Exact rational homology H_k(C; Q) and cohomology H^k(C; Q) computation
   via exact rational Gaussian elimination (fractions.Fraction).
5. Obstruction classes detecting non-trivial circulation and topological obstruction
   cycles, scaling Target 7 to higher complexes.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import pathlib
import sys
from typing import Sequence

# Optional imports for Target 7 movegraph connection
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
_REPO_STR = str(REPO)
_CODE = str(REPO / "code")
_PDC = str(REPO / "research" / "path_dependent_cost")
for _p in (_REPO_STR, _CODE, _PDC):
    if _p not in sys.path:
        sys.path.insert(0, _p)

FractionVector = list[Fraction]
FractionMatrix = list[list[Fraction]]


# ---------------------------------------------------------------------------
# Exact Rational Linear Algebra
# ---------------------------------------------------------------------------

def to_fraction(val: int | float | Fraction | str) -> Fraction:
    """Convert scalar to exact Fraction."""
    if isinstance(val, Fraction):
        return val
    if isinstance(val, int):
        return Fraction(val, 1)
    if isinstance(val, str):
        return Fraction(val)
    if isinstance(val, float):
        return Fraction(val).limit_denominator(10**9)
    raise TypeError(f"Cannot convert {type(val)} to Fraction")


def to_fraction_matrix(matrix: Sequence[Sequence[int | float | Fraction]]) -> FractionMatrix:
    """Convert 2D sequence to exact FractionMatrix."""
    return [[to_fraction(val) for val in row] for row in matrix]


def zero_matrix(rows: int, cols: int) -> FractionMatrix:
    """Create a rows x cols zero matrix of Fractions."""
    return [[Fraction(0, 1) for _ in range(cols)] for _ in range(rows)]


def identity_matrix(n: int) -> FractionMatrix:
    """Create an n x n identity matrix of Fractions."""
    m = zero_matrix(n, n)
    for i in range(n):
        m[i][i] = Fraction(1, 1)
    return m


def matrix_transpose(m: FractionMatrix) -> FractionMatrix:
    """Compute exact transpose of a FractionMatrix."""
    if not m:
        return []
    rows = len(m)
    cols = len(m[0])
    return [[m[r][c] for r in range(rows)] for c in range(cols)]


def matrix_mul(a: FractionMatrix, b: FractionMatrix) -> FractionMatrix:
    """Compute exact matrix product a * b."""
    if not a or not b:
        return []
    rows_a = len(a)
    cols_a = len(a[0])
    rows_b = len(b)
    cols_b = len(b[0])
    if cols_a != rows_b:
        raise ValueError(f"Shape mismatch in matrix_mul: ({rows_a}, {cols_a}) x ({rows_b}, {cols_b})")

    out = zero_matrix(rows_a, cols_b)
    for r in range(rows_a):
        for k in range(cols_a):
            if a[r][k] != 0:
                for c in range(cols_b):
                    out[r][c] += a[r][k] * b[k][c]
    return out


def matrix_vector_mul(m: FractionMatrix, v: Sequence[int | Fraction]) -> FractionVector:
    """Compute exact matrix-vector product m * v."""
    if not m:
        return []
    rows = len(m)
    cols = len(m[0])
    if len(v) != cols:
        raise ValueError(f"Shape mismatch in matrix_vector_mul: ({rows}, {cols}) x {len(v)}")
    fv = [to_fraction(x) for x in v]
    out: FractionVector = [Fraction(0, 1) for _ in range(rows)]
    for r in range(rows):
        total = Fraction(0, 1)
        for c in range(cols):
            if m[r][c] != 0:
                total += m[r][c] * fv[c]
        out[r] = total
    return out


def vector_dot(u: Sequence[int | Fraction], v: Sequence[int | Fraction]) -> Fraction:
    """Compute exact dot product of two vectors."""
    if len(u) != len(v):
        raise ValueError(f"Length mismatch in vector_dot: {len(u)} != {len(v)}")
    return sum((to_fraction(a) * to_fraction(b) for a, b in zip(u, v)), Fraction(0, 1))


def is_zero_matrix(m: FractionMatrix) -> bool:
    """Check if all entries in matrix are exactly 0."""
    return all(val == 0 for row in m for val in row)


def rref(matrix: FractionMatrix) -> tuple[FractionMatrix, list[int], int]:
    """Compute Reduced Row Echelon Form (RREF) over Q using exact Gaussian elimination.

    Returns:
        (rref_matrix, pivot_columns, rank)
    """
    if not matrix:
        return [], [], 0
    rows = len(matrix)
    cols = len(matrix[0])
    if cols == 0:
        return [[] for _ in range(rows)], [], 0

    m = [[matrix[r][c] for c in range(cols)] for r in range(rows)]
    pivot_cols: list[int] = []
    pivot_row = 0

    for c in range(cols):
        # Find pivot in column c at or below pivot_row
        sel = -1
        for r in range(pivot_row, rows):
            if m[r][c] != 0:
                sel = r
                break
        if sel == -1:
            continue

        # Swap rows
        m[pivot_row], m[sel] = m[sel], m[pivot_row]

        # Rescale pivot row so pivot element is 1
        pivot_val = m[pivot_row][c]
        for j in range(c, cols):
            m[pivot_row][j] /= pivot_val

        # Eliminate other rows
        for r in range(rows):
            if r != pivot_row and m[r][c] != 0:
                factor = m[r][c]
                for j in range(c, cols):
                    m[r][j] -= factor * m[pivot_row][j]

        pivot_cols.append(c)
        pivot_row += 1
        if pivot_row == rows:
            break

    return m, pivot_cols, len(pivot_cols)


def matrix_rank(matrix: FractionMatrix) -> int:
    """Compute exact rank over Q."""
    _, _, rank = rref(matrix)
    return rank


def kernel_basis(matrix: FractionMatrix) -> list[FractionVector]:
    """Compute an exact rational basis for the nullspace / kernel of matrix.

    {x in Q^cols : matrix * x = 0}.
    """
    if not matrix:
        return []
    rows = len(matrix)
    cols = len(matrix[0])
    if cols == 0:
        return []

    r_mat, pivot_cols, _ = rref(matrix)
    pivot_set = set(pivot_cols)
    free_cols = [c for c in range(cols) if c not in pivot_set]

    # Map pivot column index to its row index in rref
    pivot_row_map = {c: idx for idx, c in enumerate(pivot_cols)}

    basis: list[FractionVector] = []
    for free in free_cols:
        vec = [Fraction(0, 1) for _ in range(cols)]
        vec[free] = Fraction(1, 1)
        for p_col, r_idx in pivot_row_map.items():
            vec[p_col] = -r_mat[r_idx][free]
        basis.append(vec)

    return basis


def column_space_basis(matrix: FractionMatrix) -> list[FractionVector]:
    """Compute an exact rational basis for the column space / image of matrix.

    Columns of original matrix corresponding to pivot columns in RREF.
    """
    if not matrix:
        return []
    cols = len(matrix[0])
    if cols == 0:
        return []

    _, pivot_cols, _ = rref(matrix)
    basis: list[FractionVector] = []
    for c in pivot_cols:
        col_vec = [matrix[r][c] for r in range(len(matrix))]
        basis.append(col_vec)
    return basis


def quotient_basis(
    kernel_vectors: list[FractionVector],
    image_vectors: list[FractionVector],
    dim: int,
) -> list[FractionVector]:
    """Extract an exact basis for the quotient space Z / B over Q.

    Given a subspace Z = span(kernel_vectors) and B = span(image_vectors) <= Z,
    selects vectors from kernel_vectors that are linearly independent modulo B.
    """
    if not kernel_vectors:
        return []

    # Basis of image_vectors (B)
    basis_b: list[FractionVector] = []
    if image_vectors:
        m_b = matrix_transpose(image_vectors)
        _, pivots_b, _ = rref(m_b)
        basis_b = [image_vectors[p] for p in pivots_b]

    rank_b = len(basis_b)
    all_candidates = basis_b + kernel_vectors

    # Columns of m_all are the candidates
    m_all = matrix_transpose(all_candidates)
    _, pivots_all, _ = rref(m_all)

    # Pivot columns at or beyond rank_b select elements from kernel_vectors
    quotient_indices = [p - rank_b for p in pivots_all if p >= rank_b]
    return [kernel_vectors[idx] for idx in quotient_indices]


# ---------------------------------------------------------------------------
# Graded Chain Complex and Dual Cochain Complex
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class HomologyGroup:
    grade: int
    dim_chains: int
    dim_cycles: int
    dim_boundaries: int
    betti_number: int
    basis_cycles: list[FractionVector]


@dataclass(frozen=True)
class CohomologyGroup:
    grade: int
    dim_cochains: int
    dim_cocycles: int
    dim_coboundaries: int
    betti_number: int
    basis_cocycles: list[FractionVector]


@dataclass(frozen=True)
class ObstructionReport:
    cochain_grade: int
    is_cocycle: bool
    is_coboundary: bool
    is_obstruction_class: bool
    witness_cycle: FractionVector | None
    circulation: Fraction
    explanation: str


class GradedChainComplex:
    """Graded chain complex C_k with boundary operators \\partial_k: C_k -> C_{k-1}."""

    def __init__(
        self,
        max_grade: int,
        dimensions: dict[int, int],
        boundary_matrices: dict[int, Sequence[Sequence[int | float | Fraction]]],
        cell_names: dict[int, list[str]] | None = None,
    ) -> None:
        self.max_grade = max_grade
        self.dimensions = {k: dimensions.get(k, 0) for k in range(max_grade + 1)}
        self.cell_names = cell_names or {
            k: [f"c_{k}_{i}" for i in range(self.dimensions[k])] for k in range(max_grade + 1)
        }

        self.boundary_matrices: dict[int, FractionMatrix] = {}
        for k in range(1, max_grade + 1):
            mat = boundary_matrices.get(k, [])
            rows = self.dimensions[k - 1]
            cols = self.dimensions[k]
            if not mat:
                f_mat = zero_matrix(rows, cols)
            else:
                f_mat = to_fraction_matrix(mat)
                if len(f_mat) != rows or (rows > 0 and len(f_mat[0]) != cols):
                    raise ValueError(
                        f"Boundary matrix \\partial_{k} shape mismatch: expected ({rows}, {cols}), got ({len(f_mat)}, {len(f_mat[0]) if f_mat else 0})"
                    )
            self.boundary_matrices[k] = f_mat

    def boundary(self, k: int) -> FractionMatrix:
        """Return boundary matrix \\partial_k: C_k -> C_{k-1}."""
        if k <= 0 or k > self.max_grade:
            return zero_matrix(0, self.dimensions.get(k, 0))
        return self.boundary_matrices[k]

    def verify_nilpotency(self) -> dict[int, bool]:
        """Verify \\partial_k \\circ \\partial_{k+1} = 0 for all k in 1 .. max_grade - 1."""
        results: dict[int, bool] = {}
        for k in range(1, self.max_grade):
            d_k = self.boundary(k)
            d_k_plus_1 = self.boundary(k + 1)
            prod = matrix_mul(d_k, d_k_plus_1)
            is_zero = is_zero_matrix(prod)
            results[k] = is_zero
            if not is_zero:
                raise ValueError(f"Nilpotency failed at grade {k}: \\partial_{k} \\circ \\partial_{k+1} != 0")
        return results

    def compute_homology(self, grade: int) -> HomologyGroup:
        """Compute homology group H_k(C; Q) = Z_k / B_k."""
        if grade < 0 or grade > self.max_grade:
            return HomologyGroup(grade, 0, 0, 0, 0, [])

        n_k = self.dimensions[grade]
        if n_k == 0:
            return HomologyGroup(grade, 0, 0, 0, 0, [])

        # Z_k = ker(\partial_k)
        if grade == 0:
            # \partial_0 = 0, so Z_0 = C_0
            z_basis = identity_matrix(n_k)
        else:
            d_k = self.boundary(grade)
            z_basis = kernel_basis(d_k)

        dim_cycles = len(z_basis)

        # B_k = im(\partial_{k+1})
        if grade == self.max_grade:
            b_basis: list[FractionVector] = []
        else:
            d_k_plus_1 = self.boundary(grade + 1)
            b_basis = column_space_basis(d_k_plus_1)

        dim_boundaries = len(b_basis)
        betti = dim_cycles - dim_boundaries

        # Quotient basis for H_k
        h_basis = quotient_basis(z_basis, b_basis, n_k)

        return HomologyGroup(
            grade=grade,
            dim_chains=n_k,
            dim_cycles=dim_cycles,
            dim_boundaries=dim_boundaries,
            betti_number=betti,
            basis_cycles=h_basis,
        )

    def compute_all_homology(self) -> dict[int, HomologyGroup]:
        """Compute homology groups across all grades 0 .. max_grade."""
        return {k: self.compute_homology(k) for k in range(self.max_grade + 1)}

    def euler_characteristic(self) -> int:
        """Compute Euler characteristic \\chi = \\sum (-1)^k dim(C_k) = \\sum (-1)^k \\beta_k."""
        chi_chains = sum((-1)**k * self.dimensions[k] for k in range(self.max_grade + 1))
        h_all = self.compute_all_homology()
        chi_homology = sum((-1)**k * h_all[k].betti_number for k in range(self.max_grade + 1))
        if chi_chains != chi_homology:
            raise RuntimeError(f"Euler-Poincare mismatch: chains={chi_chains} != homology={chi_homology}")
        return chi_chains

    def dual_cochain_complex(self) -> DualCochainComplex:
        """Construct the dual cochain complex C^* with coboundary operators."""
        return DualCochainComplex(self)


class DualCochainComplex:
    """Dual cochain complex C^k with coboundary operators \\delta^k = (\\partial_{k+1})^T."""

    def __init__(self, chain_complex: GradedChainComplex) -> None:
        self.chain_complex = chain_complex
        self.max_grade = chain_complex.max_grade
        self.dimensions = chain_complex.dimensions
        self.coboundary_matrices: dict[int, FractionMatrix] = {}

        for k in range(self.max_grade):
            # \delta^k: C^k -> C^{k+1} is transpose of \partial_{k+1}: C_{k+1} -> C_k
            d_next = chain_complex.boundary(k + 1)
            self.coboundary_matrices[k] = matrix_transpose(d_next)

    def coboundary(self, k: int) -> FractionMatrix:
        """Return coboundary matrix \\delta^k: C^k -> C^{k+1}."""
        if k < 0 or k >= self.max_grade:
            return zero_matrix(0, self.dimensions.get(k, 0))
        return self.coboundary_matrices[k]

    def verify_coboundary_nilpotency(self) -> dict[int, bool]:
        """Verify \\delta^{k+1} \\circ \\delta^k = 0 for all k in 0 .. max_grade - 2."""
        results: dict[int, bool] = {}
        for k in range(self.max_grade - 1):
            delta_k = self.coboundary(k)
            delta_k_plus_1 = self.coboundary(k + 1)
            prod = matrix_mul(delta_k_plus_1, delta_k)
            is_zero = is_zero_matrix(prod)
            results[k] = is_zero
            if not is_zero:
                raise ValueError(f"Coboundary nilpotency failed at grade {k}: \\delta^{k+1} \\circ \\delta^k != 0")
        return results

    def compute_cohomology(self, grade: int) -> CohomologyGroup:
        """Compute cohomology group H^k(C; Q) = Z^k / B^k."""
        if grade < 0 or grade > self.max_grade:
            return CohomologyGroup(grade, 0, 0, 0, 0, [])

        n_k = self.dimensions[grade]
        if n_k == 0:
            return CohomologyGroup(grade, 0, 0, 0, 0, [])

        # Z^k = ker(\delta^k)
        if grade == self.max_grade:
            # \delta^max_grade = 0
            z_basis = identity_matrix(n_k)
        else:
            delta_k = self.coboundary(grade)
            z_basis = kernel_basis(delta_k)

        dim_cocycles = len(z_basis)

        # B^k = im(\delta^{k-1})
        if grade == 0:
            b_basis: list[FractionVector] = []
        else:
            delta_prev = self.coboundary(grade - 1)
            b_basis = column_space_basis(delta_prev)

        dim_coboundaries = len(b_basis)
        betti = dim_cocycles - dim_coboundaries

        # Quotient basis for H^k
        h_basis = quotient_basis(z_basis, b_basis, n_k)

        return CohomologyGroup(
            grade=grade,
            dim_cochains=n_k,
            dim_cocycles=dim_cocycles,
            dim_coboundaries=dim_coboundaries,
            betti_number=betti,
            basis_cocycles=h_basis,
        )

    def compute_all_cohomology(self) -> dict[int, CohomologyGroup]:
        """Compute cohomology groups across all grades 0 .. max_grade."""
        return {k: self.compute_cohomology(k) for k in range(self.max_grade + 1)}

    def natural_pairing(self, cochain: Sequence[int | Fraction], chain: Sequence[int | Fraction]) -> Fraction:
        """Natural duality pairing <\\omega, c> = \\sum \\omega_i c_i."""
        return vector_dot(cochain, chain)

    def verify_stokes_theorem(
        self,
        grade: int,
        cochain: Sequence[int | Fraction],
        chain_higher: Sequence[int | Fraction],
    ) -> bool:
        """Verify discrete Stokes-Cartan theorem: <\\delta^k \\omega, c> = <\\omega, \\partial_{k+1} c>."""
        if grade < 0 or grade >= self.max_grade:
            return True
        delta_k = self.coboundary(grade)
        d_next = self.chain_complex.boundary(grade + 1)

        coboundary_omega = matrix_vector_mul(delta_k, cochain)
        boundary_c = matrix_vector_mul(d_next, chain_higher)

        lhs = vector_dot(coboundary_omega, chain_higher)
        rhs = vector_dot(cochain, boundary_c)
        return lhs == rhs


# ---------------------------------------------------------------------------
# Obstruction Classes and Analysis
# ---------------------------------------------------------------------------

def analyze_obstruction(
    chain_complex: GradedChainComplex,
    grade: int,
    cochain: Sequence[int | Fraction],
) -> ObstructionReport:
    """Analyze a cochain \\omega in C^k to determine whether it represents a non-trivial obstruction class.

    Returns an ObstructionReport detailing:
    - Whether \\omega is a cocycle (\\delta^k \\omega = 0)
    - Whether \\omega is exact / coboundary (\\omega = \\delta^{k-1} P)
    - If not exact, exhibits a homology witness cycle z in Z_k with <\\omega, z> != 0.
    """
    n_k = chain_complex.dimensions[grade]
    if len(cochain) != n_k:
        raise ValueError(f"Cochain length {len(cochain)} does not match dimension {n_k} of grade {grade}")

    dual = chain_complex.dual_cochain_complex()
    f_cochain = [to_fraction(x) for x in cochain]

    # 1. Check if cocycle: \delta^k \omega == 0
    if grade < chain_complex.max_grade:
        delta_k = dual.coboundary(grade)
        d_omega = matrix_vector_mul(delta_k, f_cochain)
        is_cocycle = all(val == 0 for val in d_omega)
    else:
        is_cocycle = True

    if not is_cocycle:
        return ObstructionReport(
            cochain_grade=grade,
            is_cocycle=False,
            is_coboundary=False,
            is_obstruction_class=False,
            witness_cycle=None,
            circulation=Fraction(0, 1),
            explanation=f"Cochain at grade {grade} is not closed (curvature/coboundary is non-zero).",
        )

    # 2. Check if coboundary: \omega in im(\delta^{k-1})
    is_coboundary = False
    if grade == 0:
        # Grade 0 has no non-trivial coboundaries
        is_coboundary = all(x == 0 for x in f_cochain)
    else:
        delta_prev = dual.coboundary(grade - 1)
        # Solve delta_prev * P = f_cochain
        # Rank of delta_prev vs rank of [delta_prev | f_cochain]
        r_prev = matrix_rank(delta_prev)
        augmented = [row + [f_cochain[idx]] for idx, row in enumerate(delta_prev)]
        r_aug = matrix_rank(augmented)
        is_coboundary = (r_prev == r_aug)

    if is_coboundary:
        return ObstructionReport(
            cochain_grade=grade,
            is_cocycle=True,
            is_coboundary=True,
            is_obstruction_class=False,
            witness_cycle=None,
            circulation=Fraction(0, 1),
            explanation=f"Cochain at grade {grade} is exact (in the image of \\delta^{grade-1}).",
        )

    # 3. Non-trivial obstruction class! Find witness homology cycle
    h_k = chain_complex.compute_homology(grade)
    witness: FractionVector | None = None
    circulation = Fraction(0, 1)

    for cycle in h_k.basis_cycles:
        circ = vector_dot(f_cochain, cycle)
        if circ != 0:
            witness = cycle
            circulation = circ
            break

    # If basis_cycles did not exhibit (e.g. if dim H_k = 0), check cycles
    if witness is None:
        d_k = chain_complex.boundary(grade) if grade > 0 else zero_matrix(0, n_k)
        cycles = kernel_basis(d_k) if grade > 0 else identity_matrix(n_k)
        for cycle in cycles:
            circ = vector_dot(f_cochain, cycle)
            if circ != 0:
                witness = cycle
                circulation = circ
                break

    return ObstructionReport(
        cochain_grade=grade,
        is_cocycle=True,
        is_coboundary=False,
        is_obstruction_class=True,
        witness_cycle=witness,
        circulation=circulation,
        explanation=(
            f"Non-trivial obstruction class in H^{grade}(C; Q) with non-zero circulation "
            f"{circulation} on witness cycle."
        ),
    )


# ---------------------------------------------------------------------------
# Discrete Relational Complex Constructors
# ---------------------------------------------------------------------------

def build_cycle_complex(n: int) -> GradedChainComplex:
    """Build directed n-cycle complex C_n (1-dimensional S^1 model).

    Vertices: 0 .. n-1
    Edges: (i -> (i+1)%n) for i in 0 .. n-1.
    Expected: \\beta_0 = 1, \\beta_1 = 1.
    """
    if n < 3:
        raise ValueError("Cycle complex must have at least 3 vertices.")
    dims = {0: n, 1: n}
    d1 = zero_matrix(n, n)
    for i in range(n):
        src = i
        tgt = (i + 1) % n
        d1[src][i] -= Fraction(1, 1)
        d1[tgt][i] += Fraction(1, 1)

    return GradedChainComplex(
        max_grade=1,
        dimensions=dims,
        boundary_matrices={1: d1},
    )


def build_torus_complex(m: int = 3, n: int = 3) -> GradedChainComplex:
    """Build discretized flat 2-torus T^2 with m x n square grid and periodic boundaries.

    Vertices: (i, j) for i in 0..m-1, j in 0..n-1  (dim C_0 = mn)
    Edges: horizontal and vertical transitions    (dim C_1 = 2mn)
    2-cells: commuting squares                     (dim C_2 = mn)
    Expected: \\beta_0 = 1, \\beta_1 = 2, \\beta_2 = 1.
    """
    n_v = m * n
    n_e = 2 * m * n
    n_s = m * n

    def v_idx(i: int, j: int) -> int:
        return (i % m) * n + (j % n)

    def e_h_idx(i: int, j: int) -> int:
        return (i % m) * n + (j % n)

    def e_v_idx(i: int, j: int) -> int:
        return n_v + (i % m) * n + (j % n)

    def sq_idx(i: int, j: int) -> int:
        return (i % m) * n + (j % n)

    # d1: C_1 -> C_0
    d1 = zero_matrix(n_v, n_e)
    for i in range(m):
        for j in range(n):
            u = v_idx(i, j)
            # Horizontal edge: (i, j) -> (i+1, j)
            e_h = e_h_idx(i, j)
            tgt_h = v_idx(i + 1, j)
            d1[u][e_h] -= Fraction(1, 1)
            d1[tgt_h][e_h] += Fraction(1, 1)

            # Vertical edge: (i, j) -> (i, j+1)
            e_v = e_v_idx(i, j)
            tgt_v = v_idx(i, j + 1)
            d1[u][e_v] -= Fraction(1, 1)
            d1[tgt_v][e_v] += Fraction(1, 1)

    # d2: C_2 -> C_1
    # Square at (i, j): bottom (i,j)->(i+1,j), right (i+1,j)->(i+1,j+1),
    #                   top (i,j)->(i,j+1), left (i,j+1)->(i+1,j+1)
    d2 = zero_matrix(n_e, n_s)
    for i in range(m):
        for j in range(n):
            s = sq_idx(i, j)
            e_bottom = e_h_idx(i, j)
            e_right = e_v_idx(i + 1, j)
            e_top = e_v_idx(i, j)
            e_left = e_h_idx(i, j + 1)

            # Boundary: (bottom + right) - (top + left)
            d2[e_bottom][s] += Fraction(1, 1)
            d2[e_right][s] += Fraction(1, 1)
            d2[e_top][s] -= Fraction(1, 1)
            d2[e_left][s] -= Fraction(1, 1)

    return GradedChainComplex(
        max_grade=2,
        dimensions={0: n_v, 1: n_e, 2: n_s},
        boundary_matrices={1: d1, 2: d2},
    )


def build_cubical_cavity_complex(include_3cell: bool = False) -> GradedChainComplex:
    """Build cubical complex (boundary of 3-cube, optionally with 3-cell interior).

    Without 3-cell: \\beta_0 = 1, \\beta_1 = 0, \\beta_2 = 1  (topological 2-sphere S^2 cavity).
    With 3-cell:    \\partial_2 \\circ \\partial_3 = 0, killing H_2 so \\beta_2 = 0.
    """
    # 8 vertices: (x, y, z) in {0,1}^3
    def v_id(x: int, y: int, z: int) -> int:
        return (x << 2) | (y << 1) | z

    # 12 edges along 3 axes
    edges: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []
    edge_map: dict[tuple[tuple[int, int, int], tuple[int, int, int]], int] = {}
    for axis in range(3):
        for u in (0, 1):
            for v in (0, 1):
                if axis == 0:
                    pt0, pt1 = (0, u, v), (1, u, v)
                elif axis == 1:
                    pt0, pt1 = (u, 0, v), (u, 1, v)
                else:
                    pt0, pt1 = (u, v, 0), (u, v, 1)
                e_idx = len(edges)
                edges.append((pt0, pt1))
                edge_map[(pt0, pt1)] = e_idx

    n_v = 8
    n_e = len(edges)
    d1 = zero_matrix(n_v, n_e)
    for j, (p0, p1) in enumerate(edges):
        d1[v_id(*p0)][j] -= Fraction(1, 1)
        d1[v_id(*p1)][j] += Fraction(1, 1)

    # 6 square faces: for axis in (0,1,2), eps in (0,1)
    faces: list[tuple[int, int]] = []
    for axis in range(3):
        for eps in (0, 1):
            faces.append((axis, eps))

    n_f = len(faces)
    d2 = zero_matrix(n_e, n_f)
    for f_idx, (axis, eps) in enumerate(faces):
        rem = [a for a in range(3) if a != axis]
        a1, a2 = rem[0], rem[1]

        def get_pt(v_a1: int, v_a2: int) -> tuple[int, int, int]:
            pt = [0, 0, 0]
            pt[axis] = eps
            pt[a1] = v_a1
            pt[a2] = v_a2
            return (pt[0], pt[1], pt[2])

        e_a1_0 = edge_map[(get_pt(0, 0), get_pt(1, 0))]
        e_a1_1 = edge_map[(get_pt(0, 1), get_pt(1, 1))]
        e_a2_0 = edge_map[(get_pt(0, 0), get_pt(0, 1))]
        e_a2_1 = edge_map[(get_pt(1, 0), get_pt(1, 1))]

        d2[e_a1_0][f_idx] += Fraction(1, 1)
        d2[e_a2_1][f_idx] += Fraction(1, 1)
        d2[e_a1_1][f_idx] -= Fraction(1, 1)
        d2[e_a2_0][f_idx] -= Fraction(1, 1)

    if not include_3cell:
        return GradedChainComplex(
            max_grade=2,
            dimensions={0: n_v, 1: n_e, 2: n_f},
            boundary_matrices={1: d1, 2: d2},
        )

    # With 3-cell: interior 3-cube with boundary given by oriented faces
    n_cube = 1
    d3 = zero_matrix(n_f, n_cube)
    for f_idx, (axis, eps) in enumerate(faces):
        sgn = ((-1)**(axis + 1)) * (1 if eps == 1 else -1)
        d3[f_idx][0] = Fraction(sgn, 1)

    return GradedChainComplex(
        max_grade=3,
        dimensions={0: n_v, 1: n_e, 2: n_f, 3: n_cube},
        boundary_matrices={1: d1, 2: d2, 3: d3},
    )



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


def extract_pure_squares(
    graph: mg.MoveGraph, squares: list[tuple[int, tuple[int, int], tuple[int, int]]]
) -> list[CommutingSquare]:
    """Extract and classify all commuting squares into pure vs impure."""
    import movegraph as mg_local
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
                left_items=(mg_local.item_kind(e_l0.item), mg_local.item_kind(e_l1.item)),
                right_items=(mg_local.item_kind(e_r0.item), mg_local.item_kind(e_r1.item)),
            )
        )
    return out


def build_target7_complex(pure_only: bool = False) -> GradedChainComplex:
    """Build the discrete relational move complex from Target 7 (depth-3 move graph).

    Vertices: 262 regimes
    Edges: 638 single moves
    2-cells: 770 commuting squares (or 146 pure commuting squares)
    """
    import costs as ct
    import exactness as ex
    import movegraph as mg

    graph = mg.build()
    n_v = len(graph.states)
    n_e = len(graph.edges)

    # d1: C_1 -> C_0
    d1 = zero_matrix(n_v, n_e)
    for e_idx, e in enumerate(graph.edges):
        d1[e.source][e_idx] -= Fraction(1, 1)
        d1[e.target][e_idx] += Fraction(1, 1)

    raw_squares = ex.commuting_squares(graph)
    all_squares = extract_pure_squares(graph, raw_squares)
    selected_squares = [s for s in all_squares if s.is_pure] if pure_only else all_squares

    n_s = len(selected_squares)
    d2 = zero_matrix(n_e, n_s)
    for s_idx, sq in enumerate(selected_squares):
        # Route left - route right
        d2[sq.route_left[0]][s_idx] += Fraction(1, 1)
        d2[sq.route_left[1]][s_idx] += Fraction(1, 1)
        d2[sq.route_right[0]][s_idx] -= Fraction(1, 1)
        d2[sq.route_right[1]][s_idx] -= Fraction(1, 1)

    return GradedChainComplex(
        max_grade=2,
        dimensions={0: n_v, 1: n_e, 2: n_s},
        boundary_matrices={1: d1, 2: d2},
    )


def evaluate_target7_native_candidates(complex_target7: GradedChainComplex) -> dict[str, ObstructionReport]:
    """Evaluate native cost candidates from Target 7 as 1-cochains on the move complex."""
    import costs as ct
    import exactness as ex
    import movegraph as mg

    graph = mg.build()
    reports: dict[str, ObstructionReport] = {}
    cands = ["rule_span", "width_at_admission", "empty_admission", "mention_deficit"]

    for name in cands:
        weights = ex.edge_weights(graph, name)
        cochain = [Fraction(w, 1) for w in weights]
        reports[name] = analyze_obstruction(complex_target7, grade=1, cochain=cochain)

    return reports
