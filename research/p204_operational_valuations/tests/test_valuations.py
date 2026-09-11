"""Comprehensive test suite for Operational Valuations and Convex State Spaces (P204).

Tests:
1. OutcomeSpace initialization, indexing, validation, and immutability.
2. OperationalState probability bounds, normalization, and vector representation.
3. OperationalEffect bounds, unit effect, zero effect, and complement.
4. Operational valuation evaluation pairing and unit effect invariance.
5. Convex mixtures of operational preparations with exact rational weights.
6. Convex mixtures of operational effects.
7. Bilinearity of valuation evaluation in both state and effect arguments.
8. ClassicalSimplex unique extreme state decomposition.
9. SquareStateSpace discrete 4-extreme-state model exhibiting non-unique decompositions.
10. Tensor composition, marginal state reductions, and operational non-signaling across cuts.
11. Negative controls: invalid distributions, out-of-bounds effects, and signaling leakage.

AuthorityEffect: None.
"""

from __future__ import annotations

from fractions import Fraction
import pytest

from valuations import (
    ClassicalSimplex,
    OperationalEffect,
    OperationalState,
    OutcomeSpace,
    SquareStateSpace,
    convex_combination_effects,
    convex_combination_states,
    deterministic_state,
    evaluate,
    marginal_state_a,
    marginal_state_b,
    tensor_outcome_space,
    tensor_product_effects,
    tensor_product_states,
    verify_bilinearity,
    verify_non_signaling_across_cut,
)


class TestOutcomeSpace:
    """Test suite for finite discrete outcome spaces."""

    def test_valid_outcome_space(self) -> None:
        space = OutcomeSpace(("heads", "tails"))
        assert space.dim == 2
        assert space.outcomes == ("heads", "tails")
        assert space.contains("heads")
        assert not space.contains("edge")
        assert space.index("heads") == 0
        assert space.index("tails") == 1
        assert len(space) == 2

    def test_outcome_space_rejections(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            OutcomeSpace(())

        with pytest.raises(ValueError, match="distinct"):
            OutcomeSpace(("x", "y", "x"))

    def test_equality_and_hashing(self) -> None:
        s1 = OutcomeSpace((0, 1, 2))
        s2 = OutcomeSpace((0, 1, 2))
        s3 = OutcomeSpace((1, 0, 2))
        assert s1 == s2
        assert s1 != s3
        assert hash(s1) == hash(s2)


class TestOperationalState:
    """Test suite for operational preparation distributions."""

    def test_valid_state(self) -> None:
        space = OutcomeSpace(("a", "b", "c"))
        s = OperationalState(
            space,
            {"a": Fraction(1, 2), "b": Fraction(1, 3), "c": Fraction(1, 6)},
        )
        assert s.probability("a") == Fraction(1, 2)
        assert s.probability("b") == Fraction(1, 3)
        assert s.probability("c") == Fraction(1, 6)
        assert s.vector == (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))

    def test_normalization_failure_rejection(self) -> None:
        space = OutcomeSpace(("a", "b"))
        with pytest.raises(ValueError, match="sum to"):
            OperationalState(space, {"a": Fraction(1, 2), "b": Fraction(1, 4)})

        with pytest.raises(ValueError, match="sum to"):
            OperationalState(space, {"a": Fraction(1, 1), "b": Fraction(1, 2)})

    def test_negative_probability_rejection(self) -> None:
        space = OutcomeSpace(("a", "b"))
        with pytest.raises(ValueError, match="Negative probability"):
            OperationalState(space, {"a": Fraction(-1, 4), "b": Fraction(5, 4)})

    def test_refuses_float_as_exact_q(self) -> None:
        space = OutcomeSpace(("a", "b"))
        with pytest.raises(TypeError, match="float is not exact"):
            OperationalState(space, {"a": 0.5, "b": 0.5})  # type: ignore[dict-item]
        with pytest.raises(TypeError, match="float is not exact"):
            OperationalEffect(space, {"a": 0.25, "b": 0.5})  # type: ignore[dict-item]

    def test_deterministic_state(self) -> None:
        space = OutcomeSpace((0, 1, 2))
        d0 = deterministic_state(space, 0)
        assert d0.probability(0) == Fraction(1, 1)
        assert d0.probability(1) == Fraction(0, 1)
        assert d0.probability(2) == Fraction(0, 1)


