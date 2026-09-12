/-!
# Target X303: Bounded Operational Agency & Discrete Viability Envelopes

Pure constructive Core Lean 4 formalization of:
1. Discrete Relational Carrier States & Hard Boundary Viability Envelopes.
2. Operational Action Proposals & Ephemeral Counterfactual Projections.
3. Empirical Grounding & Committee Authorization Licensing (Alpha Engine Contract).
4. Finite Memory Horizons & Bounded State Retention.
5. Strict Refusal Semantics & Exact Carrier State Preservation on Refusal.
6. Monotonic Operational Fuel Consumption.
7. Exact Multicriteria Rational Utility Scoring & Pareto Dominance.

AuthorityEffect: None.
Axiom Baseline: strictly contained in {propext, Quot.sound} (zero Classical.choice, zero mathlib).
-/

namespace X303BoundedAgency

set_option linter.unusedVariables false

-- ============================================================================
-- 1. Discrete Relational Carrier State
-- ============================================================================

/-- Judgment instance: a judgment form index and an argument tuple of datum indices. -/
abbrev Inst := Nat × List Nat

/-- Separation requirement pair (i, j) on datum indices. -/
abbrev ReqPair := Nat × Nat

/-- Discrete relational carrier state representing the operational substrate configuration. -/
structure CarrierState where
  data : Nat
  forms : List Nat
  insts : List Inst
  rules : List Nat
  reqs : List ReqPair
  deriving DecidableEq, Repr

namespace CarrierState

def empty : CarrierState :=
  { data := 0, forms := [], insts := [], rules := [], reqs := [] }

def n_data (s : CarrierState) : Nat := s.data
def n_forms (s : CarrierState) : Nat := s.forms.length
def n_insts (s : CarrierState) : Nat := s.insts.length
def n_rules (s : CarrierState) : Nat := s.rules.length
def n_reqs (s : CarrierState) : Nat := s.reqs.length

end CarrierState

-- ============================================================================
-- 2. Discrete Viability Envelope
-- ============================================================================

/-- Explicit discrete viability envelope defining hard resource ceilings,
    non-empty core sort requirements, and mandatory separation requirements. -/
structure ViabilityEnvelope where
  minData : Nat := 1
  maxData : Nat
  minForms : Nat := 1
  maxForms : Nat
  maxArity : Nat
  maxInsts : Nat
  requiredReqs : List ReqPair := []
  deriving DecidableEq, Repr

/-- Decidable check whether a carrier state satisfies all envelope boundaries. -/
def isViableBool (env : ViabilityEnvelope) (s : CarrierState) : Bool :=
  s.data ≥ env.minData &&
  s.data ≤ env.maxData &&
  s.forms.length ≥ env.minForms &&
  s.forms.length ≤ env.maxForms &&
  s.forms.all (fun arity => arity ≤ env.maxArity) &&
  s.insts.length ≤ env.maxInsts &&
  env.requiredReqs.all (fun req => req ∈ s.reqs)

/-- Viability proposition: the carrier state resides within the viability envelope. -/
def isViable (env : ViabilityEnvelope) (s : CarrierState) : Prop :=
  isViableBool env s = true

instance (env : ViabilityEnvelope) (s : CarrierState) : Decidable (isViable env s) :=
  inferInstanceAs (Decidable (isViableBool env s = true))

-- ============================================================================
-- 3. Action Space, Fuel Costs & Counterfactual Projections
-- ============================================================================

/-- Well-formed operational interventions admissible on the relational carrier. -/
inductive Action where
  | admitDatum : Action
  | admitForm (arity : Nat) : Action
  | admitInst (form : Nat) (args : List Nat) : Action
  | imposeReq (i j : Nat) : Action
  | noop : Action
  deriving DecidableEq, Repr

/-- Exact operational fuel cost for candidate actions. -/
def actionCost : Action → Nat
  | .admitDatum => 1
  | .admitForm _ => 1
  | .admitInst _ _ => 1
  | .imposeReq _ _ => 1
  | .noop => 1

