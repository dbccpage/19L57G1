"""Non-Classicality Horizons & Gottesman-Knill Boundary (Target P209d).

AuthorityEffect: None.

Provides:
1. SymplecticTableau: exact polynomial-time O(n^2) stabilizer tableau simulator
   over F_2 following the Aaronson-Gottesman framework.
2. PhaseSpaceCarrier: discrete Wigner quasiprobability distributions on F_p x F_p
   for odd_prime dimension p = 3, delineating the Discrete Hudson boundary
   between non-negative stabilizer states (W >= 0) and contextuality-active magic states (W < 0).
3. StabilizerMixture: multi-component superposition tracking for k injected magic states,
   certifying the exponential simulation resource boundary O(2^k).
"""

from __future__ import annotations

import cmath
from enum import Enum
import math
import random
from typing import Any, Callable, Sequence


class MagicStateType(Enum):
    """Supported non-stabilizer magic state injection types."""
    T = "T"


class BitMatrix:
    """Lightweight 2D bit matrix supporting both item access [r, c] and row slice [r]."""

    __slots__ = ("rows", "cols", "_data")

    def __init__(self, rows: int, cols: int, data: list[list[int]] | None = None) -> None:
        self.rows = rows
        self.cols = cols
        if data is None:
            self._data = [[0] * cols for _ in range(rows)]
        else:
            self._data = [list(r) for r in data]

    def __getitem__(self, item: Any) -> Any:
        if isinstance(item, tuple):
            r, c = item
            return self._data[r][c]
        return self._data[item]

    def __setitem__(self, item: Any, value: Any) -> None:
        if isinstance(item, tuple):
            r, c = item
            self._data[r][c] = int(value)
        else:
            self._data[item] = list(value)

    def copy(self) -> BitMatrix:
        return BitMatrix(self.rows, self.cols, [r[:] for r in self._data])

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BitMatrix):
            return self._data == other._data
        if isinstance(other, list):
            return self._data == other
        return False


PAULI_MATRICES = {
    "I": [[1.0 + 0.0j, 0.0 + 0.0j], [0.0 + 0.0j, 1.0 + 0.0j]],
    "X": [[0.0 + 0.0j, 1.0 + 0.0j], [1.0 + 0.0j, 0.0 + 0.0j]],
    "Y": [[0.0 + 0.0j, -1.0j], [1.0j, 0.0 + 0.0j]],
    "Z": [[1.0 + 0.0j, 0.0 + 0.0j], [0.0 + 0.0j, -1.0 + 0.0j]],
}


def mat_mul(A: Sequence[Sequence[complex]], B: Sequence[Sequence[complex]]) -> list[list[complex]]:
    """Multiply two complex matrices."""
    rA, cA = len(A), len(A[0])
    rB, cB = len(B), len(B[0])
    if cA != rB:
        raise ValueError("Incompatible matrix dimensions.")
    res = [[0.0 + 0.0j] * cB for _ in range(rA)]
    for i in range(rA):
        for k in range(cA):
            aik = A[i][k]
            if aik != 0:
                for j in range(cB):
                    res[i][j] += aik * B[k][j]
    return res


def mat_add(A: Sequence[Sequence[complex]], B: Sequence[Sequence[complex]]) -> list[list[complex]]:
    """Add two complex matrices."""
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mat_sub(A: Sequence[Sequence[complex]], B: Sequence[Sequence[complex]]) -> list[list[complex]]:
    """Subtract two complex matrices."""
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def mat_scale(A: Sequence[Sequence[complex]], s: complex) -> list[list[complex]]:
    """Multiply a matrix by a complex scalar."""
    return [[A[i][j] * s for j in range(len(A[0]))] for i in range(len(A))]


def mat_trace(A: Sequence[Sequence[complex]]) -> complex:
    """Compute the trace of a square matrix."""
    return sum(A[i][i] for i in range(len(A)))


def mat_adjoint(A: Sequence[Sequence[complex]]) -> list[list[complex]]:
    """Compute the conjugate transpose of a matrix."""
    return [[A[j][i].conjugate() for j in range(len(A))] for i in range(len(A[0]))]


def mat_kron(A: Sequence[Sequence[complex]], B: Sequence[Sequence[complex]]) -> list[list[complex]]:
    """Compute the Kronecker product of two matrices."""
    rA, cA = len(A), len(A[0])
    rB, cB = len(B), len(B[0])
    res = [[0.0 + 0.0j] * (cA * cB) for _ in range(rA * rB)]
    for i in range(rA):
        for j in range(cA):
            aij = A[i][j]
            if aij != 0:
                for k in range(rB):
                    for l in range(cB):
                        res[i * rB + k][j * cB + l] = aij * B[k][l]
    return res


