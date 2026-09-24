import ResearchNativeStructure.Boundary

/-!
# The state-change count is closed

AuthorityEffect: None.  NS-10 asked whether `writes`, one for a
state-changing step and zero for an inert one, has zero boundary on every
commuting square.  It does (`writes_closed`).  With `writes_not_exact`
(NS-8) it is a closed cost that is not exact: the budget loop at genesis
costs two, so no potential exists, yet no commuting square separates the
two orders.

The proof reads each writing step as an unconditional record update
under a guard (`step_eq_or_upd`).  On a commuting square with corners
`a = step u e₁` and `b = step u e₂`, the two counts can differ only when
both events write at `u`, `e₂` writes at `a` and lands on `b`, and `e₁`
is inert at `b`: one event absorbs the other.  `absorb_false` refutes
that configuration over every pair of the eleven event constructors:

* an appending event writes injectively, so `a` would equal `u`;
* an overwrite of the budget, the license or the halt flag forces the
  same overwrite at `a`, so `a` would equal `b`;
* the two funded events leave `a` and `u` equal outside the observation,
  and no event changes the observation alone once it is declared
  (`refine_map_ne`: a refinement of a present column moves the list).
-/

namespace ResearchNativeStructure

open PrimitivePassage

/-- The unconditional record update an event performs when it writes. -/
def upd : PEvent → PState → PState
  | .admitOcc t, s => { s with occ := s.occ ++ [t] }
  | .assertWit i j, s => { s with asserted := s.asserted ++ [(i, j)] }
  | .admitWit i j, s => { s with wit := s.wit ++ [(i, j)] }
  | .protect i j, s => { s with prot := s.prot ++ [(i, j)] }
  | .declareObs, s => { s with obs := some [] }
  | .refineCol v p, s =>
      { s with obs := s.obs.map (fun cols => cols.map (fun c => if c = v then p :: c else c)),
               budget := s.budget - 1 }
  | .addCol c, s => { s with obs := s.obs.map (fun cols => cols ++ [c]), budget := s.budget - 1 }
  | .refuse i j, s => { s with refusals := s.refusals ++ [(i, j)] }
  | .setBudget n, s => { s with budget := n }
  | .setLicense b, s => { s with licensed := b }
  | .halt, s => { s with halted := true }

/-- What a writing step needs of its source, beyond not being halted.
Only the facts the proof below uses are recorded. -/
def guard : PEvent → PState → Prop
  | .declareObs, s => s.obs = none
  | .refineCol v _, s => 0 < s.budget ∧ ∃ cols, s.obs = some cols ∧ v ∈ cols
  | .addCol _, s => 0 < s.budget ∧ ∃ cols, s.obs = some cols
  | _, _ => True

/-- Every step is inert, or it is the event's unconditional update taken
from a state that is not halted and meets the event's guard. -/
theorem step_eq_or_upd (s : PState) (e : PEvent) :
    step s e = s ∨ (step s e = upd e s ∧ s.halted = false ∧ guard e s) := by
  cases hh : s.halted
  · cases e with
    | refineCol v p =>
        simp only [step, hh, Bool.false_eq_true, if_false]
        by_cases hc : (refineOk s v p && decide (0 < s.budget)) = true
        · rw [if_pos hc]
          simp only [Bool.and_eq_true, decide_eq_true_eq] at hc
          obtain ⟨hr, hb⟩ := hc
          unfold refineOk at hr
          cases ho : s.obs with
          | none => simp [ho] at hr
          | some cols =>
              right
              simp only [ho, Bool.and_eq_true, decide_eq_true_eq] at hr
              refine ⟨?_, trivial, hb, cols, ho, hr.1.1.1.1⟩
              simp [upd, ho, hh]
        · rw [if_neg hc]; exact Or.inl rfl
    | addCol c =>
        simp only [step, hh, Bool.false_eq_true, if_false]
        by_cases hc : (colOk s c && s.licensed && decide (0 < s.budget)) = true
        · rw [if_pos hc]
          simp only [Bool.and_eq_true, decide_eq_true_eq] at hc
          obtain ⟨⟨hr, _⟩, hb⟩ := hc
          unfold colOk at hr
          cases ho : s.obs with
          | none => simp [ho] at hr
          | some cols =>
              right
              refine ⟨?_, trivial, hb, cols, ho⟩
              simp [upd, ho, hh]
        · rw [if_neg hc]; exact Or.inl rfl
    | _ =>
        obtain ⟨occ, asserted, wit, prot, obs, budget, licensed, refusals, halted⟩ := s
        simp only at hh
        subst hh
        cases obs <;> simp only [step, upd, guard] <;>
          (try split) <;> (try split) <;> simp_all
  · left
    cases e <;> simp [step, hh]
    cases s; simp_all

