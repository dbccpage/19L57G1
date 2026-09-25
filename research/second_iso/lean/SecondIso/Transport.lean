import SecondIso.IsoKernel
import SecondIso.IndexSlice

/-!
# A demand transported across the implemented isomorphism

This file is this rung's own object.  What it consumes is the
reconstruction in `Kernel.lean`, `IsoKernel.lean`, `Inherited.lean` and
`IndexSlice.lean`, each carrying its own pin note; nothing in this file is
reconstructed.

The sealed estate transports COLLAPSE across its isomorphism
(`collapsed_transport`, reconstructed).  A demand reads collapse and
SEPARABILITY, and separability is an existential over contexts, so it is
not the negation of collapse unless collapse is decided -- which this
rung does not do.  So separability is transported here in its own right,
by carrying the witnessing context through the isomorphism's context
image, exactly as the sealed module carries every context for collapse.

A demand also reads the STAKE, and a stake labels datum indices.  The
isomorphism moves datum indices.  So a demand is carried to a demand only
when the stake gives each moved pair the label it gave the pair; under a
UNIFORM stake -- one label on every pair of distinct indices -- that
always holds, and carrying a demand is invariant under the isomorphism.
Whether anything weaker than uniformity suffices is NOT decided here and
stays a named leftover.

Every statement below is about the sealed grammar reconstructed in this
package, extended by a declared two-sided stake, and about no other
grammar.

AuthorityEffect: None.
-/

namespace SecondIso
namespace Transport

open SecondIso.Sealed
open SecondIso.Inherited
open SecondIso.IndexSlice

/-! ## 1. Symmetry of the two readings a label is honoured by -/

