import Lean
import EngineClass
import Restart
import Magnification

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of the three local namespaces independently of source layout and of the
printed dependency reports.  AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`EngineClass).isPrefixOf name || (`Restart).isPrefixOf name ||
      (`Magnification).isPrefixOf name
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
    throwError "MAGNIFICATION_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "MAGNIFICATION_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"MAGNIFICATION_THEOREM: {name}"

/- The compiler generates these additional theorem declarations (structure
and inductive specifications, equation lemmas, auxiliary proof terms).  Their
reports are included beside the authored reports of the three modules, and
the combined population is compared with the independent environment
census. -/
#print axioms EngineClass.Measure.mu1.sizeOf_spec
#print axioms EngineClass.Measure.mu2.sizeOf_spec
#print axioms EngineClass.Measure.ofNat_ctorIdx
#print axioms EngineClass.Path.brecOn
#print axioms EngineClass.Rooted.brecOn
#print axioms EngineClass.applyItem_wf._proof_1_1
#print axioms EngineClass.applyItem_wf._proof_1_2
#print axioms EngineClass.instDecidableEqMeasure._proof_1
#print axioms EngineClass.instDecidableEqMeasure._proof_2
#print axioms EngineClass.isMin_no_rule._proof_1_1
#print axioms Magnification.ctxRegime.eq_1
#print axioms Magnification.fresh_form_valid._proof_1_1
#print axioms Restart.idForms0._proof_1
#print axioms Restart.sw_bound._proof_1_3
