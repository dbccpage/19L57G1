# M100–M103: Internal Syntax, Operational Logic & Connectives

## Overview

This research package implements and formalizes Requirement R3 (**M100–M103: Internal Syntax, Operational Logic, Resource Pricing & Universal Connectives**) within the Genesis research program. The package provides a fully constructive, self-contained development in Lean 4 (without `mathlib`, `#print axioms` strictly contained in `{"propext", "Quot.sound"}`) paired with executable Python mirrors and comprehensive test suites.

AuthorityEffect: None.  
Terminal Status: `INTERNAL_SYNTAX_LOGIC_SOUND`.

---

## Package Architecture

### 1. Python Implementation & Test Suite
- `syntax.py` (M100): De Bruijn terms (`Var`, `Lam`, `App`, `Const`), functorial renaming (`lift_renaming`, `rename`), capture-free parallel substitution (`lift_subst`, `subst`), single beta-substitution (`subst_single`), and size metrics.
- `logic.py` (M101): Resource formulas (`Atom`, `One`, `Tensor`, `Lolli`, `WithF`, `PlusF`, `Bang`, `Bot`), operational resource-space valuation semantics (`eval_formula`, `eval_context`), sequent derivation trees (`d_id`, `d_one_r`, `d_tensor_r`, `d_lolli_r`, `d_cut`), and principal cut reductions (`reduce_tensor_cut`, `reduce_lolli_cut`).
- `pricing.py` (M102): Hierarchical address provenance tracking (`RootAddress`, `ChildAddress`, `origin`, `depth`), tagged formulas, copy-safe bang duplication (`duplicate_bang`), and priced structural rules (`priced_exchange`, `priced_weakening`, `priced_contraction`) with cost models.
- `connectives.py` (M103): Categorical proof-term morphisms (`Mor`) with universal properties for products (&), coproducts (⊕), and internal homs (⊸); explicit ontological separation of operational refusal (`StepRefusal`, `RefusalReason`) from constructive linear negation (`neg(A) = Lolli(A, Bot())`), and state-preserving step execution (`step_with_state_preservation`).
- `tests/test_logic.py`: 20-test comprehensive pytest suite covering all four milestones.

### 2. Lean 4 Constructive Package
- `lean/lakefile.toml` & `lean/lean-toolchain`: Lean 4 package `internal_syntax_logic` pinned to `leanprover/lean4:v4.33.0`.
- `lean/Syntax.lean` (M100): De Bruijn capture-free substitution calculus, renaming functoriality (`rename_id`, `rename_comp`), substitution lemmas (`subst_var`, `rename_eq_subst`, `rename_subst`, `subst_rename`, `subst_comp`), and structural recursion metrics with zero external freshness oracles.
- `lean/Logic.lean` (M101): Substructural sequent calculus with linear contexts, cut-free fragment, explicit cut rules and principal cut reductions (`cut_reduce_tensor`, `cut_reduce_lolli`), operational resource-space valuation semantics, soundness theorem (`soundness`), and constructive proof of consistency / non-triviality (`not_derivable_bot`).
- `lean/Pricing.lean` (M102): Priced exchange, weakening, and contraction derivations, cost monotonicity bounds, and copy-safe bang modality with hierarchical address provenance and separation preservation (`separation_preservation`, `duplicateBang_provenance`).
- `lean/Connectives.lean` (M103): Categorical universal properties for products (`product_proj1`, `product_proj2`, `product_universal_unique`), coproducts (`coproduct_inj1`, `coproduct_inj2`, `coproduct_universal_unique`), internal homs (`hom_eval_curry`, `hom_universal_unique`), and explicit ontological non-conflation of refusal from logical falsity (`refusal_preserves_state`, `refusal_distinct_from_logical_falsity`).
- `lean/Inventory.lean`: Metaprogrammed census enumerating all 330 compiled declarations under `InternalSyntaxLogic`.

### 3. Verification & Governance
- `verify.py`: Master verification script executing pytest, building Lean 4, auditing all 330 declarations against allowed axioms `{"propext", "Quot.sound"}`, and generating `evidence/receipt.json`.
- `evidence/receipt.json`: Signed receipt recording 20 passed tests, 330 verified Lean theorems (269 entirely axiom-free, 61 depending only on `{propext, Quot.sound}`), zero disallowed axioms, and SHA256 source digests.

---

## Epistemic Boundary & Claim Hygiene

Following the Claim Hygiene Rule:

1. **What these artifacts support:**
   - Supports constructive capture-free substitution over internalized syntax without ambient host name supplies or external freshness oracles.
   - Supports cut reduction, operational soundness, and consistency ($\neg [] \vdash \bot$) in a substructural linear logic where resource contexts are explicitly accounted.
   - Supports tracking provenance addresses and cost bounds across structural exchange, weakening, and copy-safe contraction.
   - Supports categorical product, coproduct, and internal hom universal properties by unique morphism factoring.
   - Supports the operational separation where a refusal event preserves state without mutation and does not fabricate a proof of constructive absurdity.

2. **What these artifacts do not support:**
   - Does not support unpriced structural contraction or weakening on arbitrary linear formulas.
   - Does not support classical principles (excluded middle, double negation elimination, choice).
   - Does not claim that operational refusal is equivalent to constructive negation.

3. **Narrowest Defensible Claim:**
   - Under constructive core Lean 4 with axioms in `{"propext", "Quot.sound"}`, De Bruijn substitution satisfies functorial renaming and composition; linear derivations are sound with respect to resource-space valuations and consistent; and operational refusal preserves machine state without mutating configurations.

4. **Next Test Needed:**
   - Integrate with the number tower (`research/m105_number_tower/`) to evaluate internal terms computing over endogenous natural numbers.

---

## Verification Commands

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
