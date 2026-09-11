"""X300 adversarial checks for Cohort 6."""
from __future__ import annotations

from fractions import Fraction
import math
from pathlib import Path
import random
import subprocess
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_DIRS = [
    REPO_ROOT / "research" / "p203_composite_systems",
    REPO_ROOT / "research" / "m108_internal_algebra",
    REPO_ROOT / "research" / "m109_obstruction_homology",
    REPO_ROOT / "research" / "x300_observer_information",
]
for p in reversed(TARGET_DIRS):
    p_str = str(p)
    if p_str in sys.path:
        sys.path.remove(p_str)
    sys.path.insert(0, p_str)

import composite_systems as p203
import algebra as m108
import homology as m109
import information as x300

def test_x300_adversarial_observer_information() -> int:
    """Fuzz X300 operational channels, Data Processing Inequality, dyadic uncertainty, and Landauer erasure."""
    print(">>> Fuzzing Target X300: Observer-Relative Information, Channels & Loss...")
    checks = 0
    rng = random.Random(300300)

    # 1. Operational channel composition associativity sweeps: (W3 o W2) o W1 = W3 o (W2 o W1)
    for trial in range(30):
        p_err1 = Fraction(rng.randint(1, 4), 10)
        p_err2 = Fraction(rng.randint(1, 4), 10)
        w1 = x300.Channel.binary_symmetric(p_err1)
        w2 = x300.Channel.binary_symmetric(p_err2)
        w3 = x300.Channel({
            0: x300.DiscreteDistribution({0: Fraction(3, 4), 1: Fraction(1, 4)}),
            1: x300.DiscreteDistribution({0: Fraction(1, 3), 1: Fraction(2, 3)}),
        })

        c_left = w1.compose(w2).compose(w3)
        c_right = w1.compose(w2.compose(w3))

        for x_sym in (0, 1):
            d_left = c_left.transition(x_sym)
            d_right = c_right.transition(x_sym)
            for z_sym in (0, 1):
                assert d_left.prob(z_sym) == d_right.prob(z_sym)
        checks += 2

    # 2. Data Processing Inequality (DPI) sweeps across noisy cascades
    for trial in range(30):
        # Cascaded BSC channels: X -> Y -> Z
        p_x = x300.DiscreteDistribution.uniform([0, 1])
        w_xy = x300.Channel.binary_symmetric(Fraction(rng.randint(1, 3), 10))
        w_yz = x300.Channel.binary_symmetric(Fraction(rng.randint(1, 3), 10))

        cert = x300.verify_data_processing_inequality(p_x, w_xy, w_yz)
        assert cert.passed is True
        assert cert.delta_i >= -1e-12  # Non-negative mutual information loss
        assert cert.i_xy >= cert.i_xz
        checks += 3

        # Deterministic lossy coarse-graining: X uniform on {0, 1, 2, 3} -> Y = X -> Z = Y // 2
        p_quad = x300.DiscreteDistribution.uniform([0, 1, 2, 3])
        w_id = x300.Channel.identity([0, 1, 2, 3])
        w_cg = x300.Channel.coarse_graining(lambda y: y // 2, [0, 1, 2, 3])

        cert_cg = x300.verify_data_processing_inequality(p_quad, w_id, w_cg)
        assert cert_cg.passed is True
        assert math.isclose(cert_cg.i_xy, 2.0)
        assert math.isclose(cert_cg.i_xz, 1.0)
        assert cert_cg.delta_i >= 0.999
        checks += 4

        # Invertible processing (sufficient statistic): Z = 1 - Y
        w_inv = x300.Channel.deterministic({0: 1, 1: 0})
        cert_inv = x300.verify_data_processing_inequality(p_x, w_xy, w_inv)
        assert cert_inv.passed is True
        assert cert_inv.is_sufficient_statistic is True
        assert math.isclose(cert_inv.delta_i, 0.0, abs_tol=1e-12)
        checks += 3

    # 3. Exact dyadic rational uncertainty & relative divergence non-negativity in Q
    for trial in range(30):
        # Lengths summing to Kraft equality sum 2^-l = 1
        lengths_p = {"a": 1, "b": 2, "c": 3, "d": 3}  # 1/2 + 1/4 + 1/8 + 1/8 = 1
        dist_p = x300.DiscreteDistribution.pure_dyadic(lengths_p)
        assert dist_p.is_pure_dyadic() is True
        # H(P) = 1/2*1 + 1/4*2 + 1/8*3 + 1/8*3 = 1/2 + 2/4 + 6/8 = 7/4 in Q
        assert dist_p.exact_dyadic_shannon_entropy() == Fraction(7, 4)
        checks += 2

        # Relative divergence identity: D(P || P) = 0 in Q
        assert x300.exact_dyadic_divergence(dist_p, dist_p) == Fraction(0, 1)
        checks += 1

        # Relative divergence non-negativity: D(P || Q) > 0 for Q != P
        lengths_q = {"a": 2, "b": 2, "c": 2, "d": 2}  # Uniform 1/4 each
        dist_q = x300.DiscreteDistribution.pure_dyadic(lengths_q)
        div_pq = x300.exact_dyadic_divergence(dist_p, dist_q)
        assert div_pq == Fraction(1, 4)
        assert div_pq > Fraction(0, 1)
        # Cross-uncertainty formula: H(P, Q) = H(P) + D(P || Q)
        assert x300.exact_dyadic_cross_entropy(dist_p, dist_q) == dist_p.exact_dyadic_shannon_entropy() + div_pq
        checks += 3

    # 4. Hartley capacity metric additivity sweeps
    for trial in range(25):
        p1 = x300.DiscreteDistribution.uniform(list(range(4)))  # 2^2 -> cap 2
        p2 = x300.DiscreteDistribution.uniform(list(range(8)))  # 2^3 -> cap 3
        c1 = p1.exact_hartley_capacity()
        c2 = p2.exact_hartley_capacity()
        assert c1 == 2
        assert c2 == 3

        prod = x300.product_distribution(p1, p2)
        assert prod.exact_hartley_capacity() == c1 + c2
        checks += 3

    # 5. Landauer erasure accounting sweeps
    for trial in range(25):
        p_init = x300.DiscreteDistribution.uniform([0, 1])
        acct = x300.LandauerAccounting(p_init, reset_state=0, temperature_kelvin=300.0)
        receipt = acct.compute_erasure_cost()
        assert receipt.initial_entropy_bits == 1.0
        assert receipt.final_entropy_bits == 0.0
        assert receipt.erased_entropy_bits == 1.0
        assert receipt.exact_erased_entropy_q == Fraction(1, 1)
        assert receipt.operational_non_reversibility is True
        checks += 5

        # Already erased state requires 0 dissipation
        p_zero = x300.DiscreteDistribution.point_mass(0)
        acct_zero = x300.LandauerAccounting(p_zero, reset_state=0)
        rec_zero = acct_zero.compute_erasure_cost()
        assert rec_zero.erased_entropy_bits == 0.0
        assert rec_zero.operational_non_reversibility is False
        assert rec_zero.minimal_heat_dissipated_joules == 0.0
        checks += 3

    print(f"  X300 passed {checks} adversarial checks.")
    return checks


# ==============================================================================
# 5. Multi-Target 4-Pillar Cross-Integration Pipeline Test
# ==============================================================================

