/-!
# The space of additive costs, where path-dependence can live, and one that lives there

The preceding rung showed that a cost of the form `P(apply s d) - P s`
telescopes, so it cannot tell one route from another or witness nonzero
circulation.  It named the target that remained: a cost that is additive
along composition, reads the state, and is **not** of that form.

This file does three things.

**It describes the search space.**  Additivity is a constraint, not a wish.
It forces the empty response to cost nothing, and then forces every response
to cost the sum of its items, each priced at the state it meets.  So an
additive cost *is* represented by a weighting of single moves.  The finite
candidate list studied computationally contains examples of such weightings;
it is not an enumeration of all of them.

**It rules out one source of path-dependence.**  Admission only adds, so the
states carry an order no move decreases.  A directed walk that returns to its
start therefore never moved at all.  The finite computation separately
reports self-loops, non-self fundamental cycles, and explicit pairs of
directed routes with common endpoints; the theorem does not identify every
non-self cycle with such a pair.

**It exhibits one of the second kind.**  A commitment over everything
present costs what it ranges over at the moment it is made.  Make it before
the state grows and it is cheap; make it after and the same commitment
ranges further.  The two routes end in the same state and cost differently,
so no state functional has this cost as its difference.  The sealed item
count, on the same square, cannot tell the routes apart.

At the pinned snapshot nothing here was cited from the two then-unmerged
sibling trees.  `actList` and its append law were re-proved rather than
imported across open pull requests.

Core Lean only: no `Mathlib`, no choice principle, no proof left incomplete.
`AuthorityEffect: None.`
-/

namespace PathDependentCost

variable {S I : Type}

/-! ## 1. The action, re-proved here -/

/-- Apply a sequence of items one at a time, left to right. -/
def actList (step : S → I → S) : S → List I → S
  | s, [] => s
  | s, i :: rest => actList step (step s i) rest

/-- Applying a composite is applying the parts in order. -/
theorem actList_append (step : S → I → S) (d : List I) :
    ∀ (s : S) (e : List I),
      actList step s (d ++ e) = actList step (actList step s d) e := by
  induction d with
  | nil => intro s e; rfl
  | cons i rest ih =>
      intro s e
      show actList step (step s i) (rest ++ e) = _
      exact ih (step s i) e

/-! ## 2. Additive costs are exactly weightings of single moves -/

/-- A cost is additive along composition when the price of a composite is
the price of the first part plus the price of the second, charged where the
second is actually applied. -/
def Additive (step : S → I → S) (c : S → List I → Int) : Prop :=
  ∀ (s : S) (d e : List I), c s (d ++ e) = c s d + c (actList step s d) e

/-- The cost built from a weighting of single moves by summation. -/
def sumEdges (w : S → I → Int) (step : S → I → S) : S → List I → Int
  | _, [] => 0
  | s, i :: rest => w s i + sumEdges w step (step s i) rest

theorem sumEdges_nil (w : S → I → Int) (step : S → I → S) (s : S) :
    sumEdges w step s [] = 0 := rfl

theorem sumEdges_additive (w : S → I → Int) (step : S → I → S) :
    Additive step (sumEdges w step) := by
  intro s d e
  induction d generalizing s with
  | nil => show sumEdges w step s e = 0 + sumEdges w step s e; omega
  | cons i rest ih =>
      show w s i + sumEdges w step (step s i) (rest ++ e)
          = (w s i + sumEdges w step (step s i) rest)
            + sumEdges w step (actList step (step s i) rest) e
      rw [ih (step s i)]
      omega

/-- **The empty response is free.**  Not a convention: additivity forces
it, by applying the law to the empty response twice. -/
theorem additive_empty_zero (step : S → I → S) (c : S → List I → Int)
    (h : Additive step c) (s : S) : c s [] = 0 := by
  have both : c s ([] ++ []) = c s [] + c (actList step s []) [] := h s [] []
  rw [show actList step s [] = s from rfl] at both
  simp only [List.nil_append] at both
  omega

/-- **The characterisation.**  Every additive cost is the summation of its
own restriction to single moves.  Thus unrestricted weightings represent the
whole additive class; this says nothing about whether a finite candidate list
exhausts those weightings. -/
theorem additive_eq_sumEdges (step : S → I → S) (c : S → List I → Int)
    (h : Additive step c) :
    ∀ (d : List I) (s : S), c s d = sumEdges (fun s i => c s [i]) step s d := by
  intro d
  induction d with
  | nil => intro s; rw [additive_empty_zero step c h s]; rfl
  | cons i rest ih =>
      intro s
      have split : c s ([i] ++ rest) = c s [i] + c (actList step s [i]) rest :=
        h s [i] rest
      show c s (i :: rest) = c s [i] + sumEdges (fun s i => c s [i]) step (step s i) rest
      rw [← ih (step s i)]
      show c s (i :: rest) = c s [i] + c (step s i) rest
      show c s ([i] ++ rest) = c s [i] + c (step s i) rest
      exact split

/-! ## 3. Exactness, and what two routes do to it -/

/-- A cost is exact when some state functional has it as its difference. -/
def Exact (step : S → I → S) (c : S → List I → Int) : Prop :=
  ∃ P : S → Int, ∀ (s : S) (d : List I), c s d = P (actList step s d) - P s

/-- An exact cost gives two routes with the same endpoints the same total.
It reads nothing but where the route starts and where it stops. -/
theorem exact_agrees_on_two_routes (step : S → I → S) (c : S → List I → Int)
    (h : Exact step c) (s : S) (d e : List I)
    (hend : actList step s d = actList step s e) :
    c s d = c s e := by
  obtain ⟨P, hP⟩ := h
  rw [hP s d, hP s e, hend]

