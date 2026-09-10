import Execution

/-!
# Memory: Retained Records [p, x], Depth-2 Ternary Forms [b, p, x], and the Memory Ladder

Target A: Represented Execution Substrate.
Retained internal records [p, x] and depth-2 ternary forms [b, p, x].

Core Achievements:
1. Retained record reading (Depth 1):
   Enablement reads predecessor datum p and active datum x: (3 + nops + k, [p, x]).
   The process reads its own written history without consulting an external route log.
2. Depth-2 ternary reading (Depth 2):
   Enablement reads before datum b, predecessor p, and active x: (3 + nops + k, [b, p, x]).
   Utilizes ternary control forms within the grammar's native arity freedom.
3. Memory ladder and functionality theorems:
   - functional2_of_functional1: any sequence functional in single entries is functional in pairs.
   - twist_not_functional1: the twist tape [0, 1, 0, 0] is NOT functional in single entries.
   - twist_functional2: the twist tape [0, 1, 0, 0] IS functional in pairs.
   - twist2_not_functional2: the twist2 tape [0, 1, 2, 0, 1, 0] is NOT functional in pairs.

Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
AuthorityEffect: None.
Configuration status: DECLARED_HOST_CONFIG.
-/

namespace Memory

open Derivation Execution

/-! ## 1. Retained Internal Record Reading (Depth 1) -/

def prevOf (tape : List Nat) (active : Nat) : Nat :=
  match tape.reverse with
  | _ :: p :: _ => p
  | _ => active

def previous (s : State) : Nat := prevOf s.tape s.active

def renabled (g : List Inst) (nops p x k : Nat) : Bool :=
  decide ((3 + nops + k, [p, x]) ∈ g)

def renabledAt (g : List Inst) (nops p x : Nat) : List Nat :=
  (List.range nops).filter (fun k => renabled g nops p x k)

def recordReader (s : State) : List Nat :=
  renabledAt s.graph s.nops (previous s) s.active

def rstepDet (s : State) : Terminal ⊕ State := stepDetOf recordReader s

theorem previous_fire_synced {s s' : State} {k : Nat} {t : List Nat}
    (hs : s.tape = t ++ [s.active]) (h : fire s k = .ok s') :
    previous s' = s.active := by
  have ht : s'.tape = s.tape ++ [s'.active] := fire_tape h
  unfold previous prevOf
  rw [ht, hs]
  rw [show (t ++ [s.active] ++ [s'.active]).reverse = s'.active :: s.active :: t.reverse by
    simp]

/-! ## 2. Depth-2 Ternary Control Reading (Depth 2) -/

def beforeOf (tape : List Nat) (active : Nat) : Nat :=
  match tape.reverse with
  | _ :: _ :: b :: _ => b
  | _ => prevOf tape active

def before (s : State) : Nat := beforeOf s.tape s.active

def r2enabled (g : List Inst) (nops b p x k : Nat) : Bool :=
  decide ((3 + nops + k, [b, p, x]) ∈ g)

def r2enabledAt (g : List Inst) (nops b p x : Nat) : List Nat :=
  (List.range nops).filter (fun k => r2enabled g nops b p x k)

def depthReader (s : State) : List Nat :=
  r2enabledAt s.graph s.nops (before s) (previous s) s.active

def r2stepDet (s : State) : Terminal ⊕ State := stepDetOf depthReader s

/-! ## 3. The Functionality Ladder -/

/-- Single-entry functionality: equal data have equal successors. -/
def functional1 (l : List Nat) : Prop :=
  ∀ i j, i + 1 < l.length → j + 1 < l.length →
    l.getD i 0 = l.getD j 0 → l.getD (i + 1) 0 = l.getD (j + 1) 0

/-- Pair functionality: equal pairs have equal successors. -/
def functional2 (l : List Nat) : Prop :=
  ∀ i j, i + 2 < l.length → j + 2 < l.length →
    l.getD i 0 = l.getD j 0 → l.getD (i + 1) 0 = l.getD (j + 1) 0 →
    l.getD (i + 2) 0 = l.getD (j + 2) 0

/-- The ladder monotonicity theorem: single-entry functionality implies pair functionality. -/
theorem functional2_of_functional1 {l : List Nat} (h : functional1 l) : functional2 l := by
  intro i j hi hj h0 h1
  have hi1 : i + 1 + 1 < l.length := by omega
  have hj1 : j + 1 + 1 < l.length := by omega
  exact h (i + 1) (j + 1) hi1 hj1 h1

/-! ## 4. Concrete Ceiling Refutation Theorems -/

def twistTape : List Nat := [0, 1, 0, 0]

/-- twistTape is NOT functional in single entries: 0 is followed by 1 at index 0, and by 0 at index 2. -/
theorem twist_not_functional1 : ¬ functional1 twistTape := by
  intro h
  have h_diff := h 0 2 (by decide) (by decide) (by rfl)
  revert h_diff
  decide

/-- twistTape IS functional in pairs. -/
theorem twist_functional2 : functional2 twistTape := by
  intro i j hi hj h0 h1
  change i + 2 < 4 at hi
  change j + 2 < 4 at hj
  cases i with
  | zero =>
    cases j with
    | zero => rfl
    | succ j =>
      cases j with
      | zero =>
        revert h0; decide
      | succ j => omega
  | succ i =>
    cases i with
    | zero =>
      cases j with
      | zero =>
        revert h0; decide
      | succ j =>
        cases j with
        | zero => rfl
        | succ j => omega
    | succ i => omega

def twist2Tape : List Nat := [0, 1, 2, 0, 1, 0]

/-- twist2Tape is NOT functional in pairs: pair (0, 1) is followed by 2 at index 0, and by 0 at index 3. -/
theorem twist2_not_functional2 : ¬ functional2 twist2Tape := by
  intro h
  have h_diff := h 0 3 (by decide) (by decide) (by rfl) (by rfl)
  revert h_diff
  decide

end Memory
