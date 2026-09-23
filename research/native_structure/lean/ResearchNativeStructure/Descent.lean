import ResearchNativeBridge.Passage

/-!
# Observer descent on native transitions

AuthorityEffect: None.  The observer here is the native `core`: every field
except budget and license (defined in the `native_bridge` tree).  An event
**descends** when states with the same core step to states with the same
core.

Proved here:

* `core_descends`: every event except column refinement and column
  creation descends.
* `refineCol_not_descends`, `addCol_not_descends`: the two funded events
  do not.  Two states with the same core, differing only in budget or only
  in license, step to different cores.
* `path_descends`: along an event list with no funded event, the end's
  core is determined by the start's core.
-/

namespace ResearchNativeStructure

open PrimitivePassage TraceAlgebra TransitionAlphabet ResearchNativeBridge

/-- The two events whose guard reads budget or license. -/
def funded : PEvent → Bool
  | .refineCol _ _ => true
  | .addCol _ => true
  | _ => false

theorem eq_of_core_eq {s s' : PState} (h : core s = core s') :
    s' = licS (budS s s'.budget) s'.licensed := by
  cases s
  cases s'
  simp only [core, Core.mk.injEq] at h
  obtain ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩ := h
  rfl

theorem core_licS (s : PState) (b : Bool) : core (licS s b) = core s := rfl
theorem core_budS (s : PState) (n : Nat) : core (budS s n) = core s := rfl

theorem core_step_setBudget (s : PState) (n : Nat) :
    core (step s (.setBudget n)) = core s := by
  cases hh : s.halted with
  | true => rw [step_halted s _ hh]
  | false => rw [step_setBudget_live s n hh]; rfl

theorem core_step_setLicense (s : PState) (b : Bool) :
    core (step s (.setLicense b)) = core s := by
  cases hh : s.halted with
  | true => rw [step_halted s _ hh]
  | false => rw [step_setLicense_live s b hh]; rfl

/-- **Descent.**  Every unfunded event maps states with equal cores to
states with equal cores. -/
theorem core_descends (e : PEvent) (he : funded e = false) {s s' : PState}
    (h : core s = core s') : core (step s e) = core (step s' e) := by
  cases e with
  | setBudget n => rw [core_step_setBudget, core_step_setBudget, h]
  | setLicense b => rw [core_step_setLicense, core_step_setLicense, h]
  | halt => rw [step_halt_eq, step_halt_eq, eq_of_core_eq h]; rfl
  | refineCol v p => cases he
  | addCol c => cases he
  | admitOcc t =>
      rw [eq_of_core_eq h, frame_licS _ _ _ rfl, frame_budS _ _ _ rfl]; rfl
  | assertWit i j =>
      rw [eq_of_core_eq h, frame_licS _ _ _ rfl, frame_budS _ _ _ rfl]; rfl
  | admitWit i j =>
      rw [eq_of_core_eq h, frame_licS _ _ _ rfl, frame_budS _ _ _ rfl]; rfl
  | protect i j =>
      rw [eq_of_core_eq h, frame_licS _ _ _ rfl, frame_budS _ _ _ rfl]; rfl
  | declareObs =>
      rw [eq_of_core_eq h, frame_licS _ _ _ rfl, frame_budS _ _ _ rfl]; rfl
  | refuse i j =>
      rw [eq_of_core_eq h, frame_licS _ _ _ rfl, frame_budS _ _ _ rfl]; rfl

/-- A declared observation with one empty column, a protected obstructed
pair, and budget one. -/
def refineWitness : PState :=
  { occ := [0, 1], asserted := [(0, 1)], wit := [(0, 1)], prot := [(0, 1)],
    obs := some [[]], budget := 1, licensed := true, refusals := [], halted := false }

theorem refineCol_not_descends :
    core refineWitness = core { refineWitness with budget := 0 } ∧
      core (step refineWitness (.refineCol [] 0)) ≠
        core (step { refineWitness with budget := 0 } (.refineCol [] 0)) :=
  ⟨rfl, by decide⟩

/-- A declared observation with no column, a protected obstructed pair,
and budget one. -/
def addWitness : PState :=
  { occ := [0, 1], asserted := [(0, 1)], wit := [(0, 1)], prot := [(0, 1)],
    obs := some [], budget := 1, licensed := true, refusals := [], halted := false }

theorem addCol_not_descends :
    core addWitness = core { addWitness with licensed := false } ∧
      core (step addWitness (.addCol [0])) ≠
        core (step { addWitness with licensed := false } (.addCol [0])) :=
  ⟨rfl, by decide⟩

/-- Along an unfunded event list, the end's core is a function of the
start's core. -/
theorem path_descends (l : List PEvent) (hl : ∀ e ∈ l, funded e = false)
    {s s' : PState} (h : core s = core s') : core (replayP l s) = core (replayP l s') := by
  induction l generalizing s s' with
  | nil => exact h
  | cons e rest ih =>
      exact ih (fun x hx => hl x (List.mem_cons_of_mem e hx))
        (core_descends e (hl e (List.mem_cons_self ..)) h)

end ResearchNativeStructure
