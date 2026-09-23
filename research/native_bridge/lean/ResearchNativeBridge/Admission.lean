import Derivation.Erasure
import ResearchNativeBridge.Path

/-!
# Paths of the sealed admission kernel

AuthorityEffect: None.  The sealed admission step `Derivation.stepE` may
refuse: an ill-formed admission returns `none`.  A path here is a chain
of successful steps, each carrying the equation that the sealed step
returned its next state.

Proved here:

* `PPath.run_events`, `PPath.events_ofEventsM`: a path's events replay
  under the sealed `replayE` to its end, and every successful replay is a
  path with exactly those events.
* `PPath.events_injective`: paths with the same endpoints and events are
  equal.
* `PPath.append`, `PPath.events_append`: paths compose.
* `stepE_keep_or_grow`, `admission_cycle`: every successful admission
  step keeps the regime or strictly grows its size, so every regime on a
  cycle through `r` is `r`.  The admission kernel has no nontrivial
  cycle, unlike the passage dynamics.
* `liftT`, `events_liftT`: every token-aware path maps to an admission
  path between the erased endpoints, whose events are the sealed
  `eraseHistory` of the token-aware events.
-/

namespace ResearchNativeBridge

open Derivation

/-- Replay in the option monad. -/
def runM {σ ε : Type} (g : σ → ε → Option σ) (l : List ε) (s : σ) : Option σ :=
  l.foldlM g s

theorem runM_cons {σ ε : Type} (g : σ → ε → Option σ) (e : ε) (l : List ε) (s : σ) :
    runM g (e :: l) s = (g s e).bind (fun m => runM g l m) := by
  unfold runM
  cases h : g s e <;> simp [List.foldlM, h]

/-- A chain of successful steps of an option-valued step function. -/
inductive PPath {σ ε : Type} (g : σ → ε → Option σ) : σ → σ → Type where
  | nil (s : σ) : PPath g s s
  | cons {s m t : σ} (e : ε) (h : g s e = some m) (rest : PPath g m t) : PPath g s t

namespace PPath

variable {σ ε : Type} {g : σ → ε → Option σ}

def events : {s t : σ} → PPath g s t → List ε
  | _, _, .nil _ => []
  | _, _, .cons e _ rest => e :: events rest

theorem run_events {s t : σ} (τ : PPath g s t) : runM g (events τ) s = some t := by
  induction τ with
  | nil _ => rfl
  | cons e h _ ih => rw [events, runM_cons, h]; exact ih

/-- Every successful replay is a path. -/
def ofEventsM (g : σ → ε → Option σ) :
    (s : σ) → (l : List ε) → (t : σ) → runM g l s = some t → PPath g s t
  | s, [], t, h => by
      have hst : s = t := Option.some.inj h
      exact hst ▸ PPath.nil s
  | s, e :: l, t, h =>
      match hg : g s e with
      | none => by rw [runM_cons, hg] at h; simp at h
      | some m =>
          PPath.cons e hg (ofEventsM g m l t (by rw [runM_cons, hg] at h; exact h))

theorem events_cast {s t t' : σ} (h : t = t') (τ : PPath g s t) :
    events (h ▸ τ) = events τ := by
  subst h; rfl

theorem events_ofEventsM (s : σ) (l : List ε) (t : σ) (h : runM g l s = some t) :
    events (ofEventsM g s l t h) = l := by
  induction l generalizing s with
  | nil =>
      simp only [ofEventsM]
      rw [events_cast]
      rfl
  | cons e rest ih =>
      unfold ofEventsM
      split
      · rename_i hg
        rw [runM_cons, hg] at h
        cases h
      · rename_i m hg
        exact congrArg (List.cons e) (ih m _)

