"""Discrete Clifford Group quotient and finite symplectic geometry (Target P209b).

Formalizes:
1. Exact integer and modular arithmetic for symplectic form:
   omega(u, v) = u_x * v_z - u_z * v_x mod p over F_p^2.
2. Symplectic preservation:
   omega(M u, M v) = omega(u, v) mod p.
3. Single-carrier projective Clifford group quotient Sp(2, F_2) =~ S_3 of order 6.
4. Single-carrier projective Clifford group quotient Sp(2, F_3) =~ SL(2, F_3) of order 24.
5. Exact determinant 1 mod p, group multiplication closure, element orders.
6. Eastin-Knill finite quotient obstruction: transversal gates form a strictly
   finite group, obstructing dense covering of continuous unitary groups.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def omega(u: tuple[int, int], v: tuple[int, int], p: int) -> int:
    """Canonical symplectic bilinear form on F_p^2: omega(u, v) = u_x * v_z - u_z * v_x mod p."""
    if p <= 1:
        raise ValueError("Modulus p must be an integer >= 2")
    ux, uz = u[0] % p, u[1] % p
    vx, vz = v[0] % p, v[1] % p
    return (ux * vz - uz * vx) % p


@dataclass(frozen=True)
class Matrix2:
    """A 2x2 matrix over finite field F_p."""

    a: int
    b: int
    c: int
    d: int
    p: int

    def __post_init__(self) -> None:
        if self.p <= 1:
            raise ValueError("Modulus p must be an integer >= 2")
        object.__setattr__(self, "a", self.a % self.p)
        object.__setattr__(self, "b", self.b % self.p)
        object.__setattr__(self, "c", self.c % self.p)
        object.__setattr__(self, "d", self.d % self.p)

    @property
    def det(self) -> int:
        """Determinant modulo p."""
        return (self.a * self.d - self.b * self.c) % self.p

    @property
    def trace(self) -> int:
        """Matrix trace modulo p."""
        return (self.a + self.d) % self.p

    def matmul(self, other: Matrix2) -> Matrix2:
        """Matrix multiplication modulo p."""
        if self.p != other.p:
            raise ValueError("Moduli must match for matrix multiplication")
        p = self.p
        return Matrix2(
            (self.a * other.a + self.b * other.c) % p,
            (self.a * other.b + self.b * other.d) % p,
            (self.c * other.a + self.d * other.c) % p,
            (self.c * other.b + self.d * other.d) % p,
            p,
        )

    def apply(self, v: tuple[int, int]) -> tuple[int, int]:
        """Apply matrix to a 2D vector modulo p."""
        p = self.p
        vx, vz = v[0] % p, v[1] % p
        rx = (self.a * vx + self.b * vz) % p
        rz = (self.c * vx + self.d * vz) % p
        return (rx, rz)

    def preserves_symplectic_form(self) -> bool:
        """Check whether M preserves omega(M u, M v) = omega(u, v) mod p for all u, v in F_p^2."""
        p = self.p
        vectors = [(x, z) for x in range(p) for z in range(p)]
        for u in vectors:
            for v in vectors:
                mu = self.apply(u)
                mv = self.apply(v)
                if omega(mu, mv, p) != omega(u, v, p):
                    return False
        return True

    def inverse(self) -> Matrix2:
        """Inverse matrix in SL(2, F_p), requiring det = 1 mod p."""
        if self.det != 1:
            raise ValueError("Matrix must have determinant 1 mod p for SL(2, F_p) inverse")
        p = self.p
        return Matrix2(self.d, (-self.b) % p, (-self.c) % p, self.a, p)

    def order(self) -> int:
        """Compute the multiplicative order of M in SL(2, F_p)."""
        identity = Matrix2(1, 0, 0, 1, self.p)
        curr = self
        for k in range(1, 1000):
            if curr == identity:
                return k
            curr = curr.matmul(self)
        raise RuntimeError("Multiplicative order exceeded bound")


def get_sp2_f2_generators() -> tuple[Matrix2, Matrix2]:
    """Generators H and S for Sp(2, F_2)."""
    h_mat = Matrix2(0, 1, 1, 0, 2)
    s_mat = Matrix2(1, 0, 1, 1, 2)
    return h_mat, s_mat


def build_sp2_f2_elements() -> dict[str, Matrix2]:
    """Construct the 6 explicit elements of Sp(2, F_2) =~ S_3."""
    h_mat, s_mat = get_sp2_f2_generators()
    identity = Matrix2(1, 0, 0, 1, 2)
    sh_mat = s_mat.matmul(h_mat)
    hs_mat = h_mat.matmul(s_mat)
    hsh_mat = h_mat.matmul(sh_mat)
    return {
        "I": identity,
        "H": h_mat,
        "S": s_mat,
        "SH": sh_mat,
        "HS": hs_mat,
        "HSH": hsh_mat,
    }


def get_sp2_f2_multiplication_table() -> dict[tuple[str, str], str]:
    """Generate the full Cayley multiplication table for Sp(2, F_2)."""
    elements = build_sp2_f2_elements()
    rev = {m: name for name, m in elements.items()}
    table: dict[tuple[str, str], str] = {}
    for n1, m1 in elements.items():
        for n2, m2 in elements.items():
            prod = m1.matmul(m2)
            if prod not in rev:
                raise RuntimeError(f"Multiplication closure failed for {n1} * {n2}")
            table[(n1, n2)] = rev[prod]
    return table


def build_sp2_f3_elements() -> list[Matrix2]:
    """Enumerate all 24 elements of Sp(2, F_3) =~ SL(2, F_3)."""
    elements: list[Matrix2] = []
    p = 3
    for a in range(p):
        for b in range(p):
            for c in range(p):
                for d in range(p):
                    m = Matrix2(a, b, c, d, p)
                    if m.det == 1:
                        elements.append(m)
    return elements


def get_sp2_f3_multiplication_table() -> list[list[int]]:
    """Generate the full 24x24 Cayley multiplication table for Sp(2, F_3) =~ SL(2, F_3).

    Returns a 24x24 table where table[i][j] is the index of element_i * element_j.
    """
    elements = build_sp2_f3_elements()
    rev = {m: idx for idx, m in enumerate(elements)}
    table: list[list[int]] = []
    for m1 in elements:
        row: list[int] = []
        for m2 in elements:
            prod = m1.matmul(m2)
            if prod not in rev:
                raise RuntimeError(f"Multiplication closure failed for Sp(2, F_3): {m1} * {m2}")
            row.append(rev[prod])
        table.append(row)
    return table


def get_sp2_f3_generators() -> tuple[Matrix2, Matrix2]:
    """Generators H_3 and S_3 for Sp(2, F_3)."""
    h3 = Matrix2(0, 2, 1, 0, 3)
    s3 = Matrix2(1, 0, 1, 1, 3)
    return h3, s3


def generate_group_from_generators(generators: list[Matrix2]) -> list[Matrix2]:
    """Generate finite group by closing under matrix multiplication."""
    if not generators:
        return []
    p = generators[0].p
    identity = Matrix2(1, 0, 0, 1, p)
    frontier = set(generators) | {identity}
    all_elements = set(frontier)

    while frontier:
        next_frontier: set[Matrix2] = set()
        for g in frontier:
            for h in generators:
                gh = g.matmul(h)
                if gh not in all_elements:
                    all_elements.add(gh)
                    next_frontier.add(gh)
        frontier = next_frontier

    return sorted(
        list(all_elements), key=lambda m: (m.a, m.b, m.c, m.d)
    )


def compute_order_spectrum(elements: list[Matrix2]) -> dict[int, int]:
    """Compute histogram of element orders across a finite matrix group."""
    spectrum: dict[int, int] = {}
    for m in elements:
        ord_m = m.order()
        spectrum[ord_m] = spectrum.get(ord_m, 0) + 1
    return dict(sorted(spectrum.items()))


def eastin_knill_obstruction_analysis(dimension_p: int) -> dict[str, Any]:
    """Analyze the Eastin-Knill finite quotient obstruction for a single carrier.

    Transversal operations generate a subgroup of the symplectic quotient Sp(2, F_p).
    Because the quotient order p*(p^2 - 1) is strictly finite, transversal gates
    fail to densely cover the continuous Lie group SU(d), which has positive dimension d^2 - 1.
    """
    p = dimension_p
    group_order = p * (p * p - 1)
    lie_dimension = p * p - 1

    return {
        "dimension_p": p,
        "symplectic_quotient_order": group_order,
        "continuous_carrier_lie_dimension": lie_dimension,
        "is_finite_group": True,
        "dense_covering_obstructed": True,
        "discrete_quotient_classification": f"Sp(2, F_{p})",
        "description": (
            f"Transversal operations on dimension {p} carriers quotient to "
            f"Sp(2, F_{p}) of finite order {group_order}. "
            f"This finite group forms a zero-dimensional discrete subset of "
            f"the continuous {lie_dimension}-dimensional group SU({p}), "
            f"algebraically precluding dense approximation without additional non-transversal resources."
        ),
    }
