import BoundarySeed.Basic
import BoundarySeed.Challenge1
import BoundarySeed.Challenge2
import BoundarySeed.Challenge3

/-!
# Challenge 4: two wholes with a mark on each side of the boundary

Core Lean only.  The caller supplies and retains two opaque wholes, each
carrying one mark on each side of the one admitted boundary, and requires the
two wholes to be internally separable.  The Lean events carry no token and a
regime carries no grouping of marks into wholes, so what the model records is
the placement alone; which marks the caller's first whole contributed is a
question about the Python kernel's histories, decided there and priced there.

This file closes three things the Python enumeration cannot close on its own.

The first is the obstruction itself.  `exchangeWholesRegime` — the exchange of
the first two internal identities with the next two — carries the retained
regime onto itself, and it uses **no side exchange**.  That is why the
requirement fails under BOTH readings here, where at Challenge 3 the O reading
already met it: the withdrawal that reading O carries touches the side
exchange and leaves this map alone.

The second is the whole family of candidates that only add judgment forms:
`no_invariant_pair_property_separates_the_wholes` is stated for an ARBITRARY
property of a regime and an ordered pair of internal identities, so it covers
every form the closed grammar might gain.  Its hypothesis is a real
restriction, which `firstIsMarkZero_is_not_invariant_under_the_whole_exchange`
exhibits, and the property outside it is exactly the one that reads an
admission index — the Python enumeration's one minimum under reading U.

The third is stronger than anything the enumeration reaches:
`whole_exchange_survives_every_continuation` shows that the map still carries
the regime onto itself after ANY later history of the Lean grammar, however
many further marks are placed.  The Challenge 3 counting argument, which ruled
the side exchange out once the two sides carried different numbers of marks,
says nothing about it: `crossRetained_counts_equal` records that the two
counts are equal here, and the exchange is not the side exchange in any case.
-/

namespace BoundarySeed

/-- The Challenge 4 caller history under the declared convention and the
declared within-whole order: for each retained whole, a supply for each of its
marks and then a placement for each, the left mark first. -/
def challenge4History : List Event :=
  [.supply, .supply, .place false, .place true,
   .supply, .supply, .place false, .place true]

/-- The regime the caller's Challenge 4 history retains. -/
def crossRetained (rd : Reading) : Regime := replay challenge4History (genesis rd)

theorem crossRetained_eq (rd : Reading) :
    crossRetained rd = ⟨rd, .initial, [false, true, false, true]⟩ := rfl

/-- The placement alone, with the reading projected away, so that a decision
procedure is offered a goal with no free variable in it. -/
theorem crossRetained_placement (rd : Reading) :
    (crossRetained rd).placement = [false, true, false, true] := rfl

theorem crossRetained_placement_length (rd : Reading) :
    (crossRetained rd).placement.length = 4 := rfl

/-! ## What holds after the four placements -/

theorem crossRetained_onSide_zero (rd : Reading) (s : Bool) :
    holds (crossRetained rd) (.onSide 0 s) = (s == false) := by
  rw [crossRetained_eq]; cases s <;> rfl

theorem crossRetained_onSide_one (rd : Reading) (s : Bool) :
    holds (crossRetained rd) (.onSide 1 s) = (s == true) := by
  rw [crossRetained_eq]; cases s <;> rfl

theorem crossRetained_onSide_two (rd : Reading) (s : Bool) :
    holds (crossRetained rd) (.onSide 2 s) = (s == false) := by
  rw [crossRetained_eq]; cases s <;> rfl

theorem crossRetained_onSide_three (rd : Reading) (s : Bool) :
    holds (crossRetained rd) (.onSide 3 s) = (s == true) := by
  rw [crossRetained_eq]; cases s <;> rfl

theorem crossRetained_onSide_beyond (rd : Reading) (k : Nat) (s : Bool) :
    holds (crossRetained rd) (.onSide (k + 4) s) = false := by
  rw [crossRetained_eq]; simp [holds, onSide]

