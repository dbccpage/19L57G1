"""Unit 52 check: kernel-check the book's Lean for Unit 52.

Lean (book): not part of Genesis's build, axiom report or gates. Run from
the repository root after `lake build` in lean4/:

    python textbook/checks/u52_lean.py

AuthorityEffect: None.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402

LEAN_SOURCE = """\
import Derivation.PrimitiveCats

namespace Textbook.U52
open PrimitiveCats

/-- The one-point self-witness as an object: it receives the unique map
out of `d2Obj` like every object, and that map collapses the two points. -/
def unitObj : PtdRel := ⟨Unit, fun _ _ => True, (), (), trivial⟩

theorem unit_receives_one : ∃ h : Hom d2Obj unitObj, ∀ h' : Hom d2Obj unitObj, h' = h :=
  d2_initial unitObj

theorem unit_collapses (h : Hom d2Obj unitObj) : h.f false = h.f true := rfl

/-- Initiality gives one map into `s2Obj` too: the oriented object maps
into the symmetric one. The other direction has no map at all. -/
theorem d2_to_s2 : ∃ h : Hom d2Obj s2Obj, ∀ h' : Hom d2Obj s2Obj, h' = h :=
  d2_initial s2Obj

theorem s2_to_d2_none : ¬ Nonempty (Hom s2Obj d2Obj) := s2_no_hom_to_d2

/-- `s2_initial_sym` needs its hypothesis: without it `s2Obj` is not initial. -/
theorem s2_not_initial_full : ¬ ∀ T : PtdRel, ∃ h : Hom s2Obj T, ∀ h' : Hom s2Obj T, h' = h :=
  fun h => s2_not_initial h

/-- The audit's probe: `wideObj 0` lives on `Fin 2` and IS initial, so
"every one of them admits two distinct morphisms out" does not cover n = 0. -/
theorem wideObj0_initial : Initial (wideObj 0) := by
  intro T
  refine ⟨⟨fun t => if t.val = 0 then T.a else T.b, rfl, rfl, ?_⟩, ?_⟩
  · intro x y hxy
    have hx : x = ⟨0, by omega⟩ := hxy.1
    have hy : y = ⟨1, by omega⟩ := hxy.2
    subst hx; subst hy
    exact T.w
  · intro h'
    apply hom_ext
    funext t
    match t with
    | ⟨0, _⟩ => exact h'.ha
    | ⟨1, _⟩ => exact h'.hb

/-- The two maps out of the three-point object, read at the free point. -/
theorem big0_free_point :
    (bigHomA 0).f ⟨2, by omega⟩ = false ∧ (bigHomB 0).f ⟨2, by omega⟩ = true :=
  ⟨rfl, rfl⟩

theorem big0_not_initial : ¬ Initial (bigObj 0) := larger_not_initial 0

/-- The explicit isomorphism between the two initial presentations: the swap. -/
def toSwap : Hom d2Obj d2SwapObj :=
  ⟨Bool.not, rfl, rfl, fun x y h => ⟨by rw [h.1]; rfl, by rw [h.2]; rfl⟩⟩

def fromSwap : Hom d2SwapObj d2Obj :=
  ⟨Bool.not, rfl, rfl, fun x y h => ⟨by rw [h.1]; rfl, by rw [h.2]; rfl⟩⟩

theorem swap_iso : comp fromSwap toSwap = idH d2Obj ∧ comp toSwap fromSwap = idH d2SwapObj := by
  refine ⟨hom_ext ?_, hom_ext ?_⟩ <;> funext t <;> cases t <;> rfl

theorem swap_iso_by_initiality :
    ∃ (u : Hom d2Obj d2SwapObj) (v : Hom d2SwapObj d2Obj),
      comp v u = idH d2Obj ∧ comp u v = idH d2SwapObj :=
  initials_iso _ _ d2_initial d2Swap_initial

/-- Unpointed: both the identity and the swap are automorphisms of `S2`;
pointed: every endomorphism of either object fixes both points. -/
theorem s2_two_unpointed : IsRelAuto PrimDiff.S2 id ∧ IsRelAuto PrimDiff.S2 Bool.not :=
  ⟨⟨⟨fun _ _ h => h, fun z => ⟨z, rfl⟩⟩, s2_id_auto⟩, s2_swap_isRelAuto⟩

theorem pointed_fixes (h : Hom s2Obj s2Obj) : h.f false = false ∧ h.f true = true :=
  pointed_rigid.2 h

