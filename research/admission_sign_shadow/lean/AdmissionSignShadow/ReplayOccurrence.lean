import Derivation.Erasure
import AdmissionSignShadow.Core

namespace AdmissionSignShadow.ReplayOccurrence

open Derivation

/-!
This lane reads the exact frozen token-aware event and replay types.  It derives
an occurrence projection from the retained `List TEvent`, never from the
deduplicated endpoint.  The occurrence projection is additional analysis of
the retained trace; it does not make occurrence history endpoint data.
-/

def projectedTokens : List TEvent → List Nat
  | [] => []
  | .supply _ :: rest => projectedTokens rest
  | .admitDatum token :: rest => token :: projectedTokens rest
  | .admitForm _ :: rest => projectedTokens rest
  | .admitInst _ _ :: rest => projectedTokens rest
  | .admitRuleAll _ :: rest => projectedTokens rest
  | .impose _ _ :: rest => projectedTokens rest

def canonicalDatumReplay (history : List TEvent) : List Nat :=
  (projectedTokens history).foldl insertToken []

def withIdsFrom : Nat → List Nat → List Occurrence
  | _, [] => []
  | next, token :: rest =>
      { id := next, token := token } :: withIdsFrom (next + 1) rest

def occurrenceReplay (history : List TEvent) : List Occurrence :=
  withIdsFrom 0 (projectedTokens history)

def emptyTRegime : TRegime := ⟨[], [], [], [], []⟩

def datumStep (tokens : List Nat) : TEvent → List Nat
  | .admitDatum token => insertToken tokens token
  | _ => tokens

def canonicalDatumReplayFrom (tokens : List Nat) (history : List TEvent) : List Nat :=
  history.foldl datumStep tokens

theorem projectedTokens_fold (history : List TEvent) (tokens : List Nat) :
    (projectedTokens history).foldl insertToken tokens =
      canonicalDatumReplayFrom tokens history := by
  induction history generalizing tokens with
  | nil => rfl
  | cons event rest ih =>
      cases event <;> simp [projectedTokens, canonicalDatumReplayFrom, datumStep, ih]

theorem stepT_tokens {state next : TRegime} {event : TEvent}
    (hstep : stepT state event = some next) :
    next.tokens = datumStep state.tokens event := by
  cases event with
  | supply token =>
      simp [stepT] at hstep
      cases hstep
      rfl
  | admitDatum token =>
      by_cases hmem : token ∈ state.tokens
      · simp [stepT, hmem] at hstep
        cases hstep
        simp [datumStep, insertToken, hmem]
      · simp [stepT, hmem] at hstep
        cases hstep
        simp [datumStep, insertToken, hmem]
  | admitForm arity =>
      by_cases hvalid : 1 ≤ arity
      · simp [stepT, hvalid] at hstep
        cases hstep
        rfl
      · simp [stepT, hvalid] at hstep
  | admitInst form args =>
      by_cases hvalid :
          form < state.forms.length ∧ args.length = state.forms.getD form 0 ∧
            ∀ datum ∈ args, datum < state.tokens.length
      · simp [stepT] at hstep
        rcases hstep with ⟨_, heq⟩
        cases heq
        rfl
      · simp [stepT] at hstep
        exact False.elim (hvalid hstep.1)
  | admitRuleAll form =>
      by_cases hvalid : form < state.forms.length
      · simp [stepT, hvalid] at hstep
        cases hstep
        rfl
      · simp [stepT, hvalid] at hstep
  | impose i j =>
      by_cases hvalid : i < j ∧ j < state.tokens.length
      · simp [stepT, hvalid] at hstep
        cases hstep
        rfl
      · simp [stepT, hvalid] at hstep

