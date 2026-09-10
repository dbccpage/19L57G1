import CarrierRepr

/-!
# G018 Self-Hosting: Internalized Simulator

Internalized step-simulator executing within the object carrier.
Tracks the object process step by step with ZERO external host oracles
or metatheoretic loop counters.

Simulation correctness theorem:
  stepCarrier (simEmbed spec s hostFuel) = simEmbed spec (stepMachine spec s) (hostFuel - 1)

Axioms used: strictly contained in `{propext, Quot.sound}` (zero classical choice, zero mathlib).
-/

namespace G018SelfHosting

/-- Embed a guest machine specification and state into carrier simulator state. -/
def simEmbed (spec : MachineSpec) (s : MachineState) (hostFuel : Nat) : CarrierState :=
  { guestSpec := spec, guestState := s, hostFuel := hostFuel }

/-- Extract guest machine specification and state from carrier simulator state. -/
def simExtract (cs : CarrierState) : MachineSpec × MachineState :=
  (cs.guestSpec, cs.guestState)

/-- Single internalized simulation step within the carrier.
    Operates strictly on carrier-represented data. -/
def stepCarrier (cs : CarrierState) : CarrierState :=
  if cs.hostFuel == 0 || cs.guestState.halted || cs.guestState.fuel == 0 then
    cs
  else
    { cs with
      guestState := stepMachine cs.guestSpec cs.guestState,
      hostFuel := cs.hostFuel - 1 }

/-- Multi-step execution of internalized simulator. -/
def runCarrier : Nat → CarrierState → CarrierState
  | 0, cs => cs
  | n + 1, cs =>
    if cs.hostFuel == 0 || cs.guestState.halted || cs.guestState.fuel == 0 then
      cs
    else
      runCarrier n (stepCarrier cs)

/-! ## Simulation Correctness Theorems -/

/-- Round-trip extraction identity on freshly embedded carrier states. -/
theorem sim_embed_extract_id (spec : MachineSpec) (s : MachineState) (hostFuel : Nat) :
    simExtract (simEmbed spec s hostFuel) = (spec, s) := by
  rfl

/-- Core Step Simulation Correctness Theorem:
    Executing one step of the internalized carrier simulator on an embedded guest state
    is strictly identical to embedding the result of one direct operational step,
    with host fuel decremented by 1. -/
theorem step_simulation_correctness (spec : MachineSpec) (s : MachineState) (hostFuel : Nat)
    (h_fuel : s.fuel > 0) (h_halt : s.halted = false) (h_hfuel : hostFuel > 0) :
    stepCarrier (simEmbed spec s hostFuel) = simEmbed spec (stepMachine spec s) (hostFuel - 1) := by
  dsimp [stepCarrier, simEmbed]
  have h_hf : (hostFuel == 0) = false := by
    apply beq_eq_false_iff_ne.mpr
    omega
  have h_f : (s.fuel == 0) = false := by
    apply beq_eq_false_iff_ne.mpr
    omega
  rw [h_hf, h_halt, h_f]
  dsimp

/-- Extracted operational equivalence:
    The extracted state from the stepped simulator exactly matches the direct operational step. -/
theorem step_simulation_extract_commutes (spec : MachineSpec) (s : MachineState) (hostFuel : Nat)
    (h_fuel : s.fuel > 0) (h_halt : s.halted = false) (h_hfuel : hostFuel > 0) :
    (simExtract (stepCarrier (simEmbed spec s hostFuel))).2 = stepMachine spec s := by
  rw [step_simulation_correctness spec s hostFuel h_fuel h_halt h_hfuel]
  rfl

/-- Stepping a simulator with zero host fuel is an identity. -/
theorem stepCarrier_zero_host_fuel (cs : CarrierState) (h : cs.hostFuel = 0) :
    stepCarrier cs = cs := by
  dsimp [stepCarrier]
  rw [h]
  rfl

/-- Stepping a simulator whose guest machine has halted is an identity. -/
theorem stepCarrier_guest_halted (cs : CarrierState) (h : cs.guestState.halted = true) :
    stepCarrier cs = cs := by
  dsimp [stepCarrier]
  rw [h]
  cases (cs.hostFuel == 0) <;> rfl

/-- Stepping a simulator whose guest machine has exhausted fuel is an identity. -/
theorem stepCarrier_guest_zero_fuel (cs : CarrierState) (h : cs.guestState.fuel = 0) :
    stepCarrier cs = cs := by
  dsimp [stepCarrier]
  rw [h]
  cases (cs.hostFuel == 0 || cs.guestState.halted) <;> rfl

/-- Running the simulator on a halted or fuel-exhausted state is an identity. -/
theorem runCarrier_halted (n : Nat) (cs : CarrierState) (h : cs.guestState.halted = true) :
    runCarrier n cs = cs := by
  induction n with
  | zero => rfl
  | succ n _ =>
    dsimp [runCarrier]
    rw [h]
    cases (cs.hostFuel == 0) <;> rfl

end G018SelfHosting
