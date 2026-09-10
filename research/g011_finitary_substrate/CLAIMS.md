# Claims Ledger: G011 Internal Finitary Substrate

This document formalizes the claims ledger for **G011 (Internal Finitary Substrate)**, specifying the mathematical basis, formal Lean 4 theorems, Python verification mirrors, and epistemic boundaries.

AuthorityEffect: None.  
Terminal: `FINITARY_SUBSTRATE_INTERNAL`.

---

## Claims Summary Table

| Claim ID | Scope | Lean 4 Theorems | Python Mirror | Axiom Reliance | Status |
|---|---|---|---|---|---|
| **CL-G011-01** | Ordinal Identity & Ordering | `succ_inj`, `zero_ne_succ`, `le_refl`, `le_trans`, `le_antisymm`, `lt_irrefl` | `test_ordinal_identity_and_equality`, `test_ordinal_order_relations` | None (0 axioms) | VERIFIED |
| **CL-G011-02** | Inductive Arithmetic & Trichotomy | `add_assoc`, `add_comm`, `mul_assoc`, `mul_comm`, `sub_add_cancel`, `trichotomy` | `test_ordinal_addition`, `test_ordinal_multiplication`, `test_ordinal_algebraic_laws_matrix` | None (0 axioms) | VERIFIED |
| **CL-G011-03** | Tree Addressing & Prefix Relations | `depth_root`, `depth_child`, `isPrefix_refl`, `isPrefix_root`, `isPrefix_depth` | `test_address_construction_and_identity`, `test_address_prefix_relations` | None (0 axioms) | VERIFIED |
| **CL-G011-04** | Sibling Branch Disjointness | `disjoint_siblings`, `disjoint_symm`, `disjoint_irrefl` | `test_address_disjointness`, `test_deep_address_hierarchy` | None (0 axioms) | VERIFIED |
| **CL-G011-05** | Deterministic Address Freshness | `maxBranchIndex_ge`, `freshIndex_gt`, `freshAddress_ne`, `freshAddress_not_mem` | `test_fresh_address_collision_freedom`, `test_address_registry_allocation_sequence` | None (0 axioms) | VERIFIED |
| **CL-G011-06** | Instruction Step Determinism | `step_deterministic`, `step_halted` | `test_stepper_basic_instructions`, `test_stepper_memory_allocation_and_access` | None (0 axioms) | VERIFIED |
| **CL-G011-07** | Fuel-Bounded Recursion Totality | `runWithFuel_totality`, `runWithFuel_deterministic`, `recFuel_succ` | `test_stepper_branching_and_loop`, `test_fuel_monotonicity`, `test_structural_recursion_scheme` | None (0 axioms) | VERIFIED |
| **CL-G011-08** | Constructive Metatheoretic Boundary | Census in `lean/Inventory.lean` | `verify.py` audit | Strictly within `{"propext", "Quot.sound"}` | VERIFIED |

---

## Detailed Claim Specifications

### CL-G011-01: Endogenous Ordinal Identity & Ordering
- **Statement:** The finitary ordinals formed by `zero` and `succ` satisfy strict injectivity, non-identity between zero and successor, and form a decidable total preorder whose strict relation is irreflexive and transitive.
- **Formal Theorems:**
  - `FinitarySubstrate.Ordinal.succ_inj`
  - `FinitarySubstrate.Ordinal.zero_ne_succ`
  - `FinitarySubstrate.Ordinal.le_refl`
  - `FinitarySubstrate.Ordinal.le_trans`
  - `FinitarySubstrate.Ordinal.le_antisymm`
  - `FinitarySubstrate.Ordinal.lt_irrefl`
  - `FinitarySubstrate.Ordinal.lt_trans`
- **Claim Hygiene:**
  1. *Supports:* Inductive finite ordinal comparison without consulting host integer primitives.
  2. *Does not support:* Transfinite ordinals or uncountable cardinality.
  3. *Narrowest claim:* Decidable comparison over finite inductive constructors is well-behaved.
  4. *Next test:* Extension to finite product ordinal vectors.

### CL-G011-02: Inductive Arithmetic & Decidable Trichotomy
- **Statement:** Endogenous addition and multiplication are commutative, associative, and distributive; truncated subtraction cancels addition; comparison satisfies decidable trichotomy.
- **Formal Theorems:**
  - `FinitarySubstrate.Ordinal.add_comm`
  - `FinitarySubstrate.Ordinal.add_assoc`
  - `FinitarySubstrate.Ordinal.mul_comm`
  - `FinitarySubstrate.Ordinal.mul_assoc`
  - `FinitarySubstrate.Ordinal.sub_add_cancel`
  - `FinitarySubstrate.Ordinal.trichotomy`
- **Claim Hygiene:**
  1. *Supports:* Constructive derivation of Peano arithmetic operations in Lean 4 with 0 axioms.
  2. *Does not support:* Negative integers, rational quotients, or real analysis.
  3. *Narrowest claim:* Inductive arithmetic over `Ordinal` satisfies semiring identities.
  4. *Next test:* Endogenous division with remainder.

