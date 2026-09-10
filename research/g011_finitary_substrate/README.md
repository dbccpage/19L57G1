# G011: Internal Finitary Substrate

## Overview

This research package implements and formalizes **G011 (Internal Finitary Substrate)** within the Genesis research program. The objective is to derive object-level identity, finite ordinals, hierarchical tree addresses, deterministic address freshness allocation, and fuel-bounded structural recursion internally, without reliance on host `Nat`, host memory addresses, or ambient host loop counters.

AuthorityEffect: None.  
Terminal Status: `FINITARY_SUBSTRATE_INTERNAL`.

---

## Package Architecture

### 1. Python Implementation & Test Suite
- `ordinals.py`: Pure inductive finite ordinals (`Zero`, `Succ`) with endogenous structural equality, trichotomy comparison, and arithmetic (`add`, `mul`, `sub`, `pred`).
- `address.py`: Inductive hierarchical tree addresses (`Root`, `Child`) with endogenous depth metrics, prefix relations, and sibling branch disjointness.
- `freshness.py`: Deterministic address allocator (`fresh_address`, `AddressRegistry`) generating fresh disjoint addresses strictly exceeding existing allocated indices without external oracles.
- `recursion.py`: Fuel-bounded instruction stepper (`step`) and structural recursion evaluator (`run_with_fuel`, `rec_fuel`) operating across finitary states (`pc`, `regs`, `mem`, `addrs`).
- `substrate.py`: Unified operational entrypoint and manifest for the finitary substrate.
- `tests/`: Comprehensive 30-test pytest suite covering ordinals, addressing, freshness, recursion, and integrated workflows.

### 2. Lean 4 Constructive Package
- `lean/lakefile.toml` & `lean/lean-toolchain`: Lean 4 package `g011_finitary_substrate` requiring `derivation` at toolchain `leanprover/lean4:v4.33.0`.
- `lean/Ordinal.lean`: Constructive definitions and proofs of ordinal injectivity, non-strict/strict ordering, trichotomy, and inductive arithmetic commutativity/associativity.
- `lean/Address.lean`: Constructive definitions and proofs of tree addressing, prefix ordering, depth monotonicity, and sibling branch disjointness.
- `lean/Freshness.lean`: Constructive definitions and proofs of deterministic address freshness, non-membership in allocated registries, and strict separation.
- `lean/Recursion.lean`: Constructive definitions and proofs of step determinism, fuel-bounded execution totality, and structural recursion schemes.
- `lean/Inventory.lean`: Metaprogrammed theorem census enumerating all 176 compiled declarations under `FinitarySubstrate`.

### 3. Verification & Governance
- `verify.py`: Master verification script running pytest, building the Lean package, querying theorem axioms, and producing `evidence/receipt.json`.
- `evidence/receipt.json`: Verification receipt recording test passes, 176 theorem audits, toolchain versions, and SHA256 file hashes.

---

## Epistemic Boundary & Claim Hygiene

Adhering strictly to the Claim Hygiene Rule:

1. **What it supports:**
   - Demonstrates that finite ordinals, arithmetic, tree addresses, disjoint address allocation, and fuel-bounded recursion can be derived and executed constructively without host integers or host pointers.
   - Shows in this formal setting that all 176 compiled Lean declarations depend strictly on permitted constructive axioms within `{"propext", "Quot.sound"}` with zero reliance on `Classical.choice` or `mathlib`.
   - Confirms that deterministic freshness allocation produces an address disjoint from all elements in any finite allocated registry.

2. **What it does not support:**
   - Does not demonstrate unbounded or non-terminating execution without fuel.
   - Does not establish an infinite continuum or real numbers.
   - Does not claim that host memory allocation or host Python runtime processes are physically eliminated at the machine hardware layer; rather, operational logic within the model is independent of host integer/pointer semantics.

3. **Narrowest Defensible Claim:**
   - Under the declared inductive definitions, `freshAddress(L)` produces an address structurally absent from `L`, and `runWithFuel(f, p, s)` terminates in finite steps for any finite ordinal fuel `f`.

4. **Next Test Needed:**
   - Integration with Target A (`research/target_a_execution`) to replace host configurations with endogenous finitary substrate configurations.

---

## Verification Commands

To verify the entire package locally:

```pwsh
# Run master verification
python verify.py

# Check existing receipt without mutation
python verify.py --check

# Run pytest directly
python -m pytest tests -v

# Build and check Lean 4 package directly
cd lean
lake build
lake env lean Inventory.lean
```
