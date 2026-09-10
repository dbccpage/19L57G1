import Charter
import Adequacy

/-!
# G001 Comparison Morphisms & Categorical Category Laws

Formalizes `ComparisonMorphism` connecting candidate target systems:
- State, operation, and observation mappings
- Observation commutativity and step simulation
- Faithful observation (injectivity on observables)
- Identity morphism and associative composition
- Category laws: `id_comp`, `comp_id`, `comp_assoc`
- Constructive adequacy preservation theorems

Constructive Core: `#print axioms` strictly within `{propext, Quot.sound}`.
AuthorityEffect: None.
-/

namespace Morphism

open Adequacy

/-- Functorial comparison morphism connecting two target systems. -/
structure ComparisonMorphism (A B : TargetSystem) where
  mapState : A.State → B.State
  mapOp : A.Op → B.Op
  mapObs : A.Obs → B.Obs
  comm_observe : ∀ (s : A.State), B.observe (mapState s) = mapObs (A.observe s)
  comm_step : ∀ (s : A.State) (op : A.Op) (s' : A.State),
    A.step s op = some s' → B.step (mapState s) (mapOp op) = some (mapState s')
  faithful_obs : ∀ (o1 o2 : A.Obs), mapObs o1 = mapObs o2 → o1 = o2

/-- Identity comparison morphism on a target system. -/
def idMorphism (A : TargetSystem) : ComparisonMorphism A A := {
  mapState := fun s => s,
  mapOp := fun op => op,
  mapObs := fun o => o,
  comm_observe := fun _ => rfl,
  comm_step := fun _ _ _ h => h,
  faithful_obs := fun _ _ h => h
}

/-- Associative composition of comparison morphisms. -/
def compMorphism {A B C : TargetSystem}
    (f : ComparisonMorphism A B) (g : ComparisonMorphism B C) :
    ComparisonMorphism A C := {
  mapState := fun s => g.mapState (f.mapState s),
  mapOp := fun op => g.mapOp (f.mapOp op),
  mapObs := fun o => g.mapObs (f.mapObs o),
  comm_observe := fun s => by
    have h1 := f.comm_observe s
    have h2 := g.comm_observe (f.mapState s)
    rw [h2, h1]
  comm_step := fun s op s' h => by
    have h1 := f.comm_step s op s' h
    exact g.comm_step (f.mapState s) (f.mapOp op) (f.mapState s') h1
  faithful_obs := fun o1 o2 h => by
    have h1 := g.faithful_obs (f.mapObs o1) (f.mapObs o2) h
    exact f.faithful_obs o1 o2 h1
}

/-!
### Category Laws
-/

theorem id_comp {A B : TargetSystem} (f : ComparisonMorphism A B) :
    compMorphism (idMorphism A) f = f := by
  cases f
  rfl

theorem comp_id {A B : TargetSystem} (f : ComparisonMorphism A B) :
    compMorphism f (idMorphism B) = f := by
  cases f
  rfl

theorem comp_assoc {A B C D : TargetSystem}
    (f : ComparisonMorphism A B)
    (g : ComparisonMorphism B C)
    (h : ComparisonMorphism C D) :
    compMorphism (compMorphism f g) h = compMorphism f (compMorphism g h) := by
  cases f
  cases g
  cases h
  rfl

/-!
### Adequacy Preservation Theorems
-/

/-- Morphism preserves mathematical adequacy through faithful observation. -/
theorem preserves_mathematical {A B : TargetSystem}
    (f : ComparisonMorphism A B)
    (h_math : MathematicalAdequacy A) :
    MathematicalAdequacy B := by
  rcases h_math with ⟨s0, s1, hne⟩
  exists f.mapState s0, f.mapState s1
  intro heq
  have h_comm0 := f.comm_observe s0
  have h_comm1 := f.comm_observe s1
  rw [h_comm0, h_comm1] at heq
  have h_orig := f.faithful_obs (A.observe s0) (A.observe s1) heq
  exact hne h_orig

/-- Morphism preserves empirical adequacy (observable state transition). -/
theorem preserves_empirical {A B : TargetSystem}
    (f : ComparisonMorphism A B)
    (h_emp : EmpiricalAdequacy A) :
    EmpiricalAdequacy B := by
  rcases h_emp with ⟨s, op, s', h_step, hne⟩
  exists f.mapState s, f.mapOp op, f.mapState s'
  constructor
  · exact f.comm_step s op s' h_step
  · intro heq
    have h_comm := f.comm_observe s
    have h_comm' := f.comm_observe s'
    rw [h_comm, h_comm'] at heq
    have h_orig := f.faithful_obs (A.observe s) (A.observe s') heq
    exact hne h_orig

/-- Definition of state-level injectivity of a comparison morphism. -/
def InjectiveState {A B : TargetSystem} (f : ComparisonMorphism A B) : Prop :=
  ∀ (s1 s2 : A.State), f.mapState s1 = f.mapState s2 → s1 = s2

/-- Morphism preserves computational adequacy when state mapping is injective. -/
theorem preserves_computational {A B : TargetSystem}
    (f : ComparisonMorphism A B)
    (h_inj : InjectiveState f)
    (h_comp : ComputationalAdequacy A) :
    ComputationalAdequacy B := by
  rcases h_comp with ⟨s0, op, s1, h_step, hne⟩
  exists f.mapState s0, f.mapOp op, f.mapState s1
  constructor
  · exact f.comm_step s0 op s1 h_step
  · intro heq
    have h_orig := h_inj s0 s1 heq
    exact hne h_orig

end Morphism

#print axioms Morphism.id_comp
#print axioms Morphism.comp_id
#print axioms Morphism.comp_assoc
#print axioms Morphism.preserves_mathematical
#print axioms Morphism.preserves_empirical
#print axioms Morphism.preserves_computational
