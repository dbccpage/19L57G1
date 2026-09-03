import DescribedReplay.Description

namespace DescribedReplay

def eventAt {α : Type} : List α → Nat → Option α
  | [], _ => none
  | value :: _, 0 => some value
  | _ :: rest, index + 1 => eventAt rest index

theorem eventAt_exists_of_lt {α : Type} (values : List α) (index : Nat)
    (hindex : index < values.length) :
    ∃ value, eventAt values index = some value := by
  induction values generalizing index with
  | nil => simp at hindex
  | cons head rest ih =>
      cases index with
      | zero => exact ⟨head, rfl⟩
      | succ index =>
          have htail : index < rest.length := by
            simpa using hindex
          obtain ⟨value, hvalue⟩ := ih index htail
          exact ⟨value, hvalue⟩

theorem eventAt_length {α : Type} (values : List α) :
    eventAt values values.length = none := by
  induction values with
  | nil => rfl
  | cons _ rest ih => simpa [eventAt] using ih

def prefixFoldFrom : List Event → Nat → Regime → Option Regime
  | _, 0, regime => some regime
  | [], _ + 1, regime => some regime
  | event :: rest, count + 1, regime =>
      match transition regime event with
      | none => none
      | some next => prefixFoldFrom rest count next

def prefixState (history : List Event) (pointer : Nat) : Option Regime :=
  prefixFoldFrom history pointer emptyRegime

theorem prefixFoldFrom_eq_replayFrom_take (history : List Event)
    (count : Nat) (regime : Regime) :
    prefixFoldFrom history count regime =
      replayFrom (history.take count) regime := by
  induction count generalizing history regime with
  | zero =>
      cases history <;> rfl
  | succ count ih =>
      cases history with
      | nil => rfl
      | cons event rest =>
          simp only [prefixFoldFrom, List.take, replayFrom]
          cases hnext : transition regime event with
          | none => rfl
          | some next =>
              simp [ih]

theorem prefixState_eq_replay_take (history : List Event) (pointer : Nat) :
    prefixState history pointer = replay (history.take pointer) := by
  exact prefixFoldFrom_eq_replayFrom_take history pointer emptyRegime

theorem prefixFoldFrom_next (history : List Event) (pointer : Nat)
    (regime current : Regime) (event : Event) (next : Regime)
    (hprefix : prefixFoldFrom history pointer regime = some current)
    (hevent : eventAt history pointer = some event)
    (hnext : transition current event = some next) :
    prefixFoldFrom history (pointer + 1) regime = some next := by
  induction history generalizing pointer regime current event next with
  | nil =>
      cases pointer <;> cases hevent
  | cons head rest ih =>
      cases pointer with
      | zero =>
          simp [prefixFoldFrom, eventAt] at hprefix hevent
          subst current
          subst event
          simp [prefixFoldFrom, hnext]
      | succ pointer =>
          cases hhead : transition regime head with
          | none =>
              simp [prefixFoldFrom, hhead] at hprefix
          | some afterHead =>
              simp [prefixFoldFrom, hhead] at hprefix ⊢
              exact ih pointer afterHead current event next hprefix hevent hnext

theorem prefixState_next (history : List Event) (pointer : Nat)
    (current : Regime) (event : Event) (next : Regime)
    (hprefix : prefixState history pointer = some current)
    (hevent : eventAt history pointer = some event)
    (hnext : transition current event = some next) :
    prefixState history (pointer + 1) = some next := by
  exact prefixFoldFrom_next history pointer emptyRegime current event next
    hprefix hevent hnext

