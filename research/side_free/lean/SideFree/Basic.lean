/-
The side-free carrier, re-declared in Lean.

This is a Lean re-declaration of the same carrier the Python kernel carries,
and the theorems below are about these declarations.  Two differences are
recorded here rather than left for a reader to discover.

* The Lean carrier carries no refusals.  Every refusal of the Python carrier
  -- an admission whose token was never presented, a label-keyed admission of
  a label that names more than one mark -- is a Python-side declaration about
  well-formed histories.  ``step`` here is total.
* Presentation tokens are plain strings here and the presentation layer is
  absent, because it reaches nothing in the carrier in either language.

Classification: every declaration in this file is a DERIVED DEFINITION or a
PROVED THEOREM.  Nothing here is asserted.
-/

namespace SideFree

/-- Admitted state: the labels of the admitted marks, in admission order.
A mark's internal identity is its position; the entry beside it is a
presentation label and need not be unique. -/
structure Regime where
  marks : List String
  deriving DecidableEq, Repr

/-- The regime before any admission. -/
def genesis : Regime := ⟨[]⟩

/-- The event grammar, with the pinned carrier's side argument removed. -/
inductive Event where
  /-- External presentation.  Not an admission. -/
  | supply (token : String)
  /-- Label-keyed admission: a no-op when the label already names a mark. -/
  | admitMark (token : String)
  /-- Admission of one presented occurrence as a fresh mark. -/
  | admitOccurrence (token : String)
  deriving DecidableEq, Repr

/-- Whether an event is one of the two that can change admitted state. -/
def Event.isAdmission : Event → Bool
  | .supply _ => false
  | .admitMark _ => true
  | .admitOccurrence _ => true

/-- Apply one event to admitted state. -/
def step (r : Regime) : Event → Regime
  | .supply _ => r
  | .admitMark t => if r.marks.contains t then r else ⟨r.marks ++ [t]⟩
  | .admitOccurrence t => ⟨r.marks ++ [t]⟩

/-- Rebuild a regime from an event list. -/
def replay (base : Regime) : List Event → Regime
  | [] => base
  | e :: es => replay (step base e) es

/-- The object-language transition relation is empty: no event is entailed by
admitted state. -/
def eventFollows (_r : Regime) (_e : Event) : Bool := false

/-- The number of admitted marks. -/
def Regime.size (r : Regime) : Nat := r.marks.length

/-- The one positive judgment form of the closed observation grammar. -/
def admittedJudgment (r : Regime) (mark : Nat) : Bool := mark < r.size

/-! ## The presentation event changes nothing -/

/-- A presentation event leaves admitted state exactly as it was. -/
theorem supply_no_op (r : Regime) (t : String) : step r (.supply t) = r := rfl

/-- Replaying only presentation events leaves the base regime. -/
theorem replay_supply_inert (r : Regime) :
    ∀ ts : List String, replay r (ts.map Event.supply) = r := by
  intro ts
  induction ts generalizing r with
  | nil => rfl
  | cons t rest ih => simpa [replay, step] using ih r

/-! ## State changes only by an admission event -/

/-- If an event changed admitted state, it was an admission. -/
theorem step_changes_only_by_admission (r : Regime) (e : Event) :
    step r e ≠ r → e.isAdmission = true := by
  cases e with
  | supply t => intro h; exact absurd rfl h
  | admitMark t => intro _; rfl
  | admitOccurrence t => intro _; rfl

/-- A presentation event is never an admission. -/
theorem supply_is_not_an_admission (t : String) :
    (Event.supply t).isAdmission = false := rfl

/-- An occurrence admission appends exactly one mark. -/
theorem admitOccurrence_appends (r : Regime) (t : String) :
    (step r (.admitOccurrence t)).marks = r.marks ++ [t] := rfl

/-- An occurrence admission raises the mark count by exactly one. -/
theorem admitOccurrence_size (r : Regime) (t : String) :
    (step r (.admitOccurrence t)).size = r.size + 1 := by
  simp [step, Regime.size]

/-- A label-keyed admission of a label already present is a no-op. -/
theorem admitMark_no_op (r : Regime) (t : String) (h : r.marks.contains t = true) :
    step r (.admitMark t) = r := by
  show (if r.marks.contains t = true then r else ⟨r.marks ++ [t]⟩) = r
  rw [h]
  rfl

/-! ## Replay -/

/-- Replay is deterministic in the sense that has content: it is a function of
the base and the ADMISSION subsequence alone.  Deleting every presentation
event from a history leaves the replay unchanged, so two histories that carry
the same admissions in the same order and differ only in how presentations are
interleaved reach the same regime. -/
theorem replay_deterministic (base : Regime) (h : List Event) :
    replay base (h.filter Event.isAdmission) = replay base h := by
  induction h generalizing base with
  | nil => rfl
  | cons e rest ih =>
    cases e with
    | supply t => simpa [List.filter, Event.isAdmission, replay, step] using ih base
    | admitMark t =>
        simpa [List.filter, Event.isAdmission, replay] using
          ih (step base (.admitMark t))
    | admitOccurrence t =>
        simpa [List.filter, Event.isAdmission, replay] using
          ih (step base (.admitOccurrence t))

/-- Replay of a longer history is replay of the prefix, continued. -/
theorem replay_append (base : Regime) (xs ys : List Event) :
    replay base (xs ++ ys) = replay (replay base xs) ys := by
  induction xs generalizing base with
  | nil => rfl
  | cons e rest ih => simpa [replay] using ih (step base e)

/-- Genesis admits nothing. -/
theorem genesis_size : genesis.size = 0 := rfl

/-- The observation grammar has an empty extension at genesis. -/
theorem no_judgment_at_genesis (mark : Nat) : admittedJudgment genesis mark = false := by
  simp [admittedJudgment, genesis, Regime.size]

/-- No event is entailed by admitted state. -/
theorem no_event_follows (r : Regime) (e : Event) : eventFollows r e = false := rfl

/-! ## The caller's retained regime, from genesis -/

/-- The caller's history: two presentations and two occurrence admissions. -/
def callerHistory : List Event :=
  [.supply "a", .admitOccurrence "a", .supply "a", .admitOccurrence "a"]

/-- The retained regime: two marks carrying the same label. -/
def retained : Regime := ⟨["a", "a"]⟩

/-- The retained regime is the replay of the caller's history from genesis. -/
theorem retained_replays_from_genesis : replay genesis callerHistory = retained := rfl

/-- The retained regime carries two marks. -/
theorem retained_size : retained.size = 2 := rfl

/-- Both retained marks are admitted; a third is not. -/
theorem retained_judgments :
    admittedJudgment retained 0 = true ∧
    admittedJudgment retained 1 = true ∧
    admittedJudgment retained 2 = false := by
  refine ⟨rfl, rfl, rfl⟩

/-- The retained regime under the shared identity policy carries ONE mark, so
the requirement has no subject there.  This is a refusal of the subject and
never a false. -/
theorem shared_policy_retains_one_mark :
    replay genesis [.supply "a", .admitMark "a", .supply "a", .admitMark "a"]
      = ⟨["a"]⟩ := rfl

end SideFree