theorem replayT_tokens {history : List TEvent} {base result : TRegime}
    (hreplay : replayT history base = some result) :
    result.tokens = canonicalDatumReplayFrom base.tokens history := by
  induction history generalizing base result with
  | nil =>
      simp [replayT] at hreplay
      cases hreplay
      rfl
  | cons event rest ih =>
      rw [replayT_cons] at hreplay
      cases hstep : stepT base event with
      | none => simp [hstep] at hreplay
      | some next =>
          simp [hstep] at hreplay
          calc
            result.tokens = canonicalDatumReplayFrom next.tokens rest := ih hreplay
            _ = canonicalDatumReplayFrom (datumStep base.tokens event) rest := by
              rw [stepT_tokens hstep]
            _ = canonicalDatumReplayFrom base.tokens (event :: rest) := by rfl

def consecutiveIdsFrom : Nat → Nat → List Nat
  | _, 0 => []
  | next, count + 1 => next :: consecutiveIdsFrom (next + 1) count

theorem ids_withIdsFrom (next : Nat) (tokens : List Nat) :
    ids (withIdsFrom next tokens) = consecutiveIdsFrom next tokens.length := by
  induction tokens generalizing next with
  | nil => rfl
  | cons token rest ih =>
      change next :: ids (withIdsFrom (next + 1) rest) =
        next :: consecutiveIdsFrom (next + 1) rest.length
      rw [ih]

theorem mem_consecutiveIdsFrom_ge {next count value : Nat}
    (hmem : value ∈ consecutiveIdsFrom next count) : next ≤ value := by
  induction count generalizing next with
  | zero => simp [consecutiveIdsFrom] at hmem
  | succ count ih =>
      simp only [consecutiveIdsFrom, List.mem_cons] at hmem
      rcases hmem with rfl | htail
      · exact Nat.le_refl _
      · exact Nat.le_trans (Nat.le_succ _) (ih htail)

theorem consecutiveIdsFrom_nodup (next count : Nat) :
    (consecutiveIdsFrom next count).Nodup := by
  induction count generalizing next with
  | zero => exact List.Pairwise.nil
  | succ count ih =>
      apply List.nodup_cons.mpr
      constructor
      · intro hmem
        have hge : next + 1 ≤ next := mem_consecutiveIdsFrom_ge hmem
        exact (Nat.not_succ_le_self next) hge
      · exact ih (next := next + 1)

theorem occurrenceReplay_valid (history : List TEvent) :
    OccurrenceValid (occurrenceReplay history) := by
  unfold OccurrenceValid occurrenceReplay
  rw [ids_withIdsFrom]
  exact consecutiveIdsFrom_nodup 0 (projectedTokens history).length

def tokenCount (wanted : Nat) : List Nat → Nat
  | [] => 0
  | token :: rest => (if token = wanted then 1 else 0) + tokenCount wanted rest

def replayCount (wanted : Nat) (history : List TEvent) : Nat :=
  tokenCount wanted (projectedTokens history)

theorem countToken_withIdsFrom (wanted next : Nat) (tokens : List Nat) :
    countToken wanted (withIdsFrom next tokens) = tokenCount wanted tokens := by
  induction tokens generalizing next with
  | nil => rfl
  | cons token rest ih =>
      simp [withIdsFrom, countToken, tokenCount, ih]

theorem occurrenceReplay_count (wanted : Nat) (history : List TEvent) :
    countToken wanted (occurrenceReplay history) = replayCount wanted history := by
  exact countToken_withIdsFrom wanted 0 (projectedTokens history)

theorem fold_tokens_withIdsFrom (next : Nat) (tokens accumulator : List Nat) :
    (withIdsFrom next tokens).foldl
        (fun admitted item => insertToken admitted item.token) accumulator =
      tokens.foldl insertToken accumulator := by
  induction tokens generalizing next accumulator with
  | nil => rfl
  | cons token rest ih =>
      simp [withIdsFrom, ih]

theorem forget_occurrenceReplay_eq_canonical (history : List TEvent) :
    forgetOccurrences (occurrenceReplay history) = canonicalDatumReplay history := by
  exact fold_tokens_withIdsFrom 0 (projectedTokens history) []