theorem wellFormed_transition_at (history : List Event) (pointer : Nat)
    (regime current : Regime) (event : Event)
    (hwell : wellFormedFrom history regime = true)
    (hprefix : prefixFoldFrom history pointer regime = some current)
    (hevent : eventAt history pointer = some event) :
    transition current event = some (applyEvent current event) := by
  induction history generalizing pointer regime current event with
  | nil =>
      cases pointer <;> cases hevent
  | cons head rest ih =>
      have hparts : eventValid regime head = true ∧
          wellFormedFrom rest (applyEvent regime head) = true := by
        simpa [wellFormedFrom] using hwell
      cases pointer with
      | zero =>
          simp [prefixFoldFrom, eventAt] at hprefix hevent
          subst current
          subst event
          simp [transition, hparts.1]
      | succ pointer =>
          have hhead : transition regime head = some (applyEvent regime head) := by
            simp [transition, hparts.1]
          simp [prefixFoldFrom, hhead] at hprefix
          exact ih pointer (applyEvent regime head) current event hparts.2
            hprefix hevent

def stateTraceFrom : List Event → Regime → List Regime
  | [], regime => [regime]
  | event :: rest, regime =>
      regime :: stateTraceFrom rest (applyEvent regime event)

def stateTrace (history : List Event) : List Regime :=
  stateTraceFrom history emptyRegime

theorem stateTraceFrom_length (history : List Event) (regime : Regime) :
    (stateTraceFrom history regime).length = history.length + 1 := by
  induction history generalizing regime with
  | nil => rfl
  | cons event rest ih =>
      simp [stateTraceFrom, ih]

theorem stateTrace_length (history : List Event) :
    (stateTrace history).length = history.length + 1 := by
  exact stateTraceFrom_length history emptyRegime

theorem eventAt_stateTraceFrom_eq_prefixFoldFrom (history : List Event)
    (pointer : Nat) (regime : Regime)
    (hwell : wellFormedFrom history regime = true)
    (hbound : pointer ≤ history.length) :
    eventAt (stateTraceFrom history regime) pointer =
      prefixFoldFrom history pointer regime := by
  induction history generalizing pointer regime with
  | nil =>
      have hzero : pointer = 0 := by
        simp at hbound
        omega
      subst pointer
      rfl
  | cons event rest ih =>
      have hparts : eventValid regime event = true ∧
          wellFormedFrom rest (applyEvent regime event) = true := by
        simpa [wellFormedFrom] using hwell
      cases pointer with
      | zero => rfl
      | succ pointer =>
          have htail : pointer ≤ rest.length := by
            simpa using hbound
          have htransition :
              transition regime event = some (applyEvent regime event) := by
            simp [transition, hparts.1]
          simp only [stateTraceFrom, eventAt, prefixFoldFrom]
          rw [htransition]
          exact ih pointer (applyEvent regime event) hparts.2 htail

theorem eventAt_stateTrace_eq_prefixState (history : List Event)
    (pointer : Nat) (hmember : member history = true)
    (hbound : pointer ≤ history.length) :
    eventAt (stateTrace history) pointer = prefixState history pointer := by
  have hparts := hmember
  simp [member] at hparts
  exact eventAt_stateTraceFrom_eq_prefixFoldFrom history pointer emptyRegime
    hparts.2 hbound

structure PreparedDescription where
  description : DescriptionRegime
  history : List Event
  states : List Regime
  decoded : decode description = some history
  classMember : member history = true
  statesCorrect : states = stateTrace history

def prepare (description : DescriptionRegime) : Option PreparedDescription :=
  match hdecode : decode description with
  | none => none
  | some history =>
      if hmember : member history = true then
        some
          { description := description,
            history := history,
            states := stateTrace history,
            decoded := hdecode,
            classMember := hmember,
            statesCorrect := rfl }
      else none

def preparedEncode (history : List Event)
    (hmember : member history = true) : PreparedDescription :=
  { description := encode history,
    history := history,
    states := stateTrace history,
    decoded := decode_encode_id history hmember,
    classMember := hmember,
    statesCorrect := rfl }

