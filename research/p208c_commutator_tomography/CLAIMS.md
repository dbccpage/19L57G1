# Claims Ledger: Finite Commutator Obstruction & Discrete MUB Tomography (Target P208c)

This ledger documents the formal mathematical and computational claims established by `research/p208c_commutator_tomography/` under constructive core Lean 4 and exact Python implementations.

AuthorityEffect: None.
Axiom Scope: Strictly within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## CL-P208C-01: Finite-Dimensional Commutator Trace Obstruction

- **Statement**: For any finite $N \times N$ matrices $A, B$ over characteristic zero, the trace of their commutator vanishes identically: $\operatorname{Tr}([A, B]) = 0$. Consequently, the canonical commutation relation $[Q, P] = c \cdot I_N$ with $c \neq 0$ is algebraically obstructed on any finite carrier of dimension $N \ge 1$.
- **Formal Theorems**:
  - `P208cCommutatorTomography.trace_matMul_comm`
  - `P208cCommutatorTomography.trace_commutator_zero`
  - `P208cCommutatorTomography.trace_scalar_identity`
  - `P208cCommutatorTomography.commutator_trace_obstruction`
- **Axiom Status**: `{propext, Quot.sound}`.
- **Evidence Paths**:
  - `research/p208c_commutator_tomography/lean/CommutatorTomography.lean`
  - `research/p208c_commutator_tomography/tomography.py`
  - `research/p208c_commutator_tomography/tests/test_tomography.py`
- **Claim Discipline**:
  1. *What it supports*: Demonstrates in this finite matrix model that $[Q, P] = c \cdot I$ cannot be represented on finite-dimensional carrier spaces without algebraic contradiction.
  2. *What it does not support*: Does not imply that infinite-dimensional continuous systems cannot represent canonical commutation relations.
  3. *Narrowest defensible claim*: For every finite dimension $N \ge 1$ and non-zero scalar $c$, no pair of $N \times N$ matrices satisfies $[Q, P] = c \cdot I_N$.
  4. *Next test needed*: Formulate Weyl exponentiated relations on finite cyclic groups.

---

## CL-P208C-02: Multi-Locus Microcausality on Composite Carriers

- **Statement**: On composite multi-locus carrier networks, local observables supported on disjoint loci strictly commute: $[A \otimes I_B, I_A \otimes B] = 0$. Conversely, conjugate operational step operators localized on the same locus fail to commute.
- **Formal Theorems**:
  - `P208cCommutatorTomography.tensor_mixed_product`
  - `P208cCommutatorTomography.matMul_identity_2`
  - `P208cCommutatorTomography.identity_matMul_2`
  - `P208cCommutatorTomography.multi_locus_microcausality_2x2`
- **Axiom Status**: `{propext, Quot.sound}`.
- **Evidence Paths**:
  - `research/p208c_commutator_tomography/lean/CommutatorTomography.lean`
  - `research/p208c_commutator_tomography/tomography.py`
  - `research/p208c_commutator_tomography/tests/test_tomography.py`
- **Claim Discipline**:
  1. *What it supports*: Confirms that spatial isolation on composite carriers algebraically enforces operational commutativity without background geometric metrics.
  2. *What it does not support*: Does not establish relativistic field theory or light-cone structures.
  3. *Narrowest defensible claim*: In the discrete tensor product representation, disjoint locus embeddings commute identically, while single-locus clock and shift operators do not commute.
  4. *Next test needed*: Multi-locus composite state tomography with distributed local measurements.

---

## CL-P208C-03: Discrete Mutually Unbiased Bases in Dimension d = 3

- **Statement**: In dimension $d = 3$, there exist $d + 1 = 4$ Mutually Unbiased Bases whose vectors live in the cyclotomic rationals $\mathbb{Q}(\omega)$ ($\omega^2 + \omega + 1 = 0$) and exhibit exact rational pairwise overlap $|\langle u | v \rangle|^2 = 1/3$ between any vectors from distinct bases.
- **Formal Theorems**:
  - `P208cCommutatorTomography.Cyclo3.mub0_orthonormal`
  - `P208cCommutatorTomography.Cyclo3.mub1_orthonormal`
  - `P208cCommutatorTomography.Cyclo3.mub2_orthonormal`
  - `P208cCommutatorTomography.Cyclo3.mub3_orthonormal`
  - `P208cCommutatorTomography.Cyclo3.mub0_mub1_unbiased`
  - `P208cCommutatorTomography.Cyclo3.mub0_mub2_unbiased`
  - `P208cCommutatorTomography.Cyclo3.mub0_mub3_unbiased`
  - `P208cCommutatorTomography.Cyclo3.mub1_mub2_unbiased`
  - `P208cCommutatorTomography.Cyclo3.mub1_mub3_unbiased`
  - `P208cCommutatorTomography.Cyclo3.mub2_mub3_unbiased`
