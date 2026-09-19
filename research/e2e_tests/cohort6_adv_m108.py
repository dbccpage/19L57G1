"""M108 adversarial checks for Cohort 6."""
from __future__ import annotations

from fractions import Fraction
import math
from pathlib import Path
import random
import subprocess
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
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

def test_m108_adversarial_internal_algebra() -> int:
    """Fuzz M108 free monoids, free modules over Q, free rings, and quotient factorizations."""
    print(">>> Fuzzing Target M108: General Internal Algebra...")
    checks = 0
    rng = random.Random(108108)

    # 1. Free monoid universal mapping property & arrow uniqueness
    for trial in range(30):
        alphabet = [f"g_{i}" for i in range(rng.randint(2, 6))]
        fm = m108.FreeMonoid(set(alphabet))

        # Target monoid: additive InternalInt
        val_map = {g: m108.InternalInt(rng.randint(-50, 50)) for g in alphabet}

        # Generate sample words
        sample_words = [m108.Word.unit()]
        for g in alphabet:
            sample_words.append(fm.eta(g))
        for _ in range(5):
            w = m108.Word.unit()
            for _ in range(rng.randint(2, 5)):
                w = w + fm.eta(rng.choice(alphabet))
            sample_words.append(w)

        ump_res = fm.verify_universal_mapping_property(
            f=lambda g, vm=val_map: vm[g],
            target_unit=m108.InternalInt(0),
            target_mul=lambda x, y: x + y,
            sample_words=sample_words,
        )
        assert ump_res["holds"] is True
        checks += 1

        # Verify arrow uniqueness
        def valid_candidate(w: m108.Word, vm=val_map) -> m108.InternalInt:
            tot = m108.InternalInt(0)
            for ch in w.letters:
                tot = tot + vm[ch]
            return tot

        assert fm.verify_arrow_uniqueness(
            f=lambda g, vm=val_map: vm[g],
            candidate_hom=valid_candidate,
            target_unit=m108.InternalInt(0),
            target_mul=lambda x, y: x + y,
            test_words=sample_words,
        ) is True
        checks += 1

        # Negative test: defective candidate map rejected
        def defective_candidate(w: m108.Word, vm=val_map) -> m108.InternalInt:
            base = valid_candidate(w, vm)
            return base + m108.InternalInt(1) if len(w) > 1 else base

        assert fm.verify_arrow_uniqueness(
            f=lambda g, vm=val_map: vm[g],
            candidate_hom=defective_candidate,
            target_unit=m108.InternalInt(0),
            target_mul=lambda x, y: x + y,
            test_words=sample_words,
        ) is False
        checks += 1

    # 2. Free module / vector space over Q & linear UMP sweeps
    for trial in range(30):
        basis = [f"e_{i}" for i in range(rng.randint(2, 5))]
        fmod = m108.FreeModule(set(basis), scalar_type=m108.InternalRat)

        # Target vector space: 1D rational field InternalRat
        eval_weights = {
            b: m108.InternalRat(rng.randint(-20, 20), rng.randint(1, 10)) for b in basis
        }

        # Linear combination operations
        lc1 = m108.LinearCombination.zero()
        lc2 = m108.LinearCombination.zero()
        for b in basis:
            lc1 = lc1 + fmod.eta(b).smul(m108.InternalRat(rng.randint(-5, 5), rng.randint(1, 5)))
            lc2 = lc2 + fmod.eta(b).smul(m108.InternalRat(rng.randint(-5, 5), rng.randint(1, 5)))

        # Additive inverse cancellation
        zero_test = lc1 + (-lc1)
        assert zero_test.is_zero()
        checks += 1

        # Scalar distributivity
        sc_a = m108.InternalRat(rng.randint(-5, 5), rng.randint(1, 5))
        sc_b = m108.InternalRat(rng.randint(-5, 5), rng.randint(1, 5))
        dist_lhs = (lc1 + lc2).smul(sc_a)
        dist_rhs = lc1.smul(sc_a) + lc2.smul(sc_a)
        assert dist_lhs == dist_rhs
        checks += 1

        # Free module UMP over Q
        sample_elems = [m108.LinearCombination.zero(), lc1, lc2, lc1 + lc2]
        ump_mod = fmod.verify_universal_mapping_property(
            f=lambda g, ew=eval_weights: ew[g],
            target_zero=m108.InternalRat.zero(),
            target_add=lambda x, y: x + y,
            target_smul=lambda sc, x: sc * x,
            sample_elements=sample_elems,
        )
        assert ump_mod["holds"] is True
        checks += 1

        # Arrow uniqueness
        def valid_linear(elem: m108.LinearCombination, ew=eval_weights) -> m108.InternalRat:
            acc = m108.InternalRat.zero()
            for k, c in elem.terms:
                acc = acc + c * ew[k]
            return acc

        assert fmod.verify_arrow_uniqueness(
            f=lambda g, ew=eval_weights: ew[g],
            candidate_linear=valid_linear,
            target_zero=m108.InternalRat.zero(),
            target_add=lambda x, y: x + y,
            target_smul=lambda sc, x: sc * x,
            test_elements=sample_elems,
        ) is True
        checks += 1

    # 3. Free ring Cauchy multiplication, non-commutativity & UMP
    for trial in range(25):
        gens = {"x", "y"}
        fring = m108.FreeRing(gens, scalar_type=m108.InternalRat)
        x = fring.eta("x")
        y = fring.eta("y")
        one = m108.FreeRingElement.one(m108.InternalRat)
        zero = m108.FreeRingElement.zero()

        # Cauchy multiplication associativity & distributivity
        lhs = x * (y + one)
        rhs = (x * y) + x
        assert lhs == rhs
        checks += 1

        # Non-commutativity of free ring generators: x*y != y*x
        assert x * y != y * x
        checks += 1

        # Zero annihilation
        assert (x * zero).is_zero()
        assert (zero * y).is_zero()
        checks += 2

    # 4. Congruence relation, representative independence, and quotient factorization
    for trial in range(25):
        modulus = rng.randint(3, 9)
        base_alg = m108.Algebra(
            name=f"Z_mod_{modulus}",
            signature=m108.MONOID_SIGNATURE,
            interpretations={
                "e": lambda: m108.InternalInt(0),
                "mul": lambda a, b: a + b,
            },
        )

        def mod_rel(a: m108.InternalInt, b: m108.InternalInt, m=modulus) -> bool:
            return (a.val - b.val) % m == 0

        congruence = m108.CongruenceRelation(base_alg, mod_rel, name=f"mod_{modulus}")
        sample_ints = [m108.InternalInt(i) for i in range(-15, 15)]
        op_tuples = {
            "mul": [(m108.InternalInt(i), m108.InternalInt(j)) for i in range(-3, 4) for j in range(-3, 4)]
        }

        axiom_res = congruence.verify_congruence_axioms(sample_ints, op_tuples)
        assert axiom_res["valid"] is True
        # Explicitly verify individual equivalence properties
        assert all(congruence.rel(x, x) for x in sample_ints)  # Reflexive
        assert all(congruence.rel(x, y) == congruence.rel(y, x) for x in sample_ints[:8] for y in sample_ints[:8])  # Symmetric
        assert all(
            not (congruence.rel(x, y) and congruence.rel(y, z)) or congruence.rel(x, z)
            for x in sample_ints[:6] for y in sample_ints[:6] for z in sample_ints[:6]
        )  # Transitive
        checks += 4

        # Build quotient algebra
        q_alg = m108.QuotientAlgebra(
            base_alg,
            congruence,
            canonicalizer=lambda x, m=modulus: m108.InternalInt(x.val % m),
            name=f"Z_{modulus}",
        )
        test_pairs = [
            (
                (m108.InternalInt(1), m108.InternalInt(2)),
                (m108.InternalInt(1 + modulus), m108.InternalInt(2 + modulus)),
            ),
            (
                (m108.InternalInt(0), m108.InternalInt(modulus - 1)),
                (m108.InternalInt(modulus), m108.InternalInt(2 * modulus - 1)),
            ),
        ]
        assert q_alg.check_representative_independence("mul", test_pairs) is True
        checks += 1

        # Target algebra: Z_m under addition
        target_alg = m108.Algebra(
            name=f"Z{modulus}",
            signature=m108.MONOID_SIGNATURE,
            interpretations={
                "e": lambda: m108.InternalInt(0),
                "mul": lambda a, b, m=modulus: m108.InternalInt((a.val + b.val) % m),
            },
        )
        h = m108.Homomorphism(
            source=base_alg,
            target=target_alg,
            mapping=lambda x, m=modulus: m108.InternalInt(x.val % m),
            name="mod_proj",
        )

        tilde_h = m108.quotient_factorization(h, q_alg)
        assert m108.verify_quotient_factorization_uniqueness(
            h=h,
            quotient=q_alg,
            candidate_h_bar=lambda q, m=modulus: m108.InternalInt(q.val % m),
            sample_elements=sample_ints[:10],
        ) is True
        checks += 1

        # Defective candidate is rejected
        bad_cand = lambda q, m=modulus: m108.InternalInt((q.val + 1) % m)
        assert m108.verify_quotient_factorization_uniqueness(
            h=h,
            quotient=q_alg,
            candidate_h_bar=bad_cand,
            sample_elements=sample_ints[:10],
        ) is False
        checks += 1

    print(f"  M108 passed {checks} adversarial checks.")
    return checks


# ==============================================================================
# 3. Target M109: Higher Chain Complexes & Obstruction Homology Fuzzing
# ==============================================================================

