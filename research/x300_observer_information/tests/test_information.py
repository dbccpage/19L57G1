"""Tests for Target X300: Observer-Relative Information, Channels & Loss.

Verifies:
1. Exact rational arithmetic for dyadic distributions and exact Shannon uncertainty in Q.
2. Exact dyadic relative divergence (Kullback-Leibler divergence) non-negativity and identity.
3. Hartley capacity metric additivity on product alphabets.
4. Operational channel composition, associativity, and fidelity.
5. Data processing inequality (DPI) across diverse operational channels and sufficient statistics.
6. Observer communication protocols, repetition coding, and fidelity calculation.
7. Memory retention limits and monotonic loss under Markovian noise.
8. Landauer operational erasure accounting and thermodynamic lower bounds.
"""

from __future__ import annotations

from fractions import Fraction
import math
import pytest

from information import (
    Channel,
    DiscreteDistribution,
    DistributedObserver,
    LandauerAccounting,
    MemoryRetentionModel,
    OperationalCommunicationProtocol,
    coarse_grain_loss,
    exact_dyadic_cross_entropy,
    exact_dyadic_divergence,
    exact_dyadic_mutual_information,
    marginal_x,
    marginal_y,
    mutual_information,
    product_distribution,
    shannon_divergence,
    verify_data_processing_inequality,
)


class TestDiscreteDistributionAndEntropy:
    """Test exact rational probability and operational uncertainty metrics."""

    def test_uniform_distribution(self) -> None:
        dist = DiscreteDistribution.uniform(["a", "b", "c", "d"])
        assert dist.support() == ("a", "b", "c", "d")
        for sym in ("a", "b", "c", "d"):
            assert dist.prob(sym) == Fraction(1, 4)
        assert dist.prob("unknown") == Fraction(0)
        assert dist.is_dyadic()
        assert dist.is_pure_dyadic()
        assert dist.exact_hartley_capacity() == 2
        assert dist.exact_dyadic_shannon_entropy() == Fraction(2, 1)

    def test_pure_dyadic_non_uniform(self) -> None:
        # P = {s0: 1/2, s1: 1/4, s2: 1/8, s3: 1/8}
        lengths = {"s0": 1, "s1": 2, "s2": 3, "s3": 3}
        dist = DiscreteDistribution.pure_dyadic(lengths)
        assert dist.is_pure_dyadic()
        assert dist.pure_dyadic_lengths() == lengths
        # H(P) = 1/2*1 + 1/4*2 + 1/8*3 + 1/8*3 = 1/2 + 2/4 + 6/8 = 1/2 + 1/2 + 3/4 = 7/4 in Q
        assert dist.exact_dyadic_shannon_entropy() == Fraction(7, 4)
        assert math.isclose(dist.shannon_entropy(), 1.75)

    def test_kraft_inequality_rejection(self) -> None:
        # Sum of 2^-l != 1
        with pytest.raises(ValueError, match="Kraft equality failed"):
            DiscreteDistribution.pure_dyadic({"a": 1, "b": 1, "c": 1})

    def test_exact_dyadic_divergence_properties(self) -> None:
        p = DiscreteDistribution.pure_dyadic({"s0": 1, "s1": 2, "s2": 3, "s3": 3})
        # Identity: D(P || P) == 0 in Q
        assert exact_dyadic_divergence(p, p) == Fraction(0)
        assert exact_dyadic_cross_entropy(p, p) == p.exact_dyadic_shannon_entropy()

        q = DiscreteDistribution.pure_dyadic({"s0": 2, "s1": 2, "s2": 2, "s3": 2})
        # D(P || Q) = 1/2*(2-1) + 1/4*(2-2) + 1/8*(2-3) + 1/8*(2-3)
        #           = 1/2 + 0 - 1/8 - 1/8 = 1/2 - 1/4 = 1/4 in Q
        div_pq = exact_dyadic_divergence(p, q)
        assert div_pq == Fraction(1, 4)
        assert div_pq > 0
        assert exact_dyadic_cross_entropy(p, q) == p.exact_dyadic_shannon_entropy() + div_pq

    def test_hartley_capacity_additivity(self) -> None:
        p1 = DiscreteDistribution.uniform([0, 1, 2, 3])  # |supp| = 4 = 2^2
        p2 = DiscreteDistribution.uniform([0, 1, 2, 3, 4, 5, 6, 7])  # |supp| = 8 = 2^3
        assert p1.exact_hartley_capacity() == 2
        assert p2.exact_hartley_capacity() == 3

        c1 = p1.exact_hartley_capacity()
        c2 = p2.exact_hartley_capacity()
        assert c1 is not None and c2 is not None
        prod = product_distribution(p1, p2)
        assert len(prod.support()) == 32
        assert prod.exact_hartley_capacity() == 5
        # Additivity: H0(X x Y) = H0(X) + H0(Y)
        assert prod.exact_hartley_capacity() == c1 + c2

    def test_exact_dyadic_mutual_information_and_divergence(self) -> None:
        joint = DiscreteDistribution({
            (0, 0): Fraction(1, 2),
            (1, 1): Fraction(1, 2),
        })
        px = marginal_x(joint)
        py = marginal_y(joint)
        assert px.is_pure_dyadic()
        assert py.is_pure_dyadic()
        exact_mi = exact_dyadic_mutual_information(joint)
        assert exact_mi == Fraction(1, 1)
        assert math.isclose(mutual_information(joint), 1.0)

        p = DiscreteDistribution.uniform([0, 1])
        q = DiscreteDistribution({0: Fraction(1, 4), 1: Fraction(3, 4)})
        div = shannon_divergence(p, q)
        assert div > 0.0