theorem prepare_encode_exists (history : List Event)
    (hmember : member history = true) :
    ∃ prepared : PreparedDescription,
      prepare (encode history) = some prepared ∧ prepared.history = history := by
  unfold prepare
  split
  · rename_i hnone
    have hdecode := decode_encode_id history hmember
    rw [hnone] at hdecode
    cases hdecode
  · rename_i decoded hdecode
    have hevents : decoded = history := Option.some.inj
      (hdecode.symm.trans (decode_encode_id history hmember))
    subst decoded
    split
    · exact ⟨_, rfl, rfl⟩
    · rename_i houtside
      exact False.elim (houtside hmember)

structure DescribedState where
  description : DescriptionRegime
  pointer : Nat
  current : Regime

inductive StepResult where
  | stepped (state : DescribedState)
  | done
  | invalid

def stepper (prepared : PreparedDescription) (state : DescribedState) : StepResult :=
  if state.description = prepared.description then
    match eventAt prepared.states state.pointer with
    | none => .invalid
    | some expected =>
        if state.current = expected then
          match eventAt prepared.history state.pointer with
          | none =>
              if state.pointer = prepared.history.length then .done else .invalid
          | some event =>
              match transition state.current event with
              | none => .invalid
              | some next =>
                  .stepped
                    { description := state.description,
                      pointer := state.pointer + 1,
                      current := next }
        else .invalid
  else .invalid

def preparationDispatcher (prepared : Option PreparedDescription)
    (state : DescribedState) : StepResult :=
  match prepared with
  | none => .invalid
  | some witness => stepper witness state

def runSteps (prepared : PreparedDescription) : Nat → DescribedState → StepResult
  | 0, state => .stepped state
  | count + 1, state =>
      match stepper prepared state with
      | .stepped next => runSteps prepared count next
      | .done => .done
      | .invalid => .invalid

theorem stepper_one (prepared : PreparedDescription) (state : DescribedState)
    (event : Event) (next : Regime)
    (hdescription : state.description = prepared.description)
    (hcurrent : eventAt prepared.states state.pointer = some state.current)
    (hevent : eventAt prepared.history state.pointer = some event)
    (hnext : transition state.current event = some next) :
    stepper prepared state =
      .stepped
        { description := state.description,
          pointer := state.pointer + 1,
          current := next } := by
  simp [stepper, hdescription, hcurrent, hevent, hnext]

theorem stepper_current_mismatch (prepared : PreparedDescription)
    (state : DescribedState) (expected : Regime)
    (hdescription : state.description = prepared.description)
    (hexpected : eventAt prepared.states state.pointer = some expected)
    (hmismatch : state.current ≠ expected) :
    stepper prepared state = .invalid := by
  simp [stepper, hdescription, hexpected, hmismatch]

theorem decode_failure_prepares_none (description : DescriptionRegime)
    (hdecode : decode description = none) :
    prepare description = none := by
  unfold prepare
  split
  · rfl
  · rename_i history hsome
    rw [hdecode] at hsome
    cases hsome

theorem preparation_dispatch_decode_failure (state : DescribedState)
    (hdecode : decode state.description = none) :
    preparationDispatcher (prepare state.description) state = .invalid := by
  rw [decode_failure_prepares_none state.description hdecode]
  rfl

theorem preparation_dispatch_total (state : DescribedState) :
    (prepare state.description = none ∧
        preparationDispatcher (prepare state.description) state = .invalid) ∨
    ∃ prepared : PreparedDescription,
      prepare state.description = some prepared ∧
        preparationDispatcher (prepare state.description) state =
          stepper prepared state := by
  cases hprepare : prepare state.description with
  | none => exact Or.inl ⟨rfl, rfl⟩
  | some prepared =>
      exact Or.inr ⟨prepared, rfl, rfl⟩

