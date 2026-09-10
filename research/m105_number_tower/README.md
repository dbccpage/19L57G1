# M105–M106 Number Tower: Natural Number Object & Rational Number Field

Constructive mathematical development of the standard number tower from an endogenous finitary substrate:
1. **Natural Number Object (NNO)**: Universal categorical property and initial pointed homomorphism over inductive ordinals.
2. **Grothendieck Integers (IntZ)**: Equivalence classes of difference pairs over ordinals, yielding a commutative ring with unit.
3. **Localization Rationals (RatQ)**: Equivalence classes of fractions over `IntZ × Ordinal_{>0}`, yielding an Archimedean ordered field of fractions.

AuthorityEffect: None.

---

## 1. Mathematical Architecture

### A. Natural Number Object (`NNO.lean`)
- Rooted in the pure inductive ordinal substrate (`Ordinal` from `g011_finitary_substrate`).
- Characterized by the universal mapping property of pointed endosystems $(X, pt, step)$.
- Constructive recursor `nnoRec` satisfying:
  - $h(0) = pt$
  - $h(succ(n)) = step(h(n))$
- Uniqueness theorem: any two homomorphisms from the NNO to $(X, pt, step)$ are extensionally equal (`nnoRec_unique`).
- Categorical isomorphism: any other NNO is isomorphic via a unique pair of inverse homomorphisms (`nno_unique_iso`).
- Axiomatic cost: **0 axioms** (pure constructive logic; neither `propext` nor `Quot.sound`).

### B. Grothendieck Integers (`IntZ.lean`)
- Constructed as the quotient of $(\text{Ordinal} \times \text{Ordinal})$ under the additive cross-equivalence relation:
  $$(a_1, b_1) \sim (a_2, b_2) \iff a_1 + b_2 = a_2 + b_1$$
- Commutative ring operations:
  - Addition: $[(a_1, b_1)] + [(a_2, b_2)] = [(a_1 + a_2, b_1 + b_2)]$
  - Negation: $-[(a_1, b_1)] = [(b_1, a_1)]$
  - Multiplication: $[(a_1, b_1)] \cdot [(a_2, b_2)] = [(a_1 a_2 + b_1 b_2, a_1 b_2 + b_1 a_2)]$
- Formal verification of all ring axioms: commutativity, associativity, additive/multiplicative identities ($0_Z = [(0, 0)]$, $1_Z = [(1, 0)]$), additive inverse ($z + (-z) = 0_Z$), distributivity.
- Embedding $\mathbb{N} \hookrightarrow \mathbb{Z}$ via $n \mapsto [(n, 0)]$ shown to be an injective ring homomorphism.
- Axiomatic cost: at most `propext` and `Quot.sound`. Zero `Classical.choice`.

### C. Localization Rationals (`RatQ.lean`)
- Constructed as the quotient of $\text{Frac} = \mathbb{Z} \times \text{Ordinal}_{>0}$ under cross-multiplication:
  $$(p_1, q_1) \sim (p_2, q2) \iff p_1 \cdot q_2 = p_2 \cdot q_1 \quad \text{in } \mathbb{Z}$$
  where denominators are strictly positive ($q = \text{succ}(d)$).
- Field operations:
  - Addition: $\frac{p_1}{q_1} + \frac{p_2}{q_2} = \frac{p_1 q_2 + p_2 q_1}{q_1 q_2}$
  - Multiplication: $\frac{p_1}{q_1} \cdot \frac{p_2}{q_2} = \frac{p_1 p_2}{q_1 q_2}$
  - Inversion: for non-zero $p / q$, $(\text{sgn}(p) \cdot q) / |p|$.
- Formal verification of field axioms: commutativity, associativity, distributivity, identities ($0_Q, 1_Q$), multiplicative inverse, non-triviality ($0_Q \neq 1_Q$).
- Order relation: $r_1 \le r_2 \iff \exists k d, r_2 = r_1 + \frac{k}{d+1}$.
- Canonical embeddings $\mathbb{Z} \hookrightarrow \mathbb{Q}$ and $\mathbb{N} \hookrightarrow \mathbb{Q}$ shown to be injective ring homomorphisms.
- Axiomatic cost: at most `propext` and `Quot.sound`. Zero `Classical.choice`.

---

## 2. Axiom Census & Auditing

Every declaration under the `NumberTower` namespace is enumerated by `lean/Inventory.lean` and audited by `verify.py`:

| Component | Total Declarations | Axiom-Free Declarations | Permitted Axioms (`propext`, `Quot.sound`) | Disallowed Axioms (`Classical.choice`, `mathlib`) |
|---|---|---|---|---|
| `NNO.lean` | 24 | 24 | 0 | 0 |
| `IntZ.lean` | 38 | 12 | 26 | 0 |
| `RatQ.lean` | 48 | 7 | 41 | 0 |
| **Total** | **110** | **43** | **67** | **0** |

Receipt generated and saved to `evidence/receipt.json`.

---

## 3. Python Exact Arithmetic Implementation

`number_tower.py` provides exact computational counterparts to the constructive specifications:
- `NNO`: Categorical recursor `rec(system, n)` and uniqueness checker `check_uniqueness(system, hom)`.
- `IntZ`: Arbitrary-precision difference pair `(pos, neg)` with cross-addition equality `(p1 + n2 == p2 + n1)`, canonical reduction `(pos - neg, 0)` or `(0, neg - pos)`, and exact ring arithmetic.
- `RatQ`: Fraction pair `(num, den)` with `den >= 1`, cross-multiplication equality, multiplicative inversion, and exact field arithmetic.
- Zero floating-point logic across all operations.

### Test Suite (`tests/test_number_tower.py`)
- 17 unit test functions covering:
  - Universal NNO recursion and defective-homomorphism rejection.
  - Representation independence under arbitrary non-canonical representatives.
  - Ring and field axioms (identity, inverse, associativity, commutativity, distributivity).
  - Negative and zero denominator rejection.
  - 500 randomized parity trials comparing arithmetic and order against Python's `fractions.Fraction`.

---

## 4. Verification Instructions

Run verification locally:
```bash
python verify.py
```
Or check existing receipt:
```bash
python verify.py --check
```
