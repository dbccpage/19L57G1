# Target X302: Operational Reasoning & Belief Revision

## Overview

Target X302 formalizes and implements an endogenous Truth Maintenance System (TMS)
and AGM belief revision engine. It distinguishes firm commitments (represented
axioms) from speculative commitments (contingent hypotheses), maintains an
acyclic justification DAG tracking exact hypothesis dependencies, detects direct
and operational carrier valuation contradictions without host oracles, and computes
minimal hitting set retractions to restore consistency while emitting cryptographically
hashed revision receipts.

## Architecture

```text
research/x302_operational_reasoning/
├── README.md               # Architectural overview, scope, and verification
├── CLAIMS.md               # Reconciled claims ledger (Claim Hygiene compliant)
├── pyproject.toml          # Package configuration and pytest setup
├── reasoning.py            # Pure Python operational reasoning engine
├── tests/
│   └── test_reasoning.py   # Test suite with negative control matrix
├── lean/
│   ├── lakefile.toml       # Lake package configuration
│   ├── lean-toolchain      # Pinned to leanprover/lean4:v4.33.0
│   ├── OperationalReasoning.lean  # Constructive Lean 4 formalization
│   └── Inventory.lean      # Theorem census and axiom audit
├── evidence/
│   └── receipt.json        # Cryptographic verification receipt
└── verify.py               # Master verification and audit harness
```

## Key Components

1. **Commitment Classes**:
   - `AXIOM`: Firm structural invariants with empty hypothesis support (`supp = ∅`). Immutable: cannot be retracted.
   - `HYPOTHESIS`: Speculative assumptions carrying unique identifiers and integer entrenchment weights (`supp = {h}`).

2. **Endogenous Truth Maintenance System**:
   - Maintains a directed acyclic justification graph.
   - Computes exact hypothesis support sets across deduction steps:
     $$\operatorname{supp}(n) = \bigcup_{p \in \text{antecedents}(n)} \operatorname{supp}(p)$$
   - Cycle detection prevents circular derivations.

3. **Contradiction Detection**:
   - *Direct Contradiction:* Simultaneous derivation of $\phi$ and $\neg \phi \vdash \bot$.
   - *Operational Contradiction:* Conflicting carrier variable assignments $x = v_1 \wedge x = v_2$ where $v_1 \neq v_2$.
   - When $\operatorname{supp}(\bot) = \emptyset$, raises `FoundationalInconsistencyError`.

4. **Minimal Retraction (AGM Belief Revision)**:
   - Computes minimum hitting sets over all active conflict sets $\mathcal{S}$:
     $$\forall S \in \mathcal{S}, \quad R \cap S \neq \emptyset$$
   - Prioritizes minimal cardinality $|R|$, breaking ties by minimal total entrenchment weight and lexicographical order.
   - Deactivates all nodes dependent on $R$ down the DAG.
   - Emits immutable `RevisionReceipt` with deterministic SHA-256 hash.

5. **Constructive Lean 4 Formalization**:
   - 18 substantive theorems in `lean/OperationalReasoning.lean`.
   - `#print axioms` verified strictly within `{propext, Quot.sound}` (17 theorems axiom-free, 1 using `propext`).
   - Zero `mathlib`, zero `Classical.choice`.

## Verification Commands

Run the master verification harness:

```powershell
python research/x302_operational_reasoning/verify.py
```

Run receipt validation check:

```powershell
python research/x302_operational_reasoning/verify.py --check
```

Run test suite directly:

```powershell
python -m pytest -v research/x302_operational_reasoning/tests
```

Build Lean 4 package:

```powershell
cd research/x302_operational_reasoning/lean
lake build
lake env lean Inventory.lean
```
