import Runner

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

open Derivation Translation Execution Control Product Schedule Runner

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

/-! ## 2c. Two loci: the observation moves one at a time

The producer family builds two loci as a product carrier, proves the
independence square of the *operations*, and runs them by a schedule carried
in the data.  What this family owes is the square as a statement about
**observations**, and this is it: along a whole run, at every scale, from
every start and with any fuel, consecutive entries of the observed tape
differ in at most one locus.

It is the same chain invariant as `obs_functional`, read through the
product's locality theorems rather than through determinism.  No admissible
range is assumed: the enablement instance the machine reads is what places
the datum in the carrier, so the hypothesis is the program and nothing else.
-/

/-- The next value is read from the one enabled operation. -/
theorem nextOf_of_single {g : List Inst} {nops x y k : Nat}
    (he : enabledAt g nops x = [k]) (h : nextOf g nops x = some y) :
    lookup (3 + k) x g = some y := by
  revert h
  show (match enabledAt g nops x with | [k] => lookup (3 + k) x g | _ => none) = some y →
      lookup (3 + k) x g = some y
  rw [he]
  exact id

/-- A next value exists only where exactly one operation is enabled. -/
theorem nextOf_some {g : List Inst} {nops x y : Nat} (h : nextOf g nops x = some y) :
    ∃ k, enabledAt g nops x = [k] ∧ lookup (3 + k) x g = some y := by
  have hu : nextOf g nops x =
      (match enabledAt g nops x with | [k] => lookup (3 + k) x g | _ => none) := rfl
  cases hl : enabledAt g nops x with
  | nil =>
      rw [hl] at hu
      rw [hu] at h
      cases h
  | cons k rest =>
      cases rest with
      | nil => exact ⟨k, rfl, nextOf_of_single hl h⟩
      | cons k' rest' =>
          rw [hl] at hu
          rw [hu] at h
          cases h

/-- An operation of a product setting, named by its index, moves at most one
locus.  This is `Product.prod_left_local` and `prod_right_local` read at an
index rather than at a membership. -/
theorem prod_op_one_locus (F G : FiniteSetting) {k : Nat}
    (hk : k < (prodSetting F G).ops.length) (x : Nat) :
    fstOf G.n ((prodSetting F G).ops.getD k id x) = fstOf G.n x ∨
      sndOf G.n ((prodSetting F G).ops.getD k id x) = sndOf G.n x := by
  have hmem : (prodSetting F G).ops.getD k id ∈
      F.ops.map (leftOp G.n) ++ G.ops.map (rightOp G.n) := getD_mem hk
  rcases List.mem_append.mp hmem with hleft | hright
  · exact Or.inr (prod_left_local F G hleft x)
  · exact Or.inl (prod_right_local G hright x)

/-- **The step of a two-locus program moves one locus.**  Stated of the
program's next value, so it holds wherever the machine moves at all. -/
theorem nextOf_one_locus (F G : FiniteSetting) (sched : Nat → Nat) {x y : Nat}
    (h : nextOf (program (twoLocus F G sched)) (prodSetting F G).ops.length x = some y) :
    fstOf G.n y = fstOf G.n x ∨ sndOf G.n y = sndOf G.n x := by
  obtain ⟨k, he, hl⟩ := nextOf_some h
  have hk : k < (prodSetting F G).ops.length := by
    have hkmem : k ∈ enabledAt (program (twoLocus F G sched))
        (prodSetting F G).ops.length x := by
      rw [he]
      exact List.Mem.head []
    exact (mem_enabledAt.mp hkmem).1
  have hk2 : k < (twoLocus F G sched).F.ops.length := hk
  have hmem : ((3 + k : Nat), [x, y]) ∈ program (twoLocus F G sched) := lookup_mem hl
  rcases mem_program.mp hmem with ⟨k', hk', x', -, heq⟩ | ⟨k', -, x', -, -, heq⟩
  · injection heq with h1 h2
    have hkk : k' = k := by omega
    subst hkk
    obtain ⟨hx, hy⟩ := list_two_inj h2
    subst hx
    subst hy
    exact prod_op_one_locus F G hk' x
  · injection heq with h1 _
    omega

