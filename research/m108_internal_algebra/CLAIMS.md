# Claims Ledger: Target M108 (General Internal Universal Algebra)

## 1. What it supports

1. **Constructive Free Algebraic Objects**:
   - Shows in this formal model that free monoids over discrete types $X$ admit an inductive list-based representation whose universal arrow lift satisfies the monoid homomorphism laws without external axioms.
   - Shows in this formal model that the universal arrow into any target monoid is categorically unique under generator agreement.
   - Demonstrates exact rational and integer linear combinations over finite basis sets as models for free modules over constructive commutative rings.
   - Demonstrates free associative algebras (monoid rings $R[F_{\text{Mon}}(X)]$) under Cauchy convolution multiplication.

2. **Equational Terms and Evaluation**:
   - Demonstrates multi-sorted algebraic terms, substitution operations, and the substitution-evaluation commutation identity.

3. **Quotient Representation and Representative Independence**:
   - Demonstrates that congruence relations compatible with algebraic signatures induce well-defined algebraic operations on quotient structures.
   - Shows in this formal model that quotient operations evaluated across alternate equivalence class representatives yield identical canonical results.

4. **Universal Factorization on Quotients**:
   - Shows in this constructive Lean 4 formalization that any homomorphism whose kernel contains a given congruence factors through the canonical projection arrow.
   - Shows that the induced factored arrow is uniquely determined on the quotient.

## 2. What it does not support

1. Does not claim general Birkhoff variety theorem completeness for arbitrary infinitary equational theories.
2. Does not claim continuous topological algebra, Lie groups, or infinite-dimensional functional analysis.
3. Does not assert completion of higher homotopical or univalent algebraic structures.
4. Does not treat empirical or continuous physical systems.

## 3. The narrowest defensible claim

Under the declared syntactic signatures, constructive carrier types, and equivalence relations, free monoids and quotient algebras admit constructive representations whose universal arrows are unique, whose quotient operations are independent of presentation representatives, and whose formal properties build constructively within the axiom bound `{propext, Quot.sound}` with zero reliance on `Classical.choice` or `mathlib`.

## 4. The next test needed

Integration with Target M109 (Higher Chain Complexes and Obstruction Homology), constructing chain complexes over free internal modules and computing homology groups over exact rational coefficients.
