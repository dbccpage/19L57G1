import Derivation.PresentationRelativity
open PresentationRelativity Compression
#print axioms PresentationRelativity.forced_split_of_factorization_failure
#print axioms PresentationRelativity.Metatheory.attempted_absolute_identification_collapses_to_equality
-- On the empty carrier every map factors through every other, so the
-- forced-split theorem's hypothesis is unsatisfiable there (not a defect, a scope note).
example (p q : Nat → Nat) : FactorsOn [] p q := ⟨fun _ => 0, fun _ h => by cases h⟩
-- Concrete instance: D = [0,1], p constant, q = id: the forced pair is (0,1).
example : ¬ FactorsOn [0,1] (fun _ => 0) id := by
  rintro ⟨g, hg⟩
  have h0 := hg 0 (by simp); have h1 := hg 1 (by simp)
  simp at h0 h1; omega
#eval classCount [0,1] [fun _ => 0]
#eval classCount [0,1] [jointPresentation [0,1] (fun _ => 0) id]
#check @PresentationRelativity.Metatheory.AllViewsIdentify
