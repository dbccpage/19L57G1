# Target P208c: Finite Commutator Obstruction & Discrete MUB Tomography

## Overview

This research package combines Lean theorems for integer matrices and explicit dimension-3 and dimension-4 basis tables with exact Python examples of finite tomography. The Lean commutator obstruction is over `Int`; this package does not contain a characteristic-zero-field parameterization or a Lean tomography theorem.

AuthorityEffect: None.
Axiom Scope: Constructive core Lean 4; `#print axioms` strictly within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## Core Theorems & Implementations

### 1. Finite-Dimensional Commutator Trace Obstruction
The cited Lean theorem states, for finite $N \times N$ matrices $A,B$ over the integers:
$$\operatorname{Tr}([A, B]) = \operatorname{Tr}(A B - B A) = 0$$
Consequently, for the implemented integer matrices and nonzero integer $c$, $[Q, P] = c \cdot I_N$ is obstructed when $N \ge 1$:
$$\operatorname{Tr}([Q, P]) = 0 \neq N \cdot c = \operatorname{Tr}(c \cdot I_N)$$
The corresponding statement over an arbitrary characteristic-zero field requires a separately parameterized proof; the present Lean theorem does not address an embedding of continuous systems.

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
The Python implementation reconstructs the exact finite examples it evaluates in dimensions 3 and 4 from projection probabilities along the listed MUBs. There is no cited Lean reconstruction theorem:
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
2. Pytest suite across `tests/test_tomography.py` (15 tests. Correction, 2026-09-24: this said 10 unit and property tests, already stale at 12 before three negative tests were added).
3. Lean 4 package build via `lake build`.
4. Metatheoretic theorem census and axiom verification in `Inventory.lean` (73 theorems verified within `{propext, Quot.sound}`).
5. Validates `evidence/receipt.json`.

## Correction, 2026-09-25: the zero scalar

`verify_canonical_commutation_obstruction(N, 0)` returned `True`
("obstructed") for every `N >= 1`, although `Q = P = I_N` solves
`[Q, P] = 0 * I_N`; its own inline comment named the commuting solutions.
The claim, in Lean and in `CLAIMS.md`, covers nonzero `c` only, and no
committed result called the function at zero. It now answers `False` at
`c = 0`, computed on that witness, and
`test_commutation_at_zero_is_not_obstructed` pins the answer for
`N = 1, 2, 3, 4, 10`. The receipt was regenerated through `verify.py`.
