# Claims Ledger: G012 Bound-Uniform Typed Translation & General Signature Codec

This document formalizes the claims ledger for **G012 (Bound-Uniform Typed Translation & General Signature Codec)**, specifying the mathematical basis, formal Lean 4 theorems, Python verification mirrors, and epistemic boundaries.

Scope boundary: all codec and step-commutation theorems below concern this
tree's finite typed structures and its string-token relational carrier.
Shared field names do not give an isomorphism with the sealed `Regime`.
Its removal operations have no sealed admission counterpart. A native bridge
requires separate encode/decode and transition-commutation theorems.

AuthorityEffect: None.  
Terminal: `TYPED_TRANSLATION_CONSTRUCTIVE_BOUND_UNIFORM`.

---

## Claims Summary Table

| Claim ID | Scope | Lean 4 Theorems | Python Mirror | Axiom Reliance | Status |
|---|---|---|---|---|---|
| **CL-G012-01** | Signature & Structure Canonicality | `sortId_inj`, `relId_inj`, `constId_inj`, `funcId_inj`, `element_eq`, `typedStructure_eq` | `signature.py:TypedStructure.create`, `test_codec.py` | Strictly within `{"propext"}` | VERIFIED |
| **CL-G012-02** | Round-Trip Codec Invertibility | `decode_encode_inversion` | `codec.py:decode`, `test_codec.py:test_roundtrip_*` | Strictly within `{"propext"}` | VERIFIED |
| **CL-G012-03** | Structured Refusal Preservation | `refusal_preservation`, `refusal_preservation_forms` | `codec.py:decode`, `test_codec.py:test_refusal_*` | Strictly within `{"propext"}` | VERIFIED |
| **CL-G012-04** | Operational Transition Commutation | `step_commutation`, `step_commutation_addElement`, `step_commutation_addTuple`, `step_commutation_setConstant`, `step_commutation_setFunctionValue` | `codec.py:step_commutation_holds`, `test_commutation.py` | Strictly within `{"propext"}` | VERIFIED |
| **CL-G012-05** | Translation Functoriality & Naturality | `renaming_naturality`, `renaming_id_elements`, `renaming_id_constBindings`, `renaming_id_relTuples`, `renaming_id_funcEntries` | `naturality.py:Renaming`, `test_naturality.py` | Strictly within `{"propext"}` | VERIFIED |
| **CL-G012-06** | Exact Rational Distortion Vector | `distortion_depth_ratio`, `distortion_expansion_bound`, `distortion_mark_count_bound`, `distortion_invariance_length_*` | `naturality.py:compute_distortion`, `test_naturality.py` | Strictly within `{"propext", "Quot.sound"}` | VERIFIED |
| **CL-G012-07** | Bounded Specialization (1,459 Prefixes) | `historical_event_count`, `historical_prefix_census_count`, `memoryless_fixed_block_obstruction`, `symmetric_form_cost_obstruction`, `historical_admit_*_commutation`, `*_refusal` | `specialization.py:verify_specialization_recovery`, `test_specialization.py` | Strictly within `{"propext", "Quot.sound"}` | VERIFIED |
| **CL-G012-08** | Constructive Metatheoretic Boundary | Census in `lean/Inventory.lean` (317 declarations) | `verify.py` audit | Strictly within `{"propext", "Quot.sound"}` | VERIFIED |

---

## Detailed Claim Specifications

### CL-G012-01: Signature & Structure Canonicality
- **Statement:** Multi-sorted signatures and typed finite structures with carriers, constants, relations of arbitrary arity, and functions admit deterministic canonical representations and decidable structural equality.
- **Formal Theorems:**
  - `G012TypedTranslation.sortId_inj`
  - `G012TypedTranslation.constId_inj`
  - `G012TypedTranslation.relId_inj`
  - `G012TypedTranslation.funcId_inj`
  - `G012TypedTranslation.element_eq`
  - `G012TypedTranslation.constDecl_eq`
  - `G012TypedTranslation.relDecl_eq`
  - `G012TypedTranslation.funcDecl_eq`
  - `G012TypedTranslation.typedStructure_eq`
