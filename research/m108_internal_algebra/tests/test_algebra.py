"""Unit and adversarial test suite for Target M108 General Internal Algebra.

Comprehensive test coverage:
1. Exact Integer & Rational Arithmetic (InternalInt, InternalRat)
2. Signatures, Terms, Substitution, and Equational Satisfaction
3. Free Monoids F_Mon(X) and Universal Arrow Uniqueness
4. Free Modules F_Mod(X, R) over Z and Q and Linear Arrow Uniqueness
5. Free Rings F_Ring(X, R) (Monoid Rings) and Algebra UMP
6. Internal Homomorphisms, Composition, and Kernels
7. Congruence Relations, Operational Closure, and Quotient Algebras
8. Representative Independence of Quotient Operations
9. Quotient Factorization Theorem (Universal Mapping Property of Quotients)
10. Randomized Parity and Stress Trials
"""

from __future__ import annotations

import itertools
from pathlib import Path
import pytest
from typing import Any, Dict, List, Tuple

from algebra import (
    Algebra,
    CongruenceRelation,
    Equation,
    FreeModule,
    FreeMonoid,
    FreeRing,
    FreeRingElement,
    GROUP_SIGNATURE,
    Homomorphism,
    InternalInt,
    InternalRat,
    LinearCombination,
    MONOID_SIGNATURE,
    Op,
    QuotientAlgebra,
    RING_SIGNATURE,
    Signature,
    Term,
    Var,
    Word,
    quotient_factorization,
    verify_quotient_factorization_uniqueness,
)


def test_algebra_kernel_modules_stay_under_one_thousand_lines() -> None:
    root = Path(__file__).resolve().parent.parent
    for name in (
        "algebra.py",
        "arithmetic.py",
        "structures.py",
        "free.py",
        "quotients.py",
    ):
        n = sum(1 for _ in (root / name).open(encoding="utf-8"))
        assert n < 1000, f"{name} has {n} lines"


# ==============================================================================
# 1. Exact Internal Arithmetic Tests
# ==============================================================================

class TestExactArithmetic:
    def test_internal_int_ring_axioms(self) -> None:
        a = InternalInt(7)
        b = InternalInt(-13)
        c = InternalInt(5)

        # Associativity of addition and multiplication
        assert (a + b) + c == a + (b + c)
        assert (a * b) * c == a * (b * c)

        # Commutativity
        assert a + b == b + a
        assert a * b == b * a

        # Identities
        assert a + 0 == a
        assert a * 1 == a

        # Inverses
        assert a + (-a) == InternalInt(0)

        # Distributivity
        assert a * (b + c) == (a * b) + (a * c)

        # Ordering
        assert b < c
        assert b <= a

    def test_internal_rat_field_axioms(self) -> None:
        q1 = InternalRat(3, 4)
        q2 = InternalRat(-5, 6)
        q3 = InternalRat(7, 2)

        # Addition and multiplication
        assert (q1 + q2) + q3 == q1 + (q2 + q3)
        assert (q1 * q2) * q3 == q1 * (q2 * q3)
        assert q1 + q2 == q2 + q1
        assert q1 * q2 == q2 * q1

        # Identities
        assert q1 + InternalRat.zero() == q1
        assert q1 * InternalRat.one() == q1

        # Inverses
        assert q1 + (-q1) == InternalRat.zero()
        assert q1 * q1.inv() == InternalRat.one()

        # Distributivity
        assert q1 * (q2 + q3) == (q1 * q2) + (q1 * q3)

        # Zero denominator rejection
        with pytest.raises(ZeroDivisionError):
            InternalRat(1, 0)

        with pytest.raises(ZeroDivisionError):
            InternalRat.zero().inv()

        with pytest.raises(ZeroDivisionError):
            _ = q1 / InternalRat.zero()


# ==============================================================================
# 2. Signatures, Terms, and Equations Tests
# ==============================================================================

