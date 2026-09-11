# Genesis Target P209c: Stabilizer Error-Correcting Codes on Affine Grids

AuthorityEffect: None.

This package formalizes and computationally implements stabilizer error-correcting codes on discrete multi-carrier state spaces and finite geometric incidence structures.

## Overview

Target P209c establishes:
1. **Pauli String Algebra & Discrete Carriers**:
   - Exact integer and Pauli string arithmetic over discrete two-level state carriers.
   - Exact multiplication, Kronecker tensor products, and commutation relations via binary symplectic vector coordinates.
2. **Three-Carrier Bit-Flip Code [[3, 1, 1]]**:
   - Stabilizer generators: $S_1 = ZZI$, $S_2 = IZZ$.
   - Encoded logical operators: $Z_L = ZZZ$, $X_L = XXX$.
   - Four distinct syndrome signatures diagnosing single bit-flip operations.
3. **Four-Carrier CSS Torus Code [[4, 2, 2]]**:
   - Dual stabilizers $S_Z = ZZZZ$ and $S_X = XXXX$ on a periodic 2-torus.
   - Two independent logical carrier algebras:
     $(Z_{L1} = ZZII, X_{L1} = XIXI)$ and $(Z_{L2} = ZIZI, X_{L2} = XXII)$.
   - Distance-2 error detection across all 12 single-carrier Pauli operators.
4. **Steane [[7, 1, 3]] CSS Code on the Fano Plane $PG(2, 2)$**:
   - 6 weight-4 generators constructed from 3 dual lines of the Fano plane.
   - Even pairwise intersection cardinalities ($|h_i \cap h_j| = 2 \equiv 0 \pmod 2$) algebraically enforcing generator commutativity.
   - Logical operators $X_L = X^{\otimes 7}, Z_L = Z^{\otimes 7}$.
   - Transversal Hadamard operational step $H^{\otimes 7}$ preserving the stabilizer group and interchanging logical $X_L \leftrightarrow Z_L$.
   - Deterministic diagnosis and correction of all 21 single-carrier Pauli errors.
5. **Stabilizer Projection Operator**:
   - Exact matrix representation $\Pi_S = \frac{1}{|S|} \sum_{M \in S} M$ with exact integer idempotence $\Pi_S^2 = \Pi_S$ and trace matching codespace dimension.
6. **Constructive Formalization**:
   - Core Lean 4 formalization with 100 verified theorems.
   - Axiom dependency strictly contained in `{propext, Quot.sound}` (zero `Classical.choice`, zero `mathlib`, zero `sorry`/`admit`).

## Directory Structure

```text
research/p209c_stabilizer_codes/
├── CLAIMS.md                   # Formal claims ledger with 4-part claim discipline
├── README.md                   # Architectural overview and usage guide
├── pyproject.toml              # Pytest and strict mypy configuration
├── stabilizer_codes.py         # Exact Python implementation of stabilizer codes
├── verify.py                   # Automated verification and governance harness
├── evidence/
│   └── receipt.json            # Machine-readable verification receipt
├── lean/
│   ├── StabilizerCodes.lean    # Constructive Lean 4 formalization
│   ├── Inventory.lean          # Metatheoretic theorem census and axiom auditor
│   ├── lakefile.toml           # Lake build configuration
│   └── lean-toolchain          # Lean 4 toolchain (leanprover/lean4:v4.33.0)
└── tests/
    └── test_stabilizer.py      # Pytest test suite (23 test cases)
```

## Verification & Commands

All verification gates run locally:

```pwsh
# 1. Run full verification harness (source hygiene, pytest, Lean build, axiom audit, receipt)
python verify.py --write

# 2. Check receipt against fresh run
python verify.py --check

# 3. Run pytest test suite directly
python -m pytest -v tests

# 4. Build Lean 4 package directly
cd lean
lake build
lake env lean Inventory.lean
```

## Governance & Vocabulary Hygiene

This research package strictly enforces:
- Zero prose occurrences of watched terms.
- Zero unpermitted claim verbs.
- Complete local receipt generation with zero hosted CI dependencies.