def mat_pow(A: Sequence[Sequence[complex]], power: int) -> list[list[complex]]:
    """Compute power of a square matrix via repeated squaring."""
    n = len(A)
    res = [[1.0 + 0.0j if i == j else 0.0 + 0.0j for j in range(n)] for i in range(n)]
    base = [list(r) for r in A]
    p = power
    while p > 0:
        if p % 2 == 1:
            res = mat_mul(res, base)
        base = mat_mul(base, base)
        p //= 2
    return res


def mat_vec_mul(M: Sequence[Sequence[complex]], v: Sequence[complex]) -> list[complex]:
    """Multiply matrix by vector."""
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def outer_product(u: Sequence[complex], v: Sequence[complex]) -> list[list[complex]]:
    """Compute outer product |u><v|."""
    return [[u[i] * v[j].conjugate() for j in range(len(v))] for i in range(len(u))]


def vec_norm(v: Sequence[complex]) -> float:
    """Compute L2 norm of complex vector."""
    return math.sqrt(sum(abs(x) ** 2 for x in v))


def pauli_mult_phase(x1: int, z1: int, x2: int, z2: int) -> int:
    """Return exponent g in {0, 1, 2, 3} such that P1 * P2 = i^g * P3."""
    if (x1, z1) == (0, 0) or (x2, z2) == (0, 0) or (x1, z1) == (x2, z2):
        return 0
    if (x1, z1) == (1, 0):  # X
        return 1 if (x2, z2) == (1, 1) else 3
    if (x1, z1) == (1, 1):  # Y
        return 3 if (x2, z2) == (1, 0) else 1
    if (x1, z1) == (0, 1):  # Z
        return 1 if (x2, z2) == (1, 0) else 3
    return 0


