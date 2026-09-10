import Execution

/-!
# Branch: CFG-based Branching, Jump Tables, and Non-Selection

Target A: Represented Execution Substrate.
Control-flow graphs (CFG) and jump tables represented directly as graph data.

Forms:
- cfgStepForm (10): sequential edge (10, [src, target])
- cfgBranchForm (11): conditional branch (11, [pc, cond, target])
- jumpTableForm (12): jump table entry (12, [table_id, index, target])
- cfgIndirectForm (13): indirect jump (13, [pc, table_id])

Core Invariant:
Deterministic execution and branch non-selection.
If multiple branch edges match the active data/pc (a non-deterministic fork),
the interpreter explicitly refuses to select, returning Terminal.branch.

Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
AuthorityEffect: None.
Configuration status: DECLARED_HOST_CONFIG.
-/

namespace Branch

open Derivation Execution

def cfgStepForm : Nat := 10
def cfgBranchForm : Nat := 11
def jumpTableForm : Nat := 12
def cfgIndirectForm : Nat := 13

/-! ## 1. Reading CFG and Jump Table Instances from Graph Data -/

def isBranchEdge (pc cond : Nat) : Inst → Bool
  | (g, [p, c, _]) => decide (g = cfgBranchForm ∧ p = pc ∧ c = cond)
  | _ => false

def branchTarget : Inst → Nat
  | (_, [_, _, q]) => q
  | _ => 0

def lookupBranch (pc cond : Nat) (g : List Inst) : Option Nat :=
  (g.find? (isBranchEdge pc cond)).map branchTarget

theorem lookupBranch_mem {pc cond q : Nat} {g : List Inst}
    (h : lookupBranch pc cond g = some q) : (cfgBranchForm, [pc, cond, q]) ∈ g := by
  change (g.find? (isBranchEdge pc cond)).map branchTarget = some q at h
  cases hf : g.find? (isBranchEdge pc cond) with
  | none =>
      rw [hf] at h
      cases h
  | some i =>
      rw [hf] at h
      have hmem := List.mem_of_find?_eq_some hf
      have hedge := List.find?_some hf
      cases i with
      | mk g_inst args =>
          cases args with
          | nil => cases hedge
          | cons p args1 =>
              cases args1 with
              | nil => cases hedge
              | cons c args2 =>
                  cases args2 with
                  | nil => cases hedge
                  | cons q' args3 =>
                      cases args3 with
                      | cons _ _ => cases hedge
                      | nil =>
                          have h' : decide (g_inst = cfgBranchForm ∧ p = pc ∧ c = cond) = true := hedge
                          obtain ⟨rfl, rfl, rfl⟩ := of_decide_eq_true h'
                          have hq : q' = q := Option.some.inj h
                          subst hq
                          exact hmem

/-! ## 2. Jump Table Resolution -/

def isJumpTableEdge (tbl idx : Nat) : Inst → Bool
  | (g, [t, i, _]) => decide (g = jumpTableForm ∧ t = tbl ∧ i = idx)
  | _ => false

def jumpTarget : Inst → Nat
  | (_, [_, _, q]) => q
  | _ => 0

def lookupJumpTable (tbl idx : Nat) (g : List Inst) : Option Nat :=
  (g.find? (isJumpTableEdge tbl idx)).map jumpTarget

theorem jump_table_lookup {tbl idx q : Nat} {g : List Inst}
    (h : lookupJumpTable tbl idx g = some q) : (jumpTableForm, [tbl, idx, q]) ∈ g := by
  change (g.find? (isJumpTableEdge tbl idx)).map jumpTarget = some q at h
  cases hf : g.find? (isJumpTableEdge tbl idx) with
  | none =>
      rw [hf] at h
      cases h
  | some i =>
      rw [hf] at h
      have hmem := List.mem_of_find?_eq_some hf
      have hedge := List.find?_some hf
      cases i with
      | mk g_inst args =>
          cases args with
          | nil => cases hedge
          | cons t args1 =>
              cases args1 with
              | nil => cases hedge
              | cons i_idx args2 =>
                  cases args2 with
                  | nil => cases hedge
                  | cons q' args3 =>
                      cases args3 with
                      | cons _ _ => cases hedge
                      | nil =>
                          have h' : decide (g_inst = jumpTableForm ∧ t = tbl ∧ i_idx = idx) = true := hedge
                          obtain ⟨rfl, rfl, rfl⟩ := of_decide_eq_true h'
                          have hq : q' = q := Option.some.inj h
                          subst hq
                          exact hmem

