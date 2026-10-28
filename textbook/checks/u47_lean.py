"""Unit 47 check: kernel-check the book's Lean for Unit 47.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u47_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.NoOutside

namespace Textbook.U47
open Represented NoOutside

def storyH : List Event :=
  [.setBudget 9, .admitTok 10, .admitTok 20, .admitTok 30,
   .require 0 1, .require 0 2, .require 1 2, .addView [0]]

def story : World := replay storyH genesis

/-- Two beginnings that differ only in the notes field agree on support
after the whole story: `support_replay` with the agreement supplied by `rfl`. -/
theorem notes_inert_history :
    supp (replay storyH { genesis with notes := [7, 8] }) = supp (replay storyH genesis) :=
  support_replay storyH rfl

/-- The two worlds stay different as worlds: the notes are still there. -/
theorem notes_still_differ :
    (replay storyH { genesis with notes := [7, 8] }).notes = [7, 8] ∧
    (replay storyH genesis).notes = [] := by decide

/-- The bundled dichotomy on the story, for the violated pair. -/
theorem dichotomy_instance :
    supp (replay storyH { genesis with notes := [7, 8] }) = supp story ∧
    repairFamily (replay storyH { genesis with notes := [7, 8] }) (1, 2) =
      repairFamily story (1, 2) ∧
    obstructedB (replay storyH { genesis with notes := [7, 8] }) (1, 2) =
      obstructedB story (1, 2) ∧
    quiescentB (replay storyH { genesis with notes := [7, 8] }) = quiescentB story :=
  effectual_outside_dichotomy _ _ rfl storyH (1, 2)

/-- The contrapositive, as a lemma: a difference in a verdict is a
difference in the support. -/
theorem differs_in_support (w w' : World) (h : quiescentB w ≠ quiescentB w') :
    supp w ≠ supp w' :=
  fun hs => h (support_quiescent w w' hs)

/-- And an instance of it: the story and its extension by `[1]` differ
in quiescence, so they differ in support (here, in the views). -/
theorem story_extension_differs :
    quiescentB story = false ∧ quiescentB (step story (.addView [1])) = true ∧
    supp story ≠ supp (step story (.addView [1])) := by
  refine ⟨by decide, by decide, differs_in_support _ _ ?_⟩
  decide

/-- The extended kernel: the story's events as base events, then two
evaluators admitted; the base is the story and the panel is the two. -/
def cstory : CWorld :=
  replayC (storyH.map CEvent.base ++ [.admitEvaluator [[0]], .admitEvaluator [[0, 1]]])
    ⟨genesis, []⟩

theorem cstory_values : cstory.base = story ∧ cstory.panel = [[[0]], [[0, 1]]] := by
  decide

/-- Admitting an evaluator twice records it once; admission between
base events leaves the base alone. -/
theorem admit_twice :
    (replayC [.admitEvaluator [[0]], .admitEvaluator [[0]]] ⟨genesis, []⟩).panel = [[[0]]] := by
  decide

theorem admit_inert_instance :
    (stepC cstory (.admitEvaluator [[1]])).base = story :=
  (admitEvaluator_base_inert cstory [[1]]).trans cstory_values.1

/-- The verdicts read the panel, not the base: the base is never consulted. -/
theorem cert_reads_panel (w : World) (p : List Evaluator) (i j : Nat) :
    certNegC ⟨w, p⟩ i j = certNegB p i j ∧ certPosC ⟨w, p⟩ i j = certPosB p i j :=
  ⟨rfl, rfl⟩

/-- A split panel certifies nothing either way: one evaluator separates
0 from 1, the other does not. -/
theorem split_panel :
    certPosC cstory 0 1 = false ∧ certNegC cstory 0 1 = false := by decide

/-- The ceiling on the story's base: a unanimous blind panel certifies
0 ~ 1 while the story's own column `[0]` separates them. -/
theorem ceiling_on_story :
    certNegC ⟨story, [[[0, 1]], [[0, 1]]]⟩ 0 1 = true ∧ sepB [0] 0 1 = true ∧
    [0] ∈ story.views := by decide

/-- The joint quotient, obtained from the certificate by the characterisation. -/
theorem panel_equiv_instance : PanelEquiv [[[0, 1]], [[0, 1]]] 0 1 :=
  ((certNeg_iff_panelEquiv _ 0 1).mp (by decide)).2

/-- The empty panel: its joint quotient is total, its certificate is false. -/
theorem empty_panel : PanelEquiv [] 0 1 ∧ certNegB [] 0 1 = false := by
  refine ⟨?_, by decide⟩
  intro E hE
  cases hE

/-- Transitivity, from the equivalence. -/
theorem quotient_trans (p : List Evaluator) (h1 : PanelEquiv p 0 1) (h2 : PanelEquiv p 1 2) :
    PanelEquiv p 0 2 :=
  (panel_equiv p).trans h1 h2

/-- The family ceiling on `Bool` with the swap: equivariant, and there is
no fixed point for it to constrain. -/
theorem family_ceiling_bool :
    ∀ b : Bool, (!b) = b → ([b, !b].map not) = [b, !b] :=
  equivariant_family_invariant not not (fun b => [b, !b]) (fun _ => rfl)

theorem no_fixed_point : ∀ b : Bool, (!b) ≠ b := by decide

end Textbook.U47

#print axioms Textbook.U47.notes_inert_history
#print axioms Textbook.U47.notes_still_differ
#print axioms Textbook.U47.dichotomy_instance
#print axioms Textbook.U47.differs_in_support
#print axioms Textbook.U47.story_extension_differs
#print axioms Textbook.U47.cstory_values
#print axioms Textbook.U47.admit_twice
#print axioms Textbook.U47.admit_inert_instance
#print axioms Textbook.U47.cert_reads_panel
#print axioms Textbook.U47.split_panel
#print axioms Textbook.U47.ceiling_on_story
#print axioms Textbook.U47.panel_equiv_instance
#print axioms Textbook.U47.empty_panel
#print axioms Textbook.U47.quotient_trans
#print axioms Textbook.U47.family_ceiling_bool
#print axioms Textbook.U47.no_fixed_point
#print axioms NoOutside.support_replay
#print axioms NoOutside.support_repairFamily
#print axioms NoOutside.support_quiescent
#print axioms NoOutside.support_obstructed
#print axioms NoOutside.effectual_outside_dichotomy
#print axioms NoOutside.equivariant_family_invariant
#print axioms NoOutside.stepC_conservative
#print axioms NoOutside.admitEvaluator_base_inert
#print axioms NoOutside.panel_equiv
#print axioms NoOutside.certNeg_iff_panelEquiv
#print axioms NoOutside.certC_ceiling
"""