/-- Exactly four mark-on-side judgments hold: the first and third marks on one
side, the second and fourth on the other. -/
theorem crossRetained_onSide_true_iff (rd : Reading) (i : Nat) (s : Bool) :
    holds (crossRetained rd) (.onSide i s) = true ↔
      ((i = 0 ∨ i = 2) ∧ s = false) ∨ ((i = 1 ∨ i = 3) ∧ s = true) := by
  match i with
  | 0 => rw [crossRetained_onSide_zero]; cases s <;> simp
  | 1 => rw [crossRetained_onSide_one]; cases s <;> simp
  | 2 => rw [crossRetained_onSide_two]; cases s <;> simp
  | 3 => rw [crossRetained_onSide_three]; cases s <;> simp
  | (k + 4) => rw [crossRetained_onSide_beyond]; simp

/-- **The boundary does not separate two marks that share a side.**  The first
and third retained marks satisfy exactly the same mark-on-side judgments, and
one is the caller's first whole's mark and the other the second's.  At
Challenge 3 the two retained marks lay on different sides and this judgment
form told them apart; here it does not. -/
theorem crossRetained_marks_share_a_side (rd : Reading) (s : Bool) :
    holds (crossRetained rd) (.onSide 0 s) = holds (crossRetained rd) (.onSide 2 s) := by
  rw [crossRetained_onSide_zero, crossRetained_onSide_two]

/-- The same of the OTHER pair that shares a side: the second and fourth
retained marks satisfy exactly the same mark-on-side judgments, and again one
is the caller's first whole's mark and the other the second's.  Both pairs are
stated, because the sentence the paper draws from them is about both. -/
theorem crossRetained_other_marks_share_a_side (rd : Reading) (s : Bool) :
    holds (crossRetained rd) (.onSide 1 s) = holds (crossRetained rd) (.onSide 3 s) := by
  rw [crossRetained_onSide_one, crossRetained_onSide_three]

/-- A side-name judgment holds after the four placements exactly as at genesis:
none under `U`, both under `O`. -/
theorem crossRetained_sideNamed (rd : Reading) (s : Bool) (n : Name) :
    holds (crossRetained rd) (.sideNamed s n) = holds (genesis rd) (.sideNamed s n) :=
  replay_preserves_sideNamed _ _ _ _

/-! ## The exchange of the two wholes -/

/-- The exchange of the two retained wholes, on internal identities: the first
whole's marks are `0` and `1`, the second whole's are `2` and `3`, and every
later identity is its own image. -/
def exchangeWholes (i : Nat) : Nat :=
  match i with
  | 0 => 2
  | 1 => 3
  | 2 => 0
  | 3 => 1
  | n + 4 => n + 4

theorem exchangeWholes_involutive (i : Nat) : exchangeWholes (exchangeWholes i) = i := by
  match i with
  | 0 => rfl
  | 1 => rfl
  | 2 => rfl
  | 3 => rfl
  | _ + 4 => rfl

theorem exchangeWholes_zero : exchangeWholes 0 = 2 := rfl

theorem exchangeWholes_one : exchangeWholes 1 = 3 := rfl

/-- It carries the first whole's marks onto the second whole's. -/
theorem exchangeWholes_carries_the_first_whole :
    exchangeWholes 0 = 2 ∧ exchangeWholes 1 = 3 := ⟨rfl, rfl⟩

/-- Its action on a placement list: the first two entries and the next two are
exchanged, and every later entry is fixed. -/
def swapWholes : List Bool → List Bool
  | a :: b :: c :: d :: t => c :: d :: a :: b :: t
  | l => l

theorem swapWholes_involutive (l : List Bool) : swapWholes (swapWholes l) = l := by
  match l with
  | [] => rfl
  | [_] => rfl
  | [_, _] => rfl
  | [_, _, _] => rfl
  | _ :: _ :: _ :: _ :: _ => rfl

/-- Its action on a regime. -/
def exchangeWholesRegime (r : Regime) : Regime :=
  ⟨r.reading, r.initialDatum, swapWholes r.placement⟩

