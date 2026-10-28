import Derivation.PresentationNaturality
open PresentationNaturality
#print axioms PresentationNaturality.no_natural_section_of_fixed_point_free
#print axioms PresentationNaturality.bool_obstruction_and_sealed_selector
#print axioms PresentationNaturality.heterogeneous_naturality_separates
-- The obstruction unfolds to a fixed-point statement over a one-object family:
example (O : DiffInterface.DiffObs X R) (F : PresIso O O) :
    (∃ s : Sec (autoFamily O F), IsNatural (autoFamily O F) s) ↔
    (∃ p : ContactKernel.NonZeroPair O, F.mapPair p = p) :=
  ⟨fun ⟨s, hs⟩ => ⟨s (), hs ()⟩, fun ⟨p, hp⟩ => ⟨fun _ => p, fun _ => hp⟩⟩
