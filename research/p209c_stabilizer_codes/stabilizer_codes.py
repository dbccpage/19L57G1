"""Exact Integer and Pauli String Stabilizer Error-Correcting Codes.

AuthorityEffect: None.

Implements Genesis Target P209c:
1. Exact integer and Pauli string arithmetic (I, X, Y, Z) and Kronecker tensor
   products over discrete state carriers.
2. 3-carrier bit-flip code [[3, 1, 1]]:
   - Stabilizers S1 = ZZI, S2 = IZZ.
   - Logical operators Z_L = ZZZ, X_L = XXX.
   - 4 distinct syndrome patterns detecting single-carrier bit-flips.
3. 4-carrier CSS code [[4, 2, 2]] on a discrete 2-torus:
   - Stabilizers S_Z = ZZZZ, S_X = XXXX.
   - Two independent logical carrier pairs:
     (Z_L1 = ZZII, X_L1 = XIXI) and (Z_L2 = ZIZI, X_L2 = XXII).
   - Distance-2 detection across all 12 single-carrier Pauli errors.
4. Steane [[7, 1, 3]] CSS code on the Fano plane PG(2, 2):
   - 6 generators derived from 3 dual Fano lines of weight 4.
   - Even pairwise intersections (|h_i cap h_j| = 2 = 0 mod 2) ensuring commutativity.
   - Logical operators X_L = X^{tensor 7}, Z_L = Z^{tensor 7}.
   - Transversal Hadamard H^{tensor 7} implementing logical H_L.
   - Deterministic diagnosis and correction of all 21 single-carrier Pauli errors.
5. Stabilizer projection operator:
   - Pi_S = (1 / |S|) sum_{M in S} M with exact idempotence Pi_S^2 = Pi_S.
"""

from __future__ import annotations

from enum import Enum
from fractions import Fraction
import itertools
from typing import Any, List, Sequence, Tuple


# =============================================================================
# 1. Exact Gaussian Rational Arithmetic (for scalars +/- 1, +/- i)
# =============================================================================


class GaussianRational:
    """Exact Gaussian rational element a + b*i where i^2 = -1, with a, b in Q."""

    __slots__ = ("_a", "_b")
    _a: Fraction
    _b: Fraction

    def __init__(
        self, a: int | Fraction | GaussianRational = 0, b: int | Fraction = 0
    ) -> None:
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

    def __repr__(self) -> str:
        if self._b == 0:
            return f"{self._a}"
        if self._a == 0:
            return f"{self._b}*i"
        sign = "+" if self._b > 0 else "-"
        return f"({self._a} {sign} {abs(self._b)}*i)"

    @classmethod
    def zero(cls) -> GaussianRational:
        return cls(0, 0)

    @classmethod
    def one(cls) -> GaussianRational:
        return cls(1, 0)

    @classmethod
    def i_unit(cls) -> GaussianRational:
        return cls(0, 1)

    @classmethod
    def from_phase_power(cls, k: int) -> GaussianRational:
        """Returns i^k for integer k."""
        rem = k % 4
        if rem == 0:
            return cls(1, 0)
        if rem == 1:
            return cls(0, 1)
        if rem == 2:
            return cls(-1, 0)
        return cls(0, -1)


# =============================================================================
# 2. Exact Matrix & Kronecker Tensor Operations
# =============================================================================

IntMatrix = List[List[int]]
Matrix = List[List[GaussianRational]]


def int_identity_matrix(n: int) -> IntMatrix:
    """Returns n x n exact integer identity matrix."""
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def int_zero_matrix(rows: int, cols: int) -> IntMatrix:
    """Returns rows x cols exact integer zero matrix."""
    return [[0 for _ in range(cols)] for _ in range(rows)]


