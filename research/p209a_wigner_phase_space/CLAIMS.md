# Claims Ledger: Discrete Wigner Phase_Spaces on Odd_Prime Dimensions (Target P209a)

This ledger documents the formal mathematical and computational claims established by `research/p209a_wigner_phase_space/` under constructive core Lean 4 and exact cyclotomic and rational arithmetic in Python.

AuthorityEffect: None.
Axiom Scope: Strictly within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## CL-P209A-01: Parity Reflection Involution and Tracial Normalization

- **Statement**: On discrete state carriers of odd_prime dimensions $p \in \{3, 5\}$, the parity reflection operator $P$ defined by $P |j\rangle = |-j \pmod p\rangle$ is an involution ($P^2 = I_p$) with unit trace $\operatorname{Tr}(P) = 1$.
- **Formal Theorems**:
  - `P209aWignerPhaseSpace.P3_involution`
  - `P209aWignerPhaseSpace.P3_trace_one`
  - `P209aWignerPhaseSpace.P5_involution`
  - `P209aWignerPhaseSpace.P5_trace_one`
- **Axiom Status**: `{propext, Quot.sound}` for involution; `{propext}` for trace.
- **Evidence Paths**:
  - `research/p209a_wigner_phase_space/lean/WignerPhaseSpace.lean`
  - `research/p209a_wigner_phase_space/wigner_phase_space.py`
  - `research/p209a_wigner_phase_space/tests/test_wigner.py`
- **Claim Discipline**:
  1. *What it supports*: Confirms that discrete parity reflection acts as an involutive reflection with unit trace on odd_prime dimensions.
  2. *What it does not support*: Does not extend to even dimensions ($d=2, 4$) where 2 is not invertible in the base modular field.
  3. *Narrowest defensible claim*: For $p \in \{3, 5\}$, $P^2 = I_p$ and $\operatorname{Tr}(P) = 1$ hold identically over the integers.
  4. *Next test needed*: Evaluate parity reflection on multi-qudit tensor products of odd_prime local factors.

---

## CL-P209A-02: Translation and Clock Operator Orders on Discrete Grids

- **Statement**: On discrete state carriers of dimension $p \in \{3, 5\}$, the translation shift operator $X$ and clock operator $Z$ satisfy $X^p = I_p$ and $Z^p = I_p$.
- **Formal Theorems**:
  - `P209aWignerPhaseSpace.X3_translation_order`
  - `P209aWignerPhaseSpace.X5_translation_order`
  - `P209aWignerPhaseSpace.Z3_clock_order`
- **Axiom Status**: `{propext, Quot.sound}`.
- **Evidence Paths**:
  - `research/p209a_wigner_phase_space/lean/WignerPhaseSpace.lean`
  - `research/p209a_wigner_phase_space/wigner_phase_space.py`
  - `research/p209a_wigner_phase_space/tests/test_wigner.py`
- **Claim Discipline**:
  1. *What it supports*: Demonstrates cyclic periodicity of discrete translation and clock generators on finite grids of dimension $p$.
  2. *What it does not support*: Does not imply continuous translation invariance or unbounded clock generators.
  3. *Narrowest defensible claim*: $X^p = I_p$ and $Z^p = I_p$ for $p \in \{3, 5\}$ over the cyclotomic ring $\mathbb{Z}[\zeta_p]$.
  4. *Next test needed*: Formulate discrete symplectic Clifford transformations stabilizing the discrete Heisenberg-Weyl group.

---

## CL-P209A-03: Gross Phase_Space Covariance

- **Statement**: Conjugation by the parity reflection operator $P$ inverts discrete translation shift $X$ and clock $Z$: $P X P = X^{-1}$ and $P Z P = Z^{-1}$, ensuring covariance of discrete phase_point operators $A(q, p) = D(q, p) P D(q, p)^\dagger$.
- **Formal Theorems**:
  - `P209aWignerPhaseSpace.P3_gross_covariance_X`
  - `P209aWignerPhaseSpace.P5_gross_covariance_X`
  - `P209aWignerPhaseSpace.P3_gross_covariance_Z`
- **Axiom Status**: `{propext, Quot.sound}`.
- **Evidence Paths**:
  - `research/p209a_wigner_phase_space/lean/WignerPhaseSpace.lean`
  - `research/p209a_wigner_phase_space/wigner_phase_space.py`
  - `research/p209a_wigner_phase_space/tests/test_wigner.py`
- **Claim Discipline**:
  1. *What it supports*: Shows that reflection about the origin inverts discrete phase_space displacement coordinates.
  2. *What it does not support*: Does not establish full Clifford covariance for all symplectic transformations.
  3. *Narrowest defensible claim*: Conjugation of $X$ and $Z$ by $P$ implements inversion $X \mapsto X^{-1}$ and $Z \mapsto Z^{-1}$ in dimensions 3 and 5.
  4. *Next test needed*: Characterization of the full symplectic automorphism group preserving Gross phase_point operators.

---

## CL-P209A-04: Completeness and Orthogonality of Phase_Point Operators

- **Statement**: Gross phase_point operators $A(q, p)$ on $\mathbb{F}_p \times \mathbb{F}_p$ form an orthogonal complete operator basis: $\sum_{q, p} A(q, p) = p \cdot I_p$ and $\operatorname{Tr}(A(q, p) A(q', p')) = p \cdot \delta_{q q'} \delta_{p p'}$.
- **Formal Theorems**: Verified by exact computational arithmetic in `wigner_phase_space.py`.
- **Axiom Status**: Metatheoretic exact rational verification.
- **Evidence Paths**:
  - `research/p209a_wigner_phase_space/wigner_phase_space.py`
  - `research/p209a_wigner_phase_space/tests/test_wigner.py`
