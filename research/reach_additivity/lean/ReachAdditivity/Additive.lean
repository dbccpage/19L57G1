/-!
# What additivity along composition buys, and what it costs

The instruction this rung answers asked whether a base-relative cost is
additive along composition, on the stated ground that additivity would give
the estate a price for a sequence of moves rather than a re-measurement.

The answer is yes, for a whole class of costs and not just one, and the
consequence is not the one the question expected.  A cost of the form

    diff P s d  =  P (apply s d) - P s

is additive along composition, and its total along a sequence of moves
**telescopes to the endpoints**.  So it is path-independent, and its total
around any closed walk is zero.  A cost with zero circulation on every
closed walk carries no obstruction: obstruction is precisely the part of a
cost that is not a difference of a state functional, and a difference cost
has no such part by construction.

The counterweight is in the same file.  The sealed item count is additive
along composition too -- the length of a concatenation is the sum of the
lengths -- so **additivity does not distinguish the two costs at all**.  It
is not the property the question wanted.  What separates them is exactly
what the last section proves: on a state carrying an absorbing move, the
item count is nonzero around a closed walk, so no state functional has the
item count as its difference.

Nothing here is about the sealed grammar in particular.  The state, the
one-item action and the functional are abstract; the sealed grammar supplies
one instance of the hypothesis, and `survey.py` checks that instance over a
declared rectangle.

Core Lean only: no `Mathlib`, no choice principle, no proof left incomplete.
`AuthorityEffect: None.`
-/

namespace ReachAdditivity

variable {S I : Type}

/-! ## 1. An abstract action of item sequences on states -/

/-- Apply a sequence of items one at a time, left to right. -/
def actList (step : S → I → S) : S → List I → S
  | s, [] => s
  | s, i :: rest => actList step (step s i) rest

theorem actList_nil (step : S → I → S) (s : S) : actList step s [] = s := rfl

theorem actList_cons (step : S → I → S) (s : S) (i : I) (rest : List I) :
    actList step s (i :: rest) = actList step (step s i) rest := rfl

/-- **The action is sequential.**  Applying a composite is applying the
parts in order.  This is prior to every cost question and is a fact about
the action, not about any measure. -/
theorem actList_append (step : S → I → S) (d : List I) :
    ∀ (s : S) (e : List I),
      actList step s (d ++ e) = actList step (actList step s d) e := by
  induction d with
  | nil => intro s e; rfl
  | cons i rest ih =>
      intro s e
      show actList step (step s i) (rest ++ e) = _
      exact ih (step s i) e

/-! ## 2. Difference costs, and additivity -/

/-- A difference cost: the change a response makes in a state functional.
Signed, so nothing here assumes the functional grows. -/
def diff (P : S → Int) (step : S → I → S) (s : S) (d : List I) : Int :=
  P (actList step s d) - P s

/-- **Additivity, for every difference cost.**  No property of the
functional is used: it follows from sequential action and one cancellation.
So additivity is not evidence that a particular cost is well chosen -- every
cost of this shape has it. -/
theorem diff_additive (P : S → Int) (step : S → I → S) (s : S) (d e : List I) :
    diff P step s (d ++ e)
      = diff P step s d + diff P step (actList step s d) e := by
  show P (actList step s (d ++ e)) - P s
      = (P (actList step s d) - P s)
        + (P (actList step (actList step s d) e) - P (actList step s d))
  rw [actList_append]
  omega

/-! ## 3. Paths, telescoping, and zero circulation -/

/-- Where a sequence of moves lands. -/
def pathEnd (step : S → I → S) : S → List (List I) → S
  | s, [] => s
  | s, m :: rest => pathEnd step (actList step s m) rest

/-- The total cost along a sequence of moves, summed step by step --
deliberately not computed from the endpoints, so that the telescoping below
is a result and not a definition. -/
def pathTotal (P : S → Int) (step : S → I → S) : S → List (List I) → Int
  | _, [] => 0
  | s, m :: rest => diff P step s m + pathTotal P step (actList step s m) rest

/-- **Telescoping.**  The step-by-step total equals the functional's value
at the end minus its value at the start.  Everything in between cancels. -/
theorem pathTotal_eq (P : S → Int) (step : S → I → S) (ms : List (List I)) :
    ∀ s : S, pathTotal P step s ms = P (pathEnd step s ms) - P s := by
  induction ms with
  | nil => intro s; show (0 : Int) = P s - P s; omega
  | cons m rest ih =>
      intro s
      show diff P step s m + pathTotal P step (actList step s m) rest
          = P (pathEnd step (actList step s m) rest) - P s
      rw [ih (actList step s m)]
      show P (actList step s m) - P s
          + (P (pathEnd step (actList step s m) rest) - P (actList step s m))
          = P (pathEnd step (actList step s m) rest) - P s
      omega

/-- **Path independence.**  Two sequences of moves with the same endpoints
carry the same total.  A difference cost cannot tell one route from
another. -/
theorem path_independent (P : S → Int) (step : S → I → S) (s : S)
    (ms ns : List (List I)) (h : pathEnd step s ms = pathEnd step s ns) :
    pathTotal P step s ms = pathTotal P step s ns := by
  rw [pathTotal_eq, pathTotal_eq, h]

