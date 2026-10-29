"""Unit 54 check: kernel-check the book's Lean for Unit 54.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u54_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.PrimitivePassage

namespace Textbook.U54
open PrimitivePassage

/-- The four gates at the five witness states, read off by computation.
Each row is (retained, protected, declared, zero under the declared
convention); only the last row makes `obstP` true. -/
theorem gate_rows :
    (retainedP gateWitnessNoZero 0 1, protectedP gateWitnessNoZero 0 1,
      declaredP gateWitnessNoZero, zeroDeclP gateWitnessNoZero 0 1)
      = (true, true, true, false) ∧
    (retainedP gateWitnessNoDeclaration 0 1, protectedP gateWitnessNoDeclaration 0 1,
      declaredP gateWitnessNoDeclaration, zeroDeclP gateWitnessNoDeclaration 0 1)
      = (true, true, false, true) ∧
    (retainedP gateWitnessNoProtection 0 1, protectedP gateWitnessNoProtection 0 1,
      declaredP gateWitnessNoProtection, zeroDeclP gateWitnessNoProtection 0 1)
      = (true, false, true, true) ∧
    (retainedP gateWitnessNoRetention 0 1, protectedP gateWitnessNoRetention 0 1,
      declaredP gateWitnessNoRetention, zeroDeclP gateWitnessNoRetention 0 1)
      = (false, true, true, true) ∧
    (retainedP gateWitnessAll 0 1, protectedP gateWitnessAll 0 1,
      declaredP gateWitnessAll, zeroDeclP gateWitnessAll 0 1)
      = (true, true, true, true) := by
  decide

theorem obst_rows :
    obstP gateWitnessNoZero 0 1 = false ∧ obstP gateWitnessNoDeclaration 0 1 = false ∧
    obstP gateWitnessNoProtection 0 1 = false ∧ obstP gateWitnessNoRetention 0 1 = false ∧
    obstP gateWitnessAll 0 1 = true := by
  decide

/-- The declared convention, made visible: before any observation gate 4
reads `true`, and `obstP` is still `false` because gate 3 fails. -/
theorem convention_before_declaration :
    zeroDeclP gateWitnessNoDeclaration 0 1 = true ∧
    zeroStrictP gateWitnessNoDeclaration 0 1 = false ∧
    obstP gateWitnessNoDeclaration 0 1 = false := by
  decide

/-- Genesis's factorisation, instantiated at the all-gates witness. -/
theorem factors_at_all :
    obstP gateWitnessAll 0 1 =
      (retainedP gateWitnessAll 0 1 && protectedP gateWitnessAll 0 1
        && declaredP gateWitnessAll && zeroDeclP gateWitnessAll 0 1) :=
  obstP_factors gateWitnessAll 0 1

/-- Assertion, retention, protection, declaration: one history, four
stores, each filled by its own event and by nothing else. -/
def hist4 : List PEvent :=
  [.admitOcc 7, .admitOcc 8, .assertWit 0 1, .admitWit 0 1, .protect 0 1, .declareObs]

theorem history_stores :
    (replayP hist4 genesisP).occ = [7, 8] ∧
    (replayP hist4 genesisP).asserted = [(0, 1)] ∧
    (replayP hist4 genesisP).wit = [(0, 1)] ∧
    (replayP hist4 genesisP).prot = [(0, 1)] ∧
    (replayP hist4 genesisP).obs = some [] := by
  decide

/-- The same history is `gateWitnessAll` except for the occurrence tokens. -/
theorem history_obstructs : obstP (replayP hist4 genesisP) 0 1 = true := by decide

/-- Retention asked for before any assertion changes nothing. -/
theorem early_retention_inert :
    step (replayP [.admitOcc 7, .admitOcc 8] genesisP) (.admitWit 0 1)
      = replayP [.admitOcc 7, .admitOcc 8] genesisP := by
  decide

/-- Protection asked for before retention changes nothing. -/
theorem early_protection_inert :
    step (replayP [.admitOcc 7, .admitOcc 8, .assertWit 0 1] genesisP) (.protect 0 1)
      = replayP [.admitOcc 7, .admitOcc 8, .assertWit 0 1] genesisP := by
  decide

/-- The two policies on a pre-observational state, as computed values. -/
theorem policies_at_pre :
    obstEmptyObs preRetainedObstructed 0 1 = true ∧
    obstP preRetainedObstructed 0 1 = false := by
  decide

/-- Genesis's agreement theorem, instantiated where an observation exists. -/
theorem policies_agree_at_all :
    obstP gateWitnessAll 0 1 = obstEmptyObs gateWitnessAll 0 1 :=
  obst_policies_agree_when_declared gateWitnessAll [] rfl 0 1

/-- The two-rule at the all-gates witness: nothing to repair, so the
extension branch must be taken, and the extension list is computed. -/
theorem two_rule_at_all :
    repairFamily gateWitnessAll 0 1 ≠ [] ∨
      (repairFamily gateWitnessAll 0 1 = [] ∧
        extensionProposals gateWitnessAll 0 1 ≠ []) :=
  two_rule gateWitnessAll 0 1 (by decide) (by decide) (by decide) (by decide)

theorem families_at_all :
    repairFamily gateWitnessAll 0 1 = [] ∧
    extensionProposals gateWitnessAll 0 1 = [[0], [1]] ∧
    nextFamilyP gateWitnessAll =
      [[.setBudget 1, .addCol [0]], [.setBudget 1, .addCol [1]]] := by
  decide

/-- Running the first represented block from the all-gates witness clears
the obstruction and empties the next family. -/
theorem block_resolves :
    obstP (replayP [.setBudget 1, .addCol [0]] gateWitnessAll) 0 1 = false ∧
    nextFamilyP (replayP [.setBudget 1, .addCol [0]] gateWitnessAll) = [] := by
  decide

/-- Genesis's `extension_resolves`, instantiated at the funded witness. -/
def fundedAll : PState := { gateWitnessAll with budget := 5 }

theorem resolves_at_funded : obstP (step fundedAll (.addCol [0])) 0 1 = false :=
  extension_resolves fundedAll [0] 0 1 [] rfl (by decide) (by decide) rfl
    (by decide) rfl

/-- The two gates on execution: no licence, or no budget, and the
proposal stays a proposal. -/
theorem no_licence_no_column :
    step { fundedAll with licensed := false } (.addCol [0])
      = { fundedAll with licensed := false } :=
  proposal_not_execution _ _ rfl rfl

theorem no_budget_no_column : step gateWitnessAll (.addCol [0]) = gateWitnessAll :=
  budget_gates_execution _ _ rfl rfl

/-- A refusal records the pair and moves nothing else; the obstruction
is still there afterwards. -/
theorem refusal_records :
    (step fundedAll (.refuse 0 1)).refusals = [(0, 1)] ∧
    (step fundedAll (.refuse 0 1)).obs = some [] ∧
    obstP (step fundedAll (.refuse 0 1)) 0 1 = true ∧
    (step fundedAll (.refuse 0 1)).halted = false := by
  decide

/-- Without the certificate the refusal event is inert. -/
theorem refusal_needs_certificate :
    step gateWitnessNoZero (.refuse 0 1) = gateWitnessNoZero := by
  decide

/-- The terminal absorbs: Genesis's theorem at one event. -/
theorem halt_absorbs_admit :
    step (step fundedAll .halt) (.admitOcc 9) = step fundedAll .halt :=
  terminal_absorbing fundedAll (.admitOcc 9)

/-- The quotient lemma at a concrete collapse: once `q` sends 0 and 1 to
the same point, any relation on the image cannot see the pair. -/
theorem collapse_cannot_see (g : Bool → Bool → Prop) :
    g ((fun _ : Nat => true) 0) ((fun _ : Nat => true) 1) ↔
    g ((fun _ : Nat => true) 0) ((fun _ : Nat => true) 0) :=
  quotient_no_recovery (fun _ : Nat => true) 0 1 rfl g

/-- The induced setting of the all-gates witness reads the stores as
Unit 51 relations: `arb` holds, retention holds, protection holds. -/
theorem induced_reading :
    (inducedSetting gateWitnessAll 0 1).r (0 : Nat) (1 : Nat) ∧
    (inducedSetting gateWitnessAll 0 1).ret (0 : Nat) (1 : Nat) ∧
    (inducedSetting gateWitnessAll 0 1).prot (0 : Nat) (1 : Nat) ∧
    ¬ (inducedSetting gateWitnessAll 0 1).r (1 : Nat) (0 : Nat) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · show (0, 1) ∈ gateWitnessAll.asserted
    decide
  · show (0, 1) ∈ gateWitnessAll.wit
    decide
  · show (0, 1) ∈ gateWitnessAll.prot
    decide
  · show ¬ (1, 0) ∈ gateWitnessAll.asserted
    decide

/-- Singleton proposals are a declared menu, not all columns accepted by colOk. -/
theorem singleton_menu_not_all_columns :
    let s := { gateWitnessAll with occ := [0, 1, 2] }
    colOk s [0, 2] = true ∧ [0, 2] ∉ extensionProposals s 0 1 := by decide

end Textbook.U54

#print axioms Textbook.U54.gate_rows
#print axioms Textbook.U54.singleton_menu_not_all_columns
#print axioms Textbook.U54.obst_rows
#print axioms Textbook.U54.convention_before_declaration
#print axioms Textbook.U54.factors_at_all
#print axioms Textbook.U54.history_stores
#print axioms Textbook.U54.history_obstructs
#print axioms Textbook.U54.early_retention_inert
#print axioms Textbook.U54.early_protection_inert
#print axioms Textbook.U54.policies_at_pre
#print axioms Textbook.U54.policies_agree_at_all
#print axioms Textbook.U54.two_rule_at_all
#print axioms Textbook.U54.families_at_all
#print axioms Textbook.U54.block_resolves
#print axioms Textbook.U54.resolves_at_funded
#print axioms Textbook.U54.no_licence_no_column
#print axioms Textbook.U54.no_budget_no_column
#print axioms Textbook.U54.refusal_records
#print axioms Textbook.U54.refusal_needs_certificate
#print axioms Textbook.U54.halt_absorbs_admit
#print axioms Textbook.U54.collapse_cannot_see
#print axioms Textbook.U54.induced_reading
#print axioms PrimitivePassage.obstP_factors
#print axioms PrimitivePassage.obst_requires_observation
#print axioms PrimitivePassage.obst_policies_differ
#print axioms PrimitivePassage.gate_zero_independent
#print axioms PrimitivePassage.gate_declared_independent
#print axioms PrimitivePassage.gate_protection_independent
#print axioms PrimitivePassage.gate_retention_independent
#print axioms PrimitivePassage.assertion_not_retained
#print axioms PrimitivePassage.retention_requires_assertion
#print axioms PrimitivePassage.retention_persists
#print axioms PrimitivePassage.no_protection_no_obstruction
#print axioms PrimitivePassage.quotient_no_recovery
#print axioms PrimitivePassage.zero_trans
#print axioms PrimitivePassage.two_rule
#print axioms PrimitivePassage.proposal_not_execution
#print axioms PrimitivePassage.budget_gates_execution
#print axioms PrimitivePassage.refusal_object_inert
#print axioms PrimitivePassage.terminal_absorbing
#print axioms PrimitivePassage.replay_deterministic
#print axioms PrimitivePassage.extension_resolves
#print axioms PrimitivePassage.nextFamilyP_stop
#print axioms PrimitivePassage.nextFamilyP_nonempty
"""

