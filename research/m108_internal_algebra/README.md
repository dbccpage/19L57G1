# Target M108: General Internal Universal Algebra

Constructive mathematical architecture and verification suite for internal universal algebra, free algebraic constructions, internal homomorphisms, congruence relations, and quotient algebraic structures.

AuthorityEffect: None.

---

## 1. Mathematical Architecture

### A. Constructive Internal Arithmetic (`algebra.py`)
- `InternalInt`: Exact arbitrary-precision integer arithmetic without floating-point approximations.
- `InternalRat`: Exact constructive rationals $(p, q)$ with $q > 0$, $\gcd(p, q) = 1$, exact field arithmetic, and strict zero-denominator rejection.

### B. Signatures, Terms, and Equations
- `Signature`: Explicit mapping from operation symbols to non-negative arities.
- `Term`: Abstract syntax tree consisting of variables (`Var`) and operational applications (`Op`).
- Evaluation and Substitution: Substitutions satisfy structural commutation identities under evaluation in algebraic structures.
- `Equation`: Formal equational identities evaluated across variable valuations.

### C. Free Algebraic Constructions
- **Free Monoid $F_{\text{Mon}}(X)$**:
  - Words over alphabet $X$ under list concatenation with neutral element $\varepsilon$.
  - Canonical generator inclusion arrow $\eta : X \to F_{\text{Mon}}(X)$.
  - Universal mapping property: every set map $f : X \to M$ into a monoid $M$ lifts to a unique monoid homomorphism $\hat{f} : F_{\text{Mon}}(X) \to M$.
- **Free Module $F_{\text{Mod}}(X, R)$**:
  - Formal finite linear combinations over basis set $X$ with coefficients in commutative ring $R$ ($\mathbb{Z}$ or $\mathbb{Q}$).
  - Universal mapping property: every set map $f : X \to N$ into an $R$-module $N$ lifts to a unique $R$-linear map $\hat{f} : F_{\text{Mod}}(X, R) \to N$.
- **Free Ring / Associative Algebra $F_{\text{Ring}}(X, R)$**:
  - Monoid ring $R[F_{\text{Mon}}(X)]$ with Cauchy multiplication.
  - Universal mapping property: lifts basis maps to unique $R$-algebra homomorphisms.

### D. Congruence Relations and Quotient Algebras
- `CongruenceRelation`: Equivalence relations compatible with all signature operations.
- `QuotientAlgebra`: Operational closure over equivalence classes.
- **Representative Independence**: Explicit verification that operations on canonical quotient representatives do not depend on the choice of presentation representative.
- **Universal Factorization Theorem**: Any homomorphism $h : A \to B$ whose kernel contains congruence $\sim$ factors uniquely through canonical projection $\pi : A \to A / \sim$ via $\bar{h} : A / \sim \to B$.

---

## 2. Lean 4 Constructive Formalization (`lean/`)

The inventory in `lean/Inventory.lean` names 14 theorem reports from the
formalization under `lean/InternalAlgebra.lean`.

2026-09-19: the earlier wording that this module "contains 14 theorems" is
withdrawn as a complete count. A local compiled-module census found 58
theorem constants with non-internal names, including generated declarations;
44 are outside the report list. The unreported source theorems include
`evalSum_nil`, `factorMap_map_one`, and `freeMonoidLift_nil`.
The table describes the 14 named reports only:

| Theorem | Mathematical Content | Axioms |
|---|---|---|
| `eval_subst` | Substitution-evaluation commutation identity | `Quot.sound` |
| `freeMonoidLift_eta` | Generator agreement for free monoid lift | None (0 axioms) |
| `freeMonoidLift_append` | Multiplicative homomorphism for free monoid lift | None (0 axioms) |
| `freeMonoid_universal_arrow_unique` | Categorical uniqueness of universal arrow for free monoids | `propext` |
| `evalSum_eta` | Basis agreement for free module evaluation | None (0 axioms) |
| `evalSum_append` | Additive homomorphism for free module evaluation | None (0 axioms) |
| `lift2_mk` | Axiom-free 2-argument quotient lift on representatives | None (0 axioms) |
| `quot_mul_assoc` | Associativity of multiplication in quotient monoids | `Quot.sound` |
| `quot_one_mul` | Left neutral identity in quotient monoids | `Quot.sound` |
| `quot_mul_one` | Right neutral identity in quotient monoids | `Quot.sound` |
| `quot_representative_independence` | Operational closure and representative independence | `Quot.sound` |
| `factorMap_commutes` | Commutativity equation of quotient factorization | None (0 axioms) |
| `factorMap_map_mul` | Homomorphism property of factored quotient map | `Quot.sound` |
| `factorHom_unique` | Categorical uniqueness of factored arrow on quotients | `Quot.sound` |

Axiom cost: 6 declarations are completely axiom-free; 8 declarations depend only on `Quot.sound` or `propext`. Zero `Classical.choice`. Zero `mathlib`.

---

## 3. Running Verification

Execute the complete verification pipeline (source hygiene, pytest test suite, Lean 4 build, and axiom census):

```bash
python research/m108_internal_algebra/verify.py
```

Or inspect the verified receipt:

```bash
python research/m108_internal_algebra/verify.py --check
```
