import SecondRun.Kernel

/-!
# What no run can undo

Native to continuation two.

An engine of continuation one changes its state only by the admission
events of a response, the supply and admission of growth, and the switch
marker.  Here those are EVERY history of sealed events and switch
markers, whoever chose it: nothing below mentions a demand, a response,
a minimum, a key or a run graph, because the sealed candidate space, the
responder and the generators are not reconstructed in Lean.  So each
statement holds for every run of every engine of the class, and for
every other history of the same events.

* `elems r`: the number of data plus the lengths of the lists of forms,
  instances, uniform rules and requirements.
* `stepE_elems_le`, `stepE_elems_lt_of_ne`: no sealed step lowers the
  element count, and a step that changes the regime raises it.
* `estep_elems_le`, `estep_elems_lt_of_ne`, `switch_keeps_regime`,
  `switch_switch`: the same for engine events; the switch marker keeps
  the regime, and two switch markers return the state.
* `ereplay_elems_le`, `ereplay_regime_eq_of_elems_eq`,
  `ereplay_elems_lt_of_ne`: along a history the element count never
  falls, and it stays put exactly when the regime does.
* `no_return`: after a history that changes the regime, no further
  history reaches a state holding the first regime.
* `cycle_regime_const`: on a history that returns to its starting state,
  the state reached part of the way holds the starting regime.
* `collapsed_through`, `not_separable_through`: a pair collapsed with a
  common third datum is collapsed, and so not separable, in any regime.

AuthorityEffect: None.
-/

namespace SecondRun
namespace Run

open Sealed

/-- The element count of a regime. -/
def elems (r : Regime) : Nat :=
  r.data + r.forms.length + r.insts.length + r.rules.length + r.reqs.length

/-- Deduplicating insertion never shortens a list. -/
theorem insertNew_length_le {α : Type} [DecidableEq α] (l : List α) (a : α) :
    l.length ≤ (insertNew l a).length := by
  unfold insertNew
  split <;> simp

/-- Deduplicating insertion leaves the list or lengthens it by one. -/
theorem insertNew_eq_or_succ {α : Type} [DecidableEq α] (l : List α) (a : α) :
    insertNew l a = l ∨ (insertNew l a).length = l.length + 1 := by
  unfold insertNew
  split
  · exact Or.inl rfl
  · exact Or.inr (by simp)

/-- No sealed step lowers the element count. -/
theorem stepE_elems_le {r r' : Regime} {e : Event} (h : stepE r e = some r') :
    elems r ≤ elems r' := by
  cases e with
  | supply t =>
      simp only [stepE, Option.some.injEq] at h
      subst h
      exact Nat.le_refl _
  | admitDatum =>
      simp only [stepE, Option.some.injEq] at h
      subst h
      simp only [elems]
      omega
  | admitForm a =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        simp only [elems, List.length_append, List.length_cons, List.length_nil]
        omega
      · cases h
  | admitInst f args =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        have := insertNew_length_le r.insts (f, args)
        simp only [elems]
        omega
      · cases h
  | admitRuleAll f =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        have := insertNew_length_le r.rules f
        simp only [elems]
        omega
      · cases h
  | impose i j =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        have := insertNew_length_le r.reqs (i, j)
        simp only [elems]
        omega
      · cases h