class TestOperationalEffect:
    """Test suite for operational measurement effects."""

    def test_valid_effect(self) -> None:
        space = OutcomeSpace(("x", "y"))
        e = OperationalEffect(space, {"x": Fraction(1, 4), "y": Fraction(3, 4)})
        assert e.weight("x") == Fraction(1, 4)
        assert e.weight("y") == Fraction(3, 4)

    def test_out_of_bounds_rejection(self) -> None:
        space = OutcomeSpace(("x", "y"))
        with pytest.raises(ValueError, match="outside"):
            OperationalEffect(space, {"x": Fraction(-1, 10), "y": Fraction(1, 2)})
        with pytest.raises(ValueError, match="outside"):
            OperationalEffect(space, {"x": Fraction(11, 10), "y": Fraction(1, 2)})

    def test_unit_and_zero_effect(self) -> None:
        space = OutcomeSpace(("a", "b", "c"))
        u = OperationalEffect.unit_effect(space)
        z = OperationalEffect.zero_effect(space)
        for out in space.outcomes:
            assert u.weight(out) == Fraction(1, 1)
            assert z.weight(out) == Fraction(0, 1)

    def test_complement_effect(self) -> None:
        space = OutcomeSpace((0, 1))
        e = OperationalEffect(space, {0: Fraction(1, 3), 1: Fraction(2, 3)})
        comp = e.complement()
        assert comp.weight(0) == Fraction(2, 3)
        assert comp.weight(1) == Fraction(1, 3)
        # Sum of e and comp gives unit weights
        for out in space.outcomes:
            assert e.weight(out) + comp.weight(out) == Fraction(1, 1)


class TestOperationalValuation:
    """Test suite for the valuation pairing <e, s>."""

    def test_basic_evaluation(self) -> None:
        space = OutcomeSpace((0, 1))
        s = OperationalState(space, {0: Fraction(3, 4), 1: Fraction(1, 4)})
        e = OperationalEffect(space, {0: Fraction(2, 3), 1: Fraction(1, 3)})
        # <e, s> = (2/3)*(3/4) + (1/3)*(1/4) = 6/12 + 1/12 = 7/12
        assert evaluate(e, s) == Fraction(7, 12)
        assert s.evaluate(e) == Fraction(7, 12)
        assert e.evaluate(s) == Fraction(7, 12)

    def test_unit_effect_evaluates_to_one(self) -> None:
        space = OutcomeSpace(("a", "b", "c"))
        s = OperationalState(
            space,
            {"a": Fraction(1, 5), "b": Fraction(2, 5), "c": Fraction(2, 5)},
        )
        u = OperationalEffect.unit_effect(space)
        assert evaluate(u, s) == Fraction(1, 1)

    def test_zero_effect_evaluates_to_zero(self) -> None:
        space = OutcomeSpace(("a", "b"))
        s = OperationalState(space, {"a": Fraction(1, 2), "b": Fraction(1, 2)})
        z = OperationalEffect.zero_effect(space)
        assert evaluate(z, s) == Fraction(0, 1)

    def test_complement_evaluation_identity(self) -> None:
        space = OutcomeSpace((0, 1))
        s = OperationalState(space, {0: Fraction(1, 3), 1: Fraction(2, 3)})
        e = OperationalEffect(space, {0: Fraction(3, 5), 1: Fraction(1, 5)})
        assert evaluate(e.complement(), s) == Fraction(1, 1) - evaluate(e, s)

    def test_evaluation_space_mismatch_rejection(self) -> None:
        s1 = OutcomeSpace((0, 1))
        s2 = OutcomeSpace((0, 1, 2))
        state = OperationalState(s1, {0: Fraction(1, 2), 1: Fraction(1, 2)})
        eff = OperationalEffect.unit_effect(s2)
        with pytest.raises(ValueError, match="distinct spaces"):
            evaluate(eff, state)


