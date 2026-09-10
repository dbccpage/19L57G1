# Claims Ledger: Target X300 (Observer-Relative Information, Channels & Loss)

## 1. What it supports

1. **Exact Rational Operational Entropy in $\mathbb{Q}$**:
   Supports exact rational evaluation of operational Shannon entropy and relative entropy (Kullback-Leibler divergence) for discrete dyadic distributions where $P(x) = 2^{-l_x}$, satisfying $H(P) \in \mathbb{Q}$ and $D(P \parallel Q) \in \mathbb{Q}$ with non-negativity $D(P \parallel Q) \ge 0$.
2. **Operational Communication Channels & Markov Compositions**:
   Supports discrete operational communication channels between distributed observers, establishing that Markov concatenation $(W_2 \circ W_1)(z \mid x) = \sum_y W_1(y \mid x) W_2(z \mid y)$ is associative and computes exact output distributions and transmission fidelities in $\mathbb{Q}$.
3. **Data Processing Inequality (DPI)**:
   Shows in this model that operational post-processing cannot increase mutual information or create new distinguishability distinctions ($I(X; Z) \le I(X; Y)$ for Markov chains $X \to Y \to Z$), and establishes that equality holds under invertible post-processing (sufficient statistics).
4. **Additive Hartley Capacity**:
   Demonstrates in this setting that Hartley capacity metrics over independent observer product alphabets are additive ($H_0(X \times Y) = H_0(X) + H_0(Y)$).
5. **Memory Retention Limits**:
   Shows that retained mutual information under sequential operational noise steps is monotonically non-increasing over time ($I(M_0; M_{k+1}) \le I(M_0; M_k)$).
6. **Landauer Operational Erasure Cost Accounting**:
   Demonstrates that resetting an uncertain discrete memory state to a single reset state compresses phase space, is strictly non-invertible for state spaces with two or more states, and produces an operational entropy reduction $\Delta H \ge 0$ corresponding to Landauer thermal dissipation $Q \ge k_B T \ln(2) \Delta H$.
7. **Constructive Formalization**:
   Provides a constructive Lean 4 formalization of 17 substantive theorems with zero Classical.choice, zero mathlib, zero sorry, zero admit, and axioms strictly within `{propext, Quot.sound}` (16 theorems axiom-free, 1 theorem using only propext).

## 2. What it does not support

1. Does not support continuous probability densities, measure-theoretic differential entropy, or infinite-dimensional alphabets; all structures are discrete and finite.
2. Does not claim empirical thermodynamic efficiency or physical dissipation measurements of physical computing hardware.
3. Does not establish non-commutative quantum observable algebras or continuous channel capacities.
4. Does not assert that finite discrete operational channels represent arbitrary physical networks without additional spatial or dynamic constraints.

## 3. The narrowest defensible claim

Under the declared discrete operational channel and dyadic distribution settings, operational post-processing cannot increase observer distinguishability or mutual information, dyadic Shannon entropy evaluates to exact rational numbers in $\mathbb{Q}$, and memory reset operators on multi-state alphabets are strictly non-invertible, yielding an operational entropy drop bounded by Landauer accounting.

## 4. The next test needed

Extend operational observer channels to composite distributed networks with causal propagation delays and evaluate multi-party coordination bounds.
