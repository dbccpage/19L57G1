# Target P209a: Discrete Wigner Phase_Spaces on Odd_Prime Dimensions

## Overview

This research package formalizes discrete Wigner phase_spaces on finite state carriers of odd_prime dimensions $p \in \{3, 5\}$, discrete Weyl displacement operators, Gross phase_point operators, stabilizer state non-negativity, and magic state negativity witnesses under Target P209a.

AuthorityEffect: None.
Axiom Scope: Constructive core Lean 4; `#print axioms` strictly within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## Core Theorems & Implementations

### 1. Parity Reflection Operator and Gross Phase_Space Covariance
On discrete state carriers of odd_prime dimension $p$, the parity reflection operator $P$ is defined by:
$$P |j\rangle = |-j \pmod p\rangle$$
Properties:
- **Involution**: $P^2 = I_p$.
- **Unit Trace**: $\operatorname{Tr}(P) = 1$.
- **Gross Covariance**: Reflection about the origin inverts discrete translation shift $X$ and clock $Z$:
  $$P X P = X^{-1}, \quad P Z P = Z^{-1}$$

### 2. Discrete Weyl Displacements and Gross Phase_Point Operators
For discrete phase_space coordinates $(q, p) \in \mathbb{F}_p \times \mathbb{F}_p$:
- **Discrete Weyl Displacement**:
  $$D(q, p) = \zeta_p^{2^{-1} q p} X^q Z^p$$
  where $2^{-1} = (p + 1) / 2 \pmod p$.
- **Gross Phase_Point Operator**:
  $$A(q, p) = D(q, p) P D(q, p)^\dagger$$
  Satisfying:
  - $A(0, 0) = P$.
  - Self-adjoint involution: $A(q, p)^\dagger = A(q, p)$ and $A(q, p)^2 = I_p$.
  - Unit trace: $\operatorname{Tr}(A(q, p)) = 1$.
  - **Completeness**: $\sum_{q, p} A(q, p) = p \cdot I_p$.
  - **Orthogonality**: $\operatorname{Tr}(A(q, p) A(q', p')) = p \cdot \delta_{q q'} \delta_{p p'}$.

### 3. Discrete Wigner Distribution and State Reconstruction
For any state carrier density operator $\rho$:
$$W_\rho(q, p) = \frac{1}{p} \operatorname{Tr}(\rho A(q, p))$$
- **Probability Normalization**: $\sum_{q, p} W_\rho(q, p) = \operatorname{Tr}(\rho) = 1$.
- **Exact Reconstruction**:
  $$\rho = \sum_{q, p} W_\rho(q, p) A(q, p)$$
- **Marginal Consistency**: Summing over coordinate $p$ yields position diagonal elements $\sum_p W_\rho(q, p) = \langle q | \rho | q \rangle$.

### 4. Stabilizer Non-Negativity and Magic State Negativity Witnesses
- **Stabilizer Non-Negativity**: For stabilizer eigenstates $|0\rangle$ and $|+\rangle$, $W(q, p) \ge 0$ everywhere on $\mathbb{F}_p \times \mathbb{F}_p$.
- **Magic State Negativity Witness**: For the non_classical resource state $|M\rangle = \frac{1}{\sqrt{2}}(|1\rangle - |p-1\rangle)$:
  $$P |M\rangle = -|M\rangle$$
  yielding a strict point negativity witness at the origin:
  $$W_{|M\rangle}(0, 0) = -\frac{1}{p} < 0$$
  specifically $W(0, 0) = -1/3$ in dimension 3 and $W(0, 0) = -1/5$ in dimension 5.

---

## Verification & Receipts

Run the verification harness from within `research/p209a_wigner_phase_space/`:
```bash
python verify.py --check
```
This harness executes:
1. Source hygiene audit (enforcing absence of `sorry`, `admit`, `unsafe`, `partial`, `axiom`, watched vocabulary terms, and forbidden claim words).
2. Pytest suite across `tests/test_wigner.py` (39 test cases covering dimension sweeps on 3 and 5).
3. Lean 4 package build via `lake build`.
4. Theorem census and axiom verification in `Inventory.lean` (36 theorems verified within `{propext, Quot.sound}`).
5. Validates `evidence/receipt.json`.
