import Derivation.PresentationNaturality

/-!
# Natural sections at one object: the fixed-pair criterion is an iff

`PresentationNaturality.no_natural_section_of_fixed_point_free` gives a
sufficient condition for the FAILURE of naturality over the one-object
family `autoFamily O F`: the automorphism fixes no admissible pair.  Its
contrapositive `fixed_pair_of_natural_section` is one half of an
equivalence the sealed module never states.  This module states and
proves the other half and the equivalence, then shows by two fixtures
that the invariant is "fixes an admissible pair" and not "has a fixed
point":

* `cycIso` on the sealed `card4Obs` fixes the carrier point `e1` and
  fixes no admissible pair, so it carries no natural section;
* the identity on a one-view observer fixes every carrier point and has
  no admissible pair at all, so it carries no section of any kind.

Everything here is about ONE-OBJECT families, exactly as the sealed
module's non-claims delimit.  The many-object criterion -- relative to a
declared spanning forest, a natural section exists iff the holonomy at
each root fixes a common admissible pair -- is recorded in `STATUS.md`
as the next target and is NOT proved here.  The sealed package is read
as a byte-pinned staged copy and nothing sealed is amended.
AuthorityEffect: None.
-/

namespace NaturalSections

open DiffInterface ContactKernel PresentationNaturality

variable {X R : Type}

/-! ## 1. The missing half, and the equivalence -/

/-- A fixed admissible pair gives a natural section: the constant one. -/
theorem natural_section_of_fixed_pair (O : DiffObs X R) (F : PresIso O O)
    (p : NonZeroPair O) (hp : F.mapPair p = p) :
    ∃ s : Sec (autoFamily O F), IsNatural (autoFamily O F) s :=
  ⟨fun _ => p, fun _ => hp⟩

/-- **One object: a natural section exists iff the automorphism fixes an
admissible pair.**  The forward direction is the sealed
`fixed_pair_of_natural_section`; the backward direction is the constant
section.  Over one object the whole question is this. -/
theorem natural_section_iff_fixed_pair (O : DiffObs X R) (F : PresIso O O) :
    (∃ s : Sec (autoFamily O F), IsNatural (autoFamily O F) s) ↔
      ∃ p : NonZeroPair O, F.mapPair p = p :=
  ⟨fun ⟨s, hs⟩ => fixed_pair_of_natural_section O F s hs,
   fun ⟨p, hp⟩ => natural_section_of_fixed_pair O F p hp⟩

/-- The same equivalence for the indexed family notion, through the
sealed one-object bridge `hAuto_iff_auto`. -/
theorem hnatural_section_iff_fixed_pair (O : DiffObs X R) (F : PresIso O O) :
    (∃ s : HSec (hAutoFamily O F), HIsNatural (hAutoFamily O F) s) ↔
      ∃ p : NonZeroPair O, F.mapPair p = p :=
  (hAuto_iff_auto O F).trans (natural_section_iff_fixed_pair O F)

/-- Unfolded: a fixed admissible pair is two fixed carrier points that
the observer distinguishes.  `mapPair` acts componentwise, so nothing
else could fix a pair. -/
theorem fixed_pair_iff_two_fixed_points (O : DiffObs X R) (F : PresIso O O)
    (p : NonZeroPair O) :
    F.mapPair p = p ↔
      F.car.fwd p.val.1 = p.val.1 ∧ F.car.fwd p.val.2 = p.val.2 := by
  constructor
  · intro h
    have hv : (F.car.fwd p.val.1, F.car.fwd p.val.2) = p.val :=
      congrArg Subtype.val h
    exact ⟨congrArg Prod.fst hv, congrArg Prod.snd hv⟩
  · intro h
    apply Subtype.ext
    show (F.car.fwd p.val.1, F.car.fwd p.val.2) = p.val
    rw [h.1, h.2]

/-! ## 2. A fixed point is not the invariant

Fix `e1`, cycle `e2 → e3 → e4 → e2` on the sealed four-element kernel
observer `card4Obs`.  The automorphism has a fixed point; its only fixed
pair is `(e1, e1)`, which the reflexive zero relation rules out. -/

