import BoundarySeed.Basic
import BoundarySeed.Challenge1

/-!
# Challenge 2: the caller retains `<a|>` and `<|a>`

Core Lean only.  The caller supplies and retains two opaque wholes carrying
the same visible mark, one on each side of the one admitted boundary.  The
Lean events carry no token, so the visible mark is invisible here: a `place`
always adds a fresh entry to the placement list, and a mark's internal
identity is its position in that list.  The question the visible mark raises
— whether the second whole names the first mark — is therefore a question
about the Python kernel's label-keyed admission, decided there, and the Lean
model records only what follows once two marks are placed on opposite sides.

`exchangeFirstTwo` and `exchangeMarks` are the exchange of the two internal
identities.  Under reading `U` the reflection is permitted, so the composite
of the reflection with that exchange is a permitted renaming carrying the
retained regime to itself; under `O` it is not permitted, and the theorems
below are stated for every reading with their reading-dependence named in
the prose rather than smuggled into the statement.
-/

namespace BoundarySeed

/-- The Challenge 2 caller history under the declared convention: a supply
and a placement for each retained whole.  The two supplies are the same event
value twice, separated only by their position. -/
def challenge2History : List Event := [.supply, .place false, .supply, .place true]

/-- The regime the caller's Challenge 2 history retains. -/
def retained (rd : Reading) : Regime := replay challenge2History (genesis rd)

theorem retained_eq (rd : Reading) :
    retained rd = ⟨rd, .initial, [false, true]⟩ := rfl

theorem retained_placement_length (rd : Reading) :
    (retained rd).placement.length = 2 := rfl

/-- The two supplies change nothing: dropping them leaves the same regime. -/
theorem retained_without_supplies (rd : Reading) :
    replay [.place false, .place true] (genesis rd) = retained rd := rfl

/-- The same two retentions in the other order. -/
def challenge2HistoryOtherOrder : List Event := [.supply, .place true, .supply, .place false]

def retainedOtherOrder (rd : Reading) : Regime :=
  replay challenge2HistoryOtherOrder (genesis rd)

theorem retainedOtherOrder_eq (rd : Reading) :
    retainedOtherOrder rd = ⟨rd, .initial, [true, false]⟩ := rfl

/-! ## What holds after the two retentions -/

theorem retained_onSide_zero (rd : Reading) (s : Bool) :
    holds (retained rd) (.onSide 0 s) = (s == false) := by
  rw [retained_eq]; cases s <;> rfl

theorem retained_onSide_one (rd : Reading) (s : Bool) :
    holds (retained rd) (.onSide 1 s) = (s == true) := by
  rw [retained_eq]; cases s <;> rfl

theorem retained_onSide_beyond (rd : Reading) (k : Nat) (s : Bool) :
    holds (retained rd) (.onSide (k + 2) s) = false := by
  rw [retained_eq]; simp [holds, onSide]

/-- Exactly two mark-on-side judgments hold: mark `0` on one side and mark
`1` on the other. -/
theorem retained_onSide_true_iff (rd : Reading) (i : Nat) (s : Bool) :
    holds (retained rd) (.onSide i s) = true ↔ (i = 0 ∧ s = false) ∨ (i = 1 ∧ s = true) := by
  match i with
  | 0 => rw [retained_onSide_zero]; cases s <;> simp
  | 1 => rw [retained_onSide_one]; cases s <;> simp
  | (k + 2) => rw [retained_onSide_beyond]; simp

/-- The two retained marks do not lie on the same side. -/
theorem retained_marks_differ_in_side (rd : Reading) :
    (retained rd).placement.getD 0 false ≠ (retained rd).placement.getD 1 false := by
  rw [retained_eq]; simp

/-- A side-name judgment holds after the two retentions exactly as at genesis:
none under `U`, both under `O`. -/
theorem retained_sideNamed (rd : Reading) (s : Bool) (n : Name) :
    holds (retained rd) (.sideNamed s n) = holds (genesis rd) (.sideNamed s n) :=
  replay_preserves_sideNamed _ _ _ _

theorem retained_contents_false (rd : Reading) : contents (retained rd) false = [0] := by
  rw [retained_eq]; simp [contents, List.range, List.range.loop]

theorem retained_contents_true (rd : Reading) : contents (retained rd) true = [1] := by
  rw [retained_eq]; simp [contents, List.range, List.range.loop]

/-- The two extensional side profiles differ as raw data after the two
retentions, under either reading; under `U` the difference is not invariant
under the permitted renamings, which is what `exchangeMarks_reflect_retained`
below records. -/
theorem retained_sides_differ (rd : Reading) :
    sideProfile (retained rd) false ≠ sideProfile (retained rd) true := by
  intro h
  have hm := congrArg SideProfile.marks h
  simp only [sideProfile] at hm
  rw [retained_contents_false, retained_contents_true] at hm
  exact absurd hm (by decide)

/-! ## The exchange of the two internal identities -/

/-- The exchange of the first two internal identities; every later identity
is its own image. -/
def exchangeFirstTwo (i : Nat) : Nat :=
  match i with
  | 0 => 1
  | 1 => 0
  | n + 2 => n + 2

theorem exchangeFirstTwo_involutive (i : Nat) : exchangeFirstTwo (exchangeFirstTwo i) = i := by
  match i with
  | 0 => rfl
  | 1 => rfl
  | _ + 2 => rfl

