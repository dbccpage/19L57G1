/-
AxiomReport: one report per theorem originating in this tree, followed by
the reconstructed pinned statements this tree is stated against.  Names are
fully qualified so the report text and this list are the same strings, which
is what `verify_lean.py` diffs.  AuthorityEffect: None.

2026-09-25: every theorem written in `Base.lean` is now listed.  Until then
five of its twelve (`refl_car`, `trans_car`, `symm_car_left`,
`symm_car_right`, `symm_symm_car`) had no report, and the source census in
`verify_lean.py` read `Closure.lean` only, so nothing noticed.
-/

import ClosedFamily

#print axioms ClosedFamily.Closure.sec_closure_eq
#print axioms ClosedFamily.Closure.mapPair_nil
#print axioms ClosedFamily.Closure.mapPair_comp
#print axioms ClosedFamily.Closure.mapPair_one
#print axioms ClosedFamily.Closure.mapPair_oneInv
#print axioms ClosedFamily.Closure.mapPair_inv
#print axioms ClosedFamily.Closure.comp_assoc
#print axioms ClosedFamily.Closure.nil_comp
#print axioms ClosedFamily.Closure.comp_nil
#print axioms ClosedFamily.Closure.natural_symm
#print axioms ClosedFamily.Closure.natural_on_path
#print axioms ClosedFamily.Closure.natural_iff_natural_closure
#print axioms ClosedFamily.Closure.has_natural_section_iff
#print axioms ClosedFamily.Closure.natural_closure_closure
#print axioms ClosedFamily.zeroRel_equivalence
#print axioms ClosedFamily.zeroRel_transport
#print axioms ClosedFamily.refl_car
#print axioms ClosedFamily.trans_car
#print axioms ClosedFamily.symm_car_left
#print axioms ClosedFamily.symm_car_right
#print axioms ClosedFamily.symm_symm_car
#print axioms ClosedFamily.mapPair_refl
#print axioms ClosedFamily.mapPair_trans
#print axioms ClosedFamily.mapPair_symm_left
#print axioms ClosedFamily.mapPair_symm_right
#print axioms ClosedFamily.Bij.fwd_injective
