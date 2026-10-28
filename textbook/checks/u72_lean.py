from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

SNIPPET = r"""
import Derivation.PresentationDescent
import Derivation.QuotientRetention
import Derivation.FidelityClosure
import Derivation.NoOutsideFidelity
import Derivation.EndogenousFidelityGenerator

namespace Textbook.U72

open PresentationDescent
open QuotientRetention
open FidelityClosure
open NoOutsideFidelity
open EndogenousFidelityGenerator

-- 1. Concrete TranslationGap on Bool
def partialAttempt : TranslationAttempt Bool Bool where
  forward b := if b then none else some false
  backward b := some b

def gapTrue : TranslationGap partialAttempt :=
  TranslationGap.forward true rfl

theorem partialAttempt_no_totalization :
    ¬ Nonempty (Totalization partialAttempt) :=
  translation_gap_refuses_totalization gapTrue

-- 2. Audit finding (PresentationDescent.md §11.1):
--    Injective embeddings with CoincidentImages on Bool that fail RoundTripCoherent
--    because the identification equation left p = right (u.forward p) fails.
def flipAttempt : TranslationAttempt Bool Bool where
  forward b := some (!b)
  backward b := some b

def flipTotal : Totalization flipAttempt where
  forward b := !b
  backward b := b
  forward_realizes _ := rfl
  backward_realizes _ := rfl

def flipResidual : CoherenceResidual flipTotal :=
  CoherenceResidual.left false (by decide)

theorem flip_coincident_but_incoherent :
    Function.Injective (id : Bool → Bool) ∧
    CoincidentImages (id : Bool → Bool) (id : Bool → Bool) ∧
    ¬ RoundTripCoherent flipTotal ∧
    ¬ Nonempty (FaithfulCommonDescent flipTotal) := by
  refine ⟨Function.injective_id, ?_, coherence_residual_refutes_round_trip flipResidual,
    residual_forces_index_retention flipResidual⟩
  exact ⟨fun p => ⟨p, rfl⟩, fun q => ⟨q, rfl⟩⟩

-- 3. Audit finding (QuotientRetention.md §11.1):
--    symmetry_failure_retains_multiplicity applies to a non-involutive 3-cycle on Fin 3.
def eqSetoid (α : Type) : Setoid α where
  r x y := x = y
  iseqv := ⟨fun _ => rfl, fun h => h.symm, fun h1 h2 => h1.trans h2⟩

theorem eqRefinesIndiscrete : RelationRefinement (eqSetoid (Fin 3)) (indiscreteSetoid (Fin 3)) :=
  ⟨fun _ => True.intro⟩

def cycle3 (x : Fin 3) : Fin 3 :=
  match x with
  | ⟨0, _⟩ => ⟨1, by decide⟩
  | ⟨1, _⟩ => ⟨2, by decide⟩
  | ⟨2, _⟩ => ⟨0, by decide⟩

theorem cycle3_not_involutive : cycle3 (cycle3 0) ≠ 0 := by
  decide

theorem cycle3_retains_multiplicity :
    ∃ a b : Quotient (eqSetoid (Fin 3)),
      a ≠ b ∧ collapseMap eqRefinesIndiscrete a = collapseMap eqRefinesIndiscrete b :=
  symmetry_failure_retains_multiplicity eqRefinesIndiscrete cycle3 0 True.intro
    (by intro h; cases h)

-- 4. Concrete 2-step loop network with nontrivial loop action (HolonomyResidual)
def swapAttempt : TranslationAttempt Bool Bool where
  forward b := some (!b)
  backward b := some (!b)

def swapTotal : Totalization swapAttempt where
  forward b := !b
  backward b := !b
  forward_realizes _ := rfl
  backward_realizes _ := rfl

theorem swap_coherent : RoundTripCoherent swapTotal where
  left b := by cases b <;> rfl
  right b := by cases b <;> rfl

def loopNet : TranslationNetwork where
  Index := Unit
  Carrier _ := Bool
  Attempt _ _ := Unit
  pair _ := swapAttempt

def swapLoop : FidelityPath loopNet () () :=
  FidelityPath.step () swapTotal swap_coherent

def swapLoopResidual : HolonomyResidual loopNet where
  index := ()
  loop := swapLoop
  point := false
  moved := by intro h; cases h

theorem loopNet_no_faithful_descent :
    ¬ Nonempty (FaithfulNetworkDescent loopNet) :=
  holonomy_residual_refuses_faithful_network_descent swapLoopResidual

-- 5. Audit finding (EndogenousFidelityGenerator.md §4):
--    universalCollapse identifies every pair of classes by True.intro, even for
--    FidelityRel-equivalent indices.
theorem universalCollapse_always_eq (N : TranslationNetwork) (i j : N.Index) :
    universalCollapse N (classOf N i) = universalCollapse N (classOf N j) :=
  Quotient.sound True.intro

end Textbook.U72

#print axioms Textbook.U72.partialAttempt_no_totalization
#print axioms Textbook.U72.flip_coincident_but_incoherent
#print axioms Textbook.U72.cycle3_not_involutive
#print axioms Textbook.U72.cycle3_retains_multiplicity
#print axioms Textbook.U72.swap_coherent
#print axioms Textbook.U72.loopNet_no_faithful_descent
#print axioms Textbook.U72.universalCollapse_always_eq
#print axioms PresentationDescent.translation_gap_refuses_totalization
#print axioms PresentationDescent.coherence_residual_refutes_round_trip
#print axioms PresentationDescent.faithful_common_descent_has_coincident_images
#print axioms PresentationDescent.faithful_descent_to_coherent
#print axioms PresentationDescent.faithful_descent_iff_round_trip_coherent
#print axioms PresentationDescent.incoherence_forces_index_retention
#print axioms PresentationDescent.residual_forces_index_retention
#print axioms QuotientRetention.collapseMap_surjective
#print axioms QuotientRetention.failed_identification_retains_two_classes
#print axioms QuotientRetention.failed_identification_makes_collapse_noninjective
#print axioms QuotientRetention.collapseMap_injective_iff_reverse_refinement
#print axioms QuotientRetention.symmetry_failure_retains_multiplicity
#print axioms QuotientRetention.collapseMap_compose
#print axioms FidelityClosure.class_eq_iff_coherent_path
#print axioms FidelityClosure.no_coherent_path_retains_indices
#print axioms FidelityClosure.failed_endomorphism_does_not_refute_self_fidelity
#print axioms FidelityClosure.holonomy_residual_refuses_faithful_network_descent
#print axioms FidelityClosure.faithful_network_descent_forces_trivial_loops
#print axioms FidelityClosure.label_descends_iff_fidelity_invariant
#print axioms FidelityClosure.coherent_disagreement_refuses_label_descent
#print axioms FidelityClosure.polarity_flip_is_presentation_relative
#print axioms NoOutsideFidelity.support_fiber_contains_distinct_notes
#print axioms NoOutsideFidelity.support_projection_not_injective
#print axioms NoOutsideFidelity.support_translation_never_round_trip_coherent
#print axioms NoOutsideFidelity.support_translation_never_faithfully_erases_index
#print axioms NoOutsideFidelity.no_support_inverse_faithfully_erases_index
#print axioms NoOutsideFidelity.notes_fiber_has_no_operational_authority
#print axioms EndogenousFidelityGenerator.admitted_step_has_fidelity_path
#print axioms EndogenousFidelityGenerator.fidelity_is_least_equivalence_containing_admitted_steps
#print axioms EndogenousFidelityGenerator.fidelity_refines_indiscrete
#print axioms EndogenousFidelityGenerator.universalCollapse_surjective
#print axioms EndogenousFidelityGenerator.no_coherent_path_retains_multiplicity
#print axioms EndogenousFidelityGenerator.generated_structure_is_failed_erasure
"""