def int_matrix_multiply(A: IntMatrix, B: IntMatrix) -> IntMatrix:
    """Exact integer matrix multiplication A @ B."""
    rA = len(A)
    cA = len(A[0]) if rA > 0 else 0
    rB = len(B)
    cB = len(B[0]) if rB > 0 else 0
    if cA != rB:
        raise ValueError(f"Matrix dimension mismatch: ({rA}x{cA}) and ({rB}x{cB})")
    C = [[0 for _ in range(cB)] for _ in range(rA)]
    for i in range(rA):
        for k in range(cA):
            aik = A[i][k]
            if aik == 0:
                continue
            for j in range(cB):
                bkj = B[k][j]
                if bkj != 0:
                    C[i][j] += aik * bkj
    return C


def int_matrix_add(A: IntMatrix, B: IntMatrix) -> IntMatrix:
    """Exact integer matrix addition A + B."""
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def int_matrix_scale(c: int, A: IntMatrix) -> IntMatrix:
    """Exact integer matrix scalar multiplication c * A."""
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def int_matrix_trace(A: IntMatrix) -> int:
    """Exact integer matrix trace Tr(A)."""
    return int(sum(A[i][i] for i in range(len(A))))


def int_kronecker_product(A: IntMatrix, B: IntMatrix) -> IntMatrix:
    """Exact integer Kronecker tensor product A (x) B."""
    rA, cA = len(A), len(A[0])
    rB, cB = len(B), len(B[0])
    res = [[0 for _ in range(cA * cB)] for _ in range(rA * rB)]
    for ia in range(rA):
        for ja in range(cA):
            a_val = A[ia][ja]
            if a_val == 0:
                continue
            for ib in range(rB):
                for jb in range(cB):
                    res[ia * rB + ib][ja * cB + jb] = a_val * B[ib][jb]
    return res


# Single-carrier integer 2x2 Pauli matrices (for I, X, Z)
INT_PAULI_2X2: dict[str, IntMatrix] = {
    "I": [[1, 0], [0, 1]],
    "X": [[0, 1], [1, 0]],
    "Z": [[1, 0], [0, -1]],
}

# Single-carrier GaussianRational 2x2 Pauli matrices (for I, X, Y, Z)
PAULI_MATRICES_2X2: dict[str, Matrix] = {
    "I": [
        [GaussianRational(1, 0), GaussianRational(0, 0)],
        [GaussianRational(0, 0), GaussianRational(1, 0)],
    ],
    "X": [
        [GaussianRational(0, 0), GaussianRational(1, 0)],
        [GaussianRational(1, 0), GaussianRational(0, 0)],
    ],
    "Y": [
        [GaussianRational(0, 0), GaussianRational(0, -1)],
        [GaussianRational(0, 1), GaussianRational(0, 0)],
    ],
    "Z": [
        [GaussianRational(1, 0), GaussianRational(0, 0)],
        [GaussianRational(0, 0), GaussianRational(-1, 0)],
    ],
}


def matrix_multiply(A: Matrix, B: Matrix) -> Matrix:
    """Exact Gaussian rational matrix multiplication A @ B."""
    rA, cA = len(A), len(A[0])
    rB, cB = len(B), len(B[0])
    if cA != rB:
        raise ValueError("Matrix dimension mismatch")
    C = [[GaussianRational.zero() for _ in range(cB)] for _ in range(rA)]
    for i in range(rA):
        for k in range(cA):
            aik = A[i][k]
            if aik == 0:
                continue
            for j in range(cB):
                bkj = B[k][j]
                if bkj != 0:
                    C[i][j] = C[i][j] + aik * bkj
    return C


def int_matrix_commutator(A: IntMatrix, B: IntMatrix) -> IntMatrix:
    """Exact integer matrix commutator [A, B] = A @ B - B @ A."""
    AB = int_matrix_multiply(A, B)
    BA = int_matrix_multiply(B, A)
    return [[AB[i][j] - BA[i][j] for j in range(len(AB[0]))] for i in range(len(AB))]


def matrix_commutator(A: Matrix, B: Matrix) -> Matrix:
    """Exact Gaussian rational matrix commutator [A, B] = A @ B - B @ A."""
    AB = matrix_multiply(A, B)
    BA = matrix_multiply(B, A)
    return [[AB[i][j] - BA[i][j] for j in range(len(AB[0]))] for i in range(len(AB))]