class TestSignaturesAndTerms:
    def test_signature_validation(self) -> None:
        sig = Signature({"e": 0, "inv": 1, "mul": 2})
        assert sig.arity("mul") == 2
        assert sig.arity("inv") == 1
        assert sig.arity("e") == 0
        assert "mul" in sig
        assert "foo" not in sig

        with pytest.raises(ValueError):
            Signature({"bad": -1})

    def test_term_evaluation_and_substitution(self) -> None:
        # Construct term: mul(x, inv(y))
        x = Var("x")
        y = Var("y")
        term = Op("mul", x, Op("inv", y))

        assert term.variables() == {"x", "y"}

        # Substitution x -> mul(y, z)
        z = Var("z")
        subst_term = term.substitute({"x": Op("mul", y, z)})
        assert subst_term.variables() == {"y", "z"}

        # Evaluate in additive group of integers
        # Interpretation: e = 0, inv = neg, mul = add
        int_group = Algebra(
            name="IntGroup",
            signature=GROUP_SIGNATURE,
            interpretations={
                "e": lambda: InternalInt(0),
                "inv": lambda a: -a,
                "mul": lambda a, b: a + b,
            },
        )

        val = term.eval(int_group, {"x": InternalInt(10), "y": InternalInt(3)})
        # 10 + (-3) = 7
        assert val == InternalInt(7)

    def test_equational_laws(self) -> None:
        # Associativity: mul(mul(x, y), z) ≈ mul(x, mul(y, z))
        x, y, z = Var("x"), Var("y"), Var("z")
        assoc_eq = Equation(
            Op("mul", Op("mul", x, y), z),
            Op("mul", x, Op("mul", y, z)),
        )

        int_monoid = Algebra(
            name="IntAddMonoid",
            signature=MONOID_SIGNATURE,
            interpretations={
                "e": lambda: InternalInt(0),
                "mul": lambda a, b: a + b,
            },
        )

        sample_vals = [
            {"x": InternalInt(i), "y": InternalInt(j), "z": InternalInt(k)}
            for i in [-2, 0, 3] for j in [-1, 2] for k in [0, 5]
        ]
        assert assoc_eq.holds_for_valuations(int_monoid, sample_vals)


# ==============================================================================
# 3. Free Monoid Tests
# ==============================================================================

class TestFreeMonoid:
    def test_free_monoid_construction(self) -> None:
        fm = FreeMonoid({"a", "b", "c"})
        w1 = fm.eta("a") + fm.eta("b")  # ab
        w2 = fm.eta("c")               # c
        w3 = w1 + w2                   # abc

        assert repr(w3) == "abc"
        assert len(w3) == 3
        assert w3 + Word.unit() == w3
        assert Word.unit() + w3 == w3

    def test_free_monoid_universal_mapping_property(self) -> None:
        fm = FreeMonoid({"a", "b"})
        # Map into additive integers: a -> 1, b -> 5
        valuation = {"a": InternalInt(1), "b": InternalInt(5)}

        sample_words = [
            Word.unit(),
            Word.generator("a"),
            Word.generator("b"),
            Word.generator("a") + Word.generator("b"),
            Word.generator("b") + Word.generator("a") + Word.generator("b"),
        ]

        res = fm.verify_universal_mapping_property(
            f=lambda g: valuation[g],
            target_unit=InternalInt(0),
            target_mul=lambda x, y: x + y,
            sample_words=sample_words,
        )
        assert res["holds"] is True

        # Uniqueness of universal arrow
        f_hat = fm.lift(
            f=lambda g: valuation[g],
            target_unit=InternalInt(0),
            target_mul=lambda x, y: x + y,
        )

        # Any candidate hom agreeing on generators
        def candidate(w: Word) -> InternalInt:
            total = InternalInt(0)
            for ch in w.letters:
                total = total + valuation[ch]
            return total

        assert fm.verify_arrow_uniqueness(
            f=lambda g: valuation[g],
            candidate_hom=candidate,
            target_unit=InternalInt(0),
            target_mul=lambda x, y: x + y,
            test_words=sample_words,
        )

        # Defective candidate violating homomorphism
        def bad_candidate(w: Word) -> InternalInt:
            return candidate(w) + InternalInt(1) if len(w) > 1 else candidate(w)

        assert not fm.verify_arrow_uniqueness(
            f=lambda g: valuation[g],
            candidate_hom=bad_candidate,
            target_unit=InternalInt(0),
            target_mul=lambda x, y: x + y,
            test_words=sample_words,
        )