EXPECTED = {
    "Textbook.U54.gate_rows": BOTH,
    "Textbook.U54.singleton_menu_not_all_columns": BOTH,
    "Textbook.U54.obst_rows": BOTH,
    "Textbook.U54.convention_before_declaration": BOTH,
    "Textbook.U54.factors_at_all": BOTH,
    "Textbook.U54.history_stores": BOTH,
    "Textbook.U54.history_obstructs": BOTH,
    "Textbook.U54.early_retention_inert": BOTH,
    "Textbook.U54.early_protection_inert": BOTH,
    "Textbook.U54.policies_at_pre": BOTH,
    "Textbook.U54.policies_agree_at_all": BOTH,
    "Textbook.U54.two_rule_at_all": BOTH,
    "Textbook.U54.families_at_all": BOTH,
    "Textbook.U54.block_resolves": BOTH,
    "Textbook.U54.resolves_at_funded": BOTH,
    "Textbook.U54.no_licence_no_column": BOTH,
    "Textbook.U54.no_budget_no_column": BOTH,
    "Textbook.U54.refusal_records": BOTH,
    "Textbook.U54.refusal_needs_certificate": BOTH,
    "Textbook.U54.halt_absorbs_admit": BOTH,
    "Textbook.U54.collapse_cannot_see": NONE,
    "Textbook.U54.induced_reading": BOTH,
    "PrimitivePassage.obstP_factors": BOTH,
    "PrimitivePassage.obst_requires_observation": BOTH,
    "PrimitivePassage.obst_policies_differ": BOTH,
    "PrimitivePassage.gate_zero_independent": BOTH,
    "PrimitivePassage.gate_declared_independent": BOTH,
    "PrimitivePassage.gate_protection_independent": BOTH,
    "PrimitivePassage.gate_retention_independent": BOTH,
    "PrimitivePassage.assertion_not_retained": BOTH,
    "PrimitivePassage.retention_requires_assertion": BOTH,
    "PrimitivePassage.retention_persists": BOTH,
    "PrimitivePassage.no_protection_no_obstruction": BOTH,
    "PrimitivePassage.quotient_no_recovery": NONE,
    "PrimitivePassage.zero_trans": BOTH,
    "PrimitivePassage.two_rule": BOTH,
    "PrimitivePassage.proposal_not_execution": BOTH,
    "PrimitivePassage.budget_gates_execution": BOTH,
    "PrimitivePassage.refusal_object_inert": BOTH,
    "PrimitivePassage.terminal_absorbing": BOTH,
    "PrimitivePassage.replay_deterministic": BOTH,
    "PrimitivePassage.extension_resolves": BOTH,
    "PrimitivePassage.nextFamilyP_stop": BOTH,
    "PrimitivePassage.nextFamilyP_nonempty": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U54"))
