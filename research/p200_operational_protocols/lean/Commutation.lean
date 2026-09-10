import Protocol

/-!
# Readout-to-Step Commutation

Establishes:
1. `readout_step_commutation`:
   On non-disturbing sectors (disjoint carrier footprints), embedded observer
   readout commutes with autonomous carrier step transitions:
       Readout ∘ Step = Step ∘ Readout
2. Commutation with mediating channel transitions:
   Readouts commute with step transitions at coupling locus M.
3. Disturbance detection:
   When an instrument perturbs the target locus (overlapping footprint),
   operational commutation fails in general on unpriced coordinates.

AuthorityEffect: None.
Axiom Scope: Strictly constructive; `#print axioms` in `{propext, Quot.sound}`.
-/

namespace P200OperationalProtocols

/-- Commutation predicate between two state operations. -/
def Commutes (opA opB : CarrierState → CarrierState) : Prop :=
  ∀ s, opA (opB s) = opB (opA s)

/-- Autonomous process step transition at Locus 1. -/
def stepL1 (f : Nat → Nat) (s : CarrierState) : CarrierState :=
  { s with l1 := f s.l1 }

/-- Autonomous process step transition at Locus 2. -/
def stepL2 (g : Nat → Nat) (s : CarrierState) : CarrierState :=
  { s with l2 := g s.l2 }

/-- Autonomous process step transition at coupling locus M. -/
def stepM (h : Nat → Nat) (s : CarrierState) : CarrierState :=
  { s with m := h s.m }

/-- **Readout-to-Step Commutation Theorem.**
    Non-disturbing readout of Locus 2 into R2 commutes with autonomous process
    steps at Locus 1 on all carrier states. -/
theorem readout_step_commutation (probe : Nat → Nat) (f : Nat → Nat) :
    Commutes (readout2 probe) (stepL1 f) := by
  intro s
  rfl

/-- Non-disturbing readout of Locus 1 into R1 commutes with autonomous process
    steps at Locus 2. -/
theorem readout1_stepL2_commutation (probe : Nat → Nat) (g : Nat → Nat) :
    Commutes (readout1 probe) (stepL2 g) := by
  intro s
  rfl

/-- Non-disturbing readout of Locus 2 commutes with coupling channel steps at M. -/
theorem readout2_stepM_commutation (probe : Nat → Nat) (h : Nat → Nat) :
    Commutes (readout2 probe) (stepM h) := by
  intro s
  rfl

/-- Non-disturbing readout of Locus 1 commutes with coupling channel steps at M. -/
theorem readout1_stepM_commutation (probe : Nat → Nat) (h : Nat → Nat) :
    Commutes (readout1 probe) (stepM h) := by
  intro s
  rfl

/-- Operational replay of an arbitrary finite list of autonomous process steps at Locus 1. -/
def replayL1 : List (Nat → Nat) → CarrierState → CarrierState
  | [], s => s
  | f :: fs, s => replayL1 fs (stepL1 f s)

/-- **Protocol-to-Replay Commutation Theorem.**
    Non-disturbing readout of Locus 2 into R2 commutes with any sequential
    replay of autonomous process steps at Locus 1. -/
theorem readout_replayL1_commutation (probe : Nat → Nat) (fs : List (Nat → Nat)) (s : CarrierState) :
    readout2 probe (replayL1 fs s) = replayL1 fs (readout2 probe s) := by
  induction fs generalizing s with
  | nil => rfl
  | cons f fs ih =>
    dsimp [replayL1]
    have h_comm : readout2 probe (stepL1 f s) = stepL1 f (readout2 probe s) := rfl
    rw [← h_comm]
    exact ih (stepL1 f s)

/-- Concrete step modifying Locus 1 by incrementing coordinate. -/
def concreteStepL1 (s : CarrierState) : CarrierState :=
  { s with l1 := s.l1 + 10 }

/-- Disturbing readout at Locus 1 setting L1 to zero with unit disturbance price. -/
def concreteDisturbReadout1 (s : CarrierState) : CarrierState :=
  { s with l1 := 0, r1 := s.l1, dist := s.dist + 1 }

/-- **Disturbance Detection Theorem.**
    When an embedded instrument modifies the target locus, operational
    commutation with steps on that locus fails. -/
theorem disturbing_readout_fails_commute :
    ¬ Commutes concreteDisturbReadout1 concreteStepL1 := by
  intro hcomm
  have h_eq := hcomm { l1 := 5, l2 := 0, m := 0, r1 := 0, r2 := 0, dist := 0 }
  have h_diff : (concreteDisturbReadout1 (concreteStepL1 { l1 := 5, l2 := 0, m := 0, r1 := 0, r2 := 0, dist := 0 })).r1 ≠
                (concreteStepL1 (concreteDisturbReadout1 { l1 := 5, l2 := 0, m := 0, r1 := 0, r2 := 0, dist := 0 })).r1 := by
    decide
  apply h_diff
  rw [h_eq]

end P200OperationalProtocols