class TestOperationalChannels:
    """Test operational communication channel mechanics and composition."""

    def test_channel_composition_associativity(self) -> None:
        # W1: 2 -> 2 (BSC), W2: 2 -> 3, W3: 3 -> 2
        w1 = Channel.binary_symmetric(Fraction(1, 10))
        w2 = Channel({
            0: DiscreteDistribution({0: Fraction(1, 2), 1: Fraction(1, 2)}),
            1: DiscreteDistribution({1: Fraction(1, 3), 2: Fraction(2, 3)}),
        })
        w3 = Channel({
            0: DiscreteDistribution({0: Fraction(3, 4), 1: Fraction(1, 4)}),
            1: DiscreteDistribution({0: Fraction(1, 2), 1: Fraction(1, 2)}),
            2: DiscreteDistribution({0: Fraction(1, 5), 1: Fraction(4, 5)}),
        })

        # (W3 o W2) o W1 vs W3 o (W2 o W1)
        comp_left = w1.compose(w2).compose(w3)
        comp_right = w1.compose(w2.compose(w3))

        for x in (0, 1):
            dist_left = comp_left.transition(x)
            dist_right = comp_right.transition(x)
            for z in (0, 1):
                assert dist_left.prob(z) == dist_right.prob(z)

    def test_binary_erasure_channel(self) -> None:
        bec = Channel.binary_erasure(Fraction(1, 4), erasure_symbol="e")
        inp = DiscreteDistribution({0: Fraction(1, 2), 1: Fraction(1, 2)})
        out = bec.apply(inp)
        assert out.prob(0) == Fraction(3, 8)
        assert out.prob(1) == Fraction(3, 8)
        assert out.prob("e") == Fraction(2, 8)


