import Derivation.Basic
import Execution
import Control
import Runner
import Observe
import Select
import Depth

/-!
# Target 5: Cross-Language Mirror-Refinement in Lean 4

This module formalizes a general relational transition machine refinement
framework (`MachineRefinement`) and proves:
1. One-step refinement preservation (`step_preserves_state`, `step_preserves_term`).
2. Total step preservation (`next_preserves_refinement`).
3. Multi-step iteration preservation (`iter_preserves_refinement`).
4. Observation projection preservation (`obs_preserves_refinement`).

The general refinement theorem is then instantiated across three research trees:
1. `research/represented_execution`: `Runner.stepDetOf` vs Python `runner.py:step_det_of`.
2. `research/coherent_process_limits`: `Observe.next` / `Observe.obs` vs Python `limits.py:next_state` / `obs`.
3. `research/record_reading`: `Depth.r2stepDet` / `Depth.r2obs` vs Python `depth.py:r2step_det` / `r2obs`.

All proofs are constructive with axioms strictly audited to `{propext, Quot.sound}`.
AuthorityEffect: None.
-/

namespace MirrorRefinement

open Derivation Execution Control Runner Observe Select Depth

set_option linter.unusedSimpArgs false

/-! ## 1. General Transition Machine Refinement Framework -/

/-- A deterministic transition machine with explicit terminal outcomes. -/
structure Machine (State : Type) (Terminal : Type) where
  step : State → Terminal ⊕ State

/-- Total single-step execution: at a terminal outcome, the state stands stationary. -/
def Machine.next {State Terminal : Type} (m : Machine State Terminal) (s : State) : State :=
  match m.step s with
  | .inr s' => s'
  | .inl _ => s

/-- Multi-step iteration up to scale `n`. -/
def Machine.iter {State Terminal : Type} (m : Machine State Terminal) : Nat → State → State
  | 0, s => s
  | n + 1, s => m.next (m.iter n s)

/-- Relational simulation / machine refinement between a specification machine
    and an implementation machine. -/
structure MachineRefinement {S_spec S_impl T_spec T_impl : Type}
    (spec : Machine S_spec T_spec)
    (impl : Machine S_impl T_impl)
    (R_state : S_spec → S_impl → Prop)
    (R_term : T_spec → T_impl → Prop) : Prop where
  /-- Implementation state-transitions are faithfully matched by specification transitions. -/
  step_preserves_state : ∀ s_spec s_impl s'_impl,
    R_state s_spec s_impl →
    impl.step s_impl = Sum.inr s'_impl →
    ∃ s'_spec, spec.step s_spec = Sum.inr s'_spec ∧ R_state s'_spec s'_impl
  /-- Implementation terminal outcomes are faithfully matched by specification terminal outcomes. -/
  step_preserves_term : ∀ s_spec s_impl t_impl,
    R_state s_spec s_impl →
    impl.step s_impl = Sum.inl t_impl →
    ∃ t_spec, spec.step s_spec = Sum.inl t_spec ∧ R_term t_spec t_impl
  /-- Specification state-transitions are matched by implementation transitions. -/
  spec_step_state : ∀ s_spec s_impl s'_spec,
    R_state s_spec s_impl →
    spec.step s_spec = Sum.inr s'_spec →
    ∃ s'_impl, impl.step s_impl = Sum.inr s'_impl ∧ R_state s'_spec s'_impl
  /-- Specification terminal outcomes are matched by implementation terminal outcomes. -/
  spec_step_term : ∀ s_spec s_impl t_spec,
    R_state s_spec s_impl →
    spec.step s_spec = Sum.inl t_spec →
    ∃ t_impl, impl.step s_impl = Sum.inl t_impl ∧ R_term t_spec t_impl

