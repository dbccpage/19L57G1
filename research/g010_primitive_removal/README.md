# G010: Semantic Primitive Removal

**Terminal Status**: `BOUNDARY_REMOVAL_SEMANTICALLY_EXECUTED`  
**AuthorityEffect**: None.

## Overview

The G010 module implements operational capability removal within the Genesis execution substrate. Rather than simulating primitive removal through post-hoc output filtering or synthetic classification tables, candidate computational primitives are physically absent from syntax constructors, interpreter dispatch routines, and state representations:

1. **Branching Removal (`Capability.BRANCHING`)**: The linear straight-line syntax and interpreter contain no conditional jump instructions or branch dispatch cases. State evolution strictly advances the program counter by one step for every non-halting transition.
2. **Memory Retention Removal (`Capability.MEMORY_RETENTION`)**: The memoryless machine state contains no persistent memory dictionary or auxiliary store attribute. The instruction set admits no store or load operations.
3. **Address Allocation Removal (`Capability.ADDRESS_ALLOCATION`)**: The static address machine possesses no dynamic address allocator or fresh-name generator. All operations are confined to a fixed finite set of static address slots.

Both unrestricted and restricted systems are evaluated across an identical, frozen public observation interface (`PublicView`), ensuring genuine semantic comparison.

---

## Module Architecture

```
research/g010_primitive_removal/
├── capability.py       # Formal definitions of capabilities, profiles, and PublicView
├── restriction.py      # Interpreters and ASTs with physical primitive absence
├── obstruction.py      # Constructive obstruction witnesses and non-recoverability
├── runner.py           # Comparative execution engine running systems side-by-side
├── verify.py           # Master verification harness producing evidence/receipt.json
├── README.md           # Package overview and usage
├── CLAIMS.md           # Scoped claims under the Claim Hygiene Rule
├── evidence/
│   └── receipt.json    # Machine verification receipt
├── tests/
│   ├── test_capability.py
│   ├── test_restriction.py
│   ├── test_obstruction.py
│   └── test_runner.py
└── lean/
    ├── lakefile.toml   # Lean 4 package manifest (depends on derivation)
    ├── lean-toolchain  # Lean 4.33.0
    ├── Capability.lean # Constructive definitions of capabilities and PublicObservation
    ├── Restriction.lean# Constructive ASTs, embeddings, and simulation theorems
    ├── Obstruction.lean# Constructive obstruction and non-recoverability theorems
    └── Inventory.lean  # Metaprogrammed theorem census
```

---

## 4-Part Summary (Claim Hygiene Discipline)

1. **What it supports**:
   - Demonstrates in this discrete model that removing branching, memory retention, or address allocation from abstract syntax and interpreter dispatch results in observable failure modes on tasks requiring those primitives across a shared public observation interface.
   - Demonstrates in this setup that capability-neutral linear tasks execute with identical public observations between unrestricted and restricted systems.
   - Establishes 145 constructive Lean 4 declarations strictly within `{propext, Quot.sound}` (113 axiom-free, zero `Classical.choice`, zero `mathlib`), formally confirming branching obstruction, memory erasure after clobber, finite static pigeonhole collision, and adapter non-recoverability.

2. **What it does not support**:
   - Does not claim general complexity-theoretic separations for arbitrary Turing-complete computational systems.
   - Does not claim that real-world hardware or external runtimes are free from underlying memory caches or physical branches.
   - Does not assert that every possible adapter architecture has been exhaustively analyzed beyond the declared length-preserving and capability-preserving classes.

3. **Narrowest defensible claim**:
   - For the declared discrete instruction sets and finite state representations, straight-line execution without branching maintains invariant output tape length across all inputs; register-clobbering in a state without auxiliary memory erases input distinctions; and static allocation of 3 entities into 2 slots induces a finite slot pigeonhole collision.

4. **Next test needed**:
   - Integration of G010 capability restriction signatures into the target charter comparison morphism category (`research/g001_target_charter/`).

---

## Verification

To run the full verification battery:

```pwsh
cd research/g010_primitive_removal
python verify.py --check
```
