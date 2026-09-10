import Ordinal
import Address
import Freshness

/-!
# Fuel-Bounded Endogenous Structural Recursion

Endogenous instruction evaluation, register/memory state transitions,
fuel-bounded execution, and constructive totality without host loop counters.

AuthorityEffect: None.
Axiom boundary: strictly within {propext, Quot.sound}, zero Classical.choice, zero mathlib.
-/

namespace FinitarySubstrate

namespace Recursion

open Address Freshness

/-! ## 1. Values and Instructions -/

/-- Endogenous register/memory values: either an Ordinal scalar or a Tree Address. -/
inductive Val where
  | num : Ordinal → Val
  | addr : Address → Val
  deriving DecidableEq, Repr

/-- Endogenous machine instruction set. -/
inductive Instr where
  | nop : Instr
  | setZero (reg : Ordinal) : Instr
  | succReg (reg : Ordinal) : Instr
  | predReg (reg : Ordinal) : Instr
  | copyReg (dst src : Ordinal) : Instr
  | allocAddr (dst : Ordinal) : Instr
  | writeMem (addrReg valReg : Ordinal) : Instr
  | readMem (dst addrReg : Ordinal) : Instr
  | jump (target : Ordinal) : Instr
  | branchIfZero (reg : Ordinal) (target : Ordinal) : Instr
  | halt : Instr
  deriving DecidableEq, Repr

abbrev Program := List Instr

/-- Fetch instruction from program at ordinal program counter. -/
def fetch : Ordinal → Program → Option Instr
  | .zero, [] => none
  | .zero, i :: _ => some i
  | .succ _, [] => none
  | .succ n, _ :: rest => fetch n rest

/-! ## 2. Association Storage -/

/-- Association list lookup for registers. -/
def getReg : List (Ordinal × Val) → Ordinal → Val
  | [], _ => .num .zero
  | (k, v) :: rest, r =>
      if k == r then v else getReg rest r

/-- Association list update for registers. -/
def setReg (regs : List (Ordinal × Val)) (r : Ordinal) (v : Val) : List (Ordinal × Val) :=
  (r, v) :: regs

/-- Association list lookup for address memory. -/
def getMem : List (Address × Val) → Address → Val
  | [], _ => .num .zero
  | (k, v) :: rest, a =>
      if k == a then v else getMem rest a

/-- Association list update for address memory. -/
def setMem (mem : List (Address × Val)) (a : Address) (v : Val) : List (Address × Val) :=
  (a, v) :: mem

/-! ## 3. Machine State and Single Step -/

/-- Machine State: pure finitary representation. -/
structure State where
  pc : Ordinal
  regs : List (Ordinal × Val)
  mem : List (Address × Val)
  addrs : List Address
  halted : Bool
  deriving DecidableEq, Repr

def initState : State :=
  ⟨.zero, [], [], [], false⟩

/-- Single-step operational transition function. -/
def step (prog : Program) (s : State) : State :=
  if s.halted then s
  else
    match fetch s.pc prog with
    | none => { s with halted := true }
    | some .nop =>
        { s with pc := .succ s.pc }
    | some (.setZero r) =>
        { s with regs := setReg s.regs r (.num .zero), pc := .succ s.pc }
    | some (.succReg r) =>
        let v := match getReg s.regs r with
                 | .num o => Val.num (.succ o)
                 | .addr a => Val.addr a
        { s with regs := setReg s.regs r v, pc := .succ s.pc }
    | some (.predReg r) =>
        let v := match getReg s.regs r with
                 | .num o => Val.num (Ordinal.pred o)
                 | .addr a => Val.addr a
        { s with regs := setReg s.regs r v, pc := .succ s.pc }
    | some (.copyReg dst src) =>
        let v := getReg s.regs src
        { s with regs := setReg s.regs dst v, pc := .succ s.pc }
    | some (.allocAddr dst) =>
        let fresh := freshAddress s.addrs
        { s with regs := setReg s.regs dst (.addr fresh),
                 addrs := fresh :: s.addrs,
                 mem := setMem s.mem fresh (.num .zero),
                 pc := .succ s.pc }
    | some (.writeMem addrReg valReg) =>
        match getReg s.regs addrReg with
        | .addr a =>
            let v := getReg s.regs valReg
            { s with mem := setMem s.mem a v, pc := .succ s.pc }
        | .num _ =>
            { s with halted := true }
    | some (.readMem dst addrReg) =>
        match getReg s.regs addrReg with
        | .addr a =>
            let v := getMem s.mem a
            { s with regs := setReg s.regs dst v, pc := .succ s.pc }
        | .num _ =>
            { s with halted := true }
    | some (.jump target) =>
        { s with pc := target }
    | some (.branchIfZero r target) =>
        match getReg s.regs r with
        | .num .zero => { s with pc := target }
        | _ => { s with pc := .succ s.pc }
    | some .halt =>
        { s with halted := true }

/-! ## 4. Fuel-Bounded Execution and Totality -/

inductive ExecResult where
  | halted (s : State)
  | outOfFuel (s : State)
  deriving DecidableEq, Repr

/-- Pure structural fuel-bounded recursion. -/
def runWithFuel : Ordinal → Program → State → ExecResult
  | .zero, _, s => .outOfFuel s
  | .succ fuel', prog, s =>
      if s.halted then .halted s
      else runWithFuel fuel' prog (step prog s)

/-- General endogenous structural recursion scheme on Ordinals. -/
def recFuel {α : Type} : Ordinal → α → (Ordinal → α → α) → α
  | .zero, base, _ => base
  | .succ o, base, f => f o (recFuel o base f)

theorem step_halted (prog : Program) (s : State) (h : s.halted = true) :
    step prog s = s := by
  dsimp [step]
  rw [h]
  rfl

theorem runWithFuel_zero (prog : Program) (s : State) :
    runWithFuel .zero prog s = .outOfFuel s := rfl

theorem runWithFuel_halted (fuel : Ordinal) (prog : Program) (s : State) (h : s.halted = true) :
    runWithFuel (.succ fuel) prog s = .halted s := by
  dsimp [runWithFuel]
  rw [h]
  rfl

theorem step_deterministic (prog : Program) (s1 s2 : State) (h : s1 = s2) :
    step prog s1 = step prog s2 := by
  rw [h]

theorem runWithFuel_deterministic (fuel : Ordinal) (prog : Program) (s1 s2 : State) (h : s1 = s2) :
    runWithFuel fuel prog s1 = runWithFuel fuel prog s2 := by
  rw [h]

theorem recFuel_zero {α : Type} (base : α) (f : Ordinal → α → α) :
    recFuel .zero base f = base := rfl

theorem recFuel_succ {α : Type} (o : Ordinal) (base : α) (f : Ordinal → α → α) :
    recFuel (.succ o) base f = f o (recFuel o base f) := rfl

theorem runWithFuel_totality (fuel : Ordinal) (prog : Program) (s : State) :
    (∃ s', runWithFuel fuel prog s = .halted s') ∨ (∃ s', runWithFuel fuel prog s = .outOfFuel s') := by
  induction fuel generalizing s with
  | zero =>
      right
      exact ⟨s, rfl⟩
  | succ f ih =>
      dsimp [runWithFuel]
      by_cases hh : s.halted = true
      · rw [if_pos hh]
        left
        exact ⟨s, rfl⟩
      · rw [if_neg hh]
        exact ih (step prog s)

end Recursion

end FinitarySubstrate
