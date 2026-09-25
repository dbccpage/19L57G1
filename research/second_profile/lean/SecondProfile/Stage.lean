import SecondProfile.Kernel
import SecondProfile.Classes

/-!
# What holding two needs, and when it is first reached

Native to rung nine.

* `holdsTwo_parts`: a regime that holds two has at least two data, at
  least one form and at least one instance, with no hypothesis on the
  regime.
* `parts r` is the number of data plus the lengths of the lists of forms
  and of instances.  `step_parts_le`: every event the sealed step accepts
  raises `parts` by at most one and lowers no number of data;
  `replay_parts_le`: so a history reaches a regime whose `parts` is at
  most the base's plus the length of the history, with at least the
  base's data.
* `twoness_needs_four`: every history from the sealed empty regime that
  reaches a regime holding two has at least four events.
  `twoness_needs_two_L`, `twoness_needs_two_F`: from each sealed Lean
  reading regime, at least two.
* `twoness_at_four`, `twoness_at_two_L`, `twoness_at_two_F`: each bound
  is attained, by kernel computation on an exhibited history -- a datum,
  a datum, a form of arity one and the instance of that form at the
  first datum; from a reading regime, the last two of those.
* `two_classes_at_four`: at the regime `twoness_at_four` reaches, the
  two data form a representative list.

The sealed Lean reading regimes hold a requirement between two data, and
the Python bases of the rectangle do not; requirements do not enter
derivability, so the bounds and the witnesses read the same in both.

AuthorityEffect: None.
-/

namespace SecondProfile
namespace Stage

open Sealed
open Classes (HoldsTwo Reps no_twoness_without_insts collapsed_refl)

/-- The number of data plus the lengths of the lists of forms and of
instances. -/
def parts (r : Regime) : Nat := r.data + r.forms.length + r.insts.length

/-- Deduplicating insertion lengthens a list by at most one. -/
theorem insertNew_le {α : Type} [DecidableEq α] (l : List α) (a : α) :
    (insertNew l a).length ≤ l.length + 1 := by
  unfold insertNew
  split <;> simp

/-- Every accepted event raises `parts` by at most one and keeps every
datum. -/
theorem step_parts_le {r r' : Regime} {e : Event} (h : stepE r e = some r') :
    parts r' ≤ parts r + 1 ∧ r.data ≤ r'.data := by
  cases e with
  | supply t =>
    cases Option.some.inj h
    exact ⟨Nat.le_succ _, Nat.le_refl _⟩
  | admitDatum =>
    cases Option.some.inj h
    simp only [parts]
    exact ⟨by omega, by omega⟩
  | admitForm a =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      simp only [parts, List.length_append, List.length_singleton]
      exact ⟨by omega, by omega⟩
    · cases h
  | admitInst f args =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      have := insertNew_le r.insts (f, args)
      simp only [parts]
      exact ⟨by omega, by omega⟩
    · cases h
  | admitRuleAll f =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      simp only [parts]
      exact ⟨by omega, by omega⟩
    · cases h
  | impose i j =>
    simp only [stepE] at h
    split at h
    · cases Option.some.inj h
      simp only [parts]
      exact ⟨by omega, by omega⟩
    · cases h

/-- A history reaches a regime whose `parts` is at most the base's plus
its length, with at least the base's data. -/
theorem replay_parts_le :
    ∀ (h : List Event) (b r : Regime), replayE h b = some r →
      parts r ≤ parts b + h.length ∧ b.data ≤ r.data := by
  intro h
  induction h with
  | nil =>
    intro b r hr
    have hb : b = r := Option.some.inj hr
    subst hb
    exact ⟨Nat.le_add_right _ _, Nat.le_refl _⟩
  | cons e es ih =>
    intro b r hr
    cases hs : stepE b e with
    | none =>
      have hr' : (stepE b e).bind (fun s => replayE es s) = some r := hr
      rw [hs] at hr'
      cases hr'
    | some b' =>
      have hr' : (stepE b e).bind (fun s => replayE es s) = some r := hr
      rw [hs] at hr'
      have h1 := ih b' r hr'
      have h2 := step_parts_le hs
      simp only [List.length_cons]
      exact ⟨by omega, by omega⟩

