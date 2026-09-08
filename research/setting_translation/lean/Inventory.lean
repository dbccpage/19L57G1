import Lean
import Translation
import Chains
import Visible
import Transcription

/-!
Metatheoretic audit apparatus: enumerate the compiled theorem declarations
of the four local namespaces independently of source layout and of the
printed dependency reports.  AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool :=
    (`Translation).isPrefixOf name || (`Chains).isPrefixOf name ||
      (`Visible).isPrefixOf name || (`Transcription).isPrefixOf name
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
    throwError "TRANSLATION_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "TRANSLATION_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"TRANSLATION_THEOREM: {name}"


/- The compiler generates these additional theorem declarations (structure
projections and injectivity, size specifications, auxiliary proof terms).
Their reports are included beside the authored reports of the four modules,
and the combined population is compared with the independent environment
census. -/
#print axioms Chains.bounded_shorten._proof_1_3
#print axioms Chains.cut._proof_1_1
#print axioms Chains.cut._proof_1_2
#print axioms Chains.cut._proof_1_3
#print axioms Chains.liftOp._proof_1
#print axioms Transcription.d2Bare._proof_1
#print axioms Transcription.d2Merged._proof_1
#print axioms Transcription.tri._proof_1
#print axioms Transcription.unitBare._proof_1
#print axioms Translation.FiniteSetting.a_lt
#print axioms Translation.FiniteSetting.b_lt
#print axioms Translation.FiniteSetting.mk.inj
#print axioms Translation.FiniteSetting.mk.injEq
#print axioms Translation.FiniteSetting.mk.sizeOf_spec
#print axioms Translation.FiniteSetting.ops_closed
#print axioms Translation.derivable_op._proof_1_1
#print axioms Translation.derivable_op._proof_1_2
#print axioms Translation.derivable_store._proof_1_1
#print axioms Translation.derivable_store._proof_1_2
#print axioms Translation.encode_wf._proof_1_1
#print axioms Translation.encode_wf._proof_1_2
#print axioms Translation.mem_graphsFrom._proof_1_3
#print axioms Translation.mem_graphsFrom._proof_1_4
#print axioms Translation.mem_storesFrom._proof_1_3
#print axioms Translation.mem_storesFrom._proof_1_4
#print axioms Visible.encode_form0_lt._proof_1_1
#print axioms Visible.two._proof_1
#print axioms Visible.two._proof_2
#print axioms Visible.two._proof_3