class SymplecticTableau:
    """Gottesman-Knill canonical symplectic tableau simulator for n state carriers over F_2.

    Rows 0 .. n-1: destabilizer generators D_i.
    Rows n .. 2n-1: stabilizer generators S_i.
    Columns 0 .. n-1: X bits.
    Columns n .. 2n-1: Z bits.
    Column 2n: sign bits r in {0, 1} where (-1)^r determines the sign factor.
    """

    def __init__(self, n: int) -> None:
        if n < 1:
            raise ValueError("Carrier count must be positive.")
        self.n = n
        self.x = BitMatrix(2 * n, n)
        self.z = BitMatrix(2 * n, n)
        self.r = [0] * (2 * n)
        for i in range(n):
            self.x[i, i] = 1  # destabilizer D_i = X_i
            self.z[i + n, i] = 1  # stabilizer S_i = Z_i

    def copy(self) -> SymplecticTableau:
        """Return an independent clone of the current tableau state."""
        cloned = SymplecticTableau(self.n)
        cloned.x = self.x.copy()
        cloned.z = self.z.copy()
        cloned.r = self.r.copy()
        return cloned

    def omega(self, row1: int, row2: int) -> int:
        """Compute the symplectic inner product between row1 and row2 over F_2."""
        val = sum(
            self.x[row1][j] * self.z[row2][j] + self.z[row1][j] * self.x[row2][j]
            for j in range(self.n)
        ) % 2
        return val

    def check_tableau_invariants(self) -> bool:
        """Verify stabilizer commutativity, destabilizer commutativity, and dual pairings."""
        n = self.n
        for i in range(n):
            for j in range(n):
                if self.omega(i + n, j + n) != 0:
                    return False
                if self.omega(i, j) != 0:
                    return False
                expected = 1 if i == j else 0
                if self.omega(i, j + n) != expected:
                    return False
        return True

    def h(self, a: int) -> SymplecticTableau:
        """Apply Hadamard transformation to state carrier a in O(n) steps."""
        if not (0 <= a < self.n):
            raise IndexError("Carrier index out of range.")
        for i in range(2 * self.n):
            self.r[i] ^= (self.x[i, a] & self.z[i, a])
            self.x[i, a], self.z[i, a] = self.z[i, a], self.x[i, a]
        return self

    def s_gate(self, a: int) -> SymplecticTableau:
        """Apply S_gate transformation to state carrier a in O(n) steps."""
        if not (0 <= a < self.n):
            raise IndexError("Carrier index out of range.")
        for i in range(2 * self.n):
            self.r[i] ^= (self.x[i, a] & self.z[i, a])
            self.z[i, a] ^= self.x[i, a]
        return self

    def cnot(self, a: int, b: int) -> SymplecticTableau:
        """Apply CNOT transformation with control carrier a and target b in O(n) steps."""
        if not (0 <= a < self.n and 0 <= b < self.n):
            raise IndexError("Carrier indices out of range.")
        if a == b:
            raise ValueError("Control and target carriers must be distinct.")
        for i in range(2 * self.n):
            self.r[i] ^= (self.x[i, a] & self.z[i, b] & (self.x[i, b] ^ self.z[i, a] ^ 1))
            self.x[i, b] ^= self.x[i, a]
            self.z[i, a] ^= self.z[i, b]
        return self

    def x_gate(self, a: int) -> SymplecticTableau:
        """Apply X gate to carrier a (derived as H S S H)."""
        self.h(a)
        self.s_gate(a)
        self.s_gate(a)
        self.h(a)
        return self

    def z_gate(self, a: int) -> SymplecticTableau:
        """Apply Z gate to carrier a (derived as S S)."""
        self.s_gate(a)
        self.s_gate(a)
        return self

    def y_gate(self, a: int) -> SymplecticTableau:
        """Apply Y gate to carrier a (derived as S X S_dag where S_dag = S^3)."""
        self.s_gate(a)
        self.x_gate(a)
        for _ in range(3):
            self.s_gate(a)
        return self

    def row_mult(self, h: int, i: int) -> None:
        """Multiply row h by row i in place: row_h <- row_h * row_i."""
        delta = sum(
            pauli_mult_phase(self.x[h, j], self.z[h, j], self.x[i, j], self.z[i, j])
            for j in range(self.n)
        )
        self.r[h] = ((2 * self.r[h] + 2 * self.r[i] + delta) % 4) // 2
        for j in range(self.n):
            self.x[h, j] ^= self.x[i, j]
            self.z[h, j] ^= self.z[i, j]

    def measure_z(self, a: int, forced_outcome: int | None = None) -> int:
        """Simulate Pauli Z measurement on carrier a with exact tableau reduction.

        Returns 0 (for eigenvalue +1) or 1 (for eigenvalue -1).
        """
        if not (0 <= a < self.n):
            raise IndexError("Carrier index out of range.")
        n = self.n
        p = None
        for row in range(n, 2 * n):
            if self.x[row, a] == 1:
                p = row
                break

        if p is not None:
            # Case 1: Non-commuting stabilizer -> random measurement outcome
            for i in range(2 * n):
                if i != p and i != p - n and self.x[i, a] == 1:
                    self.row_mult(i, p)
            self.x[p - n] = self.x[p][:]
            self.z[p - n] = self.z[p][:]
            self.r[p - n] = self.r[p]
            self.x[p] = [0] * n
            self.z[p] = [0] * n
            self.z[p, a] = 1
            outcome = random.randint(0, 1) if forced_outcome is None else forced_outcome
            self.r[p] = outcome
            return outcome
        else:
            # Case 2: Commuting stabilizer -> deterministic measurement outcome
            scratch_x = [0] * n
            scratch_z = [0] * n
            scratch_r = 0
            for i in range(n):
                if self.x[i, a] == 1:
                    delta = sum(
                        pauli_mult_phase(scratch_x[j], scratch_z[j], self.x[i + n, j], self.z[i + n, j])
                        for j in range(n)
                    )
                    scratch_r = ((2 * scratch_r + 2 * self.r[i + n] + delta) % 4) // 2
                    for j in range(n):
                        scratch_x[j] ^= self.x[i + n, j]
                        scratch_z[j] ^= self.z[i + n, j]
            return scratch_r

    def to_pauli_strings(self) -> dict[str, list[str]]:
        """Format stabilizer and destabilizer generators as human-readable Pauli strings."""
        def row_to_str(row: int) -> str:
            sign = "-" if self.r[row] == 1 else "+"
            symbols: list[str] = []
            for j in range(self.n):
                xj = self.x[row, j]
                zj = self.z[row, j]
                if xj == 0 and zj == 0:
                    symbols.append("I")
                elif xj == 1 and zj == 0:
                    symbols.append("X")
                elif xj == 1 and zj == 1:
                    symbols.append("Y")
                else:
                    symbols.append("Z")
            return sign + "".join(symbols)

        destab = [row_to_str(i) for i in range(self.n)]
        stab = [row_to_str(i + self.n) for i in range(self.n)]
        return {"destabilizers": destab, "stabilizers": stab}

    def state_vector(self) -> list[complex]:
        """Compute exact state vector for small carrier counts n <= 10."""
        if self.n > 10:
            raise ValueError("State vector extraction bounded to n <= 10.")
        dim = 1 << self.n
        proj = [[1.0 + 0.0j if i == j else 0.0 + 0.0j for j in range(dim)] for i in range(dim)]
        for i in range(self.n):
            row = i + self.n
            sign_factor = -1.0 if self.r[row] == 1 else 1.0
            mat = [[sign_factor + 0.0j]]
            for j in range(self.n):
                xj = self.x[row, j]
                zj = self.z[row, j]
                if xj == 0 and zj == 0:
                    pj = PAULI_MATRICES["I"]
                elif xj == 1 and zj == 0:
                    pj = PAULI_MATRICES["X"]
                elif xj == 1 and zj == 1:
                    pj = PAULI_MATRICES["Y"]
                else:
                    pj = PAULI_MATRICES["Z"]
                mat = mat_kron(mat, pj)
            id_dim = [[1.0 + 0.0j if r == c else 0.0 + 0.0j for c in range(dim)] for r in range(dim)]
            term = mat_scale(mat_add(id_dim, mat), 0.5)
            proj = mat_mul(proj, term)

        for b in range(dim):
            seed = [1.0 + 0.0j if k == b else 0.0 + 0.0j for k in range(dim)]
            candidate = mat_vec_mul(proj, seed)
            norm = vec_norm(candidate)
            if norm > 1e-8:
                return [c / norm for c in candidate]
        raise RuntimeError("Failed to extract state vector from stabilizer projector.")

    def density_matrix(self) -> list[list[complex]]:
        """Compute exact density matrix operator for small carrier counts."""
        vec = self.state_vector()
        return outer_product(vec, vec)

    def create_bell_pair(self, q0: int = 0, q1: int = 1) -> SymplecticTableau:
        """Generate standard Bell state (|00> + |11>)/sqrt(2) on carriers q0, q1."""
        self.h(q0)
        self.cnot(q0, q1)
        return self

    def create_ghz(self, carriers: list[int] | None = None) -> SymplecticTableau:
        """Generate GHZ state (|00...0> + |11...1>)/sqrt(2) across designated carriers."""
        targets = list(range(self.n)) if carriers is None else carriers
        if len(targets) < 2:
            raise ValueError("GHZ preparation requires at least 2 carriers.")
        self.h(targets[0])
        for target in targets[1:]:
            self.cnot(targets[0], target)
        return self

    def teleport(
        self,
        input_prep: Callable[[SymplecticTableau], Any],
        forced_outcomes: tuple[int, int] | None = None,
    ) -> tuple[int, int]:
        """Execute teleportation protocol of carrier 0 to carrier 2 using resource pair (1, 2)."""
        if self.n != 3:
            raise ValueError("Teleportation protocol structured for 3 carriers.")
        input_prep(self)
        self.h(1)
        self.cnot(1, 2)
        self.cnot(0, 1)
        self.h(0)
        m0 = self.measure_z(0, forced_outcome=forced_outcomes[0] if forced_outcomes else None)
        m1 = self.measure_z(1, forced_outcome=forced_outcomes[1] if forced_outcomes else None)
        if m1 == 1:
            self.x_gate(2)
        if m0 == 1:
            self.z_gate(2)
        return m0, m1


