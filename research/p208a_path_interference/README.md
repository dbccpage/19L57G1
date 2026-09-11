# Target P208a: path_interference and Vanishing Sorkin I_3 in Diamond 2-Complexes

AuthorityEffect: None.
Axiom Scope: Exact rational arithmetic in Python; constructive core Lean 4 formalization.

## Overview

This research directory implements, formalizes, and verifies Target P208a:
1. Exact rational path valuations across Gaussian rationals $\mathbb{Q}(i)$ and cyclotomic fields $\mathbb{Q}(\zeta_n)$.
2. Diamond 2-complex topological networks connecting a source_node to a sink_node via multi-path slit geometries.
3. Constructive demonstration of non-zero second-order path_interference $I_2(A, B) \neq 0$ under path_amplitude rotation and shifts.
4. Constructive verification that the third-order Sorkin quantity vanishes identically:
   $$I_3(A, B, C) = P(A \cup B \cup C) - P(A \cup B) - P(A \cup C) - P(B \cup C) + P(A) + P(B) + P(C) \equiv 0$$
5. Ruling out higher-order path_interference ($I_k \equiv 0$ for all $k \ge 3$) as a direct algebraic consequence of bilinear path_amplitude valuation.
6. Machine-checked formalization in Lean 4 with 30 theorems, zero mathlib, zero Classical.choice, and axioms strictly within `{propext, Quot.sound}`.

## Mathematical Architecture

### 1. Diamond 2-Complex Topology
A diamond 2-complex models multi-path traversal between a source_node $S$ and a sink_node $D$:
- 0-cells: source_node $S$, sink_node $D$, and intermediate path nodes $\{A, B, C, \dots\}$.
- 1-cells: directed edges $(S \to j)$ and $(j \to D)$ for each path branch $j$.
- 2-cells: 2-dimensional faces spanning adjacent alternative path loops.

### 2. Path Valuations and Quadratic Intensity
Each path $j$ carries an exact path_amplitude $a_j \in \mathbb{Q}(i)$ (or cyclotomic field $\mathbb{Q}(\zeta_n)$).
For any open path subset $\sigma \subseteq \{A, B, C\}$:
- Total path_amplitude: $A(\sigma) = \sum_{j \in \sigma} a_j$.
- Quadratic valuation / intensity: $P(\sigma) = A(\sigma) A(\sigma)^* = |A(\sigma)|^2$.

### 3. Second-Order path_interference ($I_2 \neq 0$)
The second-order path_interference quantity between two paths $A$ and $B$ is:
$$I_2(A, B) = P(A \cup B) - P(A) - P(B) = a_A a_B^* + a_B a_A^* = 2 \operatorname{Re}(a_A a_B^*)$$
Under Pythagorean rational unit rotations $(\frac{m^2-n^2}{m^2+n^2}, \frac{2mn}{m^2+n^2})$, non-zero path_interference is constructively realized:
- Aligned paths ($a_A = 1, a_B = 1$): $I_2 = 2 \neq 0$.
- Orthogonal delay ($a_A = 1, a_B = i$): $I_2 = 0$.
- Destructive shift ($a_A = 1, a_B = -1$): $I_2 = -2 \neq 0$.
- Pythagorean rotation ($a_A = 1, a_B = \frac{3}{5} + \frac{4}{5}i$): $I_2 = \frac{6}{5} \neq 0$.

### 4. Third-Order Sorkin Quantity ($I_3 \equiv 0$)
The Sorkin third-order combination is defined by the alternating subset sum:
$$I_3(A, B, C) = P(A \cup B \cup C) - P(A \cup B) - P(A \cup C) - P(B \cup C) + P(A) + P(B) + P(C)$$
Because $P(\sigma) = \sum_{j, k \in \sigma} a_j a_k^*$ expands as the sum of diagonal terms $a_j a_j^*$ and pairwise cross-terms $a_j a_k^* + a_k a_j^*$, every diagonal term appears with net coefficient $(1 - 1 - 1 - 0 + 1) = 0$, and every pairwise cross-term appears with net coefficient $(1 - 1 - 0 - 0) = 0$. Thus $I_3 \equiv 0$ holds identically in any commutative ring with involution under quadratic evaluation.

### 5. Absence of Higher-Order path_interference ($I_k \equiv 0$ for $k \ge 3$)
For any $k \ge 3$ and paths $\sigma = \{j_1, \dots, j_k\}$, the generalized Sorkin quantity:
$$I_k(\sigma) = \sum_{\tau \subseteq \sigma} (-1)^{|\sigma| - |\tau|} P(\tau)$$
coincides with the $k$-th discrete difference operator $\Delta_{j_1} \cdots \Delta_{j_k} P(\emptyset)$. Because $P(\sigma)$ is a polynomial of degree 2 in path inclusion indicator variables $x_j \in \{0, 1\}$, all discrete differences of order $k \ge 3$ vanish identically.

## Verification Suite

- Python reference implementation (`path_interference` engine): Pure Python exact arithmetic reference implementation.
- `tests/test_interference.py`: 15 pytest test cases verifying arithmetic, parameter sweeps, and discrete difference identities.
- `lean/PathInterference.lean`: Formal proofs in Lean 4.
- `lean/Inventory.lean`: Metatheoretic census auditing all 30 theorems.
- `verify.py`: End-to-end verification harness.

To execute verification:
```bash
python verify.py --check
```

## Claim Hygiene Summary

1. **What it supports**:
   - Supports the conclusion that quadratic valuations $P(\sigma) = A(\sigma) A(\sigma)^*$ over commutative rings with involution yield $I_2 \neq 0$ under shifts while strictly vanishing at third order $I_3 \equiv 0$.
   - Supports that all higher-order Sorkin quantities $I_k$ ($k \ge 3$) vanish identically by polynomial degree bounds on discrete difference operators.

2. **What it does not support**:
   - Does not support claims about continuous wave mechanics or physical laboratory apparatus beyond the declared discrete 2-complex network model.
   - Does not support generalizations to non-associative or non-commutative valuation rings without explicit verification.

3. **Narrowest defensible claim**:
   - In any discrete network where path valuations are computed by quadratic evaluation $P(\sigma) = A(\sigma) A(\sigma)^*$ in a commutative ring with involution, $I_2$ can be non-zero while $I_k = 0$ for all $k \ge 3$.

4. **Next test needed**:
   - Extension to non-commutative matrix-valued path weights and higher cochain valuations on generalized simplicial complexes.