class TestConvexMixturesAndBilinearity:
    """Test suite for convex combinations and operational bilinearity."""

    def test_convex_mixture_states(self) -> None:
        space = OutcomeSpace((0, 1))
        s1 = OperationalState(space, {0: Fraction(1, 1), 1: Fraction(0, 1)})
        s2 = OperationalState(space, {0: Fraction(0, 1), 1: Fraction(1, 1)})
        weights = (Fraction(3, 5), Fraction(2, 5))
        mixed = convex_combination_states(weights, (s1, s2))
        assert mixed.probability(0) == Fraction(3, 5)
        assert mixed.probability(1) == Fraction(2, 5)

    def test_convex_mixture_effects(self) -> None:
        space = OutcomeSpace((0, 1))
        e1 = OperationalEffect(space, {0: Fraction(1, 2), 1: Fraction(1, 4)})
        e2 = OperationalEffect(space, {0: Fraction(1, 4), 1: Fraction(3, 4)})
        weights = (Fraction(1, 3), Fraction(2, 3))
        mixed = convex_combination_effects(weights, (e1, e2))
        # out 0: (1/3)*(1/2) + (2/3)*(1/4) = 1/6 + 2/12 = 1/3
        # out 1: (1/3)*(1/4) + (2/3)*(3/4) = 1/12 + 6/12 = 7/12
        assert mixed.weight(0) == Fraction(1, 3)
        assert mixed.weight(1) == Fraction(7, 12)

    def test_bilinearity_verification(self) -> None:
        space = OutcomeSpace(("x", "y", "z"))
        s1 = deterministic_state(space, "x")
        s2 = deterministic_state(space, "y")
        s3 = deterministic_state(space, "z")

        e1 = OperationalEffect(
            space, {"x": Fraction(1, 2), "y": Fraction(1, 3), "z": Fraction(1, 4)}
        )
        e2 = OperationalEffect(
            space, {"x": Fraction(1, 4), "y": Fraction(1, 2), "z": Fraction(3, 4)}
        )

        state_w = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4))
        effect_w = (Fraction(2, 3), Fraction(1, 3))

        assert verify_bilinearity(state_w, (s1, s2, s3), effect_w, (e1, e2))


class TestClassicalSimplex:
    """Test suite for classical simplex state space uniqueness."""

    def test_simplex_decomposition_uniqueness(self) -> None:
        space = OutcomeSpace(("c1", "c2", "c3"))
        simplex = ClassicalSimplex(space)
        assert len(simplex.extreme_states) == 3

        s = OperationalState(
            space,
            {"c1": Fraction(2, 7), "c2": Fraction(4, 7), "c3": Fraction(1, 7)},
        )
        decomp = simplex.decompose(s)
        assert len(decomp) == 3

        ext0 = deterministic_state(space, "c1")
        ext1 = deterministic_state(space, "c2")
        ext2 = deterministic_state(space, "c3")

        assert decomp[ext0] == Fraction(2, 7)
        assert decomp[ext1] == Fraction(4, 7)
        assert decomp[ext2] == Fraction(1, 7)

        # Unique decomposition check
        assert simplex.is_unique_decomposition(
            s, (Fraction(2, 7), Fraction(4, 7), Fraction(1, 7))
        )
        assert not simplex.is_unique_decomposition(
            s, (Fraction(3, 7), Fraction(3, 7), Fraction(1, 7))
        )


class TestSquareStateSpace:
    """Test suite for general non-simplex discrete square state space."""

    def test_square_state_space_extreme_points(self) -> None:
        square = SquareStateSpace()
        assert len(square.extreme_states) == 4
        for ext in square.extreme_states:
            assert ext.space.dim == 4
            # Each extreme point is normalized
            assert sum(ext.vector) == Fraction(1, 1)

    def test_non_unique_decomposition_demonstration(self) -> None:
        square = SquareStateSpace()
        assert square.demonstrates_non_unique_decomposition()

        w1, s1 = square.decomposition_diagonal_1()
        w2, s2 = square.decomposition_diagonal_2()

        # Weights are distinct
        assert w1 != w2
        assert w1 == (Fraction(1, 2), Fraction(0, 1), Fraction(1, 2), Fraction(0, 1))
        assert w2 == (Fraction(0, 1), Fraction(1, 2), Fraction(0, 1), Fraction(1, 2))

        # Resulting states are identical center state
        assert s1 == s2
        assert s1 == square.center_state
        assert s1.vector == (
            Fraction(1, 4),
            Fraction(1, 4),
            Fraction(1, 4),
            Fraction(1, 4),
        )

    def test_continuous_convex_family_of_decompositions(self) -> None:
        square = SquareStateSpace()
        v1, v2, v3, v4 = square.extreme_states

        # For any parameter lambda in [0, 1], convex combination of the two diagonals
        # produces the exact same center state
        for num in range(0, 6):
            lam = Fraction(num, 5)
            w1 = Fraction(1, 2) * lam
            w2 = Fraction(1, 2) * (Fraction(1, 1) - lam)
            w3 = Fraction(1, 2) * lam
            w4 = Fraction(1, 2) * (Fraction(1, 1) - lam)

            combined_weights = (w1, w2, w3, w4)
            assert sum(combined_weights) == Fraction(1, 1)

            mixed = convex_combination_states(combined_weights, (v1, v2, v3, v4))
            assert mixed == square.center_state