# ==============================================================================
# 4. Free Module / Abelian Group Tests
# ==============================================================================

class TestFreeModule:
    def test_free_module_linear_combination_axioms(self) -> None:
        fm = FreeModule({"x", "y", "z"}, scalar_type=InternalInt)

        vx = fm.eta("x")
        vy = fm.eta("y")
        vz = fm.eta("z")

        # Zero cancellation: 1·x + (-1)·x == 0
        sum_cancel = vx + (-vx)
        assert sum_cancel.is_zero()
        assert len(sum_cancel.terms) == 0

        # Scalar multiplication
        v = (vx.smul(3) + vy.smul(-2)).smul(4)
        assert v.coefficient("x") == InternalInt(12)
        assert v.coefficient("y") == InternalInt(-8)
        assert v.coefficient("z") == InternalInt(0)

    def test_free_module_universal_mapping_property_rational(self) -> None:
        fm = FreeModule({"v1", "v2"}, scalar_type=InternalRat)

        # Target module: InternalRat itself as 1D vector space over Q
        # Set map: v1 -> 2/3, v2 -> -5/4
        f_map = {
            "v1": InternalRat(2, 3),
            "v2": InternalRat(-5, 4),
        }

        sample_elements = [
            LinearCombination.zero(),
            fm.eta("v1"),
            fm.eta("v2"),
            fm.eta("v1").smul(InternalRat(3, 2)) + fm.eta("v2").smul(InternalRat(4, 5)),
            fm.eta("v1").smul(InternalRat(-1, 3)) - fm.eta("v2").smul(InternalRat(2, 1)),
        ]

        res = fm.verify_universal_mapping_property(
            f=lambda g: f_map[g],
            target_zero=InternalRat.zero(),
            target_add=lambda a, b: a + b,
            target_smul=lambda sc, a: sc * a,
            sample_elements=sample_elements,
        )
        assert res["holds"] is True

        # Uniqueness test
        def candidate_linear(elem: LinearCombination) -> InternalRat:
            acc = InternalRat.zero()
            for k, c in elem.terms:
                acc = acc + c * f_map[k]
            return acc

        assert fm.verify_arrow_uniqueness(
            f=lambda g: f_map[g],
            candidate_linear=candidate_linear,
            target_zero=InternalRat.zero(),
            target_add=lambda a, b: a + b,
            target_smul=lambda sc, a: sc * a,
            test_elements=sample_elements,
        )


# ==============================================================================
# 5. Free Ring / Associative Algebra Tests
# ==============================================================================

