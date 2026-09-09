import Rename

/-!
# Runner: one machine, parameterised by what it reads

Three families here now run the same interpreter with three different
enablement reads: the merged one consults `enabledAt … s.active`, the
record-reading one `renabledAt … (previous s) s.active`, the depth-two one
`r2enabledAt … (before s) (previous s) s.active`.  Each copied the runner and
its theorems.

The question that copying raised was whether the reads have anything in
common beyond looking alike — specifically, whether a reader must see more
than the state.  **It need not.**  All three are functions `State → List Nat`,
so the runner is one function of a reader, and each family's runner is that
function at its own reader.

This module builds it: `stepDetOf`, `nextOf`, `iterOf`, `obsOf`, `runDetOf`
over an arbitrary `Reader`, with the theorems each family proved separately
proved once — the step is characterised by its read (`stepDetOf_inr`,
`stepDetOf_spec`), it never selects — and that is two implications, not one
(`stepDetOf_branch_iff`) —
and it only appends (`nextOf_tape`, `obsOf_prefix`, `obsOf_prefix_add`),
keeping the program (`nextOf_graph`).

Nothing existing is renamed or replaced.  The claim is made instead as an
**identification**: `Control.stepDet` *is* `stepDetOf ctrlReader`, by `rfl`
(`ctrl_stepDet`), and its runner is the generic runner at that reader
(`ctrl_runDet`).  The consuming families identify theirs the same way.  A
fourth read costs a `Reader` and no runner at all.

AuthorityEffect: None.
-/

namespace Runner

open Derivation Translation Execution Control

/-! ## 1. The machine over a reader -/

/-- What a machine of this family consults at a state to decide which
operations may fire.  It sees the state and nothing else — which is the whole
content of the abstraction. -/
abbrev Reader := State → List Nat

/-- One step: a terminal, or the next state.  It fires the one operation the
reader names, halts when it names none, and stops with `branch` when it names
two — it never selects. -/
def stepDetOf (read : Reader) (s : State) : Terminal ⊕ State :=
  match read s with
  | [] => .inl .halt
  | [k] =>
    match fire s k with
    | .ok s' => .inr s'
    | .exhausted => .inl .exhausted
    | .noEdge => .inl .refuse
  | _ :: _ :: _ => .inl .branch

/-- One step as a function: a terminal keeps the state. -/
def nextOf (read : Reader) (s : State) : State :=
  match stepDetOf read s with
  | .inr s' => s'
  | .inl _ => s

def iterOf (read : Reader) : Nat → State → State
  | 0, s => s
  | n + 1, s => nextOf read (iterOf read n s)

/-- The observation at scale `n`: the tape after `n` steps. -/
def obsOf (read : Reader) (n : Nat) (s : State) : List Nat := (iterOf read n s).tape

def runDetOf (read : Reader) : Nat → State → Terminal × State
  | 0, s =>
    match stepDetOf read s with
    | .inl t => (t, s)
    | .inr _ => (.exhausted, s)
  | b + 1, s =>
    match stepDetOf read s with
    | .inl t => (t, s)
    | .inr s' => runDetOf read b s'

/-! ## 2. The theorems, proved once -/

