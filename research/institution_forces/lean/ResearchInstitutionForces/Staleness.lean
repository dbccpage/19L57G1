import ResearchInstitutionForces.Robust
import ResearchActorInstitution.Chain

/-!
# L2: when a decision goes stale

AuthorityEffect: None.  Outside the seal.

A decision is taken when `Knows D Q q` holds.  Each force below changes one
input of that relation and is answered exactly.

* (a) Adding seats never breaks it (`add_preserves`, from `knows_mono`).
* (b) Removing seats: the kept family `K` still knows `q` exactly when
  every `q`-separated pair keeps a separating seat in `K`
  (`removal_iff`).  The count "more separating seats than removed seats"
  is sufficient for every removal of that size (`Robust.deletion_robust_iff`)
  and not necessary for a particular one (`removal_count_not_necessary`).  Corrupting the removed seats `R` in any way, a
  relabelling included, preserves the decision for every outcome exactly
  when `K` alone knows `q` (`seat_corruption_iff`).  For one particular
  relabelling neither direction is fixed by counts: on the same four-point
  family one bijective relabelling of one seat preserves the decision while
  the untouched seat alone does not know it (`relabel_can_be_harmless`), and
  another destroys it (`relabel_can_break`).
* (c) Extending the carrier by one point `x`: given the decision, it holds on
  `D ++ [x]` exactly when `q` is constant on the signature class of `x` in
  `D ++ [x]` (`extension_iff`); `extension_breaks` is a two-point instance.
* (d) A target `t`: `Knows` takes no target argument, so declaring one
  changes nothing.  Admitting `t` as a seat never breaks the decision and
  makes agreement with `t` known (`target_member_preserves`); a decision can
  hold while it fails to correspond to the target
  (`decision_holds_target_fails`).

So a decision record needs re-review on removal, on relabelling, on carrier
extension and on a newly admitted target, and never on an added seat alone.
-/

namespace ResearchInstitutionForces
namespace Staleness

open Compression ResearchTwoTheorems.Institution Joint

theorem sigEq_symm {Q : Institution} {x y : Nat} (h : SigEq Q x y) : SigEq Q y x :=
  fun p hp => (h p hp).symm

