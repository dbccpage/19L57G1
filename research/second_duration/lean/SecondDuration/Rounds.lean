import SecondDuration.Kernel

/-!
# Growths, rest rounds, and what the regime carries of them

Native to rung seven.

A history is replayed from a base by the sealed step.  A ROUND is an
event after which the regime differs (rung six's CHANGING reading).  A
GROWTH is a round after which the regime has more data; a REST ROUND is a
round that is not a growth.  An ill-formed event ends every count, as it
ends replay.

* `growths b h`, `rest b h`: the growths and the rest rounds of a
  history from a base.
* `during n b h`: the rest rounds taken while the regime has exactly `n`
  data.  From a base with `k` data, segment `i` of the duration vector is
  `during (k + i) b h`.
* `after t b h`: the rest rounds taken while the regime has more than `t`
  data.
* `naming t r`: the instances and requirements of a regime that name a
  datum index at or above `t`.

What is proved:

* `growths_counted`, `rest_counted`: the regime reached has the base's
  data plus the growths, and its element count is the base's plus the
  growths plus the rest rounds.  So the number of segments and the sum of
  the vector are functions of the base and the regime
  (`growths_given_base`, `rest_given_base`).
* `naming_bounded`: the instances and requirements naming `t` or later
  that a history adds are at most its rest rounds taken after the regime
  has more than `t` data.  No well-formedness hypothesis on the base.

`replayE_cons` and `insertNew_grows` repeat, as statements, rung six's
lemmas of the same names; they are proved again here so that this
package imports nothing.

Nothing here mentions the sealed isomorphism, and nothing here states
which vectors some history attains.

AuthorityEffect: None.
-/

namespace SecondDuration
namespace Rounds

open Sealed

/-- The element count of a regime, as rung five defined it. -/
def size (r : Regime) : Nat :=
  r.data + r.forms.length + r.insts.length + r.rules.length + r.reqs.length

/-- The growths of a history replayed from a base. -/
def growths : Regime → List Event → Nat
  | _, [] => 0
  | r, e :: es =>
    match stepE r e with
    | none => 0
    | some r' => (if r'.data = r.data then 0 else 1) + growths r' es

/-- The rest rounds of a history replayed from a base. -/
def rest : Regime → List Event → Nat
  | _, [] => 0
  | r, e :: es =>
    match stepE r e with
    | none => 0
    | some r' => (if r' ≠ r ∧ r'.data = r.data then 1 else 0) + rest r' es

/-- The rest rounds taken while the regime has exactly `n` data. -/
def during (n : Nat) : Regime → List Event → Nat
  | _, [] => 0
  | r, e :: es =>
    match stepE r e with
    | none => 0
    | some r' =>
      (if r' ≠ r ∧ r'.data = r.data ∧ r.data = n then 1 else 0) + during n r' es

/-- The rest rounds taken while the regime has more than `t` data. -/
def after (t : Nat) : Regime → List Event → Nat
  | _, [] => 0
  | r, e :: es =>
    match stepE r e with
    | none => 0
    | some r' =>
      (if r' ≠ r ∧ r'.data = r.data ∧ t < r.data then 1 else 0) + after t r' es

/-- The instances and requirements of a regime naming a datum index at or
above `t`. -/
def naming (t : Nat) (r : Regime) : Nat :=
  (r.insts.filter (fun p => p.2.any (fun x => decide (t ≤ x)))).length +
    (r.reqs.filter (fun q => decide (t ≤ q.2))).length

theorem replayE_cons (e : Event) (es : List Event) (b : Regime) :
    replayE (e :: es) b = (stepE b e).bind (fun r => replayE es r) := by
  cases hs : stepE b e <;> simp [replayE, List.foldlM, hs]

/-- Deduplicating insertion keeps a list or lengthens it by one. -/
theorem insertNew_grows {α : Type} [DecidableEq α] (l : List α) (a : α) :
    insertNew l a = l ∨ (insertNew l a).length = l.length + 1 := by
  unfold insertNew
  split
  · exact Or.inl rfl
  · exact Or.inr (by rw [List.length_append]; rfl)

/-- One event keeps the regime, or is a growth adding one element, or is a
rest round adding one element. -/
theorem step_parts {r r' : Regime} {e : Event} (h : stepE r e = some r') :
    r' = r ∨ (r'.data = r.data + 1 ∧ size r' = size r + 1) ∨
      (r'.data = r.data ∧ size r' = size r + 1) := by
  cases e with
  | supply t =>
    exact Or.inl (Option.some.inj h).symm
  | admitDatum =>
    cases Option.some.inj h
    refine Or.inr (Or.inl ⟨rfl, ?_⟩)
    simp only [size]
    omega
  | admitForm a =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      refine Or.inr (Or.inr ⟨rfl, ?_⟩)
      simp only [size, List.length_append, List.length_singleton]
      omega
    · cases h
  | admitInst f args =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      rcases insertNew_grows r.insts (f, args) with hk | hk
      · exact Or.inl (by rw [hk])
      · refine Or.inr (Or.inr ⟨rfl, ?_⟩)
        simp only [size, hk]
        omega
    · cases h
  | admitRuleAll f =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      rcases insertNew_grows r.rules f with hk | hk
      · exact Or.inl (by rw [hk])
      · refine Or.inr (Or.inr ⟨rfl, ?_⟩)
        simp only [size, hk]
        omega
    · cases h
  | impose i j =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      rcases insertNew_grows r.reqs (i, j) with hk | hk
      · exact Or.inl (by rw [hk])
      · refine Or.inr (Or.inr ⟨rfl, ?_⟩)
        simp only [size, hk]
        omega
    · cases h

