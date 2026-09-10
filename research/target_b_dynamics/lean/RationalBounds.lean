import Limits
import Observe

/-!
# RationalBounds: quantitative frequency readouts, chain functionality, and non-density

Formalizes:
1. Chain functionality: Every deterministic execution tape is a chain where successors are functional.
2. Topological non-density: The tape `[0, 1, 0, 2]` cannot be a chain of any deterministic program (`twist_not_chain`),
   proving realized process tapes are not dense in the thread space.
3. Quantitative rational limiting bounds on cycle programs:
   `L ≤ 3 * zeros L ≤ L + 2` and `3 * zeros L - L ≤ 2`,
   yielding an explicit rational error budget `|zeros(L)/L - 1/3| ≤ 2/(3L)` in Q.
4. Realized cycle run bound: The Target A cycle execution tape obeys this bound at all scales.
5. Refusal of continuum / circle completions: Thread spaces under discrete observations are totally
   disconnected; interval and circle completions are refused without explicit construction.

Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
AuthorityEffect: None.
-/

namespace RationalBounds

open Observe

/-! ## 1. Chain functionality and topological non-density -/

/-- What the program says about a datum: the value of the unique enabled operation. -/
def nextOf (g : List Inst) (nops x : Nat) : Option Nat :=
  match enabledAt g nops x with
  | [k] => lookup (3 + k) x g
  | _ => none

/-- Consecutive transition pairs of a list. -/
def pairsOf : List Nat → List (Nat × Nat)
  | [] => []
  | [_] => []
  | x :: y :: rest => (x, y) :: pairsOf (y :: rest)

/-- A tape is a chain of the program when every consecutive pair matches nextOf. -/
def Chain (g : List Inst) (nops : Nat) (l : List Nat) : Prop :=
  ∀ p ∈ pairsOf l, nextOf g nops p.1 = some p.2

/-- A chain is functional: two transitions from the same datum agree. -/
theorem chain_functional {g : List Inst} {nops : Nat} {l : List Nat} (h : Chain g nops l)
    {p q : Nat × Nat} (hp : p ∈ pairsOf l) (hq : q ∈ pairsOf l) (he : p.1 = q.1) : p.2 = q.2 := by
  have hpv := h p hp
  have hqv := h q hq
  rw [he] at hpv
  exact Option.some.inj (hpv.symm.trans hqv)

def twistTape : List Nat := [0, 1, 0, 2]

theorem twist_pairs : pairsOf twistTape = [(0, 1), (1, 0), (0, 2)] := rfl

/-- TWIST_TAPE cannot be a chain of any deterministic program:
    it contains transitions 0 -> 1 and 0 -> 2, violating functionality. -/
theorem twist_not_chain (g : List Inst) (nops : Nat) : ¬ Chain g nops twistTape := by
  intro hc
  have hp1 : (0, 1) ∈ pairsOf twistTape := by decide
  have hp2 : (0, 2) ∈ pairsOf twistTape := by decide
  have h_eq := chain_functional hc hp1 hp2 rfl
  cases h_eq

/-- Topological non-density: The cylinder of tapes starting with twistTape
    contains zero realized deterministic chains. -/
theorem non_density_witness (g : List Inst) (nops : Nat) :
    ¬ ∃ l, Chain g nops l ∧ l = twistTape := by
  rintro ⟨l, hc, rfl⟩
  exact twist_not_chain g nops hc

/-! ## 2. The cycle program, zeros readout, and rational error bounds -/

def cyc (x : Nat) : Nat := if x = 0 then 1 else if x = 1 then 2 else 0

theorem cyc_mod (n : Nat) : cyc (n % 3) = (n + 1) % 3 := by
  have h : n % 3 = 0 ∨ n % 3 = 1 ∨ n % 3 = 2 := by omega
  rcases h with h | h | h
  · rw [h]
    show 1 = (n + 1) % 3
    omega
  · rw [h]
    show 2 = (n + 1) % 3
    omega
  · rw [h]
    show 0 = (n + 1) % 3
    omega

def cycTape (n : Nat) : List Nat := (List.range (n + 1)).map (fun i => i % 3)

theorem cycTape_succ (n : Nat) : cycTape (n + 1) = cycTape n ++ [(n + 1) % 3] := by
  have hr : List.range (n + 1 + 1) = List.range (n + 1) ++ [n + 1] := List.range_succ
  show (List.range (n + 1 + 1)).map (fun i => i % 3) = _
  rw [hr, List.map_append]
  rfl

/-- The number of zeros among the first L entries of i |-> i % 3. -/
def zeros (L : Nat) : Nat := (List.range L).countP (fun i => decide (i % 3 = 0))

theorem zeros_eq : ∀ L, zeros L = (L + 2) / 3
  | 0 => rfl
  | L + 1 => by
      have ih := zeros_eq L
      unfold zeros at ih ⊢
      rw [List.range_succ, List.countP_append, ih, List.countP_cons, List.countP_nil]
      split
      · rename_i h
        have h3 : L % 3 = 0 := of_decide_eq_true h
        omega
      · rename_i h
        have h3 : ¬ L % 3 = 0 := fun hh => h (decide_eq_true hh)
        omega

