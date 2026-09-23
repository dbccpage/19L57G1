# Claims Ledger: Non-Classicality Horizons & Gottesman-Knill Boundary (Target P209d)

This ledger documents the formal mathematical and computational claims established by `research/p209d_nonclassical_horizons/` under constructive core Lean 4 and exact Python implementations.

AuthorityEffect: None.
Axiom Scope: Strictly within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## CL-P209D-01: Symplectic Tableau Representation and Commutativity Invariant

- **Statement**: On discrete state carriers over the binary field $\\mathbb{F}_2$, the symplectic inner product $\\Omega(u, v) = u_x v_z + u_z v_x \\pmod 2$ governs observable commutativity. Stabilizer configurations satisfy mutual commutativity $\\Omega(S_i, S_j) = 0$, while canonical destabilizers satisfy conjugate duality $\\Omega(D_i, S_j) = \\delta_{ij}$.
- **Formal Theorems**:
  - `P209dNonclassicalHorizons.omega2_self`
  - `P209dNonclassicalHorizons.omega2_symm`
  - `P209dNonclassicalHorizons.omega4_self`
  - `P209dNonclassicalHorizons.omega4_symm`
  - `P209dNonclassicalHorizons.canonical_pair_duality`
  - `P209dNonclassicalHorizons.stabilizer_self_commutes`
  - `P209dNonclassicalHorizons.bell_stabilizers_commute`
- **Axiom Status**: `{propext, Quot.sound}`.
- **Evidence Paths**:
  - `research/p209d_nonclassical_horizons/lean/NonclassicalHorizons.lean`
  - `research/p209d_nonclassical_horizons/horizons.py`
  - `research/p209d_nonclassical_horizons/tests/test_horizons.py`
- **Claim Discipline**:
  1. *What it supports*: Demonstrates in this discrete symplectic model that commutativity and conjugate duality are algebraically enforced over $\\mathbb{F}_2$.
  2. *What it does not support*: Does not assert algebraic closure for continuous infinite carrier spaces.
  3. *Narrowest defensible claim*: For $n \\in \\{1, 2\\}$, the defined discrete symplectic forms satisfy skew-symmetry, binary symmetry, and preserve the commutation relation of Bell stabilizer generators.
  4. *Next test needed*: Extend the formalization to arbitrary $n$-carrier symplectic matrices over $\\mathbb{F}_2$.

---

## CL-P209D-02: Clifford Group Symplectic Automorphisms and Invariant Preservation

- **Statement**: The named Lean one-carrier $H,S$ and two-carrier $CNOT$ maps preserve their respective defined symplectic forms. The cited theorems do not quantify over arbitrary $n$ or prove invariant preservation for every update of the Python simulator.
- **Formal Theorems**:
  - `P209dNonclassicalHorizons.clifford_H_preserves_omega`
  - `P209dNonclassicalHorizons.clifford_S_preserves_omega`
  - `P209dNonclassicalHorizons.clifford_CNOT_preserves_omega`
  - `P209dNonclassicalHorizons.H_preserves_commutativity`
  - `P209dNonclassicalHorizons.S_preserves_commutativity`
  - `P209dNonclassicalHorizons.CNOT_preserves_commutativity`
  - `P209dNonclassicalHorizons.H_preserves_destabilizer_pair`
  - `P209dNonclassicalHorizons.S_preserves_destabilizer_pair`
- **Axiom Status**: `{propext, Quot.sound}`.
- **Evidence Paths**:
  - `research/p209d_nonclassical_horizons/lean/NonclassicalHorizons.lean`
  - `research/p209d_nonclassical_horizons/horizons.py`
  - `research/p209d_nonclassical_horizons/tests/test_horizons.py`
- **Claim Discipline**:
  1. *What it supports*: Confirms that Clifford updates preserve the symplectic metric and stabilizer commutation relations across single-carrier and two-carrier operations.
  2. *What it does not support*: Does not establish universality for non-Clifford transformations.
  3. *Narrowest defensible claim*: The explicit finite mappings for $H$, $S$-gate, and $CNOT$ leave $\\Omega$ invariant on all inputs in $\\mathbb{F}_2^2$ and $\\mathbb{F}_2^4$.
  4. *Next test needed*: Automated compilation of multi-carrier Clifford circuits into symplectic generators.

