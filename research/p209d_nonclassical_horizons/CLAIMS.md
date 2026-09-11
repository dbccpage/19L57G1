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

- **Statement**: Elementary Clifford generators (Hadamard $H$, $S$-gate, and controlled-NOT $CNOT$) act as symplectic automorphisms on $\\mathbb{F}_2^{2n}$, preserving the symplectic metric $\\Omega(M u, M v) = \\Omega(u, v)$ and maintaining stabilizer commutativity and destabilizer duality throughout state updates.
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

## CL-P209D-03: Discrete Hudson Boundary on Odd Dimension p = 3

- **Statement**: On discrete carrier phase_space $\\mathbb{F}_3 \\times \\mathbb{F}_3$, pure stabilizer states exhibit non-negative discrete Wigner quasiprobability distributions ($W \\ge 0$), whereas non-stabilizer magic states (such as the Norrell state) possess strictly negative Wigner values ($W(0, 0) = -1/3 < 0$), establishing the Discrete Hudson non-classicality horizon.
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
  1. *What it supports*: Demonstrates in odd_prime dimension $p = 3$ that stabilizer states remain within the non-negative Wigner cone while magic states cross into Wigner negativity.
  2. *What it does not support*: Does not imply that even-dimensional carriers admit identical phase point definitions without contextual extensions.
  3. *Narrowest defensible claim*: For the explicit states evaluated in dimension 3, $|0\\rangle$ and $|+\\rangle$ have non-negative Wigner values everywhere, while $|N\\rangle$ attains value $-1/3$ at $(0, 0)$.
  4. *Next test needed*: Characterize the full convex hull of Wigner non-negative states in dimension $p = 5$.

---

## CL-P209D-04: Exponential Resource Scaling for Injected Magic States

- **Statement**: Pure Clifford operations on $n$ carriers simulate in polynomial time $O(m \\cdot n^2)$ via tableau updates. Injecting $k$ non-stabilizer magic states breaks single-tableau closure, requiring tracking a superposition mixture over $2^k$ stabilizer branches, establishing the Gottesman-Knill computational boundary.
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
  1. *What it supports*: Shows that tracking $k$ independent magic states in the standard stabilizer basis mandates $2^k$ simultaneous tableau components.
  2. *What it does not support*: Does not exclude approximate classical heuristic sampling algorithms.
  3. *Narrowest defensible claim*: The exact branch count for $k$ tensor-product magic state injections under the declared superposition representation grows as $2^k$, strictly exceeding $k^2$ for $k \\ge 5$.
  4. *Next test needed*: Benchmark stabilizer rank decomposition approximations using low-rank gadget expansions.

---

## CL-P209D-05: Teleportation and Dense Coding via Symplectic Tableaux

- **Statement**: Bipartite entanglement protocols (teleportation across all 4 measurement outcome branches and dense coding of 2 classical bits per Bell carrier) are faithfully simulated and verified via polynomial-time symplectic tableau updates and Pauli measurements.
- **Evidence Paths**:
  - `research/p209d_nonclassical_horizons/horizons.py`
  - `research/p209d_nonclassical_horizons/tests/test_horizons.py`
- **Claim Discipline**:
  1. *What it supports*: Confirms that stabilizer tableau tracking and Pauli measurement reductions execute teleportation and dense coding with exact state recovery.
  2. *What it does not support*: Does not model continuous channel noise or imperfect detector efficiency.
  3. *Narrowest defensible claim*: Across all 4 classical measurement branches in the 3-carrier protocol, Pauli corrections applied to carrier 2 reconstruct the injected input state.
  4. *Next test needed*: Simulation of multi-hop entanglement swapping over distributed network nodes.