EXPECTED = {
    "Textbook.U47.notes_inert_history": BOTH,
    "Textbook.U47.notes_still_differ": BOTH,
    "Textbook.U47.dichotomy_instance": BOTH,
    "Textbook.U47.differs_in_support": BOTH,
    "Textbook.U47.story_extension_differs": BOTH,
    "Textbook.U47.cstory_values": BOTH,
    "Textbook.U47.admit_twice": BOTH,
    "Textbook.U47.admit_inert_instance": BOTH,
    "Textbook.U47.cert_reads_panel": BOTH,
    "Textbook.U47.split_panel": BOTH,
    "Textbook.U47.ceiling_on_story": BOTH,
    "Textbook.U47.panel_equiv_instance": BOTH,
    "Textbook.U47.empty_panel": BOTH,
    "Textbook.U47.quotient_trans": NONE,
    "Textbook.U47.family_ceiling_bool": NONE,
    "Textbook.U47.no_fixed_point": NONE,
    "NoOutside.support_replay": BOTH,
    "NoOutside.support_repairFamily": BOTH,
    "NoOutside.support_quiescent": BOTH,
    "NoOutside.support_obstructed": BOTH,
    "NoOutside.effectual_outside_dichotomy": BOTH,
    "NoOutside.equivariant_family_invariant": NONE,
    "NoOutside.stepC_conservative": BOTH,
    "NoOutside.admitEvaluator_base_inert": BOTH,
    "NoOutside.panel_equiv": NONE,
    "NoOutside.certNeg_iff_panelEquiv": BOTH,
    "NoOutside.certC_ceiling": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U47"))
