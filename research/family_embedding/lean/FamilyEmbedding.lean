import Derivation.PresentationNaturality

/-!
# Embed a flat `Family` into `HFamily` and prove the natural-section iff

The sealed module's OPEN item (PresentationNaturality §14): a general
embedding of the flat `Family` (one carrier, arrows as `Arr` with
`src`/`tgt`) into `HFamily` (`Hom a b`) is not proved there.
`hAuto_iff_auto` bridges the two only at one object.

This module constructs `H F` with `Hom a b` the subtype of arrows
whose source is `a` and target is `b`, transports the declared
isomorphism along those equalities, and proves

  `(∃ s : Sec F, IsNatural F s) ↔ (∃ s' : HSec (H F), HIsNatural (H F) s')`.

The equalities are between variables, so `subst` closes every cast.
The first lemma is transport of `mapPair` under `▸`.  No choice
principle is used.  AuthorityEffect: None.
-/

namespace FamilyEmbedding

open DiffInterface ContactKernel PresentationNaturality

variable {X R : Type}

/-! ## 1. Transport of `mapPair` under observer equalities -/

/-- Recast a presentation isomorphism along equalities of its endpoint
observers.  Written with `▸` so `rfl ▸ rfl ▸ F` is definitionally `F`. -/
def isoAlong {O O' P P' : DiffObs X R}
    (hO : O = P) (hO' : O' = P') (F : PresIso O O') : PresIso P P' :=
  hO ▸ hO' ▸ F

theorem isoAlong_rfl {O O' : DiffObs X R} (F : PresIso O O') :
    isoAlong (rfl : O = O) (rfl : O' = O') F = F :=
  rfl

