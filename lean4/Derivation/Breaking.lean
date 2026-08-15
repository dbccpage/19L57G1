/-!
# A fixed-point-free reflection, and the two-cycle through each element

This module imports NOTHING.  No arithmetic, no lists, no indexing, no
succession, no ordering, no counting, no magnitude.

## The exact ceiling, stated before anything else

A declared fixed-point-free involution gives **a two-cycle through each
supplied element**.  That is all.  In particular:

* `Break` carries NO inhabitance law.  `emptyBreak` satisfies every
  field over an empty carrier, so nothing here asserts that anything
  exists.
* `Break` carries NO single-orbit law.  `fourBreak` satisfies every
  field with two disjoint reflected pairs, so nothing here asserts that
  there are exactly two things.

Both are exhibited below rather than described.  An earlier version of
this module said "two-ness is not a field, `two_arises` derives it".
That was FALSE twice over: the theorem was the fixed-point-free field
restated in the other direction, and the carrier admits both zero
elements and four.  The claim is WITHDRAWN and replaced by the ceiling
above.

## Weight

Every proof is one to four lines and each is an immediate corollary of
a field.  The content is the choice of primitive, not the difficulty,
and the primitive assumes the distinction it is sometimes said to
produce.
-/

namespace Breaking

/-- A carrier and a reflection with no fixed point.  The reflection has
no index, no provenance, no order and no cause: nothing records why it
holds and no theorem depends on why.

What it does NOT carry: any inhabitance law, and any law forcing a
single orbit.  Both omissions are load-bearing and are witnessed
below. -/
structure Break where
  Whole : Type
  e : Whole → Whole
  e_involutive : ∀ w, e (e w) = w
  e_no_fixed : ∀ w, e w ≠ w

/-- Nothing is its own reflection, in the other direction.  This is the
`e_no_fixed` FIELD restated, not a derivation of distinctness from
anything weaker — the content sits in the field, and citing this
theorem as though distinction were derived would misreport it. -/
theorem ne_image (B : Break) (w : B.Whole) : w ≠ B.e w :=
  fun h => B.e_no_fixed w h.symm

/-- Each supplied element sits on a two-cycle: the reflection carries
its image back. -/
theorem two_cycle (B : Break) (w : B.Whole) : B.e (B.e w) = w :=
  B.e_involutive w

/-! ## The two omissions, exhibited -/

/-- **No inhabitance.**  Every field holds vacuously over an empty
carrier, so `Break` does not assert that anything exists. -/
def emptyBreak : Break where
  Whole := Empty
  e := Empty.elim
  e_involutive := fun w => w.elim
  e_no_fixed := fun w => w.elim

/-- **No single orbit.**  Flipping only the first coordinate is
fixed-point-free and involutive on four elements, giving two disjoint
reflected pairs.  So `Break` does not assert that there are two
things. -/
def fourBreak : Break where
  Whole := Bool × Bool
  e p := (!p.1, p.2)
  e_involutive := by
    intro w
    cases w with
    | mk a b => cases a <;> rfl
  e_no_fixed := by
    intro w h
    cases w with
    | mk a b => cases a <;> exact Bool.noConfusion (congrArg Prod.fst h)

/-! ## Selectors -/

def Selector (B : Break) : Type := B.Whole → B.Whole

/-- What it picks is one of the two reflected things. -/
def Represents (B : Break) (s : Selector B) : Prop :=
  ∀ w, s w = w ∨ s w = B.e w

/-- It is constant on each reflected pair. -/
def OrbitConstant (B : Break) (s : Selector B) : Prop :=
  ∀ w, s (B.e w) = s w

/-- It commutes with the reflection. -/
def Equivariant (B : Break) (s : Selector B) : Prop :=
  ∀ w, s (B.e w) = B.e (s w)

/-- **No endomap is both orbit-constant and equivariant**, given an
inhabitant.

Named for exactly what it proves.  An earlier version called this
`no_global_section`, which named a quotient, a projection and a section
law that this module does not define — that name is WITHDRAWN.  A
section-of-the-quotient reading is not formalized here.

Two further honesty notes.  The proof does NOT spend `Represents`, so
carrying that hypothesis would overstate what is needed.  And it DOES
need an inhabitant: over `emptyBreak` a selector is vacuously both, and
there is no obstruction. -/
theorem no_orbit_constant_equivariant_endomap
    (B : Break) (w : B.Whole) (s : Selector B)
    (hconst : OrbitConstant B s) (hequi : Equivariant B s) : False :=
  B.e_no_fixed (s w) ((hequi w).symm.trans (hconst w))

/-! ## Both halves on a two-element carrier -/

def boolBreak : Break where
  Whole := Bool
  e := not
  e_involutive := by intro w; cases w <;> rfl
  e_no_fixed := by intro w h; cases w <;> exact Bool.noConfusion h

def constFalse : Selector boolBreak := fun _ => false

theorem constFalse_represents : Represents boolBreak constFalse := by
  intro w
  cases w
  · exact Or.inl rfl
  · exact Or.inr rfl

theorem constFalse_orbitConstant : OrbitConstant boolBreak constFalse :=
  fun _ => rfl

/-- The obstruction is not vacuous: an orbit-constant representative
selector exists and fails exactly at equivariance.  A side can be
imposed; it cannot commute with the reflection. -/
theorem constFalse_not_equivariant :
    ¬ Equivariant boolBreak constFalse :=
  fun h => Bool.noConfusion (h false)

theorem imposable_but_not_equivariant :
    (Represents boolBreak constFalse ∧ OrbitConstant boolBreak constFalse) ∧
    ¬ Equivariant boolBreak constFalse :=
  ⟨⟨constFalse_represents, constFalse_orbitConstant⟩,
   constFalse_not_equivariant⟩

/-! ## What this does NOT claim

* It does not claim `Break` is forced.  It is a declared shape.
* It does not derive distinctness, two-ness, or existence.  `ne_image`
  restates a field; `emptyBreak` and `fourBreak` show the carrier
  admits zero and four elements.
* It does not define a quotient, a projection, or a section, and
  proves nothing about any.
* It does not claim the reflection has a cause, a source, or a place in
  any order.
* It introduces no counting, magnitude, norm, or observer.
* It proves nothing about `DiffObs`, `PresIso`, `NonZeroPair`, or any
  other structure in this repository.  No bridge is proved.
-/

end Breaking
