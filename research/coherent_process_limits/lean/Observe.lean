import Control

/-!
# Observe: the represented process at finite scales

The process observed is the merged `Control` machine of the represented
execution family, run by its deterministic runner.  The scale is the number
of steps watched: `obs n s` is the tape after `n` steps of `next`, where
`next` is one step of the runner and keeps the state at a terminal.

* **Compatibility is a theorem.**  The tape after `n` steps is a prefix of
  the tape after `n + 1` (`obs_prefix`) and hence of every later scale
  (`obs_prefix_add`): the bonding of the concrete system is "forget the
  entries beyond the coarser length", and it holds at every scale because a
  step only appends (`fire_ok`).
* **What the observation loses.**  Two states with the same tape and
  different fuel have different next observations: on the `forever` program
  of the represented execution family, from datum 0 with fuel 0 the tape
  stays `[0]`, with fuel 1 it becomes `[0, 1]` (`lost_fuel`).  The tape does
  not determine the future; the lost information is the fuel.
* **What determines the next datum.**  Two states with the same program and
  active datum that both step reach the same datum (`next_active_det`): the
  next entry of the tape is a function of the program and the current entry.

AuthorityEffect: None.
-/

namespace Observe

open Derivation Translation Control

/-! ## 1. Steps, scales, observations -/

/-- One step of the deterministic runner as a function: a terminal keeps the
state. -/
def next (s : State) : State :=
  match stepDet s with
  | .inr s' => s'
  | .inl _ => s

def iter : Nat → State → State
  | 0, s => s
  | n + 1, s => next (iter n s)

/-- The observation of the run at scale `n`: the tape after `n` steps. -/
def obs (n : Nat) (s : State) : List Nat := (iter n s).tape

/-- A step of the runner is the firing of the one enabled operation. -/
theorem stepDet_inr {s s' : State} (h : stepDet s = .inr s') :
    ∃ k, enabledAt s.graph s.nops s.active = [k] ∧ fire s k = .ok s' := by
  revert h
  show (match enabledAt s.graph s.nops s.active with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok s' => Sum.inr s'
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inr s' → _
  cases he : enabledAt s.graph s.nops s.active with
  | nil =>
      intro h
      cases h
  | cons k rest =>
      cases rest with
      | nil =>
          show (match fire s k with
                | .ok s' => Sum.inr s'
                | .exhausted => Sum.inl Terminal.exhausted
                | .noEdge => Sum.inl Terminal.refuse) = Sum.inr s' → _
          cases hf : fire s k with
          | ok t =>
              intro h
              have h' : Sum.inr t = Sum.inr s' := h
              cases h'
              exact ⟨k, rfl, hf⟩
          | exhausted =>
              intro h
              have h' : Sum.inl Terminal.exhausted = Sum.inr s' := h
              cases h'
          | noEdge =>
              intro h
              have h' : Sum.inl Terminal.refuse = Sum.inr s' := h
              cases h'
      | cons k' rest' =>
          intro h
          have h' : Sum.inl Terminal.branch = Sum.inr s' := h
          cases h'

/-- A step only appends: the tape before is a prefix of the tape after. -/
theorem next_tape (s : State) : s.tape <+: (next s).tape := by
  show s.tape <+: (match stepDet s with | .inr s' => s' | .inl _ => s).tape
  cases hs : stepDet s with
  | inl t => exact List.prefix_refl _
  | inr s' =>
      obtain ⟨k, -, hf⟩ := stepDet_inr hs
      obtain ⟨-, ht, -, -, -, -⟩ := fire_ok hf
      rw [ht]
      exact List.prefix_append _ _

/-- **Compatibility.**  The observation at scale `n` is a prefix of the
observation at scale `n + 1`. -/
theorem obs_prefix (n : Nat) (s : State) : obs n s <+: obs (n + 1) s :=
  next_tape (iter n s)

/-- And hence of every later scale. -/
theorem obs_prefix_add (m : Nat) (s : State) : ∀ k, obs m s <+: obs (m + k) s
  | 0 => List.prefix_refl _
  | k + 1 => (obs_prefix_add m s k).trans (obs_prefix (m + k) s)

/-! ## 2. What determines the next datum, and what does not -/

/-- Two states with the same program and active datum that both step reach
the same datum. -/
theorem next_active_det {s t s' t' : State} (hg : s.graph = t.graph) (hn : s.nops = t.nops)
    (ha : s.active = t.active) (hs : stepDet s = .inr s') (ht : stepDet t = .inr t') :
    s'.active = t'.active := by
  obtain ⟨k, hek, hfk⟩ := stepDet_inr hs
  obtain ⟨k', hek', hfk'⟩ := stepDet_inr ht
  rw [hg, hn, ha] at hek
  rw [hek] at hek'
  have hkk : k = k' := List.singleton_inj.mp hek'
  subst hkk
  obtain ⟨hl, -, -, -, -, -⟩ := fire_ok hfk
  obtain ⟨hl', -, -, -, -, -⟩ := fire_ok hfk'
  rw [hg, ha] at hl
  rw [hl] at hl'
  exact Option.some.inj hl'

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

/-! ## 4. The readout and its bound on the cycle's sequence

The `forever` run from datum 0 visits `0, 1, 2, 0, 1, 2, …`: its tape after
`n` steps is the first `n + 1` entries of `i ↦ i % 3` (computed at every
recorded scale by the family's record; not proved here).  The readout is the
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

end Observe

#print axioms Observe.stepDet_inr
#print axioms Observe.next_tape
#print axioms Observe.obs_prefix
#print axioms Observe.obs_prefix_add
#print axioms Observe.next_active_det
#print axioms Observe.cyc_lt
#print axioms Observe.succ3_lt
#print axioms Observe.lost_fuel
#print axioms Observe.zeros_eq
#print axioms Observe.zeros_bound
