namespace SolverAdapter

structure QRat where
  num : Int
  den : Nat := 1
deriving DecidableEq, Repr

namespace QRat

def zero : QRat := ⟨0, 1⟩
def one : QRat := ⟨1, 1⟩

def nonneg (a : QRat) : Prop :=
  0 ≤ a.num

instance (a : QRat) : Decidable (nonneg a) :=
  inferInstanceAs (Decidable (0 ≤ a.num))

theorem nonneg_zero : nonneg zero := by
  decide

end QRat

theorem int_nat_mul_le_mul {a b : Int} (h : a ≤ b) (n : Nat) :
    (n : Int) * a ≤ (n : Int) * b := by
  induction n with
  | zero =>
    have hcast0 : ((0 : Nat) : Int) = (0 : Int) := rfl
    rw [hcast0]
    have h0 : (0 : Int) * a = 0 := Int.zero_mul a
    have h1 : (0 : Int) * b = 0 := Int.zero_mul b
    rw [h0, h1]
    exact Int.le_refl 0
  | succ k ih =>
    have hcast : ((k + 1 : Nat) : Int) = (k : Int) + 1 := rfl
    rw [hcast]
    have h1 : ((k : Int) + 1) * a = (k : Int) * a + a := by
      rw [Int.add_mul, Int.one_mul]
    have h2 : ((k : Int) + 1) * b = (k : Int) * b + b := by
      rw [Int.add_mul, Int.one_mul]
    rw [h1, h2]
    exact Int.add_le_add ih h

structure Constraint (α : Type) where
  eval : α → Int
  rhs : Int

def Satisfies {α : Type} (c : Constraint α) (x : α) : Prop :=
  c.eval x ≤ c.rhs

def SatisfiesAll {α : Type} (cs : List (Constraint α)) (x : α) : Prop :=
  ∀ c ∈ cs, Satisfies c x

def IsFeasible {α : Type} (cs : List (Constraint α)) : Prop :=
  ∃ x : α, SatisfiesAll cs x

theorem primal_soundness {α : Type} (cs : List (Constraint α)) (x : α)
    (h : SatisfiesAll cs x) : IsFeasible cs :=
  ⟨x, h⟩

structure DualTerm (α : Type) where
  weight : Nat
  constraint : Constraint α

def sumLHS {α : Type} (terms : List (DualTerm α)) (x : α) : Int :=
  match terms with
  | [] => 0
  | t :: ts => (t.weight : Int) * t.constraint.eval x + sumLHS ts x

def sumRHS {α : Type} (terms : List (DualTerm α)) : Int :=
  match terms with
  | [] => 0
  | t :: ts => (t.weight : Int) * t.constraint.rhs + sumRHS ts

theorem dual_combination_le {α : Type} (terms : List (DualTerm α)) (x : α)
    (h : ∀ t ∈ terms, Satisfies t.constraint x) :
    sumLHS terms x ≤ sumRHS terms := by
  induction terms with
  | nil =>
    exact Int.le_refl 0
  | cons t ts ih =>
    have ht : Satisfies t.constraint x := h t (List.Mem.head ts)
    have hts : ∀ u ∈ ts, Satisfies u.constraint x := fun u hu => h u (List.Mem.tail t hu)
    have ih' := ih hts
    have hterm : (t.weight : Int) * t.constraint.eval x ≤ (t.weight : Int) * t.constraint.rhs :=
      int_nat_mul_le_mul ht t.weight
    exact Int.add_le_add hterm ih'

theorem farkas_dual_soundness {α : Type} (cs : List (Constraint α))
    (terms : List (DualTerm α))
    (h_subset : ∀ t ∈ terms, t.constraint ∈ cs)
    (h_lhs : ∀ x : α, sumLHS terms x = 0)
    (h_rhs : sumRHS terms < 0) :
    ¬ IsFeasible cs := by
  intro ⟨x, h_feas⟩
  have h_sat : ∀ t ∈ terms, Satisfies t.constraint x := by
    intro t ht
    exact h_feas t.constraint (h_subset t ht)
  have h_le := dual_combination_le terms x h_sat
  have h_lhs_zero := h_lhs x
  rw [h_lhs_zero] at h_le
  have h_contra := Int.lt_of_le_of_lt h_le h_rhs
  exact Int.lt_irrefl 0 h_contra

inductive RefusalReason where
  | fuel_exhausted : RefusalReason
  | horizon_exceeded : RefusalReason
deriving DecidableEq, Repr

structure SolverState (α : Type) where
  constraints : List (Constraint α)
  fuel : Nat
  step_count : Nat

inductive StepOutcome (α : Type) where
  | step_refusal : RefusalReason → SolverState α → StepOutcome α
  | step_continue : SolverState α → StepOutcome α

def step {α : Type} (s : SolverState α) (do_eliminate : List (Constraint α) → Option (List (Constraint α))) : StepOutcome α :=
  match s.fuel with
  | 0 => StepOutcome.step_refusal RefusalReason.fuel_exhausted s
  | fuel' + 1 =>
    match do_eliminate s.constraints with
    | none => StepOutcome.step_refusal RefusalReason.horizon_exceeded s
    | some cs' =>
      StepOutcome.step_continue { constraints := cs', fuel := fuel', step_count := s.step_count + 1 }

theorem fuel_monotonicity {α : Type} (s : SolverState α)
    (do_elim : List (Constraint α) → Option (List (Constraint α)))
    (s' : SolverState α)
    (h : step s do_elim = StepOutcome.step_continue s') :
    s'.fuel + 1 = s.fuel := by
  cases hfuel : s.fuel with
  | zero =>
    unfold step at h
    rw [hfuel] at h
    contradiction
  | succ fuel' =>
    unfold step at h
    rw [hfuel] at h
    cases helim : do_elim s.constraints with
    | none =>
      rw [helim] at h
      contradiction
    | some cs' =>
      rw [helim] at h
      injection h with hs'
      rw [← hs']

theorem refusal_preserves_state {α : Type} (s : SolverState α)
    (do_elim : List (Constraint α) → Option (List (Constraint α)))
    (r : RefusalReason) (s' : SolverState α)
    (h : step s do_elim = StepOutcome.step_refusal r s') :
    s'.constraints = s.constraints := by
  cases hfuel : s.fuel with
  | zero =>
    unfold step at h
    rw [hfuel] at h
    injection h with hr hs'
    rw [← hs']
  | succ fuel' =>
    unfold step at h
    rw [hfuel] at h
    cases helim : do_elim s.constraints with
    | none =>
      rw [helim] at h
      injection h with hr hs'
      rw [← hs']
    | some cs' =>
      rw [helim] at h
      contradiction

end SolverAdapter