/-- The number of growths, read off the base and the regime reached. -/
theorem growths_counted (h : List Event) :
    ∀ b r : Regime, replayE h b = some r → r.data = b.data + growths b h := by
  induction h with
  | nil =>
    intro b r hr
    cases Option.some.inj hr
    rfl
  | cons e es ih =>
    intro b r hr
    rw [replayE_cons] at hr
    cases hs : stepE b e with
    | none =>
      rw [hs] at hr
      cases hr
    | some b' =>
      rw [hs] at hr
      have hrest : r.data = b'.data + growths b' es := ih b' r hr
      have hc : growths b (e :: es) =
          (if b'.data = b.data then 0 else 1) + growths b' es := by
        simp only [growths, hs]
      rw [hc, hrest]
      rcases step_parts hs with heq | ⟨hd, _⟩ | ⟨hd, _⟩
      · rw [heq, if_pos rfl]
        omega
      · rw [if_neg (by omega), hd]
        omega
      · rw [if_pos hd, hd]
        omega

/-- The element count of the regime reached is the base's plus the growths
plus the rest rounds. -/
theorem rest_counted (h : List Event) :
    ∀ b r : Regime, replayE h b = some r →
      size r = size b + growths b h + rest b h := by
  induction h with
  | nil =>
    intro b r hr
    cases Option.some.inj hr
    rfl
  | cons e es ih =>
    intro b r hr
    rw [replayE_cons] at hr
    cases hs : stepE b e with
    | none =>
      rw [hs] at hr
      cases hr
    | some b' =>
      rw [hs] at hr
      have hrest : size r = size b' + growths b' es + rest b' es := ih b' r hr
      have hg : growths b (e :: es) =
          (if b'.data = b.data then 0 else 1) + growths b' es := by
        simp only [growths, hs]
      have hq : rest b (e :: es) =
          (if b' ≠ b ∧ b'.data = b.data then 1 else 0) + rest b' es := by
        simp only [rest, hs]
      rw [hg, hq, hrest]
      rcases step_parts hs with heq | ⟨hd, hsz⟩ | ⟨hd, hsz⟩
      · subst heq
        rw [if_pos rfl, if_neg (fun hc => hc.1 rfl)]
        omega
      · have hne : b' ≠ b := fun hc => by rw [hc] at hd; omega
        rw [if_neg (by omega), if_neg (fun hc => by omega), hsz]
        omega
      · have hne : b' ≠ b := fun hc => by rw [hc] at hsz; omega
        rw [if_pos hd, if_pos ⟨hne, hd⟩, hsz]
        omega

/-- A function of the base and the regime gives the number of growths. -/
theorem growths_given_base :
    ∃ F : Regime → Regime → Nat, ∀ (h : List Event) (b r : Regime),
      replayE h b = some r → growths b h = F b r :=
  ⟨fun b r => r.data - b.data, fun h b r hr => by
    have h1 := growths_counted h b r hr
    show growths b h = r.data - b.data
    omega⟩

/-- A function of the base and the regime gives the number of rest rounds,
the sum of the duration vector. -/
theorem rest_given_base :
    ∃ F : Regime → Regime → Nat, ∀ (h : List Event) (b r : Regime),
      replayE h b = some r → rest b h = F b r :=
  ⟨fun b r => size r - size b - (r.data - b.data), fun h b r hr => by
    have h1 := growths_counted h b r hr
    have h2 := rest_counted h b r hr
    show rest b h = size r - size b - (r.data - b.data)
    omega⟩

/-- The rest rounds after `t` are among the rest rounds, for every
history, replayed or not. -/
theorem after_le_rest (t : Nat) (h : List Event) :
    ∀ b : Regime, after t b h ≤ rest b h := by
  induction h with
  | nil => intro _; exact Nat.le_refl 0
  | cons e es ih =>
    intro b
    cases hs : stepE b e with
    | none =>
      simp only [after, rest, hs]
      exact Nat.le_refl 0
    | some b' =>
      have ha : after t b (e :: es) =
          (if b' ≠ b ∧ b'.data = b.data ∧ t < b.data then 1 else 0) +
            after t b' es := by
        simp only [after, hs]
      have hq : rest b (e :: es) =
          (if b' ≠ b ∧ b'.data = b.data then 1 else 0) + rest b' es := by
        simp only [rest, hs]
      have hi := ih b'
      rw [ha, hq]
      by_cases hc : b' ≠ b ∧ b'.data = b.data ∧ t < b.data
      · rw [if_pos hc, if_pos ⟨hc.1, hc.2.1⟩]
        omega
      · rw [if_neg hc]
        split <;> omega

/-- One event adds at most one instance or requirement naming `t` or
later, and only as a rest round taken while the regime has more than `t`
data. -/
theorem naming_step {r r' : Regime} {e : Event} (t : Nat)
    (h : stepE r e = some r') :
    naming t r' ≤
      naming t r + (if r' ≠ r ∧ r'.data = r.data ∧ t < r.data then 1 else 0) := by
  cases e with
  | supply s =>
    cases Option.some.inj h
    omega
  | admitDatum =>
    cases Option.some.inj h
    simp only [naming]
    omega
  | admitForm a =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      simp only [naming]
      omega
    · cases h
  | admitInst f args =>
    simp only [stepE] at h
    split at h
    · rename_i hok
      cases Option.some.inj h
      by_cases hm : (f, args) ∈ r.insts
      · rw [insertNew_of_mem hm]
        exact Nat.le_trans (Nat.le_of_eq rfl) (Nat.le_add_right _ _)
      · rw [insertNew_of_not_mem hm]
        by_cases hp : (args.any (fun x => decide (t ≤ x))) = true
        · have hlt : t < r.data := by
            obtain ⟨x, hx, htx⟩ := List.any_eq_true.mp hp
            have := hok.2.2 x hx
            have : t ≤ x := of_decide_eq_true htx
            omega
          have hne : ({ r with insts := r.insts ++ [(f, args)] } : Regime) ≠ r := by
            intro hc
            have hl := congrArg (fun q : Regime => q.insts.length) hc
            simp only [List.length_append, List.length_singleton] at hl
            omega
          rw [if_pos ⟨hne, rfl, hlt⟩]
          simp only [naming, List.filter_append, List.length_append]
          have : ((([(f, args)] : List Inst).filter
              (fun p => p.2.any (fun x => decide (t ≤ x)))).length) ≤ 1 := by
            simp only [List.filter_cons, List.filter_nil]
            split <;> simp
          omega
        · have hz : (([(f, args)] : List Inst).filter
              (fun p => p.2.any (fun x => decide (t ≤ x)))).length = 0 := by
            simp only [List.filter_cons, List.filter_nil]
            simp [hp]
          simp only [naming, List.filter_append, List.length_append, hz]
          omega
    · cases h
  | admitRuleAll f =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      simp only [naming]
      omega
    · cases h
  | impose i j =>
    simp only [stepE] at h
    split at h
    · rename_i hok
      cases Option.some.inj h
      by_cases hm : (i, j) ∈ r.reqs
      · rw [insertNew_of_mem hm]
        exact Nat.le_trans (Nat.le_of_eq rfl) (Nat.le_add_right _ _)
      · rw [insertNew_of_not_mem hm]
        by_cases hp : t ≤ j
        · have hlt : t < r.data := by omega
          have hne : ({ r with reqs := r.reqs ++ [(i, j)] } : Regime) ≠ r := by
            intro hc
            have hl := congrArg (fun q : Regime => q.reqs.length) hc
            simp only [List.length_append, List.length_singleton] at hl
            omega
          rw [if_pos ⟨hne, rfl, hlt⟩]
          simp only [naming, List.filter_append, List.length_append]
          have : ((([(i, j)] : List (Nat × Nat)).filter
              (fun q => decide (t ≤ q.2))).length) ≤ 1 := by
            simp only [List.filter_cons, List.filter_nil]
            split <;> simp
          omega
        · have hz : (([(i, j)] : List (Nat × Nat)).filter
              (fun q => decide (t ≤ q.2))).length = 0 := by
            simp [hp]
          simp only [naming, List.filter_append, List.length_append, hz]
          omega
    · cases h

/-- What a history adds naming `t` or later is at most its rest rounds
taken after the regime has more than `t` data. -/
theorem naming_bounded (t : Nat) (h : List Event) :
    ∀ b r : Regime, replayE h b = some r → naming t r ≤ naming t b + after t b h := by
  induction h with
  | nil =>
    intro b r hr
    cases Option.some.inj hr
    exact Nat.le_add_right _ _
  | cons e es ih =>
    intro b r hr
    rw [replayE_cons] at hr
    cases hs : stepE b e with
    | none =>
      rw [hs] at hr
      cases hr
    | some b' =>
      rw [hs] at hr
      have hrest := ih b' r hr
      have ha : after t b (e :: es) =
          (if b' ≠ b ∧ b'.data = b.data ∧ t < b.data then 1 else 0) +
            after t b' es := by
        simp only [after, hs]
      have hn := naming_step t hs
      rw [ha]
      omega

end Rounds
end SecondDuration
