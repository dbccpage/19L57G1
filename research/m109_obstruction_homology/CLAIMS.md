# Claims Ledger: Target M109 (Higher Chain Complexes & Obstruction Homology)

## 1. What it supports

1. **Graded Chain Complexes & Boundary Nilpotency**:
   Demonstrates in this finite setting the construction of graded chain complexes $C_k$ with boundary operators $\partial_k: C_k \to C_{k-1}$ satisfying the nilpotency relation $\partial_k \circ \partial_{k+1} = 0$.
2. **Dual Cochain Complexes & Coboundary Nilpotency**:
   Demonstrates the dual cochain complex construction with coboundary operators $\delta^k = (\partial_{k+1})^T: C^k \to C^{k+1}$ satisfying $\delta^{k+1} \circ \delta^k = 0$, together with the discrete Stokes-Cartan pairing identity $\langle \delta^k \omega, c \rangle = \langle \omega, \partial_{k+1} c \rangle$.
3. **Exact Rational Homology and Cohomology over $\mathbb{Q}$**:
   Computes exact Betti numbers $\beta_k = \dim H_k(C; \mathbb{Q}) = \dim H^k(C; \mathbb{Q})$ using fraction-exact Gaussian elimination without floating-point approximations, confirming Euler-Poincaré characteristics across cycle complexes $C_n$, 2-torus grid complexes $T^2$, and cubical 3-complexes.
4. **Obstruction Classes Detecting Non-Trivial Circulation**:
   Exhibits constructive criteria under which closed 1-cocycles fail to be exact coboundaries, accompanied by explicit witness cycles with non-zero circulation.
5. **Scaling Target 7 Move Complexes**:
   Reproduces the cellular 2-complex invariants of the Target 7 depth-3 move graph ($|V|=262$, $|E|=638$, $H_0 \cong \mathbb{Q}^2$, $H_1 \cong \mathbb{Q}^{232}$ on pure squares), showing that native candidates such as `rule_span` exhibit non-trivial coboundary curvature on commuting squares exchanging rule commitments with data additions.
6. **Constructive Formalization in Core Lean 4**:
   Contains 12 formal theorems in `lean/ObstructionHomology.lean` audited in `lean/Inventory.lean` whose verified dependencies lie within `{propext, Quot.sound}` with zero use of external libraries, choice axioms, or unproved assertions.

## 2. What it does not support

1. Does not claim continuous manifold topology or infinite-dimensional de Rham cohomology.
2. Does not claim torsion analysis over finite fields or non-field coefficient rings (homology is computed over $\mathbb{Q}$).
3. Does not claim algorithmic polynomial-time tractability for higher-dimensional clique complexes on arbitrary infinite graphs.
4. Does not claim that every directed transition system admits a flat commuting square decomposition.

## 3. The narrowest defensible claim

Under the declared discrete move complex and exact rational linear algebra models, higher chain complexes satisfy boundary and coboundary nilpotency, exact rational homology groups $H_k(C; \mathbb{Q})$ and cohomology groups $H^k(C; \mathbb{Q})$ have matching dimensions, and non-trivial circulation on cycles identifies non-exact obstruction cocycles.

## 4. The next test needed

Extension to Target M110/Target P201: relational spacetime dimensions, higher homotopy types, and causal calibration clocks.
