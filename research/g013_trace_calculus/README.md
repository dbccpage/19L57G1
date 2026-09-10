# G013 — Coherent Trace Calculus & Higher Cell Algebra

Target G013 of Genesis Cohort 4 establishes a formal trace calculus integrating 0-cells (states), 1-cells (execution traces), higher 2-cells (replay equivalences), endpoint factorization, observer trace congruence, and additive price cocycles.

## Overview

In operational and categorical foundations of computation, execution paths between configurations are modeled as directed 1-cells, while computational equivalence between distinct execution routes sharing identical endpoints is mediated by higher 2-cells.

This package provides:
1. **0-Cells and 1-Cells**: Discrete state structures and chained transition traces with composition and replay execution semantics.
2. **Higher 2-Cells**: Replay equivalences between parallel 1-cells (commuting independent steps, identity cancellations) with vertical composition ($\circ_1$), horizontal composition ($\circ_0$), and Middle Four Interchange coherence.
3. **Endpoint Factorization**: Constructive formalization showing that future state trajectories from past histories factor through the terminal 0-cell endpoint (`future_factors_through_endpoint`).
4. **Observer Trace Congruence**: Formalization of observer projections where states indistinguishable under observation preserve identical future continuation readouts without unrecorded residuals.
5. **Additive Price Cocycles**: Valuations on 1-cells satisfying cocycle additivity and 2-cell homotopy price invariance.

## Artifact Scope & Claim Discipline

### 1. What This Artifact Supports
- In the constructive Lean 4 formalization (`lean/`), it provides checked proofs that:
  - 1-cell concatenation satisfies left identity, right identity, and associativity.
  - The Middle Four Interchange construction yields parallel 2-cells with matching source and target traces.
  - Future continuations from any past history factor strictly through the terminal state endpoint for deterministic and guarded transition systems.
  - Observer trace congruence forms an equivalence relation and preserves future observable continuation readouts.
  - Trace prices decompose additively under concatenation and remain invariant under commuting 2-cell homotopies with equal branch costs.
- In the Python test suite (`tests/`), 21 tests demonstrate empirical validity across linear pipelines, diamond DAGs, 2D rectangular grids, and cyclic state machines.

### 2. What This Artifact Does Not Support
- Does not assert that every empirical physical process admits a finite discrete 2-cell presentation.
- Does not assert complete canonical normal forms for undecidable or infinite rewriting systems.
- Does not assert unconstrained observer descent across non-projective observational channels.

### 3. The Narrowest Defensible Claim
Under the declared algebraic assumptions of discrete transition graphs and constructive type theory, execution traces form a coherent strict 2-category with respect to replay equivalence, where future state trajectories factor through terminal 0-cell boundaries, and additive price valuations are invariant under homotopy equivalences.

### 4. The Next Test Needed
Formalize infinite-horizon trace limits, non-deterministic branching bisimulations, and multi-observer co-limit gluing under presentation symmetries (Target G014).

## Structure

```
research/g013_trace_calculus/
├── README.md               # Architecture, theory, and claim discipline summary
├── CLAIMS.md               # Ledger of definitions, claims, theorems, and evidence paths
├── pyproject.toml          # Test and type-checker configuration
├── verify.py               # Master verification harness (pytest, lake build, axiom audit)
├── trace.py                # 0-cells, 1-cells, concatenation, and replay execution
├── higher_cell.py          # 2-cells, vertical/horizontal composition, and interchange
├── factorization.py        # Endpoint factorization witnesses and graph sweeps
├── congruence.py           # Observer trace congruence and residual audits
├── price.py                # Additive price cocycles and homotopy invariance
├── tests/
│   ├── test_trace.py
│   ├── test_higher_cells.py
│   ├── test_endpoint_factorization.py
│   ├── test_observer_congruence.py
│   └── test_price.py
├── lean/
│   ├── lakefile.toml       # Lean 4 build specification
│   ├── lean-toolchain      # leanprover/lean4:v4.33.0
│   ├── Trace.lean          # 0-cells, 1-cells, trace concatenation
│   ├── HigherCell.lean     # 2-cells, horizontal/vertical composition, interchange
│   ├── Factorization.lean  # Constructive future_factors_through_endpoint
│   ├── Congruence.lean     # Observer trace congruence and residual-free continuation
│   ├── Price.lean          # Additive price cocycles and homotopy invariance
│   └── Inventory.lean      # Metaprogrammed census and zero-private-theorems verification
└── evidence/
    └── receipt.json        # Pinned verification receipt and source code digests
```

## Verification

To execute the complete verification pipeline:

```bash
python verify.py
```

The script verifies:
1. All Python tests pass under `pytest`.
2. The Lean 4 package compiles without errors via `lake build`.
3. The Lean theorem census confirms zero private theorems and checks that all declarations depend strictly on allowed constructive axioms (`{propext, Quot.sound}`).
4. Compiles and checks `evidence/receipt.json`.
