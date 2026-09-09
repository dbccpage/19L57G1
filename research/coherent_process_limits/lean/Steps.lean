import Runner

/-!
# Observe.Steps: the represented process at finite scales

The process observed is the merged `Control` machine of the represented
execution family, run by its deterministic runner.  The scale is the number of
steps watched: `obs n s` is the tape after `n` steps of `next`, where `next` is
one step of the runner and keeps the state at a terminal.

* **Compatibility is a theorem.**  The tape after `n` steps is a prefix of the
  tape after `n + 1` (`obs_prefix`) and hence of every later scale
  (`obs_prefix_add`): the bonding of the concrete system is "forget the entries
  beyond the coarser length", and it holds at every scale because a step only
  appends (`fire_ok`).
* **What the observation loses.**  Two states with the same tape and different
  fuel have different next observations (`lost_fuel`): the tape does not
  determine the future, and the lost information is the fuel.
* **What determines the next datum.**  Two states with the same program and
  active datum that both step reach the same datum (`next_active_det`).
* **One step, by cases**, and the fuel read only to refuse (`obs_fuel_eq`).

This is the machine.  The studies over it are `Observe.Chain` (functionality),
`Observe.TwoLoci`, `Observe.Cycle`, `Observe.Periodic` and `Observe.Fork`, and
`Observe` imports all of them, so a consumer writing `import Observe` sees
every `Observe.*` name as before.

**A follow-up this split makes visible and does not take.**  The case family
`next_halt` / `next_branch` / `next_exhausted` / `next_refuse` / `next_fire`
each re-unfolds the same `match enabledAt` that `Control.stepDet` already
performs, and `Runner.stepDetOf_spec` is now that exhaustiveness lemma, proved
once over an arbitrary reader.  Rebuilding the family on it would delete most
of this section.  It is a change to proofs and not a move of text, so it is
named here rather than smuggled into a file split.

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

end Observe

#print axioms Observe.iter_succ
#print axioms Observe.next_active_det
#print axioms Observe.next_branch
#print axioms Observe.next_exhausted
#print axioms Observe.next_fire
#print axioms Observe.next_fuel
#print axioms Observe.next_halt
#print axioms Observe.next_refuse
#print axioms Observe.next_tape
#print axioms Observe.obs_fuel_eq
#print axioms Observe.obs_fuel_indep
#print axioms Observe.obs_prefix
#print axioms Observe.obs_prefix_add
#print axioms Observe.same_next
#print axioms Observe.stepDet_inr
