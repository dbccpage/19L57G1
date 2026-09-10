"""Comprehensive Pytest Suite for M105 Constructive Number Tower.

Tests:
1. Natural Number Object (NNO) categorical universal property and recursion.
2. IntZ Grothendieck group axioms, representative independence, order, and embeddings.
3. RatQ localization field axioms, representative independence, order, and inversion.
4. Parity with fractions.Fraction across operations and randomized trials.
5. Error cases: non-positive denominators, zero division, invalid inputs.

AuthorityEffect: None.
"""

from __future__ import annotations

import fractions
import pytest
import random

from number_tower import NNO, IntZ, PointedSystem, RatQ


# =============================================================================
# 1. NNO & Categorical Recursion Tests
# =============================================================================

class TestNNO:
    def test_nno_basic(self):
        assert NNO.zero() == 0
        assert NNO.succ(0) == 1
        assert NNO.succ(41) == 42
        with pytest.raises(ValueError):
            NNO.succ(-1)

    def test_nno_rec_addition(self):
        # Compute 5 + n using system (5, succ)
        sys_add5 = PointedSystem(pt=5, step=lambda x: x + 1)
        assert NNO.rec(sys_add5, 0) == 5
        assert NNO.rec(sys_add5, 3) == 8
        assert NNO.rec(sys_add5, 10) == 15

    def test_nno_rec_multiplication(self):
        # Compute 3 * n using system (0, lambda x: x + 3)
        sys_mul3 = PointedSystem(pt=0, step=lambda x: x + 3)
        assert NNO.rec(sys_mul3, 0) == 0
        assert NNO.rec(sys_mul3, 1) == 3
        assert NNO.rec(sys_mul3, 7) == 21

    def test_nno_rec_uniqueness(self):
        sys_step = PointedSystem(pt=10, step=lambda x: x + 2)
        # Genuine homomorphism: h(n) = 10 + 2*n
        valid_hom = lambda n: 10 + 2 * n
        assert NNO.check_uniqueness(sys_step, valid_hom, max_n=30)

        # Defective homomorphism: base step correct, inductive step fails at 5
        def defective_hom(n: int) -> int:
            return 10 + 2 * n if n != 5 else 999

        assert not NNO.check_uniqueness(sys_step, defective_hom, max_n=30)

        # Defective homomorphism: base step fails
        assert not NNO.check_uniqueness(sys_step, lambda n: 11 + 2 * n, max_n=30)

    def test_nno_rec_negative_rejected(self):
        sys_step = PointedSystem(pt=0, step=lambda x: x + 1)
        with pytest.raises(ValueError):
            NNO.rec(sys_step, -3)


# =============================================================================
# 2. IntZ Grothendieck Difference Pair Tests
# =============================================================================

