# G012 Bound-Uniform Typed Translation & General Signature Codec

## 1. Architectural Overview

This research tree implements and formalizes the general multi-sorted relational signature translation framework, establishing a constructive boundary codec between multi-sorted structures and a five-partition relational carrier:

$$\text{Carrier} = (\text{data}, \text{forms}, \text{insts}, \text{rules}, \text{reqs})$$

These names resemble the sealed admission regime, but this codec's components
are string tokens for typed structures. Its operations can remove instances,
rules, and requirements, whereas sealed admission is monotone. The round-trip
and step-commutation results below are internal to this typed-structure codec;
they do not establish a native-regime isomorphism or a commuting square with
sealed admission events.

The module supplies:
- **`signature.py`**: Finite multi-sorted signatures supporting sorts, constants, relation symbols of arbitrary arities, and function symbols, paired with canonical `TypedStructure` carriers and operational transitions `step(S, op)`.
- **`codec.py`**: Constructive bidirectional encoder `encode` and decoder `decode` returning structured `Result[TypedStructure, Refusal]`.
- **`naturality.py`**: Signature morphisms $\sigma: \Sigma_1 \to \Sigma_2$, translation functoriality, naturality square commutation, and exact rational distortion vectors in $\mathbb{Q}^3$ (`fractions.Fraction`).
- **`specialization.py`**: Bounded specialization recovering the exact historical 1,459-history prefix census from `research/typed_translation/`.
- **`lean/`**: Constructive Lean 4 package compiling 317 declarations with strict axiom boundary contained within `{'propext', 'Quot.sound'}` (zero `Classical.choice`, zero mathlib).

## 2. Boundary Codec & Structured Refusals

### 2.1 Relational Grammar
The boundary carrier partitions information across five explicit categories:
1. `data`: Token representations of sort carrier elements (`elem:<sort>:<val>`).
2. `forms`: Schema declarations for sorts, constants, relations, and functions (`sort:<sort>`, `const:<c>:<sort>`, `rel:<r>:<arity>`, `func:<f>:<arity>-><tgt>`).
3. `insts`: Atomic instantiations for constant bindings and relation tuples (`bind:<c>:<val>`, `tup:<r>:(args)`).
4. `rules`: Structural integrity constraints, function mappings, and function determinism (`rule:det:<f>`, `rule:rel:<r>:(args)`, `rule:func:<f>:(args)-><val>`).
5. `reqs`: Explicit admissibility and support requirements ensuring every assertion rests on declared carrier elements and valid sort memberships.

### 2.2 Invertibility and Refusal Preservation
- **Invertibility**: For all canonically formed `TypedStructure` instances $S$, round-trip inversion holds:
  $$\text{decode}(\text{encode}(S)) = \text{Ok}(S)$$
- **Structured Refusals**: Malformed or unparseable inputs produce structured `Err(Refusal(...))` instances rather than unhandled exceptions. Refusal codes include `MALFORMED_ENCODING`, `INVALID_SIGNATURE`, `UNSORTED_OR_DUPLICATE`, `CARRIER_MISMATCH`, `FUNCTION_NON_FUNCTIONAL`, `MISSING_REQUIREMENT`, and `UNKNOWN_SYMBOL`.
- **Operational Commutation**: For any valid operation $op$ on $S$:
  $$\text{encode}(\text{step}(S, op)) = \text{step\_relational}(\text{encode}(S), \text{encode\_op}(op, S))$$

## 3. Signature Morphisms and Naturality

A signature renaming $\sigma: \Sigma_1 \to \Sigma_2$ maps sorts, constants, relations, and functions while preserving declared arities and sort targets.
- **Functoriality**: Push-forward actions satisfy:
  $$\text{id}_*(S) = S, \quad (\tau \circ \sigma)_*(S) = \tau_*(\sigma_*(S))$$
- **Naturality Commutation**: The encoding commutes with signature push-forward:
  $$\text{encode}(\sigma_*(S)) = \hat{\sigma}(\text{encode}(S))$$
  where $\hat{\sigma}$ acts on relational carrier tokens.

## 4. Exact Rational Distortion Vector

The boundary translation cost is characterized by an exact rational distortion vector $\mathbf{d}(S) \in \mathbb{Q}^3$:
1. **State Expansion Ratio**:
   $$\text{expansion} = \frac{\#(\text{relational tokens})}{\#(\text{source atoms})} \in \mathbb{Q}$$
2. **Mark Count Ratio**:
   $$\text{mark\_ratio} = \frac{\#(\text{insts}) + \#(\text{rules})}{\max(1, \#(\text{tuples}) + \#(\text{constants}) + \#(\text{functions}))} \in \mathbb{Q}$$
3. **Address Depth Ratio**:
   $$\text{depth\_ratio} = \frac{\text{depth}(\text{relational})}{\text{depth}(\text{signature})} = \frac{3}{\text{max\_arity} + 1} \in \mathbb{Q}$$

Under any signature renaming isomorphism $\sigma$, the distortion vector is strictly preserved:
$$\mathbf{d}(\sigma_*(S)) = \mathbf{d}(S)$$

## 5. Bounded Specialization (Historical 1,459 Prefixes)

The module `specialization.py` and Lean library `Specialization.lean` construct an explicit specialization to the historical binary carrier:
- Sort: `datum` with carrier elements $\{0, 1\}$.
- Relations: nullary `Form`, unary `Instance(datum)`, nullary `Rule`.
- Events: 8 frozen source events (`supply_d0`, `admit_d0`, `supply_d1`, `admit_d1`, `admit_form`, `admit_inst0`, `admit_inst1`, `admit_rule`).
- Census Recovery: Depth-first prefix enumeration strictly recovers all 1,459 valid history prefixes, matching the historical census from `research/typed_translation/` event-for-event.
- Verification: All 22 reached unique structures round-trip decode, and all 1,396 admissible transition steps commute with the relational carrier.

## 6. Claim Hygiene Summary

1. **What it supports**:
   - Constructive round-trip invertibility for multi-sorted finite structures encoded into a five-partition relational carrier.
   - Structured refusal preservation on corrupted relational states without unhandled exceptions.
   - Exact operational transition commutation between structure updates and relational updates.
   - Preservation of exact rational distortion vectors in $\mathbb{Q}^3$ under signature morphisms.
   - Constructive Lean 4 formalization containing 317 declarations strictly bounded by `{'propext', 'Quot.sound'}` with zero `Classical.choice` and zero mathlib dependencies.
   - Exact recovery of the historical 1,459 valid history prefixes as a specialized instance of the general signature framework.
2. **What it does not support**:
   - Infinite structures or signatures with infinite carrier sets.
   - Continuous or non-finitary carrier semantics.
   - Claims of universal translation efficiency beyond the explicit rational distortion bounds calculated.
   - An encode/decode equivalence or transition-commutation theorem with the sealed admission regime. Removal operations in this carrier have no sealed admission counterpart.
3. **The narrowest defensible claim**:
   - Within finite multi-sorted signatures and the declared five-category relational carrier, the constructive codec achieves exact round-trip inversion, transition commutation, refusal safety, and recovers the historical 1,459-prefix census as a bounded specialization.
4. **The next test needed**:
   - Property-based fuzz testing of deep multi-sorted structures with large arities ($\ge 5$) and complex mutual recursion graphs.
