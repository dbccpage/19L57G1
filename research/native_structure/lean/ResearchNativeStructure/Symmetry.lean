import ResearchNativeBridge.Sim
import ResearchNativeStructure.Boundary

/-!
# A presented symmetry: renaming occurrence tokens

AuthorityEffect: None.  A renaming `π : Nat → Nat` acts on a passage state
by renaming the tokens in its occurrence store.  It acts on an event by
renaming the token of an occurrence admission and fixing every other
event.  The action is **declared** here; nothing in the sealed dynamics
supplies it.

Proved here:

* `actS_id`, `actS_comp`: the action respects identity and composition.
* `step_equivariant`: for an injective renaming, stepping commutes with
  the action.  Injectivity is a hypothesis, and `needs_injective` shows
  it cannot be dropped.
* `symSim`: an injective renaming is a commuting translation of the
  passage into itself, so it lifts native paths (and composition) through
  `native_bridge`'s `Sim.lift`.
* `size_act`, `core_act_eq`: the action preserves the size, and fixes
  every field of the core except the occurrence store.
* `cost_invariant`: a cost that is invariant under the action (a
  hypothesis) has invariant path cost.
-/

namespace ResearchNativeStructure

open PrimitivePassage TraceAlgebra TransitionAlphabet ResearchNativeBridge

def actS (π : Nat → Nat) (s : PState) : PState := { s with occ := s.occ.map π }

def actE (π : Nat → Nat) : PEvent → PEvent
  | .admitOcc t => .admitOcc (π t)
  | e => e

theorem actS_id (s : PState) : actS id s = s := by
  simp [actS]

theorem actS_comp (π ρ : Nat → Nat) (s : PState) :
    actS π (actS ρ s) = actS (π ∘ ρ) s := by
  simp [actS, List.map_map]

theorem mem_map_inj {π : Nat → Nat} (hπ : ∀ a b, π a = π b → a = b) (l : List Nat) (t : Nat) :
    π t ∈ l.map π ↔ t ∈ l := by
  constructor
  · intro h
    obtain ⟨a, ha, hpa⟩ := List.mem_map.mp h
    rw [← hπ a t hpa]; exact ha
  · intro h; exact List.mem_map_of_mem h

theorem obstP_act (π : Nat → Nat) (s : PState) (i j : Nat) :
    obstP (actS π s) i j = obstP s i j := rfl

@[simp] theorem actS_occ (π : Nat → Nat) (s : PState) : (actS π s).occ = s.occ.map π := rfl
@[simp] theorem actS_obs (π : Nat → Nat) (s : PState) : (actS π s).obs = s.obs := rfl
@[simp] theorem actS_prot (π : Nat → Nat) (s : PState) : (actS π s).prot = s.prot := rfl

theorem refineOk_act (π : Nat → Nat) (s : PState) (v : List Nat) (p : Nat) :
    refineOk (actS π s) v p = refineOk s v p := by
  simp only [refineOk, actS_obs, actS_occ, actS_prot, List.length_map, obstP_act]

theorem colOk_act (π : Nat → Nat) (s : PState) (c : List Nat) :
    colOk (actS π s) c = colOk s c := by
  simp only [colOk, actS_obs, actS_occ, actS_prot, List.length_map, obstP_act]

theorem wfPair_act (π : Nat → Nat) (s : PState) (i j : Nat) :
    wfPair (actS π s) i j = wfPair s i j := by
  unfold wfPair
  show ((i != j) && decide (i < (s.occ.map π).length) && decide (j < (s.occ.map π).length)) = _
  rw [List.length_map]