class PhaseSpaceCarrier:
    """Discrete phase_space operator formalism on F_p x F_p for odd_prime dimension p.

    Delineates the Discrete Hudson boundary:
    Stabilizer states inhabit the non-negative Wigner cone (W >= 0),
    whereas non-stabilizer magic states possess negative Wigner quasiprobability (W < 0).
    """

    def __init__(self, p: int = 3) -> None:
        if p < 3 or p % 2 == 0:
            raise ValueError("Discrete Gross phase_space requires odd_prime dimension p >= 3.")
        self.p = p
        self.omega = cmath.exp(2j * math.pi / p)
        # Shift X and Clock Z operators
        self.X = [[0.0 + 0.0j] * p for _ in range(p)]
        for i in range(p):
            self.X[(i + 1) % p][i] = 1.0
        self.Z = [[0.0 + 0.0j] * p for _ in range(p)]
        for i in range(p):
            self.Z[i][i] = self.omega ** i
        # Modular inverse of 2 mod p
        self.inv2 = (p + 1) // 2

        # Point operator at origin
        a00 = [[0.0 + 0.0j] * p for _ in range(p)]
        for u in range(p):
            for v in range(p):
                a00 = mat_add(a00, self.weyl(u, v))
        self.A00 = mat_scale(a00, 1.0 / float(p))

    def weyl(self, u: int, v: int) -> list[list[complex]]:
        """Compute Weyl-Heisenberg displacement operator D(u, v) = omega^(inv2 * u * v) X^u Z^v."""
        u_mod = u % self.p
        v_mod = v % self.p
        phase_factor = self.omega ** ((self.inv2 * u_mod * v_mod) % self.p)
        x_pow = mat_pow(self.X, u_mod)
        z_pow = mat_pow(self.Z, v_mod)
        return mat_scale(mat_mul(x_pow, z_pow), phase_factor)

    def point_operator(self, q: int, p_coord: int) -> list[list[complex]]:
        """Compute discrete phase_space point operator A(q, p)."""
        d = self.weyl(q, p_coord)
        d_adj = mat_adjoint(d)
        return mat_mul(mat_mul(d, self.A00), d_adj)

    def wigner_distribution(self, rho: Sequence[Sequence[complex]]) -> list[list[float]]:
        """Calculate the p x p discrete Wigner quasiprobability grid W(q, p)."""
        w: list[list[float]] = [[0.0] * self.p for _ in range(self.p)]
        for q in range(self.p):
            for p_coord in range(self.p):
                op = self.point_operator(q, p_coord)
                val = float(mat_trace(mat_mul(rho, op)).real) / float(self.p)
                w[q][p_coord] = val
        return w

    def is_wigner_non_negative(self, rho: Sequence[Sequence[complex]], tol: float = 1e-10) -> bool:
        """Check whether W(q, p) >= 0 everywhere on the phase_space grid."""
        w = self.wigner_distribution(rho)
        return all(w[q][p_coord] >= -tol for q in range(self.p) for p_coord in range(self.p))

    def wigner_negativity(self, rho: Sequence[Sequence[complex]]) -> float:
        """Compute sum of negative Wigner quasiprobability values: sum max(0, -W(q, p))."""
        w = self.wigner_distribution(rho)
        neg = sum(max(0.0, -w[q][p_coord]) for q in range(self.p) for p_coord in range(self.p))
        return float(neg)

    def mana(self, rho: Sequence[Sequence[complex]]) -> float:
        """Compute logarithmic Mana non-classicality measure: log2(sum |W(q, p)|)."""
        w = self.wigner_distribution(rho)
        total_l1 = sum(abs(w[q][p_coord]) for q in range(self.p) for p_coord in range(self.p))
        return float(math.log2(max(1.0, total_l1)))

    def stabilizer_states(self) -> list[list[complex]]:
        """Return pure stabilizer basis states across all p + 1 MUBs in dimension p = 3."""
        p = self.p
        states: list[list[complex]] = []
        # MUB 0: Z-basis
        for k in range(p):
            vec = [1.0 + 0.0j if i == k else 0.0 + 0.0j for i in range(p)]
            states.append(vec)

        # MUBs 1 .. p: eigenstates of Weyl(1, k)
        I_p = [[1.0 + 0.0j if i == j else 0.0 + 0.0j for j in range(p)] for i in range(p)]
        for k in range(p):
            op = self.weyl(1, k)
            evals = [cmath.exp(2j * math.pi * m / float(p)) for m in range(p)]
            for m_idx, lam in enumerate(evals):
                other_evals = [ev for j, ev in enumerate(evals) if j != m_idx]
                P = mat_mul(
                    mat_sub(op, mat_scale(I_p, other_evals[0])),
                    mat_sub(op, mat_scale(I_p, other_evals[1]))
                )
                for col_idx in range(p):
                    col = [P[row_idx][col_idx] for row_idx in range(p)]
                    norm = vec_norm(col)
                    if norm > 1e-8:
                        states.append([c / norm for c in col])
                        break
        return states

    def norrell_magic_state(self) -> list[complex]:
        """Return the Norrell magic state |N> = (|1> - |2>) / sqrt(2)."""
        vec = [0.0 + 0.0j] * self.p
        vec[1] = 1.0 / math.sqrt(2.0)
        vec[2] = -1.0 / math.sqrt(2.0)
        return vec

    def strange_magic_state(self) -> list[complex]:
        """Return the Strange magic state |S> = (|1> + |2>) / sqrt(2)."""
        vec = [0.0 + 0.0j] * self.p
        vec[1] = 1.0 / math.sqrt(2.0)
        vec[2] = 1.0 / math.sqrt(2.0)
        return vec


