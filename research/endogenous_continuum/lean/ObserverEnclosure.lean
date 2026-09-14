-- research/endogenous_continuum/lean/ObserverEnclosure.lean
-- Track 1: Endogenous Observer Enclosure
-- AuthorityEffect: None.

namespace ObserverEnclosure

set_option linter.unusedVariables false

/-!
# Track 1: Endogenous Observer Enclosure

Constructive formalization of observer enclosure within discrete relational carrier states:
1. Internal observer sub-grammar (queries, readout values, and localized readouts).
2. Carrier state with embedded observer infrastructure (`CarrierWithObserver`).
3. Localized rewrite transitions executing state updates and internal observation
   logging without external oracle reliance or prefix history inspection.
4. Internal trace invariant (`TraceInvariant`) asserting structural alignment between
   the recorded trace and the sequence of local transitions executed.
5. Constructive soundness theorems:
   - `trace_step_preserves_invariant`: local rewrite step preserves TraceInvariant.
   - `no_retrocausal_mutation`: earlier trace entries are immutable under forward steps.
   - `observer_readout_soundness`: recorded readouts are faithful reflections of carrier state
     at time of evaluation.
   - `localized_enclosure_soundness`: state evaluation and record-keeping require no external
     oracle or prefix inspection.
-/

/-- Relational instance: form index and argument tuple of datum indices. -/
abbrev Inst := Nat × List Nat

/-- Deduplicating list insertion for constructive finite collections. -/
def insertNew {α : Type} [DecidableEq α] (l : List α) (a : α) : List α :=
  if a ∈ l then l else l ++ [a]

@[simp] theorem insertNew_nil {α : Type} [DecidableEq α] (a : α) :
    insertNew [] a = [a] := rfl

-- ============================================================================
-- 1. Internal Observer Sub-Grammar
-- ============================================================================

/-- Local observation query syntax within the carrier enclosure. -/
inductive ObservationQuery where
  | carrierDataCount : ObservationQuery
  | carrierFormCount : ObservationQuery
  | carrierInstCount : ObservationQuery
  | hasInstance (form : Nat) (args : List Nat) : ObservationQuery
  | formArity (form : Nat) : ObservationQuery
deriving DecidableEq, Repr

/-- Observation readout values produced by internal evaluation. -/
inductive ReadoutValue where
  | countVal (n : Nat) : ReadoutValue
  | boolVal (b : Bool) : ReadoutValue
  | arityVal (opt : Option Nat) : ReadoutValue
deriving DecidableEq, Repr

/-- A local observation readout record tagged with its execution step index. -/
structure LocalReadout where
  stepIdx : Nat
  query   : ObservationQuery
  value   : ReadoutValue
deriving DecidableEq, Repr

/-- Carrier core components: data count, form arities, and relational instances. -/
structure CarrierCore where
  data  : Nat
  forms : List Nat
  insts : List Inst
deriving DecidableEq, Repr

/-- Localized state evaluation: evaluates an observation query strictly against
the immediate carrier contents without consulting external oracles or history traces. -/
def evaluateLocal (c : CarrierCore) : ObservationQuery → ReadoutValue
  | .carrierDataCount => .countVal c.data
  | .carrierFormCount => .countVal c.forms.length
  | .carrierInstCount => .countVal c.insts.length
  | .hasInstance f args => .boolVal (decide ((f, args) ∈ c.insts))
  | .formArity f => .arityVal c.forms[f]?

-- ============================================================================
-- 2. Transition Actions and Step Records
-- ============================================================================

/-- Transition actions executable within the enclosed carrier system. -/
inductive TransitionAction where
  | admitDatum : TransitionAction
  | admitForm (arity : Nat) : TransitionAction
  | admitInst (form : Nat) (args : List Nat) : TransitionAction
  | observe (query : ObservationQuery) : TransitionAction
deriving DecidableEq, Repr

/-- A step record preserved in the internal transition history. -/
structure StepRecord where
  stepIdx : Nat
  action  : TransitionAction
  readout : Option LocalReadout
deriving DecidableEq, Repr

