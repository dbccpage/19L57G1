import SecondResponse.Kernel
import SecondResponse.IsoKernel

/-!
# Observation carried along the sealed isomorphism (rung nine's pieces)

RESTATED, not native.  Every declaration below is rung nine's, from its
`SecondProfile/Carry.lean`, unedited but for the outer namespace; the
definition `isoSymm` is rung eight's, as rung nine recorded.  They are
stated and proved again so that this package imports nothing, and the
ledger credits each to its rung.  Rung nine's `separable_iso` and
`collapsed_iso` are not restated: this rung carries exhaustion of a form
along the isomorphism, in `SecondResponse/Exhaust.lean`, and needs only
the pieces.

* `mapCtx σ c`: a context carried along an isomorphism -- its form by
  the form map, each filled slot by the data map, each hole kept a hole.
* `plug_mapCtx`: plugging the image of a datum into a carried context
  gives the carried plugging.
* `wfCtx_mapCtx`: a well-formed context is carried to a well-formed
  context.
* `derivable_mapCtx`: for a well-formed context and an admitted datum,
  the plugging is derivable in the source exactly when the carried
  plugging is derivable in the target.

AuthorityEffect: None.
-/

namespace SecondResponse
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

end Carry
end SecondResponse
