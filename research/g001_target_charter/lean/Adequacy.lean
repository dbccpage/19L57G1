import Charter

/-!
# G001 Adequacy Predicates & Candidate Evaluation

Formalizes `TargetSystem`, the 4-way adequacy predicates:
- `ComputationalAdequacy`
- `MathematicalAdequacy`
- `PhysicalAdequacy`
- `EmpiricalAdequacy`

Includes canonical constructive witness `cycleSystem` satisfying all 4 predicates
and negative witness `trivialSystem` demonstrating non-triviality and selectivity.

Constructive Core: `#print axioms` strictly within `{propext, Quot.sound}`.
AuthorityEffect: None.
-/

namespace Adequacy

/-- Formal candidate target system. -/
structure TargetSystem where
  State : Type
  Op : Type
  Obs : Type
  step : State → Op → Option State
  observe : State → Obs

/-- Computational adequacy: admits non-trivial state evolution under operation. -/
def ComputationalAdequacy (T : TargetSystem) : Prop :=
  ∃ (s0 : T.State) (op : T.Op) (s1 : T.State), T.step s0 op = some s1 ∧ s0 ≠ s1

/-- Mathematical adequacy: observation separates distinct states. -/
def MathematicalAdequacy (T : TargetSystem) : Prop :=
  ∃ (s0 s1 : T.State), T.observe s0 ≠ T.observe s1

/-- Physical adequacy: deterministic step causality without unencoded branch selection. -/
def PhysicalAdequacy (T : TargetSystem) : Prop :=
  ∀ (s : T.State) (op : T.Op) (s1 s2 : T.State),
    T.step s op = some s1 → T.step s op = some s2 → s1 = s2

/-- Empirical adequacy: admits an operation yielding an observable state change. -/
def EmpiricalAdequacy (T : TargetSystem) : Prop :=
  ∃ (s : T.State) (op : T.Op) (s' : T.State),
    T.step s op = some s' ∧ T.observe s ≠ T.observe s'

/-- Full 4-way target-class adequacy conjunction. -/
def TargetClassAdequate (T : TargetSystem) : Prop :=
  ComputationalAdequacy T ∧
  MathematicalAdequacy T ∧
  PhysicalAdequacy T ∧
  EmpiricalAdequacy T

/-!
### Minimal Toy Witness: 2-State Binary Toggling Transducer

Epistemic Scope:
`binaryToggleSystem` serves as a minimal constructive toy witness demonstrating
that the structural predicates `TargetClassAdequate` are logically satisfiable
and separate non-trivial systems from collapsing single-state systems (`trivialSystem`).
This does NOT assert that a two-state system is an adequate physical theory of everything;
the complete 9-criterion adequacy charter is independently specified in `Charter.lean`
and evaluated under `TOE_TARGET_CLASS_FROZEN`.
-/

/-- State space of the binary toggling system. -/
inductive TwoState where
  | s0 : TwoState
  | s1 : TwoState
  deriving DecidableEq, Repr

/-- Next state under toggle operation. -/
def toggleNext : TwoState → TwoState
  | .s0 => .s1
  | .s1 => .s0

theorem toggleNext_s0 : toggleNext TwoState.s0 = TwoState.s1 := rfl
theorem toggleNext_s1 : toggleNext TwoState.s1 = TwoState.s0 := rfl

theorem s0_ne_s1 : TwoState.s0 ≠ TwoState.s1 := by
  intro h
  nomatch h

/-- Canonical target system exhibiting binary toggle dynamics. -/
def binaryToggleSystem : TargetSystem := {
  State := TwoState,
  Op := Unit,
  Obs := TwoState,
  step := fun s _ => some (toggleNext s),
  observe := fun s => s
}

theorem binaryToggle_computational : ComputationalAdequacy binaryToggleSystem := by
  exists TwoState.s0, (), TwoState.s1
  constructor
  · rfl
  · exact s0_ne_s1

theorem binaryToggle_mathematical : MathematicalAdequacy binaryToggleSystem := by
  exists TwoState.s0, TwoState.s1
  exact s0_ne_s1

theorem binaryToggle_physical : PhysicalAdequacy binaryToggleSystem := by
  intro s op sa sb h1 h2
  injection h1 with e1
  injection h2 with e2
  rw [← e1, ← e2]

theorem binaryToggle_empirical : EmpiricalAdequacy binaryToggleSystem := by
  exists TwoState.s0, (), TwoState.s1
  constructor
  · rfl
  · exact s0_ne_s1

theorem binaryToggle_target_class_adequate : TargetClassAdequate binaryToggleSystem := by
  refine ⟨binaryToggle_computational, binaryToggle_mathematical,
          binaryToggle_physical, binaryToggle_empirical⟩

/-!
### Negative Control: Degenerate Trivial Collapsing System
-/

/-- Trivial single-point system with collapsing observation. -/
def trivialSystem : TargetSystem := {
  State := Unit,
  Op := Unit,
  Obs := Unit,
  step := fun _ _ => some (),
  observe := fun _ => ()
}

theorem trivial_not_computational : ¬ ComputationalAdequacy trivialSystem := by
  intro ⟨s0, op, s1, _, hne⟩
  cases s0; cases s1
  exact hne rfl

theorem trivial_not_mathematical : ¬ MathematicalAdequacy trivialSystem := by
  intro ⟨s0, s1, hne⟩
  cases s0; cases s1
  exact hne rfl

theorem trivial_not_empirical : ¬ EmpiricalAdequacy trivialSystem := by
  intro ⟨s, op, s', _, hne⟩
  exact hne rfl

theorem trivial_not_adequate : ¬ TargetClassAdequate trivialSystem := by
  intro ⟨_, h_math, _, _⟩
  exact trivial_not_mathematical h_math

end Adequacy

#print axioms Adequacy.toggleNext_s0
#print axioms Adequacy.toggleNext_s1
#print axioms Adequacy.s0_ne_s1
#print axioms Adequacy.binaryToggle_computational
#print axioms Adequacy.binaryToggle_mathematical
#print axioms Adequacy.binaryToggle_physical
#print axioms Adequacy.binaryToggle_empirical
#print axioms Adequacy.binaryToggle_target_class_adequate
#print axioms Adequacy.trivial_not_computational
#print axioms Adequacy.trivial_not_mathematical
#print axioms Adequacy.trivial_not_empirical
#print axioms Adequacy.trivial_not_adequate
