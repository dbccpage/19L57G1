"""Unit 65 check: kernel-check the book's Lean for Unit 65 (TransitionAlphabet).

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u65_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.TransitionAlphabet

namespace Textbook.U65
open PrimitivePassage TransitionAlphabet

-- Audit check: explicit gainedPairs = [] corollaries for colS and refineS
theorem gainedPairs_colS_nil (s : PState) (cols : List (List Nat))
    (c : List Nat) (ho : s.obs = some cols) :
    gainedPairs s (colS s cols c) = [] := by
  unfold gainedPairs
  exact filter_notmem_eq_nil _ _ (obstructedPairs_colS_sub s cols c ho)

theorem gainedPairs_refineS_nil (s : PState) (cols : List (List Nat))
    (v : List Nat) (p : Nat) (ho : s.obs = some cols)
    (hok : refineOk s v p = true) :
    gainedPairs s (refineS s cols v p) = [] := by
  unfold gainedPairs
  exact filter_notmem_eq_nil _ _ (obstructedPairs_refineS_sub s cols v p ho hok)

-- Student exercise check on budS wObstructed 2
theorem budget_exercise_check :
    let s := budS wObstructed 2
    classOf s (.setBudget 0) = .writeBudget ∧
    classOf s (.setBudget 1) = .writeBudget ∧
    budgetDeltaOf s (step s (.setBudget 0)) = .rewritten ∧
    budgetDeltaOf s (step s (.setBudget 1)) = .spentOne ∧
    Accepted (step s (.setBudget 0)) (.addCol [0]) = false ∧
    Accepted (step s (.setBudget 1)) (.addCol [0]) = true := by
  decide

end Textbook.U65

#print axioms Textbook.U65.gainedPairs_colS_nil
#print axioms Textbook.U65.gainedPairs_refineS_nil
#print axioms Textbook.U65.budget_exercise_check
#print axioms TransitionAlphabet.halted_accepts_nothing
#print axioms TransitionAlphabet.halt_inert_on_halted
#print axioms TransitionAlphabet.accepted_eq_guardHolds
#print axioms TransitionAlphabet.obstMove_inert_of_eq
#print axioms TransitionAlphabet.obstEffect_split_of_inert
#print axioms TransitionAlphabet.obstEffect_colS
#print axioms TransitionAlphabet.obstEffect_refineS
#print axioms TransitionAlphabet.wf_of_replay
#print axioms TransitionAlphabet.sig_eq_classSig
#print axioms TransitionAlphabet.classSig_inj
#print axioms TransitionAlphabet.exists_unique_class
#print axioms TransitionAlphabet.declared_codebook_size
#print axioms TransitionAlphabet.guard_erased_codebook_size
#print axioms TransitionAlphabet.classSig_not_right_congruent_occurrence
#print axioms TransitionAlphabet.classSig_not_right_congruent_budget
#print axioms TransitionAlphabet.refine_addCol_effect_merge
#print axioms TransitionAlphabet.refine_addCol_domain_countermodel
#print axioms TransitionAlphabet.preserved_untouched_not_invariant
#print axioms TransitionAlphabet.budgetDelta_not_invariant
#print axioms TransitionAlphabet.budgetDelta_of_funded_guard
#print axioms TransitionAlphabet.refuse_preserves
#print axioms TransitionAlphabet.retention_creates_outside_class
#print axioms TransitionAlphabet.nextFamily_block_shape
#print axioms TransitionAlphabet.internal_family_no_occurrence_supply
#print axioms TransitionAlphabet.internal_family_no_license_write
#print axioms TransitionAlphabet.internal_family_no_terminal
#print axioms TransitionAlphabet.internal_family_emits_budget_write
#print axioms TransitionAlphabet.env_ownership_claim_refuted
#print axioms TransitionAlphabet.internal_family_env_only_unit_funding
#print axioms TransitionAlphabet.nonEnv_preserves_occ_licensed
#print axioms TransitionAlphabet.class_witnesses
#print axioms TransitionAlphabet.class_witness_sizes
"""

EXPECTED = {
    "Textbook.U65.gainedPairs_colS_nil": BOTH,
    "Textbook.U65.gainedPairs_refineS_nil": BOTH,
    "Textbook.U65.budget_exercise_check": BOTH,
    "TransitionAlphabet.halted_accepts_nothing": BOTH,
    "TransitionAlphabet.halt_inert_on_halted": BOTH,
    "TransitionAlphabet.accepted_eq_guardHolds": BOTH,
    "TransitionAlphabet.obstMove_inert_of_eq": BOTH,
    "TransitionAlphabet.obstEffect_split_of_inert": BOTH,
    "TransitionAlphabet.obstEffect_colS": BOTH,
    "TransitionAlphabet.obstEffect_refineS": BOTH,
    "TransitionAlphabet.wf_of_replay": BOTH,
    "TransitionAlphabet.sig_eq_classSig": BOTH,
    "TransitionAlphabet.classSig_inj": NONE,
    "TransitionAlphabet.exists_unique_class": BOTH,
    "TransitionAlphabet.declared_codebook_size": PROPEXT,
    "TransitionAlphabet.guard_erased_codebook_size": PROPEXT,
    "TransitionAlphabet.classSig_not_right_congruent_occurrence": BOTH,
    "TransitionAlphabet.classSig_not_right_congruent_budget": BOTH,
    "TransitionAlphabet.refine_addCol_effect_merge": BOTH,
    "TransitionAlphabet.refine_addCol_domain_countermodel": BOTH,
    "TransitionAlphabet.preserved_untouched_not_invariant": BOTH,
    "TransitionAlphabet.budgetDelta_not_invariant": BOTH,
    "TransitionAlphabet.budgetDelta_of_funded_guard": BOTH,
    "TransitionAlphabet.refuse_preserves": BOTH,
    "TransitionAlphabet.retention_creates_outside_class": BOTH,
    "TransitionAlphabet.nextFamily_block_shape": BOTH,
    "TransitionAlphabet.internal_family_no_occurrence_supply": BOTH,
    "TransitionAlphabet.internal_family_no_license_write": BOTH,
    "TransitionAlphabet.internal_family_no_terminal": BOTH,
    "TransitionAlphabet.internal_family_emits_budget_write": BOTH,
    "TransitionAlphabet.env_ownership_claim_refuted": BOTH,
    "TransitionAlphabet.internal_family_env_only_unit_funding": BOTH,
    "TransitionAlphabet.nonEnv_preserves_occ_licensed": BOTH,
    "TransitionAlphabet.class_witnesses": BOTH,
    "TransitionAlphabet.class_witness_sizes": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U65"))
