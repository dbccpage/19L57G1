import NaturalSections
import NaturalSections.HopFixture

/-!
# Pointwise re-presentation never changes the class

A pointwise re-presentation of a declared family keeps its objects and
its arrows and presents each object through a presentation isomorphism
of its own, conjugating every arrow's transport accordingly.  It is
"the same family described differently at every object".  The theorem
here: a natural section of the family exists iff one exists for any of
its pointwise re-presentations.  An obstruction is therefore never a
presentation artifact; what can remove it is a change of FAMILY --
deleting arrows, building a cover, taking a quotient -- which this file
does not touch and `representation.py` costs out.  AuthorityEffect: None.
-/

namespace NaturalSections

open DiffInterface ContactKernel PresentationNaturality

/-- A pointwise re-presentation: a new observer at each object and an
isomorphism from the old one to it. -/
structure Repres (D : HFamily) where
  car : D.Obj → Type
  res : D.Obj → Type
  obs : (a : D.Obj) → DiffObs (car a) (res a)
  g : (a : D.Obj) → PresIso (D.obs a) (obs a)

variable {D : HFamily}

/-- The re-presented family: same objects, same arrows, each transport
conjugated by the object isomorphisms. -/
def Repres.family (P : Repres D) : HFamily where
  Obj := D.Obj
  car := P.car
  res := P.res
  obs := P.obs
  Hom := D.Hom
  iso a b h := ((P.g a).symm.trans (D.iso a b h)).trans (P.g b)

theorem Repres.iso_mapPair (P : Repres D) {a b : D.Obj} (h : D.Hom a b)
    (q : NonZeroPair (P.obs a)) :
    (P.family.iso a b h).mapPair q =
      (P.g b).mapPair ((D.iso a b h).mapPair ((P.g a).symm.mapPair q)) := by
  show (((P.g a).symm.trans (D.iso a b h)).trans (P.g b)).mapPair q = _
  rw [mapPair_trans, mapPair_trans]

/-- Carry a section forward through the object isomorphisms. -/
def Repres.push (P : Repres D) (s : HSec D) : HSec P.family :=
  fun a => (P.g a).mapPair (s a)

/-- Carry a section of the re-presented family back. -/
def Repres.pull (P : Repres D) (s' : HSec P.family) : HSec D :=
  fun a => (P.g a).symm.mapPair (s' a)

theorem Repres.push_natural (P : Repres D) {s : HSec D} (hs : HIsNatural D s) :
    HIsNatural P.family (P.push s) := by
  intro a b h
  refine (P.iso_mapPair h ((P.g a).mapPair (s a))).trans ?_
  show (P.g b).mapPair ((D.iso a b h).mapPair ((P.g a).symm.mapPair ((P.g a).mapPair (s a))))
      = (P.g b).mapPair (s b)
  rw [mapPair_symm_left, hs a b h]

theorem Repres.pull_natural (P : Repres D) {s' : HSec P.family}
    (hs' : HIsNatural P.family s') : HIsNatural D (P.pull s') := by
  intro a b h
  have e : (P.g b).mapPair ((D.iso a b h).mapPair ((P.g a).symm.mapPair (s' a))) = s' b :=
    (P.iso_mapPair h (s' a)).symm.trans (hs' a b h)
  show (D.iso a b h).mapPair ((P.g a).symm.mapPair (s' a)) = (P.g b).symm.mapPair (s' b)
  rw [← e, mapPair_symm_left]

/-- **T1.**  A natural section exists for `D` iff one exists for any
pointwise re-presentation of `D`. -/
theorem natural_section_iff_repres (P : Repres D) :
    (∃ s : HSec D, HIsNatural D s) ↔ ∃ s' : HSec P.family, HIsNatural P.family s' :=
  ⟨fun ⟨s, hs⟩ => ⟨P.push s, P.push_natural hs⟩,
   fun ⟨s', hs'⟩ => ⟨P.pull s', P.pull_natural hs'⟩⟩

/-- An obstruction is not a presentation artifact. -/
theorem obstruction_survives_repres (P : Repres D)
    (h : ¬ ∃ s : HSec D, HIsNatural D s) : ¬ ∃ s' : HSec P.family, HIsNatural P.family s' :=
  fun e => h ((natural_section_iff_repres P).mpr e)

/-- The two-label square stays obstructed under every pointwise
re-presentation, whatever carriers and observers it is presented in. -/
theorem square_obstruction_survives (P : Repres Hop.squareFamily) :
    ¬ ∃ s' : HSec P.family, HIsNatural P.family s' :=
  obstruction_survives_repres P Hop.square_no_natural_section

/-- The chain keeps its section under every pointwise re-presentation. -/
theorem chain_section_survives (P : Repres Hop.chainFamily) :
    ∃ s' : HSec P.family, HIsNatural P.family s' :=
  (natural_section_iff_repres P).mp Hop.chain_has_natural_section

end NaturalSections
