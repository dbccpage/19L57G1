"""Exact rational bipartite correlations, Bell-CHSH bounds, and Cabello 18-ray contextuality.

AuthorityEffect: None.

All computations use exact rational arithmetic via fractions.Fraction.
No continuous approximations or numerical floats are admitted.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import itertools
from typing import Callable, Mapping, Sequence


# ============================================================================
# Section 1: Bipartite Bell-CHSH Scenario
# ============================================================================

INPUTS_X: tuple[int, ...] = (0, 1)
INPUTS_Y: tuple[int, ...] = (0, 1)
OUTPUTS_A: tuple[int, ...] = (1, -1)
OUTPUTS_B: tuple[int, ...] = (1, -1)


@dataclass(frozen=True)
class DeterministicStrategy:
    """Deterministic local response functions for Alice and Bob.

    Alice responds to input x in {0, 1} with a in {+1, -1}.
    Bob responds to input y in {0, 1} with b in {+1, -1}.
    """

    alice: tuple[int, int]  # (A(0), A(1))
    bob: tuple[int, int]    # (B(0), B(1))

    def evaluate(self, x: int, y: int) -> int:
        """Return outcome product A(x) * B(y)."""
        return self.alice[x] * self.bob[y]

    def correlator(self) -> int:
        """Compute CHSH correlator S = E(0,0) + E(0,1) + E(1,0) - E(1,1)."""
        e00 = self.evaluate(0, 0)
        e01 = self.evaluate(0, 1)
        e10 = self.evaluate(1, 0)
        e11 = self.evaluate(1, 1)
        return e00 + e01 + e10 - e11


def generate_all_deterministic_strategies() -> list[DeterministicStrategy]:
    """Enumerate all 16 deterministic local response pairs."""
    strategies: list[DeterministicStrategy] = []
    outcomes = (1, -1)
    for a0, a1 in itertools.product(outcomes, repeat=2):
        for b0, b1 in itertools.product(outcomes, repeat=2):
            strategies.append(
                DeterministicStrategy(alice=(a0, a1), bob=(b0, b1))
            )
    return strategies


def verify_deterministic_lhv_bounds() -> dict[str, int]:
    """Verify |S| <= 2 for every deterministic strategy.

    Returns census of outcomes showing all values lie in {-2, 2}.
    """
    strategies = generate_all_deterministic_strategies()
    counts: dict[str, int] = {"plus_2": 0, "minus_2": 0, "other": 0}
    for strat in strategies:
        val = strat.correlator()
        if val == 2:
            counts["plus_2"] += 1
        elif val == -2:
            counts["minus_2"] += 1
        else:
            counts["other"] += 1
    return counts


@dataclass(frozen=True)
class ConvexLHVModel:
    """Convex combination of local deterministic strategies.

    weights p_i >= 0, sum p_i = 1.
    """

    strategies: tuple[DeterministicStrategy, ...]
    weights: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if len(self.strategies) != len(self.weights):
            raise ValueError("Strategy count must match weight count")
        if any(w < 0 for w in self.weights):
            raise ValueError("Weights must be non-negative")
        if sum(self.weights) != Fraction(1, 1):
            raise ValueError("Weights must sum to 1")

    def expectation(self, x: int, y: int) -> Fraction:
        """Compute convex expectation value E(x, y)."""
        return sum(
            w * Fraction(s.evaluate(x, y), 1)
            for s, w in zip(self.strategies, self.weights)
        )

    def chsh_correlator(self) -> Fraction:
        """Compute CHSH correlator S = E(0,0) + E(0,1) + E(1,0) - E(1,1)."""
        return sum(
            w * Fraction(s.correlator(), 1)
            for s, w in zip(self.strategies, self.weights)
        )


# ============================================================================
# Section 2: Joint Probability Tables and No-Signaling
# ============================================================================

@dataclass(frozen=True)
class JointProbabilityTable:
    """Joint conditional probability distribution P(a, b | x, y) in Q."""

    table: dict[tuple[int, int, int, int], Fraction]

    def get(self, a: int, b: int, x: int, y: int) -> Fraction:
        """Retrieve probability P(a, b | x, y)."""
        return self.table.get((a, b, x, y), Fraction(0, 1))

    def is_valid_distribution(self) -> bool:
        """Check non-negativity and normalization for every input pair (x, y)."""
        for x in INPUTS_X:
            for y in INPUTS_Y:
                prob_sum = Fraction(0, 1)
                for a in OUTPUTS_A:
                    for b in OUTPUTS_B:
                        p = self.get(a, b, x, y)
                        if p < 0:
                            return False
                        prob_sum += p
                if prob_sum != Fraction(1, 1):
                    return False
        return True

    def marginal_alice(self, a: int, x: int, y: int) -> Fraction:
        """Compute Alice marginal P_A(a | x, y) = sum_b P(a, b | x, y)."""
        return sum(self.get(a, b, x, y) for b in OUTPUTS_B)

    def marginal_bob(self, b: int, x: int, y: int) -> Fraction:
        """Compute Bob marginal P_B(b | x, y) = sum_a P(a, b | x, y)."""
        return sum(self.get(a, b, x, y) for a in OUTPUTS_A)

    def is_no_signaling(self) -> bool:
        """Verify marginals are independent of the other party's input."""
        # Alice marginal independent of Bob's input y
        for x in INPUTS_X:
            for a in OUTPUTS_A:
                if self.marginal_alice(a, x, 0) != self.marginal_alice(a, x, 1):
                    return False
        # Bob marginal independent of Alice's input x
        for y in INPUTS_Y:
            for b in OUTPUTS_B:
                if self.marginal_bob(b, 0, y) != self.marginal_bob(b, 1, y):
                    return False
        return True

    def expectation(self, x: int, y: int) -> Fraction:
        """Compute expectation value E(x, y) = sum_{a, b} a * b * P(a, b | x, y)."""
        total = Fraction(0, 1)
        for a in OUTPUTS_A:
            for b in OUTPUTS_B:
                total += Fraction(a * b, 1) * self.get(a, b, x, y)
        return total

    def chsh_correlator(self) -> Fraction:
        """Compute CHSH correlator S = E(0,0) + E(0,1) + E(1,0) - E(1,1)."""
        e00 = self.expectation(0, 0)
        e01 = self.expectation(0, 1)
        e10 = self.expectation(1, 0)
        e11 = self.expectation(1, 1)
        return e00 + e01 + e10 - e11


