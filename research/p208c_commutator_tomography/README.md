# Target P208c: Finite Commutator Obstruction & Discrete MUB Tomography

## Overview

This research package formalizes the finite-dimensional commutator trace obstruction, multi-locus microcausality on composite carrier networks, discrete Mutually Unbiased Bases (MUBs) in dimensions 3 and 4, and complete operational state tomography under Target P208c.

AuthorityEffect: None.
Axiom Scope: Constructive core Lean 4; `#print axioms` strictly within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## Core Theorems & Implementations

### 1. Finite-Dimensional Commutator Trace Obstruction
For any finite $N \times N$ matrices $A, B$ over any field of characteristic 0:
$$\operatorname{Tr}([A, B]) = \operatorname{Tr}(A B - B A) = 0$$
Consequently, the continuous canonical commutation relation $[Q, P] = c \cdot I_N$ with $c \neq 0$ is algebraically obstructed on any finite-dimensional carrier of dimension $N \ge 1$:
$$\operatorname{Tr}([Q, P]) = 0 \neq N \cdot c = \operatorname{Tr}(c \cdot I_N)$$
This demonstrates that unbounded continuum commutation relations cannot be embedded into finite-dimensional discrete substrates without algebraic breakdown.

### 2. Multi-Locus Microcausality on Composite Carriers
On a composite multi-locus carrier network with loci $A$ and $B$:
- Observables localized on disjoint loci strictly commute:
  $$[A \otimes I_B, I_A \otimes B] = 0$$
- In contrast, conjugate operational step operators localized on the same locus (discrete clock $Z$ and shift $X$) fail to commute:
  $$Z X = \omega X Z \implies [Z, X] = (\omega - 1) X Z \neq 0$$

### 3. Discrete Mutually Unbiased Bases (MUBs)
In finite carrier dimensions, maximal sets of $d + 1$ MUBs provide complete operational state determination:
- **Dimension $d = 3$**: Construction of $d + 1 = 4$ MUBs over the cyclotomic rationals $\mathbb{Q}(\omega)$ ($\omega^2 + \omega + 1 = 0$).
- **Dimension $d = 4$**: Construction of $d + 1 = 5$ MUBs over the Gaussian rationals $\mathbb{Q}(i)$ ($i^2 = -1$).
- **Pairwise Unbiasedness**: For any two vectors $u, v$ belonging to distinct bases:
  $$|\langle u | v \rangle|^2 = \frac{1}{d}$$
  yielding exact rational overlap $1/3$ in dimension 3 and $1/4$ in dimension 4.

### 4. Complete Operational State Tomography
Any discrete carrier state represented by density operator $\rho$ is completely determined by projection measurement probabilities along all $d + 1$ MUBs:
$$p_{b, k} = \operatorname{Tr}(\rho \, \Pi_{b, k})$$
The package provides two independent exact reconstruction algorithms:
1. **Wootters Dual Frame Closed-Form Inversion**:
   $$\rho = \sum_{b=0}^d \sum_{k=0}^{d-1} p_{b, k} \, \Pi_{b, k} - I_d$$
2. **Exact Rational Linear Inversion**:
   Expresses $\rho$ in a $d^2$-dimensional Hermitian operator frame and inverts the rational measurement Gram matrix using Gaussian elimination. Both methods yield identical reconstruction.

---

## Verification & Receipts

Run the comprehensive verification harness:
```bash
python verify.py --check
```
This harness executes:
1. Source hygiene audit (enforces absence of `sorry`, `admit`, `unsafe`, `partial`, `axiom`, and watched terms).
2. Pytest suite across `tests/test_tomography.py` (10 unit and property tests).
3. Lean 4 package build via `lake build`.
4. Metatheoretic theorem census and axiom verification in `Inventory.lean` (73 theorems verified within `{propext, Quot.sound}`).
5. Validates `evidence/receipt.json`.
