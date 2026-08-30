import NaturalSections
import NaturalSections.HopFixture

/-!
# Refinement: the class is a mesh invariant

A SUBDIVISION of a declared arrow `h0 : a0 -> b0` adds a fresh midpoint
object with a declared presentation and splits `h0`'s transport through
a declared factorization `F`: the first half-arrow carries `F`, the
second carries `F.symm ; iso h0`.  The original arrow is retained; its
naturality equation is implied by the halves'.

The theorem: a natural section exists iff one exists for the subdivided
family, for EVERY family, arrow, midpoint and factorization.  The
midpoint's value is forced -- `F.mapPair (s a0)` -- so refining a mesh
adds no freedom and removes none; the class never moves.  Finite chains
of subdivisions compose by transitivity of the iff.  Nothing here
orders a refinement sequence.  AuthorityEffect: None.
-/

namespace NaturalSections

open DiffInterface ContactKernel PresentationNaturality

/-- A subdivision instruction: the arrow, the midpoint's presentation,
and the declared factorization of the arrow's transport. -/
structure Subdiv (D : HFamily) where
  a0 : D.Obj
  b0 : D.Obj
  h0 : D.Hom a0 b0
  Mid : Type
  MidR : Type
  midObs : DiffObs Mid MidR
  F : PresIso (D.obs a0) midObs

variable {D : HFamily}

/-- The subdivided family: one fresh object, the two half-arrows added,
everything else retained. -/
def Subdiv.family (S : Subdiv D) : HFamily where
  Obj := Sum D.Obj Unit
  car
    | .inl x => D.car x
    | .inr _ => S.Mid
  res
    | .inl x => D.res x
    | .inr _ => S.MidR
  obs
    | .inl x => D.obs x
    | .inr _ => S.midObs
  Hom
    | .inl x, .inl y => D.Hom x y
    | .inl x, .inr _ => PLift (S.a0 = x)
    | .inr _, .inl y => PLift (S.b0 = y)
    | .inr _, .inr _ => Empty
  iso o p h :=
    match o, p, h with
    | .inl x, .inl y, h => D.iso x y h
    | .inl _, .inr _, h => h.down ▸ S.F
    | .inr _, .inl _, h => h.down ▸ (S.F.symm.trans (D.iso S.a0 S.b0 S.h0))
    | .inr _, .inr _, h => nomatch h

/-- Push a section: old objects keep their values, the midpoint takes the
forced value `F.mapPair (s a0)`. -/
def Subdiv.push (S : Subdiv D) (s : HSec D) : HSec S.family
  | .inl x => s x
  | .inr _ => S.F.mapPair (s S.a0)

theorem Subdiv.push_natural (S : Subdiv D) {s : HSec D} (hs : HIsNatural D s) :
    HIsNatural S.family (S.push s) := by
  intro o p h
  match o, p, h with
  | .inl x, .inl y, h => exact hs x y h
  | .inl x, .inr u, h =>
    cases h with
    | up e =>
      subst e
      show S.F.mapPair (s S.a0) = S.F.mapPair (s S.a0)
      rfl
  | .inr u, .inl y, h =>
    cases h with
    | up e =>
      subst e
      show (S.F.symm.trans (D.iso S.a0 S.b0 S.h0)).mapPair (S.F.mapPair (s S.a0)) = s S.b0
      rw [mapPair_trans, mapPair_symm_left]
      exact hs S.a0 S.b0 S.h0
  | .inr u, .inr v, h => exact nomatch h