def make_correlation_table(
    e00: Fraction, e01: Fraction, e10: Fraction, e11: Fraction
) -> JointProbabilityTable:
    """Construct symmetric non-signaling probability table from expectation values.

    For unbiased marginals P_A(a|x) = 1/2 and P_B(b|y) = 1/2:
    P(a, b | x, y) = (1 + a * b * E(x, y)) / 4.
    """
    e_dict = {(0, 0): e00, (0, 1): e01, (1, 0): e10, (1, 1): e11}
    table: dict[tuple[int, int, int, int], Fraction] = {}
    for (x, y), e_val in e_dict.items():
        for a in OUTPUTS_A:
            for b in OUTPUTS_B:
                prob = (Fraction(1, 1) + Fraction(a * b, 1) * e_val) / Fraction(4, 1)
                table[(a, b, x, y)] = prob
    return JointProbabilityTable(table=table)


# ============================================================================
# Section 3: Rational Pythagorean Non-Local Correlator
# ============================================================================

# Pythagorean unit vectors in Q^2 with norm squared = 1:
# Alice vectors:
ALICE_VEC_0: tuple[Fraction, Fraction] = (Fraction(1, 1), Fraction(0, 1))
ALICE_VEC_1: tuple[Fraction, Fraction] = (Fraction(0, 1), Fraction(1, 1))

# Bob vectors:
BOB_VEC_0: tuple[Fraction, Fraction] = (Fraction(4, 5), Fraction(3, 5))
BOB_VEC_1: tuple[Fraction, Fraction] = (Fraction(4, 5), Fraction(-3, 5))


