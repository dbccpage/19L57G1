import InstanceDemand

/-!
Stage 2: a declared procedure stores every well-formed uniform consequence.
Replay through existing admissions is proved; endogenous event production is not.
AuthorityEffect: None.
-/

namespace InstanceDemand.Closure
open Derivation

def wfInst (r : Regime) (i : Inst) : Prop :=
  i.1 < r.forms.length ∧ i.2.length = r.forms.getD i.1 0 ∧ ∀ x ∈ i.2, x < r.data

def tuples (n a : Nat) : List (List Nat) :=
  Nat.rec [[]] (fun _ previous => (List.range n).flatMap fun x => previous.map (x :: ·)) a

theorem tuples_mem (n a : Nat) (xs : List Nat) :
    xs ∈ tuples n a ↔ xs.length = a ∧ ∀ x ∈ xs, x < n := by
  induction a generalizing xs with
  | zero => change xs ∈ [[]] ↔ _; cases xs <;> simp
  | succ a ih =>
      change xs ∈ (List.range n).flatMap (fun x => (tuples n a).map (x :: ·)) ↔ _
      cases xs with
      | nil =>
          constructor
          · intro h
            rcases List.mem_flatMap.mp h with ⟨x, _, hx⟩
            rcases List.mem_map.mp hx with ⟨ys, _, he⟩
            cases he
          · intro h; have he := h.1; cases he
      | cons x xs => simp [ih, and_assoc, and_left_comm, and_comm]

def uniformEntries (r : Regime) : List Inst :=
  (List.range r.forms.length).flatMap fun f =>
    if f ∈ r.rules then (tuples r.data (r.forms.getD f 0)).map (fun xs => (f, xs)) else []

theorem uniformEntries_mem (r : Regime) (i : Inst) :
    i ∈ uniformEntries r ↔ wfInst r i ∧ i.1 ∈ r.rules := by
  rcases i with ⟨f, xs⟩
  simp only [uniformEntries, List.mem_flatMap]
  constructor
  · rintro ⟨g, hg, hi⟩
    split at hi
    · rcases List.mem_map.mp hi with ⟨ys, hy, he⟩
      cases he
      exact ⟨⟨List.mem_range.mp hg, (tuples_mem _ _ _).mp hy⟩, by assumption⟩
    · contradiction
  · rintro ⟨⟨hf, ha⟩, hr⟩
    refine ⟨f, List.mem_range.mpr hf, ?_⟩
    simp only [hr, ↓reduceIte, List.mem_map, Prod.mk.injEq, true_and]
    exact ⟨xs, (tuples_mem _ _ _).mpr ha, rfl⟩

def pending (r : Regime) : List Inst :=
  (uniformEntries r).filter fun i => decide (i ∉ r.insts)

theorem pending_mem (r : Regime) (i : Inst) :
    i ∈ pending r ↔ (wfInst r i ∧ i.1 ∈ r.rules) ∧ i ∉ r.insts := by
  simp [pending, uniformEntries_mem]

theorem pending_bound (r : Regime) : (pending r).length ≤ (uniformEntries r).length :=
  List.length_filter_le _ _

def addMany (base xs : List Inst) := xs.foldl insertNew base
def storeMany (r : Regime) (xs : List Inst) := { r with insts := addMany r.insts xs }
def events (xs : List Inst) := xs.map fun i => Event.admitInst i.1 i.2
def materialize (r : Regime) := storeMany r (pending r)

theorem addMany_mem (base xs : List Inst) (i : Inst) :
    i ∈ addMany base xs ↔ i ∈ base ∨ i ∈ xs := by
  induction xs generalizing base with
  | nil => simp [addMany]
  | cons x xs ih =>
      change i ∈ addMany (insertNew base x) xs ↔ _
      rw [ih, mem_insertNew]
      simp [or_assoc]

theorem storeMany_replay (r : Regime) (xs : List Inst)
    (hw : ∀ i ∈ xs, wfInst r i) :
    replayE (events xs) r = some (storeMany r xs) := by
  induction xs generalizing r with
  | nil => rfl
  | cons i xs ih =>
      have hi := hw i (by simp)
      have hs : stepE r (.admitInst i.1 i.2) =
          some { r with insts := insertNew r.insts i } := by
        change (if i.1 < r.forms.length ∧ i.2.length = r.forms.getD i.1 0 ∧
          (∀ x ∈ i.2, x < r.data) then some { r with insts := insertNew r.insts i }
          else none) = _
        exact if_pos hi
      rw [show events (i :: xs) = .admitInst i.1 i.2 :: events xs from rfl,
        InstanceDemand.replay_cons, hs]
      apply ih
      intro j hj
      exact hw j (by simp [hj])