theorem forget_occurrenceReplay_commutes {history : List TEvent} {result : TRegime}
    (hreplay : replayT history emptyTRegime = some result) :
    forgetOccurrences (occurrenceReplay history) = result.tokens := by
  rw [forget_occurrenceReplay_eq_canonical]
  have hreplayTokens := replayT_tokens hreplay
  rw [show canonicalDatumReplay history =
      canonicalDatumReplayFrom emptyTRegime.tokens history by
        exact projectedTokens_fold history []]
  exact hreplayTokens.symm

theorem occurrenceReplay_supply_no_op (token : Nat) (history : List TEvent) :
    occurrenceReplay (.supply token :: history) = occurrenceReplay history := by
  rfl

def renameIds (rename : Nat → Nat) (history : List Occurrence) : List Occurrence :=
  history.map (fun item => { item with id := rename item.id })

theorem countToken_renameIds (rename : Nat → Nat) (wanted : Nat)
    (history : List Occurrence) :
    countToken wanted (renameIds rename history) = countToken wanted history := by
  induction history with
  | nil => rfl
  | cons item rest ih =>
      unfold renameIds at ih ⊢
      simp [countToken, ih]

theorem fold_renameIds (rename : Nat → Nat) (history : List Occurrence)
    (accumulator : List Nat) :
    (renameIds rename history).foldl
        (fun admitted item => insertToken admitted item.token) accumulator =
      history.foldl
        (fun admitted item => insertToken admitted item.token) accumulator := by
  induction history generalizing accumulator with
  | nil => rfl
  | cons item rest ih =>
      unfold renameIds at ih ⊢
      simp [ih]

theorem forgetOccurrences_renameIds (rename : Nat → Nat)
    (history : List Occurrence) :
    forgetOccurrences (renameIds rename history) = forgetOccurrences history := by
  exact fold_renameIds rename history []

theorem ids_renameIds (rename : Nat → Nat) (history : List Occurrence) :
    ids (renameIds rename history) = (ids history).map rename := by
  induction history with
  | nil => rfl
  | cons item rest ih =>
      simp [ids, renameIds]

theorem nodup_map_injective {α β : Type} [DecidableEq α] [DecidableEq β]
    (rename : α → β) (hinjective : Function.Injective rename) :
    ∀ values : List α, values.Nodup → (values.map rename).Nodup := by
  intro values
  induction values with
  | nil => intro _; exact List.Pairwise.nil
  | cons value rest ih =>
      intro hnodup
      apply List.nodup_cons.mpr
      constructor
      · intro hmem
        obtain ⟨other, hother, heq⟩ := List.mem_map.mp hmem
        have : other = value := hinjective heq
        exact (List.nodup_cons.mp hnodup).1 (this ▸ hother)
      · exact ih (List.nodup_cons.mp hnodup).2

theorem occurrenceValid_renameIds (rename : Nat → Nat)
    (hinjective : Function.Injective rename) {history : List Occurrence}
    (hvalid : OccurrenceValid history) :
    OccurrenceValid (renameIds rename history) := by
  unfold OccurrenceValid at hvalid ⊢
  rw [ids_renameIds]
  exact nodup_map_injective rename hinjective (ids history) hvalid

def onceEvents : List TEvent := [.admitDatum 7]

def duplicateEvents : List TEvent := [.admitDatum 7, .admitDatum 7]

theorem duplicate_admission_endpoint_collision :
    replayT onceEvents emptyTRegime = replayT duplicateEvents emptyTRegime ∧
      occurrenceReplay onceEvents ≠ occurrenceReplay duplicateEvents ∧
      replayCount 7 onceEvents = 1 ∧ replayCount 7 duplicateEvents = 2 := by
  decide

