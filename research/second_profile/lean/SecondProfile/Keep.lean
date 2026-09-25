import SecondProfile.Kernel
import SecondProfile.Classes
import SecondProfile.Stage

/-!
# Which events keep holding two, and which can end it

Native to rung nine.

* `separable_step_keep`: for every regime, every pair of data and every
  event that the sealed step accepts and that is neither an instance
  admission nor a rule admission, a pair separable before the event is
  separable after it.  No hypothesis on the regime.  A supply and a
  requirement change nothing derivability reads; a datum admission only
  widens the admitted range of a slot; a form admission appends a form,
  and a well-formed context of the old forms reads the same arity
  (`getD_append_lt`).
* `holdsTwo_step_keep`: so those four kinds keep holding two.
* `twoness_lost_by_inst`, `twoness_lost_by_rule`: the other two kinds
  can end it.  Each exhibits a well-formed regime that holds two -- two
  data, one form of arity one, and its instance at the first datum --
  and one accepted event after which no two admitted data are separable:
  the instance of the form at the second datum, or the uniform rule of
  the form.

`getD_append_lt` repeats, as a statement, rung five's lemma of the same
name, proved again at rung eight; it is proved again here so that this
package imports nothing.

AuthorityEffect: None.
-/

namespace SecondProfile
namespace Keep

open Sealed
open Classes (HoldsTwo)
open Stage (step_parts_le)

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

/-- Every accepted event that is neither an instance admission nor a
rule admission keeps a separable pair separable. -/
theorem separable_step_keep {r r' : Regime} {e : Event} {d d' : Nat}
    (hi : ∀ f args, e ≠ .admitInst f args) (hr : ∀ f, e ≠ .admitRuleAll f)
    (h : stepE r e = some r') (hs : separable r d d') : separable r' d d' := by
  obtain ⟨c, hc, hne⟩ := hs
  cases e with
  | supply t =>
    cases Option.some.inj h
    exact ⟨c, hc, hne⟩
  | admitDatum =>
    cases Option.some.inj h
    obtain ⟨hf, hlen, hhole, hslots⟩ := hc
    refine ⟨c, ⟨hf, hlen, hhole, ?_⟩, hne⟩
    intro t ht
    cases t with
    | none => trivial
    | some x => exact Nat.lt_succ_of_lt (hslots (some x) ht)
  | admitForm a =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      obtain ⟨hf, hlen, hhole, hslots⟩ := hc
      refine ⟨c, ⟨?_, ?_, hhole, hslots⟩, hne⟩
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
      exact ⟨c, hc, hne⟩
    · cases h

/-- Those four kinds keep holding two. -/
theorem holdsTwo_step_keep {r r' : Regime} {e : Event}
    (hi : ∀ f args, e ≠ .admitInst f args) (hr : ∀ f, e ≠ .admitRuleAll f)
    (h : stepE r e = some r') (ht : HoldsTwo r) : HoldsTwo r' := by
  obtain ⟨d, d', hd, hd', hs⟩ := ht
  have hle := (step_parts_le h).2
  exact ⟨d, d', Nat.lt_of_lt_of_le hd hle, Nat.lt_of_lt_of_le hd' hle,
    separable_step_keep hi hr h hs⟩

/-- An instance admission can end holding two. -/
theorem twoness_lost_by_inst :
    ∃ r r', r.wf ∧ HoldsTwo r ∧ stepE r (.admitInst 0 [1]) = some r' ∧
      ¬ HoldsTwo r' := by
  refine ⟨⟨2, [1], [(0, [0])], [], []⟩, ⟨2, [1], [(0, [0]), (0, [1])], [], []⟩,
    by unfold Regime.wf; decide, ⟨0, 1, by decide, by decide, ⟨0, [none]⟩, by decide, by decide⟩,
    by decide, ?_⟩
  intro ⟨d, d', hd, hd', c, hc, hne⟩
  obtain ⟨form, slots⟩ := c
  obtain ⟨hf, hlen, hhole, _⟩ := hc
  have hf0 : form = 0 := by
    have h1 : form < 1 := hf
    omega
  subst hf0
  have hl : slots.length = 1 := hlen
  match slots, hl, hhole with
  | [none], _, _ =>
    apply hne
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

/-- A rule admission can end holding two. -/
theorem twoness_lost_by_rule :
    ∃ r r', r.wf ∧ HoldsTwo r ∧ stepE r (.admitRuleAll 0) = some r' ∧
      ¬ HoldsTwo r' := by
  refine ⟨⟨2, [1], [(0, [0])], [], []⟩, ⟨2, [1], [(0, [0])], [0], []⟩,
    by unfold Regime.wf; decide, ⟨0, 1, by decide, by decide, ⟨0, [none]⟩, by decide, by decide⟩,
    by decide, ?_⟩
  intro ⟨d, d', _, _, c, hc, hne⟩
  have hf0 : c.form = 0 := by
    have h1 : c.form < 1 := hc.1
    omega
  have key : ∀ x, derivable ⟨2, [1], [(0, [0])], [0], []⟩ (plug c x) := by
    intro x
    refine Or.inr ?_
    show c.form ∈ [0]
    rw [hf0]
    exact List.mem_singleton_self 0
  exact hne (iff_of_true (key d) (key d'))

end Keep
end SecondProfile