/-- A regime that holds two has two data, a form and an instance. -/
theorem holdsTwo_parts {r : Regime} (h : HoldsTwo r) :
    2 ≤ r.data ∧ 1 ≤ r.forms.length ∧ 1 ≤ r.insts.length := by
  obtain ⟨d, d', hd, hd', c, hc, hne⟩ := h
  have hdd : d ≠ d' := by
    intro heq
    subst heq
    exact hne Iff.rfl
  have hf := hc.1
  refine ⟨by omega, by omega, ?_⟩
  cases hi : r.insts with
  | nil => exact absurd ⟨d, d', hd, hd', c, hc, hne⟩ (no_twoness_without_insts hi)
  | cons p t => exact Nat.succ_le_succ (Nat.zero_le _)

/-- From the sealed empty regime, holding two needs four events. -/
theorem twoness_needs_four {h : List Event} {r : Regime}
    (hr : replayE h genesis = some r) (ht : HoldsTwo r) : 4 ≤ h.length := by
  have h1 := replay_parts_le h genesis r hr
  have h2 := holdsTwo_parts ht
  have hg : parts genesis = 0 := rfl
  simp only [parts] at h1 hg
  omega

/-- From the sealed Lean reading regime `R2L`, holding two needs two
events. -/
theorem twoness_needs_two_L {h : List Event} {r : Regime}
    (hr : replayE h R2L = some r) (ht : HoldsTwo r) : 2 ≤ h.length := by
  have h1 := replay_parts_le h R2L r hr
  have h2 := holdsTwo_parts ht
  have hg : parts R2L = 2 := rfl
  have hd : R2L.data = 2 := rfl
  simp only [parts] at h1 hg
  omega

/-- From the sealed Lean reading regime `R2F`, holding two needs two
events. -/
theorem twoness_needs_two_F {h : List Event} {r : Regime}
    (hr : replayE h R2F = some r) (ht : HoldsTwo r) : 2 ≤ h.length := by
  have h1 := replay_parts_le h R2F r hr
  have h2 := holdsTwo_parts ht
  have hg : parts R2F = 3 := rfl
  have hd : R2F.data = 3 := rfl
  simp only [parts] at h1 hg
  omega

/-- Four events from the sealed empty regime reach a regime that holds
two. -/
theorem twoness_at_four :
    ∃ r, replayE [.admitDatum, .admitDatum, .admitForm 1, .admitInst 0 [0]]
      genesis = some r ∧ HoldsTwo r :=
  ⟨⟨2, [1], [(0, [0])], [], []⟩, by decide,
    0, 1, by decide, by decide, ⟨0, [none]⟩, by decide, by decide⟩

/-- Two events from `R2L` reach a regime that holds two. -/
theorem twoness_at_two_L :
    ∃ r, replayE [.admitForm 1, .admitInst 0 [0]] R2L = some r ∧ HoldsTwo r :=
  ⟨⟨2, [1], [(0, [0])], [], [(0, 1)]⟩, by decide,
    0, 1, by decide, by decide, ⟨0, [none]⟩, by decide, by decide⟩

/-- Two events from `R2F` reach a regime that holds two. -/
theorem twoness_at_two_F :
    ∃ r, replayE [.admitForm 1, .admitInst 0 [0]] R2F = some r ∧ HoldsTwo r :=
  ⟨⟨3, [1], [(0, [0])], [], [(1, 2)]⟩, by decide,
    0, 1, by decide, by decide, ⟨0, [none]⟩, by decide, by decide⟩

/-- At the regime `twoness_at_four` reaches, the two data form a
representative list. -/
theorem two_classes_at_four : Reps ⟨2, [1], [(0, [0])], [], []⟩ [0, 1] := by
  refine ⟨by decide, ?_, ?_⟩
  · exact List.Pairwise.cons
      (fun y hy => by
        rw [List.mem_singleton.mp hy]
        exact ⟨⟨0, [none]⟩, by decide, by decide⟩)
      (List.pairwise_singleton _ 1)
  · intro d hd
    rcases d with _ | _ | d
    · exact ⟨0, by decide, collapsed_refl _ 0⟩
    · exact ⟨1, by decide, collapsed_refl _ 1⟩
    · have h2 : d + 1 + 1 < 2 := hd
      exact absurd h2 (by omega)

end Stage
end SecondProfile