/-- The two cuts, written out, and the identity presentation's map into each. -/
theorem cuts_values :
    mergeA.q 0 = false ∧ mergeA.q 1 = true ∧ mergeA.q 2 = false ∧
    mergeB.q 0 = true ∧ mergeB.q 1 = false ∧ mergeB.q 2 = false :=
  ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

theorem id3_to_cuts :
    (∃ u : PHom idPres3 mergeA, ∀ v, v = u) ∧ (∃ u : PHom idPres3 mergeB, ∀ v, v = u) :=
  ⟨pres_initial mergeA, pres_initial mergeB⟩

theorem cuts_incomparable : ¬ Nonempty (PHom mergeA mergeB) ∧ ¬ Nonempty (PHom mergeB mergeA) :=
  ⟨no_phom_mergeA_mergeB, no_phom_mergeB_mergeA⟩

/-- The free point of `freePres2` can go either way: two commuting maps
into the identity presentation, differing at index 2. -/
def free0 : PHom2 freePres2 idPres2 := ⟨fun z => z.val == 1, by intro x; cases x <;> rfl⟩
def free1 : PHom2 freePres2 idPres2 := ⟨fun z => !(z.val == 0), by intro x; cases x <;> rfl⟩

theorem free_maps_differ : free0 ≠ free1 := by
  intro h
  have h2 := congrArg (fun u : PHom2 freePres2 idPres2 => u.h ⟨2, by omega⟩) h
  exact Bool.noConfusion h2

theorem freePres2_not_epi : ¬ Epi2 freePres2 := by
  intro h
  obtain ⟨x, hx⟩ := h ⟨2, by omega⟩
  cases x <;> exact absurd (congrArg Fin.val hx) (by decide)

/-- Against a surjective presentation the maps into `idPres2` agree. -/
theorem swap_maps_agree (u v : PHom2 swapPres2 idPres2) : u = v :=
  phom2_unique_of_epi _ swapPres2_epi u v

/-- The symmetric source needs a reverse edge at the designated pair,
not symmetry of every target edge. -/
theorem symmetric_source_map_iff (T : PtdRel) :
    Nonempty (Hom s2Obj T) ↔ T.r T.b T.a := by
  constructor
  · rintro ⟨h⟩
    have hr := h.hr true false (Or.inr PrimDiff.D2_witness)
    have ha : h.f false = T.a := h.ha
    have hb : h.f true = T.b := h.hb
    simpa only [ha, hb] using hr
  · intro hreverse
    refine ⟨⟨fun t => cond t T.b T.a, rfl, rfl, ?_⟩⟩
    intro x y hxy
    cases hxy with
    | inl h =>
      rcases h with ⟨hx, hy⟩
      subst hx; subst hy
      exact T.w
    | inr h =>
      rcases h with ⟨hy, hx⟩
      subst hx; subst hy
      exact hreverse

def localSymTarget : PtdRel :=
  ⟨Fin 3, fun x y => (x = 0 ∧ y = 1) ∨ (x = 1 ∧ y = 0) ∨ (x = 1 ∧ y = 2),
   0, 1, Or.inl ⟨rfl, rfl⟩⟩

theorem global_symmetry_not_required :
    Nonempty (Hom s2Obj localSymTarget) ∧ ¬ SymObj localSymTarget := by
  constructor
  · exact (symmetric_source_map_iff _).mpr (Or.inr (Or.inl ⟨rfl, rfl⟩))
  · intro h
    have hr := h (1 : Fin 3) (2 : Fin 3) (Or.inr (Or.inr ⟨rfl, rfl⟩))
    have hn : ¬ localSymTarget.r (2 : Fin 3) (1 : Fin 3) := by simp [localSymTarget]
    exact hn hr

end Textbook.U52