def kronecker_product(A: Matrix, B: Matrix) -> Matrix:
    """Exact Gaussian rational Kronecker tensor product A (x) B."""
    rA, cA = len(A), len(A[0])
    rB, cB = len(B), len(B[0])
    res = [
        [GaussianRational.zero() for _ in range(cA * cB)]
        for _ in range(rA * rB)
    ]
    for ia in range(rA):
        for ja in range(cA):
            a_val = A[ia][ja]
            if a_val == 0:
                continue
            for ib in range(rB):
                for jb in range(cB):
                    res[ia * rB + ib][ja * cB + jb] = a_val * B[ib][jb]
    return res


# =============================================================================
# 3. Exact Pauli String Algebra & Symplectic Carrier Representation
# =============================================================================


class Pauli(Enum):
    """Single-carrier Pauli operator."""

    I = "I"
    X = "X"
    Y = "Y"
    Z = "Z"


# Multiplications for single Paulis: (result_symbol, phase_power_k) where result = i^k * symbol
SINGLE_PAULI_MUL: dict[tuple[str, str], tuple[str, int]] = {
    ("I", "I"): ("I", 0),
    ("I", "X"): ("X", 0),
    ("I", "Y"): ("Y", 0),
    ("I", "Z"): ("Z", 0),
    ("X", "I"): ("X", 0),
    ("X", "X"): ("I", 0),
    ("X", "Y"): ("Z", 1),
    ("X", "Z"): ("Y", 3),
    ("Y", "I"): ("Y", 0),
    ("Y", "X"): ("Z", 3),
    ("Y", "Y"): ("I", 0),
    ("Y", "Z"): ("X", 1),
    ("Z", "I"): ("Z", 0),
    ("Z", "X"): ("Y", 1),
    ("Z", "Y"): ("X", 3),
    ("Z", "Z"): ("I", 0),
}