/-- **The test used below.**  Two routes to one state with two totals refute
exactness outright: no functional at all, not merely no obvious one. -/
theorem not_exact_of_routes_differ (step : S → I → S) (c : S → List I → Int)
    (s : S) (d e : List I) (hend : actList step s d = actList step s e)
    (hcost : c s d ≠ c s e) : ¬ Exact step c :=
  fun h => hcost (exact_agrees_on_two_routes step c h s d e hend)

/-! ## 4. Where path-dependence can come from when admission only adds -/

/-- A move never decreases the state, so neither does a sequence of them. -/
theorem le_actList (step : S → I → S) (le : S → S → Prop)
    (refl : ∀ s, le s s) (trans : ∀ a b c, le a b → le b c → le a c)
    (mono : ∀ s i, le s (step s i)) :
    ∀ (d : List I) (s : S), le s (actList step s d) := by
  intro d
  induction d with
  | nil => intro s; exact refl s
  | cons i rest ih =>
      intro s
      exact trans s (step s i) (actList step (step s i) rest) (mono s i) (ih (step s i))

/-- **Directed closed walks are stationary.**  If admission only adds and
the order is antisymmetric, a sequence of moves returning to its own start
never left it: every prefix is already the start.

So in an estate of this shape, path-dependence cannot come from a directed
closed walk that changes state.  This theorem does not classify every
non-self cycle of an underlying undirected graph. -/
theorem closed_directed_walk_is_stationary (step : S → I → S) (le : S → S → Prop)
    (refl : ∀ s, le s s) (trans : ∀ a b c, le a b → le b c → le a c)
    (anti : ∀ a b, le a b → le b a → a = b)
    (mono : ∀ s i, le s (step s i))
    (s : S) (p q : List I) (closed : actList step s (p ++ q) = s) :
    actList step s p = s := by
  have up : le s (actList step s p) := le_actList step le refl trans mono p s
  have on : le (actList step s p) (actList step (actList step s p) q) :=
    le_actList step le refl trans mono q (actList step s p)
  rw [← actList_append step p s q, closed] at on
  exact anti (actList step s p) s on up

/-! ## 5. A cost that prices order: the commitment and its span

The state records how much stands and whether the commitment has been made.
The commitment ranges over everything standing, so its price is what it
ranges over **at the moment it is made** -- a fact about the state, not
about the item. -/

namespace Commit

/-- How much stands, and whether the commitment has been made. -/
abbrev St : Type := Nat × Bool

inductive Move where
  | grow : Move
  | commit : Move
deriving DecidableEq, Repr

def step : St → Move → St
  | (n, c), Move.grow => (n + 1, c)
  | (n, _), Move.commit => (n, true)

/-- The commitment costs what it ranges over when it is made; growing the
state costs nothing. -/
def span : St → Move → Int
  | (_, _), Move.grow => 0
  | (n, _), Move.commit => (n : Int)

/-- The weighting reads the state: one item, two prices. -/
theorem span_reads_the_state :
    span (0, false) Move.commit ≠ span (1, false) Move.commit := by decide

/-- **The square commutes.**  Committing then growing, and growing then
committing, land on the same state. -/
theorem routes_agree (n : Nat) :
    actList step (n, false) [Move.commit, Move.grow]
      = actList step (n, false) [Move.grow, Move.commit] := rfl

/-- Committing before the state grows costs `n`. -/
theorem commit_early (n : Nat) :
    sumEdges span step (n, false) [Move.commit, Move.grow] = (n : Int) := by
  show (n : Int) + (0 + 0) = (n : Int)
  omega

/-- Committing after it grows costs `n + 1`: the same commitment, ranging
over one more thing. -/
theorem commit_late (n : Nat) :
    sumEdges span step (n, false) [Move.grow, Move.commit] = (n : Int) + 1 := by
  show (0 : Int) + (((n + 1 : Nat) : Int) + 0) = (n : Int) + 1
  omega

/-- **The two routes cost differently.** -/
theorem span_prices_the_order (n : Nat) :
    sumEdges span step (n, false) [Move.commit, Move.grow]
      ≠ sumEdges span step (n, false) [Move.grow, Move.commit] := by
  rw [commit_early, commit_late]
  omega

/-- **The cost is additive, reads the state, and is not exact.**  This is
the object the preceding rung named and did not have. -/
theorem span_is_additive : Additive step (sumEdges span step) :=
  sumEdges_additive span step

theorem span_is_not_exact : ¬ Exact step (sumEdges span step) :=
  not_exact_of_routes_differ step (sumEdges span step) (0, false)
    [Move.commit, Move.grow] [Move.grow, Move.commit]
    (routes_agree 0) (span_prices_the_order 0)

/-! ### The item count, on the same square -/

/-- The sealed count as a weighting: one per move, whatever it meets. -/
def one : St → Move → Int := fun _ _ => 1

/-- **The item count cannot see the order.**  On the very square where the
span disagrees with itself, the count gives both routes the same total, and
would go on doing so however the square were drawn: both routes use two
moves.  So the count's failure to be exact is a different phenomenon --
it charges for waste, not for order. -/
theorem count_cannot_see_the_order (n : Nat) :
    sumEdges one step (n, false) [Move.commit, Move.grow]
      = sumEdges one step (n, false) [Move.grow, Move.commit] := rfl

end Commit

end PathDependentCost