/-- A step that moves fired the one operation the reader named. -/
theorem stepDetOf_inr {read : Reader} {s s' : State} (h : stepDetOf read s = .inr s') :
    ∃ k, read s = [k] ∧ fire s k = .ok s' := by
  revert h
  show (match read s with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok t => Sum.inr t
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inr s' → _
  cases hr : read s with
  | nil =>
      intro h
      cases h
  | cons k rest =>
      cases rest with
      | nil =>
          show (match fire s k with
                | .ok t => Sum.inr t
                | .exhausted => Sum.inl Terminal.exhausted
                | .noEdge => Sum.inl Terminal.refuse) = Sum.inr s' → _
          cases hf : fire s k with
          | ok t =>
              intro h
              have ht : Sum.inr t = (Sum.inr s' : Terminal ⊕ State) := h
              injection ht with ht
              exact ⟨k, rfl, by rw [ht] at hf; exact hf⟩
          | exhausted =>
              intro h
              cases h
          | noEdge =>
              intro h
              cases h
      | cons k' rest' =>
          intro h
          cases h

/-- **One step, in full**, by what the reader named and what the edge said. -/
theorem stepDetOf_spec (read : Reader) (s : State) :
    (∃ t, stepDetOf read s = .inl t) ∨
      ∃ k f y, read s = [k] ∧ s.fuel = f + 1 ∧ lookup (3 + k) s.active s.graph = some y ∧
        stepDetOf read s = .inr ⟨s.graph, s.nops, y, s.tape ++ [y], s.clock + 1, f⟩ := by
  have hstep : stepDetOf read s =
      (match read s with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok t => Sum.inr t
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) := rfl
  cases hr : read s with
  | nil =>
      refine Or.inl ⟨Terminal.halt, ?_⟩
      rw [hstep, hr]
  | cons k rest =>
      cases rest with
      | nil =>
          cases hfu : s.fuel with
          | zero =>
              refine Or.inl ⟨Terminal.exhausted, ?_⟩
              rw [hstep, hr]
              show (match fire s k with
                    | .ok t => Sum.inr t
                    | .exhausted => Sum.inl Terminal.exhausted
                    | .noEdge => Sum.inl Terminal.refuse) = Sum.inl Terminal.exhausted
              rw [fire_exhausted hfu]
          | succ f =>
              cases hl : lookup (3 + k) s.active s.graph with
              | none =>
                  refine Or.inl ⟨Terminal.refuse, ?_⟩
                  rw [hstep, hr]
                  show (match fire s k with
                        | .ok t => Sum.inr t
                        | .exhausted => Sum.inl Terminal.exhausted
                        | .noEdge => Sum.inl Terminal.refuse) = Sum.inl Terminal.refuse
                  rw [fire_succ s k f hfu, hl]
              | some y =>
                  refine Or.inr ⟨k, f, y, rfl, rfl, hl, ?_⟩
                  rw [hstep, hr]
                  show (match fire s k with
                        | .ok t => Sum.inr t
                        | .exhausted => Sum.inl Terminal.exhausted
                        | .noEdge => Sum.inl Terminal.refuse) = _
                  rw [fire_succ s k f hfu, hl]
      | cons k' rest' =>
          refine Or.inl ⟨Terminal.branch, ?_⟩
          rw [hstep, hr]

/-- **It never selects**: `branch` only when the reader named two. -/
theorem stepDetOf_branch {read : Reader} {s : State} (h : stepDetOf read s = .inl .branch) :
    2 ≤ (read s).length := by
  revert h
  show (match read s with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok t => Sum.inr t
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) = Sum.inl Terminal.branch → _
  cases hr : read s with
  | nil =>
      intro h
      cases h
  | cons k rest =>
      cases rest with
      | nil =>
          show (match fire s k with
                | .ok t => Sum.inr t
                | .exhausted => Sum.inl Terminal.exhausted
                | .noEdge => Sum.inl Terminal.refuse) = Sum.inl Terminal.branch → _
          cases fire s k with
          | ok t =>
              intro h
              cases h
          | exhausted =>
              intro h
              cases h
          | noEdge =>
              intro h
              cases h
      | cons k' rest' =>
          intro _
          show 2 ≤ rest'.length + 2
          exact Nat.le_add_left 2 rest'.length

/-- **And it must**: two named is `branch`, not a choice.  `stepDetOf_branch`
alone is one implication — a runner that *selected* among two enabled
operations would return a state rather than `branch`, and that theorem would
stay true of it.  This is the converse, and the two together are what "never
selects" means. -/
theorem stepDetOf_of_two {read : Reader} {s : State} (h : 2 ≤ (read s).length) :
    stepDetOf read s = .inl .branch := by
  have hstep : stepDetOf read s =
      (match read s with
        | [] => Sum.inl Terminal.halt
        | [k] =>
          match fire s k with
          | .ok t => Sum.inr t
          | .exhausted => Sum.inl Terminal.exhausted
          | .noEdge => Sum.inl Terminal.refuse
        | _ :: _ :: _ => Sum.inl Terminal.branch) := rfl
  cases hr : read s with
  | nil =>
      rw [hr] at h
      have h0 : (2 : Nat) ≤ 0 := h
      exact absurd h0 (by omega)
  | cons k rest =>
      cases rest with
      | nil =>
          rw [hr] at h
          have h1 : (2 : Nat) ≤ 1 := h
          exact absurd h1 (by omega)
      | cons k' rest' =>
          rw [hstep, hr]

/-- **Never selects, both ways.** -/
theorem stepDetOf_branch_iff (read : Reader) (s : State) :
    stepDetOf read s = .inl .branch ↔ 2 ≤ (read s).length :=
  ⟨stepDetOf_branch, stepDetOf_of_two⟩

def BranchOkOf (read : Reader) (p : Terminal × State) : Prop :=
  p.1 = .branch → 2 ≤ (read p.2).length

/-- The runner's `branch` is honest at the state it returns. -/
theorem runDetOf_branch (read : Reader) : ∀ (b : Nat) (s : State),
    BranchOkOf read (runDetOf read b s)
  | 0, s => by
      show BranchOkOf read (match stepDetOf read s with
                            | .inl t => (t, s)
                            | .inr _ => (Terminal.exhausted, s))
      cases hs : stepDetOf read s with
      | inl t =>
          intro h
          have ht : t = Terminal.branch := h
          subst ht
          exact stepDetOf_branch hs
      | inr s' =>
          intro h
          cases h
  | b + 1, s => by
      show BranchOkOf read (match stepDetOf read s with
                            | .inl t => (t, s)
                            | .inr s' => runDetOf read b s')
      cases hs : stepDetOf read s with
      | inl t =>
          intro h
          have ht : t = Terminal.branch := h
          subst ht
          exact stepDetOf_branch hs
      | inr s' => exact runDetOf_branch read b s'

/-- **A step only appends**, whatever the reader named. -/
theorem nextOf_tape (read : Reader) (s : State) : s.tape <+: (nextOf read s).tape := by
  cases hs : stepDetOf read s with
  | inl t =>
      have hn : nextOf read s = s := by
        show (match stepDetOf read s with | .inr s' => s' | .inl _ => s) = s
        rw [hs]
      rw [hn]
      exact List.prefix_refl _
  | inr s' =>
      have hn : nextOf read s = s' := by
        show (match stepDetOf read s with | .inr s' => s' | .inl _ => s) = s'
        rw [hs]
      obtain ⟨k, -, hf⟩ := stepDetOf_inr hs
      obtain ⟨-, htape, -, -, -, -⟩ := fire_ok hf
      rw [hn, htape]
      exact ⟨[s'.active], rfl⟩

/-- **A step keeps the program.** -/
theorem nextOf_graph (read : Reader) (s : State) :
    (nextOf read s).graph = s.graph ∧ (nextOf read s).nops = s.nops := by
  cases hs : stepDetOf read s with
  | inl t =>
      have hn : nextOf read s = s := by
        show (match stepDetOf read s with | .inr s' => s' | .inl _ => s) = s
        rw [hs]
      rw [hn]
      exact ⟨rfl, rfl⟩
  | inr s' =>
      have hn : nextOf read s = s' := by
        show (match stepDetOf read s with | .inr s' => s' | .inl _ => s) = s'
        rw [hs]
      obtain ⟨k, -, hf⟩ := stepDetOf_inr hs
      obtain ⟨-, -, -, -, hg, hnn⟩ := fire_ok hf
      rw [hn]
      exact ⟨hg, hnn⟩

theorem iterOf_succ (read : Reader) : ∀ (n : Nat) (s : State),
    iterOf read (n + 1) s = iterOf read n (nextOf read s)
  | 0, _ => rfl
  | n + 1, s => by
      show nextOf read (iterOf read (n + 1) s) = nextOf read (iterOf read n (nextOf read s))
      rw [iterOf_succ read n s]

/-- **Compatibility**: the observation at a scale is a prefix of the next. -/
theorem obsOf_prefix (read : Reader) (n : Nat) (s : State) :
    obsOf read n s <+: obsOf read (n + 1) s :=
  nextOf_tape read (iterOf read n s)

theorem obsOf_prefix_add (read : Reader) (m : Nat) (s : State) :
    ∀ k, obsOf read m s <+: obsOf read (m + k) s
  | 0 => List.prefix_refl _
  | k + 1 => (obsOf_prefix_add read m s k).trans (obsOf_prefix read (m + k) s)

/-! ## 3. The merged machine is this machine at its reader -/

/-- What the merged machine reads: the enablements at the active datum. -/
def ctrlReader (s : State) : List Nat := enabledAt s.graph s.nops s.active

/-- **The identification, by `rfl`.**  `Control.stepDet` is not *like* the
generic step at this reader; it is that step. -/
theorem ctrl_stepDet (s : State) : Control.stepDet s = stepDetOf ctrlReader s := rfl

theorem ctrl_runDet : ∀ (b : Nat) (s : State), Control.runDet b s = runDetOf ctrlReader b s
  | 0, s => rfl
  | b + 1, s => by
      cases h : Control.stepDet s with
      | inl t =>
          have h1 : Control.runDet (b + 1) s = (t, s) := by
            show (match Control.stepDet s with
                  | .inl t => (t, s)
                  | .inr s' => Control.runDet b s') = (t, s)
            rw [h]
          have h2 : runDetOf ctrlReader (b + 1) s = (t, s) := by
            show (match stepDetOf ctrlReader s with
                  | .inl t => (t, s)
                  | .inr s' => runDetOf ctrlReader b s') = (t, s)
            rw [← ctrl_stepDet s, h]
          rw [h1, h2]
      | inr s' =>
          have h1 : Control.runDet (b + 1) s = Control.runDet b s' := by
            show (match Control.stepDet s with
                  | .inl t => (t, s)
                  | .inr s' => Control.runDet b s') = _
            rw [h]
          have h2 : runDetOf ctrlReader (b + 1) s = runDetOf ctrlReader b s' := by
            show (match stepDetOf ctrlReader s with
                  | .inl t => (t, s)
                  | .inr s' => runDetOf ctrlReader b s') = _
            rw [← ctrl_stepDet s, h]
          rw [h1, h2, ctrl_runDet b s']

theorem ctrl_run (s : State) : Control.run s = runDetOf ctrlReader s.fuel s :=
  ctrl_runDet s.fuel s

/-- And the theorems the merged family proved separately follow from the
generic ones at this reader.  Restated rather than re-proved: the point is
that these two lines are the whole of the specialisation. -/
theorem ctrl_stepDet_branch {s : State} (h : Control.stepDet s = .inl .branch) :
    2 ≤ (enabledAt s.graph s.nops s.active).length :=
  stepDetOf_branch (read := ctrlReader) (by rw [← ctrl_stepDet s]; exact h)

theorem ctrl_run_branch (s : State) : BranchOkOf ctrlReader (Control.run s) := by
  rw [ctrl_run s]
  exact runDetOf_branch ctrlReader s.fuel s

/-- The merged machine's disqualifier, both ways: with two operations enabled
the step **is** `branch`, so the runner cannot be selecting. -/
theorem ctrl_branch_iff (s : State) :
    Control.stepDet s = .inl .branch ↔ 2 ≤ (enabledAt s.graph s.nops s.active).length := by
  rw [ctrl_stepDet s]
  exact stepDetOf_branch_iff ctrlReader s

/-! ## 4. The reader sees the state, and that is the point -/

/-- **A reader that ignores the state is a machine that halts or loops.**  The
abstraction would be empty if every reader had to be the merged one; it is not,
and the two extremes are both readers. -/
def blindReader (_ : State) : List Nat := []

theorem blind_halts (s : State) : stepDetOf blindReader s = .inl .halt := rfl

/-- Two operations named at every state is a machine that always branches: the
generic runner refuses it exactly as each copy did. -/
def greedyReader (_ : State) : List Nat := [0, 1]

theorem greedy_branches (s : State) : stepDetOf greedyReader s = .inl .branch := rfl

end Runner

#print axioms Runner.stepDetOf_inr
#print axioms Runner.stepDetOf_spec
#print axioms Runner.stepDetOf_branch
#print axioms Runner.stepDetOf_of_two
#print axioms Runner.stepDetOf_branch_iff
#print axioms Runner.runDetOf_branch
#print axioms Runner.nextOf_tape
#print axioms Runner.nextOf_graph
#print axioms Runner.iterOf_succ
#print axioms Runner.obsOf_prefix
#print axioms Runner.obsOf_prefix_add
#print axioms Runner.ctrl_stepDet
#print axioms Runner.ctrl_runDet
#print axioms Runner.ctrl_run
#print axioms Runner.ctrl_stepDet_branch
#print axioms Runner.ctrl_run_branch
#print axioms Runner.ctrl_branch_iff
#print axioms Runner.blind_halts
#print axioms Runner.greedy_branches
