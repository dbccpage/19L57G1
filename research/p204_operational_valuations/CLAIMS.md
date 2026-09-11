# Claims Ledger: Target P204 Operational Valuations & Convex State Spaces

## Scope and Intent
Target P204 investigates operational valuations, convex mixtures of preparations and effects, classical simplex state spaces versus general non-simplex convex state spaces, and operational non-signaling across bipartite tensor cuts within finite discrete systems.

## Defensible Findings

### 1. Operational Valuations and Exact Rational Arithmetic
- **What it supports**:
  Operational preparations and effects are representable as exact rational mappings over discrete finite outcome spaces without floating-point error. The valuation pairing $\langle e, s \rangle = \sum_\omega e(\omega) s(\omega)$ satisfies $\langle u, s \rangle = 1$ whenever $s$ satisfies normalization $\sum_\omega s(\omega) = 1$.
- **What it does not support**:
  It does not support claims about continuous outcome spaces, infinite-dimensional operator algebras, or physical devices beyond finite discrete models.
- **Narrowest defensible claim**:
  In finite discrete models with exact rational weights, operational preparation and measurement valuation pairings satisfy exact bilinearity and normalization invariance.
- **Next test needed**:
  Test compositional hierarchies with ternary and quaternary tensor cuts under local adaptive protocols.

### 2. Classical Simplex Uniqueness vs General Convex Non-Uniqueness
- **What it supports**:
  Demonstrates constructively that while classical simplices possess unique decompositions into extreme indicator states, general convex state spaces (specifically the discrete 4-extreme-state square state space) admit non-unique decompositions of mixed preparations into extreme states. For example, the center state admits two distinct diagonal decompositions:
  $s_c = \frac{1}{2} v_1 + \frac{1}{2} v_3 = \frac{1}{2} v_2 + \frac{1}{2} v_4$.
- **What it does not support**:
  It does not support claims that all operational state spaces must be squares or simplices, nor does it establish physical realisability of arbitrary convex sets without explicit preparation protocols.
- **Narrowest defensible claim**:
  A discrete 4-vertex convex state space contains mixed states with non-unique decompositions into extreme states, distinguishing general convex operational theories from classical simplices.
- **Next test needed**:
  Characterize polytope face posets for higher-dimensional regular convex state spaces.

### 3. Operational Non-Signaling Across Bipartite Cuts
- **What it supports**:
  Demonstrates both in Python and by constructive Lean 4 formalization that for any bipartite composite state $s_{AB}$ and any operational partition of unity $\sum_i e_{A, i} = u_A$ on subsystem $A$, the marginal statistics on subsystem $B$ satisfy:
  $\sum_i \langle e_{A, i} \otimes e_B, s_{AB} \rangle = \langle u_A \otimes e_B, s_{AB} \rangle = \langle e_B, s_B \rangle$,
  independent of the local measurement partition chosen on $A$.
- **What it does not support**:
  It does not support claims about relativistic field theories or continuous manifolds. Non-signaling holds here as an algebraic identity of tensor product valuations on normalized bipartite distributions.
- **Narrowest defensible claim**:
  Under tensor product composition and operational normalization, local measurement choice on one subsystem leaves the marginal valuation on the distant subsystem invariant.
- **Next test needed**:
  Verify multi-party operational non-signaling across arbitrary network cuts under sequential localized interventions.

## Formalization and Axiom Boundary
- **Lean Toolchain**: `leanprover/lean4:v4.33.0`.
- **Axioms**: Strictly contained within `{propext, Quot.sound}`.
- **Classical Choice**: 0 uses (`Classical.choice` is entirely absent).
- **External Libraries**: 0 (`mathlib` is not used).
- **Axiom Audit**: 85 theorems verified in the census, 71 strictly axiom-free, 14 using only core `propext` or `Quot.sound`.
