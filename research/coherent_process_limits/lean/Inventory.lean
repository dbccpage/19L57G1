import Lean
import Limits
import Observe

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of the `Limits` and `Observe` namespaces independently of source layout and
of the printed dependency reports.  AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`Limits).isPrefixOf name || (`Observe).isPrefixOf name
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
    throwError "LIMITS_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "LIMITS_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"LIMITS_THEOREM: {name}"


/- The compiler generates these additional theorem declarations (the proof
terms of bounds inside definitions and of case splits inside theorems).
Their reports are included beside the authored reports of `Limits.lean` and
`Observe.lean`, and the combined population is compared with the independent
environment census. -/
#print axioms Limits.bond._proof_1
#print axioms Limits.ebond._proof_1
#print axioms Limits.ebond._proof_2
#print axioms Limits.eofSeq._proof_1
#print axioms Limits.eofSeq_etoSeq._proof_1_1
#print axioms Limits.estable._proof_1_3
#print axioms Limits.estable._proof_1_4
#print axioms Limits.etoSeq._proof_1
#print axioms Limits.etoSeq._proof_2
#print axioms Limits.eventual._proof_1
#print axioms Limits.eventual._proof_2
#print axioms Limits.eventual_agrees._proof_1_1
#print axioms Limits.ofSeq._proof_1
#print axioms Limits.restrictEven._proof_1
#print axioms Limits.restrictEven._proof_2
#print axioms Observe.cyc_mod._proof_1_1
#print axioms Observe.cyc_mod._proof_1_2
#print axioms Observe.cyc_mod._proof_1_3
#print axioms Observe.cyc_mod._proof_1_4
#print axioms Observe.enabledAt_forever._proof_1_3
#print axioms Observe.forever_iter._proof_1_3
#print axioms Observe.forever_iter._proof_1_4
#print axioms Observe.forever_iter._proof_1_5
#print axioms Observe.forever_iter._proof_1_6
#print axioms Observe.lookup_forever._proof_1_3
#print axioms Observe.next_fire._proof_1_1
#print axioms Observe.next_fire._proof_1_6
#print axioms Observe.next_chain._proof_1_1
#print axioms Observe.next_fuel._proof_1_1
#print axioms Observe.obs_fuel_indep._proof_1_3
#print axioms Observe.obs_fuel_indep._proof_1_4
#print axioms Observe.obs_fuel_indep._proof_1_5
#print axioms Observe.obs_fuel_indep._proof_1_6
#print axioms Observe.base._proof_1
#print axioms Observe.base._proof_2
#print axioms Observe.base._proof_3
#print axioms Observe.cyc_lt._proof_1_3
#print axioms Observe.succ3_lt._proof_1_3
#print axioms Observe.zeros_eq._proof_1_3
#print axioms Observe.zeros_eq._proof_1_4
#print axioms Observe.zeros_bound._proof_1_1
#print axioms Observe.zeros_bound._proof_1_2
#print axioms Observe.nextOf_one_locus._proof_1_1
#print axioms Observe.nextOf_one_locus._proof_1_2
