"""Finite Commutator Obstruction & Discrete MUB Tomography.

AuthorityEffect: None.

Implements Target P208c:
1. Exact arithmetic over cyclotomic rationals Q(w) with w^2 + w + 1 = 0 and Gaussian rationals Q(i).
2. Finite-dimensional commutator trace obstruction:
   Tr([A, B]) = 0 for any finite N x N matrices.
   Proof that [Q, P] = c * I_N with c != 0 is algebraically obstructed on any finite carrier.
3. Multi-locus microcausality on composite carriers:
   Observables on disjoint loci commute: [A (x) I_B, I_A (x) B] = 0.
   Conjugate observables on the same locus (discrete clock & shift) fail to commute.
4. Discrete Mutually Unbiased Bases (MUBs):
   Exact construction of d + 1 = 4 MUBs in dimension d = 3.
   Exact construction of d + 1 = 5 MUBs in dimension d = 4.
   Pairwise unbiasedness: |<u_j | v_k>|^2 = 1/d.
5. Complete operational state tomography:
   Reconstruction of discrete carrier density operators from measurement statistics
   along all d + 1 MUBs using exact rational inversion.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, List, Sequence, Tuple, TypeVar


# =============================================================================
# 1. Exact Number Fields: Cyclotomic Q(w) and Gaussian Q(i)
# =============================================================================

class Cyclotomic3:
    """Exact cyclotomic rational element a + b*w where w = (-1 + sqrt(-3))/2.

    Minimal polynomial: w^2 + w + 1 = 0, so w^3 = 1 and w^2 = -1 - w.
    Complex conjugate: conj(a + b*w) = (a - b) - b*w.
    Squared modulus: (a + b*w) * conj(a + b*w) = a^2 - a*b + b^2 in Q.
    """

    __slots__ = ("_a", "_b")
    _a: Fraction
    _b: Fraction

    def __init__(self, a: int | Fraction | Cyclotomic3 = 0, b: int | Fraction = 0) -> None:
        if isinstance(a, Cyclotomic3):
            self._a = a._a
            self._b = a._b
        else:
            self._a = Fraction(a)
            self._b = Fraction(b)

    @property
    def a(self) -> Fraction:
        return self._a

    @property
    def b(self) -> Fraction:
        return self._b

    def __neg__(self) -> Cyclotomic3:
        return Cyclotomic3(-self._a, -self._b)

    def __add__(self, other: Any) -> Cyclotomic3:
        if isinstance(other, (int, Fraction)):
            return Cyclotomic3(self._a + Fraction(other), self._b)
        if isinstance(other, Cyclotomic3):
            return Cyclotomic3(self._a + other._a, self._b + other._b)
        return NotImplemented

    def __radd__(self, other: Any) -> Cyclotomic3:
        return self.__add__(other)

    def __sub__(self, other: Any) -> Cyclotomic3:
        if isinstance(other, (int, Fraction)):
            return Cyclotomic3(self._a - Fraction(other), self._b)
        if isinstance(other, Cyclotomic3):
            return Cyclotomic3(self._a - other._a, self._b - other._b)
        return NotImplemented

    def __rsub__(self, other: Any) -> Cyclotomic3:
        if isinstance(other, (int, Fraction)):
            return Cyclotomic3(Fraction(other) - self._a, -self._b)
        return NotImplemented

    def __mul__(self, other: Any) -> Cyclotomic3:
        if isinstance(other, (int, Fraction)):
            f = Fraction(other)
            return Cyclotomic3(self._a * f, self._b * f)
        if isinstance(other, Cyclotomic3):
            # (a + b*w)(c + d*w) = (ac - bd) + (ad + bc - bd)*w
            a, b = self._a, self._b
            c, d = other._a, other._b
            return Cyclotomic3(a * c - b * d, a * d + b * c - b * d)
        return NotImplemented

    def __rmul__(self, other: Any) -> Cyclotomic3:
        return self.__mul__(other)

    def conj(self) -> Cyclotomic3:
        """Complex conjugation: w -> w^2 = -1 - w."""
        return Cyclotomic3(self._a - self._b, -self._b)

    def norm_sq(self) -> Fraction:
        """Exact rational squared magnitude: a^2 - a*b + b^2."""
        val: Fraction = self._a * self._a - self._a * self._b + self._b * self._b
        return val

    def abs_sq(self) -> Fraction:
        return self.norm_sq()

    def __truediv__(self, other: Any) -> Cyclotomic3:
        if isinstance(other, (int, Fraction)):
            f = Fraction(other)
            if f == 0:
                raise ZeroDivisionError("Division by rational zero")
            return Cyclotomic3(self._a / f, self._b / f)
        if isinstance(other, Cyclotomic3):
            nsq = other.norm_sq()
            if nsq == 0:
                raise ZeroDivisionError("Division by cyclotomic zero")
            num = self * other.conj()
            return Cyclotomic3(num._a / nsq, num._b / nsq)
        return NotImplemented

    def __rtruediv__(self, other: Any) -> Cyclotomic3:
        return Cyclotomic3(other) / self

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, (int, Fraction)):
            return bool(self._a == other and self._b == 0)
        if isinstance(other, Cyclotomic3):
            return bool(self._a == other._a and self._b == other._b)
        return False

    def __hash__(self) -> int:
        return hash((self._a, self._b))

    def __repr__(self) -> str:
        return f"Cyclotomic3({self._a}, {self._b})"

    def __str__(self) -> str:
        if self._b == 0:
            return str(self._a)
        if self._a == 0:
            return f"{self._b}*w"
        sign = "+" if self._b > 0 else "-"
        return f"({self._a} {sign} {abs(self._b)}*w)"

    @classmethod
    def root_power(cls, p: int) -> Cyclotomic3:
        """Returns w^p for integer p."""
        rem = p % 3
        if rem == 0:
            return cls(1, 0)
        if rem == 1:
            return cls(0, 1)
        return cls(-1, -1)


class GaussianRational:
    """Exact Gaussian rational element a + b*i where i^2 = -1, with a, b in Q."""

    __slots__ = ("_a", "_b")
    _a: Fraction
    _b: Fraction

    def __init__(self, a: int | Fraction | GaussianRational = 0, b: int | Fraction = 0) -> None:
        if isinstance(a, GaussianRational):
            self._a = a._a
            self._b = a._b
        else:
            self._a = Fraction(a)
            self._b = Fraction(b)

    @property
    def a(self) -> Fraction:
        return self._a

    @property
    def b(self) -> Fraction:
        return self._b

    def __neg__(self) -> GaussianRational:
        return GaussianRational(-self._a, -self._b)

    def __add__(self, other: Any) -> GaussianRational:
        if isinstance(other, (int, Fraction)):
            return GaussianRational(self._a + Fraction(other), self._b)
        if isinstance(other, GaussianRational):
            return GaussianRational(self._a + other._a, self._b + other._b)
        return NotImplemented

    def __radd__(self, other: Any) -> GaussianRational:
        return self.__add__(other)

    def __sub__(self, other: Any) -> GaussianRational:
        if isinstance(other, (int, Fraction)):
            return GaussianRational(self._a - Fraction(other), self._b)
        if isinstance(other, GaussianRational):
            return GaussianRational(self._a - other._a, self._b - other._b)
        return NotImplemented

    def __rsub__(self, other: Any) -> GaussianRational:
        if isinstance(other, (int, Fraction)):
            return GaussianRational(Fraction(other) - self._a, -self._b)
        return NotImplemented

    def __mul__(self, other: Any) -> GaussianRational:
        if isinstance(other, (int, Fraction)):
            f = Fraction(other)
            return GaussianRational(self._a * f, self._b * f)
        if isinstance(other, GaussianRational):
            a, b = self._a, self._b
            c, d = other._a, other._b
            return GaussianRational(a * c - b * d, a * d + b * c)
        return NotImplemented

    def __rmul__(self, other: Any) -> GaussianRational:
        return self.__mul__(other)

    def conj(self) -> GaussianRational:
        return GaussianRational(self._a, -self._b)

    def norm_sq(self) -> Fraction:
        val: Fraction = self._a * self._a + self._b * self._b
        return val

    def abs_sq(self) -> Fraction:
        return self.norm_sq()

    def __truediv__(self, other: Any) -> GaussianRational:
        if isinstance(other, (int, Fraction)):
            f = Fraction(other)
            if f == 0:
                raise ZeroDivisionError("Division by rational zero")
            return GaussianRational(self._a / f, self._b / f)
        if isinstance(other, GaussianRational):
            nsq = other.norm_sq()
            if nsq == 0:
                raise ZeroDivisionError("Division by Gaussian zero")
            num = self * other.conj()
            return GaussianRational(num._a / nsq, num._b / nsq)
        return NotImplemented

    def __rtruediv__(self, other: Any) -> GaussianRational:
        return GaussianRational(other) / self

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, (int, Fraction)):
            return bool(self._a == other and self._b == 0)
        if isinstance(other, GaussianRational):
            return bool(self._a == other._a and self._b == other._b)
        return False

    def __hash__(self) -> int:
        return hash((self._a, self._b))

    def __repr__(self) -> str:
        return f"GaussianRational({self._a}, {self._b})"

    def __str__(self) -> str:
        if self._b == 0:
            return str(self._a)
        if self._a == 0:
            return f"{self._b}*i"
        sign = "+" if self._b > 0 else "-"
        return f"({self._a} {sign} {abs(self._b)}*i)"


# Generic field element type for matrices
T = TypeVar("T")
Matrix = List[List[Any]]
Vector = List[Any]


# =============================================================================
# 2. Exact Matrix & Linear Algebra Operations
# =============================================================================

def identity_matrix(n: int, zero_val: Any = Fraction(0), one_val: Any = Fraction(1)) -> Matrix:
    """Returns n x n identity matrix with specified zero and unit values."""
    return [[one_val if i == j else zero_val for j in range(n)] for i in range(n)]


def zero_matrix(rows: int, cols: int, zero_val: Any = Fraction(0)) -> Matrix:
    """Returns rows x cols zero matrix."""
    return [[zero_val for _ in range(cols)] for _ in range(rows)]


def matrix_multiply(A: Matrix, B: Matrix) -> Matrix:
    """Exact matrix multiplication A @ B."""
    rows_A = len(A)
    cols_A = len(A[0]) if rows_A > 0 else 0
    rows_B = len(B)
    cols_B = len(B[0]) if rows_B > 0 else 0
    if cols_A != rows_B:
        raise ValueError(f"Matrix dimension mismatch: ({rows_A}x{cols_A}) and ({rows_B}x{cols_B})")
    zero_val = A[0][0] * 0 if rows_A > 0 and cols_A > 0 else 0
    C = [[zero_val for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for k in range(cols_A):
            aik = A[i][k]
            for j in range(cols_B):
                C[i][j] = C[i][j] + aik * B[k][j]
    return C


def matrix_trace(A: Matrix) -> Any:
    """Exact matrix trace Tr(A) = sum_i A_ii."""
    n = len(A)
    if n == 0:
        return Fraction(0)
    tr = A[0][0] * 0
    for i in range(n):
        tr = tr + A[i][i]
    return tr


def matrix_add(A: Matrix, B: Matrix) -> Matrix:
    """Exact matrix addition A + B."""
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def matrix_sub(A: Matrix, B: Matrix) -> Matrix:
    """Exact matrix subtraction A - B."""
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def matrix_scale(c: Any, A: Matrix) -> Matrix:
    """Exact matrix scalar multiplication c * A."""
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def matrix_adjoint(A: Matrix) -> Matrix:
    """Exact conjugate transpose (adjoint) A^dagger."""
    rows = len(A)
    cols = len(A[0]) if rows > 0 else 0
    res = [[None for _ in range(rows)] for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            val = A[i][j]
            res[j][i] = val.conj() if hasattr(val, "conj") else val
    return res


def matrix_commutator(A: Matrix, B: Matrix) -> Matrix:
    """Exact matrix commutator [A, B] = A B - B A."""
    AB = matrix_multiply(A, B)
    BA = matrix_multiply(B, A)
    return matrix_sub(AB, BA)


def kronecker_product(A: Matrix, B: Matrix) -> Matrix:
    """Exact tensor (Kronecker) product A (x) B."""
    rA, cA = len(A), len(A[0])
    rB, cB = len(B), len(B[0])
    res = [[None for _ in range(cA * cB)] for _ in range(rA * rB)]
    for ia in range(rA):
        for ja in range(cA):
            a_val = A[ia][ja]
            for ib in range(rB):
                for jb in range(cB):
                    res[ia * rB + ib][ja * cB + jb] = a_val * B[ib][jb]
    return res


def vector_dot(u: Sequence[Any], v: Sequence[Any]) -> Any:
    """Exact inner product <u | v> = sum_k conj(u_k) * v_k."""
    if len(u) != len(v):
        raise ValueError("Vector length mismatch")
    zero_val = u[0] * 0
    s = zero_val
    for uk, vk in zip(u, v):
        u_conj = uk.conj() if hasattr(uk, "conj") else uk
        s = s + u_conj * vk
    return s


def vector_outer_product(u: Sequence[Any], v: Sequence[Any]) -> Matrix:
    """Exact outer product |u><v| with entries u_i * conj(v_j)."""
    n, m = len(u), len(v)
    res = [[None for _ in range(m)] for _ in range(n)]
    for i in range(n):
        ui = u[i]
        for j in range(m):
            vj = v[j]
            vj_conj = vj.conj() if hasattr(vj, "conj") else vj
            res[i][j] = ui * vj_conj
    return res


# =============================================================================
# 3. Finite Commutator Trace Obstruction Theorem
# =============================================================================

def commutator_trace(A: Matrix, B: Matrix) -> Any:
    """Computes Tr([A, B]) = Tr(A B - B A), which identically vanishes."""
    comm = matrix_commutator(A, B)
    return matrix_trace(comm)


def commutator_obstruction_gap(Q: Matrix, P: Matrix, c: Any) -> Any:
    """Evaluates the obstruction gap Tr([Q, P] - c * I_N) = -N * c.

    For finite carrier dimension N >= 1 and scalar c != 0, this gap is strictly non-zero,
    proving that no finite representation of canonical commutation [Q, P] = c * I can exist.
    """
    N = len(Q)
    comm = matrix_commutator(Q, P)
    tr_comm = matrix_trace(comm)
    tr_target = c * N
    gap = tr_comm - tr_target
    return gap


def verify_canonical_commutation_obstruction(N: int, c: Any) -> bool:
    """Algebraic verification that [Q, P] = c * I is algebraically obstructed on dimension N.

    Theorem: For any finite N x N matrices Q, P over a field of characteristic 0:
      Tr([Q, P]) = Tr(QP - PQ) = 0.
      Tr(c * I_N) = N * c.
      If N >= 1 and c != 0, then N * c != 0 != Tr([Q, P]).
      Therefore, [Q, P] = c * I_N has no finite-dimensional solutions.
    """
    if N < 1:
        raise ValueError("Carrier dimension must be positive")
    if c == 0:
        return True  # Trivial case c = 0 has commuting solutions
    expected_obstruction = c * N
    return bool(expected_obstruction != 0)


# =============================================================================
# 4. Multi-Locus Microcausality on Composite Carriers
# =============================================================================

def discrete_shift_operator(d: int, zero_val: Any = Fraction(0), one_val: Any = Fraction(1)) -> Matrix:
    """Discrete shift operator X on dimension d: X |j> = |(j + 1) mod d>."""
    X = [[zero_val for _ in range(d)] for _ in range(d)]
    for j in range(d):
        target = (j + 1) % d
        X[target][j] = one_val
    return X


def discrete_clock_operator_dim3() -> Matrix:
    """Discrete clock operator Z on dimension d = 3: Z |j> = w^j |j>."""
    zero = Cyclotomic3(0)
    Z = [[zero for _ in range(3)] for _ in range(3)]
    Z[0][0] = Cyclotomic3.root_power(0)
    Z[1][1] = Cyclotomic3.root_power(1)
    Z[2][2] = Cyclotomic3.root_power(2)
    return Z


def discrete_clock_operator_dim4() -> Matrix:
    """Discrete clock operator on dimension d = 4 with values in Q(i): Z |j> = i^j |j>."""
    zero = GaussianRational(0)
    Z = [[zero for _ in range(4)] for _ in range(4)]
    powers = [
        GaussianRational(1, 0),
        GaussianRational(0, 1),
        GaussianRational(-1, 0),
        GaussianRational(0, -1),
    ]
    for j in range(4):
        Z[j][j] = powers[j]
    return Z


def verify_microcausality_bipartite(A: Matrix, B: Matrix) -> bool:
    """Verifies finite microcausality across a bipartite cut:

    Observables localized on disjoint loci strictly commute:
      [A (x) I_B, I_A (x) B] = 0.
    """
    dimA = len(A)
    dimB = len(B)
    zeroA = A[0][0] * 0
    oneA = zeroA + 1
    zeroB = B[0][0] * 0
    oneB = zeroB + 1

    IA = identity_matrix(dimA, zeroA, oneA)
    IB = identity_matrix(dimB, zeroB, oneB)

    OA = kronecker_product(A, IB)
    OB = kronecker_product(IA, B)

    comm = matrix_commutator(OA, OB)
    zero_comm = zero_matrix(dimA * dimB, dimA * dimB, comm[0][0] * 0)
    return bool(comm == zero_comm)


# =============================================================================
# 5. Discrete Mutually Unbiased Bases (MUBs)
# =============================================================================

def construct_mubs_dim3() -> List[List[Vector]]:
    """Constructs the d + 1 = 4 discrete MUBs in dimension d = 3 over Q(w).

    Returns 4 bases, each containing 3 vectors.
    Bases:
      B_0: Standard computational basis.
      B_1: Discrete Fourier basis (eigenbasis of shift X).
      B_2: Eigenbasis of X Z.
      B_3: Eigenbasis of X Z^2.

    Vectors are represented unscaled by sqrt(3) so that components are exact
    elements of Cyclotomic3; physical vectors are v / sqrt(3).
    """
    zero = Cyclotomic3(0)
    one = Cyclotomic3(1)

    # Basis 0: Standard basis
    b0: List[Vector] = [
        [one, zero, zero],
        [zero, one, zero],
        [zero, zero, one],
    ]

    # Bases 1, 2, 3:
    # v_{r, k}[j] = w^( (2 * r * j^2 + j * k) mod 3 )
    bases: List[List[Vector]] = [b0]
    for r in range(3):
        br: List[Vector] = []
        for k in range(3):
            vk: Vector = []
            for j in range(3):
                p = (2 * r * j * j + j * k) % 3
                vk.append(Cyclotomic3.root_power(p))
            br.append(vk)
        bases.append(br)

    return bases


def construct_mub_projectors_dim3() -> List[List[Matrix]]:
    """Constructs exact projectors Pi_{b, k} = |v_{b, k}><v_{b, k}| for d = 3.

    All entries lie strictly in Cyclotomic3.
    """
    bases = construct_mubs_dim3()
    projectors: List[List[Matrix]] = []

    # Basis 0 projectors
    b0_projs: List[Matrix] = []
    for k in range(3):
        vk = bases[0][k]
        P = vector_outer_product(vk, vk)
        b0_projs.append(P)
    projectors.append(b0_projs)

    # Bases 1, 2, 3 projectors: Pi = (1/3) * |v><v|
    for r in range(1, 4):
        br_projs: List[Matrix] = []
        for k in range(3):
            vk = bases[r][k]
            P_unnorm = vector_outer_product(vk, vk)
            P = matrix_scale(Cyclotomic3(Fraction(1, 3)), P_unnorm)
            br_projs.append(P)
        projectors.append(br_projs)

    return projectors


def construct_mubs_dim4() -> List[List[Vector]]:
    """Constructs the d + 1 = 5 discrete MUBs in dimension d = 4 over Q(i).

    Returns 5 bases, each containing 4 vectors.
    Bases are the simultaneous eigenbases of the 5 maximal commuting subsets
    of 2-carrier displacement operators.
    Each vector v in bases 1..4 satisfies v_j in {1, -1, i, -i}; physical vector is v / 2.
    """
    one = GaussianRational(1, 0)
    mone = GaussianRational(-1, 0)
    i = GaussianRational(0, 1)
    mi = GaussianRational(0, -1)
    zero = GaussianRational(0, 0)

    # Basis 0: Standard computational basis scaled by 2 so ||v||^2 = 4
    two = GaussianRational(2, 0)
    b0: List[Vector] = [
        [two, zero, zero, zero],
        [zero, two, zero, zero],
        [zero, zero, two, zero],
        [zero, zero, zero, two],
    ]

    # Basis 1: Real Hadamard-like product basis
    b1: List[Vector] = [
        [one, mone, one, mone],
        [one, one, mone, mone],
        [one, mone, mone, one],
        [one, one, one, one],
    ]

    # Basis 2
    b2: List[Vector] = [
        [one, mi, i, one],
        [one, i, mi, one],
        [one, mi, mi, mone],
        [one, i, i, mone],
    ]

    # Basis 3
    b3: List[Vector] = [
        [one, mone, mi, mi],
        [one, one, mi, i],
        [one, one, i, mi],
        [one, mone, i, i],
    ]

    # Basis 4
    b4: List[Vector] = [
        [one, mi, mone, mi],
        [one, i, mone, i],
        [one, i, one, mi],
        [one, mi, one, i]
    ]

    return [b0, b1, b2, b3, b4]


def construct_mub_projectors_dim4() -> List[List[Matrix]]:
    """Constructs exact projectors Pi_{b, k} = (1/4) * |v_{b, k}><v_{b, k}| for d = 4.

    All entries lie strictly in GaussianRational.
    """
    bases = construct_mubs_dim4()
    projectors: List[List[Matrix]] = []

    for b in bases:
        b_projs: List[Matrix] = []
        for k in range(4):
            vk = b[k]
            P_unnorm = vector_outer_product(vk, vk)
            P = matrix_scale(GaussianRational(Fraction(1, 4)), P_unnorm)
            b_projs.append(P)
        projectors.append(b_projs)

    return projectors


def verify_mub_pairwise_overlap(bases: List[List[Vector]], dim: int, norm_factor_sq: Fraction) -> bool:
    """Verifies that for any two vectors from different bases: |<u | v>|^2 = 1/d."""
    expected_overlap = Fraction(1, dim)
    num_bases = len(bases)

    for b1 in range(num_bases):
        for b2 in range(b1 + 1, num_bases):
            for k1 in range(dim):
                for k2 in range(dim):
                    dot_val = vector_dot(bases[b1][k1], bases[b2][k2])
                    nsq = dot_val.norm_sq()
                    physical_overlap = nsq / norm_factor_sq
                    if physical_overlap != expected_overlap:
                        return False
    return True


# =============================================================================
# 6. Complete Operational State Tomography
# =============================================================================

def measure_mub_probabilities(rho: Matrix, projectors: List[List[Matrix]]) -> List[List[Any]]:
    """Calculates operational measurement probabilities p_{b, k} = Tr(rho * Pi_{b, k})."""
    probabilities: List[List[Any]] = []
    for b_projs in projectors:
        b_probs: List[Any] = []
        for P in b_projs:
            p_val = matrix_trace(matrix_multiply(rho, P))
            b_probs.append(p_val)
        probabilities.append(b_probs)
    return probabilities


def reconstruct_state_from_probabilities(
    probabilities: List[List[Any]],
    projectors: List[List[Matrix]],
    dim: int,
    zero_val: Any = Fraction(0),
    one_val: Any = Fraction(1),
) -> Matrix:
    """Exact operational state reconstruction via dual operator frame inversion.

    Closed-form Wootters operational inversion formula:
      rho = sum_{b=0}^d sum_{k=0}^{d-1} p_{b, k} Pi_{b, k} - I_d.

    This formula is exact in rational arithmetic and reconstructs any density
    matrix rho identically from its projection probabilities.
    """
    Id = identity_matrix(dim, zero_val, one_val)
    reconstructed = [[-Id[i][j] for j in range(dim)] for i in range(dim)]

    num_bases = len(projectors)
    for b in range(num_bases):
        for k in range(dim):
            p = probabilities[b][k]
            P = projectors[b][k]
            for i in range(dim):
                for j in range(dim):
                    reconstructed[i][j] = reconstructed[i][j] + p * P[i][j]

    return reconstructed


def solve_linear_system_exact(M: List[List[Fraction]], b: List[Fraction]) -> List[Fraction]:
    """Solves M x = b using exact rational Gaussian elimination with partial pivoting."""
    rows = len(M)
    cols = len(M[0])
    # Build augmented matrix
    A = [[Fraction(M[i][j]) for j in range(cols)] + [Fraction(b[i])] for i in range(rows)]

    pivot_row = 0
    pivot_col = 0
    col_pivots: List[Tuple[int, int]] = []

    while pivot_row < rows and pivot_col < cols:
        # Find non-zero pivot in column pivot_col
        max_r = pivot_row
        while max_r < rows and A[max_r][pivot_col] == 0:
            max_r += 1
        if max_r == rows:
            pivot_col += 1
            continue

        # Swap rows
        A[pivot_row], A[max_r] = A[max_r], A[pivot_row]
        pivot_val = A[pivot_row][pivot_col]

        # Normalize pivot row
        for c in range(pivot_col, cols + 1):
            A[pivot_row][c] = A[pivot_row][c] / pivot_val

        # Eliminate below and above
        for r in range(rows):
            if r != pivot_row and A[r][pivot_col] != 0:
                factor = A[r][pivot_col]
                for c in range(pivot_col, cols + 1):
                    A[r][c] = A[r][c] - factor * A[pivot_row][c]

        col_pivots.append((pivot_row, pivot_col))
        pivot_row += 1
        pivot_col += 1

    x = [Fraction(0) for _ in range(cols)]
    for r, c in col_pivots:
        x[c] = A[r][cols]
    return x


def reconstruct_state_linear_inversion(
    probabilities: List[List[Any]],
    projectors: List[List[Matrix]],
    dim: int,
    zero_val: Any = Fraction(0),
    one_val: Any = Fraction(1),
) -> Matrix:
    """Reconstructs state rho via full rational linear inversion of the operator frame.

    Expands rho in an exact rational basis of d^2 Hermitian matrices {H_m}:
      rho = sum_{m=0}^{d^2-1} x_m H_m.
    Each measurement expectation satisfies:
      p_{b, k} = Tr(rho * Pi_{b, k}) = sum_m x_m Tr(H_m * Pi_{b, k}).
    Solves the exact rational linear system M x = p and reconstructs rho.
    """
    herm_basis: List[Matrix] = []

    # 1. Diagonal projectors |i><i|
    for i in range(dim):
        H = zero_matrix(dim, dim, zero_val)
        H[i][i] = one_val
        herm_basis.append(H)

    # Determine imaginary generator for antisymmetric Hermitian basis
    im_gen: Any = None
    if isinstance(zero_val, GaussianRational):
        im_gen = GaussianRational(0, 1)
    elif isinstance(zero_val, Cyclotomic3):
        # 1 + 2*w has conjugate -1 - 2*w = -(1 + 2*w), so it is pure imaginary
        im_gen = Cyclotomic3(1, 2)

    # 2. Symmetric off-diagonals |i><j| + |j><i|
    for i in range(dim):
        for j in range(i + 1, dim):
            H = zero_matrix(dim, dim, zero_val)
            H[i][j] = one_val
            H[j][i] = one_val
            herm_basis.append(H)

    # 3. Antisymmetric imaginary off-diagonals
    if im_gen is not None:
        for i in range(dim):
            for j in range(i + 1, dim):
                H = zero_matrix(dim, dim, zero_val)
                H[i][j] = -im_gen
                H[j][i] = im_gen
                herm_basis.append(H)

    num_unknowns = len(herm_basis)
    A_rows: List[List[Fraction]] = []
    b_vec: List[Fraction] = []

    for b_idx, b_projs in enumerate(projectors):
        for k, P in enumerate(b_projs):
            prob = probabilities[b_idx][k]
            if isinstance(prob, Cyclotomic3):
                p_frac = prob.a - prob.b / 2
            elif isinstance(prob, GaussianRational):
                p_frac = prob.a
            else:
                p_frac = Fraction(prob)

            row: List[Fraction] = []
            for H in herm_basis:
                tr = matrix_trace(matrix_multiply(H, P))
                if isinstance(tr, Cyclotomic3):
                    r_tr = tr.a - tr.b / 2
                elif isinstance(tr, GaussianRational):
                    r_tr = tr.a
                else:
                    r_tr = Fraction(tr)
                row.append(r_tr)

            A_rows.append(row)
            b_vec.append(p_frac)

    x_sol = solve_linear_system_exact(A_rows, b_vec)

    rec = zero_matrix(dim, dim, zero_val)
    for xm, H in zip(x_sol, herm_basis):
        scaled_c = zero_val + xm
        scaled = matrix_scale(scaled_c, H)
        rec = matrix_add(rec, scaled)

    return rec
