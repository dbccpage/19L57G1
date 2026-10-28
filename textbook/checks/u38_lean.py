"""Unit 38 check: kernel-check the book's Lean for Unit 38.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u38_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Refusal

namespace Textbook.U38
open Refusal Derivation

/-- A fresh token appends under every discipline. -/
theorem fresh_appends (m : Mode) : stepR m emptyR (.admitTok 7) = ⟨[7], [], 0⟩ := by
  cases m <;> decide

/-- The two-admission history under the three non-reifying disciplines. -/
theorem silent_two : replayR .silent [.admitTok 0, .admitTok 0] = ⟨[0], [], 0⟩ := by decide
theorem meta_two : replayR .metaMarker [.admitTok 0, .marker 0, .admitTok 0] = ⟨[0], [], 0⟩ := by
  decide
theorem fact_two : replayR .fact [.admitTok 0, .admitTok 0] = ⟨[0], [], 1⟩ := by decide

/-- Genesis's marker lemma at a concrete history. -/
theorem marker_dropped :
    replayR .fact ([.admitTok 0, .marker 0].filter fun e => !isMarker e)
      = replayR .fact [.admitTok 0, .marker 0] :=
  markers_invisible .fact _

/-- The carrier bound, chained over two admissions of one token. -/
theorem fact_stays_singleton :
    AtMostTokR 0 (stepR .fact (stepR .fact emptyR (.admitTok 0)) (.admitTok 0)) :=
  nonreify_carrier_bound (Or.inr (Or.inr rfl))
    (nonreify_carrier_bound (Or.inr (Or.inr rfl)) (Or.inl rfl)
      (fun _ h => (REvent.admitTok.inj h).symm))
    (fun _ h => (REvent.admitTok.inj h).symm)

/-- A third admission tags a third index: tags are positions. -/
theorem tagged_three :
    replayR .reifyTagged [.admitTok 0, .admitTok 0, .admitTok 0] = ⟨[0, 0, 0], [1, 2], 0⟩ := by
  decide

/-- Genesis's stepper identity, at a history with two tokens. -/
theorem untagged_is_occurrence_here :
    replayR .reifyUntagged [.admitTok 0, .admitTok 1, .admitTok 0]
      = replayOcc [.admitTok 0, .admitTok 1, .admitTok 0] :=
  reifyUntagged_replay_eq_occurrence _

/-- The swap moves only the tags. -/
theorem swap_fixes_data (s : RState) : (swapState s).data = s.data ∧ (swapState s).refusals = s.refusals :=
  ⟨rfl, rfl⟩

/-- The tagged translation is separable, hence not collapsed. -/
theorem tagged_translation_not_collapsed : ¬ collapsed taggedTranslation 0 1 :=
  separable_not_collapsed tagged_translation_separable

/-- The untagged translation is the bare two-datum regime; the tagged one
is the unary mark on datum 1 with no demand. -/
theorem translations_shape :
    taggedTranslation = ⟨2, [1], [(0, [1])], [], []⟩ ∧
    taggedTranslation.forms.length = 1 ∧ taggedTranslation.insts.length = 1 :=
  ⟨rfl, rfl, rfl⟩

end Textbook.U38

#print axioms Textbook.U38.fresh_appends
#print axioms Textbook.U38.silent_two
#print axioms Textbook.U38.meta_two
#print axioms Textbook.U38.fact_two
#print axioms Textbook.U38.marker_dropped
#print axioms Textbook.U38.fact_stays_singleton
#print axioms Textbook.U38.tagged_three
#print axioms Textbook.U38.untagged_is_occurrence_here
#print axioms Textbook.U38.swap_fixes_data
#print axioms Textbook.U38.tagged_translation_not_collapsed
#print axioms Textbook.U38.translations_shape
#print axioms Refusal.silent_eq_meta
#print axioms Refusal.markers_invisible
#print axioms Refusal.nonreify_carrier_bound
#print axioms Refusal.reifyUntagged_eq_occurrence
#print axioms Refusal.tagged_state_not_swap_invariant
#print axioms Refusal.tagged_translation_separable
"""

EXPECTED = {
    "Textbook.U38.fresh_appends": BOTH,
    "Textbook.U38.silent_two": BOTH,
    "Textbook.U38.meta_two": BOTH,
    "Textbook.U38.fact_two": BOTH,
    "Textbook.U38.marker_dropped": BOTH,
    "Textbook.U38.fact_stays_singleton": BOTH,
    "Textbook.U38.tagged_three": BOTH,
    "Textbook.U38.untagged_is_occurrence_here": BOTH,
    "Textbook.U38.swap_fixes_data": NONE,
    "Textbook.U38.tagged_translation_not_collapsed": BOTH,
    "Textbook.U38.translations_shape": NONE,
    "Refusal.silent_eq_meta": BOTH,
    "Refusal.markers_invisible": BOTH,
    "Refusal.nonreify_carrier_bound": BOTH,
    "Refusal.reifyUntagged_eq_occurrence": BOTH,
    "Refusal.tagged_state_not_swap_invariant": BOTH,
    "Refusal.tagged_translation_separable": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U38"))
