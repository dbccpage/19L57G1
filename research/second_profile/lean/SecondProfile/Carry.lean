import SecondProfile.Kernel
import SecondProfile.IsoKernel

/-!
# Observation carried along the sealed isomorphism

Native to rung nine.

The sealed isomorphism structure carries instances and uniform rules as
MEMBERSHIP, forward by the maps and back by their inverses, and keeps the
arity of every admitted form.  A context is a form with slots, and a
plugging fills every hole with one datum; so a context can be carried
along the structure -- its form by the form map, every filled slot by the
data map, every hole kept a hole (`mapCtx`) -- and plugging the image of
an admitted datum into the carried context gives the carried instance
(`plug_mapCtx`).

* `wfCtx_mapCtx`: a well-formed context of the source is carried to a
  well-formed context of the target.
* `derivable_mapCtx`: for a well-formed context and an ADMITTED datum,
  the plugging is derivable in the source exactly when the carried
  plugging is derivable in the target.
* `separable_iso`, `collapsed_iso`: so separability and collapse of two
  admitted data are carried to their images.

No hypothesis is placed on either regime: neither well-formedness nor
the absence of a repeated entry is used.  The only hypothesis is that
the data are admitted in the source, which the sealed structure needs in
order to say anything about them, since its maps are constrained only on
the admitted ranges.

`isoSymm` repeats rung eight's definition, unedited but for the
namespace; it is stated again so that this package imports nothing.

AuthorityEffect: None.
-/

namespace SecondProfile
namespace Carry

open Sealed

/-- The sealed isomorphism with its maps exchanged (rung eight's
definition). -/
def isoSymm {r s : Regime} (σ : Iso r s) : Iso s r where
  dmap := σ.dinv
  dinv := σ.dmap
  fmap := σ.finv
  finv := σ.fmap
  dmap_lt := σ.dinv_lt
  dinv_lt := σ.dmap_lt
  dinv_dmap := σ.dmap_dinv
  dmap_dinv := σ.dinv_dmap
  fmap_lt := σ.finv_lt
  finv_lt := σ.fmap_lt
  finv_fmap := σ.fmap_finv
  fmap_finv := σ.finv_fmap
  arity := fun f hf => by
    have h := σ.arity (σ.finv f) (List.mem_range.mpr (σ.finv_lt f hf))
    rw [σ.fmap_finv f hf] at h
    exact h.symm
  insts_fwd := σ.insts_bwd
  insts_bwd := σ.insts_fwd
  rules_fwd := σ.rules_bwd
  rules_bwd := σ.rules_fwd
  reqs_fwd := σ.reqs_bwd
  reqs_bwd := σ.reqs_fwd

/-- A context carried along an isomorphism: the form by the form map,
each filled slot by the data map, each hole kept a hole. -/
def mapCtx {r s : Regime} (σ : Iso r s) (c : Ctx) : Ctx :=
  ⟨σ.fmap c.form, c.slots.map (Option.map σ.dmap)⟩

/-- A map followed by a left inverse on a list returns the list. -/
theorem map_inv (f g : Nat → Nat) :
    ∀ l : List Nat, (∀ a ∈ l, g (f a) = a) → (l.map f).map g = l := by
  intro l
  induction l with
  | nil => intro _; rfl
  | cons a t ih =>
    intro h
    show g (f a) :: (t.map f).map g = a :: t
    rw [h a List.mem_cons_self, ih (fun x hx => h x (List.mem_cons_of_mem _ hx))]

/-- Plugging the image of a datum into a carried context gives the
carried plugging. -/
theorem plug_mapCtx {r s : Regime} (σ : Iso r s) (c : Ctx) (d : Nat) :
    plug (mapCtx σ c) (σ.dmap d) =
      (σ.fmap c.form, (plug c d).2.map σ.dmap) := by
  show (σ.fmap c.form, (c.slots.map (Option.map σ.dmap)).map
      (fun s => s.getD (σ.dmap d))) =
    (σ.fmap c.form, (c.slots.map (fun s => s.getD d)).map σ.dmap)
  rw [List.map_map, List.map_map]
  congr 1
  apply List.map_congr_left
  intro s _
  cases s <;> rfl

/-- Every argument of the plugging of an admitted datum into a
well-formed context is admitted. -/
theorem plug_args_lt {r : Regime} {c : Ctx} (hc : wfCtx r c) {d : Nat}
    (hd : d < r.data) : ∀ a ∈ (plug c d).2, a < r.data := by
  intro a ha
  obtain ⟨s, hs, hsa⟩ := List.mem_map.mp ha
  cases s with
  | none => rw [← hsa]; exact hd
  | some x =>
    rw [← hsa]
    exact hc.2.2.2 (some x) hs

