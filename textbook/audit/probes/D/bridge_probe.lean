import Derivation.ContactBridge
open DiffInterface ContactBridge
-- apartObs law fields are literally the IsApart fields
example {X : Type} (r : X → X → Prop) (h : Apartness.IsApart r) :
    (apartObs r h).zero_refl = fun {x} => h.irrefl x := rfl
-- kernelStage: retained is False by construction, so no obstruction is by h.1
example {X R : Type} (O : DiffObs X R) (x y : X) : (kernelStage O).retained x y = False := rfl
-- obsSetting stores: ret/prot False, Ops empty
example {X R : Type} (O : DiffObs X R) (a b : X) (x y : X) : (obsSetting O a b).ret x y = False := rfl
example {X R : Type} (O : DiffObs X R) (a b : X) (x y : X) : (obsSetting O a b).prot x y = False := rfl
-- unit_total_not_repr is Prop-valued only: Bool-valued observer on Unit representing the total relation?
#check @unit_total_not_repr
#check @d2_not_obs_complement
#check @obsApart_repr_iff
#check @cotrans_schema_iff_wlem
#check @observation_stage_realizes_observer
#print axioms kernel_stage_no_obstruction
#print axioms obsApart_repr_iff
#print axioms bool_bs_repr
#print axioms d_not_witnessed_repr
#print axioms cotrans_schema_iff_wlem