-- ============================================================================
-- 3. Carrier State with Embedded Observer Enclosure
-- ============================================================================

/-- Carrier state with internal observer sub-grammar and record-keeping trace. -/
structure CarrierWithObserver where
  data        : Nat
  forms       : List Nat
  insts       : List Inst
  stepCounter : Nat
  readoutLog  : List LocalReadout
  history     : List StepRecord
deriving DecidableEq, Repr

/-- Projection to the carrier core components. -/
def CarrierWithObserver.core (s : CarrierWithObserver) : CarrierCore :=
  ⟨s.data, s.forms, s.insts⟩

/-- Initial genesis carrier state with empty observer trace. -/
def initCarrier : CarrierWithObserver where
  data        := 0
  forms       := []
  insts       := []
  stepCounter := 0
  readoutLog  := []
  history     := []

-- ============================================================================
-- 4. Localized Rewrite Transitions
-- ============================================================================

/-- Pure carrier core transition function without trace tracking. -/
def applyActionCore (c : CarrierCore) : TransitionAction → CarrierCore
  | .admitDatum => ⟨c.data + 1, c.forms, c.insts⟩
  | .admitForm a =>
      if 1 ≤ a then ⟨c.data, c.forms ++ [a], c.insts⟩
      else c
  | .admitInst f args =>
      if f < c.forms.length ∧ args.length = c.forms.getD f 0 ∧
          (args.all (fun x => x < c.data)) then
        ⟨c.data, c.forms, insertNew c.insts (f, args)⟩
      else c
  | .observe _ => c

/-- Step rewrite modifies carrier state and records observation internally
without external oracle consultation or prefix inspection. -/
def localStep (s : CarrierWithObserver) (act : TransitionAction) : CarrierWithObserver :=
  let newCore := applyActionCore s.core act
  let newReadout : Option LocalReadout :=
    match act with
    | .observe q => some ⟨s.stepCounter, q, evaluateLocal s.core q⟩
    | _ => none
  let newReadoutLog : List LocalReadout :=
    match newReadout with
    | some ro => s.readoutLog ++ [ro]
    | none => s.readoutLog
  let newRecord : StepRecord := ⟨s.stepCounter, act, newReadout⟩
  { data        := newCore.data
    forms       := newCore.forms
    insts       := newCore.insts
    stepCounter := s.stepCounter + 1
    readoutLog  := newReadoutLog
    history     := s.history ++ [newRecord] }

/-- Multi-step rewrite executing a list of transition actions sequentially. -/
def multiStep (s : CarrierWithObserver) : List TransitionAction → CarrierWithObserver
  | [] => s
  | act :: rest => multiStep (localStep s act) rest

/-- Replay carrier core state from a history of step records. -/
def replayCore (hist : List StepRecord) : CarrierCore :=
  hist.foldl (fun c rec => applyActionCore c rec.action) ⟨0, [], []⟩

@[simp] theorem replayCore_nil : replayCore [] = ⟨0, [], []⟩ := rfl

@[simp] theorem replayCore_append_singleton (hist : List StepRecord) (rec : StepRecord) :
    replayCore (hist ++ [rec]) = applyActionCore (replayCore hist) rec.action := by
  dsimp [replayCore]
  rw [List.foldl_append]
  rfl

/-- Extract all recorded readouts from a history of step records. -/
def extractReadouts (hist : List StepRecord) : List LocalReadout :=
  hist.filterMap (fun r => r.readout)

@[simp] theorem extractReadouts_nil : extractReadouts [] = [] := rfl

@[simp] theorem extractReadouts_append (h1 h2 : List StepRecord) :
    extractReadouts (h1 ++ h2) = extractReadouts h1 ++ extractReadouts h2 := by
  dsimp [extractReadouts]
  exact List.filterMap_append

@[simp] theorem extractReadouts_singleton (rec : StepRecord) :
    extractReadouts [rec] = match rec.readout with | some ro => [ro] | none => [] := by
  dsimp [extractReadouts, List.filterMap]
  cases rec.readout <;> rfl

-- ============================================================================
-- 5. Internal Trace Invariant Definition
-- ============================================================================

