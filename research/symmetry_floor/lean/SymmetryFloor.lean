/-
  SymmetryFloor.lean -- a start that every renaming leaves alone stays that way.

  Core Lean 4.  No mathlib.  The reports at the foot record what each result
  leans on; this comment does not name the tokens the repository scan reads,
  because that scan reads comments as text.

  WHAT THE FIRST THEOREM DOES NOT ASSUME

    * `G` is not a group.  No associativity, no identity, no inverses.
    * `act` is not an action.  No `act 1 x = x`, no composition law.
    * `X` is not the glyph carrier, or finite, or anything at all.

  So it is not a statement about inscriptions, or about one carrier, or about a
  choice of start.  It holds for any notion of state and any notion of renaming.
  Changing the start cannot escape it, because the start never entered.

  What it DOES assume is the single thing the programme took for granted:
  `f` is a FUNCTION.  One state in, one state out.
-/

namespace SymmetryFloor

/--
  **A rule that reads only the state cannot break what the state already holds.**

  `agrees` says `f` cannot see whatever `act g` renames: rename the input and the
  output is renamed to match.  That is what "computed from the state alone, with
  no reading of which glyph is which and no outside choice" amounts to.

  Then any `g` that already left the state alone leaves the successor alone.
-/
theorem floor {G X : Type} (act : G → X → X) (f : X → X)
    (agrees : ∀ g x, f (act g x) = act g (f x))
    (g : G) (s : X) (still : act g s = s) :
    act g (f s) = f s := by
  rw [← agrees, still]

/-- Running the rule any finite number of times changes nothing about this. -/
def iter {X : Type} (f : X → X) : Nat → X → X
  | 0, x => x
  | n + 1, x => iter f n (f x)

theorem floor_iterated {G X : Type} (act : G → X → X) (f : X → X)
    (agrees : ∀ g x, f (act g x) = act g (f x))
    (g : G) :
    ∀ (n : Nat) (s : X), act g s = s → act g (iter f n s) = iter f n s := by
  intro n
  induction n with
  | zero => intro s still; exact still
  | succ k ih =>
      intro s still
      exact ih (f s) (floor act f agrees g s still)

/--
  **The exit is real, and it is exactly the loss of single-valuedness.**

  A step that offers a SET need only offer a set carried to itself.  Its members
  need not be carried to themselves.  Below, `swap` leaves `0` alone -- a start
  every renaming holds still -- while the set `{1, 2}` is carried to itself and
  neither member is.

  Nothing selects between `1` and `2`.  There is no fact about which.  That is
  not a defect in the rule; it is what breaking a symmetry costs when there is no
  outside to do the selecting.
-/
def swap : Fin 3 → Fin 3
  | 0 => 0
  | 1 => 2
  | 2 => 1

/-- The start is held still. -/
theorem start_still : swap 0 = 0 := by decide

/-- The offered set is carried to itself. -/
theorem offered_set_carried :
    ∀ y : Fin 3, (y = 1 ∨ y = 2) ↔ (swap y = 1 ∨ swap y = 2) := by decide

/-- Neither member of it is. -/
theorem members_move : swap 1 ≠ 1 ∧ swap 2 ≠ 2 := by decide

/--
  And the price, here at its smallest: the set that breaks the renaming has two
  members, and no one-member set does.  A one-member offer is a function, and
  `floor` already forbids it.
-/
theorem price_is_two :
    ∀ y : Fin 3, swap y = y → ¬(y = 1 ∨ y = 2) := by decide

end SymmetryFloor

-- Run: lean SymmetryFloor.lean
#print axioms SymmetryFloor.floor
#print axioms SymmetryFloor.floor_iterated
#print axioms SymmetryFloor.start_still
#print axioms SymmetryFloor.offered_set_carried
#print axioms SymmetryFloor.members_move
#print axioms SymmetryFloor.price_is_two
