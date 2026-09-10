# Claims Ledger — G001 TOE Target-Class Charter

## Summary Assessment

1. **What it supports**:
   - Supports independent pre-registration of 9 adequacy criteria and their 4-way foundational dimension partition (`Computational`, `Mathematical`, `Physical`, `Empirical`).
   - Supports freezing the criteria under `TOE_TARGET_CLASS_FROZEN` to prevent retrospective target shifting.
   - Supports automated refusal of circular candidate self-definitions and unencoded host oracles.
   - Supports constructive formalization in Lean 4 of `TargetSystem`, adequacy predicates, canonical positive and negative witnesses, and comparison morphisms satisfying category laws (`id_comp`, `comp_id`, `comp_assoc`) strictly within `{propext, Quot.sound}`.

2. **What it does not support**:
   - Does not establish that any current implementation is an empirically complete Theory of Everything.
   - Does not establish continuous background manifolds or infinite precision limits.
   - Does not claim that passing the 9 criteria establishes real-world physical validity without prospective empirical test.

3. **Narrowest defensible claim**:
   Pre-registering 9 independent adequacy criteria before candidate evaluation enables prospective evaluation of candidate target systems and categorical transfer of adequacy properties across comparison morphisms without retrospective criteria modification.

4. **Next test needed**:
   Apply the evaluation engine to candidate execution traces from Target A (`research/target_a_execution`) and Target B (`research/target_b_dynamics`), testing for adequacy preservation under morphism composition.

---

## Detailed Claims Inventory

| Claim ID | Formal / Empirical Object | Evidence Type | Status | Epistemic Scope |
|---|---|---|---|---|
| `CL-G001-01` | Pre-registered 9 independent criteria with hash freezing | Python `charter.py` + tests | VERIFIED | Freezes criteria before candidate evaluation; rejects retrospective mutations. |
| `CL-G001-02` | Refusal of circular self-definition & unencoded oracles | Python `adequacy.py` + tests | VERIFIED | Evaluator returns `Verdict.REFUSED` for self-referential or oracle-dependent systems. |
| `CL-G001-03` | Constructive `TargetSystem` and 4-way adequacy predicates | Lean 4 `Adequacy.lean` | PROVED | Formal definitions of computational, mathematical, physical, and empirical adequacy. |
| `CL-G001-04` | Non-vacuity: positive constructive witness `binaryToggleSystem` | Lean 4 `Adequacy.lean` | PROVED | Proved to satisfy all 4 adequacy predicates with zero axioms. |
| `CL-G001-05` | Selectivity: negative obstruction witness `trivialSystem` | Lean 4 `Adequacy.lean` | PROVED | Proved to fail computational, mathematical, and empirical adequacy with zero axioms. |
| `CL-G001-06` | Comparison morphism category with identity and associativity | Lean 4 `Morphism.lean` | PROVED | Category laws `id_comp`, `comp_id`, and `comp_assoc` proved constructively with zero axioms. |
| `CL-G001-07` | Adequacy preservation along faithful comparison morphisms | Lean 4 `Morphism.lean` | PROVED | Mathematical, empirical, and computational adequacy transfer along faithful/injective morphisms with zero axioms. |
| `CL-G001-08` | Metaprogrammed theorem census and strict axiom containment | Lean 4 `Inventory.lean` + `verify.py` | VERIFIED | All 73 declarations confirmed strictly within `{propext, Quot.sound}`; zero `Classical.choice`. |
