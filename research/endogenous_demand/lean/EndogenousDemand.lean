import Derivation.Basic
import Derivation.Inertia

/-!
# The reqs channel of the sealed event grammar

A demand in the sealed machine is a member of `Regime.reqs`.  The event
language is the inductive type `Event`.  This file proves that a pair
enters `reqs` if and only if a successful `impose` of that pair occurs in
the replayed history, and therefore that E2 of the endogenous-demand
brief — a new requirement with no supplying `impose` at that step — is
unsatisfiable on this class.

The class `C_reqs` is exactly that channel: constructs whose demand is
specified to be a member of `reqs` produced by sealed `stepE`.  It is the
class E2 writes down.  It is not a claim about instance-encoded reads
(the represented-execution analogue), which never enter `reqs` and are
recorded as the OPEN remainder of this family.

AuthorityEffect: None.
-/

namespace EndogenousDemand

open Derivation

/-! ## 1. Non-impose constructors leave `reqs` unchanged -/

theorem stepE_reqs_supply (r : Regime) (t : Nat) {s : Regime}
    (h : stepE r (.supply t) = some s) : s.reqs = r.reqs := by
  have h' := supply_no_op r t
  rw [h'] at h
  cases h
  rfl

theorem stepE_admitDatum (r : Regime) :
    stepE r .admitDatum = some { r with data := r.data + 1 } := rfl

theorem stepE_reqs_admitDatum (r : Regime) {s : Regime}
    (h : stepE r .admitDatum = some s) : s.reqs = r.reqs := by
  rw [stepE_admitDatum] at h
  cases h
  rfl

theorem stepE_reqs_admitForm (r : Regime) (a : Nat) {s : Regime}
    (h : stepE r (.admitForm a) = some s) : s.reqs = r.reqs := by
  change (if 1 ≤ a then some { r with forms := r.forms ++ [a] } else none) = some s at h
  split at h
  · cases h; rfl
  · cases h

theorem stepE_reqs_admitInst (r : Regime) (f : Nat) (args : List Nat) {s : Regime}
    (h : stepE r (.admitInst f args) = some s) : s.reqs = r.reqs := by
  change (if f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
      (∀ x ∈ args, x < r.data) then
    some { r with insts := insertNew r.insts (f, args) }
  else none) = some s at h
  split at h
  · cases h; rfl
  · cases h

theorem stepE_reqs_admitRuleAll (r : Regime) (f : Nat) {s : Regime}
    (h : stepE r (.admitRuleAll f) = some s) : s.reqs = r.reqs := by
  change (if f < r.forms.length then
    some { r with rules := insertNew r.rules f }
  else none) = some s at h
  split at h
  · cases h; rfl
  · cases h

/-! ## 2. `impose` is the unique writer of `reqs` -/

theorem stepE_reqs_impose (r : Regime) (i j : Nat) {s : Regime}
    (h : stepE r (.impose i j) = some s) :
    s.reqs = insertNew r.reqs (i, j) := by
  change (if i < j ∧ j < r.data then
    some { r with reqs := insertNew r.reqs (i, j) }
  else none) = some s at h
  split at h
  · cases h; rfl
  · cases h

theorem stepE_reqs_mem {r s : Regime} {e : Event} {p : Nat × Nat}
    (h : stepE r e = some s) :
    p ∈ s.reqs ↔ p ∈ r.reqs ∨ ∃ i j, e = Event.impose i j ∧ p = (i, j) := by
  cases e with
  | supply t =>
      have hs := stepE_reqs_supply r t h
      constructor
      · intro hp; exact Or.inl (hs ▸ hp)
      · intro hcases
        cases hcases with
        | inl hp => exact hs ▸ hp
        | inr hex =>
            obtain ⟨_, _, he, _⟩ := hex
            cases he
  | admitDatum =>
      have hs := stepE_reqs_admitDatum r h
      constructor
      · intro hp; exact Or.inl (hs ▸ hp)
      · intro hcases
        cases hcases with
        | inl hp => exact hs ▸ hp
        | inr hex =>
            obtain ⟨_, _, he, _⟩ := hex
            cases he
  | admitForm a =>
      have hs := stepE_reqs_admitForm r a h
      constructor
      · intro hp; exact Or.inl (hs ▸ hp)
      · intro hcases
        cases hcases with
        | inl hp => exact hs ▸ hp
        | inr hex =>
            obtain ⟨_, _, he, _⟩ := hex
            cases he
  | admitInst f args =>
      have hs := stepE_reqs_admitInst r f args h
      constructor
      · intro hp; exact Or.inl (hs ▸ hp)
      · intro hcases
        cases hcases with
        | inl hp => exact hs ▸ hp
        | inr hex =>
            obtain ⟨_, _, he, _⟩ := hex
            cases he
  | admitRuleAll f =>
      have hs := stepE_reqs_admitRuleAll r f h
      constructor
      · intro hp; exact Or.inl (hs ▸ hp)
      · intro hcases
        cases hcases with
        | inl hp => exact hs ▸ hp
        | inr hex =>
            obtain ⟨_, _, he, _⟩ := hex
            cases he
  | impose i j =>
      have hs := stepE_reqs_impose r i j h
      constructor
      · intro hp
        have hp' : p ∈ insertNew r.reqs (i, j) := hs ▸ hp
        cases (mem_insertNew).1 hp' with
        | inl hin => exact Or.inl hin
        | inr heq => exact Or.inr ⟨i, j, rfl, heq⟩
      · intro hcases
        have : p ∈ insertNew r.reqs (i, j) := by
          cases hcases with
          | inl hin => exact (mem_insertNew).2 (Or.inl hin)
          | inr hex =>
              obtain ⟨i', j', he, hpij⟩ := hex
              cases he
              exact (mem_insertNew).2 (Or.inr hpij)
        exact hs ▸ this

/-! ## 3. Responses never write `reqs` -/

theorem applyItem_reqs {r s : Regime} {it : Item}
    (h : applyItem r it = some s) : s.reqs = r.reqs := by
  cases it with
  | newDatum =>
      change some { r with data := r.data + 1 } = some s at h
      cases h; rfl
  | newForm a =>
      change (if 1 ≤ a then some { r with forms := r.forms ++ [a] } else none) = some s at h
      split at h
      · cases h; rfl
      · cases h
  | newInst f args =>
      change (if f < r.forms.length ∧ args.length = r.forms.getD f 0 ∧
          (∀ x ∈ args, x < r.data) then
        some { r with insts := insertNew r.insts (f, args) }
      else none) = some s at h
      split at h
      · cases h; rfl
      · cases h
  | newRuleAll f =>
      change (if f < r.forms.length then
        some { r with rules := insertNew r.rules f }
      else none) = some s at h
      split at h
      · cases h; rfl
      · cases h

theorem applyDelta_nil (r : Regime) : applyDelta r [] = some r := rfl

theorem applyDelta_cons (r : Regime) (it : Item) (rest : List Item) :
    applyDelta r (it :: rest) = (applyItem r it).bind (fun a => applyDelta a rest) := rfl

theorem applyDelta_reqs {r s : Regime} {δ : List Item}
    (h : applyDelta r δ = some s) : s.reqs = r.reqs := by
  induction δ generalizing r s with
  | nil =>
      rw [applyDelta_nil] at h
      cases h
      rfl
  | cons it rest ih =>
      rw [applyDelta_cons] at h
      cases hItem : applyItem r it with
      | none =>
          rw [hItem] at h
          cases h
      | some r' =>
          rw [hItem] at h
          have hkeep := applyItem_reqs hItem
          have hrest := ih h
          exact hrest.trans hkeep

/-! ## 4. Replay: membership in `reqs` is exactly the impose events -/

theorem replayE_nil (r : Regime) : replayE [] r = some r := rfl

theorem replayE_cons (e : Event) (h : List Event) (r : Regime) :
    replayE (e :: h) r = (stepE r e).bind (replayE h) := rfl

theorem genesis_reqs : genesis.reqs = [] := rfl

theorem replayE_reqs_mem {h : List Event} {r0 r : Regime} {p : Nat × Nat}
    (hr : replayE h r0 = some r) :
    p ∈ r.reqs ↔ p ∈ r0.reqs ∨ ∃ i j, Event.impose i j ∈ h ∧ p = (i, j) := by
  induction h generalizing r0 r with
  | nil =>
      rw [replayE_nil] at hr
      cases hr
      constructor
      · intro hp; exact Or.inl hp
      · intro hcases
        cases hcases with
        | inl hp => exact hp
        | inr hex =>
            obtain ⟨_, _, hin, _⟩ := hex
            cases hin
  | cons e t ih =>
      rw [replayE_cons] at hr
      cases hs : stepE r0 e with
      | none =>
          rw [hs] at hr
          cases hr
      | some s =>
          rw [hs] at hr
          have ih' := ih (r0 := s) hr
          have step := stepE_reqs_mem (p := p) hs
          constructor
          · intro hp
            cases ih'.1 hp with
            | inl hps =>
                cases step.1 hps with
                | inl hin0 => exact Or.inl hin0
                | inr hex =>
                    obtain ⟨i, j, he, hpij⟩ := hex
                    refine Or.inr ⟨i, j, ?_, hpij⟩
                    rw [he]
                    exact List.mem_cons_self
            | inr hex =>
                obtain ⟨i, j, hin, hpij⟩ := hex
                exact Or.inr ⟨i, j, List.mem_cons_of_mem e hin, hpij⟩
          · intro hcases
            cases hcases with
            | inl hin0 =>
                exact ih'.2 (Or.inl (step.2 (Or.inl hin0)))
            | inr hex =>
                obtain ⟨i, j, hin, hpij⟩ := hex
                cases (List.mem_cons.1 hin) with
                | inl he =>
                    exact ih'.2 (Or.inl (step.2 (Or.inr ⟨i, j, he.symm, hpij⟩)))
                | inr ht =>
                    exact ih'.2 (Or.inr ⟨i, j, ht, hpij⟩)

theorem replay_reqs_iff_impose {h : List Event} {r : Regime} {p : Nat × Nat}
    (hr : replayE h genesis = some r) :
    p ∈ r.reqs ↔ ∃ i j, Event.impose i j ∈ h ∧ p = (i, j) := by
  have hmem := replayE_reqs_mem (r0 := genesis) (p := p) hr
  constructor
  · intro hp
    cases hmem.1 hp with
    | inl hin =>
        rw [genesis_reqs] at hin
        cases hin
    | inr hex => exact hex
  · intro hex
    exact hmem.2 (Or.inr hex)

/-! ## 5. E2 is unsatisfiable on `C_reqs` -/

theorem no_reqs_extension_without_impose
    {h : List Event} {e : Event} {r s : Regime} {p : Nat × Nat}
    (_hr : replayE h genesis = some r)
    (hs : stepE r e = some s)
    (hp : p ∈ s.reqs) (hn : p ∉ r.reqs) :
    ∃ i j, e = Event.impose i j := by
  cases (stepE_reqs_mem hs).1 hp with
  | inl hin => exact absurd hin hn
  | inr hex =>
      obtain ⟨i, j, he, _⟩ := hex
      exact ⟨i, j, he⟩

/-- E2 on the reqs channel: the last event is not an impose, yet `reqs` grew. -/
def E2OnCReqs (h : List Event) (e : Event) : Prop :=
  (∀ i j : Nat, e ≠ Event.impose i j) ∧
  ∃ r s : Regime, ∃ p : Nat × Nat,
    replayE h genesis = some r ∧
    stepE r e = some s ∧
    p ∈ s.reqs ∧ p ∉ r.reqs

theorem e2_on_C_reqs_unsat : ∀ h e, ¬ E2OnCReqs h e := by
  intro h e ⟨hne, r, s, p, hr, hs, hp, hn⟩
  obtain ⟨i, j, he⟩ := no_reqs_extension_without_impose hr hs hp hn
  exact hne i j he

/-- The six constructors are the whole event language. -/
theorem event_constructors (e : Event) :
    (∃ t, e = Event.supply t) ∨
    e = Event.admitDatum ∨
    (∃ a, e = Event.admitForm a) ∨
    (∃ f args, e = Event.admitInst f args) ∨
    (∃ f, e = Event.admitRuleAll f) ∨
    (∃ i j, e = Event.impose i j) := by
  cases e with
  | supply t => exact Or.inl ⟨t, rfl⟩
  | admitDatum => exact Or.inr (Or.inl rfl)
  | admitForm a => exact Or.inr (Or.inr (Or.inl ⟨a, rfl⟩))
  | admitInst f args => exact Or.inr (Or.inr (Or.inr (Or.inl ⟨f, args, rfl⟩)))
  | admitRuleAll f => exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨f, rfl⟩))))
  | impose i j => exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr ⟨i, j, rfl⟩))))