EXPECTED = {
    "Textbook.U72.partialAttempt_no_totalization": PROPEXT,
    "Textbook.U72.flip_coincident_but_incoherent": NONE,
    "Textbook.U72.cycle3_not_involutive": PROPEXT,
    "Textbook.U72.cycle3_retains_multiplicity": BOTH,
    "Textbook.U72.swap_coherent": NONE,
    "Textbook.U72.loopNet_no_faithful_descent": NONE,
    "Textbook.U72.universalCollapse_always_eq": QUOT,
    "PresentationDescent.translation_gap_refuses_totalization": PROPEXT,
    "PresentationDescent.coherence_residual_refutes_round_trip": NONE,
    "PresentationDescent.faithful_common_descent_has_coincident_images": NONE,
    "PresentationDescent.faithful_descent_to_coherent": NONE,
    "PresentationDescent.faithful_descent_iff_round_trip_coherent": NONE,
    "PresentationDescent.incoherence_forces_index_retention": NONE,
    "PresentationDescent.residual_forces_index_retention": NONE,
    "QuotientRetention.collapseMap_surjective": QUOT,
    "QuotientRetention.failed_identification_retains_two_classes": BOTH,
    "QuotientRetention.failed_identification_makes_collapse_noninjective": BOTH,
    "QuotientRetention.collapseMap_injective_iff_reverse_refinement": BOTH,
    "QuotientRetention.symmetry_failure_retains_multiplicity": BOTH,
    "QuotientRetention.collapseMap_compose": QUOT,
    "FidelityClosure.class_eq_iff_coherent_path": BOTH,
    "FidelityClosure.no_coherent_path_retains_indices": BOTH,
    "FidelityClosure.failed_endomorphism_does_not_refute_self_fidelity": NONE,
    "FidelityClosure.holonomy_residual_refuses_faithful_network_descent": NONE,
    "FidelityClosure.faithful_network_descent_forces_trivial_loops": NONE,
    "FidelityClosure.label_descends_iff_fidelity_invariant": QUOT,
    "FidelityClosure.coherent_disagreement_refuses_label_descent": QUOT,
    "FidelityClosure.polarity_flip_is_presentation_relative": QUOT,
    "NoOutsideFidelity.support_fiber_contains_distinct_notes": PROPEXT,
    "NoOutsideFidelity.support_projection_not_injective": PROPEXT,
    "NoOutsideFidelity.support_translation_never_round_trip_coherent": PROPEXT,
    "NoOutsideFidelity.support_translation_never_faithfully_erases_index": PROPEXT,
    "NoOutsideFidelity.no_support_inverse_faithfully_erases_index": PROPEXT,
    "NoOutsideFidelity.notes_fiber_has_no_operational_authority": BOTH,
    "EndogenousFidelityGenerator.admitted_step_has_fidelity_path": NONE,
    "EndogenousFidelityGenerator.fidelity_is_least_equivalence_containing_admitted_steps": NONE,
    "EndogenousFidelityGenerator.fidelity_refines_indiscrete": NONE,
    "EndogenousFidelityGenerator.universalCollapse_surjective": QUOT,
    "EndogenousFidelityGenerator.no_coherent_path_retains_multiplicity": BOTH,
    "EndogenousFidelityGenerator.generated_structure_is_failed_erasure": BOTH,
}


if __name__ == "__main__":
    raise SystemExit(main(SNIPPET, EXPECTED, "U72"))