def dot_product_2d(
    u: tuple[Fraction, Fraction], v: tuple[Fraction, Fraction]
) -> Fraction:
    """Inner product of two vectors in Q^2."""
    return u[0] * v[0] + u[1] * v[1]


def pythagorean_model() -> tuple[JointProbabilityTable, Fraction]:
    """Construct rational correlation model from Pythagorean unit vectors.

    Inner products:
      E(0, 0) = a_0 . b_0 = 1*(4/5) + 0*(3/5)  =  4/5
      E(0, 1) = a_0 . b_1 = 1*(4/5) + 0*(-3/5) =  4/5
      E(1, 0) = a_1 . b_0 = 0*(4/5) + 1*(3/5)  =  3/5
      E(1, 1) = a_1 . b_1 = 0*(4/5) + 1*(-3/5) = -3/5

    Correlator:
      S = 4/5 + 4/5 + 3/5 - (-3/5) = 14/5 = 2.8 > 2.
    """
    e00 = dot_product_2d(ALICE_VEC_0, BOB_VEC_0)  # 4/5
    e01 = dot_product_2d(ALICE_VEC_0, BOB_VEC_1)  # 4/5
    e10 = dot_product_2d(ALICE_VEC_1, BOB_VEC_0)  # 3/5
    e11 = dot_product_2d(ALICE_VEC_1, BOB_VEC_1)  # -3/5

    table = make_correlation_table(e00, e01, e10, e11)
    s_val = table.chsh_correlator()
    return table, s_val


def pr_box_model() -> tuple[JointProbabilityTable, Fraction]:
    """Construct maximal algebraic non-signaling box (PR-box).

    P(a, b | x, y) = 1/2 if a * b = (-1)^{x * y} else 0.
    Achieves S = 4.
    """
    table: dict[tuple[int, int, int, int], Fraction] = {}
    for x in INPUTS_X:
        for y in INPUTS_Y:
            target_sign = -1 if (x * y == 1) else 1
            for a in OUTPUTS_A:
                for b in OUTPUTS_B:
                    if a * b == target_sign:
                        table[(a, b, x, y)] = Fraction(1, 2)
                    else:
                        table[(a, b, x, y)] = Fraction(0, 1)
    pt = JointProbabilityTable(table=table)
    return pt, pt.chsh_correlator()


# ============================================================================
# Section 4: Cabello 18-Ray Contextuality Configuration
# ============================================================================

# The 18 discrete rays in Q^4 with coordinates in {-1, 0, 1}
CABELLO_RAYS: tuple[tuple[int, int, int, int], ...] = (
    (1, 1, 1, 1),       # r0
    (1, 1, 1, -1),      # r1
    (1, 1, -1, 1),      # r2
    (1, 1, -1, -1),     # r3
    (1, 0, 1, 0),       # r4
    (1, 0, 0, 1),       # r5
    (1, 0, 0, 0),       # r6
    (1, 0, 0, -1),      # r7
    (1, -1, 0, 0),      # r8
    (1, -1, -1, 1),     # r9
    (1, -1, -1, -1),    # r10
    (0, 1, 0, 1),       # r11
    (0, 1, 0, 0),       # r12
    (0, 1, 0, -1),      # r13
    (0, 1, -1, 0),      # r14
    (0, 0, 1, 1),       # r15
    (0, 0, 1, 0),       # r16
    (0, 0, 1, -1),      # r17
)

# 9 orthogonal contexts of 4 mutually orthogonal rays each
CABELLO_CONTEXTS: tuple[tuple[int, int, int, int], ...] = (
    (0, 3, 8, 17),
    (0, 7, 9, 14),
    (1, 2, 8, 15),
    (1, 5, 10, 14),
    (2, 4, 10, 13),
    (3, 4, 9, 11),
    (5, 7, 12, 16),
    (6, 11, 13, 16),
    (6, 12, 15, 17),
)