class TestFreeRing:
    def test_free_ring_cauchy_multiplication(self) -> None:
        fr = FreeRing({"x", "y"}, scalar_type=InternalInt)

        x = fr.eta("x")
        y = fr.eta("y")
        one = FreeRingElement.one(InternalInt)

        # Distributivity: x * (y + 1) == x*y + x
        lhs = x * (y + one)
        rhs = (x * y) + x
        assert lhs == rhs

        # Non-commutativity in free ring: x*y != y*x
        assert x * y != y * x

        # Multiplication by zero
        assert (x * FreeRingElement.zero()).is_zero()
        assert (FreeRingElement.zero() * y).is_zero()

    def test_free_ring_universal_mapping_property(self) -> None:
        fr = FreeRing({"a", "b"}, scalar_type=InternalInt)

        # Target algebra: 2x2 integer matrices (represented as 4-tuples (m00, m01, m10, m11))
        # Zero: (0, 0, 0, 0), One: (1, 0, 0, 1)
        zero_mat = (InternalInt(0), InternalInt(0), InternalInt(0), InternalInt(0))
        one_mat = (InternalInt(1), InternalInt(0), InternalInt(0), InternalInt(1))

        def mat_add(m1: Tuple[InternalInt, ...], m2: Tuple[InternalInt, ...]) -> Tuple[InternalInt, ...]:
            return tuple(a + b for a, b in zip(m1, m2))

        def mat_mul(m1: Tuple[InternalInt, ...], m2: Tuple[InternalInt, ...]) -> Tuple[InternalInt, ...]:
            a00, a01, a10, a11 = m1
            b00, b01, b10, b11 = m2
            return (
                a00 * b00 + a01 * b10,
                a00 * b01 + a01 * b11,
                a10 * b00 + a11 * b10,
                a10 * b01 + a11 * b11,
            )

        def mat_smul(sc: InternalInt, m: Tuple[InternalInt, ...]) -> Tuple[InternalInt, ...]:
            return tuple(sc * x for x in m)

        # Generator assignments
        mat_a = (InternalInt(1), InternalInt(2), InternalInt(0), InternalInt(1))
        mat_b = (InternalInt(0), InternalInt(1), InternalInt(1), InternalInt(0))
        f_map = {"a": mat_a, "b": mat_b}

        sample_ring_elems = [
            FreeRingElement.zero(),
            FreeRingElement.one(InternalInt),
            fr.eta("a"),
            fr.eta("b"),
            fr.eta("a") + fr.eta("b"),
            fr.eta("a") * fr.eta("b"),
        ]

        res = fr.verify_universal_mapping_property(
            f=lambda g: f_map[g],
            target_zero=zero_mat,
            target_one=one_mat,
            target_add=mat_add,
            target_mul=mat_mul,
            target_smul=mat_smul,
            sample_elements=sample_ring_elems,
        )
        assert res["holds"] is True


# ==============================================================================
# 6. Internal Homomorphisms and Composition Tests
# ==============================================================================

class TestHomomorphisms:
    def test_homomorphism_preservation_and_composition(self) -> None:
        # Monoid A: (Z, +), Monoid B: (Z, +), Monoid C: (Z, +)
        # h1 : x -> 2x, h2 : y -> 3y
        # Composite: x -> 6x
        sig = MONOID_SIGNATURE
        monoid_z = Algebra(
            name="Z_add",
            signature=sig,
            interpretations={
                "e": lambda: InternalInt(0),
                "mul": lambda a, b: a + b,
            },
        )

        h1 = Homomorphism(
            source=monoid_z,
            target=monoid_z,
            mapping=lambda x: x * InternalInt(2),
            name="double",
        )
        h2 = Homomorphism(
            source=monoid_z,
            target=monoid_z,
            mapping=lambda x: x * InternalInt(3),
            name="triple",
        )

        sample_pairs = [
            (InternalInt(1), InternalInt(2)),
            (InternalInt(-3), InternalInt(5)),
            (InternalInt(0), InternalInt(4)),
        ]

        assert h1.preserves_operation("mul", sample_pairs)
        assert h2.preserves_operation("mul", sample_pairs)

        h_comp = h2.compose(h1)  # h2(h1(x)) = 3*(2*x) = 6x
        assert h_comp.preserves_operation("mul", sample_pairs)
        assert h_comp(InternalInt(7)) == InternalInt(42)


# ==============================================================================
# 7. Congruence Relations, Representative Independence, and Quotients
# ==============================================================================