/-- Knowledge depends on the seats as a set: reordering and duplicating
seats changes nothing.  So any removal can be written as `K ++ R`. -/
theorem knows_congr_mem {D : List Nat} {Q Q' : Institution} {q : Nat → Nat}
    (h : ∀ p, p ∈ Q ↔ p ∈ Q') : Knows D Q q ↔ Knows D Q' q :=
  ⟨knows_mono (fun p hp => (h p).mp hp), knows_mono (fun p hp => (h p).mpr hp)⟩

/-! ## (a) Addition -/

/-- **(a)** Adding seats never breaks a decision. -/
theorem add_preserves {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (M : Institution) (h : Knows D Q q) : Knows D (Q ++ M) q :=
  knows_mono (fun _ hp => List.mem_append_left _ hp) h

/-! ## (b) Removal and corruption -/

/-- **(b), removal.**  The kept seats `K` know `q` exactly when every pair
that `q` separates has more separating seats in `K ++ R` than in the removed
seats `R`, that is, keeps at least one in `K`. -/
theorem removal_iff (D : List Nat) (K R : Institution) (q : Nat → Nat) :
    Knows D K q ↔
      ∀ x, x ∈ D → ∀ y, y ∈ D → q x ≠ q y → redundancy R x y < redundancy (K ++ R) x y := by
  rw [knows_iff_redundancy]
  constructor
  · intro h x hx y hy hne
    have h1 := h x hx y hy hne
    rw [redundancy_append]
    omega
  · intro h x hx y hy hne
    have h1 := h x hx y hy hne
    rw [redundancy_append] at h1
    omega

theorem sigEq_append_consts (K : Institution) (n : Nat) {x y : Nat}
    (h : SigEq K x y) : SigEq (K ++ List.replicate n (fun _ => 0)) x y := by
  intro p hp
  rcases List.mem_append.mp hp with h' | h'
  · exact h p h'
  · rw [List.eq_of_mem_replicate h']

/-- **(b), corruption of named seats.**  The decision survives every
replacement of the seats `R` (by presentations of any kind, relabellings of
the old ones included) exactly when the other seats `K` alone know `q`. -/
theorem seat_corruption_iff (D : List Nat) (K R : Institution) (q : Nat → Nat) :
    (∀ R' : Institution, R'.length = R.length → Knows D (K ++ R') q) ↔ Knows D K q := by
  constructor
  · intro h
    have hk := h (List.replicate R.length (fun _ => 0)) List.length_replicate
    rw [knows_iff_determined] at hk ⊢
    intro x hx y hy hs
    exact hk x hx y hy (sigEq_append_consts K R.length hs)
  · intro h R' _
    exact add_preserves R' h

/-- A relabelling of the seats `R` by any `σ` keeps the decision when `K`
alone knows it. -/
theorem relabel_of_kept {D : List Nat} {K : Institution} {q : Nat → Nat}
    (R : Institution) (σ : Nat → Nat) (h : Knows D K q) :
    Knows D (K ++ R.map (fun m x => m (σ x))) q :=
  (seat_corruption_iff D K R q).mpr h _ (List.length_map _)

/-- The count "every separated pair has more seats than the removed seats
number" is sufficient for every removal of that many seats and not
necessary for a particular one: removing a constant seat from
`[id, const]` keeps the decision although the pair `0, 1` has one seat. -/
theorem removal_count_not_necessary :
    Knows [0, 1] [fun x => x] (fun x => x) ∧
    redundancy ([fun x => x] ++ [fun _ => 0]) 0 1 < 1 + 1 := by
  decide

def swap02 (x : Nat) : Nat := if x = 0 then 2 else if x = 2 then 0 else x
def swap12 (x : Nat) : Nat := if x = 1 then 2 else if x = 2 then 1 else x

/-- A bijective relabelling of one seat can be harmless where the count
says nothing: `half` alone does not know the identity, yet relabelling the
other seat by the swap of 0 and 2 keeps the decision. -/
theorem relabel_can_be_harmless :
    (∀ x, x ∈ [0, 1, 2, 3] → swap02 (swap02 x) = x) ∧
    Knows [0, 1, 2, 3] [parity, half] (fun x => x) ∧
    Knows [0, 1, 2, 3] [fun x => parity (swap02 x), half] (fun x => x) ∧
    ¬ Knows [0, 1, 2, 3] [half] (fun x => x) := by
  unfold swap02
  decide

/-- Another bijective relabelling of the same seat destroys the decision. -/
theorem relabel_can_break :
    (∀ x, x ∈ [0, 1, 2, 3] → swap12 (swap12 x) = x) ∧
    Knows [0, 1, 2, 3] [parity, half] (fun x => x) ∧
    ¬ Knows [0, 1, 2, 3] [fun x => parity (swap12 x), half] (fun x => x) := by
  unfold swap12
  decide

/-! ## (c) Carrier extension -/

/-- **(c)** Given the decision on `D`, it holds on `D ++ [x]` exactly when
`q` is constant on the signature class of `x` in `D ++ [x]`. -/
theorem extension_iff (D : List Nat) (Q : Institution) (q : Nat → Nat) (x : Nat)
    (h : Knows D Q q) :
    Knows (D ++ [x]) Q q ↔ ∀ y, y ∈ D ++ [x] → SigEq Q x y → q x = q y := by
  have hxD : x ∈ D ++ [x] := List.mem_append_right D (List.mem_singleton_self x)
  constructor
  · intro hk y hy hs
    exact (knows_iff_determined _ Q q).mp hk x hxD y hy hs
  · intro hc
    rw [knows_iff_determined] at h ⊢
    intro a ha b hb hs
    rcases List.mem_append.mp ha with ha' | ha' <;>
      rcases List.mem_append.mp hb with hb' | hb'
    · exact h a ha' b hb' hs
    · rw [List.mem_singleton.mp hb'] at hs ⊢
      exact (hc a ha (sigEq_symm hs)).symm
    · rw [List.mem_singleton.mp ha'] at hs ⊢
      exact hc b hb hs
    · rw [List.mem_singleton.mp ha', List.mem_singleton.mp hb']

/-- A new point in an old class breaks the decision: on `[0, 2]`, `[half]`
knows `parity` (it is constant there); adding `1`, which `half` puts with
`0`, breaks it. -/
theorem extension_breaks :
    Knows [0, 2] [half] parity ∧ ¬ Knows ([0, 2] ++ [1]) [half] parity := by
  decide

/-! ## (d) Targets -/

/-- **(d)** Admitting a target `t` as a seat never breaks a decision, and
makes agreement with `t` known. -/
theorem target_member_preserves {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (t : Nat → Nat) (h : Knows D Q q) :
    Knows D (Q ++ [t]) q ∧ Knows D (Q ++ [t]) (ResearchActorInstitution.Chain.agreeQ q t) :=
  ⟨add_preserves [t] h,
   ResearchActorInstitution.Chain.agreement_known_of_admitted
     (List.mem_append_right Q (List.mem_singleton_self t)) (add_preserves [t] h)⟩

/-- A decision can hold while failing its target; admitting the target
keeps the decision and makes the failure known. -/
theorem decision_holds_target_fails :
    Knows [0, 1] [] (fun _ => 0) ∧
    ¬ ResearchActorInstitution.Chain.Corr [0, 1] (fun _ => 0) (fun x => x) ∧
    Knows [0, 1] [fun x => x] (fun _ => 0) ∧
    Knows [0, 1] [fun x => x]
      (ResearchActorInstitution.Chain.agreeQ (fun _ => 0) (fun x => x)) := by
  unfold ResearchActorInstitution.Chain.Corr ResearchActorInstitution.Chain.agreeQ
  decide

end Staleness
end ResearchInstitutionForces
