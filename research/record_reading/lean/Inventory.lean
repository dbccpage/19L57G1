import Lean
import Record
import Select

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of the `Record` and `Select` namespaces independently of source layout and
of the printed dependency reports.  AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`Record).isPrefixOf name || (`Select).isPrefixOf name
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
    throwError "RECORD_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "RECORD_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"RECORD_THEOREM: {name}"


/- The compiler generates these additional theorem declarations (the
structure's injectivity and size lemmas, and the proof terms of case splits
inside theorems).  Their reports are included beside the authored reports of
`Record.lean` and `Select.lean`, and the combined population is compared
with the independent environment census. -/
#print axioms Record.Recorded.mk.inj
#print axioms Record.Recorded.mk.injEq
#print axioms Record.Recorded.mk.sizeOf_spec
#print axioms Record.encodeR_wf._proof_1_1
#print axioms Record.encodeR_wf._proof_1_2
#print axioms Record.encodeR_wf._proof_1_3
#print axioms Record.lookup_rprogram_op._proof_1_1
#print axioms Record.lookup_rprogram_op._proof_1_2
#print axioms Record.renabled_rprogram._proof_1_1
#print axioms Record.renabled_rprogram._proof_1_2
#print axioms Record.rsuccessors_complete._proof_1_1
#print axioms Select.enabledAt_ge._proof_1_1
#print axioms Select.enabledAt_ge._proof_1_2
#print axioms Select.rel_next._proof_1_1
#print axioms Select.rel_next._proof_1_2
#print axioms Select.rel_next._proof_1_3