def dot_product_4d(
    u: tuple[int, int, int, int], v: tuple[int, int, int, int]
) -> int:
    """Standard Euclidean dot product in Q^4."""
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2] + u[3] * v[3]


def verify_cabello_orthogonality() -> bool:
    """Verify every context contains 4 mutually orthogonal rays."""
    for ctx in CABELLO_CONTEXTS:
        for i in range(4):
            for j in range(i + 1, 4):
                if dot_product_4d(CABELLO_RAYS[ctx[i]], CABELLO_RAYS[ctx[j]]) != 0:
                    return False
    return True


def verify_cabello_incidence() -> dict[int, int]:
    """Verify each ray appears in exactly 2 contexts."""
    counts: dict[int, int] = {i: 0 for i in range(len(CABELLO_RAYS))}
    for ctx in CABELLO_CONTEXTS:
        for ray_idx in ctx:
            counts[ray_idx] += 1
    return counts


def build_cabello_incidence_matrix() -> list[list[int]]:
    """Construct 9 x 18 binary incidence matrix.

    M[k][i] = 1 if ray i is in context k, else 0.
    """
    matrix: list[list[int]] = []
    for ctx in CABELLO_CONTEXTS:
        row = [0] * len(CABELLO_RAYS)
        for r in ctx:
            row[r] = 1
        matrix.append(row)
    return matrix


def evaluate_noncontextual_valuation_obstruction() -> dict[str, object]:
    """Demonstrate the non-contextual valuation parity obstruction.

    A non-contextual valuation assigns v(r) in {0, 1} such that for each
    orthogonal context C_k, sum_{r in C_k} v(r) = 1.

    Summing over all 9 contexts yields:
      sum_{k=0}^8 sum_{r in C_k} v(r) = 9.

    By exact 2-incidence:
      sum_{k=0}^8 sum_{r in C_k} v(r) = 2 * sum_{i=0}^{17} v(r_i).

    This requires 2 * M = 9 for integer M = sum v(r_i), which has no integer solution.
    """
    # 1. Total context count
    num_contexts = len(CABELLO_CONTEXTS)
    # 2. Total ray count
    num_rays = len(CABELLO_RAYS)
    # 3. Ray degree in hypergraph
    inc = verify_cabello_incidence()
    degrees = list(inc.values())
    all_deg_2 = all(d == 2 for d in degrees)

    # 4. Exhaustive search over all 2^18 = 262,144 binary valuations
    valid_valuations_found = 0
    for val in itertools.product((0, 1), repeat=num_rays):
        satisfies_all = True
        for ctx in CABELLO_CONTEXTS:
            if sum(val[r] for r in ctx) != 1:
                satisfies_all = False
                break
        if satisfies_all:
            valid_valuations_found += 1

    return {
        "num_contexts": num_contexts,
        "num_rays": num_rays,
        "total_incidence_slots": num_contexts * 4,
        "each_ray_degree": 2 if all_deg_2 else None,
        "context_sum_target": num_contexts,  # 9
        "parity_contradiction": "2 * M = 9 has no solution in Z",
        "exhaustive_valid_valuations": valid_valuations_found,  # 0
    }


def cech_cochain_parity_obstruction() -> dict[str, int]:
    """Compute mod-2 Čech 1-cochain obstruction in H^1(Z_2).

    Over Z_2:
      sum_k (sum_{r in C_k} v(r)) mod 2 = 9 mod 2 = 1.
      sum_i (2 * v(r_i)) mod 2 = 0.
    The obstruction class evaluates to 1 != 0.
    """
    total_contexts = len(CABELLO_CONTEXTS)
    context_cycle_mod2 = total_contexts % 2  # 9 % 2 = 1
    incidence_degree_mod2 = 2 % 2           # 0
    coboundary_evaluation = (context_cycle_mod2 - incidence_degree_mod2) % 2
    return {
        "context_cycle_mod2": context_cycle_mod2,
        "incidence_degree_mod2": incidence_degree_mod2,
        "coboundary_obstruction_mod2": coboundary_evaluation,
    }