def swapFirstTwo : List Bool → List Bool
  | a :: b :: t => b :: a :: t
  | l => l

theorem swapFirstTwo_involutive (l : List Bool) : swapFirstTwo (swapFirstTwo l) = l := by
  match l with
  | [] => rfl
  | [_] => rfl
  | _ :: _ :: _ => rfl

/-- The exchange of the two internal identities, on a regime. -/
def exchangeMarks (r : Regime) : Regime :=
  ⟨r.reading, r.initialDatum, swapFirstTwo r.placement⟩

theorem exchangeMarks_involutive (r : Regime) : exchangeMarks (exchangeMarks r) = r := by
  cases r with
  | mk rd d p =>
    show Regime.mk rd d (swapFirstTwo (swapFirstTwo p)) = Regime.mk rd d p
    rw [swapFirstTwo_involutive]

/-- The reflection followed by the exchange of the two internal identities
carries the retained regime to itself.  Under `U` the reflection is a
permitted renaming, so the composite is a permitted renaming of the reading;
under `O` it is not. -/
theorem exchangeMarks_reflect_retained (rd : Reading) :
    exchangeMarks (reflect (retained rd)) = retained rd := rfl

/-- Neither half of the composite fixes the retained regime on its own: the
reflection alone moves it. -/
theorem reflect_retained_ne (rd : Reading) : reflect (retained rd) ≠ retained rd := by
  rw [retained_eq]
  intro h
  simp [reflect] at h

/-- Nor does the exchange of the two internal identities alone. -/
theorem exchangeMarks_retained_ne (rd : Reading) : exchangeMarks (retained rd) ≠ retained rd := by
  rw [retained_eq]
  intro h
  simp [exchangeMarks, swapFirstTwo] at h

/-- Retaining the two wholes in the other order gives the exchange of the
two internal identities. -/
theorem retainedOtherOrder_is_exchange (rd : Reading) :
    retainedOtherOrder rd = exchangeMarks (retained rd) := rfl

/-- The two orders give different raw regimes; that they are the same up to a
permitted renaming under both readings is the Python computation, and is what
makes the order of the two retentions internally unavailable. -/
theorem retainedOtherOrder_ne_retained (rd : Reading) :
    retainedOtherOrder rd ≠ retained rd := by
  rw [retainedOtherOrder_is_exchange]
  exact exchangeMarks_retained_ne rd

/-- Under `U` the composite that fixes the retained regime uses a renaming
the reading permits. -/
theorem retained_composite_permitted_U :
    reflectionPermitted .U ∧ exchangeMarks (reflect (retained .U)) = retained .U :=
  ⟨reflection_permitted_U, exchangeMarks_reflect_retained .U⟩

/-! ## What the exchange transports, and what it does not -/

/-- The composite carries every mark-on-side judgment of one retained mark to
the corresponding judgment of the other, with the side exchanged.  Under `U`,
where the composite is a permitted renaming, this is why no mark property
invariant under permitted renamings separates the two marks; under `O` the
composite is not permitted and the statement transports nothing. -/
theorem retained_exchange_transports (rd : Reading) (i : Nat) (s : Bool) :
    holds (retained rd) (.onSide (exchangeFirstTwo i) (!s))
      = holds (retained rd) (.onSide i s) := by
  match i with
  | 0 =>
    show holds (retained rd) (.onSide 1 (!s)) = holds (retained rd) (.onSide 0 s)
    rw [retained_onSide_zero, retained_onSide_one]; cases s <;> rfl
  | 1 =>
    show holds (retained rd) (.onSide 0 (!s)) = holds (retained rd) (.onSide 1 s)
    rw [retained_onSide_zero, retained_onSide_one]; cases s <;> rfl
  | (k + 2) =>
    show holds (retained rd) (.onSide (k + 2) (!s)) = holds (retained rd) (.onSide (k + 2) s)
    rw [retained_onSide_beyond, retained_onSide_beyond]

/-- Without the side exchange the two retained marks are told apart by a
single judgment form: one lies on the side the other does not.  Under `O`,
where the reflection is not permitted, this is the separation; under `U` the
composite above carries it away. -/
theorem retained_marks_separated_by_a_side (rd : Reading) :
    holds (retained rd) (.onSide 0 false) = true ∧
      holds (retained rd) (.onSide 1 false) = false := by
  constructor
  · rw [retained_onSide_zero]; rfl
  · rw [retained_onSide_one]; rfl

/-! ## Retention, inertia, and what no event changes -/

/-- Each retained mark's judgment survives every later event and history of
the Lean grammar. -/
theorem retained_judgments_survive (rd : Reading) (h : List Event) (i : Nat) (s : Bool)
    (hi : i < 2) :
    holds (replay h (retained rd)) (.onSide i s) = holds (retained rd) (.onSide i s) :=
  replay_preserves_onSide h (retained rd) i s hi

theorem retained_reading (rd : Reading) : (retained rd).reading = rd :=
  replay_reading _ _

theorem retained_initialDatum (rd : Reading) : (retained rd).initialDatum = .initial :=
  replay_initialDatum _ _

/-- No event follows from the retained regime in the declared relation. -/
theorem no_event_follows_retained (rd : Reading) (e : Event) :
    ¬ EventFollows (retained rd) e :=
  no_event_follows _ _

end BoundarySeed