/-- **separable_symm.**  Separability does not depend on the order of the
pair.  AT THE LEVEL OF A DEFINITION: the witnessing context serves both
orders, with the negated equivalence turned round. -/
theorem separable_symm {r : Regime} {d d' : Nat} :
    separable r d d' ↔ separable r d' d := by
  constructor
  · intro ⟨c, hc, hne⟩
    exact ⟨c, hc, fun h => hne h.symm⟩
  · intro ⟨c, hc, hne⟩
    exact ⟨c, hc, fun h => hne h.symm⟩

/-- **collapsed_symm.**  Collapse does not depend on the order of the pair.
AT THE LEVEL OF A DEFINITION: each context's equivalence, turned round. -/
theorem collapsed_symm {r : Regime} {d d' : Nat} :
    collapsed r d d' ↔ collapsed r d' d :=
  ⟨fun h c hc => (h c hc).symm, fun h c hc => (h c hc).symm⟩

/-- **honour_symm.**  Honour of a label by a regime does not depend on the
order of the pair, for each of the three labels. -/
theorem honour_symm (r : Regime) (l : Label) (i j : Nat) :
    honour r l i j ↔ honour r l j i := by
  cases l with
  | apart => exact separable_symm
  | same => exact collapsed_symm
  | free => exact Iff.rfl

/-! ## 2. The datum bijection, and separability carried through it -/

/-- **dmap_inj.**  The datum map of an isomorphism is injective on the
admitted data: it has a left inverse there. -/
theorem dmap_inj {r s : Regime} (h : Iso r s) {a b : Nat}
    (ha : a < r.data) (hb : b < r.data) (heq : h.dmap a = h.dmap b) :
    a = b :=
  calc a = h.dinv (h.dmap a) := (h.dinv_dmap a (List.mem_range.mpr ha)).symm
    _ = h.dinv (h.dmap b) := by rw [heq]
    _ = b := h.dinv_dmap b (List.mem_range.mpr hb)

/-- **separable_fwd.**  Separability of two admitted data maps forward
across an isomorphism.  The witnessing context is carried by the
isomorphism's context image, which the sealed module proves well formed
and plugging-compatible; no decision of collapse is made. -/
theorem separable_fwd {r s : Regime} (h : Iso r s) {d d' : Nat}
    (hd : d < r.data) (hd' : d' < r.data) (H : separable r d d') :
    separable s (h.dmap d) (h.dmap d') := by
  obtain ⟨c, hc, hne⟩ := H
  refine ⟨h.cmap c, h.wfCtx_cmap hc, ?_⟩
  rw [h.plug_cmap, h.plug_cmap,
      h.derivable_imap (i := plug c d) hc.1 (plug_args_lt hc hd),
      h.derivable_imap (i := plug c d') hc.1 (plug_args_lt hc hd')]
  exact hne

/-- **separable_transport.**  Separability transports across an
isomorphism in both directions: the backward direction is the forward
direction of the sealed inverse isomorphism. -/
theorem separable_transport {r s : Regime} (h : Iso r s) {d d' : Nat}
    (hd : d < r.data) (hd' : d' < r.data) :
    separable s (h.dmap d) (h.dmap d') ↔ separable r d d' := by
  constructor
  · intro Hs
    have key := separable_fwd h.symm (d := h.dmap d) (d' := h.dmap d')
      (h.dmap_lt d (List.mem_range.mpr hd)) (h.dmap_lt d' (List.mem_range.mpr hd')) Hs
    rw [Iso.symm_dmap, h.dinv_dmap d (List.mem_range.mpr hd),
        h.dinv_dmap d' (List.mem_range.mpr hd')] at key
    exact key
  · exact separable_fwd h hd hd'

/-- **honour_transport.**  Honour of any one label transports across an
isomorphism, the pair carried by the datum bijection. -/
theorem honour_transport {r s : Regime} (h : Iso r s) (l : Label) {i j : Nat}
    (hi : i < r.data) (hj : j < r.data) :
    honour s l (h.dmap i) (h.dmap j) ↔ honour r l i j := by
  cases l with
  | apart => exact separable_transport h hi hj
  | same => exact h.collapsed_transport hi hj
  | free => exact Iff.rfl

/-! ## 3. Stakes whose labels the isomorphism does not move -/

/-- A stake is UNIFORM when it gives one and the same label to every pair
of distinct indices. -/
def Uniform (S : Stake) : Prop :=
  ∃ l, ∀ i j, i ≠ j → S.label i j = l

/-- An isomorphism PRESERVES the labels of a stake when every held pair,
carried by the datum bijection and put in order, keeps its label. -/
def LabelPreserved (S : Stake) {r s : Regime} (h : Iso r s) : Prop :=
  ∀ i j, i < j → j < r.data →
    (h.dmap i < h.dmap j → S.label (h.dmap i) (h.dmap j) = S.label i j) ∧
    (h.dmap j < h.dmap i → S.label (h.dmap j) (h.dmap i) = S.label i j)

/-- **uniform_freeStake.**  AT THE LEVEL OF A DEFINITION. -/
theorem uniform_freeStake : Uniform freeStake :=
  ⟨Label.free, fun _ _ _ => rfl⟩

/-- **uniform_allApart.**  AT THE LEVEL OF A DEFINITION: one rewrite of
the conditional. -/
theorem uniform_allApart : Uniform allApart :=
  ⟨Label.apart, fun i j hij => by
    show (if i = j then Label.free else Label.apart) = Label.apart
    rw [if_neg hij]⟩

/-- **uniform_allSame.**  AT THE LEVEL OF A DEFINITION: one rewrite of
the conditional. -/
theorem uniform_allSame : Uniform allSame :=
  ⟨Label.same, fun i j hij => by
    show (if i = j then Label.free else Label.same) = Label.same
    rw [if_neg hij]⟩

/-- **uniform_preserved.**  Every isomorphism preserves the labels of a
uniform stake: a held pair and its image are both pairs of distinct
indices, so both carry the one label. -/
theorem uniform_preserved {S : Stake} (hu : Uniform S) {r s : Regime}
    (h : Iso r s) : LabelPreserved S h := by
  obtain ⟨l, hl⟩ := hu
  intro i j hij _
  refine ⟨fun hlt => ?_, fun hgt => ?_⟩
  · rw [hl _ _ (Nat.ne_of_lt hlt), hl i j (Nat.ne_of_lt hij)]
  · rw [hl _ _ (Nat.ne_of_lt hgt), hl i j (Nat.ne_of_lt hij)]

/-! ## 4. A demand carried across the isomorphism -/

/-- **demand_transport.**  In the sealed grammar reconstructed here,
extended by a declared two-sided stake: a demand at a regime is carried
to a demand at any isomorphic regime, whenever the isomorphism preserves
the stake's labels.  The image pair is the pair the datum bijection gives,
put in order; honour is transported label by label, and the order is
repaired by the symmetry of honour. -/
theorem demand_transport (S : Stake) {r s : Regime} (h : Iso r s)
    (hp : LabelPreserved S h) {i j : Nat} (hd : Demand S r i j) :
    ∃ i' j', Demand S s i' j' := by
  obtain ⟨hij, hj, hlab, hno⟩ := hd
  have hi : i < r.data := Nat.lt_trans hij hj
  have hne : h.dmap i ≠ h.dmap j := fun e => by
    have := dmap_inj h hi hj e
    omega
  have hsi := h.dmap_lt i (List.mem_range.mpr hi)
  have hsj := h.dmap_lt j (List.mem_range.mpr hj)
  rcases Nat.lt_or_gt_of_ne hne with hlt | hgt
  · refine ⟨h.dmap i, h.dmap j, hlt, hsj, ?_, ?_⟩
    · rw [(hp i j hij hj).1 hlt]
      exact hlab
    · rw [(hp i j hij hj).1 hlt, honour_transport h _ hi hj]
      exact hno
  · refine ⟨h.dmap j, h.dmap i, hgt, hsi, ?_, ?_⟩
    · rw [(hp i j hij hj).2 hgt]
      exact hlab
    · rw [(hp i j hij hj).2 hgt, honour_symm, honour_transport h _ hi hj]
      exact hno

/-- **hasDemand_transport_of_uniform.**  Under a uniform stake, carrying a
demand maps forward across any isomorphism. -/
theorem hasDemand_transport_of_uniform {S : Stake} (hu : Uniform S)
    {r s : Regime} (h : Iso r s) (hd : HasDemand S r) : HasDemand S s := by
  obtain ⟨i, j, hdem⟩ := hd
  exact demand_transport S h (uniform_preserved hu h) hdem

/-- **hasDemand_iff_of_uniform.**  In the sealed grammar reconstructed
here, extended by a declared two-sided stake that is uniform: two regimes
the isomorphism relates both carry a demand or both carry none, whether
or not either is reachable.  No decidability hypothesis. -/
theorem hasDemand_iff_of_uniform {S : Stake} (hu : Uniform S)
    {r s : Regime} (h : Iso r s) : HasDemand S r ↔ HasDemand S s :=
  ⟨hasDemand_transport_of_uniform hu h, hasDemand_transport_of_uniform hu h.symm⟩

end Transport
end SecondIso