theorem exchangeWholesRegime_involutive (r : Regime) :
    exchangeWholesRegime (exchangeWholesRegime r) = r := by
  cases r with
  | mk rd d p =>
    show Regime.mk rd d (swapWholes (swapWholes p)) = Regime.mk rd d p
    rw [swapWholes_involutive]

/-- **The obstruction, and it uses no side exchange.**  The exchange of the two
wholes carries the retained regime onto itself under either reading, so the
withdrawal of the side exchange that reading O carries does not touch it: this
is why the requirement fails under both readings at this rung. -/
theorem exchangeWholesRegime_crossRetained (rd : Reading) :
    exchangeWholesRegime (crossRetained rd) = crossRetained rd := rfl

/-- The side exchange alone does not fix the retained regime, so the
obstruction is not it. -/
theorem reflect_crossRetained_ne (rd : Reading) :
    reflect (crossRetained rd) ≠ crossRetained rd := by
  rw [crossRetained_eq]
  intro h
  simp [reflect] at h

/-- Nor does the exchange of the first two internal identities, which is the
map that carried the Challenge 2 retention onto itself: it is the exchange of
the two WHOLES that does the work here. -/
theorem exchangeMarks_crossRetained_ne (rd : Reading) :
    exchangeMarks (crossRetained rd) ≠ crossRetained rd := by
  rw [crossRetained_eq]
  intro h
  simp [exchangeMarks, swapFirstTwo] at h

/-! ## What no addition of judgment forms can do -/

/-- **No property of a pair of marks that the whole exchange leaves alone
separates the two retained wholes.**  `P` ranges over every property of a
regime and an ordered pair of internal identities, so this covers every
judgment form the closed grammar might gain and not only the ones the Python
space enumerates. -/
theorem no_invariant_pair_property_separates_the_wholes
    (rd : Reading) (P : Regime → Nat → Nat → Bool)
    (hinv : ∀ (r : Regime) (i j : Nat),
      P (exchangeWholesRegime r) (exchangeWholes i) (exchangeWholes j) = P r i j) :
    P (crossRetained rd) 0 1 = P (crossRetained rd) 2 3 := by
  have h := hinv (crossRetained rd) 0 1
  rw [exchangeWholesRegime_crossRetained, exchangeWholes_zero, exchangeWholes_one] at h
  exact h.symm

/-- The same for a property of a single mark: nothing the exchange leaves alone
tells the first retained mark from the third.  That is the mark-level form of
the theorem above, and the two marks it names are the ones that share a side. -/
theorem no_invariant_mark_property_separates_the_paired_marks
    (rd : Reading) (P : Regime → Nat → Bool)
    (hinv : ∀ (r : Regime) (i : Nat),
      P (exchangeWholesRegime r) (exchangeWholes i) = P r i) :
    P (crossRetained rd) 0 = P (crossRetained rd) 2 := by
  have h := hinv (crossRetained rd) 0
  rw [exchangeWholesRegime_crossRetained, exchangeWholes_zero] at h
  exact h.symm

/-- The property of a pair of marks that reads whether the first of them is the
first admitted mark.  It reads an admission index, which is a metatheoretic
name and not a judgment of the closed grammar. -/
def firstIsMarkZero (_r : Regime) (i _j : Nat) : Bool := decide (i = 0)

/-- It separates the two retained wholes. -/
theorem firstIsMarkZero_separates_the_wholes (r : Regime) :
    firstIsMarkZero r 0 1 ≠ firstIsMarkZero r 2 3 := by
  simp [firstIsMarkZero]

/-- So the hypothesis above is a real restriction and not a vacuous one: this
property lies outside it.  It is exactly the property the Python enumeration's
one minimum under reading U makes available, by declaring the admission index
to be internally available. -/
theorem firstIsMarkZero_is_not_invariant_under_the_whole_exchange :
    ¬ (∀ (r : Regime) (i j : Nat),
        firstIsMarkZero (exchangeWholesRegime r) (exchangeWholes i) (exchangeWholes j)
          = firstIsMarkZero r i j) := by
  intro h
  have h0 := h (crossRetained .U) 0 1
  simp [firstIsMarkZero, exchangeWholes] at h0

