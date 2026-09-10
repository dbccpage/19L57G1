# Target G014: Multi-Observer Descent & Natural Transport

This package implements and formally verifies multi-observer descent, joint observation fiber spaces, compatible gluing over finite observer covers, natural transport across frame automorphisms, duplicate observer agreement, and explicit obstruction witnesses.

## Components

- `observer_descent.py`: Core Python implementation of multi-locus carriers, observer projections, overlap compatibility, sheaf gluing, and natural transport.
- `tests/test_observer_descent.py`: Pytest suite exercising descent, gluing, obstruction witnesses, natural transport, and duplicate observers.
- `lean/ObserverDescent.lean`: 100% constructive core Lean 4 formalization of gluing existence, uniqueness, failed-gluing obstruction, natural transport commutation, and duplicate observer agreement.
- `lean/Inventory.lean`: Census and axiom verification confirming zero external axioms.
- `verify.py`: Top-level verification harness executing source hygiene, pytest, lake build, and axiom audits.

## Running Verification

```bash
python research/g014_observer_descent/verify.py
```
