import Capability
import Restriction

namespace G010

/-!
# G010 Constructive Obstruction Theorems

Shows in this model that computational tasks requiring removed primitives (branching, memory retention,
address allocation) cannot be solved in restricted systems across the shared PublicObservation
interface, and cannot be recovered via capability-preserving adapters.

AuthorityEffect: None.
-/

/-! ## 1. Branching Obstruction -/

theorem stepLinearOp_control (op : LinearOp) (st1 st2 : LinearState)
    (h_pc : st1.pc = st2.pc) (h_halt : st1.halted = st2.halted)
    (h_len : st1.outputTape.length = st2.outputTape.length) :
    (stepLinearOp op st1).pc = (stepLinearOp op st2).pc ∧
    (stepLinearOp op st1).halted = (stepLinearOp op st2).halted ∧
    (stepLinearOp op st1).outputTape.length = (stepLinearOp op st2).outputTape.length := by
  cases op with
  | nop =>
    dsimp [stepLinearOp]
    simp [h_pc, h_halt, h_len]
  | setConst d v =>
    dsimp [stepLinearOp]
    simp [h_pc, h_halt, h_len]
  | add d s1 s2 =>
    dsimp [stepLinearOp]
    simp [h_pc, h_halt, h_len]
  | inc r =>
    dsimp [stepLinearOp]
    simp [h_pc, h_halt, h_len]
  | emit s =>
    dsimp [stepLinearOp]
    simp [h_pc, h_halt, h_len]
  | halt =>
    dsimp [stepLinearOp]
    simp [h_pc, h_len]

theorem stepLinearFetched_control (fo : Option LinearOp) (st1 st2 : LinearState)
    (h_pc : st1.pc = st2.pc) (h_halt : st1.halted = st2.halted)
    (h_len : st1.outputTape.length = st2.outputTape.length) :
    (stepLinearFetched fo st1).pc = (stepLinearFetched fo st2).pc ∧
    (stepLinearFetched fo st1).halted = (stepLinearFetched fo st2).halted ∧
    (stepLinearFetched fo st1).outputTape.length = (stepLinearFetched fo st2).outputTape.length := by
  cases fo with
  | none =>
    dsimp [stepLinearFetched]
    simp [h_pc, h_len]
  | some op =>
    exact stepLinearOp_control op st1 st2 h_pc h_halt h_len

theorem linear_step_control (prog : List LinearOp) (st1 st2 : LinearState)
    (h_pc : st1.pc = st2.pc) (h_halt : st1.halted = st2.halted)
    (h_len : st1.outputTape.length = st2.outputTape.length) :
    (stepLinear prog st1).pc = (stepLinear prog st2).pc ∧
    (stepLinear prog st1).halted = (stepLinear prog st2).halted ∧
    (stepLinear prog st1).outputTape.length = (stepLinear prog st2).outputTape.length := by
  dsimp [stepLinear]
  cases h1 : st1.halted
  · have h2 : st2.halted = false := by rw [← h_halt, h1]
    simp [h1, h2]
    rw [h_pc]
    exact stepLinearFetched_control (fetchLinear st2.pc prog) st1 st2 h_pc h_halt h_len
  · have h2 : st2.halted = true := by rw [← h_halt, h1]
    simp [h1, h2, h_pc, h_len]

theorem linear_run_control (prog : List LinearOp) (fuel : Nat) (st1 st2 : LinearState)
    (h_pc : st1.pc = st2.pc) (h_halt : st1.halted = st2.halted)
    (h_len : st1.outputTape.length = st2.outputTape.length) :
    (runLinear prog fuel st1).outputTape.length = (runLinear prog fuel st2).outputTape.length := by
  induction fuel generalizing st1 st2 with
  | zero =>
    dsimp [runLinear]
    exact h_len
  | succ fuel' ih =>
    dsimp [runLinear]
    rw [h_halt]
    by_cases h_st_halt : st2.halted
    · simp [h_st_halt, h_len]
    · simp [h_st_halt]
      have ⟨next_pc, next_halt, next_len⟩ := linear_step_control prog st1 st2 h_pc h_halt h_len
      exact ih (stepLinear prog st1) (stepLinear prog st2) next_pc next_halt next_len

theorem linear_inputs_tape_len_eq (prog : List LinearOp) (fuel : Nat) (x y : Nat) :
    (runLinear prog fuel (initLinearState [x])).outputTape.length =
    (runLinear prog fuel (initLinearState [y])).outputTape.length := by
  apply linear_run_control prog fuel
  · rfl
  · rfl
  · rfl

/-- Constructive Branching Obstruction Theorem:
A straight-line linear program cannot emit different output lengths on different inputs. -/
theorem branching_obstruction (prog : List LinearOp) (fuel : Nat) :
    ¬ ((runLinear prog fuel (initLinearState [0])).outputTape.length = 1 ∧
       (runLinear prog fuel (initLinearState [1])).outputTape.length = 2) := by
  intro ⟨h1, h2⟩
  have h_eq := linear_inputs_tape_len_eq prog fuel 0 1
  rw [h1, h2] at h_eq
  contradiction