theorem events_injective {s t : σ} (τ τ' : PPath g s t)
    (h : events τ = events τ') : τ = τ' := by
  induction τ with
  | nil _ =>
      cases τ' with
      | nil _ => rfl
      | cons _ _ _ => cases h
  | @cons s m t e hg rest ih =>
      cases τ' with
      | nil _ => cases h
      | @cons _ m' _ e' hg' rest' =>
          simp only [events, List.cons.injEq] at h
          obtain ⟨rfl, hrest⟩ := h
          have hm : m = m' := Option.some.inj (hg.symm.trans hg')
          subst hm
          rw [ih rest' hrest]

def append : {s t w : σ} → PPath g s t → PPath g t w → PPath g s w
  | _, _, _, .nil _, q => q
  | _, _, _, .cons e h rest, q => .cons e h (append rest q)

theorem events_append {s t w : σ} (p : PPath g s t) (q : PPath g t w) :
    events (append p q) = events p ++ events q := by
  induction p with
  | nil _ => rfl
  | cons e _ _ ih => exact congrArg (List.cons e) (ih q)

theorem measure_mono (μ : σ → Nat) (hmono : ∀ s e m, g s e = some m → μ s ≤ μ m)
    {s t : σ} (τ : PPath g s t) : μ s ≤ μ t := by
  induction τ with
  | nil _ => exact Nat.le_refl _
  | cons e h _ ih => exact Nat.le_trans (hmono _ e _ h) ih

theorem eq_of_measure_eq (μ : σ → Nat)
    (hgrow : ∀ s e m, g s e = some m → m = s ∨ μ s < μ m)
    {s t : σ} (τ : PPath g s t) (hle : μ t ≤ μ s) : t = s := by
  have hmono : ∀ s e m, g s e = some m → μ s ≤ μ m := by
    intro s e m h
    rcases hgrow s e m h with h' | h'
    · rw [h']; exact Nat.le_refl _
    · exact Nat.le_of_lt h'
  induction τ with
  | nil _ => rfl
  | @cons s m t e h rest ih =>
      have h2 : μ m ≤ μ t := measure_mono μ hmono rest
      rcases hgrow s e m h with hm | hm
      · subst hm; exact ih hle
      · exact absurd (Nat.lt_of_lt_of_le hm (Nat.le_trans h2 hle)) (Nat.lt_irrefl _)

theorem cycle_eq (μ : σ → Nat)
    (hgrow : ∀ s e m, g s e = some m → m = s ∨ μ s < μ m)
    {s t : σ} (p : PPath g s t) (q : PPath g t s) : t = s := by
  have hmono : ∀ s e m, g s e = some m → μ s ≤ μ m := by
    intro s e m h
    rcases hgrow s e m h with h' | h'
    · rw [h']; exact Nat.le_refl _
    · exact Nat.le_of_lt h'
  exact eq_of_measure_eq μ hgrow p (measure_mono μ hmono q)

end PPath

/-- The sealed admission step's paths. -/
abbrev APath := PPath stepE

theorem runM_stepE (l : List Event) (r : Regime) : runM stepE l r = replayE l r := rfl

/-- Size of a regime: data plus the lengths of its four stores. -/
def rsize (r : Regime) : Nat :=
  r.data + r.forms.length + r.insts.length + r.rules.length + r.reqs.length

theorem insertNew_keep_or_grow {α : Type} [DecidableEq α] (l : List α) (a : α) :
    insertNew l a = l ∨ l.length < (insertNew l a).length := by
  by_cases h : a ∈ l
  · left; exact insertNew_of_mem h
  · right; rw [insertNew_of_not_mem h, List.length_append]; simp

/-- **Every successful admission step keeps the regime or grows it.** -/
theorem stepE_keep_or_grow (r : Regime) (e : Event) (m : Regime)
    (h : stepE r e = some m) : m = r ∨ rsize r < rsize m := by
  cases e with
  | supply tok =>
      left; simp only [stepE, Option.some.injEq] at h; exact h.symm
  | admitDatum =>
      right; simp only [stepE, Option.some.injEq] at h; subst h
      simp only [rsize]; omega
  | admitForm a =>
      right; simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h; subst h
        simp only [rsize, List.length_append, List.length_singleton]; omega
      · cases h
  | admitInst f args =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h; subst h
        rcases insertNew_keep_or_grow r.insts (f, args) with hk | hk
        · left; rw [hk]
        · right; simp only [rsize]; omega
      · cases h
  | admitRuleAll f =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h; subst h
        rcases insertNew_keep_or_grow r.rules f with hk | hk
        · left; rw [hk]
        · right; simp only [rsize]; omega
      · cases h
  | impose i j =>
      simp only [stepE] at h
      split at h
      · simp only [Option.some.injEq] at h; subst h
        rcases insertNew_keep_or_grow r.reqs (i, j) with hk | hk
        · left; rw [hk]
        · right; simp only [rsize]; omega
      · cases h

/-- **The admission kernel has no nontrivial cycle.** -/
theorem admission_cycle {r t : Regime} (p : APath r t) (q : APath t r) : t = r :=
  PPath.cycle_eq rsize stepE_keep_or_grow p q

/-! ## Token erasure as a path map -/

abbrev TPath := PPath stepT

theorem stepE_erase (t : TRegime) (e : TEvent) (m : TRegime) (h : stepT t e = some m) :
    stepE t.erase (eraseEvent t e) = some m.erase := by
  rw [← erase_step t e, h]
  rfl

/-- Every token-aware path maps to an admission path between the erased
endpoints. -/
def liftT : {t u : TRegime} → TPath t u → APath t.erase u.erase
  | _, _, .nil t => .nil t.erase
  | t, _, .cons e h rest => .cons (eraseEvent t e) (stepE_erase t e _ h) (liftT rest)

theorem events_liftT {t u : TRegime} (τ : TPath t u) :
    PPath.events (liftT τ) = eraseHistory t (PPath.events τ) := by
  induction τ with
  | nil _ => rfl
  | @cons t m u e h rest ih =>
      show eraseEvent t e :: PPath.events (liftT rest) =
        eraseHistory t (e :: PPath.events rest)
      rw [ih]
      simp only [eraseHistory, h]

end ResearchNativeBridge
