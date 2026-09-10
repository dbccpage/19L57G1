# Target M104 / M107: Coherent Equality Layers & Derived Order Family

This package formalizes and verifies the separation of four equality layers (presentation, definitional, propositional, observational) and three derived operational orders (reachability, observer refinement, trace cost).

## Components

- `equality_order.py`: Python engine implementing terms, normal form evaluation, hidden sector carriers, quotient price invariance, and the three derived orders.
- `tests/test_equality_order.py`: Unit test suite covering equality layer separations, quotient invariance, preorder/poset properties, and order non-conflation.
- `lean/EqualityOrder.lean`: 100% constructive core Lean 4 formalization with 12 theorems verifying layer hierarchy, separation witnesses, order reflexivity/transitivity, and non-conflation.
- `lean/Inventory.lean`: Theorem census and axiom verification confirming zero external axioms.
- `verify.py`: Top-level verification harness executing source hygiene, pytest, lake build, and axiom audits.

## Running Verification

```bash
python research/m104_equality_order/verify.py
```
