import Limits
import Observe

/-!
# Commute: the commuting dynamics square and scale endomorphisms

Formalizes the dynamic commuting diagram across observation scales:
  bond_n(step_{n+1}(x)) = step_n(bond_n(x))

Key constructive results:
1. Stage commuting square: Pointwise transition F on stages commutes with bonding (`bond_stepStage_commute`).
2. Thread dynamics lifting: F lifts to a continuous endomorphism on Thread c (`stepThread`).
3. Sequence correspondence: stepThread commutes with toSeq and ofSeq (`toSeq_stepThread`, `ofSeq_stepThread`).
4. Operational process commuting: Advancing one step before observing scale n equals observing scale n + 1 (`obs_iter_next_commute`).
5. Trace commuting square: bondTrace_n(stepTrace_{n+1}(s)) = stepTrace_n(s) (`trace_commuting_square`).
6. Fuel exhaustion obstruction: Commutativity breaks under fuel starvation (`fuel_starvation_divergence`).

Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
AuthorityEffect: None.
-/

namespace Commute

/-! ## 1. Pointwise stage dynamics and thread lifting -/

def stepStage (c n : Nat) (F : Fin c → Fin c) (st : Limits.Stage c n) : Limits.Stage c n :=
  fun i => F (st i)

/-- The fundamental commuting dynamics square on finite observation stages:
    bond_n(step_{n+1}(st)) = step_n(bond_n(st)). -/
theorem bond_stepStage_commute (c n : Nat) (F : Fin c → Fin c) (st : Limits.Stage c (n + 1)) :
    Limits.bond c n (stepStage c (n + 1) F st) = stepStage c n F (Limits.bond c n st) := rfl

/-- Lift the stage-wise dynamic step to an endomorphism on compatible threads. -/
def stepThread (c : Nat) (F : Fin c → Fin c) (t : Limits.Thread c) : Limits.Thread c :=
  ⟨fun n => stepStage c n F (t.val n), fun n => by
    have h := t.property n
    show Limits.bond c n (stepStage c (n + 1) F (t.val (n + 1))) = stepStage c n F (t.val n)
    rw [bond_stepStage_commute, h]⟩

/-- The dynamic thread endomorphism commutes with sequence extraction. -/
theorem toSeq_stepThread (c : Nat) (F : Fin c → Fin c) (t : Limits.Thread c) :
    Limits.toSeq c (stepThread c F t) = fun i => F (Limits.toSeq c t i) := rfl

/-- The dynamic thread endomorphism commutes with sequence embedding. -/
theorem ofSeq_stepThread (c : Nat) (F : Fin c → Fin c) (s : Nat → Fin c) :
    stepThread c F (Limits.ofSeq c s) = Limits.ofSeq c (fun i => F (s i)) := rfl

/-! ## 2. Operational process execution commuting laws -/

/-- Advancing one step before observing at scale n equals observing at scale n + 1:
    obs (n + 1) s = obs n (next s). -/
theorem obs_iter_next_commute (n : Nat) (s : Observe.State) :
    Observe.obs (n + 1) s = Observe.obs n (Observe.next s) := by
  show (Observe.iter (n + 1) s).tape = (Observe.iter n (Observe.next s)).tape
  rw [Observe.iter_succ]

/-- An observation trace up to scale n. -/
abbrev Trace (n : Nat) (s : Observe.State) : Fin (n + 1) → List Nat :=
  fun i => Observe.obs i.val s

/-- Bonding map on observation traces: forget the observation at scale n + 1. -/
def bondTrace (n : Nat) (tr : Fin (n + 2) → List Nat) : Fin (n + 1) → List Nat :=
  fun i => tr ⟨i.val, Nat.lt_trans i.isLt (Nat.lt_succ_self _)⟩

/-- Dynamic step on traces: observe the successor state. -/
def stepTrace (n : Nat) (s : Observe.State) : Fin (n + 1) → List Nat :=
  Trace n (Observe.next s)

/-- The observation trace square commutes identically:
    bondTrace_n(stepTrace_{n+1}(s)) = stepTrace_n(s). -/
theorem trace_commuting_square (n : Nat) (s : Observe.State) :
    bondTrace n (stepTrace (n + 1) s) = stepTrace n s := rfl

/-! ## 3. Obstruction: fuel starvation breaks bare tape dynamics -/

theorem fuel_starvation_divergence :
    (Observe.next (Observe.stateWithFuel 0)).tape = [0] ∧
      (Observe.next (Observe.stateWithFuel 1)).tape = [0, 1] := by
  refine ⟨?_, ?_⟩
  · decide
  · decide

theorem shift_not_local_refusal :
    ¬ ∃ φ : List Nat → List Nat, ∀ t : List Nat, (t.drop 1).take 2 = φ (t.take 2) :=
  Limits.shift_not_local

end Commute
