"""Tests for rational Bell-CHSH nonlocality and Cabello 18-ray contextuality.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from correlations import (
    ALICE_VEC_0,
    ALICE_VEC_1,
    BOB_VEC_0,
    BOB_VEC_1,
    CABELLO_CONTEXTS,
    CABELLO_RAYS,
    ConvexLHVModel,
    DeterministicStrategy,
    JointProbabilityTable,
    build_cabello_incidence_matrix,
    cech_cochain_parity_obstruction,
    dot_product_2d,
    dot_product_4d,
    evaluate_noncontextual_valuation_obstruction,
    generate_all_deterministic_strategies,
    make_correlation_table,
    pr_box_model,
    pythagorean_model,
    verify_cabello_incidence,
    verify_cabello_orthogonality,
    verify_deterministic_lhv_bounds,
)


class TestBellCHSHLHVBounds:
    """Verification of Local Hidden Variable (LHV) bounds for Bell-CHSH."""

    def test_deterministic_strategy_count(self) -> None:
        """There are exactly 2^2 * 2^2 = 16 deterministic strategies."""
        strategies = generate_all_deterministic_strategies()
        assert len(strategies) == 16

    def test_deterministic_strategy_bounds(self) -> None:
        """Every deterministic strategy yields S in {-2, +2}."""
        census = verify_deterministic_lhv_bounds()
        assert census["plus_2"] == 8
        assert census["minus_2"] == 8
        assert census["other"] == 0

    def test_deterministic_strategy_magnitudes(self) -> None:
        """Each deterministic strategy satisfies |S| <= 2."""
        for strat in generate_all_deterministic_strategies():
            s_val = strat.correlator()
            assert abs(s_val) <= 2
            assert abs(s_val) == 2

    def test_convex_lhv_combination(self) -> None:
        """Convex combinations of local strategies satisfy |S| <= 2."""
        strategies = tuple(generate_all_deterministic_strategies())
        # Uniform weighting
        uniform_weight = Fraction(1, 16)
        weights = tuple(uniform_weight for _ in range(16))
        model = ConvexLHVModel(strategies=strategies, weights=weights)
        s_val = model.chsh_correlator()
        assert abs(s_val) <= 2
        # Symmetric sum of 8 (+2) and 8 (-2) cancels to 0
        assert s_val == Fraction(0, 1)

    def test_biased_convex_lhv_combination(self) -> None:
        """Biased convex weighting respects the bound |S| <= 2."""
        strategies = tuple(generate_all_deterministic_strategies())
        # Allocate 3/4 weight to strategy with S = +2 and 1/4 to one with S = -2
        pos_strat = next(s for s in strategies if s.correlator() == 2)
        neg_strat = next(s for s in strategies if s.correlator() == -2)
        model = ConvexLHVModel(
            strategies=(pos_strat, neg_strat),
            weights=(Fraction(3, 4), Fraction(1, 4)),
        )
        s_val = model.chsh_correlator()
        # 3/4 * 2 + 1/4 * (-2) = 6/4 - 2/4 = 4/4 = 1
        assert s_val == Fraction(1, 1)
        assert abs(s_val) <= 2

    def test_convex_lhv_invalid_weights_raise(self) -> None:
        """Negative weights or weights not summing to 1 are rejected."""
        strategies = tuple(generate_all_deterministic_strategies()[:2])
        # Weights do not sum to 1
        with pytest.raises(ValueError, match="Weights must sum to 1"):
            ConvexLHVModel(
                strategies=strategies,
                weights=(Fraction(1, 2), Fraction(1, 3)),
            )
        # Negative weight
        with pytest.raises(ValueError, match="Weights must be non-negative"):
            ConvexLHVModel(
                strategies=strategies,
                weights=(Fraction(3, 2), Fraction(-1, 2)),
            )


class TestJointProbabilityAndNoSignaling:
    """Verification of joint distribution validity and no-signaling conditions."""

    def test_valid_table_checks(self) -> None:
        """Valid non-signaling table satisfies normalization and marginal invariance."""
        table = make_correlation_table(
            Fraction(1, 2), Fraction(1, 2), Fraction(1, 2), Fraction(-1, 2)
        )
        assert table.is_valid_distribution()
        assert table.is_no_signaling()

    def test_signaling_table_fails_no_signaling(self) -> None:
        """A distribution with input-dependent marginals fails no-signaling."""
        # Alice's marginal at x=0 depends on Bob's input y:
        bad_table: dict[tuple[int, int, int, int], Fraction] = {}
        for x in (0, 1):
            for y in (0, 1):
                for a in (1, -1):
                    for b in (1, -1):
                        bad_table[(a, b, x, y)] = Fraction(1, 4)
        # Mutate distribution at x=0, y=0
        bad_table[(1, 1, 0, 0)] = Fraction(1, 2)
        bad_table[(1, -1, 0, 0)] = Fraction(0, 1)
        bad_table[(-1, 1, 0, 0)] = Fraction(1, 4)
        bad_table[(-1, -1, 0, 0)] = Fraction(1, 4)

        jpt = JointProbabilityTable(table=bad_table)
        assert jpt.is_valid_distribution()
        # Alice marginal P_A(1 | 0, 0) = 1/2, while P_A(1 | 0, 1) = 1/2;
        # but P_A(-1 | 0, 0) = 1/2 vs P_A(-1 | 0, 1) = 1/2.
        # Let's adjust so marginals diverge:
        bad_table[(1, 1, 0, 1)] = Fraction(1, 8)
        bad_table[(1, -1, 0, 1)] = Fraction(1, 8)
        bad_table[(-1, 1, 0, 1)] = Fraction(3, 8)
        bad_table[(-1, -1, 0, 1)] = Fraction(3, 8)
        jpt2 = JointProbabilityTable(table=bad_table)
        assert not jpt2.is_no_signaling()

    def test_invalid_probability_sum_fails(self) -> None:
        """Table whose probabilities do not sum to 1 is invalid."""
        raw_table: dict[tuple[int, int, int, int], Fraction] = {
            (1, 1, 0, 0): Fraction(1, 2),
            (1, -1, 0, 0): Fraction(1, 2),
            (-1, 1, 0, 0): Fraction(1, 2),  # Sum = 3/2 != 1
            (-1, -1, 0, 0): Fraction(0, 1),
        }
        for x in (0, 1):
            for y in (0, 1):
                if (x, y) != (0, 0):
                    for a in (1, -1):
                        for b in (1, -1):
                            raw_table[(a, b, x, y)] = Fraction(1, 4)
        jpt = JointProbabilityTable(table=raw_table)
        assert not jpt.is_valid_distribution()


class TestPythagoreanNonLocalModel:
    """Verification of rational Pythagorean non-local correlator S = 14/5."""

    def test_pythagorean_unit_vectors(self) -> None:
        """Vectors in Q^2 are exact unit vectors."""
        assert dot_product_2d(ALICE_VEC_0, ALICE_VEC_0) == Fraction(1, 1)
        assert dot_product_2d(ALICE_VEC_1, ALICE_VEC_1) == Fraction(1, 1)
        assert dot_product_2d(BOB_VEC_0, BOB_VEC_0) == Fraction(1, 1)
        assert dot_product_2d(BOB_VEC_1, BOB_VEC_1) == Fraction(1, 1)

    def test_pythagorean_inner_products(self) -> None:
        """Inner products evaluate to exact rational fractions with denominator 5."""
        e00 = dot_product_2d(ALICE_VEC_0, BOB_VEC_0)
        e01 = dot_product_2d(ALICE_VEC_0, BOB_VEC_1)
        e10 = dot_product_2d(ALICE_VEC_1, BOB_VEC_0)
        e11 = dot_product_2d(ALICE_VEC_1, BOB_VEC_1)

        assert e00 == Fraction(4, 5)
        assert e01 == Fraction(4, 5)
        assert e10 == Fraction(3, 5)
        assert e11 == Fraction(-3, 5)

    def test_pythagorean_correlator_value(self) -> None:
        """Pythagorean correlator achieves S = 14/5 = 2.8 > 2."""
        table, s_val = pythagorean_model()
        assert s_val == Fraction(14, 5)
        assert s_val > Fraction(2, 1)
        assert s_val <= Fraction(4, 1)

    def test_pythagorean_model_validity_and_no_signaling(self) -> None:
        """Pythagorean model produces a valid non-signaling distribution."""
        table, _ = pythagorean_model()
        assert table.is_valid_distribution()
        assert table.is_no_signaling()

        # Marginals are all 1/2
        for x in (0, 1):
            for y in (0, 1):
                for a in (1, -1):
                    assert table.marginal_alice(a, x, y) == Fraction(1, 2)
                for b in (1, -1):
                    assert table.marginal_bob(b, x, y) == Fraction(1, 2)


class TestPRBoxModel:
    """Verification of algebraic maximal non-signaling box."""

    def test_pr_box_properties(self) -> None:
        """PR-box satisfies no-signaling and achieves algebraic maximum S = 4."""
        table, s_val = pr_box_model()
        assert table.is_valid_distribution()
        assert table.is_no_signaling()
        assert s_val == Fraction(4, 1)


class TestCabello18RayContextuality:
    """Verification of the 18-ray, 9-context Cabello configuration."""

    def test_counts(self) -> None:
        """Configuration contains 18 discrete rays and 9 contexts."""
        assert len(CABELLO_RAYS) == 18
        assert len(CABELLO_CONTEXTS) == 9
        for ctx in CABELLO_CONTEXTS:
            assert len(ctx) == 4

    def test_coordinates_discrete_domain(self) -> None:
        """Coordinates of all 18 rays lie in {-1, 0, 1}."""
        for ray in CABELLO_RAYS:
            for coord in ray:
                assert coord in (-1, 0, 1)

    def test_orthogonal_contexts(self) -> None:
        """All 4 rays in each context are mutually orthogonal."""
        assert verify_cabello_orthogonality() is True
        # Explicitly verify every pair
        for ctx_idx, ctx in enumerate(CABELLO_CONTEXTS):
            for i in range(4):
                for j in range(i + 1, 4):
                    r_i = CABELLO_RAYS[ctx[i]]
                    r_j = CABELLO_RAYS[ctx[j]]
                    assert dot_product_4d(r_i, r_j) == 0, (
                        f"Context {ctx_idx} pair ({ctx[i]}, {ctx[j]}) dot != 0"
                    )

    def test_incidence_regularity(self) -> None:
        """Each of the 18 rays appears in exactly 2 contexts."""
        inc = verify_cabello_incidence()
        assert len(inc) == 18
        for ray_idx, deg in inc.items():
            assert deg == 2, f"Ray {ray_idx} degree is {deg}, expected 2"
        # Total slots: 9 contexts * 4 rays = 36 slots = 18 rays * 2
        assert sum(inc.values()) == 36

    def test_incidence_matrix(self) -> None:
        """Incidence matrix has shape 9x18, row sums 4, column sums 2."""
        mat = build_cabello_incidence_matrix()
        assert len(mat) == 9
        for row in mat:
            assert len(row) == 18
            assert sum(row) == 4
        col_sums = [sum(mat[k][i] for k in range(9)) for i in range(18)]
        assert all(c == 2 for c in col_sums)

    def test_noncontextual_valuation_obstruction(self) -> None:
        """Non-contextual valuation has no solution: 2 * M = 9 contradiction."""
        res = evaluate_noncontextual_valuation_obstruction()
        assert res["num_contexts"] == 9
        assert res["num_rays"] == 18
        assert res["each_ray_degree"] == 2
        assert res["context_sum_target"] == 9
        # Exhaustive search finds 0 valid valuations among 262,144 candidates
        assert res["exhaustive_valid_valuations"] == 0

    def test_cech_cochain_obstruction(self) -> None:
        """Čech 1-cochain evaluation in H^1(Z_2) produces non-zero obstruction."""
        cech = cech_cochain_parity_obstruction()
        assert cech["context_cycle_mod2"] == 1
        assert cech["incidence_degree_mod2"] == 0
        assert cech["coboundary_obstruction_mod2"] == 1
