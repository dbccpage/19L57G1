# Claims Ledger: G010 Semantic Primitive Removal

This document formalizes the claims ledger for **G010 (Semantic Primitive Removal)**, specifying the mathematical basis, formal Lean 4 theorems, Python verification mirrors, and epistemic boundaries under the Claim Hygiene Rule.

AuthorityEffect: None.  
Terminal Status: `BOUNDARY_REMOVAL_SEMANTICALLY_EXECUTED`.

---

## Claims Summary Table

| Claim ID | Scope | Lean 4 Theorems | Python Mirror | Axiom Reliance | Status |
|---|---|---|---|---|---|
| **CL-G010-01** | Capability Definition & Profile Hierarchy | `removeCap_self`, `removeCap_other` | `test_capability_enumeration`, `test_capability_profiles`, `test_profile_subsets` | None (0 axioms) | VERIFIED |
| **CL-G010-02** | Operational Linear Execution Embedding | `linear_step_embed`, `linear_embed_step_observe`, `project_embedLinearState` | `test_base_instructions_admitted_in_all_interpreters`, `test_comparative_runner_standard_battery` | None (0 axioms) | VERIFIED |
| **CL-G010-03** | Physical Capability Refusal | Abstract syntax type exclusion | `test_linear_interpreter_refuses_branching_instructions`, `test_memoryless_interpreter_refuses_memory_instructions`, `test_static_address_interpreter_refuses_alloc_instructions` | N/A (Python / AST) | VERIFIED |
| **CL-G010-04** | Constructive Branching Obstruction | `linear_step_control`, `linear_run_control`, `linear_inputs_tape_len_eq`, `branching_obstruction` | `test_branching_obstruction_length_invariance`, `test_comparative_runner_standard_battery` | None (0 axioms) | VERIFIED |
| **CL-G010-05** | Constructive Memory Obstruction | `clobber_eq`, `memoryless_clobber_erasure`, `memory_retention_obstruction` | `test_memory_obstruction_state_collapse`, `test_comparative_runner_standard_battery` | None (0 axioms) | VERIFIED |
| **CL-G010-06** | Constructive Allocation Obstruction | `fin2_eq`, `static_pigeonhole_collision` | `test_allocation_obstruction_pigeonhole`, `test_comparative_runner_standard_battery` | None (0 axioms) | VERIFIED |
| **CL-G010-07** | Adapter Non-Recoverability | `adapter_cannot_bypass_branching` | `test_linear_adapter_cannot_bypass_branching_task` | None (0 axioms) | VERIFIED |
| **CL-G010-08** | Constructive Axiom Census | Census in `lean/Inventory.lean` (145 declarations) | `verify.py` audit | Strictly within `{"propext", "Quot.sound"}` | VERIFIED |

---

## Detailed Claim Specifications

### CL-G010-01: Capability Definition & Profile Hierarchy
- **Statement:** Computational primitives form decidable capability identifiers whose profiles support constructive complementation (`removeCap`) and subset inclusion.
- **Formal Theorems:**
  - `G010.removeCap_self`
  - `G010.removeCap_other`
- **Claim Hygiene:**
  1. *Supports:* Decidable capability tracking across restricted profiles without non-constructive sets.
  2. *Does not support:* Infinite or continuous capability spaces.
  3. *Narrowest claim:* Constructive set complementation operates correctly on finite capability profiles.
  4. *Next test:* Capability composition functors.

### CL-G010-02: Operational Linear Execution Embedding
- **Statement:** Straight-line linear execution embeds faithfully into unrestricted full execution, yielding identical public observations.
- **Formal Theorems:**
  - `G010.linear_step_embed`
  - `G010.linear_embed_step_observe`
  - `G010.project_embedLinearState`
- **Claim Hygiene:**
  1. *Supports:* Semantic preservation of common instructions between restricted and unrestricted models.
  2. *Does not support:* Equivalence for programs that invoke non-linear primitives.
  3. *Narrowest claim:* On straight-line operations, restricted linear execution agrees with the full model under observation projection.
  4. *Next test:* Bisimulation between linear and full runners under step-indexed bisimilarity.

### CL-G010-03: Physical Capability Refusal
- **Statement:** Programs containing instructions of physically removed primitives are refused by restricted interpreters at validation/load time rather than evaluated and masked post-hoc.
- **Test Evidence:**
  - `tests/test_restriction.py::test_linear_interpreter_refuses_branching_instructions`
  - `tests/test_restriction.py::test_memoryless_interpreter_refuses_memory_instructions`
  - `tests/test_restriction.py::test_static_address_interpreter_refuses_alloc_instructions`