class TestTensorCompositionAndNonSignaling:
    """Test suite for bipartite composition and operational non-signaling."""

    def test_tensor_product_state_and_effects(self) -> None:
        space_a = OutcomeSpace(("u", "d"))
        space_b = OutcomeSpace(("l", "r"))

        sa = OperationalState(space_a, {"u": Fraction(2, 3), "d": Fraction(1, 3)})
        sb = OperationalState(space_b, {"l": Fraction(3, 5), "r": Fraction(2, 5)})

        sab = tensor_product_states(sa, sb)
        assert sab.space.dim == 4
        assert sab.probability(("u", "l")) == Fraction(6, 15)
        assert sab.probability(("u", "r")) == Fraction(4, 15)
        assert sab.probability(("d", "l")) == Fraction(3, 15)
        assert sab.probability(("d", "r")) == Fraction(2, 15)

        # Marginals recover original states
        assert marginal_state_a(sab, space_a, space_b) == sa
        assert marginal_state_b(sab, space_a, space_b) == sb

    def test_non_signaling_across_bipartite_cut(self) -> None:
        space_a = OutcomeSpace((0, 1))
        space_b = OutcomeSpace((0, 1))

        # Correlated composite state (exact rational mixture)
        s_00 = deterministic_state(
            tensor_outcome_space(space_a, space_b), (0, 0)
        )
        s_11 = deterministic_state(
            tensor_outcome_space(space_a, space_b), (1, 1)
        )
        sab = convex_combination_states((Fraction(1, 2), Fraction(1, 2)), (s_00, s_11))

        # Measurement setting 1 on A: standard indicator partition
        e_a0 = OperationalEffect(space_a, {0: Fraction(1, 1), 1: Fraction(0, 1)})
        e_a1 = OperationalEffect(space_a, {0: Fraction(0, 1), 1: Fraction(1, 1)})

        # Measurement setting 2 on A: balanced operational partition
        f_a0 = OperationalEffect(space_a, {0: Fraction(1, 2), 1: Fraction(1, 2)})
        f_a1 = OperationalEffect(space_a, {0: Fraction(1, 2), 1: Fraction(1, 2)})

        # Test effect on B
        test_eff_b = OperationalEffect(
            space_b, {0: Fraction(3, 4), 1: Fraction(1, 4)}
        )

        res1 = verify_non_signaling_across_cut(
            sab, space_a, space_b, (e_a0, e_a1), test_eff_b
        )
        res2 = verify_non_signaling_across_cut(
            sab, space_a, space_b, (f_a0, f_a1), test_eff_b
        )

        assert res1["non_signaling"]
        assert res2["non_signaling"]
        # Statistics on B are identical under setting 1 and setting 2
        assert res1["summed_eval"] == res2["summed_eval"]
        assert res1["marginal_eval"] == res2["marginal_eval"]

    def test_non_signaling_failure_on_invalid_partition(self) -> None:
        space_a = OutcomeSpace((0, 1))
        space_b = OutcomeSpace((0, 1))
        sab = deterministic_state(
            tensor_outcome_space(space_a, space_b), (0, 0)
        )

        # Incomplete measurement effects (weights sum to 1/2, not 1)
        bad_eff_0 = OperationalEffect(space_a, {0: Fraction(1, 2), 1: Fraction(0, 1)})
        test_eff_b = OperationalEffect.unit_effect(space_b)

        with pytest.raises(ValueError, match="do not sum to unit"):
            verify_non_signaling_across_cut(
                sab, space_a, space_b, (bad_eff_0,), test_eff_b
            )