/-- General theorem: single-step execution preserves the state refinement relation. -/
theorem next_preserves_refinement {S_spec S_impl T_spec T_impl : Type}
    {spec : Machine S_spec T_spec} {impl : Machine S_impl T_impl}
    {R_state : S_spec → S_impl → Prop} {R_term : T_spec → T_impl → Prop}
    (ref : MachineRefinement spec impl R_state R_term) :
    ∀ s_spec s_impl, R_state s_spec s_impl →
      R_state (spec.next s_spec) (impl.next s_impl) := by
  intro s_spec s_impl hR
  cases h_impl : impl.step s_impl with
  | inr s'_impl =>
    obtain ⟨s'_spec, h_spec, hR'⟩ := ref.step_preserves_state s_spec s_impl s'_impl hR h_impl
    have hn_impl : impl.next s_impl = s'_impl := by
      show (match impl.step s_impl with | .inr s' => s' | .inl _ => s_impl) = s'_impl
      rw [h_impl]
    have hn_spec : spec.next s_spec = s'_spec := by
      show (match spec.step s_spec with | .inr s' => s' | .inl _ => s_spec) = s'_spec
      rw [h_spec]
    rw [hn_impl, hn_spec]
    exact hR'
  | inl t_impl =>
    obtain ⟨t_spec, h_spec, _⟩ := ref.step_preserves_term s_spec s_impl t_impl hR h_impl
    have hn_impl : impl.next s_impl = s_impl := by
      show (match impl.step s_impl with | .inr s' => s' | .inl _ => s_impl) = s_impl
      rw [h_impl]
    have hn_spec : spec.next s_spec = s_spec := by
      show (match spec.step s_spec with | .inr s' => s' | .inl _ => s_spec) = s_spec
      rw [h_spec]
    rw [hn_impl, hn_spec]
    exact hR

/-- General theorem: multi-step iteration preserves the state refinement relation for all n. -/
theorem iter_preserves_refinement {S_spec S_impl T_spec T_impl : Type}
    {spec : Machine S_spec T_spec} {impl : Machine S_impl T_impl}
    {R_state : S_spec → S_impl → Prop} {R_term : T_spec → T_impl → Prop}
    (ref : MachineRefinement spec impl R_state R_term) :
    ∀ n s_spec s_impl, R_state s_spec s_impl →
      R_state (spec.iter n s_spec) (impl.iter n s_impl) := by
  intro n
  induction n with
  | zero =>
    intro s_spec s_impl hR
    exact hR
  | succ k ih =>
    intro s_spec s_impl hR
    show R_state (spec.next (spec.iter k s_spec)) (impl.next (impl.iter k s_impl))
    exact next_preserves_refinement ref (spec.iter k s_spec) (impl.iter k s_impl) (ih s_spec s_impl hR)

/-- General theorem: observation projection commutes under arbitrary iteration
    whenever the projection respects the simulation relation. -/
theorem obs_preserves_refinement {S_spec S_impl T_spec T_impl Obs : Type}
    {spec : Machine S_spec T_spec} {impl : Machine S_impl T_impl}
    {R_state : S_spec → S_impl → Prop} {R_term : T_spec → T_impl → Prop}
    (ref : MachineRefinement spec impl R_state R_term)
    (obs_spec : S_spec → Obs) (obs_impl : S_impl → Obs)
    (h_obs : ∀ s_s s_i, R_state s_s s_i → obs_spec s_s = obs_impl s_i) :
    ∀ n s_spec s_impl, R_state s_spec s_impl →
      obs_spec (spec.iter n s_spec) = obs_impl (impl.iter n s_impl) := by
  intro n s_spec s_impl hR
  have h_iter := iter_preserves_refinement ref n s_spec s_impl hR
  exact h_obs _ _ h_iter

/-! ## 2. Python Mirror Data Types and Mirror Operations -/

/-- Discrete representation of Python runtime terminal outcome tags. -/
inductive PyTerminal
  | halt
  | exhausted
  | refuse
  | branch
  deriving DecidableEq, Repr

/-- Discrete representation of Python runtime state structure (`control.State`). -/
structure PyState where
  graph  : List Inst
  nops   : Nat
  active : Nat
  tape   : List Nat
  clock  : Nat
  fuel   : Nat
  deriving DecidableEq, Repr