theorem materialize_replay (r : Regime) :
    replayE (events (pending r)) r = some (materialize r) :=
  storeMany_replay r _ fun i hi => ((pending_mem r i).mp hi).1.1

theorem materialize_fields (r : Regime) :
    (materialize r).data = r.data ∧ (materialize r).forms = r.forms ∧
    (materialize r).rules = r.rules ∧ (materialize r).reqs = r.reqs := by
  exact ⟨rfl, rfl, rfl, rfl⟩

theorem materialize_mem (r : Regime) (i : Inst) :
    i ∈ (materialize r).insts ↔ i ∈ r.insts ∨ (wfInst r i ∧ i.1 ∈ r.rules) := by
  change i ∈ addMany r.insts (pending r) ↔ _
  rw [addMany_mem, pending_mem]
  by_cases h : i ∈ r.insts <;> simp [h]

theorem materialize_derivable (r : Regime) (i : Inst) :
    derivable (materialize r) i ↔ derivable r i := by
  simp only [derivable, materialize_mem]
  change (i ∈ r.insts ∨ wfInst r i ∧ i.1 ∈ r.rules) ∨ i.1 ∈ r.rules ↔ _
  constructor
  · rintro ((hi | ⟨_, hr⟩) | hr) <;> simp_all
  · rintro (hi | hr) <;> simp_all

theorem materialize_collapsed (r : Regime) (x y : Nat) :
    collapsed (materialize r) x y ↔ collapsed r x y := by
  unfold collapsed
  simp only [materialize_derivable]
  rfl

theorem materialize_separable (r : Regime) (x y : Nat) :
    separable (materialize r) x y ↔ separable r x y := by
  unfold separable
  simp only [materialize_derivable]
  rfl

theorem materialize_wf (r : Regime) (h : r.wf) : (materialize r).wf := by
  refine ⟨?_, h.2⟩
  intro i hi
  rcases (materialize_mem r i).mp hi with hi | ⟨hi, _⟩
  · exact h.1 i hi
  · exact hi

theorem pending_empty_after (r : Regime) : pending (materialize r) = [] := by
  cases he : pending (materialize r) with
  | nil => rfl
  | cons i xs =>
      have hi : i ∈ pending (materialize r) := by rw [he]; exact List.mem_cons_self
      rcases (pending_mem _ i).mp hi with ⟨⟨hw, hr⟩, hn⟩
      exact False.elim (hn ((materialize_mem r i).mpr (Or.inr ⟨hw, hr⟩)))

theorem materialize_idempotent (r : Regime) :
    materialize (materialize r) = materialize r := by
  unfold materialize
  rw [show pending (storeMany r (pending r)) = [] from pending_empty_after r]
  rfl

theorem events_no_impose (xs : List Inst) (x y : Nat) : .impose x y ∉ events xs := by
  simp [events]

def base (n : Nat) : Regime := ⟨n, [2], [], [0], []⟩

/-- A declared reading of stored syntax; the obligation role is not derived. -/
def readPair (r : Regime) (x y : Nat) := (0, [x,y]) ∈ r.insts ∧ x < y

theorem base_no_pair (n x y : Nat) : ¬ readPair (base n) x y := by
  simp [readPair, base]

theorem materialized_pairs (n x y : Nat) :
    readPair (materialize (base n)) x y ↔ x < y ∧ y < n := by
  unfold readPair
  rw [materialize_mem]
  constructor
  · rintro ⟨hi, hxy⟩
    rcases hi with hi | ⟨hi, _⟩
    · cases hi
    · exact ⟨hxy, hi.2.2 y (by simp)⟩
  · rintro ⟨hxy, hyn⟩
    refine ⟨Or.inr ⟨⟨by change 0 < 1; decide, rfl, ?_⟩, by simp [base]⟩, hxy⟩
    intro z hz
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hz
    rcases hz with hz | hz <;> subst z
    · exact Nat.lt_trans hxy hyn
    · exact hyn

theorem generated_pairs_unmet (n x y : Nat) :
    collapsed (materialize (base n)) x y := by
  apply (materialize_collapsed _ _ _).mpr
  exact collapsed_of_no_insts _ rfl x y

def response (x : Nat) : List Item := [.newForm 1, .newInst 1 [x]]
def responseEvents (x : Nat) : List Event := [.admitForm 1, .admitInst 1 [x]]
def answered (n x : Nat) : Regime :=
  { materialize (base n) with
    forms := [2,1]
    insts := insertNew (materialize (base n)).insts (1,[x]) }

theorem response_applies (n x : Nat) (hx : x < n) :
    applyDelta (materialize (base n)) (response x) = some (answered n x) := by
  simp [applyDelta, response, applyItem, materialize, storeMany, base, answered, hx]