class PauliString:
    """Exact multi-carrier Pauli string operator: (i^phase_power) * (P_1 x ... x P_n).

    phase_power is an integer mod 4, corresponding to factor i^{phase_power} in {1, i, -1, -i}.
    """

    __slots__ = ("_symbols", "_phase_power", "_n")
    _symbols: tuple[str, ...]
    _phase_power: int
    _n: int

    def __init__(
        self,
        symbols: str | Sequence[str | Pauli],
        phase_power: int = 0,
    ) -> None:
        if isinstance(symbols, str):
            sym_list = tuple(s.upper() for s in symbols)
        else:
            sym_list = tuple(
                s.value if isinstance(s, Pauli) else str(s).upper()
                for s in symbols
            )
        for s in sym_list:
            if s not in ("I", "X", "Y", "Z"):
                raise ValueError(f"Invalid Pauli symbol: {s}")
        self._symbols = sym_list
        self._phase_power = phase_power % 4
        self._n = len(sym_list)

    @property
    def symbols(self) -> tuple[str, ...]:
        return self._symbols

    @property
    def phase_power(self) -> int:
        return self._phase_power

    @property
    def n_carriers(self) -> int:
        return self._n

    def __len__(self) -> int:
        return self._n

    @property
    def weight(self) -> int:
        """Weight of the operator: count of non-identity carrier positions."""
        return sum(1 for s in self._symbols if s != "I")

    def is_real_pauli(self) -> bool:
        """True if the string contains only I, X, Z and phase_power in {0, 2}."""
        return all(s in ("I", "X", "Z") for s in self._symbols) and (
            self._phase_power % 2 == 0
        )

    def __repr__(self) -> str:
        base = "".join(self._symbols)
        if self._phase_power == 0:
            return f"+{base}"
        if self._phase_power == 1:
            return f"+i{base}"
        if self._phase_power == 2:
            return f"-{base}"
        return f"-i{base}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PauliString):
            return False
        return (
            self._symbols == other._symbols
            and self._phase_power == other._phase_power
        )

    def __hash__(self) -> int:
        return hash((self._symbols, self._phase_power))

    def __neg__(self) -> PauliString:
        return PauliString(self._symbols, (self._phase_power + 2) % 4)

    def __mul__(self, other: PauliString) -> PauliString:
        """Exact product of two Pauli strings."""
        if self._n != other._n:
            raise ValueError(
                f"Carrier count mismatch: {self._n} vs {other._n}"
            )
        out_symbols: list[str] = []
        tot_phase = (self._phase_power + other._phase_power) % 4
        for s1, s2 in zip(self._symbols, other._symbols):
            res_s, p = SINGLE_PAULI_MUL[(s1, s2)]
            out_symbols.append(res_s)
            tot_phase = (tot_phase + p) % 4
        return PauliString(tuple(out_symbols), tot_phase)

    def tensor(self, other: PauliString) -> PauliString:
        """Kronecker tensor product of two Pauli strings."""
        return PauliString(
            self._symbols + other._symbols,
            (self._phase_power + other._phase_power) % 4,
        )

    def commutes_with(self, other: PauliString) -> bool:
        """True if [self, other] = 0, False if {self, other} = 0."""
        if self._n != other._n:
            raise ValueError("Carrier count mismatch")
        anticomm_loci = 0
        for s1, s2 in zip(self._symbols, other._symbols):
            if s1 == "I" or s2 == "I" or s1 == s2:
                continue
            anticomm_loci += 1
        return anticomm_loci % 2 == 0

    def anticommutes_with(self, other: PauliString) -> bool:
        """True if {self, other} = 0."""
        return not self.commutes_with(other)

    def symplectic_vector(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """Binary symplectic vector (x, z) in F_2^n x F_2^n.

        I = (0, 0), X = (1, 0), Z = (0, 1), Y = (1, 1).
        """
        x_vec: list[int] = []
        z_vec: list[int] = []
        for s in self._symbols:
            if s == "I":
                x_vec.append(0)
                z_vec.append(0)
            elif s == "X":
                x_vec.append(1)
                z_vec.append(0)
            elif s == "Z":
                x_vec.append(0)
                z_vec.append(1)
            elif s == "Y":
                x_vec.append(1)
                z_vec.append(1)
        return (tuple(x_vec), tuple(z_vec))

    def symplectic_inner_product(self, other: PauliString) -> int:
        """Symplectic inner product <u, v> = x1*z2 + z1*x2 mod 2."""
        (x1, z1) = self.symplectic_vector()
        (x2, z2) = other.symplectic_vector()
        val = sum(x1[k] * z2[k] + z1[k] * x2[k] for k in range(self._n)) % 2
        return val

    def to_int_matrix(self) -> IntMatrix:
        """Exact 2^n x 2^n integer matrix (for strings whose matrix entries are real integers)."""
        count_y = sum(1 for s in self._symbols if s == "Y")
        tot = (self._phase_power + count_y) % 4
        if tot % 2 != 0:
            raise ValueError(
                "Cannot represent complex Pauli string with integer matrix"
            )
        real_basis: dict[str, IntMatrix] = {
            "I": [[1, 0], [0, 1]],
            "X": [[0, 1], [1, 0]],
            "Z": [[1, 0], [0, -1]],
            "Y": [[0, -1], [1, 0]],
        }
        if self._n == 0:
            val = 1 if tot == 0 else -1
            return [[val]]
        mat = real_basis[self._symbols[0]]
        for k in range(1, self._n):
            mat = int_kronecker_product(mat, real_basis[self._symbols[k]])
        if tot == 2:
            mat = int_matrix_scale(-1, mat)
        return mat

    def to_matrix(self) -> Matrix:
        """Exact 2^n x 2^n Gaussian rational matrix."""
        if self._n == 0:
            return [[GaussianRational.from_phase_power(self._phase_power)]]
        mat = PAULI_MATRICES_2X2[self._symbols[0]]
        for k in range(1, self._n):
            mat = kronecker_product(mat, PAULI_MATRICES_2X2[self._symbols[k]])
        if self._phase_power != 0:
            factor = GaussianRational.from_phase_power(self._phase_power)
            mat = [
                [factor * mat[i][j] for j in range(len(mat[0]))]
                for i in range(len(mat))
            ]
        return mat


# =============================================================================
# 4. Stabilizer Projection Operator
# =============================================================================


def generate_stabilizer_group(
    generators: Sequence[PauliString],
) -> list[PauliString]:
    """Generates the full abelian group of 2^m Pauli strings from m independent generators."""
    m = len(generators)
    group: list[PauliString] = []
    n = generators[0].n_carriers if m > 0 else 0
    id_string = PauliString("I" * n, 0)
    for bits in itertools.product((0, 1), repeat=m):
        elem = id_string
        for gen, bit in zip(generators, bits):
            if bit == 1:
                elem = elem * gen
        group.append(elem)
    return group


def stabilizer_sum_int_matrix(generators: Sequence[PauliString]) -> IntMatrix:
    """Computes exact integer sum matrix K_S = sum_{M in S} M for real Pauli stabilizer group."""
    group = generate_stabilizer_group(generators)
    dim = 2 ** generators[0].n_carriers
    sum_mat = int_zero_matrix(dim, dim)
    for elem in group:
        elem_mat = elem.to_int_matrix()
        sum_mat = int_matrix_add(sum_mat, elem_mat)
    return sum_mat


def check_projection_idempotence(generators: Sequence[PauliString]) -> bool:
    """Verifies Pi_S @ Pi_S == Pi_S exactly.

    For Pi_S = (1 / |S|) * K_S, idempotence Pi_S^2 = Pi_S is equivalent to
    the exact integer identity K_S @ K_S == |S| * K_S.
    """
    group_size = 2 ** len(generators)
    K = stabilizer_sum_int_matrix(generators)
    K_sq = int_matrix_multiply(K, K)
    target = int_matrix_scale(group_size, K)
    dim = len(K)
    for i in range(dim):
        for j in range(dim):
            if K_sq[i][j] != target[i][j]:
                return False
    return True


def stabilizer_codespace_dimension(generators: Sequence[PauliString]) -> int:
    """Returns exact dimension of codespace: Tr(Pi_S) = Tr(K_S) / |S| = 2^(n - m)."""
    group_size = 2 ** len(generators)
    K = stabilizer_sum_int_matrix(generators)
    tr = int_matrix_trace(K)
    return int(tr // group_size)


# =============================================================================
# 5. Three-Carrier Bit-Flip Code [[3, 1, 1]]
# =============================================================================


class BitFlipCode3:
    """3-carrier bit-flip code [[3, 1, 1]]:

    Stabilizers: S1 = ZZI, S2 = IZZ.
    Logicals: Z_L = ZZZ, X_L = XXX.
    Codespace has dimension 2^(3 - 2) = 2 (1 logical carrier).
    Single bit-flips (X on carrier 1, 2, or 3) produce 4 distinct syndrome patterns.
    """

    S1 = PauliString("ZZI")
    S2 = PauliString("IZZ")
    STABILIZERS = [S1, S2]

    Z_L = PauliString("ZZZ")
    X_L = PauliString("XXX")

    @classmethod
    def syndrome(cls, error: PauliString) -> tuple[int, int]:
        """Syndrome bits (s1, s2) in {0, 1}^2.

        s_k = 0 if error commutes with S_k, 1 if error anticommutes with S_k.
        """
        s1 = 1 if error.anticommutes_with(cls.S1) else 0
        s2 = 1 if error.anticommutes_with(cls.S2) else 0
        return (s1, s2)

    @classmethod
    def syndrome_table_single_bitflips(
        cls,
    ) -> dict[tuple[int, int], PauliString]:
        """Returns map from syndrome (s1, s2) to the single-carrier X error."""
        errors = [
            PauliString("III"),
            PauliString("XII"),
            PauliString("IXI"),
            PauliString("IIX"),
        ]
        return {cls.syndrome(e): e for e in errors}

    @classmethod
    def correct(cls, error: PauliString) -> PauliString:
        """Returns the single-carrier bit-flip correction operator for a given error."""
        table = cls.syndrome_table_single_bitflips()
        syn = cls.syndrome(error)
        if syn not in table:
            raise ValueError(f"Unrecognized syndrome {syn} for [[3, 1, 1]] code")
        return table[syn]


# =============================================================================
# 6. Four-Carrier CSS Code [[4, 2, 2]] on Discrete 2-Torus
# =============================================================================


class TorusCode4:
    """4-carrier CSS code [[4, 2, 2]] arranged on a discrete 2-torus:

    Stabilizers: S_Z = ZZZZ, S_X = XXXX.
    Two independent logical carrier algebras:
      Carrier 1: Z_L1 = ZZII, X_L1 = XIXI
      Carrier 2: Z_L2 = ZIZI, X_L2 = XXII
    Codespace has dimension 2^(4 - 2) = 4 (2 logical carriers).
    All 12 single-carrier Pauli errors produce non-trivial syndromes (distance 2).
    """

    S_Z = PauliString("ZZZZ")
    S_X = PauliString("XXXX")
    STABILIZERS = [S_Z, S_X]

    Z_L1 = PauliString("ZZII")
    X_L1 = PauliString("XIXI")
    Z_L2 = PauliString("ZIZI")
    X_L2 = PauliString("XXII")

    @classmethod
    def syndrome(cls, error: PauliString) -> tuple[int, int]:
        """Syndrome (s_Z, s_X) in {0, 1}^2.

        s_Z = 1 if error anticommutes with S_Z (indicates X or Y error).
        s_X = 1 if error anticommutes with S_X (indicates Z or Y error).
        """
        s_z = 1 if error.anticommutes_with(cls.S_Z) else 0
        s_x = 1 if error.anticommutes_with(cls.S_X) else 0
        return (s_z, s_x)

    @classmethod
    def all_single_carrier_errors(cls) -> list[PauliString]:
        """All 4 x 3 = 12 single-carrier Pauli errors."""
        errs: list[PauliString] = []
        paulis = ["X", "Y", "Z"]
        for locus in range(4):
            for p in paulis:
                syms = ["I"] * 4
                syms[locus] = p
                errs.append(PauliString(syms))
        return errs


# =============================================================================
# 7. Steane [[7, 1, 3]] CSS Code on Fano Plane PG(2, 2)
# =============================================================================


class SteaneCode7:
    """Steane [[7, 1, 3]] CSS code on the Fano plane PG(2, 2):

    Points 1..7 labeled 0..6:
    The 3 dual Fano lines (weight 4):
      h1 = {3, 4, 5, 6} (loci 4, 5, 6, 7 in 1-based indexing: MSB of binary)
      h2 = {1, 2, 5, 6} (loci 2, 3, 6, 7 in 1-based indexing: middle bit of binary)
      h3 = {0, 2, 4, 6} (loci 1, 3, 5, 7 in 1-based indexing: LSB of binary)

    Stabilizers:
      M_Z1 = IIIZZZZ, M_Z2 = IZZIIZZ, M_Z3 = ZIZIZIZ
      M_X1 = IIIXXXX, M_X2 = IXXIIXX, M_X3 = XIXIXIX

    Logicals:
      X_L = XXXXXXX
      Z_L = ZZZZZZZ

    Transversal Hadamard H^{tensor 7} exchanges M_Xi <-> M_Zi and X_L <-> Z_L.
    Deterministic correction of all 21 single-carrier Pauli errors (7 X, 7 Z, 7 Y).
    """

    # Dual Fano line support indices (0-based)
    H1: tuple[int, ...] = (3, 4, 5, 6)
    H2: tuple[int, ...] = (1, 2, 5, 6)
    H3: tuple[int, ...] = (0, 2, 4, 6)

    DUAL_LINES = (H1, H2, H3)

    # 6 Stabilizer generators
    M_Z1 = PauliString("IIIZZZZ")
    M_Z2 = PauliString("IZZIIZZ")
    M_Z3 = PauliString("ZIZIZIZ")

    M_X1 = PauliString("IIIXXXX")
    M_X2 = PauliString("IXXIIXX")
    M_X3 = PauliString("XIXIXIX")

    Z_STABILIZERS = [M_Z1, M_Z2, M_Z3]
    X_STABILIZERS = [M_X1, M_X2, M_X3]
    STABILIZERS = [M_Z1, M_Z2, M_Z3, M_X1, M_X2, M_X3]

    X_L = PauliString("XXXXXXX")
    Z_L = PauliString("ZZZZZZZ")

    @classmethod
    def dual_line_intersections(cls) -> dict[tuple[int, int], int]:
        """Pairwise intersection cardinalities of the dual lines."""
        lines = [set(cls.H1), set(cls.H2), set(cls.H3)]
        res: dict[tuple[int, int], int] = {}
        for i in range(3):
            for j in range(i + 1, 3):
                res[(i, j)] = len(lines[i].intersection(lines[j]))
        return res

    @classmethod
    def syndrome(
        cls, error: PauliString
    ) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        """Returns syndrome (s_Z, s_X) where:

        s_Z measures anticommutation with (M_Z1, M_Z2, M_Z3) -> detects X and Y.
        s_X measures anticommutation with (M_X1, M_X2, M_X3) -> detects Z and Y.
        """
        s_z = (
            1 if error.anticommutes_with(cls.M_Z1) else 0,
            1 if error.anticommutes_with(cls.M_Z2) else 0,
            1 if error.anticommutes_with(cls.M_Z3) else 0,
        )
        s_x = (
            1 if error.anticommutes_with(cls.M_X1) else 0,
            1 if error.anticommutes_with(cls.M_X2) else 0,
            1 if error.anticommutes_with(cls.M_X3) else 0,
        )
        return (s_z, s_x)

    @classmethod
    def binary_to_locus(cls, syn_bits: tuple[int, int, int]) -> int:
        """Converts binary syndrome (b2, b1, b0) to 0-based carrier locus index (1..7 -> 0..6)."""
        val = syn_bits[0] * 4 + syn_bits[1] * 2 + syn_bits[2]
        return val - 1

    @classmethod
    def all_single_carrier_errors(cls) -> list[PauliString]:
        """All 7 x 3 = 21 single-carrier Pauli errors."""
        errs: list[PauliString] = []
        for locus in range(7):
            for p in ("X", "Y", "Z"):
                syms = ["I"] * 7
                syms[locus] = p
                errs.append(PauliString(syms))
        return errs

    @classmethod
    def correct(cls, error: PauliString) -> PauliString:
        """Deterministically diagnoses and returns the recovery Pauli operator."""
        s_z, s_x = cls.syndrome(error)
        has_x_syndrome = s_z != (0, 0, 0)
        has_z_syndrome = s_x != (0, 0, 0)

        if not has_x_syndrome and not has_z_syndrome:
            return PauliString("IIIIIII")

        if has_x_syndrome and not has_z_syndrome:
            loc = cls.binary_to_locus(s_z)
            syms = ["I"] * 7
            syms[loc] = "X"
            return PauliString(syms)

        if not has_x_syndrome and has_z_syndrome:
            loc = cls.binary_to_locus(s_x)
            syms = ["I"] * 7
            syms[loc] = "Z"
            return PauliString(syms)

        loc_x = cls.binary_to_locus(s_z)
        loc_z = cls.binary_to_locus(s_x)
        if loc_x != loc_z:
            raise ValueError(
                f"Inconsistent Y error syndrome: locus_x={loc_x} != locus_z={loc_z}"
            )
        syms = ["I"] * 7
        syms[loc_x] = "Y"
        return PauliString(syms)

    @classmethod
    def transversal_hadamard_transform(cls, p: PauliString) -> PauliString:
        """Applies transversal Hadamard conjugation H^{tensor 7} P H^{tensor 7}:

        H I H = I, H X H = Z, H Z H = X, H Y H = -Y.
        """
        new_symbols: list[str] = []
        added_phase = 0
        for s in p.symbols:
            if s == "I":
                new_symbols.append("I")
            elif s == "X":
                new_symbols.append("Z")
            elif s == "Z":
                new_symbols.append("X")
            elif s == "Y":
                new_symbols.append("Y")
                added_phase = (added_phase + 2) % 4
        return PauliString(new_symbols, (p.phase_power + added_phase) % 4)
