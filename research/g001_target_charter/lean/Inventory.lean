import Lean
import Charter
import Adequacy
import Morphism

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of the `Charter`, `Adequacy`, and `Morphism` namespaces independently of
source layout and of the printed dependency reports.

AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`Charter).isPrefixOf name || (`Adequacy).isPrefixOf name || (`Morphism).isPrefixOf name
  let names := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ => if local? name then name.toString :: found else found
      | _ => found
  let hidden := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if isPrivateName name && ((privateToUserName? name).any local?)
          then name.toString :: found else found
      | _ => found
  if !hidden.isEmpty then
    throwError "CHARTER_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "CHARTER_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"CHARTER_THEOREM: {name}"

/-!
The compiler generates these additional theorem declarations for structures,
inductive types, and proofs. Their axiom reports are checked here to match the
environment theorem census.
-/

#print axioms Adequacy.TargetSystem.mk.inj
#print axioms Adequacy.TargetSystem.mk.injEq
#print axioms Adequacy.TargetSystem.mk.sizeOf_spec
#print axioms Adequacy.TwoState.ofNat_ctorIdx
#print axioms Adequacy.TwoState.s0.sizeOf_spec
#print axioms Adequacy.TwoState.s1.sizeOf_spec
#print axioms Adequacy.instDecidableEqTwoState._proof_1
#print axioms Adequacy.instDecidableEqTwoState._proof_2

#print axioms Charter.CharterRecord.mk.inj
#print axioms Charter.CharterRecord.mk.injEq
#print axioms Charter.CharterRecord.mk.sizeOf_spec
#print axioms Charter.CriterionID.calculusUniqueness.sizeOf_spec
#print axioms Charter.CriterionID.comparisonMorphisms.sizeOf_spec
#print axioms Charter.CriterionID.computational.sizeOf_spec
#print axioms Charter.CriterionID.empirical.sizeOf_spec
#print axioms Charter.CriterionID.foundational.sizeOf_spec
#print axioms Charter.CriterionID.ofNat_ctorIdx
#print axioms Charter.CriterionID.physical.sizeOf_spec
#print axioms Charter.CriterionID.physicalModelUniqueness.sizeOf_spec
#print axioms Charter.CriterionID.reasoning.sizeOf_spec
#print axioms Charter.CriterionID.representational.sizeOf_spec
#print axioms Charter.Dimension.computational.sizeOf_spec
#print axioms Charter.Dimension.empirical.sizeOf_spec
#print axioms Charter.Dimension.mathematical.sizeOf_spec
#print axioms Charter.Dimension.ofNat_ctorIdx
#print axioms Charter.Dimension.physical.sizeOf_spec
#print axioms Charter.instDecidableEqCriterionID._proof_1
#print axioms Charter.instDecidableEqCriterionID._proof_2
#print axioms Charter.instDecidableEqDimension._proof_1
#print axioms Charter.instDecidableEqDimension._proof_2

#print axioms Morphism.ComparisonMorphism.comm_observe
#print axioms Morphism.ComparisonMorphism.comm_step
#print axioms Morphism.ComparisonMorphism.faithful_obs
#print axioms Morphism.ComparisonMorphism.mk.inj
#print axioms Morphism.ComparisonMorphism.mk.injEq
#print axioms Morphism.ComparisonMorphism.mk.sizeOf_spec
#print axioms Morphism.compMorphism._proof_1
#print axioms Morphism.compMorphism._proof_2
#print axioms Morphism.compMorphism._proof_3
#print axioms Morphism.idMorphism._proof_1
