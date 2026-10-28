import ResearchTwoTheorems.Institution
import ResearchTwoTheorems.Reading

/-!
# The institution theorem

An institution is a list of presentations on one represented carrier
(`ResearchTwoTheorems.Institution.Institution`, consumed as it stands).  It
*knows* a question `q` when `q` factors through its joint presentation
(`Knows`).  This module settles when the family knows what no member knows.

* `Exceeds D Q q`: the family knows `q` and no member does.
* `exceeds_iff`: the exact condition — every `q`-distinct pair is separated
  by some member, and every member merges some `q`-distinct pair.
* `exceeds_two_members`, `exceeds_three_data`: two members that disagree on a
  pair, and three distinct data, are necessary.  `no_exceeding_on_two_points`
  and `no_exceeding_single_member` are the same bounds as refusals.
* `exceeds_three_two`: the bounds are attained: three data, two two-valued
  members, a two-valued question.  This is smaller than the four-point
  parity/half witness of `institution_exceeds_members`.
* `correspondence_matters`: the shared carrier is an admission with teeth.
  Re-indexing one member's data by a permutation destroys the family's
  knowledge, so "the same datum in two presentations" is supplied, not
  derived.  `knows_rename` is the positive side: one renaming applied to the
  carrier, every member and the question changes nothing.
* Degradation: `aggregates_inert` (any list of aggregates of the members adds
  no information: an organisational hierarchy adds no distinctions),
  `aggregate_hides_exceeding` (the aggregate of a family that exceeds its
  members equals the aggregate of a single omniscient member: provenance is
  lost), `essential_iff` (a member matters exactly when the rest do not know
  it), `duplicate_inert`, `consensus_after_loss` (losing the only separator
  of a pair turns the family's verdict from "apart" to unanimous "same" while
  nothing observed about the pair changed).

Every carrier is a finite list; every quantifier below ranges over Lean's
`Nat` and `List`, which are metatheory, not anything the institution holds.
AuthorityEffect: None.
-/

namespace ResearchActorInstitution
namespace Inst

open Compression ResearchTwoTheorems.Institution ResearchTwoTheorems.Reading

/-- The family knows `q`, and no single member does. -/
def Exceeds (D : List Nat) (Q : Institution) (q : Nat → Nat) : Prop :=
  Knows D Q q ∧ ∀ p, p ∈ Q → ¬ Knows D [p] q

theorem sigEq_single (p : Nat → Nat) (x y : Nat) : SigEq [p] x y ↔ p x = p y := by
  constructor
  · intro h; exact h p List.mem_cons_self
  · intro h q hq
    rw [List.mem_singleton.mp hq]; exact h

theorem not_knows_single_iff (D : List Nat) (p q : Nat → Nat) :
    ¬ Knows D [p] q ↔ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ p x = p y ∧ q x ≠ q y := by
  rw [not_knows_iff_witness]
  constructor
  · rintro ⟨x, hx, y, hy, hs, hne⟩
    exact ⟨x, hx, y, hy, (sigEq_single p x y).mp hs, hne⟩
  · rintro ⟨x, hx, y, hy, hs, hne⟩
    exact ⟨x, hx, y, hy, (sigEq_single p x y).mpr hs, hne⟩