### CL-G011-03: Tree Addressing & Prefix Relations
- **Statement:** Hierarchical tree addresses formed by `root` and `child` evaluate depth monotonically under prefix inclusion.
- **Formal Theorems:**
  - `FinitarySubstrate.Address.depth_root`
  - `FinitarySubstrate.Address.depth_child`
  - `FinitarySubstrate.Address.isPrefix_refl`
  - `FinitarySubstrate.Address.isPrefix_root`
  - `FinitarySubstrate.Address.isPrefix_depth`
- **Claim Hygiene:**
  1. *Supports:* Endogenous naming and hierarchical addressing without host pointers or memory locations.
  2. *Does not support:* Cyclic or graph-structured address spaces without explicit pointer quotients.
  3. *Narrowest claim:* Prefix inclusion implies non-strict depth inequality.
  4. *Next test:* Tree address concatenation and relative path navigation.

### CL-G011-04: Sibling Branch Disjointness
- **Statement:** Any two child addresses branching from the same parent with distinct branch ordinals are mutually disjoint.
- **Formal Theorems:**
  - `FinitarySubstrate.Address.not_isPrefix_child_parent`
  - `FinitarySubstrate.Address.disjoint_siblings`
  - `FinitarySubstrate.Address.disjoint_symm`
- **Claim Hygiene:**
  1. *Supports:* Structural separation between parallel execution branches.
  2. *Does not support:* Topological compactness or metric completeness.
  3. *Narrowest claim:* Sibling tree addresses have empty path overlap beyond their common ancestor.
  4. *Next test:* Disjointness propagation to arbitrary descendant subtrees.

### CL-G011-05: Deterministic Address Freshness
- **Statement:** `freshAddress(L)` evaluates purely from the admitted allocated list and produces an address that is not an element of `L`.
- **Formal Theorems:**
  - `FinitarySubstrate.Freshness.maxBranchIndex_ge`
  - `FinitarySubstrate.Freshness.freshIndex_gt`
  - `FinitarySubstrate.Freshness.freshAddress_ne`
  - `FinitarySubstrate.Freshness.freshAddress_not_mem`
  - `FinitarySubstrate.Freshness.allocate_fresh`
- **Claim Hygiene:**
  1. *Supports:* Deterministic fresh address generation without randomness or external UUID oracles.
  2. *Does not support:* Infinite concurrent allocation without synchronizing the registry.
  3. *Narrowest claim:* For any finite list `L` of addresses, `freshAddress(L) ∉ L`.
  4. *Next test:* Multi-locus parallel freshness allocators.

### CL-G011-06: Instruction Step Determinism
- **Statement:** The single-step transition function `step` is deterministic and respects halted terminal states.
- **Formal Theorems:**
  - `FinitarySubstrate.Recursion.step_halted`
  - `FinitarySubstrate.Recursion.step_deterministic`
- **Claim Hygiene:**
  1. *Supports:* Deterministic execution of endogenous instructions without hidden scheduling.
  2. *Does not support:* Non-deterministic concurrency or external interrupts.
  3. *Narrowest claim:* State equality is preserved under stepping.
  4. *Next test:* Step relation over non-deterministic fork programs.

### CL-G011-07: Fuel-Bounded Recursion Totality
- **Statement:** For any finite ordinal fuel amount, program, and initial state, `runWithFuel` terminates in either a halted state or fuel exhaustion.
- **Formal Theorems:**
  - `FinitarySubstrate.Recursion.runWithFuel_zero`
  - `FinitarySubstrate.Recursion.runWithFuel_halted`
  - `FinitarySubstrate.Recursion.runWithFuel_deterministic`
  - `FinitarySubstrate.Recursion.runWithFuel_totality`
- **Claim Hygiene:**
  1. *Supports:* Constructive totality of execution bounded by endogenous fuel ordinals.
  2. *Does not support:* General halting problem decidability for unbounded loops.
  3. *Narrowest claim:* Evaluation terminates in finite steps indexed by the fuel ordinal.
  4. *Next test:* Monadic composition of fuel-bounded runs.

### CL-G011-08: Constructive Metatheoretic Boundary
- **Statement:** All 176 compiled declarations under `FinitarySubstrate` in the Lean 4 environment depend strictly on permitted axioms within `{"propext", "Quot.sound"}` with 0 axioms used in core proofs and zero reliance on `Classical.choice` or `mathlib`.
- **Formal Evidence:**
  - `lean/Inventory.lean`
  - `evidence/receipt.json`
- **Claim Hygiene:**
  1. *Supports:* Strict adherence to the Genesis constructive core standard.
  2. *Does not support:* Equivalence with classical set theory (ZFC).
  3. *Narrowest claim:* No non-constructive axioms are invoked by the compiled package.
  4. *Next test:* Automated CI gating of future modifications.
