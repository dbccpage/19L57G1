import CanonicalMinimizer

/-!
# Inventory: Replay Audit and Axiom Roll-Call for CL-ISO-SOUND

Axiom verification for all formal theorems in `Permutation.lean`, `RegimeAction.lean`,
and `CanonicalMinimizer.lean`.

Requirement R3: Axiom audit verifying all theorems depend strictly on
`{propext, Quot.sound}` or no axioms.

Narrowed 2026-09-18: the completeness claim above is WITHDRAWN.
Rechecked 2026-09-19: this file reports exactly the 27 theorem
constants named by its report lines below. The verifier requires that
exact named population. A fresh compiled-module census found
60 non-internal theorem constants in the three local modules, including
generated declarations and proof-valued instances; 33 are outside this
report list. These are compiled constants, not a count of explicit
theorem statements in source. The previous draft counts are superseded
by this population criterion.
A reported theorem includes the axioms of its dependencies. An
unreported declaration that no reported theorem uses remains outside
this audit. This note does not turn the named list into a full census.

AuthorityEffect: None.
-/

namespace IsoSoundLean

-- Permutation group laws
#print axioms Perm.ext
#print axioms Perm.id_comp
#print axioms Perm.comp_id
#print axioms Perm.comp_assoc
#print axioms Perm.comp_left_inv
#print axioms Perm.comp_right_inv
#print axioms Perm.inv_id
#print axioms Perm.inv_inv
#print axioms Perm.inv_comp

-- Group action & orbit equivalence
#print axioms inv_act_act
#print axioms act_inv_act
#print axioms act_inj
#print axioms act_eq_iff
#print axioms iso_refl
#print axioms iso_symm
#print axioms iso_trans
#print axioms mem_orbit_iff
#print axioms iso_iff_same_orbit

-- Canonical minimizer, witness inversion & soundness
#print axioms witness_extract
#print axioms iso_witness_of_orbit_choice
#print axioms cl_iso_sound
#print axioms cl_iso_complete
#print axioms canonical_classification
#print axioms key_soundness
#print axioms key_classification
#print axioms equivariant_search_same_image
#print axioms minimizer_isomorphism_sound

end IsoSoundLean
