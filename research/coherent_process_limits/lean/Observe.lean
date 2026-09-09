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

open Derivation Translation Execution Control

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

/-! ## 2a. One step, by cases; and what the fuel does not change -/

/-- Iterating `n + 1` times is stepping once and iterating `n` times. -/
theorem iter_succ : ∀ (n : Nat) (s : State), iter (n + 1) s = iter n (next s)
  | 0, _ => rfl
  | n + 1, s => by
      show next (iter (n + 1) s) = next (iter n (next s))
      rw [iter_succ n s]

/-- No operation enabled: the state stands. -/
theorem next_halt {s : State} (he : enabledAt s.graph s.nops s.active = []) : next s = s := by
  have h : stepDet s = Sum.inl Terminal.halt := by
    show (match enabledAt s.graph s.nops s.active with
          | [] => Sum.inl Terminal.halt
          | [k] =>
            match fire s k with
            | .ok s' => Sum.inr s'
            | .exhausted => Sum.inl Terminal.exhausted
            | .noEdge => Sum.inl Terminal.refuse
          | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inl Terminal.halt
    rw [he]
  show (match stepDet s with | .inr s' => s' | .inl _ => s) = s
  rw [h]

/-- Two enabled: the runner refuses to pick and the state stands. -/
theorem next_branch {s : State} {a b : Nat} {rest : List Nat}
    (he : enabledAt s.graph s.nops s.active = a :: b :: rest) : next s = s := by
  have h : stepDet s = Sum.inl Terminal.branch := by
    show (match enabledAt s.graph s.nops s.active with
          | [] => Sum.inl Terminal.halt
          | [k] =>
            match fire s k with
            | .ok s' => Sum.inr s'
            | .exhausted => Sum.inl Terminal.exhausted
            | .noEdge => Sum.inl Terminal.refuse
          | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inl Terminal.branch
    rw [he]
  show (match stepDet s with | .inr s' => s' | .inl _ => s) = s
  rw [h]

/-- No fuel: the state stands. -/
theorem next_exhausted {s : State} {k : Nat} (he : enabledAt s.graph s.nops s.active = [k])
    (hf : s.fuel = 0) : next s = s := by
  have h : stepDet s = Sum.inl Terminal.exhausted := by
    show (match enabledAt s.graph s.nops s.active with
          | [] => Sum.inl Terminal.halt
          | [k] =>
            match fire s k with
            | .ok s' => Sum.inr s'
            | .exhausted => Sum.inl Terminal.exhausted
            | .noEdge => Sum.inl Terminal.refuse
          | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inl Terminal.exhausted
    rw [he]
    show (match fire s k with
          | .ok s' => Sum.inr s'
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse) = Sum.inl Terminal.exhausted
    rw [fire_exhausted hf]
  show (match stepDet s with | .inr s' => s' | .inl _ => s) = s
  rw [h]

/-- The one enabled operation has no edge: the state stands. -/
theorem next_refuse {s : State} {k : Nat} (he : enabledAt s.graph s.nops s.active = [k])
    (hl : lookup (3 + k) s.active s.graph = none) : next s = s := by
  cases hfu : s.fuel with
  | zero => exact next_exhausted he hfu
  | succ f =>
      have h : stepDet s = Sum.inl Terminal.refuse := by
        show (match enabledAt s.graph s.nops s.active with
              | [] => Sum.inl Terminal.halt
              | [k] =>
                match fire s k with
                | .ok s' => Sum.inr s'
                | .exhausted => Sum.inl Terminal.exhausted
                | .noEdge => Sum.inl Terminal.refuse
              | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inl Terminal.refuse
        rw [he]
        show (match fire s k with
              | .ok s' => Sum.inr s'
              | .exhausted => Sum.inl Terminal.exhausted
              | .noEdge => Sum.inl Terminal.refuse) = Sum.inl Terminal.refuse
        rw [fire_succ s k f hfu, hl]
      show (match stepDet s with | .inr s' => s' | .inl _ => s) = s
      rw [h]

/-- **One firing, in full.**  With one operation enabled, an edge for it and
fuel, the step moves to the edge's value, appends it, ticks the clock and
spends one fuel, keeping the program. -/
theorem next_fire {s : State} {k y : Nat} (he : enabledAt s.graph s.nops s.active = [k])
    (hfuel : 0 < s.fuel) (hl : lookup (3 + k) s.active s.graph = some y) :
    next s = ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, s.fuel - 1⟩ := by
  obtain ⟨f, hf⟩ : ∃ f, s.fuel = f + 1 := ⟨s.fuel - 1, by omega⟩
  have h : stepDet s = Sum.inr ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩ := by
    show (match enabledAt s.graph s.nops s.active with
          | [] => Sum.inl Terminal.halt
          | [k] =>
            match fire s k with
            | .ok s' => Sum.inr s'
            | .exhausted => Sum.inl Terminal.exhausted
            | .noEdge => Sum.inl Terminal.refuse
          | _ :: _ :: _ => Sum.inl Terminal.branch) = _
    rw [he]
    show (match fire s k with
          | .ok s' => Sum.inr s'
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse) = _
    rw [fire_succ s k f hf, hl]
  show (match stepDet s with | .inr s' => s' | .inl _ => s) = _
  rw [h]
  have hff : f = s.fuel - 1 := by omega
  rw [hff]

/-- A step spends at most one fuel. -/
theorem next_fuel (s : State) : s.fuel - 1 ≤ (next s).fuel := by
  show s.fuel - 1 ≤ (match stepDet s with | .inr s' => s' | .inl _ => s).fuel
  cases hs : stepDet s with
  | inl t => exact Nat.sub_le _ _
  | inr s' =>
      show s.fuel - 1 ≤ s'.fuel
      obtain ⟨k, -, hf⟩ := stepDet_inr hs
      obtain ⟨-, -, -, hfuel, -, -⟩ := fire_ok hf
      omega

/-- Two states agreeing on everything a step reads except the fuel. -/
def Same (s t : State) : Prop :=
  s.graph = t.graph ∧ s.nops = t.nops ∧ s.active = t.active ∧ s.tape = t.tape

/-- With fuel on both sides, a step preserves that agreement: the fuel is
consulted only to refuse. -/
theorem same_next {s t : State} (h : Same s t) (hs : 0 < s.fuel) (ht : 0 < t.fuel) :
    Same (next s) (next t) := by
  obtain ⟨hg, hn, ha, htape⟩ := h
  have he : enabledAt t.graph t.nops t.active = enabledAt s.graph s.nops s.active := by
    rw [hg, hn, ha]
  cases hes : enabledAt s.graph s.nops s.active with
  | nil =>
      rw [next_halt hes, next_halt (he.trans hes)]
      exact ⟨hg, hn, ha, htape⟩
  | cons k rest =>
      cases rest with
      | nil =>
          cases hl : lookup (3 + k) s.active s.graph with
          | none =>
              rw [next_refuse hes hl, next_refuse (he.trans hes) (by rw [← hg, ← ha]; exact hl)]
              exact ⟨hg, hn, ha, htape⟩
          | some y =>
              rw [next_fire hes hs hl,
                next_fire (he.trans hes) ht (by rw [← hg, ← ha]; exact hl)]
              exact ⟨hg, hn, rfl, by rw [htape]⟩
      | cons k' rest' =>
          rw [next_branch hes, next_branch (he.trans hes)]
          exact ⟨hg, hn, ha, htape⟩

/-- **The observation does not read the declared fuel while fuel lasts.**
Two states differing only in the fuel, each with at least `n`, have the same
observation at scale `n`.  (CL-CP-04's obligation.) -/
theorem obs_fuel_indep : ∀ (n : Nat) {s t : State}, Same s t → n ≤ s.fuel → n ≤ t.fuel →
    Same (iter n s) (iter n t)
  | 0, _, _, h, _, _ => h
  | n + 1, s, t, h, hs, ht => by
      rw [iter_succ, iter_succ]
      have hs0 : 0 < s.fuel := by omega
      have ht0 : 0 < t.fuel := by omega
      have hfs : s.fuel - 1 ≤ (next s).fuel := next_fuel s
      have hft : t.fuel - 1 ≤ (next t).fuel := next_fuel t
      have hns : n ≤ (next s).fuel := by omega
      have hnt : n ≤ (next t).fuel := by omega
      exact obs_fuel_indep n (same_next h hs0 ht0) hns hnt

theorem obs_fuel_eq (n : Nat) {s t : State} (h : Same s t) (hs : n ≤ s.fuel) (ht : n ≤ t.fuel) :
    obs n s = obs n t := (obs_fuel_indep n h hs ht).2.2.2

/-! ## 2b. The tape is a chain of the machine, and therefore functional -/

/-- The value the runner moves to at a datum: the value of the one enabled
operation, and none when none, two, or no edge.  The fuel is not read: this is
what the *program* says about the datum. -/
def nextOf (g : List Inst) (nops x : Nat) : Option Nat :=
  match enabledAt g nops x with
  | [k] => lookup (3 + k) x g
  | _ => none

/-- The consecutive pairs of a list. -/
def pairsOf : List Nat → List (Nat × Nat)
  | [] => []
  | [_] => []
  | x :: y :: rest => (x, y) :: pairsOf (y :: rest)

/-- A tape is a chain of the machine when each entry is the next value of the
entry before it. -/
def Chain (g : List Inst) (nops : Nat) (l : List Nat) : Prop :=
  ∀ p ∈ pairsOf l, nextOf g nops p.1 = some p.2

/-- **A chain is functional.**  Two entries that agree are followed by entries
that agree, because the next value is a function of the datum. -/
theorem chain_functional {g : List Inst} {nops : Nat} {l : List Nat} (h : Chain g nops l)
    {p q : Nat × Nat} (hp : p ∈ pairsOf l) (hq : q ∈ pairsOf l) (he : p.1 = q.1) : p.2 = q.2 := by
  have hpv := h p hp
  have hqv := h q hq
  rw [he] at hpv
  exact Option.some.inj (hpv.symm.trans hqv)

theorem getLast?_snoc (l : List Nat) (y : Nat) : (l ++ [y]).getLast? = some y := by simp

theorem mem_pairsOf_snoc : ∀ (l : List Nat) {x y : Nat} {p : Nat × Nat}, l.getLast? = some x →
    (p ∈ pairsOf (l ++ [y]) ↔ p ∈ pairsOf l ∨ p = (x, y))
  | [], x, _, _, hl => absurd hl (by simp)
  | [a], x, y, p, hl => by
      have hx : a = x := by
        have : (some a : Option Nat) = some x := hl
        exact Option.some.inj this
      subst hx
      show p ∈ pairsOf [a, y] ↔ p ∈ pairsOf [a] ∨ p = (a, y)
      show p ∈ [(a, y)] ↔ p ∈ ([] : List (Nat × Nat)) ∨ p = (a, y)
      constructor
      · intro h
        exact Or.inr (List.mem_singleton.mp h)
      · rintro (h | rfl)
        · exact absurd h List.not_mem_nil
        · exact List.mem_singleton.mpr rfl
  | a :: b :: rest, x, y, p, hl => by
      have hl' : (b :: rest).getLast? = some x := hl
      show p ∈ pairsOf (a :: ((b :: rest) ++ [y])) ↔ p ∈ pairsOf (a :: b :: rest) ∨ p = (x, y)
      show p ∈ (a, b) :: pairsOf ((b :: rest) ++ [y]) ↔
        p ∈ (a, b) :: pairsOf (b :: rest) ∨ p = (x, y)
      rw [List.mem_cons, List.mem_cons, mem_pairsOf_snoc (b :: rest) hl']
      constructor
      · rintro (rfl | h | rfl)
        · exact Or.inl (Or.inl rfl)
        · exact Or.inl (Or.inr h)
        · exact Or.inr rfl
      · rintro ((rfl | h) | rfl)
        · exact Or.inl rfl
        · exact Or.inr (Or.inl h)
        · exact Or.inr (Or.inr rfl)

theorem chain_snoc {g : List Inst} {nops : Nat} {l : List Nat} {x y : Nat}
    (hc : Chain g nops l) (hl : l.getLast? = some x) (hn : nextOf g nops x = some y) :
    Chain g nops (l ++ [y]) := by
  intro p hp
  rcases (mem_pairsOf_snoc l hl).mp hp with h | rfl
  · exact hc p h
  · exact hn

/-- A step keeps the tape a chain, and keeps the last entry the active datum. -/
theorem next_chain {s : State} (hc : Chain s.graph s.nops s.tape)
    (hl : s.tape.getLast? = some s.active) :
    Chain (next s).graph (next s).nops (next s).tape ∧
      (next s).tape.getLast? = some (next s).active := by
  cases hes : enabledAt s.graph s.nops s.active with
  | nil =>
      rw [next_halt hes]
      exact ⟨hc, hl⟩
  | cons k rest =>
      cases rest with
      | nil =>
          cases hlk : lookup (3 + k) s.active s.graph with
          | none =>
              rw [next_refuse hes hlk]
              exact ⟨hc, hl⟩
          | some y =>
              cases hfu : s.fuel with
              | zero =>
                  rw [next_exhausted hes hfu]
                  exact ⟨hc, hl⟩
              | succ f =>
                  have hn : nextOf s.graph s.nops s.active = some y := by
                    show (match enabledAt s.graph s.nops s.active with
                          | [k] => lookup (3 + k) s.active s.graph
                          | _ => none) = some y
                    rw [hes]
                    exact hlk
                  rw [next_fire hes (by omega) hlk]
                  exact ⟨chain_snoc hc hl hn, getLast?_snoc _ _⟩
      | cons k' rest' =>
          rw [next_branch hes]
          exact ⟨hc, hl⟩

theorem iter_chain : ∀ (n : Nat) (s : State), Chain s.graph s.nops s.tape →
    s.tape.getLast? = some s.active →
    Chain (iter n s).graph (iter n s).nops (iter n s).tape ∧
      (iter n s).tape.getLast? = some (iter n s).active
  | 0, _, hc, hl => ⟨hc, hl⟩
  | n + 1, s, hc, hl => by
      rw [iter_succ]
      obtain ⟨hc', hl'⟩ := next_chain hc hl
      exact iter_chain n (next s) hc' hl'

theorem init_chain (C : Controlled) (x fuel : Nat) :
    Chain (Control.init C x fuel).graph (Control.init C x fuel).nops
        (Control.init C x fuel).tape ∧
      (Control.init C x fuel).tape.getLast? = some (Control.init C x fuel).active :=
  ⟨fun _ hp => absurd hp List.not_mem_nil, rfl⟩

/-- **Every realized tape is functional along the whole run.**  Two entries of
the observation that agree are followed by entries that agree.  One-step
determinism (`next_active_det`) said this of a single step; the chain
invariant carries it along the whole run, which is CL-CP-07's obligation. -/
theorem obs_functional (C : Controlled) (x fuel n : Nat) {p q : Nat × Nat}
    (hp : p ∈ pairsOf (obs n (Control.init C x fuel)))
    (hq : q ∈ pairsOf (obs n (Control.init C x fuel)))
    (he : p.1 = q.1) : p.2 = q.2 :=
  chain_functional
    (iter_chain n _ (init_chain C x fuel).1 (init_chain C x fuel).2).1 hp hq he

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

#print axioms Observe.stepDet_inr
#print axioms Observe.iter_succ
#print axioms Observe.next_halt
#print axioms Observe.next_branch
#print axioms Observe.next_exhausted
#print axioms Observe.next_refuse
#print axioms Observe.next_fire
#print axioms Observe.next_fuel
#print axioms Observe.same_next
#print axioms Observe.obs_fuel_indep
#print axioms Observe.obs_fuel_eq
#print axioms Observe.chain_functional
#print axioms Observe.getLast?_snoc
#print axioms Observe.mem_pairsOf_snoc
#print axioms Observe.chain_snoc
#print axioms Observe.next_chain
#print axioms Observe.iter_chain
#print axioms Observe.init_chain
#print axioms Observe.obs_functional
#print axioms Observe.enabledAt_forever
#print axioms Observe.lookup_forever
#print axioms Observe.cyc_mod
#print axioms Observe.cycTape_succ
#print axioms Observe.forever_iter
#print axioms Observe.forever_obs
#print axioms Observe.forever_length
#print axioms Observe.forever_zeros
#print axioms Observe.forever_run_bound
#print axioms Observe.next_tape
#print axioms Observe.obs_prefix
#print axioms Observe.obs_prefix_add
#print axioms Observe.next_active_det
#print axioms Observe.cyc_lt
#print axioms Observe.succ3_lt
#print axioms Observe.lost_fuel
#print axioms Observe.zeros_eq
#print axioms Observe.zeros_bound