class TestQuotientAlgebras:
    def test_congruence_relation_axioms(self) -> None:
        # Base algebra: (Z, +, 0)
        # Modulo 5 congruence: x ~ y iff (x - y) % 5 == 0
        int_add = Algebra(
            name="Z",
            signature=MONOID_SIGNATURE,
            interpretations={
                "e": lambda: InternalInt(0),
                "mul": lambda a, b: a + b,
            },
        )

        def mod5_rel(x: InternalInt, y: InternalInt) -> bool:
            return (x.val - y.val) % 5 == 0

        c5 = CongruenceRelation(int_add, mod5_rel, name="mod5")

        samples = [InternalInt(i) for i in range(-10, 15)]
        op_tuples = {
            "mul": [(InternalInt(i), InternalInt(j)) for i in range(-3, 4) for j in range(-3, 4)]
        }

        res = c5.verify_congruence_axioms(samples, op_tuples)
        assert res["valid"] is True

    def test_representative_independence(self) -> None:
        # Base algebra: (Z, +, 0) modulo 4
        int_add = Algebra(
            name="Z",
            signature=MONOID_SIGNATURE,
            interpretations={
                "e": lambda: InternalInt(0),
                "mul": lambda a, b: a + b,
            },
        )

        def mod4_rel(x: InternalInt, y: InternalInt) -> bool:
            return (x.val - y.val) % 4 == 0

        c4 = CongruenceRelation(int_add, mod4_rel, name="mod4")
        canonicalizer = lambda x: InternalInt(x.val % 4)

        q4 = QuotientAlgebra(int_add, c4, canonicalizer, name="Z_4")

        # Test representative independence:
        # (1, 2) ~ (5, 6) ~ (9, -2)
        pairs_to_test = [
            ((InternalInt(1), InternalInt(2)), (InternalInt(5), InternalInt(6))),
            ((InternalInt(1), InternalInt(2)), (InternalInt(9), InternalInt(-2))),
            ((InternalInt(3), InternalInt(3)), (InternalInt(7), InternalInt(-1))),
        ]

        assert q4.check_representative_independence("mul", pairs_to_test)

    def test_quotient_factorization_theorem(self) -> None:
        # Base algebra: (Z, +)
        # Congruence: mod 6
        # Target algebra: (Z_2, +)
        # Homomorphism h : Z -> Z_2 via x -> x % 2
        # Since x = y (mod 6) implies x = y (mod 2), h factors through Z / 6Z!
        int_add = Algebra(
            name="Z",
            signature=MONOID_SIGNATURE,
            interpretations={
                "e": lambda: InternalInt(0),
                "mul": lambda a, b: a + b,
            },
        )

        z2 = Algebra(
            name="Z_2",
            signature=MONOID_SIGNATURE,
            interpretations={
                "e": lambda: InternalInt(0),
                "mul": lambda a, b: InternalInt((a.val + b.val) % 2),
            },
        )

        h = Homomorphism(
            source=int_add,
            target=z2,
            mapping=lambda x: InternalInt(x.val % 2),
            name="mod2_proj",
        )

        c6 = CongruenceRelation(
            int_add,
            lambda x, y: (x.val - y.val) % 6 == 0,
            name="mod6",
        )
        q6 = QuotientAlgebra(int_add, c6, canonicalizer=lambda x: InternalInt(x.val % 6))

        # Construct factored map h_bar : Z_6 -> Z_2
        h_bar = quotient_factorization(h, q6)

        # Verify commutativity: h_bar(pi(x)) == h(x)
        sample_ints = [InternalInt(i) for i in range(-20, 25)]
        for x in sample_ints:
            assert h_bar(q6.pi(x)) == h(x)

        # Verify h_bar is a homomorphism on quotient
        sample_q_pairs = [
            (InternalInt(i), InternalInt(j)) for i in range(6) for j in range(6)
        ]
        assert h_bar.preserves_operation("mul", sample_q_pairs)

        # Verify uniqueness of universal arrow
        assert verify_quotient_factorization_uniqueness(
            h=h,
            quotient=q6,
            candidate_h_bar=lambda q: InternalInt(q.val % 2),
            sample_elements=sample_ints,
        )

        # Defective candidate should fail uniqueness
        bad_candidate = lambda q: InternalInt((q.val + 1) % 2)
        assert not verify_quotient_factorization_uniqueness(
            h=h,
            quotient=q6,
            candidate_h_bar=bad_candidate,
            sample_elements=sample_ints,
        )

    def test_congruence_violation_detection(self) -> None:
        int_add = Algebra(
            name="Z",
            signature=MONOID_SIGNATURE,
            interpretations={
                "e": lambda: InternalInt(0),
                "mul": lambda a, b: a + b,
            },
        )

        # Non-symmetric relation: x <= y
        bad_sym = CongruenceRelation(int_add, lambda x, y: x.val <= y.val)
        res_sym = bad_sym.verify_congruence_axioms(
            [InternalInt(1), InternalInt(2)],
            {"mul": []},
        )
        assert res_sym["valid"] is False
        assert "Symmetry failed" in res_sym["failure"]

        # Non-transitive relation: |x - y| <= 1
        bad_trans = CongruenceRelation(int_add, lambda x, y: abs(x.val - y.val) <= 1)
        res_trans = bad_trans.verify_congruence_axioms(
            [InternalInt(0), InternalInt(1), InternalInt(2)],
            {"mul": []},
        )
        assert res_trans["valid"] is False
        assert "Transitivity failed" in res_trans["failure"]

    def test_term_error_paths(self) -> None:
        sig = Signature({"mul": 2})
        alg = Algebra(
            name="TestAlg",
            signature=sig,
            interpretations={"mul": lambda a, b: a + b},
        )

        # Arity mismatch
        with pytest.raises(ValueError, match="requires arity 2"):
            Op("mul", Var("x")).eval(alg, {"x": 1})

        # Unbound variable
        with pytest.raises(KeyError, match="unbound"):
            Var("y").eval(alg, {"x": 1})

        # Unsupported symbol
        with pytest.raises(ValueError, match="not supported"):
            Op("unsupported", Var("x")).eval(alg, {"x": 1})

    def test_free_ring_full_axioms(self) -> None:
        fr = FreeRing({"x", "y"}, scalar_type=InternalInt)
        x = fr.eta("x")
        y = fr.eta("y")
        one = FreeRingElement.one(InternalInt)
        zero = FreeRingElement.zero()

        # Multiplicative associativity: (x * y) * (x + y) == x * (y * (x + y))
        u = x * y
        v = x + y
        assert (u * v) == (x * (y * v))

        # Right distributivity: (x + y) * one == x + y
        assert (x + y) * one == x + y
        assert one * (x + y) == x + y

        # Left & right zero: zero * x == zero == x * zero
        assert (zero * x).is_zero()
        assert (x * zero).is_zero()

    def test_free_module_scalar_distribution(self) -> None:
        fm = FreeModule({"a", "b"}, scalar_type=InternalInt)
        va = fm.eta("a")
        vb = fm.eta("b")

        r = InternalInt(3)
        s = InternalInt(-5)

        # (r + s) · v == r · v + s · v
        v = va.smul(2) + vb.smul(7)
        lhs = v.smul(r + s)
        rhs = v.smul(r) + v.smul(s)
        assert lhs == rhs

        # r · (u + w) == r · u + r · w
        u = va.smul(4) - vb
        w = va - vb.smul(3)
        assert (u + w).smul(r) == u.smul(r) + w.smul(r)



# ==============================================================================
# 8. Randomized Stress & Parity Trials
# ==============================================================================

class TestRandomizedStress:
    def test_randomized_rational_module_parity(self) -> None:
        import random
        rng = random.Random(42)

        fm = FreeModule({"x", "y"}, scalar_type=InternalRat)
        # Linear map: x -> 5/7, y -> -3/8
        fx = InternalRat(5, 7)
        fy = InternalRat(-3, 8)

        f_hat = fm.lift(
            f=lambda g: fx if g == "x" else fy,
            target_zero=InternalRat.zero(),
            target_add=lambda a, b: a + b,
            target_smul=lambda sc, a: sc * a,
        )

        for _ in range(100):
            c1_num = rng.randint(-50, 50)
            c1_den = rng.randint(1, 20)
            c2_num = rng.randint(-50, 50)
            c2_den = rng.randint(1, 20)

            q1 = InternalRat(c1_num, c1_den)
            q2 = InternalRat(c2_num, c2_den)

            elem = fm.eta("x").smul(q1) + fm.eta("y").smul(q2)
            eval_res = f_hat(elem)

            expected = q1 * fx + q2 * fy
            assert eval_res == expected