/-- Mapping from Python terminal outcomes to Lean kernel terminal types. -/
def pyTerminalToTerminal : PyTerminal → Control.Terminal
  | .halt => .halt
  | .exhausted => .exhausted
  | .refuse => .refuse
  | .branch => .branch

/-- Mapping from Lean kernel terminal types to Python terminal outcomes. -/
def terminalToPyTerminal : Control.Terminal → PyTerminal
  | .halt => .halt
  | .exhausted => .exhausted
  | .refuse => .refuse
  | .branch => .branch

/-- Decoding function mapping Python state representation to Lean kernel state. -/
def pyStateToState (p : PyState) : Control.State :=
  ⟨p.graph, p.nops, p.active, p.tape, p.clock, p.fuel⟩

/-- Encoding function mapping Lean kernel state to Python state representation. -/
def stateToPyState (s : Control.State) : PyState :=
  ⟨s.graph, s.nops, s.active, s.tape, s.clock, s.fuel⟩

@[simp] theorem pyStateToState_stateToPyState (s : Control.State) :
    pyStateToState (stateToPyState s) = s := by
  cases s; rfl

@[simp] theorem stateToPyState_pyStateToState (p : PyState) :
    stateToPyState (pyStateToState p) = p := by
  cases p; rfl

@[simp] theorem pyTerminalToTerminal_terminalToPyTerminal (t : Control.Terminal) :
    pyTerminalToTerminal (terminalToPyTerminal t) = t := by
  cases t <;> rfl

@[simp] theorem terminalToPyTerminal_pyTerminalToTerminal (pt : PyTerminal) :
    terminalToPyTerminal (pyTerminalToTerminal pt) = pt := by
  cases pt <;> rfl

/-- State simulation relation between Lean specification state and Python mirror state. -/
def R_runner (s : Control.State) (p : PyState) : Prop :=
  pyStateToState p = s

/-- Terminal simulation relation between Lean specification terminal and Python terminal outcome. -/
def R_term_runner (t : Control.Terminal) (pt : PyTerminal) : Prop :=
  pyTerminalToTerminal pt = t

/-- Python mirror of `fire` operation in `control.py:fire`. -/
def pyFire (p : PyState) (k : Nat) : PyTerminal ⊕ PyState :=
  match p.fuel with
  | 0 => .inl .exhausted
  | f + 1 =>
    match Execution.lookup (3 + k) p.active p.graph with
    | none => .inl .refuse
    | some y => .inr ⟨p.graph, p.nops, y, p.tape ++ [y], p.clock + 1, f⟩

/-- Python mirror of `step_det_of` in `runner.py:step_det_of`. -/
def pyStepDetOf (read : Runner.Reader) (p : PyState) : PyTerminal ⊕ PyState :=
  match read (pyStateToState p) with
  | [] => .inl .halt
  | [k] => pyFire p k
  | _ :: _ :: _ => .inl .branch

theorem pyStepDetOf_equiv (read : Runner.Reader) (p : PyState) :
    (match pyStepDetOf read p with
     | .inr p' => Sum.inr (pyStateToState p')
     | .inl pt => Sum.inl (pyTerminalToTerminal pt)) =
    Runner.stepDetOf read (pyStateToState p) := by
  cases p with
  | mk graph nops active tape clock fuel =>
    dsimp [pyStepDetOf, Runner.stepDetOf, pyStateToState]
    cases hr : read ⟨graph, nops, active, tape, clock, fuel⟩ with
    | nil => rfl
    | cons k rest =>
      cases rest with
      | nil =>
        dsimp [pyFire, Control.fire]
        cases fuel with
        | zero => rfl
        | succ f =>
          cases Execution.lookup (3 + k) active graph with
          | none => rfl
          | some y => rfl
      | cons k' rest' => rfl

/-! ## 3. Instantiation 1: research/represented_execution -/

/-- Specification machine for `represented_execution` runner. -/
def runnerMachine (read : Runner.Reader) : Machine Control.State Control.Terminal where
  step := Runner.stepDetOf read

/-- Python implementation machine mirroring `runner.py:step_det_of`. -/
def pyRunnerMachine (read : Runner.Reader) : Machine PyState PyTerminal where
  step := pyStepDetOf read