class TestIntZ:
    def test_representative_independence(self):
        # 2 can be represented by (2, 0), (5, 3), (102, 100)
        z1 = IntZ(2, 0)
        z2 = IntZ(5, 3)
        z3 = IntZ(102, 100)
        assert z1 == z2
        assert z2 == z3
        assert z1 == 2
        assert hash(z1) == hash(z2) == hash(z3)
        assert z1.to_int() == z2.to_int() == 2
        assert z2.canonical() == (2, 0)

        # -3 can be represented by (0, 3), (2, 5), (10, 13)
        neg1 = IntZ(0, 3)
        neg2 = IntZ(2, 5)
        neg3 = IntZ(10, 13)
        assert neg1 == neg2 == neg3
        assert neg1 == -3
        assert hash(neg1) == hash(neg2)
        assert neg2.canonical() == (0, 3)

    def test_ring_axioms(self):
        # Test with varied non-canonical representatives
        samples = [
            IntZ(0, 0),
            IntZ(4, 4),
            IntZ(7, 2),   # +5
            IntZ(12, 7),  # +5
            IntZ(1, 9),   # -8
            IntZ(10, 18), # -8
            IntZ(15, 0),  # +15
            IntZ(0, 12),  # -12
        ]

        zero = IntZ.zero()
        one = IntZ.one()

        for a in samples:
            # Additive identity
            assert a + zero == a
            assert zero + a == a

            # Additive inverse
            assert a + (-a) == zero
            assert (-a) + a == zero

            # Multiplicative identity
            assert a * one == a
            assert one * a == a

            # Multiplicative zero
            assert a * zero == zero
            assert zero * a == zero

            for b in samples:
                # Additive commutativity
                assert a + b == b + a
                # Multiplicative commutativity
                assert a * b == b * a

                for c in samples[:4]:
                    # Additive associativity
                    assert (a + b) + c == a + (b + c)
                    # Multiplicative associativity
                    assert (a * b) * c == a * (b * c)
                    # Distributivity
                    assert a * (b + c) == (a * b) + (a * c)

    def test_subtraction_self(self):
        for val in [-10, 0, 5, 23]:
            z = IntZ.from_int(val)
            assert z - z == IntZ.zero()
            # Non-canonical
            z_noncan = IntZ(z.pos + 7, z.neg + 7)
            assert z_noncan - z == IntZ.zero()

    def test_order_and_trichotomy(self):
        z_neg = IntZ(2, 7)  # -5
        z_zero = IntZ(3, 3) # 0
        z_pos = IntZ(8, 2)  # +6

        assert z_neg < z_zero < z_pos
        assert z_neg <= z_neg
        assert z_pos > z_zero
        assert z_pos >= z_pos
        assert not (z_pos < z_neg)
        assert z_neg != z_pos

    def test_nat_embedding(self):
        for n in [0, 1, 5, 42]:
            z = IntZ.from_nat(n)
            assert z.to_int() == n
            assert z.is_nonneg()
            assert z == n

        # Homomorphism
        m, n = 7, 13
        zm, zn = IntZ.from_nat(m), IntZ.from_nat(n)
        assert IntZ.from_nat(m + n) == zm + zn
        assert IntZ.from_nat(m * n) == zm * zn

    def test_invalid_construction(self):
        with pytest.raises(ValueError):
            IntZ(-1, 2)
        with pytest.raises(ValueError):
            IntZ(2, -1)
        with pytest.raises(TypeError):
            IntZ("a", 2)  # type: ignore


# =============================================================================
# 3. RatQ Localization & Field Axioms Tests
# =============================================================================

class TestRatQ:
    def test_representative_independence(self):
        # 1/2 can be represented by (1, 2), (2, 4), (5, 10)
        r1 = RatQ(IntZ(1, 0), 2)
        r2 = RatQ(IntZ(2, 0), 4)
        r3 = RatQ(IntZ(5, 0), 10)
        # Even with non-canonical IntZ numerator: (6, 4) in Z represents 2
        r4 = RatQ(IntZ(6, 4), 4)
        assert r1 == r2 == r3 == r4
        assert hash(r1) == hash(r2) == hash(r3) == hash(r4)
        assert r1.canonical() == (1, 2)
        assert r4.canonical() == (1, 2)

        # -3/5
        neg1 = RatQ(IntZ(0, 3), 5)
        neg2 = RatQ(IntZ(0, 6), 10)
        neg3 = RatQ(IntZ(3, 6), 5) # 3-6 = -3
        assert neg1 == neg2 == neg3
        assert hash(neg1) == hash(neg2) == hash(neg3)
        assert neg1.canonical() == (-3, 5)

    def test_field_axioms(self):
        samples = [
            RatQ(IntZ(0, 0), 1),
            RatQ(IntZ(2, 2), 3),   # 0
            RatQ(IntZ(1, 0), 1),   # 1
            RatQ(IntZ(3, 0), 3),   # 1
            RatQ(IntZ(2, 0), 3),   # 2/3
            RatQ(IntZ(5, 1), 6),   # 4/6 = 2/3
            RatQ(IntZ(0, 5), 4),   # -5/4
            RatQ(IntZ(2, 7), 4),   # -5/4
            RatQ(IntZ(7, 1), 2),   # 6/2 = 3
        ]

        zero = RatQ.zero()
        one = RatQ.one()

        assert zero != one

        for a in samples:
            # Additive identity
            assert a + zero == a
            assert zero + a == a

            # Additive inverse
            assert a + (-a) == zero
            assert (-a) + a == zero
            assert a - a == zero

            # Multiplicative identity
            assert a * one == a
            assert one * a == a

            # Multiplicative zero
            assert a * zero == zero
            assert zero * a == zero

            # Multiplicative inverse (for non-zero)
            if not a.is_zero():
                inv_a = a.inv()
                assert a * inv_a == one
                assert inv_a * a == one
                assert a / a == one

            for b in samples[:5]:
                # Commutativity
                assert a + b == b + a
                assert a * b == b * a

                for c in samples[:3]:
                    # Associativity
                    assert (a + b) + c == a + (b + c)
                    assert (a * b) * c == a * (b * c)
                    # Distributivity
                    assert a * (b + c) == (a * b) + (a * c)

    def test_order_properties(self):
        r_neg = RatQ(IntZ(0, 3), 4)  # -3/4
        r_zero = RatQ.zero()         # 0
        r_half = RatQ(IntZ(1, 0), 2) # 1/2
        r_one = RatQ.one()           # 1

        assert r_neg < r_zero < r_half < r_one
        assert r_neg <= r_neg
        assert r_one > r_half
        assert r_one >= r_one

        # Cross-comparison with non-canonical forms
        assert RatQ(IntZ(2, 0), 4) == RatQ(IntZ(5, 0), 10)
        assert RatQ(IntZ(1, 0), 3) < RatQ(IntZ(1, 0), 2)

    def test_division_by_zero_and_bad_denominators(self):
        zero = RatQ.zero()
        with pytest.raises(ZeroDivisionError):
            zero.inv()

        with pytest.raises(ZeroDivisionError):
            RatQ(IntZ(1, 0), 1) / zero

        with pytest.raises(ValueError):
            RatQ(IntZ(1, 0), 0)

        with pytest.raises(ValueError):
            RatQ(IntZ(1, 0), -2)

    def test_embeddings(self):
        # Nat -> RatQ
        for n in [0, 1, 3, 10]:
            rn = RatQ.from_nat(n)
            assert rn == n
            assert rn.is_nonneg()

        # IntZ -> RatQ
        z_pos = IntZ(7, 2)  # +5
        z_neg = IntZ(2, 7)  # -5
        rz_pos = RatQ.from_int_z(z_pos)
        rz_neg = RatQ.from_int_z(z_neg)

        assert rz_pos + rz_neg == RatQ.zero()
        assert rz_pos * rz_neg == RatQ.from_int(-25)


