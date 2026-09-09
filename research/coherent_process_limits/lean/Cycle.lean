import Steps

/-!
# Observe.Cycle: the transcribed `forever` program, its tape and its bound

The three-point carrier with the cycle, the constant map and the climb, and the
program that enables the cycle everywhere.  `forever_obs`: after `n` steps from
datum 0 with fuel to spare, the tape **is** the first `n + 1` entries of
`i ↦ i % 3`.  `forever_run_bound`: the readout of that observation obeys
`L ≤ 3 · count ≤ L + 2`.

The setting and the program are **transcribed by hand** here, while the Python
identifies them from the consumed artifact.  That asymmetry is real and is
recorded in this family's ledger; the Lean cannot read a JSON artifact, so the
transcription is checked by the Python replaying every recorded run.

AuthorityEffect: None.
-/

namespace Observe

open Derivation Translation Execution Control Product Schedule Runner

/-! ## 3. The `forever` program of the represented execution family -/

def cyc (x : Nat) : Nat := if x = 0 then 1 else if x = 1 then 2 else 0
def zero (_ : Nat) : Nat := 0
def succ3 (x : Nat) : Nat := if x = 0 then 1 else 2

theorem cyc_lt : ∀ x, x < 3 → cyc x < 3
  | 0, _ => by decide
  | 1, _ => by decide
  | 2, _ => by decide
  | n + 3, h => absurd h (by omega)

theorem succ3_lt : ∀ x, x < 3 → succ3 x < 3
  | 0, _ => by decide
  | 1, _ => by decide
  | 2, _ => by decide
  | n + 3, h => absurd h (by omega)

/-- The three-point carrier with the cycle, the constant map and the climb. -/
def base : FiniteSetting :=
  ⟨3, fun _ _ => false, fun _ _ => false, fun _ _ => false, 0, 1, [cyc, zero, succ3],
   by decide, by decide, by
     intro g hg x hx
     rcases List.mem_cons.mp hg with rfl | hg
     · exact cyc_lt x hx
     rcases List.mem_cons.mp hg with rfl | hg
     · exact Nat.zero_lt_succ _
     rcases List.mem_cons.mp hg with rfl | hg
     · exact succ3_lt x hx
     exact absurd hg List.not_mem_nil⟩

/-- The cycle enabled everywhere. -/
def forever : Controlled := ⟨base, fun _ k => decide (k = 0)⟩

/-- **The tape does not determine the future; the fuel is what is lost.**
From datum 0 the states with fuel 0 and fuel 1 have the same tape `[0]`; after
one step the first still reads `[0]` and the second reads `[0, 1]`. -/
theorem lost_fuel :
    (Control.init forever 0 0).tape = (Control.init forever 0 1).tape ∧
      (next (Control.init forever 0 0)).tape = [0] ∧
      (next (Control.init forever 0 1)).tape = [0, 1] := by
  refine ⟨rfl, ?_, ?_⟩
  · decide
  · decide

/-! ### The `forever` run, entry by entry -/

/-- At every admitted datum the cycle, and only the cycle, is enabled. -/
theorem enabledAt_forever : ∀ x, x < 3 → enabledAt (program forever) 3 x = [0]
  | 0, _ => by decide
  | 1, _ => by decide
  | 2, _ => by decide
  | _ + 3, h => absurd h (by omega)

/-- And the edge it reads is the cycle's value. -/
theorem lookup_forever : ∀ x, x < 3 → lookup (3 + 0) x (program forever) = some (cyc x)
  | 0, _ => by decide
  | 1, _ => by decide
  | 2, _ => by decide
  | _ + 3, h => absurd h (by omega)

/-- The cycle is the successor modulo three. -/
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

/-- The first `n + 1` entries of the sequence `i ↦ i % 3`. -/
def cycTape (n : Nat) : List Nat := (List.range (n + 1)).map (fun i => i % 3)

theorem cycTape_succ (n : Nat) : cycTape (n + 1) = cycTape n ++ [(n + 1) % 3] := by
  have hr : List.range (n + 1 + 1) = List.range (n + 1) ++ [n + 1] := List.range_succ
  show (List.range (n + 1 + 1)).map (fun i => i % 3) = _
  rw [hr, List.map_append]
  rfl