theorem actionCost_pos (a : Action) : 0 < actionCost a := by
  cases a <;> (dsimp [actionCost]; decide)

/-- Counterfactual projection: ephemerally evaluates the causal consequences of an action
    on a candidate carrier state without committing state mutations. -/
def project (s : CarrierState) : Action → CarrierState
  | .admitDatum =>
      { s with data := s.data + 1 }
  | .admitForm arity =>
      { s with forms := s.forms ++ [arity] }
  | .admitInst form args =>
      if (form, args) ∈ s.insts then s
      else { s with insts := s.insts ++ [(form, args)] }
  | .imposeReq i j =>
      if (i, j) ∈ s.reqs then s
      else { s with reqs := s.reqs ++ [(i, j)] }
  | .noop => s

-- ============================================================================
-- 4. Empirical Grounding & Counterfactual Causal Evaluation
-- ============================================================================

/-- Decidable check for empirical grounding: verifies that an action refers only to
    extant forms, correct arities, and valid carrier data indices. -/
def isEmpiricallyGroundedBool (s : CarrierState) : Action → Bool
  | .admitDatum => true
  | .admitForm arity => arity ≥ 1
  | .admitInst form args =>
      form < s.forms.length &&
      args.all (fun d => d < s.data) &&
      (args.length == s.forms.getD form 0)
  | .imposeReq i j =>
      i < s.data && j < s.data && (i != j)
  | .noop => true

/-- Empirical grounding proposition. -/
def isEmpiricallyGrounded (s : CarrierState) (a : Action) : Prop :=
  isEmpiricallyGroundedBool s a = true

instance (s : CarrierState) (a : Action) : Decidable (isEmpiricallyGrounded s a) :=
  inferInstanceAs (Decidable (isEmpiricallyGroundedBool s a = true))

-- ============================================================================
-- 5. Authorization Licensing & The Alpha Engine Contract
-- ============================================================================

/-- Metatheoretic authorization license issued by the authorization committee.
    Adheres to the Alpha Engine Proposal -> EvalResult -> License contract. -/
structure License where
  granter : String
  scope : String
  authorizedAction : Action
  deriving DecidableEq, Repr

/-- Authorization license validity: a license is valid for an action, carrier state, and envelope
    if and only if it authorizes that specific action, the action is empirically grounded,
    and its counterfactual projection preserves the viability envelope. -/
def isLicensed (env : ViabilityEnvelope) (s : CarrierState) (a : Action) (lic : License) : Prop :=
  lic.authorizedAction = a ∧
  isEmpiricallyGrounded s a ∧
  isViable env (project s a)

/-- Decidable check for license validity. -/
def isLicensedBool (env : ViabilityEnvelope) (s : CarrierState) (a : Action) (lic : License) : Bool :=
  (lic.authorizedAction == a) &&
  isEmpiricallyGroundedBool s a &&
  isViableBool env (project s a)

theorem isLicensed_iff_bool (env : ViabilityEnvelope) (s : CarrierState) (a : Action) (lic : License) :
    isLicensed env s a lic ↔ isLicensedBool env s a lic = true := by
  dsimp [isLicensed, isLicensedBool, isEmpiricallyGrounded, isViable]
  rw [Bool.and_eq_true, Bool.and_eq_true, beq_iff_eq, and_assoc]

-- ============================================================================
-- 6. Finite Memory Horizon & Bounded State Retention
-- ============================================================================

/-- Single transition record stored in bounded memory. -/
structure MemoryRecord where
  stepIndex : Nat
  actionTaken : Action
  fuelCost : Nat
  deriving DecidableEq, Repr

/-- Bounded memory buffer of maximum horizon H. -/
structure BoundedMemory where
  horizon : Nat
  records : List MemoryRecord
  deriving DecidableEq, Repr

