# G013 — Coherent Trace Calculus & Higher Cell Algebra

Target G013 of Genesis Cohort 4 defines typed traces, proposed 2-cell syntax, endpoint factorization, observer trace congruence, and additive trace prices. Its higher-cell syntax is an exploratory presentation, not yet a strict 2-category of guarded native transitions.

## Overview

In operational and categorical foundations of computation, execution paths between configurations are modeled as directed 1-cells, while computational equivalence between distinct execution routes sharing identical endpoints is mediated by higher 2-cells.

This package provides:
1. **0-Cells and 1-Cells**: Discrete state structures and chained transition traces with composition and replay execution semantics.
2. **Higher 2-Cells**: Constructors between parallel traces, including a constructor for any two parallel two-step routes, together with vertical and horizontal composition syntax. The interchange relation is declared as a constructor of `EqCell2`; independence of the steps is not a premise.
3. **Endpoint Factorization**: Constructive formalization showing that future state trajectories from past histories factor through the terminal 0-cell endpoint (`future_factors_through_endpoint`).
4. **Observer Trace Congruence**: Formalization of observer projections where states indistinguishable under observation preserve identical future continuation readouts without unrecorded residuals.
5. **Additive Trace Prices**: Valuations additive under concatenation. The diamond price lemma assumes equal costs on its two branches.

## Artifact Scope & Claim Discipline

### 1. What This Artifact Supports
- In the constructive Lean 4 formalization (`lean/`), it provides checked proofs that:
  - 1-cell concatenation satisfies left identity, right identity, and associativity.
  - The two interchange compositions have the same indexed source and target traces; their `EqCell2` relation follows from its declared interchange constructor.
  - Future continuations from any past history factor strictly through the terminal state endpoint for deterministic and guarded transition systems.
  - Observer trace congruence forms an equivalence relation and preserves future observable continuation readouts.
  - Trace prices decompose additively under concatenation; equal branch costs imply equal diamond prices.
- In the Python test suite (`tests/`), 21 tests demonstrate empirical validity across linear pipelines, diamond DAGs, 2D rectangular grids, and cyclic state machines.

### 2. What This Artifact Does Not Support
- Does not assert that every empirical physical process admits a finite discrete 2-cell presentation.
- Does not assert complete canonical normal forms for undecidable or infinite rewriting systems.
- Does not assert unconstrained observer descent across non-projective observational channels.
- Does not prove vertical and horizontal unit and associativity laws or quotient well-definedness for 2-cells, nor that the freely admitted two-step cells are valid guarded native commutations.

### 3. The Narrowest Defensible Claim
For the declared discrete transition syntax, typed traces have associative composition and identities. The package constructs parallel 2-cell terms and declares an interchange equivalence between two composites; endpoint and price results hold under their stated premises. A strict 2-category or a native replay equivalence requires further laws and a bridge to guarded transitions.

### 4. The Next Test Needed
First prove vertical and horizontal unit and associativity, interchange and congruence compatibility on a specified quotient, and that each nontrivial 2-cell denotes a permitted commuting square of guarded native steps. Infinite-horizon and multi-observer extensions can follow that bridge.

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
