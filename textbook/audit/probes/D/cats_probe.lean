import Derivation.PrimitiveCats
open PrimitiveCats
-- Probe 1: wideObj 0 (carrier Fin 2) IS initial, so the paper's
-- "every one of them admits two distinct morphisms out" (said of
-- ptd_on_every_larger_carrier's objects) overreads at n = 0.
theorem wideObj0_initial : Initial (wideObj 0) := by
  intro T
  refine ⟨⟨fun t => if t.val = 0 then T.a else T.b, rfl, rfl, ?_⟩, ?_⟩
  · intro x y hxy
    have hx := hxy.1; have hy := hxy.2
    subst hx; subst hy
    exact T.w
  · intro h'
    apply hom_ext
    funext t
    match t with
    | ⟨0, _⟩ => exact h'.ha
    | ⟨1, _⟩ => exact h'.hb
-- Probe 2: the general fact that an initial object's carrier is in
-- bijection with Bool (via initials_iso) is derivable but not stated
-- in the module; we only check that initials_iso has the expected type.
#check @initials_iso
#print axioms wideObj0_initial
#print axioms PrimitiveCats.catsFindings