theorem endpoint_does_not_determine_occurrence_count :
    ¬ ∃ recover : List Nat → Nat,
      ∀ history : List TEvent,
        recover (canonicalDatumReplay history) = replayCount 7 history := by
  rintro ⟨recover, hrecover⟩
  have hone := hrecover onceEvents
  have htwo := hrecover duplicateEvents
  have hendpoint : canonicalDatumReplay onceEvents = canonicalDatumReplay duplicateEvents := by
    decide
  have impossible : replayCount 7 onceEvents = replayCount 7 duplicateEvents := by
    exact hone.symm.trans ((congrArg recover hendpoint).trans htwo)
  exact (by decide : replayCount 7 onceEvents ≠ replayCount 7 duplicateEvents) impossible

theorem endpoint_does_not_determine_occurrence_history :
    ¬ ∃ recover : List Nat → List Occurrence,
      ∀ history : List TEvent,
        recover (canonicalDatumReplay history) = occurrenceReplay history := by
  rintro ⟨recover, hrecover⟩
  have hone := hrecover onceEvents
  have htwo := hrecover duplicateEvents
  have hendpoint : canonicalDatumReplay onceEvents = canonicalDatumReplay duplicateEvents := by
    decide
  have impossible : occurrenceReplay onceEvents = occurrenceReplay duplicateEvents := by
    exact hone.symm.trans ((congrArg recover hendpoint).trans htwo)
  exact duplicate_admission_endpoint_collision.2.1 impossible

structure AdditiveEncoding where
  encode : Nat → Int
  zero : encode 0 = 0
  additive : ∀ left right, encode (left + right) = encode left + encode right

def natScale (unit : Int) : Nat → Int
  | 0 => 0
  | count + 1 => natScale unit count + unit

theorem natScale_add (unit : Int) (left right : Nat) :
    natScale unit (left + right) = natScale unit left + natScale unit right := by
  induction right with
  | zero => simp [natScale]
  | succ right ih =>
      rw [Nat.add_succ]
      simp [natScale, ih, Int.add_assoc]

def scaledEncoding (unit : Int) : AdditiveEncoding where
  encode := natScale unit
  zero := rfl
  additive := natScale_add unit

theorem additiveEncoding_eq_scaled (encoding : AdditiveEncoding) :
    ∀ count, encoding.encode count = natScale (encoding.encode 1) count := by
  intro count
  induction count with
  | zero =>
      change encoding.encode 0 = 0
      exact encoding.zero
  | succ previous ih =>
      calc
        encoding.encode (previous + 1) =
            encoding.encode previous + encoding.encode 1 :=
          encoding.additive previous 1
        _ = natScale (encoding.encode 1) previous + encoding.encode 1 := by rw [ih]
        _ = natScale (encoding.encode 1) (previous + 1) := by rfl

theorem additive_laws_do_not_select_integer_unit :
    ¬ ∃ unit : Int, ∀ encoding : AdditiveEncoding, encoding.encode 1 = unit := by
  rintro ⟨unit, hunit⟩
  have hzero := hunit (scaledEncoding 0)
  change (0 : Int) = unit at hzero
  have hone := hunit (scaledEncoding 1)
  change (1 : Int) = unit at hone
  have impossible : (0 : Int) = 1 := hzero.trans hone.symm
  exact (by decide : (0 : Int) ≠ 1) impossible

theorem unit_calibration_is_conditional (encoding : AdditiveEncoding)
    (hunit : encoding.encode 1 = 1) :
    ∀ count, encoding.encode count = Int.ofNat count := by
  let calibration : CountCalibration := {
    encode := encoding.encode
    zero := encoding.zero
    additive := encoding.additive
    unit := hunit
  }
  exact count_calibration_unique calibration

#print axioms occurrenceReplay_valid
#print axioms occurrenceReplay_count
#print axioms forget_occurrenceReplay_commutes
#print axioms occurrenceValid_renameIds
#print axioms duplicate_admission_endpoint_collision
#print axioms endpoint_does_not_determine_occurrence_count
#print axioms endpoint_does_not_determine_occurrence_history
#print axioms additive_laws_do_not_select_integer_unit
#print axioms unit_calibration_is_conditional

end AdmissionSignShadow.ReplayOccurrence
