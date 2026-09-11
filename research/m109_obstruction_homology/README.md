# Target M109: Higher Chain Complexes & Obstruction Homology

This package formalizes, implements, and verifies higher chain complexes, boundary and coboundary nilpotency, exact rational homology and cohomology computation over $\mathbb{Q}$, and obstruction classes detecting non-trivial circulation on discrete relational move complexes.

## Components

- `homology.py`: Python engine implementing exact rational linear algebra over $\mathbb{Q}$, graded chain complexes $C_k$, dual cochain complexes $C^k$, Betti numbers $\beta_k = \dim H_k(C; \mathbb{Q}) = \dim H^k(C; \mathbb{Q})$, discrete Stokes-Cartan evaluation, canonical complex builders ($S^1$, $T^2$, $S^2$, $D^3$), and Target 7 move complex scaling.
- `tests/test_homology.py`: Comprehensive test suite covering 14 test cases spanning linear algebra, nilpotency, duality, alternating Betti sum invariants, obstruction detection, and Target 7 integration.
- `lean/ObstructionHomology.lean`: Constructive core Lean 4 formalization containing 12 theorems verifying chain and coboundary nilpotency, discrete relational square boundaries, Stokes duality, and the native commitment-growth obstruction witness.
- `lean/Inventory.lean`: Theorem census and axiom audit confirming all theorems evaluate within `{propext, Quot.sound}`.
- `verify.py`: Top-level verification harness executing source hygiene checks, pytest suite, `lake build`, and Lean axiom verification, emitting `evidence/receipt.json`.
- `CLAIMS.md`: Claims ledger observing the Claim Hygiene Rule.

## Running Verification

To execute the automated verification harness and regenerate `evidence/receipt.json`:

```bash
python research/m109_obstruction_homology/verify.py
```

To run the unit test suite directly:

```bash
python -m pytest -v research/m109_obstruction_homology/tests
```

To build the constructive Lean 4 formalization:

```bash
cd research/m109_obstruction_homology/lean
lake build
lake env lean Inventory.lean
```
