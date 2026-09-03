import Std

namespace DescribedReplay

inductive Datum where
  | a
  | b
deriving DecidableEq, Repr

inductive Event where
  | supplyA
  | supplyB
  | addA
  | addB
  | addUnary
  | addInst0
  | addInst1
  | addRule0
  | impose01
deriving DecidableEq, Repr

structure Regime where
  data : List Datum
  unaryForms : Nat
  instance0 : Bool
  instance1 : Bool
  rule0 : Bool
  imposed01 : Bool
deriving DecidableEq, Repr

def emptyRegime : Regime :=
  { data := [], unaryForms := 0, instance0 := false, instance1 := false,
    rule0 := false, imposed01 := false }

def appendFresh (data : List Datum) (token : Datum) : List Datum :=
  if token ∈ data then data else data ++ [token]

def eventValid (regime : Regime) : Event → Bool
  | .supplyA => true
  | .supplyB => true
  | .addA => true
  | .addB => true
  | .addUnary => true
  | .addInst0 => decide (0 < regime.unaryForms ∧ 0 < regime.data.length)
  | .addInst1 => decide (0 < regime.unaryForms ∧ 1 < regime.data.length)
  | .addRule0 => decide (0 < regime.unaryForms)
  | .impose01 => decide (1 < regime.data.length)

def applyEvent (regime : Regime) : Event → Regime
  | .supplyA => regime
  | .supplyB => regime
  | .addA => { regime with data := appendFresh regime.data .a }
  | .addB => { regime with data := appendFresh regime.data .b }
  | .addUnary => { regime with unaryForms := regime.unaryForms + 1 }
  | .addInst0 => { regime with instance0 := true }
  | .addInst1 => { regime with instance1 := true }
  | .addRule0 => { regime with rule0 := true }
  | .impose01 => { regime with imposed01 := true }

def transition (regime : Regime) (event : Event) : Option Regime :=
  if eventValid regime event then some (applyEvent regime event) else none

theorem supply_inertia (regime : Regime) :
    transition regime .supplyA = some regime ∧
      transition regime .supplyB = some regime := by
  exact ⟨rfl, rfl⟩

def replayFrom : List Event → Regime → Option Regime
  | [], regime => some regime
  | event :: rest, regime =>
      match transition regime event with
      | none => none
      | some next => replayFrom rest next

def replay (history : List Event) : Option Regime :=
  replayFrom history emptyRegime

def replayTotalFrom : List Event → Regime → Regime
  | [], regime => regime
  | event :: rest, regime => replayTotalFrom rest (applyEvent regime event)

def replayTotal (history : List Event) : Regime :=
  replayTotalFrom history emptyRegime

def wellFormedFrom : List Event → Regime → Bool
  | [], _ => true
  | event :: rest, regime =>
      eventValid regime event && wellFormedFrom rest (applyEvent regime event)

def wellFormed (history : List Event) : Bool :=
  wellFormedFrom history emptyRegime

def member (history : List Event) : Bool :=
  decide (history.length ≤ 3) && wellFormed history

theorem replayFrom_eq_replayTotalFrom (history : List Event) (regime : Regime)
    (hwell : wellFormedFrom history regime = true) :
    replayFrom history regime = some (replayTotalFrom history regime) := by
  induction history generalizing regime with
  | nil => rfl
  | cons event rest ih =>
      have hparts : eventValid regime event = true ∧
          wellFormedFrom rest (applyEvent regime event) = true := by
        simpa [wellFormedFrom] using hwell
      simp [replayFrom, replayTotalFrom, transition, hparts.1,
        ih (applyEvent regime event) hparts.2]

theorem replay_eq_replayTotal_of_member (history : List Event)
    (hmember : member history = true) :
    replay history = some (replayTotal history) := by
  have hparts := hmember
  simp [member] at hparts
  exact replayFrom_eq_replayTotalFrom history emptyRegime hparts.2

end DescribedReplay