/-- **Transport of `mapPair` under `▸`.**  The equalities are between
variables, so `subst` closes every cast.  `hnatural_of_natural` rewrites
along this lemma. -/
theorem mapPair_along {O O' P P' : DiffObs X R}
    (hO : O = P) (hO' : O' = P') (F : PresIso O O') (p : NonZeroPair O) :
    (isoAlong hO hO' F).mapPair (hO ▸ p) = hO' ▸ F.mapPair p := by
  subst hO
  subst hO'
  rfl

/-! ## 2. The embedding `H` -/

/-- The indexed family with the same objects, the same observers, and
`Hom a b` the arrows of `F` that start at `a` and end at `b`.  The
isomorphism at such an arrow is the declared `F.iso`, recast along the
two equalities. -/
def H (F : Family X R) : HFamily where
  Obj := F.Obj
  car _ := X
  res _ := R
  obs := F.obs
  Hom a b := { f : F.Arr // F.src f = a ∧ F.tgt f = b }
  iso _ _ h :=
    isoAlong (congrArg F.obs h.property.1) (congrArg F.obs h.property.2) (F.iso h.val)

/-- On an arrow presented at its own source and target, the recast is
the declared isomorphism. -/
theorem embedIso_rfl (F : Family X R) (f : F.Arr) :
    (H F).iso (F.src f) (F.tgt f) ⟨f, rfl, rfl⟩ = F.iso f :=
  rfl

/-! ## 3. The iff, both directions -/

/-- A natural section of the flat family is natural for `H F`.  The
section values are recast along `congrArg F.obs` of the two endpoint
equalities; `mapPair_along` turns the recast isomorphism into the
flat `mapPair`, and `hs f` closes. -/
theorem hnatural_of_natural (F : Family X R) (s : Sec F)
    (hs : IsNatural F s) : HIsNatural (H F) s := by
  intro a b h
  rcases h with ⟨f, hsrc, htgt⟩
  subst hsrc
  subst htgt
  change
    (isoAlong (Eq.refl (F.obs (F.src f))) (Eq.refl (F.obs (F.tgt f))) (F.iso f)).mapPair
        (Eq.refl (F.obs (F.src f)) ▸ s (F.src f)) =
      Eq.refl (F.obs (F.tgt f)) ▸ s (F.tgt f)
  rw [mapPair_along]
  rw [hs f]

/-- A natural section of `H F` is natural for the flat family: every
flat arrow is the subtype member `⟨f, rfl, rfl⟩`. -/
theorem natural_of_hnatural (F : Family X R) (s : HSec (H F))
    (hs : HIsNatural (H F) s) : IsNatural F s := by
  intro f
  exact hs (F.src f) (F.tgt f) ⟨f, rfl, rfl⟩

/-- **The embedding iff.**  A natural section exists for the flat
family `F` if and only if one exists for `H F`.  Both directions keep
the same section; only the naturality predicate is rewritten. -/
theorem natural_section_iff_embed (F : Family X R) :
    (∃ s : Sec F, IsNatural F s) ↔
      (∃ s' : HSec (H F), HIsNatural (H F) s') :=
  ⟨fun ⟨s, hs⟩ => ⟨s, hnatural_of_natural F s hs⟩,
   fun ⟨s', hs'⟩ => ⟨s', natural_of_hnatural F s' hs'⟩⟩

/-- The one-object case recovers behaviour consistent with the sealed
`hAuto_iff_auto`: a natural section of `H (autoFamily O F)` exists
exactly when one exists of `hAutoFamily O F`. -/
theorem one_object_recovers (O : DiffObs X R) (F : PresIso O O) :
    (∃ s : HSec (H (autoFamily O F)), HIsNatural (H (autoFamily O F)) s) ↔
      (∃ s : HSec (hAutoFamily O F), HIsNatural (hAutoFamily O F) s) :=
  (natural_section_iff_embed (autoFamily O F)).symm.trans (hAuto_iff_auto O F).symm

theorem autoFamily_hom_inhabited (O : DiffObs X R) (F : PresIso O O) :
    Nonempty ((H (autoFamily O F)).Hom () ()) :=
  ⟨⟨(), rfl, rfl⟩⟩

/-! ## 4. Two-object fixtures (anti-vacuity)

Same two objects, same observers (`boolEqObs` on `Bool`), four arrows
so every `Hom` cell is inhabited: a loop at each object and a crossing
in each direction.  The obstructed family puts the sealed `negIso` on
both loops (a fixed-point-free automorphism of the carrier) and the
identity on the crossings.  The clean family puts the identity on
every arrow.  An empty or wrong `Hom` would make one of these fail:
the obstructed family would not be obstructed on the `H` side, or the
clean family would have no arrow to be natural at. -/

inductive TwoObj where
  | a | b
  deriving DecidableEq, Repr

inductive TwoArr where
  | loopA | loopB | crossAB | crossBA
  deriving DecidableEq, Repr

def twoSrc : TwoArr → TwoObj
  | .loopA => .a
  | .loopB => .b
  | .crossAB => .a
  | .crossBA => .b

def twoTgt : TwoArr → TwoObj
  | .loopA => .a
  | .loopB => .b
  | .crossAB => .b
  | .crossBA => .a

def twoIso (loopIso : PresIso boolEqObs boolEqObs) :
    (f : TwoArr) → PresIso boolEqObs boolEqObs
  | .loopA => loopIso
  | .loopB => loopIso
  | .crossAB => PresIso.refl boolEqObs
  | .crossBA => PresIso.refl boolEqObs

/-- One graph, parameterized by the loop isomorphism. -/
def twoFamily (loopIso : PresIso boolEqObs boolEqObs) : Family Bool Bool where
  Obj := TwoObj
  obs _ := boolEqObs
  Arr := TwoArr
  src := twoSrc
  tgt := twoTgt
  iso := twoIso loopIso

def obstructed : Family Bool Bool := twoFamily negIso

def clean : Family Bool Bool := twoFamily (PresIso.refl boolEqObs)

theorem obstructed_loopA_is_neg :
    (H obstructed).iso .a .a ⟨.loopA, rfl, rfl⟩ = negIso :=
  rfl

theorem two_hom_cells (loopIso : PresIso boolEqObs boolEqObs) :
    Nonempty ((H (twoFamily loopIso)).Hom .a .a) ∧
    Nonempty ((H (twoFamily loopIso)).Hom .a .b) ∧
    Nonempty ((H (twoFamily loopIso)).Hom .b .a) ∧
    Nonempty ((H (twoFamily loopIso)).Hom .b .b) :=
  ⟨⟨⟨.loopA, rfl, rfl⟩⟩, ⟨⟨.crossAB, rfl, rfl⟩⟩,
   ⟨⟨.crossBA, rfl, rfl⟩⟩, ⟨⟨.loopB, rfl, rfl⟩⟩⟩

/-- Every `Hom` cell of the obstructed embedding is inhabited. -/
theorem obstructed_hom_inhabited :
    Nonempty ((H obstructed).Hom .a .a) ∧
    Nonempty ((H obstructed).Hom .a .b) ∧
    Nonempty ((H obstructed).Hom .b .a) ∧
    Nonempty ((H obstructed).Hom .b .b) :=
  two_hom_cells negIso

/-- The flat obstructed family has no natural section: the loop at
`.a` is `negIso`, which fixes no admissible pair. -/
theorem obstructed_no_section :
    ¬ ∃ s : Sec obstructed, IsNatural obstructed s := by
  rintro ⟨s, hs⟩
  exact negIso_fixed_point_free (s .a) (hs .loopA)

/-- `H` of the obstructed family is obstructed too.  The endomorphism
at `.a` is `negIso` (see `obstructed_loopA_is_neg`), so the sealed
`no_natural_section_of_endo` applies. -/
theorem obstructed_H_no_section :
    ¬ ∃ s' : HSec (H obstructed), HIsNatural (H obstructed) s' :=
  no_natural_section_of_endo (H obstructed) .a ⟨.loopA, rfl, rfl⟩
    (by
      intro p
      rw [obstructed_loopA_is_neg]
      exact negIso_fixed_point_free p)

theorem clean_hom_inhabited :
    Nonempty ((H clean).Hom .a .a) ∧
    Nonempty ((H clean).Hom .a .b) ∧
    Nonempty ((H clean).Hom .b .a) ∧
    Nonempty ((H clean).Hom .b .b) :=
  two_hom_cells (PresIso.refl boolEqObs)

def cleanSection : Sec clean := fun _ => boolEqPair

theorem clean_natural : IsNatural clean cleanSection := by
  intro f
  cases f <;> exact mapPair_refl boolEqObs boolEqPair

theorem clean_has_section :
    ∃ s : Sec clean, IsNatural clean s :=
  ⟨cleanSection, clean_natural⟩

theorem clean_H_has_section :
    ∃ s' : HSec (H clean), HIsNatural (H clean) s' :=
  (natural_section_iff_embed clean).mp clean_has_section

end FamilyEmbedding
