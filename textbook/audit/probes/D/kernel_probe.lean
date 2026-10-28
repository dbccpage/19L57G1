import Derivation.ContactKernel
open DiffInterface ContactKernel
#check @kernel_not_bs
#check @kernel_zero_not_trans
#check @kernel_not_observer
#check @kernel_no_terminal_collector
#check @PrimitiveCats.d2_initial
#print PrimitiveCats.Initial
#print PrimitiveCats.Hom
#print PrimitiveCats.d2Obj
#check @PrimitiveContact.NativeKernel
#check @kernel_licenses_entry
#check @kernel_two_point_presentation
-- universe check: WitnessedDiff is fixed at Type (universe 0)
#check @WitnessedDiff
-- the kernel_not_bs witness is literally the ofSetting of the D2 setting? compare shapes
example : (kernelApart boolKernel false true) := by decide
-- the "kernel" of kernel_not_bs: its induced apartness is D2, i.e. ¬¬D2 - check equivalence by decide
example : ∀ x y : Bool, (¬ ¬ PrimDiff.D2 x y) ↔ PrimDiff.D2 x y := by
  intro x y; constructor
  · intro h; cases x <;> cases y <;> first | exact ⟨rfl, rfl⟩ | exact absurd (fun hd : PrimDiff.D2 _ _ => by cases hd with | intro h1 h2 => cases h1) h |  exact absurd (fun hd : PrimDiff.D2 _ _ => by cases hd with | intro h1 h2 => cases h2) h
  · intro h hn; exact hn h
-- vacuity: no_kernel_on_subsingleton hypotheses jointly unsatisfiable by design (that is the theorem)
#print axioms kernel_not_bs
#print axioms kernel_zero_not_trans
#print axioms kernel_not_observer
#print axioms kernel_no_terminal_collector
#print axioms entry_pre_observation
#print axioms contactCells_length
#eval contactCells.length
#eval (contactCells.map (·.1)).eraseDups.length