/-- Both sealed Challenge-3 histories write `reqs` by `impose`, not by admission. -/
theorem historyL_reqs_from_impose :
    ∃ r, replayE
      [.supply 0, .supply 1, .supply 1, .supply 2,
       .admitDatum, .admitDatum, .impose 0 1] genesis = some r ∧
      r.reqs = [(0, 1)] := by
  refine ⟨R2L, historyL_replays, ?_⟩
  rfl

theorem historyF_reqs_from_impose :
    ∃ r, replayE
      [.supply 0, .admitDatum, .supply 1, .supply 1, .supply 2,
       .admitDatum, .admitDatum, .impose 1 2] genesis = some r ∧
      r.reqs = [(1, 2)] := by
  refine ⟨R2F, historyF_replays, ?_⟩
  rfl

end EndogenousDemand

#print axioms EndogenousDemand.stepE_reqs_supply
#print axioms EndogenousDemand.stepE_admitDatum
#print axioms EndogenousDemand.stepE_reqs_admitDatum
#print axioms EndogenousDemand.stepE_reqs_admitForm
#print axioms EndogenousDemand.stepE_reqs_admitInst
#print axioms EndogenousDemand.stepE_reqs_admitRuleAll
#print axioms EndogenousDemand.stepE_reqs_impose
#print axioms EndogenousDemand.stepE_reqs_mem
#print axioms EndogenousDemand.applyItem_reqs
#print axioms EndogenousDemand.applyDelta_nil
#print axioms EndogenousDemand.applyDelta_cons
#print axioms EndogenousDemand.applyDelta_reqs
#print axioms EndogenousDemand.replayE_nil
#print axioms EndogenousDemand.replayE_cons
#print axioms EndogenousDemand.genesis_reqs
#print axioms EndogenousDemand.replayE_reqs_mem
#print axioms EndogenousDemand.replay_reqs_iff_impose
#print axioms EndogenousDemand.no_reqs_extension_without_impose
#print axioms EndogenousDemand.e2_on_C_reqs_unsat
#print axioms EndogenousDemand.event_constructors
#print axioms EndogenousDemand.historyL_reqs_from_impose
#print axioms EndogenousDemand.historyF_reqs_from_impose