theorem stepper_transition_semantics (prepared : PreparedDescription)
    (state next : DescribedState)
    (hone : stepper prepared state = .stepped next) :
    ∃ event : Event,
      state.description = prepared.description ∧
      eventAt prepared.states state.pointer = some state.current ∧
      eventAt prepared.history state.pointer = some event ∧
      transition state.current event = some next.current ∧
      next.description = state.description ∧
      next.pointer = state.pointer + 1 := by
  by_cases hdescription : state.description = prepared.description
  · cases hcached : eventAt prepared.states state.pointer with
    | none =>
        simp [stepper, hdescription, hcached] at hone
    | some expected =>
        by_cases hcurrent : state.current = expected
        · subst expected
          cases hevent : eventAt prepared.history state.pointer with
          | none =>
              by_cases hpointer : state.pointer = prepared.history.length
              · have hcachedEnd :
                    eventAt prepared.states prepared.history.length =
                      some state.current := by
                  simpa [hpointer] using hcached
                simp [stepper, hdescription, hpointer, hcachedEnd,
                  eventAt_length] at hone
              · simp [stepper, hdescription, hcached, hevent, hpointer] at hone
          | some event =>
              cases htransition : transition state.current event with
              | none =>
                  simp [stepper, hdescription, hcached, hevent, htransition]
                    at hone
              | some after =>
                  have hstep :
                      StepResult.stepped
                          { description := state.description,
                            pointer := state.pointer + 1,
                            current := after } = StepResult.stepped next := by
                    simpa [stepper, hdescription, hcached, hevent, htransition]
                      using hone
                  have hshape := StepResult.stepped.inj hstep
                  cases hshape
                  exact ⟨event, hdescription, rfl, rfl, htransition,
                    rfl, rfl⟩
        · simp [stepper, hdescription, hcached, hcurrent] at hone
  · simp [stepper, hdescription] at hone

theorem stepped_state_shape (prepared : PreparedDescription)
    (state next : DescribedState)
    (hone : stepper prepared state = .stepped next) :
    next.description = state.description ∧
      next.pointer = state.pointer + 1 := by
  obtain ⟨_, _, _, _, _, hdescription, hpointer⟩ :=
    stepper_transition_semantics prepared state next hone
  exact ⟨hdescription, hpointer⟩

theorem stepped_state_prefix (prepared : PreparedDescription)
    (state next : DescribedState)
    (hprefix : prefixState prepared.history state.pointer = some state.current)
    (hone : stepper prepared state = .stepped next) :
    prefixState prepared.history next.pointer = some next.current := by
  obtain ⟨event, _, _, hevent, htransition, _, hpointer⟩ :=
    stepper_transition_semantics prepared state next hone
  rw [hpointer]
  exact prefixState_next prepared.history state.pointer state.current
    event next.current hprefix hevent htransition

theorem runSteps_from_prefix (prepared : PreparedDescription)
    (pointer count : Nat) (current : Regime)
    (hprefix : prefixState prepared.history pointer = some current)
    (hbound : pointer + count ≤ prepared.history.length) :
    ∃ final : DescribedState,
      runSteps prepared count
          { description := prepared.description,
            pointer := pointer,
            current := current } =
        .stepped final ∧
      final.description = prepared.description ∧
      final.pointer = pointer + count ∧
      prefixState prepared.history final.pointer = some final.current := by
  induction count generalizing pointer current with
  | zero =>
      let final : DescribedState :=
        { description := prepared.description,
          pointer := pointer,
          current := current }
      exact ⟨final, rfl, rfl, by simp [final], hprefix⟩
  | succ count ih =>
      have hpointer : pointer < prepared.history.length := by omega
      obtain ⟨event, hevent⟩ :=
        eventAt_exists_of_lt prepared.history pointer hpointer
      have hwell := prepared.classMember
      simp [member] at hwell
      have htransition := wellFormed_transition_at prepared.history pointer
        emptyRegime current event hwell.2 hprefix hevent
      have hcached : eventAt prepared.states pointer = some current := by
        rw [prepared.statesCorrect]
        rw [eventAt_stateTrace_eq_prefixState prepared.history pointer
          prepared.classMember (by omega)]
        exact hprefix
      let nextState : DescribedState :=
        { description := prepared.description,
          pointer := pointer + 1,
          current := applyEvent current event }
      have hstep : stepper prepared
          { description := prepared.description,
            pointer := pointer,
            current := current } =
          .stepped nextState := by
        exact stepper_one prepared
          { description := prepared.description,
            pointer := pointer,
            current := current }
          event (applyEvent current event) rfl hcached hevent htransition
      have hprefixNext :
          prefixState prepared.history (pointer + 1) =
            some (applyEvent current event) :=
        prefixState_next prepared.history pointer current event
          (applyEvent current event) hprefix hevent htransition
      obtain ⟨final, hrun, hdescription, hfinalPointer, hfinalPrefix⟩ :=
        ih (pointer + 1) (applyEvent current event) hprefixNext (by omega)
      refine ⟨final, ?_, hdescription, ?_, hfinalPrefix⟩
      · simp [runSteps, hstep, nextState, hrun]
      · rw [hfinalPointer]
        omega

