# Target P209d: Non-Classicality Horizons & Gottesman-Knill Boundary

## Overview

This research package contains finite symplectic-tableau examples, three explicitly defined Wigner-value tables in dimension 3, and arithmetic for a declared doubling branch-count recurrence. Its Lean statements do not prove a general simulator correctness theorem, a characterization of all non-negative states, or a lower bound on simulation complexity.

AuthorityEffect: None.
Axiom Scope: Constructive core Lean 4; `#print axioms` strictly within `{propext, Quot.sound}`; zero `Classical.choice`; zero `mathlib`.

---

## Core Theorems & Implementations

### 1. Python symplectic tableau model and explicit Lean identities
The Python model uses a binary tableau with $n$ destabilizer and $n$ stabilizer rows. The cited Lean identities concern one-carrier $H,S$ and two-carrier $CNOT$ vectors; there is no Lean theorem for arbitrary $n$ or a simulator-wide complexity bound.
- **Explicit Symplectic Identities**: The named Lean operations preserve the defined form on their declared vector types:
  $$\\Omega(M u, M v) = \\Omega(u, v) \\pmod 2$$
  maintaining mutual stabilizer commutativity $\\Omega(S_i, S_j) = 0$ and conjugate destabilizer duality $\\Omega(D_i, S_j) = \\delta_{ij}$.
- **Python Measurement Examples**: The tested $Z$-measurement branches distinguish deterministic and random outcomes in the implemented tableau model.

### 2. Explicit Dimension-3 Wigner Tables
On discrete carrier phase_space $\mathbb{F}_p \times \mathbb{F}_p$ for odd_prime dimension $p = 3$:
- **Discrete Wigner Quasiprobability**: Constructed via Gross phase_point operators $A(q, p)$ derived from Weyl-Heisenberg displacement operators $D(u, v) = \omega^{2 u v} X^u Z^v$.
- **Named Stabilizer Tables**: The explicitly defined tables are non-negative across their finite grid. This does not classify all stabilizer states.
- **Declared magic-state table**: Has $W(0, 0) = -1/3 < 0$. The Lean proof checks this defined value; it does not derive the table from a density operator or classify all pure states.

### 3. Declared Branch-Count Model
- The model assigns two branches to each of $k$ declared non-stabilizer insertions; no universal branch requirement is established.
- In the defined recurrence, $B(0)=1$ and $B(k+1)=2B(k)$, hence $B(k)=2^k$.
- This proves arithmetic about that representation, not that every exact or approximate simulator must use $2^k$ branches or time $\\Omega(2^k \\cdot n^2)$.

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