/-- **The tape is the sequence.**  With fuel to spare, after `n` steps of the
cycle-everywhere program from datum 0 the active datum is `n % 3` and the tape
is the first `n + 1` entries of `i ↦ i % 3`.  This is the connection CL-CP-08
left computed: the bound below is proved on the sequence, and this carries it
to the process. -/
theorem forever_iter (f : Nat) : ∀ n, n ≤ f →
    (iter n (Control.init forever 0 f)).graph = program forever ∧
      (iter n (Control.init forever 0 f)).nops = 3 ∧
      (iter n (Control.init forever 0 f)).active = n % 3 ∧
      (iter n (Control.init forever 0 f)).tape = cycTape n ∧
      (iter n (Control.init forever 0 f)).fuel = f - n
  | 0, _ => ⟨rfl, rfl, rfl, rfl, rfl⟩
  | n + 1, h => by
      obtain ⟨hg, hn, ha, ht, hf⟩ := forever_iter f n (by omega)
      have hlt : n % 3 < 3 := by omega
      have hen : enabledAt (iter n (Control.init forever 0 f)).graph
          (iter n (Control.init forever 0 f)).nops
          (iter n (Control.init forever 0 f)).active = [0] := by
        rw [hg, hn, ha]
        exact enabledAt_forever _ hlt
      have hl : lookup (3 + 0) (iter n (Control.init forever 0 f)).active
          (iter n (Control.init forever 0 f)).graph = some ((n + 1) % 3) := by
        rw [hg, ha, ← cyc_mod n]
        exact lookup_forever _ hlt
      have hfuel : 0 < (iter n (Control.init forever 0 f)).fuel := by
        rw [hf]
        omega
      have hstep : iter (n + 1) (Control.init forever 0 f)
          = next (iter n (Control.init forever 0 f)) := rfl
      rw [hstep, next_fire hen hfuel hl]
      refine ⟨hg, hn, rfl, ?_, ?_⟩
      · rw [ht, cycTape_succ]
      · rw [hf]
        show f - n - 1 = f - (n + 1)
        omega

/-- The observation at scale `n` of that run **is** the sequence's prefix. -/
theorem forever_obs (f n : Nat) (h : n ≤ f) :
    obs n (Control.init forever 0 f) = cycTape n := (forever_iter f n h).2.2.2.1

/-! ## 4. The readout and its bound on the cycle's sequence

The `forever` run from datum 0 visits `0, 1, 2, 0, 1, 2, …`: its tape after
`n` steps is the first `n + 1` entries of `i ↦ i % 3` — `forever_obs`, proved
just above, and not merely computed at the recorded scales.  The readout is the
number of zeros among the first `L` entries, and it obeys the bound the
observer derives at the coarsest scale — one visit of `0` per period of
three — at every scale: `L ≤ 3 · zeros L ≤ L + 2`.  That is an explicit
approximation of the frequency `1 / 3` with the precision rule
`L ≥ 2 / (3 ε)`, proved as arithmetic on the sequence.  No interval and no
real number is used: the bound is on naturals. -/

/-- The number of zeros among the first `L` entries of `i ↦ i % 3`. -/
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

/-- **The bound.**  At every scale the readout stays within two of a third
of the length: the frequency of `0` is `1 / 3` up to `2 / (3 L)`. -/
theorem zeros_bound (L : Nat) : L ≤ 3 * zeros L ∧ 3 * zeros L ≤ L + 2 := by
  rw [zeros_eq]
  exact ⟨by omega, by omega⟩

/-! ### The bound, carried from the sequence to the run

`zeros_bound` is arithmetic on the sequence `i ↦ i % 3`.  With `forever_obs`
— the tape *is* that sequence's prefix — it becomes a statement about the
process the family observes, which is what CL-CP-08 left as its obligation. -/

theorem forever_length (f n : Nat) (h : n ≤ f) :
    (obs n (Control.init forever 0 f)).length = n + 1 := by
  rw [forever_obs f n h]
  show ((List.range (n + 1)).map (fun i => i % 3)).length = n + 1
  rw [List.length_map, List.length_range]

theorem forever_zeros (f n : Nat) (h : n ≤ f) :
    (obs n (Control.init forever 0 f)).countP (fun x => decide (x = 0)) = zeros (n + 1) := by
  rw [forever_obs f n h]
  show ((List.range (n + 1)).map (fun i => i % 3)).countP (fun x => decide (x = 0)) = _
  rw [List.countP_map]
  rfl

/-- **The bound is a fact about the run.**  The observed tape's length `L` and
its count of datum 0 satisfy `L ≤ 3 · count ≤ L + 2` at every scale the
declared fuel allows. -/
theorem forever_run_bound (f n : Nat) (h : n ≤ f) :
    (obs n (Control.init forever 0 f)).length
        ≤ 3 * (obs n (Control.init forever 0 f)).countP (fun x => decide (x = 0)) ∧
      3 * (obs n (Control.init forever 0 f)).countP (fun x => decide (x = 0))
        ≤ (obs n (Control.init forever 0 f)).length + 2 := by
  rw [forever_length f n h, forever_zeros f n h]
  exact zeros_bound (n + 1)

end Observe

#print axioms Observe.cycTape_succ
#print axioms Observe.cyc_lt
#print axioms Observe.cyc_mod
#print axioms Observe.enabledAt_forever
#print axioms Observe.forever_iter
#print axioms Observe.forever_length
#print axioms Observe.forever_obs
#print axioms Observe.forever_run_bound
#print axioms Observe.forever_zeros
#print axioms Observe.lookup_forever
#print axioms Observe.lost_fuel
#print axioms Observe.succ3_lt
#print axioms Observe.zeros_bound
#print axioms Observe.zeros_eq
