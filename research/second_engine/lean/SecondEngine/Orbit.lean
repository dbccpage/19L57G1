import SecondEngine.Kernel
import SecondEngine.IsoKernel
import SecondEngine.Carry

/-!
# Orbits, requirements and collapse carried along the sealed isomorphism

Native to continuation one.

Rung two, track two, named three observables that its stake rules read
and that this tree mirrors in Lean: O-one, whether two data have equal
sealed profiles (here: `collapsed`, and its negation `separable`); O-four,
whether some automorphism carries one datum to the other (`OneOrbit`);
and O-six, whether the sorted pair is a requirement (`ReqMember`).  Rung
two left the invariance of the rules reading O-four OPEN: it computed the
source values but did not replay the labels on renamed regimes.  This
module proves that each of the three observables is carried, forward and
back, by every inhabitant of the sealed isomorphism, for every pair of
regimes, with the only hypothesis that the two data are admitted in the
source.

* `isoTrans σ τ`: the composite of two inhabitants of the sealed
  isomorphism, its maps composed.
* `oneOrbit_iso`: two data lie in one orbit exactly when their images do.
  The automorphism of the target is the source's conjugated by `σ`.
* `reqMember_iso`: the sorted pair is a requirement exactly when the
  sorted pair of the images is.
* `separable_iso_iff`, `collapsed_iso_iff`: rung nine's forward carrying,
  made an equivalence along `isoSymm`.

No hypothesis is placed on either regime.

AuthorityEffect: None.
-/

namespace SecondEngine
namespace Orbit

open Sealed Carry

/-- A pair and its swap sort to one pair. -/
theorem sortPair_swap (a b : Nat) : sortPair (b, a) = sortPair (a, b) := by
  unfold sortPair
  by_cases h1 : a ≤ b
  · by_cases h2 : b ≤ a
    · simp only [h1, h2, if_true]
      exact Prod.ext (Nat.le_antisymm h2 h1) (Nat.le_antisymm h1 h2)
    · simp only [h1, h2, if_true, if_false]
  · have h2 : b ≤ a := Nat.le_of_lt (Nat.lt_of_not_le h1)
    simp only [h1, h2, if_true, if_false]

/-- Sorting a pair before or after mapping both entries gives one sorted
pair. -/
theorem sortPair_map (g : Nat → Nat) (p : Nat × Nat) :
    sortPair (g (sortPair p).1, g (sortPair p).2) = sortPair (g p.1, g p.2) := by
  by_cases h : p.1 ≤ p.2
  · have hp : sortPair p = p := by unfold sortPair; simp only [h, if_true]
    rw [hp]
  · have hp : sortPair p = (p.2, p.1) := by unfold sortPair; simp only [h, if_false]
    rw [hp]
    exact sortPair_swap (g p.1) (g p.2)

/-- The composite of two inhabitants of the sealed isomorphism. -/
def isoTrans {r s t : Regime} (σ : Iso r s) (τ : Iso s t) : Iso r t where
  dmap := fun d => τ.dmap (σ.dmap d)
  dinv := fun d => σ.dinv (τ.dinv d)
  fmap := fun f => τ.fmap (σ.fmap f)
  finv := fun f => σ.finv (τ.finv f)
  dmap_lt := fun d hd => τ.dmap_lt _ (List.mem_range.mpr (σ.dmap_lt d hd))
  dinv_lt := fun d hd => σ.dinv_lt _ (List.mem_range.mpr (τ.dinv_lt d hd))
  dinv_dmap := fun d hd => by
    show σ.dinv (τ.dinv (τ.dmap (σ.dmap d))) = d
    rw [τ.dinv_dmap _ (List.mem_range.mpr (σ.dmap_lt d hd)), σ.dinv_dmap d hd]
  dmap_dinv := fun d hd => by
    show τ.dmap (σ.dmap (σ.dinv (τ.dinv d))) = d
    rw [σ.dmap_dinv _ (List.mem_range.mpr (τ.dinv_lt d hd)), τ.dmap_dinv d hd]
  fmap_lt := fun f hf => τ.fmap_lt _ (List.mem_range.mpr (σ.fmap_lt f hf))
  finv_lt := fun f hf => σ.finv_lt _ (List.mem_range.mpr (τ.finv_lt f hf))
  finv_fmap := fun f hf => by
    show σ.finv (τ.finv (τ.fmap (σ.fmap f))) = f
    rw [τ.finv_fmap _ (List.mem_range.mpr (σ.fmap_lt f hf)), σ.finv_fmap f hf]
  fmap_finv := fun f hf => by
    show τ.fmap (σ.fmap (σ.finv (τ.finv f))) = f
    rw [σ.fmap_finv _ (List.mem_range.mpr (τ.finv_lt f hf)), τ.fmap_finv f hf]
  arity := fun f hf => by
    show t.forms.getD (τ.fmap (σ.fmap f)) 0 = r.forms.getD f 0
    rw [τ.arity _ (List.mem_range.mpr (σ.fmap_lt f hf)), σ.arity f hf]
  insts_fwd := fun p hp => by
    have h := τ.insts_fwd _ (σ.insts_fwd p hp)
    simp only [List.map_map] at h
    exact h
  insts_bwd := fun p hp => by
    have h := σ.insts_bwd _ (τ.insts_bwd p hp)
    simp only [List.map_map] at h
    exact h
  rules_fwd := fun f hf => τ.rules_fwd _ (σ.rules_fwd f hf)
  rules_bwd := fun f hf => σ.rules_bwd _ (τ.rules_bwd f hf)
  reqs_fwd := fun q hq => by
    have h := τ.reqs_fwd _ (σ.reqs_fwd q hq)
    rwa [sortPair_map] at h
  reqs_bwd := fun q hq => by
    have h := σ.reqs_bwd _ (τ.reqs_bwd q hq)
    rwa [sortPair_map] at h