def initialState (prepared : PreparedDescription) : DescribedState :=
  { description := prepared.description, pointer := 0, current := emptyRegime }

def completedState (prepared : PreparedDescription) : DescribedState :=
  { description := prepared.description,
    pointer := prepared.history.length,
    current := replayTotal prepared.history }

theorem stepper_full_iteration (prepared : PreparedDescription) :
    runSteps prepared prepared.history.length (initialState prepared) =
        .stepped (completedState prepared) ∧
      stepper prepared (completedState prepared) = .done ∧
      replay prepared.history = some (replayTotal prepared.history) := by
  have hreplay := replay_eq_replayTotal_of_member prepared.history
    prepared.classMember
  have hprefixEnd :
      prefixState prepared.history prepared.history.length =
        some (replayTotal prepared.history) := by
    rw [prefixState_eq_replay_take]
    simpa using hreplay
  obtain ⟨final, hrun, hdescription, hpointer, hprefix⟩ :=
    runSteps_from_prefix prepared 0 prepared.history.length emptyRegime
      (by simp [prefixState, prefixFoldFrom]) (by simp)
  have hpointerEnd : final.pointer = prepared.history.length := by
    simpa using hpointer
  have hcurrent : final.current = replayTotal prepared.history := by
    rw [hpointerEnd] at hprefix
    exact Option.some.inj (hprefix.symm.trans hprefixEnd)
  have hfinal : final = completedState prepared := by
    cases final
    simp_all [completedState]
  subst final
  have hcachedEnd :
      eventAt prepared.states prepared.history.length =
        some (replayTotal prepared.history) := by
    rw [prepared.statesCorrect]
    rw [eventAt_stateTrace_eq_prefixState prepared.history
      prepared.history.length prepared.classMember (by simp)]
    exact hprefixEnd
  have hdone : stepper prepared (completedState prepared) = .done := by
    simp [stepper, completedState, hcachedEnd, eventAt_length]
  exact ⟨by simpa [initialState] using hrun, hdone, hreplay⟩

theorem encoded_member_full_iteration (history : List Event)
    (hmember : member history = true) :
    runSteps (preparedEncode history hmember) history.length
        (initialState (preparedEncode history hmember)) =
        .stepped (completedState (preparedEncode history hmember)) ∧
      stepper (preparedEncode history hmember)
          (completedState (preparedEncode history hmember)) = .done ∧
      replay history = some (replayTotal history) := by
  exact stepper_full_iteration (preparedEncode history hmember)

theorem stepper_iterate (prepared : PreparedDescription) (count : Nat)
    (state final : DescribedState)
    (hdescription : state.description = prepared.description)
    (hprefix : prefixState prepared.history state.pointer = some state.current)
    (hresult : runSteps prepared count state = .stepped final) :
    final.description = state.description ∧
      final.pointer = state.pointer + count ∧
      prefixState prepared.history final.pointer = some final.current ∧
      replay (prepared.history.take final.pointer) = some final.current := by
  induction count generalizing state with
  | zero =>
      simp [runSteps] at hresult
      subst final
      exact ⟨rfl, by simp, hprefix,
        (prefixState_eq_replay_take prepared.history state.pointer).symm.trans
          hprefix⟩
  | succ count ih =>
      simp only [runSteps] at hresult
      cases hstep : stepper prepared state with
      | invalid => simp [hstep] at hresult
      | done => simp [hstep] at hresult
      | stepped next =>
          simp [hstep] at hresult
          have hone := stepped_state_shape prepared state next hstep
          have hprefixNext := stepped_state_prefix prepared state next hprefix hstep
          have htail := ih next (hone.1.trans hdescription) hprefixNext hresult
          constructor
          · exact htail.1.trans hone.1
          · constructor
            · rw [htail.2.1, hone.2]
              omega
            · constructor
              · exact htail.2.2.1
              · exact htail.2.2.2