- **Claim Hygiene:**
  1. *Supports:* Canonical representation of multi-sorted first-order finite structures without host pointer equality.
  2. *Does not support:* Infinite relational signatures or uncountable carrier models.
  3. *Narrowest claim:* Equal signatures and component lists yield equal structure representations.
  4. *Next test:* Signatures parameterized over higher-order inductive sorts.

### CL-G012-02: Round-Trip Codec Invertibility
- **Statement:** Encoding a canonical typed structure into the five-part relational carrier $(\text{data}, \text{forms}, \text{insts}, \text{rules}, \text{reqs})$ is invertibly decodable: $\text{decode}(\text{encode}(S)) = \text{Ok}(S)$.
- **Formal Theorems:**
  - `G012TypedTranslation.decode_encode_inversion`
- **Claim Hygiene:**
  1. *Supports:* Exact information preservation across the relational boundary codec for all valid typed structures.
  2. *Does not support:* Parsing unconstrained informal strings outside the declared relational grammar.
  3. *Narrowest claim:* Any well-formed typed structure is mapped bijectively to its canonical relational state.
  4. *Next test:* Incremental streaming codec for large-scale relation tuples.

### CL-G012-03: Structured Refusal Preservation
- **Statement:** Malformed relational carriers or states violating signature consistency, carrier membership, sorting, or determinism decode strictly to structured `Refusal` descriptors, avoiding unhandled exceptions.
- **Formal Theorems:**
  - `G012TypedTranslation.refusal_preservation`
  - `G012TypedTranslation.refusal_preservation_forms`
- **Claim Hygiene:**
  1. *Supports:* Total error safety and structured classification of boundary errors.
  2. *Does not support:* Automatic error recovery or semantic guessing of corrupt tokens.
  3. *Narrowest claim:* Corrupted carrier states fail with defined refusal codes rather than unhandled faults.
  4. *Next test:* Automated fuzzing over corrupted relational state bitstrings.

### CL-G012-04: Operational Transition Commutation
- **Statement:** Operational transitions on typed structures commute with encoded transitions on the relational carrier: $\text{encode}(\text{step}(S, op)) = \text{step\_relational}(\text{encode}(S), \text{encode\_op}(op, S))$.
- **Formal Theorems:**
  - `G012TypedTranslation.step_commutation`
  - `G012TypedTranslation.step_commutation_addElement`
  - `G012TypedTranslation.step_commutation_setConstant`
  - `G012TypedTranslation.step_commutation_addTuple`
  - `G012TypedTranslation.step_commutation_setFunctionValue`
- **Claim Hygiene:**
  1. *Supports:* Dynamic operational fidelity: state evolution before and after encoding is isomorphic.
  2. *Does not support:* Concurrent non-deterministic race conditions without serialized operational sequencing.
  3. *Narrowest claim:* Single operational steps commute identically with encoded relational operations.
  4. *Next test:* Batched multi-operation atomic transactions.

### CL-G012-05: Translation Functoriality & Naturality
- **Statement:** Signature morphisms $\sigma: \Sigma_1 \to \Sigma_2$ act functorially on structures, preserving identity and composition, and form a commutative naturality square with relational encoding.
- **Formal Theorems:**
  - `G012TypedTranslation.renaming_naturality`
  - `G012TypedTranslation.renaming_id_elements`
  - `G012TypedTranslation.renaming_id_constBindings`
  - `G012TypedTranslation.renaming_id_relTuples`
  - `G012TypedTranslation.renaming_id_funcEntries`
- **Claim Hygiene:**
  1. *Supports:* Symbol renamings and signature morphisms translate consistently without altering semantic content.
  2. *Does not support:* Non-injective quotients that merge distinct carrier sorts without quotient equivalence relations.
  3. *Narrowest claim:* Sort and symbol renamings commute with encoding across all declared components.
  4. *Next test:* Contravariant reducts along signature inclusions.