- **Claim Hygiene:**
  1. *Supports:* Genuine structural absence in syntax dispatch.
  2. *Does not support:* Hardware-level hardware fault interception.
  3. *Narrowest claim:* The AST validator and interpreter dispatch reject foreign primitive instructions prior to state modification.
  4. *Next test:* Dependent type-level AST construction where invalid instructions cannot be typed.

### CL-G010-04: Constructive Branching Obstruction
- **Statement:** In the absence of branching capability, execution path control is invariant under register inputs, forcing output tape length to remain constant across all inputs; consequently, conditional routing tasks requiring differing output lengths cannot be solved.
- **Formal Theorems:**
  - `G010.linear_step_control`
  - `G010.linear_run_control`
  - `G010.linear_inputs_tape_len_eq`
  - `G010.branching_obstruction`
- **Claim Hygiene:**
  1. *Supports:* Constructive obstruction proof of conditional length branching in straight-line programs with zero axioms.
  2. *Does not support:* Complex semantic branching where tape length is identical but contents vary through arithmetic tricks.
  3. *Narrowest claim:* Straight-line programs emit an invariant number of outputs independent of input register data.
  4. *Next test:* Arithmetic output content obstruction under bounded algebraic rings.

### CL-G010-05: Constructive Memory Obstruction
- **Statement:** In the absence of auxiliary memory retention, a state whose registers are overwritten by intermediate computations suffers complete state collapse, erasing input distinction and preventing retrieval of prior data.
- **Formal Theorems:**
  - `G010.clobber_eq`
  - `G010.memoryless_clobber_erasure`
  - `G010.memory_retention_obstruction`
- **Claim Hygiene:**
  1. *Supports:* Constructive obstruction proof showing that erasing register state destroys distinction in the absence of external memory.
  2. *Does not support:* Space-complexity lower bounds for general Turing machines.
  3. *Narrowest claim:* Zeroing registers in a memoryless state maps distinct initial values to identical states.
  4. *Next test:* Retention obstruction over partially clobbered register subsets.

### CL-G010-06: Constructive Allocation Obstruction
- **Statement:** By finite slot collision, allocating 3 entities into 2 static slots forces at least one duplicate, demonstrating that dynamic allocation cannot be simulated by a smaller static slot pool.
- **Formal Theorems:**
  - `G010.fin2_eq`
  - `G010.static_pigeonhole_collision`
- **Claim Hygiene:**
  1. *Supports:* Constructive proof that no injection exists from `Fin 3` to `Fin 2` with 0 axioms.
  2. *Does not support:* Arbitrary infinite cardinal separations.
  3. *Narrowest claim:* Any map from 3 elements to 2 elements has non-trivial collision.
  4. *Next test:* Generalized constructive pigeonhole principle for `Fin (n + 1) → Fin n`.

### CL-G010-07: Adapter Non-Recoverability
- **Statement:** A length-preserving observation adapter cannot recover branching capability from an obstructed linear system.
- **Formal Theorems:**
  - `G010.adapter_cannot_bypass_branching`
- **Claim Hygiene:**
  1. *Supports:* Formal proof that length-preserving observation adapters preserve the branching obstruction.
  2. *Does not support:* Arbitrary stateful or branching adapters (which themselves embed the missing primitive).
  3. *Narrowest claim:* Composition of a straight-line system with a length-preserving post-processor retains invariant output length.
  4. *Next test:* Characterization of the minimal capability required for an adapter to recover branching.

### CL-G010-08: Constructive Axiom Census
- **Statement:** All 145 compiled declarations under `G010` rely strictly on axioms within `{"propext", "Quot.sound"}` with zero `Classical.choice` and zero `mathlib`.
- **Evidence:** Verified by `lean/Inventory.lean` and `verify.py`.
- **Claim Hygiene:**
  1. *Supports:* Complete constructive compliance of the formal proof suite.
  2. *Does not support:* Metatheoretic consistency of Lean 4 itself.
  3. *Narrowest claim:* Every compiled lemma in the G010 package is audited by Lean's environment with zero non-constructive axioms.
  4. *Next test:* Lake dependency tree integrity audit across the full repository.
