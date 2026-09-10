import Capability

namespace G010

/-!
# G010 Operational Capability Removal

Constructive ASTs, state representations, and step functions where branching,
memory retention, and dynamic allocation are physically removed from syntax and state.

AuthorityEffect: None.
-/

/-- Linear straight-line operations: branching, memory store, and alloc are physically absent. -/
inductive LinearOp where
  | nop : LinearOp
  | setConst : Nat → Nat → LinearOp    -- dst, val
  | add : Nat → Nat → Nat → LinearOp   -- dst, src1, src2
  | inc : Nat → LinearOp               -- reg
  | emit : Nat → LinearOp              -- src
  | halt : LinearOp
  deriving DecidableEq, Repr

/-- Linear state: memory heap and dynamic allocator are physically absent. -/
structure LinearState where
  pc : Nat
  regs : Nat → Nat
  outputTape : List Nat
  halted : Bool
  steps : Nat

def initLinearState (inputs : List Nat) : LinearState :=
  { pc := 0,
    regs := fun idx => inputs.getD idx 0,
    outputTape := [],
    halted := false,
    steps := 0 }

def fetchLinear : Nat → List LinearOp → Option LinearOp
  | 0, [] => none
  | 0, op :: _ => some op
  | _ + 1, [] => none
  | n + 1, _ :: rest => fetchLinear n rest

def stepLinearOp : LinearOp → LinearState → LinearState
  | LinearOp.nop, st =>
    { st with pc := st.pc + 1, steps := st.steps + 1 }
  | LinearOp.setConst dst val, st =>
    { st with pc := st.pc + 1,
              regs := fun r => if r == dst then val else st.regs r,
              steps := st.steps + 1 }
  | LinearOp.add dst s1 s2, st =>
    { st with pc := st.pc + 1,
              regs := fun r => if r == dst then st.regs s1 + st.regs s2 else st.regs r,
              steps := st.steps + 1 }
  | LinearOp.inc reg, st =>
    { st with pc := st.pc + 1,
              regs := fun r => if r == reg then st.regs reg + 1 else st.regs r,
              steps := st.steps + 1 }
  | LinearOp.emit src, st =>
    { st with pc := st.pc + 1,
              outputTape := st.outputTape ++ [st.regs src],
              steps := st.steps + 1 }
  | LinearOp.halt, st =>
    { st with halted := true, steps := st.steps + 1 }

def stepLinearFetched : Option LinearOp → LinearState → LinearState
  | none, st => { st with halted := true }
  | some op, st => stepLinearOp op st

def stepLinear (prog : List LinearOp) (st : LinearState) : LinearState :=
  if st.halted then st
  else stepLinearFetched (fetchLinear st.pc prog) st

def runLinear (prog : List LinearOp) (fuel : Nat) (st : LinearState) : LinearState :=
  match fuel with
  | 0 => st
  | fuel' + 1 =>
    if st.halted then st
    else runLinear prog fuel' (stepLinear prog st)

def observeLinear (st : LinearState) : PublicObservation :=
  { outputTape := st.outputTape, steps := st.steps, halted := st.halted }

theorem linear_halted_step (prog : List LinearOp) (st : LinearState) (h : st.halted = true) :
    stepLinear prog st = st := by
  dsimp [stepLinear]
  simp [h]

theorem linear_run_zero (prog : List LinearOp) (st : LinearState) :
    runLinear prog 0 st = st := by
  rfl

/-- Full instruction set including branching, memory, and allocation. -/
inductive FullOp where
  | nop : FullOp
  | setConst : Nat → Nat → FullOp
  | add : Nat → Nat → Nat → FullOp
  | inc : Nat → FullOp
  | emit : Nat → FullOp
  | halt : FullOp
  | jumpIfZero : Nat → Nat → FullOp   -- condReg, targetPc
  | storeMem : Nat → Nat → FullOp     -- addrReg, valReg
  | loadMem : Nat → Nat → FullOp      -- dstReg, addrReg
  | allocFresh : Nat → FullOp         -- dstReg
  deriving DecidableEq, Repr

structure FullState where
  pc : Nat
  regs : Nat → Nat
  memory : Nat → Nat
  allocCount : Nat
  outputTape : List Nat
  halted : Bool
  steps : Nat

def initFullState (inputs : List Nat) : FullState :=
  { pc := 0,
    regs := fun idx => inputs.getD idx 0,
    memory := fun _ => 0,
    allocCount := 0,
    outputTape := [],
    halted := false,
    steps := 0 }

def fetchFull : Nat → List FullOp → Option FullOp
  | 0, [] => none
  | 0, op :: _ => some op
  | _ + 1, [] => none
  | n + 1, _ :: rest => fetchFull n rest