### CL-G012-06: Exact Rational Distortion Vector
- **Statement:** Relational translation introduces bounded rational distortion measured by state expansion, mark count, and address depth ratios in $\mathbb{Q}^3$, invariant under signature isomorphisms.
- **Formal Theorems:**
  - `G012TypedTranslation.distortion_depth_ratio`
  - `G012TypedTranslation.distortion_mark_count_bound`
  - `G012TypedTranslation.distortion_expansion_bound`
  - `G012TypedTranslation.distortion_invariance_length_sorts`
  - `G012TypedTranslation.distortion_invariance_length_elements`
  - `G012TypedTranslation.distortion_invariance_length_constBindings`
  - `G012TypedTranslation.distortion_invariance_length_relTuples`
  - `G012TypedTranslation.distortion_invariance_length_funcEntries`
- **Claim Hygiene:**
  1. *Supports:* Exact rational bounds on translation overhead without asymptotic approximations.
  2. *Does not support:* Zero-overhead lossless compression.
  3. *Narrowest claim:* Distortion components are positive rational numbers invariant under signature renamings.
  4. *Next test:* Minimized variable-length prefix addressing.

### CL-G012-07: Bounded Specialization (1,459 Prefixes)
- **Statement:** The general typed translation framework strictly specializes to the historical binary carrier from `research/typed_translation/`, recovering all 1,459 valid history prefixes, verifying round-trip decode across all 22 reached unique structures, and confirming commutation on all 1,396 step extensions.
- **Formal Theorems:**
  - `G012TypedTranslation.historical_event_count`
  - `G012TypedTranslation.historical_prefix_census_count`
  - `G012TypedTranslation.historical_prefix_positive`
  - `G012TypedTranslation.memoryless_fixed_block_obstruction`
  - `G012TypedTranslation.symmetric_form_cost_obstruction`
  - `G012TypedTranslation.unsupplied_d0_refusal`
  - `G012TypedTranslation.unsupplied_d1_refusal`
  - `G012TypedTranslation.unformed_inst0_refusal`
  - `G012TypedTranslation.unformed_inst1_refusal`
  - `G012TypedTranslation.unformed_rule_refusal`
  - `G012TypedTranslation.duplicate_supply_d0_refusal`
  - `G012TypedTranslation.duplicate_supply_d1_refusal`
  - `G012TypedTranslation.historical_admit_d0_commutation`
  - `G012TypedTranslation.historical_admit_d1_commutation`
  - `G012TypedTranslation.historical_admit_form_commutation`
  - `G012TypedTranslation.historical_admit_inst0_commutation`
  - `G012TypedTranslation.historical_admit_inst1_commutation`
  - `G012TypedTranslation.historical_admit_rule_commutation`
- **Claim Hygiene:**
  1. *Supports:* Backward compatibility and formal subsumption of the historical 8-event bounded experiment.
  2. *Does not support:* Generalization of the 1,459 prefix count to larger universes without recalculation.
  3. *Narrowest claim:* Under the declared historical signature, the specialized replay machine recovers the exact 1,459 prefix census.
  4. *Next test:* Exploration of 3-datum ternary carrier prefix posets.

### CL-G012-08: Constructive Metatheoretic Axiom Boundary
- **Statement:** All 317 compiled declarations in the `G012TypedTranslation` Lean 4 package satisfy the strict constructive axiom boundary contained in `{'propext', 'Quot.sound'}`, with zero occurrences of `Classical.choice` and zero mathlib dependencies.
- **Formal Verification:**
  - Verified by `lean/Inventory.lean` census and audited by `verify.py`.
- **Claim Hygiene:**
  1. *Supports:* Constructive foundational purity for all formal claims.
  2. *Does not support:* Classical non-constructive principles or non-computable choice.
  3. *Narrowest claim:* Every compiled declaration is strictly constructive within Lean 4 core logic.
  4. *Next test:* Mechanized constructive extraction into verified executable code.