class StabilizerMixture:
    """Multi-component superposition tracker for circuits with injected magic states.

    Represents a state carrier as a linear superposition over chi stabilizer tableaux:
    |Psi> = sum_b c_b |T_b>.
    Demonstrates that injecting k magic states breaks single-tableau closure,
    requiring chi = 2^k stabilizer branches and certifying the Gottesman-Knill boundary.
    """

    def __init__(self, n_carriers: int) -> None:
        self.n_carriers = n_carriers
        self.branches: list[tuple[complex, SymplecticTableau]] = [
            (1.0 + 0.0j, SymplecticTableau(n_carriers))
        ]

    @property
    def branch_count(self) -> int:
        """Current count of active stabilizer branches."""
        return len(self.branches)

    def inject_magic_state(
        self,
        carrier_idx: int,
        magic_type: MagicStateType | str = MagicStateType.T,
    ) -> StabilizerMixture:
        """Inject a non-stabilizer magic state, doubling every active stabilizer branch.

        For T-type state: |T> = 1/sqrt(2) (|0> + e^(i pi / 4) |1>).
        """
        if not (0 <= carrier_idx < self.n_carriers):
            raise IndexError("Carrier index out of range.")

        m_type = magic_type.value if isinstance(magic_type, MagicStateType) else str(magic_type)
        if m_type != MagicStateType.T.value:
            raise ValueError(f"Unsupported magic state type: {magic_type}")

        c0_factor = 1.0 / math.sqrt(2.0)
        c1_factor = cmath.exp(1j * math.pi / 4.0) / math.sqrt(2.0)

        new_branches: list[tuple[complex, SymplecticTableau]] = []
        for coeff, tab in self.branches:
            # Branch 0: carrier left in |0>
            tab0 = tab.copy()
            new_branches.append((coeff * c0_factor, tab0))
            # Branch 1: carrier flipped to |1> via X_gate
            tab1 = tab.copy()
            tab1.x_gate(carrier_idx)
            new_branches.append((coeff * c1_factor, tab1))

        self.branches = new_branches
        return self

    def apply_h(self, a: int) -> StabilizerMixture:
        """Apply Hadamard transformation to all active stabilizer branches in parallel."""
        for _, tab in self.branches:
            tab.h(a)
        return self

    def apply_s_gate(self, a: int) -> StabilizerMixture:
        """Apply S_gate transformation to all active stabilizer branches in parallel."""
        for _, tab in self.branches:
            tab.s_gate(a)
        return self

    def apply_cnot(self, a: int, b: int) -> StabilizerMixture:
        """Apply CNOT transformation to all active stabilizer branches in parallel."""
        for _, tab in self.branches:
            tab.cnot(a, b)
        return self

    def state_vector(self) -> list[complex]:
        """Compute coherent state vector across all branches for small n <= 10."""
        if self.n_carriers > 10:
            raise ValueError("State vector extraction bounded to n <= 10.")
        dim = 1 << self.n_carriers
        total_vec = [0.0 + 0.0j] * dim
        for coeff, tab in self.branches:
            tab_v = tab.state_vector()
            for i in range(dim):
                total_vec[i] += coeff * tab_v[i]
        norm = vec_norm(total_vec)
        if norm > 1e-10:
            total_vec = [c / norm for c in total_vec]
        return total_vec

    @staticmethod
    def benchmark_scaling(k_max: int, n_carriers: int = 4) -> dict[str, Any]:
        """Demonstrate exponential branch proliferation O(2^k) under k magic injections."""
        results: list[dict[str, int]] = []
        for k in range(k_max + 1):
            mixture = StabilizerMixture(n_carriers)
            for i in range(k):
                mixture.inject_magic_state(i % n_carriers, magic_type=MagicStateType.T)
            results.append({
                "magic_count_k": k,
                "branch_count": mixture.branch_count,
                "expected_exponential": 1 << k,
            })
        return {"carrier_count": n_carriers, "scaling_results": results}
