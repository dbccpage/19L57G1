/-!
# One thing, an event, and the two-ness that arises

This module imports NOTHING.  No arithmetic, no lists, no indexing, no
succession, no ordering, no counting, no norms — so its independence
from all of those is checkable by reading the import line rather than by
trusting prose.

The data is one thing and one event.  The event carries no index, no
cause, no predecessor and no successor.  It is not applied to a pair;
there is no pair until it holds.  It is a reflection of the whole onto
itself with no fixed point, and that is the entire content of "the
symmetry breaks".

Two-ness is not a field.  `two_arises` derives it: under the event, no
element is its own reflection, so nothing is one thing.  A prior module
in this repository, `TwoPresentations`, posited the two as separate
fields `pi` and `pj`; that assumed what should be derived, and this
module does not repeat it.

## What "no global section" means here, exactly

A selector may pick a representative for each reflected pair
(`Consistent`), and it may commute with the event (`Equivariant`).  It
cannot do both — `no_global_section`.  That the constraint is not
vacuous is exhibited, not asserted: `constFalse` on `boolBreak` is a
consistent representative selector that is simply not equivariant.  So
local choice is available and global choice is obstructed, and both
halves are proved.

## Weight, recorded before the theorems

Every proof here is one to four lines.  The content is the choice of
primitive, not the difficulty.  Cite it that way.

## Classification

Metatheory apparatus and DECLARED structure.  `Break` is a declared
shape; nothing here claims it is forced, and nothing here connects it to
`DiffObs`, `PresIso`, observers, or any other structure in this
repository.  No bridge is proved and none should be read in.
-/

namespace Breaking

/-- **One thing and one event.**  `Whole` is opaque.  `e` is the event:
a reflection with no fixed point.  It has no index, no provenance, no
order, and no cause — nothing records why it holds, and nothing here
depends on why. -/
structure Break where
  Whole : Type
  e : Whole → Whole
  e_involutive : ∀ w, e (e w) = w
  e_no_fixed : ∀ w, e w ≠ w

/-- **Two-ness arises; it is not assumed.**  Under the event nothing is
its own reflection, so nothing is one thing.  This is derived from the
event, not posited as a pair. -/
theorem two_arises (B : Break) (w : B.Whole) : w ≠ B.e w :=
  fun h => B.e_no_fixed w h.symm

/-- **The reflection is mutual.**  Neither side is first, and neither is
the original: each is the reflection of the other.  There is no fact of
the matter about which one was there before, because there is no
before. -/
theorem reflection_is_mutual (B : Break) (w : B.Whole) :
    B.e (B.e w) = w := B.e_involutive w

/-- A selector picks something for each element. -/
def Selector (B : Break) : Type := B.Whole → B.Whole

/-- It is a REPRESENTATIVE selector when what it picks is one of the two
reflected things. -/
def Represents (B : Break) (s : Selector B) : Prop :=
  ∀ w, s w = w ∨ s w = B.e w

/-- It is CONSISTENT when the two reflected things get the same pick —
one choice per pair, which is what selecting a side means. -/
def Consistent (B : Break) (s : Selector B) : Prop :=
  ∀ w, s (B.e w) = s w

/-- It is EQUIVARIANT when it commutes with the event — when the choice
is made without appeal to anything outside the structure. -/
def Equivariant (B : Break) (s : Selector B) : Prop :=
  ∀ w, s (B.e w) = B.e (s w)

/-- **No global section.**  No selector is both consistent and
equivariant.  Consistency says the pair gets one pick; equivariance says
the pick commutes with the reflection; together they would make that
pick its own reflection, which the event forbids.

Two things stated honestly.  The proof does NOT spend `Represents`: the
obstruction is between consistency and equivariance alone, and carrying
a representativeness hypothesis it never uses would overstate what is
needed.  And it DOES need an inhabitant `w`.  That is not a technicality
— with nothing there, a selector is vacuously both, and there is no
obstruction.  No thing, no break. -/
theorem no_global_section (B : Break) (w : B.Whole) (s : Selector B)
    (hcons : Consistent B s) (hequi : Equivariant B s) : False :=
  B.e_no_fixed (s w) ((hequi w).symm.trans (hcons w))

/-- **Local choice is available.**  Two elements, the event being
reflection.  Nothing counts and nothing is ordered; `Bool` is used only
as a two-element carrier. -/
def boolBreak : Break where
  Whole := Bool
  e := not
  e_involutive := by intro w; cases w <;> rfl
  e_no_fixed := by intro w h; cases w <;> exact Bool.noConfusion h

/-- The constant selector picks one side for every pair. -/
def constFalse : Selector boolBreak := fun _ => false

theorem constFalse_represents : Represents boolBreak constFalse := by
  intro w
  cases w
  · exact Or.inl rfl
  · exact Or.inr rfl

theorem constFalse_consistent : Consistent boolBreak constFalse :=
  fun _ => rfl

/-- **And it is not equivariant.**  So the obstruction is real rather
than vacuous: a consistent representative selector exists, and it fails
exactly at equivariance. -/
theorem constFalse_not_equivariant :
    ¬ Equivariant boolBreak constFalse :=
  fun h => Bool.noConfusion (h false)

/-- Both halves together: local choice available, global choice
obstructed. -/
theorem local_available_global_obstructed :
    (Represents boolBreak constFalse ∧ Consistent boolBreak constFalse) ∧
    ¬ Equivariant boolBreak constFalse :=
  ⟨⟨constFalse_represents, constFalse_consistent⟩,
   constFalse_not_equivariant⟩

/-! ## What this does NOT claim

* It does not claim `Break` is forced.  It is a declared shape.
* It does not claim the event has a cause, a source, or a place in any
  order.  Nothing records why it holds, and no theorem depends on why.
* It does not introduce counting, magnitude, norm, or observer.  Those
  are absent, not deferred to a hidden layer.
* It does not claim repetition.  One event is modelled here; whether
  further breaking is representable without succession is NOT settled by
  this module.
* It proves nothing about `DiffObs`, `PresIso`, `NonZeroPair`, or any
  other structure in this repository.  No bridge is proved.
-/

end Breaking