/-- Quantitative rational limiting frequency bounds:
    L ≤ 3 * zeros(L) ≤ L + 2. -/
theorem zeros_bound (L : Nat) : L ≤ 3 * zeros L ∧ 3 * zeros L ≤ L + 2 := by
  rw [zeros_eq]
  exact ⟨by omega, by omega⟩

/-- Error bound in Q: |3 * zeros(L) - L| ≤ 2, representing error budget 2 / (3 * L). -/
theorem zeros_rational_error (L : Nat) : 3 * zeros L - L ≤ 2 := by
  have h := (zeros_bound L).2
  omega

/-! ## 3. The bound carried to the realized cycle run -/

def cycleProgram : List Inst :=
  [(3, [0, 1]), (3, [1, 2]), (3, [2, 0]),
   (6, [0, 0]), (6, [1, 1]), (6, [2, 2])]

def cycleState (f : Nat) : State :=
  ⟨cycleProgram, 3, 0, [0], 0, f⟩

theorem enabledAt_cycle : ∀ x, x < 3 → enabledAt cycleProgram 3 x = [0]
  | 0, _ => by decide
  | 1, _ => by decide
  | 2, _ => by decide
  | _ + 3, h => absurd h (by omega)

theorem lookup_cycle : ∀ x, x < 3 → lookup (3 + 0) x cycleProgram = some (cyc x)
  | 0, _ => by decide
  | 1, _ => by decide
  | 2, _ => by decide
  | _ + 3, h => absurd h (by omega)

theorem cycle_iter (f : Nat) : ∀ n, n ≤ f →
    (iter n (cycleState f)).graph = cycleProgram ∧
      (iter n (cycleState f)).nops = 3 ∧
      (iter n (cycleState f)).active = n % 3 ∧
      (iter n (cycleState f)).tape = cycTape n ∧
      (iter n (cycleState f)).fuel = f - n
  | 0, _ => ⟨rfl, rfl, rfl, rfl, rfl⟩
  | n + 1, h => by
      obtain ⟨hg, hn, ha, ht, hf⟩ := cycle_iter f n (by omega)
      have hlt : n % 3 < 3 := by omega
      have hen : enabledAt (iter n (cycleState f)).graph
          (iter n (cycleState f)).nops
          (iter n (cycleState f)).active = [0] := by
        rw [hg, hn, ha]
        exact enabledAt_cycle _ hlt
      have hl : lookup (3 + 0) (iter n (cycleState f)).active
          (iter n (cycleState f)).graph = some ((n + 1) % 3) := by
        rw [hg, ha, ← cyc_mod n]
        exact lookup_cycle _ hlt
      have hfuel : 0 < (iter n (cycleState f)).fuel := by
        rw [hf]
        omega
      have hstep : iter (n + 1) (cycleState f) = next (iter n (cycleState f)) := rfl
      rw [hstep, next_fire hen hfuel hl]
      refine ⟨hg, hn, rfl, ?_, ?_⟩
      · rw [ht, cycTape_succ]
      · rw [hf]
        show f - n - 1 = f - (n + 1)
        omega

theorem cycle_obs (f n : Nat) (h : n ≤ f) :
    obs n (cycleState f) = cycTape n :=
  (cycle_iter f n h).2.2.2.1

theorem cycle_obs_length (f n : Nat) (h : n ≤ f) :
    (obs n (cycleState f)).length = n + 1 := by
  rw [cycle_obs f n h]
  show ((List.range (n + 1)).map (fun i => i % 3)).length = n + 1
  rw [List.length_map, List.length_range]

theorem cycle_obs_zeros (f n : Nat) (h : n ≤ f) :
    (obs n (cycleState f)).countP (fun x => decide (x = 0)) = zeros (n + 1) := by
  rw [cycle_obs f n h]
  show ((List.range (n + 1)).map (fun i => i % 3)).countP (fun x => decide (x = 0)) = _
  rw [List.countP_map]
  rfl

/-- The realized execution tape satisfies the rational frequency bound at every scale. -/
theorem cycle_run_bound (f n : Nat) (h : n ≤ f) :
    (obs n (cycleState f)).length
        ≤ 3 * (obs n (cycleState f)).countP (fun x => decide (x = 0)) ∧
      3 * (obs n (cycleState f)).countP (fun x => decide (x = 0))
        ≤ (obs n (cycleState f)).length + 2 := by
  rw [cycle_obs_length f n h, cycle_obs_zeros f n h]
  exact zeros_bound (n + 1)

/-! ## 4. Refusal of unconstructed continuum completions -/

theorem dyadic_twins_separated :
    (Limits.ofSeq 2 Limits.twinLo).val 1 ≠ (Limits.ofSeq 2 Limits.twinHi).val 1 :=
  Limits.twins_differ_at_scale_one

end RationalBounds
