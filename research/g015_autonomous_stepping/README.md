# Target G015 / G017: First-Demand, Invocation Bridge & Autonomous Stepping

This package formalizes and verifies demand lifecycle management, first-demand index selection, autonomous endogenous stepping without host oracles, prohibition of spontaneous demand from inert histories, and finite saturation with exact resource accounting.

## Components

- `stepping.py`: Python engine for demand records, priority selection, autonomous transitions, and saturation loops.
- `tests/test_stepping.py`: Unit test suite covering priority selection, tie-breaking, stepping transitions, quiescence, inert histories, and refusals.
- `lean/AutonomousStepping.lean`: 100% constructive core Lean 4 formalization of demand stepping, refusal state preservation, resource conservation, and finite saturation.
- `lean/Inventory.lean`: Census and axiom verification confirming `{propext, Quot.sound}` bounds.
- `verify.py`: Top-level verification harness executing source hygiene, pytest, lake build, and axiom audits.

## Running Verification

```bash
python research/g015_autonomous_stepping/verify.py
```
