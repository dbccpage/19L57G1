# Retained-Record Enablement Multi-Depth Ladder

## Target 6 Deliverable

This directory scales depth-two retained-record enablement to an arbitrary multi-depth ladder.

### Components

1. **Formal Core Lean 4 (`lean/DepthLadder.lean`):**
   - Implements generic `windowsOf (k : Nat) : List Nat → List (List Nat)` without ad-hoc tuple types.
   - Defines `functional (k : Nat) (tape : List Nat) : Prop` stating that length-$(k+1)$ windows agreeing on their length-$k$ prefix must be identical.
   - Proves `ladder_monotonic (k : Nat) (tape : List Nat) : functional k tape → functional (k + 1) tape` constructively.
   - Verified clean under `#print axioms` strictly contained in `{propext, Quot.sound}` (zero `Classical.choice`, zero `mathlib`).

2. **Python Mirror & Sweep Verification (`multi_depth.py`):**
   - Implements arbitrary depth-$d$ retained-record enablement machines on arity-$(d+1)$ control forms admitted under the sealed grammar.
   - Mirrors `windows`, `functional`, and monotonicity checks.
   - Verified renaming invariance across 1,152 sweep runs (6 carrier permutations $\times$ 64 deterministic programs $\times$ 3 initial states) without host logs or external oracles.
   - Implements generic witness construction `twist_tape(k)` proving strict inclusion of depth classes for all $k \ge 1$.

3. **Receipts & Audits:**
   - `verify_lean.py`: Audits that all Lean proofs compile and depend only on `{propext, Quot.sound}`.
   - `test_multi_depth.py`: 6 unit tests covering window extraction, functionality, monotonicity, strict ladder separation, and 1,152 sweep runs.
   - `receipts/multi_depth.json`: Pinned execution receipt.