/-- A tape moves one locus at a time when each consecutive pair leaves one of
the two coordinates exactly where it was. -/
def OneLocus (m : Nat) (l : List Nat) : Prop :=
  ∀ p ∈ pairsOf l, fstOf m p.2 = fstOf m p.1 ∨ sndOf m p.2 = sndOf m p.1

/-- A chain of a two-locus program moves one locus at a time. -/
theorem chain_one_locus (F G : FiniteSetting) (sched : Nat → Nat) {l : List Nat}
    (h : Chain (program (twoLocus F G sched)) (prodSetting F G).ops.length l) :
    OneLocus G.n l := fun p hp => nextOf_one_locus F G sched (h p hp)

/-- A step keeps the program and the operation count. -/
theorem next_graph (s : State) : (next s).graph = s.graph ∧ (next s).nops = s.nops := by
  cases hs : stepDet s with
  | inl t =>
      have hn : next s = s := by
        show (match stepDet s with | .inr s' => s' | .inl _ => s) = s
        rw [hs]
      rw [hn]
      exact ⟨rfl, rfl⟩
  | inr s' =>
      have hn : next s = s' := by
        show (match stepDet s with | .inr s' => s' | .inl _ => s) = s'
        rw [hs]
      obtain ⟨k, -, hf⟩ := stepDet_inr hs
      obtain ⟨-, -, -, -, hg, hnn⟩ := fire_ok hf
      rw [hn]
      exact ⟨hg, hnn⟩

theorem iter_graph : ∀ (n : Nat) (s : State),
    (iter n s).graph = s.graph ∧ (iter n s).nops = s.nops
  | 0, _ => ⟨rfl, rfl⟩
  | n + 1, s => by
      rw [iter_succ]
      obtain ⟨hg, hn⟩ := iter_graph n (next s)
      obtain ⟨hg', hn'⟩ := next_graph s
      exact ⟨hg.trans hg', hn.trans hn'⟩

/-- **The square, lifted to the observation.**  At every scale, from every
start, with any fuel, the observed tape of a two-locus run moves one locus at
a time: the record never shows the two loci moving together.  This is what
the family's causal-footprint entry recorded as not delivered. -/
theorem obs_one_locus (F G : FiniteSetting) (sched : Nat → Nat) (x fuel n : Nat) :
    OneLocus G.n (obs n (Control.init (twoLocus F G sched) x fuel)) := by
  have hstart := init_chain (twoLocus F G sched) x fuel
  have hchain := (iter_chain n (Control.init (twoLocus F G sched) x fuel) hstart.1 hstart.2).1
  obtain ⟨hg, hn⟩ := iter_graph n (Control.init (twoLocus F G sched) x fuel)
  rw [hg, hn] at hchain
  exact chain_one_locus F G sched hchain

/-- And the run the producer family records is one: its observation at scale
four is the tape the theorem there names, and it moves one locus at a time. -/
theorem pair_obs : obs 4 (Control.init Schedule.pair 0 4) = [0, 2, 3, 1, 0] := by decide

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

/-! ## 5. Eventual periodicity, formalised

A tape functional along the whole run (`obs_functional`) on a finite carrier
is eventually periodic.  Every ledger in this family has called that "the
standard consequence" and left it unstated; this states it.

Nothing is cited.  The pigeonhole is proved here, constructively: the census
of reliance refuses the standard library's classical lemmas, and this package
consumes no finite-set library.  The datum sequence is identified with the
orbit of one function on the carrier — the value the runner moves to, with
the datum itself wherever it stops — and the orbit of a function on `n` data
repeats within `n` steps. -/