/-- O-four mirrored: some automorphism carries `i` to `j`. -/
def OneOrbit (r : Regime) (i j : Nat) : Prop :=
  ∃ α : Iso r r, α.dmap i = j

/-- O-six mirrored: the sorted pair is a requirement. -/
def ReqMember (r : Regime) (i j : Nat) : Prop :=
  sortPair (i, j) ∈ r.reqs

/-- Separability of two admitted data is carried to their images and
back. -/
theorem separable_iso_iff {r s : Regime} (σ : Iso r s) {i j : Nat}
    (hi : i < r.data) (hj : j < r.data) :
    separable r i j ↔ separable s (σ.dmap i) (σ.dmap j) := by
  constructor
  · exact separable_iso σ hi hj
  · intro h
    have h' := separable_iso (isoSymm σ)
      (σ.dmap_lt i (List.mem_range.mpr hi)) (σ.dmap_lt j (List.mem_range.mpr hj)) h
    have bi : (isoSymm σ).dmap (σ.dmap i) = i := σ.dinv_dmap i (List.mem_range.mpr hi)
    have bj : (isoSymm σ).dmap (σ.dmap j) = j := σ.dinv_dmap j (List.mem_range.mpr hj)
    rw [bi, bj] at h'
    exact h'

/-- Collapse of two admitted data is carried to their images and back. -/
theorem collapsed_iso_iff {r s : Regime} (σ : Iso r s) {i j : Nat}
    (hi : i < r.data) (hj : j < r.data) :
    collapsed r i j ↔ collapsed s (σ.dmap i) (σ.dmap j) := by
  constructor
  · exact collapsed_iso σ hi hj
  · intro h
    have h' := collapsed_iso (isoSymm σ)
      (σ.dmap_lt i (List.mem_range.mpr hi)) (σ.dmap_lt j (List.mem_range.mpr hj)) h
    have bi : (isoSymm σ).dmap (σ.dmap i) = i := σ.dinv_dmap i (List.mem_range.mpr hi)
    have bj : (isoSymm σ).dmap (σ.dmap j) = j := σ.dinv_dmap j (List.mem_range.mpr hj)
    rw [bi, bj] at h'
    exact h'

/-- O-four is carried: two admitted data lie in one orbit exactly when
their images do.  Forward, the source's automorphism is conjugated by
`σ`; back, the target's is conjugated by the inverse. -/
theorem oneOrbit_iso {r s : Regime} (σ : Iso r s) {i j : Nat}
    (hi : i < r.data) (hj : j < r.data) :
    OneOrbit r i j ↔ OneOrbit s (σ.dmap i) (σ.dmap j) := by
  constructor
  · rintro ⟨α, hα⟩
    refine ⟨isoTrans (isoTrans (isoSymm σ) α) σ, ?_⟩
    show σ.dmap (α.dmap (σ.dinv (σ.dmap i))) = σ.dmap j
    rw [σ.dinv_dmap i (List.mem_range.mpr hi), hα]
  · rintro ⟨β, hβ⟩
    refine ⟨isoTrans (isoTrans σ β) (isoSymm σ), ?_⟩
    show σ.dinv (β.dmap (σ.dmap i)) = j
    rw [hβ, σ.dinv_dmap j (List.mem_range.mpr hj)]

/-- O-six is carried: the sorted pair of two admitted data is a
requirement exactly when the sorted pair of their images is. -/
theorem reqMember_iso {r s : Regime} (σ : Iso r s) {i j : Nat}
    (hi : i < r.data) (hj : j < r.data) :
    ReqMember r i j ↔ ReqMember s (σ.dmap i) (σ.dmap j) := by
  constructor
  · intro h
    have h' := σ.reqs_fwd _ h
    rwa [sortPair_map σ.dmap (i, j)] at h'
  · intro h
    have h' := σ.reqs_bwd _ h
    rw [sortPair_map σ.dinv (σ.dmap i, σ.dmap j)] at h'
    show sortPair (i, j) ∈ r.reqs
    rw [← σ.dinv_dmap i (List.mem_range.mpr hi), ← σ.dinv_dmap j (List.mem_range.mpr hj)]
    exact h'

end Orbit
end SecondEngine
