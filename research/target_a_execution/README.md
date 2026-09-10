# Target A: Represented Execution Substrate

AuthorityEffect: None.  
Configuration status: DECLARED_HOST_CONFIG.

## 1. Overview

Target A establishes an autonomous, data-driven execution substrate where encoded program graphs drive a stepwise interpreter directly from stored carrier instances without consulting unencoded host operation functions (`F.ops`).

The substrate operates across both a Python reference mirror and a constructive formalization in Lean 4 (`#print axioms ⊆ {propext, Quot.sound}`, zero `Classical.choice`, zero `mathlib`).

## 2. Architecture & Components

The implementation consists of four primary modules, a comprehensive test battery, and a constructive Lean 4 formal package:

### Python Modules
1. `runner.py`:
   - Fixed graph interpreter reading encoded instruction edges `(3 + k, (x, y))` via `lookup` without calling unencoded operation functions.
   - Refusal of ambiguous outgoing edges on an operation form.
   - Word machine interpreter (`step_word`, `run_word`, `eval_word`) relating stepwise execution to reference folds.
   - Parameterized deterministic runner (`step_det_of`, `run_det_of`, `iter_of`, `obs_of`, `next_of`).
   - Terminals kept apart: `HALT`, `EXHAUSTED`, `REFUSE`, `BRANCH`.

2. `control.py`:
   - Enablement encoded directly as graph data using reflexive self-instances `(3 + nops + k, (x, x))`.
   - Data-driven control execution maintaining `State(graph, nops, active, tape, clock, fuel)`.
   - Explicit refusal to select on non-deterministic forks: when two or more operations are enabled, the interpreter stops with `Terminal.BRANCH`.
   - Successor family enumeration (`successors`) exposing all candidate branches for relational analysis without arbitrary choice.
   - Monotonic resource accounting: clock ticks by +1 on each applied operation; fuel is spent monotonically by -1.

3. `branch.py`:
   - Control-Flow Graphs (CFG) and indirect jump tables represented directly as graph data.
   - Sequential steps: `(FORM_CFG_STEP, (pc, next_pc))`.
   - Conditional branches: `(FORM_CFG_BRANCH, (pc, cond_val, target_pc))`.
   - Jump tables: `(FORM_JUMP_TABLE, (table_id, index, target_pc))`.
   - Indirect jumps: `(FORM_CFG_INDIRECT, (pc, table_id))`.
   - Enforces branch non-selection: if multiple branch targets match the current data, `step_cfg` yields `Terminal.BRANCH`.

4. `memory.py`:
   - Retained internal records (Depth 1): enablement reads predecessor datum `p` and active datum `x` via instances `(3 + nops + k, (p, x))`.
   - Depth-2 ternary forms (Depth 2): enablement reads `before` datum `b`, predecessor `p`, and active `x` via ternary instances `(3 + nops + k, (b, p, x))`.
   - Memory ladder and functionality verification: evaluates whether contiguous windows satisfy prefix determinism across reading depths.

### Lean 4 Constructive Package (`lean/`)
- `lakefile.toml` & `lean-toolchain`: configured for `leanprover/lean4:v4.33.0`, consuming sealed `derivation` at `../../../lean4` read-only.
- `Execution.lean`: formal proofs of edge lookup (`lookup_mem`), word machine unit laws (`run_nil`), fold agreement (`run_evalWord`), and parameterized runner determinism (`stepDetOf_inr`, `stepDetOf_branch`).
- `Branch.lean`: formal proofs of CFG branch non-selection (`branch_non_selection`), deterministic jump table lookup (`jump_table_lookup`), and state step accounting (`stepCFG_clock`, `stepCFG_fuel`).
- `Memory.lean`: formal proofs of retained record stepping (`previous_fire_synced`), ladder monotonicity (`functional2_of_functional1`), and ceiling refutations (`twist_not_functional1`, `twist_functional2`, `twist2_not_functional2`).
- `Inventory.lean`: metaprogrammed environment census auditing all 58 compiled theorem declarations and verifying their reliance within `{propext, Quot.sound}`.

### Verification Harness (`verify.py`)
- Executes pytest test suite across `tests/`.
- Builds the Lean 4 package with `lake build`.
- Audits compiled theorem census and axiom dependence.
- Generates reproducible verification artifact `evidence/receipt.json`.

## 3. Claim Hygiene Summary

### 1. What it supports
- Supports that a finite setting encoded as graph instances can drive a stepwise execution process by reading stored carrier data directly without consulting external host function oracles.
- Supports that non-deterministic forks can be explicitly refused by returning a dedicated `branch` terminal rather than relying on an unrecorded scheduler or list-order choice.
- Supports that retained internal records `[p, x]` and depth-2 ternary forms `[b, p, x]` allow the process to distinguish routes sharing an active endpoint, breaking lower-depth functionality ceilings.

### 2. What it does not support
- Does not support Turing completeness or general unbounded recursion (all executions remain bounded by finite fuel).
- Does not support that the configuration container itself is an encoded regime (it is explicitly designated as `DECLARED_HOST_CONFIG`).
- Does not support continuous time or physical dynamics (clocks and steps measure discrete operation applications).

### 3. The narrowest defensible claim
For any finite carrier setting and well-formed enablement relation, the graph-reading interpreter computes the declared transitions within fuel bounds using only represented instances, and halts with `branch` whenever two or more operations are enabled.

### 4. The next test needed
Construction of an endogenous fuel replenishment mechanism and an encoded configuration regime within the object language.