/-- Whether some `i` at most `m` has `f i = v`.  Decided by recursion rather
than by a bounded-quantifier instance, so the proof term is visible. -/
theorem find_eq : ∀ (m : Nat) (f : Nat → Nat) (v : Nat),
    (∃ i, i ≤ m ∧ f i = v) ∨ (∀ i, i ≤ m → f i ≠ v)
  | 0, f, v => by
      rcases Nat.decEq (f 0) v with hne | heq
      · refine Or.inr (fun i hi => ?_)
        have hi0 : i = 0 := Nat.le_zero.mp hi
        rw [hi0]
        exact hne
      · exact Or.inl ⟨0, Nat.le_refl 0, heq⟩
  | m + 1, f, v => by
      rcases find_eq m f v with ⟨i, hi, he⟩ | hno
      · exact Or.inl ⟨i, Nat.le_succ_of_le hi, he⟩
      · rcases Nat.decEq (f (m + 1)) v with hne | heq
        · refine Or.inr (fun i hi hfi => ?_)
          rcases Nat.lt_or_ge i (m + 1) with hlt | hge
          · exact hno i (by omega) hfi
          · have him : i = m + 1 := by omega
            rw [him] at hfi
            exact hne hfi
        · exact Or.inl ⟨m + 1, Nat.le_refl _, heq⟩

/-- **Pigeonhole.**  `n + 1` values below `n` repeat. -/
theorem pigeon : ∀ (n : Nat) (f : Nat → Nat), (∀ i, i ≤ n → f i < n) →
    ∃ i j, i < j ∧ j ≤ n ∧ f i = f j
  | 0, f, h => absurd (h 0 (Nat.le_refl 0)) (Nat.not_lt_zero _)
  | n + 1, f, h => by
      rcases find_eq n f (f (n + 1)) with ⟨i, hi, he⟩ | hno
      · exact ⟨i, n + 1, by omega, Nat.le_refl _, he⟩
      · have hbound : ∀ i, i ≤ n → (if f i < f (n + 1) then f i else f i - 1) < n := by
          intro i hi
          have hfi : f i < n + 1 := h i (by omega)
          have hne : f i ≠ f (n + 1) := hno i hi
          have hv : f (n + 1) < n + 1 := h (n + 1) (Nat.le_refl _)
          rcases Nat.lt_or_ge (f i) (f (n + 1)) with hlt | hge
          · rw [if_pos hlt]
            omega
          · rw [if_neg (by omega)]
            omega
        obtain ⟨i, j, hij, hjn, hgij⟩ :=
          pigeon n (fun i => if f i < f (n + 1) then f i else f i - 1) hbound
        refine ⟨i, j, hij, by omega, ?_⟩
        have hfi : f i < n + 1 := h i (by omega)
        have hfj : f j < n + 1 := h j (by omega)
        have hnei : f i ≠ f (n + 1) := hno i (by omega)
        have hnej : f j ≠ f (n + 1) := hno j (by omega)
        have hg : (if f i < f (n + 1) then f i else f i - 1)
            = (if f j < f (n + 1) then f j else f j - 1) := hgij
        rcases Nat.lt_or_ge (f i) (f (n + 1)) with hi1 | hi2
        · rcases Nat.lt_or_ge (f j) (f (n + 1)) with hj1 | hj2
          · rw [if_pos hi1, if_pos hj1] at hg
            exact hg
          · rw [if_pos hi1, if_neg (by omega)] at hg
            omega
        · rcases Nat.lt_or_ge (f j) (f (n + 1)) with hj1 | hj2
          · rw [if_neg (by omega), if_pos hj1] at hg
            omega
          · rw [if_neg (by omega), if_neg (by omega)] at hg
            omega

/-- The orbit of a function from a datum. -/
def orbit (g : Nat → Nat) (x : Nat) : Nat → Nat
  | 0 => x
  | t + 1 => g (orbit g x t)

theorem orbit_add (g : Nat → Nat) (x a : Nat) :
    ∀ b, orbit g x (a + b) = orbit g (orbit g x a) b
  | 0 => rfl
  | b + 1 => by
      show g (orbit g x (a + b)) = g (orbit g (orbit g x a) b)
      rw [orbit_add g x a b]

theorem orbit_lt {g : Nat → Nat} {n x : Nat} (hx : x < n) (hg : ∀ y, y < n → g y < n) :
    ∀ t, orbit g x t < n
  | 0 => hx
  | t + 1 => hg _ (orbit_lt hx hg t)