/-! ## 3. Branch Target Enumeration & Non-Selection -/

def branchTargets (pc cond : Nat) (g : List Inst) : List Nat :=
  g.filterMap (fun i =>
    match i with
    | (g_inst, [p, c, q]) =>
        if g_inst = cfgBranchForm ∧ p = pc ∧ c = cond then some q else none
    | _ => none)

/-- Deterministic branch resolution:
    - [] => halt (no valid outgoing branch)
    - [q] => target q
    - >= 2 targets => branch (explicit refusal to select on a non-deterministic fork) -/
def stepBranch (pc cond : Nat) (g : List Inst) : Terminal ⊕ Nat :=
  match branchTargets pc cond g with
  | [] => .inl .halt
  | [q] => .inr q
  | _ :: _ :: _ => .inl .branch

theorem branch_non_selection {pc cond q1 q2 : Nat} {rest : List Nat} {g : List Inst}
    (h : branchTargets pc cond g = q1 :: q2 :: rest) :
    stepBranch pc cond g = .inl .branch := by
  have hstep : stepBranch pc cond g =
      (match branchTargets pc cond g with
      | [] => .inl .halt
      | [q] => .inr q
      | _ :: _ :: _ => .inl .branch) := rfl
  rw [hstep, h]

theorem branch_deterministic {pc cond q : Nat} {g : List Inst}
    (h : branchTargets pc cond g = [q]) :
    stepBranch pc cond g = .inr q := by
  have hstep : stepBranch pc cond g =
      (match branchTargets pc cond g with
      | [] => .inl .halt
      | [q] => .inr q
      | _ :: _ :: _ => .inl .branch) := rfl
  rw [hstep, h]

theorem branch_halt {pc cond : Nat} {g : List Inst}
    (h : branchTargets pc cond g = []) :
    stepBranch pc cond g = .inl .halt := by
  have hstep : stepBranch pc cond g =
      (match branchTargets pc cond g with
      | [] => .inl .halt
      | [q] => .inr q
      | _ :: _ :: _ => .inl .branch) := rfl
  rw [hstep, h]

/-! ## 4. CFG Execution State -/

structure CFGState where
  graph : List Inst
  pc : Nat
  data : Nat
  clock : Nat
  fuel : Nat

def stepCFG (s : CFGState) : Terminal ⊕ CFGState :=
  match stepBranch s.pc s.data s.graph with
  | .inl t => .inl t
  | .inr next_pc =>
    match s.fuel with
    | 0 => .inl .exhausted
    | f + 1 => .inr ⟨s.graph, next_pc, s.data, s.clock + 1, f⟩

theorem stepCFG_fork {s : CFGState} {q1 q2 : Nat} {rest : List Nat}
    (h : branchTargets s.pc s.data s.graph = q1 :: q2 :: rest) :
    stepCFG s = .inl .branch := by
  have hstep : stepCFG s =
      (match stepBranch s.pc s.data s.graph with
      | .inl t => .inl t
      | .inr next_pc =>
        match s.fuel with
        | 0 => .inl .exhausted
        | f + 1 => .inr ⟨s.graph, next_pc, s.data, s.clock + 1, f⟩) := rfl
  rw [hstep, branch_non_selection h]

theorem stepCFG_ok {s s' : CFGState} (h : stepCFG s = .inr s') :
    s'.clock = s.clock + 1 ∧ s.fuel = s'.fuel + 1 := by
  have hstep : stepCFG s =
      (match stepBranch s.pc s.data s.graph with
      | .inl t => .inl t
      | .inr next_pc =>
        match s.fuel with
        | 0 => .inl .exhausted
        | f + 1 => .inr ⟨s.graph, next_pc, s.data, s.clock + 1, f⟩) := rfl
  rw [hstep] at h
  cases hsb : stepBranch s.pc s.data s.graph with
  | inl t =>
      rw [hsb] at h
      cases h
  | inr next_pc =>
      rw [hsb] at h
      cases hfu : s.fuel with
      | zero =>
          rw [hfu] at h
          cases h
      | succ f =>
          rw [hfu] at h
          injection h with h'
          subst h'
          exact ⟨rfl, rfl⟩

theorem stepCFG_clock {s s' : CFGState} (h : stepCFG s = .inr s') :
    s'.clock = s.clock + 1 :=
  (stepCFG_ok h).1

theorem stepCFG_fuel {s s' : CFGState} (h : stepCFG s = .inr s') :
    s.fuel = s'.fuel + 1 :=
  (stepCFG_ok h).2

end Branch
