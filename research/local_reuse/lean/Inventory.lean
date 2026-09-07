import Lean
import LocalReuse

/-!
Metatheoretic audit apparatus. Enumerate compiled theorem declarations
independently of source layout and printed dependency reports.
AuthorityEffect: None.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let names := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if (`LocalReuse).isPrefixOf name then name.toString :: found else found
      | _ => found
  -- A private theorem is registered as `_private.<module>.<n>.LocalReuse.<name>`,
  -- which carries no `LocalReuse` prefix, so it would appear in neither this
  -- census nor the required report population and would need no `#print axioms`
  -- line to keep the two sets equal. Rather than spell mangled names, the
  -- packet declares it has none and refuses one that appears.
  let hidden := environment.constants.fold (init := ([] : List String))
    fun found name declaration =>
      match declaration with
      | .thmInfo _ =>
          if isPrivateName name && ((privateToUserName? name).any (`LocalReuse).isPrefixOf)
          then name.toString :: found else found
      | _ => found
  if !hidden.isEmpty then
    throwError "LOCAL_REUSE_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "LOCAL_REUSE_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"LOCAL_REUSE_THEOREM: {name}"

/- The compiler generates these additional theorem declarations. Include
their reports alongside the authored reports in LocalReuse.lean, then
compare that combined population to the independent environment census. -/
#print axioms LocalReuse.ContextPath.brecOn
#print axioms LocalReuse.ResponsePath.brecOn
#print axioms LocalReuse.difference_can_have_no_response_step._proof_1_1
#print axioms LocalReuse.difference_can_have_no_response_step._proof_1_2
#print axioms LocalReuse.markedLeft.eq_1
#print axioms LocalReuse.markedRight.eq_1
#print axioms LocalReuse.no_seven_closed_rounds_on_two_data._proof_1_1
#print axioms LocalReuse.padF_absorb._proof_1_1