/-- A well-formed context of the source is carried to a well-formed
context of the target. -/
theorem wfCtx_mapCtx {r s : Regime} (σ : Iso r s) {c : Ctx}
    (hc : wfCtx r c) : wfCtx s (mapCtx σ c) := by
  obtain ⟨hf, hlen, hhole, hslots⟩ := hc
  refine ⟨σ.fmap_lt c.form (List.mem_range.mpr hf), ?_, ?_, ?_⟩
  · show (c.slots.map (Option.map σ.dmap)).length = s.forms.getD (σ.fmap c.form) 0
    rw [List.length_map, σ.arity c.form (List.mem_range.mpr hf)]
    exact hlen
  · exact List.mem_map.mpr ⟨none, hhole, rfl⟩
  · intro t ht
    obtain ⟨u, hu, hut⟩ := List.mem_map.mp ht
    cases u with
    | none => rw [← hut]; trivial
    | some x =>
      rw [← hut]
      exact σ.dmap_lt x (List.mem_range.mpr (hslots (some x) hu))

/-- Derivability is carried forward by the maps. -/
theorem derivable_fwd {r s : Regime} (σ : Iso r s) {i : Inst}
    (h : derivable r i) : derivable s (σ.fmap i.1, i.2.map σ.dmap) := by
  cases h with
  | inl h => exact Or.inl (σ.insts_fwd i h)
  | inr h => exact Or.inr (σ.rules_fwd i.1 h)

/-- Derivability is carried back, for an instance whose form and
arguments are admitted. -/
theorem derivable_bwd {r s : Regime} (σ : Iso r s) {i : Inst}
    (hf : i.1 < r.forms.length) (ha : ∀ a ∈ i.2, a < r.data)
    (h : derivable s (σ.fmap i.1, i.2.map σ.dmap)) : derivable r i := by
  have hff : σ.finv (σ.fmap i.1) = i.1 := σ.finv_fmap i.1 (List.mem_range.mpr hf)
  have hargs : (i.2.map σ.dmap).map σ.dinv = i.2 :=
    map_inv σ.dmap σ.dinv i.2 (fun a h' => σ.dinv_dmap a (List.mem_range.mpr (ha a h')))
  cases h with
  | inl h =>
    have h' := σ.insts_bwd _ h
    simp only at h'
    rw [hff, hargs] at h'
    exact Or.inl h'
  | inr h =>
    have h' := σ.rules_bwd _ h
    rw [hff] at h'
    exact Or.inr h'

/-- For a well-formed context and an admitted datum, the plugging is
derivable in the source exactly when the carried plugging is derivable
in the target. -/
theorem derivable_mapCtx {r s : Regime} (σ : Iso r s) {c : Ctx}
    (hc : wfCtx r c) {d : Nat} (hd : d < r.data) :
    derivable r (plug c d) ↔ derivable s (plug (mapCtx σ c) (σ.dmap d)) := by
  rw [plug_mapCtx]
  constructor
  · intro h
    exact derivable_fwd σ h
  · intro h
    exact derivable_bwd σ hc.1 (plug_args_lt hc hd) h

/-- Separability of two admitted data is carried to their images. -/
theorem separable_iso {r s : Regime} (σ : Iso r s) {d d' : Nat}
    (hd : d < r.data) (hd' : d' < r.data) (h : separable r d d') :
    separable s (σ.dmap d) (σ.dmap d') := by
  obtain ⟨c, hc, hne⟩ := h
  refine ⟨mapCtx σ c, wfCtx_mapCtx σ hc, ?_⟩
  rw [← derivable_mapCtx σ hc hd, ← derivable_mapCtx σ hc hd']
  exact hne

/-- Collapse of two admitted data is carried to their images: every
well-formed context of the target is carried back to one of the
source. -/
theorem collapsed_iso {r s : Regime} (σ : Iso r s) {d d' : Nat}
    (hd : d < r.data) (hd' : d' < r.data) (h : collapsed r d d') :
    collapsed s (σ.dmap d) (σ.dmap d') := by
  intro c hc
  have hx : σ.dmap d < s.data := σ.dmap_lt d (List.mem_range.mpr hd)
  have hx' : σ.dmap d' < s.data := σ.dmap_lt d' (List.mem_range.mpr hd')
  have e1 := derivable_mapCtx (isoSymm σ) hc hx
  have e2 := derivable_mapCtx (isoSymm σ) hc hx'
  have b1 : (isoSymm σ).dmap (σ.dmap d) = d := σ.dinv_dmap d (List.mem_range.mpr hd)
  have b2 : (isoSymm σ).dmap (σ.dmap d') = d' := σ.dinv_dmap d' (List.mem_range.mpr hd')
  rw [b1] at e1
  rw [b2] at e2
  exact e1.trans ((h _ (wfCtx_mapCtx (isoSymm σ) hc)).trans e2.symm)

end Carry
end SecondProfile