- **Claim Discipline**:
  1. *What it supports*: Confirms that $A(q, p)$ forms a complete self-adjoint orthogonal operator basis in dimensions 3 and 5.
  2. *What it does not support*: Does not imply that continuous phase_space distributions admit finite orthogonal decompositions.
  3. *Narrowest defensible claim*: For $p \in \{3, 5\}$, the $p^2$ operators $A(q, p)$ satisfy completeness and orthogonality over $\mathbb{Q}(\zeta_p)$.
  4. *Next test needed*: Construction of discrete Wigner kernels on multi-party composite systems.

---

## CL-P209A-05: Stabilizer State Non-Negativity

- **Statement**: Discrete Wigner distributions $W_\rho(q, p) = \frac{1}{p} \operatorname{Tr}(\rho A(q, p))$ for stabilizer eigenstates $|0\rangle$ and $|+\rangle$ are non-negative everywhere on $\mathbb{F}_p \times \mathbb{F}_p$, taking exact rational values in $\{0, 1/p\}$.
- **Formal Theorems**:
  - `P209aWignerPhaseSpace.P3_stabilizer_ket0_eigenstate`
  - `P209aWignerPhaseSpace.P3_stabilizer_ket_plus_eigenstate`
  - `P209aWignerPhaseSpace.P5_stabilizer_ket0_eigenstate`
  - `P209aWignerPhaseSpace.P5_stabilizer_ket_plus_eigenstate`
- **Axiom Status**: `{propext, Quot.sound}`.
- **Evidence Paths**:
  - `research/p209a_wigner_phase_space/lean/WignerPhaseSpace.lean`
  - `research/p209a_wigner_phase_space/wigner_phase_space.py`
  - `research/p209a_wigner_phase_space/tests/test_wigner.py`
- **Claim Discipline**:
  1. *What it supports*: Confirms that discrete stabilizer states admit non-negative quasi-probability representations on discrete phase_space grids.
  2. *What it does not support*: Does not imply non-negativity for non-stabilizer pure states.
  3. *Narrowest defensible claim*: For $p \in \{3, 5\}$, $W_{|0\rangle}(q, p) \ge 0$ and $W_{|+\rangle}(q, p) \ge 0$ at all grid points.
  4. *Next test needed*: Verification of non-negativity across all Clifford orbit states in dimension 3.

---

## CL-P209A-06: Magic State Point Negativity Witness

- **Statement**: Non_classical magic states $|M_3\rangle = \frac{1}{\sqrt{2}}(|1\rangle - |2\rangle)$ and $|M_5\rangle = \frac{1}{\sqrt{2}}(|1\rangle - |4\rangle)$ are odd eigenstates of parity reflection ($P |M\rangle = -|M\rangle$) and witness strict point negativity at the phase_space origin: $W_{|M\rangle}(0, 0) = -1/p < 0$.
- **Formal Theorems**:
  - `P209aWignerPhaseSpace.P3_magic_state_eigenstate`
  - `P209aWignerPhaseSpace.P5_magic_state_eigenstate`
  - `P209aWignerPhaseSpace.magic_state_parity_expectation_3`
  - `P209aWignerPhaseSpace.magic_state_parity_expectation_5`
  - `P209aWignerPhaseSpace.magic_state_negativity_witness_3`
  - `P209aWignerPhaseSpace.magic_state_negativity_witness_5`
- **Axiom Status**: `{propext, Quot.sound}` for eigenstates; `{propext}` for expectation; zero axioms for strict rational inequality.
- **Evidence Paths**:
  - `research/p209a_wigner_phase_space/lean/WignerPhaseSpace.lean`
  - `research/p209a_wigner_phase_space/wigner_phase_space.py`
  - `research/p209a_wigner_phase_space/tests/test_wigner.py`
- **Claim Discipline**:
  1. *What it supports*: Confirms that non-stabilizer resource states exhibit point negativity in discrete Wigner distributions, serving as non_classical witnesses.
  2. *What it does not support*: Does not establish whether negativity is necessary for computational speedup in general settings.
  3. *Narrowest defensible claim*: In dimensions 3 and 5, $|M\rangle$ has $W_{|M\rangle}(0, 0) = -1/p < 0$.
  4. *Next test needed*: Relate discrete negativity volume to contextuality degree and distillation thresholds.

---

## CL-P209A-07: Exact State Reconstruction from Discrete Wigner Distributions

- **Statement**: Any discrete density operator $\rho$ is reconstructed from its discrete Wigner distribution: $\rho = \sum_{q, p} W_\rho(q, p) A(q, p)$, satisfying total normalization $\sum_{q, p} W_\rho(q, p) = \operatorname{Tr}(\rho) = 1$.
- **Formal Theorems**: Verified by exact computational arithmetic in `wigner_phase_space.py`.
- **Axiom Status**: Metatheoretic exact cyclotomic reconstruction.
- **Evidence Paths**:
  - `research/p209a_wigner_phase_space/wigner_phase_space.py`
  - `research/p209a_wigner_phase_space/tests/test_wigner.py`
- **Claim Discipline**:
  1. *What it supports*: Demonstrates exact dual frame inversion from quasi-probability distributions to state operators on discrete carriers.
  2. *What it does not support*: Does not imply state tomography under noisy imperfect measurements.
  3. *Narrowest defensible claim*: For $p \in \{3, 5\}$, exact linear inversion reconstructs $\rho$ from its $p^2$ Wigner values over $\mathbb{Q}(\zeta_p)$.
  4. *Next test needed*: Tomographic sampling efficiency of discrete Wigner point measurements.