/-- Internal trace invariant: states that recorded history matches the sequence
of local transitions executed, the step counter matches history length, step indices
are strictly sequenced, readouts in the log match those recorded in the history, and
the carrier state is the faithful replay of the transition history from genesis. -/
structure TraceInvariant (s : CarrierWithObserver) : Prop where
  step_count_eq : s.stepCounter = s.history.length
  history_indexing : ∀ (i : Nat) (h : i < s.history.length),
    s.history[i].stepIdx = i
  carrier_replays : s.core = replayCore s.history
  readout_log_matches : s.readoutLog = extractReadouts s.history

/-- The genesis carrier state satisfies the internal trace invariant. -/
theorem init_carrier_invariant : TraceInvariant initCarrier := by
  refine ⟨rfl, fun i h => (Nat.not_lt_zero i h).elim, rfl, rfl⟩

-- ============================================================================
-- 6. Key Constructive Soundness Theorems
-- ============================================================================

/-- Trace step preservation: local rewrite step preserves TraceInvariant. -/
theorem trace_step_preserves_invariant (s : CarrierWithObserver) (act : TransitionAction)
    (h : TraceInvariant s) : TraceInvariant (localStep s act) := by
  have h_step_eq : (localStep s act).stepCounter = (localStep s act).history.length := by
    dsimp [localStep]
    rw [List.length_append, List.length_singleton]
    rw [h.step_count_eq]
  have h_idx : ∀ (i : Nat) (hi : i < (localStep s act).history.length),
      (localStep s act).history[i].stepIdx = i := by
    intro i hi
    dsimp [localStep] at hi ⊢
    rw [List.length_append, List.length_singleton] at hi
    have h_split : i < s.history.length ∨ i = s.history.length := by
      omega
    cases h_split with
    | inl h_lt =>
      rw [List.getElem_append_left h_lt]
      exact h.history_indexing i h_lt
    | inr h_eq =>
      rw [List.getElem_concat_length h_eq]
      dsimp
      subst h_eq
      exact h.step_count_eq
  have h_core : (localStep s act).core = replayCore (localStep s act).history := by
    dsimp [localStep, CarrierWithObserver.core]
    rw [replayCore_append_singleton]
    rw [← h.carrier_replays]
    rfl
  have h_ro : (localStep s act).readoutLog = extractReadouts (localStep s act).history := by
    dsimp [localStep]
    rw [extractReadouts_append, extractReadouts_singleton]
    rw [← h.readout_log_matches]
    cases act with
    | admitDatum => rw [List.append_nil]
    | admitForm a => rw [List.append_nil]
    | admitInst f args => rw [List.append_nil]
    | observe q => rfl
  exact ⟨h_step_eq, h_idx, h_core, h_ro⟩

/-- Multi-step execution preserves TraceInvariant by finite induction. -/
theorem trace_multi_step_preserves_invariant (s : CarrierWithObserver) (acts : List TransitionAction)
    (h : TraceInvariant s) : TraceInvariant (multiStep s acts) := by
  induction acts generalizing s with
  | nil => exact h
  | cons act rest ih =>
    exact ih (localStep s act) (trace_step_preserves_invariant s act h)

/-- Earlier trace entries in the history are immutable under forward steps. -/
theorem no_retrocausal_mutation (s : CarrierWithObserver) (act : TransitionAction)
    (i : Nat) (hi : i < s.history.length) :
    (localStep s act).history[i]? = s.history[i]? := by
  dsimp [localStep]
  exact List.getElem?_append_left hi

/-- Earlier trace entries in the readout log are immutable under forward steps. -/
theorem no_retrocausal_readout_mutation (s : CarrierWithObserver) (act : TransitionAction)
    (i : Nat) (hi : i < s.readoutLog.length) :
    (localStep s act).readoutLog[i]? = s.readoutLog[i]? := by
  dsimp [localStep]
  cases act with
  | admitDatum => rfl
  | admitForm a => rfl
  | admitInst f args => rfl
  | observe q => exact List.getElem?_append_left hi

