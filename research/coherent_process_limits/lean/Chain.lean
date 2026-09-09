import Steps

/-!
# Observe.Chain: the tape is a chain of the machine, and therefore functional

`nextOf` is what the *program* says about a datum: the value of the one enabled
operation, and none when none, two, or no edge — the fuel is not read.  A tape
is a chain when each entry is the next value of the entry before it, and a
chain is functional because the next value is a function of the datum.

`obs_functional` carries that along the whole run, for every controlled
setting, start, fuel and scale.

AuthorityEffect: None.
-/

namespace Observe

open Derivation Translation Execution Control Product Schedule Runner

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

/-! ## Generic facts about the next value and the step

These are about `nextOf` and `next`, not about any study over them.  They
were written inside the two-locus section and used by the periodicity one;
the split moved them to where both can reach them. -/

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

end Observe

#print axioms Observe.chain_functional
#print axioms Observe.chain_snoc
#print axioms Observe.getLast?_snoc
#print axioms Observe.init_chain
#print axioms Observe.iter_chain
#print axioms Observe.mem_pairsOf_snoc
#print axioms Observe.next_chain
#print axioms Observe.obs_functional
#print axioms Observe.nextOf_of_single
#print axioms Observe.nextOf_some
#print axioms Observe.next_graph
#print axioms Observe.iter_graph
