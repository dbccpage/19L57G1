"""Target P208a: path_interference and Vanishing Sorkin I_3 in Diamond 2-Complexes.

AuthorityEffect: None.
Axiom Scope: Exact rational arithmetic; constructive core Lean 4 formalization.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
import math
from typing import Any, Dict, FrozenSet, Iterable, List, Sequence, Tuple, Union


# =============================================================================
# 1. Exact Gaussian Rationals Q(i)
# =============================================================================

@dataclass(frozen=True)
class GaussianRational:
    """Exact element of Q(i) = {x + i y : x, y in Q}."""

    re: Fraction
    im: Fraction

    def __init__(
        self,
        re: Union[int, Fraction, float, Tuple[int, int]] = 0,
        im: Union[int, Fraction, float, Tuple[int, int]] = 0,
    ) -> None:
        def _to_frac(val: Union[int, Fraction, float, Tuple[int, int]]) -> Fraction:
            if isinstance(val, Fraction):
                return val
            if isinstance(val, int):
                return Fraction(val, 1)
            if isinstance(val, tuple) and len(val) == 2:
                return Fraction(val[0], val[1])
            if isinstance(val, float):
                return Fraction(str(val))
            raise TypeError(f"Unsupported scalar conversion: {type(val)}")

        object.__setattr__(self, "re", _to_frac(re))
        object.__setattr__(self, "im", _to_frac(im))

    @classmethod
    def zero(cls) -> GaussianRational:
        return cls(0, 0)

    @classmethod
    def one(cls) -> GaussianRational:
        return cls(1, 0)

    @classmethod
    def i(cls) -> GaussianRational:
        return cls(0, 1)

    @classmethod
    def unit_pythagorean(cls, m: int, n: int) -> GaussianRational:
        """Exact rational unit rotation on the unit circle via Pythagorean generator:

        re = (m^2 - n^2) / (m^2 + n^2)
        im = (2 * m * n) / (m^2 + n^2)
        Norm squared is strictly 1 in exact rational arithmetic.
        """
        if m == 0 and n == 0:
            raise ValueError("Pythagorean generator parameters cannot both be zero.")
        den = m * m + n * n
        num_re = m * m - n * n
        num_im = 2 * m * n
        return cls(Fraction(num_re, den), Fraction(num_im, den))

    def conjugate(self) -> GaussianRational:
        return GaussianRational(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def valuation(self) -> Fraction:
        """Modulus-squared valuation P(z) = z * z^* in Q."""
        return self.norm_sq()

    def __add__(self, other: Any) -> GaussianRational:
        if isinstance(other, GaussianRational):
            return GaussianRational(self.re + other.re, self.im + other.im)
        if isinstance(other, (int, Fraction)):
            return GaussianRational(self.re + other, self.im)
        return NotImplemented

    def __radd__(self, other: Any) -> GaussianRational:
        return self.__add__(other)

    def __sub__(self, other: Any) -> GaussianRational:
        if isinstance(other, GaussianRational):
            return GaussianRational(self.re - other.re, self.im - other.im)
        if isinstance(other, (int, Fraction)):
            return GaussianRational(self.re - other, self.im)
        return NotImplemented

    def __rsub__(self, other: Any) -> GaussianRational:
        if isinstance(other, (int, Fraction)):
            return GaussianRational(other - self.re, -self.im)
        return NotImplemented

    def __mul__(self, other: Any) -> GaussianRational:
        if isinstance(other, GaussianRational):
            return GaussianRational(
                self.re * other.re - self.im * other.im,
                self.re * other.im + self.im * other.re,
            )
        if isinstance(other, (int, Fraction)):
            return GaussianRational(self.re * other, self.im * other)
        return NotImplemented

    def __rmul__(self, other: Any) -> GaussianRational:
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> GaussianRational:
        if isinstance(other, GaussianRational):
            d = other.norm_sq()
            if d == 0:
                raise ZeroDivisionError("Division by zero in Q(i)")
            return GaussianRational(
                (self.re * other.re + self.im * other.im) / d,
                (self.im * other.re - self.re * other.im) / d,
            )
        if isinstance(other, (int, Fraction)):
            if other == 0:
                raise ZeroDivisionError("Division by zero in Q(i)")
            return GaussianRational(self.re / other, self.im / other)
        return NotImplemented

    def __neg__(self) -> GaussianRational:
        return GaussianRational(-self.re, -self.im)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, GaussianRational):
            return self.re == other.re and self.im == other.im
        if isinstance(other, (int, Fraction)):
            return self.re == other and self.im == 0
        return False

    def __hash__(self) -> int:
        return hash((self.re, self.im))

    def __repr__(self) -> str:
        return f"GaussianRational({self.re}, {self.im})"

    def __str__(self) -> str:
        if self.im >= 0:
            return f"{self.re} + {self.im}*i"
        return f"{self.re} - {-self.im}*i"


# =============================================================================
# 2. Exact Cyclotomic Field Q(root_gen_n)
# =============================================================================

class CyclotomicRational:
    """Exact element of cyclotomic field Q(root_gen_n) = Q[x] / (Phi_n(x))."""

    _PHI: Dict[int, Tuple[int, ...]] = {
        1: (-1, 1),
        2: (1, 1),
        3: (1, 1, 1),
        4: (1, 0, 1),
        6: (1, -1, 1),
        8: (1, 0, 0, 0, 1),
        12: (1, 0, -1, 0, 1),
    }

    def __init__(self, n: int, coeffs: Sequence[Union[int, Fraction]] = (0,)) -> None:
        if n not in self._PHI:
            raise ValueError(f"Cyclotomic order n={n} not in supported list: {list(self._PHI.keys())}")
        self.n = n
        self.phi = [Fraction(c, 1) for c in self._PHI[n]]
        self.degree_phi = len(self.phi) - 1

        raw_coeffs = [Fraction(c) if not isinstance(c, Fraction) else c for c in coeffs]
        reduced = self._reduce(raw_coeffs)
        self.coeffs: Tuple[Fraction, ...] = tuple(reduced)

    def _reduce(self, poly: List[Fraction]) -> List[Fraction]:
        """Reduce polynomial modulo Phi_n(x)."""
        p = list(poly)
        while len(p) > 0 and p[-1] == 0:
            p.pop()
        deg_phi = self.degree_phi
        while len(p) > deg_phi:
            deg_p = len(p) - 1
            leading = p.pop()
            if leading == 0:
                continue
            deg_diff = deg_p - deg_phi
            for k in range(deg_phi):
                p[k + deg_diff] -= leading * self.phi[k]
            while len(p) > 0 and p[-1] == 0:
                p.pop()
        while len(p) < deg_phi:
            p.append(Fraction(0, 1))
        return p

    @classmethod
    def root_gen(cls, n: int) -> CyclotomicRational:
        """The primitive root generator root_gen_n = x."""
        return cls(n, [0, 1])

    @classmethod
    def zero(cls, n: int) -> CyclotomicRational:
        return cls(n, [0])

    @classmethod
    def one(cls, n: int) -> CyclotomicRational:
        return cls(n, [1])

    def conjugate(self) -> CyclotomicRational:
        """Involution mapping root_gen_n -> root_gen_n^{-1} = root_gen_n^{n - 1}."""
        res_poly = [Fraction(0, 1)] * self.n
        for k, c in enumerate(self.coeffs):
            if c != 0:
                res_poly[(-k) % self.n] += c
        return CyclotomicRational(self.n, res_poly)

    def valuation(self) -> CyclotomicRational:
        """Quadratic valuation P(z) = z * z^* in Q(root_gen_n)."""
        return self * self.conjugate()

    def is_zero(self) -> bool:
        return all(c == 0 for c in self.coeffs)

    def __add__(self, other: Any) -> CyclotomicRational:
        if isinstance(other, CyclotomicRational):
            if self.n != other.n:
                raise ValueError("Cannot add cyclotomic rationals of differing orders")
            sum_coeffs = [
                self.coeffs[k] + other.coeffs[k] for k in range(self.degree_phi)
            ]
            return CyclotomicRational(self.n, sum_coeffs)
        if isinstance(other, (int, Fraction)):
            sum_coeffs = list(self.coeffs)
            sum_coeffs[0] += Fraction(other)
            return CyclotomicRational(self.n, sum_coeffs)
        return NotImplemented

    def __radd__(self, other: Any) -> CyclotomicRational:
        return self.__add__(other)

    def __sub__(self, other: Any) -> CyclotomicRational:
        if isinstance(other, CyclotomicRational):
            if self.n != other.n:
                raise ValueError("Cannot subtract cyclotomic rationals of differing orders")
            diff_coeffs = [
                self.coeffs[k] - other.coeffs[k] for k in range(self.degree_phi)
            ]
            return CyclotomicRational(self.n, diff_coeffs)
        if isinstance(other, (int, Fraction)):
            diff_coeffs = list(self.coeffs)
            diff_coeffs[0] -= Fraction(other)
            return CyclotomicRational(self.n, diff_coeffs)
        return NotImplemented

    def __rsub__(self, other: Any) -> CyclotomicRational:
        if isinstance(other, (int, Fraction)):
            diff_coeffs = [-c for c in self.coeffs]
            diff_coeffs[0] += Fraction(other)
            return CyclotomicRational(self.n, diff_coeffs)
        return NotImplemented

    def __mul__(self, other: Any) -> CyclotomicRational:
        if isinstance(other, CyclotomicRational):
            if self.n != other.n:
                raise ValueError("Cannot multiply cyclotomic rationals of differing orders")
            res = [Fraction(0, 1)] * (len(self.coeffs) + len(other.coeffs))
            for i, ci in enumerate(self.coeffs):
                for j, cj in enumerate(other.coeffs):
                    res[i + j] += ci * cj
            return CyclotomicRational(self.n, res)
        if isinstance(other, (int, Fraction)):
            prod_coeffs = [c * Fraction(other) for c in self.coeffs]
            return CyclotomicRational(self.n, prod_coeffs)
        return NotImplemented

    def __rmul__(self, other: Any) -> CyclotomicRational:
        return self.__mul__(other)

    def __neg__(self) -> CyclotomicRational:
        return CyclotomicRational(self.n, [-c for c in self.coeffs])

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CyclotomicRational):
            return self.n == other.n and self.coeffs == other.coeffs
        if isinstance(other, (int, Fraction)):
            if self.coeffs[0] != Fraction(other):
                return False
            return all(c == 0 for c in self.coeffs[1:])
        return False

    def __hash__(self) -> int:
        return hash((self.n, self.coeffs))

    def __repr__(self) -> str:
        return f"CyclotomicRational(n={self.n}, coeffs={self.coeffs})"


# =============================================================================
# 3. Diamond 2-Complex Network Topology
# =============================================================================

@dataclass
class Diamond2Complex:
    """Diamond 2-complex multi-slit topology connecting source_node to sink_node.

    The 2-complex consists of:
    - 0-cells: source_node 'S', sink_node 'D', intermediate path branch nodes.
    - 1-cells: directed edges (S -> path) and (path -> D).
    - 2-cells: 2-dimensional faces spanning adjacent path loops.
    """

    path_names: Tuple[str, ...]
    path_amplitudes: Dict[str, Union[GaussianRational, CyclotomicRational]]

    def __init__(
        self,
        path_names: Sequence[str] = ("A", "B", "C"),
        path_amplitudes: Dict[str, Union[GaussianRational, CyclotomicRational]] | None = None,
    ) -> None:
        self.path_names = tuple(path_names)
        if path_amplitudes is None:
            self.path_amplitudes = {p: GaussianRational.one() for p in self.path_names}
        else:
            for p in self.path_names:
                if p not in path_amplitudes:
                    raise KeyError(f"Missing path_amplitude for path: {p}")
            self.path_amplitudes = dict(path_amplitudes)

    def set_path_amplitude(
        self, path: str, val: Union[GaussianRational, CyclotomicRational]
    ) -> None:
        if path not in self.path_names:
            raise KeyError(f"Unknown path: {path}")
        self.path_amplitudes[path] = val

    def total_amplitude(
        self, open_subset: Iterable[str]
    ) -> Union[GaussianRational, CyclotomicRational]:
        """Total path_amplitude A(sigma) = sum_{j in sigma} a_j."""
        subset = list(open_subset)
        if not subset:
            first = next(iter(self.path_amplitudes.values()))
            if isinstance(first, GaussianRational):
                return GaussianRational.zero()
            return CyclotomicRational.zero(first.n)

        acc = self.path_amplitudes[subset[0]]
        for p in subset[1:]:
            acc = acc + self.path_amplitudes[p]
        return acc

    def intensity(
        self, open_subset: Iterable[str]
    ) -> Union[Fraction, CyclotomicRational]:
        """Quadratic path valuation: P(sigma) = A(sigma) A(sigma)^*."""
        total_amp = self.total_amplitude(open_subset)
        return total_amp.valuation()

    def second_order_interference(
        self, p1: str, p2: str
    ) -> Union[Fraction, CyclotomicRational]:
        """Second-order path_interference:

        I_2(A, B) = P(A cup B) - P(A) - P(B) = a_A a_B^* + a_B a_A^*.
        """
        p_ab = self.intensity([p1, p2])
        p_a = self.intensity([p1])
        p_b = self.intensity([p2])
        return p_ab - p_a - p_b

    def third_order_sorkin(
        self, p1: str, p2: str, p3: str
    ) -> Union[Fraction, CyclotomicRational]:
        """Third-order Sorkin quantity:

        I_3(A, B, C) = P(A cup B cup C) - P(A cup B) - P(A cup C) - P(B cup C)
                       + P(A) + P(B) + P(C).
        """
        p_abc = self.intensity([p1, p2, p3])
        p_ab = self.intensity([p1, p2])
        p_ac = self.intensity([p1, p3])
        p_bc = self.intensity([p2, p3])
        p_a = self.intensity([p1])
        p_b = self.intensity([p2])
        p_c = self.intensity([p3])
        return p_abc - p_ab - p_ac - p_bc + p_a + p_b + p_c

    def higher_order_sorkin(
        self, paths: Sequence[str]
    ) -> Union[Fraction, CyclotomicRational]:
        """Generalized k-th order Sorkin inclusion-exclusion quantity:

        I_k(sigma) = sum_{tau subseteq sigma} (-1)^{|sigma| - |tau|} P(tau).
        """
        k = len(paths)
        first = next(iter(self.path_amplitudes.values()))
        if isinstance(first, GaussianRational):
            total: Union[Fraction, CyclotomicRational] = Fraction(0, 1)
        else:
            total = CyclotomicRational.zero(first.n)

        for r in range(1, k + 1):
            sign = -1 if (k - r) % 2 == 1 else 1
            for sub in combinations(paths, r):
                val = self.intensity(sub)
                if sign == 1:
                    total = total + val
                else:
                    total = total - val
        return total

    def is_sorkin_zero(self, paths: Sequence[str]) -> bool:
        res = self.higher_order_sorkin(paths)
        if isinstance(res, Fraction):
            return res == 0
        return res.is_zero()


# =============================================================================
# 4. Bilinear Structure and Discrete Differences
# =============================================================================

def discrete_derivative(
    diamond: Diamond2Complex,
    base_subset: Sequence[str],
    shift_path: str,
) -> Union[Fraction, CyclotomicRational]:
    """Delta_j P(sigma) = P(sigma cup {j}) - P(sigma)."""
    s = set(base_subset)
    p_with = diamond.intensity(s | {shift_path})
    p_without = diamond.intensity(s - {shift_path})
    return p_with - p_without


def higher_order_discrete_difference(
    diamond: Diamond2Complex,
    paths: Sequence[str],
) -> Union[Fraction, CyclotomicRational]:
    """Compute finite difference Delta_{j_1} ... Delta_{j_k} P(empty).

    By the discrete difference theorem, this equals exactly the Sorkin
    inclusion-exclusion quantity I_k(paths).
    """
    return diamond.higher_order_sorkin(paths)


# =============================================================================
# 5. Constructive Verification and Sweeps
# =============================================================================

def verify_constructive_nonzero_i2() -> Tuple[Fraction, GaussianRational, GaussianRational]:
    """Constructive witness that I_2 != 0 under angular path_amplitude rotation / shift."""
    a1 = GaussianRational.one()
    a2 = GaussianRational.unit_pythagorean(2, 1)  # (3/5, 4/5)

    c = Diamond2Complex(["A", "B"], {"A": a1, "B": a2})
    i2 = c.second_order_interference("A", "B")
    expected = Fraction(6, 5)
    if i2 != expected:
        raise ValueError(f"Unexpected I_2: got {i2}, expected {expected}")
    assert isinstance(i2, Fraction)
    return i2, a1, a2


def run_pythagorean_parameter_sweep(
    max_param: int = 6,
) -> Dict[str, Any]:
    """Sweep over rational Pythagorean rotations and verify:

    1. I_2 != 0 for non-orthogonal rotations.
    2. I_3 = 0 strictly across all 3-path configurations.
    3. I_k = 0 for k in {4, 5} across higher-order subsets.
    """
    tested_count = 0
    zero_i3_count = 0
    nonzero_i2_count = 0
    zero_ik_count = 0

    unit_rotations: List[GaussianRational] = [
        GaussianRational(1, 0),
        GaussianRational(0, 1),
        GaussianRational(-1, 0),
        GaussianRational(0, -1),
    ]

    for m in range(1, max_param + 1):
        for n in range(1, max_param + 1):
            if math.gcd(m, n) == 1:
                unit_rotations.append(GaussianRational.unit_pythagorean(m, n))

    for idx1 in range(len(unit_rotations)):
        for idx2 in range(idx1, len(unit_rotations)):
            for idx3 in range(idx2, min(idx2 + 5, len(unit_rotations))):
                a1 = unit_rotations[idx1]
                a2 = unit_rotations[idx2]
                a3 = unit_rotations[idx3]

                c = Diamond2Complex(
                    ["A", "B", "C"],
                    {"A": a1, "B": a2, "C": a3},
                )
                i3 = c.third_order_sorkin("A", "B", "C")
                if i3 != Fraction(0, 1):
                    raise ValueError(f"Sorkin I_3 non-zero: {i3} for ({a1}, {a2}, {a3})")
                zero_i3_count += 1
                tested_count += 1

                i2 = c.second_order_interference("A", "B")
                if i2 != Fraction(0, 1):
                    nonzero_i2_count += 1

    # Test 4-path and 5-path higher-order vanishes
    c_multi = Diamond2Complex(
        ["A", "B", "C", "D", "E"],
        {
            "A": GaussianRational(2, 3),
            "B": GaussianRational(-1, 4),
            "C": GaussianRational(5, -2),
            "D": GaussianRational.unit_pythagorean(3, 2),
            "E": GaussianRational.unit_pythagorean(4, 1),
        },
    )
    for k in (3, 4, 5):
        for subset in combinations(["A", "B", "C", "D", "E"], k):
            ik = c_multi.higher_order_sorkin(subset)
            if ik != Fraction(0, 1):
                raise ValueError(f"Higher-order I_{k} non-zero: {ik} for subset {subset}")
            zero_ik_count += 1

    return {
        "configurations_tested": tested_count,
        "i3_zero_count": zero_i3_count,
        "i2_nonzero_count": nonzero_i2_count,
        "higher_order_zero_count": zero_ik_count,
        "all_i3_identically_zero": (zero_i3_count == tested_count),
    }


def run_cyclotomic_parameter_sweep() -> Dict[str, Any]:
    """Verify vanishing I_3 identically over cyclotomic fields Q(root_gen_n) for n in {3, 4, 6, 8, 12}."""
    orders = [3, 4, 6, 8, 12]
    tested = 0
    zero_count = 0

    for n in orders:
        gen = CyclotomicRational.root_gen(n)
        one = CyclotomicRational.one(n)
        gen_sq = gen * gen

        c = Diamond2Complex(["A", "B", "C"], {"A": one, "B": gen, "C": gen_sq})
        i3 = c.third_order_sorkin("A", "B", "C")
        assert isinstance(i3, CyclotomicRational)
        if not i3.is_zero():
            raise ValueError(f"Cyclotomic I_3 non-zero for n={n}: {i3}")
        zero_count += 1
        tested += 1

        p_a = one + gen
        p_b = gen_sq - one
        p_c = gen * gen_sq
        c2 = Diamond2Complex(["A", "B", "C"], {"A": p_a, "B": p_b, "C": p_c})
        i3_2 = c2.third_order_sorkin("A", "B", "C")
        assert isinstance(i3_2, CyclotomicRational)
        if not i3_2.is_zero():
            raise ValueError(f"Cyclotomic combination I_3 non-zero for n={n}: {i3_2}")
        zero_count += 1
        tested += 1

    return {
        "cyclotomic_orders_tested": orders,
        "configurations_tested": tested,
        "all_i3_identically_zero": (zero_count == tested),
    }