"""Discrete Wigner Phase_Spaces on Odd_Prime Dimensions.

AuthorityEffect: None.

Implements Target P209a:
1. Exact cyclotomic and rational arithmetic over Q(zeta_p) for odd_prime dimensions p in {3, 5}.
2. Parity reflection operator P: P |j> = |-j mod p> with P^2 = I and Tr(P) = 1.
3. Discrete Weyl displacement operators D(q, p) and Gross phase_point operators A(q, p).
4. Completeness sum_{q, p} A(q, p) = p * I_p and orthogonality Tr(A(q, p) A(q', p')) = p * delta_{q q'} delta_{p p'}.
5. Discrete Wigner distribution W_rho(q, p) = (1/p) * Tr(rho A(q, p)).
6. Stabilizer state non-negativity: W_{|0>}(q, p) >= 0 and W_{|+>}(q, p) >= 0 everywhere.
7. Magic state point negativity witness: W_{|M>}(0, 0) = -1/p < 0.
8. Gross phase_space covariance: P X P = X^{-1} and P Z P = Z^{-1}.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict, List, Sequence, Tuple, Union


def _exact_q(val: object) -> Fraction:
    """Convert int/Fraction to Q. Refuse float stand-ins for claimed exact rationals."""
    if isinstance(val, float):
        raise TypeError("float is not exact Q; pass Fraction or int")
    if isinstance(val, Fraction):
        return val
    if isinstance(val, int):
        return Fraction(val, 1)
    raise TypeError(f"Unsupported exact-Q conversion: {type(val)}")


# =============================================================================
# 1. Exact Cyclotomic Arithmetic over Q(zeta_p)
# =============================================================================

class CyclotomicPrime:
    """Exact element of the cyclotomic number field Q(w_p) for odd_prime dimension p.

    The minimal polynomial for primitive root w_p is:
        Phi_p(x) = 1 + x + x^2 + ... + x^{p-1} = 0.
    The basis over Q is {1, w_p, w_p^2, ..., w_p^{p-2}}.
    An element is stored as a tuple of p - 1 Fractions (c_0, c_1, ..., c_{p-2}).
    """

    __slots__ = ("_p", "_coeffs")
    _p: int
    _coeffs: Tuple[Fraction, ...]

    def __init__(self, p: int, coeffs: Sequence[Union[int, Fraction]]) -> None:
        if p not in (3, 5):
            raise ValueError(f"Supported odd_prime dimensions are 3 and 5, received {p}")
        if len(coeffs) != p - 1:
            raise ValueError(f"Expected {p - 1} coefficients for dimension {p}, got {len(coeffs)}")
        self._p = p
        self._coeffs = tuple(_exact_q(c) for c in coeffs)

    @property
    def p(self) -> int:
        return self._p

    @property
    def coeffs(self) -> Tuple[Fraction, ...]:
        return self._coeffs

    @classmethod
    def from_rational(cls, p: int, val: Union[int, Fraction]) -> CyclotomicPrime:
        f = _exact_q(val)
        return cls(p, (f,) + (Fraction(0),) * (p - 2))

    @classmethod
    def root_unity(cls, p: int, power: int = 1) -> CyclotomicPrime:
        """Return w_p^power in exact representation."""
        pow_mod = power % p
        if pow_mod == 0:
            return cls.from_rational(p, 1)
        if pow_mod < p - 1:
            c = [Fraction(0)] * (p - 1)
            c[pow_mod] = Fraction(1)
            return cls(p, tuple(c))
        # pow_mod == p - 1: w^(p-1) = -1 - w - ... - w^(p-2)
        return cls(p, tuple(Fraction(-1) for _ in range(p - 1)))

    def is_rational(self) -> bool:
        """Return True if all non-constant cyclotomic coefficients vanish."""
        return all(c == 0 for c in self._coeffs[1:])

    def to_rational(self) -> Fraction:
        """Extract rational value if element lies in Q, otherwise raise ValueError."""
        if not self.is_rational():
            raise ValueError(f"Element {self} is not purely rational")
        return self._coeffs[0]

    def is_real(self) -> bool:
        """Return True if element is invariant under complex conjugation."""
        return self == self.conj()

    def conj(self) -> CyclotomicPrime:
        """Complex conjugate: maps w_p^k to w_p^{-k}."""
        p = self._p
        res_powers = [Fraction(0)] * p
        for j, c in enumerate(self._coeffs):
            if c == 0:
                continue
            k = (-j) % p
            res_powers[k] += c
        high = res_powers[p - 1]
        final_coeffs = tuple(res_powers[k] - high for k in range(p - 1))
        return CyclotomicPrime(p, final_coeffs)

    def norm_sq(self) -> CyclotomicPrime:
        """Return squared modulus: self * self.conj()."""
        return self * self.conj()

    def __neg__(self) -> CyclotomicPrime:
        return CyclotomicPrime(self._p, tuple(-c for c in self._coeffs))

    def __add__(self, other: Any) -> CyclotomicPrime:
        if isinstance(other, (int, Fraction)):
            other = CyclotomicPrime.from_rational(self._p, other)
        if isinstance(other, CyclotomicPrime):
            if self._p != other._p:
                raise ValueError("Cannot add elements of different dimensions")
            return CyclotomicPrime(
                self._p, tuple(a + b for a, b in zip(self._coeffs, other._coeffs))
            )
        return NotImplemented

    def __radd__(self, other: Any) -> CyclotomicPrime:
        return self.__add__(other)

    def __sub__(self, other: Any) -> CyclotomicPrime:
        if isinstance(other, (int, Fraction)):
            other = CyclotomicPrime.from_rational(self._p, other)
        if isinstance(other, CyclotomicPrime):
            if self._p != other._p:
                raise ValueError("Cannot subtract elements of different dimensions")
            return CyclotomicPrime(
                self._p, tuple(a - b for a, b in zip(self._coeffs, other._coeffs))
            )
        return NotImplemented

    def __rsub__(self, other: Any) -> CyclotomicPrime:
        return (-self).__add__(other)

    def __mul__(self, other: Any) -> CyclotomicPrime:
        if isinstance(other, (int, Fraction)):
            f = Fraction(other)
            return CyclotomicPrime(self._p, tuple(c * f for c in self._coeffs))
        if isinstance(other, CyclotomicPrime):
            if self._p != other._p:
                raise ValueError("Cannot multiply elements of different dimensions")
            p = self._p
            res_powers = [Fraction(0)] * p
            for i, ci in enumerate(self._coeffs):
                if ci == 0:
                    continue
                for j, cj in enumerate(other._coeffs):
                    if cj == 0:
                        continue
                    k = (i + j) % p
                    res_powers[k] += ci * cj
            high = res_powers[p - 1]
            final_coeffs = tuple(res_powers[k] - high for k in range(p - 1))
            return CyclotomicPrime(p, final_coeffs)
        return NotImplemented

    def __rmul__(self, other: Any) -> CyclotomicPrime:
        return self.__mul__(other)

    def inv(self) -> CyclotomicPrime:
        """Compute multiplicative inverse using exact rational linear elimination."""
        p = self._p
        if all(c == 0 for c in self._coeffs):
            raise ZeroDivisionError("Multiplicative inverse of zero")
        n = p - 1
        cols: List[List[Fraction]] = []
        for j in range(n):
            ej = [Fraction(0)] * n
            ej[j] = Fraction(1)
            res = [Fraction(0)] * p
            for i, ci in enumerate(self._coeffs):
                k = (i + j) % p
                res[k] += ci
            high = res[p - 1]
            cols.append([res[k] - high for k in range(n)])

        mat = [[cols[j][i] for j in range(n)] for i in range(n)]
        rhs = [Fraction(1) if i == 0 else Fraction(0) for i in range(n)]

        for i in range(n):
            pivot = i
            while pivot < n and mat[pivot][i] == 0:
                pivot += 1
            if pivot == n:
                raise ZeroDivisionError("Singular element in field inversion")
            mat[i], mat[pivot] = mat[pivot], mat[i]
            rhs[i], rhs[pivot] = rhs[pivot], rhs[i]
            scale = mat[i][i]
            mat[i] = [val / scale for val in mat[i]]
            rhs[i] = rhs[i] / scale
            for r in range(n):
                if r != i and mat[r][i] != 0:
                    factor = mat[r][i]
                    mat[r] = [mat[r][c_idx] - factor * mat[i][c_idx] for c_idx in range(n)]
                    rhs[r] = rhs[r] - factor * rhs[i]
        return CyclotomicPrime(p, tuple(rhs))

    def __truediv__(self, other: Any) -> CyclotomicPrime:
        if isinstance(other, (int, Fraction)):
            f = Fraction(other)
            return self * (Fraction(1) / f)
        if isinstance(other, CyclotomicPrime):
            return self * other.inv()
        return NotImplemented

    def __rtruediv__(self, other: Any) -> CyclotomicPrime:
        return CyclotomicPrime.from_rational(self._p, other) * self.inv()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, (int, Fraction)):
            other = CyclotomicPrime.from_rational(self._p, other)
        if not isinstance(other, CyclotomicPrime):
            return False
        return self._p == other._p and self._coeffs == other._coeffs

    def __repr__(self) -> str:
        if self.is_rational():
            return f"Q_{self._p}({self._coeffs[0]})"
        terms = [f"{c}*w^{i}" if i > 0 else f"{c}" for i, c in enumerate(self._coeffs) if c != 0]
        return f"Q_{self._p}(" + (" + ".join(terms) if terms else "0") + ")"


# =============================================================================
# 2. Exact Matrix Algebra over Cyclotomic Fields
# =============================================================================

class ExactMatrix:
    """Exact matrix of elements in Q(zeta_p)."""

    __slots__ = ("_p", "_dim", "_data")
    _p: int
    _dim: int
    _data: List[List[CyclotomicPrime]]

    def __init__(self, p: int, data: Sequence[Sequence[Any]]) -> None:
        self._p = p
        self._dim = len(data)
        converted: List[List[CyclotomicPrime]] = []
        for row in data:
            if len(row) != self._dim:
                raise ValueError("Matrix must be square")
            converted_row: List[CyclotomicPrime] = []
            for item in row:
                if isinstance(item, CyclotomicPrime):
                    if item.p != p:
                        raise ValueError(f"Cyclotomic element dimension mismatch: {item.p} vs {p}")
                    converted_row.append(item)
                else:
                    converted_row.append(CyclotomicPrime.from_rational(p, item))
            converted.append(converted_row)
        self._data = converted

    @property
    def p(self) -> int:
        return self._p

    @property
    def dim(self) -> int:
        return self._dim

    def __getitem__(self, idx: Tuple[int, int]) -> CyclotomicPrime:
        r, c = idx
        return self._data[r][c]

    @classmethod
    def eye(cls, p: int, dim: int) -> ExactMatrix:
        rows = [[1 if i == j else 0 for j in range(dim)] for i in range(dim)]
        return cls(p, rows)

    @classmethod
    def zeros(cls, p: int, dim: int) -> ExactMatrix:
        rows = [[0 for _ in range(dim)] for _ in range(dim)]
        return cls(p, rows)

    def trace(self) -> CyclotomicPrime:
        tr = CyclotomicPrime.from_rational(self._p, 0)
        for i in range(self._dim):
            tr = tr + self._data[i][i]
        return tr

    def dag(self) -> ExactMatrix:
        """Conjugate transpose."""
        new_data = [
            [self._data[j][i].conj() for j in range(self._dim)]
            for i in range(self._dim)
        ]
        return ExactMatrix(self._p, new_data)

    def __add__(self, other: ExactMatrix) -> ExactMatrix:
        if self._dim != other._dim or self._p != other._p:
            raise ValueError("Dimension mismatch in matrix addition")
        new_data = [
            [self._data[i][j] + other._data[i][j] for j in range(self._dim)]
            for i in range(self._dim)
        ]
        return ExactMatrix(self._p, new_data)

    def __sub__(self, other: ExactMatrix) -> ExactMatrix:
        if self._dim != other._dim or self._p != other._p:
            raise ValueError("Dimension mismatch in matrix subtraction")
        new_data = [
            [self._data[i][j] - other._data[i][j] for j in range(self._dim)]
            for i in range(self._dim)
        ]
        return ExactMatrix(self._p, new_data)

    def __mul__(self, scalar: Any) -> ExactMatrix:
        new_data = [
            [self._data[i][j] * scalar for j in range(self._dim)]
            for i in range(self._dim)
        ]
        return ExactMatrix(self._p, new_data)

    def __rmul__(self, scalar: Any) -> ExactMatrix:
        return self.__mul__(scalar)

    def __matmul__(self, other: ExactMatrix) -> ExactMatrix:
        if self._dim != other._dim or self._p != other._p:
            raise ValueError("Dimension mismatch in matrix multiplication")
        d = self._dim
        p = self._p
        new_data: List[List[CyclotomicPrime]] = []
        for i in range(d):
            row: List[CyclotomicPrime] = []
            for j in range(d):
                s = CyclotomicPrime.from_rational(p, 0)
                for k in range(d):
                    s = s + self._data[i][k] * other._data[k][j]
                row.append(s)
            new_data.append(row)
        return ExactMatrix(p, new_data)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ExactMatrix):
            return False
        if self._p != other._p or self._dim != other._dim:
            return False
        for i in range(self._dim):
            for j in range(self._dim):
                if self._data[i][j] != other._data[i][j]:
                    return False
        return True


# =============================================================================
# 3. Discrete Phase_Space Operators on Odd_Prime Dimensions
# =============================================================================

def discrete_shift(p: int) -> ExactMatrix:
    """Translation shift operator X on dimension p: X |j> = |j+1 mod p>."""
    rows = [[1 if i == (j + 1) % p else 0 for j in range(p)] for i in range(p)]
    return ExactMatrix(p, rows)


def discrete_clock(p: int) -> ExactMatrix:
    """Clock operator Z on dimension p: Z |j> = w_p^j |j>."""
    rows: List[List[Any]] = []
    for i in range(p):
        row: List[Any] = []
        for j in range(p):
            if i == j:
                row.append(CyclotomicPrime.root_unity(p, i))
            else:
                row.append(0)
        rows.append(row)
    return ExactMatrix(p, rows)


def parity_operator(p: int) -> ExactMatrix:
    """Parity reflection operator P: P |j> = |-j mod p>."""
    rows = [[1 if (i + j) % p == 0 else 0 for j in range(p)] for i in range(p)]
    return ExactMatrix(p, rows)


def matrix_power(M: ExactMatrix, k: int) -> ExactMatrix:
    """Compute non-negative integer power of square matrix."""
    if k == 0:
        return ExactMatrix.eye(M.p, M.dim)
    res = ExactMatrix.eye(M.p, M.dim)
    curr = M
    pow_k = k
    while pow_k > 0:
        if pow_k % 2 == 1:
            res = res @ curr
        curr = curr @ curr
        pow_k //= 2
    return res


def displacement_operator(p: int, q: int, p_coord: int) -> ExactMatrix:
    """Discrete Weyl displacement operator D(q, p) on F_p x F_p.

    D(q, p) = w_p^{2^{-1} * q * p} * X^q * Z^p,
    where 2^{-1} = (p + 1) // 2 mod p.
    """
    q_mod = q % p
    p_mod = p_coord % p
    inv2 = (p + 1) // 2
    phase_pow = (inv2 * q_mod * p_mod) % p
    phase_factor = CyclotomicPrime.root_unity(p, phase_pow)

    X = discrete_shift(p)
    Z = discrete_clock(p)
    Xq = matrix_power(X, q_mod)
    Zp = matrix_power(Z, p_mod)
    return (Xq @ Zp) * phase_factor


def phase_point_operator(p: int, q: int, p_coord: int) -> ExactMatrix:
    """Gross phase_point operator A(q, p) = D(q, p) * P * D(q, p)^dagger."""
    D = displacement_operator(p, q, p_coord)
    P = parity_operator(p)
    return D @ P @ D.dag()


# =============================================================================
# 4. State Carriers, Wigner Distributions & Reconstruction
# =============================================================================

def ket_zero_density(p: int) -> ExactMatrix:
    """Density operator for stabilizer state |0>."""
    rows = [[1 if i == 0 and j == 0 else 0 for j in range(p)] for i in range(p)]
    return ExactMatrix(p, rows)


def ket_plus_density(p: int) -> ExactMatrix:
    """Density operator for stabilizer state |+> = (1/sqrt(p)) sum_j |j>."""
    val = Fraction(1, p)
    rows = [[val for _ in range(p)] for _ in range(p)]
    return ExactMatrix(p, rows)


def ket_magic_density(p: int) -> ExactMatrix:
    """Density operator for magic state |M> = (1/sqrt(2))(|1> - |p-1>)."""
    # Vector: entry 1 is 1/sqrt(2), entry p-1 is -1/sqrt(2)
    # Density matrix entries:
    # (1, 1): 1/2, (1, p-1): -1/2, (p-1, 1): -1/2, (p-1, p-1): 1/2
    half = Fraction(1, 2)
    rows: List[List[Any]] = [[0 for _ in range(p)] for _ in range(p)]
    rows[1][1] = half
    rows[1][p - 1] = -half
    rows[p - 1][1] = -half
    rows[p - 1][p - 1] = half
    return ExactMatrix(p, rows)


def discrete_wigner_point(p: int, rho: ExactMatrix, q: int, p_coord: int) -> CyclotomicPrime:
    """Evaluate discrete Wigner distribution point W_rho(q, p) = (1/p) * Tr(rho * A(q, p))."""
    A = phase_point_operator(p, q, p_coord)
    tr = (rho @ A).trace()
    return tr / Fraction(p, 1)


def discrete_wigner_distribution(p: int, rho: ExactMatrix) -> Dict[Tuple[int, int], CyclotomicPrime]:
    """Compute discrete Wigner distribution across all p^2 phase_space points in F_p x F_p."""
    wigner: Dict[Tuple[int, int], CyclotomicPrime] = {}
    for q in range(p):
        for p_coord in range(p):
            wigner[(q, p_coord)] = discrete_wigner_point(p, rho, q, p_coord)
    return wigner


def reconstruct_state(p: int, wigner: Dict[Tuple[int, int], CyclotomicPrime]) -> ExactMatrix:
    """Exact state reconstruction: rho = sum_{q, p} W(q, p) * A(q, p)."""
    rho = ExactMatrix.zeros(p, p)
    for (q, p_coord), w_val in wigner.items():
        A = phase_point_operator(p, q, p_coord)
        rho = rho + (A * w_val)
    return rho


# =============================================================================
# 5. High-Level Algebraic Invariant Checkers
# =============================================================================

def verify_parity_involution(p: int) -> bool:
    """Verify P^2 = I and Tr(P) = 1."""
    P = parity_operator(p)
    P_sq = P @ P
    eye = ExactMatrix.eye(p, p)
    return (P_sq == eye) and (P.trace() == CyclotomicPrime.from_rational(p, 1))


def verify_gross_covariance(p: int) -> bool:
    """Verify Gross phase_space covariance: P X P = X^{-1} and P Z P = Z^{-1}."""
    P = parity_operator(p)
    X = discrete_shift(p)
    Z = discrete_clock(p)
    X_inv = matrix_power(X, p - 1)
    Z_inv = matrix_power(Z, p - 1)
    cond_x = (P @ X @ P) == X_inv
    cond_z = (P @ Z @ P) == Z_inv
    return cond_x and cond_z


def verify_completeness(p: int) -> bool:
    """Verify completeness: sum_{q, p} A(q, p) = p * I_p."""
    sum_A = ExactMatrix.zeros(p, p)
    for q in range(p):
        for p_coord in range(p):
            sum_A = sum_A + phase_point_operator(p, q, p_coord)
    expected = ExactMatrix.eye(p, p) * Fraction(p, 1)
    return sum_A == expected


def trace_prod(A: ExactMatrix, B: ExactMatrix) -> CyclotomicPrime:
    """Compute Tr(A * B) efficiently using sum_{i, j} A[i, j] * B[j, i]."""
    p = A.p
    d = A.dim
    tr = CyclotomicPrime.from_rational(p, 0)
    for i in range(d):
        for j in range(d):
            tr = tr + A[i, j] * B[j, i]
    return tr


def verify_orthogonality(p: int) -> bool:
    """Verify orthogonality: Tr(A(q, p) A(q', p')) = p * delta_{q q'} delta_{p p'}."""
    ops = {
        (q, p_coord): phase_point_operator(p, q, p_coord)
        for q in range(p)
        for p_coord in range(p)
    }
    for q in range(p):
        for p_coord in range(p):
            A1 = ops[(q, p_coord)]
            for q2 in range(p):
                for p2 in range(p):
                    A2 = ops[(q2, p2)]
                    tr = trace_prod(A1, A2)
                    expected_val = p if (q == q2 and p_coord == p2) else 0
                    if tr != CyclotomicPrime.from_rational(p, expected_val):
                        return False
    return True

