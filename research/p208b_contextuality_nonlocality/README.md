# Target P208b: Rational Bell-CHSH Nonlocality & Cabello 18-Ray Contextuality

AuthorityEffect: None.

## Overview

This research package provides a constructive, finite, exact rational treatment of:
1. **Bipartite Bell-CHSH Nonlocality**:
   - Bipartite scenario with binary inputs $x, y \in \{0, 1\}$ and binary outcomes $a, b \in \{+1, -1\}$.
   - Constructive derivation of the Local Hidden Variable (LHV) bound $|S| \le 2$ across all 16 deterministic local response pairs and their convex combinations.
   - Realization of an exact rational non-local correlator achieving $S = 14/5 = 2.8 > 2$ using Pythagorean unit coordinates in $\mathbb{Q}^2$, strictly exceeding the LHV bound while satisfying the no-signaling condition and respecting the algebraic bound $\le 4$.
2. **Cabello 18-Ray Contextuality Configuration**:
   - Discrete set of 18 rays in $\mathbb{Q}^4$ with coordinates in $\{-1, 0, 1\}$.
   - 9 orthogonal contexts of 4 mutually orthogonal rays each.
   - Exact 2-incidence regularity: each ray belongs to exactly 2 contexts ($9 \times 4 = 36 = 18 \times 2$).
   - Non-contextual binary valuation obstruction: the context constraint $\sum_{r \in C_k} v(r) = 1$ leads to $2 \sum_i v(r_i) = 9$, which has no solution over integers.
   - Cohomological characterization as a non-zero Čech 1-cochain obstruction class in $H^1(\mathbb{Z}_2)$.

## Structure

- `correlations.py`: Pure Python module in exact rational arithmetic (`fractions.Fraction`).
- `tests/test_correlations.py`: Pytest suite verifying all algebraic bounds, no-signaling constraints, and incidence structures.
- `lean/ContextualityNonlocality.lean`: Constructive Lean 4 formalization of the LHV bound, rational correlator, and Cabello parity obstruction.
- `lean/Inventory.lean`: Metatheoretic theorem census and axiom dependency audit.
- `verify.py`: Verification harness running hygiene checks, pytest, lake build, and axiom verification.
- `CLAIMS.md`: Precise claim ledger complying with claim hygiene standards.

## Verification

To run all checks and verify receipts:

```bash
python verify.py --write
python verify.py --check
```

All Lean 4 proofs are verified using the Lean 4 compiler without external dependencies (zero mathlib) and depend only on `{propext, Quot.sound}` (zero choice).
