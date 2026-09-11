# Target P208a: Claims and Evidence Ledger

AuthorityEffect: None.
Axiom Scope: Exact rational arithmetic; constructive core Lean 4 formalization.

## Ledger Overview

This document records the formal claims, machine-checked evidence, and epistemic boundaries for Target P208a: path_interference and Vanishing Sorkin $I_3 \equiv 0$ in Diamond 2-Complexes.

---

### Claim 1: Non-Zero Second-Order path_interference ($I_2 \neq 0$)

- **Statement**: Under relative angular path_amplitude shifts, second-order path_interference $I_2(A, B) = P(A \cup B) - P(A) - P(B) = 2 \operatorname{Re}(a_A a_B^*)$ does not vanish in general and takes non-zero values in $\mathbb{Q}$.
- **Constructive Witness**:
  - For path_amplitudes $a_A = 1$ and $a_B = \frac{3}{5} + \frac{4}{5}i$ (exact Pythagorean unit rotation), $I_2(A, B) = \frac{6}{5} \neq 0$.
  - For aligned path_amplitudes $a_A = 1, a_B = 1$, $I_2(A, B) = 2 \neq 0$.
  - For destructive shift $a_A = 1, a_B = -1$, $I_2(A, B) = -2 \neq 0$.
  - For orthogonal delay $a_A = 1, a_B = i$, $I_2(A, B) = 0$.
- **Machine Evidence**:
  - Python: `tests/test_interference.py::test_second_order_path_interference_constructive_witness` passes with exact rational equality $6/5$.
  - Lean 4: `P208aPathInterference.GaussInt.I2_constructive_nonzero` and `I2_constructive_nonzero_ne_zero` verified axiom-free.
- **Narrowest Defensible Claim**: There exist configurations of two paths in a diamond 2-complex with path_amplitudes in $\mathbb{Q}(i)$ for which $I_2(A, B) \neq 0$.

---

### Claim 2: Exact Vanishing of Third-Order Sorkin Quantity ($I_3 \equiv 0$)

- **Statement**: For any diamond 2-complex with three paths carrying path_amplitudes $a_A, a_B, a_C$ in a commutative ring with involution and quadratic valuation $P(\sigma) = A(\sigma) A(\sigma)^*$, the third-order Sorkin combination vanishes identically:
  $$I_3(A, B, C) = P(A \cup B \cup C) - P(A \cup B) - P(A \cup C) - P(B \cup C) + P(A) + P(B) + P(C) = 0$$
- **Algebraic Mechanism**:
  - $P(A \cup B \cup C) = \sum_{j} P(j) + \sum_{j < k} I_2(j, k)$.
  - $\sum_{j < k} P(j \cup k) = 2 \sum_{j} P(j) + \sum_{j < k} I_2(j, k)$.
  - $\sum_{j} P(j) = \sum_{j} P(j)$.
  - Net coefficient of each diagonal term $P(j)$ is $1 - 2 + 1 = 0$.
  - Net coefficient of each cross-term $I_2(j, k)$ is $1 - 1 = 0$.
- **Machine Evidence**:
  - Python: 460-configuration parameter sweep over rational Pythagorean rotations verifies $I_3 = 0$ in 100% of tested instances.
  - Python: Cyclotomic field evaluations over orders $n \in \{3, 4, 6, 8, 12\}$ verify exact vanishing of $I_3$.
  - Lean 4: `P208aPathInterference.GaussInt.sorkin_I3_identically_zero` verified within `{propext, Quot.sound}`.
  - Lean 4: `P208aPathInterference.gauss_quadratic_valuation_I3_zero` verified within `{propext, Quot.sound}`.
- **Narrowest Defensible Claim**: The Sorkin third-order quantity $I_3$ evaluates to zero for all path_amplitudes in any commutative ring with involution evaluated under $P(x) = x \cdot x^*$.

---

### Claim 3: Ruling Out Higher-Order path_interference ($I_k \equiv 0$ for all $k \ge 3$)

- **Statement**: For any finite subset of paths $\sigma$ with $|\sigma| = k \ge 3$, the generalized Sorkin inclusion-exclusion quantity $I_k(\sigma) = \sum_{\tau \subseteq \sigma} (-1)^{|\sigma| - |\tau|} P(\tau)$ is identically zero.
- **Discrete Difference Mechanism**:
  - $I_k(\sigma)$ is the $k$-th order discrete difference $\Delta_{j_1} \cdots \Delta_{j_k} P(\emptyset)$.
  - The path valuation $P(\sigma) = \sum_{j, l \in \sigma} a_j a_l^* = \sum_{j, l} a_j a_l^* x_j x_l$ is a polynomial of degree at most 2 in path indicator variables $x_j \in \{0, 1\}$.
  - Any discrete difference operator of order $k > \deg(P) = 2$ applied to a degree-2 polynomial vanishes identically.
- **Machine Evidence**:
  - Python: `tests/test_interference.py::test_higher_order_path_interference_discrete_difference` passes for 3-path, 4-path, and 5-path subsets.
  - Python: `tests/test_interference.py::test_bilinear_structure_algebraic_proof` passes across higher orders $k \in \{3, 4, 5, 6\}$.
- **Narrowest Defensible Claim**: In any path valuation model where the valuation is quadratic in path presence indicators, all discrete differences of order 3 or higher vanish.

---

### Claim 4: Invariance Across Cyclotomic Extensions $\mathbb{Q}(\zeta_n)$

- **Statement**: The vanishing identity $I_3 \equiv 0$ does not depend on the specific choice of Gaussian rationals $\mathbb{Q}(i) = \mathbb{Q}(\zeta_4)$ and holds in cyclotomic extensions $\mathbb{Q}(\zeta_n)$ for all tested orders $n \in \{3, 4, 6, 8, 12\}$.
- **Machine Evidence**:
  - Python: Exact polynomial quotient arithmetic in $\mathbb{Q}[x] / (\Phi_n(x))$ confirms $I_3 = 0$ for all tested orders without floating-point approximations.
- **Narrowest Defensible Claim**: The identity $I_3 = 0$ is preserved under cyclotomic extensions of $\mathbb{Q}$.

---

## Metatheoretic Census and Axiom Audit

- **Theorems Audited**: 30 theorems in namespace `P208aPathInterference`.
- **Axiom-Free Declarations**: 17 declarations.
- **Axioms Present**: Strictly restricted to `{propext, Quot.sound}`.
- **Classical Choice**: Zero dependencies on `Classical.choice`.
- **Mathlib Dependencies**: Zero mathlib imports or dependencies.

---

## Claim Hygiene Summary

1. **What it supports**:
   - Supports the constructive derivation that quadratic path valuations $P(\sigma) = A(\sigma) A(\sigma)^*$ generate second-order path_interference while ruling out third- and higher-order path_interference.
   - Supports the algebraic independence of the vanishing theorem from choice of coordinates or specific roots of unity.

2. **What it does not support**:
   - Does not support physical claims regarding continuous laboratory setups outside the discrete 2-complex graph representation.
   - Does not support extensions to non-commutative valuation algebras without additional verification.

3. **Narrowest defensible claim**:
   - Discrete quadratic valuations over commutative rings with involution satisfy $I_2 \neq 0$ and $I_k \equiv 0$ for all $k \ge 3$.

4. **Next test needed**:
   - Formal verification of higher cochain valuations on triangulated manifolds and non-commutative matrix valuations.