/-- Multi-step non-retrocausal immutability of historical trace entries. -/
theorem no_retrocausal_mutation_multi (s : CarrierWithObserver) (acts : List TransitionAction)
    (i : Nat) (hi : i < s.history.length) :
    (multiStep s acts).history[i]? = s.history[i]? := by
  induction acts generalizing s with
  | nil => rfl
  | cons act rest ih =>
    dsimp [multiStep]
    have h_step : (localStep s act).history[i]? = s.history[i]? :=
      no_retrocausal_mutation s act i hi
    have hi' : i < (localStep s act).history.length := by
      dsimp [localStep]
      rw [List.length_append, List.length_singleton]
      omega
    rw [ih (localStep s act) hi']
    exact h_step

/-- Recorded readouts are faithful reflections of carrier state at time of evaluation. -/
theorem observer_readout_soundness (s : CarrierWithObserver) (q : ObservationQuery)
    (h_inv : TraceInvariant s) :
    let s' := localStep s (.observe q)
    ∃ ro : LocalReadout,
      s'.history[s.stepCounter]? = some ⟨s.stepCounter, .observe q, some ro⟩ ∧
      ro.stepIdx = s.stepCounter ∧
      ro.query = q ∧
      ro.value = evaluateLocal s.core q := by
  dsimp [localStep]
  refine ⟨⟨s.stepCounter, q, evaluateLocal s.core q⟩, ?_, rfl, rfl, rfl⟩
  rw [h_inv.step_count_eq]
  exact List.getElem?_concat_length

/-- Recorded readout in the log is a faithful reflection of the evaluated carrier state. -/
theorem observer_readout_log_soundness (s : CarrierWithObserver) (q : ObservationQuery) :
    (localStep s (.observe q)).readoutLog[s.readoutLog.length]? =
      some ⟨s.stepCounter, q, evaluateLocal s.core q⟩ := by
  dsimp [localStep]
  exact List.getElem?_concat_length

/-- Localized enclosure soundness: state evaluation and record-keeping require
no external oracle or prefix inspection. Two states agreeing on carrier core and
step counter yield identical local query evaluations, identical next carrier states,
and identical newly emitted step records, regardless of past trace prefixes. -/
theorem localized_enclosure_soundness
    (s1 s2 : CarrierWithObserver) (act : TransitionAction) (q : ObservationQuery)
    (h_core : s1.core = s2.core)
    (h_step : s1.stepCounter = s2.stepCounter) :
    evaluateLocal s1.core q = evaluateLocal s2.core q ∧
    (localStep s1 act).core = (localStep s2 act).core ∧
    (localStep s1 act).history[s1.history.length]? =
      (localStep s2 act).history[s2.history.length]? := by
  have h_eval : evaluateLocal s1.core q = evaluateLocal s2.core q := by
    rw [h_core]
  have h_next_core : (localStep s1 act).core = (localStep s2 act).core := by
    change applyActionCore s1.core act = applyActionCore s2.core act
    rw [h_core]
  have h_rec : (localStep s1 act).history[s1.history.length]? =
      (localStep s2 act).history[s2.history.length]? := by
    dsimp [localStep]
    rw [List.getElem?_concat_length, List.getElem?_concat_length]
    rw [h_core, h_step]
  exact ⟨h_eval, h_next_core, h_rec⟩

/-- Local evaluation on carrier state has zero dependence on trace history. -/
theorem local_evaluation_prefix_independent (s : CarrierWithObserver)
    (hist' : List StepRecord) (q : ObservationQuery) :
    evaluateLocal { s with history := hist' }.core q = evaluateLocal s.core q := rfl

-- ============================================================================
-- 7. Axiom Audit
-- ============================================================================

#print axioms init_carrier_invariant
#print axioms trace_step_preserves_invariant
#print axioms trace_multi_step_preserves_invariant
#print axioms no_retrocausal_mutation
#print axioms no_retrocausal_readout_mutation
#print axioms no_retrocausal_mutation_multi
#print axioms observer_readout_soundness
#print axioms observer_readout_log_soundness
#print axioms localized_enclosure_soundness
#print axioms local_evaluation_prefix_independent

end ObserverEnclosure