theorem response_replays (n x : Nat) (hx : x < n) :
    replayE (responseEvents x) (materialize (base n)) = some (answered n x) := by
  simp [replayE, responseEvents, stepE, materialize, storeMany, base, answered, hx]

theorem answer_separates (n x y : Nat) (hne : x ≠ y) :
    separable (answered n x) x y := by
  refine ⟨⟨1, [none]⟩, ?_, ?_⟩
  · simp [wfCtx, answered, slotOk]
  · have yes : derivable (answered n x) (plug ⟨1,[none]⟩ x) := by
      apply Or.inl
      simp [answered, plug, mem_insertNew]
    have no : ¬ derivable (answered n x) (plug ⟨1,[none]⟩ y) := by
      simp only [derivable, answered, plug, mem_insertNew, materialize_mem]
      simp [wfInst, base, materialize, storeMany, Ne.symm hne]
    intro h
    exact no (h.mp yes)

theorem generated_pairs_answerable (n x y : Nat)
    (h : readPair (materialize (base n)) x y) :
    validResponse (materialize (base n)) x y (response x) := by
  have hp := (materialized_pairs n x y).mp h
  refine ⟨answered n x, response_applies n x (by omega), answer_separates n x y (by omega), ?_⟩
  simp [materialize, storeMany, base]

theorem answered_pair_still_read (n x y : Nat)
    (h : readPair (materialize (base n)) x y) : readPair (answered n x) x y := by
  refine ⟨?_, h.2⟩
  exact mem_insertNew.mpr (Or.inl h.1)

theorem replay_append (h k : List Event) (r : Regime) :
    replayE (h ++ k) r = (replayE h r).bind (replayE k) := by
  induction h generalizing r with
  | nil => rfl
  | cons e h ih =>
      simp only [List.cons_append, InstanceDemand.replay_cons]
      cases hs : stepE r e <;> simp [ih]

def seedL : List Event := [.admitDatum, .admitDatum, .admitForm 2, .admitRuleAll 0]
def seedF : List Event := [.admitDatum, .admitDatum, .admitDatum, .admitForm 2, .admitRuleAll 0]

theorem seeds_replay : replayE seedL genesis = some (base 2) ∧
    replayE seedF genesis = some (base 3) := by decide

theorem seeds_well_formed : (base 2).wf ∧ (base 3).wf := by simp [Regime.wf, base]

theorem complete_histories_replay :
    replayE (seedL ++ events (pending (base 2)) ++ responseEvents 0) genesis =
      some (answered 2 0) ∧
    replayE (seedF ++ events (pending (base 3)) ++ responseEvents 1) genesis =
      some (answered 3 1) := by
  simp only [replay_append, seeds_replay.1, seeds_replay.2, Option.bind_some,
    materialize_replay]
  exact ⟨response_replays 2 0 (by decide), response_replays 3 1 (by decide)⟩

end InstanceDemand.Closure

#print axioms InstanceDemand.Closure.tuples_mem
#print axioms InstanceDemand.Closure.uniformEntries_mem
#print axioms InstanceDemand.Closure.pending_mem
#print axioms InstanceDemand.Closure.pending_bound
#print axioms InstanceDemand.Closure.addMany_mem
#print axioms InstanceDemand.Closure.storeMany_replay
#print axioms InstanceDemand.Closure.materialize_replay
#print axioms InstanceDemand.Closure.materialize_fields
#print axioms InstanceDemand.Closure.materialize_mem
#print axioms InstanceDemand.Closure.materialize_derivable
#print axioms InstanceDemand.Closure.materialize_collapsed
#print axioms InstanceDemand.Closure.materialize_separable
#print axioms InstanceDemand.Closure.materialize_wf
#print axioms InstanceDemand.Closure.pending_empty_after
#print axioms InstanceDemand.Closure.materialize_idempotent
#print axioms InstanceDemand.Closure.events_no_impose
#print axioms InstanceDemand.Closure.base_no_pair
#print axioms InstanceDemand.Closure.materialized_pairs
#print axioms InstanceDemand.Closure.generated_pairs_unmet
#print axioms InstanceDemand.Closure.response_applies
#print axioms InstanceDemand.Closure.response_replays
#print axioms InstanceDemand.Closure.answer_separates
#print axioms InstanceDemand.Closure.generated_pairs_answerable
#print axioms InstanceDemand.Closure.answered_pair_still_read
#print axioms InstanceDemand.Closure.replay_append
#print axioms InstanceDemand.Closure.seeds_replay
#print axioms InstanceDemand.Closure.seeds_well_formed
#print axioms InstanceDemand.Closure.complete_histories_replay