/-- **Exact condition.**  The family exceeds its members on `q` iff every
pair that `q` tells apart is told apart by some member, and every member
merges some pair that `q` tells apart. -/
theorem exceeds_iff (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Exceeds D Q q ↔
      (∀ x, x ∈ D → ∀ y, y ∈ D → q x ≠ q y → ∃ p, p ∈ Q ∧ p x ≠ p y) ∧
      (∀ p, p ∈ Q → ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ p x = p y ∧ q x ≠ q y) := by
  unfold Exceeds
  constructor
  · rintro ⟨hk, hm⟩
    refine ⟨?_, fun p hp => (not_knows_single_iff D p q).mp (hm p hp)⟩
    intro x hx y hy hne
    apply exists_separator_of_not_sigEq
    intro hs
    exact hne ((knows_iff_determined D Q q).mp hk x hx y hy hs)
  · rintro ⟨hsep, hm⟩
    refine ⟨?_, fun p hp => (not_knows_single_iff D p q).mpr (hm p hp)⟩
    rw [knows_iff_determined]
    intro x hx y hy hs
    cases Nat.decEq (q x) (q y) with
    | isTrue h => exact h
    | isFalse hne =>
      exfalso
      obtain ⟨p, hp, hpne⟩ := hsep x hx y hy hne
      exact hpne (hs p hp)

/-- The empty institution "exceeds its members" on exactly the constant
questions: the second clause is vacuous.  Stated so that the degenerate case
is on record, not hidden. -/
theorem exceeds_nil_iff (D : List Nat) (q : Nat → Nat) :
    Exceeds D [] q ↔ ∀ x, x ∈ D → ∀ y, y ∈ D → q x = q y := by
  unfold Exceeds
  rw [knows_iff_determined]
  constructor
  · rintro ⟨h, _⟩ x hx y hy
    exact h x hx y hy (fun p hp => nomatch hp)
  · intro h
    exact ⟨fun x hx y hy _ => h x hx y hy, fun p hp => nomatch hp⟩

/-- **Two members that disagree are necessary.** -/
theorem exceeds_two_members {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (h : Exceeds D Q q) (hne : Q ≠ []) :
    ∃ p, p ∈ Q ∧ ∃ p', p' ∈ Q ∧ ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ p x = p y ∧ p' x ≠ p' y := by
  obtain ⟨hsep, hm⟩ := (exceeds_iff D Q q).mp h
  cases Q with
  | nil => exact absurd rfl hne
  | cons p Q' =>
    obtain ⟨x, hx, y, hy, hpxy, hq⟩ := hm p List.mem_cons_self
    obtain ⟨p', hp', hp'ne⟩ := hsep x hx y hy hq
    exact ⟨p, List.mem_cons_self, p', hp', x, hx, y, hy, hpxy, hp'ne⟩

/-- **Three distinct data are necessary.**  Two data cannot carry a
distinction that one member merges, another separates, and a third pair
that the second member merges. -/
theorem exceeds_three_data {D : List Nat} {Q : Institution} {q : Nat → Nat}
    (h : Exceeds D Q q) (hne : Q ≠ []) :
    ∃ x, x ∈ D ∧ ∃ y, y ∈ D ∧ ∃ z, z ∈ D ∧ x ≠ y ∧ y ≠ z ∧ x ≠ z := by
  obtain ⟨hsep, hm⟩ := (exceeds_iff D Q q).mp h
  cases Q with
  | nil => exact absurd rfl hne
  | cons p Q' =>
    obtain ⟨x, hx, y, hy, _, hqxy⟩ := hm p List.mem_cons_self
    obtain ⟨p', hp', hp'ne⟩ := hsep x hx y hy hqxy
    obtain ⟨u, hu, v, hv, hp'uv, hquv⟩ := hm p' hp'
    have hxy : x ≠ y := fun e => hqxy (by rw [e])
    have huv : u ≠ v := fun e => hquv (by rw [e])
    cases Nat.decEq u x with
    | isTrue hux =>
      cases Nat.decEq v y with
      | isTrue hvy =>
        exfalso
        apply hp'ne
        rw [← hux, ← hvy]
        exact hp'uv
      | isFalse hvy =>
        exact ⟨x, hx, y, hy, v, hv, hxy, fun e => hvy e.symm, fun e => huv (hux.trans e)⟩
    | isFalse hux =>
      cases Nat.decEq u y with
      | isTrue huy =>
        cases Nat.decEq v x with
        | isTrue hvx =>
          exfalso
          apply hp'ne
          rw [← hvx, ← huy]
          exact hp'uv.symm
        | isFalse hvx =>
          exact ⟨x, hx, y, hy, v, hv, hxy, fun e => huv (huy.trans e), fun e => hvx e.symm⟩
      | isFalse huy =>
        exact ⟨x, hx, y, hy, u, hu, hxy, fun e => huy e.symm, fun e => hux e.symm⟩

theorem mem_pair {x : Nat} (h : x ∈ [0, 1]) : x = 0 ∨ x = 1 := by
  rcases List.mem_cons.mp h with h0 | h1
  · exact Or.inl h0
  · exact Or.inr (List.mem_singleton.mp h1)

/-- On two data no nonempty institution exceeds its members. -/
theorem no_exceeding_on_two_points (Q : Institution) (q : Nat → Nat) (hne : Q ≠ []) :
    ¬ Exceeds [0, 1] Q q := by
  intro h
  obtain ⟨x, hx, y, hy, z, hz, hxy, hyz, hxz⟩ := exceeds_three_data h hne
  have hx' := mem_pair hx
  have hy' := mem_pair hy
  have hz' := mem_pair hz
  omega

/-- A single member never exceeds itself. -/
theorem no_exceeding_single_member (D : List Nat) (p q : Nat → Nat) :
    ¬ Exceeds D [p] q := by
  rintro ⟨hk, hm⟩
  exact hm p List.mem_cons_self hk

/-! ## The minimum is attained -/

/-- Merges `0` and `2`. -/
def p1 : Nat → Nat := fun x => if x = 1 then 1 else 0
/-- Merges `1` and `2`. -/
def p2 : Nat → Nat := fun x => if x = 0 then 0 else 1
/-- Tells `2` from `0` and `1`. -/
def q3 : Nat → Nat := fun x => if x = 2 then 1 else 0

/-- **Three data, two members, two values suffice.**  Each member merges a
pair that `q3` separates; together they separate everything `q3` does. -/
theorem exceeds_three_two : Exceeds [0, 1, 2] [p1, p2] q3 := by
  unfold Exceeds
  decide

/-- The same witness, read through the exact condition: both members are
two-valued and the question is two-valued, so no cheaper resolution exists
on either side. -/
theorem exceeds_three_two_resolution :
    classCount [0, 1, 2] [p1] = 2 ∧ classCount [0, 1, 2] [p2] = 2 ∧
    classCount [0, 1, 2] [q3] = 2 ∧ information [0, 1, 2] [p1, p2] = 3 := by
  decide

/-! ## The shared carrier is an admission -/

/-- Swap the indices `0` and `1`. -/
def swap01 : Nat → Nat := fun x => if x = 0 then 1 else if x = 1 then 0 else x

/-- **Correspondence matters.**  The family `[p1, p2]` knows `q3`; the family
in which the second member reads its data through a permutation of the
carrier does not.  So the identification of datum `i` across members is a
supplied correspondence, not a consequence of anything the members present.
(Compare `research/uncollapse` U9: the raw family index is
presentation-dependent.) -/
theorem correspondence_matters :
    Knows [0, 1, 2] [p1, p2] q3 ∧
    ¬ Knows [0, 1, 2] [p1, fun x => p2 (swap01 x)] q3 := by
  decide

/-- **Renaming invariance.**  One renaming `τ` of the carrier, with a left
inverse `σ`, applied to the carrier, to every member and to the question,
changes nothing: knowledge depends on no choice of names. -/
theorem knows_rename {σ τ : Nat → Nat} (hστ : ∀ x, σ (τ x) = x)
    (D : List Nat) (Q : Institution) (q : Nat → Nat) :
    Knows (D.map τ) (Q.map (fun p => fun x => p (σ x))) (fun x => q (σ x)) ↔
      Knows D Q q := by
  rw [knows_iff_determined, knows_iff_determined]
  constructor
  · intro h x hx y hy hs
    have h1 := h (τ x) (List.mem_map.mpr ⟨x, hx, rfl⟩)
      (τ y) (List.mem_map.mpr ⟨y, hy, rfl⟩) ?_
    · show q x = q y
      have h2 : q (σ (τ x)) = q (σ (τ y)) := h1
      rw [hστ, hστ] at h2
      exact h2
    · intro p' hp'
      obtain ⟨p, hp, rfl⟩ := List.mem_map.mp hp'
      show p (σ (τ x)) = p (σ (τ y))
      rw [hστ, hστ]
      exact hs p hp
  · intro h x' hx' y' hy' hs
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hx'
    obtain ⟨y, hy, rfl⟩ := List.mem_map.mp hy'
    show q (σ (τ x)) = q (σ (τ y))
    rw [hστ, hστ]
    apply h x hx y hy
    intro p hp
    have h2 : p (σ (τ x)) = p (σ (τ y)) :=
      hs (fun z => p (σ z)) (List.mem_map.mpr ⟨p, hp, rfl⟩)
    rw [hστ, hστ] at h2
    exact h2

/-! ## Degradation -/

/-- Information depends on the members as a set. -/
theorem information_congr_mem {D : List Nat} {Q Q' : Institution}
    (h : ∀ p, p ∈ Q ↔ p ∈ Q') : information D Q = information D Q' :=
  Nat.le_antisymm (information_mono (fun p hp => (h p).mp hp))
    (information_mono (fun p hp => (h p).mpr hp))

/-- **Hierarchies add no distinctions.**  Any list of aggregates — members
each of which the family already knows (digests, reports, managers'
summaries, nested joint presentations) — leaves the information unchanged. -/
theorem aggregates_inert (D : List Nat) :
    ∀ (M : Institution) (Q : Institution), (∀ m, m ∈ M → Knows D Q m) →
      information D (Q ++ M) = information D Q := by
  intro M
  induction M with
  | nil => intro Q _; rw [List.append_nil]
  | cons m M' ih =>
    intro Q hM
    have hm : Knows D Q m := hM m List.mem_cons_self
    have h1 : information D ((Q ++ [m]) ++ M') = information D (Q ++ [m]) := by
      apply ih
      intro m' hm'
      exact knows_mono (fun p hp => List.mem_append_left _ hp)
        (hM m' (List.mem_cons_of_mem _ hm'))
    rw [List.append_assoc, List.singleton_append] at h1
    rw [h1]
    exact information_append_of_knows hm

/-- The same for knowledge: aggregates change what is known of nothing. -/
theorem aggregates_inert_knows (D : List Nat) (q : Nat → Nat) :
    ∀ (M : Institution) (Q : Institution), (∀ m, m ∈ M → Knows D Q m) →
      (Knows D (Q ++ M) q ↔ Knows D Q q) := by
  intro M
  induction M with
  | nil => intro Q _; rw [List.append_nil]
  | cons m M' ih =>
    intro Q hM
    have hm : Knows D Q m := hM m List.mem_cons_self
    have h1 : Knows D ((Q ++ [m]) ++ M') q ↔ Knows D (Q ++ [m]) q := by
      apply ih
      intro m' hm'
      exact knows_mono (fun p hp => List.mem_append_left _ hp)
        (hM m' (List.mem_cons_of_mem _ hm'))
    rw [List.append_assoc, List.singleton_append] at h1
    rw [h1]
    exact known_extension_inert hm q

/-- **A member is essential exactly when the others do not know it.**
Removing it loses information iff its question is not determined by the
rest. -/
theorem essential_iff (D : List Nat) (Q1 Q2 : Institution) (p : Nat → Nat) :
    information D (Q1 ++ Q2) < information D (Q1 ++ p :: Q2) ↔
      ¬ Knows D (Q1 ++ Q2) p := by
  have hmem : ∀ r, r ∈ Q1 ++ p :: Q2 ↔ r ∈ (Q1 ++ Q2) ++ [p] := by
    intro r
    constructor
    · intro h
      rcases List.mem_append.mp h with h | h
      · exact List.mem_append_left _ (List.mem_append_left _ h)
      · rcases List.mem_cons.mp h with h | h
        · rw [h]; exact List.mem_append_right _ List.mem_cons_self
        · exact List.mem_append_left _ (List.mem_append_right _ h)
    · intro h
      rcases List.mem_append.mp h with h | h
      · rcases List.mem_append.mp h with h | h
        · exact List.mem_append_left _ h
        · exact List.mem_append_right _ (List.mem_cons_of_mem _ h)
      · rw [List.mem_singleton.mp h]
        exact List.mem_append_right _ List.mem_cons_self
  rw [information_congr_mem (D := D) hmem]
  constructor
  · intro hlt hk
    rw [information_append_of_knows hk] at hlt
    exact Nat.lt_irrefl _ hlt
  · intro hn
    exact information_lt_of_not_knows hn

/-- A duplicated member is redundant: losing one copy changes nothing. -/
theorem duplicate_inert (D : List Nat) (Q : Institution) (p : Nat → Nat) :
    information D (p :: p :: Q) = information D (p :: Q) := by
  apply information_congr_mem
  intro r
  constructor
  · intro h
    rcases List.mem_cons.mp h with h | h
    · rw [h]; exact List.mem_cons_self
    · exact h
  · intro h
    exact List.mem_cons_of_mem _ h

/-- **Provenance is lost in the aggregate.**  On four points the family
`[parity, half]` exceeds its members on the identity question, the single
member `[id]` does not, and the two have the same joint presentation on the
carrier.  Whoever holds only the aggregate cannot tell an institution that
exceeds its members from one omniscient actor. -/
theorem aggregate_hides_exceeding :
    (∀ x, x ∈ [0, 1, 2, 3] →
      pQ [0, 1, 2, 3] [parity, half] x = pQ [0, 1, 2, 3] [fun x => x] x) ∧
    Exceeds [0, 1, 2, 3] [parity, half] (fun x => x) ∧
    ¬ Exceeds [0, 1, 2, 3] [fun x => x] (fun x => x) := by
  unfold Exceeds
  decide

/-- **Consensus after loss.**  In the three-point witness the pair `(0, 2)`
is told apart by `p2` alone.  Lose `p2`: every remaining member merges the
pair, the family's verdict on it turns from "apart" to "same", and `q3`
is no longer known — while nothing presented about `0` or `2` changed.
Unanimity produced by loss is not evidence of identity. -/
theorem consensus_after_loss :
    ¬ SigEq [p1, p2] 0 2 ∧ SigEq [p1] 0 2 ∧
    Knows [0, 1, 2] [p1, p2] q3 ∧ ¬ Knows [0, 1, 2] [p1] q3 := by
  unfold SigEq
  decide

end Inst
end ResearchActorInstitution