class TestDataProcessingInequality:
    """Test verification of the operational Data Processing Inequality (DPI)."""

    def test_dpi_on_cascaded_noisy_channels(self) -> None:
        # X -> Y -> Z where each step is a Binary Symmetric Channel
        px = DiscreteDistribution.uniform([0, 1])
        w_xy = Channel.binary_symmetric(Fraction(1, 5))
        w_yz = Channel.binary_symmetric(Fraction(1, 4))

        cert = verify_data_processing_inequality(px, w_xy, w_yz)
        assert cert.passed
        assert cert.delta_i >= 0.0
        assert cert.i_xy > cert.i_xz
        assert not cert.is_sufficient_statistic

    def test_dpi_deterministic_coarse_graining(self) -> None:
        # X uniform on {0, 1, 2, 3}
        # Y = X (identity channel)
        # Z = Y // 2 (lossy 2-to-1 coarse graining)
        px = DiscreteDistribution.uniform([0, 1, 2, 3])
        w_xy = Channel.identity([0, 1, 2, 3])
        w_yz = Channel.coarse_graining(lambda y: y // 2, [0, 1, 2, 3])

        cert = verify_data_processing_inequality(px, w_xy, w_yz)
        assert cert.passed
        assert math.isclose(cert.i_xy, 2.0)  # log2(4) = 2 bits
        assert math.isclose(cert.i_xz, 1.0)  # log2(2) = 1 bit
        assert cert.delta_i >= 0.999999

    def test_dpi_pure_dyadic_records_exact_fraction_delta(self) -> None:
        px = DiscreteDistribution.uniform([0, 1])
        identity = Channel.identity([0, 1])
        cert = verify_data_processing_inequality(px, identity, identity)
        assert cert.passed
        assert isinstance(cert.exact_rational_diff, Fraction)
        assert cert.exact_rational_diff == Fraction(0)

    def test_dpi_invertible_processing_sufficient_statistic(self) -> None:
        # Invertible bijection Z = 1 - Y retains all mutual information
        px = DiscreteDistribution({0: Fraction(2, 3), 1: Fraction(1, 3)})
        w_xy = Channel.binary_symmetric(Fraction(1, 10))
        w_yz = Channel.deterministic({0: 1, 1: 0})  # bit flip (invertible)

        cert = verify_data_processing_inequality(px, w_xy, w_yz)
        assert cert.passed
        assert cert.is_sufficient_statistic
        assert math.isclose(cert.delta_i, 0.0, abs_tol=1e-12)


class TestDistributedObserverAndProtocols:
    """Test distributed observer protocols, repetition coding, and transmission fidelity."""

    def test_observer_memory(self) -> None:
        obs = DistributedObserver("Observer_Alice", (0, 1, 2))
        assert obs.readout() is None
        obs.store(1)
        assert obs.readout() == 1
        obs.erase_memory(0)
        assert obs.readout() == 0

    def test_repetition_code_protocol(self) -> None:
        # Observer A encodes 1 bit into 3 repeated bits (0 -> 000, 1 -> 111)
        # Channel is 3 independent BSC(p)
        # Decoder takes majority vote
        p_error = Fraction(1, 10)
        bsc_single = Channel.binary_symmetric(p_error)

        # 3-bit channel: transition from (b0, b1, b2) to received (y0, y1, y2)
        # For simplicity, model repetition transmission directly:
        def encode(m: int) -> tuple[int, int, int]:
            return (m, m, m)

        # Transition table for 3-bit repetition channel
        def p_rec(transmitted_bit: int, rec_bit: int) -> Fraction:
            return Fraction(9, 10) if transmitted_bit == rec_bit else Fraction(1, 10)

        trans_table: dict[tuple[int, int, int], dict[tuple[int, int, int], Fraction]] = {}
        for bit in (0, 1):
            tx = (bit, bit, bit)
            d: dict[tuple[int, int, int], Fraction] = {}
            for y0 in (0, 1):
                for y1 in (0, 1):
                    for y2 in (0, 1):
                        prob = p_rec(bit, y0) * p_rec(bit, y1) * p_rec(bit, y2)
                        d[(y0, y1, y2)] = prob
            trans_table[tx] = d

        rep_channel = Channel(trans_table)

        def decode(y: tuple[int, int, int]) -> int:
            return 1 if sum(y) >= 2 else 0

        p_m = DiscreteDistribution.uniform([0, 1])
        proto = OperationalCommunicationProtocol(p_m, encode, rep_channel, decode)

        # Raw channel fidelity is 9/10 = 0.90
        raw_proto = OperationalCommunicationProtocol(p_m, lambda m: m, bsc_single, lambda y: y)
        raw_fid = raw_proto.transmission_fidelity()
        assert raw_fid == Fraction(9, 10)

        # Majority vote fidelity: (9/10)^3 + 3 * (9/10)^2 * (1/10) = 729/1000 + 243/1000 = 972/1000 = 243/250 = 0.972
        fid = proto.transmission_fidelity()
        assert fid == Fraction(972, 1000)
        assert fid > raw_fid
        assert proto.error_probability() == Fraction(28, 1000)
        assert proto.mutual_information_transferred() > 0.8


class TestMemoryRetentionAndErasure:
    """Test memory degradation limits, coarse-graining, and Landauer erasure accounting."""

    def test_memory_retention_monotonic_loss(self) -> None:
        init_p = DiscreteDistribution.uniform([0, 1])
        # Step channel has crossover probability 1/10
        noise_channel = Channel.binary_symmetric(Fraction(1, 10))
        model = MemoryRetentionModel(init_p, noise_channel)

        retained = model.verify_monotonic_retention_loss(max_steps=5)
        # Step 0: full information (1.0 bit)
        assert math.isclose(retained[0], 1.0)
        # Monotonically strictly decreasing towards 0
        for i in range(1, len(retained)):
            assert retained[i] < retained[i - 1]

    def test_lossy_coarse_graining(self) -> None:
        fine = DiscreteDistribution.uniform(["00", "01", "10", "11"])
        coarse, loss = coarse_grain_loss(fine, lambda s: s[0])
        assert math.isclose(fine.shannon_entropy(), 2.0)
        assert math.isclose(coarse.shannon_entropy(), 1.0)
        assert math.isclose(loss, 1.0)

    def test_landauer_erasure_accounting(self) -> None:
        # Uniform 1-bit memory cell
        init = DiscreteDistribution.uniform([0, 1])
        accounting = LandauerAccounting(init, reset_state=0, temperature_kelvin=300.0)
        receipt = accounting.compute_erasure_cost()

        assert receipt.initial_entropy_bits == 1.0
        assert receipt.final_entropy_bits == 0.0
        assert receipt.erased_entropy_bits == 1.0
        assert receipt.exact_erased_entropy_q == Fraction(1, 1)
        assert receipt.operational_non_reversibility
        # Minimal dissipation Q >= kB * T * ln(2) * 1.0
        expected_q = 1.380649e-23 * 300.0 * math.log(2.0)
        assert math.isclose(receipt.minimal_heat_dissipated_joules, expected_q)

    def test_landauer_already_erased(self) -> None:
        # Deterministic state has 0 initial uncertainty -> 0 erasure cost
        init = DiscreteDistribution.point_mass(0)
        accounting = LandauerAccounting(init, reset_state=0)
        receipt = accounting.compute_erasure_cost()
        assert receipt.erased_entropy_bits == 0.0
        assert not receipt.operational_non_reversibility
        assert receipt.minimal_heat_dissipated_joules == 0.0
