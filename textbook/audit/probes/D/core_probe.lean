import Derivation.PrimitiveCore
open PrimitiveCore
#print axioms PrimitiveCore.tri_not_bc
#print axioms PrimitiveCore.d2_not_symm
#print axioms PrimitiveCore.triSym_not_bc
#print axioms PrimitiveCore.boolEmpty_e
-- f_ops_irrelevant is definitional
example : ∀ S : Setting, ∀ O' : (S.X → S.X) → Prop, F { S with Ops := O' } ↔ F S := fun _ _ => Iff.rfl
-- the W→Bl countermodel fails Bl only through A: unitBare is located
example : Located unitBare.r := located_of_decidable _
-- Located over a non-decidable relation is not refutable here: sanity that Located is a Prop existential over X → X → Bool
#check @Located