/-- Cross-language machine refinement theorem for `represented_execution`:
    the Python runner implementation faithfully refines the Lean specification machine. -/
theorem runner_refinement (read : Runner.Reader) :
    MachineRefinement (runnerMachine read) (pyRunnerMachine read) R_runner R_term_runner where
  step_preserves_state := by
    intro s_spec s_impl s'_impl hR h_step
    have heq := pyStepDetOf_equiv read s_impl
    have h_py : (pyRunnerMachine read).step s_impl = pyStepDetOf read s_impl := rfl
    rw [h_py] at h_step
    rw [h_step] at heq
    subst hR
    refine ⟨pyStateToState s'_impl, heq.symm, rfl⟩
  step_preserves_term := by
    intro s_spec s_impl t_impl hR h_step
    have heq := pyStepDetOf_equiv read s_impl
    have h_py : (pyRunnerMachine read).step s_impl = pyStepDetOf read s_impl := rfl
    rw [h_py] at h_step
    rw [h_step] at heq
    subst hR
    refine ⟨pyTerminalToTerminal t_impl, heq.symm, rfl⟩
  spec_step_state := by
    intro s_spec s_impl s'_spec hR h_step
    subst hR
    have heq := pyStepDetOf_equiv read s_impl
    have h_spec_step : (runnerMachine read).step (pyStateToState s_impl) = Runner.stepDetOf read (pyStateToState s_impl) := rfl
    rw [h_spec_step] at h_step
    cases h_impl : pyStepDetOf read s_impl with
    | inr p' =>
      rw [h_impl] at heq
      have heq2 : Sum.inr (pyStateToState p') = Sum.inr s'_spec := heq.trans h_step
      injection heq2 with heq_s'
      subst heq_s'
      have h_mach : (pyRunnerMachine read).step s_impl = Sum.inr p' := h_impl
      refine ⟨p', h_mach, rfl⟩
    | inl pt =>
      rw [h_impl] at heq
      have heq2 : Sum.inl (pyTerminalToTerminal pt) = Sum.inr s'_spec := heq.trans h_step
      cases heq2
  spec_step_term := by
    intro s_spec s_impl t_spec hR h_step
    subst hR
    have heq := pyStepDetOf_equiv read s_impl
    have h_spec_step : (runnerMachine read).step (pyStateToState s_impl) = Runner.stepDetOf read (pyStateToState s_impl) := rfl
    rw [h_spec_step] at h_step
    cases h_impl : pyStepDetOf read s_impl with
    | inr p' =>
      rw [h_impl] at heq
      have heq2 : Sum.inr (pyStateToState p') = Sum.inl t_spec := heq.trans h_step
      cases heq2
    | inl pt =>
      rw [h_impl] at heq
      have heq2 : Sum.inl (pyTerminalToTerminal pt) = Sum.inl t_spec := heq.trans h_step
      injection heq2 with heq_t
      subst heq_t
      have h_mach : (pyRunnerMachine read).step s_impl = Sum.inl pt := h_impl
      refine ⟨pt, h_mach, rfl⟩

theorem runnerMachine_next_eq (read : Runner.Reader) (s : Control.State) :
    (runnerMachine read).next s = Runner.nextOf read s := by
  dsimp [Machine.next, runnerMachine, Runner.nextOf]
  cases Runner.stepDetOf read s <;> rfl

theorem runnerMachine_iter_eq (read : Runner.Reader) :
    ∀ n s, (runnerMachine read).iter n s = Runner.iterOf read n s
  | 0, _ => rfl
  | n + 1, s => by
    show (runnerMachine read).next ((runnerMachine read).iter n s) = Runner.nextOf read (Runner.iterOf read n s)
    rw [runnerMachine_iter_eq read n s, runnerMachine_next_eq]

/-- Multi-step iteration preservation for `represented_execution`. -/
theorem runner_iter_refinement (read : Runner.Reader) (n : Nat) (s : Control.State) (p : PyState)
    (hR : R_runner s p) :
    R_runner (Runner.iterOf read n s) ((pyRunnerMachine read).iter n p) := by
  have h_iter := iter_preserves_refinement (runner_refinement read) n s p hR
  have heq := runnerMachine_iter_eq read n s
  rw [heq] at h_iter
  exact h_iter

/-- Tape observation projection preservation for `represented_execution`. -/
theorem runner_obs_refinement (read : Runner.Reader) (n : Nat) (s : Control.State) (p : PyState)
    (hR : R_runner s p) :
    Runner.obsOf read n s = ((pyRunnerMachine read).iter n p).tape := by
  have hR_iter := runner_iter_refinement read n s p hR
  exact congrArg Control.State.tape hR_iter.symm

/-! ## 4. Instantiation 2: research/coherent_process_limits -/

/-- Specification machine for `coherent_process_limits` process observation. -/
def observeMachine : Machine Control.State Control.Terminal where
  step := Control.stepDet

/-- Python implementation machine mirroring `limits.py:next_state`. -/
def pyLimitsMachine : Machine PyState PyTerminal where
  step := pyStepDetOf Runner.ctrlReader

theorem observeMachine_eq_runnerMachine :
    observeMachine.step = (runnerMachine Runner.ctrlReader).step := by
  funext s
  show Control.stepDet s = Runner.stepDetOf Runner.ctrlReader s
  exact Runner.ctrl_stepDet s

/-- Cross-language machine refinement theorem for `coherent_process_limits`:
    the Python limits runner faithfully refines the Lean process observation machine. -/
theorem limits_refinement :
    MachineRefinement observeMachine pyLimitsMachine R_runner R_term_runner where
  step_preserves_state := by
    intro s_spec s_impl s'_impl hR h_step
    have h_ref := (runner_refinement Runner.ctrlReader).step_preserves_state s_spec s_impl s'_impl hR h_step
    obtain ⟨s'_spec, hs, hR'⟩ := h_ref
    rw [observeMachine_eq_runnerMachine]
    exact ⟨s'_spec, hs, hR'⟩
  step_preserves_term := by
    intro s_spec s_impl t_impl hR h_step
    have h_ref := (runner_refinement Runner.ctrlReader).step_preserves_term s_spec s_impl t_impl hR h_step
    obtain ⟨t_spec, hs, hR'⟩ := h_ref
    rw [observeMachine_eq_runnerMachine]
    exact ⟨t_spec, hs, hR'⟩
  spec_step_state := by
    intro s_spec s_impl s'_spec hR h_step
    have hs' : (runnerMachine Runner.ctrlReader).step s_spec = Sum.inr s'_spec := by
      rw [← observeMachine_eq_runnerMachine]
      exact h_step
    exact (runner_refinement Runner.ctrlReader).spec_step_state s_spec s_impl s'_spec hR hs'
  spec_step_term := by
    intro s_spec s_impl t_spec hR h_step
    have hs' : (runnerMachine Runner.ctrlReader).step s_spec = Sum.inl t_spec := by
      rw [← observeMachine_eq_runnerMachine]
      exact h_step
    exact (runner_refinement Runner.ctrlReader).spec_step_term s_spec s_impl t_spec hR hs'

theorem observeMachine_next_eq (s : Control.State) :
    observeMachine.next s = Observe.next s := by
  dsimp [Machine.next, observeMachine, Observe.next]
  cases Control.stepDet s <;> rfl

theorem observeMachine_iter_eq : ∀ n s, observeMachine.iter n s = Observe.iter n s
  | 0, _ => rfl
  | n + 1, s => by
    show observeMachine.next (observeMachine.iter n s) = Observe.next (Observe.iter n s)
    rw [observeMachine_iter_eq n s, observeMachine_next_eq]

/-- Observation projection preservation for `coherent_process_limits` at scale `n`:
    the Python `limits.py:obs` observation matches Lean `Observe.obs`. -/
theorem limits_obs_refinement (n : Nat) (s : Control.State) (p : PyState)
    (hR : R_runner s p) :
    Observe.obs n s = (pyLimitsMachine.iter n p).tape := by
  have h_iter := iter_preserves_refinement limits_refinement n s p hR
  have h_tape : (observeMachine.iter n s).tape = (pyLimitsMachine.iter n p).tape :=
    congrArg Control.State.tape h_iter.symm
  have heq := observeMachine_iter_eq n s
  rw [heq] at h_tape
  exact h_tape

/-! ## 5. Instantiation 3: research/record_reading -/

/-- Specification machine for `record_reading` depth-two runner. -/
def depthMachine : Machine Control.State Control.Terminal where
  step := Depth.r2stepDet

/-- Python implementation machine mirroring `depth.py:r2step_det`. -/
def pyDepthMachine : Machine PyState PyTerminal where
  step := pyStepDetOf Depth.depthReader

theorem depthMachine_eq_runnerMachine :
    depthMachine.step = (runnerMachine Depth.depthReader).step := rfl

/-- Cross-language machine refinement theorem for `record_reading`:
    the Python depth-two runner faithfully refines the Lean specification machine. -/
theorem depth_refinement :
    MachineRefinement depthMachine pyDepthMachine R_runner R_term_runner where
  step_preserves_state := by
    intro s_spec s_impl s'_impl hR h_step
    have h_ref := (runner_refinement Depth.depthReader).step_preserves_state s_spec s_impl s'_impl hR h_step
    obtain ⟨s'_spec, hs, hR'⟩ := h_ref
    exact ⟨s'_spec, hs, hR'⟩
  step_preserves_term := by
    intro s_spec s_impl t_impl hR h_step
    have h_ref := (runner_refinement Depth.depthReader).step_preserves_term s_spec s_impl t_impl hR h_step
    obtain ⟨t_spec, hs, hR'⟩ := h_ref
    exact ⟨t_spec, hs, hR'⟩
  spec_step_state := by
    intro s_spec s_impl s'_spec hR h_step
    exact (runner_refinement Depth.depthReader).spec_step_state s_spec s_impl s'_spec hR h_step
  spec_step_term := by
    intro s_spec s_impl t_spec hR h_step
    exact (runner_refinement Depth.depthReader).spec_step_term s_spec s_impl t_spec hR h_step

theorem depthMachine_next_eq (s : Control.State) :
    depthMachine.next s = Depth.r2next s := by
  dsimp [Machine.next, depthMachine, Depth.r2next]
  cases Depth.r2stepDet s <;> rfl

theorem depthMachine_iter_eq : ∀ n s, depthMachine.iter n s = Depth.r2iter n s
  | 0, _ => rfl
  | n + 1, s => by
    show depthMachine.next (depthMachine.iter n s) = Depth.r2next (Depth.r2iter n s)
    rw [depthMachine_iter_eq n s, depthMachine_next_eq]

/-- Observation projection preservation for `record_reading` at scale `n`:
    the Python `depth.py:r2obs` observation matches Lean `Depth.r2obs`. -/
theorem depth_obs_refinement (n : Nat) (s : Control.State) (p : PyState)
    (hR : R_runner s p) :
    Depth.r2obs n s = (pyDepthMachine.iter n p).tape := by
  have h_iter := iter_preserves_refinement depth_refinement n s p hR
  have h_tape : (depthMachine.iter n s).tape = (pyDepthMachine.iter n p).tape :=
    congrArg Control.State.tape h_iter.symm
  have heq := depthMachine_iter_eq n s
  rw [heq] at h_tape
  exact h_tape

end MirrorRefinement

#print axioms MirrorRefinement.next_preserves_refinement
#print axioms MirrorRefinement.iter_preserves_refinement
#print axioms MirrorRefinement.obs_preserves_refinement
#print axioms MirrorRefinement.pyStepDetOf_equiv
#print axioms MirrorRefinement.runner_refinement
#print axioms MirrorRefinement.runner_iter_refinement
#print axioms MirrorRefinement.runner_obs_refinement
#print axioms MirrorRefinement.limits_refinement
#print axioms MirrorRefinement.limits_obs_refinement
#print axioms MirrorRefinement.depth_refinement
#print axioms MirrorRefinement.depth_obs_refinement