/-! ## 2. Memory Retention Obstruction -/

def clobberState (st : LinearState) : LinearState :=
  { st with regs := fun _ => 0 }

theorem clobber_eq (x y : Nat) :
    clobberState (initLinearState [x]) = clobberState (initLinearState [y]) := by
  rfl

theorem memoryless_clobber_erasure (prog : List LinearOp) (fuel : Nat) (x y : Nat) :
    runLinear prog fuel (clobberState (initLinearState [x])) =
    runLinear prog fuel (clobberState (initLinearState [y])) := by
  rw [clobber_eq x y]

/-- Constructive Memory Obstruction Theorem:
In the absence of memory retention, clobbering registers permanently erases input distinction. -/
theorem memory_retention_obstruction (prog : List LinearOp) (fuel : Nat) (x y : Nat) (h_diff : x ≠ y) :
    ¬ ((runLinear prog fuel (clobberState (initLinearState [x]))).regs 0 = x ∧
       (runLinear prog fuel (clobberState (initLinearState [y]))).regs 0 = y) := by
  intro ⟨hx, hy⟩
  have h_eq : runLinear prog fuel (clobberState (initLinearState [x])) =
              runLinear prog fuel (clobberState (initLinearState [y])) :=
    memoryless_clobber_erasure prog fuel x y
  have h_val : (runLinear prog fuel (clobberState (initLinearState [x]))).regs 0 =
               (runLinear prog fuel (clobberState (initLinearState [y]))).regs 0 := by
    rw [h_eq]
  rw [hx, hy] at h_val
  exact h_diff h_val

/-! ## 3. Address Allocation Obstruction (Pigeonhole Collision) -/

theorem fin2_eq (a : Fin 2) : a = 0 ∨ a = 1 := by
  match a with
  | ⟨0, _⟩ => exact Or.inl rfl
  | ⟨1, _⟩ => exact Or.inr rfl
  | ⟨n+2, h⟩ => contradiction

/-- Constructive Allocation Obstruction Theorem:
By finite slot pigeonhole collision, allocating 3 entities into 2 static slots forces a collision. -/
theorem static_pigeonhole_collision (f : Fin 3 → Fin 2) : ¬ Function.Injective f := by
  intro h_inj
  rcases fin2_eq (f 0) with h0 | h0 <;>
  rcases fin2_eq (f 1) with h1 | h1 <;>
  rcases fin2_eq (f 2) with h2 | h2
  · have : f 0 = f 1 := by rw [h0, h1]
    have : (0 : Fin 3) = 1 := h_inj this
    contradiction
  · have : f 0 = f 1 := by rw [h0, h1]
    have : (0 : Fin 3) = 1 := h_inj this
    contradiction
  · have : f 0 = f 2 := by rw [h0, h2]
    have : (0 : Fin 3) = 2 := h_inj this
    contradiction
  · have : f 1 = f 2 := by rw [h1, h2]
    have : (1 : Fin 3) = 2 := h_inj this
    contradiction
  · have : f 1 = f 2 := by rw [h1, h2]
    have : (1 : Fin 3) = 2 := h_inj this
    contradiction
  · have : f 0 = f 2 := by rw [h0, h2]
    have : (0 : Fin 3) = 2 := h_inj this
    contradiction
  · have : f 0 = f 1 := by rw [h0, h1]
    have : (0 : Fin 3) = 1 := h_inj this
    contradiction
  · have : f 0 = f 1 := by rw [h0, h1]
    have : (0 : Fin 3) = 1 := h_inj this
    contradiction

/-! ## 4. Hidden Adapter Non-Recoverability -/

def LengthPreserving (A : PublicObservation → PublicObservation) : Prop :=
  ∀ obs, (A obs).outputTape.length = obs.outputTape.length

/-- Constructive Non-Recoverability Theorem:
A length-preserving adapter cannot recover branching capability from an obstructed linear system. -/
theorem adapter_cannot_bypass_branching
    (A : PublicObservation → PublicObservation)
    (hA : LengthPreserving A)
    (prog : List LinearOp)
    (fuel : Nat) :
    ¬ ((A (observeLinear (runLinear prog fuel (initLinearState [0])))).outputTape.length = 1 ∧
       (A (observeLinear (runLinear prog fuel (initLinearState [1])))).outputTape.length = 2) := by
  intro ⟨h1, h2⟩
  have ha0 := hA (observeLinear (runLinear prog fuel (initLinearState [0])))
  have ha1 := hA (observeLinear (runLinear prog fuel (initLinearState [1])))
  rw [ha0] at h1
  rw [ha1] at h2
  dsimp [observeLinear] at h1 h2
  have h_eq := linear_inputs_tape_len_eq prog fuel 0 1
  rw [h1, h2] at h_eq
  contradiction

end G010
