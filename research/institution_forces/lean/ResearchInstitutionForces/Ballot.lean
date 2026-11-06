import ResearchInstitutionForces.Staleness

/-!
# L3: ballots know at most what the pooled observations know

AuthorityEffect: None.  Outside the seal.

A seat `m` casts the ballot `f ∘ m`, one ballot map `f` per seat.  The
ballot values are read as NAY `0`, AYE `1`, ABSTAIN `2`; nothing below
depends on that reading, and the general theorems hold for ballot maps
with any values.

* `knows_of_known_members`: if every member of `B` is known by `Q`, then
  whatever `B` knows, `Q` knows.
* `ballot_compression` (L3, per-seat maps): `Knows D (ballots fs Q) q`
  implies `Knows D Q q`.  `ballots` pairs maps and seats in order and stops
  at the shorter list, so seats without a map cast no ballot; the theorem
  holds either way.  `uniform_ballot_compression` is the special case of
  one map for every seat.
* `tally_compression`: a rule that sees only the count of one ballot value
  knows at most what the ballots know.
* `sincere`: the ballot that says AYE or NAY where the question is settled
  on the seat's class and ABSTAIN where it is not.  `sincere_known` shows it
  is a ballot of its seat (a function of the seat's answer on `D`), so the
  compression theorem covers it (`sincere_compression`).
* `ballot_loses_exceeding`: the converse fails.  On four points the family
  `[parity, half]` knows `xorPH` while neither seat does; both sincere
  ballots are ABSTAIN at every point, so the ballots know nothing but the
  constants.  `injective_ballot_keeps`: a ballot map that is injective on
  the seat's two values loses nothing here, so the loss comes from what the
  ballot reports, not from the number of ballot values.
-/

namespace ResearchInstitutionForces
namespace Ballot

open Compression ResearchTwoTheorems.Institution

/-- If `Q` knows every member of `B`, it knows whatever `B` knows. -/
theorem knows_of_known_members {D : List Nat} {Q B : Institution} {q : Nat → Nat}
    (hB : ∀ b, b ∈ B → Knows D Q b) (h : Knows D B q) : Knows D Q q := by
  rw [knows_iff_determined] at h ⊢
  intro x hx y hy hs
  apply h x hx y hy
  intro b hb
  exact (knows_iff_determined D Q b).mp (hB b hb) x hx y hy hs

/-- Per-seat ballots: seat `m` with map `f` casts `f ∘ m`. -/
def ballots : List (Nat → Nat) → Institution → Institution
  | f :: fs, m :: Q => (fun x => f (m x)) :: ballots fs Q
  | _, _ => []

theorem mem_ballots : ∀ (fs : List (Nat → Nat)) (Q : Institution) (b : Nat → Nat),
    b ∈ ballots fs Q → ∃ f : Nat → Nat, ∃ m : Nat → Nat, m ∈ Q ∧ b = fun x => f (m x)
  | [], _, _, hb => by cases hb
  | _ :: _, [], _, hb => by cases hb
  | f :: fs, m :: Q, b, hb => by
    rcases List.mem_cons.mp hb with h | h
    · exact ⟨f, m, List.mem_cons_self, h⟩
    · obtain ⟨f', m', hm', e⟩ := mem_ballots fs Q b h
      exact ⟨f', m', List.mem_cons_of_mem _ hm', e⟩

theorem ballot_known (D : List Nat) (Q : Institution) (fs : List (Nat → Nat)) :
    ∀ b, b ∈ ballots fs Q → Knows D Q b := by
  intro b hb
  obtain ⟨f, m, hm, rfl⟩ := mem_ballots fs Q b hb
  exact knows_comp f (knows_member hm)

/-- **L3, per-seat ballot maps.**  What the ballots know, the seats know. -/
theorem ballot_compression (D : List Nat) (Q : Institution) (fs : List (Nat → Nat))
    (q : Nat → Nat) (h : Knows D (ballots fs Q) q) : Knows D Q q :=
  knows_of_known_members (ballot_known D Q fs) h

/-- **L3, one map for every seat.** -/
theorem uniform_ballot_compression (D : List Nat) (Q : Institution) (f : Nat → Nat)
    (q : Nat → Nat) (h : Knows D (Q.map (fun m x => f (m x))) q) : Knows D Q q := by
  apply knows_of_known_members _ h
  intro b hb
  obtain ⟨m, hm, rfl⟩ := List.mem_map.mp hb
  exact knows_comp f (knows_member hm)

/-- The number of ballots of value `v` at `x`. -/
def tallyOf (v : Nat) (B : Institution) : Nat → Nat := fun x => (sigList B x).count v

theorem tally_known (D : List Nat) (B : Institution) (v : Nat) :
    Knows D B (tallyOf v B) := by
  rw [knows_iff_sigList]
  intro x _ y _ hs
  show (sigList B x).count v = (sigList B y).count v
  rw [hs]

/-- A rule that sees only one tally knows at most what the ballots know. -/
theorem tally_compression (D : List Nat) (B : Institution) (v : Nat) (q : Nat → Nat)
    (h : Knows D [tallyOf v B] q) : Knows D B q := by
  apply knows_of_known_members _ h
  intro b hb
  rw [List.mem_singleton.mp hb]
  exact tally_known D B v

/-! ## The sincere ballot -/

/-- `q` is settled on the class of `x` under the single seat `m`. -/
def settledAt (D : List Nat) (q m : Nat → Nat) (x : Nat) : Bool :=
  D.all (fun y => !(decide (m y = m x)) || decide (q y = q x))

/-- The sincere ballot of seat `m` on `q`: NAY `0` or AYE `1` where `q` is
settled on the seat's class (by whether `q` is `0` there), ABSTAIN `2`
elsewhere. -/
def sincere (D : List Nat) (q m : Nat → Nat) : Nat → Nat := fun x =>
  if settledAt D q m x = true then (if q x = 0 then 0 else 1) else 2

theorem settledAt_eq {D : List Nat} {q m : Nat → Nat} {x y : Nat} (hy : y ∈ D)
    (hm : m x = m y) (h : settledAt D q m x = true) : q x = q y := by
  unfold settledAt at h
  rw [List.all_eq_true] at h
  rcases Bool.or_eq_true_iff.mp (h y hy) with e | e
  · rw [Bool.not_eq_true', decide_eq_false_iff_not] at e
    exact absurd hm.symm e
  · exact (of_decide_eq_true e).symm

theorem settledAt_congr {D : List Nat} {q m : Nat → Nat} {x y : Nat}
    (hm : m x = m y) (hq : q x = q y) : settledAt D q m x = settledAt D q m y := by
  unfold settledAt
  rw [hm, hq]

/-- The sincere ballot is a ballot of its seat: on `D` it is a function of
the seat's answer. -/
theorem sincere_known (D : List Nat) (q m : Nat → Nat) : Knows D [m] (sincere D q m) := by
  rw [knows_iff_determined]
  intro x hx y hy hs
  have hm : m x = m y := hs m List.mem_cons_self
  unfold sincere
  cases hcx : settledAt D q m x with
  | true =>
    have hq := settledAt_eq hy hm hcx
    have hcy : settledAt D q m y = true := by rw [← settledAt_congr hm hq]; exact hcx
    rw [if_pos rfl, if_pos hcy, hq]
  | false =>
    cases hcy : settledAt D q m y with
    | true =>
      have hq := settledAt_eq hx hm.symm hcy
      have hcx' : settledAt D q m x = true := by rw [settledAt_congr hm hq.symm]; exact hcy
      rw [hcx] at hcx'
      exact Bool.noConfusion hcx'
    | false => rfl

/-- **L3 for sincere ballots.** -/
theorem sincere_compression (D : List Nat) (Q : Institution) (q q' : Nat → Nat)
    (h : Knows D (Q.map (sincere D q)) q') : Knows D Q q' := by
  apply knows_of_known_members _ h
  intro b hb
  obtain ⟨m, hm, rfl⟩ := List.mem_map.mp hb
  exact knows_mono (fun p hp => by rw [List.mem_singleton.mp hp]; exact hm)
    (sincere_known D q m)

/-! ## The converse fails -/

/-- Parity of `parity + half` on four points: known jointly, by no seat. -/
def xorPH (x : Nat) : Nat := (parity x + half x) % 2

/-- **Ballots lose exceeding knowledge.**  `[parity, half]` knows `xorPH`
and no seat alone does; both sincere ballots are ABSTAIN at every point,
these are the ballots of the constant map `2`, and they do not know
`xorPH`. -/
theorem ballot_loses_exceeding :
    ResearchActorInstitution.Inst.Exceeds [0, 1, 2, 3] [parity, half] xorPH ∧
    (∀ x, x ∈ [0, 1, 2, 3] →
      sincere [0, 1, 2, 3] xorPH parity x = 2 ∧ sincere [0, 1, 2, 3] xorPH half x = 2) ∧
    ¬ Knows [0, 1, 2, 3] (ballots [fun _ => 2, fun _ => 2] [parity, half]) xorPH := by
  unfold ResearchActorInstitution.Inst.Exceeds
  decide

/-- An injective ballot map loses nothing on this family. -/
theorem injective_ballot_keeps :
    Knows [0, 1, 2, 3] (ballots [fun v => 1 - v, fun v => 1 - v] [parity, half]) xorPH := by
  decide

end Ballot
end ResearchInstitutionForces
