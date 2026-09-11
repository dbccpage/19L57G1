# Claims and Scope: Target P208b Contextuality & Nonlocality

AuthorityEffect: None.

## Claim Assessment Summary

### 1. What it supports
- Supports the constructive derivation that all 16 bipartite deterministic response functions with inputs $x, y \in \{0, 1\}$ and outcomes $a, b \in \{+1, -1\}$ satisfy the Bell-CHSH correlator value $S \in \{-2, 2\}$, and hence all convex mixtures satisfy $|S| \le 2$.
- Supports the realization of an exact rational non-signaling probability distribution derived from Pythagorean unit coordinates in $\mathbb{Q}^2$ that achieves $S = 14/5 = 2.8$, strictly exceeding the local bound $2$ while respecting the algebraic no-signaling limit $4$.
- Supports the formal specification of the Cabello 18-ray configuration in $\mathbb{Q}^4$ with coordinates in $\{-1, 0, 1\}$ partitioned into 9 orthogonal contexts of 4 mutually orthogonal rays each.
- Supports the exact 2-incidence property ($9 \times 4 = 18 \times 2 = 36$) and the resulting parity obstruction showing that no non-contextual binary valuation $v: \text{Fin } 18 \to \{0, 1\}$ can satisfy $\sum_{r \in C_k} v(r) = 1$ for all contexts, because $2 \sum v(r_i) = 9$ has no integer solution.
- Supports the formal Lean 4 verification of these results within the metatheoretic apparatus $\{propext, Quot.sound\}$ with zero use of external axioms or choice.

### 2. What it does not support
- Does not support assertions regarding continuous manifolds or non-rational geometries.
- Does not support physical claims beyond finite discrete linear algebra and combinatorics over $\mathbb{Q}$.
- Does not support general contextual characterizations beyond the specified 18-ray configuration and bipartite 2-input 2-output scenario.

### 3. Narrowest defensible claim
Under exact rational arithmetic and finite incidence structures:
- The local deterministic Bell-CHSH correlator is bounded by $|S| \le 2$, and an explicit rational non-signaling model achieves $S = 14/5 > 2$.
- The 18-ray Cabello configuration exhibits exact 2-incidence across 9 contexts of size 4, creating an even-odd parity obstruction in $H^1(\mathbb{Z}_2)$ that precludes any non-contextual binary valuation.

### 4. Next test needed
- Formulation of contextual fraction bounds over general graph and hypergraph packings in exact rational arithmetic.
- Investigation of multi-party non-local correlation polytopes under exact linear programming certificates in $\mathbb{Q}$.