/-- **An orbit on `n` data is eventually periodic**, with preperiod and period
together at most `n`. -/
theorem eventually_periodic {g : Nat → Nat} {n x : Nat} (hx : x < n)
    (hg : ∀ y, y < n → g y < n) :
    ∃ i k, 0 < k ∧ i + k ≤ n ∧ ∀ t, orbit g x (i + k + t) = orbit g x (i + t) := by
  obtain ⟨i, j, hij, hjn, he⟩ := pigeon n (orbit g x) (fun t _ => orbit_lt hx hg t)
  refine ⟨i, j - i, by omega, by omega, fun t => ?_⟩
  have hik : i + (j - i) = j := by omega
  rw [hik, orbit_add g x j t, orbit_add g x i t, he]

/-- The next value read off the program, or the datum where the runner
stops.  A total function on the carrier, which is what an orbit needs. -/
def nextVal (g : List Inst) (nops x : Nat) : Nat := (nextOf g nops x).getD x

theorem nextOf_eq_lookup {g : List Inst} {nops x k : Nat} (he : enabledAt g nops x = [k]) :
    nextOf g nops x = lookup (3 + k) x g := by
  show (match enabledAt g nops x with | [k] => lookup (3 + k) x g | _ => none) = _
  rw [he]

/-- **The next value keeps the carrier.**  Where the runner moves it moves
along an operation edge, and where it stops it stays. -/
theorem nextVal_lt (C : Controlled) {y : Nat} (hy : y < C.F.n) :
    nextVal (program C) C.F.ops.length y < C.F.n := by
  have hu : nextVal (program C) C.F.ops.length y =
      (nextOf (program C) C.F.ops.length y).getD y := rfl
  cases hv : nextOf (program C) C.F.ops.length y with
  | none =>
      rw [hu, hv]
      exact hy
  | some z =>
      rw [hu, hv]
      show z < C.F.n
      obtain ⟨k, he, hl⟩ := nextOf_some hv
      have hkmem : k ∈ enabledAt (program C) C.F.ops.length y := by
        rw [he]
        exact List.Mem.head []
      have hk : k < C.F.ops.length := (mem_enabledAt.mp hkmem).1
      have hmem : ((3 + k : Nat), [y, z]) ∈ program C := lookup_mem hl
      rcases mem_program.mp hmem with ⟨k', hk', y', hy', heq⟩ | ⟨k', -, y', -, -, heq⟩
      · injection heq with h1 h2
        have hkk : k' = k := by omega
        subst hkk
        obtain ⟨hyy, hzz⟩ := list_two_inj h2
        subst hyy
        subst hzz
        exact C.F.ops_closed _ (getD_mem hk') _ hy'
      · injection heq with h1 _
        omega

/-- One step with fuel moves the datum to the next value. -/
theorem next_active (s : State) (hf : 0 < s.fuel) :
    (next s).active = nextVal s.graph s.nops s.active := by
  have hu : nextVal s.graph s.nops s.active =
      (nextOf s.graph s.nops s.active).getD s.active := rfl
  cases hes : enabledAt s.graph s.nops s.active with
  | nil =>
      have hn : nextOf s.graph s.nops s.active = none := by
        show (match enabledAt s.graph s.nops s.active with
              | [k] => lookup (3 + k) s.active s.graph | _ => none) = none
        rw [hes]
      rw [next_halt hes, hu, hn]
      rfl
  | cons k rest =>
      cases rest with
      | nil =>
          cases hl : lookup (3 + k) s.active s.graph with
          | none =>
              rw [next_refuse hes hl, hu, nextOf_eq_lookup hes, hl]
              rfl
          | some y =>
              rw [next_fire hes hf hl, hu, nextOf_eq_lookup hes, hl]
              rfl
      | cons k' rest' =>
          have hn : nextOf s.graph s.nops s.active = none := by
            show (match enabledAt s.graph s.nops s.active with
                  | [k] => lookup (3 + k) s.active s.graph | _ => none) = none
            rw [hes]
          rw [next_branch hes, hu, hn]
          rfl

/-- **The datum after `n` steps is the orbit at `n`**, while the fuel lasts. -/
theorem iter_active : ∀ (n : Nat) (s : State), n ≤ s.fuel →
    (iter n s).active = orbit (nextVal s.graph s.nops) s.active n
  | 0, _, _ => rfl
  | n + 1, s, hn => by
      rw [iter_succ]
      have hf : 0 < s.fuel := by omega
      obtain ⟨hg, hnn⟩ := next_graph s
      have hspare := next_fuel s
      have hfuel : n ≤ (next s).fuel := by omega
      have hshift : orbit (nextVal s.graph s.nops) (nextVal s.graph s.nops s.active) n
          = orbit (nextVal s.graph s.nops) s.active (n + 1) := by
        have h1 : orbit (nextVal s.graph s.nops) s.active (1 + n)
            = orbit (nextVal s.graph s.nops) (orbit (nextVal s.graph s.nops) s.active 1) n :=
          orbit_add _ _ 1 n
        rw [Nat.add_comm 1 n] at h1
        exact h1.symm
      rw [iter_active n (next s) hfuel, hg, hnn, next_active s hf, hshift]

/-- **Eventual periodicity of a run.**  On a finite carrier the datum a run is
at repeats: there are a preperiod and a positive period, together at most the
carrier size, after which every later step revisits the datum a period
earlier.  This is the consequence the family's ledgers called standard and
left unstated. -/
theorem eventually_periodic_run (C : Controlled) (x fuel : Nat) (hx : x < C.F.n) :
    ∃ i k, 0 < k ∧ i + k ≤ C.F.n ∧ ∀ t, i + k + t ≤ fuel →
      (iter (i + k + t) (Control.init C x fuel)).active
        = (iter (i + t) (Control.init C x fuel)).active := by
  obtain ⟨i, k, hk, hik, hper⟩ :=
    eventually_periodic (g := nextVal (program C) C.F.ops.length) hx
      (fun y hy => nextVal_lt C hy)
  refine ⟨i, k, hk, hik, fun t ht => ?_⟩
  have hfu : (Control.init C x fuel).fuel = fuel := rfl
  rw [iter_active (i + k + t) (Control.init C x fuel) (by omega),
    iter_active (i + t) (Control.init C x fuel) (by omega)]
  exact hper t

/-- And the observation ends on that datum, so the two tapes end on the same
entry: the periodicity is visible in the record and not only in the state. -/
theorem obs_last_repeats (C : Controlled) (x fuel : Nat) (hx : x < C.F.n) :
    ∃ i k, 0 < k ∧ i + k ≤ C.F.n ∧ ∀ t, i + k + t ≤ fuel →
      (obs (i + k + t) (Control.init C x fuel)).getLast?
        = (obs (i + t) (Control.init C x fuel)).getLast? := by
  obtain ⟨i, k, hk, hik, hper⟩ := eventually_periodic_run C x fuel hx
  refine ⟨i, k, hk, hik, fun t ht => ?_⟩
  have hstart := init_chain C x fuel
  have hone := (iter_chain (i + k + t) (Control.init C x fuel) hstart.1 hstart.2).2
  have htwo := (iter_chain (i + t) (Control.init C x fuel) hstart.1 hstart.2).2
  show (iter (i + k + t) (Control.init C x fuel)).tape.getLast? =
      (iter (i + t) (Control.init C x fuel)).tape.getLast?
  rw [hone, htwo, hper t ht]


/-! ## 6. A fork observed as a family

The deterministic runner stops at a fork: `stepDet` returns `branch` and
`next` keeps the state, so the tape freezes.  Every ledger here has recorded
that as the reason a fork's successor relation is not lifted to threads.  The
relational half is available without selecting anything: observe the whole
*family* of successors at each scale instead of one of them.

`branchStep` takes a state to its successors, or to itself where there are
none, so it is never empty; `frontier n` iterates it and `obsSet n` reads the
tapes off.  What is proved is the relational form of compatibility: every tape
at a scale is a prefix of some tape at the next (`obsSet_prefix`), and hence
of some tape at every later scale (`obsSet_prefix_add`).

What is **not** proved, and is the point: a *thread* out of the family.  A
thread needs one tape per scale, and choosing one at a fork is exactly the
selection the runner refuses to make.  The family is the honest object; the
lifting condition is that some choice function be declared, and none is. -/

/-- The successors of a state, or the state itself where there are none.
Never empty, so the frontier never dies at a terminal. -/
def branchStep (s : State) : List State :=
  match successors s with
  | [] => [s]
  | t :: rest => t :: rest

theorem branchStep_ne_nil (s : State) : branchStep s ≠ [] := by
  show (match successors s with | [] => [s] | t :: rest => t :: rest) ≠ []
  cases successors s with
  | nil => exact List.cons_ne_nil s []
  | cons t rest => exact List.cons_ne_nil t rest

/-- Whatever a branch step does, it only appends to the tape. -/
theorem branchStep_tape {s t : State} (h : t ∈ branchStep s) : s.tape <+: t.tape := by
  revert h
  show t ∈ (match successors s with | [] => [s] | u :: rest => u :: rest) → _
  cases hs : successors s with
  | nil =>
      intro h
      rw [List.mem_singleton.mp h]
      exact List.prefix_refl _
  | cons u rest =>
      intro h
      have hmem : t ∈ successors s := by
        rw [hs]
        exact h
      obtain ⟨k, -, hf⟩ := mem_successors.mp hmem
      obtain ⟨-, htape, -, -, -, -⟩ := fire_ok hf
      rw [htape]
      exact ⟨[t.active], rfl⟩

/-- The frontier at a scale: every state the process can be in after that
many steps, with no selection made. -/
def frontier : Nat → State → List State
  | 0, s => [s]
  | n + 1, s => (frontier n s).flatMap branchStep

/-- The family of observations at a scale. -/
def obsSet (n : Nat) (s : State) : List (List Nat) := (frontier n s).map (·.tape)

theorem frontier_ne_nil : ∀ (n : Nat) (s : State), frontier n s ≠ []
  | 0, s => List.cons_ne_nil s []
  | n + 1, s => by
      show (frontier n s).flatMap branchStep ≠ []
      cases hf : frontier n s with
      | nil => exact absurd hf (frontier_ne_nil n s)
      | cons t rest =>
          intro h
          have hmem : ∀ u ∈ branchStep t, u ∈ ((t :: rest).flatMap branchStep) := by
            intro u hu
            exact List.mem_flatMap.mpr ⟨t, List.Mem.head rest, hu⟩
          cases hb : branchStep t with
          | nil => exact branchStep_ne_nil t hb
          | cons u urest =>
              have : u ∈ ((t :: rest).flatMap branchStep) := hmem u (by rw [hb]; exact List.Mem.head urest)
              rw [h] at this
              exact absurd this List.not_mem_nil

/-- **Compatibility, relationally.**  Every tape observed at a scale is a
prefix of some tape observed at the next.  No branch is selected: the witness
is *some* member of the next family, not a designated one. -/
theorem obsSet_prefix (n : Nat) (s : State) :
    ∀ w ∈ obsSet n s, ∃ v ∈ obsSet (n + 1) s, w <+: v := by
  intro w hw
  obtain ⟨t, ht, rfl⟩ := List.mem_map.mp hw
  cases hb : branchStep t with
  | nil => exact absurd hb (branchStep_ne_nil t)
  | cons u urest =>
      have hu : u ∈ branchStep t := by
        rw [hb]
        exact List.Mem.head urest
      refine ⟨u.tape, List.mem_map.mpr ⟨u, ?_, rfl⟩, branchStep_tape hu⟩
      show u ∈ (frontier n s).flatMap branchStep
      exact List.mem_flatMap.mpr ⟨t, ht, hu⟩

/-- And hence of some tape at every later scale. -/
theorem obsSet_prefix_add (m : Nat) (s : State) :
    ∀ k, ∀ w ∈ obsSet m s, ∃ v ∈ obsSet (m + k) s, w <+: v
  | 0, w, hw => ⟨w, hw, List.prefix_refl w⟩
  | k + 1, w, hw => by
      obtain ⟨v, hv, hwv⟩ := obsSet_prefix_add m s k w hw
      obtain ⟨z, hz, hvz⟩ := obsSet_prefix (m + k) s v hv
      exact ⟨z, hz, hwv.trans hvz⟩

/-- **A fork has two observations where the runner has none.**  On the
represented family's forking program the family at scale one carries two
distinct tapes, while the deterministic runner's own observation has frozen at
the start.  That gap is the reason the successor relation is not lifted to a
thread here: a thread would need one of the two chosen. -/
def forking : Controlled := ⟨base, fun x k => decide (x = 0 ∧ (k = 0 ∨ k = 1))⟩

theorem fork_family_is_two :
    obsSet 1 (Control.init forking 0 5) = [[0, 1], [0, 0]] := by decide

theorem fork_runner_is_frozen :
    obs 1 (Control.init forking 0 5) = [0] := by decide

/-- The runner's observation is a member of the family only when the family is
a singleton; at the fork it is not even that, because the runner stayed. -/
theorem fork_runner_not_in_the_family :
    obs 1 (Control.init forking 0 5) ∉ obsSet 1 (Control.init forking 0 5) := by decide


/-! ## 7. This family's observation is the generic one at the merged reader

The producer family parameterised the interpreter over an enablement reader
and identified its own step with the generic step at `Runner.ctrlReader`.
This family's `next`, `iter` and `obs` are that machine's, at the same reader,
and the identifications are `rfl` or a one-line induction.

The point is not economy.  It is that the compatibility this family proves
(`obs_prefix_add`) and the compatibility the generic runner proves
(`Runner.obsOf_prefix_add`) are the same theorem, so a second reader — the
record-reading one, the depth-two one — inherits it instead of copying it. -/

theorem next_is_generic (s : State) : next s = Runner.nextOf Runner.ctrlReader s := rfl

theorem iter_is_generic : ∀ (n : Nat) (s : State),
    iter n s = Runner.iterOf Runner.ctrlReader n s
  | 0, _ => rfl
  | n + 1, s => by
      show next (iter n s) = Runner.nextOf Runner.ctrlReader (Runner.iterOf Runner.ctrlReader n s)
      rw [iter_is_generic n s, next_is_generic]

theorem obs_is_generic (n : Nat) (s : State) : obs n s = Runner.obsOf Runner.ctrlReader n s := by
  show (iter n s).tape = (Runner.iterOf Runner.ctrlReader n s).tape
  rw [iter_is_generic n s]

/-- And so this family's compatibility is the generic one, not a second proof
of it. -/
theorem obs_prefix_is_generic (m : Nat) (s : State) (k : Nat) :
    obs m s <+: obs (m + k) s := by
  rw [obs_is_generic m s, obs_is_generic (m + k) s]
  exact Runner.obsOf_prefix_add Runner.ctrlReader m s k


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
#print axioms Observe.nextOf_of_single
#print axioms Observe.nextOf_some
#print axioms Observe.prod_op_one_locus
#print axioms Observe.nextOf_one_locus
#print axioms Observe.chain_one_locus
#print axioms Observe.next_graph
#print axioms Observe.iter_graph
#print axioms Observe.obs_one_locus
#print axioms Observe.pair_obs
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
#print axioms Observe.find_eq
#print axioms Observe.pigeon
#print axioms Observe.orbit_add
#print axioms Observe.orbit_lt
#print axioms Observe.eventually_periodic
#print axioms Observe.nextOf_eq_lookup
#print axioms Observe.nextVal_lt
#print axioms Observe.next_active
#print axioms Observe.iter_active
#print axioms Observe.eventually_periodic_run
#print axioms Observe.obs_last_repeats
#print axioms Observe.branchStep_ne_nil
#print axioms Observe.branchStep_tape
#print axioms Observe.frontier_ne_nil
#print axioms Observe.obsSet_prefix
#print axioms Observe.obsSet_prefix_add
#print axioms Observe.fork_family_is_two
#print axioms Observe.fork_runner_is_frozen
#print axioms Observe.fork_runner_not_in_the_family
#print axioms Observe.next_is_generic
#print axioms Observe.iter_is_generic
#print axioms Observe.obs_is_generic
#print axioms Observe.obs_prefix_is_generic
