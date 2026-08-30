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

end NaturalSections