def cyc : Card4 → Card4
  | .e1 => .e1
  | .e2 => .e3
  | .e3 => .e4
  | .e4 => .e2

def cycInv : Card4 → Card4
  | .e1 => .e1
  | .e2 => .e4
  | .e3 => .e2
  | .e4 => .e3

theorem cyc_cycInv : ∀ x, cyc (cycInv x) = x := by
  intro x; cases x <;> rfl

theorem cycInv_cyc : ∀ x, cycInv (cyc x) = x := by
  intro x; cases x <;> rfl

def cycBij : Bij Card4 Card4 where
  fwd := cyc
  bwd := cycInv
  fwd_bwd := cyc_cycInv
  bwd_fwd := cycInv_cyc

def cycPairBij : Bij (Card4 × Card4) (Card4 × Card4) where
  fwd p := (cyc p.1, cyc p.2)
  bwd p := (cycInv p.1, cycInv p.2)
  fwd_bwd p := by
    show (cyc (cycInv p.1), cyc (cycInv p.2)) = p
    rw [cyc_cycInv, cyc_cycInv]
  bwd_fwd p := by
    show (cycInv (cyc p.1), cycInv (cyc p.2)) = p
    rw [cycInv_cyc, cycInv_cyc]

/-- The 3-cycle is a presentation automorphism of the sealed `card4Obs`. -/
def cycIso : PresIso card4Obs card4Obs where
  car := cycBij
  res := cycPairBij
  delta_transport _ _ := rfl
  zero_transport r := by
    show r.1 = r.2 ↔ cyc r.1 = cyc r.2
    constructor
    · intro h; rw [h]
    · intro h; exact cycBij.fwd_injective h

theorem cyc_fixes_e1 : cyc .e1 = .e1 := rfl

theorem cyc_fixes_only_e1 : ∀ x, cyc x = x → x = .e1 := by
  intro x h
  cases x <;> first | rfl | cases h

/-- The 3-cycle fixes no admissible pair. -/
theorem cycIso_fixed_pair_free (p : NonZeroPair card4Obs) :
    cycIso.mapPair p ≠ p := by
  intro h
  have hv := (fixed_pair_iff_two_fixed_points card4Obs cycIso p).mp h
  have h1 := cyc_fixes_only_e1 p.val.1 hv.1
  have h2 := cyc_fixes_only_e1 p.val.2 hv.2
  exact p.property (show p.val.1 = p.val.2 from h1.trans h2.symm)

/-- **The separation.**  A fixed carrier point, no fixed admissible
pair, no natural section: "the automorphism has a fixed point" is not
the condition; "the automorphism fixes an admissible pair" is. -/
theorem fixed_point_without_natural_section :
    cyc .e1 = .e1 ∧
      ¬ ∃ s : Sec (autoFamily card4Obs cycIso),
          IsNatural (autoFamily card4Obs cycIso) s :=
  ⟨rfl, no_natural_section_of_fixed_point_free card4Obs cycIso cycIso_fixed_pair_free⟩

/-! ## 3. Fixed points everywhere, admissible pairs nowhere -/

/-- The observer that sees one value: its zero relation is total. -/
def blindObs : DiffObs Bool (Unit × Unit) := kernelObs (fun _ : Bool => ())

theorem blindObs_no_admissible_pair (p : NonZeroPair blindObs) : False :=
  p.property rfl

/-- The identity fixes every carrier point, and there is no section at
all, natural or not.  A fixed-point reading of the criterion would call
this a positive case; the fixed-pair reading correctly does not. -/
theorem identity_fixes_everything_no_section :
    (∀ x, (PresIso.refl blindObs).car.fwd x = x) ∧
      ¬ ∃ s : Sec (autoFamily blindObs (PresIso.refl blindObs)),
          IsNatural (autoFamily blindObs (PresIso.refl blindObs)) s :=
  ⟨fun _ => rfl, fun ⟨s, _⟩ => blindObs_no_admissible_pair (s ())⟩

end NaturalSections
