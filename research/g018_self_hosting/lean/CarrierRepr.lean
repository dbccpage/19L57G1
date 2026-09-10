/-!
# G018 Self-Hosting: Carrier Representation

Representation of the execution engine's own transition function,
state graph, and machine configurations within the object carrier.

Axioms used: strictly contained in `{propext, Quot.sound}` (zero classical choice, zero mathlib).
-/

namespace G018SelfHosting

/-- A single deterministic transition edge. -/
structure Transition where
  currState : Nat
  readSym : Nat
  nextState : Nat
  writeSym : Nat
  moveCursor : Int
  halt : Bool
deriving Repr, DecidableEq

/-- Deterministic transition machine specification. -/
structure MachineSpec where
  transitions : List Transition
  defaultSym : Nat
deriving Repr, DecidableEq

/-- Operational configuration of a machine inside the carrier. -/
structure MachineState where
  state : Nat
  cursor : Nat
  tape : List Nat
  fuel : Nat
  halted : Bool
deriving Repr, DecidableEq

/-- Look up a transition rule in the transition table. -/
def lookupTransition : List Transition → Nat → Nat → Option Transition
  | [], _, _ => none
  | t :: rest, st, sym =>
    if t.currState == st && t.readSym == sym then
      some t
    else
      lookupTransition rest st sym

/-- Structural tape read function. -/
def readTape : List Nat → Nat → Nat → Nat
  | [], _, defaultSym => defaultSym
  | x :: _, 0, _ => x
  | _ :: xs, n + 1, defaultSym => readTape xs n defaultSym

/-- Structural tape write function. -/
def writeTape : List Nat → Nat → Nat → List Nat
  | [], 0, sym => [sym]
  | _ :: xs, 0, sym => sym :: xs
  | [], n + 1, sym => 0 :: writeTape [] n sym
  | x :: xs, n + 1, sym => x :: writeTape xs n sym

/-- Cursor motion clamped to non-negative coordinates. -/
def moveCursorPos (cursor : Nat) (offset : Int) : Nat :=
  if offset < 0 then
    cursor - offset.natAbs
  else
    cursor + offset.toNat

/-- Operational machine single-step transition. -/
def stepMachine (spec : MachineSpec) (s : MachineState) : MachineState :=
  if s.halted || s.fuel == 0 then
    s
  else
    let sym := readTape s.tape s.cursor spec.defaultSym
    match lookupTransition spec.transitions s.state sym with
    | none =>
      { s with halted := true, fuel := s.fuel - 1 }
    | some t =>
      { state := t.nextState,
        cursor := moveCursorPos s.cursor t.moveCursor,
        tape := writeTape s.tape s.cursor t.writeSym,
        fuel := s.fuel - 1,
        halted := t.halt }

/-- Multi-step operational execution. -/
def runMachine (spec : MachineSpec) : Nat → MachineState → MachineState
  | 0, s => s
  | n + 1, s =>
    if s.halted || s.fuel == 0 then
      s
    else
      runMachine spec n (stepMachine spec s)

/-- Carrier configuration holding an embedded guest machine. -/
structure CarrierState where
  guestSpec : MachineSpec
  guestState : MachineState
  hostFuel : Nat
deriving Repr, DecidableEq

/-! ## Carrier Representation Theorems -/

/-- Stepping a halted machine preserves the state identically. -/
theorem stepMachine_halted (spec : MachineSpec) (s : MachineState) (h : s.halted = true) :
    stepMachine spec s = s := by
  dsimp [stepMachine]
  rw [h]
  simp

/-- Stepping a machine with zero fuel preserves the state identically. -/
theorem stepMachine_zero_fuel (spec : MachineSpec) (s : MachineState) (h : s.fuel = 0) :
    stepMachine spec s = s := by
  dsimp [stepMachine]
  rw [h]
  have hz : (0 == 0) = true := rfl
  rw [hz, Bool.or_true]
  rfl

/-- Running a halted machine for any number of steps is an identity. -/
theorem runMachine_halted (spec : MachineSpec) (n : Nat) (s : MachineState) (h : s.halted = true) :
    runMachine spec n s = s := by
  induction n with
  | zero => rfl
  | succ n _ =>
    dsimp [runMachine]
    rw [h]
    rfl

/-- Running a machine with zero fuel for any number of steps is an identity. -/
theorem runMachine_zero_fuel (spec : MachineSpec) (n : Nat) (s : MachineState) (h : s.fuel = 0) :
    runMachine spec n s = s := by
  induction n with
  | zero => rfl
  | succ n _ =>
    dsimp [runMachine]
    rw [h]
    have hz : (0 == 0) = true := rfl
    rw [hz, Bool.or_true]
    rfl

/-- Fuel consumption theorem: each active step decrements fuel by exactly 1. -/
theorem stepMachine_fuel_decrement (spec : MachineSpec) (s : MachineState)
    (h_fuel : s.fuel > 0) (h_halt : s.halted = false) :
    (stepMachine spec s).fuel = s.fuel - 1 := by
  dsimp [stepMachine]
  rw [h_halt]
  have hf : (s.fuel == 0) = false := by
    apply beq_eq_false_iff_ne.mpr
    omega
  rw [hf]
  dsimp
  split
  · rfl
  · rfl

end G018SelfHosting
