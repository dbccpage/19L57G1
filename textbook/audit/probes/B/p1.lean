import Derivation.PrimDiff
import Derivation.Bridge
#print axioms PrimDiff.selfdiff_consistent
#print axioms PrimDiff.obstruction_under_irrefl
#check @PrimDiff.obstruction_under_irrefl
-- vacuity probe: FidelityObstruction Irrefl holds for ANY r with a witnessed collided pair
example : PrimDiff.FidelityObstruction PrimDiff.Irrefl (fun _ _ : Unit => True) (fun _ : Unit => ()) :=
  PrimDiff.obstruction_under_irrefl (a := ()) (b := ()) trivial rfl
#check @Bridge.irrefl_law_not_entailed
