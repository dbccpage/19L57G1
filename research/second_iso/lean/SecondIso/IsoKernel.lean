import SecondIso.Kernel

/-!
# The sealed isomorphism relation and the transport of collapse, reconstructed verbatim

PIN NOTE (whole file).  Every declaration below is reproduced VERBATIM
from two sealed modules at the blobs recorded in `SOURCE_MANIFEST.json`,
at the snapshot recorded there: from `lean4/Derivation/Minimality.lean`,
lines one hundred and sixty-nine through two hundred and twenty-four --
the requirement ordering `sortPair`, the isomorphism structure `Iso`
that mirrors the sealed Python relation, its identity instance `isoRefl`
and the swap of the first two data `swap01`; and from the parked sealed
module `lean4/Derivation/IsoCollapse.lean`, lines thirty-two through one
hundred and seventy-six -- the inverse isomorphism, the image of an
instance and of a context, and the transport of collapse across an
isomorphism.  The only change is the outer namespace, so that this
package stays self-contained and imports nothing sealed.  Doc comments,
section headers and proofs are the sealed ones, unedited.

`verify_pins.py` recomputes the blob hash of each sealed source and each
span at the snapshot and reports drift at HEAD, and
`test_reconstruction.py` compares this file declaration by declaration
with the pinned blobs AT THE SNAPSHOT.

What a pin proves: that the sealed source did not move.  A theorem
reconstructed here is the sealed estate's result, classed RECONSTRUCTION
in the census, and is never counted as this rung's content.  The sealed
module `IsoCollapse` is parked -- not imported by the sealed root -- and
its axioms are audited by the sealed parked-module census; here they are
audited again, by this rung's own fresh build.

AuthorityEffect: None.
-/

namespace SecondIso
namespace Sealed

def sortPair (p : Nat × Nat) : Nat × Nat :=
  if p.1 ≤ p.2 then p else (p.2, p.1)

/-- Isomorphism of regimes: bijections on datum and form indices (given by
two-sided inverses on the admitted ranges) preserving arities, instances,
rules, and requirements.  Mirrors `code/derivation/iso.py`; presentation
tokens are already absent from the Lean model. -/
structure Iso (r s : Regime) where
  dmap : Nat → Nat
  dinv : Nat → Nat
  fmap : Nat → Nat
  finv : Nat → Nat
  dmap_lt : ∀ d ∈ List.range r.data, dmap d < s.data
  dinv_lt : ∀ d ∈ List.range s.data, dinv d < r.data
  dinv_dmap : ∀ d ∈ List.range r.data, dinv (dmap d) = d
  dmap_dinv : ∀ d ∈ List.range s.data, dmap (dinv d) = d
  fmap_lt : ∀ f ∈ List.range r.forms.length, fmap f < s.forms.length
  finv_lt : ∀ f ∈ List.range s.forms.length, finv f < r.forms.length
  finv_fmap : ∀ f ∈ List.range r.forms.length, finv (fmap f) = f
  fmap_finv : ∀ f ∈ List.range s.forms.length, fmap (finv f) = f
  arity : ∀ f ∈ List.range r.forms.length,
      s.forms.getD (fmap f) 0 = r.forms.getD f 0
  insts_fwd : ∀ p ∈ r.insts, (fmap p.1, p.2.map dmap) ∈ s.insts
  insts_bwd : ∀ p ∈ s.insts, (finv p.1, p.2.map dinv) ∈ r.insts
  rules_fwd : ∀ f ∈ r.rules, fmap f ∈ s.rules
  rules_bwd : ∀ f ∈ s.rules, finv f ∈ r.rules
  reqs_fwd : ∀ q ∈ r.reqs, sortPair (dmap q.1, dmap q.2) ∈ s.reqs
  reqs_bwd : ∀ q ∈ s.reqs, sortPair (dinv q.1, dinv q.2) ∈ r.reqs