/-- Pull a section back: restrict to the old objects. -/
def Subdiv.pull (S : Subdiv D) (s' : HSec S.family) : HSec D :=
  fun x => s' (.inl x)

theorem Subdiv.pull_natural (S : Subdiv D) {s' : HSec S.family}
    (hs' : HIsNatural S.family s') : HIsNatural D (S.pull s') :=
  fun x y h => hs' (.inl x) (.inl y) h

/-- **The class is a mesh invariant.**  A natural section exists iff one
exists for any declared subdivision; finite chains compose by
transitivity. -/
theorem natural_section_iff_subdiv (S : Subdiv D) :
    (∃ s : HSec D, HIsNatural D s) ↔ ∃ s' : HSec S.family, HIsNatural S.family s' :=
  ⟨fun ⟨s, hs⟩ => ⟨S.push s, S.push_natural hs⟩,
   fun ⟨s', hs'⟩ => ⟨S.pull s', S.pull_natural hs'⟩⟩

/-- Refining never removes an obstruction. -/
theorem class_refinement_invariant (S : Subdiv D)
    (h : ¬ ∃ s : HSec D, HIsNatural D s) :
    ¬ ∃ s' : HSec S.family, HIsNatural S.family s' :=
  fun e => h ((natural_section_iff_subdiv S).mpr e)

/-- Every one-step subdivision of the two-label square is obstructed. -/
theorem square_subdiv_obstructed (S : Subdiv Hop.squareFamily) :
    ¬ ∃ s' : HSec S.family, HIsNatural S.family s' :=
  class_refinement_invariant S Hop.square_no_natural_section

/-- Every one-step subdivision of the chain keeps its section. -/
theorem chain_subdiv_section (S : Subdiv Hop.chainFamily) :
    ∃ s' : HSec S.family, HIsNatural S.family s' :=
  (natural_section_iff_subdiv S).mp Hop.chain_has_natural_section

/-! ## Replacement

`Subdiv.family` RETAINS the original arrow, so the theorem above covers
a redundant midpoint extension; the Python fixtures REPLACE each hop by
its two halves.  A reviewer of pull request 98 pointed out the mismatch.
`Repl` is the replacement operation: the original arrow is removed from
the family, and its naturality equation is DERIVED from the two halves
(`Repl.h0_equation`).  Removing an arrow means the instruction must be
able to point at it, so a replacement carries two decidabilities as
declared data: equality of objects, and equality with the removed arrow
at its own position.  Every fixture has both. -/

structure Repl (D : HFamily) extends Subdiv D where
  decObj : DecidableEq D.Obj
  dec0 : ∀ f : D.Hom a0 b0, Decidable (f = h0)

/-- The replacement family: the fresh midpoint, the two half-arrows, and
every original arrow EXCEPT the subdivided one. -/
def Repl.family (S : Repl D) : HFamily where
  Obj := Sum D.Obj Unit
  car
    | .inl x => D.car x
    | .inr _ => S.Mid
  res
    | .inl x => D.res x
    | .inr _ => S.MidR
  obs
    | .inl x => D.obs x
    | .inr _ => S.midObs
  Hom
    | .inl x, .inl y =>
        {f : D.Hom x y // ∀ (ex : S.a0 = x) (ey : S.b0 = y), ex ▸ ey ▸ S.h0 ≠ f}
    | .inl x, .inr _ => PLift (S.a0 = x)
    | .inr _, .inl y => PLift (S.b0 = y)
    | .inr _, .inr _ => Empty
  iso o p h :=
    match o, p, h with
    | .inl x, .inl y, h => D.iso x y h.val
    | .inl _, .inr _, h => h.down ▸ S.F
    | .inr _, .inl _, h => h.down ▸ (S.F.symm.trans (D.iso S.a0 S.b0 S.h0))
    | .inr _, .inr _, h => nomatch h

def Repl.push (S : Repl D) (s : HSec D) : HSec S.family
  | .inl x => s x
  | .inr _ => S.F.mapPair (s S.a0)

theorem Repl.push_natural (S : Repl D) {s : HSec D} (hs : HIsNatural D s) :
    HIsNatural S.family (S.push s) := by
  intro o p h
  match o, p, h with
  | .inl x, .inl y, h => exact hs x y h.val
  | .inl x, .inr u, h =>
    cases h with
    | up e =>
      subst e
      show S.F.mapPair (s S.a0) = S.F.mapPair (s S.a0)
      rfl
  | .inr u, .inl y, h =>
    cases h with
    | up e =>
      subst e
      show (S.F.symm.trans (D.iso S.a0 S.b0 S.h0)).mapPair (S.F.mapPair (s S.a0)) = s S.b0
      rw [mapPair_trans, mapPair_symm_left]
      exact hs S.a0 S.b0 S.h0
  | .inr u, .inr v, h => exact nomatch h

/-- **The removed arrow's equation is derived from the two halves**: the
halves compose to its transport. -/
theorem Repl.h0_equation (S : Repl D) {s' : HSec S.family}
    (hs' : HIsNatural S.family s') :
    (D.iso S.a0 S.b0 S.h0).mapPair (s' (.inl S.a0)) = s' (.inl S.b0) := by
  have key : ∀ (p : NonZeroPair (D.obs S.a0)) (q : NonZeroPair S.midObs)
      (r : NonZeroPair (D.obs S.b0)),
      S.F.mapPair p = q →
      (S.F.symm.trans (D.iso S.a0 S.b0 S.h0)).mapPair q = r →
      (D.iso S.a0 S.b0 S.h0).mapPair p = r := by
    intro p q r h1 h2
    rw [← h1, mapPair_trans, mapPair_symm_left] at h2
    exact h2
  exact key _ _ _ (hs' (.inl S.a0) (.inr ()) ⟨rfl⟩) (hs' (.inr ()) (.inl S.b0) ⟨rfl⟩)

theorem Repl.pull_natural (S : Repl D) {s' : HSec S.family}
    (hs' : HIsNatural S.family s') : HIsNatural D (fun x => s' (.inl x)) := by
  intro x y f
  cases S.decObj S.a0 x with
  | isFalse hx => exact hs' (.inl x) (.inl y) ⟨f, fun ex _ => absurd ex hx⟩
  | isTrue hx =>
    cases S.decObj S.b0 y with
    | isFalse hy => exact hs' (.inl x) (.inl y) ⟨f, fun _ ey => absurd ey hy⟩
    | isTrue hy =>
      subst hx
      subst hy
      cases S.dec0 f with
      | isTrue hf =>
        subst hf
        exact S.h0_equation hs'
      | isFalse hf =>
        exact hs' (.inl S.a0) (.inl S.b0) ⟨f, fun _ _ he => hf he.symm⟩

/-- **Replacement invariance**: the operation the fixtures perform -- the
arrow removed, the halves added -- changes nothing about sections. -/
theorem natural_section_iff_repl (S : Repl D) :
    (∃ s : HSec D, HIsNatural D s) ↔ ∃ s' : HSec S.family, HIsNatural S.family s' :=
  ⟨fun ⟨s, hs⟩ => ⟨S.push s, S.push_natural hs⟩,
   fun ⟨s', hs'⟩ => ⟨fun x => s' (.inl x), S.pull_natural hs'⟩⟩

/-- Every one-step replacement of a square hop leaves the square obstructed. -/
theorem square_repl_obstructed (S : Repl Hop.squareFamily) :
    ¬ ∃ s' : HSec S.family, HIsNatural S.family s' :=
  fun e => Hop.square_no_natural_section ((natural_section_iff_repl S).mpr e)

/-- Every one-step replacement of a chain hop keeps the chain's section. -/
theorem chain_repl_section (S : Repl Hop.chainFamily) :
    ∃ s' : HSec S.family, HIsNatural S.family s' :=
  (natural_section_iff_repl S).mp Hop.chain_has_natural_section

end NaturalSections
