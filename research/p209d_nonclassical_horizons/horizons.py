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

import math
from typing import Any, Callable, cast
import numpy as np

PAULI_MATRICES = {
    "I": np.eye(2, dtype=complex),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.array([[1, 0], [0, -1]], dtype=complex),
}


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
        self.x = np.zeros((2 * n, n), dtype=int)
        self.z = np.zeros((2 * n, n), dtype=int)
        self.r = np.zeros(2 * n, dtype=int)
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
        val = int(np.sum(self.x[row1] * self.z[row2] + self.z[row1] * self.x[row2]) % 2)
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
        """Apply Y gate to carrier a (derived as S X S_dag)."""
        self.s_gate(a)
        self.x_gate(a)
        self.s_gate(a)
        self.s_gate(a)
        self.s_gate(a)
        return self

    def row_mult(self, h: int, i: int) -> None:
        """Multiply row h by row i in place: row_h <- row_h * row_i."""
        delta = sum(
            pauli_mult_phase(self.x[h, j], self.z[h, j], self.x[i, j], self.z[i, j])
            for j in range(self.n)
        )
        self.r[h] = ((2 * self.r[h] + 2 * self.r[i] + delta) % 4) // 2
        self.x[h] ^= self.x[i]
        self.z[h] ^= self.z[i]

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
            self.x[p - n] = self.x[p].copy()
            self.z[p - n] = self.z[p].copy()
            self.r[p - n] = self.r[p]
            self.x[p] = np.zeros(n, dtype=int)
            self.z[p] = np.zeros(n, dtype=int)
            self.z[p, a] = 1
            outcome = int(np.random.randint(0, 2)) if forced_outcome is None else forced_outcome
            self.r[p] = outcome
            return outcome
        else:
            # Case 2: Commuting stabilizer -> deterministic measurement outcome
            scratch_x = np.zeros(n, dtype=int)
            scratch_z = np.zeros(n, dtype=int)
            scratch_r = 0
            for i in range(n):
                if self.x[i, a] == 1:
                    delta = sum(
                        pauli_mult_phase(scratch_x[j], scratch_z[j], self.x[i + n, j], self.z[i + n, j])
                        for j in range(n)
                    )
                    scratch_r = ((2 * scratch_r + 2 * self.r[i + n] + delta) % 4) // 2
                    scratch_x ^= self.x[i + n]
                    scratch_z ^= self.z[i + n]
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

    def state_vector(self) -> np.ndarray:
        """Compute exact state vector for small carrier counts n <= 10."""
        if self.n > 10:
            raise ValueError("State vector extraction bounded to n <= 10.")
        dim = 1 << self.n
        proj = np.eye(dim, dtype=complex)
        for i in range(self.n):
            row = i + self.n
            mat = (-1) ** int(self.r[row]) * np.eye(1, dtype=complex)
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
                mat = np.kron(mat, pj)
            proj = proj @ ((np.eye(dim, dtype=complex) + mat) / 2.0)

        for b in range(dim):
            seed = np.zeros(dim, dtype=complex)
            seed[b] = 1.0
            candidate = proj @ seed
            norm = np.linalg.norm(candidate)
            if norm > 1e-8:
                return cast(np.ndarray, candidate / norm)
        raise RuntimeError("Failed to extract state vector from stabilizer projector.")

    def density_matrix(self) -> np.ndarray:
        """Compute exact density matrix operator for small carrier counts."""
        vec = self.state_vector()
        return np.outer(vec, vec.conj())

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
        self.omega = np.exp(2j * np.pi / p)
        # Shift X and Clock Z operators
        self.X = np.zeros((p, p), dtype=complex)
        for i in range(p):
            self.X[(i + 1) % p, i] = 1.0
        self.Z = np.diag([self.omega ** i for i in range(p)])
        # Modular inverse of 2 mod p
        self.inv2 = (p + 1) // 2

        # Point operator at origin
        a00 = np.zeros((p, p), dtype=complex)
        for u in range(p):
            for v in range(p):
                a00 += self.weyl(u, v)
        self.A00 = a00 / float(p)

    def weyl(self, u: int, v: int) -> np.ndarray:
        """Compute Weyl-Heisenberg displacement operator D(u, v) = omega^(inv2 * u * v) X^u Z^v."""
        u_mod = u % self.p
        v_mod = v % self.p
        phase_factor = self.omega ** ((self.inv2 * u_mod * v_mod) % self.p)
        x_pow = np.linalg.matrix_power(self.X, u_mod)
        z_pow = np.linalg.matrix_power(self.Z, v_mod)
        return cast(np.ndarray, phase_factor * (x_pow @ z_pow))

    def point_operator(self, q: int, p_coord: int) -> np.ndarray:
        """Compute discrete phase_space point operator A(q, p)."""
        d = self.weyl(q, p_coord)
        return cast(np.ndarray, d @ self.A00 @ d.conj().T)

    def wigner_distribution(self, rho: np.ndarray) -> np.ndarray:
        """Calculate the p x p discrete Wigner quasiprobability grid W(q, p)."""
        w = np.zeros((self.p, self.p), dtype=float)
        for q in range(self.p):
            for p_coord in range(self.p):
                op = self.point_operator(q, p_coord)
                val = float(np.real(np.trace(rho @ op))) / float(self.p)
                w[q, p_coord] = val
        return w

    def is_wigner_non_negative(self, rho: np.ndarray, tol: float = 1e-10) -> bool:
        """Check whether W(q, p) >= 0 everywhere on the phase_space grid."""
        w = self.wigner_distribution(rho)
        return bool(np.min(w) >= -tol)

    def wigner_negativity(self, rho: np.ndarray) -> float:
        """Compute sum of negative Wigner quasiprobability values: sum max(0, -W(q, p))."""
        w = self.wigner_distribution(rho)
        neg = np.sum(np.maximum(0.0, -w))
        return float(neg)

    def mana(self, rho: np.ndarray) -> float:
        """Compute logarithmic Mana non-classicality measure: log2(sum |W(q, p)|)."""
        w = self.wigner_distribution(rho)
        total_l1 = np.sum(np.abs(w))
        return float(math.log2(max(1.0, total_l1)))

    def stabilizer_states(self) -> list[np.ndarray]:
        """Return pure stabilizer basis states across all p + 1 MUBs in dimension p."""
        p = self.p
        states: list[np.ndarray] = []
        # MUB 0: Z-basis
        for k in range(p):
            vec = np.zeros(p, dtype=complex)
            vec[k] = 1.0
            states.append(vec)
        # MUBs 1 .. p: eigenstates of X Z^k
        for k in range(p):
            op = self.weyl(1, k)
            _, vecs = np.linalg.eig(op)
            for col in range(p):
                states.append(vecs[:, col] / np.linalg.norm(vecs[:, col]))
        return states

    def norrell_magic_state(self) -> np.ndarray:
        """Return the Norrell magic state |N> = (|1> - |2>) / sqrt(2)."""
        vec = np.zeros(self.p, dtype=complex)
        vec[1] = 1.0 / np.sqrt(2.0)
        vec[2] = -1.0 / np.sqrt(2.0)
        return cast(np.ndarray, vec)

    def strange_magic_state(self) -> np.ndarray:
        """Return the Strange magic state |S> = (|1> + |2>) / sqrt(2)."""
        vec = np.zeros(self.p, dtype=complex)
        vec[1] = 1.0 / np.sqrt(2.0)
        vec[2] = 1.0 / np.sqrt(2.0)
        return cast(np.ndarray, vec)


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

    def inject_magic_state(self, carrier_idx: int, magic_type: str = "T") -> StabilizerMixture:
        """Inject a non-stabilizer magic state, doubling every active stabilizer branch.

        For T-type state: |T> = 1/sqrt(2) (|0> + e^(i pi / 4) |1>).
        """
        if not (0 <= carrier_idx < self.n_carriers):
            raise IndexError("Carrier index out of range.")

        new_branches: list[tuple[complex, SymplecticTableau]] = []
        if magic_type == "T":
            c0_factor = 1.0 / np.sqrt(2.0)
            c1_factor = np.exp(1j * np.pi / 4.0) / np.sqrt(2.0)
        elif magic_type == "H":
            c0_factor = np.cos(np.pi / 8.0)
            c1_factor = np.sin(np.pi / 8.0)
        else:
            c0_factor = 1.0 / np.sqrt(2.0)
            c1_factor = 1.0 / np.sqrt(2.0)

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

    def state_vector(self) -> np.ndarray:
        """Compute coherent state vector across all branches for small n <= 10."""
        if self.n_carriers > 10:
            raise ValueError("State vector extraction bounded to n <= 10.")
        dim = 1 << self.n_carriers
        total_vec = np.zeros(dim, dtype=complex)
        for coeff, tab in self.branches:
            total_vec += coeff * tab.state_vector()
        norm = np.linalg.norm(total_vec)
        if norm > 1e-10:
            total_vec = total_vec / norm
        return cast(np.ndarray, total_vec)

    @staticmethod
    def benchmark_scaling(k_max: int, n_carriers: int = 4) -> dict[str, Any]:
        """Demonstrate exponential branch proliferation O(2^k) under k magic injections."""
        results: list[dict[str, int]] = []
        for k in range(k_max + 1):
            mixture = StabilizerMixture(n_carriers)
            for i in range(k):
                mixture.inject_magic_state(i % n_carriers, magic_type="T")
            results.append({
                "magic_count_k": k,
                "branch_count": mixture.branch_count,
                "expected_exponential": 1 << k,
            })
        return {"carrier_count": n_carriers, "scaling_results": results}