def stepFullOp : FullOp → FullState → FullState
  | FullOp.nop, st =>
    { st with pc := st.pc + 1, steps := st.steps + 1 }
  | FullOp.setConst dst val, st =>
    { st with pc := st.pc + 1,
              regs := fun r => if r == dst then val else st.regs r,
              steps := st.steps + 1 }
  | FullOp.add dst s1 s2, st =>
    { st with pc := st.pc + 1,
              regs := fun r => if r == dst then st.regs s1 + st.regs s2 else st.regs r,
              steps := st.steps + 1 }
  | FullOp.inc reg, st =>
    { st with pc := st.pc + 1,
              regs := fun r => if r == reg then st.regs reg + 1 else st.regs r,
              steps := st.steps + 1 }
  | FullOp.emit src, st =>
    { st with pc := st.pc + 1,
              outputTape := st.outputTape ++ [st.regs src],
              steps := st.steps + 1 }
  | FullOp.halt, st =>
    { st with halted := true, steps := st.steps + 1 }
  | FullOp.jumpIfZero cond target, st =>
    let st' := { st with steps := st.steps + 1 }
    if st.regs cond == 0 then { st' with pc := target }
    else { st' with pc := st.pc + 1 }
  | FullOp.storeMem addrReg valReg, st =>
    let a := st.regs addrReg
    let v := st.regs valReg
    { st with pc := st.pc + 1,
              memory := fun m => if m == a then v else st.memory m,
              steps := st.steps + 1 }
  | FullOp.loadMem dstReg addrReg, st =>
    let a := st.regs addrReg
    let v := st.memory a
    { st with pc := st.pc + 1,
              regs := fun r => if r == dstReg then v else st.regs r,
              steps := st.steps + 1 }
  | FullOp.allocFresh dstReg, st =>
    let fresh := st.allocCount + 1
    { st with pc := st.pc + 1,
              allocCount := fresh,
              regs := fun r => if r == dstReg then fresh else st.regs r,
              steps := st.steps + 1 }

def stepFullFetched : Option FullOp → FullState → FullState
  | none, st => { st with halted := true }
  | some op, st => stepFullOp op st

def stepFull (prog : List FullOp) (st : FullState) : FullState :=
  if st.halted then st
  else stepFullFetched (fetchFull st.pc prog) st

def runFull (prog : List FullOp) (fuel : Nat) (st : FullState) : FullState :=
  match fuel with
  | 0 => st
  | fuel' + 1 =>
    if st.halted then st
    else runFull prog fuel' (stepFull prog st)

def observeFull (st : FullState) : PublicObservation :=
  { outputTape := st.outputTape, steps := st.steps, halted := st.halted }

def embedLinearOp : LinearOp → FullOp
  | .nop => .nop
  | .setConst d v => .setConst d v
  | .add d s1 s2 => .add d s1 s2
  | .inc r => .inc r
  | .emit s => .emit s
  | .halt => .halt

def embedLinearProg (p : List LinearOp) : List FullOp :=
  p.map embedLinearOp

def embedLinearState (st : LinearState) : FullState :=
  { pc := st.pc,
    regs := st.regs,
    memory := fun _ => 0,
    allocCount := 0,
    outputTape := st.outputTape,
    halted := st.halted,
    steps := st.steps }

theorem project_embedLinearState (st : LinearState) :
    observeFull (embedLinearState st) = observeLinear st := by
  rfl

theorem fetch_embed (pc : Nat) (prog : List LinearOp) :
    fetchFull pc (embedLinearProg prog) = (fetchLinear pc prog).map embedLinearOp := by
  induction pc generalizing prog with
  | zero =>
    cases prog with
    | nil => rfl
    | cons op rest => rfl
  | succ n ih =>
    cases prog with
    | nil => rfl
    | cons op rest =>
      dsimp [fetchFull, fetchLinear, embedLinearProg]
      exact ih rest

theorem linear_step_embed_op (op : LinearOp) (st : LinearState) :
    stepFullOp (embedLinearOp op) (embedLinearState st) = embedLinearState (stepLinearOp op st) := by
  cases op <;> rfl

theorem linear_step_embed_fetched (fo : Option LinearOp) (st : LinearState) :
    stepFullFetched (fo.map embedLinearOp) (embedLinearState st) = embedLinearState (stepLinearFetched fo st) := by
  cases fo with
  | none => rfl
  | some op => exact linear_step_embed_op op st

theorem linear_step_embed (prog : List LinearOp) (st : LinearState) :
    stepFull (embedLinearProg prog) (embedLinearState st) = embedLinearState (stepLinear prog st) := by
  dsimp [stepFull, stepLinear]
  have h_h : (embedLinearState st).halted = st.halted := rfl
  have h_pc : (embedLinearState st).pc = st.pc := rfl
  rw [h_h, h_pc]
  by_cases h_halt : st.halted
  · simp [h_halt]
  · simp [h_halt]
    rw [fetch_embed]
    exact linear_step_embed_fetched (fetchLinear st.pc prog) st

theorem linear_embed_step_observe (prog : List LinearOp) (st : LinearState) :
    observeFull (stepFull (embedLinearProg prog) (embedLinearState st)) = observeLinear (stepLinear prog st) := by
  rw [linear_step_embed]
  rfl

end G010
