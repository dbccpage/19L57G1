"""Unit 12 check: kernel-check the book's Lean for Unit 12.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u12_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.Inertia
import Derivation.Mention
import Derivation.Minimality

namespace Textbook.U12
open Derivation

/-- Reading L after one more datum: three data, nothing else, one demand. -/
def R3L : Regime := ⟨3, [], [], [], [(0, 1)]⟩

/-- The step the Genesis theorem takes, named. -/
theorem fresh_steps : stepE R2L .admitDatum = some R3L := by decide

/-- It is a real change of state. -/
theorem fresh_is_a_change : R3L ≠ R2L := by decide

/-- The old pair is still collapsed (Unit 10's theorem). -/
theorem old_pair_still_collapsed : collapsed R3L 0 1 :=
  collapsed_of_no_insts _ rfl 0 1

/-- So are the two pairs that involve the new datum: the Genesis theorem
does not state this, but the same lemma gives it. -/
theorem new_pairs_collapsed : collapsed R3L 0 2 ∧ collapsed R3L 1 2 :=
  ⟨collapsed_of_no_insts _ rfl 0 2, collapsed_of_no_insts _ rfl 1 2⟩

/-- R1's hypothesis holds of `R2L` for free: it has no instances. -/
theorem R2L_insts_wf : ∀ p ∈ R2L.insts, ∀ a ∈ p.2, a < R2L.data :=
  fun _ hp => nomatch hp

/-- The same fact by the mention lemma: the fresh datum leaves the collapse
of `(0, 1)` exactly as it was, in both directions. -/
theorem old_pair_via_R1 :
    collapsed { R2L with data := R2L.data + 1 } 0 1 ↔ collapsed R2L 0 1 :=
  collapsed_fresh_datum R2L 0 1 R2L_insts_wf

/-- The record-update form is `R3L` on the nose. -/
theorem R3L_eq : ({ R2L with data := R2L.data + 1 } : Regime) = R3L := rfl

/-- The link regime `BL` with a fresh datum. -/
def BL3 : Regime := { BL with data := BL.data + 1 }

/-- `BL` is well formed in the one respect R1 needs. -/
theorem BL_insts_wf : ∀ p ∈ BL.insts, ∀ a ∈ p.2, a < BL.data := by decide

/-- A separation also survives a fresh datum: `BL3` still tells 0 from 1. -/
theorem BL3_not_collapsed : ¬ collapsed BL3 0 1 :=
  fun h => separable_not_collapsed BL_separable
    ((collapsed_fresh_datum BL 0 1 BL_insts_wf).mp h)

/-- R1 is silent about pairs that include the fresh datum. In `BL3` the
fresh datum 2 is separable from 0: the context "form 0, hole then datum 1"
holds of 0 (the instance (0, [0, 1])) and fails of 2. -/
theorem BL3_sep_02 : separable BL3 0 2 :=
  ⟨⟨0, [none, some 1]⟩, by decide, by decide⟩

/-- A context that names the fresh datum fails on both sides: neither plug
is an instance, and there is no rule. -/
theorem reaching_context_fails_both :
    ¬ derivable BL3 (plug ⟨0, [none, some 2]⟩ 0) ∧
    ¬ derivable BL3 (plug ⟨0, [none, some 2]⟩ 1) := by decide

/-- The hole lemma, re-proved: the plugged datum is among the arguments. -/
theorem mem_plug_of_hole' (c : Ctx) (h : none ∈ c.slots) (d : Nat) :
    d ∈ (plug c d).2 := by
  simp only [plug]
  exact List.mem_map.mpr ⟨none, h, rfl⟩

/-- With one unary form, every well-formed context is its single hole. -/
theorem unary_context_shape (r : Regime) (hforms : r.forms = [1])
    (c : Ctx) (hc : wfCtx r c) : c = ⟨0, [none]⟩ := by
  have hf : c.form = 0 := by
    have h : c.form < 1 := by simpa only [hforms, List.length_cons, List.length_nil] using hc.1
    exact Nat.eq_zero_of_le_zero (Nat.le_of_lt_succ h)
  have hlen : c.slots.length = 1 := by simpa [hforms, hf] using hc.2.1
  cases hs : c.slots with
  | nil => simp [hs] at hlen
  | cons slot rest =>
      cases rest with
      | nil =>
          have hh : none = slot := by simpa [hs] using hc.2.2.1
          have hslots : c.slots = [none] :=
            hs.trans (congrArg (fun s : Option Nat => [s]) hh.symm)
          rcases c with ⟨f, slots⟩
          change f = 0 at hf
          change slots = [none] at hslots
          cases hf
          cases hslots
          rfl
      | cons other tail =>
          have hbad : Nat.succ (Nat.succ tail.length) = Nat.succ 0 := by
            simpa only [hs, List.length_cons] using hlen
          exact False.elim (Nat.noConfusion (Nat.succ.inj hbad))

def bothMarked : Regime := ⟨2, [1], [(0, [0]), (0, [1])], [], []⟩

theorem both_marked_collapsed : collapsed bothMarked 0 1 := by
  intro c hc
  have h := unary_context_shape bothMarked rfl c hc
  subst c
  decide

/-- Preserved old collapse does not mean a preserved class count. -/
theorem fresh_adds_new_distinction :
    collapsed bothMarked 0 1 ∧
    collapsed { bothMarked with data := 3 } 0 1 ∧
    separable { bothMarked with data := 3 } 0 2 := by
  have hwf : ∀ p ∈ bothMarked.insts, ∀ a ∈ p.2, a < bothMarked.data := by decide
  refine ⟨both_marked_collapsed, ?_, ⟨⟨0, [none]⟩, by decide, by decide⟩⟩
  exact (collapsed_fresh_datum bothMarked 0 1 hwf).mpr both_marked_collapsed

def blankThree : Regime := ⟨3, [1], [], [], []⟩

/-- Avoiding just datum 0 does not preserve its comparison with datum 1. -/
theorem avoidance_needs_both_targets :
    0 ∉ ([1] : List Nat) ∧ collapsed blankThree 0 1 ∧
    separable { blankThree with insts := [(0, [1])] } 0 1 :=
  ⟨by decide, collapsed_of_no_insts _ rfl 0 1, ⟨⟨0, [none]⟩, by decide, by decide⟩⟩

theorem avoiding_both_preserves :
    collapsed { blankThree with insts := [(0, [2])] } 0 1 := by
  have h := collapsed_append_unmentioning blankThree [(0, [2])] 0 1
    (by decide) (by decide)
  exact h.mpr (collapsed_of_no_insts _ rfl 0 1)

/-- Reuse an existing positive witness without a negated-collapse converse. -/
theorem separation_preserved_fresh (r : Regime) (d d' : Nat)
    (h : separable r d d') : separable { r with data := r.data + 1 } d d' := by
  obtain ⟨c, hc, hne⟩ := h
  refine ⟨c, ⟨hc.1, hc.2.1, hc.2.2.1, ?_⟩, hne⟩
  intro s hs
  have hold := hc.2.2.2 s hs
  cases s with
  | none => trivial
  | some x => exact Nat.lt_succ_of_lt hold

end Textbook.U12

#print axioms Textbook.U12.fresh_steps
#print axioms Textbook.U12.fresh_is_a_change
#print axioms Textbook.U12.old_pair_still_collapsed
#print axioms Textbook.U12.new_pairs_collapsed
#print axioms Textbook.U12.R2L_insts_wf
#print axioms Textbook.U12.old_pair_via_R1
#print axioms Textbook.U12.R3L_eq
#print axioms Textbook.U12.BL_insts_wf
#print axioms Textbook.U12.BL3_not_collapsed
#print axioms Textbook.U12.BL3_sep_02
#print axioms Textbook.U12.reaching_context_fails_both
#print axioms Textbook.U12.mem_plug_of_hole'
#print axioms Textbook.U12.unary_context_shape
#print axioms Textbook.U12.both_marked_collapsed
#print axioms Textbook.U12.fresh_adds_new_distinction
#print axioms Textbook.U12.avoidance_needs_both_targets
#print axioms Textbook.U12.avoiding_both_preserves
#print axioms Textbook.U12.separation_preserved_fresh
#print axioms Derivation.admission_without_expressive_increase
#print axioms Derivation.collapsed_fresh_datum
#print axioms Derivation.collapsed_append_unmentioning
#print axioms Derivation.mem_plug_of_hole
#print axioms Derivation.exists_out_of_range_slot
#print axioms Derivation.not_mem_of_arg_out_of_range
"""