/-- Deterministic FIFO push respecting the finite memory horizon bound H. -/
def BoundedMemory.push (mem : BoundedMemory) (rec : MemoryRecord) : BoundedMemory :=
  let updated := mem.records ++ [rec]
  if updated.length > mem.horizon then
    { mem with records := updated.drop (updated.length - mem.horizon) }
  else
    { mem with records := updated }

theorem memory_bounded (mem : BoundedMemory) (rec : MemoryRecord) :
    (mem.push rec).records.length ≤ mem.horizon := by
  dsimp [BoundedMemory.push]
  split
  · next h_gt =>
    dsimp
    rw [List.length_drop]
    omega
  · next h_le =>
    dsimp
    omega

-- ============================================================================
-- 7. Agent State, Step Execution & Strict Refusal Semantics
-- ============================================================================

/-- Controller state carrying operational fuel budget and bounded memory buffer. -/
structure AgentState where
  fuel : Nat
  memory : BoundedMemory
  deriving DecidableEq, Repr

/-- Typed operational refusal reasons. -/
inductive RefusalReason where
  | viabilityBoundaryExceeded : RefusalReason
  | fuelExhausted : RefusalReason
  | unauthorizedAction : RefusalReason
  | ungroundedIntervention : RefusalReason
  deriving DecidableEq, Repr

/-- Typed step execution result. -/
inductive StepResult where
  | admitted (nextState : CarrierState) (nextAgent : AgentState) (license : License) : StepResult
  | refusal (retainedState : CarrierState) (retainedAgent : AgentState) (reason : RefusalReason) : StepResult
  deriving DecidableEq, Repr

def StepResult.state : StepResult → CarrierState
  | .admitted nextState _ _ => nextState
  | .refusal retainedState _ _ => retainedState

def StepResult.fuel : StepResult → Nat
  | .admitted _ nextAgent _ => nextAgent.fuel
  | .refusal _ retainedAgent _ => retainedAgent.fuel

/-- Bounded operational execution step:
    Applies an action under strict committee licensing and viability envelope checks.
    Emits typed refusal preserving carrier state and fuel unmutated if any condition fails. -/
def stepExecution
    (env : ViabilityEnvelope) (s : CarrierState) (agent : AgentState)
    (a : Action) (optLic : Option License) (stepIndex : Nat) : StepResult :=
  if agent.fuel < actionCost a then
    StepResult.refusal s agent RefusalReason.fuelExhausted
  else
    match optLic with
    | none =>
        StepResult.refusal s agent RefusalReason.unauthorizedAction
    | some lic =>
        if lic.authorizedAction ≠ a then
          StepResult.refusal s agent RefusalReason.unauthorizedAction
        else if isEmpiricallyGroundedBool s a = false then
          StepResult.refusal s agent RefusalReason.ungroundedIntervention
        else if isViableBool env (project s a) = false then
          StepResult.refusal s agent RefusalReason.viabilityBoundaryExceeded
        else
          let nextState := project s a
          let nextMem := agent.memory.push { stepIndex := stepIndex, actionTaken := a, fuelCost := actionCost a }
          let nextAgent := { fuel := agent.fuel - actionCost a, memory := nextMem }
          StepResult.admitted nextState nextAgent lic

-- ============================================================================
-- 8. Core Theorems
-- ============================================================================

/-- Theorem 1 (viability_preservation):
    A licensed state transition guarantees preservation of the discrete viability envelope. -/
