import SecondProfile.Kernel
import SecondProfile.IsoKernel
import SecondProfile.Carry

/-!
# Holding two, and the observational classes

Native to rung nine.

* `collapsed_refl`, `collapsed_symm`, `collapsed_trans`: collapse is
  reflexive, symmetric and transitive, by unfolding; so the
  observational classes of a regime are classes.
* `HoldsTwo r`: some two admitted data of `r` are separable -- the
  reading of the census row for two-ness this rung declares.
* `Reps r l`: `l` is a REPRESENTATIVE LIST of `r` -- its entries are
  admitted, any two at different positions are separable, and every
  admitted datum is collapsed with some entry.
* `holdsTwo_iso`: a regime holds two exactly when an isomorphic regime
  does, with no hypothesis on either.
* `reps_iso`: a representative list, carried by the data map, is a
  representative list of the target, of the same length, with no
  hypothesis.
* `holdsTwo_of_reps`, `reps_of_no_insts`, `no_twoness_without_insts`:
  a representative list of length at least two witnesses holding two;
  with no instance, the first datum alone represents every admitted
  datum, and no regime holds two.

No statement here counts classes as a NUMBER.  Collapse quantifies over
every context, and no decision procedure for it is built in this run
(rung three's X-1); whether any two representative lists of one regime
have one length is not proved here.

AuthorityEffect: None.
-/

namespace SecondProfile
namespace Classes

open Sealed
open Carry (isoSymm separable_iso collapsed_iso)

/-- Collapse is reflexive. -/
theorem collapsed_refl (r : Regime) (d : Nat) : collapsed r d d :=
  fun _ _ => Iff.rfl

/-- Collapse is symmetric. -/
theorem collapsed_symm {r : Regime} {d d' : Nat} (h : collapsed r d d') :
    collapsed r d' d :=
  fun c hc => (h c hc).symm

/-- Collapse is transitive. -/
theorem collapsed_trans {r : Regime} {d d' d'' : Nat} (h : collapsed r d d')
    (h' : collapsed r d' d'') : collapsed r d d'' :=
  fun c hc => (h c hc).trans (h' c hc)

/-- Some two admitted data are separable. -/
def HoldsTwo (r : Regime) : Prop :=
  ∃ d d', d < r.data ∧ d' < r.data ∧ separable r d d'

/-- A representative list: admitted entries, any two at different
positions separable, every admitted datum collapsed with some entry. -/
def Reps (r : Regime) (l : List Nat) : Prop :=
  (∀ x ∈ l, x < r.data) ∧ l.Pairwise (separable r) ∧
    ∀ d, d < r.data → ∃ x ∈ l, collapsed r d x

/-- A regime holds two exactly when an isomorphic regime does. -/
theorem holdsTwo_iso {r s : Regime} (σ : Iso r s) :
    HoldsTwo r ↔ HoldsTwo s := by
  constructor
  · intro ⟨d, d', hd, hd', h⟩
    exact ⟨σ.dmap d, σ.dmap d', σ.dmap_lt d (List.mem_range.mpr hd),
      σ.dmap_lt d' (List.mem_range.mpr hd'), separable_iso σ hd hd' h⟩
  · intro ⟨d, d', hd, hd', h⟩
    exact ⟨σ.dinv d, σ.dinv d', σ.dinv_lt d (List.mem_range.mpr hd),
      σ.dinv_lt d' (List.mem_range.mpr hd'), separable_iso (isoSymm σ) hd hd' h⟩

/-- A representative list, carried by the data map, is a representative
list of the target, of the same length. -/
theorem reps_iso {r s : Regime} (σ : Iso r s) {l : List Nat} (h : Reps r l) :
    Reps s (l.map σ.dmap) ∧ (l.map σ.dmap).length = l.length := by
  obtain ⟨hlt, hpw, hcov⟩ := h
  refine ⟨⟨?_, ?_, ?_⟩, List.length_map _⟩
  · intro y hy
    obtain ⟨x, hx, hxy⟩ := List.mem_map.mp hy
    rw [← hxy]
    exact σ.dmap_lt x (List.mem_range.mpr (hlt x hx))
  · rw [List.pairwise_map]
    exact hpw.imp_of_mem (fun ha hb hab => separable_iso σ (hlt _ ha) (hlt _ hb) hab)
  · intro d hd
    have hback : σ.dinv d < r.data := σ.dinv_lt d (List.mem_range.mpr hd)
    obtain ⟨x, hx, hcol⟩ := hcov (σ.dinv d) hback
    refine ⟨σ.dmap x, List.mem_map.mpr ⟨x, hx, rfl⟩, ?_⟩
    have h' := collapsed_iso σ hback (hlt x hx) hcol
    rw [σ.dmap_dinv d (List.mem_range.mpr hd)] at h'
    exact h'

/-- A representative list with two entries witnesses holding two. -/
theorem holdsTwo_of_reps {r : Regime} {l : List Nat} (h : Reps r l)
    (hl : 2 ≤ l.length) : HoldsTwo r := by
  obtain ⟨hlt, hpw, _⟩ := h
  match l, hl, hpw with
  | x :: y :: _, _, hpw =>
    exact ⟨x, y, hlt x List.mem_cons_self,
      hlt y (List.mem_cons_of_mem _ List.mem_cons_self),
      List.rel_of_pairwise_cons hpw List.mem_cons_self⟩

/-- With no instance, the first datum alone represents every admitted
datum. -/
theorem reps_of_no_insts {r : Regime} (hi : r.insts = []) (hd : 0 < r.data) :
    Reps r [0] :=
  ⟨fun x hx => by rw [List.mem_singleton.mp hx]; exact hd,
    List.pairwise_singleton _ 0,
    fun d _ => ⟨0, List.mem_singleton_self 0, collapsed_of_no_insts r hi d 0⟩⟩

/-- With no instance, no regime holds two. -/
theorem no_twoness_without_insts {r : Regime} (hi : r.insts = []) :
    ¬ HoldsTwo r := by
  intro ⟨d, d', _, _, h⟩
  exact separable_not_collapsed h (collapsed_of_no_insts r hi d d')

end Classes
end SecondProfile