EXPECTED = {
    "Textbook.U12.fresh_steps": PROPEXT,
    "Textbook.U12.fresh_is_a_change": NONE,
    "Textbook.U12.old_pair_still_collapsed": PROPEXT,
    "Textbook.U12.new_pairs_collapsed": PROPEXT,
    "Textbook.U12.R2L_insts_wf": NONE,
    "Textbook.U12.old_pair_via_R1": BOTH,
    "Textbook.U12.R3L_eq": NONE,
    "Textbook.U12.BL_insts_wf": NONE,
    "Textbook.U12.BL3_not_collapsed": BOTH,
    "Textbook.U12.BL3_sep_02": BOTH,
    "Textbook.U12.reaching_context_fails_both": BOTH,
    "Textbook.U12.mem_plug_of_hole'": BOTH,
    "Textbook.U12.unary_context_shape": PROPEXT,
    "Textbook.U12.both_marked_collapsed": BOTH,
    "Textbook.U12.fresh_adds_new_distinction": BOTH,
    "Textbook.U12.avoidance_needs_both_targets": BOTH,
    "Textbook.U12.avoiding_both_preserves": BOTH,
    "Textbook.U12.separation_preserved_fresh": PROPEXT,
    "Derivation.admission_without_expressive_increase": PROPEXT,
    "Derivation.collapsed_fresh_datum": BOTH,
    "Derivation.collapsed_append_unmentioning": BOTH,
    "Derivation.mem_plug_of_hole": BOTH,
    "Derivation.exists_out_of_range_slot": PROPEXT,
    "Derivation.not_mem_of_arg_out_of_range": NONE,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U12"))
