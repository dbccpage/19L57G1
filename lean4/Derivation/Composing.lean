/-!
# Composition as a relation that may fail to hold

This module imports NOTHING.  No arithmetic, no lists, no indexing, no
succession, no ordering, no counting, no magnitude.

The point is one field.  A category supplies composition as an
OPERATION: `∘` takes two arrows and DELIVERS a third, for every
composable pair, always.  That totality is what forces a domain closed
under composition — a container — and it is the thing being refused
here.

`Web` supplies composition as a three-place RELATION instead.
`Composes f g h` says that `h` is a composite of `f` then `g`.  Nothing
requires such an `h` to exist, nothing makes it unique, and nothing
makes the relation associative.  Composition is a fact that may hold of
a triple, not something performed on a pair.

So "some compose" is the primitive.  It is NOT a filter applied to a
pre-existing collection of all composites — there is no such
collection, which is the whole reason for the shape.

## What is exhibited, rather than assumed

Each of the three things a category hands you for free is shown here to
be a genuine extra assumption, by exhibiting a `Web` where it fails:

* `composition_may_fail` — a pair with no composite at all;
* `composite_may_be_nonunique` — a pair with two distinct composites,
  so no operation is determined even where composites exist;
* `associativity_is_not_free` — composites existing on both bracketings
  and disagreeing.

Non-uniqueness is the load-bearing one.  It shows that `Composes`
cannot be replaced by any function, so the relation is not an operation
in disguise.

## Weight

The proofs are one to three lines each.  The content is the choice of
shape — a relation rather than an operator — not the difficulty.

## Classification

Metatheory apparatus and DECLARED structure.  `Web` is a declared
shape.  Nothing here claims it is forced, and no bridge to any other
structure in this repository is proved.
-/

namespace Composing

/-- Nodes, declared arrows between them, and a three-place composition
RELATION.  `Arr a b` may be empty.  `Composes f g h` may hold for no
`h`, for one, or for several.  There is no operator, no identity, and
no associativity law. -/
structure Web where
  Node : Type
  Arr : Node → Node → Type
  Composes : (a b c : Node) → Arr a b → Arr b c → Arr a c → Prop

/-- A pair composes when some composite holds of it.  Nothing requires
this. -/
def Composable (W : Web) (a b c : W.Node)
    (f : W.Arr a b) (g : W.Arr b c) : Prop :=
  ∃ h : W.Arr a c, W.Composes a b c f g h

/-! ## 1. Composition may simply fail -/

def noneCompose : Web where
  Node := Unit
  Arr _ _ := Bool
  Composes _ _ _ _ _ _ := False

/-- **Nothing has to compose.**  Arrows are present and no composite
holds of any pair.  So `Composable` is a real condition, not a
formality. -/
theorem composition_may_fail :
    ¬ Composable noneCompose () () () true true := by
  rintro ⟨_, hfalse⟩
  exact hfalse

/-! ## 2. A composite need not be unique -/

def allCompose : Web where
  Node := Unit
  Arr _ _ := Bool
  Composes _ _ _ _ _ _ := True

/-- **No operation is determined.**  Two distinct arrows are both
composites of the same pair, so no function could extract "the"
composite.  This is why `Composes` is a relation and cannot be an
operator in disguise. -/
theorem composite_may_be_nonunique :
    ∃ h h' : allCompose.Arr () (),
      h ≠ h' ∧
      allCompose.Composes () () () true true h ∧
      allCompose.Composes () () () true true h' :=
  ⟨true, false, fun c => Bool.noConfusion c, trivial, trivial⟩

/-! ## 3. Associativity is an extra assumption -/

/-- A composition relation that is not associative. -/
def skewCompose : Web where
  Node := Unit
  Arr _ _ := Bool
  Composes _ _ _ f g h := h = (f && !g)

/-- **Associativity does not come for free.**  Composites exist on both
bracketings of the same three arrows and disagree.  So a `Web` is not a
category with the laws left implicit; the laws are absent. -/
theorem associativity_is_not_free :
    ∃ f g k u v w w' : skewCompose.Arr () (),
      skewCompose.Composes () () () f g u ∧
      skewCompose.Composes () () () u k w ∧
      skewCompose.Composes () () () g k v ∧
      skewCompose.Composes () () () f v w' ∧
      w ≠ w' :=
  ⟨true, false, true, true, false, false, true,
   rfl, rfl, rfl, rfl, fun c => Bool.noConfusion c⟩

/-! ## What this does NOT claim

* It does not claim `Web` is forced.  It is a declared shape.
* It does not supply identities, inverses, associativity, or totality,
  and it does not claim they are unavailable — only that they are extra,
  and each is exhibited failing above.
* It does not claim a collection of all composites exists.  There is no
  such collection here, and `Composable` quantifies over arrows of a
  declared type rather than over any totality of paths.
* It says nothing about magnitude, weight, measure, or summing.  No
  integral, no norm, no scalar is available or implied.
* It proves nothing about `DiffObs`, `PresIso`, `HFamily`, `Break`, or
  any other structure in this repository.  No bridge is proved.
-/

end Composing