/-- A sealed step that changes the regime raises the element count. -/
theorem stepE_elems_lt_of_ne {r r' : Regime} {e : Event} (h : stepE r e = some r')
    (hne : r' ≠ r) : elems r < elems r' := by
  cases e with
  | supply t =>
      simp only [stepE, Option.some.injEq] at h
      exact absurd h.symm hne
  | admitDatum =>
      simp only [stepE, Option.some.injEq] at h
      subst h
      simp only [elems]
      omega
  | admitForm a =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        simp only [elems, List.length_append, List.length_cons, List.length_nil]
        omega
      · cases h
  | admitInst f args =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        rcases insertNew_eq_or_succ r.insts (f, args) with heq | hlen
        · exact absurd (by rw [heq]) hne
        · simp only [elems]
          omega
      · cases h
  | admitRuleAll f =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        rcases insertNew_eq_or_succ r.rules f with heq | hlen
        · exact absurd (by rw [heq]) hne
        · simp only [elems]
          omega
      · cases h
  | impose i j =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h
        subst h
        rcases insertNew_eq_or_succ r.reqs (i, j) with heq | hlen
        · exact absurd (by rw [heq]) hne
        · simp only [elems]
          omega
      · cases h

/-- An engine event: a sealed event, or the switch marker. -/
inductive EEvent where
  | sealed (e : Event)
  | switch

/-- An engine state: a regime and the mode, `true` when flipped. -/
structure EState where
  regime : Regime
  flipped : Bool
deriving DecidableEq

/-- One engine event: a sealed event steps the regime by the sealed step,
the switch marker flips the mode and keeps the regime. -/
def estep (s : EState) : EEvent → Option EState
  | .sealed e => (stepE s.regime e).map (fun r => { s with regime := r })
  | .switch => some { s with flipped := !s.flipped }

/-- The engine's replay: the fold of `estep`, all or nothing. -/
def ereplay (h : List EEvent) (s : EState) : Option EState :=
  h.foldlM estep s

/-- The switch marker keeps the regime. -/
theorem switch_keeps_regime (s t : EState) (h : estep s .switch = some t) :
    t.regime = s.regime := by
  simp only [estep, Option.some.injEq] at h
  rw [← h]

/-- Two switch markers return the state. -/
theorem switch_switch (s : EState) :
    (estep s .switch).bind (fun t => estep t .switch) = some s := by
  cases s
  simp [estep]

/-- No engine event lowers the element count. -/
theorem estep_elems_le {s t : EState} {e : EEvent} (h : estep s e = some t) :
    elems s.regime ≤ elems t.regime := by
  cases e with
  | sealed e =>
      simp only [estep, Option.map_eq_some_iff] at h
      obtain ⟨r, hr, rfl⟩ := h
      exact stepE_elems_le hr
  | switch =>
      rw [switch_keeps_regime s t h]
      exact Nat.le_refl _

/-- An engine event that changes the regime raises the element count. -/
theorem estep_elems_lt_of_ne {s t : EState} {e : EEvent} (h : estep s e = some t)
    (hne : t.regime ≠ s.regime) : elems s.regime < elems t.regime := by
  cases e with
  | sealed e =>
      simp only [estep, Option.map_eq_some_iff] at h
      obtain ⟨r, hr, rfl⟩ := h
      exact stepE_elems_lt_of_ne hr hne
  | switch =>
      exact absurd (switch_keeps_regime s t h) hne

/-- No history of engine events lowers the element count. -/
theorem ereplay_elems_le (h : List EEvent) {s t : EState} (hr : ereplay h s = some t) :
    elems s.regime ≤ elems t.regime := by
  induction h generalizing s with
  | nil =>
      simp only [ereplay, List.foldlM, Option.pure_def, Option.some.injEq] at hr
      rw [hr]
      exact Nat.le_refl _
  | cons e es ih =>
      simp only [ereplay, List.foldlM] at hr
      cases hs : estep s e with
      | none => rw [hs] at hr; cases hr
      | some u =>
          rw [hs] at hr
          exact Nat.le_trans (estep_elems_le hs) (ih hr)

/-- A history that leaves the element count unchanged leaves the regime
unchanged. -/
theorem ereplay_regime_eq_of_elems_eq (h : List EEvent) {s t : EState}
    (hr : ereplay h s = some t) (he : elems t.regime = elems s.regime) :
    t.regime = s.regime := by
  induction h generalizing s with
  | nil =>
      simp only [ereplay, List.foldlM, Option.pure_def, Option.some.injEq] at hr
      rw [hr]
  | cons e es ih =>
      simp only [ereplay, List.foldlM] at hr
      cases hs : estep s e with
      | none => rw [hs] at hr; cases hr
      | some u =>
          rw [hs] at hr
          have h1 := estep_elems_le hs
          have h2 := ereplay_elems_le es hr
          have hu : u.regime = s.regime := by
            cases Nat.lt_or_eq_of_le h1 with
            | inl hlt => omega
            | inr heq =>
                exact ((Decidable.em (u.regime = s.regime)).elim id
                  (fun hne => absurd heq (Nat.ne_of_lt (estep_elems_lt_of_ne hs hne))))
          have ht : t.regime = u.regime := ih hr (by omega)
          rw [ht, hu]

/-- A history that changes the regime raises the element count. -/
theorem ereplay_elems_lt_of_ne (h : List EEvent) {s t : EState}
    (hr : ereplay h s = some t) (hne : t.regime ≠ s.regime) :
    elems s.regime < elems t.regime := by
  have hle := ereplay_elems_le h hr
  cases Nat.lt_or_eq_of_le hle with
  | inl hlt => exact hlt
  | inr heq => exact absurd (ereplay_regime_eq_of_elems_eq h hr heq.symm) hne

/-- After a history that changes the regime, no further history reaches a
state holding the first regime. -/
theorem no_return (h₁ h₂ : List EEvent) {s t u : EState}
    (h1 : ereplay h₁ s = some t) (hne : t.regime ≠ s.regime)
    (h2 : ereplay h₂ t = some u) : u.regime ≠ s.regime := by
  intro heq
  have hlt := ereplay_elems_lt_of_ne h₁ h1 hne
  have hle := ereplay_elems_le h₂ h2
  rw [heq] at hle
  omega

/-- On a history that returns to its starting state, the state reached
part of the way holds the starting regime. -/
theorem cycle_regime_const (h₁ h₂ : List EEvent) {s t : EState}
    (h1 : ereplay h₁ s = some t) (h2 : ereplay h₂ t = some s) :
    t.regime = s.regime := by
  have a := ereplay_elems_le h₁ h1
  have b := ereplay_elems_le h₂ h2
  exact ereplay_regime_eq_of_elems_eq h₁ h1 (by omega)

/-- Collapse through a common third datum is collapse. -/
theorem collapsed_through {r : Regime} {a b c : Nat} (h1 : collapsed r a c)
    (h2 : collapsed r b c) : collapsed r a b :=
  fun x hx => (h1 x hx).trans (h2 x hx).symm

/-- A pair collapsed with a common third datum is not separable, in any
regime.  So a history that keeps both of those pairs collapsed, whatever
its length, leaves the pair collapsed: the refused apart demands of the
runs have this shape. -/
theorem not_separable_through {r : Regime} {a b c : Nat} (h1 : collapsed r a c)
    (h2 : collapsed r b c) : ¬ separable r a b :=
  fun hs => separable_not_collapsed hs (collapsed_through h1 h2)

end Run
end SecondRun
