import SecondEngine.Kernel
import SecondEngine.IsoKernel
import SecondEngine.Carry
import SecondEngine.Orbit

/-!
# Stake readings, their flips, their demands, and renaming

Native to continuation one.

A stake rule labels a pair of held data apart, same or free by reading
the regime.  Here a READING is two predicates on a regime and two data:
labelled apart, and labelled same; a pair satisfying neither is free.
The FLIP of a reading exchanges the two, which is what an engine's switch
does to the rule its generator reads.  A DEMAND is a labelled pair that
is not honoured: labelled apart and collapsed, or labelled same and
separable -- the sealed profiles equal where apart was asked, different
where same was asked.  The demand is read off the regime; no event emits
it.

Four of rung two's nine rules read only the observables mirrored in
`SecondEngine/Orbit.lean`, and are mirrored here:

* `E1`: apart when separable, same when collapsed (O-one).
* `E3`: same on one orbit, apart off it (O-four).
* `E4`: apart on one orbit, same off it (O-four).
* `E8`: apart on a requirement, never same (O-six).

The other five read a profile's emptiness or size, or the number of
classes, which this package does not mirror; nothing here speaks of them.

* `e1_never_demands`: `E1` gives no demand anywhere.
* `e1_flip_demands`: its flip demands every collapsed and every
  separable pair.
* `e3_flip_eq_e4`, `e4_flip_eq_e3`: the two orbit rules are one
  another's flip, by `rfl`.
* `e8_quiet_without_reqs`: a regime with no requirement gives `E8` and
  its flip no demand.
* `demand_carried`, and `e1_carried` to `e8_carried` with `carried_flip`:
  every one of the four readings, in both modes, is carried by every
  inhabitant of the sealed isomorphism at admitted data, and so are its
  demands.

AuthorityEffect: None.
-/

namespace SecondEngine
namespace Stake

open Sealed Carry Orbit

/-- A stake reading: labelled apart, labelled same; free otherwise. -/
structure Reading where
  apart : Regime → Nat → Nat → Prop
  same : Regime → Nat → Nat → Prop

/-- The flip exchanges apart and same and keeps free. -/
def Reading.flip (ρ : Reading) : Reading := ⟨ρ.same, ρ.apart⟩

/-- A labelled pair that is not honoured. -/
def Demand (ρ : Reading) (r : Regime) (i j : Nat) : Prop :=
  (ρ.apart r i j ∧ collapsed r i j) ∨ (ρ.same r i j ∧ separable r i j)

/-- Both predicates of a reading are carried, forward and back, by every
inhabitant of the sealed isomorphism, at admitted data. -/
def Carried (ρ : Reading) : Prop :=
  ∀ (r s : Regime) (σ : Iso r s) (i j : Nat), i < r.data → j < r.data →
    (ρ.apart r i j ↔ ρ.apart s (σ.dmap i) (σ.dmap j)) ∧
    (ρ.same r i j ↔ ρ.same s (σ.dmap i) (σ.dmap j))

/-- Rung two's E-one mirrored. -/
def E1 : Reading := ⟨fun r i j => separable r i j, fun r i j => collapsed r i j⟩

/-- Rung two's E-three mirrored. -/
def E3 : Reading := ⟨fun r i j => ¬ OneOrbit r i j, fun r i j => OneOrbit r i j⟩

/-- Rung two's E-four mirrored. -/
def E4 : Reading := ⟨fun r i j => OneOrbit r i j, fun r i j => ¬ OneOrbit r i j⟩

/-- Rung two's E-eight mirrored. -/
def E8 : Reading := ⟨fun r i j => ReqMember r i j, fun _ _ _ => False⟩

/-- Flipping twice is the identity. -/
theorem flip_flip (ρ : Reading) : ρ.flip.flip = ρ := rfl

/-- The flip of E-three is E-four. -/
theorem e3_flip_eq_e4 : E3.flip = E4 := rfl

/-- The flip of E-four is E-three. -/
theorem e4_flip_eq_e3 : E4.flip = E3 := rfl

/-- E-one gives no demand at any regime and any two data: it labels
apart exactly the separable pairs and same exactly the collapsed ones. -/
theorem e1_never_demands (r : Regime) (i j : Nat) : ¬ Demand E1 r i j := by
  rintro (⟨hs, hc⟩ | ⟨hc, hs⟩)
  · exact separable_not_collapsed hs hc
  · exact separable_not_collapsed hs hc

/-- The flip of E-one demands every collapsed and every separable pair. -/
theorem e1_flip_demands (r : Regime) (i j : Nat)
    (h : collapsed r i j ∨ separable r i j) : Demand E1.flip r i j := by
  cases h with
  | inl h => exact Or.inl ⟨h, h⟩
  | inr h => exact Or.inr ⟨h, h⟩

/-- A regime holding no requirement gives E-eight and its flip no
demand. -/
theorem e8_quiet_without_reqs (r : Regime) (hr : r.reqs = []) (i j : Nat) :
    ¬ Demand E8 r i j ∧ ¬ Demand E8.flip r i j := by
  have hm : ¬ ReqMember r i j := by
    intro h
    unfold ReqMember at h
    rw [hr] at h
    cases h
  refine ⟨?_, ?_⟩
  · rintro (⟨h, _⟩ | ⟨h, _⟩)
    · exact hm h
    · exact h
  · rintro (⟨h, _⟩ | ⟨h, _⟩)
    · exact h
    · exact hm h

/-- The flip of a carried reading is carried. -/
theorem carried_flip {ρ : Reading} (h : Carried ρ) : Carried ρ.flip :=
  fun r s σ i j hi hj => ⟨(h r s σ i j hi hj).2, (h r s σ i j hi hj).1⟩

/-- The demands of a carried reading are carried, forward and back. -/
theorem demand_carried {ρ : Reading} (h : Carried ρ) {r s : Regime} (σ : Iso r s)
    {i j : Nat} (hi : i < r.data) (hj : j < r.data) :
    Demand ρ r i j ↔ Demand ρ s (σ.dmap i) (σ.dmap j) := by
  have ha := (h r s σ i j hi hj).1
  have hs := (h r s σ i j hi hj).2
  have hc := collapsed_iso_iff σ hi hj
  have hp := separable_iso_iff σ hi hj
  unfold Demand
  rw [ha, hs, hc, hp]

/-- E-one is carried. -/
theorem e1_carried : Carried E1 :=
  fun _ _ σ _ _ hi hj => ⟨separable_iso_iff σ hi hj, collapsed_iso_iff σ hi hj⟩

/-- E-three is carried. -/
theorem e3_carried : Carried E3 :=
  fun _ _ σ _ _ hi hj => ⟨not_congr (oneOrbit_iso σ hi hj), oneOrbit_iso σ hi hj⟩

/-- E-four is carried. -/
theorem e4_carried : Carried E4 :=
  fun _ _ σ _ _ hi hj => ⟨oneOrbit_iso σ hi hj, not_congr (oneOrbit_iso σ hi hj)⟩

/-- E-eight is carried. -/
theorem e8_carried : Carried E8 :=
  fun _ _ σ _ _ hi hj => ⟨reqMember_iso σ hi hj, Iff.rfl⟩

end Stake
end SecondEngine