theorem viability_preservation
    (env : ViabilityEnvelope) (s : CarrierState) (agent : AgentState)
    (a : Action) (lic : Option License) (idx : Nat)
    (s' : CarrierState) (agent' : AgentState) (l : License)
    (h_step : stepExecution env s agent a lic idx = StepResult.admitted s' agent' l) :
    isViable env s' := by
  dsimp [stepExecution] at h_step
  split at h_step
  · contradiction
  · cases lic with
    | none => contradiction
    | some licVal =>
        dsimp at h_step
        split at h_step
        · contradiction
        · split at h_step
          · contradiction
          · split at h_step
            · contradiction
            · injection h_step with h_s' _ _
              dsimp [isViable]
              rw [← h_s']
              cases hb : isViableBool env (project s a)
              · contradiction
              · rfl

/-- Lemma: Direct action-level viability preservation for any authorized action. -/
theorem licensed_action_preserves_viability
    (env : ViabilityEnvelope) (s : CarrierState) (a : Action) (lic : License)
    (h_lic : isLicensed env s a lic) :
    isViable env (project s a) :=
  h_lic.2.2

/-- Theorem 2 (causal_action_selection_soundness):
    An action is licensed only if its counterfactual projection preserves empirical grounding and viability. -/
theorem causal_action_selection_soundness
    (env : ViabilityEnvelope) (s : CarrierState) (a : Action) (lic : License)
    (h_lic : isLicensed env s a lic) :
    isViable env (project s a) ∧ isEmpiricallyGrounded s a :=
  ⟨h_lic.2.2, h_lic.2.1⟩

/-- Soundness of step execution: an admitted step satisfies counterfactual viability,
    empirical grounding, and authorization licensing. -/
theorem step_causal_action_selection_soundness
    (env : ViabilityEnvelope) (s : CarrierState) (agent : AgentState)
    (a : Action) (lic : Option License) (idx : Nat)
    (s' : CarrierState) (agent' : AgentState) (l : License)
    (h_step : stepExecution env s agent a lic idx = StepResult.admitted s' agent' l) :
    isViable env (project s a) ∧ isEmpiricallyGrounded s a ∧ l.authorizedAction = a := by
  dsimp [stepExecution] at h_step
  split at h_step
  · contradiction
  · cases lic with
    | none => contradiction
    | some licVal =>
        dsimp at h_step
        split at h_step
        · contradiction
        · split at h_step
          · contradiction
          · split at h_step
            · contradiction
            · injection h_step with _ _ h_l
              have h_eq_act : l.authorizedAction = a := by
                have h_eq : licVal.authorizedAction = a := by
                  by_cases h : licVal.authorizedAction = a
                  · exact h
                  · contradiction
                rw [← h_l, h_eq]
              have h_grd_p : isEmpiricallyGrounded s a := by
                dsimp [isEmpiricallyGrounded]
                cases h_gb : isEmpiricallyGroundedBool s a
                · contradiction
                · rfl
              have h_viab_p : isViable env (project s a) := by
                dsimp [isViable]
                cases h_vb : isViableBool env (project s a)
                · contradiction
                · rfl
              exact ⟨h_viab_p, h_grd_p, h_eq_act⟩

/-- Theorem 3 (state_preservation_on_refusal):
    When execution emits refusal, the carrier state is preserved identically (`state_after = state_before`). -/
theorem state_preservation_on_refusal
    (env : ViabilityEnvelope) (s : CarrierState) (agent : AgentState)
    (a : Action) (lic : Option License) (idx : Nat)
    (s_ret : CarrierState) (agent_ret : AgentState) (reason : RefusalReason)
    (h_ref : stepExecution env s agent a lic idx = StepResult.refusal s_ret agent_ret reason) :
    s_ret = s := by
  dsimp [stepExecution] at h_ref
  split at h_ref
  · injection h_ref with h_s _ _
    exact h_s.symm
  · cases lic with
    | none =>
        injection h_ref with h_s _ _
        exact h_s.symm
    | some licVal =>
        dsimp at h_ref
        split at h_ref
        · injection h_ref with h_s _ _
          exact h_s.symm
        · split at h_ref
          · injection h_ref with h_s _ _
            exact h_s.symm
          · split at h_ref
            · injection h_ref with h_s _ _
              exact h_s.symm
            · contradiction

/-- State identity accessor under refusal. -/
theorem state_preservation_on_refusal_state
    (env : ViabilityEnvelope) (s : CarrierState) (agent : AgentState)
    (a : Action) (lic : Option License) (idx : Nat)
    (s_ret : CarrierState) (agent_ret : AgentState) (reason : RefusalReason)
    (h_ref : stepExecution env s agent a lic idx = StepResult.refusal s_ret agent_ret reason) :
    (stepExecution env s agent a lic idx).state = s := by
  rw [h_ref]
  dsimp [StepResult.state]
  exact state_preservation_on_refusal env s agent a lic idx s_ret agent_ret reason h_ref

/-- Theorem 4 (fuel_monotonicity):
    Every execution step strictly consumes fuel monotonically (`fuel_after < fuel_before` on action,
    or preserves fuel on refusal). -/
theorem fuel_monotonicity
    (env : ViabilityEnvelope) (s : CarrierState) (agent : AgentState)
    (a : Action) (lic : Option License) (idx : Nat) :
    match stepExecution env s agent a lic idx with
    | .admitted _ agent' _ => agent'.fuel < agent.fuel
    | .refusal _ agent' _ => agent'.fuel = agent.fuel := by
  cases h_step : stepExecution env s agent a lic idx with
  | admitted s' agent' l =>
      dsimp [stepExecution] at h_step
      split at h_step
      · contradiction
      · rename_i h_fuel
        cases lic with
        | none => contradiction
        | some licVal =>
            dsimp at h_step
            split at h_step
            · contradiction
            · split at h_step
              · contradiction
              · split at h_step
                · contradiction
                · injection h_step with _ h_ag _
                  rw [← h_ag]
                  dsimp
                  have h_cost_pos := actionCost_pos a
                  omega
  | refusal s_ret agent_ret reason =>
      dsimp [stepExecution] at h_step
      split at h_step
      · injection h_step with _ h_ag _
        rw [← h_ag]
      · cases lic with
        | none =>
            injection h_step with _ h_ag _
            rw [← h_ag]
        | some licVal =>
            dsimp at h_step
            split at h_step
            · injection h_step with _ h_ag _
              rw [← h_ag]
            · split at h_step
              · injection h_step with _ h_ag _
                rw [← h_ag]
              · split at h_step
                · injection h_step with _ h_ag _
                  rw [← h_ag]
                · contradiction

/-- Strict fuel consumption on admitted action execution. -/
theorem fuel_monotonicity_action
    (env : ViabilityEnvelope) (s : CarrierState) (agent : AgentState)
    (a : Action) (lic : Option License) (idx : Nat)
    (s' : CarrierState) (agent' : AgentState) (l : License)
    (h_step : stepExecution env s agent a lic idx = StepResult.admitted s' agent' l) :
    agent'.fuel < agent.fuel := by
  have hm := fuel_monotonicity env s agent a lic idx
  rw [h_step] at hm
  exact hm

/-- Fuel preservation on typed refusal. -/
theorem fuel_monotonicity_refusal
    (env : ViabilityEnvelope) (s : CarrierState) (agent : AgentState)
    (a : Action) (lic : Option License) (idx : Nat)
    (s_ret : CarrierState) (agent_ret : AgentState) (reason : RefusalReason)
    (h_ref : stepExecution env s agent a lic idx = StepResult.refusal s_ret agent_ret reason) :
    agent_ret.fuel = agent.fuel := by
  have hm := fuel_monotonicity env s agent a lic idx
  rw [h_ref] at hm
  exact hm

/-- Weak monotonicity: fuel never increases across any execution step. -/
theorem fuel_monotonicity_le
    (env : ViabilityEnvelope) (s : CarrierState) (agent : AgentState)
    (a : Action) (lic : Option License) (idx : Nat) :
    (stepExecution env s agent a lic idx).fuel ≤ agent.fuel := by
  have hm := fuel_monotonicity env s agent a lic idx
  cases h_step : stepExecution env s agent a lic idx with
  | admitted s' agent' l =>
      rw [h_step] at hm
      dsimp [StepResult.fuel]
      omega
  | refusal s_ret agent_ret reason =>
      rw [h_step] at hm
      dsimp [StepResult.fuel]
      omega

-- ============================================================================
-- 9. Zero Unilateral Authority & Refusal Triggers
-- ============================================================================

/-- Zero unilateral authority: executing an action without a license unconditionally emits refusal. -/
theorem zero_unilateral_authority
    (env : ViabilityEnvelope) (s : CarrierState) (agent : AgentState)
    (a : Action) (idx : Nat) :
    ∃ reason, stepExecution env s agent a none idx = StepResult.refusal s agent reason := by
  dsimp [stepExecution]
  split
  · exact ⟨RefusalReason.fuelExhausted, rfl⟩
  · exact ⟨RefusalReason.unauthorizedAction, rfl⟩

/-- Fuel exhaustion refusal: executing any action when fuel = 0 emits refusal and preserves state. -/
theorem fuel_exhaustion_refusal
    (env : ViabilityEnvelope) (s : CarrierState) (agent : AgentState)
    (a : Action) (lic : Option License) (idx : Nat)
    (h_fuel_zero : agent.fuel = 0) :
    stepExecution env s agent a lic idx =
      StepResult.refusal s agent RefusalReason.fuelExhausted := by
  dsimp [stepExecution]
  have h_cost := actionCost_pos a
  have h_lt : agent.fuel < actionCost a := by omega
  rw [if_pos h_lt]

-- ============================================================================
-- 10. Exact Multicriteria Rational Scoring & Pareto Dominance
-- ============================================================================

/-- Multicriteria rational valuation vector:
    All components represent exact rational scores scaled to natural numbers. -/
structure UtilityVector where
  margin : Nat
  fuel : Nat
  goal : Nat
  deriving DecidableEq, Repr

/-- Exact Pareto dominance relation:
    u1 dominates u2 iff u1 is weakly superior in all criteria and strictly superior in at least one. -/
def paretoDominates (u1 u2 : UtilityVector) : Prop :=
  u1.margin ≥ u2.margin ∧ u1.fuel ≥ u2.fuel ∧ u1.goal ≥ u2.goal ∧
  (u1.margin > u2.margin ∨ u1.fuel > u2.fuel ∨ u1.goal > u2.goal)

/-- Pareto dominance is strictly irreflexive. -/
theorem pareto_dominance_irreflexive (u : UtilityVector) :
    ¬ paretoDominates u u := by
  intro ⟨_, _, _, h_or⟩
  rcases h_or with h | h | h <;> omega

/-- Pareto dominance is transitive. -/
theorem pareto_dominance_transitive (u1 u2 u3 : UtilityVector) :
    paretoDominates u1 u2 → paretoDominates u2 u3 → paretoDominates u1 u3 := by
  intro ⟨h_m1, h_f1, h_g1, h_or1⟩ ⟨h_m2, h_f2, h_g2, h_or2⟩
  refine ⟨by omega, by omega, by omega, ?_⟩
  rcases h_or1 with hm1 | hf1 | hg1
  · left; omega
  · rcases h_or2 with hm2 | hf2 | hg2
    · left; omega
    · right; left; omega
    · right; left; omega
  · rcases h_or2 with hm2 | hf2 | hg2
    · left; omega
    · right; left; omega
    · right; right; omega

/-- Pareto dominance is asymmetric. -/
theorem pareto_dominance_asymmetric (u1 u2 : UtilityVector) :
    paretoDominates u1 u2 → ¬ paretoDominates u2 u1 := by
  intro h12 h21
  have h11 := pareto_dominance_transitive u1 u2 u1 h12 h21
  exact pareto_dominance_irreflexive u1 h11

end X303BoundedAgency
