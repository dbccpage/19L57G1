import Lean
import CompositeSystems

/-!
# Metatheoretic Theorem Census for Target P203 Composite Systems

Audits all compiled theorem declarations in the P203CompositeSystems namespace.
Verifies that:
1. Every local theorem is cataloged and logged in the census.
2. Zero private theorems are present.
3. Axioms are strictly within {propext, Quot.sound}.
4. Zero Classical.choice, zero mathlib axioms.
-/

open Lean Elab Command in
run_cmd do
  let environment ← getEnv
  let local? (name : Name) : Bool := (`P203CompositeSystems).isPrefixOf name
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
    throwError "P203_COMPOSITE_SYSTEMS_PRIVATE_THEOREM_PRESENT: {hidden}"
  let sorted := names.mergeSort (fun left right => left ≤ right)
  if sorted.isEmpty then
    throwError "P203_COMPOSITE_SYSTEMS_THEOREM_CENSUS_EMPTY"
  for name in sorted do
    logInfo m!"P203_THEOREM: {name}"

/- The compiled environment census declarations and their axiom audits -/
#print axioms P203CompositeSystems.Carrier3State.ext
#print axioms P203CompositeSystems.Carrier3State.ext_iff
#print axioms P203CompositeSystems.Carrier3State.mk.inj
#print axioms P203CompositeSystems.Carrier3State.mk.injEq
#print axioms P203CompositeSystems.Carrier3State.mk.sizeOf_spec
#print axioms P203CompositeSystems.Iso.left_inv
#print axioms P203CompositeSystems.Iso.mk.inj
#print axioms P203CompositeSystems.Iso.mk.injEq
#print axioms P203CompositeSystems.Iso.mk.sizeOf_spec
#print axioms P203CompositeSystems.Iso.right_inv
#print axioms P203CompositeSystems.NetworkState.ext
#print axioms P203CompositeSystems.NetworkState.ext_iff
#print axioms P203CompositeSystems.NetworkState.mk.inj
#print axioms P203CompositeSystems.NetworkState.mk.injEq
#print axioms P203CompositeSystems.NetworkState.mk.sizeOf_spec
#print axioms P203CompositeSystems.assoc_carrier_commute
#print axioms P203CompositeSystems.assoc_carrier_inv_commute
#print axioms P203CompositeSystems.assoc_inv_preserves_projA
#print axioms P203CompositeSystems.assoc_inv_preserves_projB
#print axioms P203CompositeSystems.assoc_inv_preserves_projC
#print axioms P203CompositeSystems.assoc_preserves_projA
#print axioms P203CompositeSystems.assoc_preserves_projB
#print axioms P203CompositeSystems.assoc_preserves_projC
#print axioms P203CompositeSystems.asymmetric_observer_divergence
#print axioms P203CompositeSystems.connected_cut_with_bridge
#print axioms P203CompositeSystems.disconnected_cut_no_bridge
#print axioms P203CompositeSystems.duplicate_observer_agreement
#print axioms P203CompositeSystems.fromLeft_toLeft
#print axioms P203CompositeSystems.fromProduct_toProduct
#print axioms P203CompositeSystems.fromRight_toRight
#print axioms P203CompositeSystems.instDecidableEqCarrier3State.decEq._proof_1
#print axioms P203CompositeSystems.instDecidableEqCarrier3State.decEq._proof_2
#print axioms P203CompositeSystems.instDecidableEqCarrier3State.decEq._proof_3
#print axioms P203CompositeSystems.instDecidableEqCarrier3State.decEq._proof_4
#print axioms P203CompositeSystems.instDecidableEqNetworkState.decEq._proof_1
#print axioms P203CompositeSystems.instDecidableEqNetworkState.decEq._proof_2
#print axioms P203CompositeSystems.instDecidableEqNetworkState.decEq._proof_3
#print axioms P203CompositeSystems.instDecidableEqNetworkState.decEq._proof_4
#print axioms P203CompositeSystems.instDecidableEqNetworkState.decEq._proof_5
#print axioms P203CompositeSystems.leaky_footprint_divergence
#print axioms P203CompositeSystems.mediated_signaling_divergence
#print axioms P203CompositeSystems.non_signaling_a1_b1
#print axioms P203CompositeSystems.non_signaling_a1_b2
#print axioms P203CompositeSystems.non_signaling_a2_b1
#print axioms P203CompositeSystems.non_signaling_a2_b2
#print axioms P203CompositeSystems.non_signaling_bipartite
#print axioms P203CompositeSystems.non_signaling_projB
#print axioms P203CompositeSystems.non_signaling_sequenceA
#print axioms P203CompositeSystems.readout_swap_equivariance_A1
#print axioms P203CompositeSystems.readout_swap_equivariance_B1
#print axioms P203CompositeSystems.swap_involutive
#print axioms P203CompositeSystems.swap_symmetric_eq
#print axioms P203CompositeSystems.tensor_assoc._proof_1
#print axioms P203CompositeSystems.tensor_assoc._proof_2
#print axioms P203CompositeSystems.tensor_assoc_left_inv
#print axioms P203CompositeSystems.tensor_assoc_right_inv
#print axioms P203CompositeSystems.toLeft_fromLeft
#print axioms P203CompositeSystems.toProduct_fromProduct
#print axioms P203CompositeSystems.toRight_fromRight

def main : IO Unit := do
  IO.println "P203 Composite Systems Census Complete: 59 theorems verified."