# =============================================================================
# 4. Randomized Parity Against fractions.Fraction
# =============================================================================

class TestFractionsParity:
    def test_randomized_arithmetic_parity(self):
        rng = random.Random(42)
        trials = 500

        for _ in range(trials):
            n1 = rng.randint(-100, 100)
            d1 = rng.randint(1, 100)
            n2 = rng.randint(-100, 100)
            d2 = rng.randint(1, 100)

            # Generate non-canonical difference pair for num1 & num2
            pad1 = rng.randint(0, 50)
            pad2 = rng.randint(0, 50)
            if n1 >= 0:
                z1 = IntZ(n1 + pad1, pad1)
            else:
                z1 = IntZ(pad1, -n1 + pad1)

            if n2 >= 0:
                z2 = IntZ(n2 + pad2, pad2)
            else:
                z2 = IntZ(pad2, -n2 + pad2)

            q1 = RatQ(z1, d1)
            q2 = RatQ(z2, d2)

            f1 = fractions.Fraction(n1, d1)
            f2 = fractions.Fraction(n2, d2)

            # Check conversions
            assert q1.to_fraction() == f1
            assert q2.to_fraction() == f2
            assert RatQ.from_fraction(f1) == q1
            assert RatQ.from_fraction(f2) == q2

            # Equality & Comparison
            assert (q1 == q2) == (f1 == f2)
            assert (q1 < q2) == (f1 < f2)
            assert (q1 <= q2) == (f1 <= f2)
            assert (q1 > q2) == (f1 > f2)
            assert (q1 >= q2) == (f1 >= f2)

            # Addition
            assert (q1 + q2).to_fraction() == f1 + f2
            # Subtraction
            assert (q1 - q2).to_fraction() == f1 - f2
            # Multiplication
            assert (q1 * q2).to_fraction() == f1 * f2

            # Division (when q2 != 0)
            if f2 != 0:
                assert (q1 / q2).to_fraction() == f1 / f2
                assert (q2.inv()).to_fraction() == 1 / f2

            # Canonical representation coprime check
            cn, cd = q1.canonical()
            assert cd > 0
            assert fractions.Fraction(cn, cd) == f1
