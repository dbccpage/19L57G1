import SecondResponse.Kernel
import SecondResponse.Exhaust

/-!
# Which events begin, end and keep exhaustion

Native to rung ten, apart from the two restatements named below.

* `ctx_step_keep`: an accepted event that is neither an instance nor a
  rule admission keeps every well-formed context well formed, leaves
  derivability of every instance as it was, and keeps every datum.
* `separable_step_keep` (rung nine's statement) and
  `distinguishes_step_keep`: so those four kinds keep every separable
  pair separable and every distinguishing form distinguishing, on every
  regime.
* `exhausted_step_keep`: a supply, a requirement, a form admission and a
  rule admission keep every exhausted admitted form exhausted, on every
  regime.
* `fresh_form_exhausted`: a form admission to a well-formed regime adds
  an exhausted form.
* `exhaustion_begun_by_inst`, `exhaustion_begun_by_rule`: an instance
  admission and a rule admission can each begin the exhaustion of a
  form; `exhaustion_ended_by_datum`, `exhaustion_ended_by_inst`: a datum
  admission and an instance admission can each end it.  Each exhibits a
  well-formed regime and one accepted event.
* `step_data_le`: every accepted event keeps every datum.

`getD_append_lt` repeats, as a statement, rung five's lemma of the same
name, proved again at rungs eight and nine; `separable_step_keep`
repeats rung nine's statement.  Both are proved again here so that this
package imports nothing.

AuthorityEffect: None.
-/

namespace SecondResponse
namespace ExhaustStep

open Sealed
open Exhaust (Distinguishes Exhausted exhausted_of_rule exhausted_of_no_inst
  exhausted_of_le_one)

/-- Reading a list extended at its end, at an index inside the list
(rung five's statement). -/
theorem getD_append_lt (l : List Nat) (a : Nat) {i : Nat} (h : i < l.length) :
    (l ++ [a]).getD i 0 = l.getD i 0 := by
  induction l generalizing i with
  | nil => exact absurd h (Nat.not_lt_zero i)
  | cons x xs ih =>
    cases i with
    | zero => rfl
    | succ k =>
      have hk : k < xs.length := Nat.lt_of_succ_lt_succ h
      exact ih hk

/-- Every accepted event keeps every datum. -/
theorem step_data_le {r r' : Regime} {e : Event} (h : stepE r e = some r') :
    r.data ≤ r'.data := by
  cases e with
  | supply t =>
    cases Option.some.inj h
    exact Nat.le_refl _
  | admitDatum =>
    cases Option.some.inj h
    exact Nat.le_succ _
  | admitForm a =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      exact Nat.le_refl _
    · cases h
  | admitInst f args =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      exact Nat.le_refl _
    · cases h
  | admitRuleAll f =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      exact Nat.le_refl _
    · cases h
  | impose i j =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      exact Nat.le_refl _
    · cases h

/-- An accepted event that is neither an instance nor a rule admission
keeps every well-formed context well formed and leaves derivability of
every instance as it was. -/
theorem ctx_step_keep {r r' : Regime} {e : Event}
    (hi : ∀ f args, e ≠ .admitInst f args) (hr : ∀ f, e ≠ .admitRuleAll f)
    (h : stepE r e = some r') :
    (∀ c, wfCtx r c → wfCtx r' c) ∧ (∀ i, derivable r' i ↔ derivable r i) := by
  cases e with
  | supply t =>
    cases Option.some.inj h
    exact ⟨fun _ hc => hc, fun _ => Iff.rfl⟩
  | admitDatum =>
    cases Option.some.inj h
    refine ⟨?_, fun _ => Iff.rfl⟩
    intro c hc
    obtain ⟨hf, hlen, hhole, hslots⟩ := hc
    refine ⟨hf, hlen, hhole, ?_⟩
    intro t ht
    cases t with
    | none => trivial
    | some x => exact Nat.lt_succ_of_lt (hslots (some x) ht)
  | admitForm a =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      refine ⟨?_, fun _ => Iff.rfl⟩
      intro c hc
      obtain ⟨hf, hlen, hhole, hslots⟩ := hc
      refine ⟨?_, ?_, hhole, hslots⟩
      · show c.form < (r.forms ++ [a]).length
        rw [List.length_append]
        exact Nat.lt_succ_of_lt hf
      · show c.slots.length = (r.forms ++ [a]).getD c.form 0
        rw [getD_append_lt r.forms a hf]
        exact hlen
    · cases h
  | admitInst f args => exact absurd rfl (hi f args)
  | admitRuleAll f => exact absurd rfl (hr f)
  | impose i j =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      exact ⟨fun _ hc => hc, fun _ => Iff.rfl⟩
    · cases h

/-- Every accepted event that is neither an instance admission nor a
rule admission keeps a separable pair separable (rung nine's
statement). -/
theorem separable_step_keep {r r' : Regime} {e : Event} {d d' : Nat}
    (hi : ∀ f args, e ≠ .admitInst f args) (hr : ∀ f, e ≠ .admitRuleAll f)
    (h : stepE r e = some r') (hs : separable r d d') : separable r' d d' := by
  obtain ⟨hc, hder⟩ := ctx_step_keep hi hr h
  obtain ⟨c, hwc, hne⟩ := hs
  exact ⟨c, hc c hwc, by rw [hder, hder]; exact hne⟩

/-- Those four kinds keep a distinguishing form distinguishing. -/
theorem distinguishes_step_keep {r r' : Regime} {e : Event} {f : Nat}
    (hi : ∀ g args, e ≠ .admitInst g args) (hr : ∀ g, e ≠ .admitRuleAll g)
    (h : stepE r e = some r') (hs : Distinguishes r f) : Distinguishes r' f := by
  obtain ⟨hc, hder⟩ := ctx_step_keep hi hr h
  have hle := step_data_le h
  obtain ⟨c, d, d', hwc, hf, hd, hd', hne⟩ := hs
  exact ⟨c, d, d', hc c hwc, hf, Nat.lt_of_lt_of_le hd hle,
    Nat.lt_of_lt_of_le hd' hle, by rw [hder, hder]; exact hne⟩

/-- A supply, a requirement, a form admission and a rule admission keep
every exhausted admitted form exhausted. -/
theorem exhausted_step_keep {r r' : Regime} {e : Event} {f : Nat}
    (hd : e ≠ .admitDatum) (hi : ∀ g args, e ≠ .admitInst g args)
    (h : stepE r e = some r') (hf : f < r.forms.length) (hx : Exhausted r f) :
    Exhausted r' f := by
  cases e with
  | supply t =>
    cases Option.some.inj h
    exact hx
  | admitDatum => exact absurd rfl hd
  | admitForm a =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      intro c hc hcf x x' hxd hxd'
      obtain ⟨_, hlen, hhole, hslots⟩ := hc
      have hcl : c.form < r.forms.length := by rw [hcf]; exact hf
      have hwc : wfCtx r c := by
        refine ⟨hcl, ?_, hhole, hslots⟩
        have e : (r.forms ++ [a]).getD c.form 0 = r.forms.getD c.form 0 :=
          getD_append_lt r.forms a hcl
        exact hlen.trans e
      exact hx c hwc hcf x x' hxd hxd'
    · cases h
  | admitInst g args => exact absurd rfl (hi g args)
  | admitRuleAll g =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      intro c hc hcf x x' hxd hxd'
      by_cases hg : c.form = g
      · have hm : c.form ∈ insertNew r.rules g := mem_insertNew.mpr (Or.inr hg)
        exact iff_of_true (Or.inr hm) (Or.inr hm)
      · have key : ∀ y, derivable { r with rules := insertNew r.rules g } (plug c y) ↔
            derivable r (plug c y) := by
          intro y
          show (plug c y ∈ r.insts ∨ c.form ∈ insertNew r.rules g) ↔
            (plug c y ∈ r.insts ∨ c.form ∈ r.rules)
          rw [mem_insertNew]
          constructor
          · intro hy
            rcases hy with hy | hy | hy
            · exact Or.inl hy
            · exact Or.inr hy
            · exact absurd hy hg
          · intro hy
            rcases hy with hy | hy
            · exact Or.inl hy
            · exact Or.inr (Or.inl hy)
        rw [key, key]
        exact hx c hc hcf x x' hxd hxd'
    · cases h
  | impose i j =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      exact hx
    · cases h

/-- A form admission to a well-formed regime adds an exhausted form. -/
theorem fresh_form_exhausted {r r' : Regime} {a : Nat} (hwf : r.wf)
    (h : stepE r (.admitForm a) = some r') : Exhausted r' r.forms.length := by
  simp only [stepE] at h
  split at h
  · cases Option.some.inj h
    apply exhausted_of_no_inst
    intro p hp heq
    have hlt := (hwf.1 p hp).1
    rw [heq] at hlt
    exact Nat.lt_irrefl _ hlt
  · cases h

/-- An instance admission can begin the exhaustion of a form. -/
theorem exhaustion_begun_by_inst :
    ∃ r r', r.wf ∧ Distinguishes r 0 ∧ stepE r (.admitInst 0 [1]) = some r' ∧
      Exhausted r' 0 := by
  refine ⟨⟨2, [1], [(0, [0])], [], []⟩, ⟨2, [1], [(0, [0]), (0, [1])], [], []⟩,
    by unfold Regime.wf; decide,
    ⟨⟨0, [none]⟩, 0, 1, by decide, rfl, by decide, by decide, by decide⟩,
    by decide, ?_⟩
  intro c hc _ d d' hd hd'
  obtain ⟨form, slots⟩ := c
  obtain ⟨hf, hlen, hhole, _⟩ := hc
  have hf0 : form = 0 := by
    have h1 : form < 1 := hf
    exact Nat.eq_zero_of_le_zero (Nat.le_of_lt_succ h1)
  subst hf0
  have hl : slots.length = 1 := hlen
  match slots, hl, hhole with
  | [none], _, _ =>
    have key : ∀ x, x < 2 →
        derivable ⟨2, [1], [(0, [0]), (0, [1])], [], []⟩ (plug ⟨0, [none]⟩ x) := by
      intro x hx
      rcases x with _ | _ | x
      · decide
      · decide
      · have h2 : x + 1 + 1 < 2 := hx
        exact absurd h2 (by omega)
    exact iff_of_true (key d hd) (key d' hd')
  | [some y], _, hhole => simp at hhole

/-- A rule admission can begin the exhaustion of a form. -/
theorem exhaustion_begun_by_rule :
    ∃ r r', r.wf ∧ Distinguishes r 0 ∧ stepE r (.admitRuleAll 0) = some r' ∧
      Exhausted r' 0 :=
  ⟨⟨2, [1], [(0, [0])], [], []⟩, ⟨2, [1], [(0, [0])], [0], []⟩,
    by unfold Regime.wf; decide,
    ⟨⟨0, [none]⟩, 0, 1, by decide, rfl, by decide, by decide, by decide⟩,
    by decide, exhausted_of_rule (by decide)⟩

/-- A datum admission can end the exhaustion of a form. -/
theorem exhaustion_ended_by_datum :
    ∃ r r', r.wf ∧ Exhausted r 0 ∧ stepE r .admitDatum = some r' ∧
      Distinguishes r' 0 :=
  ⟨⟨1, [1], [(0, [0])], [], []⟩, ⟨2, [1], [(0, [0])], [], []⟩,
    by unfold Regime.wf; decide, exhausted_of_le_one (by decide) 0, by decide,
    ⟨⟨0, [none]⟩, 0, 1, by decide, rfl, by decide, by decide, by decide⟩⟩

/-- An instance admission can end the exhaustion of a form. -/
theorem exhaustion_ended_by_inst :
    ∃ r r', r.wf ∧ Exhausted r 0 ∧ stepE r (.admitInst 0 [0]) = some r' ∧
      Distinguishes r' 0 :=
  ⟨⟨2, [1], [], [], []⟩, ⟨2, [1], [(0, [0])], [], []⟩,
    by unfold Regime.wf; decide,
    exhausted_of_no_inst (fun p hp => absurd hp (List.not_mem_nil)), by decide,
    ⟨⟨0, [none]⟩, 0, 1, by decide, rfl, by decide, by decide, by decide⟩⟩

end ExhaustStep
end SecondResponse