/-- Every regime with sorted requirement pairs is isomorphic to itself. -/
def isoRefl (r : Regime) (hreqs : ∀ q ∈ r.reqs, q.1 ≤ q.2) : Iso r r where
  dmap := id
  dinv := id
  fmap := id
  finv := id
  dmap_lt := fun d hd => List.mem_range.mp hd
  dinv_lt := fun d hd => List.mem_range.mp hd
  dinv_dmap := fun _ _ => rfl
  dmap_dinv := fun _ _ => rfl
  fmap_lt := fun f hf => List.mem_range.mp hf
  finv_lt := fun f hf => List.mem_range.mp hf
  finv_fmap := fun _ _ => rfl
  fmap_finv := fun _ _ => rfl
  arity := fun _ _ => rfl
  insts_fwd := fun p hp => by simpa [List.map_id] using hp
  insts_bwd := fun p hp => by simpa [List.map_id] using hp
  rules_fwd := fun _ hf => hf
  rules_bwd := fun _ hf => hf
  reqs_fwd := fun q hq => by
    simpa [sortPair, hreqs q hq] using hq
  reqs_bwd := fun q hq => by
    simpa [sortPair, hreqs q hq] using hq

/-- The swap of the two data. -/
def swap01 (d : Nat) : Nat :=
  if d = 0 then 1 else if d = 1 then 0 else d

/-- A list is fixed by a map that fixes each of its members. -/
theorem map_eq_self_of_mem {l : List Nat} {f : Nat → Nat}
    (hf : ∀ a ∈ l, f a = a) : l.map f = l := by
  induction l with
  | nil => rfl
  | cons a as ih =>
    simp only [List.map_cons]
    rw [hf a (List.mem_cons.mpr (Or.inl rfl)),
        ih (fun x hx => hf x (List.mem_cons.mpr (Or.inr hx)))]

/-- Every datum plugged into a well-formed context is admitted, provided the
plugged datum is. -/
theorem plug_args_lt {r : Regime} {c : Ctx} (hc : wfCtx r c)
    {d : Nat} (hd : d < r.data) : ∀ a ∈ (plug c d).2, a < r.data := by
  intro a ha
  obtain ⟨sl, hsl, hsle⟩ := List.mem_map.mp ha
  have h4 := hc.2.2.2 sl hsl
  cases sl with
  | none => exact hsle ▸ hd
  | some x => exact hsle ▸ h4

namespace Iso

variable {r s : Regime}

/-- The inverse isomorphism: swap the two half-bijections and the forward and
backward membership conditions.  Only `arity` needs a computation. -/
def symm (h : Iso r s) : Iso s r where
  dmap := h.dinv
  dinv := h.dmap
  fmap := h.finv
  finv := h.fmap
  dmap_lt := h.dinv_lt
  dinv_lt := h.dmap_lt
  dinv_dmap := h.dmap_dinv
  dmap_dinv := h.dinv_dmap
  fmap_lt := h.finv_lt
  finv_lt := h.fmap_lt
  finv_fmap := h.fmap_finv
  fmap_finv := h.finv_fmap
  arity := by
    intro f hf
    have hfr : h.finv f < r.forms.length := h.finv_lt f hf
    have hkey := h.arity (h.finv f) (List.mem_range.mpr hfr)
    rw [h.fmap_finv f hf] at hkey
    exact hkey.symm
  insts_fwd := h.insts_bwd
  insts_bwd := h.insts_fwd
  rules_fwd := h.rules_bwd
  rules_bwd := h.rules_fwd
  reqs_fwd := h.reqs_bwd
  reqs_bwd := h.reqs_fwd

@[simp] theorem symm_dmap (h : Iso r s) : h.symm.dmap = h.dinv := rfl

/-- The image of an instance under the isomorphism's maps. -/
def imap (h : Iso r s) (i : Inst) : Inst := (h.fmap i.1, i.2.map h.dmap)

/-- The image of a context: form index by `fmap`, filled slots by `dmap`. -/
def cmap (h : Iso r s) (c : Ctx) : Ctx :=
  ⟨h.fmap c.form, c.slots.map (Option.map h.dmap)⟩

/-- Plugging commutes with the context/instance image. -/
theorem plug_cmap (h : Iso r s) (c : Ctx) (d : Nat) :
    plug (h.cmap c) (h.dmap d) = h.imap (plug c d) := by
  have hfun : (fun sl : Option Nat => Option.getD (Option.map h.dmap sl) (h.dmap d))
            = (fun sl : Option Nat => h.dmap (Option.getD sl d)) := by
    funext sl; cases sl <;> rfl
  simp only [plug, Iso.cmap, Iso.imap, List.map_map]
  congr 1
  show List.map ((fun sl => Option.getD sl (h.dmap d)) ∘ Option.map h.dmap) c.slots
     = List.map (h.dmap ∘ (fun sl => Option.getD sl d)) c.slots
  exact congrArg (fun g => List.map g c.slots) hfun