theorem stepper_total (prepared : PreparedDescription)
    (state : DescribedState) :
    (state.description ≠ prepared.description ∧
        stepper prepared state = .invalid) ∨
    (state.description = prepared.description ∧
        eventAt prepared.states state.pointer = none ∧
        stepper prepared state = .invalid) ∨
    (∃ expected,
        state.description = prepared.description ∧
        eventAt prepared.states state.pointer = some expected ∧
        state.current ≠ expected ∧
        stepper prepared state = .invalid) ∨
    (state.description = prepared.description ∧
        eventAt prepared.states state.pointer = some state.current ∧
        eventAt prepared.history state.pointer = none ∧
        state.pointer = prepared.history.length ∧
        stepper prepared state = .done) ∨
    (state.description = prepared.description ∧
        eventAt prepared.states state.pointer = some state.current ∧
        eventAt prepared.history state.pointer = none ∧
        state.pointer ≠ prepared.history.length ∧
        stepper prepared state = .invalid) ∨
    (∃ event,
        state.description = prepared.description ∧
        eventAt prepared.states state.pointer = some state.current ∧
        eventAt prepared.history state.pointer = some event ∧
        transition state.current event = none ∧
        stepper prepared state = .invalid) ∨
    (∃ event next,
        state.description = prepared.description ∧
        eventAt prepared.states state.pointer = some state.current ∧
        eventAt prepared.history state.pointer = some event ∧
        transition state.current event = some next ∧
        stepper prepared state =
          .stepped
            { description := state.description,
              pointer := state.pointer + 1,
              current := next }) := by
  by_cases hdescription : state.description = prepared.description
  · cases hcached : eventAt prepared.states state.pointer with
    | none =>
        exact Or.inr (Or.inl ⟨hdescription, rfl,
          by simp [stepper, hdescription, hcached]⟩)
    | some expected =>
        by_cases hcurrent : state.current = expected
        · subst expected
          cases hevent : eventAt prepared.history state.pointer with
          | none =>
              by_cases hpointer : state.pointer = prepared.history.length
              · have hcachedEnd :
                    eventAt prepared.states prepared.history.length =
                      some state.current := by
                  simpa [hpointer] using hcached
                exact Or.inr (Or.inr (Or.inr (Or.inl
                  ⟨hdescription, rfl, rfl, hpointer,
                    by simp [stepper, hdescription, hpointer, hcachedEnd,
                      eventAt_length]⟩)))
              · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
                  ⟨hdescription, rfl, rfl, hpointer,
                    by simp [stepper, hdescription, hcached, hevent, hpointer]⟩))))
          | some event =>
              cases htransition : transition state.current event with
              | none =>
                  exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
                    ⟨event, hdescription, rfl, rfl, htransition,
                      by simp [stepper, hdescription, hcached, hevent,
                        htransition]⟩)))))
              | some next =>
                  exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr
                    ⟨event, next, hdescription, rfl, rfl, htransition,
                      by simp [stepper, hdescription, hcached, hevent,
                        htransition]⟩)))))
        · exact Or.inr (Or.inr (Or.inl
            ⟨expected, hdescription, rfl, hcurrent,
              stepper_current_mismatch prepared state expected hdescription
                hcached hcurrent⟩))
  · exact Or.inl ⟨hdescription, by simp [stepper, hdescription]⟩

end DescribedReplay