- **Axiom Status**: `{propext}`.
- **Evidence Paths**:
  - `research/p208c_commutator_tomography/lean/CommutatorTomography.lean`
  - `research/p208c_commutator_tomography/tomography.py`
  - `research/p208c_commutator_tomography/tests/test_tomography.py`
- **Claim Discipline**:
  1. *What it supports*: Confirms exact constructive existence of complete MUB sets in dimension 3 using cyclotomic arithmetic.
  2. *What it does not support*: Does not imply existence of complete MUB sets in composite non-power dimensions such as dimension 6.
  3. *Narrowest defensible claim*: The 4 explicit bases in dimension 3 are mutually unbiased with pairwise overlap $1/3$.
  4. *Next test needed*: Verification of discrete Wigner functions on the discrete grid.

---

## CL-P208C-04: Discrete Mutually Unbiased Bases in Dimension d = 4

- **Statement**: In dimension $d = 4$, there exist $d + 1 = 5$ Mutually Unbiased Bases whose vectors live in the Gaussian rationals $\mathbb{Q}(i)$ ($i^2 = -1$) and exhibit exact rational pairwise overlap $|\langle u | v \rangle|^2 = 1/4$ between any vectors from distinct bases.
- **Formal Theorems**:
  - `P208cCommutatorTomography.GaussInt.mub4_0_orthonormal`
  - `P208cCommutatorTomography.GaussInt.mub4_1_orthonormal`
  - `P208cCommutatorTomography.GaussInt.mub4_2_orthonormal`
  - `P208cCommutatorTomography.GaussInt.mub4_3_orthonormal`
  - `P208cCommutatorTomography.GaussInt.mub4_4_orthonormal`
  - `P208cCommutatorTomography.GaussInt.mub4_0_1_unbiased` through `mub4_3_4_unbiased` (10 pairwise theorems)
- **Axiom Status**: `{propext}`.
- **Evidence Paths**:
  - `research/p208c_commutator_tomography/lean/CommutatorTomography.lean`
  - `research/p208c_commutator_tomography/tomography.py`
  - `research/p208c_commutator_tomography/tests/test_tomography.py`
- **Claim Discipline**:
  1. *What it supports*: Confirms exact constructive existence of complete MUB sets in power dimension 4 using Gaussian rational arithmetic.
  2. *What it does not support*: Does not extend to arbitrary composite non-power dimensions.
  3. *Narrowest defensible claim*: The 5 explicit bases in dimension 4 are mutually unbiased with pairwise overlap $1/4$.
  4. *Next test needed*: Construction of stabilizer codes from the maximal abelian subgroups in dimension 4.

---

## CL-P208C-05: Complete Operational State Tomography

- **Statement**: Any discrete carrier density matrix $\rho$ of dimension $d \in \{3, 4\}$ is completely and identically reconstructed from projection measurement probabilities along all $d + 1$ MUBs via Wootters closed-form inversion and exact rational linear system solving.
- **Evidence Paths**:
  - `research/p208c_commutator_tomography/tomography.py`
  - `research/p208c_commutator_tomography/tests/test_tomography.py`
- **Claim Discipline**:
  1. *What it supports*: Demonstrates that projection statistics along $d+1$ MUBs constitute an informationally complete operational measurement frame in dimensions 3 and 4.
  2. *What it does not support*: Does not address finite sample statistical noise or continuous variable state estimation.
  3. *Narrowest defensible claim*: Given exact rational probabilities along the constructed MUBs, state reconstruction is exact with zero reconstruction error.
  4. *Next test needed*: Maximum likelihood estimation for simulated finite-count measurement records.