---

## CL-P209D-03: Comparison of Three Explicit Dimension-3 Tables

- **Statement**: Two defined tables are pointwise non-negative and a third defined table has value $-1/3$ at the origin. The Lean theorem does not reconstruct these tables from states or prove a characterization of non-negative pure states.
- **Formal Theorems**:
  - `P209dNonclassicalHorizons.wigner_stab_zero_non_negative`
  - `P209dNonclassicalHorizons.wigner_stab_plus_non_negative`
  - `P209dNonclassicalHorizons.wigner_magic_origin_negative`
  - `P209dNonclassicalHorizons.discrete_hudson_boundary_separation`
- **Axiom Status**: `{propext, Quot.sound}`.
- **Evidence Paths**:
  - `research/p209d_nonclassical_horizons/lean/NonclassicalHorizons.lean`
  - `research/p209d_nonclassical_horizons/horizons.py`
  - `research/p209d_nonclassical_horizons/tests/test_horizons.py`
- **Claim Discipline**:
  1. *What it supports*: Checks the signs of the three explicit dimension-3 tables.
  2. *What it does not support*: Does not imply that even-dimensional carriers admit identical phase_point definitions without contextual extensions.
  3. *Narrowest defensible claim*: For the explicit states evaluated in dimension 3, $|0\rangle$ and $|+\rangle$ have non-negative Wigner values everywhere, while $|N\rangle$ attains value $-1/3$ at $(0, 0)$.
  4. *Next test needed*: Characterize the full convex hull of Wigner non-negative states in dimension $p = 5$.

---

## CL-P209D-04: Arithmetic of a Declared Doubling Recurrence

- **Statement**: The defined cost is $4mn^2$ and the defined branch count satisfies $B(0)=1$, $B(k+1)=2B(k)$, hence $B(k)=2^k$. These equations are not a generic simulator lower bound.
- **Formal Theorems**:
  - `P209dNonclassicalHorizons.clifford_cost_polynomial`
  - `P209dNonclassicalHorizons.clifford_cost_linear_in_gates`
  - `P209dNonclassicalHorizons.magic_branch_count_pow`
  - `P209dNonclassicalHorizons.magic_branch_lower_bound`
  - `P209dNonclassicalHorizons.magic_branch_5_gt_quadratic`
  - `P209dNonclassicalHorizons.gottesman_knill_separation`
- **Axiom Status**: `{propext, Quot.sound}`.
- **Evidence Paths**:
  - `research/p209d_nonclassical_horizons/lean/NonclassicalHorizons.lean`
  - `research/p209d_nonclassical_horizons/horizons.py`
  - `research/p209d_nonclassical_horizons/tests/test_horizons.py`
- **Claim Discipline**:
  1. *What it supports*: Proves the closed form of this declared branch-count function.
  2. *What it does not support*: Does not exclude approximate classical heuristic sampling algorithms.
  3. *Narrowest defensible claim*: In the declared recurrence $B(k)=2^k$; the Lean comparison with $k^2$ is checked at specified values, including $k=5$ and $k=10$.
  4. *Next test needed*: Link an actual simulator state and update operation to the cost and branch-count functions before making a complexity claim.

---

## CL-P209D-05: Teleportation and Dense Coding via Symplectic Tableaux

- **Statement**: Python checks the four named measurement branches of its three-carrier teleportation fixture and the dense-coding messages in its Bell-carrier fixture. This package does not prove a general tableau complexity theorem.
- **Evidence Paths**:
  - `research/p209d_nonclassical_horizons/horizons.py`
  - `research/p209d_nonclassical_horizons/tests/test_horizons.py`
- **Claim Discipline**:
  1. *What it supports*: Confirms exact state recovery and decoded messages for the tested finite fixtures.
  2. *What it does not support*: Does not model continuous channel noise or imperfect measurement readout.
  3. *Narrowest defensible claim*: Across all 4 classical measurement branches in the 3-carrier protocol, Pauli corrections applied to carrier 2 reconstruct the injected input state.
  4. *Next test needed*: Simulation of multi-step carrier correlation transfer over distributed network nodes.
