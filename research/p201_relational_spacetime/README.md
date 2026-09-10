# Target P201 / P202: Relational Dimensions, Calibration & Causal Relational Clocks

This package formalizes and verifies relational quantities, typed dimensions, unit covariance, dimensionless ratio invariance, future-test equivalence congruence, and embedded relational clock synchronization with exact rational rates in Q.

## Components

- `relational_spacetime.py`: Python implementation of relational quantities, calibration rescaling, dimensionless invariants, future trajectory congruence, and embedded clocks.
- `tests/test_relational_spacetime.py`: Unit test suite covering unit covariance, ratio invariance, cross-dimension refusal, future-test congruence, and clock gear ratios.
- `lean/RelationalSpacetime.lean`: 100% constructive core Lean 4 formalization proving ratio invariance under unit rescaling, dimension disjointness, future-test equivalence congruence, and exact clock synchronization.
- `lean/Inventory.lean`: Census and axiom verification confirming `{propext, Quot.sound}` bounds.
- `verify.py`: Top-level verification harness executing source hygiene, pytest, lake build, and axiom audits.

## Running Verification

```bash
python research/p201_relational_spacetime/verify.py
```