theorem guardHolds_act {π : Nat → Nat} (hπ : ∀ a b, π a = π b → a = b)
    (s : PState) (e : PEvent) : guardHolds (actS π s) (actE π e) = guardHolds s e := by
  cases e with
  | admitOcc t =>
      show (!s.halted && !(decide (π t ∈ s.occ.map π))) = (!s.halted && !(decide (t ∈ s.occ)))
      rw [decide_eq_decide.mpr (mem_map_inj hπ s.occ t)]
  | assertWit i j =>
      show (!s.halted && wfPair (actS π s) i j && _) = _
      rw [wfPair_act]; rfl
  | admitWit i j =>
      show (!s.halted && wfPair (actS π s) i j && _ && _) = _
      rw [wfPair_act]; rfl
  | refineCol v p =>
      show (!s.halted && refineOk (actS π s) v p && _) = _
      rw [refineOk_act]; rfl
  | addCol c =>
      show (!s.halted && colOk (actS π s) c && _ && _) = _
      rw [colOk_act]; rfl
  | protect i j => rfl
  | declareObs => rfl
  | refuse i j => rfl
  | setBudget n => rfl
  | setLicense b => rfl
  | halt => rfl

theorem postOf_act (π : Nat → Nat) (s : PState) (e : PEvent) :
    postOf (actS π s) (actE π e) = actS π (postOf s e) := by
  cases e with
  | admitOcc t => simp [postOf, actE, occS, actS, List.map_append]
  | refineCol v p => cases h : s.obs <;> simp [postOf, actE, actS, h, refineS]
  | addCol c => cases h : s.obs <;> simp [postOf, actE, actS, h, colS]
  | _ => rfl

/-- **Equivariance** under an injective renaming. -/
theorem step_equivariant {π : Nat → Nat} (hπ : ∀ a b, π a = π b → a = b)
    (s : PState) (e : PEvent) : step (actS π s) (actE π e) = actS π (step s e) := by
  rw [step_eq_ite, step_eq_ite s e, guardHolds_act hπ, postOf_act,
    apply_ite (actS π)]

/-- Without injectivity, equivariance fails: two tokens renamed to one. -/
theorem needs_injective :
    step (actS (fun _ => 0) (step genesisP (.admitOcc 0))) (actE (fun _ => 0) (.admitOcc 1)) ≠
      actS (fun _ => 0) (step (step genesisP (.admitOcc 0)) (.admitOcc 1)) := by
  decide

/-- An injective renaming as a commuting translation of the passage into
itself. -/
def symSim (π : Nat → Nat) (hπ : ∀ a b, π a = π b → a = b) : Sim step step where
  enc := actS π
  tr := fun _ e => [actE π e]
  comm := fun s e => step_equivariant hπ s e

theorem size_act (π : Nat → Nat) (s : PState) : size (actS π s) = size s := by
  simp [size, actS, List.length_map]

theorem core_act_eq (π : Nat → Nat) (s : PState) :
    core (actS π s) = { core s with occ := s.occ.map π } := rfl

theorem replayP_act {π : Nat → Nat} (hπ : ∀ a b, π a = π b → a = b)
    (s : PState) (l : List PEvent) :
    replayP (l.map (actE π)) (actS π s) = actS π (replayP l s) := by
  induction l generalizing s with
  | nil => rfl
  | cons e rest ih =>
      show replayP (rest.map (actE π)) (step (actS π s) (actE π e)) = _
      rw [step_equivariant hπ]
      exact ih (step s e)

/-- A cost invariant under the action has invariant path cost. -/
theorem cost_invariant {π : Nat → Nat} (hπ : ∀ a b, π a = π b → a = b)
    (c : PState → PEvent → Int) (hc : ∀ s e, c (actS π s) (actE π e) = c s e)
    (s : PState) (l : List PEvent) :
    pathCost c (actS π s) (l.map (actE π)) = pathCost c s l := by
  induction l generalizing s with
  | nil => rfl
  | cons e rest ih =>
      show c (actS π s) (actE π e) + pathCost c (step (actS π s) (actE π e)) (rest.map (actE π)) =
        c s e + pathCost c (step s e) rest
      rw [hc, step_equivariant hπ, ih]

end ResearchNativeStructure