/-! ## What the counting argument does not reach -/

/-- The two sides carry equally many marks, so the Challenge 3 counting
argument says nothing here.  There, unequal counts ruled the side exchange out
of every renaming that fixes the regime; here the counts are equal, and the
obstruction is not the side exchange in any case. -/
theorem crossRetained_counts_equal (rd : Reading) :
    countOn (crossRetained rd).placement false
      = countOn (crossRetained rd).placement true := by
  rw [crossRetained_placement]
  decide

/-! ## What no continuation can do -/

/-- Replaying any history appends to the placement. -/
theorem replay_placement_append (h : List Event) (base : Regime) :
    ∃ suffix, (replay h base).placement = base.placement ++ suffix := by
  induction h generalizing base with
  | nil => exact ⟨[], (List.append_nil _).symm⟩
  | cons e t ih =>
    obtain ⟨s, hs⟩ := ih (step base e)
    cases e with
    | supply => exact ⟨s, hs⟩
    | place b =>
      refine ⟨b :: s, ?_⟩
      show (replay t (step base (.place b))).placement = base.placement ++ (b :: s)
      rw [hs]
      show (base.placement ++ [b]) ++ s = base.placement ++ (b :: s)
      simp

/-- A regime whose placement begins with the retained one is carried onto
itself by the whole exchange. -/
theorem exchangeWholesRegime_of_prefix (r : Regime) (t : List Bool)
    (h : r.placement = false :: true :: false :: true :: t) :
    exchangeWholesRegime r = r := by
  cases r with
  | mk rd d p =>
    have hp : p = false :: true :: false :: true :: t := h
    subst hp
    rfl

/-- **No continuation ever separates the two retained wholes.**  Whatever
history follows — any number of further supplies and placements, the
further-mark candidate of the declared space among them — the whole exchange
still carries the regime onto itself, so the obstruction is still there.  This
is stronger than the enumeration, which reaches one further mark. -/
theorem whole_exchange_survives_every_continuation (rd : Reading) (h : List Event) :
    exchangeWholesRegime (replay h (crossRetained rd)) = replay h (crossRetained rd) := by
  obtain ⟨s, hs⟩ := replay_placement_append h (crossRetained rd)
  rw [crossRetained_placement] at hs
  exact exchangeWholesRegime_of_prefix _ s hs

/-- In particular one further mark on either side, which was a minimum at
Challenge 3, does not meet the requirement here. -/
theorem whole_exchange_survives_a_further_mark (rd : Reading) (s : Bool) :
    exchangeWholesRegime (step (crossRetained rd) (.place s))
      = step (crossRetained rd) (.place s) :=
  whole_exchange_survives_every_continuation rd [.place s]

/-! ## Retention and inertia -/

/-- Each retained mark's judgment survives every later history of the Lean
grammar. -/
theorem crossRetained_judgments_survive (rd : Reading) (h : List Event) (i : Nat) (t : Bool)
    (hi : i < 4) :
    holds (replay h (crossRetained rd)) (.onSide i t)
      = holds (crossRetained rd) (.onSide i t) := by
  have hlen : i < (crossRetained rd).placement.length := by
    rw [crossRetained_placement_length]; exact hi
  exact replay_preserves_onSide h (crossRetained rd) i t hlen

theorem crossRetained_reading (rd : Reading) : (crossRetained rd).reading = rd :=
  replay_reading _ _

theorem crossRetained_initialDatum (rd : Reading) :
    (crossRetained rd).initialDatum = .initial :=
  replay_initialDatum _ _

/-- No event follows from the retained regime in the declared relation. -/
theorem no_event_follows_crossRetained (rd : Reading) (e : Event) :
    ¬ EventFollows (crossRetained rd) e :=
  no_event_follows _ _

end BoundarySeed
