# Target P209d: Non-Classicality Horizons & Gottesman-Knill Boundary

## Overview

This research package formalizes and implements the Gottesman-Knill symplectic tableau simulator, the Discrete Hudson theorem boundary on discrete carrier phase_space, and the exponential resource scaling boundary induced by non-stabilizer magic state injection under Target P209d.

AuthorityEffect: None.
Axiom Scope: Constructive core Lean 4; `#print axioms` strictly within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## Core Theorems & Implementations

### 1. Gottesman-Knill Symplectic Tableau Simulator
On an $n$-carrier discrete substrate over the binary field $\\mathbb{F}_2$:
- **Tableau Representation**: An $(2n) \\times (2n+1)$ binary tableau tracks $n$ destabilizer generators $D_i$ and $n$ stabilizer generators $S_i$ alongside sign bits $r_i \\in \\{0, 1\\}$.
- **Polynomial Update Scaling**: Clifford generators (Hadamard $H$, $S$-gate, and $CNOT$) execute in $O(n^2)$ arithmetic operations over $\\mathbb{F}_2$.
- **Symplectic Invariant Preservation**: Every Clifford generator acts as a symplectic automorphism preserving the discrete metric:
  $$\\Omega(M u, M v) = \\Omega(u, v) \\pmod 2$$
  maintaining mutual stabilizer commutativity $\\Omega(S_i, S_j) = 0$ and conjugate destabilizer duality $\\Omega(D_i, S_j) = \\delta_{ij}$.
- **Measurement and Reduction**: Pauli $Z$-measurements execute in $O(n^2)$ steps, distinguishing deterministic outcomes (stabilizer subspace projection) from random outcomes (generating state collapse and updating the tableau basis).

### 2. The Non-Classicality Horizon & Discrete Hudson Boundary
On discrete carrier phase_space $\mathbb{F}_p \times \mathbb{F}_p$ for odd_prime dimension $p = 3$:
- **Discrete Wigner Quasiprobability**: Constructed via Gross phase_point operators $A(q, p)$ derived from Weyl-Heisenberg displacement operators $D(u, v) = \omega^{2 u v} X^u Z^v$.
- **Stabilizer States**: Inhabit the non-negative Wigner cone ($W \\ge 0$) everywhere across the $p \\times p$ grid.
- **Magic States**: Break non-negativity, attaining strictly negative Wigner quasiprobability values ($W(0, 0) = -1/3 < 0$), establishing contextuality as the operational resource boundary.

### 3. Magic State Tracking & Exponential Resource Boundary
- Injecting $k$ non-stabilizer magic states (such as $|T\\rangle = \\frac{1}{\\sqrt{2}}(|0\\rangle + e^{i\\pi/4}|1\\rangle)$) breaks single-tableau closure.
- In the stabilizer basis decomposition, simulating $k$ injected magic states requires tracking a superposition mixture over $2^k$ stabilizer tableaux.
- The simulation complexity branches exponentially as $\\Omega(2^k \\cdot n^2)$, establishing the boundary between classical polynomial efficiency and non-classical simulation hardness.

---

## Verification & Receipts

Run the comprehensive verification harness:
```bash
python verify.py --check
```
To refresh the evidence receipt:
```bash
python verify.py --write
```

The harness executes:
1. Source hygiene check (enforces absence of `sorry`, `admit`, `unsafe`, `partial`, `axiom`, and watched vocabulary terms).
2. Pytest suite across `tests/test_horizons.py` (20 unit, integration, and property tests).
3. Lean 4 package build via `lake build`.
4. Metatheoretic theorem census and axiom audit in `Inventory.lean` (55 theorems verified within `{propext, Quot.sound}`).
5. Emits and validates `evidence/receipt.json`.