/-- A refinement of a column that is present moves the column list.  The
statement is in the form `simp` normalizes the refinement map to. -/
theorem refine_map_ne {v : List Nat} (p : Nat) :
    ∀ {cols : List (List Nat)}, v ∈ cols →
      cols.map (fun c => if c = v then p :: v else c) ≠ cols
  | x :: xs, hv, h => by
      simp only [List.map_cons, List.cons.injEq] at h
      by_cases hx : x = v
      · subst hx
        rw [if_pos rfl] at h
        exact List.cons_ne_self p x h.1
      · rw [if_neg hx] at h
        have hv' : v ∈ xs := by
          cases hv with
          | head => exact absurd rfl hx
          | tail _ h' => exact h'
        exact refine_map_ne p hv' h.2

theorem refine_map_eq_self_iff {v : List Nat} {cols : List (List Nat)} (p : Nat)
    (hv : v ∈ cols) : cols.map (fun c => if c = v then p :: v else c) = cols ↔ False :=
  ⟨refine_map_ne p hv, False.elim⟩

/-- **No event absorbs another on a commuting square.**  Both events
write at `u`; `e₂` writes at `a = step u e₁` and lands on `b = step u e₂`;
`e₁` is inert at `b`.  That configuration is impossible. -/
theorem absorb_false (u : PState) (e₁ e₂ : PEvent)
    (h1 : step u e₁ ≠ u) (h2 : step u e₂ ≠ u)
    (h3 : step (step u e₁) e₂ = step u e₂)
    (h4 : step (step u e₂) e₁ = step u e₂)
    (h5 : step (step u e₁) e₂ ≠ step u e₁) : False := by
  rcases step_eq_or_upd u e₁ with ha | ⟨ha, hu1, g1⟩
  · exact h1 ha
  rcases step_eq_or_upd u e₂ with hb | ⟨hb, hu2, g2⟩
  · exact h2 hb
  rcases step_eq_or_upd (step u e₁) e₂ with hv | ⟨hv, ha2, g2a⟩
  · exact h5 hv
  rw [hv] at h3 h5
  rw [ha] at h1 h3 h5 ha2 g2a
  rw [hb] at h2 h3 h4
  obtain ⟨occ, asserted, wit, prot, obs, budget, licensed, refusals, halted⟩ := u
  cases e₁ <;> cases e₂ <;> cases obs <;> simp only [upd, guard] at * <;>
    simp_all [refine_map_eq_self_iff]
  all_goals (try simp only [step, Bool.false_eq_true, if_false] at h4) <;> (try simp_all) <;>
    (try omega)

/-- **NS-10.** The count of state-changing steps is closed: every commuting
square has zero boundary. -/
theorem writes_closed : Closed writes := by
  intro u e₁ e₂ hc
  unfold dSquare writes
  by_cases ha : step u e₁ = u
  · have hb' : step (step u e₂) e₁ = step u e₂ := by rw [← hc, ha]
    simp only [ha, hb', if_true]
    split <;> omega
  by_cases hb : step u e₂ = u
  · have ha' : step (step u e₁) e₂ = step u e₁ := by rw [hc, hb]
    simp only [hb, ha', if_true]
    split <;> omega
  by_cases hva : step (step u e₁) e₂ = step u e₁
  · by_cases hvb : step (step u e₂) e₁ = step u e₂
    · simp only [ha, hb, hva, hvb, if_true, if_false]; omega
    · exact (absorb_false u e₂ e₁ hb ha (by rw [← hc, hva]) hva hvb).elim
  · by_cases hvb : step (step u e₂) e₁ = step u e₂
    · exact (absorb_false u e₁ e₂ ha hb (by rw [hc, hvb]) hvb hva).elim
    · simp only [ha, hb, hva, hvb, if_false]; omega

/-- With NS-8, a closed cost that is not exact. -/
theorem writes_closed_not_exact : Closed writes ∧ ¬ Exact writes :=
  ⟨writes_closed, writes_not_exact⟩

end ResearchNativeStructure