/-- Well-formed contexts map forward under the isomorphism. -/
theorem wfCtx_cmap (h : Iso r s) {c : Ctx} (hc : wfCtx r c) :
    wfCtx s (h.cmap c) := by
  obtain ⟨h1, h2, h3, h4⟩ := hc
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact h.fmap_lt c.form (List.mem_range.mpr h1)
  · show (c.slots.map (Option.map h.dmap)).length = s.forms.getD (h.fmap c.form) 0
    rw [List.length_map, h2, h.arity c.form (List.mem_range.mpr h1)]
  · show none ∈ c.slots.map (Option.map h.dmap)
    exact List.mem_map.mpr ⟨none, h3, rfl⟩
  · intro sl hsl
    obtain ⟨t, ht, hte⟩ := List.mem_map.mp hsl
    have h4t := h4 t ht
    cases t with
    | none => exact hte ▸ trivial
    | some x => exact hte ▸ h.dmap_lt x (List.mem_range.mpr h4t)

/-- Derivability transports across the isomorphism, on an instance whose form
index and data are admitted. -/
theorem derivable_imap (h : Iso r s) {i : Inst}
    (hf : i.1 < r.forms.length) (ha : ∀ a ∈ i.2, a < r.data) :
    derivable s (h.imap i) ↔ derivable r i := by
  constructor
  · intro hd
    cases hd with
    | inl hm =>
      have hb := h.insts_bwd (h.imap i) hm
      have e1 : h.finv (h.imap i).1 = i.1 := h.finv_fmap i.1 (List.mem_range.mpr hf)
      have e2 : (h.imap i).2.map h.dinv = i.2 := by
        show (i.2.map h.dmap).map h.dinv = i.2
        rw [List.map_map]
        exact map_eq_self_of_mem
          (fun a ha' => h.dinv_dmap a (List.mem_range.mpr (ha a ha')))
      rw [e1, e2] at hb
      exact Or.inl hb
    | inr hr =>
      have hb := h.rules_bwd (h.fmap i.1) hr
      rw [h.finv_fmap i.1 (List.mem_range.mpr hf)] at hb
      exact Or.inr hb
  · intro hd
    cases hd with
    | inl hm => exact Or.inl (h.insts_fwd i hm)
    | inr hr => exact Or.inr (h.rules_fwd i.1 hr)

/-- **Collapse maps forward** across the isomorphism, datum pair by `dmap`. -/
theorem collapsed_fwd (h : Iso r s) {d d' : Nat}
    (hd : d < r.data) (hd' : d' < r.data)
    (H : collapsed s (h.dmap d) (h.dmap d')) : collapsed r d d' := by
  intro c hc
  have hh := H (h.cmap c) (h.wfCtx_cmap hc)
  rw [h.plug_cmap, h.plug_cmap,
      h.derivable_imap (i := plug c d) hc.1 (plug_args_lt hc hd),
      h.derivable_imap (i := plug c d') hc.1 (plug_args_lt hc hd')] at hh
  exact hh

/-- **Collapse transports across a regime isomorphism.**  The datum pair is
carried by the isomorphism's datum bijection; forms, rules, and instances are
handled by its membership fields, and requirements never enter collapse. -/
theorem collapsed_transport (h : Iso r s) {d d' : Nat}
    (hd : d < r.data) (hd' : d' < r.data) :
    collapsed s (h.dmap d) (h.dmap d') ↔ collapsed r d d' := by
  constructor
  · exact h.collapsed_fwd hd hd'
  · intro Hr
    have key := h.symm.collapsed_fwd (d := h.dmap d) (d' := h.dmap d')
      (h.dmap_lt d (List.mem_range.mpr hd)) (h.dmap_lt d' (List.mem_range.mpr hd'))
    rw [symm_dmap, h.dinv_dmap d (List.mem_range.mpr hd),
        h.dinv_dmap d' (List.mem_range.mpr hd')] at key
    exact key Hr

end Iso

end Sealed
end SecondIso