/-- **Zero circulation.**  Around any closed walk -- any sequence of moves
returning to its own start -- the total of a difference cost is zero.

This is the rung's headline, and it is a limitation rather than a virtue: a
cost with zero circulation on every closed walk carries no obstruction. -/
theorem circulation_zero (P : S → Int) (step : S → I → S) (s : S)
    (ms : List (List I)) (h : pathEnd step s ms = s) :
    pathTotal P step s ms = 0 := by
  rw [pathTotal_eq, h]
  omega

/-! ## 4. The item count is additive too -/

/-- The sealed item count, as a cost. -/
def countCost (d : List I) : Int := (d.length : Int)

/-- **The item count is additive along composition.**  So additivity does
not separate a base-relative cost from a base-free one, and the question's
premise -- that additivity is what makes a price into a price along a path
-- does not hold. -/
theorem count_additive (d e : List I) :
    countCost (d ++ e) = countCost d + countCost e := by
  show ((d ++ e).length : Int) = (d.length : Int) + (e.length : Int)
  rw [List.length_append]
  omega

/-! ## 5. A concrete state carrying an absorbing move -/

namespace Loop

/-- Two items: one that changes the state and one that does not. -/
inductive Tok where
  | keep : Tok
  | grow : Tok
deriving DecidableEq, Repr

def step : Nat → Tok → Nat
  | n, Tok.keep => n
  | n, Tok.grow => n + 1

/-- The absorbing move is a closed walk of length one. -/
theorem keep_is_a_closed_walk (n : Nat) :
    actList step n [Tok.keep] = n := rfl

/-- Every difference cost is zero on it, whatever the functional. -/
theorem diff_zero_on_the_closed_walk (P : Nat → Int) (n : Nat) :
    diff P step n [Tok.keep] = 0 := by
  show P (actList step n [Tok.keep]) - P n = 0
  rw [keep_is_a_closed_walk]
  omega

/-- **The item count is not a difference cost.**  No state functional has
it as its difference, because it is nonzero around a closed walk and every
difference is zero there.

This is what actually separates the two costs, and it is a refutation
rather than a failure to find one. -/
theorem count_is_not_a_difference :
    ¬ ∃ P : Nat → Int, ∀ (s : Nat) (d : List Tok),
        countCost d = P (actList step s d) - P s := by
  intro h
  obtain ⟨P, hP⟩ := h
  have one : countCost [Tok.keep] = P (actList step 0 [Tok.keep]) - P 0 :=
    hP 0 [Tok.keep]
  rw [keep_is_a_closed_walk] at one
  have value : countCost [Tok.keep] = (1 : Int) := rfl
  rw [value] at one
  omega

end Loop

/-! ## 6. The unsigned form, and why the sign is load-bearing -/

namespace Unsigned

/-- The same cost with truncated subtraction. -/
def natDiff (P : S → Nat) (step : S → I → S) (s : S) (d : List I) : Nat :=
  P (actList step s d) - P s

/-- Additivity survives truncation **only** under a monotonicity
hypothesis, and the hypothesis has to be supplied. -/
theorem natDiff_additive_of_monotone (P : S → Nat) (step : S → I → S) (s : S)
    (d e : List I)
    (h1 : P s ≤ P (actList step s d))
    (h2 : P (actList step s d) ≤ P (actList step (actList step s d) e)) :
    natDiff P step s (d ++ e)
      = natDiff P step s d + natDiff P step (actList step s d) e := by
  show P (actList step s (d ++ e)) - P s
      = (P (actList step s d) - P s)
        + (P (actList step (actList step s d) e) - P (actList step s d))
  rw [actList_append]
  omega

/-- Two items, one raising the state and one lowering it. -/
inductive Move where
  | up : Move
  | down : Move
deriving DecidableEq, Repr

def step2 : Nat → Move → Nat
  | n, Move.up => n + 1
  | n, Move.down => n - 1

/-- **Without monotonicity the unsigned form is not additive**, exhibited
rather than argued: a rise then a fall totals one step by step and zero as a
composite, because the fall is truncated away. -/
theorem natDiff_not_additive :
    natDiff id step2 0 ([Move.up] ++ [Move.down])
      ≠ natDiff id step2 0 [Move.up]
        + natDiff id step2 (actList step2 0 [Move.up]) [Move.down] := by
  decide

/-- The same model over the signed coefficients is additive, by the general
theorem.  So the failure above is the truncation and nothing else. -/
theorem signed_is_additive_on_the_same_model :
    diff (fun n : Nat => (n : Int)) step2 0 ([Move.up] ++ [Move.down])
      = diff (fun n : Nat => (n : Int)) step2 0 [Move.up]
        + diff (fun n : Nat => (n : Int)) step2 (actList step2 0 [Move.up])
            [Move.down] :=
  diff_additive _ _ _ _ _

end Unsigned

end ReachAdditivity