#print axioms Textbook.U52.unit_receives_one
#print axioms Textbook.U52.unit_collapses
#print axioms Textbook.U52.d2_to_s2
#print axioms Textbook.U52.s2_to_d2_none
#print axioms Textbook.U52.s2_not_initial_full
#print axioms Textbook.U52.wideObj0_initial
#print axioms Textbook.U52.big0_free_point
#print axioms Textbook.U52.big0_not_initial
#print axioms Textbook.U52.swap_iso
#print axioms Textbook.U52.swap_iso_by_initiality
#print axioms Textbook.U52.s2_two_unpointed
#print axioms Textbook.U52.pointed_fixes
#print axioms Textbook.U52.cuts_values
#print axioms Textbook.U52.id3_to_cuts
#print axioms Textbook.U52.cuts_incomparable
#print axioms Textbook.U52.free_maps_differ
#print axioms Textbook.U52.freePres2_not_epi
#print axioms Textbook.U52.swap_maps_agree
#print axioms Textbook.U52.symmetric_source_map_iff
#print axioms Textbook.U52.global_symmetry_not_required
#print axioms PrimitiveCats.d2_initial
#print axioms PrimitiveCats.d2_initial_irrefl
#print axioms PrimitiveCats.d2_map_injective
#print axioms PrimitiveCats.d2_map_not_injective_without_irrefl
#print axioms PrimitiveCats.s2_initial_sym
#print axioms PrimitiveCats.s2_no_hom_to_d2
#print axioms PrimitiveCats.s2_not_weakly_initial
#print axioms PrimitiveCats.d2Swap_initial
#print axioms PrimitiveCats.two_initials_not_identical
#print axioms PrimitiveCats.initials_iso
#print axioms PrimitiveCats.ptd_on_every_larger_carrier
#print axioms PrimitiveCats.larger_not_initial
#print axioms PrimitiveCats.pointed_rigid
#print axioms PrimitiveCats.s2_swap_isRelAuto
#print axioms PrimitiveCats.pres_initial
#print axioms PrimitiveCats.no_phom_mergeA_mergeB
#print axioms PrimitiveCats.no_terminal_pres
#print axioms PrimitiveCats.phom2_unique_of_epi
#print axioms PrimitiveCats.no_terminal_pres2
"""

EXPECTED = {
    "Textbook.U52.unit_receives_one": QUOT,
    "Textbook.U52.symmetric_source_map_iff": NONE,
    "Textbook.U52.global_symmetry_not_required": PROPEXT,
    "Textbook.U52.unit_collapses": NONE,
    "Textbook.U52.d2_to_s2": QUOT,
    "Textbook.U52.s2_to_d2_none": NONE,
    "Textbook.U52.s2_not_initial_full": NONE,
    "Textbook.U52.wideObj0_initial": BOTH,
    "Textbook.U52.big0_free_point": BOTH,
    "Textbook.U52.big0_not_initial": BOTH,
    "Textbook.U52.swap_iso": QUOT,
    "Textbook.U52.swap_iso_by_initiality": QUOT,
    "Textbook.U52.s2_two_unpointed": NONE,
    "Textbook.U52.pointed_fixes": NONE,
    "Textbook.U52.cuts_values": PROPEXT,
    "Textbook.U52.id3_to_cuts": BOTH,
    "Textbook.U52.cuts_incomparable": PROPEXT,
    "Textbook.U52.free_maps_differ": BOTH,
    "Textbook.U52.freePres2_not_epi": BOTH,
    "Textbook.U52.swap_maps_agree": QUOT,
    "PrimitiveCats.d2_initial": QUOT,
    "PrimitiveCats.d2_initial_irrefl": QUOT,
    "PrimitiveCats.d2_map_injective": NONE,
    "PrimitiveCats.d2_map_not_injective_without_irrefl": NONE,
    "PrimitiveCats.s2_initial_sym": QUOT,
    "PrimitiveCats.s2_no_hom_to_d2": NONE,
    "PrimitiveCats.s2_not_weakly_initial": NONE,
    "PrimitiveCats.d2Swap_initial": QUOT,
    "PrimitiveCats.two_initials_not_identical": NONE,
    "PrimitiveCats.initials_iso": NONE,
    "PrimitiveCats.ptd_on_every_larger_carrier": BOTH,
    "PrimitiveCats.larger_not_initial": BOTH,
    "PrimitiveCats.pointed_rigid": NONE,
    "PrimitiveCats.s2_swap_isRelAuto": NONE,
    "PrimitiveCats.pres_initial": BOTH,
    "PrimitiveCats.no_phom_mergeA_mergeB": PROPEXT,
    "PrimitiveCats.no_terminal_pres": PROPEXT,
    "PrimitiveCats.phom2_unique_of_epi": QUOT,
    "PrimitiveCats.no_terminal_pres2": BOTH,
}

if __name__ == "__main__":
    raise SystemExit(main(LEAN_SOURCE, EXPECTED, "U52"))
